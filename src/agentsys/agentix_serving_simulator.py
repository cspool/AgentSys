from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass
from enum import Enum
from statistics import mean
from typing import Any

from .agentix import AgentixPolicy, AgentixResult, AgentixSimulator, CallSpec


class ServingMode(str, Enum):
    VLLM = "vllm"
    VLLM_OPT = "vllm_opt"
    MLFQ = "mlfq"
    AGENTIX = "agentix"


@dataclass(frozen=True, slots=True)
class ServingWorkloadConfig:
    name: str
    kind: str
    programs: int
    seed: int
    batch_size: int
    slo_cycles_per_output_token: float
    max_interarrival: int
    vllm_prefix_scale: float
    agentix_batch_efficiency: float = 1.0
    agentix_overhead_period: int = 0
    mlfq_batch_efficiency: float = 1.0
    mlfq_swap_period: int = 0
    anti_starvation_beta: float = 64.0


@dataclass(frozen=True, slots=True)
class ServingSimulationPoint:
    mode: ServingMode
    mean_interarrival: int
    offered_programs_per_kcycle: float
    mean_program_cycles_per_token: float
    p95_program_cycles_per_token: float
    completed_programs: int
    logical_output_tokens: int
    makespan: int
    calls: int
    schedule_digest: str
    anti_starvation_promotions: int

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["mode"] = self.mode.value
        return value


@dataclass(frozen=True, slots=True)
class ServingCapacityResult:
    workload: str
    mode: ServingMode
    slo_cycles_per_output_token: float
    minimum_mean_interarrival: int
    supported_programs_per_kcycle: float
    boundary_pass: ServingSimulationPoint
    boundary_fail: ServingSimulationPoint | None
    evaluated: tuple[ServingSimulationPoint, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "workload": self.workload,
            "mode": self.mode.value,
            "slo_cycles_per_output_token": self.slo_cycles_per_output_token,
            "minimum_mean_interarrival": self.minimum_mean_interarrival,
            "supported_programs_per_kcycle": self.supported_programs_per_kcycle,
            "boundary_pass": self.boundary_pass.to_dict(),
            "boundary_fail": self.boundary_fail.to_dict() if self.boundary_fail else None,
            "evaluated": [point.to_dict() for point in self.evaluated],
        }


WORKLOAD_CONFIGS = {
    "single": ServingWorkloadConfig(
        "single", "single", 40, 5, 2, 8.5, 64, 0.18,
        agentix_batch_efficiency=1.0,
        mlfq_batch_efficiency=1.0,
        mlfq_swap_period=2,
    ),
    "lats": ServingWorkloadConfig(
        "lats", "lats", 30, 7, 4, 4.7, 48, 0.25,
        agentix_batch_efficiency=2.0,
        agentix_overhead_period=3,
        mlfq_batch_efficiency=1.15,
    ),
    "mixed": ServingWorkloadConfig(
        "mixed", "mixed", 36, 11, 4, 6.15, 64, 0.18,
        agentix_batch_efficiency=2.0,
        agentix_overhead_period=6,
        mlfq_batch_efficiency=1.1,
        mlfq_swap_period=3,
    ),
}


def _duration(
    mode: ServingMode,
    decode: int,
    context: int,
    sequence: int,
    config: ServingWorkloadConfig,
) -> int:
    if mode is ServingMode.VLLM:
        # vLLM has no cross-call prefix reuse in the registered baseline.
        return decode + max(1, round(context * config.vllm_prefix_scale))
    if mode is ServingMode.AGENTIX:
        useful = max(1, math.ceil((decode + 1) / config.agentix_batch_efficiency))
        overhead = (
            1
            if config.agentix_overhead_period
            and sequence % config.agentix_overhead_period == 0
            else 0
        )
        return useful + overhead
    if mode is ServingMode.MLFQ:
        useful = max(1, math.ceil((decode + 1) / config.mlfq_batch_efficiency))
        swap = (
            1
            if config.mlfq_swap_period
            and sequence > 0
            and sequence % config.mlfq_swap_period == 0
            else 0
        )
        return useful + swap
    return decode + 1


def _arrival(rng: random.Random, previous: int, mean_interarrival: int, first: bool) -> int:
    if first:
        return 0
    return previous + max(1, round(rng.expovariate(1 / mean_interarrival)))


def _append_serial_program(
    calls: list[CallSpec],
    tokens: dict[str, int],
    rng: random.Random,
    pid: str,
    arrival: int,
    mode: ServingMode,
    config: ServingWorkloadConfig,
    *,
    long_form: bool,
) -> None:
    if config.kind == "single":
        sample = rng.random()
        call_count = (
            rng.randint(2, 3)
            if sample < 0.65
            else (rng.randint(7, 10) if sample < 0.9 else rng.randint(25, 35))
        )
        context = 6
    else:
        call_count = rng.randint(8, 14) if long_form else rng.randint(2, 4)
        context = 20 if long_form else 8
    previous: str | None = None
    output_tokens = 0
    for sequence in range(call_count):
        if config.kind == "single":
            decode = rng.randint(1, 3) if rng.random() < 0.9 else rng.randint(8, 12)
            context_step = decode + 1
        elif long_form:
            decode = rng.randint(1, 3)
            context_step = decode + 2
        else:
            decode = rng.randint(1, 5)
            context_step = decode + 1
        call_id = f"{pid}:call:{sequence}"
        calls.append(
            CallSpec(
                call_id,
                pid,
                _duration(mode, decode, context, sequence, config),
                () if previous is None else (previous,),
                arrival,
            )
        )
        previous = call_id
        context += context_step
        output_tokens += decode
    tokens[pid] = output_tokens


def _append_lats_program(
    calls: list[CallSpec],
    tokens: dict[str, int],
    rng: random.Random,
    pid: str,
    arrival: int,
    mode: ServingMode,
    config: ServingWorkloadConfig,
    *,
    mixed: bool,
) -> None:
    sample = rng.random()
    if mixed:
        branches, depth = (3, 3) if sample < 0.75 else (7, 6)
        root_context = 12
        branch_context = 15
    else:
        branches, depth = (2, 2) if sample < 0.6 else ((4, 4) if sample < 0.9 else (7, 6))
        root_context = 8
        branch_context = 10
    root_decode = rng.randint(2, 5)
    root = f"{pid}:root"
    calls.append(
        CallSpec(
            root,
            pid,
            _duration(mode, root_decode, root_context, 0, config),
            (),
            arrival,
        )
    )
    output_tokens = root_decode
    leaves: list[str] = []
    join_context = branch_context
    for branch in range(branches):
        previous = root
        context = branch_context
        for sequence in range(depth):
            decode = rng.randint(1, 4) if rng.random() < 0.9 else rng.randint(7, 10)
            call_id = f"{pid}:branch:{branch}:call:{sequence}"
            calls.append(
                CallSpec(
                    call_id,
                    pid,
                    _duration(mode, decode, context, sequence + 1, config),
                    (previous,),
                    arrival,
                    thread_id=str(branch),
                )
            )
            previous = call_id
            context += decode + 1
            output_tokens += decode
        leaves.append(previous)
        join_context = max(join_context, context)
    join_decode = 3
    calls.append(
        CallSpec(
            f"{pid}:join",
            pid,
            _duration(mode, join_decode, join_context + 10, depth + 1, config),
            tuple(leaves),
            arrival,
        )
    )
    tokens[pid] = output_tokens + join_decode


def build_serving_trace(
    config: ServingWorkloadConfig,
    mean_interarrival: int,
    mode: ServingMode | str,
    *,
    programs: int | None = None,
    all_at_zero: bool = False,
) -> tuple[tuple[CallSpec, ...], dict[str, int], dict[str, int]]:
    mode = ServingMode(mode)
    rng = random.Random(config.seed)
    calls: list[CallSpec] = []
    arrivals: dict[str, int] = {}
    tokens: dict[str, int] = {}
    arrival = 0
    count = programs or config.programs
    for index in range(count):
        arrival = 0 if all_at_zero else _arrival(rng, arrival, mean_interarrival, index == 0)
        pid = f"{config.name}:program:{index}"
        arrivals[pid] = arrival
        if config.kind == "single":
            _append_serial_program(calls, tokens, rng, pid, arrival, mode, config, long_form=False)
        elif config.kind == "lats":
            _append_lats_program(calls, tokens, rng, pid, arrival, mode, config, mixed=False)
        elif index % 3 < 2:
            _append_serial_program(
                calls,
                tokens,
                rng,
                pid,
                arrival,
                mode,
                config,
                long_form=index % 3 == 1,
            )
        else:
            _append_lats_program(calls, tokens, rng, pid, arrival, mode, config, mixed=True)
    return tuple(calls), arrivals, tokens


def _percentile(values: list[float], quantile: float) -> float:
    ordered = sorted(values)
    return ordered[max(0, math.ceil(len(ordered) * quantile) - 1)]


def _schedule_digest(result: AgentixResult) -> str:
    payload = [
        (item.start, item.lane, item.call_id, item.queue_level, item.inherited_service)
        for item in result.slices
    ]
    return hashlib.sha256(json.dumps(payload, separators=(",", ":")).encode()).hexdigest()


def simulate_serving_point(
    config: ServingWorkloadConfig,
    mode: ServingMode | str,
    mean_interarrival: int,
) -> ServingSimulationPoint:
    mode = ServingMode(mode)
    calls, arrivals, tokens = build_serving_trace(config, mean_interarrival, mode)
    policy = {
        ServingMode.VLLM: AgentixPolicy.FCFS,
        ServingMode.VLLM_OPT: AgentixPolicy.FCFS,
        ServingMode.MLFQ: AgentixPolicy.MLFQ,
        ServingMode.AGENTIX: (
            AgentixPolicy.PLAS if config.kind == "single" else AgentixPolicy.ATLAS
        ),
    }[mode]
    simulator = AgentixSimulator(
        batch_size=config.batch_size,
        queue_bounds=(0, 4, 12, 32, 80),
        queue_quanta=(2, 4, 8, 16, 32),
        anti_starvation_beta=(
            config.anti_starvation_beta if mode is ServingMode.AGENTIX else None
        ),
    )
    result = simulator.run(calls, policy)
    normalized = [
        (result.program_completion[pid] - arrivals[pid]) / tokens[pid] for pid in arrivals
    ]
    return ServingSimulationPoint(
        mode=mode,
        mean_interarrival=mean_interarrival,
        offered_programs_per_kcycle=1000.0 / mean_interarrival,
        mean_program_cycles_per_token=mean(normalized),
        p95_program_cycles_per_token=_percentile(normalized, 0.95),
        completed_programs=len(result.program_completion),
        logical_output_tokens=sum(tokens.values()),
        makespan=result.makespan,
        calls=len(calls),
        schedule_digest=_schedule_digest(result),
        anti_starvation_promotions=result.anti_starvation_promotions,
    )


def find_slo_capacity(
    config: ServingWorkloadConfig,
    mode: ServingMode | str,
) -> ServingCapacityResult:
    mode = ServingMode(mode)
    cache: dict[int, ServingSimulationPoint] = {}

    def evaluate(interarrival: int) -> ServingSimulationPoint:
        if interarrival not in cache:
            cache[interarrival] = simulate_serving_point(config, mode, interarrival)
        return cache[interarrival]

    low, high = 1, config.max_interarrival
    if evaluate(high).mean_program_cycles_per_token > config.slo_cycles_per_output_token:
        raise RuntimeError(f"{config.name}/{mode.value} never reaches the registered SLO")
    while low < high:
        middle = (low + high) // 2
        if evaluate(middle).mean_program_cycles_per_token <= config.slo_cycles_per_output_token:
            high = middle
        else:
            low = middle + 1
    candidate = low
    # Integer/exponential trace rounding can introduce a one-point ripple.
    # Audit the local boundary explicitly and select the first passing point.
    for value in range(max(1, candidate - 2), min(config.max_interarrival, candidate + 2) + 1):
        evaluate(value)
    passing = sorted(
        value
        for value, point in cache.items()
        if point.mean_program_cycles_per_token <= config.slo_cycles_per_output_token
    )
    candidate = min(value for value in passing if value >= max(1, low - 2))
    boundary_fail = evaluate(candidate - 1) if candidate > 1 else None
    if boundary_fail is not None and boundary_fail.mean_program_cycles_per_token <= config.slo_cycles_per_output_token:
        raise AssertionError("capacity boundary is not fail/pass ordered")
    return ServingCapacityResult(
        workload=config.name,
        mode=mode,
        slo_cycles_per_output_token=config.slo_cycles_per_output_token,
        minimum_mean_interarrival=candidate,
        supported_programs_per_kcycle=1000.0 / candidate,
        boundary_pass=evaluate(candidate),
        boundary_fail=boundary_fail,
        evaluated=tuple(cache[key] for key in sorted(cache)),
    )


def run_capacity_experiment(
    config: ServingWorkloadConfig,
) -> dict[str, ServingCapacityResult]:
    return {mode.value: find_slo_capacity(config, mode) for mode in ServingMode}


def _swap_cost(
    result: AgentixResult,
    *,
    cache_programs: int,
    blocks_per_program: int,
    block_cycles: int,
    dma_setup_cycles: int,
    bulk: bool,
    multi_step: int,
) -> tuple[int, int]:
    resident: list[str] = []
    swaps = 0
    cycles = 0
    batches: dict[int, list[str]] = {}
    for item in result.slices:
        if item.start % multi_step != 0:
            continue
        batches.setdefault(item.start, []).append(item.program_id)
    for timestamp in sorted(batches):
        for program_id in dict.fromkeys(batches[timestamp]):
            if program_id in resident:
                resident.remove(program_id)
                resident.append(program_id)
                continue
            swaps += 1
            if len(resident) >= cache_programs:
                resident.pop(0)
            resident.append(program_id)
            cycles += (
                dma_setup_cycles + blocks_per_program * block_cycles
                if bulk
                else blocks_per_program * (dma_setup_cycles + block_cycles)
            )
    return swaps, cycles


def simulate_offline_batch(programs: int) -> dict[str, Any]:
    if programs not in {1000, 2000, 3000, 4000}:
        raise ValueError("offline Agentix experiment supports 1000/2000/3000/4000 programs")
    representative_programs = programs // 100
    config = WORKLOAD_CONFIGS["single"]
    baseline_calls, _, _ = build_serving_trace(
        config, 1, ServingMode.VLLM_OPT, programs=representative_programs, all_at_zero=True
    )
    agentix_calls, _, _ = build_serving_trace(
        config, 1, ServingMode.AGENTIX, programs=representative_programs, all_at_zero=True
    )
    simulator = AgentixSimulator(
        batch_size=config.batch_size,
        queue_bounds=(0, 4, 12, 32, 80),
        queue_quanta=(2, 4, 8, 16, 32),
    )
    baseline = simulator.run(baseline_calls, AgentixPolicy.FCFS)
    agentix = simulator.run(agentix_calls, AgentixPolicy.PLAS)
    cache_programs = 6
    blocks = 4
    baseline_swaps, baseline_swap_cycles = _swap_cost(
        baseline,
        cache_programs=cache_programs,
        blocks_per_program=blocks,
        block_cycles=1,
        dma_setup_cycles=1,
        bulk=False,
        multi_step=1,
    )
    agentix_swaps, agentix_swap_cycles = _swap_cost(
        agentix,
        cache_programs=cache_programs,
        blocks_per_program=blocks,
        block_cycles=1,
        dma_setup_cycles=1,
        bulk=True,
        multi_step=2,
    )
    baseline_cycles = baseline.makespan + baseline_swap_cycles
    agentix_cycles = agentix.makespan + agentix_swap_cycles
    return {
        "programs": programs,
        "representative_programs": representative_programs,
        "population_scale": 100,
        "baseline": {
            "scheduler_cycles": baseline.makespan,
            "swaps": baseline_swaps,
            "swap_cycles": baseline_swap_cycles,
            "cycles": baseline_cycles,
        },
        "agentix": {
            "scheduler_cycles": agentix.makespan,
            "swaps": agentix_swaps,
            "swap_cycles": agentix_swap_cycles,
            "cycles": agentix_cycles,
        },
        "reduction": 1.0 - agentix_cycles / baseline_cycles,
    }

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from enum import Enum
from statistics import mean
from typing import Iterable

from .model import FlowKind, FlowSpec, Priority


class XPUmode(str, Enum):
    IGPU = "igpu"
    SERIAL = "serial_npu_igpu"
    HEG = "heg"


@dataclass(frozen=True, slots=True)
class XPUConfig:
    tick_s: float = 0.002
    baseline_prefill_chunk_tokens: int = 2048
    heg_prefill_chunk_tokens: int = 16
    igpu_prefill_tokens_s: float = 140.0
    serial_prefill_tokens_s: float = 112.0
    heg_prefill_tokens_s: float = 190.0
    igpu_decode_tokens_s: float = 31.0
    heg_decode_tokens_s: float = 31.0
    max_decode_batch: int = 16
    max_reactive_decode_batch: int = 3
    decode_batch_cost: float = 0.12
    warmup_s: float = 0.060
    preemption_overhead_s: float = 0.004
    mixed_gemv_slowdown: float = 1.59
    heg_igpu_prefill_share: float = 0.50
    igpu_power_w_prefill: float = 31.0
    igpu_power_w_decode: float = 25.0
    npu_power_w: float = 10.0
    cpu_npu_control_power_w: float = 12.0
    igpu_prefill_active_utilization: float = 1.0
    igpu_decode_active_utilization: float = 0.46
    heg_prefill_active_utilization: float = 0.80

    def __post_init__(self) -> None:
        if self.tick_s <= 0:
            raise ValueError("tick must be positive")
        if self.baseline_prefill_chunk_tokens <= 0 or self.heg_prefill_chunk_tokens <= 0:
            raise ValueError("prefill chunks must be positive")
        if self.max_decode_batch <= 0 or self.max_reactive_decode_batch <= 0:
            raise ValueError("batch sizes must be positive")
        if self.mixed_gemv_slowdown < 1.0:
            raise ValueError("mixed GEMV slowdown cannot be below one")
        if not 0.0 <= self.heg_igpu_prefill_share <= 1.0:
            raise ValueError("HEG iGPU prefill share must be in [0, 1]")


@dataclass(slots=True)
class _FlowState:
    spec: FlowSpec
    prefill_remaining: int
    decode_remaining: int
    first_prefill_start: float | None = None
    prefill_complete: float | None = None
    complete: float | None = None


@dataclass(slots=True)
class _Operation:
    kind: str
    flow_ids: tuple[str, ...]
    remaining_s: float
    started: float
    tokens: int


@dataclass(frozen=True, slots=True)
class AgentXPUResult:
    mode: XPUmode
    completed: int
    horizon_s: float
    throughput_req_s: float
    normalized_latency_s_token: float
    mean_latency_s: float
    reactive_mean_latency_s: float | None
    reactive_p90_latency_s: float | None
    proactive_mean_latency_s: float | None
    reactive_prefill_pending_s: float | None
    igpu_utilization: float
    igpu_wall_occupancy: float
    npu_utilization: float
    energy_j_token: float
    cpu_control_energy_j: float
    preemptions: int
    logical_input_tokens: int
    logical_output_tokens: int
    flow_latency_s: dict[str, float]

    def to_dict(self) -> dict[str, object]:
        return {
            "mode": self.mode.value,
            "completed": self.completed,
            "horizon_s": self.horizon_s,
            "throughput_req_s": self.throughput_req_s,
            "normalized_latency_s_token": self.normalized_latency_s_token,
            "mean_latency_s": self.mean_latency_s,
            "reactive_mean_latency_s": self.reactive_mean_latency_s,
            "reactive_p90_latency_s": self.reactive_p90_latency_s,
            "proactive_mean_latency_s": self.proactive_mean_latency_s,
            "reactive_prefill_pending_s": self.reactive_prefill_pending_s,
            "igpu_utilization": self.igpu_utilization,
            "igpu_wall_occupancy": self.igpu_wall_occupancy,
            "npu_utilization": self.npu_utilization,
            "energy_j_token": self.energy_j_token,
            "cpu_control_energy_j": self.cpu_control_energy_j,
            "preemptions": self.preemptions,
            "logical_input_tokens": self.logical_input_tokens,
            "logical_output_tokens": self.logical_output_tokens,
            "flow_latency_s": self.flow_latency_s,
        }


def _percentile(values: list[float], quantile: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = max(0, math.ceil(quantile * len(ordered)) - 1)
    return ordered[index]


class AgentXPUSimulator:
    """Stage-elastic flow simulator grounded in the public LLM.xpu behavior.

    IGPU/SERIAL serialize chunked prefill and decode on the graphics engine.
    HEG sends chunked prefill to an independent NPU pipeline while the iGPU
    performs adaptive batched decode. Reactive-first selection happens only at
    chunk/token boundaries, representing the paper's fine-grained preemption.
    """

    def __init__(self, config: XPUConfig | None = None) -> None:
        self.config = config or XPUConfig()

    @staticmethod
    def _validate(flows: tuple[FlowSpec, ...]) -> None:
        ids = [flow.flow_id for flow in flows]
        if len(ids) != len(set(ids)):
            raise ValueError("flow ids must be unique")
        if tuple(sorted(flow.arrival for flow in flows)) != tuple(flow.arrival for flow in flows):
            raise ValueError("flows must be sorted by arrival")

    def run(
        self,
        flows: Iterable[FlowSpec],
        mode: XPUmode | str,
        *,
        drain: bool = True,
    ) -> AgentXPUResult:
        mode = XPUmode(mode)
        specs = tuple(flows)
        self._validate(specs)
        cfg = self.config
        states = {
            flow.flow_id: _FlowState(flow, flow.input_tokens, flow.output_tokens) for flow in specs
        }
        prefill_queue: list[str] = []
        decode_queue: list[str] = []
        igpu_op: _Operation | None = None
        npu_op: _Operation | None = None
        arrival_index = 0
        time = 0.0
        igpu_prefill_busy = 0.0
        igpu_decode_busy = 0.0
        npu_busy = 0.0
        heg_igpu_prefill_busy = 0.0
        preemptions = 0
        previous_prefill_kind: FlowKind | None = None
        max_arrival = specs[-1].arrival if specs else 0.0
        total_service_upper = sum(
            flow.input_tokens / min(cfg.igpu_prefill_tokens_s, cfg.serial_prefill_tokens_s)
            + flow.output_tokens / cfg.igpu_decode_tokens_s
            for flow in specs
        )
        max_time = max_arrival + total_service_upper * 2.5 + 60.0
        flow_kinds = {flow.kind for flow in specs}
        mixed_priorities = FlowKind.REACTIVE in flow_kinds and FlowKind.PROACTIVE in flow_kinds

        def choose_prefill() -> tuple[str, bool] | None:
            nonlocal preemptions, previous_prefill_kind
            if not prefill_queue:
                return None
            if mode is XPUmode.HEG:
                index = min(
                    range(len(prefill_queue)),
                    key=lambda pos: (
                        int(states[prefill_queue[pos]].spec.priority),
                        states[prefill_queue[pos]].spec.arrival,
                        pos,
                    ),
                )
            else:
                index = min(
                    range(len(prefill_queue)),
                    key=lambda pos: (states[prefill_queue[pos]].spec.arrival, pos),
                )
            flow_id = prefill_queue.pop(index)
            kind = states[flow_id].spec.kind
            preempted = (
                mode is XPUmode.HEG
                and previous_prefill_kind is FlowKind.PROACTIVE
                and kind is FlowKind.REACTIVE
            )
            if preempted:
                preemptions += 1
            previous_prefill_kind = kind
            return flow_id, preempted

        def make_prefill_op(flow_id: str, now: float, preempted: bool) -> _Operation:
            state = states[flow_id]
            if mode is XPUmode.HEG:
                rate = cfg.heg_prefill_tokens_s
                chunk_tokens = cfg.heg_prefill_chunk_tokens
            elif mode is XPUmode.SERIAL:
                rate = cfg.serial_prefill_tokens_s
                chunk_tokens = cfg.baseline_prefill_chunk_tokens
            else:
                rate = cfg.igpu_prefill_tokens_s
                chunk_tokens = cfg.baseline_prefill_chunk_tokens
            tokens = min(chunk_tokens, state.prefill_remaining)
            overhead = cfg.preemption_overhead_s if preempted else 0.0
            if state.first_prefill_start is None:
                state.first_prefill_start = now + overhead
            return _Operation("prefill", (flow_id,), tokens / rate + overhead, now, tokens)

        def choose_decode_batch() -> tuple[str, ...]:
            if not decode_queue:
                return ()
            unique = list(dict.fromkeys(decode_queue))
            if mode is XPUmode.HEG:
                reactive = [
                    flow_id
                    for flow_id in unique
                    if states[flow_id].spec.kind is FlowKind.REACTIVE
                ]
                proactive = [
                    flow_id
                    for flow_id in unique
                    if states[flow_id].spec.kind is FlowKind.PROACTIVE
                ]
                if reactive:
                    cap = cfg.max_reactive_decode_batch
                    selected = reactive[:cap]
                    selected += proactive[: max(0, cap - len(selected))]
                else:
                    selected = proactive[: cfg.max_decode_batch]
            else:
                selected = unique[: cfg.max_decode_batch]
            selected_set = set(selected)
            decode_queue[:] = [flow_id for flow_id in decode_queue if flow_id not in selected_set]
            return tuple(selected)

        def make_decode_op(batch: tuple[str, ...], now: float) -> _Operation:
            rate = cfg.heg_decode_tokens_s if mode is XPUmode.HEG else cfg.igpu_decode_tokens_s
            batch_cost = 1.0 + cfg.decode_batch_cost * max(0, len(batch) - 1)
            if mode is XPUmode.IGPU and mixed_priorities and prefill_queue:
                # Figure 4: shared-DDR co-execution primarily hurts the
                # memory-bound GEMV/decode side; use the single published
                # maximum slowdown for every mixed-flow configuration.
                batch_cost *= cfg.mixed_gemv_slowdown
            return _Operation("decode", batch, batch_cost / rate, now, len(batch))

        def finish_op(op: _Operation, now: float) -> None:
            if op.kind == "prefill":
                state = states[op.flow_ids[0]]
                state.prefill_remaining -= op.tokens
                if state.prefill_remaining == 0:
                    state.prefill_complete = now
                    decode_queue.append(state.spec.flow_id)
                else:
                    prefill_queue.append(state.spec.flow_id)
            else:
                for flow_id in op.flow_ids:
                    state = states[flow_id]
                    state.decode_remaining -= 1
                    if state.decode_remaining == 0:
                        state.complete = now
                    else:
                        decode_queue.append(flow_id)

        while True:
            while arrival_index < len(specs) and specs[arrival_index].arrival <= time + 1e-12:
                prefill_queue.append(specs[arrival_index].flow_id)
                arrival_index += 1

            if igpu_op is not None:
                step = min(cfg.tick_s, igpu_op.remaining_s)
                igpu_op.remaining_s -= step
                if igpu_op.kind == "prefill":
                    igpu_prefill_busy += step
                else:
                    igpu_decode_busy += step
                if igpu_op.remaining_s <= 1e-12:
                    finish_op(igpu_op, time + step)
                    igpu_op = None

            if npu_op is not None:
                step = min(cfg.tick_s, npu_op.remaining_s)
                npu_op.remaining_s -= step
                npu_busy += step
                heg_igpu_prefill_busy += step * cfg.heg_igpu_prefill_share
                if npu_op.remaining_s <= 1e-12:
                    finish_op(npu_op, time + step)
                    npu_op = None

            if mode is XPUmode.HEG:
                if npu_op is None:
                    selected = choose_prefill()
                    if selected is not None:
                        npu_op = make_prefill_op(selected[0], time, selected[1])
                if igpu_op is None:
                    batch = choose_decode_batch()
                    if batch:
                        igpu_op = make_decode_op(batch, time)
            elif igpu_op is None:
                # Decode is revisited at every token boundary; prefills are
                # chunked so neither stage monopolizes the serving engine.
                batch = choose_decode_batch()
                if batch:
                    igpu_op = make_decode_op(batch, time)
                else:
                    selected = choose_prefill()
                    if selected is not None:
                        igpu_op = make_prefill_op(selected[0], time, selected[1])

            finished = sum(state.complete is not None for state in states.values())
            no_live_work = (
                arrival_index == len(specs)
                and not prefill_queue
                and not decode_queue
                and igpu_op is None
                and npu_op is None
            )
            if no_live_work:
                break
            if not drain and time >= max_arrival:
                break
            time += cfg.tick_s
            if time > max_time:
                raise RuntimeError("Agent.xpu simulation exceeded progress bound")

        completed_states = [state for state in states.values() if state.complete is not None]
        latencies = {
            state.spec.flow_id: (state.complete or 0.0) - state.spec.arrival for state in completed_states
        }
        reactive_states = [
            state for state in completed_states if state.spec.kind is FlowKind.REACTIVE
        ]
        proactive_states = [
            state for state in completed_states if state.spec.kind is FlowKind.PROACTIVE
        ]
        reactive_latencies = [latencies[state.spec.flow_id] for state in reactive_states]
        proactive_latencies = [latencies[state.spec.flow_id] for state in proactive_states]
        pending = [
            (state.first_prefill_start or state.spec.arrival) - state.spec.arrival
            for state in reactive_states
        ]
        total_tokens = sum(
            state.spec.input_tokens + state.spec.output_tokens for state in completed_states
        )
        total_output = sum(state.spec.output_tokens for state in completed_states)
        horizon = max((state.complete or 0.0 for state in completed_states), default=time)
        cpu_control_energy = (
            npu_busy * cfg.cpu_npu_control_power_w if mode is XPUmode.HEG else 0.0
        )
        energy = (
            (igpu_prefill_busy + heg_igpu_prefill_busy) * cfg.igpu_power_w_prefill
            + igpu_decode_busy * cfg.igpu_power_w_decode
            + npu_busy * cfg.npu_power_w
            + cpu_control_energy
        )
        igpu_wall_occupancy = (
            (igpu_prefill_busy + igpu_decode_busy + heg_igpu_prefill_busy) / horizon
            if horizon
            else 0.0
        )
        if mode is XPUmode.HEG:
            active_period = npu_busy + igpu_decode_busy
            active_utilization = (
                npu_busy
                * cfg.heg_igpu_prefill_share
                * cfg.heg_prefill_active_utilization
                + igpu_decode_busy * cfg.igpu_decode_active_utilization
            ) / active_period if active_period else 0.0
        else:
            active_period = igpu_prefill_busy + igpu_decode_busy
            active_utilization = (
                igpu_prefill_busy * cfg.igpu_prefill_active_utilization
                + igpu_decode_busy * cfg.igpu_decode_active_utilization
            ) / active_period if active_period else 0.0
        mean_latency = mean(latencies.values()) if latencies else 0.0
        return AgentXPUResult(
            mode=mode,
            completed=len(completed_states),
            horizon_s=horizon,
            throughput_req_s=len(completed_states) / horizon if horizon else 0.0,
            normalized_latency_s_token=mean_latency / (total_tokens / len(completed_states))
            if completed_states and total_tokens
            else 0.0,
            mean_latency_s=mean_latency,
            reactive_mean_latency_s=mean(reactive_latencies) if reactive_latencies else None,
            reactive_p90_latency_s=_percentile(reactive_latencies, 0.90),
            proactive_mean_latency_s=mean(proactive_latencies) if proactive_latencies else None,
            reactive_prefill_pending_s=mean(pending) if pending else None,
            igpu_utilization=active_utilization,
            igpu_wall_occupancy=igpu_wall_occupancy,
            npu_utilization=npu_busy / horizon if horizon else 0.0,
            energy_j_token=energy / total_tokens if total_tokens else 0.0,
            cpu_control_energy_j=cpu_control_energy,
            preemptions=preemptions,
            logical_input_tokens=sum(state.spec.input_tokens for state in completed_states),
            logical_output_tokens=total_output,
            flow_latency_s=latencies,
        )


def poisson_mixed_flows(
    *,
    duration_s: float = 900.0,
    proactive_rate_min: float = 6.0,
    reactive_rate_min: float = 3.0,
    model_scale: float = 1.0,
    seed: int = 2025,
) -> tuple[FlowSpec, ...]:
    """Generate paper-shaped mixed flows with independent Poisson arrivals."""

    if duration_s <= 0 or proactive_rate_min < 0 or reactive_rate_min < 0:
        raise ValueError("invalid workload duration or rate")
    rng = random.Random(seed)
    flows: list[FlowSpec] = []

    def generate(kind: FlowKind, rate_min: float, input_mean: float, output_mean: float) -> None:
        if rate_min == 0:
            return
        arrival = rng.expovariate(rate_min / 60.0)
        index = 0
        while arrival < duration_s:
            # Log-normal-like positive variation without a third-party package.
            input_tokens = max(8, round(input_mean * model_scale * rng.uniform(0.65, 1.35)))
            output_tokens = max(4, round(output_mean * model_scale * rng.uniform(0.60, 1.40)))
            prefix = "r" if kind is FlowKind.REACTIVE else "p"
            priority = Priority.REACTIVE if kind is FlowKind.REACTIVE else Priority.PROACTIVE
            flows.append(
                FlowSpec(
                    flow_id=f"{prefix}{index}",
                    call_id=f"{prefix}-call{index}",
                    program_id=f"{prefix}-program{index}",
                    kind=kind,
                    priority=priority,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    arrival=arrival,
                )
            )
            index += 1
            arrival += rng.expovariate(rate_min / 60.0)

    generate(FlowKind.PROACTIVE, proactive_rate_min, 434.9, 81.3)
    generate(FlowKind.REACTIVE, reactive_rate_min, 213.0, 69.7)
    flows.sort(key=lambda flow: (flow.arrival, flow.flow_id))
    return tuple(flows)

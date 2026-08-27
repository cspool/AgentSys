from __future__ import annotations

import hashlib
import heapq
import json
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Iterable

from .mllm_backend import MLLM_ROOT, MllmOperator, operator_digest, parse_mir


PROJECT_ROOT = Path(__file__).resolve().parents[2]
QWEN_MIR = MLLM_ROOT / "examples/qwen3_qnn_aot/qwen3_qnn_aot_1.7B.mir"
QWEN_CONFIG = MLLM_ROOT / "examples/qwen3_qnn_aot/config_1.7B.json"
PAPER_TARGETS = PROJECT_ROOT / "data" / "paper_targets.json"


class Processor(str, Enum):
    CPU = "cpu"
    NPU = "npu"


@dataclass(frozen=True, slots=True)
class LlmNpuConfig:
    # The released QNN-AOT MIR is a 32-token graph. The paper's Figure 7 also
    # illustrates chunk length 32, while the product default is 256.
    prompt_tokens: int = 1024
    chunk_tokens: int = 32
    graph_ablation_prompt_tokens: int = 512
    # Paper section 3.4: Qwen1.5-1.8B, 256-token prompt, NPU 315 ms and
    # approximately twice the CPU time.
    profile_prompt_tokens: int = 256
    npu_profile_us: float = 315_000.0
    cpu_to_npu_time_ratio: float = 0.5
    # "Microsecond-level" online heuristic. Three microseconds is applied per
    # NPU subgraph dispatch; it is not read from the endpoint target file.
    scheduler_overhead_us: float = 3.0
    # Figure 4 reports 8.1--10.7x overhead for group quantization.
    per_group_overhead_low: float = 8.1
    per_group_overhead_high: float = 10.7
    # Figures 10--12 and section 4: 0.1--0.3% outlier channels, 85% pruning.
    outlier_channel_fraction: float = 0.002
    outlier_layer_pruning: float = 0.85
    hot_channel_fraction: float = 0.03
    # QNN graph preparation for Qwen1.5-1.8B in Figure 2.
    graph_create_ms: float = 450.0
    graph_optimize_ms: float = 3300.0

    def validate(self) -> None:
        if self.prompt_tokens <= 0 or self.chunk_tokens <= 0:
            raise ValueError("prompt/chunk tokens must be positive")
        if self.prompt_tokens % self.chunk_tokens:
            raise ValueError("prompt must contain an integral number of chunks")
        if self.graph_ablation_prompt_tokens % self.chunk_tokens:
            raise ValueError("graph ablation prompt must contain integral chunks")
        if self.profile_prompt_tokens % self.chunk_tokens:
            raise ValueError("profile prompt must contain integral chunks")
        if not 0.0 <= self.outlier_layer_pruning < 1.0:
            raise ValueError("outlier pruning must be in [0, 1)")


@dataclass(frozen=True, slots=True)
class Subgraph:
    task_id: str
    chunk: int
    layer: int
    stage: int
    kind: str
    processor: Processor
    duration_us: float
    deps: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ScheduleEvent:
    task_id: str
    chunk: int
    layer: int
    stage: int
    kind: str
    processor: str
    ready_us: float
    start_us: float
    end_us: float
    dispatch_overhead_us: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "chunk": self.chunk,
            "layer": self.layer,
            "stage": self.stage,
            "kind": self.kind,
            "processor": self.processor,
            "ready_us": self.ready_us,
            "start_us": self.start_us,
            "end_us": self.end_us,
            "dispatch_overhead_us": self.dispatch_overhead_us,
        }


@dataclass(frozen=True, slots=True)
class ScheduleResult:
    mode: str
    makespan_us: float
    busy_us: dict[str, float]
    bubble_rate: dict[str, float]
    dispatch_overhead_us: float
    completed: int
    dependency_checks: int
    events: tuple[ScheduleEvent, ...]

    def summary(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "makespan_us": self.makespan_us,
            "busy_us": self.busy_us,
            "bubble_rate": self.bubble_rate,
            "dispatch_overhead_us": self.dispatch_overhead_us,
            "completed": self.completed,
            "dependency_checks": self.dependency_checks,
            "event_count": len(self.events),
        }


STATIC_SHAREABLE_OPS = {
    "LinearOp",
    "RMSNormOp",
    "AddOp",
    "MulOp",
    "SigmoidOp",
    "NegOp",
    "CastTypeOp",
}


def native_graph_contract() -> dict[str, Any]:
    raw_config = json.loads(QWEN_CONFIG.read_text(encoding="utf-8"))
    layers = int(raw_config["num_hidden_layers"])
    operators = parse_mir(QWEN_MIR)
    if len(operators) < 63:
        raise ValueError("native mllm graph is too short to contain a decoder block")
    # Operations 6..62 are the first complete decoder block at the pinned
    # revision. Their types and shapes, rather than paper endpoints, determine
    # which graph fragments can be shared.
    block = tuple(operators[6:63])
    embedding_outputs = operators[0].outputs
    if not embedding_outputs or len(embedding_outputs[0].shape) < 2:
        raise ValueError("native mllm embedding does not expose a sequence dimension")
    chunk_tokens = embedding_outputs[0].shape[1]
    static_count = sum(operator.op_type in STATIC_SHAREABLE_OPS for operator in block)
    return {
        "layers": layers,
        "chunk_tokens": chunk_tokens,
        "operator_count": len(operators),
        "block_operator_count": len(block),
        "static_operator_count": static_count,
        "dynamic_operator_count": len(block) - static_count,
        "static_fraction": static_count / len(block),
        "operator_digest": operator_digest(operators),
        "block_digest": operator_digest(block),
    }


def chunk_sharing_experiment(config: LlmNpuConfig, graph: dict[str, Any]) -> dict[str, Any]:
    chunks = config.graph_ablation_prompt_tokens // config.chunk_tokens
    static_fraction = float(graph["static_fraction"])
    dynamic_fraction = 1.0 - static_fraction
    graph_prep_ms = config.graph_create_ms + config.graph_optimize_ms
    naive_ms = chunks * graph_prep_ms
    shared_ms = static_fraction * graph_prep_ms + chunks * dynamic_fraction * graph_prep_ms
    return {
        "prompt_tokens": config.graph_ablation_prompt_tokens,
        "chunk_tokens": config.chunk_tokens,
        "chunks": chunks,
        "static_fraction_from_native_mir": static_fraction,
        "dynamic_fraction_from_native_mir": dynamic_fraction,
        "naive_graph_preparation_ms": naive_ms,
        "chunk_sharing_graph_preparation_ms": shared_ms,
        "speedup": naive_ms / shared_ms,
        "static_graph_instances": 1,
        "dynamic_graph_instances": chunks,
        "causal_kv_edges": chunks - 1,
    }


def shadow_outlier_experiment(config: LlmNpuConfig) -> dict[str, Any]:
    npu_us = config.npu_profile_us
    cpu_us = npu_us * config.cpu_to_npu_time_ratio
    group_overhead = (config.per_group_overhead_low + config.per_group_overhead_high) / 2.0
    per_group_us = npu_us * group_overhead + cpu_us
    active_outlier_fraction = config.outlier_channel_fraction * (1.0 - config.outlier_layer_pruning)
    shadow_cpu_us = npu_us * active_outlier_fraction
    # Section 3.3 states that sparse shadow work is fully hidden by original
    # NPU MatMul execution. Essential CPU float work remains in the base path.
    per_tensor_shadow_us = npu_us + cpu_us + max(0.0, shadow_cpu_us - npu_us)
    return {
        "per_group_overhead": group_overhead,
        "baseline_per_group_us": per_group_us,
        "per_tensor_shadow_us": per_tensor_shadow_us,
        "speedup": per_group_us / per_tensor_shadow_us,
        "outlier_channel_fraction": config.outlier_channel_fraction,
        "pruned_layer_fraction": config.outlier_layer_pruning,
        "active_outlier_fraction": active_outlier_fraction,
        "shadow_cpu_us": shadow_cpu_us,
        "shadow_fully_hidden": shadow_cpu_us < npu_us,
        "hot_channel_weight_fraction": config.hot_channel_fraction,
    }


def _task_id(chunk: int, layer: int, stage: int) -> str:
    return f"c{chunk:02d}.l{layer:02d}.g{stage}"


def build_subgraphs(config: LlmNpuConfig, *, layers: int) -> tuple[Subgraph, ...]:
    config.validate()
    chunks = config.prompt_tokens // config.chunk_tokens
    profile_chunks = config.profile_prompt_tokens // config.chunk_tokens
    npu_per_chunk_us = config.npu_profile_us / profile_chunks
    cpu_per_chunk_us = npu_per_chunk_us * config.cpu_to_npu_time_ratio
    # Figure 5 partitions each decoder block into QKV, attention, output,
    # normalization/shadow, and FFN subgraphs. Fractions are fixed structural
    # weights and sum independently to the profiled CPU/NPU totals.
    stages = (
        ("qkv_int8", Processor.NPU, npu_per_chunk_us * 0.35 / layers),
        ("attention_fp", Processor.CPU, cpu_per_chunk_us * 0.60 / layers),
        ("output_int8", Processor.NPU, npu_per_chunk_us * 0.20 / layers),
        ("norm_shadow_fp", Processor.CPU, cpu_per_chunk_us * 0.40 / layers),
        ("ffn_int8", Processor.NPU, npu_per_chunk_us * 0.45 / layers),
    )
    tasks: list[Subgraph] = []
    for chunk in range(chunks):
        previous: str | None = None
        for layer in range(layers):
            for stage, (kind, processor, duration_us) in enumerate(stages):
                deps: set[str] = set()
                if previous is not None:
                    deps.add(previous)
                # Paper Eq. 2: the attention subgraph of chunk i waits for the
                # preceding QKV subgraph of every earlier causal chunk.
                if stage == 1:
                    deps.update(_task_id(earlier, layer, 0) for earlier in range(chunk))
                task_id = _task_id(chunk, layer, stage)
                tasks.append(
                    Subgraph(
                        task_id=task_id,
                        chunk=chunk,
                        layer=layer,
                        stage=stage,
                        kind=kind,
                        processor=processor,
                        duration_us=duration_us,
                        deps=tuple(sorted(deps)),
                    )
                )
                previous = task_id
    return tuple(tasks)


def _contribution(
    task: Subgraph,
    *,
    successors: dict[str, list[str]],
    by_id: dict[str, Subgraph],
) -> float:
    # Operationalize the paper's stall-contribution heuristic. CPU work is
    # prioritized by the NPU work it releases. For an NPU candidate, feeding
    # the longer ready CPU subgraph first prevents that CPU path from becoming
    # the subsequent NPU stall source.
    opposite = Processor.NPU if task.processor is Processor.CPU else Processor.CPU
    return sum(
        by_id[successor].duration_us
        for successor in successors[task.task_id]
        if by_id[successor].processor is opposite
    )


def schedule_subgraphs(
    tasks: Iterable[Subgraph],
    *,
    mode: str,
    scheduler_overhead_us: float = 0.0,
) -> ScheduleResult:
    if mode not in {"naive", "out_of_order"}:
        raise ValueError(f"unknown schedule mode: {mode}")
    tasks = tuple(tasks)
    by_id = {task.task_id: task for task in tasks}
    if len(by_id) != len(tasks):
        raise ValueError("duplicate subgraph id")
    successors: dict[str, list[str]] = defaultdict(list)
    for task in tasks:
        for dep in task.deps:
            if dep not in by_id:
                raise ValueError(f"missing dependency {dep}")
            successors[dep].append(task.task_id)

    ready: dict[Processor, set[str]] = {Processor.CPU: set(), Processor.NPU: set()}
    ready_at: dict[str, float] = {}
    for task in tasks:
        if not task.deps:
            ready[task.processor].add(task.task_id)
            ready_at[task.task_id] = 0.0

    now = 0.0
    completed: set[str] = set()
    completed_at: dict[str, float] = {}
    running: dict[Processor, str] = {}
    finish_heap: list[tuple[float, str, str, float, float]] = []
    busy = {Processor.CPU: 0.0, Processor.NPU: 0.0}
    total_dispatch_overhead = 0.0
    events: list[ScheduleEvent] = []

    while len(completed) < len(tasks):
        for processor in (Processor.CPU, Processor.NPU):
            if processor in running:
                continue
            candidates = ready[processor]
            if mode == "naive" and candidates:
                active_chunk = min(task.chunk for task in tasks if task.task_id not in completed)
                candidates = {
                    task_id for task_id in candidates if by_id[task_id].chunk == active_chunk
                }
            if not candidates:
                continue
            if mode == "naive":
                task_id = min(
                    candidates,
                    key=lambda item: (
                        by_id[item].chunk,
                        by_id[item].layer,
                        by_id[item].stage,
                    ),
                )
            else:
                task_id = max(
                    candidates,
                    key=lambda item: (
                        _contribution(by_id[item], successors=successors, by_id=by_id),
                        -by_id[item].layer,
                        -by_id[item].stage,
                        -by_id[item].chunk,
                    ),
                )
            ready[processor].remove(task_id)
            task = by_id[task_id]
            overhead = (
                scheduler_overhead_us
                if mode == "out_of_order" and processor is Processor.NPU
                else 0.0
            )
            start_us = now + overhead
            end_us = start_us + task.duration_us
            total_dispatch_overhead += overhead
            busy[processor] += task.duration_us
            running[processor] = task_id
            heapq.heappush(
                finish_heap,
                (end_us, processor.value, task_id, start_us, overhead),
            )

        if not finish_heap:
            unresolved = sorted(set(by_id) - completed)
            raise RuntimeError(f"subgraph dependency deadlock: {unresolved[:5]}")

        now = finish_heap[0][0]
        finished: list[tuple[float, str, str, float, float]] = []
        while finish_heap and abs(finish_heap[0][0] - now) < 1e-9:
            finished.append(heapq.heappop(finish_heap))

        for end_us, processor_name, task_id, start_us, overhead in finished:
            task = by_id[task_id]
            processor = Processor(processor_name)
            running.pop(processor)
            completed.add(task_id)
            completed_at[task_id] = end_us
            events.append(
                ScheduleEvent(
                    task_id=task_id,
                    chunk=task.chunk,
                    layer=task.layer,
                    stage=task.stage,
                    kind=task.kind,
                    processor=processor.value,
                    ready_us=ready_at[task_id],
                    start_us=start_us,
                    end_us=end_us,
                    dispatch_overhead_us=overhead,
                )
            )

        for _, _, task_id, _, _ in finished:
            for successor_id in successors[task_id]:
                successor = by_id[successor_id]
                if successor_id in completed or successor_id in running.values():
                    continue
                if all(dep in completed for dep in successor.deps):
                    ready[successor.processor].add(successor_id)
                    ready_at.setdefault(successor_id, now)

    dependency_checks = 0
    event_start = {event.task_id: event.start_us for event in events}
    for task in tasks:
        for dep in task.deps:
            dependency_checks += 1
            if completed_at[dep] > event_start[task.task_id] + 1e-9:
                raise AssertionError(f"dependency violation: {dep} -> {task.task_id}")
    busy_json = {processor.value: value for processor, value in busy.items()}
    return ScheduleResult(
        mode=mode,
        makespan_us=now,
        busy_us=busy_json,
        bubble_rate={name: 1.0 - value / now for name, value in busy_json.items()},
        dispatch_overhead_us=total_dispatch_overhead,
        completed=len(completed),
        dependency_checks=dependency_checks,
        events=tuple(sorted(events, key=lambda event: (event.end_us, event.task_id))),
    )


def _relative_error(observed: float, target: float) -> float:
    return abs(observed - target) / abs(target)


def _range_error(observed: float, bounds: list[float]) -> float:
    low, high = bounds
    if low <= observed <= high:
        return 0.0
    boundary = low if observed < low else high
    return abs(observed - boundary) / abs(boundary)


def evaluate_mllm_endpoints(
    result: dict[str, Any],
    *,
    target_path: Path = PAPER_TARGETS,
    limit_override: float | None = None,
) -> dict[str, Any]:
    targets = json.loads(target_path.read_text(encoding="utf-8"))
    paper = targets["mllm"]
    limit = (
        float(limit_override)
        if limit_override is not None
        else float(targets["revised_stack_max_relative_error"])
    )
    observed = {
        "chunk_sharing_speedup": result["chunk_sharing"]["speedup"],
        "shadow_outlier_speedup": result["shadow_outlier"]["speedup"],
        "out_of_order_prefill_reduction": result["out_of_order"]["latency_reduction"],
        "naive_npu_bubble_rate": result["naive_schedule"]["bubble_rate"]["npu"],
        "out_of_order_npu_bubble_rate": result["out_of_order_schedule"]["bubble_rate"]["npu"],
    }
    specs = {
        "chunk_sharing_speedup": (paper["chunk_sharing_speedup_range"], True),
        "shadow_outlier_speedup": (paper["shadow_outlier_speedup_range"], True),
        "out_of_order_prefill_reduction": (paper["out_of_order_prefill_reduction_range"], True),
        "naive_npu_bubble_rate": (paper["naive_npu_bubble_rate"], False),
        "out_of_order_npu_bubble_rate": (paper["out_of_order_npu_bubble_rate"], False),
    }
    endpoints: list[dict[str, Any]] = []
    for name, value in observed.items():
        target, is_range = specs[name]
        error = _range_error(value, target) if is_range else _relative_error(value, target)
        endpoints.append(
            {
                "name": name,
                "observed": value,
                "target": target,
                "relative_error": error,
                "limit": limit,
                "pass": error <= limit,
            }
        )
    max_error = max(endpoint["relative_error"] for endpoint in endpoints)
    return {
        "endpoints": endpoints,
        "passed": sum(endpoint["pass"] for endpoint in endpoints),
        "total": len(endpoints),
        "max_relative_error": max_error,
        "limit": limit,
        "pass": all(endpoint["pass"] for endpoint in endpoints),
        "secondary_headline": {
            "target": paper["headline_average_prefill_speedup"],
            "status": "not_comparable_cross_platform_average",
            "reason": "requires the original five baselines and two Qualcomm phones",
        },
    }


def run_mllm_npu_reproduction(
    *,
    run_id: str,
    config: LlmNpuConfig | None = None,
    limit: float | None = None,
) -> dict[str, Any]:
    config = config or LlmNpuConfig()
    config.validate()
    graph = native_graph_contract()
    if graph["chunk_tokens"] != config.chunk_tokens:
        raise AssertionError("native MIR chunk length differs from reproduction config")
    chunk = chunk_sharing_experiment(config, graph)
    shadow = shadow_outlier_experiment(config)
    tasks = build_subgraphs(config, layers=int(graph["layers"]))
    naive = schedule_subgraphs(tasks, mode="naive")
    out_of_order = schedule_subgraphs(
        tasks,
        mode="out_of_order",
        scheduler_overhead_us=config.scheduler_overhead_us,
    )
    result: dict[str, Any] = {
        "schema_version": 1,
        "run_id": run_id,
        "component": "mllm-llm.npu",
        "evidence_type": "native_mllm_graph_plus_source_grounded_event_simulation",
        "source_contract": {
            "paper": "Fast On-device LLM Inference with NPUs",
            "doi": "10.1145/3669940.3707239",
            "mllm_commit": _git_head(MLLM_ROOT),
            "native_mir_sha256": hashlib.sha256(QWEN_MIR.read_bytes()).hexdigest(),
            "config": {
                field: getattr(config, field)
                for field in config.__dataclass_fields__
            },
        },
        "native_graph": graph,
        "chunk_sharing": chunk,
        "shadow_outlier": shadow,
        "naive_schedule": naive.summary(),
        "out_of_order_schedule": out_of_order.summary(),
        "out_of_order": {
            "latency_reduction": 1.0 - out_of_order.makespan_us / naive.makespan_us,
            "speedup": naive.makespan_us / out_of_order.makespan_us,
            "same_npu_work": abs(
                naive.busy_us[Processor.NPU.value] - out_of_order.busy_us[Processor.NPU.value]
            )
            < 1e-6,
            "same_cpu_work": abs(
                naive.busy_us[Processor.CPU.value] - out_of_order.busy_us[Processor.CPU.value]
            )
            < 1e-6,
        },
        "invariants": {
            "task_count": len(tasks),
            "same_completed": naive.completed == out_of_order.completed == len(tasks),
            "same_dependency_checks": naive.dependency_checks == out_of_order.dependency_checks,
            "out_of_order_faster": out_of_order.makespan_us < naive.makespan_us,
            "outlier_hidden": shadow["shadow_fully_hidden"],
            "native_graph_consumed": graph["operator_count"] > 0,
        },
    }
    result["paper_accuracy"] = evaluate_mllm_endpoints(
        result, limit_override=limit
    )
    result["summary"] = {
        "pass": result["paper_accuracy"]["pass"] and all(result["invariants"].values()),
        "paper_endpoints_passed": result["paper_accuracy"]["passed"],
        "paper_endpoints_total": result["paper_accuracy"]["total"],
        "max_relative_error": result["paper_accuracy"]["max_relative_error"],
    }
    # Events are returned privately for the runner and omitted from JSON result.
    result["_schedule_events"] = {
        "naive": naive.events,
        "out_of_order": out_of_order.events,
    }
    return result


def _git_head(path: Path) -> str:
    import subprocess

    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def write_schedule_trace(events: Iterable[ScheduleEvent], path: Path, *, mode: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for event in events:
            payload = event.to_dict()
            payload["schedule_mode"] = mode
            handle.write(json.dumps(payload, sort_keys=True) + "\n")

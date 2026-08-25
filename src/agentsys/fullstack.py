from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from .agentix import AgentixPolicy, AgentixResult, AgentixSimulator, CallSpec
from .mllm_backend import parse_mir, lower_to_tiles
from .model import FlowKind, Priority, Tile
from .tisa import TISAMode, TISAResult, TISASimulator
from .trace import TraceEvent, TraceRecorder
from .workloads import dynamic_agent_dag


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURE = PROJECT_ROOT / "integrations/mllm/fixtures/transformer_slice.mir"
TIME_SCALE = 1024


PROGRAM_PRIORITY = {
    "react": Priority.REACTIVE,
    "moa": Priority.PROACTIVE,
    "mcts": Priority.PROACTIVE,
}


@dataclass(frozen=True, slots=True)
class FullStackConfiguration:
    name: str
    agentix_policy: AgentixPolicy
    tisa_mode: TISAMode
    propagate_priority: bool


@dataclass(frozen=True, slots=True)
class FullStackResult:
    configuration: FullStackConfiguration
    agentix: AgentixResult
    tisa: TISAResult
    program_completion: dict[str, int]
    makespan: int
    reactive_completion: int
    proactive_completed: int
    proactive_throughput: float
    logical_digest: str
    dependency_valid: bool
    engine_work: dict[str, int]
    tiles: tuple[Tile, ...]

    def to_dict(self, *, include_tiles: bool = False) -> dict[str, Any]:
        value: dict[str, Any] = {
            "configuration": {
                "name": self.configuration.name,
                "agentix_policy": self.configuration.agentix_policy.value,
                "tisa_mode": self.configuration.tisa_mode.value,
                "propagate_priority": self.configuration.propagate_priority,
            },
            "agentix": self.agentix.to_dict(),
            "tisa": self.tisa.to_dict(),
            "program_completion": self.program_completion,
            "makespan": self.makespan,
            "reactive_completion": self.reactive_completion,
            "proactive_completed": self.proactive_completed,
            "proactive_throughput": self.proactive_throughput,
            "logical_digest": self.logical_digest,
            "dependency_valid": self.dependency_valid,
            "engine_work": self.engine_work,
        }
        if include_tiles:
            value["tiles"] = [
                {
                    "tile_id": tile.tile_id,
                    "task_id": tile.task_id,
                    "flow_id": tile.flow_id,
                    "call_id": tile.call_id,
                    "program_id": tile.program_id,
                    "engine": tile.engine.value,
                    "duration": tile.duration,
                    "priority": int(tile.priority),
                    "op_type": tile.op_type,
                    "sequence": tile.sequence,
                    "deps": tile.deps,
                    "arrival_cycle": tile.metadata["arrival_cycle"],
                }
                for tile in self.tiles
            ]
        return value


def _first_start(result: AgentixResult) -> dict[str, int]:
    starts: dict[str, int] = {}
    for item in result.slices:
        starts[item.call_id] = min(starts.get(item.call_id, item.start), item.start)
    return starts


def _logical_digest(calls: tuple[CallSpec, ...], template: tuple[Tile, ...]) -> str:
    payload = {
        "calls": [
            {
                "call": call.call_id,
                "program": call.program_id,
                "duration": call.duration,
                "deps": call.deps,
            }
            for call in calls
        ],
        "template": [
            {
                "local": tile.tile_id,
                "op": tile.op_type,
                "engine": tile.engine.value,
                "duration": tile.duration,
                "deps": tile.deps,
            }
            for tile in template
        ],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def _build_tiles(
    calls: tuple[CallSpec, ...],
    agentix: AgentixResult,
    configuration: FullStackConfiguration,
) -> tuple[tuple[Tile, ...], str]:
    template_ops = parse_mir(FIXTURE)
    template = lower_to_tiles(template_ops)
    starts = _first_start(agentix)
    original_order = {call.call_id: index for index, call in enumerate(calls)}
    ordered_calls = sorted(calls, key=lambda call: (starts[call.call_id], original_order[call.call_id]))
    final_tile: dict[str, str] = {}
    tiles: list[Tile] = []
    sequence = 0

    for call in ordered_calls:
        priority = PROGRAM_PRIORITY[call.program_id] if configuration.propagate_priority else Priority.NORMAL
        local_ids = {
            local.tile_id: f"tile:{call.call_id}:{local.sequence}" for local in template
        }
        parent_exits = tuple(final_tile[parent] for parent in call.deps)
        for local in template:
            deps = tuple(local_ids[dep] for dep in local.deps)
            if not deps:
                deps = parent_exits
            tile_id = local_ids[local.tile_id]
            metadata = dict(local.metadata)
            metadata["arrival_cycle"] = starts[call.call_id] * TIME_SCALE
            metadata["static_group"] = sequence
            tiles.append(
                replace(
                    local,
                    tile_id=tile_id,
                    task_id=f"task:{call.call_id}",
                    flow_id=f"flow:{call.call_id}",
                    call_id=f"call:{call.call_id}",
                    program_id=f"program:{call.program_id}",
                    priority=priority,
                    sequence=sequence,
                    deps=deps,
                    metadata=metadata,
                )
            )
            sequence += 1
        final_tile[call.call_id] = local_ids[template[-1].tile_id]
    return tuple(tiles), _logical_digest(calls, template)


def run_configuration(configuration: FullStackConfiguration) -> FullStackResult:
    calls = dynamic_agent_dag()
    agentix = AgentixSimulator(batch_size=3).run(calls, configuration.agentix_policy)
    tiles, digest = _build_tiles(calls, agentix, configuration)
    tisa = TISASimulator(window=8, dispatch_latency=7).run(tiles, configuration.tisa_mode)
    issue_by_tile = {issue.tile_id: issue for issue in tisa.issues}
    dependency_valid = all(
        all(issue_by_tile[dep].complete <= issue_by_tile[tile.tile_id].issue for dep in tile.deps)
        for tile in tiles
    )
    program_completion = {
        program: max(
            issue_by_tile[tile.tile_id].complete
            for tile in tiles
            if tile.program_id == f"program:{program}"
        )
        for program in PROGRAM_PRIORITY
    }
    makespan = max(program_completion.values())
    proactive_completed = sum(program in program_completion for program in ("moa", "mcts"))
    engine_work = {
        engine: sum(tile.duration for tile in tiles if tile.engine.value == engine)
        for engine in ("me", "ve", "de")
    }
    return FullStackResult(
        configuration=configuration,
        agentix=agentix,
        tisa=tisa,
        program_completion=program_completion,
        makespan=makespan,
        reactive_completion=program_completion["react"],
        proactive_completed=proactive_completed,
        proactive_throughput=proactive_completed / makespan,
        logical_digest=digest,
        dependency_valid=dependency_valid,
        engine_work=engine_work,
        tiles=tiles,
    )


def build_unified_trace(result: FullStackResult) -> TraceRecorder:
    if result.configuration.name != "full_stack":
        raise ValueError("unified trace is emitted only for full_stack")
    calls = dynamic_agent_dag()
    call_by_id = {call.call_id: call for call in calls}
    issues = {issue.tile_id: issue for issue in result.tisa.issues}
    raw_events: list[TraceEvent] = []

    for program, priority in PROGRAM_PRIORITY.items():
        program_id = f"program:{program}"
        raw_events.append(TraceEvent(0, "create", "program", program_id, priority, program_id))

    for call in calls:
        priority = PROGRAM_PRIORITY[call.program_id]
        program_id = f"program:{call.program_id}"
        call_id = f"call:{call.call_id}"
        flow_id = f"flow:{call.call_id}"
        task_id = f"task:{call.call_id}"
        raw_events.extend(
            (
                TraceEvent(0, "create", "call", call_id, priority, program_id, call_id=call_id, parent_id=program_id),
                TraceEvent(0, "create", "flow", flow_id, priority, program_id, call_id=call_id, flow_id=flow_id, parent_id=call_id),
                TraceEvent(0, "create", "task", task_id, priority, program_id, call_id=call_id, flow_id=flow_id, task_id=task_id, parent_id=flow_id),
            )
        )

    for tile in result.tiles:
        raw_events.append(
            TraceEvent(
                0,
                "create",
                "tile",
                tile.tile_id,
                tile.priority,
                tile.program_id,
                call_id=tile.call_id,
                flow_id=tile.flow_id,
                task_id=tile.task_id,
                tile_id=tile.tile_id,
                parent_id=tile.task_id,
                details={"op_type": tile.op_type, "engine": tile.engine.value},
            )
        )

    for program, priority in PROGRAM_PRIORITY.items():
        program_id = f"program:{program}"
        arrival = min(call.program_arrival for call in calls if call.program_id == program) * TIME_SCALE
        raw_events.append(TraceEvent(arrival, "submit", "program", program_id, priority, program_id))

    call_start = _first_start(result.agentix)
    for call in calls:
        priority = PROGRAM_PRIORITY[call.program_id]
        program_id = f"program:{call.program_id}"
        call_id = f"call:{call.call_id}"
        flow_id = f"flow:{call.call_id}"
        task_id = f"task:{call.call_id}"
        timestamp = call_start[call.call_id] * TIME_SCALE
        raw_events.extend(
            (
                TraceEvent(timestamp, "enqueue", "call", call_id, priority, program_id, call_id=call_id, parent_id=program_id),
                TraceEvent(timestamp, "submit", "flow", flow_id, priority, program_id, call_id=call_id, flow_id=flow_id, parent_id=call_id),
                TraceEvent(timestamp, "submit", "task", task_id, priority, program_id, call_id=call_id, flow_id=flow_id, task_id=task_id, parent_id=flow_id),
            )
        )

    for tile in result.tiles:
        issue = issues[tile.tile_id]
        engine_id = f"engine-event:{tile.tile_id}"
        raw_events.extend(
            (
                TraceEvent(tile.metadata["arrival_cycle"], "enqueue", "tile", tile.tile_id, tile.priority, tile.program_id, call_id=tile.call_id, flow_id=tile.flow_id, task_id=tile.task_id, tile_id=tile.tile_id, parent_id=tile.task_id),
                TraceEvent(issue.issue, "issue", "tile", tile.tile_id, tile.priority, tile.program_id, call_id=tile.call_id, flow_id=tile.flow_id, task_id=tile.task_id, tile_id=tile.tile_id, engine=tile.engine.value, parent_id=tile.task_id),
                TraceEvent(issue.issue, "create", "engine", engine_id, tile.priority, tile.program_id, call_id=tile.call_id, flow_id=tile.flow_id, task_id=tile.task_id, tile_id=tile.tile_id, engine=tile.engine.value, parent_id=tile.tile_id),
                TraceEvent(issue.complete, "complete", "engine", engine_id, tile.priority, tile.program_id, call_id=tile.call_id, flow_id=tile.flow_id, task_id=tile.task_id, tile_id=tile.tile_id, engine=tile.engine.value, parent_id=tile.tile_id),
                TraceEvent(issue.complete, "complete", "tile", tile.tile_id, tile.priority, tile.program_id, call_id=tile.call_id, flow_id=tile.flow_id, task_id=tile.task_id, tile_id=tile.tile_id, engine=tile.engine.value, parent_id=tile.task_id),
            )
        )

    for call in calls:
        program_id = f"program:{call.program_id}"
        call_id = f"call:{call.call_id}"
        flow_id = f"flow:{call.call_id}"
        task_id = f"task:{call.call_id}"
        priority = PROGRAM_PRIORITY[call.program_id]
        completed = max(
            issues[tile.tile_id].complete for tile in result.tiles if tile.call_id == call_id
        )
        raw_events.extend(
            (
                TraceEvent(completed, "complete", "task", task_id, priority, program_id, call_id=call_id, flow_id=flow_id, task_id=task_id, parent_id=flow_id),
                TraceEvent(completed, "complete", "flow", flow_id, priority, program_id, call_id=call_id, flow_id=flow_id, parent_id=call_id),
                TraceEvent(completed, "complete", "call", call_id, priority, program_id, call_id=call_id, parent_id=program_id),
            )
        )

    for program, priority in PROGRAM_PRIORITY.items():
        program_id = f"program:{program}"
        raw_events.append(
            TraceEvent(result.program_completion[program], "complete", "program", program_id, priority, program_id)
        )

    event_order = {"create": 0, "submit": 1, "enqueue": 2, "issue": 3, "complete": 4, "cancel": 4}
    raw_events.sort(key=lambda event: (event.timestamp, event_order[event.event]))
    recorder = TraceRecorder()
    recorder.extend(raw_events)
    return recorder


CONFIGURATIONS = (
    FullStackConfiguration("fcfs_static", AgentixPolicy.FCFS, TISAMode.STATIC, False),
    FullStackConfiguration("atlas_static", AgentixPolicy.ATLAS, TISAMode.STATIC, True),
    FullStackConfiguration("fcfs_dynamic", AgentixPolicy.FCFS, TISAMode.DYNAMIC, False),
    FullStackConfiguration("full_stack", AgentixPolicy.ATLAS, TISAMode.DYNAMIC, True),
)


def run_full_stack(*, run_id: str = "run_007") -> tuple[dict[str, Any], TraceRecorder]:
    results = {config.name: run_configuration(config) for config in CONFIGURATIONS}
    full = results["full_stack"]
    baseline = results["fcfs_static"]
    trace = build_unified_trace(full)
    lineage = trace.validate_lineage()
    inheritance = trace.validate_priority_inheritance()
    layers = sorted({event.layer for event in trace.events})
    digests = {result.logical_digest for result in results.values()}
    work = {tuple(sorted(result.engine_work.items())) for result in results.values()}
    dependency_valid = all(result.dependency_valid for result in results.values())
    gates = {
        "logical_digest_equal": len(digests) == 1,
        "engine_work_equal": len(work) == 1,
        "dependencies_valid": dependency_valid,
        "lineage": lineage["terminal"] > 0,
        "priority_inheritance": inheritance["events_checked"] == len(trace.events),
        "six_layers": layers == ["call", "engine", "flow", "program", "task", "tile"],
        "full_makespan_improves": full.makespan < baseline.makespan,
        "full_reactive_improves": full.reactive_completion < baseline.reactive_completion,
        "no_proactive_loss": full.proactive_completed == baseline.proactive_completed == 2,
    }
    artifact = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "exploratory_full_stack_trace_simulation",
        "time_scale_cycles_per_agentix_step": TIME_SCALE,
        "configurations": {
            name: result.to_dict(include_tiles=name == "full_stack") for name, result in results.items()
        },
        "derived": {
            "full_vs_baseline_makespan_speedup": baseline.makespan / full.makespan,
            "full_vs_baseline_reactive_speedup": baseline.reactive_completion / full.reactive_completion,
            "atlas_static_speedup": baseline.makespan / results["atlas_static"].makespan,
            "fcfs_dynamic_speedup": baseline.makespan / results["fcfs_dynamic"].makespan,
            "stacking_efficiency": (baseline.makespan / full.makespan)
            / ((baseline.makespan / results["atlas_static"].makespan)
               * (baseline.makespan / results["fcfs_dynamic"].makespan)),
        },
        "trace": {
            "events": len(trace.events),
            "layers": layers,
            "lineage": lineage,
            "priority_inheritance": inheritance,
        },
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }
    return artifact, trace


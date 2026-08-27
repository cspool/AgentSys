from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .agentix import AgentixSimulator
from .mllm_backend import operator_digest, parse_mir
from .model import Priority
from .workload import AgentWorkload, WorkloadCall


def _first_start(result: Any) -> dict[str, int]:
    starts: dict[str, int] = {}
    for item in result.slices:
        starts[item.call_id] = min(starts.get(item.call_id, item.start), item.start)
    return starts


def _tool_execute(call: WorkloadCall, parent_outputs: tuple[str, ...]) -> str:
    if call.tool_kind != "deterministic_lookup":
        raise ValueError(f"unsupported tool adapter: {call.tool_kind}")
    payload = json.dumps(
        {"tool": call.tool_kind, "call": call.call_id, "parents": parent_outputs},
        sort_keys=True,
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def execute_agent_workload(workload: AgentWorkload, *, run_id: str) -> dict[str, Any]:
    specs = workload.call_specs()
    schedule = AgentixSimulator(batch_size=workload.agentix_batch_size).run(
        specs,
        workload.agentix_policy,
        program_priorities=workload.program_priorities,
    )
    starts = _first_start(schedule)
    original = {call.call_id: index for index, call in enumerate(workload.calls)}
    call_by_id = {call.call_id: call for call in workload.calls}
    order = sorted(workload.calls, key=lambda call: (starts[call.call_id], original[call.call_id]))

    model_evidence: dict[str, Any] = {}
    framework_digests: dict[str, str] = {}
    for model in workload.models:
        operators = parse_mir(model.framework_mir)
        digest = operator_digest(operators)
        framework_digests[model.model_id] = digest
        model_evidence[model.model_id] = {
            "framework_mir": str(model.framework_mir),
            "framework_mir_sha256": hashlib.sha256(model.framework_mir.read_bytes()).hexdigest(),
            "framework_operator_digest": digest,
            "framework_operators": [operator.to_dict() for operator in operators],
            "hardware_mir": str(model.hardware_mir),
            "hardware_mir_sha256": hashlib.sha256(model.hardware_mir.read_bytes()).hexdigest(),
            "selected_source_indices": list(model.selected_source_indices),
            "duration_divisors": dict(model.duration_divisors),
            "stages": list(model.stages),
        }

    events: list[dict[str, Any]] = []
    calls: list[dict[str, Any]] = []
    outputs: dict[str, str] = {}
    started_programs: set[str] = set()
    remaining = {
        program.program_id: sum(call.program_id == program.program_id for call in workload.calls)
        for program in workload.programs
    }
    program_codes = workload.program_codes

    for index, call in enumerate(order):
        if any(dependency not in outputs for dependency in call.deps):
            raise AssertionError(f"Agentix released {call.call_id} before dependencies")
        logical_time = starts[call.call_id]
        priority = workload.program_priorities[call.program_id]
        if call.program_id not in started_programs:
            started_programs.add(call.program_id)
            events.append(
                {
                    "logical_time": logical_time,
                    "layer": "application",
                    "event": "program_start",
                    "program_id": call.program_id,
                    "call_id": None,
                    "details": {"priority": int(priority)},
                }
            )
        events.append(
            {
                "logical_time": logical_time,
                "layer": "framework",
                "event": "call_release",
                "program_id": call.program_id,
                "call_id": call.call_id,
                "details": {"deps": list(call.deps), "thread": call.thread_id},
            }
        )

        parent_outputs = tuple(outputs[dependency] for dependency in call.deps)
        if call.kind == "tool":
            digest = _tool_execute(call, parent_outputs)
            binding = "rocket_cpu_tool"
            events.append(
                {
                    "logical_time": logical_time,
                    "layer": "framework",
                    "event": "tool_execute",
                    "program_id": call.program_id,
                    "call_id": call.call_id,
                    "details": {"tool": call.tool_kind, "cycles": call.tool_cycles},
                }
            )
        else:
            assert call.model_profile is not None
            model_digest = framework_digests[call.model_profile]
            payload = json.dumps(
                {
                    "call": call.call_id,
                    "parents": parent_outputs,
                    "model": model_digest,
                    "tokens": [call.input_tokens, call.output_tokens],
                },
                sort_keys=True,
            ).encode()
            digest = hashlib.sha256(payload).hexdigest()
            binding = (
                "npu_prefill+igpu_reactive_decode"
                if priority is Priority.REACTIVE
                else "npu_prefill+igpu_slack_decode"
            )
            events.extend(
                (
                    {
                        "logical_time": logical_time,
                        "layer": "framework",
                        "event": "flow_bind",
                        "program_id": call.program_id,
                        "call_id": call.call_id,
                        "details": {
                            "binding": binding,
                            "input_tokens": call.input_tokens,
                            "model_profile": call.model_profile,
                        },
                    },
                    {
                        "logical_time": logical_time,
                        "layer": "framework",
                        "event": "mllm_lower",
                        "program_id": call.program_id,
                        "call_id": call.call_id,
                        "details": {
                            "model_profile": call.model_profile,
                            "model_digest": model_digest,
                            "selected_operators": len(
                                workload.models_by_id[call.model_profile].selected_source_indices
                            ),
                        },
                    },
                )
            )
        outputs[call.call_id] = digest
        calls.append(
            {
                "index": index,
                "call_id": call.call_id,
                "program_id": call.program_id,
                "program_code": program_codes[call.program_id],
                "kind": call.kind,
                "priority": int(priority),
                "deps": list(call.deps),
                "scheduled_step": logical_time,
                "input_tokens": call.input_tokens,
                "output_tokens": call.output_tokens,
                "flow_binding": binding,
                "model_profile": call.model_profile,
                "tool_kind": call.tool_kind,
                "tool_cycles": call.tool_cycles,
                "output_digest": digest,
            }
        )
        events.append(
            {
                "logical_time": logical_time + call.duration,
                "layer": "framework",
                "event": "call_complete",
                "program_id": call.program_id,
                "call_id": call.call_id,
                "details": {"output_digest": digest},
            }
        )
        remaining[call.program_id] -= 1
        if remaining[call.program_id] == 0:
            events.append(
                {
                    "logical_time": logical_time + call.duration,
                    "layer": "application",
                    "event": "program_complete",
                    "program_id": call.program_id,
                    "call_id": None,
                    "details": {
                        "calls": sum(
                            item.program_id == call.program_id for item in workload.calls
                        )
                    },
                }
            )

    model_identity: str | dict[str, str]
    if len(framework_digests) == 1:
        model_identity = next(iter(framework_digests.values()))
    else:
        model_identity = framework_digests
    final_digest = hashlib.sha256(
        json.dumps(
            {
                "outputs": outputs,
                "model": model_identity,
                "order": [call["call_id"] for call in calls],
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()
    events.sort(key=lambda event: (event["logical_time"], event["layer"], event["event"]))
    summary = {
        "programs": len(workload.programs),
        "calls": len(calls),
        "llm_calls": sum(call["kind"] == "llm" for call in calls),
        "tool_calls": sum(call["kind"] == "tool" for call in calls),
        "events": len(events),
        "pass": len(outputs) == len(calls),
    }
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "manifest_driven_executed_agent_application",
        "application": workload.name,
        "workload": workload.to_contract_dict(),
        "models": model_evidence,
        "agentix_result": schedule.to_dict(),
        "calls": calls,
        "events": events,
        "output_digest": final_digest,
        "summary": summary,
    }


def write_parameterized_application(
    workload: AgentWorkload,
    path: Path,
    *,
    run_id: str,
) -> dict[str, Any]:
    result = execute_agent_workload(workload, run_id=run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result

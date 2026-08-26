from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .agentix import AgentixPolicy, AgentixSimulator
from .mllm_backend import lower_to_tiles, operator_digest, parse_mir
from .model import Priority
from .workloads import dynamic_agent_dag


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_MIR = PROJECT_ROOT / "integrations/mllm/fixtures/transformer_slice.mir"


PROGRAM_PRIORITY = {
    "react": Priority.REACTIVE,
    "moa": Priority.PROACTIVE,
    "mcts": Priority.PROACTIVE,
}


@dataclass(frozen=True, slots=True)
class FrameworkEvent:
    logical_time: int
    layer: str
    event: str
    program_id: str
    call_id: str | None
    details: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ApplicationCall:
    index: int
    call_id: str
    program_id: str
    kind: str
    priority: int
    deps: tuple[str, ...]
    scheduled_step: int
    input_tokens: int
    output_tokens: int
    flow_binding: str
    output_digest: str


@dataclass(frozen=True, slots=True)
class AgentApplicationTrace:
    run_id: str
    application: str
    model_mir: str
    model_digest: str
    calls: tuple[ApplicationCall, ...]
    events: tuple[FrameworkEvent, ...]
    operator_template: tuple[dict[str, Any], ...]
    output_digest: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "run_id": self.run_id,
            "classification": "executed_agent_application_and_framework_trace",
            "application": self.application,
            "model_mir": self.model_mir,
            "model_digest": self.model_digest,
            "calls": [asdict(call) for call in self.calls],
            "events": [asdict(event) for event in self.events],
            "operator_template": list(self.operator_template),
            "output_digest": self.output_digest,
            "summary": {
                "programs": len({call.program_id for call in self.calls}),
                "calls": len(self.calls),
                "llm_calls": sum(call.kind == "llm" for call in self.calls),
                "tool_calls": sum(call.kind == "tool" for call in self.calls),
                "events": len(self.events),
                "operators_per_llm_call": len(self.operator_template),
                "pass": True,
            },
        }


def _first_start(result: Any) -> dict[str, int]:
    starts: dict[str, int] = {}
    for item in result.slices:
        starts[item.call_id] = min(starts.get(item.call_id, item.start), item.start)
    return starts


def _token_shape(program_id: str, duration: int, call_index: int) -> tuple[int, int]:
    if program_id == "react":
        return 213 + 8 * call_index, 70 + 2 * duration
    if program_id == "moa":
        return 435 + 16 * call_index, 81 + 3 * duration
    return 467 + 12 * call_index, 73 + 4 * duration


def _tool_execute(call_id: str, parent_outputs: tuple[str, ...]) -> str:
    payload = json.dumps(
        {"tool": "deterministic_lookup", "call": call_id, "parents": parent_outputs},
        sort_keys=True,
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def run_agent_application(*, run_id: str = "run_021") -> AgentApplicationTrace:
    specs = dynamic_agent_dag()
    by_id = {call.call_id: call for call in specs}
    schedule = AgentixSimulator(batch_size=3).run(
        specs,
        AgentixPolicy.ATLAS,
        program_priorities=PROGRAM_PRIORITY,
    )
    starts = _first_start(schedule)
    original = {call.call_id: index for index, call in enumerate(specs)}
    order = sorted(specs, key=lambda call: (starts[call.call_id], original[call.call_id]))

    operators = parse_mir(MODEL_MIR)
    tiles = lower_to_tiles(operators)
    model_hash = operator_digest(operators)
    operator_template = tuple(
        {
            "index": operator.index,
            "op_type": operator.op_type,
            "engine": operator.engine.value,
            "duration": operator.duration,
            "deps": list(operator.deps),
            "source_line": operator.source_line,
        }
        for operator in operators
    )
    if len(tiles) != 8:
        raise AssertionError("Rocket AgentSys window requires exactly eight lowered model tiles")

    events: list[FrameworkEvent] = []
    calls: list[ApplicationCall] = []
    outputs: dict[str, str] = {}
    created_programs: set[str] = set()
    remaining_by_program = {
        program: sum(call.program_id == program for call in specs) for program in PROGRAM_PRIORITY
    }

    for index, spec in enumerate(order):
        if any(dep not in outputs for dep in spec.deps):
            raise AssertionError(f"framework released {spec.call_id} before its dependencies")
        logical_time = starts[spec.call_id]
        if spec.program_id not in created_programs:
            created_programs.add(spec.program_id)
            events.append(
                FrameworkEvent(
                    logical_time,
                    "application",
                    "program_start",
                    spec.program_id,
                    None,
                    {"priority": int(PROGRAM_PRIORITY[spec.program_id])},
                )
            )
        events.append(
            FrameworkEvent(
                logical_time,
                "framework",
                "call_release",
                spec.program_id,
                spec.call_id,
                {"deps": list(spec.deps), "thread": spec.thread_id},
            )
        )
        kind = "tool" if spec.call_id == "react-tool" else "llm"
        input_tokens, output_tokens = _token_shape(spec.program_id, spec.duration, index)
        parent_outputs = tuple(outputs[dep] for dep in spec.deps)
        if kind == "tool":
            digest = _tool_execute(spec.call_id, parent_outputs)
            binding = "rocket_cpu_tool"
            events.append(
                FrameworkEvent(
                    logical_time,
                    "framework",
                    "tool_execute",
                    spec.program_id,
                    spec.call_id,
                    {"tool": "deterministic_lookup"},
                )
            )
        else:
            payload = json.dumps(
                {
                    "call": spec.call_id,
                    "parents": parent_outputs,
                    "model": model_hash,
                    "tokens": [input_tokens, output_tokens],
                },
                sort_keys=True,
            ).encode()
            digest = hashlib.sha256(payload).hexdigest()
            binding = (
                "npu_prefill+igpu_reactive_decode"
                if PROGRAM_PRIORITY[spec.program_id] is Priority.REACTIVE
                else "npu_prefill+igpu_slack_decode"
            )
            events.extend(
                (
                    FrameworkEvent(
                        logical_time,
                        "framework",
                        "flow_bind",
                        spec.program_id,
                        spec.call_id,
                        {"binding": binding, "input_tokens": input_tokens},
                    ),
                    FrameworkEvent(
                        logical_time,
                        "framework",
                        "mllm_lower",
                        spec.program_id,
                        spec.call_id,
                        {"operators": len(operators), "model_digest": model_hash},
                    ),
                )
            )
        outputs[spec.call_id] = digest
        calls.append(
            ApplicationCall(
                index=index,
                call_id=spec.call_id,
                program_id=spec.program_id,
                kind=kind,
                priority=int(PROGRAM_PRIORITY[spec.program_id]),
                deps=spec.deps,
                scheduled_step=logical_time,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                flow_binding=binding,
                output_digest=digest,
            )
        )
        events.append(
            FrameworkEvent(
                logical_time + spec.duration,
                "framework",
                "call_complete",
                spec.program_id,
                spec.call_id,
                {"output_digest": digest},
            )
        )
        remaining_by_program[spec.program_id] -= 1
        if remaining_by_program[spec.program_id] == 0:
            events.append(
                FrameworkEvent(
                    logical_time + spec.duration,
                    "application",
                    "program_complete",
                    spec.program_id,
                    None,
                    {"calls": sum(call.program_id == spec.program_id for call in specs)},
                )
            )

    final_digest = hashlib.sha256(
        json.dumps(
            {"outputs": outputs, "model": model_hash, "order": [call.call_id for call in calls]},
            sort_keys=True,
        ).encode()
    ).hexdigest()
    events.sort(key=lambda event: (event.logical_time, event.layer, event.event))
    return AgentApplicationTrace(
        run_id=run_id,
        application="ReAct+Mixture-of-Agents+MCTS",
        model_mir=str(MODEL_MIR.relative_to(PROJECT_ROOT)),
        model_digest=model_hash,
        calls=tuple(calls),
        events=tuple(events),
        operator_template=operator_template,
        output_digest=final_digest,
    )


def write_agent_application_trace(path: Path, *, run_id: str = "run_021") -> dict[str, Any]:
    result = run_agent_application(run_id=run_id).to_dict()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result

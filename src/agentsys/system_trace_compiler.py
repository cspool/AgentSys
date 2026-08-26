from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .agent_application import PROJECT_ROOT, AgentApplicationTrace, run_agent_application
from .mllm_backend import MllmOperator, parse_mir
from .model import Engine


GENERATED_HEADER = PROJECT_ROOT / "system_sim/software/generated/agentsys_app_trace.h"
COMPILED_MANIFEST = PROJECT_ROOT / "artifacts/app_traces/compiled-system-workload-run_021.json"
APPLICATION_TRACE = PROJECT_ROOT / "artifacts/app_traces/agent-application-run_021.json"


ENGINE_CODE = {Engine.ME: 0, Engine.VE: 1, Engine.DE: 2}
ENGINE_DURATION_DIVISOR = {Engine.ME: 12.8, Engine.VE: 12.8, Engine.DE: 12.8}
PROGRAM_CODE = {"react": 0, "moa": 1, "mcts": 2}


@dataclass(frozen=True, slots=True)
class HardwareDescriptor:
    index: int
    control: int
    tilemem: int
    engine: str
    duration: int
    deps_mask: int
    op_type: str


@dataclass(frozen=True, slots=True)
class HardwareCall:
    index: int
    call_id: str
    program_id: str
    program_code: int
    kind: str
    priority: int
    deps_mask: int
    program_first: int
    program_last: int
    input_tokens: int
    output_tokens: int
    tool_cycles: int
    descriptors: tuple[HardwareDescriptor, ...]


def _control_word(
    *,
    tile_id: int,
    task_id: int,
    deps: int,
    access: int,
    priority: int,
    engine: int,
    op_type: int,
    duration: int,
    static_group: int,
) -> int:
    return (
        (1 << 60)
        | (static_group << 52)
        | (duration << 36)
        | (op_type << 30)
        | (engine << 28)
        | (priority << 26)
        | (access << 24)
        | (deps << 16)
        | (task_id << 8)
        | tile_id
    )


def _tilemem_word(base: int, size: int, scope: int, bank: int) -> int:
    bounded_size = max(1, min(size, 0xFFFF))
    return (bank << 50) | (scope << 48) | ((bounded_size - 1) << 32) | (base & 0xFFFFFFFF)


def _descriptor_template(operators: tuple[MllmOperator, ...], priority: int) -> tuple[HardwareDescriptor, ...]:
    if len(operators) != 8:
        raise ValueError("hardware compiler requires exactly eight MIR operators")
    descriptors: list[HardwareDescriptor] = []
    for operator in operators:
        deps = 0
        for dependency in operator.deps:
            deps |= 1 << dependency
        duration = max(1, min(0xFFFF, math.ceil(operator.duration / ENGINE_DURATION_DIVISOR[operator.engine])))
        output = operator.outputs[0]
        base = int(output.ssa) * 0x100000
        tilemem = _tilemem_word(base, output.bytes, 1, int(output.ssa) % 4)
        control = _control_word(
            tile_id=operator.index,
            task_id=0,
            deps=deps,
            access=1,
            priority=priority,
            engine=ENGINE_CODE[operator.engine],
            op_type=operator.index + 1,
            duration=duration,
            static_group=operator.index,
        )
        descriptors.append(
            HardwareDescriptor(
                index=operator.index,
                control=control,
                tilemem=tilemem,
                engine=operator.engine.value,
                duration=duration,
                deps_mask=deps,
                op_type=operator.op_type,
            )
        )
    return tuple(descriptors)


def compile_application_trace(application: AgentApplicationTrace) -> tuple[HardwareCall, ...]:
    operators = parse_mir(PROJECT_ROOT / application.model_mir)
    index_by_id = {call.call_id: call.index for call in application.calls}
    remaining = {
        program: sum(call.program_id == program for call in application.calls)
        for program in PROGRAM_CODE
    }
    seen: set[str] = set()
    calls: list[HardwareCall] = []
    for call in application.calls:
        deps_mask = 0
        for dependency in call.deps:
            deps_mask |= 1 << index_by_id[dependency]
        first = int(call.program_id not in seen)
        seen.add(call.program_id)
        remaining[call.program_id] -= 1
        last = int(remaining[call.program_id] == 0)
        descriptors = (
            _descriptor_template(operators, call.priority) if call.kind == "llm" else ()
        )
        calls.append(
            HardwareCall(
                index=call.index,
                call_id=call.call_id,
                program_id=call.program_id,
                program_code=PROGRAM_CODE[call.program_id],
                kind=call.kind,
                priority=call.priority,
                deps_mask=deps_mask,
                program_first=first,
                program_last=last,
                input_tokens=call.input_tokens,
                output_tokens=call.output_tokens,
                tool_cycles=64 * max(1, call.output_tokens // 16) if call.kind == "tool" else 0,
                descriptors=descriptors,
            )
        )
    return tuple(calls)


def _c_string(value: str) -> str:
    return json.dumps(value)


def render_header(application: AgentApplicationTrace, calls: tuple[HardwareCall, ...]) -> str:
    digest64 = int(application.output_digest[:16], 16)
    lines = [
        "#pragma once",
        "",
        "#include <stdint.h>",
        "",
        "#define AGENTSYS_APP_CALLS %d" % len(calls),
        "#define AGENTSYS_APP_PROGRAMS 3",
        "#define AGENTSYS_APP_MAX_DESCRIPTORS 8",
        "#define AGENTSYS_APP_INPUT_BEATS 8",
        "#define AGENTSYS_APP_OUTPUT_BEATS 4",
        "#define AGENTSYS_APP_TRACE_DIGEST UINT64_C(0x%016x)" % digest64,
        "",
        "typedef struct {",
        "  const char *call_id;",
        "  const char *program_id;",
        "  uint8_t program_code;",
        "  uint8_t kind; /* 0=LLM/XPU, 1=CPU tool */",
        "  uint8_t priority;",
        "  uint8_t descriptor_count;",
        "  uint16_t deps_mask;",
        "  uint8_t program_first;",
        "  uint8_t program_last;",
        "  uint16_t input_tokens;",
        "  uint16_t output_tokens;",
        "  uint16_t tool_cycles;",
        "  uint64_t control[AGENTSYS_APP_MAX_DESCRIPTORS];",
        "  uint64_t tilemem[AGENTSYS_APP_MAX_DESCRIPTORS];",
        "} agentsys_app_call_t;",
        "",
        "static const agentsys_app_call_t agentsys_app_calls[AGENTSYS_APP_CALLS] = {",
    ]
    for call in calls:
        controls = [descriptor.control for descriptor in call.descriptors]
        tilemem = [descriptor.tilemem for descriptor in call.descriptors]
        controls.extend([0] * (8 - len(controls)))
        tilemem.extend([0] * (8 - len(tilemem)))
        lines.extend(
            (
                "  {",
                f"    {_c_string(call.call_id)}, {_c_string(call.program_id)}, {call.program_code}, "
                f"{1 if call.kind == 'tool' else 0}, {call.priority}, {len(call.descriptors)},",
                f"    UINT16_C(0x{call.deps_mask:04x}), {call.program_first}, {call.program_last}, "
                f"{call.input_tokens}, {call.output_tokens}, {call.tool_cycles},",
                "    {" + ", ".join(f"UINT64_C(0x{value:016x})" for value in controls) + "},",
                "    {" + ", ".join(f"UINT64_C(0x{value:016x})" for value in tilemem) + "}",
                "  },",
            )
        )
    lines.extend(("};", ""))
    return "\n".join(lines)


def compile_and_write(
    *,
    header_path: Path = GENERATED_HEADER,
    manifest_path: Path = COMPILED_MANIFEST,
    application_path: Path = APPLICATION_TRACE,
    run_id: str = "run_021",
) -> dict[str, Any]:
    application = run_agent_application(run_id=run_id)
    application_value = application.to_dict()
    application_path.parent.mkdir(parents=True, exist_ok=True)
    application_path.write_text(
        json.dumps(application_value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    calls = compile_application_trace(application)
    header = render_header(application, calls)
    header_path.parent.mkdir(parents=True, exist_ok=True)
    if not header_path.is_file() or header_path.read_text(encoding="utf-8") != header:
        header_path.write_text(header, encoding="utf-8")
    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "agent_framework_to_riscv_xpu_trace_compilation",
        "application": application_value,
        "application_trace": str(application_path.relative_to(PROJECT_ROOT)),
        "application_trace_sha256": hashlib.sha256(application_path.read_bytes()).hexdigest(),
        "hardware_calls": [
            {
                **{key: value for key, value in asdict(call).items() if key != "descriptors"},
                "descriptors": [asdict(descriptor) for descriptor in call.descriptors],
            }
            for call in calls
        ],
        "generated_header": str(header_path.relative_to(PROJECT_ROOT)),
        "generated_header_sha256": hashlib.sha256(header.encode()).hexdigest(),
        "summary": {
            "programs": 3,
            "calls": len(calls),
            "llm_calls": sum(call.kind == "llm" for call in calls),
            "tool_calls": sum(call.kind == "tool" for call in calls),
            "descriptors": sum(len(call.descriptors) for call in calls),
            "dependencies": sum(bool(call.deps_mask) for call in calls),
            "pass": (
                len(calls) == 11
                and sum(call.kind == "llm" for call in calls) == 10
                and sum(len(call.descriptors) for call in calls) == 80
            ),
        },
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .agent_application import PROJECT_ROOT, AgentApplicationTrace, run_agent_application
from .agentxpu import XPUConfig
from .mllm_backend import MLLM_ROOT, MllmOperator, operator_digest, parse_mir
from .model import Engine


UPSTREAM_MIR = MLLM_ROOT / "examples/qwen3_qnn_aot/qwen3_qnn_aot_1.7B.mir"
UPSTREAM_MLLM_COMMIT = "50ad5a9b6fbea742e38b5b31776c187e50319c8e"
SELECTED_SOURCE_INDICES = (6, 7, 8, 10, 11, 12, 13, 14)
GENERATED_HEADER = PROJECT_ROOT / "system_sim/software/generated/agentsys_revised_app_trace.h"
COMPILED_MANIFEST = PROJECT_ROOT / "artifacts/app_traces/revised-compiled-workload-run_027.json"
APPLICATION_TRACE = PROJECT_ROOT / "artifacts/app_traces/revised-agent-application-run_027.json"

ENGINE_CODE = {Engine.ME: 0, Engine.VE: 1, Engine.DE: 2}
PLACEMENT = {Engine.ME: "hptpe", Engine.VE: "vector", Engine.DE: "data"}
PLACEMENT_CODE = {Engine.ME: 0, Engine.VE: 1, Engine.DE: 2}
ENGINE_DURATION_DIVISOR = {Engine.ME: 12.8, Engine.VE: 12.8, Engine.DE: 12.8}
PROGRAM_CODE = {"react": 0, "moa": 1, "mcts": 2}


@dataclass(frozen=True, slots=True)
class RevisedDescriptor:
    index: int
    source_index: int
    control: int
    tilemem: int
    engine: str
    placement: str
    placement_code: int
    stage: str
    stage_code: int
    flow_class: str
    flow_code: int
    preemptible: int
    duration: int
    deps_mask: int
    op_type: str


@dataclass(frozen=True, slots=True)
class RevisedCall:
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
    flow_class: str
    flow_code: int
    prefill_chunk_tokens: int
    decode_batch_cap: int
    elastic_hptpe_percent: int
    descriptors: tuple[RevisedDescriptor, ...]


def _git_head(path: Path) -> str:
    import subprocess

    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def selected_native_operators() -> tuple[MllmOperator, ...]:
    operators = parse_mir(UPSTREAM_MIR)
    return tuple(operators[index] for index in SELECTED_SOURCE_INDICES)


def _control_word(
    *,
    tile_id: int,
    task_id: int,
    deps: int,
    access: int,
    priority: int,
    engine: int,
    native_op: int,
    placement: int,
    duration: int,
    static_group: int,
    flow: int,
    stage: int,
    preemptible: int,
) -> int:
    return (
        (stage << 63)
        | (preemptible << 62)
        | (flow << 61)
        | (1 << 60)
        | (static_group << 52)
        | (duration << 36)
        | (placement << 34)
        | ((native_op & 0xF) << 30)
        | (engine << 28)
        | (priority << 26)
        | (access << 24)
        | (deps << 16)
        | (task_id << 8)
        | tile_id
    )


def _tilemem_word(base: int, size: int, scope: int, bank: int, source_index: int) -> int:
    bounded_size = max(1, min(size, 0xFFFF))
    return (
        ((source_index & 0x3FF) << 54)
        | (bank << 50)
        | (scope << 48)
        | ((bounded_size - 1) << 32)
        | (base & 0xFFFFFFFF)
    )


def _flow_plan(priority: int) -> dict[str, int | str]:
    cfg = XPUConfig()
    reactive = priority == 0
    return {
        "flow_class": "reactive" if reactive else "proactive",
        "flow_code": 0 if reactive else 1,
        "prefill_chunk_tokens": cfg.heg_prefill_chunk_tokens,
        "decode_batch_cap": cfg.max_reactive_decode_batch if reactive else cfg.max_decode_batch,
        "elastic_hptpe_percent": int(round((1.0 - cfg.heg_igpu_prefill_share) * 100)),
    }


def _descriptor_template(operators: tuple[MllmOperator, ...], priority: int) -> tuple[RevisedDescriptor, ...]:
    if tuple(operator.index for operator in operators) != SELECTED_SOURCE_INDICES:
        raise ValueError("native mllm operator selection drift")
    selected_map = {operator.index: index for index, operator in enumerate(operators)}
    flow = _flow_plan(priority)
    descriptors: list[RevisedDescriptor] = []
    for index, operator in enumerate(operators):
        deps = 0
        for dependency in operator.deps:
            if dependency in selected_map:
                deps |= 1 << selected_map[dependency]
        duration = max(
            1,
            min(
                0xFFFF,
                math.ceil(operator.duration / ENGINE_DURATION_DIVISOR[operator.engine]),
            ),
        )
        output = operator.outputs[0]
        base = int(output.ssa) * 0x100000
        stage_code = int(index >= 6)
        placement_code = PLACEMENT_CODE[operator.engine]
        tilemem = _tilemem_word(
            base,
            output.bytes,
            1,
            int(output.ssa) % 4,
            operator.index,
        )
        control = _control_word(
            tile_id=index,
            task_id=index,
            deps=deps,
            access=1,
            priority=priority,
            engine=ENGINE_CODE[operator.engine],
            native_op=operator.index,
            placement=placement_code,
            duration=duration,
            # The paper's comparison baseline is a strong static tile pipeline,
            # not per-operator serialization.  Reuse the already-defined
            # Agent.xpu prefill/decode-handoff stage boundary.
            static_group=stage_code,
            flow=int(flow["flow_code"]),
            stage=stage_code,
            preemptible=1,
        )
        descriptors.append(
            RevisedDescriptor(
                index=index,
                source_index=operator.index,
                control=control,
                tilemem=tilemem,
                engine=operator.engine.value,
                placement=PLACEMENT[operator.engine],
                placement_code=placement_code,
                stage="decode_handoff" if stage_code else "prefill",
                stage_code=stage_code,
                flow_class=str(flow["flow_class"]),
                flow_code=int(flow["flow_code"]),
                preemptible=1,
                duration=duration,
                deps_mask=deps,
                op_type=operator.op_type,
            )
        )
    return tuple(descriptors)


def compile_revised_application(application: AgentApplicationTrace) -> tuple[RevisedCall, ...]:
    operators = selected_native_operators()
    index_by_id = {call.call_id: call.index for call in application.calls}
    remaining = {
        program: sum(call.program_id == program for call in application.calls)
        for program in PROGRAM_CODE
    }
    seen: set[str] = set()
    calls: list[RevisedCall] = []
    for call in application.calls:
        deps_mask = 0
        for dependency in call.deps:
            deps_mask |= 1 << index_by_id[dependency]
        first = int(call.program_id not in seen)
        seen.add(call.program_id)
        remaining[call.program_id] -= 1
        last = int(remaining[call.program_id] == 0)
        plan = _flow_plan(call.priority)
        descriptors = _descriptor_template(operators, call.priority) if call.kind == "llm" else ()
        calls.append(
            RevisedCall(
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
                flow_class=str(plan["flow_class"]),
                flow_code=int(plan["flow_code"]),
                prefill_chunk_tokens=int(plan["prefill_chunk_tokens"]),
                decode_batch_cap=int(plan["decode_batch_cap"]),
                elastic_hptpe_percent=int(plan["elastic_hptpe_percent"]),
                descriptors=descriptors,
            )
        )
    return tuple(calls)


def _c_string(value: str) -> str:
    return json.dumps(value)


def render_header(application: AgentApplicationTrace, calls: tuple[RevisedCall, ...]) -> str:
    digest64 = int(application.output_digest[:16], 16)
    operators = selected_native_operators()
    mir_digest64 = int(operator_digest(operators)[:16], 16)
    lines = [
        "#pragma once",
        "",
        "#include <stdint.h>",
        "",
        f"#define AGENTSYS_REVISED_CALLS {len(calls)}",
        "#define AGENTSYS_REVISED_PROGRAMS 3",
        "#define AGENTSYS_REVISED_MAX_DESCRIPTORS 8",
        "#define AGENTSYS_REVISED_INPUT_BEATS 8",
        "#define AGENTSYS_REVISED_OUTPUT_BEATS 4",
        f"#define AGENTSYS_REVISED_TRACE_DIGEST UINT64_C(0x{digest64:016x})",
        f"#define AGENTSYS_REVISED_MIR_DIGEST UINT64_C(0x{mir_digest64:016x})",
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
        "  uint8_t flow_code; /* 0=reactive, 1=proactive */",
        "  uint8_t prefill_chunk_tokens;",
        "  uint8_t decode_batch_cap;",
        "  uint8_t elastic_hptpe_percent;",
        "  uint64_t control[AGENTSYS_REVISED_MAX_DESCRIPTORS];",
        "  uint64_t tilemem[AGENTSYS_REVISED_MAX_DESCRIPTORS];",
        "  uint16_t source_op[AGENTSYS_REVISED_MAX_DESCRIPTORS];",
        "  uint8_t placement[AGENTSYS_REVISED_MAX_DESCRIPTORS];",
        "  uint8_t stage[AGENTSYS_REVISED_MAX_DESCRIPTORS];",
        "} agentsys_revised_call_t;",
        "",
        "static const agentsys_revised_call_t agentsys_revised_calls[AGENTSYS_REVISED_CALLS] = {",
    ]
    for call in calls:
        controls = [descriptor.control for descriptor in call.descriptors]
        tilemem = [descriptor.tilemem for descriptor in call.descriptors]
        source_op = [descriptor.source_index for descriptor in call.descriptors]
        placement = [descriptor.placement_code for descriptor in call.descriptors]
        stage = [descriptor.stage_code for descriptor in call.descriptors]
        for values in (controls, tilemem, source_op, placement, stage):
            values.extend([0] * (8 - len(values)))
        lines.extend(
            (
                "  {",
                f"    {_c_string(call.call_id)}, {_c_string(call.program_id)}, {call.program_code}, "
                f"{1 if call.kind == 'tool' else 0}, {call.priority}, {len(call.descriptors)},",
                f"    UINT16_C(0x{call.deps_mask:04x}), {call.program_first}, {call.program_last}, "
                f"{call.input_tokens}, {call.output_tokens}, {call.tool_cycles},",
                f"    {call.flow_code}, {call.prefill_chunk_tokens}, {call.decode_batch_cap}, "
                f"{call.elastic_hptpe_percent},",
                "    {" + ", ".join(f"UINT64_C(0x{value:016x})" for value in controls) + "},",
                "    {" + ", ".join(f"UINT64_C(0x{value:016x})" for value in tilemem) + "},",
                "    {" + ", ".join(str(value) for value in source_op) + "},",
                "    {" + ", ".join(str(value) for value in placement) + "},",
                "    {" + ", ".join(str(value) for value in stage) + "}",
                "  },",
            )
        )
    lines.extend(("};", ""))
    return "\n".join(lines)


def compile_and_write_revised(
    *,
    header_path: Path = GENERATED_HEADER,
    manifest_path: Path = COMPILED_MANIFEST,
    application_path: Path = APPLICATION_TRACE,
    run_id: str = "run_027",
) -> dict[str, Any]:
    if _git_head(MLLM_ROOT) != UPSTREAM_MLLM_COMMIT:
        raise RuntimeError("mllm reference revision drift")
    application = run_agent_application(run_id=run_id)
    application_value = application.to_dict()
    application_path.parent.mkdir(parents=True, exist_ok=True)
    application_path.write_text(json.dumps(application_value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    calls = compile_revised_application(application)
    header = render_header(application, calls)
    header_path.parent.mkdir(parents=True, exist_ok=True)
    header_path.write_text(header, encoding="utf-8")
    operators = selected_native_operators()
    descriptors = [descriptor for call in calls for descriptor in call.descriptors]
    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "agentix_mllm_agentxpu_to_neutral_riscv_tisa_hptpe_compilation",
        "application": application_value,
        "application_trace": str(application_path.relative_to(PROJECT_ROOT)),
        "application_trace_sha256": hashlib.sha256(application_path.read_bytes()).hexdigest(),
        "mllm": {
            "commit": UPSTREAM_MLLM_COMMIT,
            "mir": str(UPSTREAM_MIR.relative_to(PROJECT_ROOT)),
            "mir_sha256": hashlib.sha256(UPSTREAM_MIR.read_bytes()).hexdigest(),
            "selected_source_indices": list(SELECTED_SOURCE_INDICES),
            "selected_operator_digest": operator_digest(operators),
            "selected_operators": [operator.to_dict() for operator in operators],
        },
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
            "descriptors": len(descriptors),
            "dependencies": sum(bool(call.deps_mask) for call in calls),
            "reactive_flows": sum(call.kind == "llm" and call.flow_code == 0 for call in calls),
            "proactive_flows": sum(call.kind == "llm" and call.flow_code == 1 for call in calls),
            "hptpe_descriptors": sum(descriptor.placement == "hptpe" for descriptor in descriptors),
            "vector_descriptors": sum(descriptor.placement == "vector" for descriptor in descriptors),
            "data_descriptors": sum(descriptor.placement == "data" for descriptor in descriptors),
            "preemptible_descriptors": sum(descriptor.preemptible for descriptor in descriptors),
            "native_engine_counts": {
                engine.value: sum(operator.engine is engine for operator in operators)
                for engine in (Engine.ME, Engine.VE, Engine.DE)
            },
            "pass": (
                len(calls) == 11
                and len(descriptors) == 80
                and sum(descriptor.placement == "hptpe" for descriptor in descriptors) == 30
                and sum(descriptor.placement == "vector" for descriptor in descriptors) == 30
                and sum(descriptor.placement == "data" for descriptor in descriptors) == 20
                and all(descriptor.preemptible for descriptor in descriptors)
            ),
        },
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest

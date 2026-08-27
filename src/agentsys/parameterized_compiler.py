from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .paths import resolve_chipyard_root
from .mllm_backend import MllmOperator, operator_digest, parse_mir
from .model import Engine
from .revised_system_compiler import (
    ENGINE_CODE,
    PLACEMENT,
    PLACEMENT_CODE,
    RevisedCall,
    RevisedDescriptor,
    _control_word,
    _tilemem_word,
)
from .workload import AgentWorkload, WorkloadModel


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _selected_operators(model: WorkloadModel) -> tuple[MllmOperator, ...]:
    operators = parse_mir(model.hardware_mir)
    by_index = {operator.index: operator for operator in operators}
    missing = set(model.selected_source_indices) - set(by_index)
    if missing:
        raise ValueError(
            f"model {model.model_id} selects missing MIR operators: {sorted(missing)}"
        )
    return tuple(by_index[index] for index in model.selected_source_indices)


def _flow_plan(workload: AgentWorkload, priority: int) -> dict[str, int | str]:
    config = workload.agentxpu_config
    reactive = priority == 0
    return {
        "flow_class": "reactive" if reactive else "proactive",
        "flow_code": 0 if reactive else 1,
        "prefill_chunk_tokens": config.heg_prefill_chunk_tokens,
        "decode_batch_cap": (
            config.max_reactive_decode_batch if reactive else config.max_decode_batch
        ),
        "elastic_hptpe_percent": int(round((1.0 - config.heg_igpu_prefill_share) * 100)),
    }


def _descriptor_template(
    workload: AgentWorkload,
    model: WorkloadModel,
    priority: int,
) -> tuple[RevisedDescriptor, ...]:
    operators = _selected_operators(model)
    selected_map = {operator.index: index for index, operator in enumerate(operators)}
    flow = _flow_plan(workload, priority)
    descriptors: list[RevisedDescriptor] = []
    for index, (operator, stage_code) in enumerate(zip(operators, model.stages, strict=True)):
        deps = 0
        for dependency in operator.deps:
            if dependency in selected_map:
                deps |= 1 << selected_map[dependency]
        duration = max(
            1,
            min(
                0xFFFF,
                math.ceil(operator.duration / model.duration_divisors[operator.engine.value]),
            ),
        )
        output = operator.outputs[0]
        placement_code = PLACEMENT_CODE[operator.engine]
        tilemem = _tilemem_word(
            int(output.ssa) * 0x100000,
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
                stage=f"stage_{stage_code}",
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


def compile_parameterized_calls(
    workload: AgentWorkload,
    application: dict[str, Any],
) -> tuple[RevisedCall, ...]:
    application_calls = application["calls"]
    index_by_id = {call["call_id"]: int(call["index"]) for call in application_calls}
    source_by_id = {call.call_id: call for call in workload.calls}
    remaining = {
        program.program_id: sum(call["program_id"] == program.program_id for call in application_calls)
        for program in workload.programs
    }
    seen: set[str] = set()
    calls: list[RevisedCall] = []
    for application_call in application_calls:
        source = source_by_id[application_call["call_id"]]
        deps_mask = 0
        for dependency in source.deps:
            deps_mask |= 1 << index_by_id[dependency]
        first = int(source.program_id not in seen)
        seen.add(source.program_id)
        remaining[source.program_id] -= 1
        last = int(remaining[source.program_id] == 0)
        plan = _flow_plan(workload, int(application_call["priority"]))
        descriptors: tuple[RevisedDescriptor, ...] = ()
        if source.kind == "llm":
            assert source.model_profile is not None
            descriptors = _descriptor_template(
                workload,
                workload.models_by_id[source.model_profile],
                int(application_call["priority"]),
            )
        calls.append(
            RevisedCall(
                index=int(application_call["index"]),
                call_id=source.call_id,
                program_id=source.program_id,
                program_code=workload.program_codes[source.program_id],
                kind=source.kind,
                priority=int(application_call["priority"]),
                deps_mask=deps_mask,
                program_first=first,
                program_last=last,
                input_tokens=source.input_tokens,
                output_tokens=source.output_tokens,
                tool_cycles=source.tool_cycles,
                flow_class=str(plan["flow_class"]),
                flow_code=int(plan["flow_code"]),
                prefill_chunk_tokens=int(plan["prefill_chunk_tokens"]),
                decode_batch_cap=int(plan["decode_batch_cap"]),
                elastic_hptpe_percent=int(plan["elastic_hptpe_percent"]),
                descriptors=descriptors,
            )
        )
    return tuple(calls)


def _summary(workload: AgentWorkload, calls: tuple[RevisedCall, ...]) -> dict[str, Any]:
    descriptors = [descriptor for call in calls for descriptor in call.descriptors]
    engine_descriptors = {
        engine: sum(descriptor.engine == engine for descriptor in descriptors)
        for engine in ("me", "ve", "de")
    }
    engine_busy = {
        engine: sum(
            descriptor.duration for descriptor in descriptors if descriptor.engine == engine
        )
        for engine in ("me", "ve", "de")
    }
    return {
        "programs": len(workload.programs),
        "calls": len(calls),
        "llm_calls": sum(call.kind == "llm" for call in calls),
        "tool_calls": sum(call.kind == "tool" for call in calls),
        "descriptors": len(descriptors),
        "dependencies": sum(bool(call.deps_mask) for call in calls),
        "reactive_flows": sum(call.kind == "llm" and call.flow_code == 0 for call in calls),
        "proactive_flows": sum(call.kind == "llm" and call.flow_code == 1 for call in calls),
        "hptpe_descriptors": engine_descriptors["me"],
        "vector_descriptors": engine_descriptors["ve"],
        "data_descriptors": engine_descriptors["de"],
        "me_busy": engine_busy["me"],
        "ve_busy": engine_busy["ve"],
        "de_busy": engine_busy["de"],
        "hptpe_mac_ops": engine_busy["me"] * workload.hardware.hptpe_lanes,
        "preemptible_descriptors": sum(descriptor.preemptible for descriptor in descriptors),
        "pass": (
            len(calls) == len(workload.calls)
            and len(descriptors)
            == sum(
                len(workload.models_by_id[call.model_profile].selected_source_indices)
                for call in workload.calls
                if call.kind == "llm" and call.model_profile is not None
            )
        ),
    }


def _selected_model_evidence(workload: AgentWorkload) -> tuple[dict[str, Any], int]:
    evidence: dict[str, Any] = {}
    selected_digests: dict[str, str] = {}
    for model in workload.models:
        operators = _selected_operators(model)
        digest = operator_digest(operators)
        selected_digests[model.model_id] = digest
        evidence[model.model_id] = {
            "hardware_mir": str(model.hardware_mir),
            "hardware_mir_sha256": hashlib.sha256(model.hardware_mir.read_bytes()).hexdigest(),
            "selected_source_indices": list(model.selected_source_indices),
            "selected_operator_digest": digest,
            "selected_operators": [operator.to_dict() for operator in operators],
            "duration_divisors": dict(model.duration_divisors),
            "stages": list(model.stages),
        }
    if len(selected_digests) == 1:
        digest64 = int(next(iter(selected_digests.values()))[:16], 16)
    else:
        combined = hashlib.sha256(
            json.dumps(selected_digests, sort_keys=True).encode()
        ).hexdigest()
        digest64 = int(combined[:16], 16)
    return evidence, digest64


def render_parameterized_header(
    workload: AgentWorkload,
    application: dict[str, Any],
    calls: tuple[RevisedCall, ...],
) -> str:
    summary = _summary(workload, calls)
    _model_evidence, mir_digest64 = _selected_model_evidence(workload)
    trace_digest64 = int(application["output_digest"][:16], 16)
    workload_digest64 = int(workload.sha256[:16], 16)
    trace_capacity = max(32, len(calls) * 16 + len(workload.programs) * 2 + 8)
    lines = [
        "#pragma once",
        "",
        "#include <stdint.h>",
        "",
        f'#define AGENTSYS_WORKLOAD_NAME "{workload.name}"',
        f"#define AGENTSYS_WORKLOAD_DIGEST UINT64_C(0x{workload_digest64:016x})",
        f"#define AGENTSYS_REVISED_CALLS {len(calls)}",
        f"#define AGENTSYS_REVISED_PROGRAMS {len(workload.programs)}",
        "#define AGENTSYS_REVISED_MAX_DESCRIPTORS 8",
        f"#define AGENTSYS_REVISED_INPUT_BEATS {workload.hardware.input_beats}",
        f"#define AGENTSYS_REVISED_OUTPUT_BEATS {workload.hardware.output_beats}",
        f"#define AGENTSYS_REVISED_TRACE_CAPACITY {trace_capacity}",
        f"#define AGENTSYS_REVISED_TRACE_DIGEST UINT64_C(0x{trace_digest64:016x})",
        f"#define AGENTSYS_REVISED_MIR_DIGEST UINT64_C(0x{mir_digest64:016x})",
        f"#define AGENTSYS_EXPECT_LLM_CALLS {summary['llm_calls']}",
        f"#define AGENTSYS_EXPECT_TOOL_CALLS {summary['tool_calls']}",
        f"#define AGENTSYS_EXPECT_DESCRIPTORS {summary['descriptors']}",
        f"#define AGENTSYS_EXPECT_REACTIVE_FLOWS {summary['reactive_flows']}",
        f"#define AGENTSYS_EXPECT_PROACTIVE_FLOWS {summary['proactive_flows']}",
        f"#define AGENTSYS_EXPECT_HPTPE_PLACEMENTS {summary['hptpe_descriptors']}",
        f"#define AGENTSYS_EXPECT_VECTOR_PLACEMENTS {summary['vector_descriptors']}",
        f"#define AGENTSYS_EXPECT_DATA_PLACEMENTS {summary['data_descriptors']}",
        f"#define AGENTSYS_EXPECT_ME_BUSY {summary['me_busy']}",
        f"#define AGENTSYS_EXPECT_VE_BUSY {summary['ve_busy']}",
        f"#define AGENTSYS_EXPECT_DE_BUSY {summary['de_busy']}",
        f"#define AGENTSYS_HPTPE_LANES {workload.hardware.hptpe_lanes}",
        "",
        "typedef struct {",
        "  const char *call_id;",
        "  const char *program_id;",
        "  uint8_t program_code;",
        "  uint8_t kind; /* 0=LLM/XPU, 1=CPU tool */",
        "  uint8_t priority;",
        "  uint8_t descriptor_count;",
        "  uint64_t deps_mask;",
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
        source_ops = [descriptor.source_index for descriptor in call.descriptors]
        placements = [descriptor.placement_code for descriptor in call.descriptors]
        stages = [descriptor.stage_code for descriptor in call.descriptors]
        for values in (controls, tilemem, source_ops, placements, stages):
            values.extend([0] * (8 - len(values)))
        lines.extend(
            (
                "  {",
                f"    {json.dumps(call.call_id)}, {json.dumps(call.program_id)}, "
                f"{call.program_code}, {1 if call.kind == 'tool' else 0}, "
                f"{call.priority}, {len(call.descriptors)},",
                f"    UINT64_C(0x{call.deps_mask:016x}), {call.program_first}, "
                f"{call.program_last}, {call.input_tokens}, {call.output_tokens}, "
                f"{call.tool_cycles},",
                f"    {call.flow_code}, {call.prefill_chunk_tokens}, "
                f"{call.decode_batch_cap}, {call.elastic_hptpe_percent},",
                "    {" + ", ".join(f"UINT64_C(0x{value:016x})" for value in controls) + "},",
                "    {" + ", ".join(f"UINT64_C(0x{value:016x})" for value in tilemem) + "},",
                "    {" + ", ".join(str(value) for value in source_ops) + "},",
                "    {" + ", ".join(str(value) for value in placements) + "},",
                "    {" + ", ".join(str(value) for value in stages) + "}",
                "  },",
            )
        )
    lines.extend(("};", ""))
    return "\n".join(lines)


def compile_parameterized_workload(
    workload: AgentWorkload,
    application: dict[str, Any],
    *,
    application_path: Path,
    manifest_path: Path,
    header_path: Path,
    run_id: str,
) -> dict[str, Any]:
    workload.hardware.require_installed_profile()
    if application["workload"]["sha256"] != workload.sha256:
        raise ValueError("application/workload identity mismatch")
    calls = compile_parameterized_calls(workload, application)
    summary = _summary(workload, calls)
    models, mir_digest64 = _selected_model_evidence(workload)
    header = render_parameterized_header(workload, application, calls)
    header_path.parent.mkdir(parents=True, exist_ok=True)
    header_path.write_text(header, encoding="utf-8")
    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "manifest_driven_agentix_mllm_agentxpu_tisa_hptpe_compilation",
        "workload": workload.to_contract_dict(),
        "application_trace": str(application_path),
        "application_trace_sha256": hashlib.sha256(application_path.read_bytes()).hexdigest(),
        "application_output_digest": application["output_digest"],
        "models": models,
        "mir_digest_hex": f"{mir_digest64:016x}",
        "hardware_calls": [
            {
                **{key: value for key, value in asdict(call).items() if key != "descriptors"},
                "descriptors": [asdict(descriptor) for descriptor in call.descriptors],
            }
            for call in calls
        ],
        "generated_header": str(header_path),
        "generated_header_sha256": hashlib.sha256(header.encode()).hexdigest(),
        "expectations": {
            "dynamic_faster": workload.expectations.dynamic_faster,
            "require_static_overlap": workload.expectations.require_static_overlap,
            "backend_speedup_range": (
                list(workload.expectations.backend_speedup_range)
                if workload.expectations.backend_speedup_range is not None
                else None
            ),
        },
        "summary": summary,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def build_parameterized_elf(
    header_path: Path,
    elf_path: Path,
    *,
    chipyard_root: Path | None = None,
) -> dict[str, Any]:
    chipyard_root = chipyard_root or resolve_chipyard_root()
    compiler = chipyard_root / "esp-tools-install/bin/riscv64-unknown-elf-gcc"
    source = PROJECT_ROOT / "system_sim/software/agentsys_revised_system_test.c"
    runtime = PROJECT_ROOT / "system_sim/software/agentsys_xpu_runtime.h"
    if not compiler.is_file() or not os.access(compiler, os.X_OK):
        raise FileNotFoundError(compiler)
    for path in (header_path, source, runtime):
        if not path.is_file():
            raise FileNotFoundError(path)
    elf_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        str(compiler),
        "-std=gnu99",
        "-O2",
        "-g",
        "-fno-common",
        "-fno-builtin-printf",
        "-Wall",
        "-Wextra",
        f"-I{chipyard_root / 'tests'}",
        f"-I{PROJECT_ROOT / 'system_sim/software'}",
        f'-DAGENTSYS_REVISED_TRACE_HEADER="{header_path.resolve()}"',
        str(source),
        "-static",
        "-specs=htif_nano.specs",
        "-o",
        str(elf_path),
    ]
    process = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if process.returncode != 0:
        raise RuntimeError(f"RISC-V workload ELF build failed:\n{process.stdout}")
    return {
        "classification": "parameterized_workload_riscv_elf_build",
        "command": command,
        "exit_code": process.returncode,
        "output": process.stdout,
        "elf": str(elf_path),
        "elf_bytes": elf_path.stat().st_size,
        "elf_sha256": hashlib.sha256(elf_path.read_bytes()).hexdigest(),
        "header": str(header_path),
        "header_sha256": hashlib.sha256(header_path.read_bytes()).hexdigest(),
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "runtime_sha256": hashlib.sha256(runtime.read_bytes()).hexdigest(),
        "pass": elf_path.is_file() and elf_path.stat().st_size > 0,
    }

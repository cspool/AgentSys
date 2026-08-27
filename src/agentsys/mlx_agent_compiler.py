from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from .mlx_reference import DEFAULT_CONFIG as DEFAULT_SOURCE_CONFIG
from .workload import AgentWorkload, PROJECT_ROOT


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_sha(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _source_for_micro_op(
    operation: str,
    ordinal: int,
    selected: list[dict[str, Any]],
    counters: dict[str, int],
) -> dict[str, Any]:
    by_index = {int(item["index"]): item for item in selected}
    if operation == "fma":
        sources = (10, 11, 12)
        source_index = sources[counters.get("fma", 0) % len(sources)]
        counters["fma"] = counters.get("fma", 0) + 1
    elif operation == "mul":
        sources = (6, 8)
        source_index = sources[counters.get("mul", 0) % len(sources)]
        counters["mul"] = counters.get("mul", 0) + 1
    elif operation == "add":
        source_index = 7
    elif operation in {"max", "exp"}:
        source_index = 6
    elif operation == "div":
        source_index = 8
    elif operation == "shuffle":
        source_index = 13
    elif operation in {"xfer", "store"}:
        source_index = 14
    elif operation == "load":
        source_index = int(selected[ordinal % len(selected)]["index"])
    else:
        raise ValueError(f"unmapped MLX operation: {operation}")
    if source_index not in by_index:
        source_index = int(selected[ordinal % len(selected)]["index"])
    return by_index[source_index]


def _micro_lineage(
    template: dict[str, Any], selected: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    counters: dict[str, int] = {}
    result: list[dict[str, Any]] = []
    for ordinal, entry in enumerate(template["lineage"]):
        source = _source_for_micro_op(
            str(entry["normalized"]["op"]), ordinal, selected, counters
        )
        result.append(
            {
                "micro_index": ordinal,
                "pe": int(entry["pe"]),
                "pc": int(entry["index"]),
                "word": entry["word"],
                "mlx_operation": entry["normalized"]["op"],
                "mlx_tag": int(entry["normalized"]["tag"]),
                "route_dx": int(entry["normalized"]["dx"]),
                "route_dy": int(entry["normalized"]["dy"]),
                "mir_source_index": int(source["index"]),
                "mir_op_type": source["op_type"],
                "tisa_engine": source["engine"],
            }
        )
    return result


def render_agent_header(
    workload: AgentWorkload,
    application: dict[str, Any],
    compiled: dict[str, Any],
) -> str:
    compiled_by_id = {call["call_id"]: call for call in compiled["hardware_calls"]}
    source_by_id = {call.call_id: call for call in workload.calls}
    workload_digest = int(workload.sha256[:16], 16)
    app_digest = int(application["output_digest"][:16], 16)
    mir_digest = int(compiled["mir_digest_hex"], 16)
    calls = application["calls"]
    llm_calls = sum(source_by_id[call["call_id"]].kind == "llm" for call in calls)
    tool_calls = len(calls) - llm_calls
    lines = [
        "#pragma once",
        "",
        "#include <stdint.h>",
        "",
        f'#define AGENTSYS_MLX_WORKLOAD_NAME "{workload.name}"',
        f"#define AGENTSYS_MLX_WORKLOAD_DIGEST UINT64_C(0x{workload_digest:016x})",
        f"#define AGENTSYS_MLX_APP_DIGEST UINT64_C(0x{app_digest:016x})",
        f"#define AGENTSYS_MLX_MIR_DIGEST UINT64_C(0x{mir_digest:016x})",
        f"#define AGENTSYS_MLX_PROGRAMS {len(workload.programs)}u",
        f"#define AGENTSYS_MLX_CALLS {len(calls)}u",
        f"#define AGENTSYS_MLX_EXPECT_LLM_CALLS {llm_calls}u",
        f"#define AGENTSYS_MLX_EXPECT_TOOL_CALLS {tool_calls}u",
        f"#define AGENTSYS_MLX_EXPECT_COMPLETED_MASK UINT64_C(0x{((1 << len(calls)) - 1):016x})",
        "",
        "typedef struct {",
        "  const char *call_id;",
        "  const char *program_id;",
        "  uint8_t index;",
        "  uint8_t kind; /* 0=LLM/MLX, 1=CPU tool */",
        "  uint8_t priority;",
        "  uint8_t program_first;",
        "  uint8_t program_last;",
        "  uint8_t flow_code;",
        "  uint8_t prefill_chunk_tokens;",
        "  uint8_t decode_batch_cap;",
        "  uint16_t input_tokens;",
        "  uint16_t output_tokens;",
        "  uint16_t tool_cycles;",
        "  uint64_t deps_mask;",
        "} agentsys_mlx_call_t;",
        "",
        "static const agentsys_mlx_call_t agentsys_mlx_calls[AGENTSYS_MLX_CALLS] = {",
    ]
    for call in calls:
        source = source_by_id[call["call_id"]]
        lowered = compiled_by_id[source.call_id]
        lines.extend(
            [
                "  {",
                f"    {json.dumps(source.call_id)}, {json.dumps(source.program_id)},",
                f"    {int(call['index'])}, {1 if source.kind == 'tool' else 0}, {int(call['priority'])},",
                f"    {int(lowered['program_first'])}, {int(lowered['program_last'])}, {int(lowered['flow_code'])},",
                f"    {int(lowered['prefill_chunk_tokens'])}, {int(lowered['decode_batch_cap'])},",
                f"    {source.input_tokens}, {source.output_tokens}, {source.tool_cycles},",
                f"    UINT64_C(0x{int(lowered['deps_mask']):016x})",
                "  },",
            ]
        )
    lines.extend(["};", ""])
    return "\n".join(lines)


def compile_agent_mlx(
    workload: AgentWorkload,
    application: dict[str, Any],
    compiled: dict[str, Any],
    *,
    application_path: Path,
    compiled_path: Path,
    header_path: Path,
    manifest_path: Path,
    source_config_path: Path = DEFAULT_SOURCE_CONFIG,
    run_id: str,
) -> dict[str, Any]:
    if {
        workload.sha256,
        application["workload"]["sha256"],
        compiled["workload"]["sha256"],
    } != {workload.sha256}:
        raise ValueError("Agent/application/compiled identity mismatch")
    source_config = json.loads(source_config_path.read_text(encoding="utf-8"))
    source_root = (PROJECT_ROOT / source_config["active_path"]).resolve()
    system_manifest_path = (
        source_root / "artifacts/environment/h205/mlx-system-workload-manifest.json"
    )
    system_manifest = json.loads(system_manifest_path.read_text(encoding="utf-8"))
    template = next(
        item for item in system_manifest["workloads"] if item["name"] == "transformer_block"
    )
    model_id = workload.models[0].model_id
    selected = compiled["models"][model_id]["selected_operators"]
    lineage = _micro_lineage(template, selected)
    selected_indices = {int(item["index"]) for item in selected}
    mapped_indices = {int(item["mir_source_index"]) for item in lineage}
    header = render_agent_header(workload, application, compiled)
    header_path.parent.mkdir(parents=True, exist_ok=True)
    header_path.write_text(header, encoding="utf-8")
    source_by_id = {call.call_id: call for call in workload.calls}
    compiled_by_id = {call["call_id"]: call for call in compiled["hardware_calls"]}
    calls = []
    for app_call in application["calls"]:
        source = source_by_id[app_call["call_id"]]
        lowered = compiled_by_id[source.call_id]
        calls.append(
            {
                "index": int(app_call["index"]),
                "call_id": source.call_id,
                "program_id": source.program_id,
                "kind": source.kind,
                "priority": int(app_call["priority"]),
                "deps": list(source.deps),
                "deps_mask": int(lowered["deps_mask"]),
                "program_first": int(lowered["program_first"]),
                "program_last": int(lowered["program_last"]),
                "input_tokens": source.input_tokens,
                "output_tokens": source.output_tokens,
                "tool_cycles": source.tool_cycles,
                "agentxpu": {
                    "flow_class": lowered["flow_class"],
                    "flow_code": int(lowered["flow_code"]),
                    "prefill_chunk_tokens": int(lowered["prefill_chunk_tokens"]),
                    "decode_batch_cap": int(lowered["decode_batch_cap"]),
                    "elastic_hptpe_percent_source_field": int(
                        lowered["elastic_hptpe_percent"]
                    ),
                },
                "tisa_descriptors": lowered["descriptors"],
                "mlx": (
                    {
                        "template": "transformer_block",
                        "micro_ops": len(lineage),
                        "micro_lineage_sha256": _canonical_sha(lineage),
                        "instructions": int(template["instruction_count"]),
                        "active_pes": int(template["active_pes"]),
                        "input_vectors": int(template["input_vectors"]),
                        "output_vectors": int(template["output_vectors"]),
                        "dma_bytes": 64
                        * (int(template["input_vectors"]) + int(template["output_vectors"])),
                    }
                    if source.kind == "llm"
                    else None
                ),
            }
        )
    llm_calls = sum(call["kind"] == "llm" for call in calls)
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "agentix_mllm_agentxpu_tisa_to_mlx_spatial_compilation",
        "evidence_boundary": (
            "AgentSys maps upstream mllm/TISA identities onto a qualified MLX "
            "template; this is not an MLX_dev-provided Agent compiler"
        ),
        "workload": workload.to_contract_dict(),
        "lineage": {
            "application": {"path": str(application_path), "sha256": _sha256(application_path)},
            "compiled_tisa": {"path": str(compiled_path), "sha256": _sha256(compiled_path)},
            "mlx_source_config": {
                "path": str(source_config_path),
                "sha256": _sha256(source_config_path),
                "commit": source_config["active_commit"],
            },
            "mlx_system_manifest": {
                "path": str(system_manifest_path),
                "sha256": _sha256(system_manifest_path),
            },
            "mlx_template": {
                "header": str(source_root / template["header"]),
                "header_sha256": template["header_sha256"],
                "program": str(source_root / template["program"]),
                "program_sha256": template["program_sha256"],
                "input": str(source_root / template["input_hex"]),
                "input_sha256": template["input_hex_sha256"],
                "golden": str(source_root / template["golden_hex"]),
                "golden_sha256": template["golden_hex_sha256"],
            },
        },
        "model": {
            "id": model_id,
            "selected_operators": selected,
            "selected_source_indices": sorted(selected_indices),
        },
        "micro_lineage": lineage,
        "micro_lineage_sha256": _canonical_sha(lineage),
        "calls": calls,
        "generated_header": {"path": str(header_path), "sha256": _sha256(header_path)},
        "gates": {
            "identity": True,
            "template_qualified": int(template["instruction_count"]) == 45
            and int(template["active_pes"]) == 9
            and int(template["input_vectors"]) == 8
            and int(template["output_vectors"]) == 1,
            "all_micro_ops_lineaged": len(lineage) == int(template["instruction_count"]),
            "all_mir_sources_covered": mapped_indices == selected_indices,
            "all_calls_compiled": len(calls) == len(workload.calls),
        },
        "summary": {
            "programs": len(workload.programs),
            "calls": len(calls),
            "llm_calls": llm_calls,
            "tool_calls": len(calls) - llm_calls,
            "mir_sources_per_llm": len(selected),
            "mlx_micro_ops_per_llm": len(lineage),
            "mlx_micro_ops": llm_calls * len(lineage),
            "mlx_instructions": llm_calls * int(template["instruction_count"]),
            "mlx_dma_bytes": llm_calls
            * 64
            * (int(template["input_vectors"]) + int(template["output_vectors"])),
            "pass": True,
        },
    }
    result["summary"]["pass"] = all(result["gates"].values())
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def build_agent_mlx_elf(
    *,
    agent_header: Path,
    mlx_manifest: dict[str, Any],
    elf_path: Path,
    source_config_path: Path = DEFAULT_SOURCE_CONFIG,
) -> dict[str, Any]:
    source_config = json.loads(source_config_path.read_text(encoding="utf-8"))
    source_root = (PROJECT_ROOT / source_config["active_path"]).resolve()
    chipyard = Path(source_config["chipyard"]["path"])
    compiler = chipyard / "esp-tools-install/bin/riscv64-unknown-elf-gcc"
    source = PROJECT_ROOT / "system_sim/software/agentsys_mlx_agent.c"
    runtime_root = source_root / "system_sim/software"
    template_header = Path(mlx_manifest["lineage"]["mlx_template"]["header"])
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
        f"-I{chipyard / 'tests'}",
        f"-I{runtime_root}",
        f"-I{agent_header.parent}",
        f"-I{template_header.parent}",
        f'-DAGENTSYS_MLX_AGENT_HEADER="{agent_header.resolve()}"',
        f'-DMLX_WORKLOAD_HEADER="{template_header.name}"',
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
        raise RuntimeError(f"Agent MLX ELF build failed:\n{process.stdout}")
    return {
        "classification": "agent_dag_ordinary_riscv_mlx_elf_build",
        "command": command,
        "exit_code": process.returncode,
        "output": process.stdout,
        "elf": str(elf_path),
        "bytes": elf_path.stat().st_size,
        "sha256": _sha256(elf_path),
        "source_sha256": _sha256(source),
        "agent_header_sha256": _sha256(agent_header),
        "template_header_sha256": _sha256(template_header),
        "pass": elf_path.is_file() and elf_path.stat().st_size > 0,
    }

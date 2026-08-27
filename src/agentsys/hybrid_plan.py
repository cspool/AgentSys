from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any

from .workload import AgentWorkload, PROJECT_ROOT


DEFAULT_CONFIG = PROJECT_ROOT / "config/hybrid-system.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonical_sha(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _wave_by_call(workload: AgentWorkload) -> dict[str, int]:
    calls = {call.call_id: call for call in workload.calls}
    waves: dict[str, int] = {}

    def visit(call_id: str) -> int:
        if call_id in waves:
            return waves[call_id]
        call = calls[call_id]
        wave = 0 if not call.deps else 1 + max(visit(dep) for dep in call.deps)
        waves[call_id] = wave
        return wave

    for call in workload.calls:
        visit(call.call_id)
    return waves


def _matrix_size(input_tokens: int, adapter: dict[str, Any]) -> int:
    buckets = math.ceil(input_tokens / int(adapter["token_quantum"]))
    return min(
        int(adapter["matrix_max"]),
        int(adapter["matrix_base"]) + int(adapter["matrix_step"]) * buckets,
    )


def _llm_rank(ordinal: int, placement: str) -> int:
    if placement == "round_robin":
        return ordinal % 2
    if placement == "gpu0_only":
        return 0
    if placement == "gpu1_only":
        return 1
    raise ValueError(f"unsupported native GPU placement: {placement}")


def compile_hybrid_plan(
    workload: AgentWorkload,
    *,
    application_path: Path,
    compiled_path: Path,
    header_path: Path,
    elf_path: Path,
    config_path: Path = DEFAULT_CONFIG,
    placement: str | None = None,
    run_id: str,
) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("schema_version") != 1:
        raise ValueError("unsupported hybrid-system configuration")
    placement = placement or str(config["placement"])
    application = json.loads(application_path.read_text(encoding="utf-8"))
    compiled = json.loads(compiled_path.read_text(encoding="utf-8"))
    identities = {
        workload.sha256,
        application["workload"]["sha256"],
        compiled["workload"]["sha256"],
    }
    if len(identities) != 1:
        raise ValueError("workload/application/compiled identity mismatch")
    if not header_path.is_file() or not elf_path.is_file():
        raise FileNotFoundError("hybrid plan requires the generated header and RISC-V ELF")

    gpu_config_path = (PROJECT_ROOT / config["gpu_runtime"]).resolve()
    gpu_config = json.loads(gpu_config_path.read_text(encoding="utf-8"))
    if len(gpu_config["gpus"]) != 2:
        raise ValueError("hybrid plan requires exactly two GPU ranks")
    mllm_audit_path = (PROJECT_ROOT / config["mllm_cuda_audit"]).resolve()
    mllm_audit = json.loads(mllm_audit_path.read_text(encoding="utf-8"))
    if not mllm_audit["summary"]["pass"]:
        raise ValueError("pinned mllm CUDA lifecycle audit is not passing")

    source_calls = {call.call_id: call for call in workload.calls}
    compiled_calls = {
        call["call_id"]: call for call in compiled["hardware_calls"]
    }
    model_ops = {
        model_id: model["selected_operators"]
        for model_id, model in compiled["models"].items()
    }
    waves = _wave_by_call(workload)
    adapter = config["adapter"]
    planned: list[dict[str, Any]] = []
    ranks: dict[str, int] = {}
    llm_ordinal = 0
    for application_call in application["calls"]:
        call_id = application_call["call_id"]
        source = source_calls[call_id]
        compiled_call = compiled_calls[call_id]
        if source.kind == "llm":
            rank = _llm_rank(llm_ordinal, placement)
            llm_ordinal += 1
        elif source.deps:
            rank = ranks[source.deps[0]]
        else:
            rank = int(application_call["index"]) % 2
        ranks[call_id] = rank
        gpu = gpu_config["gpus"][rank]
        operators = (
            model_ops[source.model_profile] if source.kind == "llm" else []
        )
        descriptors = compiled_call["descriptors"]
        planned.append(
            {
                "index": int(application_call["index"]),
                "call_id": call_id,
                "program_id": source.program_id,
                "kind": source.kind,
                "priority": int(application_call["priority"]),
                "deps": list(source.deps),
                "deps_mask": int(compiled_call["deps_mask"]),
                "wave": waves[call_id],
                "input_tokens": source.input_tokens,
                "output_tokens": source.output_tokens,
                "model": source.model_profile,
                "tool": source.tool_kind,
                "native": {
                    "rank": rank,
                    "device": int(gpu["device"]),
                    "numa_node": int(gpu["numa_node"]),
                    "cpu_affinity": gpu["cpu_affinity"],
                    "matrix_size": (
                        _matrix_size(source.input_tokens, adapter)
                        if source.kind == "llm"
                        else int(adapter["cpu_matrix_size"])
                    ),
                    "dtype": adapter["dtype"] if source.kind == "llm" else "float32",
                    "adapter": (
                        "agentsys_mir_cuda_operator_adapter"
                        if source.kind == "llm"
                        else "agentsys_numa_cpu_tool_adapter"
                    ),
                },
                "mir_operators": operators,
                "xpu": {
                    "descriptors": descriptors,
                    "descriptor_digest": _canonical_sha(descriptors),
                    "flow_class": compiled_call["flow_class"],
                    "prefill_chunk_tokens": compiled_call["prefill_chunk_tokens"],
                    "decode_batch_cap": compiled_call["decode_batch_cap"],
                    "elastic_hptpe_percent": compiled_call[
                        "elastic_hptpe_percent"
                    ],
                },
            }
        )

    operator_counts = {
        engine: sum(
            operator["engine"] == engine
            for call in planned
            for operator in call["mir_operators"]
        )
        for engine in ("me", "ve", "de")
    }
    llm_calls = sum(call["kind"] == "llm" for call in planned)
    tool_calls = len(planned) - llm_calls
    per_rank_llm = [
        sum(call["kind"] == "llm" and call["native"]["rank"] == rank for call in planned)
        for rank in range(2)
    ]
    summary = {
        "programs": len(workload.programs),
        "calls": len(planned),
        "llm_calls": llm_calls,
        "tool_calls": tool_calls,
        "waves": max(waves.values()) + 1,
        "mir_operators": sum(operator_counts.values()),
        "me_operators": operator_counts["me"],
        "ve_operators": operator_counts["ve"],
        "de_operators": operator_counts["de"],
        "xpu_descriptors": sum(len(call["xpu"]["descriptors"]) for call in planned),
        "gpu_rank_llm_calls": per_rank_llm,
        "gpu_ranks_used": sum(value > 0 for value in per_rank_llm),
        "pass": len(planned) == len(workload.calls)
        and sum(operator_counts.values()) == llm_calls * 8
        and operator_counts
        == {"me": llm_calls * 3, "ve": llm_calls * 3, "de": llm_calls * 2},
    }
    body = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "agent_dag_mllm_mir_to_native_gpu_and_tisa_hptpe_plan",
        "evidence_boundary": (
            "AgentSys MIR-to-CUDA adapter plus upstream mllm lifecycle scaffold; "
            "local RTX4090 execution is not A100 paper reproduction"
        ),
        "configuration": {
            "path": str(config_path),
            "sha256": _sha256(config_path),
            "placement": placement,
            "adapter": adapter,
            "gpu_runtime_path": str(gpu_config_path),
            "gpu_runtime_sha256": _sha256(gpu_config_path),
        },
        "workload": workload.to_contract_dict(),
        "lineage": {
            "application": {"path": str(application_path), "sha256": _sha256(application_path)},
            "compiled": {"path": str(compiled_path), "sha256": _sha256(compiled_path)},
            "generated_header": {"path": str(header_path), "sha256": _sha256(header_path)},
            "riscv_elf": {"path": str(elf_path), "sha256": _sha256(elf_path)},
            "mllm_cuda_audit": {
                "path": str(mllm_audit_path),
                "sha256": _sha256(mllm_audit_path),
                "summary": mllm_audit["summary"],
                "source_boundary": mllm_audit["source_boundary"]["classification"],
                "framework_patch_sha256": mllm_audit["framework_patch"]["sha256"],
            },
        },
        "calls": planned,
        "summary": summary,
    }
    return {**body, "plan_sha256": _canonical_sha(body)}


def write_hybrid_plan(path: Path, *args: Any, **kwargs: Any) -> dict[str, Any]:
    result = compile_hybrid_plan(*args, **kwargs)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result

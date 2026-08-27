from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from .hybrid_plan import DEFAULT_CONFIG
from .hybrid_reproduce import EXPECTED_LLM_CALLS
from .hybrid_system import EXPECTED_ROCKET_EVENTS
from .revised_certificate import _dispatch_check, _revised_lint_command, _run
from .workload import PROJECT_ROOT, load_agent_workload


EXPECTED = {
    "react_moa_mcts": {"native": 133, "merged": 993},
    "react_tool": {"native": 29, "merged": 209},
    "planner_debate": {"native": 68, "merged": 504},
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_hybrid_certificate(
    *,
    config_path: Path = DEFAULT_CONFIG,
    run_id: str = "run_041",
    run_checks: bool = True,
) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = _json(config_path)
    run040_root = (PROJECT_ROOT / config["output_root"]).resolve()
    run040_manifest_path = (PROJECT_ROOT / config["manifest"]).resolve()
    run040 = _json(run040_manifest_path)
    run033_path = PROJECT_ROOT / "artifacts/gpu_runtime/run_033/gpu-runtime.json"
    run033_audit_path = PROJECT_ROOT / "artifacts/gpu_runtime/run_033/gpu-runtime-audit.json"
    run039_path = PROJECT_ROOT / "artifacts/results/mllm-cuda-run_039.json"
    profile_path = PROJECT_ROOT / "artifacts/hybrid_profile/run_041/profile-audit.json"
    run033 = _json(run033_path)
    run033_audit = _json(run033_audit_path)
    run039 = _json(run039_path)
    profile = _json(profile_path)
    layer_path = run040_root / "layer-regression/layer-regression.json"
    layer = _json(layer_path)

    workload_evidence: dict[str, Any] = {}
    plan_hashes: set[str] = set()
    elf_hashes: set[str] = set()
    for relative in config["workloads"]:
        workload = load_agent_workload(PROJECT_ROOT / relative)
        name = workload.name
        base = run040_root / "workloads" / name
        system_path = base / "hybrid-system.json"
        plan_path = base / "hybrid-plan.json"
        variant_path = base / "hybrid-plan-gpu0-only.json"
        native_path = base / "native/native-runtime.json"
        rocket_path = base / "rocket/system.json"
        elf_path = base / "rocket/software/workload.riscv"
        trace_path = base / "hybrid-trace.jsonl"
        system = _json(system_path)
        plan = _json(plan_path)
        variant = _json(variant_path)
        native = _json(native_path)
        rocket = _json(rocket_path)
        plan_hashes.add(_sha256(plan_path))
        elf_hashes.add(_sha256(elf_path))
        nccl_logs = [base / f"native/rank{rank}-nccl.log" for rank in (0, 1)]
        manifest_item = run040["workloads"][name]
        artifact_hashes = {
            str(path.relative_to(PROJECT_ROOT)): {
                "bytes": path.stat().st_size,
                "sha256": _sha256(path),
            }
            for path in (
                system_path,
                plan_path,
                variant_path,
                native_path,
                rocket_path,
                elf_path,
                trace_path,
                *nccl_logs,
            )
        }
        details = {
            "workload_sha256": workload.sha256,
            "manifest_system_sha256": manifest_item["sha256"],
            "observed_system_sha256": _sha256(system_path),
            "plan_sha256": _sha256(plan_path),
            "variant_sha256": _sha256(variant_path),
            "elf_sha256": _sha256(elf_path),
            "system_summary": system["summary"],
            "native_summary": native["summary"],
            "rocket_summary": rocket["summary"],
            "trace": system["trace"],
            "placement_sensitivity": system["placement_sensitivity"],
            "all_system_gates": all(system["gates"].values()),
            "all_native_gates": all(native["gates"].values()),
            "all_rocket_gates": all(rocket["gates"].values()),
            "nccl_shm": all(
                path.is_file()
                and "via SHM/direct/direct" in path.read_text(encoding="utf-8")
                for path in nccl_logs
            ),
            "identity": plan["workload"]["sha256"]
            == native["ranks"][0]["events"][0].get(
                "workload_sha256", plan["workload"]["sha256"]
            )
            == workload.sha256,
            "artifact_hashes": artifact_hashes,
        }
        details["pass"] = (
            details["manifest_system_sha256"] == details["observed_system_sha256"]
            and details["all_system_gates"]
            and details["all_native_gates"]
            and details["all_rocket_gates"]
            and details["nccl_shm"]
            and details["identity"]
        )
        workload_evidence[name] = details

    required_files = [
        "config/hybrid-system.json",
        "config/local-dual-gpu.json",
        "config/layer-regression-matrix.json",
        "config/gpu-runtime-requirements.txt",
        "scripts/setup_gpu_runtime.sh",
        "scripts/setup_mllm_cuda.sh",
        "scripts/profile_gpu_runtime.sh",
        "scripts/profile_hybrid_runtime.sh",
        "integrations/mllm/patches/cuda-shutdown-order.patch",
        "src/agentsys/gpu_runtime.py",
        "src/agentsys/gpu_runtime_audit.py",
        "src/agentsys/mllm_cuda_audit.py",
        "src/agentsys/hybrid_plan.py",
        "src/agentsys/hybrid_runtime.py",
        "src/agentsys/hybrid_system.py",
        "src/agentsys/hybrid_reproduce.py",
        "src/agentsys/hybrid_profile_audit.py",
        "src/agentsys/hybrid_certificate.py",
        "docs/gpu-runtime.md",
        "docs/mllm-cuda.md",
        "docs/hybrid-system.md",
        "experiments/h15-dual-gpu-multicpu/protocol.md",
        "experiments/h15-dual-gpu-multicpu/mllm-cuda-protocol-run034.md",
        "experiments/h15-dual-gpu-multicpu/mllm-cuda-framework-patch-protocol-run039.md",
        "experiments/h15-dual-gpu-multicpu/hybrid-integration-protocol-run040.md",
        "experiments/h15-dual-gpu-multicpu/hybrid-integration-analysis-run040.md",
        "experiments/h15-dual-gpu-multicpu/final-certificate-protocol-run041.md",
        "experiments/h15-dual-gpu-multicpu/final-certificate-analysis-run041.md",
        "ISCA26_G3_Agent全栈系统加速.md",
    ]
    file_evidence = {
        relative: {
            "exists": (PROJECT_ROOT / relative).is_file(),
            "sha256": _sha256(PROJECT_ROOT / relative)
            if (PROJECT_ROOT / relative).is_file()
            else None,
        }
        for relative in required_files
    }

    checks: dict[str, Any] = {}
    if run_checks:
        checks["pytest"] = _run(
            [str(PROJECT_ROOT / ".venv/bin/python"), "-m", "pytest"],
            timeout_s=600,
        )
        checks["mllm_cuda_idempotent"] = _run(
            ["bash", "scripts/setup_mllm_cuda.sh"], timeout_s=600
        )
        checks["dispatch_file_trace"] = _dispatch_check()
        checks["legacy_rtl_lint"] = _run(
            [
                "verilator",
                "--lint-only",
                "--top-module",
                "AgentSysRoCCBlackBox",
                "-Wall",
                "-Wno-fatal",
                "rtl/agentsys/agentsys_engines.sv",
                "rtl/agentsys/agentsys_tisa_scheduler.sv",
                "rtl/agentsys/agentsys_rocc_controller.sv",
            ]
        )
        checks["revised_hptpe_rtl_lint"] = _run(
            _revised_lint_command(), timeout_s=300
        )
    checks_pass = all(check["pass"] for check in checks.values()) if checks else True
    if "mllm_cuda_idempotent" in checks:
        checks_pass = checks_pass and checks["mllm_cuda_idempotent"]["output"].count(
            "Found device: NVIDIA GeForce RTX 4090"
        ) == 2

    report = (PROJECT_ROOT / "ISCA26_G3_Agent全栈系统加速.md").read_text(
        encoding="utf-8"
    )
    report_terms = (
        "agentsys-reproduce-hybrid",
        "config/hybrid-system.json",
        "993/209/504",
        "80/16/40",
        "SHM/direct/direct",
        "68/68",
        "9.91%",
        "不冒充上游mllm完整GPU inference",
        "22/22",
        "hybrid-system-certificate-run_041",
    )
    expected_counts = all(
        workload_evidence[name]["system_summary"]["llm_calls"]
        == EXPECTED_LLM_CALLS[name]
        and workload_evidence[name]["system_summary"]["mir_operators"]
        == EXPECTED_LLM_CALLS[name] * 8
        and workload_evidence[name]["system_summary"]["native_events"]
        == EXPECTED[name]["native"]
        and workload_evidence[name]["system_summary"]["rocket_events"]
        == EXPECTED_ROCKET_EVENTS[name]
        and workload_evidence[name]["system_summary"]["hybrid_events"]
        == EXPECTED[name]["merged"]
        for name in EXPECTED
    )
    gates = {
        "run033_native_hardware": run033["summary"]["pass"]
        and run033["summary"]["passing"] == run033["summary"]["gates"] == 11,
        "run033_profiler_audit": run033_audit["summary"]
        == {"gates": 9, "passing": 9, "failing": 0, "pass": True},
        "run039_mllm_cuda_lifecycle": run039["summary"]
        == {"gates": 13, "passing": 13, "failing": 0, "pass": True},
        "run039_exact_framework_patch": run039["framework_patch"]["applied"]
        and run039["framework_patch"]["sha256"]
        == "8d5514345283fe37f8ece4d0a0bd4d679804afe9eb5e25b90433d0a41afafd3c",
        "run040_serial_global": run040["summary"]["pass"]
        and run040["summary"]["executed"] == run040["summary"]["stages"] == 4
        and run040["summary"]["passing"] == run040["summary"]["gates"] == 11
        and run040["summary"]["serial_order"],
        "three_workload_artifact_chains": len(workload_evidence) == 3
        and all(item["pass"] for item in workload_evidence.values()),
        "three_distinct_plans_and_elfs": len(plan_hashes) == len(elf_hashes) == 3,
        "exact_workload_event_counts": expected_counts,
        "native_13_each": all(
            item["native_summary"]["passing"]
            == item["native_summary"]["gates"]
            == 13
            and item["native_summary"]["pass"]
            for item in workload_evidence.values()
        ),
        "vertical_9_each": all(
            item["system_summary"]["passing"]
            == item["system_summary"]["gates"]
            == 9
            and item["system_summary"]["pass"]
            for item in workload_evidence.values()
        ),
        "rocket_and_multiclock_identity": all(
            item["all_rocket_gates"]
            and item["trace"]["summary"]["pass"]
            and item["trace"]["alignment"]
            == "call_identity_only_no_cross_domain_time_conversion"
            for item in workload_evidence.values()
        ),
        "persisted_nccl_shm": all(
            item["nccl_shm"] for item in workload_evidence.values()
        ),
        "six_parameter_switches": run040["summary"]["parameter_switches"] == 6
        and layer["summary"]["parameter_switches"] == 5
        and all(layer["sensitivity_gates"].values())
        and all(
            item["placement_sensitivity"]["pass"]
            for item in workload_evidence.values()
        ),
        "paper_endpoints_68_at_10_percent": layer["summary"]["endpoints"]
        == layer["summary"]["passing"]
        == 68
        and layer["limit"] == 0.10
        and layer["summary"]["max_relative_error"] <= 0.10,
        "run041_profile_native_13": profile["native_summary"]["pass"]
        and profile["native_summary"]["passing"]
        == profile["native_summary"]["gates"]
        == 13,
        "run041_nsight_9": profile["summary"]
        == {"gates": 9, "passing": 9, "failing": 0, "pass": True}
        and all(profile["gates"].values()),
        "profile_evidence_hashes": all(
            (PROJECT_ROOT / relative).is_file()
            and _sha256(PROJECT_ROOT / relative) == item["sha256"]
            for relative, item in profile["evidence"].items()
        ),
        "required_files": all(item["exists"] for item in file_evidence.values()),
        "report_updated": all(term in report for term in report_terms),
        "fresh_tests_and_rtl": checks_pass,
        "ordinary_riscv_no_atx": all(
            _json(run040_root / f"workloads/{name}/rocket/system.json")["gates"][
                "no_cancel_prefetch_or_atx"
            ]
            for name in EXPECTED
        ),
        "evidence_boundaries": "not A100/Core-Ultra" in run033["evidence_boundary"]
        and "not full mllm CUDA inference" in run039["evidence_boundary"]
        and "separate paper-config simulation/RTL" in run040["evidence_boundary"]
        and profile["gates"]["evidence_boundary"],
    }
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "complete_dual_gpu_multicpu_rocket_agent_experiment_system_certificate",
        "project_commit": _git_head(PROJECT_ROOT),
        "configuration": {"path": str(config_path), "sha256": _sha256(config_path)},
        "inputs": {
            "run033": {"path": str(run033_path), "sha256": _sha256(run033_path)},
            "run033_audit": {"path": str(run033_audit_path), "sha256": _sha256(run033_audit_path)},
            "run039": {"path": str(run039_path), "sha256": _sha256(run039_path)},
            "run040": {"path": str(run040_manifest_path), "sha256": _sha256(run040_manifest_path)},
            "run041_profile": {"path": str(profile_path), "sha256": _sha256(profile_path)},
            "layer_regression": {"path": str(layer_path), "sha256": _sha256(layer_path)},
        },
        "workloads": workload_evidence,
        "profile": profile,
        "required_files": file_evidence,
        "checks": checks,
        "requirements": gates,
        "summary": {
            "requirements": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "workloads": len(workload_evidence),
            "paper_layers": layer["summary"]["layers"],
            "parameter_switches": 6,
            "paper_endpoints": layer["summary"]["endpoints"],
            "paper_endpoints_passing": layer["summary"]["passing"],
            "max_relative_error": layer["summary"]["max_relative_error"],
            "fresh_checks": len(checks),
            "full_goal_complete": all(gates.values()),
        },
    }


def write_hybrid_certificate(
    path: Path,
    *,
    config_path: Path = DEFAULT_CONFIG,
    run_id: str = "run_041",
) -> dict[str, Any]:
    result = build_hybrid_certificate(
        config_path=config_path, run_id=run_id, run_checks=True
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Issue the final hybrid Agent system certificate")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id", default="run_041")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/hybrid-system-certificate-run_041.json",
    )
    args = parser.parse_args(argv)
    result = write_hybrid_certificate(
        args.output, config_path=args.config, run_id=args.run_id
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(args.output)
    return 0 if result["summary"]["full_goal_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

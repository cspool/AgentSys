from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from .parameterized_reproduce import DEFAULT_CONFIG
from .revised_certificate import _dispatch_check, _revised_lint_command, _run
from .toolchain import PROJECT_ROOT, build_toolchain_audit
from .workload import load_agent_workload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def build_parameterized_certificate(
    *,
    config_path: Path = DEFAULT_CONFIG,
    run_id: str = "run_032",
    run_checks: bool = True,
) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    output_root = (PROJECT_ROOT / config["output_root"]).resolve()
    manifest_path = (PROJECT_ROOT / config["manifest"]).resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    layer_path = output_root / "layer-regression/layer-regression.json"
    layer = json.loads(layer_path.read_text(encoding="utf-8"))

    workloads: dict[str, Any] = {}
    workload_hashes: set[str] = set()
    header_hashes: set[str] = set()
    elf_hashes: set[str] = set()
    workload_gate_details: dict[str, Any] = {}
    for workload_text in config["workloads"]:
        declared = load_agent_workload(PROJECT_ROOT / workload_text)
        root = output_root / "workloads" / declared.name
        pipeline = json.loads((root / "pipeline.json").read_text(encoding="utf-8"))
        application = json.loads((root / "application.json").read_text(encoding="utf-8"))
        compiled = json.loads((root / "compiled.json").read_text(encoding="utf-8"))
        system = json.loads((root / "system.json").read_text(encoding="utf-8"))
        header = root / "generated/workload.h"
        elf = root / "software/workload.riscv"
        workload_hashes.add(declared.sha256)
        header_hashes.add(_sha256(header))
        elf_hashes.add(_sha256(elf))
        dedicated_logs = [root / "logs/static-tisa.log", root / "logs/dynamic-tisa.log"]
        expected_tile_lines = int(compiled["summary"]["descriptors"]) * 2
        dedicated_pass = all(
            log.is_file()
            and len(log.read_text(encoding="utf-8").splitlines()) == expected_tile_lines
            and all(" call=" in line for line in log.read_text(encoding="utf-8").splitlines())
            for log in dedicated_logs
        )
        details = {
            "declared_sha256": declared.sha256,
            "pipeline_sha256": pipeline["workload"]["sha256"],
            "application_sha256": application["workload"]["sha256"],
            "compiled_sha256": compiled["workload"]["sha256"],
            "system_sha256": system["workload"]["sha256"],
            "pipeline_pass": pipeline["summary"]["pass"],
            "system_pass": system["summary"]["pass"],
            "system_gates": system["gates"],
            "descriptors": compiled["summary"]["descriptors"],
            "trace_events": system["trace"]["events"],
            "trace_layers": system["trace"]["layers"],
            "dedicated_trace_pass": dedicated_pass,
            "header_sha256": _sha256(header),
            "elf_sha256": _sha256(elf),
        }
        identity_values = {
            details["declared_sha256"],
            details["pipeline_sha256"],
            details["application_sha256"],
            details["compiled_sha256"],
            details["system_sha256"],
        }
        details["pass"] = (
            len(identity_values) == 1
            and details["pipeline_pass"]
            and details["system_pass"]
            and all(system["gates"].values())
            and dedicated_pass
        )
        workloads[declared.name] = {
            "pipeline": pipeline,
            "application_summary": application["summary"],
            "compiled_summary": compiled["summary"],
            "system_summary": system["summary"],
            "system_derived": system["derived"],
        }
        workload_gate_details[declared.name] = details

    base_config = (PROJECT_ROOT / config["base_toolchain"]).resolve()
    built_toolchain = build_toolchain_audit(
        level="built", config_path=base_config, project_root=PROJECT_ROOT
    )

    required_files = [
        "config/parameterized-system.json",
        "config/layer-regression-matrix.json",
        "src/agentsys/workload.py",
        "src/agentsys/parameterized_application.py",
        "src/agentsys/parameterized_compiler.py",
        "src/agentsys/parameterized_system.py",
        "src/agentsys/workload_pipeline.py",
        "src/agentsys/layer_regression.py",
        "src/agentsys/parameterized_reproduce.py",
        "src/agentsys/parameterized_certificate.py",
        "scripts/setup_parameterized_toolchain.sh",
        "docs/parameterized-workloads.md",
        "docs/layer-regression.md",
        "experiments/h14-parameterized-workloads/protocol.md",
        "experiments/h14-parameterized-workloads/run029-analysis.md",
        "experiments/h14-parameterized-workloads/run030-protocol.md",
        "experiments/h14-parameterized-workloads/run030-analysis.md",
        "experiments/h14-layer-regression/protocol.md",
        "experiments/h14-layer-regression/run031-analysis.md",
        "experiments/h14-parameterized-system-final/protocol.md",
        "experiments/h14-parameterized-system-final/run032-analysis.md",
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

    report_path = PROJECT_ROOT / "ISCA26_G3_Agent全栈系统加速.md"
    report = report_path.read_text(encoding="utf-8")
    report_terms = (
        "agentsys-run-workload",
        "agentsys-layer-regression",
        "agentsys-reproduce-parameterized",
        "react_moa_mcts",
        "react_tool",
        "planner_debate",
        "68/68",
        "10%",
        "860/180/436",
        "专用 TISA",
    )

    checks: dict[str, Any] = {}
    if run_checks:
        checks["pytest"] = _run(
            [str(PROJECT_ROOT / ".venv/bin/python"), "-m", "pytest"], timeout_s=600
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

    layer_summary = layer["summary"]
    gates = {
        "configuration_identity": manifest["configuration"]["sha256"]
        == _sha256(config_path),
        "serial_reproduction_4": manifest["summary"]
        == {
            "stages": 4,
            "executed": 4,
            "passing": 4,
            "failing": 0,
            "serial_order": True,
            "pass": True,
        }
        and manifest["stage_order"] == manifest["expected_stage_order"],
        "workload_schema_and_cli": all(file_evidence[path]["exists"] for path in (
            "src/agentsys/workload.py",
            "src/agentsys/workload_pipeline.py",
            "docs/parameterized-workloads.md",
        )),
        "three_distinct_workloads": len(workloads)
        == len(workload_hashes)
        == len(header_hashes)
        == len(elf_hashes)
        == 3,
        "three_workload_pipelines": all(
            detail["pass"] for detail in workload_gate_details.values()
        ),
        "dedicated_zero_repair_traces": all(
            detail["dedicated_trace_pass"]
            and detail["system_gates"]["dedicated_hardware_transport"]
            for detail in workload_gate_details.values()
        ),
        "per_tile_checksum_identity": all(
            detail["system_gates"]["per_tile_checksum_identity"]
            for detail in workload_gate_details.values()
        ),
        "five_layer_matrix": layer_summary["pass"]
        and layer_summary["layers"] == 5
        and layer_summary["parameter_switches"] == 5
        and all(layer["configuration_consumed"].values())
        and all(layer["sensitivity_gates"].values()),
        "paper_endpoints_68_at_10_percent": layer_summary["endpoints"]
        == layer_summary["passing"]
        == 68
        and layer["limit"] == 0.10
        and layer_summary["max_relative_error"] <= 0.10,
        "mllm_and_hptpe_functional": layer["gates"]["mllm_native_framework_pass"]
        and layer["gates"]["hptpe_rtl_functional_pass"],
        "ordinary_riscv_xpu_no_atx": all(
            detail["system_gates"]["neutral_xpu_v2_abi"]
            and detail["system_gates"]["no_cancel_prefetch_or_atx"]
            for detail in workload_gate_details.values()
        ),
        "base_toolchain_built": built_toolchain["summary"]
        == {"gates": 10, "passing": 10, "failing": 0, "pass": True},
        "required_files": all(item["exists"] for item in file_evidence.values()),
        "report_updated": all(term in report for term in report_terms),
        "fresh_checks": checks_pass,
    }
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "complete_parameterized_agent_experiment_system_certificate",
        "project_commit": _git_head(PROJECT_ROOT),
        "configuration": {
            "path": str(config_path),
            "sha256": _sha256(config_path),
        },
        "manifest": {
            "path": str(manifest_path),
            "sha256": _sha256(manifest_path),
            "summary": manifest["summary"],
        },
        "layer_regression": {
            "path": str(layer_path),
            "sha256": _sha256(layer_path),
            "summary": layer_summary,
        },
        "workloads": workload_gate_details,
        "base_toolchain": built_toolchain,
        "required_files": file_evidence,
        "checks": checks,
        "requirements": gates,
        "summary": {
            "requirements": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "workloads": len(workloads),
            "layers": layer_summary["layers"],
            "parameter_switches": layer_summary["parameter_switches"],
            "paper_endpoints": layer_summary["endpoints"],
            "paper_endpoints_passing": layer_summary["passing"],
            "max_relative_error": layer_summary["max_relative_error"],
            "full_goal_complete": all(gates.values()),
        },
    }


def write_parameterized_certificate(
    path: Path,
    *,
    config_path: Path = DEFAULT_CONFIG,
    run_id: str = "run_032",
) -> dict[str, Any]:
    result = build_parameterized_certificate(
        config_path=config_path, run_id=run_id, run_checks=True
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Issue the complete parameterized Agent experiment-system certificate"
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id", default="run_032")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/parameterized-system-certificate-run_032.json",
    )
    args = parser.parse_args(argv)
    result = write_parameterized_certificate(
        args.output, config_path=args.config, run_id=args.run_id
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(args.output)
    return 0 if result["summary"]["full_goal_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

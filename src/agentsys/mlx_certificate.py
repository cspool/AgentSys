from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .revised_certificate import _run
from .workload import PROJECT_ROOT, load_agent_workload


DEFAULT_CONFIG = PROJECT_ROOT / "config/mlx-complete-system.json"
RUN048 = PROJECT_ROOT / "artifacts/mlx_complete/run_048/reproduction.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _git_head(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def _fresh_iverilog(source_root: Path) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="agentsys-mlx-cycle-") as directory:
        output = Path(directory) / "mlx-cycle.vvp"
        command = [
            "iverilog",
            "-g2012",
            "-DMLX_CYCLE_MODEL",
            "-s",
            "tb_mlx_array_4x4",
            "-o",
            str(output),
            str(source_root / "rtl/mlx/mlx_fp16.sv"),
            str(source_root / "rtl/mlx/mlx_fu.sv"),
            str(source_root / "rtl/mlx/mlx_cycle_model.sv"),
            str(source_root / "rtl/mlx/tb_mlx_array_4x4.sv"),
        ]
        result = _run(command)
        result["output_bytes"] = output.stat().st_size if output.is_file() else 0
        result["pass"] = result["pass"] and result["output_bytes"] > 0
        return result


def _fresh_verilator_lint(source_root: Path) -> dict[str, Any]:
    names = (
        "mlx_fp16.sv",
        "mlx_fu.sv",
        "mlx_register_file.sv",
        "mlx_tag_buffer.sv",
        "mlx_config_network.sv",
        "mlx_data_network.sv",
        "mlx_control_logic.sv",
        "mlx_pe_top.sv",
        "mlx_array_4x4.sv",
    )
    return _run(
        [
            "verilator",
            "--lint-only",
            "--top-module",
            "mlx_array_4x4",
            "-Wno-fatal",
            "-Wno-PINCONNECTEMPTY",
            "-Wno-DECLFILENAME",
            "-Wno-WIDTH",
            "-Wno-UNUSED",
            "-DMLX_NO_WRAPPERS",
            *(str(source_root / f"rtl/mlx/{name}") for name in names),
        ]
    )


def build_mlx_certificate(
    *,
    config_path: Path = DEFAULT_CONFIG,
    run_id: str = "run_049",
    run_checks: bool = True,
) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = _json(config_path)
    run048 = _json(RUN048)
    source_config_path = PROJECT_ROOT / config["source_config"]
    source_config = _json(source_config_path)
    source_root = PROJECT_ROOT / source_config["active_path"]
    layer_path = Path(run048["results"]["layers"]["path"])
    agents_path = Path(run048["results"]["agents"]["path"])
    standalone_path = Path(run048["results"]["standalone"]["path"])
    chipyard_path = Path(run048["results"]["chipyard"]["path"])
    source_audit_path = Path(run048["results"]["source"]["path"])
    layer = _json(layer_path)
    agents = _json(agents_path)
    standalone = _json(standalone_path)
    chipyard = _json(chipyard_path)
    source_audit = _json(source_audit_path)
    gpu_runtime_path = PROJECT_ROOT / "artifacts/gpu_runtime/run_033/gpu-runtime.json"
    gpu_audit_path = PROJECT_ROOT / "artifacts/gpu_runtime/run_033/gpu-runtime-audit.json"
    mllm_cuda_path = PROJECT_ROOT / "artifacts/results/mllm-cuda-run_039.json"
    gpu_profile_path = PROJECT_ROOT / "artifacts/hybrid_profile/run_041/profile-audit.json"
    gpu_runtime = _json(gpu_runtime_path)
    gpu_audit = _json(gpu_audit_path)
    mllm_cuda = _json(mllm_cuda_path)
    gpu_profile = _json(gpu_profile_path)

    stage_hashes_valid = all(
        (PROJECT_ROOT / relative).is_file()
        and _sha256(PROJECT_ROOT / relative) == item["sha256"]
        for stage in run048["stages"]
        for relative, item in stage["artifacts"].items()
    )
    result_hashes_valid = all(
        Path(item["path"]).is_file()
        and _sha256(Path(item["path"])) == item["sha256"]
        for item in run048["results"].values()
    )

    expected_workloads = {
        "react_moa_mcts": {"calls": 11, "llm": 10, "micro": 450, "trace": 762},
        "react_tool": {"calls": 3, "llm": 2, "micro": 90, "trace": 158},
        "planner_debate": {"calls": 6, "llm": 5, "micro": 225, "trace": 385},
    }
    workload_evidence: dict[str, Any] = {}
    header_hashes: set[str] = set()
    elf_hashes: set[str] = set()
    for relative in _json(PROJECT_ROOT / config["agent_system"])["workloads"]:
        workload = load_agent_workload(PROJECT_ROOT / relative)
        name = workload.name
        root = Path(config["output_root"]).name  # run_048, used only as a guard below
        base = PROJECT_ROOT / "artifacts/mlx_complete/run_048/agent-workloads/workloads" / name
        system_path = base / "mlx-agent-system.json"
        compiled_path = base / "compiled-mlx.json"
        header_path = base / "generated/agent-mlx.h"
        elf_path = base / "software/agent-mlx.riscv"
        trace_path = base / "system-trace.jsonl"
        system = _json(system_path)
        compiled = _json(compiled_path)
        header_hashes.add(_sha256(header_path))
        elf_hashes.add(_sha256(elf_path))
        expected = expected_workloads[name]
        details = {
            "workload_sha256": workload.sha256,
            "system": {"path": str(system_path), "sha256": _sha256(system_path)},
            "compiled": {"path": str(compiled_path), "sha256": _sha256(compiled_path)},
            "header": {"path": str(header_path), "sha256": _sha256(header_path)},
            "elf": {"path": str(elf_path), "sha256": _sha256(elf_path)},
            "trace": {"path": str(trace_path), "sha256": _sha256(trace_path)},
            "summary": system["summary"],
            "layers": system["trace"]["layers"],
            "all_system_gates": all(system["gates"].values()),
            "all_backend_gates": all(
                all(values.values()) for values in system["backend_gates"].values()
            ),
            "no_atx_hptpe": system["gates"]["ordinary_cpu_no_atx_hptpe"],
            "identity": compiled["workload"]["sha256"]
            == system["workload"]["sha256"]
            == workload.sha256,
            "counts": system["summary"]["calls"] == expected["calls"]
            and system["summary"]["llm_calls"] == expected["llm"]
            and system["summary"]["mlx_micro_ops"] == expected["micro"]
            and system["summary"]["trace_events"] == expected["trace"],
            "run_root_guard": root == "run_048",
        }
        details["pass"] = all(
            (
                details["all_system_gates"],
                details["all_backend_gates"],
                details["no_atx_hptpe"],
                details["identity"],
                details["counts"],
                details["run_root_guard"],
            )
        )
        workload_evidence[name] = details

    required_files = [
        "config/mlx-active-source.json",
        "config/mlx-runtime-requirements.txt",
        "config/mlx-agent-system.json",
        "config/mlx-six-layer-matrix.json",
        "config/mlx-complete-system.json",
        "scripts/setup_mlx_active.sh",
        "scripts/setup_mlx_toolchain.sh",
        "scripts/install_mlx_chipyard.sh",
        "src/agentsys/mlx_reference.py",
        "src/agentsys/mlx_standalone.py",
        "src/agentsys/mlx_chipyard.py",
        "src/agentsys/mlx_agent_compiler.py",
        "src/agentsys/mlx_agent_system.py",
        "src/agentsys/mlx_agent_reproduce.py",
        "src/agentsys/mlx_layer_regression.py",
        "src/agentsys/mlx_complete_reproduce.py",
        "src/agentsys/mlx_certificate.py",
        "system_sim/software/agentsys_mlx_smoke.c",
        "system_sim/software/agentsys_mlx_agent.c",
        "docs/mlx-agent-system.md",
        "docs/layer-regression.md",
        "docs/toolchain.md",
        "experiments/h16-mlx-cpu-rebase/protocol.md",
        "experiments/h17-mlx-standalone/protocol.md",
        "experiments/h17-mlx-chipyard/protocol.md",
        "experiments/h18-agent-mlx-integration/protocol.md",
        "experiments/h18-agent-mlx-integration/recovery-protocol-run046.md",
        "experiments/h19-mlx-layer-regression/protocol.md",
        "experiments/h19-mlx-final-replay/protocol.md",
        "experiments/h19-mlx-final-certificate/protocol.md",
        "experiments/h19-mlx-final-certificate/run049-analysis.md",
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
            timeout_s=900,
        )
        checks["mlx_toolchain_setup"] = _run(
            ["bash", "scripts/setup_mlx_toolchain.sh"], timeout_s=300
        )
        checks["mlx_chipyard_overlay"] = _run(
            ["bash", "scripts/install_mlx_chipyard.sh"], timeout_s=300
        )
        checks["mlx_cycle_compile"] = _fresh_iverilog(source_root)
        checks["mlx_rtl_lint"] = _fresh_verilator_lint(source_root)
    checks_pass = all(check["pass"] for check in checks.values()) if checks else True
    pytest_count = None
    if "pytest" in checks:
        match = re.search(r"(\d+) passed", checks["pytest"]["output"])
        pytest_count = int(match.group(1)) if match else None
        checks_pass = checks_pass and pytest_count is not None
    if "mlx_chipyard_overlay" in checks:
        checks_pass = checks_pass and "12/12 files" in checks["mlx_chipyard_overlay"]["output"]

    report = (PROJECT_ROOT / "ISCA26_G3_Agent全栈系统加速.md").read_text(
        encoding="utf-8"
    )
    report_terms = (
        "agentsys-reproduce-mlx-complete",
        "Rocket+MLX",
        "73/73",
        "765",
        "344",
        "216",
        "target-informed",
        "20.77%",
        "1/18",
        "mlx-cpu-final-certificate-run_049",
    )
    mlx_layer = layer["layers"]["mlx"]
    gates = {
        "run048_complete_serial": run048["summary"]["pass"]
        and run048["summary"]["executed"] == run048["summary"]["stages"] == 5
        and run048["summary"]["gates_passing"] == run048["summary"]["gates"] == 10
        and run048["summary"]["serial_order"],
        "run048_stage_and_result_hashes": stage_hashes_valid and result_hashes_valid,
        "source_audit_10": source_audit["summary"]["passing"]
        == source_audit["summary"]["gates"]
        == 10,
        "standalone_10": standalone["summary"]["passing"]
        == standalone["summary"]["gates"]
        == 10,
        "chipyard_12": chipyard["summary"]["passing"]
        == chipyard["summary"]["gates"]
        == 12,
        "six_layers_73_at_10_percent": layer["summary"]["layers"] == 6
        and layer["summary"]["endpoints"] == layer["summary"]["passing"] == 73
        and layer["summary"]["max_relative_error"] <= 0.10
        and layer["limit"] == 0.10,
        "six_parameter_switches": layer["summary"]["parameter_switches"] == 6
        and all(layer["configuration_consumed"].values())
        and all(layer["sensitivity_gates"].values()),
        "three_agent_workloads_9": agents["summary"]["passing"]
        == agents["summary"]["gates"]
        == 9
        and agents["summary"]["workloads"] == 3,
        "three_workload_artifact_chains": len(workload_evidence) == 3
        and all(item["pass"] for item in workload_evidence.values())
        and len(header_hashes) == len(elf_hashes) == 3,
        "exact_agent_counts": agents["summary"]["calls"] == 20
        and agents["summary"]["llm_calls"] == 17
        and agents["summary"]["tool_calls"] == 3
        and agents["summary"]["mlx_micro_ops"] == 765,
        "trace_14_layers": all(len(item["layers"]) == 14 for item in workload_evidence.values()),
        "primary_mlx_no_atx": layer["primary_system_hardware"] == "mlx"
        and "atx" in layer["excluded_layers"]
        and all(item["no_atx_hptpe"] for item in workload_evidence.values()),
        "active_source_pinned_clean": source_audit["active"]["commit"]
        == source_config["active_commit"]
        and source_audit["active"]["clean"]
        and not subprocess.check_output(
            ["git", "-C", str(source_root), "status", "--porcelain", "--untracked-files=no"],
            text=True,
        ).strip(),
        "installed_mlx_overlays": chipyard["gates"]["installed_sources_match"]
        and len(chipyard["chipyard"]["installed"]) == 12,
        "mlx_target_informed_boundary": mlx_layer["paper_source"]["validation_eligible"]
        is False
        and mlx_layer["paper_accuracy"]["max_relative_error"] <= 0.10
        and mlx_layer["paper_accuracy"]["leave_one_out_max_relative_error"] > 0.10,
        "mlx_full_paper_negative": mlx_layer["full_paper_scope"][
            "all_paper_experiments_reproduced_within_10pct"
        ]
        is False
        and mlx_layer["full_paper_scope"]["reproduced_within_10pct_count"] == 1
        and mlx_layer["full_paper_scope"]["not_fully_reproduced_count"] == 17,
        "mllm_hptpe_functional": layer["gates"]["mllm_hptpe_functional"],
        "aux_gpu_runtime_11_9": gpu_runtime["summary"]["passing"]
        == gpu_runtime["summary"]["gates"]
        == 11
        and gpu_audit["summary"] == {"gates": 9, "passing": 9, "failing": 0, "pass": True},
        "aux_mllm_cuda_13": mllm_cuda["summary"]
        == {"gates": 13, "passing": 13, "failing": 0, "pass": True},
        "aux_gpu_profile_9": gpu_profile["summary"]
        == {"gates": 9, "passing": 9, "failing": 0, "pass": True},
        "mlx_environment_pinned": _json(
            PROJECT_ROOT / "artifacts/mlx_environment/environment.json"
        )["numpy"]
        == "2.2.6"
        and "PyYAML==6.0.2"
        in (PROJECT_ROOT / "config/mlx-runtime-requirements.txt").read_text(encoding="utf-8"),
        "required_files": all(item["exists"] for item in file_evidence.values()),
        "report_updated": all(term in report for term in report_terms),
        "fresh_checks": checks_pass,
        "complete_evidence_classification": "open surrogate" in source_audit[
            "evidence_boundary"
        ]
        and "target-informed" in layer["evidence_boundary"]
        and "registered 73-endpoint" in run048["evidence_boundary"],
    }
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "final_complete_parameterized_agent_mlx_cpu_experiment_certificate",
        "project_commit": _git_head(PROJECT_ROOT),
        "configuration": {"path": str(config_path), "sha256": _sha256(config_path)},
        "inputs": {
            "run048": {"path": str(RUN048), "sha256": _sha256(RUN048)},
            "source": {"path": str(source_audit_path), "sha256": _sha256(source_audit_path)},
            "standalone": {"path": str(standalone_path), "sha256": _sha256(standalone_path)},
            "chipyard": {"path": str(chipyard_path), "sha256": _sha256(chipyard_path)},
            "layers": {"path": str(layer_path), "sha256": _sha256(layer_path)},
            "agents": {"path": str(agents_path), "sha256": _sha256(agents_path)},
            "gpu_runtime": {"path": str(gpu_runtime_path), "sha256": _sha256(gpu_runtime_path)},
            "mllm_cuda": {"path": str(mllm_cuda_path), "sha256": _sha256(mllm_cuda_path)},
            "gpu_profile": {"path": str(gpu_profile_path), "sha256": _sha256(gpu_profile_path)},
        },
        "workloads": workload_evidence,
        "required_files": file_evidence,
        "checks": checks,
        "requirements": gates,
        "summary": {
            "requirements": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "fresh_checks": len(checks),
            "pytest_passed": pytest_count,
            "paper_layers": 6,
            "paper_endpoints": 73,
            "paper_endpoints_passing": 73,
            "parameter_switches": 6,
            "agent_workloads": 3,
            "mlx_executions": 24,
            "max_relative_error": layer["summary"]["max_relative_error"],
            "full_goal_complete": all(gates.values()),
        },
    }


def write_mlx_certificate(
    output: Path,
    *,
    config_path: Path = DEFAULT_CONFIG,
    run_id: str = "run_049",
) -> dict[str, Any]:
    result = build_mlx_certificate(
        config_path=config_path, run_id=run_id, run_checks=True
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Issue the final MLX+CPU AgentSys certificate")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id", default="run_049")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/mlx-cpu-final-certificate-run_049.json",
    )
    args = parser.parse_args(argv)
    result = write_mlx_certificate(args.output, config_path=args.config, run_id=args.run_id)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(args.output)
    return 0 if result["summary"]["full_goal_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

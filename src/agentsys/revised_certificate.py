from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .paths import chipyard_source_identity, resolve_chipyard_root
from .toolchain import PROJECT_ROOT, load_toolchain_config, resolve_path


DEFAULT_CONFIG = PROJECT_ROOT / "config/revised-toolchain.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head(path: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def _load(path: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    value = json.loads(path.read_text(encoding="utf-8"))
    return value, {"path": str(path), "bytes": path.stat().st_size, "sha256": _sha256(path)}


def _run(command: list[str], *, timeout_s: int = 300) -> dict[str, Any]:
    try:
        process = subprocess.run(
            command,
            cwd=PROJECT_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_s,
            check=False,
        )
        return {
            "command": command,
            "exit_code": process.returncode,
            "output": process.stdout,
            "pass": process.returncode == 0,
        }
    except subprocess.TimeoutExpired as error:
        return {"command": command, "exit_code": 124, "output": str(error), "pass": False}


def _dispatch_check() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="agentsys-tisa-dispatch-") as directory:
        executable = Path(directory) / "dispatch.vvp"
        compile_result = _run(
            [
                "iverilog",
                "-g2012",
                "-s",
                "tb_agentsys_tisa_dispatch",
                "-o",
                str(executable),
                "rtl/agentsys/agentsys_tisa_scheduler.sv",
                "rtl/agentsys/tb_agentsys_tisa_dispatch.sv",
            ]
        )
        if not compile_result["pass"]:
            return {"compile": compile_result, "execute": None, "pass": False}
        execute_result = _run(["vvp", str(executable)])
        passed = execute_result["pass"] and (
            "AGENTSYS_TISA_DISPATCH_PASS static_first=0 dynamic_first=7"
            in execute_result["output"]
        )
        return {"compile": compile_result, "execute": execute_result, "pass": passed}


def _revised_lint_command() -> list[str]:
    vsrc = str(
        resolve_chipyard_root()
        / "generators/chipyard/src/main/resources/vsrc"
    )
    return [
        "verilator",
        "--lint-only",
        "--top-module",
        "AgentSysRevisedRoCCBlackBox",
        "-Wall",
        "-Wno-fatal",
        "rtl/agentsys/agentsys_tisa_scheduler.sv",
        "rtl/agentsys/agentsys_revised_engines.sv",
        "rtl/agentsys/agentsys_revised_rocc_controller.sv",
        *[
            f"{vsrc}/{name}"
            for name in (
                "hptpe_timescale.sv",
                "hptpe_booth_gen.v",
                "hptpe_booth_pp.v",
                "hptpe_booth_pp1.v",
                "hptpe_dw02_tree.sv",
                "hptpe_inv_converter.v",
                "hptpe_inv_unit.v",
                "hptpe_inv_unit_nor.v",
                "hptpe_opt1_mac.v",
                "hptpe_pe.v",
                "hptpe_pipeline.v",
                "hptpe_top.v",
            )
        ],
    ]


def build_revised_certificate(
    *,
    run_id: str = "run_028",
    config_path: Path = DEFAULT_CONFIG,
    run_checks: bool = True,
) -> dict[str, Any]:
    config = load_toolchain_config(config_path)
    artifact_paths = {
        **{
            f"paper_{name}": resolve_path(profile["output"])
            for name, profile in config["paper_profiles"].items()
        },
        "components": resolve_path(config["revised_component_certificate"]),
        "compiled": PROJECT_ROOT / "artifacts/app_traces/revised-compiled-workload-run_028.json",
        "system": resolve_path(config["revised_system_result"]),
        "reproduction": resolve_path(config["reproduction_manifest"]),
        "toolchain": resolve_path(config["toolchain_audit"]),
    }
    loaded: dict[str, dict[str, Any]] = {}
    artifact_evidence: dict[str, dict[str, Any]] = {}
    for name, path in artifact_paths.items():
        loaded[name], artifact_evidence[name] = _load(path)

    components = loaded["components"]
    system = loaded["system"]
    static = system["static"]["parsed"]["summary"]
    dynamic = system["dynamic"]["parsed"]["summary"]
    profile_names = tuple(config["paper_profiles"])
    profile_gates = {
        "agentix": loaded["paper_agentix"]["summary"]["pass"]
        and loaded["paper_agentix"]["summary"]["endpoints"] == 16,
        "agentxpu": loaded["paper_agentxpu"]["summary"]["pass"]
        and loaded["paper_agentxpu"]["summary"]["endpoints"] == 11,
        "tisa": loaded["paper_tisa"]["summary"]["pass"]
        and loaded["paper_tisa"]["summary"]["endpoints"] == 10,
        "mllm": loaded["paper_mllm"]["summary"]
        == {
            "max_relative_error": 0.09909909909909899,
            "native_executables_passed": 20,
            "native_executables_total": 20,
            "native_gtest_cases_passed": 101,
            "paper_endpoints_passed": 5,
            "paper_endpoints_total": 5,
            "pass": True,
        },
        "hptpe": loaded["paper_hptpe"]["summary"]
        == {
            "max_relative_error": 0.009756097560975618,
            "paper_endpoints_passed": 26,
            "paper_endpoints_total": 26,
            "pass": True,
            "rtl_functional_passed": 9,
            "rtl_functional_total": 9,
            "rtl_golden_checks": 302,
            "rtl_lint_passed": 9,
            "rtl_lint_total": 9,
        },
    }

    trace_path = resolve_path(config["revised_system_trace"])
    trace_events = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines()]
    trace_layers = sorted({event["layer"] for event in trace_events})
    expected_layers = [
        "agentxpu",
        "application",
        "cpu",
        "dma",
        "framework",
        "hptpe",
        "mllm",
        "software",
        "tisa",
        "ve_de",
        "xpu",
    ]

    same_work_keys = (
        "programs",
        "calls",
        "launches",
        "descriptors",
        "dma_bytes",
        "me_busy",
        "ve_busy",
        "de_busy",
        "hptpe_mac_ops",
        "flows",
        "placements",
        "checksum",
        "app_digest",
        "mir_digest",
    )
    reproduction = loaded["reproduction"]
    toolchain = loaded["toolchain"]

    configured_files = list(config["source_files"])
    artifact_files = [
        str(path.relative_to(PROJECT_ROOT))
        for path in artifact_paths.values()
        if path.is_relative_to(PROJECT_ROOT)
    ] + [
        config["revised_system_trace"],
        "artifacts/logs/revised-system-static-run_028.log",
        "artifacts/logs/revised-system-dynamic-run_028.log",
        "experiments/h13-revised-stack/final-toolchain-analysis-run_028.md",
    ]
    required_files: dict[str, Any] = {}
    for relative in dict.fromkeys(configured_files + artifact_files):
        path = resolve_path(relative)
        required_files[relative] = {
            "exists": path.is_file(),
            "sha256": _sha256(path) if path.is_file() else None,
        }

    references: dict[str, Any] = {}
    for reference in config["references"]:
        path = resolve_path(reference["path"])
        observed = (
            chipyard_source_identity(path)["commit"]
            if reference["name"] == "chipyard"
            else _git_head(path)
        )
        references[reference["name"]] = {
            "role": reference.get("role"),
            "expected": reference["commit"],
            "observed": observed,
            "pass": observed == reference["commit"],
        }

    report_path = PROJECT_ROOT / "ISCA26_G3_Agent全栈系统加速.md"
    report_text = report_path.read_text(encoding="utf-8")
    required_report_terms = (
        "普通 RISC-V",
        "mllm → Agent.xpu → TISA → HPTPE",
        "run 023",
        "run 024",
        "run 025",
        "run 026",
        "run 027",
        "68/68",
        "860 events",
        "1.376",
        "ATX",
    )

    checks: dict[str, Any] = {}
    if run_checks:
        checks["pytest"] = _run([str(PROJECT_ROOT / ".venv/bin/python"), "-m", "pytest"])
        checks["dispatch_rtl"] = _dispatch_check()
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
        checks["revised_hptpe_rtl_lint"] = _run(_revised_lint_command(), timeout_s=300)
    checks_pass = all(check["pass"] for check in checks.values()) if checks else True

    gates = {
        "active_profiles_5_no_atx": profile_names
        == ("agentix", "agentxpu", "tisa", "mllm", "hptpe")
        and config["excluded_components"] == ["atx"],
        "independent_profiles_5": all(profile_gates.values()),
        "standalone_components_68": components["summary"]
        == {
            "components_passed": 5,
            "components_total": 5,
            "endpoints_passed": 68,
            "endpoints_total": 68,
            "gates_passed": 8,
            "gates_total": 8,
            "max_relative_error": 0.09909909909909899,
            "pass": True,
        }
        and components["active_components"] == list(profile_names)
        and components["excluded_components"] == ["atx"],
        "compiled_agent_stack": loaded["compiled"]["summary"]["pass"]
        and loaded["compiled"]["summary"]["descriptors"] == 80
        and loaded["compiled"]["mllm"]["commit"]
        == "50ad5a9b6fbea742e38b5b31776c187e50319c8e",
        "ordinary_rocket_hptpe_system_20": system["summary"]
        == {"failing": 0, "gates": 20, "pass": True, "passing": 20}
        and system["classification"]
        == "real_ordinary_rocket_plus_tisa_hptpe_agent_system_trace",
        "system_same_work_and_checksum": all(static[key] == dynamic[key] for key in same_work_keys),
        "tisa_performance_contract": static["dispatch_latency"] == 0
        and dynamic["dispatch_latency"] == 7
        and 1.14 <= system["derived"]["backend_speedup"] <= 1.63
        and system["derived"]["system_speedup"] > 1.0,
        "hptpe_integrated_work": static["hptpe_mac_ops"]
        == dynamic["hptpe_mac_ops"]
        == 614400,
        "trace_860_11_layers": len(trace_events) == 860 and trace_layers == expected_layers,
        "serial_reproduction_8": reproduction["summary"]["pass"]
        and reproduction["summary"]["executed"] == 8
        and reproduction["summary"]["passing"] == 8
        and reproduction["summary"]["serial_order"]
        and reproduction["toolchain_config"]["sha256"] == _sha256(config_path),
        "toolchain_12": toolchain["summary"]
        == {"failing": 0, "gates": 12, "pass": True, "passing": 12}
        and toolchain["level"] == "full",
        "required_files": all(item["exists"] for item in required_files.values()),
        "pinned_references": all(item["pass"] for item in references.values()),
        "report_updated": len(report_text.splitlines()) >= 300
        and all(term in report_text for term in required_report_terms),
        "fresh_checks": checks_pass,
    }
    complete = all(gates.values())
    return {
        "schema_version": 1,
        "run_id": run_id,
        "objective": "Five standalone components within 15%, then Agentix-to-HPTPE integration on ordinary RISC-V with real system trace.",
        "classification": "revised_ordinary_riscv_full_stack_completion_certificate",
        "project_commit": _git_head(PROJECT_ROOT),
        "active_components": list(profile_names),
        "excluded_components": ["atx"],
        "profile_gates": profile_gates,
        "artifacts": artifact_evidence,
        "required_files": required_files,
        "references": references,
        "system": {
            "static": static,
            "dynamic": dynamic,
            "derived": system["derived"],
            "trace_events": len(trace_events),
            "trace_layers": trace_layers,
        },
        "checks": checks,
        "requirements": gates,
        "summary": {
            "requirements": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "components": 5,
            "endpoints": 68,
            "endpoints_passing": 68 if gates["standalone_components_68"] else 0,
            "max_relative_error": components["summary"]["max_relative_error"],
            "full_goal_complete": complete,
        },
    }


def write_revised_certificate(
    path: Path,
    *,
    run_id: str = "run_028",
    config_path: Path = DEFAULT_CONFIG,
) -> dict[str, Any]:
    result = build_revised_certificate(
        run_id=run_id, config_path=config_path, run_checks=True
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Issue the revised AgentSys completion certificate")
    parser.add_argument("--run-id", default="run_028")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/revised-final-certificate-run_028.json",
    )
    args = parser.parse_args(argv)
    result = write_revised_certificate(args.output, run_id=args.run_id, config_path=args.config)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(args.output)
    return 0 if result["summary"]["full_goal_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

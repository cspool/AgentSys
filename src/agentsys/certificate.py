from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]


ARTIFACTS = {
    "paper_agentix": "artifacts/results/paper-agentix-run_019.json",
    "paper_agentxpu": "artifacts/results/paper-agentxpu-run_019.json",
    "paper_atx": "artifacts/results/paper-atx-run_019.json",
    "paper_tisa": "artifacts/results/paper-tisa-run_019.json",
    "chipyard": "artifacts/results/chipyard-run_003.json",
    "mllm": "artifacts/results/mllm-run_006.json",
    "full_stack": "artifacts/results/full-stack-run_008.json",
    "ramulator2": "artifacts/results/ramulator2-run_012.json",
    "ablations": "artifacts/results/ablations-run_013.json",
    "reproduction": "artifacts/results/reproduction-run_019.json",
    "toolchain": "artifacts/results/toolchain-run_019.json",
}


REFERENCE_COMMITS = {
    ".references/MLX_dev_sys": "b3a6d59f2ed634ea6181f5a29f3fa96281b1f384",
    ".references/LLM.xpu": "689be270aa29bb88447e3867cd97d85a55f454d5",
    ".references/HPTPE": "ebe4db7d2d3c36d10c47683d7689f65f5c4ca3e4",
    ".references/mllm": "50ad5a9b6fbea742e38b5b31776c187e50319c8e",
    ".references/ramulator2": "be93be78055d922aa1d4d33e15bcc8f2b0c61a9d",
    ".references/autellix": "1df19874d1fb10e497b7185bf813fdd7be189683",
    "/root/chipyard": "b5d013190d637e634113cb5179f8c8885df1945a",
}


REQUIRED_FILES = (
    "ISCA26_G3_Agent全栈系统加速.md",
    "src/agentsys/agentix.py",
    "src/agentsys/agentix_model.py",
    "src/agentsys/agentix_serving_simulator.py",
    "src/agentsys/agentix_reference.py",
    "src/agentsys/agentxpu.py",
    "src/agentsys/atx.py",
    "src/agentsys/atx_model.py",
    "src/agentsys/atx_simulator.py",
    "src/agentsys/tisa.py",
    "src/agentsys/mllm_backend.py",
    "src/agentsys/fullstack.py",
    "src/agentsys/ramulator.py",
    "rtl/agentsys/agentsys_engines.sv",
    "rtl/agentsys/agentsys_tisa_scheduler.sv",
    "rtl/agentsys/agentsys_rocc_controller.sv",
    "system_sim/chipyard/AgentSysRoCC.scala",
    "system_sim/software/agentsys_runtime.h",
    "system_sim/software/agentsys_system_test.c",
    "scripts/install_agentsys_chipyard.sh",
    "scripts/build_ramulator2.sh",
    "scripts/setup_toolchain.sh",
    ".python-version",
    "uv.lock",
    "config/toolchain.json",
    "src/agentsys/toolchain.py",
    "src/agentsys/reproduce.py",
    "src/agentsys/paper_reproduction.py",
    "docs/toolchain.md",
    "docs/source-discovery.md",
    "experiments/h9-toolchain/protocol.md",
    "experiments/h9-toolchain/analysis.md",
    "experiments/h10-paper10/protocol.md",
    "experiments/h10-paper10/analysis.md",
    "experiments/h11-open-substitutes/protocol.md",
    "artifacts/results/paper-agentix-run_019.json",
    "artifacts/results/paper-agentxpu-run_019.json",
    "artifacts/results/paper-atx-run_019.json",
    "artifacts/results/paper-tisa-run_019.json",
    "artifacts/results/reproduction-run_019.json",
    "artifacts/results/toolchain-run_019.json",
    "artifacts/traces/full-stack-run_008.jsonl",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load(relative: str) -> tuple[dict[str, Any], dict[str, Any]]:
    path = PROJECT_ROOT / relative
    value = json.loads(path.read_text(encoding="utf-8"))
    return value, {"path": relative, "sha256": _sha256(path), "bytes": path.stat().st_size}


def _git_head(path_text: str) -> str | None:
    path = Path(path_text) if path_text.startswith("/") else PROJECT_ROOT / path_text
    if not path.exists():
        return None
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError:
        return None


def collect_paper_endpoints() -> list[dict[str, Any]]:
    endpoints: list[dict[str, Any]] = []
    for name in ("paper_agentix", "paper_agentxpu", "paper_atx", "paper_tisa"):
        paper, _ = _load(ARTIFACTS[name])
        endpoints.extend(paper["audit"])
    return endpoints


def _run_command(command: list[str], *, cwd: Path = PROJECT_ROOT, timeout: int = 300) -> dict[str, Any]:
    process = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    return {"command": command, "exit_code": process.returncode, "output": process.stdout}


def build_certificate(*, run_id: str = "run_020", run_checks: bool = True) -> dict[str, Any]:
    loaded: dict[str, dict[str, Any]] = {}
    manifests: dict[str, dict[str, Any]] = {}
    for name, relative in ARTIFACTS.items():
        loaded[name], manifests[name] = _load(relative)

    endpoints = collect_paper_endpoints()
    endpoint_names = [entry["endpoint"] for entry in endpoints]
    endpoint_errors = [float(entry["relative_error"]) for entry in endpoints]
    registered_limit = float(
        json.loads((PROJECT_ROOT / "data/paper_targets.json").read_text(encoding="utf-8"))[
            "max_relative_error"
        ]
    )
    paper_gate = (
        registered_limit == 0.10
        and len(endpoints) == 55
        and len(endpoint_names) == len(set(endpoint_names))
        and all(entry["pass"] for entry in endpoints)
        and all(float(entry["limit"]) == registered_limit for entry in endpoints)
        and max(endpoint_errors) <= registered_limit
    )

    expected_paper_counts = {
        "paper_agentix": 16,
        "paper_agentxpu": 11,
        "paper_atx": 18,
        "paper_tisa": 10,
    }
    individual_papers_gate = all(
        loaded[name]["paper"] == name.removeprefix("paper_")
        and loaded[name]["summary"]["pass"]
        and loaded[name]["summary"]["endpoints"] == count
        and float(loaded[name]["summary"]["limit"]) == registered_limit
        and loaded[name]["summary"]["toolchain_profile_pass"]
        for name, count in expected_paper_counts.items()
    ) and (
        loaded["paper_agentix"]["components"]["aggregate"]["classification"]
        == "executable_open_agentix_serving_substitute_simulation"
        and loaded["paper_agentix"]["components"]["aggregate"]["public_reference_audit"]["summary"]["pass"]
        and loaded["paper_atx"]["components"]["microarchitecture_simulation"]["classification"]
        == "executable_open_atx_ute_microarchitecture_simulation"
    )

    component_gates = {
        "paper_endpoints_55": paper_gate,
        "individual_papers_4": individual_papers_gate,
        "closed_platform_substitutes_2": (
            loaded["paper_agentix"]["evidence_classes"][
                "open_executable_closed_platform_substitute"
            ]
            == 13
            and loaded["paper_atx"]["evidence_classes"][
                "open_executable_closed_platform_substitute"
            ]
            == 18
            and loaded["paper_agentix"]["evidence_classes"][
                "paper_parameterized_component_replay"
            ]
            == 0
            and loaded["paper_atx"]["evidence_classes"][
                "paper_parameterized_component_replay"
            ]
            == 0
        ),
        "chipyard_17": loaded["chipyard"]["summary"] == {"failing": 0, "gates": 17, "pass": True, "passing": 17},
        "mllm_9": loaded["mllm"]["summary"]["pass"] and loaded["mllm"]["summary"]["gates"] == 9,
        "full_stack_10": loaded["full_stack"]["summary"]["pass"] and loaded["full_stack"]["summary"]["gates"] == 10,
        "ramulator2_7": loaded["ramulator2"]["summary"]["pass"] and loaded["ramulator2"]["summary"]["gates"] == 7,
        "ablations_7": loaded["ablations"]["summary"]["pass"] and loaded["ablations"]["summary"]["gates"] == 7,
        "serial_reproduction_9": (
            loaded["reproduction"]["summary"]["pass"]
            and loaded["reproduction"]["summary"]["executed"] == 9
            and loaded["reproduction"]["summary"]["passing"] == 9
            and loaded["reproduction"]["summary"]["serial_order"]
        ),
        "toolchain_12": (
            loaded["toolchain"]["summary"]["pass"]
            and loaded["toolchain"]["summary"]["gates"] == 12
            and loaded["toolchain"]["level"] == "full"
        ),
    }

    required_files = {
        relative: {
            "exists": (PROJECT_ROOT / relative).is_file(),
            "sha256": _sha256(PROJECT_ROOT / relative) if (PROJECT_ROOT / relative).is_file() else None,
        }
        for relative in REQUIRED_FILES
    }
    files_gate = all(value["exists"] for value in required_files.values())

    observed_commits = {path: _git_head(path) for path in REFERENCE_COMMITS}
    commits_gate = all(observed_commits[path] == expected for path, expected in REFERENCE_COMMITS.items())

    report_path = PROJECT_ROOT / "ISCA26_G3_Agent全栈系统加速.md"
    report_text = report_path.read_text(encoding="utf-8")
    required_report_terms = (
        "## 系统架构",
        "## 实验方法",
        "## 论文核心结果复现",
        "## 限制与不应外推的结论",
        "## 工具链与配置",
        "## 环境与重放",
        "## 验收矩阵",
        "agentsys-reproduce-all",
        "四篇论文独立工具链",
        "10%",
        "55/55",
        "636/636",
    )
    report_gate = len(report_text.splitlines()) >= 300 and all(term in report_text for term in required_report_terms)

    trace_path = PROJECT_ROOT / "artifacts/traces/full-stack-run_008.jsonl"
    trace_events = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines()]
    trace_layers = sorted({event["layer"] for event in trace_events})
    trace_gate = len(trace_events) == 636 and trace_layers == ["call", "engine", "flow", "program", "task", "tile"]

    checks: dict[str, Any] = {}
    if run_checks:
        checks["pytest"] = _run_command([str(PROJECT_ROOT / ".venv/bin/python"), "-m", "pytest"])
        checks["rtl_lint"] = _run_command(
            [
                "verilator",
                "--lint-only",
                "--top-module",
                "AgentSysRoCCBlackBox",
                "-Wall",
                "rtl/agentsys/agentsys_engines.sv",
                "rtl/agentsys/agentsys_tisa_scheduler.sv",
                "rtl/agentsys/agentsys_rocc_controller.sv",
            ]
        )
    checks_gate = all(value["exit_code"] == 0 for value in checks.values()) if checks else True

    requirement_gates = {
        **component_gates,
        "required_files": files_gate,
        "pinned_commits": commits_gate,
        "report": report_gate,
        "trace": trace_gate,
        "fresh_checks": checks_gate,
    }
    full_goal_complete = all(requirement_gates.values())
    return {
        "schema_version": 1,
        "run_id": run_id,
        "objective": "Complete independent AgentSys paper toolchains and reproduce every registered endpoint within 10%.",
        "classification": "requirement_by_requirement_completion_certificate",
        "project_commit": _git_head(str(PROJECT_ROOT)),
        "paper_endpoints": {
            "count": len(endpoints),
            "unique": len(set(endpoint_names)),
            "passing": sum(bool(entry["pass"]) for entry in endpoints),
            "max_relative_error": max(endpoint_errors),
            "registered_limit": registered_limit,
            "evidence_classes": {
                "executable_or_source_grounded": 24,
                "open_executable_closed_platform_substitute": 31,
                "paper_parameterized_component_replay": 0,
            },
            "endpoints": endpoints,
        },
        "artifacts": manifests,
        "component_gates": component_gates,
        "required_files": required_files,
        "references": {
            path: {"expected": expected, "observed": observed_commits[path], "pass": observed_commits[path] == expected}
            for path, expected in REFERENCE_COMMITS.items()
        },
        "report": {"lines": len(report_text.splitlines()), "required_terms": list(required_report_terms), "pass": report_gate},
        "trace": {"events": len(trace_events), "layers": trace_layers, "pass": trace_gate},
        "checks": checks,
        "requirements": requirement_gates,
        "summary": {
            "requirements": len(requirement_gates),
            "passing": sum(requirement_gates.values()),
            "failing": len(requirement_gates) - sum(requirement_gates.values()),
            "paper_endpoints": len(endpoints),
            "paper_endpoints_passing": sum(bool(entry["pass"]) for entry in endpoints),
            "max_relative_error": max(endpoint_errors),
            "full_goal_complete": full_goal_complete,
        },
    }


def write_certificate(path: Path, *, run_id: str = "run_020") -> dict[str, Any]:
    result = build_certificate(run_id=run_id, run_checks=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result

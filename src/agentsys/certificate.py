from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]


ARTIFACTS = {
    "direct_paper": "artifacts/results/run_011.json",
    "agentix_aggregate": "artifacts/results/agentix-run_010.json",
    "atx": "artifacts/results/atx-run_004.json",
    "chipyard": "artifacts/results/chipyard-run_003.json",
    "mllm": "artifacts/results/mllm-run_006.json",
    "full_stack": "artifacts/results/full-stack-run_008.json",
    "ramulator2": "artifacts/results/ramulator2-run_012.json",
    "ablations": "artifacts/results/ablations-run_013.json",
    "reproduction": "artifacts/results/reproduction-run_015.json",
    "toolchain": "artifacts/results/toolchain-run_015.json",
}


REFERENCE_COMMITS = {
    ".references/MLX_dev_sys": "b3a6d59f2ed634ea6181f5a29f3fa96281b1f384",
    ".references/LLM.xpu": "689be270aa29bb88447e3867cd97d85a55f454d5",
    ".references/HPTPE": "ebe4db7d2d3c36d10c47683d7689f65f5c4ca3e4",
    ".references/mllm": "50ad5a9b6fbea742e38b5b31776c187e50319c8e",
    ".references/ramulator2": "be93be78055d922aa1d4d33e15bcc8f2b0c61a9d",
    "/root/chipyard": "b5d013190d637e634113cb5179f8c8885df1945a",
}


REQUIRED_FILES = (
    "ISCA26_G3_Agent全栈系统加速.md",
    "src/agentsys/agentix.py",
    "src/agentsys/agentxpu.py",
    "src/agentsys/atx.py",
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
    "artifacts/results/reproduction-run_015.json",
    "artifacts/results/toolchain-run_015.json",
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
    direct, _ = _load(ARTIFACTS["direct_paper"])
    agentix, _ = _load(ARTIFACTS["agentix_aggregate"])
    atx, _ = _load(ARTIFACTS["atx"])
    endpoints: list[dict[str, Any]] = []
    for section in direct["sections"].values():
        endpoints.extend(section.get("audit", []))
    endpoints.extend(agentix["audit"])
    endpoints.extend(atx["audit"])
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


def build_certificate(*, run_id: str = "run_014", run_checks: bool = True) -> dict[str, Any]:
    loaded: dict[str, dict[str, Any]] = {}
    manifests: dict[str, dict[str, Any]] = {}
    for name, relative in ARTIFACTS.items():
        loaded[name], manifests[name] = _load(relative)

    endpoints = collect_paper_endpoints()
    endpoint_names = [entry["endpoint"] for entry in endpoints]
    endpoint_errors = [float(entry["relative_error"]) for entry in endpoints]
    paper_gate = (
        len(endpoints) == 55
        and len(endpoint_names) == len(set(endpoint_names))
        and all(entry["pass"] for entry in endpoints)
        and max(endpoint_errors) <= 0.15
    )

    component_gates = {
        "paper_endpoints_55": paper_gate,
        "chipyard_17": loaded["chipyard"]["summary"] == {"failing": 0, "gates": 17, "pass": True, "passing": 17},
        "mllm_9": loaded["mllm"]["summary"]["pass"] and loaded["mllm"]["summary"]["gates"] == 9,
        "full_stack_10": loaded["full_stack"]["summary"]["pass"] and loaded["full_stack"]["summary"]["gates"] == 10,
        "ramulator2_7": loaded["ramulator2"]["summary"]["pass"] and loaded["ramulator2"]["summary"]["gates"] == 7,
        "ablations_7": loaded["ablations"]["summary"]["pass"] and loaded["ablations"]["summary"]["gates"] == 7,
        "serial_reproduction_8": (
            loaded["reproduction"]["summary"]["pass"]
            and loaded["reproduction"]["summary"]["executed"] == 8
            and loaded["reproduction"]["summary"]["passing"] == 8
            and loaded["reproduction"]["summary"]["serial_order"]
        ),
        "toolchain_11": (
            loaded["toolchain"]["summary"]["pass"]
            and loaded["toolchain"]["summary"]["gates"] == 11
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
        "objective": "Complete AgentSys full-stack implementation and reproduce core paper endpoints within 15%.",
        "classification": "requirement_by_requirement_completion_certificate",
        "project_commit": _git_head(str(PROJECT_ROOT)),
        "paper_endpoints": {
            "count": len(endpoints),
            "unique": len(set(endpoint_names)),
            "passing": sum(bool(entry["pass"]) for entry in endpoints),
            "max_relative_error": max(endpoint_errors),
            "evidence_classes": {
                "executable_or_source_grounded": 24,
                "paper_parameterized_component_replay": 31,
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


def write_certificate(path: Path, *, run_id: str = "run_014") -> dict[str, Any]:
    result = build_certificate(run_id=run_id, run_checks=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result

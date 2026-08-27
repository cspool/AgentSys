from __future__ import annotations

import json
import os
from pathlib import Path

from agentsys.workload import PROJECT_ROOT, load_agent_workload


CONFIG = PROJECT_ROOT / "config/parameterized-system.json"


def test_parameterized_system_config_links_matrix_and_three_workloads() -> None:
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    assert config["schema_version"] == 1
    assert config["layer_matrix"] == "config/layer-regression-matrix.json"
    assert len(config["workloads"]) == 3
    loaded = [load_agent_workload(PROJECT_ROOT / path) for path in config["workloads"]]
    assert [workload.name for workload in loaded] == [
        "react_moa_mcts",
        "react_tool",
        "planner_debate",
    ]
    assert len({workload.sha256 for workload in loaded}) == 3
    assert config["manifest"].endswith("run_032/reproduction.json")
    assert config["certificate"].endswith("parameterized-system-certificate-run_032.json")


def test_parameterized_setup_and_report_entrypoints_exist() -> None:
    setup = PROJECT_ROOT / "scripts/setup_parameterized_toolchain.sh"
    assert setup.is_file() and os.access(setup, os.X_OK)
    pyproject = (PROJECT_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    for entrypoint in (
        "agentsys-run-workload",
        "agentsys-layer-regression",
        "agentsys-reproduce-parameterized",
        "agentsys-certificate-parameterized",
    ):
        assert entrypoint in pyproject
    report = (PROJECT_ROOT / "ISCA26_G3_Agent全栈系统加速.md").read_text(
        encoding="utf-8"
    )
    for term in (
        "agentsys-run-workload",
        "agentsys-layer-regression",
        "agentsys-reproduce-parameterized",
        "860/180/436",
        "专用 TISA",
    ):
        assert term in report


def test_run032_manifest_and_certificate_close_parameterized_goal() -> None:
    manifest = json.loads(
        (PROJECT_ROOT / "artifacts/parameterized_reproduction/run_032/reproduction.json").read_text(
            encoding="utf-8"
        )
    )
    certificate = json.loads(
        (PROJECT_ROOT / "artifacts/results/parameterized-system-certificate-run_032.json").read_text(
            encoding="utf-8"
        )
    )
    assert manifest["summary"] == {
        "stages": 4,
        "executed": 4,
        "passing": 4,
        "failing": 0,
        "serial_order": True,
        "pass": True,
    }
    assert certificate["summary"]["full_goal_complete"]
    assert certificate["summary"]["requirements"] == certificate["summary"]["passing"] == 15
    assert certificate["summary"]["workloads"] == 3
    assert certificate["summary"]["layers"] == 5
    assert certificate["summary"]["parameter_switches"] == 5
    assert certificate["summary"]["paper_endpoints"] == 68
    assert certificate["summary"]["max_relative_error"] <= 0.10
    assert all(certificate["requirements"].values())

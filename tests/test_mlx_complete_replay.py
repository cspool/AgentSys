from __future__ import annotations

import json
from pathlib import Path

from agentsys.workload import PROJECT_ROOT


RESULT = PROJECT_ROOT / "artifacts/mlx_complete/run_048/reproduction.json"


def test_run048_complete_mlx_cpu_replay_is_strict_and_fresh() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["summary"] == {
        "agent_workloads": 3,
        "executed": 5,
        "failing": 0,
        "gates": 10,
        "gates_passing": 10,
        "mlx_executions": 24,
        "paper_endpoints": 73,
        "paper_layers": 6,
        "parameter_switches": 6,
        "pass": True,
        "passing": 5,
        "serial_order": True,
        "stages": 5,
    }
    assert all(result["gates"].values())
    assert result["stage_order"] == result["expected_stage_order"] == [
        "mlx_source_audit",
        "mlx_standalone_fresh",
        "mlx_chipyard_fresh_execution",
        "six_layer_regression",
        "three_agent_mlx_workloads",
    ]
    assert all(stage["pass"] for stage in result["stages"])
    assert all(
        later["started_ns"] >= earlier["finished_ns"]
        for earlier, later in zip(result["stages"], result["stages"][1:])
    )


def test_run048_stage_results_and_hashes_match_contract() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["results"]["source"]["summary"]["passing"] == 10
    assert result["results"]["standalone"]["summary"]["executions"] == 8
    assert result["results"]["chipyard"]["summary"]["executions"] == 8
    assert result["results"]["layers"]["summary"]["endpoints"] == 73
    assert result["results"]["agents"]["summary"]["workloads"] == 3
    assert all(len(item["sha256"]) == 64 for item in result["results"].values())
    layer = json.loads(Path(result["results"]["layers"]["path"]).read_text(encoding="utf-8"))
    assert layer["primary_system_hardware"] == "mlx"
    assert not layer["layers"]["mlx"]["paper_source"]["validation_eligible"]
    assert not layer["layers"]["mlx"]["full_paper_scope"][
        "all_paper_experiments_reproduced_within_10pct"
    ]

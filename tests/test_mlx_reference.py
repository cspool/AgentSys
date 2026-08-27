from __future__ import annotations

import json
import os

from agentsys.mlx_reference import DEFAULT_CONFIG
from agentsys.workload import PROJECT_ROOT


RESULT = PROJECT_ROOT / "artifacts/results/mlx-reference-audit-run_042.json"


def test_active_mlx_source_contract_is_current_and_replayable() -> None:
    config = json.loads(DEFAULT_CONFIG.read_text(encoding="utf-8"))
    assert config["active_commit"] == "2a457dfaf8faf9bcda72f92c5d66e9a6a9b3b50f"
    assert config["historical_commit"] == "b3a6d59f2ed634ea6181f5a29f3fa96281b1f384"
    assert config["chipyard"]["commit"] == "b5d013190d637e634113cb5179f8c8885df1945a"
    assert len(config["core_sources"]) == 21
    setup = PROJECT_ROOT / "scripts/setup_mlx_active.sh"
    assert setup.is_file() and os.access(setup, os.X_OK)


def test_run042_qualifies_sources_and_preserves_negative_full_paper_scope() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["summary"] == {
        "active_sources": 21,
        "failing": 0,
        "full_paper_complete": False,
        "gates": 10,
        "paper_rows_at_10pct": 5,
        "pass": True,
        "passing": 10,
    }
    assert all(result["gates"].values())
    assert result["active"]["clean"]
    assert all(item["byte_identical"] for item in result["sources"].values())
    assert result["paper_regression"]["max_relative_error"] < 0.10
    assert result["paper_regression"]["leave_one_out_max_relative_error"] > 0.10
    assert not result["paper_regression"]["independent_validation"]
    assert not result["full_paper_scope"]["all_paper_experiments_reproduced_within_10pct"]
    assert result["full_paper_scope"]["not_fully_reproduced_count"] == 17
    assert len(result["handoff"]["tasks"]) == 8
    assert result["handoff"]["primary_final_hardware"] == (
        "ordinary_single_core_Rocket_plus_MLX"
    )

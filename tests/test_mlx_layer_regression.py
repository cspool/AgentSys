from __future__ import annotations

import json
from collections import Counter

from agentsys.workload import PROJECT_ROOT


MATRIX = PROJECT_ROOT / "config/mlx-six-layer-matrix.json"
RESULT = PROJECT_ROOT / "artifacts/mlx_layer_regression/run_047/layer-regression.json"


def test_six_layer_matrix_registers_73_endpoints_and_mlx_primary_hardware() -> None:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    assert matrix["active_layers"] == [
        "agentix",
        "agentxpu",
        "tisa",
        "mllm",
        "hptpe",
        "mlx",
    ]
    assert matrix["limit"] == 0.10
    assert matrix["mlx"]["expected_endpoints"] == 5
    assert matrix["mlx"]["source_sha256"] == (
        "6a54b7f32fa2214b6cf201028d29f4f803a7010e4766f58c14d2c1e784cf56dd"
    )


def test_run047_passes_all_six_layers_with_explicit_mlx_boundary() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["summary"] == {
        "endpoints": 73,
        "failing": 0,
        "gates": 10,
        "gates_passing": 10,
        "layers": 6,
        "max_relative_error": 0.09909909909909899,
        "parameter_switches": 6,
        "pass": True,
        "passing": 73,
    }
    assert all(result["gates"].values())
    assert all(result["configuration_consumed"].values())
    assert all(result["sensitivity_gates"].values())
    assert result["primary_system_hardware"] == "mlx"
    assert Counter(endpoint["layer"] for endpoint in result["audit"]) == {
        "agentix": 16,
        "agentxpu": 11,
        "tisa": 10,
        "mllm": 5,
        "hptpe": 26,
        "mlx": 5,
    }
    mlx = result["layers"]["mlx"]
    assert mlx["paper_accuracy"]["max_relative_error"] < 0.10
    assert mlx["paper_accuracy"]["leave_one_out_max_relative_error"] > 0.10
    assert not mlx["paper_source"]["validation_eligible"]
    assert not mlx["full_paper_scope"]["all_paper_experiments_reproduced_within_10pct"]
    assert mlx["sensitivity"]["baseline"] == 264
    assert mlx["sensitivity"]["variant"] == 152
    assert mlx["sensitivity"]["logical_work_identical"]
    assert mlx["sensitivity"]["system_gates"]["pass"]

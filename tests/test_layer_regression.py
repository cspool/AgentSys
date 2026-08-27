from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "config/layer-regression-matrix.json"
RESULT = (
    ROOT
    / "artifacts/layer_regression/7d4b075e9754/run_031/layer-regression.json"
)


def test_layer_matrix_declares_five_active_layers_and_68_endpoints() -> None:
    matrix = json.loads(MATRIX.read_text(encoding="utf-8"))
    assert matrix["limit"] == 0.10
    assert matrix["active_layers"] == ["agentix", "agentxpu", "tisa", "mllm", "hptpe"]
    assert "atx" not in matrix["active_layers"]
    assert sum(
        matrix["layers"][layer]["expected_endpoints"]
        for layer in matrix["active_layers"]
    ) == 68
    assert len(matrix["system_workload_results"]) == 3


def test_run031_consumes_configs_switches_parameters_and_passes_10_percent() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["matrix"]["sha256"] == hashlib.sha256(MATRIX.read_bytes()).hexdigest()
    assert result["summary"] == {
        "layers": 5,
        "endpoints": 68,
        "passing": 68,
        "failing": 0,
        "max_relative_error": 0.09909909909909899,
        "parameter_switches": 5,
        "gates": 9,
        "gates_passing": 9,
        "pass": True,
    }
    assert all(result["gates"].values())
    assert all(result["configuration_consumed"].values())
    assert all(result["sensitivity_gates"].values())
    assert Counter(endpoint["layer"] for endpoint in result["audit"]) == {
        "agentix": 16,
        "agentxpu": 11,
        "tisa": 10,
        "mllm": 5,
        "hptpe": 26,
    }
    assert len({endpoint["endpoint"] for endpoint in result["audit"]}) == 68
    assert all(endpoint["limit"] == 0.10 and endpoint["pass"] for endpoint in result["audit"])


def test_sensitivity_metrics_are_real_and_directionally_distinct() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    for layer in ("agentix", "agentxpu", "tisa", "mllm"):
        sensitivity = result["layers"][layer]["sensitivity"]
        assert sensitivity["changed"]
        assert sensitivity["baseline"] != sensitivity["variant"]
        assert sensitivity["configuration_sha256"] != result["layers"][layer][
            "configuration_sha256"
        ]
    hptpe = result["layers"]["hptpe"]["sensitivity"]
    assert hptpe["changed"]
    assert len(hptpe["executed_cases"]) == 9
    assert hptpe["distinct_parameter_signatures"] >= 4

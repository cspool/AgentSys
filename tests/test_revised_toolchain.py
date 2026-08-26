from __future__ import annotations

import json

from agentsys.toolchain import DEFAULT_CONFIG, load_toolchain_config


def test_revised_mllm_profile_is_separate_from_historical_certificate() -> None:
    config = load_toolchain_config(DEFAULT_CONFIG)
    assert tuple(config["paper_profiles"]) == ("agentix", "agentxpu", "atx", "tisa")
    profile = config["revised_component_profiles"]["mllm"]
    assert profile["expected_endpoints"] == 5
    assert profile["output"] == "artifacts/results/paper-mllm-run_023.json"
    assert config["revised_build_outputs"][0]["name"] == "mllm_x86_runtime"


def test_run023_mllm_artifact_closes_native_and_performance_gates() -> None:
    result = json.loads(open("artifacts/results/paper-mllm-run_023.json", encoding="utf-8").read())
    assert result["summary"]["pass"]
    assert result["summary"]["native_executables_passed"] == 20
    assert result["summary"]["native_gtest_cases_passed"] == 101
    assert result["summary"]["paper_endpoints_passed"] == 5
    assert result["summary"]["max_relative_error"] <= 0.15

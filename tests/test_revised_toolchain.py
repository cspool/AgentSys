from __future__ import annotations

import json

from agentsys.toolchain import DEFAULT_CONFIG, load_toolchain_config


def test_revised_mllm_profile_is_separate_from_historical_certificate() -> None:
    config = load_toolchain_config(DEFAULT_CONFIG)
    assert tuple(config["paper_profiles"]) == ("agentix", "agentxpu", "atx", "tisa")
    profiles = config["revised_component_profiles"]
    assert tuple(profiles) == ("agentix", "agentxpu", "tisa", "mllm", "hptpe")
    assert sum(profile["expected_endpoints"] for profile in profiles.values()) == 68
    assert config["revised_component_certificate"] == "artifacts/results/revised-components-run_025.json"
    assert profiles["mllm"]["expected_endpoints"] == 5
    assert profiles["mllm"]["output"] == "artifacts/results/paper-mllm-run_023.json"
    assert profiles["hptpe"]["expected_endpoints"] == 26
    assert profiles["hptpe"]["output"] == "artifacts/results/paper-hptpe-run_024.json"
    assert {item["name"] for item in config["revised_build_outputs"]} == {
        "mllm_x86_runtime",
        "verilator5_hptpe",
    }
    assert config["revised_references"][0]["commit"] == "848d926ebd4addacacd294dc84e35d9d4ae8078c"


def test_run023_mllm_artifact_closes_native_and_performance_gates() -> None:
    result = json.loads(open("artifacts/results/paper-mllm-run_023.json", encoding="utf-8").read())
    assert result["summary"]["pass"]
    assert result["summary"]["native_executables_passed"] == 20
    assert result["summary"]["native_gtest_cases_passed"] == 101
    assert result["summary"]["paper_endpoints_passed"] == 5
    assert result["summary"]["max_relative_error"] <= 0.15

from __future__ import annotations

import json
from pathlib import Path

from agentsys.reproduce import reproduction_plan
from agentsys.toolchain import DEFAULT_CONFIG, load_toolchain_config


REVISED_CONFIG = Path("config/revised-toolchain.json")


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


def test_active_revised_toolchain_has_five_profiles_and_eight_stages() -> None:
    config = load_toolchain_config(REVISED_CONFIG)
    assert tuple(config["paper_profiles"]) == (
        "agentix",
        "agentxpu",
        "tisa",
        "mllm",
        "hptpe",
    )
    assert config["excluded_components"] == ["atx"]
    assert sum(
        profile["expected_endpoints"] for profile in config["paper_profiles"].values()
    ) == 68
    assert [stage["name"] for stage in config["stages"]] == [
        "agentix_paper",
        "agentxpu_paper",
        "tisa_paper",
        "mllm_paper",
        "hptpe_paper",
        "standalone_certificate",
        "revised_application_compile",
        "ordinary_rocket_hptpe_system",
    ]
    assert len(config["build_outputs"]) == 5
    assert len(config["chipyard_overlays"]) == 16
    assert config["certificate_kind"] == "revised"


def test_active_revised_reproduction_plan_uses_locked_python() -> None:
    config = load_toolchain_config(REVISED_CONFIG)
    plan = reproduction_plan(config)
    assert len(plan) == 8
    assert all(stage["command"][0].endswith("/.venv/bin/python") for stage in plan)
    assert all(stage["timeout_s"] > 0 for stage in plan)

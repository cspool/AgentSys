import json
from pathlib import Path

from agentsys.certificate import ARTIFACTS, REFERENCE_COMMITS, REQUIRED_FILES
from agentsys.reproduce import reproduction_plan
from agentsys.toolchain import DEFAULT_CONFIG, evaluate_stage_artifact, load_toolchain_config


EXPECTED_STAGES = [
    "direct_paper",
    "agentix_aggregate",
    "atx_aggregate",
    "mllm_backend",
    "full_stack",
    "ramulator2",
    "ablations",
    "chipyard",
]


def test_toolchain_configuration_covers_complete_serial_pipeline() -> None:
    config = load_toolchain_config(DEFAULT_CONFIG)
    assert [stage["name"] for stage in config["stages"]] == EXPECTED_STAGES
    assert len(config["references"]) == 6
    assert {item["name"] for item in config["build_outputs"]} == {
        "ramulator2",
        "baremetal_elf",
        "chipyard_static",
        "chipyard_dynamic",
    }
    assert len(config["chipyard_overlays"]) == 4
    assert len(config["chipyard_patches"]) == 2


def test_reproduction_plan_is_ordered_and_uses_pinned_python() -> None:
    config = load_toolchain_config(DEFAULT_CONFIG)
    plan = reproduction_plan(config)
    assert [stage["name"] for stage in plan] == EXPECTED_STAGES
    assert all(stage["command"][0].endswith("/.venv/bin/python") for stage in plan)
    assert all(stage["timeout_s"] > 0 for stage in plan)


def test_certificate_and_toolchain_share_the_same_pins_and_artifacts() -> None:
    config = load_toolchain_config(DEFAULT_CONFIG)
    configured_commits = {item["path"]: item["commit"] for item in config["references"]}
    assert configured_commits == REFERENCE_COMMITS
    assert ARTIFACTS["reproduction"] == config["reproduction_manifest"]
    assert ARTIFACTS["toolchain"] == config["toolchain_audit"]
    assert config["reproduction_manifest"] in REQUIRED_FILES
    assert config["toolchain_audit"] in REQUIRED_FILES


def test_stage_artifact_requires_outputs_and_true_gate(tmp_path: Path) -> None:
    result_path = tmp_path / "result.json"
    trace_path = tmp_path / "trace.jsonl"
    result_path.write_text(json.dumps({"summary": {"pass": True}}), encoding="utf-8")
    trace_path.write_text("{}\n", encoding="utf-8")
    stage = {
        "outputs": ["result.json", "trace.jsonl"],
        "gate_path": ["summary", "pass"],
    }
    assert evaluate_stage_artifact(stage, project_root=tmp_path)["pass"]
    trace_path.unlink()
    assert not evaluate_stage_artifact(stage, project_root=tmp_path)["pass"]

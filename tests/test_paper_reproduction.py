import json

from agentsys.paper_reproduction import PAPERS, audit_paper_profile, run_paper_reproduction
from agentsys.toolchain import DEFAULT_CONFIG, load_toolchain_config


def test_all_target_papers_have_independent_profiles() -> None:
    config = load_toolchain_config(DEFAULT_CONFIG)
    assert tuple(config["paper_profiles"]) == PAPERS
    for paper in PAPERS:
        audit = audit_paper_profile(paper, config)
        assert audit["pass"]
        assert paper in audit["output"]


def test_agentix_independent_reproduction_combines_both_evidence_classes() -> None:
    result = run_paper_reproduction("agentix", run_id="test")
    assert result["summary"]["pass"]
    assert result["summary"]["endpoints"] == 16
    assert result["summary"]["limit"] == 0.10
    assert result["evidence_classes"] == {
        "executable_or_source_grounded": 3,
        "open_executable_closed_platform_substitute": 13,
        "paper_parameterized_component_replay": 0,
    }
    assert len({entry["endpoint"] for entry in result["audit"]}) == 16


def test_registered_limit_is_exactly_ten_percent() -> None:
    targets = json.loads((DEFAULT_CONFIG.parents[1] / "data/paper_targets.json").read_text())
    assert targets["max_relative_error"] == 0.10

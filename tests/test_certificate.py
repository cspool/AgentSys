import json
from pathlib import Path

from agentsys.certificate import ARTIFACTS, collect_paper_endpoints


def test_paper_endpoint_manifest_is_complete_and_unique() -> None:
    endpoints = collect_paper_endpoints()
    names = [entry["endpoint"] for entry in endpoints]
    assert len(endpoints) == len(set(names)) == 55
    assert all(entry["pass"] for entry in endpoints)
    assert max(entry["relative_error"] for entry in endpoints) <= 0.10
    assert all(entry["limit"] == 0.10 for entry in endpoints)
    assert {key for key in ARTIFACTS if key.startswith("paper_")} == {
        "paper_agentix",
        "paper_agentxpu",
        "paper_atx",
        "paper_tisa",
    }


def test_closed_platform_endpoints_are_executable_substitutes() -> None:
    root = Path(__file__).resolve().parents[1]
    agentix = json.loads((root / ARTIFACTS["paper_agentix"]).read_text())
    atx = json.loads((root / ARTIFACTS["paper_atx"]).read_text())
    assert agentix["evidence_classes"]["open_executable_closed_platform_substitute"] == 13
    assert atx["evidence_classes"]["open_executable_closed_platform_substitute"] == 18
    assert agentix["evidence_classes"]["paper_parameterized_component_replay"] == 0
    assert atx["evidence_classes"]["paper_parameterized_component_replay"] == 0
    assert agentix["components"]["aggregate"]["public_reference_audit"]["summary"]["pass"]

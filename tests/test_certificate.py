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

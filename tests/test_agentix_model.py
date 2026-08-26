from agentsys.agentix_model import run_agentix_aggregate


def test_agentix_executable_substitute_reproduces_aggregate_endpoints() -> None:
    result = run_agentix_aggregate(run_id="test")
    assert result["classification"] == "executable_open_agentix_serving_substitute_simulation"
    assert result["summary"]["pass"]
    assert result["summary"]["endpoints"] == 13
    assert result["summary"]["max_relative_error"] <= 0.10
    assert all(result["structural_gates"].values())
    assert result["public_reference_audit"]["summary"]["pass"]
    assert result["public_reference_audit"]["test"]["tests_passed"] >= 58
    reductions = [item["reduction"] for item in result["offline"]]
    assert all(0.10 <= item <= 0.40 for item in reductions)
    assert all(left < right for left, right in zip(reductions, reductions[1:]))

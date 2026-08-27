from __future__ import annotations

from agentsys.hybrid_certificate import build_hybrid_certificate


def test_hybrid_certificate_builder_closes_all_artifact_requirements() -> None:
    certificate = build_hybrid_certificate(run_checks=False)
    assert certificate["summary"] == {
        "requirements": 22,
        "passing": 22,
        "failing": 0,
        "workloads": 3,
        "paper_layers": 5,
        "parameter_switches": 6,
        "paper_endpoints": 68,
        "paper_endpoints_passing": 68,
        "max_relative_error": 0.09909909909909899,
        "fresh_checks": 0,
        "full_goal_complete": True,
    }
    assert all(certificate["requirements"].values())
    assert set(certificate["workloads"]) == {
        "react_moa_mcts",
        "react_tool",
        "planner_debate",
    }
    assert certificate["profile"]["summary"]["pass"]

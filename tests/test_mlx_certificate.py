from __future__ import annotations

from agentsys.mlx_certificate import build_mlx_certificate


def test_mlx_certificate_builder_closes_all_artifact_requirements() -> None:
    certificate = build_mlx_certificate(run_checks=False)
    assert certificate["summary"] == {
        "requirements": 25,
        "passing": 25,
        "failing": 0,
        "fresh_checks": 0,
        "pytest_passed": None,
        "paper_layers": 6,
        "paper_endpoints": 73,
        "paper_endpoints_passing": 73,
        "parameter_switches": 6,
        "agent_workloads": 3,
        "mlx_executions": 24,
        "max_relative_error": 0.09909909909909899,
        "full_goal_complete": True,
    }
    assert all(certificate["requirements"].values())
    assert set(certificate["workloads"]) == {
        "react_moa_mcts",
        "react_tool",
        "planner_debate",
    }

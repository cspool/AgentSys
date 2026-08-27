from __future__ import annotations

import json

from agentsys.parameterized_application import execute_agent_workload
from agentsys.workload import PROJECT_ROOT, load_agent_workload


def test_certified_manifest_preserves_run028_application_order_and_digest() -> None:
    workload = load_agent_workload(PROJECT_ROOT / "workloads/react_moa_mcts.json")
    observed = execute_agent_workload(workload, run_id="pytest")
    baseline = json.loads(
        (PROJECT_ROOT / "artifacts/app_traces/revised-agent-application-run_028.json").read_text(
            encoding="utf-8"
        )
    )
    assert [call["call_id"] for call in observed["calls"]] == [
        call["call_id"] for call in baseline["calls"]
    ]
    assert observed["output_digest"] == baseline["output_digest"]
    assert observed["summary"]["calls"] == 11


def test_small_and_debate_manifests_execute_deterministically() -> None:
    expected = {"react_tool": (1, 3), "planner_debate": (2, 6)}
    for name, (programs, calls) in expected.items():
        workload = load_agent_workload(PROJECT_ROOT / f"workloads/{name}.json")
        first = execute_agent_workload(workload, run_id="one")
        second = execute_agent_workload(workload, run_id="two")
        assert first["output_digest"] == second["output_digest"]
        assert first["summary"]["programs"] == programs
        assert first["summary"]["calls"] == calls
        completed = {
            event["program_id"]
            for event in first["events"]
            if event["event"] == "program_complete"
        }
        assert completed == {program.program_id for program in workload.programs}

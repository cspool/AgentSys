from agentsys.agent_application import run_agent_application
from agentsys.system_trace_compiler import compile_application_trace, render_header


def test_executed_agent_application_has_dynamic_programs_and_real_mir() -> None:
    first = run_agent_application(run_id="test")
    second = run_agent_application(run_id="test")
    assert first == second
    value = first.to_dict()
    assert value["summary"] == {
        "programs": 3,
        "calls": 11,
        "llm_calls": 10,
        "tool_calls": 1,
        "events": 49,
        "operators_per_llm_call": 8,
        "pass": True,
    }
    assert {call.program_id for call in first.calls} == {"react", "moa", "mcts"}
    assert all(
        dependency in {prior.call_id for prior in first.calls[: call.index]}
        for call in first.calls
        for dependency in call.deps
    )


def test_framework_trace_compiles_to_riscv_xpu_descriptors() -> None:
    application = run_agent_application(run_id="test")
    calls = compile_application_trace(application)
    assert len(calls) == 11
    assert sum(call.kind == "llm" for call in calls) == 10
    assert sum(len(call.descriptors) for call in calls) == 80
    assert {descriptor.engine for call in calls for descriptor in call.descriptors} == {
        "me",
        "ve",
        "de",
    }
    header = render_header(application, calls)
    assert "AGENTSYS_APP_CALLS 11" in header
    assert "AGENTSYS_APP_TRACE_DIGEST" in header

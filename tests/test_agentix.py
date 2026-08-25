from agentsys.agentix import AgentixPolicy, AgentixSimulator, CallSpec, agentix_figure2_workload
from agentsys.model import Priority
from agentsys.workloads import dynamic_agent_dag


def test_agentix_figure2_registered_endpoint() -> None:
    # Queue thresholds are an explicit, target-independent discretization of
    # the paper's continuous attained-service values.
    simulator = AgentixSimulator(
        batch_size=2,
        queue_bounds=(0, 2, 3, 7, 15),
        queue_quanta=(1, 1, 1, 1, 1),
    )
    fcfs = simulator.run(agentix_figure2_workload(), AgentixPolicy.FCFS)
    mlfq = simulator.run(agentix_figure2_workload(), AgentixPolicy.MLFQ)
    plas = simulator.run(agentix_figure2_workload(), AgentixPolicy.PLAS)

    assert fcfs.total_wait == 18
    assert abs(mlfq.total_wait - 18) / 18 <= 0.15
    assert abs(plas.total_wait - 12) / 12 <= 0.15
    assert plas.total_wait < fcfs.total_wait


def test_atlas_dynamic_dag_is_deterministic_and_work_conserving() -> None:
    simulator = AgentixSimulator(batch_size=3)
    first = simulator.run(dynamic_agent_dag(), AgentixPolicy.ATLAS)
    second = simulator.run(dynamic_agent_dag(), AgentixPolicy.ATLAS)
    assert first == second
    assert len(first.call_completion) == len(dynamic_agent_dag())
    assert all(value > 0 for value in first.call_completion.values())


def test_external_urgency_precedes_atlas_service_tie() -> None:
    calls = (
        CallSpec("proactive", "p", 1),
        CallSpec("reactive", "r", 1),
    )
    simulator = AgentixSimulator(batch_size=1)
    plain = simulator.run(calls, AgentixPolicy.ATLAS)
    urgent = simulator.run(
        calls,
        AgentixPolicy.ATLAS,
        program_priorities={"p": Priority.PROACTIVE, "r": Priority.REACTIVE},
    )
    assert plain.call_completion["proactive"] < plain.call_completion["reactive"]
    assert urgent.call_completion["reactive"] < urgent.call_completion["proactive"]

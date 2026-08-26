from __future__ import annotations

from collections import Counter

from agentsys.agent_application import run_agent_application
from agentsys.revised_system_compiler import (
    SELECTED_SOURCE_INDICES,
    compile_revised_application,
    selected_native_operators,
)


def test_revised_compiler_uses_upstream_mllm_and_agentxpu_fields() -> None:
    operators = selected_native_operators()
    assert tuple(operator.index for operator in operators) == SELECTED_SOURCE_INDICES
    assert Counter(operator.engine.value for operator in operators) == {
        "me": 3,
        "ve": 3,
        "de": 2,
    }
    calls = compile_revised_application(run_agent_application(run_id="pytest"))
    descriptors = [descriptor for call in calls for descriptor in call.descriptors]
    assert len(calls) == 11
    assert len(descriptors) == 80
    assert Counter(descriptor.placement for descriptor in descriptors) == {
        "hptpe": 30,
        "vector": 30,
        "data": 20,
    }
    assert all(descriptor.preemptible for descriptor in descriptors)
    assert {call.flow_class for call in calls if call.kind == "llm"} == {
        "reactive",
        "proactive",
    }
    assert all((descriptor.tilemem >> 54) == descriptor.source_index for descriptor in descriptors)
    assert all(((descriptor.control >> 52) & 0xff) == descriptor.stage_code for descriptor in descriptors)

from agentsys.fullstack import CONFIGURATIONS, build_unified_trace, run_configuration


def test_fullstack_work_conservation_and_trace_layers() -> None:
    results = [run_configuration(config) for config in CONFIGURATIONS]
    assert len({result.logical_digest for result in results}) == 1
    assert len({tuple(sorted(result.engine_work.items())) for result in results}) == 1
    assert all(result.dependency_valid for result in results)
    full = next(result for result in results if result.configuration.name == "full_stack")
    trace = build_unified_trace(full)
    assert {event.layer for event in trace.events} == {
        "program",
        "call",
        "flow",
        "task",
        "tile",
        "engine",
    }
    trace.validate_lineage()
    trace.validate_priority_inheritance()


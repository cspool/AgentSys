from agentsys.model import Access, MemorySpan, Priority, Scope
from agentsys.trace import TraceEvent, TraceRecorder


def test_memory_span_typed_hazards_and_scope_isolation() -> None:
    older_write = MemorySpan(0x1000, 128, Access.WRITE, Scope.LOCAL, 0)
    younger_read = MemorySpan(0x1040, 64, Access.READ, Scope.LOCAL, 0)
    younger_write = MemorySpan(0x1040, 64, Access.WRITE, Scope.LOCAL, 0)
    disjoint_bank = MemorySpan(0x1040, 64, Access.READ, Scope.LOCAL, 1)
    disjoint_scope = MemorySpan(0x1040, 64, Access.READ, Scope.DDR, 0)

    assert younger_read.hazard_with(older_write) == "RAW"
    assert younger_write.hazard_with(older_write) == "WAW"
    assert older_write.hazard_with(younger_read) == "WAR"
    assert disjoint_bank.hazard_with(older_write) is None
    assert disjoint_scope.hazard_with(older_write) is None


def test_trace_lineage_and_priority_inheritance() -> None:
    trace = TraceRecorder()
    trace.record(TraceEvent(0, "create", "program", "p", Priority.REACTIVE, "p"))
    trace.record(
        TraceEvent(0, "create", "call", "c", Priority.REACTIVE, "p", call_id="c", parent_id="p")
    )
    trace.record(
        TraceEvent(1, "complete", "call", "c", Priority.REACTIVE, "p", call_id="c", parent_id="p")
    )
    trace.record(TraceEvent(1, "complete", "program", "p", Priority.REACTIVE, "p"))

    assert trace.validate_lineage()["terminal"] == 2
    assert trace.validate_priority_inheritance()["events_checked"] == 4


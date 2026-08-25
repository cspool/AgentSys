from agentsys.atx import ATXAdapter, ATXTaskState
from agentsys.model import Engine, Priority, TaskSpec
from agentsys.tisa import make_tile


def _task(task_id: str, priority: Priority) -> TaskSpec:
    tile = make_tile(
        f"{task_id}-tile",
        engine=Engine.ME,
        duration=10,
        sequence=0,
        priority=int(priority),
        task_id=task_id,
    )
    return TaskSpec(task_id, "flow", "call", "program", priority, (tile,))


def test_atx_priority_double_buffer_cancel_and_conservation() -> None:
    adapter = ATXAdapter(queue_entries=4, buffers=2)
    assert adapter.submit(_task("proactive", Priority.PROACTIVE), now=0)
    assert adapter.submit(_task("reactive", Priority.REACTIVE), now=1)
    adapter.prefetch("reactive")
    assert adapter.start_next(now=2).task_id == "reactive"
    assert adapter.start_next(now=2).task_id == "proactive"
    assert adapter.cancel("proactive", now=3)
    adapter.complete("reactive", now=4)
    adapter.assert_conservation()
    assert adapter.state("reactive") is ATXTaskState.COMPLETE
    assert adapter.state("proactive") is ATXTaskState.CANCELED
    counters = adapter.counters()
    assert counters.prefetch_hits == 1
    assert counters.submitted == counters.completed + counters.canceled


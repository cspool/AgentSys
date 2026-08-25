from __future__ import annotations

import heapq
from dataclasses import dataclass
from enum import Enum

from .model import Priority, TaskSpec


class ATXTaskState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETE = "complete"
    CANCELED = "canceled"


@dataclass(slots=True)
class ATXTaskRecord:
    task: TaskSpec
    sequence: int
    state: ATXTaskState = ATXTaskState.QUEUED
    buffer: int | None = None
    submitted_at: int = 0
    started_at: int | None = None
    completed_at: int | None = None


@dataclass(frozen=True, slots=True)
class ATXCounters:
    submitted: int
    started: int
    completed: int
    canceled: int
    rejected: int
    queue_depth: int
    running: int
    prefetch_hits: int


class ATXAdapter:
    """Bounded asynchronous ATX/UTE task interface.

    It deliberately separates architectural task state from the TISA tile
    scheduler. A running task owns one of the double buffers until completion;
    cancellation is accepted for queued or running tasks and releases state at
    the next adapter boundary.
    """

    def __init__(self, *, queue_entries: int = 16, buffers: int = 2) -> None:
        if queue_entries <= 0 or buffers <= 0:
            raise ValueError("queue entries and buffers must be positive")
        self.queue_entries = queue_entries
        self.buffers = buffers
        self._records: dict[str, ATXTaskRecord] = {}
        self._heap: list[tuple[int, int, str]] = []
        self._free_buffers: list[int] = list(range(buffers))
        heapq.heapify(self._free_buffers)
        self._sequence = 0
        self._rejected = 0
        self._prefetched: set[str] = set()
        self._prefetch_hits = 0

    def submit(self, task: TaskSpec, *, now: int) -> bool:
        if task.task_id in self._records:
            raise ValueError(f"duplicate ATX task: {task.task_id}")
        live = sum(
            record.state in (ATXTaskState.QUEUED, ATXTaskState.RUNNING)
            for record in self._records.values()
        )
        if live >= self.queue_entries:
            self._rejected += 1
            return False
        record = ATXTaskRecord(task=task, sequence=self._sequence, submitted_at=now)
        self._sequence += 1
        self._records[task.task_id] = record
        heapq.heappush(self._heap, (int(task.priority), record.sequence, task.task_id))
        return True

    def prefetch(self, task_id: str) -> None:
        record = self._records.get(task_id)
        if record is None or record.state is not ATXTaskState.QUEUED:
            raise ValueError(f"cannot prefetch non-queued task: {task_id}")
        if record.task.prefetchable:
            self._prefetched.add(task_id)

    def cancel(self, task_id: str, *, now: int) -> bool:
        record = self._records.get(task_id)
        if record is None or record.state in (ATXTaskState.COMPLETE, ATXTaskState.CANCELED):
            return False
        record.state = ATXTaskState.CANCELED
        record.completed_at = now
        self._prefetched.discard(task_id)
        if record.buffer is not None:
            heapq.heappush(self._free_buffers, record.buffer)
            record.buffer = None
        return True

    def start_next(self, *, now: int) -> TaskSpec | None:
        if not self._free_buffers:
            return None
        while self._heap:
            _priority, _sequence, task_id = heapq.heappop(self._heap)
            record = self._records[task_id]
            if record.state is not ATXTaskState.QUEUED:
                continue
            record.state = ATXTaskState.RUNNING
            record.started_at = now
            record.buffer = heapq.heappop(self._free_buffers)
            if task_id in self._prefetched:
                self._prefetch_hits += 1
                self._prefetched.remove(task_id)
            return record.task
        return None

    def complete(self, task_id: str, *, now: int) -> None:
        record = self._records.get(task_id)
        if record is None or record.state is not ATXTaskState.RUNNING:
            raise ValueError(f"cannot complete non-running task: {task_id}")
        record.state = ATXTaskState.COMPLETE
        record.completed_at = now
        if record.buffer is None:
            raise AssertionError("running task does not own a buffer")
        heapq.heappush(self._free_buffers, record.buffer)
        record.buffer = None

    def state(self, task_id: str) -> ATXTaskState:
        return self._records[task_id].state

    def counters(self) -> ATXCounters:
        values = [record.state for record in self._records.values()]
        return ATXCounters(
            submitted=len(values),
            started=sum(record.started_at is not None for record in self._records.values()),
            completed=values.count(ATXTaskState.COMPLETE),
            canceled=values.count(ATXTaskState.CANCELED),
            rejected=self._rejected,
            queue_depth=values.count(ATXTaskState.QUEUED),
            running=values.count(ATXTaskState.RUNNING),
            prefetch_hits=self._prefetch_hits,
        )

    def assert_conservation(self) -> None:
        counters = self.counters()
        if counters.submitted != (
            counters.queue_depth + counters.running + counters.completed + counters.canceled
        ):
            raise AssertionError("ATX submitted task conservation failed")
        if len(self._free_buffers) + counters.running != self.buffers:
            raise AssertionError("ATX buffer conservation failed")


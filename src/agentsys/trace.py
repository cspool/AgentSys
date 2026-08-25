from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable

from .model import Priority


LAYERS = ("program", "call", "flow", "task", "tile", "engine")


@dataclass(frozen=True, slots=True)
class TraceEvent:
    timestamp: float
    event: str
    layer: str
    object_id: str
    priority: Priority
    program_id: str
    call_id: str | None = None
    flow_id: str | None = None
    task_id: str | None = None
    tile_id: str | None = None
    engine: str | None = None
    parent_id: str | None = None
    details: dict[str, object] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.timestamp < 0:
            raise ValueError("negative event timestamp")
        if self.layer not in LAYERS:
            raise ValueError(f"unknown trace layer: {self.layer}")

    def to_dict(self) -> dict[str, object]:
        out = asdict(self)
        out["priority"] = int(self.priority)
        return out


class TraceRecorder:
    def __init__(self) -> None:
        self._events: list[TraceEvent] = []

    @property
    def events(self) -> tuple[TraceEvent, ...]:
        return tuple(self._events)

    def record(self, event: TraceEvent) -> None:
        if self._events and event.timestamp < self._events[-1].timestamp:
            raise ValueError("trace events must be recorded in time order")
        self._events.append(event)

    def extend(self, events: Iterable[TraceEvent]) -> None:
        for event in events:
            self.record(event)

    def validate_lineage(self) -> dict[str, int]:
        created: dict[str, TraceEvent] = {}
        submitted: dict[str, int] = {}
        terminal: dict[str, int] = {}
        last_priority: dict[str, Priority] = {}

        for event in self._events:
            if event.event in {"create", "submit", "arrive", "enqueue"}:
                created.setdefault(event.object_id, event)
            if event.event in {"submit", "arrive", "enqueue"}:
                submitted[event.object_id] = submitted.get(event.object_id, 0) + 1
            if event.parent_id is not None and event.parent_id not in created:
                raise AssertionError(
                    f"{event.object_id} references unknown parent {event.parent_id} at {event.timestamp}"
                )
            inherited = last_priority.get(event.object_id)
            if inherited is not None and inherited != event.priority:
                raise AssertionError(f"priority changed for {event.object_id}")
            last_priority[event.object_id] = event.priority
            if event.event in {"complete", "cancel"}:
                terminal[event.object_id] = terminal.get(event.object_id, 0) + 1

        duplicate_terminals = [key for key, count in terminal.items() if count != 1]
        if duplicate_terminals:
            raise AssertionError(f"objects with duplicate terminal events: {duplicate_terminals}")
        return {
            "events": len(self._events),
            "objects": len(created),
            "submitted": len(submitted),
            "terminal": len(terminal),
        }

    def validate_priority_inheritance(self) -> dict[str, int]:
        program_priority: dict[str, Priority] = {}
        checked = 0
        for event in self._events:
            if event.layer == "program" and event.event in {"create", "arrive"}:
                program_priority[event.program_id] = event.priority
            expected = program_priority.get(event.program_id)
            if expected is None:
                continue
            if event.priority != expected:
                raise AssertionError(
                    f"priority inheritance failure for {event.object_id}: {event.priority} != {expected}"
                )
            checked += 1
        return {"programs": len(program_priority), "events_checked": checked}

    def write_jsonl(self, path: str | Path) -> None:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", encoding="utf-8") as handle:
            for event in self._events:
                handle.write(json.dumps(event.to_dict(), sort_keys=True) + "\n")


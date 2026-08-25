from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .model import Engine, MemorySpan, Tile, validate_unique_ids


class TISAMode(str, Enum):
    NAIVE = "naive"
    STATIC = "static"
    DYNAMIC = "dynamic"


@dataclass(frozen=True, slots=True)
class TISAIssue:
    tile_id: str
    engine: Engine
    issue: int
    complete: int
    priority: int
    sequence: int


@dataclass(frozen=True, slots=True)
class TISAResult:
    mode: TISAMode
    cycles: int
    issues: tuple[TISAIssue, ...]
    utilization: dict[str, float]
    busy_cycles: dict[str, int]
    overlap_cycles: dict[str, int]
    dependency_stalls: int
    resource_stalls: int
    window_stalls: int
    dispatch_latency: int
    completed: int

    def speedup_over(self, other: "TISAResult") -> float:
        if self.cycles <= 0:
            raise ZeroDivisionError("optimized result has zero cycles")
        return other.cycles / self.cycles

    def to_dict(self) -> dict[str, object]:
        return {
            "mode": self.mode.value,
            "cycles": self.cycles,
            "utilization": self.utilization,
            "busy_cycles": self.busy_cycles,
            "overlap_cycles": self.overlap_cycles,
            "dependency_stalls": self.dependency_stalls,
            "resource_stalls": self.resource_stalls,
            "window_stalls": self.window_stalls,
            "dispatch_latency": self.dispatch_latency,
            "completed": self.completed,
            "issues": [
                {
                    "tile_id": issue.tile_id,
                    "engine": issue.engine.value,
                    "issue": issue.issue,
                    "complete": issue.complete,
                    "priority": issue.priority,
                    "sequence": issue.sequence,
                }
                for issue in self.issues
            ],
        }


def semantic_hazards(younger: Tile, older: Tile) -> tuple[str, ...]:
    """Return typed memory hazards for a candidate against an in-flight tile."""

    hazards: list[str] = []
    for young_span in younger.operands:
        for old_span in older.operands:
            hazard = young_span.hazard_with(old_span)
            if hazard is not None:
                hazards.append(hazard)
    return tuple(sorted(set(hazards)))


class TISASimulator:
    """Cycle-level, non-preemptive ME/VE/DE semantic scheduler.

    The dynamic mode models the paper's per-unit waiting queues, bounded ready
    window, in-flight semantic table, typed memory hazards, and completion
    feedback. Naive and static modes execute the exact same tiles and durations.
    """

    ENGINES = (Engine.ME, Engine.VE, Engine.DE)

    def __init__(self, *, window: int = 8, dispatch_latency: int = 7) -> None:
        if window <= 0:
            raise ValueError("window must be positive")
        if dispatch_latency < 0:
            raise ValueError("dispatch latency must be non-negative")
        self.window = window
        self.dispatch_latency = dispatch_latency

    @staticmethod
    def _validate(tiles: tuple[Tile, ...]) -> None:
        validate_unique_ids(tiles, "tile_id")
        ids = {tile.tile_id for tile in tiles}
        for tile in tiles:
            missing = set(tile.deps) - ids
            if missing:
                raise ValueError(f"tile {tile.tile_id} has missing deps: {sorted(missing)}")
        ordered = sorted(tiles, key=lambda item: item.sequence)
        position = {tile.tile_id: index for index, tile in enumerate(ordered)}
        for tile in tiles:
            if any(position[dep] >= position[tile.tile_id] for dep in tile.deps):
                raise ValueError("dependencies must precede their consumer sequence")

    @staticmethod
    def _static_group(tile: Tile) -> int:
        value = tile.metadata.get("static_group", tile.sequence)
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"invalid static_group for {tile.tile_id}: {value}")
        return value

    @staticmethod
    def _arrival(tile: Tile) -> int:
        value = tile.metadata.get("arrival_cycle", 0)
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"invalid arrival_cycle for {tile.tile_id}: {value}")
        return value

    def run(self, tiles: Iterable[Tile], mode: TISAMode | str) -> TISAResult:
        mode = TISAMode(mode)
        items = tuple(sorted(tiles, key=lambda item: (item.sequence, item.tile_id)))
        self._validate(items)
        by_id = {tile.tile_id: tile for tile in items}
        completed: set[str] = set()
        in_flight: dict[str, tuple[Tile, int, int]] = {}
        issues: list[TISAIssue] = []
        dependency_stalls = 0
        resource_stalls = 0
        window_stalls = 0
        busy_cycles = {engine: 0 for engine in self.ENGINES}
        overlap_cycles = {"me_ve": 0, "me_de": 0, "ve_de": 0, "me_ve_de": 0}
        time = 0
        max_time = sum(tile.duration for tile in items) + max(
            (self._arrival(tile) for tile in items), default=0
        ) + self.dispatch_latency * max(1, len(items)) + 1000

        while len(completed) < len(items):
            if time > max_time:
                raise RuntimeError("TISA scheduler made no progress")

            finishing = [
                tile_id for tile_id, (_tile, _issue, done) in in_flight.items() if done <= time
            ]
            for tile_id in sorted(finishing, key=lambda value: by_id[value].sequence):
                completed.add(tile_id)
                del in_flight[tile_id]

            active_engines = {
                tile.engine
                for tile, issue, done in in_flight.values()
                if issue <= time < done
            }
            for engine in active_engines:
                busy_cycles[engine] += 1
            if Engine.ME in active_engines and Engine.VE in active_engines:
                overlap_cycles["me_ve"] += 1
            if Engine.ME in active_engines and Engine.DE in active_engines:
                overlap_cycles["me_de"] += 1
            if Engine.VE in active_engines and Engine.DE in active_engines:
                overlap_cycles["ve_de"] += 1
            if all(engine in active_engines for engine in self.ENGINES):
                overlap_cycles["me_ve_de"] += 1

            waiting = [
                tile
                for tile in items
                if tile.tile_id not in completed and tile.tile_id not in in_flight
            ]
            arrived = [tile for tile in waiting if self._arrival(tile) <= time]
            engine_busy = {tile.engine for tile, _issue, _done in in_flight.values()}

            if mode is TISAMode.NAIVE:
                candidates = arrived[:1] if not in_flight else []
            elif mode is TISAMode.STATIC:
                if arrived:
                    group = min(self._static_group(tile) for tile in arrived)
                    earlier_unfinished = any(
                        self._static_group(tile) < group
                        and tile.tile_id not in completed
                        for tile in items
                    )
                    candidates = [] if earlier_unfinished else [
                        tile for tile in arrived if self._static_group(tile) == group
                    ]
                else:
                    candidates = []
            else:
                # Semantic routing: independent per-unit WQs, each exposing W
                # oldest entries; global priority resolves cross-unit order.
                candidates = []
                for engine in self.ENGINES:
                    queue = [tile for tile in arrived if tile.engine is engine]
                    candidates.extend(queue[: self.window])
                    if len(queue) > self.window:
                        window_stalls += len(queue) - self.window
                candidates.sort(key=lambda tile: (int(tile.priority), tile.sequence, tile.tile_id))

            issued_engines: set[Engine] = set()
            issued_any = False
            for tile in candidates:
                if tile.engine in engine_busy or tile.engine in issued_engines:
                    resource_stalls += 1
                    continue
                if not all(dep in completed for dep in tile.deps):
                    dependency_stalls += 1
                    continue
                if mode is TISAMode.DYNAMIC:
                    older_tiles = [entry[0] for entry in in_flight.values()]
                    if any(semantic_hazards(tile, older) for older in older_tiles):
                        dependency_stalls += 1
                        continue

                issue_time = time + (self.dispatch_latency if mode is TISAMode.DYNAMIC else 0)
                complete_time = issue_time + tile.duration
                in_flight[tile.tile_id] = (tile, issue_time, complete_time)
                issues.append(
                    TISAIssue(
                        tile_id=tile.tile_id,
                        engine=tile.engine,
                        issue=issue_time,
                        complete=complete_time,
                        priority=int(tile.priority),
                        sequence=tile.sequence,
                    )
                )
                issued_engines.add(tile.engine)
                issued_any = True
                if mode is TISAMode.NAIVE:
                    break

            if not in_flight and not issued_any and arrived:
                # An arrived tile with unsatisfied predecessors indicates a
                # malformed sequence or a true deadlock, not normal backpressure.
                if all(any(dep not in completed for dep in tile.deps) for tile in arrived):
                    raise RuntimeError("TISA dependency deadlock")

            time += 1

        cycles = max((issue.complete for issue in issues), default=0)
        utilization = {
            engine.value: (sum(issue.complete - issue.issue for issue in issues if issue.engine is engine) / cycles)
            if cycles
            else 0.0
            for engine in self.ENGINES
        }
        exact_busy = {
            engine.value: sum(issue.complete - issue.issue for issue in issues if issue.engine is engine)
            for engine in self.ENGINES
        }
        return TISAResult(
            mode=mode,
            cycles=cycles,
            issues=tuple(issues),
            utilization=utilization,
            busy_cycles=exact_busy,
            overlap_cycles=overlap_cycles,
            dependency_stalls=dependency_stalls,
            resource_stalls=resource_stalls,
            window_stalls=window_stalls,
            dispatch_latency=self.dispatch_latency if mode is TISAMode.DYNAMIC else 0,
            completed=len(completed),
        )


def make_tile(
    tile_id: str,
    *,
    engine: Engine,
    duration: int,
    sequence: int,
    operands: tuple[MemorySpan, ...] = (),
    deps: tuple[str, ...] = (),
    static_group: int | None = None,
    priority: int = 1,
    program_id: str = "program0",
    call_id: str = "call0",
    flow_id: str = "flow0",
    task_id: str = "task0",
    op_type: str | None = None,
) -> Tile:
    from .model import Priority

    metadata: dict[str, object] = {}
    if static_group is not None:
        metadata["static_group"] = static_group
    return Tile(
        tile_id=tile_id,
        task_id=task_id,
        flow_id=flow_id,
        call_id=call_id,
        program_id=program_id,
        engine=engine,
        duration=duration,
        priority=Priority(priority),
        op_type=op_type or engine.value,
        sequence=sequence,
        operands=operands,
        deps=deps,
        metadata=metadata,
    )

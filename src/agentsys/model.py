from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum, IntEnum
from typing import Iterable


class Priority(IntEnum):
    """Smaller values are more urgent at every layer."""

    REACTIVE = 0
    NORMAL = 1
    PROACTIVE = 2


class FlowKind(str, Enum):
    REACTIVE = "reactive"
    PROACTIVE = "proactive"


class Engine(str, Enum):
    CPU = "cpu"
    IGPU = "igpu"
    NPU = "npu"
    ME = "me"
    VE = "ve"
    DE = "de"
    TOOL = "tool"


class Scope(str, Enum):
    PRIVATE = "private"
    LOCAL = "local"
    SHARED = "shared"
    DDR = "ddr"


class Access(str, Enum):
    READ = "read"
    WRITE = "write"
    READ_WRITE = "read_write"

    @property
    def reads(self) -> bool:
        return self in (Access.READ, Access.READ_WRITE)

    @property
    def writes(self) -> bool:
        return self in (Access.WRITE, Access.READ_WRITE)


@dataclass(frozen=True, slots=True)
class MemorySpan:
    base: int
    size: int
    access: Access
    scope: Scope = Scope.LOCAL
    bank: int = 0

    def __post_init__(self) -> None:
        if self.base < 0:
            raise ValueError("memory base must be non-negative")
        if self.size <= 0:
            raise ValueError("memory size must be positive")
        if self.bank < 0:
            raise ValueError("memory bank must be non-negative")

    @property
    def end(self) -> int:
        return self.base + self.size

    def aliases(self, other: "MemorySpan") -> bool:
        if self.scope != other.scope or self.bank != other.bank:
            return False
        return self.base < other.end and other.base < self.end

    def hazard_with(self, older: "MemorySpan") -> str | None:
        """Return the younger-vs-older dependence kind when ranges alias."""

        if not self.aliases(older):
            return None
        if older.access.writes and self.access.reads:
            return "RAW"
        if older.access.reads and self.access.writes:
            return "WAR"
        if older.access.writes and self.access.writes:
            return "WAW"
        return None


@dataclass(frozen=True, slots=True)
class Tile:
    tile_id: str
    task_id: str
    flow_id: str
    call_id: str
    program_id: str
    engine: Engine
    duration: int
    priority: Priority
    op_type: str
    sequence: int
    operands: tuple[MemorySpan, ...] = ()
    deps: tuple[str, ...] = ()
    preemptible: bool = False
    metadata: dict[str, object] = field(default_factory=dict, compare=False)

    def __post_init__(self) -> None:
        if self.duration <= 0:
            raise ValueError("tile duration must be positive")
        if self.sequence < 0:
            raise ValueError("tile sequence must be non-negative")
        if self.engine not in (Engine.ME, Engine.VE, Engine.DE):
            raise ValueError("TISA tile engine must be ME, VE, or DE")

    def inherit_priority(self, priority: Priority) -> "Tile":
        return replace(self, priority=priority)


@dataclass(frozen=True, slots=True)
class TaskSpec:
    task_id: str
    flow_id: str
    call_id: str
    program_id: str
    priority: Priority
    tiles: tuple[Tile, ...]
    deps: tuple[str, ...] = ()
    prefetchable: bool = True

    def __post_init__(self) -> None:
        if not self.tiles:
            raise ValueError("task must contain at least one tile")
        if any(tile.task_id != self.task_id for tile in self.tiles):
            raise ValueError("all task tiles must carry the task id")
        if any(tile.priority != self.priority for tile in self.tiles):
            raise ValueError("task priority must be inherited by every tile")


@dataclass(frozen=True, slots=True)
class FlowSpec:
    flow_id: str
    call_id: str
    program_id: str
    kind: FlowKind
    priority: Priority
    input_tokens: int
    output_tokens: int
    arrival: float
    tasks: tuple[TaskSpec, ...] = ()

    def __post_init__(self) -> None:
        if self.input_tokens <= 0 or self.output_tokens <= 0:
            raise ValueError("flow token counts must be positive")
        expected = Priority.REACTIVE if self.kind is FlowKind.REACTIVE else Priority.PROACTIVE
        if self.priority != expected:
            raise ValueError("flow kind and priority disagree")
        if any(task.priority != self.priority for task in self.tasks):
            raise ValueError("flow priority must be inherited by every task")


def validate_unique_ids(items: Iterable[object], attr: str) -> None:
    seen: set[object] = set()
    for item in items:
        value = getattr(item, attr)
        if value in seen:
            raise ValueError(f"duplicate {attr}: {value}")
        seen.add(value)


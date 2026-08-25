from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from math import inf
from typing import Iterable


class AgentixPolicy(str, Enum):
    FCFS = "fcfs"
    MLFQ = "mlfq"
    PLAS = "plas"
    ATLAS = "atlas"


@dataclass(frozen=True, slots=True)
class CallSpec:
    call_id: str
    program_id: str
    duration: int
    deps: tuple[str, ...] = ()
    program_arrival: int = 0
    external_delay: int = 0
    thread_id: str = "main"

    def __post_init__(self) -> None:
        if self.duration <= 0:
            raise ValueError("call duration must be positive")
        if self.program_arrival < 0 or self.external_delay < 0:
            raise ValueError("arrival and external delay must be non-negative")


@dataclass(slots=True)
class _CallState:
    spec: CallSpec
    remaining: int
    arrived: bool = False
    ready_time: int | None = None
    ready_order: int = -1
    started: int | None = None
    completed: int | None = None
    attained: int = 0
    queue_level: int = 0
    quantum_left: int = 1
    inherited_service: int = 0
    waiting: int = 0


@dataclass(frozen=True, slots=True)
class CallSlice:
    start: int
    end: int
    lane: int
    call_id: str
    program_id: str
    queue_level: int
    inherited_service: int


@dataclass(frozen=True, slots=True)
class AgentixResult:
    policy: AgentixPolicy
    total_wait: int
    total_call_wait: int
    makespan: int
    program_completion: dict[str, int]
    program_wait: dict[str, int]
    slices: tuple[CallSlice, ...]
    call_completion: dict[str, int]

    def to_dict(self) -> dict[str, object]:
        return {
            "policy": self.policy.value,
            "total_wait": self.total_wait,
            "total_call_wait": self.total_call_wait,
            "makespan": self.makespan,
            "program_completion": self.program_completion,
            "program_wait": self.program_wait,
            "call_completion": self.call_completion,
            "slices": [
                {
                    "start": item.start,
                    "end": item.end,
                    "lane": item.lane,
                    "call_id": item.call_id,
                    "program_id": item.program_id,
                    "queue_level": item.queue_level,
                    "inherited_service": item.inherited_service,
                }
                for item in self.slices
            ],
        }


class AgentixSimulator:
    """Decode-step scheduler implementing the paper's non-clairvoyant priorities.

    Calls become visible only after all dynamic parents complete. FCFS is
    non-preemptive. MLFQ, PLAS, and ATLAS use discrete queues and execute one
    decode step at a time, matching Agentix's scheduling boundary.
    """

    def __init__(
        self,
        *,
        batch_size: int = 2,
        queue_bounds: tuple[int, ...] = (0, 1, 3, 7, 15),
        queue_quanta: tuple[int, ...] = (1, 2, 4, 8, 16),
    ) -> None:
        if batch_size <= 0:
            raise ValueError("batch size must be positive")
        if not queue_bounds or queue_bounds[0] != 0:
            raise ValueError("queue bounds must start at zero")
        if tuple(sorted(queue_bounds)) != queue_bounds:
            raise ValueError("queue bounds must be sorted")
        if len(queue_bounds) != len(queue_quanta):
            raise ValueError("queue bounds and quanta must have equal length")
        self.batch_size = batch_size
        self.queue_bounds = queue_bounds
        self.queue_quanta = queue_quanta

    def _queue_for_service(self, service: int) -> int:
        for index in range(len(self.queue_bounds) - 1, -1, -1):
            if service >= self.queue_bounds[index]:
                return index
        raise AssertionError("unreachable")

    @staticmethod
    def _validate(calls: tuple[CallSpec, ...]) -> None:
        ids = [call.call_id for call in calls]
        if len(ids) != len(set(ids)):
            raise ValueError("call ids must be unique")
        known = set(ids)
        for call in calls:
            missing = set(call.deps) - known
            if missing:
                raise ValueError(f"call {call.call_id} has missing deps: {sorted(missing)}")

        visiting: set[str] = set()
        visited: set[str] = set()
        by_id = {call.call_id: call for call in calls}

        def visit(call_id: str) -> None:
            if call_id in visited:
                return
            if call_id in visiting:
                raise ValueError("call graph contains a cycle")
            visiting.add(call_id)
            for dep in by_id[call_id].deps:
                visit(dep)
            visiting.remove(call_id)
            visited.add(call_id)

        for call_id in ids:
            visit(call_id)

    def run(self, calls: Iterable[CallSpec], policy: AgentixPolicy | str) -> AgentixResult:
        policy = AgentixPolicy(policy)
        specs = tuple(calls)
        self._validate(specs)
        states = {call.call_id: _CallState(call, call.duration) for call in specs}
        program_ids = tuple(dict.fromkeys(call.program_id for call in specs))
        program_service = {program_id: 0 for program_id in program_ids}
        program_wait_acc = {program_id: 0 for program_id in program_ids}
        completed: set[str] = set()
        ready: list[str] = []
        active_fcfs: list[str | None] = [None] * self.batch_size
        ready_counter = 0
        time = min((call.program_arrival for call in specs), default=0)
        slices: list[CallSlice] = []
        max_time = sum(call.duration + call.external_delay for call in specs) + max(
            (call.program_arrival for call in specs), default=0
        ) + 1000

        def deps_complete(state: _CallState) -> bool:
            return all(dep in completed for dep in state.spec.deps)

        def parent_ready_time(state: _CallState) -> int:
            if not state.spec.deps:
                return state.spec.program_arrival
            return max(states[dep].completed or 0 for dep in state.spec.deps) + state.spec.external_delay

        def inherit_service(state: _CallState) -> int:
            if policy is AgentixPolicy.MLFQ or policy is AgentixPolicy.FCFS:
                return 0
            if policy is AgentixPolicy.PLAS:
                return program_service[state.spec.program_id]
            if not state.spec.deps:
                return 0
            return max(
                states[dep].inherited_service + states[dep].spec.duration
                for dep in state.spec.deps
            )

        def enqueue_newly_ready(now: int) -> None:
            nonlocal ready_counter
            for spec in specs:
                state = states[spec.call_id]
                if state.arrived or state.completed is not None or not deps_complete(state):
                    continue
                eligible = parent_ready_time(state)
                if eligible > now:
                    continue
                state.arrived = True
                state.ready_time = eligible
                state.ready_order = ready_counter
                ready_counter += 1
                state.inherited_service = inherit_service(state)
                base = 0 if policy is AgentixPolicy.MLFQ else state.inherited_service
                state.queue_level = self._queue_for_service(base)
                state.quantum_left = self.queue_quanta[state.queue_level]
                ready.append(spec.call_id)

        def preemptive_key(call_id: str) -> tuple[int, int, int, str]:
            state = states[call_id]
            if policy is AgentixPolicy.MLFQ:
                return (state.queue_level, 0, state.ready_order, call_id)
            if policy is AgentixPolicy.PLAS:
                return (
                    state.queue_level,
                    0,
                    state.ready_order,
                    call_id,
                )
            # ATLAS groups equal-priority threads of the same program without
            # hiding the stable arrival order between programs.
            return (
                state.queue_level,
                0,
                state.ready_order,
                call_id,
            )

        enqueue_newly_ready(time)
        while len(completed) < len(specs):
            if time > max_time:
                raise RuntimeError("scheduler made no progress")
            enqueue_newly_ready(time)

            if policy is AgentixPolicy.FCFS:
                for lane, call_id in enumerate(active_fcfs):
                    if call_id is not None and states[call_id].completed is None:
                        continue
                    active_fcfs[lane] = None
                    if ready:
                        next_id = min(ready, key=lambda cid: (states[cid].ready_order, cid))
                        ready.remove(next_id)
                        active_fcfs[lane] = next_id
                selected = [call_id for call_id in active_fcfs if call_id is not None]
            else:
                selected = sorted(ready, key=preemptive_key)[: self.batch_size]

            if not selected:
                future = [
                    parent_ready_time(state)
                    for state in states.values()
                    if not state.arrived and state.completed is None and deps_complete(state)
                ]
                if not future:
                    raise RuntimeError("deadlock: unfinished calls but no future arrival")
                time = max(time + 1, min(future))
                continue

            selected_set = set(selected)
            for call_id in ready:
                if call_id not in selected_set:
                    states[call_id].waiting += 1
                    program_wait_acc[states[call_id].spec.program_id] += 1

            for lane, call_id in enumerate(selected):
                state = states[call_id]
                if state.started is None:
                    state.started = time
                slices.append(
                    CallSlice(
                        start=time,
                        end=time + 1,
                        lane=lane,
                        call_id=call_id,
                        program_id=state.spec.program_id,
                        queue_level=state.queue_level,
                        inherited_service=state.inherited_service,
                    )
                )
                state.remaining -= 1
                state.attained += 1
                state.quantum_left -= 1

            time += 1

            for call_id in selected:
                state = states[call_id]
                if state.remaining == 0:
                    state.completed = time
                    completed.add(call_id)
                    if call_id in ready:
                        ready.remove(call_id)
                    if policy is AgentixPolicy.FCFS:
                        for lane, active_id in enumerate(active_fcfs):
                            if active_id == call_id:
                                active_fcfs[lane] = None
                    path_service = state.inherited_service + state.spec.duration
                    if policy is AgentixPolicy.PLAS:
                        program_service[state.spec.program_id] += state.spec.duration
                    elif policy is AgentixPolicy.ATLAS:
                        program_service[state.spec.program_id] = max(
                            program_service[state.spec.program_id], path_service
                        )
                elif policy is not AgentixPolicy.FCFS and state.quantum_left == 0:
                    state.queue_level = min(state.queue_level + 1, len(self.queue_quanta) - 1)
                    state.quantum_left = self.queue_quanta[state.queue_level]
                    # Demotion removes and appends the call to the next queue
                    # (Algorithm 1, lines 20--23), so its FCFS position changes.
                    state.ready_order = ready_counter
                    ready_counter += 1

            enqueue_newly_ready(time)

        program_completion: dict[str, int] = {}
        program_wait: dict[str, int] = {}
        for program_id in program_ids:
            program_calls = [state for state in states.values() if state.spec.program_id == program_id]
            completion = max(state.completed or 0 for state in program_calls)
            arrival = min(state.spec.program_arrival for state in program_calls)
            # Program wait follows Agentix Fig. 2: JCT minus total model service
            # for single-threaded programs. For DAGs, subtract the critical path.
            longest_path: dict[str, int] = {}
            for state in program_calls:
                longest_path[state.spec.call_id] = state.spec.duration + max(
                    (longest_path[dep] for dep in state.spec.deps), default=0
                )
            service = max(longest_path.values())
            program_completion[program_id] = completion
            program_wait[program_id] = completion - arrival - service

        return AgentixResult(
            policy=policy,
            total_wait=sum(program_wait.values()),
            total_call_wait=sum(state.waiting for state in states.values()),
            makespan=max(program_completion.values(), default=0),
            program_completion=program_completion,
            program_wait=program_wait,
            slices=tuple(slices),
            call_completion={call_id: state.completed or 0 for call_id, state in states.items()},
        )


def agentix_figure2_workload() -> tuple[CallSpec, ...]:
    """Call durations transcribed from Agentix Figure 2(a)."""

    programs = {
        "A": (4, 3, 1, 1),
        "B": (3, 3, 4),
        "C": (1, 2),
        "D": (4,),
    }
    calls: list[CallSpec] = []
    for call_index in range(max(len(items) for items in programs.values())):
        for program_id, durations in programs.items():
            if call_index >= len(durations):
                continue
            sequence = call_index + 1
            call_id = f"{program_id}{sequence}"
            deps = () if sequence == 1 else (f"{program_id}{sequence - 1}",)
            calls.append(CallSpec(call_id, program_id, durations[call_index], deps))
    return tuple(calls)

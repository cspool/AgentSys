from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from enum import Enum
from statistics import mean
from typing import Iterable


class ATXOrganization(str, Enum):
    CORE = "core"
    ICA = "ica"
    L2_OCA = "l2_oca"
    ATX_NO_PREFETCH = "atx_no_prefetch"
    ATX = "atx"


@dataclass(frozen=True, slots=True)
class ATXHardware:
    frequency_ghz: float = 2.5
    atx_queue_entries: int = 16
    stream_units: int = 32
    ldq_entries: int = 128
    common_bus_bytes_per_cycle: int = 128
    scratchpad_buffers: int = 2
    scratchpad_bytes_per_buffer: int = 32 * 1024
    tile_register_bytes: int = 2 * 1024
    core_vector_ops_per_cycle: int = 16
    inspect_records_per_cycle: int = 4
    nca_ops_per_cycle: int = 64
    predictor_tail_cycles: int = 20
    l2_launch_base_cycles: int = 16
    l2_launch_cycles_per_stream: int = 2
    llc_bytes_per_cycle: int = 64
    llc_fixed_cycles: int = 552


@dataclass(frozen=True, slots=True)
class ATXWorkload:
    name: str
    cpu_vector_ops: int
    inspect_records: int
    nca_ops: int
    input_bytes: int
    stream_descriptors: int
    ica_memory_cycles: int
    tasks: int = 64

    def __post_init__(self) -> None:
        for key, value in asdict(self).items():
            if key != "name" and value < 0:
                raise ValueError(f"negative ATX workload field {key}")
        if self.tasks < 3:
            raise ValueError("ATX steady-state simulation requires at least three tasks")


@dataclass(frozen=True, slots=True)
class ATXDurations:
    core: int
    inspect: int
    accelerator: int
    transfer: int
    l2_launch: int
    ica_memory: int
    predicted_tail: int


@dataclass(frozen=True, slots=True)
class UTETransferStats:
    cache_lines: int
    cycles: int
    stream_units_used: int
    ldq_peak_entries: int
    common_bus_bytes: int


@dataclass(frozen=True, slots=True)
class ATXEvent:
    task: int
    kind: str
    resource: str
    start: int
    end: int


@dataclass(frozen=True, slots=True)
class ATXSimulationResult:
    organization: ATXOrganization
    cycles_per_task: float
    first_complete: int
    last_complete: int
    completions: tuple[int, ...]
    events: tuple[ATXEvent, ...]
    resource_busy: dict[str, int]

    def to_dict(self, *, include_events: bool = False) -> dict[str, object]:
        value: dict[str, object] = {
            "organization": self.organization.value,
            "cycles_per_task": self.cycles_per_task,
            "first_complete": self.first_complete,
            "last_complete": self.last_complete,
            "completions": list(self.completions),
            "resource_busy": self.resource_busy,
            "event_count": len(self.events),
        }
        if include_events:
            value["events"] = [asdict(event) for event in self.events]
        return value


KERNEL_WORKLOADS = {
    "spmm": ATXWorkload("spmm", 4480, 400, 3200, 10368, 32, 80),
    "sddmm": ATXWorkload("sddmm", 4320, 400, 3840, 10624, 20, 40),
    "gemm": ATXWorkload("gemm", 4320, 120, 6400, 1024, 8, 0),
}


DECOMPRESSION_WORKLOAD = ATXWorkload(
    "decompression", 6400, 160, 6400, 26624, 33, 40
)


def derive_durations(
    workload: ATXWorkload, hardware: ATXHardware = ATXHardware()
) -> ATXDurations:
    transfer = simulate_ute_transfer(workload, hardware).cycles
    return ATXDurations(
        core=math.ceil(workload.cpu_vector_ops / hardware.core_vector_ops_per_cycle),
        inspect=math.ceil(workload.inspect_records / hardware.inspect_records_per_cycle),
        accelerator=math.ceil(workload.nca_ops / hardware.nca_ops_per_cycle),
        transfer=transfer,
        l2_launch=(
            hardware.l2_launch_base_cycles
            + hardware.l2_launch_cycles_per_stream * workload.stream_descriptors
        ),
        ica_memory=workload.ica_memory_cycles,
        predicted_tail=min(hardware.predictor_tail_cycles, transfer),
    )


def simulate_ute_transfer(
    workload: ATXWorkload, hardware: ATXHardware = ATXHardware()
) -> UTETransferStats:
    """Cycle the UTE Stream Units, LDQ and 128-byte Common Bus.

    Stream Units may generate one cache-line request per cycle. Requests become
    bus-ready after one modeled L2 pipeline cycle; the Common Bus drains one
    ``common_bus_bytes_per_cycle`` beat per cycle. The bus is the expected
    bottleneck for the registered task shapes, but the explicit LDQ occupancy
    makes insufficient Stream Units/LDQ entries observable in design sweeps.
    """

    cache_lines = math.ceil(workload.input_bytes / hardware.common_bus_bytes_per_cycle)
    stream_units = max(1, min(workload.stream_descriptors, hardware.stream_units))
    remaining = cache_lines
    inflight: list[int] = []
    ready_lines = 0
    retired = 0
    cycle = 0
    ldq_peak = 0
    while retired < cache_lines:
        newly_ready = sum(completion <= cycle for completion in inflight)
        if newly_ready:
            ready_lines += newly_ready
            inflight = [completion for completion in inflight if completion > cycle]
        slots = hardware.ldq_entries - len(inflight) - ready_lines
        issued = min(stream_units, remaining, max(0, slots))
        inflight.extend([cycle + 1] * issued)
        remaining -= issued
        ldq_peak = max(ldq_peak, len(inflight) + ready_lines)
        if ready_lines:
            ready_lines -= 1
            retired += 1
        cycle += 1
    return UTETransferStats(
        cache_lines=cache_lines,
        cycles=cycle,
        stream_units_used=stream_units,
        ldq_peak_entries=ldq_peak,
        common_bus_bytes=cache_lines * hardware.common_bus_bytes_per_cycle,
    )


class _Timeline:
    def __init__(self) -> None:
        self.available: dict[str, int] = {}
        self.events: list[ATXEvent] = []

    def schedule(self, task: int, kind: str, resource: str, ready: int, duration: int) -> int:
        start = max(ready, self.available.get(resource, 0))
        end = start + duration
        self.available[resource] = end
        self.events.append(ATXEvent(task, kind, resource, start, end))
        return end


def _steady_interval(completions: Iterable[int]) -> float:
    values = tuple(completions)
    if len(values) < 2:
        raise ValueError("at least two completions are required")
    return mean(right - left for left, right in zip(values, values[1:]))


def simulate_workload(
    workload: ATXWorkload,
    organization: ATXOrganization | str,
    *,
    hardware: ATXHardware = ATXHardware(),
) -> ATXSimulationResult:
    organization = ATXOrganization(organization)
    durations = derive_durations(workload, hardware)
    timeline = _Timeline()
    completions: list[int] = []
    previous_complete = 0
    buffer_available = [0 for _ in range(hardware.scratchpad_buffers)]

    for task in range(workload.tasks):
        queue_ready = (
            completions[task - hardware.atx_queue_entries]
            if task >= hardware.atx_queue_entries
            else 0
        )
        if organization is ATXOrganization.CORE:
            complete = timeline.schedule(
                task, "cpu_kernel", "core", previous_complete, durations.core
            )
            previous_complete = complete
        elif organization is ATXOrganization.ICA:
            inspected = timeline.schedule(
                task, "cpu_inspection", "core", previous_complete, durations.inspect
            )
            supplied = timeline.schedule(
                task, "core_memory_supply", "core_memory", inspected, durations.ica_memory
            )
            complete = timeline.schedule(
                task, "ica_compute", "accelerator", supplied, durations.accelerator
            )
            previous_complete = complete
        elif organization is ATXOrganization.L2_OCA:
            launched = timeline.schedule(
                task, "rob_head_launch", "core", previous_complete, durations.l2_launch
            )
            transferred = timeline.schedule(
                task, "l2_transfer", "ute", launched, durations.transfer
            )
            complete = timeline.schedule(
                task, "oca_compute", "accelerator", transferred, durations.accelerator
            )
            previous_complete = complete
        elif organization is ATXOrganization.ATX_NO_PREFETCH:
            inspected = timeline.schedule(
                task, "runtime_inspection", "core", queue_ready, durations.inspect
            )
            nca_path = timeline.schedule(
                task,
                "demand_transfer_and_compute",
                "single_buffer_nca_path",
                queue_ready,
                durations.transfer + durations.accelerator,
            )
            complete = max(inspected, nca_path)
            timeline.events.append(ATXEvent(task, "prf_writeback", "atx_port", complete, complete))
        else:
            inspected = timeline.schedule(
                task, "runtime_inspection", "core", queue_ready, durations.inspect
            )
            buffer = task % hardware.scratchpad_buffers
            prefetched = timeline.schedule(
                task,
                "predicted_task_tail",
                "ute",
                max(queue_ready, buffer_available[buffer]),
                durations.predicted_tail,
            )
            ready = max(inspected, prefetched)
            complete = timeline.schedule(
                task, "nca_compute", "accelerator", ready, durations.accelerator
            )
            buffer_available[buffer] = complete
            timeline.events.append(ATXEvent(task, "prf_writeback", "atx_port", complete, complete))
        completions.append(complete)

    resource_busy: dict[str, int] = {}
    for event in timeline.events:
        resource_busy[event.resource] = resource_busy.get(event.resource, 0) + event.end - event.start
    return ATXSimulationResult(
        organization=organization,
        cycles_per_task=_steady_interval(completions),
        first_complete=completions[0],
        last_complete=completions[-1],
        completions=tuple(completions),
        events=tuple(timeline.events),
        resource_busy=resource_busy,
    )


def simulate_all_organizations(
    workload: ATXWorkload, *, hardware: ATXHardware = ATXHardware()
) -> dict[str, ATXSimulationResult]:
    return {
        organization.value: simulate_workload(workload, organization, hardware=hardware)
        for organization in ATXOrganization
    }


def simulate_task_size(
    task_kib: float,
    organization: str,
    *,
    hardware: ATXHardware = ATXHardware(),
) -> float:
    if task_kib <= 0:
        raise ValueError("task size must be positive")
    byte_count = math.ceil(task_kib * 1024)
    if organization == "atx":
        return 8 + math.ceil(byte_count / hardware.common_bus_bytes_per_cycle)
    if organization == "llc":
        return hardware.llc_fixed_cycles + math.ceil(byte_count / hardware.llc_bytes_per_cycle)
    raise ValueError(f"unknown task-size organization: {organization}")

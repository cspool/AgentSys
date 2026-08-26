from agentsys.atx_simulator import (
    ATXHardware,
    ATXOrganization,
    KERNEL_WORKLOADS,
    derive_durations,
    simulate_all_organizations,
)


def test_atx_hardware_matches_paper_ute_shape() -> None:
    hardware = ATXHardware()
    assert (hardware.atx_queue_entries, hardware.stream_units, hardware.ldq_entries) == (
        16,
        32,
        128,
    )
    assert hardware.common_bus_bytes_per_cycle == 128
    assert hardware.scratchpad_buffers == 2
    assert hardware.scratchpad_bytes_per_buffer == 32 * 1024


def test_atx_events_conserve_tasks_and_expose_prefetch_overlap() -> None:
    workload = KERNEL_WORKLOADS["spmm"]
    durations = derive_durations(workload)
    results = simulate_all_organizations(workload)
    assert all(len(result.completions) == workload.tasks for result in results.values())
    assert results[ATXOrganization.ATX.value].cycles_per_task == max(
        durations.inspect, durations.accelerator, durations.predicted_tail
    )
    assert results[ATXOrganization.ATX.value].cycles_per_task < results[
        ATXOrganization.ATX_NO_PREFETCH.value
    ].cycles_per_task

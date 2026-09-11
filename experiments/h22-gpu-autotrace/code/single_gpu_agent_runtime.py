#!/usr/bin/env python3
"""Execute an AgentSys hybrid plan on one GPU, with warmup and measured phases.

This is the w01 collector for the h22 AutoTrace-style lineage. It imports the
certified operator adapters from ``agentsys.hybrid_runtime`` read-only; nothing
under ``src/agentsys/`` is modified, so the run_052 source closure stays exact.

The shipped ``run_hybrid_native`` entry point requires exactly two visible GPUs
and spawns one rank per GPU. This lineage is single-GPU by protocol, so the plan
is rewritten onto one device and executed in-process, with the DAG replayed for
``--warmup-iters`` discarded iterations followed by ``--measured-iters``
measured ones. Each iteration is wrapped in an NVTX range naming its phase, so
the trace can be split into warmup and measured windows downstream.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import socket
import sys
import time
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from agentsys.hybrid_runtime import (  # noqa: E402
    _cpu_matrix_event,
    _cpus,
    _execute_llm,
    _nvml_sample,
    _sha256,
)

PHASE_RANGE = "agentsys.autotrace::phase={phase}::iter={iteration}"


def _rewrite_plan_single_gpu(
    plan: dict[str, Any], *, device: int, numa_node: int
) -> dict[str, Any]:
    """Place every call of a dual-rank plan on one device as rank 0.

    Only the placement fields change. Call order, wave structure, operator
    lists, matrix sizes and dtypes are left exactly as the certified compiler
    emitted them, so the executed operator sequence is the plan's own.
    """
    for call in plan["calls"]:
        call["native"]["rank"] = 0
        call["native"]["device"] = device
        call["native"]["numa_node"] = numa_node
    return plan


def _run_dag(
    plan: dict[str, Any],
    adapter: dict[str, Any],
    *,
    phase: str,
    iteration: int,
    collect: bool,
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    import torch

    events: list[dict[str, Any]] = []
    checksums: dict[str, float] = {}
    max_wave = max(call["wave"] for call in plan["calls"])
    torch.cuda.nvtx.range_push(
        PHASE_RANGE.format(phase=phase, iteration=iteration)
    )
    try:
        for wave in range(max_wave + 1):
            for call in sorted(
                (item for item in plan["calls"] if item["wave"] == wave),
                key=lambda item: item["index"],
            ):
                if call["kind"] == "llm":
                    call_events, checksum = _execute_llm(call, 0, adapter)
                    if collect:
                        events.extend(call_events)
                else:
                    event, checksum = _cpu_matrix_event(
                        call,
                        0,
                        int(adapter["cpu_matrix_size"]),
                        event_name="agent_tool_execute",
                    )
                    if collect:
                        events.append(event)
                checksums[call["call_id"]] = checksum
        torch.cuda.synchronize()
    finally:
        torch.cuda.nvtx.range_pop()
    if collect:
        for event in events:
            event["phase"] = phase
            event["iteration"] = iteration
    return events, checksums


def run(
    *,
    plan_path: Path,
    output_dir: Path,
    device: int,
    numa_node: int,
    cpu_affinity: str,
    warmup_iters: int,
    measured_iters: int,
) -> dict[str, Any]:
    import pynvml
    import torch

    plan_path = plan_path.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    plan_sha = _sha256(plan_path)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    adapter = plan["configuration"]["adapter"]
    plan = _rewrite_plan_single_gpu(plan, device=device, numa_node=numa_node)

    affinity = _cpus(cpu_affinity)
    os.sched_setaffinity(0, affinity)
    torch.set_num_threads(int(adapter["cpu_threads_per_rank"]))
    torch.set_num_interop_threads(1)
    torch.cuda.set_device(device)

    pynvml.nvmlInit()
    nvml_before = _nvml_sample(device)
    properties = torch.cuda.get_device_properties(device)

    started_ns = time.monotonic_ns()
    warmup_checksums: dict[str, float] = {}
    for iteration in range(warmup_iters):
        _, warmup_checksums = _run_dag(
            plan, adapter, phase="warmup", iteration=iteration, collect=False
        )
    warmup_done_ns = time.monotonic_ns()

    events: list[dict[str, Any]] = []
    measured_checksums: list[dict[str, float]] = []
    for iteration in range(measured_iters):
        iteration_events, checksums = _run_dag(
            plan, adapter, phase="measured", iteration=iteration, collect=True
        )
        events.extend(iteration_events)
        measured_checksums.append(checksums)
    finished_ns = time.monotonic_ns()

    nvml_after = _nvml_sample(device)
    pynvml.nvmlShutdown()

    # Determinism check: the adapter is seeded per call, so every replay of the
    # DAG must reproduce the same checksums. A mismatch invalidates the
    # denominator, because the iterations would not be the same computation.
    reference = measured_checksums[0] if measured_checksums else {}
    deterministic = all(item == reference for item in measured_checksums) and (
        not warmup_checksums or warmup_checksums == reference
    )

    events.sort(key=lambda event: (int(event["start_ns"]), str(event["event"])))
    trace_path = output_dir / "native-trace.jsonl"
    with trace_path.open("w", encoding="utf-8") as handle:
        for sequence, event in enumerate(events):
            event["sequence"] = sequence
            event["workload"] = plan["workload"]["name"]
            event["workload_sha256"] = plan["workload"]["sha256"]
            handle.write(json.dumps(event, sort_keys=True) + "\n")

    operator_events = [event for event in events if event["event"] == "mir_operator"]
    expected_operators = (
        int(plan["summary"]["mir_operators"]) * measured_iters
    )
    metadata = {
        "schema_version": 1,
        "lineage": "h22-gpu-autotrace",
        "goal": "G01",
        "plan_path": str(plan_path),
        "plan_sha256": plan_sha,
        "workload": plan["workload"]["name"],
        "workload_sha256": plan["workload"]["sha256"],
        "single_gpu": {
            "device": device,
            "name": properties.name,
            "uuid": nvml_before["uuid"],
            "pci_bus_id": nvml_before["pci_bus_id"],
            "numa_node": numa_node,
            "configured_affinity": sorted(affinity),
            "observed_affinity": sorted(os.sched_getaffinity(0)),
        },
        "iterations": {
            "warmup": warmup_iters,
            "measured": measured_iters,
        },
        "adapter": adapter,
        "planned": {
            "calls": int(plan["summary"]["calls"]),
            "llm_calls": int(plan["summary"]["llm_calls"]),
            "tool_calls": int(plan["summary"]["tool_calls"]),
            "mir_operators": int(plan["summary"]["mir_operators"]),
            "waves": int(plan["summary"]["waves"]),
        },
        "observed": {
            "operator_events": len(operator_events),
            "expected_operator_events": expected_operators,
            "total_events": len(events),
        },
        "timing_ns": {
            "started": started_ns,
            "warmup_done": warmup_done_ns,
            "finished": finished_ns,
            "warmup_wall_ms": (warmup_done_ns - started_ns) / 1e6,
            "measured_wall_ms": (finished_ns - warmup_done_ns) / 1e6,
        },
        "determinism": {
            "checksums_match": deterministic,
            "reference_checksums": reference,
        },
        "environment": {
            "host": socket.gethostname(),
            "python": platform.python_version(),
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "driver_sm_clock_mhz": nvml_before["sm_clock_mhz"],
            "nvml_before": nvml_before,
            "nvml_after": nvml_after,
        },
        "pass": (
            deterministic
            and len(operator_events) == expected_operators
            and measured_iters > 0
        ),
    }
    metadata_path = output_dir / "run_metadata.json"
    metadata_path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return metadata


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Execute an AgentSys hybrid plan on a single GPU"
    )
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--device", type=int, default=1)
    parser.add_argument("--numa-node", type=int, default=1)
    parser.add_argument("--cpu-affinity", default="16-31,48-63")
    parser.add_argument("--warmup-iters", type=int, default=3)
    parser.add_argument("--measured-iters", type=int, default=10)
    args = parser.parse_args(argv)

    metadata = run(
        plan_path=args.plan,
        output_dir=args.output_dir,
        device=args.device,
        numa_node=args.numa_node,
        cpu_affinity=args.cpu_affinity,
        warmup_iters=args.warmup_iters,
        measured_iters=args.measured_iters,
    )
    print(json.dumps(metadata["observed"], indent=2, sort_keys=True))
    print(json.dumps(metadata["timing_ns"], indent=2, sort_keys=True))
    print(args.output_dir / "run_metadata.json")
    return 0 if metadata["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

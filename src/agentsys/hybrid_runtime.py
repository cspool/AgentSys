from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import socket
import time
from pathlib import Path
from typing import Any, Callable

from .gpu_runtime import _cpus, _nvml_sample
from .workload import PROJECT_ROOT


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handle:
        handle.bind(("127.0.0.1", 0))
        return int(handle.getsockname()[1])


def _seed(call_id: str, rank: int) -> int:
    digest = hashlib.sha256(f"{call_id}:{rank}:run040".encode()).digest()
    return int.from_bytes(digest[:4], "little")


def _cuda_measure(operation: Callable[[], Any]) -> tuple[Any, float, int, int]:
    import torch

    start_host = time.monotonic_ns()
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    start.record()
    value = operation()
    end.record()
    end.synchronize()
    end_host = time.monotonic_ns()
    return value, float(start.elapsed_time(end)), start_host, end_host


def _base_event(call: dict[str, Any], rank: int) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "rank": rank,
        "call_id": call["call_id"],
        "call_index": call["index"],
        "program_id": call["program_id"],
        "priority": call["priority"],
        "wave": call["wave"],
    }


def _cpu_matrix_event(
    call: dict[str, Any],
    rank: int,
    size: int,
    *,
    event_name: str,
) -> tuple[dict[str, Any], float]:
    import torch

    generator = torch.Generator(device="cpu")
    generator.manual_seed(_seed(call["call_id"], rank))
    left = torch.randn((size, size), generator=generator, dtype=torch.float32)
    right = torch.randn((size, size), generator=generator, dtype=torch.float32)
    started = time.monotonic_ns()
    output = left @ right
    finished = time.monotonic_ns()
    checksum = float(output[:8, :8].sum())
    event = {
        **_base_event(call, rank),
        "layer": "cpu",
        "event": event_name,
        "resource": f"cpu_numa{call['native']['numa_node']}",
        "clock_domain": "host_monotonic_ns",
        "start_ns": started,
        "end_ns": finished,
        "duration_ms": (finished - started) / 1e6,
        "matrix_size": size,
        "checksum": checksum,
    }
    return event, checksum


def _execute_llm(
    call: dict[str, Any],
    rank: int,
    adapter: dict[str, Any],
) -> tuple[list[dict[str, Any]], float]:
    import torch

    device_index = int(call["native"]["device"])
    device = torch.device("cuda", device_index)
    dtype_name = str(call["native"]["dtype"])
    if dtype_name == "float16":
        dtype = torch.float16
    elif dtype_name == "bfloat16":
        dtype = torch.bfloat16
    else:
        raise ValueError(f"unsupported MIR CUDA adapter dtype: {dtype_name}")
    matrix_size = int(call["native"]["matrix_size"])
    events: list[dict[str, Any]] = []
    started = time.monotonic_ns()
    events.append(
        {
            **_base_event(call, rank),
            "layer": "mllm",
            "event": "mir_adapter_start",
            "resource": f"gpu{device_index}",
            "clock_domain": "host_monotonic_ns",
            "start_ns": started,
            "end_ns": started,
            "model": call["model"],
            "adapter": call["native"]["adapter"],
        }
    )
    cpu_event, _ = _cpu_matrix_event(
        call,
        rank,
        int(adapter["cpu_matrix_size"]),
        event_name="mllm_token_preprocess",
    )
    events.append(cpu_event)

    generator = torch.Generator(device="cpu")
    generator.manual_seed(_seed(call["call_id"], rank))
    host_input = torch.empty(
        (matrix_size, matrix_size), dtype=dtype, pin_memory=True
    )
    host_input.uniform_(-0.25, 0.25, generator=generator)
    state = torch.empty((matrix_size, matrix_size), dtype=dtype, device=device)
    _, duration_ms, start_ns, end_ns = _cuda_measure(
        lambda: state.copy_(host_input, non_blocking=True)
    )
    events.append(
        {
            **_base_event(call, rank),
            "layer": "cuda",
            "event": "h2d",
            "resource": f"gpu{device_index}",
            "clock_domain": "host_monotonic_ns",
            "start_ns": start_ns,
            "end_ns": end_ns,
            "cuda_ms": duration_ms,
            "bytes": host_input.numel() * host_input.element_size(),
        }
    )
    torch.cuda.manual_seed(_seed(call["call_id"], rank) + 17)
    weight = torch.randn(
        (matrix_size, matrix_size), device=device, dtype=dtype
    ) / math.sqrt(matrix_size)

    for operator in call["mir_operators"]:
        op_type = operator["op_type"]

        def operation() -> Any:
            nonlocal state
            if op_type == "RMSNormOp":
                state = torch.nn.functional.rms_norm(
                    state, (matrix_size,), eps=1e-5
                )
            elif op_type == "AddOp":
                state = state + 0.0009765625
            elif op_type == "LinearOp":
                state = torch.mm(state, weight)
            elif op_type == "ViewOp":
                state = state.reshape(matrix_size, matrix_size)
            elif op_type == "TransposeOp":
                state = state.transpose(0, 1).contiguous()
            else:
                raise ValueError(f"unsupported MIR CUDA adapter op: {op_type}")
            return state

        range_name = (
            f"agentsys.mllm::{call['call_id']}::{operator['index']}::{op_type}"
        )
        iterations = int(adapter["operator_iterations"])

        def measured_operation() -> Any:
            value: Any = None
            for _ in range(iterations):
                value = operation()
            return value

        torch.cuda.nvtx.range_push(range_name)
        try:
            _, duration_ms, start_ns, end_ns = _cuda_measure(measured_operation)
        finally:
            torch.cuda.nvtx.range_pop()
        events.append(
            {
                **_base_event(call, rank),
                "layer": "gpu",
                "event": "mir_operator",
                "resource": f"gpu{device_index}",
                "clock_domain": "host_monotonic_ns",
                "start_ns": start_ns,
                "end_ns": end_ns,
                "cuda_ms": duration_ms,
                "source_index": operator["index"],
                "op_type": op_type,
                "engine": operator["engine"],
                "matrix_size": matrix_size,
                "dtype": dtype_name,
                "iterations": iterations,
                "adapter": "agentsys_mir_cuda_operator_adapter",
            }
        )

    host_output = torch.empty_like(host_input, pin_memory=True)
    _, duration_ms, start_ns, end_ns = _cuda_measure(
        lambda: host_output.copy_(state, non_blocking=True)
    )
    checksum = float(host_output[:8, :8].float().sum())
    events.append(
        {
            **_base_event(call, rank),
            "layer": "cuda",
            "event": "d2h",
            "resource": f"gpu{device_index}",
            "clock_domain": "host_monotonic_ns",
            "start_ns": start_ns,
            "end_ns": end_ns,
            "cuda_ms": duration_ms,
            "bytes": host_output.numel() * host_output.element_size(),
            "checksum": checksum,
        }
    )
    finished = time.monotonic_ns()
    events.append(
        {
            **_base_event(call, rank),
            "layer": "mllm",
            "event": "mir_adapter_complete",
            "resource": f"gpu{device_index}",
            "clock_domain": "host_monotonic_ns",
            "start_ns": finished,
            "end_ns": finished,
            "checksum": checksum,
        }
    )
    return events, checksum


def _worker(
    rank: int,
    world_size: int,
    init_method: str,
    plan_path_text: str,
    gpu_config_path_text: str,
    output_dir_text: str,
) -> None:
    import pynvml
    import torch
    import torch.distributed as dist

    plan = json.loads(Path(plan_path_text).read_text(encoding="utf-8"))
    gpu_config = json.loads(Path(gpu_config_path_text).read_text(encoding="utf-8"))
    output_dir = Path(output_dir_text)
    gpu = gpu_config["gpus"][rank]
    adapter = plan["configuration"]["adapter"]
    affinity = _cpus(gpu["cpu_affinity"])
    os.sched_setaffinity(0, affinity)
    observed_affinity = sorted(os.sched_getaffinity(0))
    torch.set_num_threads(int(adapter["cpu_threads_per_rank"]))
    torch.set_num_interop_threads(1)
    device_index = int(gpu["device"])
    torch.cuda.set_device(device_index)
    device = torch.device("cuda", device_index)
    os.environ.setdefault("NCCL_DEBUG", "INFO")
    os.environ["NCCL_DEBUG_FILE"] = str(output_dir / f"rank{rank}-nccl.log")
    os.environ.setdefault("TORCH_NCCL_ASYNC_ERROR_HANDLING", "1")
    dist.init_process_group(
        backend=gpu_config["backend"],
        init_method=init_method,
        rank=rank,
        world_size=world_size,
        device_id=device,
    )
    pynvml.nvmlInit()
    nvml_before = _nvml_sample(device_index)
    p2p = {
        str(peer): bool(torch.cuda.can_device_access_peer(device_index, peer))
        for peer in range(world_size)
        if peer != device_index
    }
    events: list[dict[str, Any]] = []
    checksums: dict[str, float] = {}
    calls = [
        call for call in plan["calls"] if int(call["native"]["rank"]) == rank
    ]
    max_wave = max(call["wave"] for call in plan["calls"])
    for wave in range(max_wave + 1):
        dist.barrier()
        for call in sorted(
            (item for item in calls if item["wave"] == wave),
            key=lambda item: item["index"],
        ):
            if call["kind"] == "llm":
                call_events, checksum = _execute_llm(call, rank, adapter)
                events.extend(call_events)
            else:
                event, checksum = _cpu_matrix_event(
                    call,
                    rank,
                    int(adapter["cpu_matrix_size"]),
                    event_name="agent_tool_execute",
                )
                events.append(event)
            checksums[call["call_id"]] = checksum
        dist.barrier()

    local_counts = torch.tensor(
        [
            sum(call["kind"] == "llm" for call in calls),
            sum(call["kind"] == "tool" for call in calls),
            sum(len(call["mir_operators"]) for call in calls),
        ],
        dtype=torch.int64,
        device=device,
    )
    start_ns = time.monotonic_ns()
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    start.record()
    dist.all_reduce(local_counts)
    end.record()
    end.synchronize()
    end_ns = time.monotonic_ns()
    observed_collective = [int(value) for value in local_counts.cpu().tolist()]
    expected_collective = [
        int(plan["summary"]["llm_calls"]),
        int(plan["summary"]["tool_calls"]),
        int(plan["summary"]["mir_operators"]),
    ]
    events.append(
        {
            "schema_version": 1,
            "rank": rank,
            "call_id": None,
            "call_index": None,
            "program_id": None,
            "priority": None,
            "wave": max_wave + 1,
            "layer": "nccl",
            "event": "all_reduce_counts",
            "resource": "nccl",
            "clock_domain": "host_monotonic_ns",
            "start_ns": start_ns,
            "end_ns": end_ns,
            "cuda_ms": float(start.elapsed_time(end)),
            "observed": observed_collective,
            "expected": expected_collective,
            "correct": observed_collective == expected_collective,
        }
    )
    nvml_after = _nvml_sample(device_index)
    pynvml.nvmlShutdown()
    dist.barrier()
    dist.destroy_process_group()
    properties = torch.cuda.get_device_properties(device_index)
    result = {
        "rank": rank,
        "device": device_index,
        "device_name": properties.name,
        "device_uuid": nvml_before["uuid"],
        "numa_node": int(gpu["numa_node"]),
        "configured_affinity": sorted(affinity),
        "observed_affinity": observed_affinity,
        "torch_cpu_threads": torch.get_num_threads(),
        "p2p": p2p,
        "nvml_before": nvml_before,
        "nvml_after": nvml_after,
        "calls": [call["call_id"] for call in calls],
        "checksums": checksums,
        "collective": {
            "observed": observed_collective,
            "expected": expected_collective,
            "correct": observed_collective == expected_collective,
        },
        "events": events,
    }
    (output_dir / f"rank{rank}.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def run_hybrid_native(
    *,
    plan_path: Path,
    output_dir: Path,
    gpu_config_path: Path | None = None,
) -> dict[str, Any]:
    import pynvml
    import torch
    import torch.multiprocessing as mp

    plan_path = plan_path.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    gpu_config_path = (
        gpu_config_path
        or Path(plan["configuration"]["gpu_runtime_path"])
    ).resolve()
    gpu_config = json.loads(gpu_config_path.read_text(encoding="utf-8"))
    world_size = len(gpu_config["gpus"])
    if world_size != 2 or torch.cuda.device_count() != 2:
        raise RuntimeError("hybrid native runtime requires exactly two visible GPUs")
    pynvml.nvmlInit()
    discovery = [_nvml_sample(index) for index in range(world_size)]
    pynvml.nvmlShutdown()
    started_ns = time.monotonic_ns()
    mp.spawn(
        _worker,
        args=(
            world_size,
            f"tcp://127.0.0.1:{_free_port()}",
            str(plan_path),
            str(gpu_config_path),
            str(output_dir),
        ),
        nprocs=world_size,
        join=True,
    )
    finished_ns = time.monotonic_ns()
    ranks = [
        json.loads((output_dir / f"rank{rank}.json").read_text(encoding="utf-8"))
        for rank in range(world_size)
    ]
    events = [event for item in ranks for event in item["events"]]
    events.sort(
        key=lambda event: (
            int(event["start_ns"]),
            int(event["rank"]),
            str(event["event"]),
        )
    )
    trace_path = output_dir / "native-trace.jsonl"
    with trace_path.open("w", encoding="utf-8") as handle:
        for sequence, event in enumerate(events):
            event["sequence"] = sequence
            event["workload"] = plan["workload"]["name"]
            event["workload_sha256"] = plan["workload"]["sha256"]
            handle.write(json.dumps(event, sort_keys=True) + "\n")

    completion_events = [
        event
        for event in events
        if event["event"] in {"mir_adapter_complete", "agent_tool_execute"}
    ]
    op_events = [event for event in events if event["event"] == "mir_operator"]
    call_windows: dict[str, tuple[int, int]] = {}
    for event in events:
        if event["call_id"] is None:
            continue
        old = call_windows.get(event["call_id"])
        start = int(event["start_ns"])
        end = int(event["end_ns"])
        call_windows[event["call_id"]] = (
            min(start, old[0]) if old else start,
            max(end, old[1]) if old else end,
        )
    planned_calls = {call["call_id"]: call for call in plan["calls"]}
    engine_gate = True
    for call in plan["calls"]:
        if call["kind"] != "llm":
            continue
        observed = {
            engine: sum(
                event["call_id"] == call["call_id"] and event["engine"] == engine
                for event in op_events
            )
            for engine in ("me", "ve", "de")
        }
        engine_gate = engine_gate and observed == {"me": 3, "ve": 3, "de": 2}
    dag_gate = all(
        call_windows[dependency][1] <= call_windows[call["call_id"]][0]
        for call in plan["calls"]
        for dependency in call["deps"]
    )
    observed_call_ids = [event["call_id"] for event in completion_events]
    gates = {
        "two_distinct_local_gpus": len({item["uuid"] for item in discovery}) == 2
        and all(item["name"] == "NVIDIA GeForce RTX 4090" for item in discovery),
        "numa_affinity_exact": all(
            rank["configured_affinity"] == rank["observed_affinity"] for rank in ranks
        )
        and {rank["numa_node"] for rank in ranks} == {0, 1}
        and all(
            rank["torch_cpu_threads"]
            == int(plan["configuration"]["adapter"]["cpu_threads_per_rank"])
            for rank in ranks
        ),
        "planned_gpu_placement": all(
            planned_calls[call_id]["native"]["rank"] == rank["rank"]
            for rank in ranks
            for call_id in rank["calls"]
        ),
        "all_calls_exactly_once": len(observed_call_ids) == len(set(observed_call_ids))
        == plan["summary"]["calls"]
        and set(observed_call_ids) == set(planned_calls),
        "dag_runtime_order": dag_gate,
        "mir_operator_identity": len(op_events) == plan["summary"]["mir_operators"]
        and all(
            any(
                operator["index"] == event["source_index"]
                and operator["op_type"] == event["op_type"]
                and operator["engine"] == event["engine"]
                for operator in planned_calls[event["call_id"]]["mir_operators"]
            )
            for event in op_events
        ),
        "per_call_engine_shape": engine_gate,
        "transfer_and_cpu_events": sum(event["event"] == "h2d" for event in events)
        == sum(event["event"] == "d2h" for event in events)
        == plan["summary"]["llm_calls"]
        and sum(
            event["event"] in {"mllm_token_preprocess", "agent_tool_execute"}
            for event in events
        )
        == plan["summary"]["calls"],
        "nccl_collective_correct": all(rank["collective"]["correct"] for rank in ranks),
        "finite_checksums": all(
            math.isfinite(checksum)
            for rank in ranks
            for checksum in rank["checksums"].values()
        ),
        "active_gpu_ranks_match_plan": {
            rank["rank"]
            for rank in ranks
            if any(planned_calls[call]["kind"] == "llm" for call in rank["calls"])
        }
        == {
            call["native"]["rank"]
            for call in plan["calls"]
            if call["kind"] == "llm"
        },
        "p2p_queried": all(len(rank["p2p"]) == 1 for rank in ranks),
        "adapter_boundary": "AgentSys MIR-to-CUDA adapter" in plan["evidence_boundary"]
        and plan["lineage"]["mllm_cuda_audit"]["summary"]["pass"],
    }
    result = {
        "schema_version": 1,
        "run_id": plan["run_id"],
        "classification": "real_workload_aware_dual_gpu_dual_numa_execution",
        "evidence_boundary": plan["evidence_boundary"],
        "plan": {"path": str(plan_path), "sha256": _sha256(plan_path)},
        "gpu_configuration": {
            "path": str(gpu_config_path),
            "sha256": _sha256(gpu_config_path),
        },
        "discovery": discovery,
        "ranks": ranks,
        "trace": {"path": str(trace_path), "sha256": _sha256(trace_path), "events": len(events)},
        "wall_time_s": (finished_ns - started_ns) / 1e9,
        "gates": gates,
        "summary": {
            "calls": plan["summary"]["calls"],
            "llm_calls": plan["summary"]["llm_calls"],
            "tool_calls": plan["summary"]["tool_calls"],
            "mir_operators": len(op_events),
            "events": len(events),
            "gpus": 2,
            "numa_nodes": 2,
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }
    output = output_dir / "native-runtime.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["output"] = str(output)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Execute a hybrid Agent plan on two GPUs/NUMA nodes")
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--gpu-config", type=Path)
    args = parser.parse_args(argv)
    result = run_hybrid_native(
        plan_path=args.plan,
        output_dir=args.output_dir,
        gpu_config_path=args.gpu_config,
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

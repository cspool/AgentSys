from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import subprocess
import time
from pathlib import Path
from statistics import mean
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config/local-dual-gpu.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _cpus(value: str) -> set[int]:
    result: set[int] = set()
    for part in value.split(","):
        if "-" in part:
            low, high = (int(item) for item in part.split("-", 1))
            result.update(range(low, high + 1))
        else:
            result.add(int(part))
    return result


def _nvml_sample(index: int) -> dict[str, Any]:
    import pynvml

    handle = pynvml.nvmlDeviceGetHandleByIndex(index)
    pci = pynvml.nvmlDeviceGetPciInfo(handle)
    memory = pynvml.nvmlDeviceGetMemoryInfo(handle)
    utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
    bus_id = pci.busId.decode() if isinstance(pci.busId, bytes) else str(pci.busId)
    uuid = pynvml.nvmlDeviceGetUUID(handle)
    if isinstance(uuid, bytes):
        uuid = uuid.decode()
    return {
        "index": index,
        "name": pynvml.nvmlDeviceGetName(handle),
        "uuid": uuid,
        "pci_bus_id": bus_id,
        "memory_total": memory.total,
        "memory_used": memory.used,
        "gpu_utilization_percent": utilization.gpu,
        "memory_utilization_percent": utilization.memory,
        "temperature_c": pynvml.nvmlDeviceGetTemperature(
            handle, pynvml.NVML_TEMPERATURE_GPU
        ),
        "power_w": pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0,
        "sm_clock_mhz": pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_SM),
        "memory_clock_mhz": pynvml.nvmlDeviceGetClockInfo(
            handle, pynvml.NVML_CLOCK_MEM
        ),
    }


def _measure_cuda(operation, *, iterations: int) -> tuple[list[float], int, int]:
    import torch

    durations: list[float] = []
    wall_start = time.time_ns()
    for _ in range(iterations):
        start = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)
        start.record()
        operation()
        end.record()
        end.synchronize()
        durations.append(float(start.elapsed_time(end)))
    wall_end = time.time_ns()
    return durations, wall_start, wall_end


def _worker(
    rank: int,
    world_size: int,
    init_method: str,
    config: dict[str, Any],
    output_dir_text: str,
) -> None:
    import numpy as np
    import pynvml
    import torch
    import torch.distributed as dist
    from torch.profiler import ProfilerActivity, profile, record_function

    output_dir = Path(output_dir_text)
    gpu = config["gpus"][rank]
    bench = config["benchmark"]
    affinity = _cpus(gpu["cpu_affinity"])
    os.sched_setaffinity(0, affinity)
    observed_affinity = set(os.sched_getaffinity(0))
    torch.set_num_threads(int(bench["cpu_threads_per_rank"]))
    torch.set_num_interop_threads(1)
    device_index = int(gpu["device"])
    torch.cuda.set_device(device_index)
    device = torch.device("cuda", device_index)
    os.environ.setdefault("NCCL_DEBUG", "INFO")
    os.environ["NCCL_DEBUG_FILE"] = str(output_dir / f"rank{rank}-nccl.log")
    os.environ.setdefault("TORCH_NCCL_ASYNC_ERROR_HANDLING", "1")
    dist.init_process_group(
        backend=config["backend"],
        init_method=init_method,
        rank=rank,
        world_size=world_size,
        device_id=device,
    )
    pynvml.nvmlInit()
    nvml_before = _nvml_sample(device_index)
    properties = torch.cuda.get_device_properties(device_index)
    p2p = {
        str(peer): bool(torch.cuda.can_device_access_peer(device_index, peer))
        for peer in range(world_size)
        if peer != device_index
    }
    events: list[dict[str, Any]] = []

    # Real multi-core CPU preprocessing on the GPU-local socket.
    torch.manual_seed(2026)
    cpu_size = int(bench["cpu_matrix_size"])
    cpu_a = torch.randn((cpu_size, cpu_size), dtype=torch.float32)
    cpu_b = torch.randn((cpu_size, cpu_size), dtype=torch.float32)
    dist.barrier()
    cpu_start = time.time_ns()
    cpu_c = cpu_a @ cpu_b
    cpu_end = time.time_ns()
    cpu_checksum = float(cpu_c[:16, :16].sum())
    events.append(
        {
            "rank": rank,
            "resource": f"cpu_numa{gpu['numa_node']}",
            "event": "cpu_matmul",
            "start_ns": cpu_start,
            "end_ns": cpu_end,
            "duration_ms": (cpu_end - cpu_start) / 1e6,
        }
    )

    dtype = torch.float16 if bench["dtype"] == "float16" else torch.bfloat16
    matrix_size = int(bench["matrix_size"])
    torch.cuda.manual_seed(2026)
    a = torch.randn((matrix_size, matrix_size), device=device, dtype=dtype)
    b = torch.randn((matrix_size, matrix_size), device=device, dtype=dtype)
    for _ in range(int(bench["warmup_iterations"])):
        c = a @ b
    torch.cuda.synchronize(device)
    matmul_durations, start_ns, end_ns = _measure_cuda(
        lambda: torch.mm(a, b), iterations=int(bench["measured_iterations"])
    )
    c = a @ b
    torch.cuda.synchronize(device)
    gpu_checksum = float(c[:16, :16].float().sum())
    average_matmul_ms = mean(matmul_durations)
    matmul_flops = 2 * matrix_size**3
    events.append(
        {
            "rank": rank,
            "resource": f"gpu{device_index}",
            "event": "fp16_matmul",
            "start_ns": start_ns,
            "end_ns": end_ns,
            "cuda_mean_ms": average_matmul_ms,
            "iterations": len(matmul_durations),
            "tflops": matmul_flops / (average_matmul_ms / 1000.0) / 1e12,
        }
    )

    elementwise_durations, start_ns, end_ns = _measure_cuda(
        lambda: torch.nn.functional.silu(c),
        iterations=int(bench["measured_iterations"]),
    )
    events.append(
        {
            "rank": rank,
            "resource": f"gpu{device_index}",
            "event": "silu",
            "start_ns": start_ns,
            "end_ns": end_ns,
            "cuda_mean_ms": mean(elementwise_durations),
        }
    )

    transfer_elements = int(bench["transfer_mib"]) * 1024 * 1024 // 4
    host = torch.empty(transfer_elements, dtype=torch.float32, pin_memory=True).normal_()
    gpu_buffer = torch.empty(transfer_elements, dtype=torch.float32, device=device)
    h2d_durations, start_ns, end_ns = _measure_cuda(
        lambda: gpu_buffer.copy_(host, non_blocking=True), iterations=5
    )
    events.append(
        {
            "rank": rank,
            "resource": f"gpu{device_index}",
            "event": "h2d",
            "start_ns": start_ns,
            "end_ns": end_ns,
            "cuda_mean_ms": mean(h2d_durations),
            "mib": int(bench["transfer_mib"]),
        }
    )
    host_out = torch.empty_like(host, pin_memory=True)
    d2h_durations, start_ns, end_ns = _measure_cuda(
        lambda: host_out.copy_(gpu_buffer, non_blocking=True), iterations=5
    )
    events.append(
        {
            "rank": rank,
            "resource": f"gpu{device_index}",
            "event": "d2h",
            "start_ns": start_ns,
            "end_ns": end_ns,
            "cuda_mean_ms": mean(d2h_durations),
            "mib": int(bench["transfer_mib"]),
        }
    )

    collective_elements = int(bench["all_reduce_mib"]) * 1024 * 1024 // 4
    collective = torch.full(
        (collective_elements,), float(rank + 1), device=device, dtype=torch.float32
    )
    dist.barrier()
    allreduce_durations, start_ns, end_ns = _measure_cuda(
        lambda: dist.all_reduce(collective), iterations=1
    )
    torch.cuda.synchronize(device)
    collective_value = float(collective[0])
    collective_expected = float(sum(range(1, world_size + 1)))
    events.append(
        {
            "rank": rank,
            "resource": "nccl",
            "event": "all_reduce",
            "start_ns": start_ns,
            "end_ns": end_ns,
            "cuda_mean_ms": mean(allreduce_durations),
            "mib": int(bench["all_reduce_mib"]),
        }
    )

    profiler_path = output_dir / f"rank{rank}-torch-trace.json"
    if bench.get("profiler_trace", True):
        prof_tensor = torch.full((1024 * 1024,), float(rank + 1), device=device)
        with profile(
            activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
            record_shapes=True,
        ) as profiler:
            with record_function("agentsys_gpu_matmul"):
                _ = a @ b
            with record_function("agentsys_nccl_all_reduce"):
                dist.all_reduce(prof_tensor)
            torch.cuda.synchronize(device)
        profiler.export_chrome_trace(str(profiler_path))

    nvml_after = _nvml_sample(device_index)
    pynvml.nvmlShutdown()
    dist.barrier()
    dist.destroy_process_group()
    result = {
        "rank": rank,
        "device": device_index,
        "device_name": properties.name,
        "compute_capability": [properties.major, properties.minor],
        "total_memory": properties.total_memory,
        "numa_node": gpu["numa_node"],
        "configured_affinity": sorted(affinity),
        "observed_affinity": sorted(observed_affinity),
        "torch_cpu_threads": torch.get_num_threads(),
        "p2p": p2p,
        "cpu": {
            "matrix_size": cpu_size,
            "duration_ms": (cpu_end - cpu_start) / 1e6,
            "checksum": cpu_checksum,
        },
        "gpu": {
            "matrix_size": matrix_size,
            "dtype": str(dtype),
            "matmul_ms": matmul_durations,
            "matmul_mean_ms": average_matmul_ms,
            "matmul_tflops": matmul_flops / (average_matmul_ms / 1000.0) / 1e12,
            "elementwise_mean_ms": mean(elementwise_durations),
            "h2d_mean_ms": mean(h2d_durations),
            "d2h_mean_ms": mean(d2h_durations),
            "checksum": gpu_checksum,
        },
        "collective": {
            "backend": config["backend"],
            "all_reduce_mean_ms": mean(allreduce_durations),
            "observed": collective_value,
            "expected": collective_expected,
            "correct": abs(collective_value - collective_expected) < 1e-6,
        },
        "nvml_before": nvml_before,
        "nvml_after": nvml_after,
        "profiler_trace": str(profiler_path) if profiler_path.is_file() else None,
        "profiler_trace_bytes": (
            profiler_path.stat().st_size if profiler_path.is_file() else 0
        ),
        "nccl_log": str(output_dir / f"rank{rank}-nccl.log"),
        "events": events,
    }
    path = output_dir / f"rank{rank}.json"
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as handle:
        handle.bind(("127.0.0.1", 0))
        return int(handle.getsockname()[1])


def run_gpu_runtime(
    *,
    config_path: Path = DEFAULT_CONFIG,
    run_id: str = "run_033",
    output_dir: Path | None = None,
    profiler_trace: bool | None = None,
) -> dict[str, Any]:
    import pynvml
    import torch
    import torch.multiprocessing as mp

    config_path = config_path.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("schema_version") != 1:
        raise ValueError("unsupported GPU runtime config")
    if profiler_trace is not None:
        config["benchmark"]["profiler_trace"] = profiler_trace
    world_size = len(config["gpus"])
    if world_size != 2 or torch.cuda.device_count() != 2:
        raise RuntimeError("dual-GPU runtime requires exactly two visible CUDA devices")
    output_dir = (
        output_dir
        or PROJECT_ROOT / "artifacts/gpu_runtime" / run_id
    ).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    pynvml.nvmlInit()
    discovery = [_nvml_sample(index) for index in range(world_size)]
    pynvml.nvmlShutdown()
    topology = subprocess.check_output(["nvidia-smi", "topo", "-m"], text=True)
    lscpu = subprocess.check_output(["lscpu"], text=True)
    init_method = f"tcp://127.0.0.1:{_free_port()}"
    started_ns = time.time_ns()
    mp.spawn(
        _worker,
        args=(world_size, init_method, config, str(output_dir)),
        nprocs=world_size,
        join=True,
    )
    finished_ns = time.time_ns()
    ranks = [
        json.loads((output_dir / f"rank{rank}.json").read_text(encoding="utf-8"))
        for rank in range(world_size)
    ]
    events = [event for rank in ranks for event in rank["events"]]
    events.sort(key=lambda event: (event["start_ns"], event["rank"], event["event"]))
    trace_path = output_dir / "native-hardware-trace.jsonl"
    with trace_path.open("w", encoding="utf-8") as handle:
        for sequence, event in enumerate(events):
            handle.write(json.dumps({**event, "sequence": sequence}, sort_keys=True) + "\n")

    expected_names = [gpu["expected_name"] for gpu in config["gpus"]]
    expected_buses = [gpu["expected_pci_bus"].lower() for gpu in config["gpus"]]
    gates = {
        "two_distinct_rtx4090": len({item["uuid"] for item in discovery}) == 2
        and [item["name"] for item in discovery] == expected_names,
        "pci_bus_identity": [item["pci_bus_id"].lower() for item in discovery]
        == expected_buses,
        "numa_affinity": all(
            rank["configured_affinity"] == rank["observed_affinity"]
            for rank in ranks
        ),
        "both_gpu_ranks_execute": [rank["device"] for rank in ranks] == [0, 1]
        and all(rank["gpu"]["matmul_mean_ms"] > 0 for rank in ranks),
        "multi_cpu_execute": all(
            rank["cpu"]["duration_ms"] > 0
            and rank["torch_cpu_threads"] == config["benchmark"]["cpu_threads_per_rank"]
            for rank in ranks
        ),
        "nccl_collective_correct": all(rank["collective"]["correct"] for rank in ranks),
        "same_gpu_work_checksum": abs(
            ranks[0]["gpu"]["checksum"] - ranks[1]["gpu"]["checksum"]
        )
        < 1e-3,
        "p2p_queried": all(len(rank["p2p"]) == 1 for rank in ranks),
        "nvml_samples": all(
            rank["nvml_before"]["uuid"] == rank["nvml_after"]["uuid"]
            for rank in ranks
        ),
        "kernel_and_transfer_events": all(
            {event["event"] for event in rank["events"]}
            >= {"fp16_matmul", "silu", "h2d", "d2h", "all_reduce", "cpu_matmul"}
            for rank in ranks
        ),
        "profiler_traces": not config["benchmark"].get("profiler_trace", True)
        or all(rank["profiler_trace_bytes"] > 0 for rank in ranks),
    }
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "native_dual_rtx4090_dual_numa_cpu_runtime_measurement",
        "evidence_boundary": "local RTX4090/Xeon measurement; not A100/Core-Ultra paper reproduction",
        "configuration": {
            "path": str(config_path),
            "sha256": _sha256(config_path),
            "value": config,
        },
        "software": {
            "python": os.sys.version,
            "torch": torch.__version__,
            "cuda": torch.version.cuda,
            "nccl": list(torch.cuda.nccl.version()),
            "driver": discovery[0],
        },
        "topology": {"nvidia_smi": topology, "lscpu": lscpu},
        "discovery": discovery,
        "ranks": ranks,
        "trace": {
            "path": str(trace_path),
            "sha256": _sha256(trace_path),
            "events": len(events),
        },
        "wall_time_s": (finished_ns - started_ns) / 1e9,
        "gates": gates,
        "summary": {
            "gpus": world_size,
            "numa_nodes": len({gpu["numa_node"] for gpu in config["gpus"]}),
            "events": len(events),
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }
    result_path = output_dir / "gpu-runtime.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["output"] = str(result_path)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run native dual-GPU, dual-NUMA AgentSys runtime")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id", default="run_033")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument(
        "--disable-torch-profiler",
        action="store_true",
        help="disable the inner CUPTI subscriber when an outer profiler is active",
    )
    args = parser.parse_args(argv)
    result = run_gpu_runtime(
        config_path=args.config,
        run_id=args.run_id,
        output_dir=args.output_dir,
        profiler_trace=False if args.disable_torch_profiler else None,
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def audit_gpu_runtime(
    *,
    run_dir: Path,
    run_id: str = "run_033",
) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    runtime_path = run_dir / "gpu-runtime.json"
    profiled_runtime_path = run_dir / "nsight-runtime/gpu-runtime.json"
    environment_path = PROJECT_ROOT / "artifacts/gpu_runtime/environment.json"
    freeze_path = PROJECT_ROOT / "artifacts/gpu_runtime/pip-freeze.txt"
    report_path = run_dir / "nsight-dual-gpu.nsys-rep"
    sqlite_path = run_dir / "nsight-dual-gpu.sqlite"
    kernel_path = run_dir / "nsight-stats_cuda_gpu_kern_sum.csv"
    api_path = run_dir / "nsight-stats_cuda_api_sum.csv"
    memory_path = run_dir / "nsight-stats_cuda_gpu_mem_time_sum.csv"
    paths = (
        runtime_path,
        profiled_runtime_path,
        environment_path,
        freeze_path,
        report_path,
        sqlite_path,
        kernel_path,
        api_path,
        memory_path,
    )
    if not all(path.is_file() and path.stat().st_size > 0 for path in paths):
        missing = [str(path) for path in paths if not path.is_file() or path.stat().st_size == 0]
        raise FileNotFoundError(f"missing GPU evidence: {missing}")
    runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
    profiled_runtime = json.loads(profiled_runtime_path.read_text(encoding="utf-8"))
    environment = json.loads(environment_path.read_text(encoding="utf-8"))
    freeze = freeze_path.read_text(encoding="utf-8")
    kernels = _csv(kernel_path)
    apis = _csv(api_path)
    memory = _csv(memory_path)
    kernel_names = {row["Name"] for row in kernels}
    api_names = {row["Name"] for row in apis}
    memory_names = {row["Operation"] for row in memory}
    gates = {
        "runtime_11": runtime["summary"]
        == {
            "gpus": 2,
            "numa_nodes": 2,
            "events": 12,
            "gates": 11,
            "passing": 11,
            "failing": 0,
            "pass": True,
        },
        "profiled_runtime_11": profiled_runtime["summary"] == runtime["summary"]
        and profiled_runtime["configuration"]["sha256"]
        == runtime["configuration"]["sha256"]
        and len(profiled_runtime["ranks"]) == 2,
        "software_lock": environment["torch"] == "2.7.0+cu128"
        and environment["torch_cuda"] == "12.8"
        and environment["nccl"] == [2, 26, 2]
        and "torch==2.7.0+cu128" in freeze
        and "nvidia-ml-py==13.610.43" in freeze,
        "nsight_report": report_path.stat().st_size > 1_000_000
        and sqlite_path.stat().st_size > 1_000_000,
        "nsight_kernels": any("gemm" in name.lower() for name in kernel_names)
        and any("nccl" in name.lower() for name in kernel_names)
        and any("silu" in name.lower() for name in kernel_names),
        "nsight_cuda_api": "cudaLaunchKernel" in api_names
        and "cudaMemcpyAsync" in api_names,
        "nsight_memory": "[CUDA memcpy Host-to-Device]" in memory_names
        and "[CUDA memcpy Device-to-Host]" in memory_names,
        "p2p_false_and_collective_correct": all(
            not any(rank["p2p"].values()) and rank["collective"]["correct"]
            for rank in runtime["ranks"]
        ),
        "local_measurement_boundary": "not A100/Core-Ultra" in runtime["evidence_boundary"],
    }
    evidence = {
        str(path.relative_to(PROJECT_ROOT)): {
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        for path in paths
    }
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "native_dual_gpu_multicpu_runtime_and_nsight_audit",
        "evidence": evidence,
        "kernel_rows": len(kernels),
        "api_rows": len(apis),
        "memory_rows": len(memory),
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }
    output = run_dir / "gpu-runtime-audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["output"] = str(output)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit native GPU runtime and Nsight evidence")
    parser.add_argument(
        "--run-dir", type=Path, default=PROJECT_ROOT / "artifacts/gpu_runtime/run_033"
    )
    parser.add_argument("--run-id", default="run_033")
    args = parser.parse_args(argv)
    result = audit_gpu_runtime(run_dir=args.run_dir, run_id=args.run_id)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

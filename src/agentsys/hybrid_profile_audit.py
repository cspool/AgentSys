from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

from .workload import PROJECT_ROOT


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _values(rows: list[dict[str, str]]) -> list[str]:
    return [str(value) for row in rows for value in row.values()]


def audit_hybrid_profile(*, profile_dir: Path, run_id: str) -> dict[str, Any]:
    profile_dir = profile_dir.resolve()
    native_path = profile_dir / "native/native-runtime.json"
    trace_path = profile_dir / "native/native-trace.jsonl"
    report_path = profile_dir / "react-tool.nsys-rep"
    sqlite_path = profile_dir / "react-tool.sqlite"
    kernel_path = profile_dir / "nsight-stats_cuda_gpu_kern_sum.csv"
    api_path = profile_dir / "nsight-stats_cuda_api_sum.csv"
    memory_path = profile_dir / "nsight-stats_cuda_gpu_mem_time_sum.csv"
    nvtx_path = profile_dir / "nsight-stats_nvtx_sum.csv"
    log_path = profile_dir / "profile.log"
    paths = (
        native_path,
        trace_path,
        report_path,
        sqlite_path,
        kernel_path,
        api_path,
        memory_path,
        nvtx_path,
        log_path,
    )
    missing = [path for path in paths if not path.is_file() or path.stat().st_size == 0]
    if missing:
        raise FileNotFoundError(f"missing hybrid profile evidence: {missing}")
    native = json.loads(native_path.read_text(encoding="utf-8"))
    trace = [json.loads(line) for line in trace_path.read_text(encoding="utf-8").splitlines()]
    kernels = _csv(kernel_path)
    apis = _csv(api_path)
    memory = _csv(memory_path)
    nvtx = _csv(nvtx_path)
    kernel_text = "\n".join(_values(kernels)).lower()
    api_text = "\n".join(_values(apis))
    memory_text = "\n".join(_values(memory))
    nvtx_text = "\n".join(_values(nvtx))
    op_events = [event for event in trace if event["event"] == "mir_operator"]
    expected_ranges = {
        f"agentsys.mllm::{event['call_id']}::{event['source_index']}::{event['op_type']}"
        for event in op_events
    }
    nccl_logs = [profile_dir / f"native/rank{rank}-nccl.log" for rank in (0, 1)]
    gates = {
        "native_runtime_13": native["summary"]
        == {
            "calls": 3,
            "events": 29,
            "failing": 0,
            "gates": 13,
            "gpus": 2,
            "llm_calls": 2,
            "mir_operators": 16,
            "numa_nodes": 2,
            "pass": True,
            "passing": 13,
            "tool_calls": 1,
        }
        and all(native["gates"].values()),
        "profile_reports": report_path.stat().st_size > 500_000
        and sqlite_path.stat().st_size > 1_000_000,
        "cuda_kernel_classes": any(token in kernel_text for token in ("gemm", "cutlass"))
        and "nccl" in kernel_text
        and any(token in kernel_text for token in ("elementwise", "rms", "norm")),
        "cuda_api": "cudaLaunchKernel" in api_text
        and "cudaMemcpyAsync" in api_text,
        "cuda_memory": "Host-to-Device" in memory_text
        and "Device-to-Host" in memory_text,
        "all_mir_nvtx_ranges": len(expected_ranges) == 16
        and all(name in nvtx_text for name in expected_ranges),
        "trace_parameter_consumption": len(op_events) == 16
        and all(event.get("dtype") == "float16" for event in op_events)
        and all(event.get("iterations") == 1 for event in op_events),
        "nccl_shm_transport": all(
            path.is_file()
            and "via SHM/direct/direct" in path.read_text(encoding="utf-8")
            for path in nccl_logs
        ),
        "evidence_boundary": "AgentSys MIR-to-CUDA adapter" in native["evidence_boundary"]
        and "not A100" in native["evidence_boundary"],
    }
    evidence = {
        str(path.relative_to(PROJECT_ROOT)): {
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        for path in (*paths, *nccl_logs)
    }
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "nsight_profiled_workload_aware_dual_gpu_mir_adapter_audit",
        "profile_dir": str(profile_dir),
        "native_summary": native["summary"],
        "rows": {
            "kernels": len(kernels),
            "apis": len(apis),
            "memory": len(memory),
            "nvtx": len(nvtx),
        },
        "expected_nvtx_ranges": sorted(expected_ranges),
        "evidence": evidence,
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }
    output = profile_dir / "profile-audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["output"] = str(output)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit Nsight evidence for the hybrid Agent runtime")
    parser.add_argument(
        "--profile-dir",
        type=Path,
        default=PROJECT_ROOT / "artifacts/hybrid_profile/run_041",
    )
    parser.add_argument("--run-id", default="run_041")
    args = parser.parse_args(argv)
    result = audit_hybrid_profile(profile_dir=args.profile_dir, run_id=args.run_id)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

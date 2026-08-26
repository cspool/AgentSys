#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.mllm_native import DEFAULT_BUILD_DIR, run_native_mllm_suite
from agentsys.mllm_npu import PROJECT_ROOT, run_mllm_npu_reproduction, write_schedule_trace


def _absolute(path: Path) -> Path:
    return path if path.is_absolute() else PROJECT_ROOT / path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_023")
    parser.add_argument("--build-dir", type=Path, default=DEFAULT_BUILD_DIR)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/paper-mllm-run_023.json",
    )
    parser.add_argument(
        "--trace-prefix",
        type=Path,
        default=PROJECT_ROOT / "artifacts/traces/paper-mllm-run_023",
    )
    args = parser.parse_args()
    output = _absolute(args.output)
    trace_prefix = _absolute(args.trace_prefix)

    native = run_native_mllm_suite(build_dir=args.build_dir, run_id=args.run_id)
    performance = run_mllm_npu_reproduction(run_id=args.run_id)
    events = performance.pop("_schedule_events")
    naive_trace = trace_prefix.with_name(trace_prefix.name + "-naive.jsonl")
    ooo_trace = trace_prefix.with_name(trace_prefix.name + "-ooo.jsonl")
    write_schedule_trace(events["naive"], naive_trace, mode="naive")
    write_schedule_trace(events["out_of_order"], ooo_trace, mode="out_of_order")
    performance["traces"] = {
        "naive": str(naive_trace.relative_to(PROJECT_ROOT)),
        "out_of_order": str(ooo_trace.relative_to(PROJECT_ROOT)),
    }
    result = {
        "schema_version": 1,
        "run_id": args.run_id,
        "paper": "mllm/llm.npu",
        "native_framework": native,
        "performance_reproduction": performance,
        "summary": {
            "native_executables_passed": native["summary"]["executables_passed"],
            "native_executables_total": native["summary"]["executables"],
            "native_gtest_cases_passed": native["summary"]["gtest_cases_passed"],
            "paper_endpoints_passed": performance["summary"]["paper_endpoints_passed"],
            "paper_endpoints_total": performance["summary"]["paper_endpoints_total"],
            "max_relative_error": performance["summary"]["max_relative_error"],
            "pass": native["summary"]["pass"] and performance["summary"]["pass"],
        },
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

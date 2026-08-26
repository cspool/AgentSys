#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.mllm_npu import PROJECT_ROOT, run_mllm_npu_reproduction, write_schedule_trace


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_023")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/mllm-npu-run_023.json",
    )
    parser.add_argument(
        "--trace-prefix",
        type=Path,
        default=PROJECT_ROOT / "artifacts/traces/mllm-npu-run_023",
    )
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    trace_prefix = (
        args.trace_prefix
        if args.trace_prefix.is_absolute()
        else PROJECT_ROOT / args.trace_prefix
    )
    result = run_mllm_npu_reproduction(run_id=args.run_id)
    schedule_events = result.pop("_schedule_events")
    naive_trace = trace_prefix.with_name(trace_prefix.name + "-naive.jsonl")
    ooo_trace = trace_prefix.with_name(trace_prefix.name + "-ooo.jsonl")
    write_schedule_trace(schedule_events["naive"], naive_trace, mode="naive")
    write_schedule_trace(schedule_events["out_of_order"], ooo_trace, mode="out_of_order")
    result["traces"] = {
        "naive": str(naive_trace.relative_to(PROJECT_ROOT)),
        "out_of_order": str(ooo_trace.relative_to(PROJECT_ROOT)),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(output)
    print(naive_trace)
    print(ooo_trace)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

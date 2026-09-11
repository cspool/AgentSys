#!/usr/bin/env python3
"""Build a larger execution load from a certified run_040 hybrid plan.

The shipped plans are short (16-80 operators, matrix 768-1024, one operator
iteration), so single-operator GPU time is 1-16 us and host staging dominates.
This builder produces a longer, heavier DAG *without touching src/agentsys/*:

* ``--matrix-scale k``: multiply every LLM call's matrix_size by k;
* ``--operator-iterations n``: set the adapter's operator_iterations (each MIR
  operator is replayed n times inside its NVTX range, exactly as the certified
  adapter already supports);
* ``--repeat r``: replicate the whole DAG r times back to back, with unique
  call ids (``<call>#r<i>``) and shifted waves, so the workload is r times
  longer with the same per-wave structure.

Everything else (operator lists, engines, dtypes, tool calls, priorities) is
copied verbatim. The summary block and workload name are rewritten so the
downstream analyzers see a consistent plan.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--matrix-scale", type=int, default=4)
    parser.add_argument("--operator-iterations", type=int, default=32)
    parser.add_argument("--repeat", type=int, default=1)
    args = parser.parse_args(argv)

    base = json.loads(args.plan.read_text())
    plan = copy.deepcopy(base)
    plan["configuration"]["adapter"]["operator_iterations"] = args.operator_iterations
    plan["configuration"]["adapter"]["matrix_base"] = int(base["configuration"]["adapter"]["matrix_base"]) * args.matrix_scale
    plan["configuration"]["adapter"]["matrix_max"] = int(base["configuration"]["adapter"]["matrix_max"]) * args.matrix_scale
    plan["configuration"]["adapter"]["matrix_step"] = int(base["configuration"]["adapter"]["matrix_step"]) * args.matrix_scale

    base_calls = sorted(base["calls"], key=lambda c: (c["wave"], c["index"]))
    waves = int(base["summary"]["waves"])
    calls = []
    for r in range(args.repeat):
        for c in base_calls:
            nc = copy.deepcopy(c)
            nc["call_id"] = f"{c['call_id']}#r{r}" if args.repeat > 1 else c["call_id"]
            nc["index"] = c["index"] + r * len(base_calls)
            nc["wave"] = c["wave"] + r * waves
            nc["deps"] = [f"{d}#r{r}" if args.repeat > 1 else d for d in c.get("deps", [])]
            if nc["kind"] == "llm":
                nc["native"]["matrix_size"] = int(c["native"]["matrix_size"]) * args.matrix_scale
            calls.append(nc)
    plan["calls"] = calls
    s = plan["summary"]
    s["calls"] = len(calls)
    s["llm_calls"] = sum(1 for c in calls if c["kind"] == "llm")
    s["tool_calls"] = sum(1 for c in calls if c["kind"] == "tool")
    s["mir_operators"] = sum(len(c.get("mir_operators", [])) for c in calls)
    s["waves"] = waves * args.repeat
    for eng in ("me", "ve", "de"):
        s[f"{eng}_operators"] = sum(1 for c in calls for o in c.get("mir_operators", []) if o["engine"] == eng)
    plan["workload"]["name"] = args.name
    plan["workload"]["derived_from"] = {"plan": str(args.plan), "sha256": hashlib.sha256(args.plan.read_bytes()).hexdigest(), "base_workload": base["workload"]["name"],
                                        "matrix_scale": args.matrix_scale, "operator_iterations": args.operator_iterations, "repeat": args.repeat}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"name": args.name, "calls": s["calls"], "llm_calls": s["llm_calls"], "mir_operators": s["mir_operators"], "waves": s["waves"],
                      "matrix_sizes": sorted({c["native"]["matrix_size"] for c in calls if c["kind"] == "llm"}), "operator_iterations": args.operator_iterations}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

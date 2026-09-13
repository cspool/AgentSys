#!/usr/bin/env python3
"""Build the reduced plan for w03 NCU replay in the llm strand.

Every LLM call keeps its real prompt length (real prefill GEMM/SDPA shapes)
but decodes only 2 tokens (one prefill forward + one decode forward), so the
NCU replay covers every forward-stage kernel family once per call without
replaying tens of thousands of decode launches. Tool calls are unchanged.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--plan", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--output-tokens", type=int, default=2)
    a = p.parse_args()
    plan = json.loads(a.plan.read_text())
    for call in plan["calls"]:
        if call["kind"] == "llm":
            call["output_tokens"] = a.output_tokens
    plan["workload"]["name"] = plan["workload"]["name"] + f"_ncu{a.output_tokens}"
    plan.setdefault("provenance", {})["llm_ncu_reduction"] = {
        "source_plan": str(a.plan), "output_tokens_per_llm_call": a.output_tokens,
        "note": "prompt lengths unchanged; reduced decode for NCU replay only",
    }
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(plan, indent=2) + "\n")
    print(a.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

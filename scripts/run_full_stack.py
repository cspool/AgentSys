#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.fullstack import PROJECT_ROOT, run_full_stack


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_007")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/full-stack-run_007.json",
    )
    parser.add_argument(
        "--trace-output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/traces/full-stack-run_007.jsonl",
    )
    args = parser.parse_args()
    artifact, trace = run_full_stack(run_id=args.run_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    trace.write_jsonl(args.trace_output)
    print(json.dumps(artifact["summary"], indent=2, sort_keys=True))
    print(json.dumps(artifact["derived"], indent=2, sort_keys=True))
    print(args.output)
    print(args.trace_output)
    return 0 if artifact["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


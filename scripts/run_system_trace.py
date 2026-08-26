#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.system_trace import PROJECT_ROOT, write_system_trace


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_021")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/system-trace-run_021.json",
    )
    parser.add_argument(
        "--trace-output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/traces/system-trace-run_021.jsonl",
    )
    args = parser.parse_args()
    result = write_system_trace(args.output, args.trace_output, run_id=args.run_id)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(json.dumps(result["derived"], indent=2, sort_keys=True))
    print(args.output)
    print(args.trace_output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

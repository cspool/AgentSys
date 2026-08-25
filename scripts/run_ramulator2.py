#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.ramulator import PROJECT_ROOT, run_ramulator


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_012")
    parser.add_argument("--max-records", type=int, default=32768)
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "artifacts/results/ramulator2-run_012.json")
    args = parser.parse_args()
    result = run_ramulator(run_id=args.run_id, max_records=args.max_records)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(json.dumps(result["derived"], indent=2, sort_keys=True))
    print(args.output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.agentix_model import PROJECT_ROOT, run_agentix_aggregate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_010")
    parser.add_argument("--output", type=Path, default=PROJECT_ROOT / "artifacts/results/agentix-run_010.json")
    args = parser.parse_args()
    result = run_agentix_aggregate(run_id=args.run_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(args.output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.atx_model import PROJECT_ROOT, write_atx_audit


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_004")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/atx-run_004.json",
    )
    args = parser.parse_args()
    result = write_atx_audit(args.output, run_id=args.run_id)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(args.output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


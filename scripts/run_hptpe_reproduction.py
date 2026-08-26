#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.hptpe import PROJECT_ROOT, run_hptpe_reproduction


def _absolute(path: Path) -> Path:
    return path if path.is_absolute() else PROJECT_ROOT / path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_024")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/paper-hptpe-run_024.json",
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=PROJECT_ROOT / "artifacts/logs/hptpe-run_024",
    )
    args = parser.parse_args()
    output = _absolute(args.output)
    log_dir = _absolute(args.log_dir)
    result = run_hptpe_reproduction(run_id=args.run_id, log_dir=log_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(output)
    print(log_dir)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.mllm_native import DEFAULT_BUILD_DIR, PROJECT_ROOT, run_native_mllm_suite


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_023")
    parser.add_argument("--build-dir", type=Path, default=DEFAULT_BUILD_DIR)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/mllm-native-run_023.json",
    )
    args = parser.parse_args()
    result = run_native_mllm_suite(build_dir=args.build_dir, run_id=args.run_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(args.output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

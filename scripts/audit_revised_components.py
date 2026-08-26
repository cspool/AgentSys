#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.hptpe import PROJECT_ROOT
from agentsys.revised_components import audit_revised_components


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_025")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/revised-components-run_025.json",
    )
    args = parser.parse_args()
    output = args.output if args.output.is_absolute() else PROJECT_ROOT / args.output
    result = audit_revised_components(run_id=args.run_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

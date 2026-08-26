#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.agent_application import PROJECT_ROOT
from agentsys.revised_system_compiler import compile_and_write_revised


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_028")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/app_traces/revised-compiled-workload-run_028.json",
    )
    parser.add_argument(
        "--application-output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/app_traces/revised-agent-application-run_028.json",
    )
    parser.add_argument(
        "--header-output",
        type=Path,
        default=PROJECT_ROOT / "system_sim/software/generated/agentsys_revised_app_trace.h",
    )
    args = parser.parse_args()
    result = compile_and_write_revised(
        run_id=args.run_id,
        manifest_path=args.output,
        application_path=args.application_output,
        header_path=args.header_output,
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(args.output)
    print(args.header_output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

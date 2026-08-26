#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.system_trace_compiler import (
    APPLICATION_TRACE,
    COMPILED_MANIFEST,
    GENERATED_HEADER,
    compile_and_write,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_021")
    parser.add_argument("--header", type=Path, default=GENERATED_HEADER)
    parser.add_argument("--manifest", type=Path, default=COMPILED_MANIFEST)
    parser.add_argument("--application-output", type=Path, default=APPLICATION_TRACE)
    args = parser.parse_args()
    result = compile_and_write(
        header_path=args.header,
        manifest_path=args.manifest,
        application_path=args.application_output,
        run_id=args.run_id,
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(args.header)
    print(args.manifest)
    print(args.application_output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

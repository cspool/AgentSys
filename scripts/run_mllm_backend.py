#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from agentsys.mllm_backend import MLLM_ROOT, PROJECT_ROOT, parse_mir, run_mllm_backend, write_operator_jsonl


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", default="run_005")
    parser.add_argument("--max-ops", type=int, default=160)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/results/mllm-run_005.json",
    )
    parser.add_argument(
        "--trace-output",
        type=Path,
        default=PROJECT_ROOT / "artifacts/traces/mllm-qwen3-run_005.jsonl",
    )
    args = parser.parse_args()
    result = run_mllm_backend(model_ops=args.max_ops, run_id=args.run_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    operators = parse_mir(
        MLLM_ROOT / "examples/qwen3_qnn_aot/qwen3_qnn_aot_1.7B.mir",
        max_ops=args.max_ops,
    )
    write_operator_jsonl(operators, args.trace_output)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(json.dumps({"decoder_slice_speedup": result["decoder_slice"]["speedup"]}, indent=2))
    print(args.output)
    print(args.trace_output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())


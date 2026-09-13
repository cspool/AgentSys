#!/usr/bin/env python3
"""w04 / G05, llm strand: full-workload estimate with forward-stage operators.

Identical method to ``analyze_w04_full_workload_estimate`` (representative
w02 medians keyed by (call kind, matrix size, process, op type), instance
counts from the target plan, target evidence used only for scoring) — but the
per-call operator enumeration follows the real-model runtime: one prefill
forward + (output_tokens - 1) decode forwards, each forward being
``embed``, ``layerNN`` x L, ``head``, ``sample`` stages, exactly the NVTX
stages the llm runtime emits.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyze_w04_full_workload_estimate as w04  # noqa: E402

NUM_LAYERS: int = 0  # set in main from the target's w01 run metadata


def llm_expected_instances(plan: dict[str, Any]) -> list[dict[str, Any]]:
    stages = ["embed"] + [f"layer{i:02d}" for i in range(NUM_LAYERS)] + ["head", "sample"]
    out: list[dict[str, Any]] = []
    for call in sorted(plan["calls"], key=lambda c: (c["wave"], c["index"])):
        size = str(call["native"]["matrix_size"])
        out.append({"call_id": None, "call_kind": "dag", "matrix_size": "", "process": "dag_schedule_gap", "op_type": "", "before_call": call["call_id"]})
        if call["kind"] == "llm":
            for p in w04.LLM_FIXED[:5]:
                out.append({"call_id": call["call_id"], "call_kind": "llm", "matrix_size": size, "process": p, "op_type": ""})
            index = 0
            for step in range(int(call["output_tokens"])):
                phase = "prefill" if step == 0 else "decode"
                for stage in stages:
                    if index > 0:
                        out.append({"call_id": call["call_id"], "call_kind": "llm", "matrix_size": size, "process": "inter_operator_dispatch", "op_type": ""})
                    op_type = f"{phase}_{stage}"
                    out.append({"call_id": call["call_id"], "call_kind": "llm", "matrix_size": size, "process": f"mir_operator:{op_type}", "op_type": op_type, "op_index": index, "engine": "llm"})
                    index += 1
        else:
            out.append({"call_id": call["call_id"], "call_kind": "tool", "matrix_size": size, "process": "agent_tool_execute_cpu", "op_type": ""})
        if call["kind"] == "llm":
            for p in w04.LLM_FIXED[5:]:
                out.append({"call_id": call["call_id"], "call_kind": "llm", "matrix_size": size, "process": p, "op_type": ""})
    out.append({"call_id": None, "call_kind": "dag", "matrix_size": "", "process": "iteration_tail_sync", "op_type": ""})
    return out


def main(argv: list[str] | None = None) -> int:
    global NUM_LAYERS
    args = argv if argv is not None else sys.argv[1:]
    root = Path(args[args.index("--artifact-root") + 1])
    target = args[args.index("--target") + 1] if "--target" in args else "react_moa_mcts"
    meta = json.loads((root / "g01_operator_trace" / target / "native" / "run_metadata.json").read_text())
    NUM_LAYERS = int(meta["model"]["layers"])
    w04.expected_instances = llm_expected_instances
    return w04.main(args)


if __name__ == "__main__":
    raise SystemExit(main())

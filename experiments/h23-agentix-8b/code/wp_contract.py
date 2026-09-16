#!/usr/bin/env python3
"""Write the canonical workload-profile run contract (R07 shared contract).

Every capture in the chain writes this sidecar before its output is interpreted.
The contract_id is a digest over the contract fields themselves, so two captures
carry the same id only when every declared field matches.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

FIELDS = (
    "run_mode", "run_id", "model_path", "model_base", "engine_version",
    "engine_flags", "workload_path", "workload_class",
    "arrival_rate_programs_per_s", "seed", "policy", "max_model_len",
    "max_num_seqs", "dtype", "attention_backend", "enforce_eager",
    "cudagraph_mode", "enable_prefix_caching", "gpu_memory_utilization",
    "device", "layer_count_contract", "instrumentation",
)


def git_rev() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--run-mode", default="FRESH_RUN", choices=["FRESH_RUN", "REFERENCE_AUDIT"])
    ap.add_argument("--workload", type=Path, required=True)
    ap.add_argument("--policy", required=True)
    ap.add_argument("--model-path", default="/data3/docker_model/AgentSys/Llama-3.1-8B")
    ap.add_argument("--max-model-len", type=int, default=4096)
    ap.add_argument("--max-num-seqs", type=int, default=16)
    ap.add_argument("--gpu-util", type=float, default=0.90)
    ap.add_argument("--device", default="1")
    ap.add_argument("--enforce-eager", action="store_true")
    ap.add_argument("--prefix-caching", default="true")
    ap.add_argument("--instrumentation", default="none",
                    help="comma list, e.g. modproc,w_probes,nsys,dispatchmode")
    a = ap.parse_args()

    wl = json.loads(a.workload.read_text())
    cfg = wl.get("config", {})
    contract = {
        "run_mode": a.run_mode,
        "run_id": a.run_id,
        "source_revision": git_rev(),
        "model_path": a.model_path,
        "model_base": Path(a.model_path).name,
        "engine_version": "vllm-0.29-v1",
        "engine_flags": {
            "VLLM_USE_V2_MODEL_RUNNER": "0",
            "VLLM_ENABLE_V1_MULTIPROCESSING": "0",
            "VLLM_NVTX_SCOPES_FOR_PROFILING": "1",
        },
        "workload_path": str(a.workload),
        "workload_class": cfg.get("workload_class"),
        "arrival_rate_programs_per_s": cfg.get("arrival_rate_programs_per_s"),
        "seed": cfg.get("seed"),
        "policy": a.policy,
        "max_model_len": a.max_model_len,
        "max_num_seqs": a.max_num_seqs,
        "dtype": "bfloat16",
        "attention_backend": "flash-attn (vLLM default selection)",
        "enforce_eager": bool(a.enforce_eager),
        "cudagraph_mode": "none" if a.enforce_eager else "FULL_AND_PIECEWISE",
        "enable_prefix_caching": a.prefix_caching == "true",
        "gpu_memory_utilization": a.gpu_util,
        "device": a.device,
        "layer_count_contract": {"model": Path(a.model_path).name, "layers": 32},
        "instrumentation": [s for s in a.instrumentation.split(",") if s and s != "none"],
    }
    body = json.dumps({k: contract[k] for k in FIELDS}, sort_keys=True)
    contract["contract_id"] = hashlib.sha256(body.encode()).hexdigest()[:16]
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(contract, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"contract_id": contract["contract_id"], "out": str(a.out)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

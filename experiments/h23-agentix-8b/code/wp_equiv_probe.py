#!/usr/bin/env python3
"""R01 wrapper-equivalence probe.

One process, one model load, two passes: pass A runs the unpatched model, then
the module process hooks are installed and pass B runs the same prompts with the
same sampling parameters. Equivalence is decided on the produced token id
sequences, not on token counts — identical counts are guaranteed by
max_tokens/ignore_eos and would prove nothing.

Same-process comparison is deliberate: two separate processes would also differ
in allocator state and KV block layout, so a mismatch could not be attributed to
the patch.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", default="/data3/docker_model/AgentSys/Llama-3.1-8B")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--prompts", type=int, default=6)
    ap.add_argument("--prompt-tokens", type=int, default=256)
    ap.add_argument("--max-tokens", type=int, default=48)
    ap.add_argument("--gpu-util", type=float, default=0.85)
    ap.add_argument("--max-model-len", type=int, default=2048)
    ap.add_argument("--filler-token-id", type=int, default=970)
    a = ap.parse_args()
    a.out.parent.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("VLLM_USE_V2_MODEL_RUNNER", "0")
    os.environ.setdefault("VLLM_ENABLE_V1_MULTIPROCESSING", "0")
    from vllm import LLM, SamplingParams

    llm = LLM(model=a.model_dir, dtype="bfloat16", gpu_memory_utilization=a.gpu_util,
              max_model_len=a.max_model_len, enforce_eager=True, seed=0,
              enable_prefix_caching=False, disable_log_stats=True)
    params = SamplingParams(max_tokens=a.max_tokens, ignore_eos=True, temperature=0.0)
    prompts = [{"prompt_token_ids": [a.filler_token_id] * (a.prompt_tokens + i)}
               for i in range(a.prompts)]

    def run() -> list[list[int]]:
        outs = llm.generate(prompts, params)
        return [list(o.outputs[0].token_ids) for o in outs]

    before = run()

    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import wp_modproc
    installed = wp_modproc.install(verbose=True)

    after = run()

    mismatches = [{"prompt_index": i,
                   "first_divergence": next((k for k, (x, y) in enumerate(zip(b, c)) if x != y), None),
                   "len_before": len(b), "len_after": len(c)}
                  for i, (b, c) in enumerate(zip(before, after)) if b != c]
    payload = {
        "gate": "wrapper_equivalence",
        "method": "same-process unpatched pass A vs patched pass B, token-id equality",
        "model_dir": a.model_dir,
        "enforce_eager": True,
        "prompts": a.prompts,
        "prompt_tokens_base": a.prompt_tokens,
        "max_tokens": a.max_tokens,
        "taxonomy": installed.get("taxonomy"),
        "sequences_compared": len(before),
        "tokens_compared": sum(len(x) for x in before),
        "mismatched_sequences": len(mismatches),
        "mismatches": mismatches,
        "passed": not mismatches,
    }
    a.out.write_text(json.dumps(payload, indent=1) + "\n")
    print(json.dumps({k: payload[k] for k in
                      ("sequences_compared", "tokens_compared",
                       "mismatched_sequences", "passed")}))
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

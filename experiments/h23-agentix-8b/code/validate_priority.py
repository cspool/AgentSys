#!/usr/bin/env python3
"""Validate that vLLM's priority scheduling actually reorders a queue.

Fills the engine with low-priority (large value) requests so the waiting queue is
non-empty, then submits one high-priority (value 0) request and measures its
TTFT. With the control arm (all priorities equal) the late request must wait
behind the whole queue; with priority it must jump it.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import time


async def run(args: argparse.Namespace) -> dict:
    from vllm import SamplingParams
    from vllm.engine.arg_utils import AsyncEngineArgs
    from vllm.v1.engine.async_llm import AsyncLLM

    engine_args = AsyncEngineArgs(
        model=str(args.model_dir), dtype="bfloat16", gpu_memory_utilization=args.gpu_memory_utilization,
        max_model_len=args.max_model_len, max_num_seqs=args.max_num_seqs, enforce_eager=True,
        disable_log_stats=True, scheduling_policy="priority", seed=0,
    )
    engine = AsyncLLM.from_engine_args(engine_args)
    try:
        async def one(rid: str, priority: int, n_out: int, prompt_len: int) -> dict:
            params = SamplingParams(max_tokens=n_out, ignore_eos=True, temperature=0.0)
            t0 = time.monotonic_ns()
            first = None
            async for _ in engine.generate({"prompt_token_ids": [970] * prompt_len}, params, request_id=rid, priority=priority):
                if first is None:
                    first = time.monotonic_ns()
            done = time.monotonic_ns()
            return {"id": rid, "priority": priority, "ttft_ms": (first - t0) / 1e6 if first else None,
                    "total_ms": (done - t0) / 1e6}

        # warm-up
        async for _ in engine.generate({"prompt_token_ids": [970] * 32}, SamplingParams(max_tokens=4, ignore_eos=True), request_id="warmup", priority=0):
            pass

        n_backlog = args.backlog
        fillers = [asyncio.create_task(one(f"fill{i}", args.fill_priority, args.fill_tokens, args.prompt_len)) for i in range(n_backlog)]
        await asyncio.sleep(0.3)  # let the backlog enter the waiting queue
        late = await one("late", 0 if args.honor_priority else args.fill_priority, args.late_tokens, args.prompt_len)
        rest = await asyncio.gather(*fillers)
        return {"late": late, "backlog_ttft_ms": sorted(r["ttft_ms"] for r in rest),
                "backlog_median_ttft_ms": sorted(r["ttft_ms"] for r in rest)[len(rest) // 2],
                "honor_priority": args.honor_priority, "max_num_seqs": args.max_num_seqs,
                "backlog": n_backlog, "pass": late["ttft_ms"] < sorted(r["ttft_ms"] for r in rest)[len(rest) // 2] if args.honor_priority else True}
    finally:
        engine.shutdown()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", default="/data3/docker_model/AgentSys/Llama-3.1-8B")
    ap.add_argument("--gpu-memory-utilization", type=float, default=0.90)
    ap.add_argument("--max-model-len", type=int, default=4096)
    ap.add_argument("--max-num-seqs", type=int, default=8)
    ap.add_argument("--backlog", type=int, default=16)
    ap.add_argument("--prompt-len", type=int, default=512)
    ap.add_argument("--fill-tokens", type=int, default=64)
    ap.add_argument("--late-tokens", type=int, default=8)
    ap.add_argument("--fill-priority", type=int, default=100000)
    ap.add_argument("--honor-priority", action="store_true", help="give the late request priority 0; otherwise it shares the backlog's priority")
    a = ap.parse_args()
    print(json.dumps(asyncio.run(run(a)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

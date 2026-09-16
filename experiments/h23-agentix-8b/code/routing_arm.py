#!/usr/bin/env python3
"""Third innovation group reproduction: process-table STICKY ROUTING
(multi-engine KV affinity) vs affinity-blind round-robin.

Two identical engines (same model, same GPU, split memory = two CUDA
contexts). The ONLY variable is the router:
  sticky : program -> fixed engine (process-table affinity, the paper's ③)
  rr     : call    -> engines in round-robin (breaks within-program affinity)

Real reuse surface: each program owns a private random token stream; call j's
prompt is stream[:L_j] with L_j strictly growing (capped at --ctx-cap), so
prompt_j prefix-matches prompt_{j-1} exactly. On the same engine the prefix is
cached (within-program hit, paper Fig.7 left); on a different engine it is
cold. Cross-program prompts never share a prefix (Fig.7 right).

Outputs calls_routing_<policy>.jsonl with the same fields the A3/A4 timeline
builders consume, plus engine index and context length per call; engine-side
prefix-cache hit-rate lines are kept in the log (disable_log_stats=False).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import multiprocessing as mp
import os
import random
import time
from pathlib import Path


def engine_proc(role: str, model_dir: str, gpu_util: float, max_num_seqs: int,
                req_q: mp.Queue, res_q: mp.Queue, ready, device: str):
    os.environ["CUDA_VISIBLE_DEVICES"] = device
    os.environ.setdefault("VLLM_USE_V2_MODEL_RUNNER", "0")
    from vllm import SamplingParams
    from vllm.engine.arg_utils import AsyncEngineArgs
    from vllm.v1.engine.async_llm import AsyncLLM

    args = AsyncEngineArgs(
        model=model_dir, dtype="bfloat16", gpu_memory_utilization=gpu_util,
        max_model_len=4096, enforce_eager=False, disable_log_stats=False,
        max_num_seqs=max_num_seqs, seed=0)
    engine = AsyncLLM.from_engine_args(args)

    async def main():
        warm = SamplingParams(max_tokens=4, ignore_eos=True, temperature=0.0)
        async for _ in engine.generate({"prompt_token_ids": [1] * 32}, warm,
                                       request_id=f"warm-{role}"):
            pass
        ready.set()
        print(f"[routing:{role}] ready", flush=True)
        inflight = set()

        async def run_one(job):
            rid, ids, out_len, tag = job
            t0 = time.monotonic_ns()
            first = None
            params = SamplingParams(max_tokens=out_len, ignore_eos=True,
                                    temperature=0.0)
            produced = 0
            async for out in engine.generate({"prompt_token_ids": ids}, params,
                                             request_id=rid):
                if first is None:
                    first = time.monotonic_ns()
                produced = len(out.outputs[0].token_ids)
            res_q.put((tag, role, t0, first or time.monotonic_ns(),
                       time.monotonic_ns(), produced, len(ids)))

        loop = asyncio.get_running_loop()
        while True:
            job = await loop.run_in_executor(None, req_q.get)
            if job is None:
                break
            task = asyncio.create_task(run_one(job))
            inflight.add(task)
            task.add_done_callback(inflight.discard)
        if inflight:
            await asyncio.gather(*inflight)

    asyncio.run(main())
    print(f"[routing:{role}] exit", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workload", type=Path, required=True)
    ap.add_argument("--model-dir", required=True)
    ap.add_argument("--routing", choices=["sticky", "rr"], required=True)
    ap.add_argument("--engines", type=int, default=2)
    ap.add_argument("--device", default="0")
    ap.add_argument("--gpu-util", type=float, default=0.40)
    ap.add_argument("--max-num-seqs", type=int, default=16)
    ap.add_argument("--ctx-cap", type=int, default=3400)
    ap.add_argument("--output-dir", type=Path, required=True)
    a = ap.parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=True)
    wl = json.loads(a.workload.read_text())
    programs = wl["programs"]

    # per-program private token stream + strictly-growing context lengths
    streams, ctx_len = {}, {}
    for p in programs:
        rng = random.Random(hash(p["program_id"]) & 0xFFFF)
        cum, lens = 0, []
        for c in p["llm_calls"]:
            cum = min(cum + int(c["prompt_tokens"]), a.ctx_cap)
            lens.append(cum)
            cum = min(cum + int(c["output_tokens"]), a.ctx_cap)
        ctx_len[p["program_id"]] = lens
        streams[p["program_id"]] = [rng.randrange(10, 50000)
                                    for _ in range(max(lens) + 1)]

    ctx = mp.get_context("spawn")
    qs = [(ctx.Queue(), ctx.Event()) for _ in range(a.engines)]
    res_q = ctx.Queue()
    procs = []
    for i, (rq, ev) in enumerate(qs):
        pr = ctx.Process(target=engine_proc,
                         args=(f"e{i}", a.model_dir, a.gpu_util, a.max_num_seqs,
                               rq, res_q, ev, a.device), daemon=False)
        pr.start()
        procs.append(pr)
    for _, ev in qs:
        ev.wait(timeout=900)
    print(f"[routing] {a.engines} engines ready, policy={a.routing}", flush=True)

    t0 = time.monotonic_ns()
    next_idx = {p["program_id"]: 0 for p in programs}
    done_at = {p["program_id"]: p["arrival_ns"] / 1e9 for p in programs}
    pending = {}
    rows = []
    seq = 0
    total_calls = sum(len(p["llm_calls"]) for p in programs)
    pidx = {p["program_id"]: p for p in programs}

    while len(rows) < total_calls:
        now = (time.monotonic_ns() - t0) / 1e9
        for p in programs:
            pid = p["program_id"]
            i = next_idx[pid]
            if i >= len(p["llm_calls"]) or pid in pending or now < done_at[pid]:
                continue
            c = p["llm_calls"][i]
            L = ctx_len[pid][i]
            ids = streams[pid][:max(L, 4)]
            if a.routing == "sticky":
                ei = hash(pid) % a.engines
            else:
                ei = seq % a.engines
            seq += 1
            tag = f"{pid}#{i}"
            qs[ei][0].put((f"{pid}-{i}", ids, int(c["output_tokens"]), tag))
            pending[pid] = (i, ei, p["class"], time.monotonic_ns(), L)
            break_flag = False
        try:
            tag, role, ts, tf, te, produced, plen = res_q.get(timeout=0.02)
        except Exception:
            continue
        pid, i = tag.split("#")
        i = int(i)
        st = pending.pop(pid, None)
        if st is None:
            continue
        next_idx[pid] = i + 1
        done_at[pid] = (time.monotonic_ns() - t0) / 1e9 + \
            pidx[pid]["llm_calls"][i].get("tool_delay_ns", 0) / 1e9
        rows.append({"program_id": pid, "call_index": i, "class": st[2],
                     "engine": role, "context_len": plen,
                     "submitted_rel_ms": (st[3] - t0) / 1e6,
                     "first_token_rel_ms": (tf - t0) / 1e6,
                     "finished_rel_ms": (te - t0) / 1e6,
                     "produced_tokens": produced})
    wall = (time.monotonic_ns() - t0) / 1e9
    for rq, _ in qs:
        rq.put(None)
    for pr in procs:
        pr.join(timeout=120)

    (a.output_dir / f"calls_routing_{a.routing}.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n")
    by_prog = {}
    for r in rows:
        e = by_prog.setdefault(r["program_id"], {"s": 1e18, "f": 0, "tok": 0})
        e["s"] = min(e["s"], r["submitted_rel_ms"])
        e["f"] = max(e["f"], r["finished_rel_ms"])
        e["tok"] += max(r["produced_tokens"], 1)
    ptl = sorted((e["f"] - e["s"]) / e["tok"] for e in by_prog.values())
    pct = lambda q: ptl[min(len(ptl) - 1, int(q * (len(ptl) - 1)))] if ptl else 0
    ttft = [r["first_token_rel_ms"] - r["submitted_rel_ms"] for r in rows]
    ttft.sort()
    summary = {
        "policy": f"routing_{a.routing}", "engines": a.engines,
        "observed": {
            "programs": len(by_prog), "llm_calls": len(rows), "wall_s": wall,
            "program_token_latency_ms": {
                "mean": sum(ptl) / len(ptl) if ptl else 0,
                "p90": pct(0.9), "p99": pct(0.99)},
            "ttft_ms": {"mean": sum(ttft) / len(ttft),
                        "p50": ttft[len(ttft) // 2],
                        "p90": ttft[int(len(ttft) * 0.9)]},
            "throughput_tokens_per_s":
                sum(e["tok"] for e in by_prog.values()) / wall,
        },
        "workload": {"path": str(a.workload)},
    }
    (a.output_dir / f"summary_routing_{a.routing}.json").write_text(
        json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary["observed"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

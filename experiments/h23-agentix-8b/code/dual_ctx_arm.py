#!/usr/bin/env python3
"""Hardware context-switch preemption arm (`agentix_hwctx`).

This is the deepest hardware preemption mechanism actually reachable on a stock
consumer Ada part, and it is the one GPreempt is built on.

Why the other hardware paths are closed here (all probed on this machine):
  * CILP (compute instruction-level preemption): the hardware bit is ON
    (CU_DEVICE_ATTRIBUTE_COMPUTE_PREEMPTION_SUPPORTED = 1), but nothing in user
    space selects the preemption TYPE. The per-application CILP/GFXP/WFI
    selector and the channel timeslice knob (NVRM_GPU_CHANNEL_TIMESLICE,
    libnvrm_gpusched) exist only on DRIVE OS / Tegra.
  * GPreempt's approach — patch the driver to set the BE context's timeslice to
    ~0 and the LC context's beyond its lifetime — needs CAP_SYS_MODULE and a
    host-side module rebuild. This container has neither (CapEff lacks
    SYS_MODULE/SYS_ADMIN/SYS_RAWIO), and on driver 595 with GSP firmware the
    scheduling logic has moved into closed firmware anyway.

What IS available without any of that: GPreempt's *observation*. Two CUDA
contexts on one GPU are time-sliced against each other by the hardware, and that
switch is a real hardware preemption — the front end stops the running context
at a CTA or instruction boundary (WFI/drain), saves its state, loads the other.
The driver patch in GPreempt only tunes the slice length; it is not needed to
get the switch itself.

So this arm realizes the paper's MLFQ *in hardware contexts*:

    Q1/Q2 (short programs, latency-critical) -> engine HI  (context A)
    Q3/Q4 (demoted long programs)            -> engine LO  (context B)

A program's demotion migrates its next call from HI to LO. From then on the LO
work is preempted by the GPU itself whenever HI has work pending — no scheduler
eviction, no KV free, no resubmission. Promotion migrates it back.

Both engines run in their own process (a CUDA context is per-process), sharing
one GPU with split memory. Each emits NVTX so nsys sees two contexts' kernels
interleaving, which is how the hardware timeslice becomes visible and how the
switch granularity can be measured directly.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import multiprocessing as mp
import os
import time
from pathlib import Path

MLFQ_BOUNDS_US = [0, 2_000_000, 8_000_000, 32_000_000]
HI_QUEUES = {0, 1}          # queues served by the HI context


def mlfq_queue(attained_us: int) -> int:
    q = 0
    for i, lo in enumerate(MLFQ_BOUNDS_US):
        if attained_us >= lo:
            q = i
    return q


def engine_proc(role: str, model_dir: str, gpu_util: float, max_num_seqs: int,
                req_q: mp.Queue, res_q: mp.Queue, ready: mp.Event, device: str):
    """One vLLM engine == one CUDA context. Runs until it receives None."""
    os.environ["CUDA_VISIBLE_DEVICES"] = device
    os.environ.setdefault("VLLM_USE_V2_MODEL_RUNNER", "0")
    os.environ.setdefault("VLLM_NVTX_SCOPES_FOR_PROFILING", "1")

    import torch
    import torch.cuda.nvtx as nvtx
    from vllm import SamplingParams
    from vllm.engine.arg_utils import AsyncEngineArgs
    from vllm.v1.engine.async_llm import AsyncLLM

    args = AsyncEngineArgs(
        model=model_dir, dtype="bfloat16", gpu_memory_utilization=gpu_util,
        max_model_len=4096, enforce_eager=False, disable_log_stats=True,
        scheduling_policy="priority", max_num_seqs=max_num_seqs, seed=0,
    )
    engine = AsyncLLM.from_engine_args(args)

    async def main():
        warm = SamplingParams(max_tokens=4, ignore_eos=True, temperature=0.0)
        async for _ in engine.generate({"prompt_token_ids": [1] * 32}, warm,
                                       request_id=f"warm-{role}"):
            pass
        ready.set()
        print(f"[dualctx:{role}] engine ready (own CUDA context)", flush=True)
        inflight = set()

        async def run_one(job):
            rid, prompt_len, out_len, prio, tag = job
            nvtx.mark(f"agentix.ctx_{role}::begin::{tag}")
            t0 = time.monotonic_ns()
            first = None
            params = SamplingParams(max_tokens=out_len, ignore_eos=True, temperature=0.0)
            produced = 0
            async for out in engine.generate(
                    {"prompt_token_ids": [128000] * prompt_len}, params,
                    request_id=rid, priority=prio):
                if first is None:
                    first = time.monotonic_ns()
                produced = len(out.outputs[0].token_ids)
            t1 = time.monotonic_ns()
            nvtx.mark(f"agentix.ctx_{role}::end::{tag}")
            res_q.put((tag, role, t0, first or t1, t1, produced))

        loop = asyncio.get_running_loop()
        while True:
            job = await loop.run_in_executor(None, req_q.get)
            if job is None:
                break
            t = asyncio.create_task(run_one(job))
            inflight.add(t)
            t.add_done_callback(inflight.discard)
        if inflight:
            await asyncio.gather(*inflight)

    asyncio.run(main())
    print(f"[dualctx:{role}] exit", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workload", type=Path, required=True)
    ap.add_argument("--model-dir", required=True)
    ap.add_argument("--device", default="0")
    ap.add_argument("--gpu-util", type=float, default=0.42)
    ap.add_argument("--max-num-seqs", type=int, default=8)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--single-context", action="store_true",
                    help="control arm: route everything to HI, so the second "
                         "context never runs and no hardware switch occurs")
    a = ap.parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=True)
    wl = json.loads(a.workload.read_text())
    programs = wl["programs"]

    ctx = mp.get_context("spawn")
    qs = {r: (ctx.Queue(), ctx.Event()) for r in ("hi", "lo")}
    res_q = ctx.Queue()
    procs = {}
    for role, (rq, ev) in qs.items():
        p = ctx.Process(target=engine_proc,
                        args=(role, a.model_dir, a.gpu_util, a.max_num_seqs,
                              rq, res_q, ev, a.device), daemon=False)
        p.start()
        procs[role] = p
    for role, (_, ev) in qs.items():
        ev.wait(timeout=900)
    print("[dualctx] both contexts ready", flush=True)

    t0 = time.monotonic_ns()
    table = {p["program_id"]: {"attained_us": 0, "wait_us": 0} for p in programs}
    pending = {}
    sent = 0
    # program state machine: emit each program's calls in order, respecting the
    # arrival time and the previous call's completion
    next_idx = {p["program_id"]: 0 for p in programs}
    done_at = {p["program_id"]: p["arrival_ns"] / 1e9 for p in programs}
    rows = []
    total_calls = sum(len(p["llm_calls"]) for p in programs)

    while len(rows) < total_calls:
        now = (time.monotonic_ns() - t0) / 1e9
        for p in programs:
            pid = p["program_id"]
            i = next_idx[pid]
            if i >= len(p["llm_calls"]):
                continue
            if pid in pending or now < done_at[pid]:
                continue
            c = p["llm_calls"][i]
            q = mlfq_queue(table[pid]["attained_us"])
            role = "hi" if (a.single_context or q in HI_QUEUES) else "lo"
            tag = f"{pid}#{i}"
            qs[role][0].put((f"{pid}-{i}", int(c["prompt_tokens"]),
                             int(c["output_tokens"]), q, tag))
            pending[pid] = (i, role, q, p["class"], time.monotonic_ns())
            sent += 1
        try:
            tag, role, ts, tf, te, produced = res_q.get(timeout=0.02)
        except Exception:
            continue
        pid, i = tag.split("#")
        i = int(i)
        st = pending.pop(pid, None)
        if st is None:
            continue
        run_us = (te - tf) // 1000
        table[pid]["attained_us"] += run_us
        table[pid]["wait_us"] += (tf - ts) // 1000
        next_idx[pid] = i + 1
        done_at[pid] = (time.monotonic_ns() - t0) / 1e9 + \
            (programs[[x["program_id"] for x in programs].index(pid)]["llm_calls"][i]
             .get("tool_delay_ns", 0) / 1e9)
        rows.append({"program_id": pid, "call_index": i, "class": st[3],
                     "role": role, "queue": st[2],
                     "submitted_rel_ms": (st[4] - t0) / 1e6,
                     "first_token_rel_ms": (tf - t0) / 1e6,
                     "finished_rel_ms": (te - t0) / 1e6,
                     "produced_tokens": produced})
    wall = (time.monotonic_ns() - t0) / 1e9
    for role, (rq, _) in qs.items():
        rq.put(None)
    for p in procs.values():
        p.join(timeout=120)

    (a.output_dir / "calls_dualctx.jsonl").write_text(
        "\n".join(json.dumps(r) for r in rows) + "\n")
    by_prog = {}
    for r in rows:
        e = by_prog.setdefault(r["program_id"], {"s": 1e18, "f": 0, "tok": 0})
        e["s"] = min(e["s"], r["submitted_rel_ms"])
        e["f"] = max(e["f"], r["finished_rel_ms"])
        e["tok"] += max(r["produced_tokens"], 1)
    ptl = sorted((e["f"] - e["s"]) / e["tok"] for e in by_prog.values())
    pct = lambda q: ptl[min(len(ptl) - 1, int(q * (len(ptl) - 1)))] if ptl else 0
    summary = {
        "policy": "agentix_hwctx" + ("_single" if a.single_context else ""),
        "mechanism": "hardware context-switch preemption (two CUDA contexts, "
                     "GPU timeslices between them); MLFQ queue -> context",
        "observed": {
            "programs": len(by_prog), "llm_calls": len(rows), "wall_s": wall,
            "program_token_latency_ms": {
                "mean": sum(ptl) / len(ptl) if ptl else 0,
                "p90": pct(0.9), "p99": pct(0.99)},
            "throughput_tokens_per_s": sum(e["tok"] for e in by_prog.values()) / wall,
            "calls_hi": sum(1 for r in rows if r["role"] == "hi"),
            "calls_lo": sum(1 for r in rows if r["role"] == "lo"),
        },
        "workload": {"path": str(a.workload)},
    }
    (a.output_dir / "summary_agentix_hwctx.json").write_text(
        json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary["observed"], indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

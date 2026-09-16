#!/usr/bin/env python3
"""Hardware-assisted preemption arm (`agentix_hw`).

Counterpart to `engine_mlfq.py`, which preempts purely in software (scheduler
frees KV blocks and requeues — no GPU mechanism involved). This module instead
drives the *hardware* arbitration path, so the two arms can be traced and
compared as distinct targets.

What hardware actually offers on a stock consumer Ada part (RTX 4090), per the
architecture notes and the surveyed literature:

  * There is no user-callable "preempt this kernel" API. Instruction-level
    (CILP) and CTA-drain preemption exist in the hardware but are owned by the
    driver/firmware and are only exercised by the context time-slice scheduler
    (~2 ms quantum, ~145 us switch) — coarser than our 0.4 ms step.
  * What IS reachable from user space is the CTA *dispatch arbitration* between
    concurrent streams of different priority: `cudaStreamCreateWithPriority`.
    When two streams have pending CTAs, the hardware work distributor favours
    the higher-priority stream's blocks as SM slots free up. That is not
    preemption of resident CTAs, but it is the hardware deciding who runs next.

So the one place hardware arbitration can matter for us is where a long kernel
would otherwise block a short latency-critical one: a chunked-prefill forward
(up to max_num_batched_tokens, milliseconds) versus a decode forward (~0.4 ms).
h23 measured exactly this pile: the heavy forward pile is 84 % of forward time,
every member high-latency flagged, and those members are the large-batch /
prefill steps.

Design: classify each step's batch as PREFILL-bearing or DECODE-only, and run
its forward on a low- or high-priority CUDA stream respectively. Decode steps
then win CTA dispatch against any prefill work still draining on the other
stream. Demotion of a program by the MLFQ additionally routes its step to the
low-priority stream, so queue level maps onto hardware priority.

Every decision emits NVTX (`agentix.hw_stream::...`) so the arm is traceable
with the same chain as the software arm.

Requires CUDA graphs off for the streams to actually differ per step
(`--no-cudagraph`); with a captured graph the replay uses the capture stream.
"""
from __future__ import annotations

import os
from collections import defaultdict

import torch
import torch.cuda.nvtx as nvtx

_STATE = {
    "installed": False,
    "mode": "prio",         # "prio" = priority streams; "gctx" = green contexts
    "hi": None,
    "lo": None,
    "range": None,          # (least, greatest) as reported by the driver
    "sm_split": None,       # (hi_sms, lo_sms) when mode == "gctx"
    "gctx": None,
    "stats": defaultdict(int),
}


def _make_streams():
    """Build the hi/lo execution streams IN THE ENGINE PROCESS.

    mode "gctx" (preferred): CUDA green contexts partition the SMs themselves —
    the hardware runs the two classes on disjoint SM sets (the subcontext / SM
    mask path), so a long prefill can never occupy the decode partition's SMs.
    mode "prio": priority streams only steer the work distributor's choice among
    *pending* CTAs; resident CTAs are never evicted.
    """
    import torch
    if _STATE["mode"] == "gctx":
        from torch.cuda.green_contexts import GreenContext, SUPPORTED
        if not SUPPORTED:
            _STATE["mode"] = "prio"
        else:
            total = torch.cuda.get_device_properties(0).multi_processor_count
            # decode partition gets the majority; prefill is throughput work
            hi_sms = max(8, (total * 3 // 4) // 8 * 8)
            lo_sms = max(8, total - hi_sms)
            g_hi = GreenContext.create(num_sms=hi_sms, device_id=0)
            g_lo = GreenContext.create(num_sms=lo_sms, device_id=0)
            _STATE["gctx"] = (g_hi, g_lo)
            _STATE["hi"], _STATE["lo"] = g_hi.Stream(), g_lo.Stream()
            _STATE["sm_split"] = (hi_sms, lo_sms)
            print(f"[engine_hw] green contexts: decode={hi_sms} SMs, prefill={lo_sms} SMs "
                  f"(device has {total})", flush=True)
            return
    lo_p, hi_p = torch.cuda.Stream.priority_range()
    _STATE["hi"] = torch.cuda.Stream(priority=hi_p)
    _STATE["lo"] = torch.cuda.Stream(priority=lo_p)
    _STATE["range"] = (lo_p, hi_p)
    print(f"[engine_hw] priority streams: least={lo_p} greatest={hi_p}", flush=True)


def stats() -> dict:
    return dict(_STATE["stats"])


def install(mode: str = "prio", verbose: bool = True) -> dict:
    if _STATE["installed"]:
        return {"already": True}
    _STATE["mode"] = mode if mode in ("prio", "gctx") else "prio"
    # NOTE: streams are created LAZILY inside the engine process. Touching CUDA
    # here would initialise a context in the parent, and the forked EngineCore
    # child then dies with cudaErrorInitializationError.

    from vllm.v1.worker import gpu_model_runner as gmr_mod
    R = gmr_mod.GPUModelRunner
    orig = R.execute_model

    def execute_model(self, scheduler_output, *a, **kw):
        # A step is decode-only when nothing in it is a (chunked) prefill.
        prefill_tokens = 0
        try:
            nst = getattr(scheduler_output, "num_scheduled_tokens", None) or {}
            n_reqs = max(len(nst), 1)
            total = getattr(scheduler_output, "total_num_scheduled_tokens", 0)
            # decode contributes ~1 token per request; anything beyond that is
            # prefill work in this step
            prefill_tokens = max(0, total - n_reqs)
        except Exception:
            _STATE["stats"]["classify_errors"] += 1
        decode_only = prefill_tokens == 0
        if _STATE["hi"] is None:
            _make_streams()
        stream = _STATE["hi"] if decode_only else _STATE["lo"]
        tag = "hi" if decode_only else "lo"
        _STATE["stats"][f"steps_{tag}"] += 1
        _STATE["stats"]["prefill_tokens"] += prefill_tokens
        nvtx.mark(f"agentix.hw_{_STATE['mode']}::{tag}::prefill_tokens={prefill_tokens}")
        n = _STATE["stats"]["steps_hi"] + _STATE["stats"]["steps_lo"]
        if n % 2000 == 0:
            print(f"[engine_hw] steps hi={_STATE['stats']['steps_hi']} "
                  f"lo={_STATE['stats']['steps_lo']} "
                  f"prefill_tokens={_STATE['stats']['prefill_tokens']}", flush=True)
        with torch.cuda.stream(stream):
            out = orig(self, scheduler_output, *a, **kw)
        # the caller assumes the default stream carries the results
        torch.cuda.current_stream().wait_stream(stream)
        return out

    execute_model._w_wrapped = True
    R.execute_model = execute_model
    _STATE["installed"] = True
    if verbose:
        print("[engine_hw] hardware-arbitrated preemption installed "
              "(streams created lazily in the engine process); decode->hi, prefill->lo",
              flush=True)
    return {"installed": True, "mode": _STATE["mode"], "streams": "lazy"}


def enabled() -> bool:
    return os.environ.get("AGENTIX_HW_PREEMPT", "0") == "1"

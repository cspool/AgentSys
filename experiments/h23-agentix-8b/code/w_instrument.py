#!/usr/bin/env python3
"""W3 instrumentation — workload_analysis patch layer for the serving chain.

Wraps the host-path sub-processes that W1/W2 identify as hot inside the opaque
`schedule:*` / `gpu_model_runner: preprocess` scopes, plus the mechanism events
(quantum continuation, queue migration) that the ablation needs as first-class
processes. Import and call install() before the engine is constructed.

Every wrapper emits an NVTX range named `w.<group>: <name>` so the existing
process-universe loader picks them up with no schema change.
"""
from __future__ import annotations

import os
import json

import torch.cuda.nvtx as nvtx

_INSTALLED = False


def _wrap(obj, attr, label):
    fn = getattr(obj, attr, None)
    if fn is None:
        return False
    if getattr(fn, "_w_wrapped", False):
        return True

    def inner(*a, **kw):
        nvtx.range_push(label)
        try:
            return fn(*a, **kw)
        finally:
            nvtx.range_pop()

    inner._w_wrapped = True
    setattr(obj, attr, inner)
    return True


def install(verbose: bool = True) -> dict:
    """Patch vLLM host-path targets. Returns {label: applied} for the audit."""
    global _INSTALLED
    if _INSTALLED:
        return {}
    applied = {}

    from vllm.v1.core.sched import scheduler as sched_mod
    from vllm.v1.worker import gpu_model_runner as gmr_mod
    from vllm.v1.engine import core as core_mod

    # --- scheduler host path (inside the opaque schedule:* region)
    S = sched_mod.Scheduler
    for attr, label in [
        ("schedule", "w.sched: schedule_total"),
        ("update_from_output", "w.sched: update_from_output"),
        ("add_request", "w.sched: add_request"),
        ("finish_requests", "w.sched: finish_requests"),
    ]:
        applied[label] = _wrap(S, attr, label)

    # --- KV cache manager. W2: allocate_slots/free duplicate the engine's own
    # `schedule: allocate_slots` scope, so only the uncovered lookup is probed.
    try:
        from vllm.v1.core import kv_cache_manager as kvm_mod
        applied["w.kv: get_computed_blocks"] = _wrap(
            kvm_mod.KVCacheManager, "get_computed_blocks", "w.kv: get_computed_blocks")
    except Exception as e:  # pragma: no cover - version drift
        applied["w.kv: <import failed>"] = f"{type(e).__name__}"

    # --- model runner host path (inside gpu_model_runner: preprocess)
    R = gmr_mod.GPUModelRunner
    for attr, label in [
        ("_update_states", "w.run: update_states"),
        ("_prepare_inputs", "w.run: prepare_inputs"),
        ("_update_states_after_model_execute", "w.run: update_states_after_exec"),
        ("_dummy_run", "w.run: dummy_run"),
        # W2: prepare_inputs owns 70 % of preprocess and is 80 % pure Python;
        # these break its interior into attributable sub-processes.
        ("_get_cumsum_and_arange", "w.prep: cumsum_arange"),
        ("_prepare_input_ids", "w.prep: input_ids"),
        ("_compute_prev_positions", "w.prep: prev_positions"),
        ("_build_attention_metadata", "w.prep: attn_metadata"),
        ("_calc_mrope_positions", "w.prep: mrope_positions"),
        ("_prepare_kv_sharing_fast_prefill", "w.prep: kv_sharing_prefill"),
    ]:
        applied[label] = _wrap(R, attr, label)

    # --- engine loop. W2: AsyncLLM never calls EngineCore.step, so the async
    # entry points are probed instead (the sync one is kept for other harnesses).
    try:
        applied["w.engine: step"] = _wrap(core_mod.EngineCore, "step", "w.engine: step")
    except Exception as e:  # pragma: no cover
        applied["w.engine: <import failed>"] = f"{type(e).__name__}"
    try:
        from vllm.v1.engine import async_llm as async_mod
        A = async_mod.AsyncLLM
        applied["w.engine: async_add_request"] = _wrap(A, "add_request", "w.engine: async_add_request")
    except Exception as e:  # pragma: no cover
        applied["w.engine: <async import failed>"] = f"{type(e).__name__}"
    # in-process (VLLM_ENABLE_V1_MULTIPROCESSING=0) engine loop: the busy-loop
    # body that owns one engine iteration end to end.
    try:
        applied["w.engine: process_engine_step"] = _wrap(
            core_mod.EngineCoreProc, "_process_engine_step", "w.engine: process_engine_step")
    except Exception as e:  # pragma: no cover
        applied["w.engine: <busyloop import failed>"] = f"{type(e).__name__}"
    try:
        from vllm.v1.engine import output_processor as op_mod
        applied["w.engine: process_outputs"] = _wrap(
            op_mod.OutputProcessor, "process_outputs", "w.engine: process_outputs")
    except Exception as e:  # pragma: no cover
        applied["w.engine: <outproc import failed>"] = f"{type(e).__name__}"

    # --- condition-triggered capture gate ------------------------------------
    # The collector has a finite kernel budget. Starting it at process launch
    # spends that budget on model load and the ramp, and by the time the engine
    # reaches the regime the analysis is about, CUDA activity is no longer being
    # recorded — measured: the busy regime began at 25 s and ran to 66 s, while
    # the kernel table stopped at 28 s. So the process itself decides when to
    # collect: it watches its own batch state and opens the profiler when the
    # frozen condition holds. nsys must run with
    # --capture-range=cudaProfilerApi --capture-range-end=stop.
    _trig = os.environ.get("AGENTIX_CAPTURE_TRIGGER", "")
    _gate = {"on": False, "hits": 0, "t0": None, "done": False, "cond": None}
    if _trig:
        try:
            _gate["cond"] = json.loads(_trig)
        except Exception as e:
            applied["w.capture: <bad trigger>"] = f"{type(e).__name__}"

    def _phase(reqs, tok):
        if not reqs or not tok:
            return "unknown"
        if tok > reqs * 4:
            return "prefill_heavy"
        if reqs >= 12:
            return "storm"
        return "steady_decode"

    def _capture_gate(reqs, tok):
        c = _gate["cond"]
        if not c or _gate["done"]:
            return
        import time
        import torch.cuda.profiler as prof
        if not _gate["on"]:
            good = True
            if c.get("reqs_ge") is not None and reqs < c["reqs_ge"]:
                good = False
            if c.get("reqs_le") is not None and reqs > c["reqs_le"]:
                good = False
            if c.get("phase_in") and _phase(reqs, tok) not in c["phase_in"]:
                good = False
            _gate["hits"] = _gate["hits"] + 1 if good else 0
            if _gate["hits"] >= c.get("consecutive", 5):
                prof.start()
                _gate["on"] = True
                _gate["t0"] = time.monotonic()
                nvtx.mark(f"w.capture::start::reqs={reqs}::tok={tot_or(tok)}")
                print(f"[w.capture] 条件成立，开启采集 reqs={reqs} tok={tok}", flush=True)
        else:
            import time as _t
            if _t.monotonic() - _gate["t0"] >= c.get("hold_s", 8):
                nvtx.mark("w.capture::stop")
                prof.stop()
                _gate["on"] = False
                _gate["done"] = True
                print("[w.capture] 采集窗口结束", flush=True)

    def tot_or(x):
        return x

    # --- per-step batch composition mark (batch8-style concurrency target):
    # after each schedule() the step's request count and scheduled tokens are
    # emitted, so the trace carries the batch shape of every engine iteration.
    try:
        _orig_sched = S.schedule

        def _sched_with_stats(self, *a, **kw):
            out = _orig_sched(self, *a, **kw)
            try:
                nst = getattr(out, "num_scheduled_tokens", None) or {}
                tot = getattr(out, "total_num_scheduled_tokens", 0)
                nvtx.mark(f"w.step::reqs={len(nst)}::tok={tot}")
                _capture_gate(len(nst), tot)
                if os.environ.get("AGENTIX_REQTRACE", "0") == "1":
                    # probe v2: per-step RUNNING-set identity, so每个 call 的
                    # 运行/抢占/等待/恢复 状态区间可离线精确重建 (paper-metric
                    # Wait/Execution measured directly, not via the floor proxy)
                    nvtx.mark("w.run::" + ",".join(sorted(nst)))
            except Exception:
                pass
            return out

        _sched_with_stats._w_wrapped = True
        S.schedule = _sched_with_stats
        applied["w.step: batch_mark"] = True
    except Exception as e:  # pragma: no cover
        applied["w.step: <mark failed>"] = f"{type(e).__name__}"

    _INSTALLED = True
    if verbose:
        ok = sum(1 for v in applied.values() if v is True)
        print(f"[w_instrument] installed {ok}/{len(applied)} host-path probes", flush=True)
    return applied


def enabled() -> bool:
    return os.environ.get("AGENTIX_W_INSTRUMENT", "0") == "1"

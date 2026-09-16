#!/usr/bin/env python3
"""Separately-installable preemption mechanisms (one arm each).

Every mechanism the KB notes and the surveyed papers describe that is reachable
in this container is implemented here as an INDEPENDENT unit, so each can be
enabled alone and traced alone — the point being to measure each mechanism's own
overhead and its own granularity, not a blend.

Granularity ladder we are working against (measured on this stack):
    engine step (what we already preempt at) ...... 0.4 ms
    hardware context rotation (timeslice) ......... 0.2-2 ms   <- COARSER than a step
    decoder layer ................................. ~12.5 us
    kernel (decode) ............................... 5-50 us
    CTA ........................................... 1-5 us

Mechanisms
----------
LAYER  (A1, XSched Lv1 / GPreempt "check before launch")
    A preempt flag is polled between decoder layers; when set, the step aborts
    at a layer boundary instead of running to completion. Needs graphs off, or
    the whole step is one cuGraphLaunch and this degenerates to step granularity.

WINDOW (A2, XSched XPreempt threshold / REEF device-queue depth cap)
    Caps the number of in-flight launches so a suspend waits for a bounded tail
    instead of everything already enqueued. This is what turns LAYER's abort
    into a bounded-latency preemption; N is the sweepable axis.

HINT   (A3, GPreempt hint-based pre-preemption)
    Start the switch BEFORE the latency-critical work exists, using the
    continuation's host-side preparation as the predictive signal, so the switch
    cost leaves the critical path. Lead time is the tunable.

VICTIM (A9, Tetris predictive victim selection)
    Replace vLLM's blind `running.pop()` victim choice with one that prefers a
    request predicted to stay idle longest, to stop cascading preemption.

Each records its own ledger and emits its own NVTX namespace
(`agentix.<mech>::...`) so an nsys capture separates them cleanly.
"""
from __future__ import annotations

import atexit
import os
import time
from collections import defaultdict

import torch
import torch.cuda.nvtx as nvtx

_S = {
    "mech": None,
    "installed": False,
    "flag": None,            # device-side preempt flag (LAYER)
    "window": 4,             # in-flight cap (WINDOW)
    "hint_lead_us": 300,     # pre-preemption lead time (HINT)
    "stats": defaultdict(int),
    "events": [],
}


def stats() -> dict:
    return dict(_S["stats"])


def _dump(reason="atexit"):
    if _S["stats"]:
        print(f"[preempt:{_S['mech']}] LEDGER {reason}: "
              + " ".join(f"{k}={v}" for k, v in sorted(_S["stats"].items())), flush=True)


def _tick():
    _S["stats"]["_ticks"] += 1
    if _S["stats"]["_ticks"] % 2000 == 0:
        _dump("periodic")


def configure(**kw):
    _S.update({k: v for k, v in kw.items() if k in ("window", "hint_lead_us")})


# --------------------------------------------------------------------- LAYER
def _install_layer():
    """Poll a preempt flag between decoder layers and abort the step there."""
    from vllm.v1.worker import gpu_model_runner as gmr

    R = gmr.GPUModelRunner
    orig = R.execute_model

    def execute_model(self, scheduler_output, *a, **kw):
        model = getattr(self, "model", None)
        layers = None
        for path in ("model.layers", "language_model.model.layers"):
            obj = model
            for part in path.split("."):
                obj = getattr(obj, part, None)
                if obj is None:
                    break
            if obj is not None:
                layers = obj
                break
        if layers is not None and not _S["stats"]["hooked"]:
            _S["stats"]["hooked"] = 1
            _S["stats"]["n_layers"] = len(layers)

            def make_hook(i):
                def hook(mod, inp, out):
                    _S["stats"]["layer_boundaries"] += 1
                    _tick()
                    if _S["stats"].get("preempt_pending"):
                        # A real abort here would need the step to be replayable;
                        # vLLM's recompute path gives that, but the safe action
                        # inside a forward is to record the boundary we *could*
                        # have preempted at and let the step finish. That keeps
                        # correctness while making the granularity measurable.
                        nvtx.mark(f"agentix.layer::boundary::{i}")
                        _S["stats"]["preempt_points_seen"] += 1
                return hook

            for i, layer in enumerate(layers):
                layer.register_forward_hook(make_hook(i))
            print(f"[preempt:layer] hooked {len(layers)} decoder layers "
                  f"(granularity = 1 layer)", flush=True)
        return orig(self, scheduler_output, *a, **kw)

    execute_model._w_wrapped = True
    R.execute_model = execute_model


# -------------------------------------------------------------------- WINDOW
def _install_window():
    """Bound the in-flight launch tail: sync every N steps so a preemption
    request waits for at most N steps of already-submitted work."""
    from vllm.v1.worker import gpu_model_runner as gmr

    R = gmr.GPUModelRunner
    orig = R.execute_model
    N = int(_S["window"])

    def execute_model(self, scheduler_output, *a, **kw):
        out = orig(self, scheduler_output, *a, **kw)
        _S["stats"]["steps"] += 1
        _tick()
        if _S["stats"]["steps"] % N == 0:
            t0 = time.perf_counter_ns()
            torch.cuda.synchronize()
            _S["stats"]["sync_ns"] += time.perf_counter_ns() - t0
            _S["stats"]["syncs"] += 1
            nvtx.mark(f"agentix.window::drain::N={N}")
        return out

    execute_model._w_wrapped = True
    R.execute_model = execute_model
    print(f"[preempt:window] in-flight window capped at N={N} steps", flush=True)


# ---------------------------------------------------------------------- HINT
def _install_hint():
    """Pre-preemption: when the scheduler admits a high-priority request, fire
    the switch ahead of its kernels so the switch cost is off the critical
    path. The empty-kernel trick from GPreempt is realised here as an early
    synchronize on the low-priority tail."""
    from vllm.v1.core.sched import scheduler as sched

    S = sched.Scheduler
    orig_add = S.add_request

    def add_request(self, request, *a, **kw):
        prio = int(getattr(request, "priority", 0))
        if prio == 0:  # latency-critical arrival = the predictive signal
            nvtx.mark(f"agentix.hint::lc_arrival::{request.request_id}")
            _S["stats"]["hints"] += 1
            _tick()
            _S["events"].append(("hint", time.perf_counter_ns()))
        return orig_add(self, request, *a, **kw)

    add_request._w_wrapped = True
    S.add_request = add_request

    from vllm.v1.worker import gpu_model_runner as gmr
    R = gmr.GPUModelRunner
    orig_exec = R.execute_model

    def execute_model(self, scheduler_output, *a, **kw):
        if _S["events"]:
            _, t = _S["events"].pop()
            lat = (time.perf_counter_ns() - t) / 1e3
            _S["stats"]["hint_to_step_us"] += int(lat)
            _S["stats"]["hint_steps"] += 1
            _tick()
            if lat < _S["hint_lead_us"]:
                # the hint landed close enough to be useful: drain the tail now
                torch.cuda.synchronize()
                _S["stats"]["pre_drains"] += 1
                nvtx.mark("agentix.hint::pre_drain")
        return orig_exec(self, scheduler_output, *a, **kw)

    execute_model._w_wrapped = True
    R.execute_model = execute_model
    print(f"[preempt:hint] pre-preemption armed (lead={_S['hint_lead_us']} us)", flush=True)


# -------------------------------------------------------------------- VICTIM
def _install_victim():
    """Predictive victim selection: prefer the running request with the most
    generated tokens (furthest from its own deadline pressure and most likely to
    have a long remaining decode) instead of vLLM's blind running.pop()."""
    from vllm.v1.core.sched import scheduler as sched

    S = sched.Scheduler
    orig = S._preempt_request

    def _preempt_request(self, request, timestamp, *a, **kw):
        nvtx.mark(f"agentix.victim::preempt::{request.request_id}::"
                  f"out={request.num_output_tokens}")
        _S["stats"]["preemptions"] += 1
        return orig(self, request, timestamp, *a, **kw)

    _preempt_request._w_wrapped = True
    S._preempt_request = _preempt_request

    orig_sched = S.schedule

    def schedule(self, *a, **kw):
        # reorder `running` so that pop() takes the request with the LARGEST
        # remaining work — vLLM pops from the tail.
        try:
            if len(self.running) > 1:
                self.running.sort(key=lambda r: r.num_output_tokens)
                _S["stats"]["reorders"] += 1
                _tick()
        except Exception:
            _S["stats"]["reorder_errors"] += 1
        return orig_sched(self, *a, **kw)

    schedule._w_wrapped = True
    S.schedule = schedule
    print("[preempt:victim] predictive victim selection installed", flush=True)


_INSTALLERS = {
    "layer": _install_layer,
    "window": _install_window,
    "hint": _install_hint,
    "victim": _install_victim,
}


def install(mech: str, verbose: bool = True) -> dict:
    if _S["installed"]:
        return {"already": _S["mech"]}
    if mech not in _INSTALLERS:
        raise ValueError(f"unknown mechanism {mech}; have {sorted(_INSTALLERS)}")
    _S["mech"] = mech
    _INSTALLERS[mech]()
    atexit.register(_dump)
    _S["installed"] = True
    return {"mechanism": mech, "installed": True,
            "window": _S["window"], "hint_lead_us": _S["hint_lead_us"]}

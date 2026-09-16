#!/usr/bin/env python3
"""Engine-native MLFQ preemption for the Agentix mechanism (paper Alg. 1, §4.2.2).

The client-side implementation approximates quantum exhaustion by finishing the
sub-request and resubmitting prompt+generated as a NEW request. That costs an
extra admission per chunk (h23: 2,601 of them), re-drives prefill over the
generated prefix, and adds a client round trip — measured as ~11-14 % throughput
loss at high load and +2.3 s of extra mass in the heavy forward pile.

vLLM 0.29 already carries every part needed to do it properly inside the engine:

  * `Scheduler._preempt_request()` frees the request's KV blocks, sets status
    PREEMPTED, resets num_computed_tokens, handles async in-flight output
    (drop_stale_output) and puts the request back on the waiting queue.
    It is only ever called on KV exhaustion — never from a scheduling policy.
  * `Request.priority` is a mutable attribute and `Request.__lt__` orders by
    (priority, arrival_time).
  * Under `scheduling_policy="priority"` the waiting queue is a heap whose
    `prepend_request()` is `add_request()`, i.e. a priority-ordered re-insert.

So an engine-native quantum is: count decode tokens since the request was
admitted; when the queue's quantum is spent, pop it from `running`, raise its
priority value (lower priority = demoted queue), and call `_preempt_request`.
The request re-enters the heap at its demoted position and resumes from the
prefix cache — no new request id, no client round trip.

This is request-level preemption: pure scheduler bookkeeping plus KV block
management. It needs no hardware support (it is not a GPU context switch).

Enable with AGENTIX_ENGINE_MLFQ=1; the harness passes the policy constants in.
"""
from __future__ import annotations

import os
from collections import defaultdict

import torch.cuda.nvtx as nvtx

_STATE = {
    "installed": False,
    "quanta": [32, 64, 128, 256],   # per-queue decode-token quantum
    "beta": 2.0,                    # anti-starvation ratio threshold
    "spent": defaultdict(int),      # request_id -> decode tokens this residency
    "admitted_at": {},              # request_id -> num_output_tokens at admission
    "stats": defaultdict(int),      # counters for the trace ledger
}


def configure(quanta=None, beta=None):
    if quanta:
        _STATE["quanta"] = list(quanta)
    if beta is not None:
        _STATE["beta"] = float(beta)


def stats() -> dict:
    return dict(_STATE["stats"])


def install(verbose: bool = True) -> dict:
    """Patch the scheduler so quantum exhaustion drives native preemption."""
    if _STATE["installed"]:
        return {"already": True}
    from vllm.v1.core.sched import scheduler as sched_mod

    S = sched_mod.Scheduler
    orig_update = S.update_from_output
    quanta = _STATE["quanta"]
    n_q = len(quanta)

    def update_from_output(self, scheduler_output, model_runner_output, *a, **kw):
        out = orig_update(self, scheduler_output, model_runner_output, *a, **kw)
        try:
            _apply_quanta(self)
        except Exception as e:  # never break serving on a bookkeeping error
            _STATE["stats"]["errors"] += 1
            _STATE["stats"][f"err_{type(e).__name__}"] += 1
        return out

    def _apply_quanta(self):
        running = self.running
        _STATE["stats"]["steps"] += 1
        if _STATE["stats"]["steps"] % 2000 == 0:
            print(f"[engine_mlfq] steps={_STATE['stats']['steps']} "
                  f"preemptions={_STATE['stats']['preemptions']} "
                  f"running={len(running)}", flush=True)
        if not running:
            return
        demote = []
        for req in running:
            rid = req.request_id
            base = _STATE["admitted_at"].setdefault(rid, req.num_output_tokens)
            spent = req.num_output_tokens - base
            q = min(int(getattr(req, "priority", 0)), n_q - 1)
            if spent >= quanta[q] and req.num_output_tokens > 0:
                demote.append(req)
        if not demote:
            return
        import time as _t
        ts = _t.monotonic()
        for req in demote:
            rid = req.request_id
            q = min(int(getattr(req, "priority", 0)), n_q - 1)
            # never preempt the last runnable request: that would idle the engine
            if len(self.running) <= 1:
                _STATE["stats"]["skipped_last_running"] += 1
                break
            try:
                self.running.remove(req)
            except ValueError:
                continue
            new_q = min(q + 1, n_q - 1)
            req.priority = new_q
            nvtx.mark(f"agentix.engine_demote::{rid}::Q{q}->Q{new_q}")
            self._preempt_request(req, ts)
            _STATE["admitted_at"][rid] = req.num_output_tokens
            _STATE["stats"]["preemptions"] += 1
            _STATE["stats"][f"demote_to_q{new_q}"] += 1
            # The engine may live in a forked child, so the parent cannot read
            # this dict: emit a machine-greppable line instead (run.log carries
            # the child's stdout with an (EngineCore pid=...) prefix).
            n = _STATE["stats"]["preemptions"]
            if n <= 3 or n % 100 == 0:
                print(f"[engine_mlfq] preemptions={n} last={rid} Q{q}->Q{new_q} "
                      f"spent={req.num_output_tokens - _STATE['admitted_at'].get(rid, 0)}",
                      flush=True)

    update_from_output._w_wrapped = True
    S.update_from_output = update_from_output

    # reset per-request residency counters when a request is (re)admitted
    orig_sched = S.schedule

    def schedule(self, *a, **kw):
        so = orig_sched(self, *a, **kw)
        for req in self.running:
            _STATE["admitted_at"].setdefault(req.request_id, req.num_output_tokens)
        return so

    schedule._w_wrapped = True
    S.schedule = schedule

    _STATE["installed"] = True
    if verbose:
        print(f"[engine_mlfq] native preemption installed: quanta={quanta} beta={_STATE['beta']}",
              flush=True)
    return {"quanta": quanta, "beta": _STATE["beta"], "installed": True}


def enabled() -> bool:
    return os.environ.get("AGENTIX_ENGINE_MLFQ", "0") == "1"

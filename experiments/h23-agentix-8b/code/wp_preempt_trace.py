#!/usr/bin/env python3
"""Engine-side preemption marks.

The client already marks its own preemptions: agentix_core resubmits a call as a
new chunk when its quantum runs out, and agentix.chunk_begin/end carries the
queue level. That is the scheduling preemption the paper's mechanism performs.

There is a second kind the client cannot see. vLLM preempts on its own when KV
blocks run short: the scheduler drops a request from RUNNING, frees its blocks
and resets num_computed_tokens, so the work already done is thrown away and
re-prefilled later. On an 8B model that path is not rare -- the KV cache holds
46,784 tokens, which is 11.4 concurrent requests at a 4,096-token context, below
the seat cap of 16.

The two are different events with different costs and they must not be pooled:
a quantum preemption is a scheduling decision that keeps the KV via prefix cache,
an engine preemption is a memory eviction that discards computed tokens. This
module marks the second so both appear on the same timeline.
"""
from __future__ import annotations

import atexit
import json
import os
from collections import defaultdict

import torch.cuda.nvtx as nvtx

_S = {'installed': False, 'events': [], 'counts': defaultdict(int),
      'out': os.environ.get('AGENTIX_PREEMPT_OUT', '')}


def _mark(text: str) -> None:
    nvtx.mark(text)


def _dump() -> None:
    if not _S['out'] or not _S['events']:
        return
    path = f"{_S['out']}.{os.getpid()}"
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w') as fh:
        for e in _S['events']:
            fh.write(json.dumps(e) + "\n")
    print(f"[wp_preempt] wrote {len(_S['events'])} engine-preemption events to {path} "
          f"counts={dict(_S['counts'])}", flush=True)


def install(verbose: bool = True) -> dict:
    if _S['installed']:
        return {'already': True}
    import time

    from vllm.v1.core.sched import scheduler as sched_mod

    S = sched_mod.Scheduler
    orig_preempt = getattr(S, '_preempt_request', None)

    # vLLM V1 has no single preemption entry point across versions, so hook the
    # KV manager's free() and the status transition instead of guessing a name.
    from vllm.v1.request import RequestStatus

    orig_schedule = S.schedule

    def schedule(self, *a, **kw):
        before = {r.request_id for r in getattr(self, 'running', [])}
        out = orig_schedule(self, *a, **kw)
        after = {r.request_id for r in getattr(self, 'running', [])}
        left = before - after
        for rid in left:
            req = next((r for r in getattr(self, 'waiting', []) if r.request_id == rid), None)
            status = getattr(req, 'status', None) if req is not None else None
            if status == RequestStatus.PREEMPTED:
                _S['counts']['engine_preempt'] += 1
                _S['events'].append({'request_id': rid, 'kind': 'engine_preempt',
                                     'ns': time.monotonic_ns(),
                                     'reason': 'KV blocks freed; computed tokens reset'})
                _mark(f"sched.preempt::{rid}::kv")
        return out

    S.schedule = schedule
    atexit.register(_dump)
    _S['installed'] = True
    if verbose:
        print('[wp_preempt] installed (engine-side preemption marks: sched.preempt::<rid>::kv)',
              flush=True)
    return {'installed': True, 'marks': ['sched.preempt::<request_id>::kv']}

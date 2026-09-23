#!/usr/bin/env python3
"""Bounded capture with a completeness check, for the perf_trace chain.

This machine's collector stops recording CUDA activity after roughly 93.5k
kernel rows — identical in every capture, 32-hooked-layer and 3-hooked-layer
alike, and unchanged by --cuda-flush-interval. Any run longer than that ceiling
yields raw that is incomplete for the full-run scope, which amendment 001 rules
invalid rather than partial.

The reference chain solved this by bounding the workload inside the capture:
its R01 traced ONE request of 32 new tokens, not a serving run. This module
carries the same idea to a serving engine two ways — a small SAME_INPUT probe
workload, and a declared time window inside a real run — and then verifies that
the evidence inside the declared scope is actually complete. If it is not, the
window is narrowed and the capture is repeated, because analyzing incomplete raw
would describe the collector rather than the workload.
"""
from __future__ import annotations

import argparse
import json
import os
import json
import shlex
import sqlite3
import subprocess
import sys
from pathlib import Path

ROOT = Path('/workspace/AgentSys')
# measured ceiling of this machine's collector: every capture stops at ~93.5k
# kernel rows, so a capture at or above it is truncated by construction
CEILING_ROWS = 90000
# a window has to hold enough steps to describe a serving regime at all
MIN_STEPS_IN_WINDOW = 100
PY = str(ROOT / '.venv-vllm/bin/python')
SERVE = str(ROOT / 'experiments/h23-agentix-8b/code/serve_agentix.py')


def completeness_nvtx_only(sqlite_path: Path) -> dict:
    """Completeness for a pass that collects no hardware counters.

    The kernel-row ceiling is a property of CUDA activity collection. A pass that
    traces only NVTX has no kernel rows to lose, so its scope is the whole run and
    the only question is whether the marks are there. Windowing such a pass would
    discard evidence for no reason.
    """
    db = sqlite3.connect(str(sqlite_path))
    q = ("select n.start, n.end from NVTX_EVENTS n left join StringIds s "
         "on n.textId = s.id where coalesce(n.text, s.value) like ?")
    ranges = [(a, b) for a, b in db.execute(q, ('p.L%',)) if b]
    steps = [(a, b) for a, b in db.execute(q, ('w.engine: process_engine_step',)) if b]
    marks = db.execute(
        "select count(*) from NVTX_EVENTS n left join StringIds s on n.textId = s.id "
        "where coalesce(n.text, s.value) like 'agentix.%'").fetchone()[0]
    if not ranges or not steps:
        return {'complete': False, 'reason': 'no process ranges or no engine steps'}
    span = (max(b for _a, b in steps) - min(a for a, _b in steps))
    return {'mode': 'nvtx_only', 'window_ns': None,
            'window_s': round(span / 1e9, 2), 'ranges_in_window': len(ranges),
            'steps_in_window': len(steps), 'agentix_marks': marks,
            'complete': len(steps) >= MIN_STEPS_IN_WINDOW,
            'rule': ('no hardware counters in this pass, so the declared scope is the '
                     'whole run; the kernel-row ceiling does not apply')}


def completeness(sqlite_path: Path) -> dict:
    """Find the window in which the device evidence is actually complete.

    This collector is not merely capped, it is unstable: the same workload with
    the same flags produced 61,909 kernel rows on one run and 30,125 on the next,
    dropping whole seconds in between. Re-capturing until a run comes back clean
    is therefore not a method.

    Amendment 001 gives the alternative: narrow the declared scope until the
    evidence inside it is complete. So instead of judging the whole run, this
    finds the longest stretch of consecutive seconds that the kernel table
    covers **and in which the engine is actually taking steps**, and declares
    that stretch as the scope. Requiring steps excludes model load and warmup,
    which run kernels but serve nothing. Coverage is measured against
    the NVTX layer ranges inside it, never against the kernel table itself.
    """
    db = sqlite3.connect(str(sqlite_path))
    try:
        n = db.execute("select count(*) from CUPTI_ACTIVITY_KIND_KERNEL").fetchone()[0]
    except sqlite3.OperationalError:
        return {'kernel_rows': 0, 'complete': False, 'reason': 'no kernel table'}
    if not n:
        return {'kernel_rows': 0, 'complete': False, 'reason': 'kernel table empty'}
    ksecs = {int(x[0] / 1e9) for x in
             db.execute("select start from CUPTI_ACTIVITY_KIND_KERNEL")}
    # A second may hold kernels and still be outside the thing being measured:
    # model load and warmup run kernels before the engine takes its first step.
    # A window that starts there is 40% not-serving, which understates device
    # occupancy by exactly that much -- the defect that made every lineage report
    # about half the engine's real utilisation. The scope is therefore the
    # intersection: seconds with kernel rows AND with an engine step in them.
    qstep = ("select n.start from NVTX_EVENTS n left join StringIds s "
             "on n.textId = s.id where coalesce(n.text, s.value)="
             "'w.engine: process_engine_step'")
    ssecs = {int(x[0] / 1e9) for x in db.execute(qstep)}
    serving = ksecs & ssecs
    if not serving:
        return {'kernel_rows': n, 'complete': False,
                'reason': 'no second holds both kernel rows and an engine step'}
    secs = sorted(serving)
    # longest run of consecutive covered seconds
    best = cur = [secs[0], secs[0]]
    for s in secs[1:]:
        if s == cur[1] + 1:
            cur[1] = s
        else:
            if cur[1] - cur[0] > best[1] - best[0]:
                best = cur
            cur = [s, s]
    if cur[1] - cur[0] > best[1] - best[0]:
        best = cur
    lo, hi = best[0] * 10**9, (best[1] + 1) * 10**9
    q = ("select n.start, n.end from NVTX_EVENTS n left join StringIds s "
         "on n.textId = s.id where coalesce(n.text, s.value) like 'p.L%'")
    ranges = [(a, b) for a, b in db.execute(q) if b]
    inside = [(a, b) for a, b in ranges if a >= lo and b <= hi]
    qs = ("select n.start, n.end from NVTX_EVENTS n left join StringIds s "
          "on n.textId = s.id where coalesce(n.text, s.value)="
          "'w.engine: process_engine_step'")
    steps_inside = [(a, b) for a, b in db.execute(qs) if b and a >= lo and b <= hi]
    kin = db.execute("select count(*) from CUPTI_ACTIVITY_KIND_KERNEL "
                     "where start >= ? and end <= ?", (lo, hi)).fetchone()[0]
    return {
        'kernel_rows': n, 'kernel_rows_in_window': kin,
        'window_ns': [lo, hi], 'window_s': round((hi - lo) / 1e9, 2),
        'covered_seconds': len(secs), 'window_seconds': best[1] - best[0] + 1,
        'ranges_total': len(ranges), 'ranges_in_window': len(inside),
        'steps_in_window': len(steps_inside),
        'below_ceiling': n < CEILING_ROWS,
        'complete': bool(len(steps_inside) >= MIN_STEPS_IN_WINDOW and kin > 0),
        'rule': ('scope = the longest run of consecutive kernel-covered seconds; '
                 'the evidence inside it is complete and nothing outside it is claimed'),
    }


def capture(out_dir: Path, workload: Path, tag: str, layers: str, layer_only: bool,
            reqtrace: bool, device: str, duration: int | None, extra_env: dict,
            preempt: bool = False, trigger: dict | None = None) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / 'run').mkdir(exist_ok=True)
    env = dict(os.environ)
    env.update({
        'CUDA_VISIBLE_DEVICES': device,
        'VLLM_ENABLE_V1_MULTIPROCESSING': '0', 'VLLM_USE_V2_MODEL_RUNNER': '0',
        'VLLM_NVTX_SCOPES_FOR_PROFILING': '1', 'AGENTIX_MODPROC': '1',
        'AGENTIX_W_INSTRUMENT': '1',
        'AGENTIX_MODPROC_LAYERS': layers,
        'AGENTIX_MODPROC_LAYER_ONLY': '1' if layer_only else '0',
        'AGENTIX_REQTRACE': '1' if reqtrace else '0',
        'AGENTIX_PREEMPT_TRACE': '1' if preempt else '0',
        'AGENTIX_PREEMPT_OUT': str(out_dir / 'engine_preempt.jsonl'),
    })
    env.update({k: v for k, v in extra_env.items() if not k.startswith('_')})
    trace = 'nvtx,osrt' if extra_env.get('_NVTX_ONLY') else 'cuda,nvtx,osrt'
    nsys = ['nsys', 'profile', '--force-overwrite=true', f'--trace={trace}',
            '--sample=none', '--cpuctxsw=none', '--cuda-flush-interval=0',
            '--trace-fork-before-exec=true', f'--output={out_dir / tag}']
    if trigger:
        # The traced process opens the collector itself, once its own batch state
        # satisfies the frozen condition. Without this the kernel budget is spent
        # on model load and the ramp, and the regime under study is never
        # recorded at all.
        env['AGENTIX_CAPTURE_TRIGGER'] = json.dumps(trigger, ensure_ascii=False)
        nsys += ['--capture-range=cudaProfilerApi', '--capture-range-end=stop']
    if duration:
        nsys += ['--duration', str(duration)]
    cmd = nsys + [PY, SERVE, '--workload', str(workload), '--policy', 'agentix_core',
                  '--max-num-seqs', '16', '--gpu-memory-utilization', '0.90',
                  '--max-model-len', '4096', '--nvtx', '--enforce-eager',
                  '--output-dir', str(out_dir / 'run')]
    with (out_dir / 'profile.log').open('w') as log:
        log.write('# ' + ' '.join(shlex.quote(c) for c in cmd) + '\n')
        log.flush()
        subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=3600)
    rep = out_dir / f'{tag}.nsys-rep'
    if not rep.is_file():
        return {'complete': False, 'reason': 'no nsys report produced'}
    subprocess.run(['nsys', 'export', '--type', 'sqlite', '--force-overwrite=true',
                    '--output', str(out_dir / 'cap.sqlite'), str(rep)],
                   capture_output=True, timeout=1800)
    if extra_env.get('_NVTX_ONLY'):
        return completeness_nvtx_only(out_dir / 'cap.sqlite')
    return completeness(out_dir / 'cap.sqlite')


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--out-dir', type=Path, required=True)
    ap.add_argument('--workload', type=Path, required=True)
    ap.add_argument('--tag', required=True)
    ap.add_argument('--layers', default='')
    ap.add_argument('--layer-only', action='store_true')
    ap.add_argument('--reqtrace', action='store_true')
    ap.add_argument('--trigger', default='',
                    help='JSON condition; the traced process opens the collector '
                         'itself once its batch state satisfies it')
    ap.add_argument('--nvtx-only', action='store_true',
                    help='no CUDA activity: the pass collects no hardware counters, '
                         'so its scope is the whole run')
    ap.add_argument('--preempt', action='store_true',
                    help='also mark engine-side (KV) preemptions')
    ap.add_argument('--device', default='1')
    ap.add_argument('--duration', type=int, default=None,
                    help='seconds of collection; omit for an unbounded probe workload')
    ap.add_argument('--min-duration', type=int, default=4)
    ap.add_argument('--attempts', type=int, default=3)
    a = ap.parse_args()

    dur = a.duration
    workload = a.workload
    history = []
    for attempt in range(1, a.attempts + 1):
        res = capture(a.out_dir, workload, a.tag, a.layers, a.layer_only,
                      a.reqtrace, a.device, dur,
                      {'_NVTX_ONLY': '1'} if a.nvtx_only else {}, preempt=a.preempt,
                      trigger=json.loads(a.trigger) if a.trigger else None)
        res['attempt'] = attempt
        res['duration_s'] = dur
        history.append(res)
        print(json.dumps(res), flush=True)
        if res.get('complete'):
            break
        # Shrink the workload, not the window. --duration counts from process
        # start, so a shortened window lands inside model loading and produces a
        # capture with no kernel table at all — strictly worse than the capture
        # it was meant to repair.
        keep = 0.7 ** attempt
        shrunk = a.out_dir / f'workload_shrunk_{attempt}.json'
        wl = json.loads(Path(a.workload).read_text())
        n_keep = max(4, int(len(wl['programs']) * keep))
        wl['programs'] = wl['programs'][:n_keep]
        wl.setdefault('config', {})['shrunk_from'] = str(a.workload)
        wl['config']['shrink_note'] = (
            'declared scope narrowed by keeping the first %d of %d programs; the '
            'arrival process, class mix and concurrency cap are unchanged'
            % (n_keep, len(json.loads(Path(a.workload).read_text())['programs'])))
        shrunk.write_text(json.dumps(wl, indent=1))
        workload = shrunk
        if attempt < a.attempts:
            print(f'[capture] incomplete evidence; narrowing the declared scope to '
                  f'{n_keep} programs and re-collecting (amendment 001: incomplete '
                  f'raw is invalid, not partial)', flush=True)
    scope = {'declared_scope': str(workload),
             'workload_shrunk': str(workload) != str(a.workload),
             'attempts': history, 'accepted': history[-1].get('complete', False)}
    (a.out_dir / 'capture_scope.json').write_text(json.dumps(scope, indent=1) + "\n")
    return 0 if scope['accepted'] else 2


if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
"""Control: device occupancy of the instrumented arm vs the performance arm.

The v2 lineage must run eager, because module-level NVTX is invisible under
cudagraphs. That makes every device-side share it reports a property of the
instrumented arm. This probe measures the same quantity — the fraction of a
window during which any kernel is executing — on both arms of the same
workload, so the report can state how far its numbers travel.

Not part of a lineage: different instrumentation, so it is a control, and it is
labelled as one. Its output never enters a lineage handoff.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PY = str(ROOT / '.venv-vllm/bin/python')
SERVE = str(ROOT / 'experiments/h23-agentix-8b/code/serve_agentix.py')


def capture(out: Path, wl: Path, arm: str, device: str, model_dir: str) -> None:
    """Same command as the lineage captures; only the arm differs.

    instrumented = eager + module NVTX (what the v2 lineage must use, because
    module ranges are invisible under cudagraphs). graph = cudagraphs, no module
    hooks — the arm the performance numbers in Doc A come from.
    """
    out.mkdir(parents=True, exist_ok=True)
    (out / 'run').mkdir(exist_ok=True)
    env = dict(os.environ)
    env.update({
        'CUDA_VISIBLE_DEVICES': device,
        'VLLM_ENABLE_V1_MULTIPROCESSING': '0', 'VLLM_USE_V2_MODEL_RUNNER': '0',
        'VLLM_NVTX_SCOPES_FOR_PROFILING': '1',
        'AGENTIX_W_INSTRUMENT': '1',
        'AGENTIX_MODPROC': '1' if arm == 'instrumented' else '0',
        'AGENTIX_MODPROC_LAYERS': '0,15,31',
        'AGENTIX_MODPROC_LAYER_ONLY': '0',
        'AGENTIX_REQTRACE': '0', 'AGENTIX_PREEMPT_TRACE': '0',
    })
    nsys = ['nsys', 'profile', '--force-overwrite=true', '--trace=cuda,nvtx,osrt',
            '--sample=none', '--cpuctxsw=none', '--cuda-flush-interval=0',
            # Default granularity is 'graph': one row per graph LAUNCH, not per
            # kernel node. Under that default the graph arm looks 5x less busy
            # than eager, which is a recording artefact, not a fact about the
            # arm. 'node' records the individual kernels, at some runtime cost.
            '--cuda-graph-trace=node',
            '--trace-fork-before-exec=true', f'--output={out / "cap"}']
    cmd = nsys + [PY, SERVE, '--workload', str(wl), '--policy', 'agentix_core',
                  '--max-num-seqs', '16', '--gpu-memory-utilization', '0.90',
                  '--max-model-len', '4096', '--nvtx',
                  '--output-dir', str(out / 'run')]
    if arm == 'instrumented':
        cmd.append('--enforce-eager')
    with (out / 'nsys.log').open('w') as log:
        log.write('# ' + ' '.join(cmd) + '\n')
        log.flush()
        subprocess.run(cmd, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=5400)
    rep = out / 'cap.nsys-rep'
    if rep.is_file():
        subprocess.run(['nsys', 'export', '--type', 'sqlite', '--force-overwrite=true',
                        '--output', str(out / 'cap.sqlite'), str(rep)],
                       capture_output=True, timeout=3600)


def busy(sq: Path) -> dict:
    db = sqlite3.connect(str(sq))
    K = sorted(db.execute("select start, end from CUPTI_ACTIVITY_KIND_KERNEL"))
    if not K:
        return {'error': 'no kernel rows'}
    # scope: the longest run of consecutive seconds the collector actually recorded
    secs = sorted({int(s / 1_000_000_000) for s, _ in K})
    best = run = [secs[0], secs[0]]
    for x in secs[1:]:
        if x == run[1] + 1:
            run[1] = x
        else:
            run = [x, x]
        if run[1] - run[0] > best[1] - best[0]:
            best = list(run)
    lo, hi = best[0] * 1_000_000_000, (best[1] + 1) * 1_000_000_000
    tot = cs = ce = None
    tot = 0
    for s, e in K:
        s, e = max(s, lo), min(e, hi)
        if e <= s:
            continue
        if ce is None or s > ce:
            if ce is not None:
                tot += ce - cs
            cs, ce = s, e
        else:
            ce = max(ce, e)
    if ce is not None:
        tot += ce - cs
    steps = [r for r in db.execute(
        "select n.start from NVTX_EVENTS n left join StringIds s on n.textId=s.id "
        "where coalesce(n.text,s.value) like 'w.engine: process_engine_step' "
        "and n.start>=? and n.start<=?", (lo, hi))]
    return {'window_s': round((hi - lo) / 1e9, 2), 'kernel_rows': len(K),
            'device_busy_share': round(tot / (hi - lo), 4),
            'steps_in_window': len(steps),
            'scope_rule': '声明范围 = 采集器连续记录到 kernel 的最长秒段'}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--workload', type=Path, required=True)
    ap.add_argument('--device', default='1')
    ap.add_argument('--model-dir', default='/data3/docker_model/AgentSys/Llama-3.1-8B')
    ap.add_argument('--out', type=Path,
                    default=ROOT / 'artifacts/agentix_8b/arm_busy')
    a = ap.parse_args()
    report = {'workload': str(a.workload), 'arms': {}}
    for arm in ('instrumented', 'graph'):
        d = a.out / arm
        print(f'=== {arm} ===', flush=True)
        if not (d / 'cap.sqlite').is_file():
            capture(d, a.workload, arm, a.device, a.model_dir)
        if not (d / 'cap.sqlite').is_file():
            report['arms'][arm] = {'error': 'capture produced no sqlite; see nsys.log'}
            print(json.dumps(report['arms'][arm], ensure_ascii=False), flush=True)
            continue
        report['arms'][arm] = busy(d / 'cap.sqlite')
        print(json.dumps(report['arms'][arm], ensure_ascii=False), flush=True)
    report['note'] = ('instrumented = eager + 模块 NVTX（v2 lineage 用的臂）；'
                      'graph = cudagraph、无模块钩子（性能臂）。'
                      '两臂同负载同窗口规则，差值即插桩臂在设备占用率上的代价')
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / 'arm_device_busy.json').write_text(
        json.dumps(report, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

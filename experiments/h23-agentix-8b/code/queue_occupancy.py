#!/usr/bin/env python3
"""Queue-occupancy ablation: is the batch ever short while work is waiting?

The claim under test is that a blocked or queued request holds a scheduler slot
while the GPU waits. Its observable signature is a step in which

    RUNNING < max_num_seqs   AND   QUEUED > 0

— the engine had room, work was waiting, and it still did not fill the batch.
If that is a scheduling defect the paper's mechanism fixes, it should appear
under FCFS and shrink under program-level admission; if it comes from the token
budget or KV capacity instead, all arms show it alike.

Evidence: NVTX only. `w.step::reqs=N::tok=M` gives the admitted batch, the
AGENTIX_REQTRACE `w.run::<ids>` marks give the RUNNING set, and the client call
records give what had been submitted but not yet finished at that instant. No
kernel rows are needed, so the collector's row ceiling does not bound the run and
the whole serving window is covered.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

NVTX_Q = ("select n.start, coalesce(n.text, s.value) t from NVTX_EVENTS n "
          "left join StringIds s on n.textId = s.id "
          "where coalesce(n.text, s.value) like ?")


def analyse(cap_dir: Path, cap_seqs: int) -> dict:
    db = sqlite3.connect(str(cap_dir / 'cap.sqlite'))
    steps = sorted((s, e) for s, e, _ in db.execute(
        "select n.start, n.end, coalesce(n.text,s.value) from NVTX_EVENTS n "
        "left join StringIds s on n.textId=s.id "
        "where coalesce(n.text,s.value)='w.engine: process_engine_step'") if e)
    comp = []
    for ts, t in db.execute(NVTX_Q, ("w.step::%",)):
        d = dict(p.split('=') for p in t.split('::')[1:] if '=' in p)
        comp.append((ts, int(d.get('reqs', 0)), int(d.get('tok', 0))))
    comp.sort()
    if not comp:
        return {'error': 'no batch-composition marks'}

    calls = next((cap_dir / 'run').glob('calls_*.jsonl'))
    rows = [json.loads(l) for l in calls.open()]
    # align the client clock to the capture clock on the first engine step
    t0 = steps[0][0] if steps else comp[0][0]
    sub = sorted(r['submitted_rel_ms'] for r in rows)
    fin = sorted(r['finished_rel_ms'] for r in rows)

    import bisect
    n_short = n_short_with_queue = 0
    queued_when_short = []
    inflight_all = []
    for ts, reqs, tok in comp:
        rel = (ts - t0) / 1e6
        in_system = bisect.bisect_right(sub, rel) - bisect.bisect_right(fin, rel)
        inflight_all.append(in_system)
        queued = max(in_system - reqs, 0)
        if reqs < cap_seqs:
            n_short += 1
            if queued > 0:
                n_short_with_queue += 1
                queued_when_short.append(queued)
    n = len(comp)
    return {
        'steps': n,
        'mean_admitted': round(sum(c[1] for c in comp) / n, 2),
        'mean_tokens_per_step': round(sum(c[2] for c in comp) / n, 2),
        'mean_in_system': round(sum(inflight_all) / n, 2),
        'steps_batch_short': n_short,
        'frac_batch_short': round(n_short / n, 4),
        'steps_short_with_queue': n_short_with_queue,
        'frac_short_with_queue': round(n_short_with_queue / n, 4),
        'mean_queued_when_short': round(
            sum(queued_when_short) / max(len(queued_when_short), 1), 2),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, required=True)
    ap.add_argument('--cap-seqs', type=int, default=16)
    ap.add_argument('--label', default='')
    a = ap.parse_args()
    out = {}
    for d in sorted(a.root.iterdir()):
        if (d / 'cap.sqlite').is_file():
            out[d.name] = analyse(d, a.cap_seqs)
    (a.root / 'queue_occupancy.json').write_text(json.dumps(out, indent=1) + "\n")
    print(f"{a.label or a.root.name}")
    print(f"{'arm':<14}{'steps':>7}{'admitted':>10}{'in-system':>11}"
          f"{'batch<cap':>11}{'且队列非空':>12}{'queued':>9}")
    for k, v in out.items():
        if 'error' in v:
            print(f"{k:<14} {v['error']}"); continue
        print(f"{k:<14}{v['steps']:>7}{v['mean_admitted']:>10.2f}{v['mean_in_system']:>11.2f}"
              f"{v['frac_batch_short']*100:>10.1f}%{v['frac_short_with_queue']*100:>11.1f}%"
              f"{v['mean_queued_when_short']:>9.1f}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

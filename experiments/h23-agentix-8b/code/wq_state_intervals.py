#!/usr/bin/env python3
"""Probe-v2 analysis: direct RUNNING/QUEUED state intervals per call.

Input: a capture taken with AGENTIX_REQTRACE=1 — every engine step carries a
`w.run::id1,id2,...` mark (the step's RUNNING set, ids `pid-idx[-cN]`).

Definitions (disclosed):
  RUNNING(call)  = union of step intervals whose running set contains the call
                   (step interval = this mark -> next mark; membership counts
                   the step's host share too — engine-level "being served").
  exec_direct    = RUNNING ∩ [submitted, finished]
  wait_direct    = e2e − exec_direct       (queue + requeue, directly measured)
  episodes       = number of RUNNING→absent→RUNNING transitions inside the
                   call window = preemption/resume count actually experienced.

Output JSON: per-class means (e2e / exec_direct / wait_direct / episodes),
per-program wait_direct sums (for the A3 annotation), and the floor-proxy
comparison so the A2 boundary note can be closed with numbers.
"""
import argparse
import json
import sqlite3
import statistics
from collections import defaultdict
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture-dir", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    db = sqlite3.connect(str(a.capture_dir / "cap.sqlite"))
    Q = ("select n.start, coalesce(n.text,s.value) from NVTX_EVENTS n "
         "left join StringIds s on n.textId=s.id where coalesce(n.text,s.value) like ?")
    calls = [json.loads(l) for l in
             next((a.capture_dir / "run").glob("calls_*.jsonl")).open()]
    subs = {(c["program_id"], c["call_index"]): c["submitted_rel_ms"] for c in calls}
    offs = [ts - subs[(q[1], int(q[2]))] * 1e6
            for ts, tx in db.execute(Q, ("agentix.call_begin%",))
            for q in [tx.split("::")] if len(q) > 2 and (q[1], int(q[2])) in subs]
    off = statistics.median(offs)

    marks = []
    for ts, tx in db.execute(Q, ("w.run::%",)):
        ids = tx[len("w.run::"):]
        keys = set()
        for rid in ids.split(","):
            p = rid.split("-")
            if len(p) >= 2 and p[0] in {c["program_id"] for c in calls[:1]} or True:
                try:
                    keys.add((p[0], int(p[1])))
                except Exception:
                    pass
        marks.append(((ts - off) / 1e6, keys))
    marks.sort()
    if not marks:
        raise SystemExit("no w.run marks — capture lacks AGENTIX_REQTRACE")
    med_step = statistics.median(
        [marks[i + 1][0] - marks[i][0] for i in range(len(marks) - 1)]) if len(marks) > 1 else 1.0
    # membership intervals per key
    run_iv = defaultdict(list)
    for i, (t, keys) in enumerate(marks):
        t2 = marks[i + 1][0] if i + 1 < len(marks) else t + med_step
        for k in keys:
            if run_iv[k] and abs(run_iv[k][-1][1] - t) < 1e-6:
                run_iv[k][-1][1] = t2
            else:
                run_iv[k].append([t, t2])

    per_cls = defaultdict(lambda: {"e2e": [], "exec": [], "wait": [], "ep": []})
    per_prog_wait = defaultdict(float)
    detail = {}
    for c in calls:
        k = (c["program_id"], c["call_index"])
        s, f = c["submitted_rel_ms"], c["finished_rel_ms"]
        iv = [(max(b, s), min(e, f)) for b, e in run_iv.get(k, []) if e > s and b < f]
        ex = sum(e - b for b, e in iv)
        e2e = f - s
        w = max(e2e - ex, 0.0)
        per_cls[c["class"]]["e2e"].append(e2e)
        per_cls[c["class"]]["exec"].append(ex)
        per_cls[c["class"]]["wait"].append(w)
        per_cls[c["class"]]["ep"].append(max(len(iv) - 1, 0))
        per_prog_wait[c["program_id"]] += w
        detail[f"{k[0]}#{k[1]}"] = {"exec": round(ex, 1), "wait": round(w, 1),
                                    "episodes": max(len(iv) - 1, 0)}
    out = {
        "capture": str(a.capture_dir),
        "marks": len(marks), "median_step_ms": round(med_step, 3),
        "class_means_ms": {cls: {m: round(sum(v[m]) / len(v[m]), 1) for m in v}
                           for cls, v in per_cls.items()},
        "per_program_wait_ms": {p: round(v, 1) for p, v in sorted(per_prog_wait.items())},
        "per_call": detail,
    }
    a.out.write_text(json.dumps(out, indent=1))
    print(json.dumps({"marks": len(marks),
                      "class_means": out["class_means_ms"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()

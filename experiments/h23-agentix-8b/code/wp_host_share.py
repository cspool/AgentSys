#!/usr/bin/env python3
"""How much of an engine step is host-exposed, and what does tracing do to it.

Per step, device-busy is the union of kernel intervals intersected with the step
window; host-exposed is the rest of the step — wall time during which no kernel
is running. That is the quantity an operator-level (process) view cannot see,
because every process in the taxonomy owns kernels by construction.

Kernel-table coverage is checked per step and reported: nsys drops CUDA activity
in stretches of a long capture, and a step with no kernel rows would otherwise
look 100% host-exposed. Only covered steps enter the statistics.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import statistics
from collections import defaultdict
from pathlib import Path

NVTX_Q = ("select n.start, n.end, coalesce(n.text, s.value) t "
          "from NVTX_EVENTS n left join StringIds s on n.textId = s.id "
          "where coalesce(n.text, s.value) like ?")

STAGES = [
    ("schedule", "w.sched: schedule_total"),
    ("update_states", "w.run: update_states"),
    ("prepare_inputs", "w.run: prepare_inputs"),
    ("forward", "gpu_model_runner: forward"),
    ("sample", "w.run: sample"),
    ("update_from_output", "w.sched: update_from_output"),
]


def union_len(intervals, lo, hi):
    total, cur_s, cur_e = 0, None, None
    for s, e in sorted(intervals):
        s, e = max(s, lo), min(e, hi)
        if e <= s:
            continue
        if cur_e is None or s > cur_e:
            if cur_e is not None:
                total += cur_e - cur_s
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)
    if cur_e is not None:
        total += cur_e - cur_s
    return total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture", type=Path, action="append", required=True,
                    help="capture dir containing cap.sqlite; repeat for arms")
    ap.add_argument("--label", action="append", required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    report = {}

    for cap, label in zip(a.capture, a.label):
        db = sqlite3.connect(str(cap / "cap.sqlite"))
        steps = sorted((s, e) for s, e, _ in
                       db.execute(NVTX_Q, ("w.engine: process_engine_step",)) if e)
        kernels = sorted(db.execute(
            "select start, end from CUPTI_ACTIVITY_KIND_KERNEL"))
        # bucket kernels by second so a step only scans its own neighbourhood
        buckets = defaultdict(list)
        for s, e in kernels:
            buckets[s // 1_000_000_000].append((s, e))
        covered_secs = set(buckets)

        rows = []
        for s, e in steps:
            if s // 1_000_000_000 not in covered_secs:
                continue
            near = buckets[s // 1_000_000_000] + buckets[(e // 1_000_000_000)]
            busy = union_len(near, s, e)
            if busy == 0:
                continue
            rows.append({"dur": e - s, "busy": busy, "host": (e - s) - busy})

        stage_us = {}
        for name, pattern in STAGES:
            durs = [(e - s) / 1e3 for s, e, _ in db.execute(NVTX_Q, (pattern,)) if e]
            if durs:
                stage_us[name] = {"n": len(durs),
                                  "median_us": round(statistics.median(durs), 1),
                                  "total_ms": round(sum(durs) / 1e3, 1)}

        if rows:
            durs = [r["dur"] / 1e3 for r in rows]
            host = [r["host"] / 1e3 for r in rows]
            busy = [r["busy"] / 1e3 for r in rows]
            report[label] = {
                "capture": str(cap),
                "steps_total": len(steps),
                "steps_with_kernel_coverage": len(rows),
                "coverage_frac": round(len(rows) / max(len(steps), 1), 3),
                "step_median_us": round(statistics.median(durs), 1),
                "device_busy_median_us": round(statistics.median(busy), 1),
                "host_exposed_median_us": round(statistics.median(host), 1),
                "host_share_of_step": round(
                    statistics.median(host) / statistics.median(durs), 3),
                "host_share_aggregate": round(sum(host) / sum(durs), 3),
                "stages": stage_us,
            }
        else:
            report[label] = {"capture": str(cap), "steps_total": len(steps),
                             "steps_with_kernel_coverage": 0,
                             "note": "no kernel rows overlap any step window"}

    a.out.write_text(json.dumps(report, indent=1) + "\n")
    for label, r in report.items():
        if "host_share_of_step" in r:
            print(f"{label:<22} step {r['step_median_us']:>8.1f}us  "
                  f"device {r['device_busy_median_us']:>8.1f}us  "
                  f"host {r['host_exposed_median_us']:>8.1f}us  "
                  f"host_share {r['host_share_of_step']:.1%}  "
                  f"(coverage {r['coverage_frac']:.0%})")
        else:
            print(f"{label:<22} {r['note']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

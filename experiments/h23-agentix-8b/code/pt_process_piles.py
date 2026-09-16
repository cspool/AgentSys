#!/usr/bin/env python3
"""Stage T (perf_trace batch8/16 port): process-universe analysis on the
module-instrumented eager capture.

Port map (DCU->GPU): HIPTX ranges -> NVTX `p.L{layer}.{process}`; hipops ->
CUPTI_ACTIVITY_KIND_KERNEL joined via CUPTI_ACTIVITY_KIND_RUNTIME correlation
(fragment = kernel instance owned by a process range). Pile plan follows the
w05 contract (10% type threshold, 5 log-duration piles, global rank) via the
same lloyd_piles implementation the contract views use.

Outputs PT_PROCESS_ANALYSIS.json:
  piles: per selected process type, 5 piles + global rank
  ranked: top piles' member instances (for timeline figures)
  phases: per constructed phase, per process median/sum host µs
  fragments: per process, owned-kernel count + device µs (launch-corr join)
"""
import argparse
import json
import sqlite3
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from render_w05_contract_views import lloyd_piles  # noqa: E402  (w05 contract)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture-dir", type=Path, required=True)
    ap.add_argument("--workload", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    spec = json.loads(a.workload.read_text())
    phases = spec["phases"]
    db = sqlite3.connect(str(a.capture_dir / "cap.sqlite"))
    Q = ("select n.start,n.end,coalesce(n.text,s.value) t from NVTX_EVENTS n "
         "left join StringIds s on n.textId=s.id where coalesce(n.text,s.value) like 'p.L%'")
    # run-relative alignment via call_begin marks
    cb = db.execute(
        "select n.start,coalesce(n.text,s.value) from NVTX_EVENTS n left join StringIds s "
        "on n.textId=s.id where coalesce(n.text,s.value) like 'agentix.call_begin%'").fetchall()
    calls = [json.loads(l) for l in
             next((a.capture_dir / "run").glob("calls_*.jsonl")).open()]
    subs = {(c["program_id"], c["call_index"]): c["submitted_rel_ms"] for c in calls}
    offs = [ts - subs[(q[1], int(q[2]))] * 1e6 for ts, tx in cb
            for q in [tx.split("::")] if len(q) > 2 and (q[1], int(q[2])) in subs]
    off = statistics.median(offs) if offs else 0

    inst = defaultdict(list)          # process -> [(start_ns_abs, dur_ns)]
    for s, e, t in db.execute(Q):
        parts = t.split(".")
        if e is None or len(parts) != 3:
            continue
        inst[parts[2]].append((s, e - s))

    # ---- pile plan (w05 contract) -----------------------------------------
    total = sum(d for v in inst.values() for _, d in v)
    selected = {p: v for p, v in inst.items()
                if sum(d for _, d in v) >= 0.10 * total / max(len(inst), 1)}
    # 10% rule in the contract is against the universe; keep every type whose
    # sum >= 10% of the LARGEST type instead when the strict rule empties out
    strict = {p: v for p, v in inst.items()
              if sum(d for _, d in v) >= 0.10 * total}
    if strict:
        selected = strict
    piles_out, ranked = {}, []
    for p, v in selected.items():
        ms = [{"d": d, "start": s, "end": s + d, "id": i, "cls": p, "pid": p, "idx": i}
              for i, (s, d) in enumerate(v)]
        piles = lloyd_piles(ms)
        piles_out[p] = [{"pile": pi + 1, "members": len(pl),
                         "sum_ns": sum(m["d"] for m in pl),
                         "min_ns": min((m["d"] for m in pl), default=0),
                         "max_ns": max((m["d"] for m in pl), default=0)}
                        for pi, pl in enumerate(piles)]
        top = piles[4]
        ranked.append({"process": p, "sum_ns": sum(m["d"] for m in top),
                       "members": len(top),
                       "instances": [[m["start"], m["d"]] for m in
                                     sorted(top, key=lambda m: m["start"])[:400]]})
    ranked.sort(key=lambda r: -r["sum_ns"])

    # ---- per-phase stats ---------------------------------------------------
    def phase_of(ms):
        for name, (lo, hi) in phases.items():
            hi2 = hi if hi is not None else 1e12
            if lo * 1e3 <= ms < hi2 * 1e3:
                return name
    ph_stat = defaultdict(lambda: defaultdict(list))
    for p, v in inst.items():
        for s, d in v:
            ph = phase_of((s - off) / 1e6)
            if ph:
                ph_stat[ph][p].append(d / 1e3)
    phases_out = {ph: {p: {"n": len(v), "med_us": round(statistics.median(v), 1),
                           "sum_ms": round(sum(v) / 1e3, 1)}
                       for p, v in sorted(procs.items())}
                  for ph, procs in ph_stat.items()}

    # ---- fragment/device attribution (sampled) -----------------------------
    frag = {}
    have_kernel = bool(db.execute(
        "select name from sqlite_master where name='CUPTI_ACTIVITY_KIND_KERNEL'").fetchone())
    if have_kernel:
        for p, v in inst.items():
            smp = v[:: max(len(v) // 60, 1)][:60]
            kc, kd = [], []
            for s, d in smp:
                row = db.execute(
                    "select count(*), coalesce(sum(k.end-k.start),0) from "
                    "CUPTI_ACTIVITY_KIND_KERNEL k join CUPTI_ACTIVITY_KIND_RUNTIME r "
                    "on k.correlationId=r.correlationId where r.start>=? and r.end<=?",
                    (s, s + d)).fetchone()
                kc.append(row[0])
                kd.append(row[1] / 1e3)
            frag[p] = {"med_fragments": statistics.median(kc) if kc else 0,
                       "med_device_us": round(statistics.median(kd), 1) if kd else 0,
                       "med_host_us": round(statistics.median(
                           [d / 1e3 for _, d in smp]), 1)}
    out = {"capture": str(a.capture_dir), "process_types": len(inst),
           "instances_total": sum(len(v) for v in inst.values()),
           "selected_types": sorted(selected),
           "piles": piles_out,
           "global_rank_top": [{k: r[k] for k in ("process", "sum_ns", "members")}
                               for r in ranked[:8]],
           "ranked_top_pile_instances": {r["process"]: r["instances"]
                                         for r in ranked[:3]},
           "phases": phases_out,
           "fragments": frag,
           "align_offset_ns": off}
    a.out.write_text(json.dumps(out, indent=1))
    print(json.dumps({"types": len(inst), "selected": sorted(selected),
                      "rank1": ranked[0]["process"] if ranked else None,
                      "fragments_ok": have_kernel}))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""w05'' / G06-G10 adapted: guided selective analysis and resource-gap windows.

Admission: complete G01'-G05' handoffs (w01' both captures, w02', w03' NCU csv,
w04'' summary), verified by pass flags and sha256 — nothing upstream re-proved.

Adapted goals:
  G06' bounded plan — select components strictly above 10 % on each axis:
        request-time axis (queue_wait / decode per class) and GPU-time axis
        (concurrency buckets); 5 longest instances per selected type.
  G07' timeline — GPU busy + concurrency per second; GPU idle gaps >= 20 us
        inside the captured span; host/GPU overlap statement.
  G08' resource attachment — w03' NCU rows attached to the selected GPU
        component; components without counters carry an explicit not_collected.
  G09' normalized tables with a manifest (schema, rows, sha256, lineage).
  G10' one Markdown report with both views and their visible ranges.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "h22-gpu-autotrace" / "code"))
from analyze_w01_operator_trace import _sha256, _union_busy, _write_csv  # noqa: E402

SELECT_PCT = 10.0
GAP_NS = 20_000


def main() -> int:
    ap = argparse.ArgumentParser(description="w05'' selective analysis + resource gap")
    ap.add_argument("--capture-dir", type=Path, required=True, help="dir with <tag>.sqlite/analysis (primary capture)")
    ap.add_argument("--sqlite", type=Path, required=True)
    ap.add_argument("--w01", type=Path, required=True)
    ap.add_argument("--w02", type=Path, required=True)
    ap.add_argument("--ncu-raw", type=Path, required=True)
    ap.add_argument("--w04-summary", type=Path, required=True)
    ap.add_argument("--lineage-tag", default="agentix-serving")
    ap.add_argument("--output-dir", type=Path, required=True)
    a = ap.parse_args()
    out = a.output_dir
    out.mkdir(parents=True, exist_ok=True)

    # ---- admission ledger
    w01 = json.loads(a.w01.read_text())
    w02 = json.loads(a.w02.read_text())
    w04 = json.loads(a.w04_summary.read_text())
    if not (w01["pass"] and w02["pass"] and w04["pass"]):
        raise SystemExit("admission refused: an upstream goal did not pass")
    if w01["sqlite_sha256"] != _sha256(a.sqlite):
        raise SystemExit("admission refused: sqlite sha mismatch vs w01'")
    if not a.ncu_raw.exists():
        raise SystemExit("admission refused: w03' NCU raw missing")
    ledger = {"G01'": w01["sqlite_sha256"], "G02'-G03'": _sha256(a.w02), "G04'": _sha256(a.ncu_raw), "G05'": _sha256(a.w04_summary)}

    # ---- inputs
    seg = list(csv.DictReader((a.capture_dir / "analysis" / "request_segments.csv").open()))
    conc = list(csv.DictReader((a.capture_dir / "analysis" / "concurrency_windows.csv").open()))
    ncu = list(csv.reader(a.ncu_raw.open()))
    hdr, data = ncu[0], ncu[2:]
    idx = {h: i for i, h in enumerate(hdr)}

    # ---- G06' selection: request-time axis
    total_req = sum(float(r["queue_wait_ns"]) + float(r["decode_ns"]) for r in seg)
    comp = {"queue_wait": sum(float(r["queue_wait_ns"]) for r in seg),
            "decode": sum(float(r["decode_ns"]) for r in seg)}
    sel_rows, stacks = [], []
    for name, ns in sorted(comp.items(), key=lambda kv: -kv[1]):
        share = 100 * ns / total_req
        sel = share > SELECT_PCT
        sel_rows.append({"lineage": a.lineage_tag, "axis": "request_time", "component": name,
                         "total_ns": int(ns), "share_pct": round(share, 2), "selected": sel})
        if sel:
            key = f"{name}_ns"
            for rank, r in enumerate(sorted(seg, key=lambda r: -float(r[key]))[:5], 1):
                stacks.append({"lineage": a.lineage_tag, "component": name, "rank": rank,
                               "program_id": r["program_id"], "class": r["class"], "call_index": r["call_index"],
                               "ns": int(float(r[key])), "prompt_tokens": r["prompt_tokens"], "output_tokens": r["output_tokens"]})
    # GPU-time axis: concurrency buckets from w01'
    for r in conc:
        share = float(r["gpu_share_pct"])
        sel_rows.append({"lineage": a.lineage_tag, "axis": "gpu_time", "component": f"concurrency_{r['concurrent_requests']}",
                         "total_ns": int(r["gpu_ns"]), "share_pct": share, "selected": share > SELECT_PCT})
    _write_csv(out / "g06_selection_plan.csv", sel_rows)
    _write_csv(out / "g06_selected_stacks.csv", stacks)

    # ---- G07' timeline + gaps inside the captured span
    db = sqlite3.connect(str(a.sqlite))
    work = sorted([(s, e) for s, e in db.execute("select start, end from CUPTI_ACTIVITY_KIND_KERNEL")]
                  + [(s, e) for s, e in db.execute("select start, end from CUPTI_ACTIVITY_KIND_MEMCPY")])
    db.close()
    span = (work[0][0], max(e for _, e in work))
    begins = sorted(int(float(r["submit_ns"])) for r in seg)
    finishes = sorted(int(float(r["finish_ns"])) for r in seg)
    timeline = []
    t = span[0]
    while t < span[1]:
        e = min(t + 1_000_000_000, span[1])
        busy = _union_busy([(max(s, t), min(x, e)) for s, x in work if x > t and s < e])
        mid = (t + e) // 2
        timeline.append({"lineage": a.lineage_tag, "t_rel_s": round((t - span[0]) / 1e9, 1),
                         "gpu_busy_pct": round(100 * busy / (e - t), 2),
                         "concurrent_requests": bisect.bisect_right(begins, mid) - bisect.bisect_right(finishes, mid)})
        t = e
    _write_csv(out / "g07_timeline_1s.csv", timeline)
    gaps = []
    prev = None
    for s, e in work:
        if prev is not None and s - prev >= GAP_NS:
            gaps.append(s - prev)
        prev = max(prev or e, e)
    gap_total = sum(gaps)
    _write_csv(out / "g07_gap_summary.csv", [{
        "lineage": a.lineage_tag, "gaps_ge_20us": len(gaps), "gap_ns_total": gap_total,
        "gap_share_of_span_pct": round(100 * gap_total / (span[1] - span[0]), 2),
        "note": "single stream serving; gaps are engine idle (host scheduling + tool waits), the dominant resource gap in this unsaturated regime"}])

    # ---- G08' resource attachment
    def med(col):
        vals = [float(r[idx[col]].replace(",", "")) for r in data if r[idx[col]] not in ("", "n/a")]
        vals.sort()
        return vals[len(vals) // 2] if vals else None

    gemm_row = {"sm_pct": med("sm__throughput.avg.pct_of_peak_sustained_elapsed"),
                "dram_pct": med("dram__cycles_active.avg.pct_of_peak_sustained_elapsed"),
                "l2_pct": med("lts__throughput.avg.pct_of_peak_sustained_elapsed"),
                "tensor_pct": med("sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active"),
                "occ_pct": med("sm__warps_active.avg.pct_of_peak_sustained_active")}
    resource = []
    for r in sel_rows:
        if not r["selected"]:
            continue
        if r["axis"] == "gpu_time":
            interp = ("L2/tensor-pipe bound batched GEMM" if gemm_row["l2_pct"] and gemm_row["l2_pct"] >= 60
                      else "see counters")
            row = {"lineage": a.lineage_tag, "component": r["component"], "share_pct": r["share_pct"],
                   "resource_status": "profiled_family:gemm",
                   "interpretation": interp,
                   "caveat": "NCU rows cover the batched-GEMM family only; attention/elementwise not profiled"}
            row.update({k: (round(v, 1) if v is not None else "") for k, v in gemm_row.items()})
            resource.append(row)
        else:
            resource.append({"lineage": a.lineage_tag, "component": r["component"], "share_pct": r["share_pct"],
                             "resource_status": "not_collected_host_or_wait",
                             "interpretation": "decode segment time is engine residency (batch sharing), not a single kernel; queue_wait is host-side",
                             "caveat": "", **{k: "" for k in gemm_row}})
    _write_csv(out / "g08_resource_attachment.csv", resource)

    # opportunities
    unsat = [r for r in timeline if r["concurrent_requests"] > 0]
    mean_busy = sum(r["gpu_busy_pct"] for r in unsat) / len(unsat) if unsat else 0
    opp = [{"lineage": a.lineage_tag, "opportunity": "increase_batch_residency",
            "evidence": f"mean GPU busy {mean_busy:.1f}% while requests in flight; engine never queued (w02' queue share {w02['requests']['queue_share_pct']}%)",
            "bound_note": "throughput headroom, not latency: programs are bound by their own critical paths (tool delays x waves)"},
           {"lineage": a.lineage_tag, "opportunity": "program_level_scheduling",
            "evidence": "pays only in queueing regimes: cap16 run gave PLAS 0.72x mean / 0.57x p90 program-token latency (results.md §5.2)",
            "bound_note": "no effect without a waiting queue (rate sweep §5.1)"}]
    _write_csv(out / "g08_opportunities.csv", opp)

    # ---- G09' manifest
    tables = ["g06_selection_plan.csv", "g06_selected_stacks.csv", "g07_timeline_1s.csv",
              "g07_gap_summary.csv", "g08_resource_attachment.csv", "g08_opportunities.csv"]
    manifest = {"schema_version": 1, "lineage": f"h23-agentix-8b/{a.lineage_tag}", "goal": ["G06'", "G07'", "G08'", "G09'", "G10'"],
                "admission_ledger": ledger,
                "tables": {t: {"rows": sum(1 for _ in (out / t).open()) - 1, "sha256": _sha256(out / t)} for t in tables},
                "selection": [r["component"] for r in sel_rows if r["selected"]],
                "pass": any(r["selected"] for r in sel_rows)}
    (out / "tables_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")

    # ---- G10' report
    L = ["# G06'-G10' selective analysis and resource gap (Agentix serving reproduction)", "",
         f"Lineage `{manifest['lineage']}`. Admission ledger: " + ", ".join(f"{k}={v[:12]}…" for k, v in ledger.items()), "",
         "## View A — selection and longest instances (visible range: full captured span)", "",
         "| axis | component | share | selected |", "|---|---|---:|---|"]
    for r in sel_rows:
        L.append(f"| {r['axis']} | {r['component']} | {r['share_pct']} % | {'**yes**' if r['selected'] else 'no'} |")
    L += ["", "Longest instances per selected request-time component:", "",
          "| component | rank | program | class | ns |", "|---|---:|---|---|---:|"]
    for s in stacks:
        L.append(f"| {s['component']} | {s['rank']} | {s['program_id']} | {s['class']} | {s['ns']:,} |")
    L += ["", "## View B — resource window (visible range: captured CUDA span only)", "",
          "| component | share | status | SM % | DRAM % | L2 % | Tensor % | interpretation |", "|---|---:|---|---:|---:|---:|---:|---|"]
    for r in resource:
        L.append(f"| {r['component']} | {r['share_pct']} % | {r['resource_status']} | {r.get('sm_pct','')} | {r.get('dram_pct','')} | {r.get('l2_pct','')} | {r.get('tensor_pct','')} | {r['interpretation']} |")
    L += ["", "## Opportunities", ""]
    for o in opp:
        L.append(f"- **{o['opportunity']}** — {o['evidence']} ({o['bound_note']})")
    L += ["", "Visible-range statement (G10'): View A covers every request in the run; View B is bounded by the captured",
          "CUDA span (~30 s, see w01' `analysed_span_is_truncated`) and by the NCU sample (batched-GEMM family only).", ""]
    (out / "G06_G10_REPORT.md").write_text("\n".join(L))
    print(json.dumps({"selection": manifest["selection"], "tables": len(tables), "pass": manifest["pass"]}, indent=2))
    return 0 if manifest["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

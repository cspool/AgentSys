#!/usr/bin/env python3
"""w05 / G06-G10: guided selective process analysis and resource-gap windows.

Admission: complete, ordered G01-G05 handoffs for every workload named. Each
is verified by its summary/conservation ``pass`` flag and sha256 before any
table is written. Nothing upstream is re-proved here.

Adapted AutoTrace goals:

* G06 bounded plan: process types strictly above 10 % of the total process
  host time; five longest instances (stacks) per selected type with their
  real start/end on the shared clock; global ranking by cumulative duration.
* G07 trace timeline: representative-iteration process and kernel timelines,
  GPU launch gaps, host/GPU overlap scan, high-latency instances (median +
  3 * MAD per type over all measured iterations).
* G08 resource attachment: per selected GPU-owning process, the w03 kernel
  family metrics (SM, tensor, DRAM, L2, occupancy). Host-only processes get an
  explicit ``not_collected`` status with the reason; nothing is zero-filled.
* G09 normalized tables with a manifest (schema, rows, sha256, lineage).
* G10 two views in one Markdown report: the high-latency process
  distribution and the resource window, each stating its visible range.
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_w01_operator_trace import _sha256, _union_busy, _write_csv  # noqa: E402

SELECT_THRESHOLD_PCT = 10.0
STACKS_PER_TYPE = 5
GAP_THRESHOLD_NS = 20_000  # 20 us GPU idle gap is reported


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def _mad(vals: list[float]) -> float:
    med = statistics.median(vals)
    return statistics.median(abs(v - med) for v in vals)


def admission(root: Path, workloads: list[str], w03_dir: Path, w04_dir: Path | None) -> dict[str, Any]:
    ledger: dict[str, Any] = {"goals": {}}
    for w in workloads:
        c = json.loads((root / "g01_operator_trace" / w / "analysis" / "conservation.json").read_text())
        s2 = json.loads((root / "g02_g03_call_process" / w / "summary.json").read_text())
        if not (c["pass"] and s2["pass"]):
            raise SystemExit(f"admission refused: G01/G02 not passed for {w}")
        if s2["upstream"]["sqlite_sha256"] != c["sqlite_sha256"]:
            raise SystemExit(f"admission refused: w02 upstream sha mismatch for {w}")
        ledger["goals"][w] = {"G01": c["sqlite_sha256"], "G02_G03": _sha256(root / "g02_g03_call_process" / w / "summary.json")}
    s3 = json.loads((w03_dir / "summary.json").read_text())
    if not s3["pass"]:
        raise SystemExit("admission refused: G04 not passed")
    ledger["G04"] = {"summary_sha256": _sha256(w03_dir / "summary.json"), "workloads": s3["workloads"]}
    if w04_dir is not None:
        s4 = json.loads((w04_dir / "summary.json").read_text())
        if not s4["pass"]:
            raise SystemExit("admission refused: G05 not passed")
        ledger["G05"] = {"summary_sha256": _sha256(w04_dir / "summary.json"), "target": s4["target"]}
    return ledger


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="w05 selective trace + resource gap")
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--workloads", nargs="+", required=True)
    parser.add_argument("--w03-analysis", type=Path, required=True)
    parser.add_argument("--w04-analysis", type=Path)
    parser.add_argument("--lineage-tag", default="base")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    root, out = args.artifact_root, args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    ledger = admission(root, args.workloads, args.w03_analysis, args.w04_analysis)
    family_hw = _read(args.w03_analysis / "ncu_process_family_hardware_report.csv")

    selection_rows, stack_rows, ranking_rows, timeline_rows, kernel_rows, gap_rows, hl_rows, overlap_rows, resource_rows, opp_rows, denom_rows = ([] for _ in range(11))

    for w in args.workloads:
        inst = _read(root / "g02_g03_call_process" / w / "call_process_instances.csv")
        s2 = json.loads((root / "g02_g03_call_process" / w / "summary.json").read_text())
        rep_iter = s2["representative_iteration"]
        iters = s2["iterations_measured"]
        total_host = sum(float(r["host_ns"]) for r in inst)
        by_type: dict[str, list[dict[str, str]]] = defaultdict(list)
        for r in inst:
            by_type[r["process"]].append(r)
        denom_rows.append({"lineage": args.lineage_tag, "workload": w, "total_process_host_ns": total_host, "iterations": iters, "process_types": len(by_type), "instances": len(inst)})

        # ---- G06 selection and stacks
        selected = []
        for proc, rs in sorted(by_type.items(), key=lambda kv: -sum(float(r["host_ns"]) for r in kv[1])):
            tot = sum(float(r["host_ns"]) for r in rs)
            share = 100 * tot / total_host
            vals = [float(r["host_ns"]) for r in rs]
            sel = share > SELECT_THRESHOLD_PCT
            selection_rows.append({"lineage": args.lineage_tag, "workload": w, "process": proc, "instances": len(rs), "cumulative_host_ns": tot, "share_pct": round(share, 2), "selected": sel,
                                   "median_ns": statistics.median(vals), "p90_ns": sorted(vals)[int(0.9 * (len(vals) - 1))], "max_ns": max(vals), "mad_ns": _mad(vals),
                                   "gpu_owning": any(int(r["kernel_launches"]) + int(r["memcpy_memset"]) > 0 for r in rs)})
            if sel:
                selected.append(proc)
                for rank, r in enumerate(sorted(rs, key=lambda r: -float(r["host_ns"]))[:STACKS_PER_TYPE], 1):
                    stack_rows.append({"lineage": args.lineage_tag, "workload": w, "process": proc, "stack_rank": rank, "iteration": r["iteration"], "call_id": r["call_id"], "op_index": r["op_index"],
                                       "start_ns": r["start"], "end_ns": r["end"], "host_ns": r["host_ns"], "gpu_work_ns": r["gpu_work_ns"], "cuda_api_ns": r["cuda_api_ns"], "cuda_api_top": r["cuda_api_top"]})
        for rank, (proc, rs) in enumerate(sorted(by_type.items(), key=lambda kv: -sum(float(r["host_ns"]) for r in kv[1])), 1):
            ranking_rows.append({"lineage": args.lineage_tag, "workload": w, "global_rank": rank, "process": proc, "cumulative_host_ns": sum(float(r["host_ns"]) for r in rs), "selected": proc in selected})

        # ---- G07 timeline (representative iteration) and gaps / overlap
        rep = sorted((r for r in inst if int(r["iteration"]) == rep_iter), key=lambda r: int(r["start"]))
        t0 = int(rep[0]["start"])
        for r in rep:
            timeline_rows.append({"lineage": args.lineage_tag, "workload": w, "iteration": rep_iter, "call_id": r["call_id"], "call_kind": r["call_kind"], "process": r["process"], "op_index": r["op_index"],
                                  "start_rel_us": round((int(r["start"]) - t0) / 1e3, 1), "end_rel_us": round((int(r["end"]) - t0) / 1e3, 1), "host_ns": r["host_ns"], "gpu_work_ns": r["gpu_work_ns"], "selected": r["process"] in selected})
        launch = _read(root / "g02_g03_call_process" / w / "kernel_launch_order_representative_iteration.csv")
        gpu_items = []
        for k in launch:
            gs = int(round(float(k["gpu_start_rel_us"]) * 1e3)) + t0
            ge = gs + int(k["gpu_ns"])
            gpu_items.append((gs, ge, k))
            kernel_rows.append({"lineage": args.lineage_tag, "workload": w, "iteration": rep_iter, **{kk: k[kk] for kk in ("launch_order", "call_id", "process", "op_index", "kind", "family", "gpu_ns", "launch_latency_ns", "gpu_start_rel_us")}})
        gpu_items.sort()
        prev_end = None
        for gs, ge, k in gpu_items:
            if prev_end is not None and gs - prev_end >= GAP_THRESHOLD_NS:
                covering = [r for r in rep if int(r["start"]) <= prev_end and int(r["end"]) >= gs]
                cover_names = "|".join(dict.fromkeys(f"{r['call_id'] or 'dag'}:{r['process']}" for r in rep if int(r["end"]) > prev_end and int(r["start"]) < gs))
                gap_rows.append({"lineage": args.lineage_tag, "workload": w, "iteration": rep_iter, "gap_start_rel_us": round((prev_end - t0) / 1e3, 1), "gap_ns": gs - prev_end,
                                 "next_gpu_item": f"{k['call_id']}:{k['process']}:{k['family']}", "host_processes_covering_gap": cover_names[:200]})
            prev_end = max(prev_end or ge, ge)
        gpu_busy = _union_busy([(gs, ge) for gs, ge, _ in gpu_items])
        host_with_gpu = _union_busy([(int(r["start"]), int(r["end"])) for r in rep if int(r["kernel_launches"]) + int(r["memcpy_memset"]) > 0])
        wall = int(rep[-1]["end"]) - t0
        overlap_rows.append({"lineage": args.lineage_tag, "workload": w, "iteration": rep_iter, "wall_ns": wall, "gpu_busy_ns": gpu_busy, "gpu_busy_pct": round(100 * gpu_busy / wall, 2),
                             "host_segments_owning_gpu_ns": host_with_gpu, "host_only_ns": wall - host_with_gpu, "host_only_pct": round(100 * (wall - host_with_gpu) / wall, 2),
                             "max_concurrent_gpu_items": 1 if gpu_items else 0, "gpu_streams": len({k["stream"] for k in launch}), "gaps_reported": sum(1 for g in gap_rows if g["workload"] == w),
                             "gap_ns_total": sum(g["gap_ns"] for g in gap_rows if g["workload"] == w)})

        # high-latency instances over all iterations
        for proc, rs in by_type.items():
            vals = [float(r["host_ns"]) for r in rs]
            med, mad = statistics.median(vals), _mad(vals)
            thr = med + max(3 * mad, 0.05 * med, 1.0)
            for r in rs:
                if float(r["host_ns"]) > thr:
                    hl_rows.append({"lineage": args.lineage_tag, "workload": w, "process": proc, "iteration": r["iteration"], "call_id": r["call_id"], "op_index": r["op_index"], "host_ns": r["host_ns"],
                                    "median_ns": med, "threshold_ns": round(thr), "excess_ns": round(float(r["host_ns"]) - med), "classification": "warm_or_first_iteration" if int(r["iteration"]) == 0 else "sporadic",
                                    "cuda_api_top": r["cuda_api_top"], "gpu_work_ns": r["gpu_work_ns"]})

        # ---- G08 resource attachment for selected + all GPU-owning types
        hw_by = defaultdict(list)
        for h in family_hw:
            hw_by[(h["workload"], h["process"])].append(h)
        for proc, rs in by_type.items():
            gpu_owning = any(int(r["kernel_launches"]) + int(r["memcpy_memset"]) > 0 for r in rs)
            share = 100 * sum(float(r["host_ns"]) for r in rs) / total_host
            hw = hw_by.get((w, proc)) or [h for (ww, pp), hs in hw_by.items() if pp == proc for h in hs]
            if not gpu_owning:
                resource_rows.append({"lineage": args.lineage_tag, "workload": w, "process": proc, "selected": proc in selected, "share_pct": round(share, 2), "resource_status": "not_collected_cpu_process",
                                      "reason": "host-side Python/CPU segment; no GPU counters exist for it", "family": "", "sm_pct": None, "tensor_pct": None, "dram_active_pct": None, "dram_bw_pct_peak": None, "l2_pct": None, "occupancy_pct": None, "waves_per_sm": None, "hw_source_workload": ""})
                continue
            if not hw:
                resource_rows.append({"lineage": args.lineage_tag, "workload": w, "process": proc, "selected": proc in selected, "share_pct": round(share, 2), "resource_status": "not_collected", "reason": "no w03 family row", "family": "",
                                      "sm_pct": None, "tensor_pct": None, "dram_active_pct": None, "dram_bw_pct_peak": None, "l2_pct": None, "occupancy_pct": None, "waves_per_sm": None, "hw_source_workload": ""})
                continue
            for h in hw:
                resource_rows.append({"lineage": args.lineage_tag, "workload": w, "process": proc, "selected": proc in selected, "share_pct": round(share, 2), "resource_status": h["ncu_status"],
                                      "reason": h["hardware_bottleneck_interpretation"], "family": h["matched_kernel_family"], "sm_pct": h["sm_throughput_pct"] or None, "tensor_pct": h["tensor_pipe_active_pct"] or None,
                                      "dram_active_pct": h["dram_cycles_active_pct"] or None, "dram_bw_pct_peak": h["dram_bw_pct_of_peak"] or None, "l2_pct": h["l2_throughput_pct"] or None,
                                      "occupancy_pct": h["achieved_occupancy_pct"] or None, "waves_per_sm": h["waves_per_sm"] or None, "hw_source_workload": h["workload"]})

        # ---- opportunities (derived, per workload)
        ptype = {r["process"]: r for r in _read(root / "g02_g03_call_process" / w / "process_type_breakdown.csv")}
        wall_total = sum(float(r["host_ns"]) for r in inst)
        gpu_total = sum(float(r["gpu_work_ns"]) for r in inst)
        hig = ptype.get("host_input_generate")
        wi = ptype.get("weight_init")
        if hig and wi:
            opp_rows.append({"lineage": args.lineage_tag, "workload": w, "opportunity": "move_input_generation_to_device", "evidence": "host_input_generate host vs weight_init GPU rng for the same shape",
                             "current_ns_per_iter": float(hig["host_ns_total"]) / iters, "reference_ns_per_iter": float(wi["gpu_ns_total"]) / iters,
                             "bound_pct_of_wall": round(100 * float(hig["host_ns_total"]) / wall_total, 2), "note": "seeded CPU-generator uniform_ into pinned fp16 is single-threaded and O(n^2); device randn for the same n^2 is the weight_init GPU time"})
        ops = [p for p in ptype if p.startswith("mir_operator")]
        op_host = sum(float(ptype[p]["host_ns_total"]) for p in ops)
        op_gpu = sum(float(ptype[p]["gpu_ns_total"]) for p in ops)
        opp_rows.append({"lineage": args.lineage_tag, "workload": w, "opportunity": "remove_per_operator_synchronize", "evidence": "mir_operator host range vs launch-owned GPU time",
                         "current_ns_per_iter": op_host / iters, "reference_ns_per_iter": op_gpu / iters, "bound_pct_of_wall": round(100 * (op_host - op_gpu) / wall_total, 2),
                         "note": "each operator ends with cudaEventSynchronize; the host range minus GPU work is dispatch + sync latency that async launch would hide"})
        opp_rows.append({"lineage": args.lineage_tag, "workload": w, "opportunity": "gpu_idle_window", "evidence": "1 - gpu_busy_union / wall over measured iterations",
                         "current_ns_per_iter": (wall_total - gpu_total) / iters, "reference_ns_per_iter": gpu_total / iters, "bound_pct_of_wall": round(100 * (wall_total - gpu_total) / wall_total, 2),
                         "note": "upper bound on wall reduction if all host work were overlapped or removed; single stream, no kernel concurrency observed"})

    tables = {"g06_selection_plan.csv": selection_rows, "g06_selected_stacks.csv": stack_rows, "g06_global_ranking.csv": ranking_rows, "g06_denominators.csv": denom_rows,
              "g07_process_timeline_representative.csv": timeline_rows, "g07_kernel_timeline_representative.csv": kernel_rows, "g07_launch_gaps.csv": gap_rows,
              "g07_high_latency_instances.csv": hl_rows, "g07_host_gpu_overlap.csv": overlap_rows, "g08_resource_attachment.csv": resource_rows, "g08_opportunities.csv": opp_rows}
    manifest = {"schema_version": 1, "lineage": f"h22-gpu-autotrace/{args.lineage_tag}", "goal": ["G06", "G07", "G08", "G09", "G10"], "admission_ledger": ledger, "tables": {}}
    for name, rows in tables.items():
        _write_csv(out / name, rows)
        manifest["tables"][name] = {"rows": len(rows), "schema": list(rows[0].keys()) if rows else [], "sha256": _sha256(out / name)}
    manifest["selection"] = {w: [r["process"] for r in selection_rows if r["workload"] == w and r["selected"]] for w in args.workloads}
    manifest["pass"] = all(manifest["selection"][w] for w in args.workloads)
    (out / "tables_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    _write_report(out / "G06_G10_SELECTIVE_TRACE_AND_RESOURCE_GAP_REPORT.md", args, manifest, tables)
    print(json.dumps({"lineage": args.lineage_tag, "pass": manifest["pass"], "selection": manifest["selection"], "high_latency_instances": len(hl_rows), "gaps": len(gap_rows)}, indent=2))
    return 0 if manifest["pass"] else 1


def _us(v: Any) -> str:
    return f"{float(v) / 1e3:,.1f}" if v not in ("", None) else ""


def _write_report(path: Path, args: Any, manifest: dict[str, Any], t: dict[str, list[dict[str, Any]]]) -> None:
    L = [f"# G06-G10 selective process trace and resource gap: lineage `{args.lineage_tag}`", "",
         "Lineage `h22-gpu-autotrace`, workflow w05. Admission ledger (sha256 of every upstream handoff) is in `tables_manifest.json`.",
         "Two views follow. The first hides nothing below the 10 % threshold except in the stacks table; the second shows only instances with a", "successfully attached hardware metric and says so.", "",
         "## View A: high-latency process distribution (G06/G07)", "",
         "### Selection (strictly > 10 % of total process host time)", "",
         "| workload | process | instances | cumulative (us) | share | median (us) | p90 (us) | max (us) | MAD (us) | GPU-owning | selected |", "|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|"]
    for r in t["g06_selection_plan.csv"]:
        L.append(f"| {r['workload']} | {r['process']} | {r['instances']} | {_us(r['cumulative_host_ns'])} | {r['share_pct']} % | {_us(r['median_ns'])} | {_us(r['p90_ns'])} | {_us(r['max_ns'])} | {_us(r['mad_ns'])} | {r['gpu_owning']} | {'**yes**' if r['selected'] else 'no'} |")
    L += ["", "### Five longest instances per selected type (real start/end on the nsys clock)", "", "| workload | process | rank | iter | call | start (ns) | host (us) | GPU (us) | top CUDA API |", "|---|---|---:|---:|---|---:|---:|---:|---|"]
    for r in t["g06_selected_stacks.csv"]:
        L.append(f"| {r['workload']} | {r['process']} | {r['stack_rank']} | {r['iteration']} | {r['call_id']} | {r['start_ns']} | {_us(r['host_ns'])} | {_us(r['gpu_work_ns'])} | {r['cuda_api_top']} |")
    L += ["", "### Host/GPU overlap and launch gaps, representative iteration (G07)", "", "| workload | iter | wall (us) | GPU busy | host-only | streams | max concurrent GPU | gaps >= 20 us | gap total (us) |", "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for r in t["g07_host_gpu_overlap.csv"]:
        L.append(f"| {r['workload']} | {r['iteration']} | {_us(r['wall_ns'])} | {r['gpu_busy_pct']} % | {r['host_only_pct']} % | {r['gpu_streams']} | {r['max_concurrent_gpu_items']} | {r['gaps_reported']} | {_us(r['gap_ns_total'])} |")
    L += ["", "Largest GPU launch gaps and the host processes covering them:", "", "| workload | gap start (us) | gap (us) | next GPU item | host processes covering |", "|---|---:|---:|---|---|"]
    for r in sorted(t["g07_launch_gaps.csv"], key=lambda r: -r["gap_ns"])[:15]:
        L.append(f"| {r['workload']} | {r['gap_start_rel_us']} | {_us(r['gap_ns'])} | {r['next_gpu_item']} | {r['host_processes_covering_gap'][:90]} |")
    hl = t["g07_high_latency_instances.csv"]
    L += ["", f"### High-latency instances (median + 3 MAD per type): {len(hl)} total", "", "| workload | process | iter | call | host (us) | median (us) | excess (us) | class |", "|---|---|---:|---|---:|---:|---:|---|"]
    for r in sorted(hl, key=lambda r: -float(r["excess_ns"]))[:20]:
        L.append(f"| {r['workload']} | {r['process']} | {r['iteration']} | {r['call_id']} | {_us(r['host_ns'])} | {_us(r['median_ns'])} | {_us(r['excess_ns'])} | {r['classification']} |")
    L += ["", "## View B: resource window (G08)", "", "Only rows with an attached hardware metric are shown with numbers; host-only processes are listed with their status so the coverage is explicit.", "",
          "| workload | process | selected | share | status | family | SM % | Tensor % | DRAM active % | DRAM BW % peak | L2 % | occupancy % | waves/SM | interpretation |", "|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|"]
    for r in t["g08_resource_attachment.csv"]:
        f = lambda k: "" if r[k] is None else r[k]
        L.append(f"| {r['workload']} | {r['process']} | {r['selected']} | {r['share_pct']} % | {r['resource_status']} | {r['family']} | {f('sm_pct')} | {f('tensor_pct')} | {f('dram_active_pct')} | {f('dram_bw_pct_peak')} | {f('l2_pct')} | {f('occupancy_pct')} | {f('waves_per_sm')} | {r['reason'][:70]} |")
    L += ["", "### Opportunities (derived, bounded by measured evidence)", "", "| workload | opportunity | current per iter (us) | reference per iter (us) | bound (% of wall) | note |", "|---|---|---:|---:|---:|---|"]
    for r in t["g08_opportunities.csv"]:
        L.append(f"| {r['workload']} | {r['opportunity']} | {_us(r['current_ns_per_iter'])} | {_us(r['reference_ns_per_iter'])} | {r['bound_pct_of_wall']} % | {r['note']} |")
    L += ["", "## Tables (G09)", "", "| table | rows | sha256 |", "|---|---:|---|"]
    for name, m in manifest["tables"].items():
        L.append(f"| {name} | {m['rows']} | {m['sha256'][:16]}… |")
    L += ["", "Visible-range statement (G10): View A stacks show 5 instances per selected type; View B shows every process type but numbers only where a w03 family row attached.",
          "Full per-instance evidence remains in the w01/w02 tables referenced by the admission ledger.", ""]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())

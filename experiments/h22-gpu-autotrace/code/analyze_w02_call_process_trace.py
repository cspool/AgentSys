#!/usr/bin/env python3
"""w02 / G02+G03: call-wise (agent-node) process attribution inside the w01 denominator.

The w01 trace already carries two process-level sources that together tile
every iteration without gaps:

* NVTX operator ranges (nsys clock), one per MIR operator, from the certified
  adapter in ``agentsys.hybrid_runtime``;
* host events in ``native-trace.jsonl`` (``time.monotonic_ns``): adapter
  start/complete, token preprocess, H2D, D2H, tool execution.

The two clocks differ by a constant offset (nsys session-relative). The offset
is fitted from the 1:1 pairing of operator NVTX ranges with operator host
events; the fit residual is reported and must stay in the tens of
microseconds, otherwise the alignment is rejected.

Every measured iteration is then cut into named process segments, in order,
so that ``sum(segment) == iteration wall`` exactly. Each segment gets its
launch-owned GPU work (runtime API launched inside it, kernel by
correlationId) and its CUDA runtime API time by API name. G03 adds the kernel
launch order per call for a representative iteration and kernel families per
process.

This script does not re-time anything and does not modify ``src/agentsys``.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import hashlib
import json
import sqlite3
import statistics
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from analyze_w01_operator_trace import (  # noqa: E402
    GpuWork,
    Range,
    _kernel_family,
    _parse_op,
    _parse_phase,
    _sha256,
    _union_busy,
    _write_csv,
    load_trace,
)

MAX_ALIGN_SPREAD_NS = 200_000  # 200 us; observed ~14 us


@dataclass
class Segment:
    phase: str
    iteration: int
    call_id: str | None
    call_kind: str  # llm | tool | dag
    process: str
    op_index: int | None
    op_type: str | None
    engine: str | None
    start: int
    end: int
    basis: str

    @property
    def duration(self) -> int:
        return self.end - self.start


def fit_offset(nvtx_ops: list[Range], host_ops: list[dict[str, Any]]) -> dict[str, Any]:
    """Pair measured-phase operator ranges to host operator events in order."""
    measured_nvtx = nvtx_ops  # caller passes only measured ones
    if len(measured_nvtx) != len(host_ops):
        raise SystemExit(f"alignment: {len(measured_nvtx)} nvtx operator ranges vs {len(host_ops)} host operator events")
    offsets = []
    for nv, ev in zip(measured_nvtx, host_ops):
        c, i, t = _parse_op(nv.text)
        if (c, i, t) != (ev["call_id"], int(ev["source_index"]), ev["op_type"]):
            raise SystemExit(f"alignment: pairing mismatch {nv.text} vs {ev['call_id']}:{ev['source_index']}:{ev['op_type']}")
        offsets.append(int(ev["start_ns"]) - nv.start)
    med = int(statistics.median(offsets))
    spread = max(offsets) - min(offsets)
    return {"offset_ns": med, "pairs": len(offsets), "spread_ns": spread, "min_ns": min(offsets), "max_ns": max(offsets), "pass": spread <= MAX_ALIGN_SPREAD_NS}


def build_segments(
    phases: list[Range],
    nvtx_ops: list[Range],
    host_events: list[dict[str, Any]],
    plan: dict[str, Any],
    offset_ns: int,
) -> list[Segment]:
    kind_of = {c["call_id"]: c["kind"] for c in plan["calls"]}
    engine_of = {(c["call_id"], int(o["index"])): o["engine"] for c in plan["calls"] for o in c.get("mir_operators", [])}

    def h2n(ts: int) -> int:  # host monotonic -> nsys clock
        return int(ts) - offset_ns

    by_iter_events: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for ev in host_events:
        if ev.get("phase") == "measured":
            by_iter_events[int(ev["iteration"])].append(ev)

    segments: list[Segment] = []
    for ph in phases:
        phase, iteration = _parse_phase(ph.text)
        if phase != "measured":
            continue
        ops_in = [r for r in nvtx_ops if ph.start <= r.start and r.end <= ph.end]
        evs = sorted(by_iter_events.get(iteration, []), key=lambda e: int(e["start_ns"]))
        # Build the ordered marker list on the nsys clock.
        markers: list[tuple[int, int, str, str, int | None, str | None, str]] = []  # (start,end,call,process,op_index,op_type,basis)
        for ev in evs:
            s, e = h2n(ev["start_ns"]), h2n(ev["end_ns"])
            name = ev["event"]
            if name == "mir_adapter_start":
                markers.append((s, s, ev["call_id"], "adapter_start", None, None, "host_event"))
            elif name == "mir_adapter_complete":
                markers.append((s, s, ev["call_id"], "adapter_complete", None, None, "host_event"))
            elif name == "mllm_token_preprocess":
                markers.append((s, e, ev["call_id"], "token_preprocess_cpu", None, None, "host_event"))
            elif name == "h2d":
                markers.append((s, e, ev["call_id"], "h2d_stage", None, None, "host_event"))
            elif name == "d2h":
                markers.append((s, e, ev["call_id"], "d2h_stage", None, None, "host_event"))
            elif name == "agent_tool_execute":
                markers.append((s, e, ev["call_id"], "agent_tool_execute_cpu", None, None, "host_event"))
            elif name == "mir_operator":
                pass  # NVTX range is authoritative for operators
        for r in ops_in:
            c, i, t = _parse_op(r.text)
            markers.append((r.start, r.end, c, f"mir_operator:{t}", i, t, "nvtx_range"))
        markers.sort(key=lambda m: (m[0], m[1]))

        # Walk markers, emitting explicit segments and named gaps.
        cursor = ph.start
        current_call: str | None = None
        last_process: str | None = None
        first_op_seen: set[str] = set()
        for s, e, call, proc, opi, opt, basis in markers:
            s = max(s, cursor)
            e = max(e, s)
            if s > cursor:
                # gap before this marker
                if current_call is None or proc == "adapter_start" or (call != current_call and kind_of.get(call) == "tool"):
                    gname, gcall, gkind = "dag_schedule_gap", None, "dag"
                elif proc == "token_preprocess_cpu":
                    gname, gcall, gkind = "adapter_dispatch", call, "llm"
                elif proc == "h2d_stage":
                    gname, gcall, gkind = "host_input_generate", call, "llm"
                elif proc.startswith("mir_operator") and call not in first_op_seen:
                    gname, gcall, gkind = "weight_init", call, "llm"
                elif proc.startswith("mir_operator"):
                    gname, gcall, gkind = "inter_operator_dispatch", call, "llm"
                elif proc == "d2h_stage":
                    gname, gcall, gkind = "pre_d2h_alloc", call, "llm"
                elif proc == "adapter_complete":
                    gname, gcall, gkind = "checksum_complete", call, "llm"
                else:
                    gname, gcall, gkind = "unnamed_gap", call, kind_of.get(call, "dag")
                segments.append(Segment(phase, iteration, gcall, gkind, gname, None, None, None, cursor, s, "gap_between_markers"))
            if proc == "adapter_start":
                current_call = call
            elif proc == "adapter_complete":
                current_call = None
            if e > s:
                segments.append(Segment(phase, iteration, call, kind_of.get(call, "llm"), proc, opi, opt, engine_of.get((call, opi)) if opi is not None else None, s, e, basis))
                if proc.startswith("mir_operator"):
                    first_op_seen.add(call)
            cursor = max(cursor, e)
            last_process = proc
        if cursor < ph.end:
            segments.append(Segment(phase, iteration, None, "dag", "iteration_tail_sync", None, None, None, cursor, ph.end, "gap_to_phase_end"))
    return segments


def attach_gpu(segments: list[Segment], work: list[GpuWork], api_rows: list[tuple[int, int, str]]) -> tuple[dict[int, list[GpuWork]], dict[int, dict[str, tuple[int, int]]]]:
    work_starts = [w.api_start for w in work]
    api_rows.sort()
    api_starts = [a[0] for a in api_rows]
    seg_work: dict[int, list[GpuWork]] = {}
    seg_api: dict[int, dict[str, tuple[int, int]]] = {}
    claimed: set[int] = set()
    for idx, seg in enumerate(segments):
        lo, hi = bisect.bisect_left(work_starts, seg.start), bisect.bisect_right(work_starts, seg.end)
        items = []
        for w in work[lo:hi]:
            if w.correlation_id in claimed:
                continue
            claimed.add(w.correlation_id)
            items.append(w)
        seg_work[idx] = items
        lo, hi = bisect.bisect_left(api_starts, seg.start), bisect.bisect_right(api_starts, seg.end)
        agg: dict[str, tuple[int, int]] = {}
        for s, e, name in api_rows[lo:hi]:
            ns, n = agg.get(name, (0, 0))
            agg[name] = (ns + (min(e, seg.end) - s), n + 1)
        seg_api[idx] = agg
    return seg_work, seg_api


def load_api(sqlite_path: Path) -> list[tuple[int, int, str]]:
    db = sqlite3.connect(str(sqlite_path))
    strings = dict(db.execute("select id, value from StringIds"))
    rows = [(s, e, strings.get(n, str(n)).split("_v")[0]) for s, e, n in db.execute("select start, end, nameId from CUPTI_ACTIVITY_KIND_RUNTIME")]
    db.close()
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="w02 call-wise process attribution")
    parser.add_argument("--sqlite", type=Path, required=True)
    parser.add_argument("--native-trace", type=Path, required=True)
    parser.add_argument("--run-metadata", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--w01-conservation", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    metadata = json.loads(args.run_metadata.read_text())
    plan = json.loads(args.plan.read_text())
    w01 = json.loads(args.w01_conservation.read_text())
    workload = metadata["workload"]
    if not w01.get("pass"):
        raise SystemExit("w01 conservation did not pass; w02 admission refused")
    if w01["sqlite_sha256"] != _sha256(args.sqlite):
        raise SystemExit("sqlite sha256 differs from the w01 conservation record")

    phases, nvtx_ops, work, info = load_trace(args.sqlite)
    host_events = [json.loads(line) for line in args.native_trace.read_text().splitlines() if line.strip()]
    measured_phase_windows = [(p.start, p.end) for p in phases if p.text.startswith("agentsys.autotrace::phase=measured")]
    measured_nvtx_ops = [r for r in nvtx_ops if any(s <= r.start and r.end <= e for s, e in measured_phase_windows)]
    host_ops = sorted([e for e in host_events if e["event"] == "mir_operator" and e.get("phase") == "measured"], key=lambda e: int(e["start_ns"]))
    align = fit_offset(measured_nvtx_ops, host_ops)
    if not align["pass"]:
        raise SystemExit(f"clock alignment rejected: {align}")

    segments = build_segments(phases, nvtx_ops, host_events, plan, align["offset_ns"])
    api_rows = load_api(args.sqlite)
    seg_work, seg_api = attach_gpu(segments, work, api_rows)

    # ---- instance table
    rows: list[dict[str, Any]] = []
    for idx, s in enumerate(segments):
        items = seg_work[idx]
        api = seg_api[idx]
        api_ns = sum(v[0] for v in api.values())
        rows.append(
            {
                "workload": workload, "phase": s.phase, "iteration": s.iteration, "call_id": s.call_id or "", "call_kind": s.call_kind,
                "process": s.process, "op_index": s.op_index if s.op_index is not None else "", "op_type": s.op_type or "", "engine": s.engine or "",
                "basis": s.basis, "start": s.start, "end": s.end, "host_ns": s.duration,
                "gpu_work_ns": sum(w.duration for w in items), "gpu_busy_union_ns": _union_busy([(w.start, w.end) for w in items]),
                "kernel_launches": sum(1 for w in items if w.kind == "kernel"), "memcpy_memset": sum(1 for w in items if w.kind != "kernel"),
                "cuda_api_ns": api_ns, "cuda_api_calls": sum(v[1] for v in api.values()),
                "cuda_api_top": max(api.items(), key=lambda kv: kv[1][0])[0] if api else "",
                "host_minus_api_ns": s.duration - api_ns,
                "kernel_families": "|".join(sorted({w.family for w in items})),
            }
        )
    _write_csv(out / "call_process_instances.csv", rows)

    # ---- conservation per iteration
    iters: dict[int, dict[str, Any]] = {}
    for p in phases:
        phase, it = _parse_phase(p.text)
        if phase == "measured":
            iters[it] = {"workload": workload, "iteration": it, "wall_ns": p.duration, "segment_sum_ns": 0, "segments": 0, "gpu_work_ns": 0, "cuda_api_ns": 0}
    for r in rows:
        d = iters[r["iteration"]]
        d["segment_sum_ns"] += r["host_ns"]
        d["segments"] += 1
        d["gpu_work_ns"] += r["gpu_work_ns"]
        d["cuda_api_ns"] += r["cuda_api_ns"]
    iter_rows = []
    for it, d in sorted(iters.items()):
        d["conservation_err_ns"] = d["segment_sum_ns"] - d["wall_ns"]
        iter_rows.append(d)
    _write_csv(out / "iteration_conservation.csv", iter_rows)
    max_err = max(abs(d["conservation_err_ns"]) for d in iter_rows)

    # ---- per process type
    total_wall = sum(d["wall_ns"] for d in iter_rows)
    total_gpu = sum(r["gpu_work_ns"] for r in rows)
    ptype: dict[str, dict[str, float]] = defaultdict(lambda: {"host_ns": 0, "gpu_ns": 0, "api_ns": 0, "n": 0, "launches": 0})
    for r in rows:
        t = ptype[r["process"]]
        t["host_ns"] += r["host_ns"]; t["gpu_ns"] += r["gpu_work_ns"]; t["api_ns"] += r["cuda_api_ns"]; t["n"] += 1; t["launches"] += r["kernel_launches"]
    ptype_rows = [
        {"workload": workload, "process": k, "instances": v["n"], "host_ns_total": v["host_ns"], "host_share_pct": round(100 * v["host_ns"] / total_wall, 2),
         "host_ns_per_instance": round(v["host_ns"] / v["n"], 1), "gpu_ns_total": v["gpu_ns"], "gpu_share_pct": round(100 * v["gpu_ns"] / total_gpu, 2) if total_gpu else "",
         "cuda_api_ns_total": v["api_ns"], "cuda_api_share_of_host_pct": round(100 * v["api_ns"] / v["host_ns"], 1) if v["host_ns"] else "",
         "kernel_launches": v["launches"], "gpu_over_host_pct": round(100 * v["gpu_ns"] / v["host_ns"], 1) if v["host_ns"] else ""}
        for k, v in sorted(ptype.items(), key=lambda kv: -kv[1]["host_ns"])
    ]
    _write_csv(out / "process_type_breakdown.csv", ptype_rows)

    # ---- per call
    ccall: dict[str, dict[str, float]] = defaultdict(lambda: {"host_ns": 0, "gpu_ns": 0, "n": set(), "kind": ""})
    for r in rows:
        key = r["call_id"] or "<dag>"
        c = ccall[key]
        c["host_ns"] += r["host_ns"]; c["gpu_ns"] += r["gpu_work_ns"]; c["n"].add(r["iteration"]); c["kind"] = r["call_kind"]
    order = {c["call_id"]: (c["wave"], c["index"]) for c in plan["calls"]}
    call_rows = [
        {"workload": workload, "call_id": k, "call_kind": v["kind"], "wave": order.get(k, (99, 99))[0] if k in order else "",
         "matrix_size": next((c["native"]["matrix_size"] for c in plan["calls"] if c["call_id"] == k), ""),
         "host_ns_per_iter": round(v["host_ns"] / len(iter_rows), 1), "host_share_pct": round(100 * v["host_ns"] / total_wall, 2),
         "gpu_ns_per_iter": round(v["gpu_ns"] / len(iter_rows), 1), "gpu_share_pct": round(100 * v["gpu_ns"] / total_gpu, 2) if total_gpu else "",
         "gpu_over_host_pct": round(100 * v["gpu_ns"] / v["host_ns"], 2) if v["host_ns"] else ""}
        for k, v in sorted(ccall.items(), key=lambda kv: order.get(kv[0], (99, 99)))
    ]
    _write_csv(out / "call_breakdown.csv", call_rows)

    # ---- per (call, process) summary
    cp: dict[tuple[str, str, Any], list[dict[str, Any]]] = defaultdict(list)
    for r in rows:
        cp[(r["call_id"], r["process"], r["op_index"])].append(r)
    cp_rows = []
    for (call, proc, opi), rs in sorted(cp.items(), key=lambda kv: (order.get(kv[0][0], (99, 99)), min(r["start"] for r in kv[1]))):
        h = [r["host_ns"] for r in rs]; g = [r["gpu_work_ns"] for r in rs]
        cp_rows.append({"workload": workload, "call_id": call, "process": proc, "op_index": opi, "op_type": rs[0]["op_type"], "engine": rs[0]["engine"],
                        "instances": len(rs), "host_ns_median": statistics.median(h), "host_ns_min": min(h), "host_ns_max": max(h),
                        "gpu_ns_median": statistics.median(g), "cuda_api_ns_median": statistics.median(r["cuda_api_ns"] for r in rs),
                        "cuda_api_top": rs[0]["cuda_api_top"], "kernel_families": rs[0]["kernel_families"],
                        "kernels_per_instance": round(statistics.mean(r["kernel_launches"] for r in rs), 2)})
    _write_csv(out / "call_process_summary.csv", cp_rows)

    # ---- G03: kernel launch order for the representative iteration (median wall)
    walls = sorted(iter_rows, key=lambda d: d["wall_ns"])
    rep_iter = walls[len(walls) // 2]["iteration"]
    launch_rows = []
    order_n = 0
    for idx, s in enumerate(segments):
        if s.iteration != rep_iter:
            continue
        for w in sorted(seg_work[idx], key=lambda w: w.api_start):
            order_n += 1
            launch_rows.append({"workload": workload, "iteration": rep_iter, "launch_order": order_n, "call_id": s.call_id or "", "process": s.process,
                                "op_index": s.op_index if s.op_index is not None else "", "kind": w.kind, "family": w.family, "name": w.name[:120],
                                "api_name": w.api_name, "api_start_rel_us": round((w.api_start - segments[0].start) / 1e3, 1),
                                "gpu_start_rel_us": round((w.start - segments[0].start) / 1e3, 1), "gpu_ns": w.duration,
                                "launch_latency_ns": w.start - w.api_start, "grid": "x".join(map(str, w.grid)), "block": "x".join(map(str, w.block)), "stream": w.stream})
    _write_csv(out / "kernel_launch_order_representative_iteration.csv", launch_rows)

    fam: dict[tuple[str, str], dict[str, float]] = defaultdict(lambda: {"ns": 0, "n": 0})
    for idx, s in enumerate(segments):
        for w in seg_work[idx]:
            fam[(s.process, w.family)]["ns"] += w.duration; fam[(s.process, w.family)]["n"] += 1
    fam_rows = [{"workload": workload, "process": p, "family": f, "instances": v["n"], "gpu_ns_total": v["ns"], "gpu_share_pct": round(100 * v["ns"] / total_gpu, 2) if total_gpu else ""}
                for (p, f), v in sorted(fam.items(), key=lambda kv: -kv[1]["ns"])]
    _write_csv(out / "kernel_family_by_process.csv", fam_rows)

    api_tot: dict[str, dict[str, float]] = defaultdict(lambda: {"ns": 0, "n": 0})
    for idx in seg_api:
        for name, (ns, n) in seg_api[idx].items():
            api_tot[name]["ns"] += ns; api_tot[name]["n"] += n
    api_rows_out = [{"workload": workload, "api": k, "calls": v["n"], "ns_total": v["ns"], "share_of_wall_pct": round(100 * v["ns"] / total_wall, 2)} for k, v in sorted(api_tot.items(), key=lambda kv: -kv[1]["ns"])]
    _write_csv(out / "cuda_runtime_api_breakdown.csv", api_rows_out)

    summary = {
        "schema_version": 1, "lineage": "h22-gpu-autotrace", "goal": ["G02", "G03"], "workload": workload,
        "upstream": {"w01_conservation": str(args.w01_conservation), "sqlite_sha256": w01["sqlite_sha256"], "native_trace_sha256": _sha256(args.native_trace), "plan_sha256": metadata["plan_sha256"]},
        "clock_alignment": align,
        "iterations_measured": len(iter_rows), "representative_iteration": rep_iter,
        "wall_ns_total": total_wall, "gpu_work_ns_total": total_gpu, "w01_operator_plus_overhead_gpu_ns": w01["measured"]["sum_attributed_gpu_ns_total"],
        "gpu_conservation_vs_w01_ns": total_gpu - w01["measured"]["sum_attributed_gpu_ns_total"],
        "max_segment_conservation_err_ns": max_err, "unnamed_gap_ns": ptype.get("unnamed_gap", {}).get("host_ns", 0),
        "process_types": [r["process"] for r in ptype_rows],
        "pass": max_err == 0 and total_gpu == w01["measured"]["sum_attributed_gpu_ns_total"] and ptype.get("unnamed_gap", {}).get("host_ns", 0) == 0,
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    _write_report(out / "G02_G03_CALL_PROCESS_REPORT.md", workload, summary, ptype_rows, call_rows, cp_rows, api_rows_out, fam_rows, launch_rows)
    print(json.dumps({"workload": workload, "pass": summary["pass"], "align_spread_us": align["spread_ns"] / 1e3, "max_conservation_err_ns": max_err,
                      "gpu_vs_w01_ns": summary["gpu_conservation_vs_w01_ns"], "top_processes": [(r["process"], r["host_share_pct"]) for r in ptype_rows[:5]]}, indent=2))
    return 0 if summary["pass"] else 1


def _us(ns: float) -> str:
    return f"{ns / 1e3:,.1f}"


def _write_report(path: Path, workload: str, s: dict[str, Any], ptype: list[dict[str, Any]], calls: list[dict[str, Any]], cp: list[dict[str, Any]], api: list[dict[str, Any]], fam: list[dict[str, Any]], launches: list[dict[str, Any]]) -> None:
    a = s["clock_alignment"]
    L = [
        f"# G02/G03 call-wise process attribution: `{workload}`",
        "",
        "Lineage `h22-gpu-autotrace`, workflow w02. Consumes the w01 trace only; no re-timing.",
        f"Host events aligned to the nsys clock by a constant offset fitted on {a['pairs']} operator pairs (spread {_us(a['spread_ns'])} us).",
        "",
        "## Conservation",
        "",
        "| Quantity | Value |",
        "|---|---:|",
        f"| Measured iterations | {s['iterations_measured']} |",
        f"| Sum of process segments minus iteration wall (max abs) | {s['max_segment_conservation_err_ns']} ns |",
        f"| GPU work attributed here minus w01 attributed GPU | {s['gpu_conservation_vs_w01_ns']} ns |",
        f"| Unnamed gap time | {_us(s['unnamed_gap_ns'])} us |",
        f"| Pass | {s['pass']} |",
        "",
        "## Process-type breakdown (share of measured wall)",
        "",
        "| process | instances | host total (us) | host share | per instance (us) | GPU total (us) | GPU share | CUDA API share of host | GPU/host |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in ptype:
        L.append(f"| {r['process']} | {r['instances']} | {_us(r['host_ns_total'])} | {r['host_share_pct']} % | {_us(r['host_ns_per_instance'])} | {_us(r['gpu_ns_total'])} | {r['gpu_share_pct']} % | {r['cuda_api_share_of_host_pct']} % | {r['gpu_over_host_pct']} % |")
    L += ["", "## Call breakdown (agent nodes)", "", "| call | kind | wave | matrix | host per iter (us) | host share | GPU per iter (us) | GPU share | GPU/host |", "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for r in calls:
        L.append(f"| {r['call_id']} | {r['call_kind']} | {r['wave']} | {r['matrix_size']} | {_us(r['host_ns_per_iter'])} | {r['host_share_pct']} % | {_us(r['gpu_ns_per_iter'])} | {r['gpu_share_pct']} % | {r['gpu_over_host_pct']} % |")
    L += ["", "## CUDA runtime API inside the measured window", "", "| API | calls | total (us) | share of wall |", "|---|---:|---:|---:|"]
    for r in api[:12]:
        L.append(f"| {r['api']} | {r['calls']} | {_us(r['ns_total'])} | {r['share_of_wall_pct']} % |")
    L += ["", "## Kernel families by process (G03)", "", "| process | family | instances | GPU total (us) | share |", "|---|---|---:|---:|---:|"]
    for r in fam:
        L.append(f"| {r['process']} | {r['family']} | {r['instances']} | {_us(r['gpu_ns_total'])} | {r['gpu_share_pct']} % |")
    L += ["", f"## Kernel launch order, representative iteration {s['representative_iteration']} (G03)", "", "| # | call | process | kind | family | GPU (us) | launch latency (us) | grid | block |", "|---:|---|---|---|---|---:|---:|---|---|"]
    for r in launches[:60]:
        L.append(f"| {r['launch_order']} | {r['call_id']} | {r['process']}{(':' + str(r['op_index'])) if r['op_index'] != '' else ''} | {r['kind']} | {r['family']} | {_us(r['gpu_ns'])} | {_us(r['launch_latency_ns'])} | {r['grid']} | {r['block']} |")
    if len(launches) > 60:
        L.append(f"| … | | {len(launches) - 60} more rows in kernel_launch_order_representative_iteration.csv | | | | | | |")
    L += ["", "## Per call/process summary (medians over measured iterations)", "", "| call | process | op | host median (us) | host min/max (us) | GPU median (us) | top CUDA API | kernels |", "|---|---|---:|---:|---:|---:|---|---:|"]
    for r in cp:
        L.append(f"| {r['call_id'] or '<dag>'} | {r['process']} | {r['op_index']} | {_us(r['host_ns_median'])} | {_us(r['host_ns_min'])}/{_us(r['host_ns_max'])} | {_us(r['gpu_ns_median'])} | {r['cuda_api_top']} | {r['kernels_per_instance']} |")
    L += [
        "",
        "## Process inventory (handoff contract)",
        "",
        "| process | owner | evidence | what it contains |",
        "|---|---|---|---|",
        "| dag_schedule_gap | dag | gap host | scheduler between calls / before first call |",
        "| adapter_dispatch | llm call | gap host | adapter_start -> token preprocess |",
        "| token_preprocess_cpu | llm call | host event | seeded 256x256 fp32 CPU matmul |",
        "| host_input_generate | llm call | gap host | pinned fp16 tensor alloc + CPU-generator uniform_ |",
        "| h2d_stage | llm call | host event + memcpy | pinned -> device copy, cudaEvent bracket |",
        "| weight_init | llm call | gap host + kernels | torch.cuda.manual_seed + randn weight on device |",
        "| mir_operator:<type> | llm call | NVTX range + kernels | one MIR operator incl. cudaEventSynchronize |",
        "| inter_operator_dispatch | llm call | gap host | Python between operator ranges |",
        "| pre_d2h_alloc | llm call | gap host | pinned output alloc |",
        "| d2h_stage | llm call | host event + memcpy | device -> pinned copy |",
        "| checksum_complete | llm call | gap host | host checksum, adapter_complete |",
        "| agent_tool_execute_cpu | tool call | host event | seeded 256x256 fp32 CPU matmul |",
        "| iteration_tail_sync | dag | gap host | torch.cuda.synchronize + range pop |",
        "",
    ]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())

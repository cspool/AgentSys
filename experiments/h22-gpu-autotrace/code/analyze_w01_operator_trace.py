#!/usr/bin/env python3
"""w01 / G01 analyzer: operator-wise conservation denominator from an nsys trace.

Attribution is by launch ownership only, in the AutoTrace sense:

    operator NVTX CPU range (same thread)
      -> CUDA runtime API call whose start timestamp lies inside that range
      -> CUPTI kernel / memcpy / memset with the same correlationId

GPU work launched inside a phase range but outside any operator range is
"call overhead" (weight init, H2D/D2H staging, dtype copies). It is attributed
to a call by position: work before a call's first operator belongs to that
call, work after its last operator belongs to it, so that the phase total is
conserved: sum(operator) + sum(call_overhead) + unattributed == phase GPU busy.

Nothing here re-times the workload. The denominator is the measured-phase
window from the NVTX phase ranges; warmup iterations are reported separately
and never mixed into measured statistics.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sqlite3
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

PHASE_PREFIX = "agentsys.autotrace::phase="
OP_PREFIX = "agentsys.mllm::"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _kernel_family(name: str) -> str:
    """Coarse family label for a demangled kernel name."""
    lowered = name.lower()
    if "gemv" in lowered:
        return "gemv"
    if "flash" in lowered or "fmha" in lowered or "attention" in lowered:
        return "attention"
    if "catarraybatchedcopy" in lowered:
        return "concat"
    if "cutlass" in lowered or "gemm" in lowered or "sgemm" in lowered:
        return "gemm"
    if "distribution_elementwise" in lowered or "normal_and_transform" in lowered:
        return "rng_init"
    if "reduce_kernel" in lowered:
        return "reduce"
    if "direct_copy_kernel" in lowered or "copy_kernel" in lowered:
        return "copy"
    if "rsqrt" in lowered or "pow_tensor_scalar" in lowered:
        return "elementwise_unary"
    if "binaryfunctor" in lowered or "cudafunctoronself_add" in lowered or "mul" in lowered:
        return "elementwise_binary"
    if "elementwise" in lowered:
        return "elementwise_other"
    if "fill" in lowered:
        return "fill"
    return "other"


@dataclass
class Range:
    start: int
    end: int
    text: str
    tid: int

    @property
    def duration(self) -> int:
        return self.end - self.start


@dataclass
class GpuWork:
    kind: str  # kernel | memcpy | memset
    start: int
    end: int
    correlation_id: int
    name: str
    family: str
    api_start: int
    api_end: int
    api_name: str
    stream: int
    grid: tuple[int, int, int] = (0, 0, 0)
    block: tuple[int, int, int] = (0, 0, 0)
    registers: int = 0
    static_smem: int = 0
    dynamic_smem: int = 0
    bytes: int = 0

    @property
    def duration(self) -> int:
        return self.end - self.start


@dataclass
class Owner:
    phase: str
    iteration: int
    call_id: str | None
    op_index: int | None
    op_type: str | None
    engine: str | None
    basis: str
    nvtx: Range | None
    work: list[GpuWork] = field(default_factory=list)

    @property
    def key(self) -> tuple[Any, ...]:
        return (self.phase, self.iteration, self.call_id, self.op_index)


def load_trace(sqlite_path: Path) -> tuple[list[Range], list[Range], list[GpuWork], dict[str, Any]]:
    db = sqlite3.connect(str(sqlite_path))
    strings = dict(db.execute("select id, value from StringIds"))

    phases: list[Range] = []
    ops: list[Range] = []
    for start, end, text, tid in db.execute(
        "select start, end, text, globalTid from NVTX_EVENTS where text is not null"
    ):
        if text.startswith(PHASE_PREFIX):
            phases.append(Range(start, end, text, tid))
        elif text.startswith(OP_PREFIX):
            ops.append(Range(start, end, text, tid))
    phases.sort(key=lambda r: r.start)
    ops.sort(key=lambda r: r.start)

    api: dict[int, tuple[int, int, str, int]] = {}
    for start, end, cid, name_id, tid in db.execute(
        "select start, end, correlationId, nameId, globalTid from CUPTI_ACTIVITY_KIND_RUNTIME"
    ):
        api[cid] = (start, end, strings.get(name_id, str(name_id)), tid)

    work: list[GpuWork] = []
    for row in db.execute(
        "select start, end, correlationId, demangledName, streamId, gridX, gridY, gridZ, "
        "blockX, blockY, blockZ, registersPerThread, staticSharedMemory, dynamicSharedMemory "
        "from CUPTI_ACTIVITY_KIND_KERNEL"
    ):
        start, end, cid, name_id, stream = row[:5]
        a = api.get(cid, (0, 0, "?", 0))
        name = strings.get(name_id, str(name_id))
        work.append(
            GpuWork(
                "kernel", start, end, cid, name, _kernel_family(name), a[0], a[1], a[2], stream,
                grid=tuple(row[5:8]), block=tuple(row[8:11]), registers=row[11],
                static_smem=row[12], dynamic_smem=row[13],
            )
        )
    copy_kind = dict(db.execute("select id, label from ENUM_CUDA_MEMCPY_OPER")) if _has_table(db, "ENUM_CUDA_MEMCPY_OPER") else {}
    for start, end, cid, nbytes, kind, stream in db.execute(
        "select start, end, correlationId, bytes, copyKind, streamId from CUPTI_ACTIVITY_KIND_MEMCPY"
    ):
        a = api.get(cid, (0, 0, "?", 0))
        label = f"memcpy_{copy_kind.get(kind, kind)}"
        work.append(GpuWork("memcpy", start, end, cid, label, "memcpy", a[0], a[1], a[2], stream, bytes=nbytes))
    if _has_table(db, "CUPTI_ACTIVITY_KIND_MEMSET"):
        for start, end, cid, nbytes, stream in db.execute(
            "select start, end, correlationId, bytes, streamId from CUPTI_ACTIVITY_KIND_MEMSET"
        ):
            a = api.get(cid, (0, 0, "?", 0))
            work.append(GpuWork("memset", start, end, cid, "memset", "memset", a[0], a[1], a[2], stream, bytes=nbytes))
    work.sort(key=lambda w: w.api_start)

    gpu = db.execute(
        "select name, busLocation, uuid, smCount, clockRate, memoryBandwidth, l2CacheSize from TARGET_INFO_GPU where isDiscrete=1"
    ).fetchall()
    db.close()
    info = {
        "gpus": [
            {"name": g[0], "bus": g[1], "uuid": g[2], "sm_count": g[3], "clock_hz": g[4], "mem_bw_bytes_s": g[5], "l2_bytes": g[6]}
            for g in gpu
        ],
        "runtime_api_calls": len(api),
    }
    return phases, ops, work, info


def _has_table(db: sqlite3.Connection, name: str) -> bool:
    return db.execute("select 1 from sqlite_master where type='table' and name=?", (name,)).fetchone() is not None


def _parse_phase(text: str) -> tuple[str, int]:
    body = text[len(PHASE_PREFIX):]
    phase, _, iteration = body.partition("::iter=")
    return phase, int(iteration)


def _parse_op(text: str) -> tuple[str, int, str]:
    _, call_id, index, op_type = text.split("::")
    return call_id, int(index), op_type


def attribute(
    phases: list[Range], ops: list[Range], work: list[GpuWork], plan: dict[str, Any]
) -> tuple[list[Owner], list[GpuWork]]:
    """Launch-owned attribution of GPU work to operators and call overhead."""
    engine_of: dict[tuple[str, int], str] = {}
    call_order: list[str] = []
    for call in sorted(plan["calls"], key=lambda c: (c["wave"], c["index"])):
        call_order.append(call["call_id"])
        for op in call.get("mir_operators", []):
            engine_of[(call["call_id"], int(op["index"]))] = op["engine"]

    owners: list[Owner] = []
    unattributed: list[GpuWork] = []

    # Work index by api_start for range queries
    work_starts = [w.api_start for w in work]
    import bisect

    def work_in(start: int, end: int) -> list[GpuWork]:
        lo = bisect.bisect_left(work_starts, start)
        hi = bisect.bisect_right(work_starts, end)
        return work[lo:hi]

    op_index_by_phase: dict[int, list[Range]] = defaultdict(list)
    for op in ops:
        # find enclosing phase by time
        for i, ph in enumerate(phases):
            if ph.start <= op.start and op.end <= ph.end and ph.tid == op.tid:
                op_index_by_phase[i].append(op)
                break

    covered_cids: set[int] = set()
    for i, ph in enumerate(phases):
        phase, iteration = _parse_phase(ph.text)
        phase_ops = sorted(op_index_by_phase.get(i, []), key=lambda r: r.start)
        # operator-owned
        op_owners: list[Owner] = []
        for op in phase_ops:
            call_id, index, op_type = _parse_op(op.text)
            owner = Owner(phase, iteration, call_id, index, op_type, engine_of.get((call_id, index)), "nvtx_operator_range", op)
            for w in work_in(op.start, op.end):
                if w.correlation_id in covered_cids:
                    continue
                owner.work.append(w)
                covered_cids.add(w.correlation_id)
            op_owners.append(owner)
        owners.extend(op_owners)
        # call overhead: gaps inside the phase not covered by any operator range
        # Attribute a gap to the call whose first operator follows it; the tail
        # gap after the last operator belongs to the last call (D2H staging).
        cursor = ph.start
        boundaries: list[tuple[int, int, str, str]] = []
        for op in phase_ops:
            call_id, _, _ = _parse_op(op.text)
            if op.start > cursor:
                boundaries.append((cursor, op.start, call_id, "gap_before_operator"))
            cursor = max(cursor, op.end)
        if cursor < ph.end and phase_ops:
            last_call, _, _ = _parse_op(phase_ops[-1].text)
            boundaries.append((cursor, ph.end, last_call, "gap_after_last_operator"))
        gap_owner: dict[str, Owner] = {}
        for gstart, gend, call_id, basis in boundaries:
            for w in work_in(gstart, gend):
                if w.correlation_id in covered_cids:
                    continue
                key = call_id
                if key not in gap_owner:
                    gap_owner[key] = Owner(phase, iteration, call_id, None, "call_overhead", None, basis, None)
                gap_owner[key].work.append(w)
                covered_cids.add(w.correlation_id)
        owners.extend(gap_owner.values())

    for w in work:
        if w.correlation_id not in covered_cids:
            unattributed.append(w)
    return owners, unattributed


def _union_busy(intervals: list[tuple[int, int]]) -> int:
    if not intervals:
        return 0
    intervals.sort()
    total = 0
    cur_s, cur_e = intervals[0]
    for s, e in intervals[1:]:
        if s > cur_e:
            total += cur_e - cur_s
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)
    return total + (cur_e - cur_s)


def summarize(
    workload: str,
    phases: list[Range],
    owners: list[Owner],
    unattributed: list[GpuWork],
    work: list[GpuWork],
    out_dir: Path,
    metadata: dict[str, Any],
    info: dict[str, Any],
    sqlite_path: Path,
) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)

    # ---- per-instance attribution table
    inst_rows: list[dict[str, Any]] = []
    for o in owners:
        kernels = [w for w in o.work if w.kind == "kernel"]
        copies = [w for w in o.work if w.kind != "kernel"]
        gpu_ns = sum(w.duration for w in o.work)
        first_launch = min((w.api_start for w in o.work), default=None)
        first_gpu = min((w.start for w in o.work), default=None)
        last_gpu = max((w.end for w in o.work), default=None)
        inst_rows.append(
            {
                "workload": workload,
                "phase": o.phase,
                "iteration": o.iteration,
                "call_id": o.call_id,
                "op_index": o.op_index if o.op_index is not None else "",
                "op_type": o.op_type,
                "engine": o.engine or "",
                "attribution_basis": o.basis,
                "nvtx_cpu_ns": o.nvtx.duration if o.nvtx else "",
                "nvtx_start": o.nvtx.start if o.nvtx else "",
                "gpu_work_ns": gpu_ns,
                "kernel_ns": sum(w.duration for w in kernels),
                "memcpy_memset_ns": sum(w.duration for w in copies),
                "kernel_count": len(kernels),
                "memcpy_memset_count": len(copies),
                "launch_to_gpu_start_ns": (first_gpu - first_launch) if first_launch is not None and first_gpu is not None else "",
                "gpu_span_ns": (last_gpu - first_gpu) if first_gpu is not None and last_gpu is not None else "",
                "kernel_families": "|".join(sorted({w.family for w in o.work})),
                "kernel_names": "|".join(dict.fromkeys(w.name[:80] for w in o.work)),
            }
        )
    inst_rows.sort(key=lambda r: (r["phase"] != "measured", r["iteration"], r["nvtx_start"] or 0))
    _write_csv(out_dir / "operator_instance_attribution.csv", inst_rows)

    # ---- kernel-level table (every launch-owned GPU item with its owner)
    kern_rows: list[dict[str, Any]] = []
    for o in owners:
        for w in o.work:
            kern_rows.append(
                {
                    "workload": workload, "phase": o.phase, "iteration": o.iteration, "call_id": o.call_id,
                    "op_index": o.op_index if o.op_index is not None else "", "op_type": o.op_type,
                    "kind": w.kind, "family": w.family, "name": w.name, "correlation_id": w.correlation_id,
                    "api_name": w.api_name, "api_start": w.api_start, "api_end": w.api_end,
                    "gpu_start": w.start, "gpu_end": w.end, "gpu_ns": w.duration, "stream": w.stream,
                    "grid": "x".join(map(str, w.grid)), "block": "x".join(map(str, w.block)),
                    "registers": w.registers, "static_smem": w.static_smem, "dynamic_smem": w.dynamic_smem, "bytes": w.bytes,
                }
            )
    kern_rows.sort(key=lambda r: r["api_start"])
    _write_csv(out_dir / "gpu_work_attribution.csv", kern_rows)

    # ---- per-operator summary over measured iterations
    grouped: dict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for r in inst_rows:
        grouped[(r["phase"], r["call_id"], r["op_index"], r["op_type"], r["engine"])].append(r)
    summary_rows: list[dict[str, Any]] = []
    for (phase, call_id, op_index, op_type, engine), rows in sorted(grouped.items(), key=lambda kv: (kv[0][0] != "measured", str(kv[0][1]), kv[0][2] if kv[0][2] != "" else 999)):
        gpu = [r["gpu_work_ns"] for r in rows]
        cpu = [r["nvtx_cpu_ns"] for r in rows if r["nvtx_cpu_ns"] != ""]
        summary_rows.append(
            {
                "workload": workload, "phase": phase, "call_id": call_id, "op_index": op_index, "op_type": op_type, "engine": engine,
                "instances": len(rows),
                "gpu_ns_mean": round(statistics.mean(gpu), 1), "gpu_ns_median": statistics.median(gpu),
                "gpu_ns_min": min(gpu), "gpu_ns_max": max(gpu), "gpu_ns_stdev": round(statistics.pstdev(gpu), 1) if len(gpu) > 1 else 0,
                "nvtx_cpu_ns_mean": round(statistics.mean(cpu), 1) if cpu else "", "nvtx_cpu_ns_median": statistics.median(cpu) if cpu else "",
                "nvtx_cpu_ns_min": min(cpu) if cpu else "", "nvtx_cpu_ns_max": max(cpu) if cpu else "",
                "kernels_per_instance": round(statistics.mean(r["kernel_count"] for r in rows), 2),
                "gpu_over_cpu_pct": round(100 * statistics.mean(gpu) / statistics.mean(cpu), 1) if cpu and statistics.mean(cpu) else "",
                "kernel_families": rows[0]["kernel_families"],
            }
        )
    _write_csv(out_dir / "operator_summary.csv", summary_rows)

    # ---- per-iteration conservation
    iter_rows: list[dict[str, Any]] = []
    phase_lookup = {(_parse_phase(p.text)): p for p in phases}
    by_iter: dict[tuple[str, int], list[Owner]] = defaultdict(list)
    for o in owners:
        by_iter[(o.phase, o.iteration)].append(o)
    for (phase, iteration), ph in sorted(phase_lookup.items(), key=lambda kv: (kv[0][0] != "warmup", kv[0][1])):
        os_ = by_iter.get((phase, iteration), [])
        op_ns = sum(w.duration for o in os_ if o.op_index is not None for w in o.work)
        ovh_ns = sum(w.duration for o in os_ if o.op_index is None for w in o.work)
        all_work = [w for o in os_ for w in o.work]
        busy = _union_busy([(w.start, w.end) for w in all_work])
        wall = ph.duration
        iter_rows.append(
            {
                "workload": workload, "phase": phase, "iteration": iteration, "wall_ns": wall,
                "gpu_busy_union_ns": busy, "gpu_busy_pct": round(100 * busy / wall, 2) if wall else "",
                "operator_gpu_ns": op_ns, "call_overhead_gpu_ns": ovh_ns, "sum_attributed_gpu_ns": op_ns + ovh_ns,
                "kernel_launches": sum(1 for w in all_work if w.kind == "kernel"),
                "memcpy_memset": sum(1 for w in all_work if w.kind != "kernel"),
                "operator_nvtx_cpu_ns": sum(o.nvtx.duration for o in os_ if o.nvtx),
            }
        )
    _write_csv(out_dir / "iteration_conservation.csv", iter_rows)

    measured = [r for r in iter_rows if r["phase"] == "measured"]
    warm = [r for r in iter_rows if r["phase"] == "warmup"]
    measured_window = (min(p.start for p in phases if p.text.startswith(PHASE_PREFIX + "measured")),
                       max(p.end for p in phases if p.text.startswith(PHASE_PREFIX + "measured")))
    in_window = [w for w in work if measured_window[0] <= w.api_start <= measured_window[1]]
    attributed_cids = {w.correlation_id for o in owners for w in o.work}
    unattr_in_window = [w for w in in_window if w.correlation_id not in attributed_cids]

    def _s(rows: list[dict[str, Any]], key: str) -> dict[str, Any]:
        vals = [r[key] for r in rows]
        return {"mean": round(statistics.mean(vals), 1), "median": statistics.median(vals), "min": min(vals), "max": max(vals)}

    # per op_type totals over measured
    type_tot: dict[str, dict[str, float]] = defaultdict(lambda: {"gpu_ns": 0.0, "nvtx_cpu_ns": 0.0, "instances": 0, "kernels": 0})
    for r in inst_rows:
        if r["phase"] != "measured":
            continue
        t = type_tot[r["op_type"]]
        t["gpu_ns"] += r["gpu_work_ns"]
        t["nvtx_cpu_ns"] += r["nvtx_cpu_ns"] or 0
        t["instances"] += 1
        t["kernels"] += r["kernel_count"]
    measured_gpu_total = sum(t["gpu_ns"] for t in type_tot.values())
    measured_wall_total = sum(r["wall_ns"] for r in measured)
    type_rows = [
        {"workload": workload, "op_type": k, "instances": v["instances"], "kernel_launches": v["kernels"],
         "gpu_ns_total": v["gpu_ns"], "gpu_share_pct": round(100 * v["gpu_ns"] / measured_gpu_total, 2) if measured_gpu_total else "",
         "nvtx_cpu_ns_total": v["nvtx_cpu_ns"], "wall_share_pct": round(100 * v["nvtx_cpu_ns"] / measured_wall_total, 2) if measured_wall_total else "",
         "gpu_ns_per_instance": round(v["gpu_ns"] / v["instances"], 1) if v["instances"] else ""}
        for k, v in sorted(type_tot.items(), key=lambda kv: -kv[1]["gpu_ns"])
    ]
    _write_csv(out_dir / "op_type_breakdown.csv", type_rows)

    family_tot: dict[str, dict[str, float]] = defaultdict(lambda: {"ns": 0.0, "n": 0})
    for r in kern_rows:
        if r["phase"] == "measured":
            family_tot[r["family"]]["ns"] += r["gpu_ns"]
            family_tot[r["family"]]["n"] += 1
    family_rows = [
        {"workload": workload, "family": k, "instances": v["n"], "gpu_ns_total": v["ns"],
         "gpu_share_pct": round(100 * v["ns"] / measured_gpu_total, 2) if measured_gpu_total else ""}
        for k, v in sorted(family_tot.items(), key=lambda kv: -kv[1]["ns"])
    ]
    _write_csv(out_dir / "kernel_family_breakdown.csv", family_rows)

    conservation = {
        "schema_version": 1,
        "lineage": "h22-gpu-autotrace",
        "goal": "G01",
        "workload": workload,
        "sqlite": str(sqlite_path),
        "sqlite_sha256": _sha256(sqlite_path),
        "plan_sha256": metadata["plan_sha256"],
        "gpu": info["gpus"][0] if info["gpus"] else None,
        "iterations": {"warmup": len(warm), "measured": len(measured)},
        "measured_window_ns": measured_window[1] - measured_window[0],
        "measured": {
            "wall_ns_total": measured_wall_total,
            "wall_ns_per_iter": _s(measured, "wall_ns"),
            "gpu_busy_union_ns_total": sum(r["gpu_busy_union_ns"] for r in measured),
            "gpu_busy_pct_per_iter": _s(measured, "gpu_busy_pct"),
            "operator_gpu_ns_total": sum(r["operator_gpu_ns"] for r in measured),
            "call_overhead_gpu_ns_total": sum(r["call_overhead_gpu_ns"] for r in measured),
            "sum_attributed_gpu_ns_total": sum(r["sum_attributed_gpu_ns"] for r in measured),
            "unattributed_gpu_items_in_window": len(unattr_in_window),
            "unattributed_gpu_ns_in_window": sum(w.duration for w in unattr_in_window),
            "kernel_launches_total": sum(r["kernel_launches"] for r in measured),
            "operator_instances": sum(1 for r in inst_rows if r["phase"] == "measured" and r["op_index"] != ""),
            "expected_operator_instances": int(metadata["planned"]["mir_operators"]) * len(measured),
        },
        "warmup": {
            "wall_ns_per_iter": _s(warm, "wall_ns") if warm else None,
            "gpu_busy_pct_per_iter": _s(warm, "gpu_busy_pct") if warm else None,
            "first_iter_wall_ns": warm[0]["wall_ns"] if warm else None,
        },
        "global": {
            "total_gpu_items_in_trace": len(work),
            "unattributed_gpu_items_anywhere": len(unattributed),
            "unattributed_gpu_ns_anywhere": sum(w.duration for w in unattributed),
            "unattributed_examples": [w.name[:80] for w in unattributed[:5]],
        },
    }
    m = conservation["measured"]
    conservation["pass"] = (
        m["operator_instances"] == m["expected_operator_instances"]
        and m["unattributed_gpu_items_in_window"] == 0
        and m["sum_attributed_gpu_ns_total"] > 0
    )
    (out_dir / "conservation.json").write_text(json.dumps(conservation, indent=2, sort_keys=True) + "\n")
    _write_report(out_dir / "G01_OPERATOR_TRACE_REPORT.md", workload, conservation, summary_rows, type_rows, family_rows, iter_rows, metadata)
    return conservation


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _fmt_us(ns: float) -> str:
    return f"{ns / 1e3:,.1f}"


def _write_report(path: Path, workload: str, c: dict[str, Any], summary: list[dict[str, Any]], types: list[dict[str, Any]], families: list[dict[str, Any]], iters: list[dict[str, Any]], metadata: dict[str, Any]) -> None:
    m = c["measured"]
    w = c["warmup"]
    lines = [
        f"# G01 operator-wise single-GPU trace: `{workload}`",
        "",
        "Lineage `h22-gpu-autotrace`, workflow w01. Real execution on one RTX 4090",
        f"(`{c['gpu']['bus']}`), warmup {c['iterations']['warmup']} iterations discarded, "
        f"{c['iterations']['measured']} measured iterations. Attribution basis: NVTX operator range -> "
        "CUDA runtime API launched inside it -> CUPTI kernel/memcpy by correlationId.",
        "",
        "## Conservation",
        "",
        "| Quantity | Value |",
        "|---|---:|",
        f"| Operator instances observed / expected | {m['operator_instances']} / {m['expected_operator_instances']} |",
        f"| Measured wall per iteration (median) | {_fmt_us(m['wall_ns_per_iter']['median'])} us |",
        f"| GPU busy per iteration (median, union of GPU intervals) | {m['gpu_busy_pct_per_iter']['median']:.1f} % |",
        f"| Operator-owned GPU time (total over measured) | {_fmt_us(m['operator_gpu_ns_total'])} us |",
        f"| Call-overhead GPU time (weight init, H2D/D2H, staging) | {_fmt_us(m['call_overhead_gpu_ns_total'])} us |",
        f"| Unattributed GPU items inside measured window | {m['unattributed_gpu_items_in_window']} ({_fmt_us(m['unattributed_gpu_ns_in_window'])} us) |",
        f"| Kernel launches over measured iterations | {m['kernel_launches_total']} |",
        f"| Warmup iteration 0 wall | {_fmt_us(w['first_iter_wall_ns']) if w['first_iter_wall_ns'] else 'n/a'} us |",
        f"| Warmup GPU busy (median) | {w['gpu_busy_pct_per_iter']['median'] if w['gpu_busy_pct_per_iter'] else 'n/a'} % |",
        f"| Pass | {c['pass']} |",
        "",
        "## Operator-type breakdown (measured iterations)",
        "",
        "| op_type | instances | kernel launches | GPU total (us) | GPU share | NVTX CPU total (us) | wall share | GPU per instance (us) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for t in types:
        lines.append(
            f"| {t['op_type']} | {t['instances']} | {t['kernel_launches']} | {_fmt_us(t['gpu_ns_total'])} | {t['gpu_share_pct']} % | "
            f"{_fmt_us(t['nvtx_cpu_ns_total'])} | {t['wall_share_pct']} % | {_fmt_us(t['gpu_ns_per_instance']) if t['gpu_ns_per_instance'] != '' else ''} |"
        )
    lines += ["", "## Kernel-family breakdown (measured iterations)", "", "| family | instances | GPU total (us) | share |", "|---|---:|---:|---:|"]
    for f in families:
        lines.append(f"| {f['family']} | {f['instances']} | {_fmt_us(f['gpu_ns_total'])} | {f['gpu_share_pct']} % |")
    lines += ["", "## Per-operator summary (measured iterations)", "", "| call | idx | op_type | engine | GPU median (us) | GPU min/max (us) | NVTX CPU median (us) | GPU/CPU | kernels |", "|---|---:|---|---|---:|---:|---:|---:|---:|"]
    for s in summary:
        if s["phase"] != "measured":
            continue
        lines.append(
            f"| {s['call_id']} | {s['op_index']} | {s['op_type']} | {s['engine']} | {_fmt_us(s['gpu_ns_median'])} | "
            f"{_fmt_us(s['gpu_ns_min'])}/{_fmt_us(s['gpu_ns_max'])} | {_fmt_us(s['nvtx_cpu_ns_median']) if s['nvtx_cpu_ns_median'] != '' else ''} | "
            f"{s['gpu_over_cpu_pct']} % | {s['kernels_per_instance']} |"
        )
    lines += ["", "## Per-iteration conservation", "", "| phase | iter | wall (us) | GPU busy % | operator GPU (us) | overhead GPU (us) | launches |", "|---|---:|---:|---:|---:|---:|---:|"]
    for r in iters:
        lines.append(f"| {r['phase']} | {r['iteration']} | {_fmt_us(r['wall_ns'])} | {r['gpu_busy_pct']} | {_fmt_us(r['operator_gpu_ns'])} | {_fmt_us(r['call_overhead_gpu_ns'])} | {r['kernel_launches']} |")
    lines += [
        "",
        "## Reading notes",
        "",
        "- `GPU busy %` is the union of all GPU intervals launched inside the iteration divided by the iteration wall.",
        "  The remainder is host-side: Python dispatch, per-operator `cudaEventSynchronize`, CPU tool matmuls, pinned staging.",
        "- `GPU/CPU` per operator compares launch-owned GPU time to the NVTX CPU range, which encloses a synchronize.",
        "- Warmup rows are shown for context only; no measured statistic includes them.",
        f"- Plan `{metadata['plan_path']}` sha256 `{metadata['plan_sha256'][:16]}…`; sqlite sha256 `{c['sqlite_sha256'][:16]}…`.",
        "",
    ]
    path.write_text("\n".join(lines))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="w01 launch-owned operator attribution")
    parser.add_argument("--sqlite", type=Path, required=True)
    parser.add_argument("--run-metadata", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args(argv)

    metadata = json.loads(args.run_metadata.read_text())
    plan = json.loads(args.plan.read_text())
    workload = metadata["workload"]
    phases, ops, work, info = load_trace(args.sqlite)
    owners, unattributed = attribute(phases, ops, work, plan)
    conservation = summarize(workload, phases, owners, unattributed, work, args.output_dir, metadata, info, args.sqlite)
    m = conservation["measured"]
    print(json.dumps({"workload": workload, "pass": conservation["pass"], "operator_instances": m["operator_instances"],
                      "gpu_busy_pct_median": m["gpu_busy_pct_per_iter"]["median"], "unattributed_in_window": m["unattributed_gpu_items_in_window"],
                      "unattributed_anywhere": conservation["global"]["unattributed_gpu_items_anywhere"]}, indent=2))
    return 0 if conservation["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

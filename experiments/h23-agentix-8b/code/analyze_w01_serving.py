#!/usr/bin/env python3
"""w01' / G01 adapted to a serving engine: conservation denominator + concurrency windows.

Method adaptation (see experiments/h23-agentix-8b/protocol.md):

* The measured window is the client-side NVTX range ``agentix.window::measured``.
* vLLM's ``--enable-layerwise-nvtx-tracing`` was enabled but emits no per-module
  ranges under this execution mode (CUDA-graph path), so operator-level
  launch-ownership attribution is unavailable. Instead, GPU work is attributed:
    - by **kernel family** (what kind of work), and
    - by **request concurrency bucket** (how many requests the work was shared by),
      using the client-side request windows (``agentix.call_begin/end``).
  Both are partitions of the same GPU-busy interval set, so the conservation
  identity holds by construction: sum(buckets) == sum(families) == GPU busy.
* Under continuous batching one forward serves many requests, so a per-request
  kernel split stays undefined and is not attempted.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "h22-gpu-autotrace" / "code"))
from analyze_w01_operator_trace import GpuWork, _kernel_family, _sha256, _union_busy, _write_csv  # noqa: E402

WINDOW_PREFIX = "agentix.window::"
CALL_BEGIN = "agentix.call_begin::"
CALL_END = "agentix.call_end::"
BUCKETS = [(1, 1, "1"), (2, 3, "2-3"), (4, 7, "4-7"), (8, 15, "8-15"), (16, 31, "16-31"), (32, 10**9, "32+")]


def load_nvtx(path: Path) -> list[tuple[int, int, str, int]]:
    db = sqlite3.connect(str(path))
    strings = dict(db.execute("select id, value from StringIds"))
    out = []
    for start, end, text, text_id, gtid in db.execute("select start, end, text, textId, globalTid from NVTX_EVENTS"):
        out.append((start, end or start, text if text else strings.get(text_id, ""), gtid))
    db.close()
    out.sort(key=lambda r: r[0])
    return out


def load_work(path: Path) -> list[GpuWork]:
    db = sqlite3.connect(str(path))
    strings = dict(db.execute("select id, value from StringIds"))
    api: dict[int, tuple[int, int, str, int]] = {}
    for start, end, cid, name_id, tid in db.execute(
        "select start, end, correlationId, nameId, globalTid from CUPTI_ACTIVITY_KIND_RUNTIME"
    ):
        api[cid] = (start, end, strings.get(name_id, str(name_id)), tid)
    work: list[GpuWork] = []
    for row in db.execute(
        "select start, end, correlationId, demangledName, streamId, gridX, gridY, gridZ, blockX, blockY, blockZ from "
        "CUPTI_ACTIVITY_KIND_KERNEL"
    ):
        start, end, cid, name_id, stream = row[:5]
        a = api.get(cid, (0, 0, "?", 0))
        name = strings.get(name_id, str(name_id))
        work.append(GpuWork("kernel", start, end, cid, name, _kernel_family(name), a[0], a[1], a[2], stream,
                            grid=tuple(row[5:8]), block=tuple(row[8:11])))
    for start, end, cid, nbytes, kind, stream in db.execute(
        "select start, end, correlationId, bytes, copyKind, streamId from CUPTI_ACTIVITY_KIND_MEMCPY"
    ):
        a = api.get(cid, (0, 0, "?", 0))
        work.append(GpuWork("memcpy", start, end, cid, f"memcpy_{kind}", "memcpy", a[0], a[1], a[2], stream, bytes=nbytes))
    try:
        for start, end, cid, nbytes, stream in db.execute(
            "select start, end, correlationId, bytes, streamId from CUPTI_ACTIVITY_KIND_MEMSET"
        ):
            a = api.get(cid, (0, 0, "?", 0))
            work.append(GpuWork("memset", start, end, cid, "memset", "memset", a[0], a[1], a[2], stream, bytes=nbytes))
    except sqlite3.Error:
        pass
    db.close()
    work.sort(key=lambda w: w.api_start)
    return work


def concurrency_at(t: int, starts: list[int], ends: list[int]) -> int:
    import bisect

    return bisect.bisect_right(starts, t) - bisect.bisect_right(ends, t)


def main() -> int:
    ap = argparse.ArgumentParser(description="w01' serving-adapted conservation + concurrency windows")
    ap.add_argument("--sqlite", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--label", default="serving")
    a = ap.parse_args()
    a.output_dir.mkdir(parents=True, exist_ok=True)

    nvtx = load_nvtx(a.sqlite)
    work = load_work(a.sqlite)
    windows = [r for r in nvtx if r[2].startswith(WINDOW_PREFIX)]
    if not windows:
        raise SystemExit("no agentix.window::measured range; was --nvtx on?")
    win = max(windows, key=lambda r: r[1] - r[0])
    begins = [(r[0], r[2][len(CALL_BEGIN):]) for r in nvtx if r[2].startswith(CALL_BEGIN)]
    ends = {r[2][len(CALL_END):]: r[0] for r in nvtx if r[2].startswith(CALL_END)}
    calls = sorted((s, ends[k]) for s, k in begins if k in ends and ends[k] > s)

    # nsys in this container stops recording CUDA activity partway through the
    # run (verified reproducible with multiprocessing disabled and with a CUDA
    # flush interval set), so the analysed interval is the measured window
    # intersected with the captured CUDA span. Both bounds are reported.
    captured = (min(w.start for w in work), max(w.end for w in work)) if work else (win[0], win[1])
    span = (max(win[0], captured[0]), min(win[1], captured[1]))
    in_window = [w for w in work if w.end > span[0] and w.start < span[1]]
    busy = _union_busy([(max(w.start, span[0]), min(w.end, span[1])) for w in in_window])

    starts, ends_sorted = [c[0] for c in calls], sorted(c[1] for c in calls)

    # family partition
    fam: dict[str, dict[str, Any]] = defaultdict(lambda: {"ns": 0, "items": 0})
    for w in in_window:
        fam[w.family]["ns"] += min(w.end, span[1]) - max(w.start, span[0])
        fam[w.family]["items"] += 1
    fam_rows = [{"label": a.label, "family": k, "items": v["items"], "gpu_ns": v["ns"],
                 "gpu_share_pct": round(100 * v["ns"] / busy, 2) if busy else 0}
                for k, v in sorted(fam.items(), key=lambda kv: -kv[1]["ns"])]
    _write_csv(a.output_dir / "kernel_family_breakdown.csv", fam_rows)

    # concurrency partition: split each GPU item at request window edges
    edges = sorted({win[0], win[1]} | {c[0] for c in calls} | {c[1] for c in calls})
    bucket_ns: dict[str, int] = defaultdict(int)
    bucket_fam: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for w in in_window:
        s, e = max(w.start, span[0]), min(w.end, span[1])
        # collect cover edges inside [s, e]
        import bisect

        lo = bisect.bisect_right(edges, s)
        hi = bisect.bisect_left(edges, e)
        points = [s] + [edges[i] for i in range(lo, hi)] + [e]
        for p0, p1 in zip(points, points[1:]):
            if p1 <= p0:
                continue
            c = concurrency_at(p0, starts, ends_sorted)
            label = next((n for lo_, hi_, n in BUCKETS if lo_ <= c <= hi_), "0")
            bucket_ns[label] += p1 - p0
            bucket_fam[label][w.family] += p1 - p0
    order = [n for _, _, n in BUCKETS]
    bucket_rows = [{"label": a.label, "concurrent_requests": n, "gpu_ns": bucket_ns.get(n, 0),
                    "gpu_share_pct": round(100 * bucket_ns.get(n, 0) / busy, 2) if busy else 0,
                    "top_families": ";".join(f"{f}:{round(100 * v / bucket_ns[n], 1)}%"
                                             for f, v in sorted(bucket_fam.get(n, {}).items(), key=lambda kv: -kv[1])[:4])}
                   for n in ["0"] + order if bucket_ns.get(n)]
    _write_csv(a.output_dir / "concurrency_windows.csv", bucket_rows)

    # ---- phase partition (launch ownership), available when the worker was run
    # with VLLM_NVTX_SCOPES_FOR_PROFILING=1 and the V1 model runner: kernels are
    # attributed to the innermost worker-side scope range whose thread launched
    # them and whose interval contains the CUDA API start — the original
    # AutoTrace rule, restored at engine-phase granularity.
    scope_ranges = [r for r in nvtx if (r[2].startswith("gpu_model_runner:") or r[2].startswith("schedule:")) and r[1] > r[0]]
    phase_rows = []
    phase_unattributed = 0
    if scope_ranges:
        from collections import defaultdict as _dd
        by_thread: dict[int, list[tuple[int, int, str]]] = _dd(list)
        for st, en, txt, tid in scope_ranges:
            by_thread[tid].append((st, en, txt))
        for rs in by_thread.values():
            rs.sort()
        thread_starts = {tid: [r[0] for r in rs] for tid, rs in by_thread.items()}
        api_by_cid = {}  # already inside GpuWork (api_start, api_tid unavailable) -> reload
        db2 = sqlite3.connect(str(a.sqlite))
        api_tid = {cid: tid for _, _, cid, tid in db2.execute(
            "select start, end, correlationId, globalTid from CUPTI_ACTIVITY_KIND_RUNTIME")}
        db2.close()
        phase_ns: dict[str, int] = _dd(int)
        phase_items: dict[str, int] = _dd(int)
        import bisect as _bs
        for w in in_window:
            tid = api_tid.get(w.correlation_id)
            best = None
            rs = by_thread.get(tid)
            if rs:
                # scopes are (near-)sequential per thread; walk back a bounded
                # number of entries from the bisect point to find the innermost
                # containing range
                i = _bs.bisect_right(thread_starts[tid], w.api_start) - 1
                for j in range(i, max(-1, i - 64), -1):
                    st, en, txt = rs[j]
                    if st <= w.api_start <= en and (best is None or en - st < best[1] - best[0]):
                        best = (st, en, txt)
            spanw = min(w.end, span[1]) - max(w.start, span[0])
            if best is None:
                phase_unattributed += spanw
            else:
                phase_ns[best[2][:50]] += spanw
                phase_items[best[2][:50]] += 1
        phase_rows = [{"label": a.label, "phase": k, "items": phase_items[k], "gpu_ns": v,
                       "gpu_share_pct": round(100 * v / busy, 2) if busy else 0}
                      for k, v in sorted(phase_ns.items(), key=lambda kv: -kv[1])]
        phase_rows.append({"label": a.label, "phase": "<unattributed>", "items": 0, "gpu_ns": phase_unattributed,
                           "gpu_share_pct": round(100 * phase_unattributed / busy, 2) if busy else 0})
        _write_csv(a.output_dir / "phase_attribution.csv", phase_rows)

    event_counts = sorted([(c[0], 1) for c in calls] + [(c[1], -1) for c in calls])
    cur = peak = 0
    for _, d in event_counts:
        cur += d
        peak = max(peak, cur)

    summary = {
        "schema_version": 1, "lineage": "h23-agentix-8b/autotrace", "goal": "G01'", "label": a.label,
        "sqlite": str(a.sqlite), "sqlite_sha256": _sha256(a.sqlite),
        "measured_window_ns": win[1] - win[0],
        "captured_cuda_span_ns": captured[1] - captured[0],
        "analysed_span_ns": span[1] - span[0],
        "analysed_span_is_truncated": (span[1] - span[0]) < (win[1] - win[0]),
        "gpu_busy_ns": busy,
        "gpu_busy_pct": round(100 * busy / (span[1] - span[0]), 2),
        "kernel_items_in_window": len(in_window),
        "operator_attribution": "phase-level launch ownership available when worker scopes present (see phase_attribution); per-layer module NVTX remains unavailable in this vLLM build",
        "requests": {"count": len(calls), "peak_concurrent": peak},
        "family_conservation_err_ns": sum(v["ns"] for v in fam.values()) - busy,
        "concurrency_conservation_err_ns": sum(bucket_ns.values()) - busy,
        "phase_attribution": ({"available": True,
                               "phases": {r["phase"]: r["gpu_share_pct"] for r in phase_rows[:8]},
                               "conservation_err_ns": sum(r["gpu_ns"] for r in phase_rows) - busy}
                              if phase_rows else {"available": False,
                                                  "reason": "no worker-side scopes; run with VLLM_NVTX_SCOPES_FOR_PROFILING=1 and VLLM_USE_V2_MODEL_RUNNER=0"}),
        "families": {r["family"]: r["gpu_share_pct"] for r in fam_rows[:9]},
        "pass": bool(busy > 0 and fam_rows),
    }
    summary["conservation_err_ns"] = max(abs(summary["family_conservation_err_ns"]), abs(summary["concurrency_conservation_err_ns"]))
    (a.output_dir / "w01_serving_conservation.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: summary[k] for k in ("label", "gpu_busy_pct", "analysed_span_is_truncated", "requests", "conservation_err_ns", "families", "phase_attribution", "pass")}, indent=2))
    return 0 if summary["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

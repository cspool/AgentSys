#!/usr/bin/env python3
"""R10 final report, four-arm edition — REPLACES the 3-model pair edition.

Universe: LLaMA-3.1-8B, thr_mixed r0.5, cap16, four traced arms
(vLLM素 / vLLM-opt FCFS / MLFQ调用级 / agentix_core). Style, outline and figure
geometry follow the frozen skill (workflow06/skill) and reuse the pair-edition
template constants; every figure and number here is rebuilt from the NEW
captures. The pair edition remains in git history.

Core fix this edition carries: the end-to-end lanes now draw THREE quantities
separately — 等待 (submit→首token, red), busy (quantum 段真实执行, class color),
驻留中的再排队 (quantum-requeue gaps inside the residence, pale red) — so the
"scheduling must not change execution" invariant is checkable in the figure
itself instead of being contradicted by a conflated 彩段.
"""
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import statistics
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from build_r10_summary_doc import (  # noqa: E402
    CLS_COLOR, WAIT, W, LEFT, RIGHT, load_calls, pick_wait_window, axis, fig,
    hl_strip, cu_strip, compo_section, char_art, class_lifecycle_figs,
    call_top_pile, call_pile_strip, kernel_micro_best, kernel_micro_strip,
    paper_fig)

REQUEUE = "#e4b6b6"          # residence-requeue (pale red, distinct from wait)
ARM_COLOR = {"plain": "#6b7280", "opt": "#1f2f45", "mlfq": "#a8541f", "core": "#2f6f9f",
             "S": "#1f7a4f", "R": "#8a4f9f"}

ARMS = [
    ("plain", "vLLM 素（无前缀缓存/无分块预填充）", "vllm_plain_cap16", "payload_vllm_plain_cap16.json"),
    ("opt",   "vLLM-opt（FCFS）",                    "llama_fcfs_cap16", "payload_llama_fcfs_cap16.json"),
    ("mlfq",  "MLFQ（调用级）",                      "mlfq_call_cap16",  "payload_mlfq_call_cap16.json"),
    ("core",  "agentix_core（程序级）",              "llama_core_cap16", "payload_llama_core_cap16.json"),
]


# ---------------------------------------------------------------- chunk layer
def load_chunks(capdir: Path, calls):
    """Per-call quantum segments from the arm's own NVTX chunk marks,
    aligned to run-relative ms via the call_begin marks."""
    db = sqlite3.connect(str(capdir / "cap.sqlite"))
    rows = db.execute(
        "select start, text from NVTX_EVENTS where text like 'agentix.c%'").fetchall()
    db.close()
    subs = {(c["program_id"], c["call_index"]): c["submitted_rel_ms"] for c in calls}
    offs, beg, end = [], {}, {}
    for ts, txt in rows:
        p = (txt or "").split("::")
        if p[0] == "agentix.call_begin" and len(p) >= 3 and (p[1], int(p[2])) in subs:
            offs.append(ts - subs[(p[1], int(p[2]))] * 1e6)
        elif p[0] == "agentix.chunk_begin" and len(p) >= 4:
            beg[(p[1], int(p[2]), int(p[3]))] = (ts, p[4] if len(p) > 4 else "")
        elif p[0] == "agentix.chunk_end" and len(p) >= 4:
            end[(p[1], int(p[2]), int(p[3]))] = ts
    if not offs:
        return {}
    off = statistics.median(offs)
    ch = defaultdict(list)
    for k, (b, q) in beg.items():
        e = end.get(k)
        if e and e > b:
            ch[(k[0], k[1])].append(((b - off) / 1e6, (e - off) / 1e6, q))
    for v in ch.values():
        v.sort()
    return dict(ch)


def seg_union_ms(segs, lo, hi):
    """Union of [b,e] clipped to [lo,hi] — chunk marks can overlap the wait."""
    iv = sorted((max(b, lo), min(e, hi)) for b, e, _ in segs)
    merged = []
    for b, e in iv:
        if e <= b:
            continue
        if merged and b <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([b, e])
    return sum(e - b for b, e in merged)


def tri_stats(calls, chunks):
    """Mean 等待 / 引擎内 quantum 段 / quantum 间再排队 per class (ms per call)."""
    per = defaultdict(lambda: {"wait": [], "engine": [], "requeue": []})
    for c in calls:
        k = (c["program_id"], c["call_index"])
        ft, fin = c["first_token_rel_ms"], c["finished_rel_ms"]
        w = ft - c["submitted_rel_ms"]
        res = fin - ft
        segs = chunks.get(k)
        eng = seg_union_ms(segs, ft, fin) if segs else res
        per[c["class"]]["wait"].append(w)
        per[c["class"]]["engine"].append(eng)
        per[c["class"]]["requeue"].append(max(res - eng, 0.0))
    return {cls: {m: sum(v[m]) / len(v[m]) for m in v} for cls, v in per.items()}


# ------------------------------------------------------------ e2e trichotomy
def e2e_strip_tri(calls, chunks, w0, w1, y0, tag, color):
    lanes = {}
    for c in calls:
        lanes.setdefault(c["program_id"], {"cls": c["class"], "cs": []})["cs"].append(c)
    order = sorted(lanes.items(), key=lambda kv: (
        {"bfcl": 0, "sharegpt": 1, "lats": 2}[kv[1]["cls"]],
        min(x["submitted_rel_ms"] for x in kv[1]["cs"])))
    rh = 9
    out = [f'<text x="4" y="{y0+10}" font-size="20" font-weight="600" fill="{color}">{tag}</text>']
    X = lambda t: LEFT + (W - LEFT - RIGHT) * (max(min(t, w1), w0) - w0) / (w1 - w0)
    for i, (pid, ln) in enumerate(order):
        y = y0 + 16 + i * rh
        out.append(f'<text x="{LEFT-6}" y="{y+7}" font-size="14" text-anchor="end" fill="#8fa2b6">{pid}·{ln["cls"]}</text>')
        for c in ln["cs"]:
            if c["finished_rel_ms"] < w0 or c["submitted_rel_ms"] > w1:
                continue
            ft, fin = c["first_token_rel_ms"], c["finished_rel_ms"]
            x0, x1, x2 = X(c["submitted_rel_ms"]), X(ft), X(fin)
            if x1 > x0:
                out.append(f'<rect x="{x0:.1f}" y="{y+1}" width="{max(x1-x0,0.5):.1f}" height="6" fill="{WAIT}" opacity=".85"/>')
            segs = chunks.get((pid, c["call_index"]))
            if segs:
                # residence backdrop = requeue color; busy quanta drawn on top
                out.append(f'<rect x="{x1:.1f}" y="{y+1}" width="{max(x2-x1,0.5):.1f}" height="6" fill="{REQUEUE}" opacity=".9"/>')
                for b, e, _q in segs:
                    b, e = max(b, ft), min(e, fin)
                    if e <= b:
                        continue
                    out.append(f'<rect x="{X(b):.1f}" y="{y+1}" width="{max(X(e)-X(b),0.5):.1f}" height="6" fill="{CLS_COLOR[ln["cls"]]}"/>')
            else:
                out.append(f'<rect x="{x1:.1f}" y="{y+1}" width="{max(x2-x1,0.5):.1f}" height="6" fill="{CLS_COLOR[ln["cls"]]}" opacity=".9"/>')
    return out, y0 + 16 + len(order) * rh + 6


def e2e_program_blocks(C, CH, arm_meta, floor, rh=12, bh=8):
    """一 (v2): per-program compact blocks — the SAME program's four arm rows
    packed adjacently, each program on its OWN busiest window (no shared axis).
    Window rule: whole lifetime (union over arms) if ≤40 s, else the densest
    30 s by call activity across the four arms."""
    by_arm = {k: defaultdict(list) for k, *_ in arm_meta}
    for k, *_ in arm_meta:
        for c in C[k]:
            by_arm[k][c["program_id"]].append(c)
    pids = sorted(by_arm[arm_meta[0][0]],
                  key=lambda p: ({"bfcl": 0, "sharegpt": 1, "lats": 2}
                                 [by_arm[arm_meta[0][0]][p][0]["class"]],
                                 min(c["submitted_rel_ms"] for c in by_arm[arm_meta[0][0]][p])))
    SHORT = {"plain": "素", "opt": "opt", "mlfq": "M", "core": "C", "S": "S", "R": "R"}
    # class-aggregate wait (paper metric) per arm, for the header rows
    cls_wait = {}
    for k, *_ in arm_meta:
        agg = {}
        for pid2, cs2 in by_arm[k].items():
            c0 = cs2[0]["class"]
            agg.setdefault(c0, []).append(sum(
                (c["finished_rel_ms"] - c["submitted_rel_ms"]) - floor[(pid2, c["call_index"])]
                for c in cs2))
        cls_wait[k] = {c2: sum(v) / len(v) for c2, v in agg.items()}
    cls_ptl, tot_wait, all_ptl = {}, {}, {}
    for k, *_ in arm_meta:
        aggp, tw, ap = {}, 0.0, []
        for pid2, cs2 in by_arm[k].items():
            c0 = cs2[0]["class"]
            span = max(c["finished_rel_ms"] for c in cs2) - min(c["submitted_rel_ms"] for c in cs2)
            tok = max(sum(max(c["produced_tokens"], 1) for c in cs2), 1)
            aggp.setdefault(c0, []).append(span / tok)
            ap.append(span / tok)
            tw += sum((c["finished_rel_ms"] - c["submitted_rel_ms"]) - floor[(pid2, c["call_index"])]
                      for c in cs2)
        cls_ptl[k] = {c2: sum(v) / len(v) for c2, v in aggp.items()}
        tot_wait[k] = tw
        all_ptl[k] = sum(ap) / len(ap)
    seen_cls = set()
    out, y = [], 8
    windows = {}
    for pid in pids:
        _cls0 = by_arm[arm_meta[0][0]][pid][0]["class"]
        if not seen_cls:
            # overall banner: the two metrics head-to-head
            _tw = {k: tot_wait[k] for k, *_ in arm_meta}
            _pt = {k: all_ptl[k] for k, *_ in arm_meta}
            _wtw = min(_tw, key=lambda k: _tw[k]); _wpt = min(_pt, key=lambda k: _pt[k])
            _l1 = "　".join((f'<tspan font-weight="700" fill="#c94040">{SHORT[k]} {v/1e3:,.0f}s</tspan>'
                            if k == _wtw else f'{SHORT[k]} {v/1e3:,.0f}s') for k, v in _tw.items())
            _l2 = "　".join((f'<tspan font-weight="700" fill="#c94040">{SHORT[k]} {v:.1f}</tspan>'
                            if k == _wpt else f'{SHORT[k]} {v:.1f}') for k, v in _pt.items())
            out.append(f'<rect x="0" y="{y}" width="{W}" height="46" fill="#e8f0e6"/>')
            out.append(f'<text x="6" y="{y+17}" font-size="16" fill="#1f5f3f">全体 '
                       f'{len(by_arm[arm_meta[0][0]])} 程序 · Σ等待（call 加权总量）：' + _l1 + '</text>')
            out.append(f'<text x="6" y="{y+38}" font-size="16" fill="#1f5f3f">'
                       f'论文指标 · 程序延迟 mean（程序等权 ms/tok）：' + _l2 + '</text>')
            y += 52
        if _cls0 not in seen_cls:
            seen_cls.add(_cls0)
            _vals = {k: cls_wait[k].get(_cls0, 0.0) for k, *_ in arm_meta}
            _pv = {k: cls_ptl[k].get(_cls0, 0.0) for k, *_ in arm_meta}
            _wink = min(_vals, key=lambda k: _vals[k])
            _wpt2 = min(_pv, key=lambda k: _pv[k])
            _parts = []
            for k, v in _vals.items():
                seg2 = SHORT[k] + " " + f"{v/1e3:.1f}" + "s"
                if k == _wink:
                    seg2 = '<tspan font-weight="700" fill="#c94040">' + seg2 + '</tspan>'
                _parts.append(seg2)
            _parts2 = []
            for k, v in _pv.items():
                seg3 = SHORT[k] + " " + f"{v:.1f}"
                if k == _wpt2:
                    seg3 = '<tspan font-weight="700" fill="#c94040">' + seg3 + '</tspan>'
                _parts2.append(seg3)
            out.append(f'<rect x="0" y="{y}" width="{W}" height="46" fill="#eef4fa"/>')
            out.append(f'<text x="6" y="{y+17}" font-size="16" fill="#2f6f9f">'
                       f'{_cls0} · 等待均值/程序：' + '　'.join(_parts) + '</text>')
            out.append(f'<text x="6" y="{y+38}" font-size="16" fill="#2f6f9f">'
                       f'{_cls0} · 论文指标 程序延迟 ms/tok：' + '　'.join(_parts2) + '</text>')
            y += 52
        allc = [c for k, *_ in arm_meta for c in by_arm[k][pid]]
        cls = allc[0]["class"]
        t0 = min(c["submitted_rel_ms"] for c in allc)
        t1 = max(c["finished_rel_ms"] for c in allc)
        if t1 - t0 > 40e3:
            width, step, best, b0 = 30e3, 5e3, -1.0, t0
            t = t0
            while t + width <= t1 + step:
                act = sum(max(0.0, min(c["finished_rel_ms"], t + width) - max(c["submitted_rel_ms"], t))
                          for c in allc)
                if act > best:
                    best, b0 = act, t
                t += step
            w0, w1 = b0, b0 + width
        else:
            pad = max((t1 - t0) * 0.02, 50.0)
            w0, w1 = t0 - pad, t1 + pad
        windows[pid] = [w0 / 1e3, w1 / 1e3]
        ncalls = len(by_arm[arm_meta[0][0]][pid])
        # per-arm annotations: TOTAL program wait (Σ submit→first-token) and
        # program token latency (response / produced tokens) — the global-
        # service metric that decides the bold row
        wsum, ptl = {}, {}
        for key, *_ in arm_meta:
            cs = by_arm[key][pid]
            # PAPER-METRIC wait: per-call non-execution time = call e2e minus
            # the call's execution floor (min residence across the four arms),
            # summed over the program. Additive, >=0, parallel-safe — the
            # same accounting as Fig.17's Wait (requeue counts as waiting).
            wsum[key] = sum(
                (c["finished_rel_ms"] - c["submitted_rel_ms"])
                - floor[(pid, c["call_index"])]
                for c in cs)
            span = max(c["finished_rel_ms"] for c in cs) - min(c["submitted_rel_ms"] for c in cs)
            ptl[key] = span / max(sum(max(c["produced_tokens"], 1) for c in cs), 1)
        pmin = min(ptl.values())
        wmin = min(wsum.values())
        out.append(f'<text x="4" y="{y+15}" font-size="17" font-weight="600" fill="#1f2f45">'
                   f'{pid}·{cls}·{ncalls} 调用 · 窗 [{w0/1e3:.1f}, {w1/1e3:.1f}] s（宽 {(w1-w0)/1e3:.1f} s）</text>')
        y += 22
        R2 = 185   # right margin reserved for the per-arm annotations
        X = lambda t: LEFT + (W - LEFT - R2) * (max(min(t, w1), w0) - w0) / (w1 - w0)
        for key, _lab, *_ in arm_meta:
            out.append(f'<text x="{LEFT-6}" y="{y+bh+1}" font-size="15" text-anchor="end" '
                       f'fill="{ARM_COLOR[key]}">{SHORT[key]}</text>')
            best = wsum[key] <= wmin + 1e-9
            out.append(f'<text x="{W-6}" y="{y+bh+1}" font-size="{14 if best else 13}" '
                       f'text-anchor="end" fill="{ARM_COLOR[key] if best else "#8fa2b6"}"'
                       f'{" font-weight=\"700\"" if best else ""}>等 {wsum[key]/1e3:,.1f}s · '
                       f'{ptl[key]:,.0f}ms/tok</text>')
            for c in by_arm[key][pid]:
                if c["finished_rel_ms"] < w0 or c["submitted_rel_ms"] > w1:
                    continue
                ft, fin = c["first_token_rel_ms"], c["finished_rel_ms"]
                x0, x1, x2 = X(c["submitted_rel_ms"]), X(ft), X(fin)
                if x1 > x0:
                    out.append(f'<rect x="{x0:.1f}" y="{y+1}" width="{max(x1-x0,0.5):.1f}" height="{bh}" fill="{WAIT}" opacity=".85"/>')
                segs = CH[key].get((pid, c["call_index"]))
                if segs:
                    out.append(f'<rect x="{x1:.1f}" y="{y+1}" width="{max(x2-x1,0.5):.1f}" height="{bh}" fill="{REQUEUE}" opacity=".9"/>')
                    for b, e, _q in segs:
                        b, e = max(b, ft), min(e, fin)
                        if e <= b:
                            continue
                        out.append(f'<rect x="{X(b):.1f}" y="{y+1}" width="{max(X(e)-X(b),0.5):.1f}" height="{bh}" fill="{CLS_COLOR[cls]}"/>')
                else:
                    out.append(f'<rect x="{x1:.1f}" y="{y+1}" width="{max(x2-x1,0.5):.1f}" height="{bh}" fill="{CLS_COLOR[cls]}" opacity=".9"/>')
            y += rh
        out.append(f'<line x1="{LEFT}" y1="{y+4}" x2="{W-RIGHT}" y2="{y+4}" stroke="#eef2ee"/>')
        y += 12
    return out, y, windows


# ------------------------------------------------------------------ DFG (W6)
DFG_TOP = [
    ("schedule", "w.sched: schedule_total"),
    ("prepare_inputs", "w.run: prepare_inputs"),
    ("forward", "gpu_model_runner: forward"),
    ("sample", "gpu_model_runner: sample"),
    ("postprocess", "gpu_model_runner: postprocess"),
    ("async 出口", "gpu_model_runner: AsyncGPUModelRunnerOutput"),
]
DFG_BOT = [
    ("update_from_output", "w.sched: update_from_output"),
    ("process_outputs", "w.engine: process_outputs"),
]


def dfg_fig(w2, arm_label):
    ranked = {r["process"]: r for r in w2["ranked_processes"]}
    bounds = {b["boundary"]: b for b in w2["dominant_idle_boundaries"]}
    async_gap = next((b for k, b in bounds.items() if "set_async" in k), None)
    bw, bh, gap = 158, 74, 14
    parts = [f'<text x="4" y="20" font-size="19" font-weight="600" fill="#1f2f45">'
             f'W6 · 引擎步 stage 的 DFG（节点 = 运行时 stage，非算子 process；节点数字 = {arm_label} 实测：调用次数 / 时间和）</text>']
    def box(x, y, name, key):
        r = ranked.get(key)
        num = f'{r["count"]:,} 次 / {r["union_ns"]/1e9:.1f} s' if r else "—"
        return (f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="7" fill="#f2f7fb" stroke="#8fb2ce"/>'
                f'<text x="{x+bw/2}" y="{y+28}" font-size="15" text-anchor="middle" fill="#1f2f45">{name}</text>'
                f'<text x="{x+bw/2}" y="{y+52}" font-size="14" text-anchor="middle" fill="#48607d">{num}</text>')
    y_top, y_bot = 44, 210
    xs = [LEFT - 90 + i * (bw + gap) for i in range(len(DFG_TOP))]
    for x, (name, key) in zip(xs, DFG_TOP):
        parts.append(box(x, y_top, name, key))
    for i in range(len(xs) - 1):
        parts.append(f'<line x1="{xs[i]+bw}" y1="{y_top+bh/2}" x2="{xs[i+1]}" y2="{y_top+bh/2}" stroke="#48607d" stroke-width="1.6" marker-end="url(#arr)"/>')
    xb = [xs[3], xs[1]]
    for x, (name, key) in zip(xb, DFG_BOT):
        parts.append(box(x, y_bot, name, key))
    # async boundary edge (the report's dominant idle)
    ag = f'{async_gap["sum_ns"]/1e9:.0f} s / {async_gap["count"]:,} 次 / 均 {async_gap["mean_ms"]:.1f} ms' if async_gap else "—"
    parts.append(f'<path d="M{xs[-1]+bw/2} {y_top+bh} C {xs[-1]+bw/2} {y_bot-20}, {xb[0]+bw+70} {y_bot-40}, {xb[0]+bw} {y_bot+bh/2}" fill="none" stroke="{WAIT}" stroke-width="2.2" stroke-dasharray="7 4" marker-end="url(#arrR)"/>')
    parts.append(f'<text x="{xs[-1]-40}" y="{y_bot-28}" font-size="15" fill="{WAIT}">async 输出等待（GPU 已出结果、host 未消费）：{ag}</text>')
    parts.append(f'<line x1="{xb[0]}" y1="{y_bot+bh/2}" x2="{xb[1]+bw}" y2="{y_bot+bh/2}" stroke="#48607d" stroke-width="1.6" marker-end="url(#arr)"/>')
    # loop back
    parts.append(f'<path d="M{xb[1]} {y_bot+bh/2} C {xs[0]-40} {y_bot+bh/2}, {xs[0]-40} {y_top+bh/2}, {xs[0]} {y_top+bh/2}" fill="none" stroke="#8fa2b6" stroke-width="1.4" stroke-dasharray="3 4" marker-end="url(#arr)"/>')
    parts.append(f'<text x="{xs[0]-36}" y="{(y_top+y_bot)/2+30}" font-size="14" fill="#8fa2b6">下一步</text>')
    defs = ('<defs><marker id="arr" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto">'
            '<path d="M0 0L9 4.5L0 9Z" fill="#48607d"/></marker>'
            '<marker id="arrR" markerWidth="9" markerHeight="9" refX="8" refY="4.5" orient="auto">'
            f'<path d="M0 0L9 4.5L0 9Z" fill="{WAIT}"/></marker></defs>')
    return fig([defs] + parts, y_bot + bh + 22)


# ----------------------------------------------------------------------- doc
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--art", type=Path, required=True, help="artifacts/agentix_8b")
    ap.add_argument("--scratch", type=Path, required=True)
    ap.add_argument("--fourarm", type=Path, required=True,
                    help="endpoint chapter fragment from build_r10_fourarm_chapter.py")
    ap.add_argument("--out-ablation", type=Path, required=True)
    ap.add_argument("--process-capture", default=None,
                    help="capture dir under autotrace/ for Doc B (e.g. ctrl_conc16_core)")
    ap.add_argument("--out-process", type=Path, required=True)
    a = ap.parse_args()
    AT = a.art / "autotrace"

    D, C, P, CH, W2, W5 = {}, {}, {}, {}, {}, {}
    for key, label, capname, payname in ARMS:
        D[key] = AT / capname
        C[key] = load_calls(D[key])
        P[key] = json.loads((a.scratch / payname).read_text())
        CH[key] = load_chunks(D[key], C[key]) if key in ("mlfq", "core") else {}
        W2[key] = json.loads((D[key] / "w2_hotspot.json").read_text())
        W5[key] = json.loads((D[key] / "W5_REPRESENTATIVE_PROCESSES.json").read_text())
    BK = "core"
    spec_b, wstep_b, _off_b = None, [], 0
    if a.process_capture:
        BK = "bcap"
        D[BK] = AT / a.process_capture
        C[BK] = load_calls(D[BK])
        P[BK] = json.loads((a.scratch / f"payload_{a.process_capture}.json").read_text())
        CH[BK] = load_chunks(D[BK], C[BK])
        W2[BK] = json.loads((D[BK] / "w2_hotspot.json").read_text())
        W5[BK] = json.loads((D[BK] / "W5_REPRESENTATIVE_PROCESSES.json").read_text())
        spec_b = json.loads(Path("experiments/h23-agentix-8b/workloads/ctrl_conc16.json").read_text())
        _db = sqlite3.connect(str(D[BK] / "cap.sqlite"))
        _sm = _db.execute("select start,text from NVTX_EVENTS where text like 'w.step::%'").fetchall()
        _cb = _db.execute("select start,text from NVTX_EVENTS where text like 'agentix.call_begin%'").fetchall()
        _db.close()
        _subs = {(c["program_id"], c["call_index"]): c["submitted_rel_ms"] for c in C[BK]}
        _offs = [ts - _subs[(q[1], int(q[2]))] * 1e6 for ts, tx in _cb
                 for q in [tx.split("::")] if len(q) > 2 and (q[1], int(q[2])) in _subs]
        _off_b = statistics.median(_offs) if _offs else 0
        for ts, tx in _sm:
            try:
                q = dict(kv.split("=") for kv in tx.split("::")[1:])
                wstep_b.append(((ts - _off_b) / 1e6, int(q["reqs"]), int(q["tok"])))
            except Exception:
                pass
        wstep_b.sort()
    pairs = {k: json.loads((AT / f"pair_facts_{k}.json").read_text())
             for k in ("state_reuse", "call_preempt", "program_identity")}
    audit = {"purpose": "R10 four-arm edition window/selection criteria", "windows": {}}

    # ---------------- trichotomy table + cross-checks ----------------------
    idx = {k: {(r["program_id"], r["call_index"]): r for r in C[k]} for k, *_ in ARMS}
    def _res(r):
        return r["finished_rel_ms"] - r["first_token_rel_ms"]
    _floor = {ck: min(_res(idx[k][ck]) for k, *_ in ARMS if ck in idx[k])
              for ck in idx["opt"]}
    TRI, FLOORC = {}, defaultdict(list)
    for ck, v in _floor.items():
        FLOORC[idx["opt"][ck]["class"]].append(v)
    FLOORC = {c: sum(v) / len(v) for c, v in FLOORC.items()}
    for k, *_ in ARMS:
        per = defaultdict(lambda: {"ftwait": [], "inres": [], "wait": []})
        for ck, r in idx[k].items():
            fw = r["first_token_rel_ms"] - r["submitted_rel_ms"]
            ir = _res(r) - _floor[ck]
            per[r["class"]]["ftwait"].append(fw)
            per[r["class"]]["inres"].append(ir)
            per[r["class"]]["wait"].append(fw + ir)
        TRI[k] = {c: {m: sum(v[m]) / max(len(v[m]), 1) for m in v} for c, v in per.items()}
    def tri_row(key, label):
        t = TRI[key]
        cells = "".join(
            f"<td>{t[c]['ftwait']:.0f} + {t[c]['inres']:.0f} = <b>{t[c]['wait']:.0f}</b></td>"
            for c in ("bfcl", "sharegpt", "lats"))
        return f"<tr><td>{label}</td>{cells}</tr>"
    tbl_tri = ('<table><tr><th>臂（每调用均值 ms：首token等待 + 驻留内等待 = Wait）</th>'
               '<th>bfcl</th><th>sharegpt</th><th>lats</th></tr>'
               + "".join(tri_row(k, lab) for k, lab, *_ in ARMS)
               + f"<tr><td><b>Execution（执行底，四臂共用）</b></td>"
               + "".join(f"<td>{FLOORC[c]:.0f}</td>" for c in ("bfcl", "sharegpt", "lats"))
               + "</tr></table>")
    # execution invariance: matched calls UNPREEMPTED on both sides —
    # residence ratio should be 1 (per-token step time is policy-blind)
    def res_of(key, ck):
        r = idx[key][ck]
        return r["finished_rel_ms"] - r["first_token_rel_ms"]
    inv, inv_n = {}, {}
    for key in ("mlfq", "core"):
        ks = [k for k in idx["opt"] if k in idx[key] and len(CH[key].get(k, [])) <= 1]
        ratios = sorted(res_of(key, k) / max(res_of("opt", k), 1e-6) for k in ks)
        inv[key] = ratios[len(ratios) // 2] if ratios else float("nan")
        inv_n[key] = len(ratios)
    # re-prefill signature: later chunks are wall-longer than first chunks
    chunk_sig = {}
    for key in ("mlfq", "core"):
        first, later = [], []
        for segs in CH[key].values():
            for i, (b, e, _q) in enumerate(sorted(segs)):
                (first if i == 0 else later).append(e - b)
        if later:
            chunk_sig[key] = (statistics.median(first), statistics.median(later), len(later))

    # ============ 一、端到端（每程序一块，四臂行紧凑相邻，无公共轴） ========
    floor_map = {ck: min(idx[k][ck]["finished_rel_ms"] - idx[k][ck]["first_token_rel_ms"]
                         for k, *_ in ARMS if ck in idx[k])
                 for ck in idx["opt"]}
    # metric ladder: where does the winner flip between the two accountings?
    _P = {}
    for k, *_ in ARMS:
        for ck, r in idx[k].items():
            e = _P.setdefault(r["program_id"], {}).setdefault(k, {"w": 0.0, "s": 1e18, "e": 0.0, "tok": 0})
            e["w"] += (r["finished_rel_ms"] - r["submitted_rel_ms"]) - floor_map[ck]
            e["s"] = min(e["s"], r["submitted_rel_ms"])
            e["e"] = max(e["e"], r["finished_rel_ms"])
            e["tok"] += max(r["produced_tokens"], 1)
    _n = len(_P)
    def _lad(fn):
        return {k: sum(fn(_P[p][k]) for p in _P) / _n for k, *_ in ARMS}
    L1 = {k: sum(_P[p][k]["w"] for p in _P) / 1e3 for k, *_ in ARMS}
    L2 = {k: v / 1e3 for k, v in _lad(lambda e: e["w"]).items()}
    L3 = _lad(lambda e: e["w"] / e["tok"])
    L4 = _lad(lambda e: (e["e"] - e["s"]) / e["tok"])
    def _lrow(name, d, unit, fmt):
        wk = min(d, key=lambda k: d[k])
        return (f"<tr><td>{name}</td>" + "".join(
            (f"<td><b>{fmt.format(d[k])}</b></td>" if k == wk else f"<td>{fmt.format(d[k])}</td>")
            for k, *_ in ARMS) + f"<td>{ {'plain':'素','opt':'opt','mlfq':'M','core':'C'}[wk] }</td></tr>")
    tbl_ladder = ('<table><tr><th>指标阶梯</th><th>素</th><th>opt</th><th>M</th><th>C</th><th>赢家</th></tr>'
                  + _lrow("① Σ等待，call 加权总量（s）", L1, "s", "{:,.0f}")
                  + _lrow("② 程序等权 · 程序等待均值（s）", L2, "s", "{:.1f}")
                  + _lrow("③ 程序等权 · 等待/token（ms/tok）", L3, "", "{:.1f}")
                  + _lrow("④ 论文指标 program-level token latency（ms/tok，原文定义）", L4, "", "{:.1f}")
                  + '</table>')
    blocks, yb, pwin = e2e_program_blocks(C, CH, ARMS, floor_map)
    fig1 = fig(blocks, yb + 4)
    wait_sums = {k: sum(c["first_token_rel_ms"] - c["submitted_rel_ms"]
                        for c in C[k] if c["class"] != "lats") / 1e3 for k, *_ in ARMS}
    audit["windows"]["part1"] = {
        "criterion": "per-program window: whole lifetime (union over arms) if <=40 s, "
                     "else densest 30 s by four-arm call activity; no shared axis",
        "program_windows_s": pwin, "short_wait_total_s": wait_sums}

    # ================= 二、高延迟（调用堆四臂主图 + step 堆支撑） ==========
    seg = {k: call_top_pile(C[k]) for k, *_ in ARMS}
    if BK == "bcap":
        seg[BK] = call_top_pile(C[BK])
    win = int(60e9)
    best_n, cw0 = -1, 0
    for t in range(0, int(max(m["end"] for m in seg["plain"])) - win, int(5e9)):
        n = sum(1 for m in seg["plain"] if m["start"] < t + win and m["end"] > t)
        if n > best_n:
            best_n, cw0 = n, t
    cw1 = cw0 + win
    parts2 = axis(cw0 / 1e6, cw1 / 1e6, 60, 1560)
    y = 70
    pile_notes = []
    from collections import Counter
    SHORTN = {"plain": "素", "opt": "opt", "mlfq": "MLFQ", "core": "core"}
    pile_comp = []
    for key, label, *_ in ARMS:
        sg = seg[key]
        inw = [m for m in sg if m["start"] < cw1 and m["end"] > cw0]
        s, y = call_pile_strip(inw, y, f"{SHORTN[key]}（窗内 {len(inw)}/{len(sg)} 成员）", cw0, cw1)
        y += 8
        parts2 += s
        comp = Counter(m["cls"] for m in sg)
        short_n = sum(v for k2, v in comp.items() if k2 != "lats")
        pile_notes.append(f"{SHORTN[key]}：{len(sg)} 个调用 / {sum(m['d'] for m in sg)/1e9:.0f} s，短程序成员 {short_n}")
        by_pid = Counter(m["pid"] for m in sg)
        tops = "、".join(f"{pid}({n}调用)" for pid, n in by_pid.most_common(3))
        pile_comp.append(
            f"<b>{SHORTN[key]}</b>：{comp.get('bfcl',0)} 个 bfcl + {comp.get('sharegpt',0)} 个 sharegpt + "
            f"{comp.get('lats',0)} 个 lats 调用；成员最多的程序 {tops}")
    fig2 = fig(parts2, y + 6)
    audit["windows"]["part2"] = {"criterion": "densest 60 s of vLLM素 top call pile",
                                 "window_s": [cw0 / 1e9, cw1 / 1e9]}
    # step-pile strips, ALL FOUR ARMS (call-internal iter universe, w05 contract)
    p1 = P["opt"]["hl"]["piles"][0]
    si = max(range(len(p1["rows"])), key=lambda i: len(p1["rows"][i]))
    sec = P["opt"]["hl"]["sections"][si]
    sb, se = int(sec["begin_ns"]), int(sec["end_ns"])
    ob_f = int(P["opt"]["hl"]["origin"])
    parts2b = axis((sb - ob_f) / 1e6, (se - ob_f) / 1e6, 60, 1350)
    yh = 70
    for key, label, *_ in ARMS:
        obk = int(P[key]["hl"]["origin"])
        s, yh = hl_strip(P[key]["hl"], yh, SHORTN[key], sb - ob_f + obk, se - ob_f + obk)
        yh += 6
    fig2b = fig(parts2b, yh + 6)
    step_sums = {k: P[k]["hl"]["piles"][0]["sum_ns"] / 1e9 for k, *_ in ARMS}
    audit["windows"]["part2b"] = {"criterion": "densest section of opt rank-1 forward pile, same rel window on all arms",
                                  "section": si + 1}
    # scope/phase composition table (call-internal, per arm; from W5 host layer)
    SCOPES = ["w.sched: schedule_total", "w.run: prepare_inputs", "gpu_model_runner: forward",
              "gpu_model_runner: sample", "gpu_model_runner: postprocess",
              "w.sched: update_from_output", "w.engine: process_outputs"]
    def sc_row(key, label):
        w2r = {r["process"]: r for r in W2[key]["ranked_processes"]}
        cells = "".join(f"<td>{w2r[s]['union_ns']/1e9:.1f}</td>" if s in w2r else "<td>—</td>"
                        for s in SCOPES)
        gap = next((b for b in W2[key]["dominant_idle_boundaries"] if "set_async" in b["boundary"]), {})
        return f"<tr><td>{label}</td>{cells}<td>{gap.get('sum_ns',0)/1e9:.0f}</td></tr>"
    tbl_scope = ('<table><tr><th>臂（各 scope 时间和 s）</th><th>schedule</th><th>prepare</th>'
                 '<th>forward</th><th>sample</th><th>postproc</th><th>update</th><th>outputs</th>'
                 '<th>async 等待</th></tr>'
                 + "".join(sc_row(k, {"plain":"素","opt":"opt","mlfq":"MLFQ","core":"core"}[k])
                           for k, *_ in ARMS) + "</table>")

    # ================= 三、并发与资源（四臂 lanes + 显微） ==================
    def at_cap_window(calls, cap=16, width_ms=30000, step=5000):
        ev = []
        for c in calls:
            ev.append((c["submitted_rel_ms"], 1))
            ev.append((c["finished_rel_ms"], -1))
        ev.sort()
        # depth timeline
        depth, tl = 0, []
        for t, d in ev:
            depth += d
            tl.append((t, depth))
        wall = ev[-1][0]
        best, b0 = -1, 0
        t = 0.0
        while t + width_ms <= wall:
            over = 0.0
            prev_t, prev_d = t, 0
            for tt, dd in tl:
                if tt < t:
                    prev_d = dd
                    continue
                if tt > t + width_ms:
                    break
                if prev_d > cap:
                    over += tt - max(prev_t, t)
                prev_t, prev_d = tt, dd
            if over > best:
                best, b0 = over, t
            t += step
        return b0, b0 + width_ms
    c0, c1 = at_cap_window(C["opt"])
    audit["windows"]["part4_atcap"] = {"criterion": "30 s window with max opt time-above-cap16",
                                       "window_s": [c0 / 1e3, c1 / 1e3]}

    # ---- 4.1 per-METRIC whole-run overlays: one figure per metric, 4 arms --
    wall_ms = max(max(c["finished_rel_ms"] for c in C[k]) for k, *_ in ARMS)
    def run0_of(key):
        return int(P[key]["e2e"]["origin"]) - int(P[key]["hl"]["origin"])
    def metric_overlay(lane_idx, title, cap=None):
        H = 330
        parts = axis(0.0, wall_ms, 60, H - 40)
        lanes = {k: P[k]["cu"]["lanes"][lane_idx] for k, *_ in ARMS}
        ymax = max(l["max"] for l in lanes.values()) or 1
        base, top = H - 30, 74
        Xm = lambda ms: LEFT + (W - LEFT - RIGHT) * min(max(ms, 0), wall_ms) / wall_ms
        Ym = lambda v: base - (base - top) * min(v / ymax, 1.0)
        parts.append(f'<text x="4" y="26" font-size="20" font-weight="600" fill="#1f2f45">{title}'
                     f'（四臂叠加，满量程 {ymax:g}{lanes[ARMS[0][0]]["unit"]}）</text>')
        lx = LEFT
        for key, label, *_ in ARMS:
            parts.append(f'<rect x="{lx}" y="34" width="22" height="4" fill="{ARM_COLOR[key]}"/>'
                         f'<text x="{lx+27}" y="41" font-size="15" fill="#48607d">{label.split("（")[0]}</text>')
            lx += 250
        for key, *_ in ARMS:
            r0 = run0_of(key)
            seg_path = ""
            for rows in lanes[key]["rows"]:
                for r in rows:
                    ms0, ms1 = (r[0] - r0) / 1e6, (r[0] + r[1] - r0) / 1e6
                    if ms1 < 0 or ms0 > wall_ms:
                        continue
                    seg_path += f"M{Xm(ms0):.1f} {Ym(r[2]):.1f}H{Xm(ms1):.1f}"
            parts.append(f'<path d="{seg_path}" stroke="{ARM_COLOR[key]}" stroke-width="1.5" '
                         f'fill="none" opacity=".85"/>')
        if cap is not None:
            parts.append(f'<line x1="{LEFT}" y1="{Ym(cap):.1f}" x2="{W-RIGHT}" y2="{Ym(cap):.1f}" '
                         f'stroke="{WAIT}" stroke-dasharray="4 3"/>'
                         f'<text x="{W-RIGHT-2}" y="{Ym(cap)-4:.1f}" font-size="15" '
                         f'text-anchor="end" fill="{WAIT}">cap=16</text>')
        return fig(parts, H)
    fig4_busy = metric_overlay(0, "GPU busy（%）")
    fig4_gemm = metric_overlay(1, "gemm 家族时间占比（%）")
    fig4_inf = metric_overlay(2, "在飞调用数（个）", cap=16)

    # ---- 4.2 per-ARM deep dive: high-latency + concurrency window,
    #      process timelines co-axial with metric-time lanes -----------------
    def deep_dive(key, label, fixed=None, extra_lanes=None, color=None):
        r0 = run0_of(key)
        sg = seg[key]                       # top call-pile members, run-rel ns
        # (a) high-latency period: densest 10 s of top-pile member activity
        win = 10e3
        best, h0 = -1.0, 0.0
        tt = 0.0
        while tt + win <= wall_ms:
            act = sum(max(0.0, min(m["end"] / 1e6, tt + win) - max(m["start"] / 1e6, tt)) for m in sg)
            if act > best:
                best, h0 = act, tt
            tt += 2500.0
        # (b) concurrency period: densest 10 s of above-cap in-flight
        inf_rows = [r for rows in P[key]["cu"]["lanes"][2]["rows"] for r in rows]
        best, q0 = -1.0, 0.0
        tt = 0.0
        while tt + win <= wall_ms:
            over = sum(r[1] / 1e6 for r in inf_rows
                       if r[2] >= 16 and (r[0] - r0) / 1e6 >= tt and (r[0] - r0) / 1e6 < tt + win)
            if over > best:
                best, q0 = over, tt
            tt += 2500.0
        w0 = min(h0, q0)
        w1 = max(h0 + win, q0 + win)
        if w1 - w0 > 25e3:                   # disjoint far apart: keep the HL window
            w0, w1 = h0, h0 + win
        if fixed is not None:                # constructed phase window overrides
            w0, w1 = fixed
            h0 = q0 = w0
        hl_pids = {m["pid"] for m in sg if m["start"] / 1e6 < w1 and m["end"] / 1e6 > w0}
        parts = axis(w0, w1, 60, 0)          # height patched at the end
        parts.append(f'<text x="4" y="26" font-size="20" font-weight="600" fill="{color or ARM_COLOR.get(key, '#2f6f9f')}">'
                     f'{label} · 高延迟段 [{h0/1e3:.0f},{(h0+win)/1e3:.0f}] s · '
                     f'超cap并发段 [{q0/1e3:.0f},{(q0+win)/1e3:.0f}] s · 图窗 [{w0/1e3:.0f},{w1/1e3:.0f}] s</text>')
        y = 74
        Xd = lambda ms: LEFT + (W - LEFT - RIGHT) * (max(min(ms, w1), w0) - w0) / (w1 - w0)
        # call-internal process timeline: every forward-step instance in the
        # window is one tick, greedily packed into lanes; rank-1 pile members red
        e2o = int(P[key]["e2e"]["origin"])
        inst = []
        for pi, pile in enumerate(P[key]["hl"]["piles"]):
            for rows_ in pile["rows"]:
                for st, du in rows_:
                    ms0 = (st - e2o) / 1e6
                    ms1 = ms0 + du / 1e6
                    if ms1 < w0 or ms0 > w1:
                        continue
                    inst.append((ms0, ms1, pi == 0))
        inst.sort()
        lane_end = []
        rh_i = 8
        n_red = sum(1 for *_x, r in inst if r)
        parts.append(f'<text x="{LEFT-6}" y="{y+8}" font-size="14" text-anchor="end" '
                     f'fill="#48607d">step 容器</text>')
        for ms0, ms1, red in inst:
            li = next((i for i, e in enumerate(lane_end) if ms0 >= e), None)
            if li is None:
                if len(lane_end) >= 18:
                    li = min(range(len(lane_end)), key=lambda i: lane_end[i])
                else:
                    lane_end.append(0.0)
                    li = len(lane_end) - 1
            lane_end[li] = ms1
            yy = y + li * rh_i
            parts.append(f'<rect x="{Xd(ms0):.1f}" y="{yy}" width="{max(Xd(ms1)-Xd(ms0),0.7):.1f}" '
                         f'height="{rh_i-2}" fill="{WAIT if red else "#9db3c8"}" '
                         f'opacity="{".95" if red else ".55"}"/>')
        y += max(len(lane_end), 1) * rh_i + 16
        parts.append(f'<text x="{LEFT}" y="{y-4}" font-size="14" fill="#48607d">'
                     f'窗内 step 实例 {len(inst):,} 个，红色 = 全局第 1 名重 forward 堆成员（{n_red:,} 个）；'
                     f'其余灰色。一行内的相邻矩形 = 依次执行的引擎迭代。</text>')
        y += 10
        y += 10
        # metric lanes sharing the same axis: busy / gemm / in-flight / step rate
        def lane(rows_iter, label_l, vmax, color, cap_line=None):
            nonlocal y
            lane_h = 96
            base = y + lane_h - 8
            parts.append(f'<text x="{LEFT-6}" y="{y+14}" font-size="15" text-anchor="end" '
                         f'fill="#48607d">{label_l}</text>')
            parts.append(f'<rect x="{LEFT}" y="{y}" width="{W-LEFT-RIGHT}" height="{lane_h}" '
                         f'fill="#fbfbf9" stroke="#eee"/>')
            path = ""
            for ms0, ms1, v in rows_iter:
                if ms1 < w0 or ms0 > w1:
                    continue
                h = (lane_h - 18) * min(v / vmax, 1.0)
                path += f"M{Xd(ms0):.1f} {base:.1f}V{base-h:.1f}H{Xd(ms1):.1f}V{base:.1f}"
            parts.append(f'<path d="{path}" stroke="{color}" stroke-width="1" fill="none"/>')
            if cap_line is not None:
                yc = base - (lane_h - 18) * min(cap_line / vmax, 1.0)
                parts.append(f'<line x1="{LEFT}" y1="{yc:.1f}" x2="{W-RIGHT}" y2="{yc:.1f}" '
                             f'stroke="{WAIT}" stroke-dasharray="4 3"/>')
            y += lane_h + 18
        cuL = P[key]["cu"]["lanes"]
        def cu_rows(li):
            return [((r[0] - r0) / 1e6, (r[0] + r[1] - r0) / 1e6, r[2])
                    for rows in cuL[li]["rows"] for r in rows]
        lane(cu_rows(0), "GPU busy %", 100, "#2f6f9f")
        lane(cu_rows(1), "gemm 占比 %", 100, "#a8802f")
        lane(cu_rows(2), "在飞（个）", cuL[2]["max"], "#1baf7a", cap_line=16)
        fw = sorted((m[0] for pile in P[key]["hl"]["piles"] for rows in pile["rows"]
                     for m in rows), key=lambda x: x)
        e2o = int(P[key]["e2e"]["origin"])
        binw = 250.0
        bins = {}
        for st in fw:
            ms = (st - e2o) / 1e6
            if w0 - binw <= ms <= w1 + binw:
                bins[int(ms // binw)] = bins.get(int(ms // binw), 0) + 1
        srate = [(b * binw, (b + 1) * binw, n / (binw / 1e3)) for b, n in sorted(bins.items())]
        smax = max((v for *_, v in srate), default=1)
        lane(srate, "step 率（步/s）", smax, "#7a5fb0")
        for lb, rows_x, vmx, colx, capx in (extra_lanes or []):
            lane(rows_x, lb, vmx, colx, cap_line=capx)
        audit["windows"].setdefault("part4_deepdive", {})[key] = {
            "hl_window_s": [h0 / 1e3, (h0 + win) / 1e3],
            "atcap_window_s": [q0 / 1e3, (q0 + win) / 1e3],
            "figure_window_s": [w0 / 1e3, w1 / 1e3],
            "hl_programs": sorted(hl_pids)}
        # patch the axis height now that y is known
        parts[0:len(axis(w0, w1, 60, 0))] = axis(w0, w1, 60, y - 50)
        return fig(parts, y + 6), sorted(hl_pids)
    deep_figs, deep_hl = {}, {}
    for key, label, *_ in ARMS:
        deep_figs[key], deep_hl[key] = deep_dive(key, label)

    # ================= 五、负载分析 W1–W6 ==================================
    def w2row(key, label):
        w2, w5 = W2[key], W5[key]
        gap = next((b for b in w2["dominant_idle_boundaries"] if "set_async" in b["boundary"]), {})
        return (f"<tr><td>{label}</td>"
                f"<td>{w2['prepare_inputs_api_split']['window_union_ns']/1e9:.1f}</td>"
                f"<td>{100*w2['prepare_inputs_api_split']['cuda_api_ns']/max(w2['prepare_inputs_api_split']['window_union_ns'],1):.0f} %</td>"
                f"<td>{gap.get('sum_ns',0)/1e9:.0f} s / {gap.get('mean_ms',0):.1f} ms</td>"
                f"<td>{100*w5['layers']['host']['selected_share'] if 'selected_share' in w5['layers']['host'] else sum(s['share_of_host'] for s in w5['layers']['host']['selected'])*100:.1f} %</td></tr>")
    tbl_w = ('<table><tr><th>臂</th><th>prepare_inputs 和（s）</th><th>其中 CUDA API</th>'
             '<th>async 输出等待（和 / 均）</th><th>W5 代表 stage 集覆盖 host</th></tr>'
             + "".join(w2row(k, lab) for k, lab, *_ in ARMS) + "</table>")
    dfg_html = dfg_fig(W2["opt"], "vLLM-opt")
    async_tbl = "".join(
        f"<tr><td>{lab}</td><td>{next((b['sum_ns']/1e9 for b in W2[k]['dominant_idle_boundaries'] if 'set_async' in b['boundary']),0):.0f} s</td>"
        f"<td>{step_sums[k]:.0f} s</td></tr>" for k, lab, *_ in ARMS)

    # ---- one real call walked through all four arms (for the method block) --
    kb = max((k for k, r in idx["opt"].items() if r["class"] == "bfcl"
              and all(k in idx[a] for a, *_ in ARMS)),
             key=lambda k: idx["opt"][k]["first_token_rel_ms"] - idx["opt"][k]["submitted_rel_ms"])
    def walk_row(key, label):
        r = idx[key][kb]
        w = r["first_token_rel_ms"] - r["submitted_rel_ms"]
        res = r["finished_rel_ms"] - r["first_token_rel_ms"]
        nch = len(CH[key].get(kb, [])) or 1
        return (f"<tr><td>{label}</td><td>{w:,.0f}</td><td>{res:,.0f}</td>"
                f"<td>{nch}</td><td>{w+res:,.0f}</td></tr>")
    walk_tbl = ('<table><tr><th>臂（同一真实调用 '
                f'{kb[0]}#{kb[1]}，bfcl）</th><th>首token等待 ms</th><th>驻留 ms</th>'
                '<th>quantum 段数</th><th>端到端 ms</th></tr>'
                + "".join(walk_row(k, lab) for k, lab, *_ in ARMS) + "</table>")

    e_sr, e_cp, e_pi = (pairs[k]["endpoint"]["speedup"] for k in
                        ("state_reuse", "call_preempt", "program_identity"))
    _compo_raw = compo_section(Path("experiments/h23-agentix-8b/workloads/thr_mixed_r0.5.json"))
    _mt = re.search(r"<table>.*?</table>", _compo_raw, re.S)
    compo_tbl = _mt.group(0) if _mt else ""
    life_html = class_lifecycle_figs(C["opt"])
    for _old, _new in (
        ("<b>bfcl 的生命周期：</b>", "<b>bfcl.</b> 红段多、彩段短、段间留有工具延迟空隙。这个程序的寿命由等待与工具间隔构成，正是排序优化的目标形态。原注："),
        ("<b>sharegpt 的生命周期：</b>", "<b>sharegpt.</b> 彩段远长于红段。寿命由长 decode 服务主导，因此它是 quantum 抢占的主要作用面。原注："),
        ("<b>lats 的生命周期：</b>", "<b>lats.</b> 五行并行波逐波推进，每波都在等最慢的一路。寿命等于关键路径，这是 ATLAS 存在的理由。原注："),
    ):
        life_html = life_html.replace(_old, _new)
    sig_m = chunk_sig.get("mlfq", (0, 0, 0))
    # probe-v2 direct state-interval validation (dedicated REQTRACE reruns)
    tbl_direct = ""
    _si = {}
    for _arm, _lbl in (("llama_core_req16", "core"), ("mlfq_call_req16", "MLFQ")):
        _f = AT / _arm / "STATE_INTERVALS.json"
        if _f.exists():
            _si[_lbl] = json.loads(_f.read_text())["class_means_ms"]
    if _si:
        tbl_direct = ('<table><tr><th>直测（探针 v2 专采）：exec / wait / 抢占-恢复次数</th>'
                      '<th>bfcl</th><th>sharegpt</th><th>lats</th></tr>' + "".join(
            f"<tr><td>{lbl}</td>" + "".join(
                f"<td>{d[c]['exec']:.0f} / {d[c]['wait']:.0f} / {d[c]['ep']:.1f}</td>"
                for c in ("bfcl", "sharegpt", "lats")) + "</tr>"
            for lbl, d in _si.items()) + "</table>"
            '<p class="cap"><b>直测闭环：</b>上表来自带 AGENTIX_REQTRACE 的专采（每步 RUNNING 集'
            '身份 → 每 call 的 RUNNING/QUEUED 区间直接重建；RUNNING 含步内 host 份额，即'
            '"正被引擎服务"）。同类均值与 floor 代理一致到 5–15 %（另含跑间方差）——A2 的测量'
            '边界就此闭合；直测独有的第三个数是<b>抢占-恢复次数</b>：core 对 lats 为 0（压后即'
            '不再打断）、对 sharegpt 1.7；MLFQ 对 sharegpt 2.7 次且 wait 直测 13.3 s——'
            'quantum 反复切长 decode 的机制代价由状态机直读。</p>')
    tri_def = f"""
<div class="block howto"><b>时间量的统一定义（A 全文共用）</b>
<p>每个 call 的端到端拆成两部分：<b>Execution（执行底）</b>= 该 call 在四臂中的最小驻留
（缓存暖、不被打扰时的真实解码工作，四臂共用一个值）；<b>Wait（论文口径等待）</b>=
端到端 − 执行底。Wait 再按位置拆两段：<b>首token等待</b>（提交→首token：排队+首段 prefill）
与<b>驻留内等待</b>（驻留−执行底：quantum 间再排队、续段再 prefill、慢批干扰）。表内每格
"a + b = <b>W</b>"即这三个数。与论文图 17 的对应：W ↔ Wait（红），Execution ↔ 蓝，
我们的 recompute 把论文的 Swap（绿）合并进了驻留内等待。</p>
<p>竖读一列看同类负载的 Wait 重分配，加号两侧看等待藏在首token段还是驻留内段；Execution 行四臂共用是构造使然。</p>
<p><b>机制代价在表内的位置：</b>驻留内等待列就是它——MLFQ 续段 quantum 墙钟中位
{sig_m[1]:,.0f} ms 对首段 {sig_m[0]:,.0f} ms（{sig_m[2]:,} 个续段）是其微观形态。</p>
<p><b>测量边界（诚实声明）：</b>现有 trace 无引擎侧"运行/抢占/恢复"状态事件，驻留内等待是
差值代理、不能在时间轴上逐段定位（A3 图内浅红底只显示 chunk 未覆盖的可见部分）；探针 v2
（每步 running 集身份）已实现、待 GPU 恢复后重采即可把 Wait/Execution 换成状态区间直测。</p></div>
{tbl_tri}
{tbl_direct}
<p class="cap"><b>表注：</b>bfcl 列 Wait：素 {TRI['plain']['bfcl']['wait']:.0f} → opt
{TRI['opt']['bfcl']['wait']:.0f} → MLFQ {TRI['mlfq']['bfcl']['wait']:.0f} → core
<b>{TRI['core']['bfcl']['wait']:.0f}</b> ms——目标类上 core 最短（与论文图 17 一致）；
sharegpt 列 MLFQ 的 {TRI['mlfq']['sharegpt']['ftwait']:.0f}+{TRI['mlfq']['sharegpt']['inres']:.0f}
是"首token等待被搬进驻留内"的直读证据；lats 列 core 首token段
{TRI['core']['lats']['ftwait']:.0f} ms 是设计（压后长程序）。</p>"""

    _PAPER = {
        1: ("_page_0_Figure_9.jpeg",
            "四个 agent 工作流被画成 LLM 调用与工具/人类中断连成的图：单线程成链，多线程成 DAG。",
            "这就是 program 这一层的出处，A0 的三类负载是它的实例。"),
        2: ("_page_1_Figure_0.jpeg",
            "同一批 4 程序在 2 槽引擎里的三张甘特图，等待合计 FCFS 18、MLFQ 18、PLAS 12 个单位。",
            "程序信息值 6 个单位；A3/A4 的实盘图就是这张玩具图的 16 槽版本。"),
        3: ("_page_2_Figure_13.jpeg",
            "架构分两层：上层程序编排与状态，下层 serving 引擎执行调用。",
            "我们的 19 个探针打在下层步循环、程序账本记在上层，A00 三方对账沿这条层界。"),
        4: ("_page_3_Figure_0.jpeg",
            "稳态一小时内，等待被优化后引擎里的在飞调用量反而更高。",
            "等待缩短让程序更快发起下一调用（闭环 λ=N/W），论文吞吐叙事以此为前提。"),
        5: ("_page_3_Figure_5.jpeg",
            "负载升高后，各类 agent 程序的时间构成里等待占大头。",
            "『优化等待』由此成为全文的问题定义。"),
        6: ("_page_4_Figure_0.jpeg",
            "短调用与短程序的等待÷执行比冲到 10–50 倍，FCFS 在调用轴、MLFQ 在程序轴各占一列高位。",
            "两级队头阻塞同时存在而 MLFQ 只解了调用级——这是换程序单位的动机。"),
        7: ("_page_4_Figure_6.jpeg",
            "程序内的前缀命中率高，跨程序接近零。",
            "状态复用的机会被程序边界圈定，消融第一对（素→opt）的收益来源与调度无关。"),
        70: ("_page_4_Figure_7.jpeg",
            "跨程序命中率面板：几乎无前缀可共享。",
            "复用面在程序边界截止，这也是多引擎要做亲和路由的原因。"),
        8: ("_page_5_Figure_0.jpeg",
            "全局进程表同时喂给调度器与负载均衡器。",
            "一张表两个消费者：单引擎的调度收益与多引擎的 KV 亲和由此分工。"),
        9: ("_page_6_Figure_0.jpeg",
            "同一个 DAG 的两种排法，makespan 一个 14、一个 11。",
            "程序内并行给了引擎服务顺序自由度，ATLAS 的关键路径聚合就是来拿它的。"),
        10: ("_page_7_Figure_0.jpeg",
            "一次调用在 Q0–Q3 之间的生命周期状态机：按 p(c<sub>j</sub>) 准入、quantum 用尽降级、β 提升。",
            "我们账本里 admission 97/102/237/2004 与 151 次降级就是这台状态机的运行记录。"),
        11: ("_page_8_Figure_8.jpeg",
            "三类负载的输入/输出长度分布与每程序调用数分布。",
            "A0 组成表的每一列按此逐项校准。"),
        12: ("_page_9_Figure_0.jpeg",
            "四条延迟-到达率曲线低载并拢、高载分离，Agentix 始终最低。",
            "附录端点表是这张图在 4090 上的重测，排序在五个到达率全部复现。"),
        13: ("_page_10_Figure_0.jpeg",
            "P95/99 口径下 MLFQ 与 Agentix 的间距不随负载闭合。",
            "调用级抢占救均值不救尾，程序身份的价值集中在尾部。"),
        14: ("_page_10_Figure_6.jpeg",
            "多引擎下不同负载均衡策略的延迟对比。",
            "多卡内容不在单卡复现范围，由偏差表衔接。"),
        15: ("_page_11_Figure_0.jpeg",
            "同一 SLO 下最大可持续到达率随引擎副本数线性增长。",
            "这解释了单卡可持续 r 低于论文测试台。"),
        16: ("_page_11_Figure_2.jpeg",
            "离线批处理下 Agentix 的 makespan 比基线低 10–40 %。",
            "其来源是 swap 内核与 gang 调度；我们的 recompute 路径 makespan 持平，两个结果在各自配置下成立。"),
        17: ("_page_11_Figure_4.jpeg",
            "每根柱子里蓝色执行段三系统等高，红色等待段相差数倍。",
            "调度只重分配等待、不碰执行——A2 时间量表的论文侧对照。"),
        18: ("_page_11_Figure_10.jpeg",
            "swap 内核减少换出次数与换出时间。",
            "本复现用 recompute 处置被抢占者，此项收益是偏差表 swap→recompute 一行的论文侧依据。"),
        19: ("_page_16_Picture_9.jpeg",
            "两程序玩具例：MLFQ 下 A 的并行小调用让 B 等 5 步，ATLAS 把 A 的第三路降级后 B 只等 3 步。",
            "这是程序身份在多线程上的第二重价值；单线程时 ATLAS 退化为 PLAS。"),
        20: ("_page_16_Figure_11.jpeg",
            "仿真中各策略与 SRPT 神谕的差距，Agentix 最近但缺口可见。",
            "免预测近似的代价被论文自己量化，也给后续机制探索标出上限方向。"),
    }
    def pf(n, num=None):
        fname, s1, s2 = _PAPER[n]
        num = num if num else (7 if n == 70 else n)
        return paper_fig(fname, f"<b>论文图 {num}.</b> {s1} {s2}")
    cw = pairs["call_preempt"]["class_wait_ms"]
    ml_a = pairs["program_identity"]["mlfq"]
    METH = f"""
<h2>A1 论文的方法与 baseline 的对比 —— 负载带来的消融机会（多图）</h2>
<div class="block"><b>A1.0 机制纲要（三点，讨论定稿）</b>
<p><b>其一（问题与方法主线）：</b>agent 程序并发的特点是异质——不同程序的 call 触发频率不同
（工具/思考间隔各异）、call 长度不同、<b>程序剩余轮次</b>也不同。理想目标是最小化等待
（SJF/SRPT 最优），但 call 的未来频率、长度与程序剩余轮次都不可预知。于是用<b>已发生的实测
替代预知</b>：记录每程序 call 的累计服务时间，新 call 到达时据此在线定级（随状态在线调度）
进入程序级 MLFQ——轻/新程序高优先、重程序压后；队内执行按 time quantum 预算、用尽降级，
防长 call 独占。附带的 KV 保护收益（两条）：短 call 一个 quantum 内一次跑完、全程不被
抢占，KV 驻留到完成（无论文的 swap 换出、无本复现的 recompute 释放重算）；且 quantum 阶梯
越低队越大（32/64/128/256），重程序长 call <b>直接低队准入 = 跳过前几级小 quantum</b>、
抢占次数更少——直测 episodes：core 对 sharegpt/lats 为 1.7/0 次，MLFQ 为 2.7/1.1 次
（A2 直测表），KV 换出/重算的暴露随之下降。单引擎内的 KV 复用由引擎自带前缀缓存提供、与调度顺序无关（实测未抢占同调用
驻留比 1.00）；KV 复用真正进入决策的是<b>多引擎路由</b>：各引擎 KV 互不可访问、跨引擎 =
前缀整段重算，进程表驱动的亲和路由把程序的下一个 call 送回其 KV 所在引擎。</p>
<p><b>其二（机制细节）：</b>程序累计 call 的服务时间 T<sub>p</sub>（多个短 call 或间歇长 call
都会积累），使该程序<b>未来 call 的初始队列</b>逐级降低；入队后各 call 按 MLFQ 原样运转
（队内 FCFS、quantum 用尽降级）。短程序（少且短 call）因此优先完成、等待最小。β 阈值防饿：
当 (W<sub>p</sub>+W<sub>c</sub>)/(T<sub>p</sub>+T<sub>c</sub>) ≥ β 时把该程序的 call 提升回
Q1 并重置其 W/T 计数——覆盖"重程序新 call 被低准入压死"与"长 call 降到底爬不出"两种饿死，
本负载 β=2.0 零触发（保险丝而非收益来源）。</p>
<p><b>其三（负载特点如何敲定改进）：</b>sharegpt = 单线程间歇长 call；tooluse/bfcl = 单线程
频繁短 call；lats = 多线程高频短 call。三个特点各敲定一个部件：频繁短 call 的洪流使
call 级 MLFQ 每个新 call 回 Q0 而永远插队 → 程序级准入；间歇长 call 的单次长占 quanta
已能治，程序级增量是其后续轮次也被压后；多线程使 sum 累计高估并行程序 → ATLAS 关键路径
聚合。一句话根因：<b>call 长度与程序长度反相关</b>，按 call 的 LAS 对 agent 负载系统性
排错，改进 = 只换单位、不换机制。</p></div>
<div class="block"><b>① 论点</b>
<p>三类负载（组成见 A2）结构不对称，使三种优化各有独立杠杆：bfcl 的密集短调用给"排序"最大杠杆；
sharegpt 的长 decode 调用是"quantum 抢占"的作用面；lats 的调用洪流制造两级队头阻塞——只有认得
"程序身份"的调度才能区分"洪流的第 180 个调用"与"新程序的第 1 个调用"。三个机会互不重叠，
四臂因此可以首尾相接地逐对消融。理论主线一句话：理想基准是 SJF/SRPT（对均值等待最优，但需
预知剩余执行量，不可实现）；Agentix = 程序粒度 Least-Attained-Service 的免预测近似——用已获
服务的实测替代对未来的预知，重尾下"用得多≈剩得多"；附录论文图 20 给出这套近似与 SRPT 神谕
的差距，即免预测付出的代价。</p></div>
{pf(2)}
<div class="block"><b>② Baseline 是什么、缺陷是什么（沿一个真实请求走全栈）</b>
<p>论文实际评估的基线：vLLM（素）、vLLM-opt（+前缀缓存+分块预填充）、调用级 MLFQ。四臂在
"提交 → waiting 队列 → 16 槽连续批 → 每 step 一 token → 完成"这条路径上的分歧只有两处：
<b>队列出队顺序</b>与 <b>prefill 是否重算</b>。取我们 trace 里等待最重的 bfcl 调用
{kb[0]}#{kb[1]} 实测四臂对照：</p>
{walk_tbl}
<p class="cap"><b>表注：</b>同一到达序列下同一调用的四臂实测；等待列即各自缺陷的直接读数
（素 = 重复 prefill + FCFS；opt = 调用级队头阻塞；MLFQ = 程序级阻塞仍在 + 续段再 prefill，
论文未明确说明续段实现，本复现为客户端续发；core = 程序身份出队）。</p></div>
{pf(6)}
<div class="block impl"><b>③ 创新点按三元素（动机 → 机制 → 证据角色），逐个对应消融对</b>
<p><b>论文创新组件清单（先摆全景再消融）：</b>①程序抽象 + 全局进程表；②调度器 PLAS（单线程，
按累计服务准入）与 ATLAS（多线程扩展，关键路径聚合）；③sticky 路由（进程表驱动、同程序 call
发同一引擎——多引擎的 KV 亲和组件）；④swap 内核（抢占保 KV）。本复现覆盖 ①②（单引擎），
③④ 记入偏差表。注意：基线 MLFQ 无程序概念、无任何 KV 亲和机制——它享受的前缀命中只是
vLLM 自带缓存的顺带效果，三个缓存臂同享。</p>
<p><b>状态复用</b>（素→opt）：动机是消除重复 prefill；机制是前缀缓存 + 分块预填充；证据角色
是第一对配对事实 mean {e_sr['mean']:.2f}×——先剥离它，后两个消融才不会把工程优化记成调度
收益。下两张原图给出机会边界：程序内命中高、跨程序命中低。</p></div>
{pf(7)}{pf(70)}
<div class="block impl">
<p><b>调用级抢占</b>（opt→MLFQ）：动机是打破调用级队头阻塞；机制是每队列 time quantum（服务配额，本复现以 token 数计 32/64/128/256；论文未给具体值）
（32/64/128/256）+ 用尽降级；证据角色是类等待坍缩（bfcl p50 {cw['fcfs']['bfcl']['p50']:.0f}→
{cw['core']['bfcl']['p50']:.0f} ms）与 mean 仅 {e_cp['mean']:.2f}× 并存——省下的等待被再
prefill 与再排队吃掉，尾部才有 p90 {e_cp['p90']:.2f}×。<b>程序身份</b>（MLFQ→core）：动机是
程序级队头阻塞；机制是进程表累计 PLAS 的离散化准入 p(c<sub>j</sub>) =
Σ<sub>k&lt;j</sub> t<sub>k</sub>（本负载把 {ml_a['admission'].get('3', 2004)} 个长程序调用
直接放进 Q3）+ β 抗饿（(W<sub>p</sub>+W<sub>c</sub>)/(T<sub>p</sub>+T<sub>c</sub>) ≥ β，
β=2.0 未触发）；两个常见误读先拆掉：其一，方向不是"优先/聚集同程序的 call"（KV 亲和归路由与 swap），而是<b>压制</b>已获服务多的程序的新 call——重程序的 call 直接进低队，轻/新程序先走；其二，T<sub>p</sub> 不是估计器——它是已发生服务的实测，按 Least-Attained-Service 思想在程序粒度近似 SJF，全程无需预测 call 数或长度（论文的 non-clairvoyant 卖点）。证据角色是 lats 等待被刻意抬到 p50 {cw['core']['lats']['p50']:.0f} ms，换
mean {e_pi['mean']:.2f}× / p99 {e_pi['p99']:.2f}×。下方状态机原图即该机制本体，玩具例原图
给出它在多线程（lats）上的第二重价值——注意边界：这重价值只作用于多线程程序，对单线程的 sharegpt/bfcl，ATLAS 退化为 PLAS，调度只在程序之间重排等待（论文图 17a 的蓝段等高、红段悬殊即此意）。</p></div>
{pf(10)}{pf(19)}
<div class="block howto"><b>④ 边界</b>
<p>论文图 2 的收益前提是槽被占满。附录 r=0.2 端点三个缓存臂并拢，前提失效时四臂差异也消失。</p></div>
"""

    # ============ A4: high-latency calls, grouped per program ==============
    def hl_prog_strip(members, y0, tag, w0ns, w1ns):
        by_p = {}
        for m in members:
            by_p.setdefault(m["pid"], []).append(m)
        order = sorted(by_p.items(), key=lambda kv: (
            {"bfcl": 0, "sharegpt": 1, "lats": 2}[kv[1][0]["cls"]], kv[0]))
        out = [f'<text x="4" y="{y0+12}" font-size="19" font-weight="600" fill="#1f2f45">{tag}'
               f' · 最高延迟区间共 {len(members)} 个 call、{len(order)} 个 program</text>']
        rh = 13
        X = lambda t: LEFT + (W - LEFT - RIGHT) * (min(max(t, w0ns), w1ns) - w0ns) / (w1ns - w0ns)
        y = y0 + 20
        for pid, ms in order:
            cls = ms[0]["cls"]
            out.append(f'<text x="{LEFT-6}" y="{y+9}" font-size="13" text-anchor="end" '
                       f'fill="#48607d">{pid}·{cls}·{len(ms)}</text>')
            for m in ms:
                x0, x1 = X(m["start"]), max(X(m["end"]), X(m["start"]) + 0.8)
                th = 7 if cls != "lats" else 4
                out.append(f'<rect x="{x0:.1f}" y="{y+(9-th)//2}" width="{x1-x0:.1f}" height="{th}" '
                           f'fill="{CLS_COLOR[cls]}" opacity="{0.95 if cls != "lats" else 0.55}"/>')
            y += rh
        return out, y + 8
    # A4 v3: subjects = the PROGRAMS owning core's top-latency pile; window =
    # densest 60 s of the core pile. Each arm shows those programs' FULL call
    # timelines (A3 drawing incl. requeue backdrop) in the SAME window.
    _clsord = {"bfcl": 0, "sharegpt": 1, "lats": 2}
    hl_pids_core = sorted({m["pid"] for m in seg["core"]},
                          key=lambda pid: (_clsord.get(
                              next(iter(idx["core"][k]["class"] for k in idx["core"]
                                        if k[0] == pid)), 3), pid))
    win_c = int(60e9)
    best_n, aw0 = -1, 0
    for tt in range(0, int(max(m["end"] for m in seg["core"])) - win_c, int(5e9)):
        n = sum(1 for m in seg["core"] if m["start"] < tt + win_c and m["end"] > tt)
        if n > best_n:
            best_n, aw0 = n, tt
    aw1 = aw0 + win_c
    w0m, w1m = aw0 / 1e6, aw1 / 1e6
    partsA4 = axis(w0m, w1m, 60, 2000)
    yA4 = 70
    _hl_set = set(hl_pids_core)
    for key, label, *_ in ARMS:
        sub = [c for c in C[key] if c["program_id"] in _hl_set]
        s_, yA4 = e2e_strip_tri(sub, CH[key], w0m, w1m, yA4,
                                f'{SHORTN[key]}（core 高延迟程序 {len(hl_pids_core)} 个的完整时间线）',
                                ARM_COLOR[key])
        yA4 += 10
        partsA4 += s_
    audit["windows"]["A4"] = {"criterion": "subjects = programs owning core top-pile "
                              "calls; window = densest 60 s of core pile; full call "
                              "timelines of those programs per arm, same window",
                              "window_s": [aw0 / 1e9, aw1 / 1e9],
                              "programs": hl_pids_core}
    figA4 = fig(partsA4, yA4 + 6)

    # ============ B: tables / figs on the Doc-B capture (BK) ================
    dfg_html_B = dfg_fig(W2[BK], "core" if BK == "core" else "core·ctrl_conc16")
    def one_row(tbl_html):
        m = re.search(r"(<table><tr>.*?</tr>)(.*)</table>", tbl_html, re.S)
        rows = re.findall(r"<tr><td>.*?</tr>", m.group(2), re.S)
        keep = [r for r in rows if r.startswith("<tr><td>core") or "agentix" in r[:40]]
        return m.group(1) + "".join(keep) + "</table>"
    if BK == "core":
        tbl_w_B = one_row(tbl_w)
        tbl_scope_B = one_row(tbl_scope)
        tbl_piles_B = ('<table><tr><th>#</th><th>类型</th><th>堆</th><th>成员数</th><th>时间和 s</th>'
                       '<th>高延迟成员</th></tr>' + "".join(
            f"<tr><td>{g['rank']}</td><td>{g['type'].replace('gpu_model_runner: ','').replace('w.sched: ','').replace('w.engine: ','').replace('w.run: ','')}</td>"
            f"<td>{g['pile']}</td><td>{g['members']:,}</td><td>{g['sum_ns']/1e9:.1f}</td>"
            f"<td>{g['hl_members']:,}</td></tr>"
            for g in json.loads((AT / "llama_core_cap16_views" / "GROUPS.json").read_text())["groups"][:8])
            + '</table>')
        tbl_phase, figB_P1, figB_P3 = "", "", ""
    else:
        hdr_w = ('<table><tr><th>臂</th><th>prepare_inputs 和（s）</th><th>其中 CUDA API</th>'
                 '<th>async 输出等待（和 / 均）</th><th>W5 代表 stage 集覆盖 host</th></tr>')
        tbl_w_B = hdr_w + w2row(BK, "core·ctrl") + "</table>"
        tbl_scope_B = ('<table><tr><th>臂（各 scope 时间和 s）</th><th>schedule</th><th>prepare</th>'
                       '<th>forward</th><th>sample</th><th>postproc</th><th>update</th><th>outputs</th>'
                       '<th>async 等待</th></tr>' + sc_row(BK, "core·ctrl") + "</table>")
        tbl_piles_B = ('<table><tr><th>#</th><th>类型</th><th>成员数</th><th>时间和 s</th></tr>' + "".join(
            f"<tr><td>{i+1}</td><td>{g['type'].replace('gpu_model_runner: ','').replace('w.sched: ','').replace('w.engine: ','').replace('w.run: ','')}"
            f" 堆{g['pile_index']}</td><td>{g['count']:,}</td><td>{g['sum_ns']/1e9:.1f}</td></tr>"
            for i, g in enumerate(P[BK]["hl"]["piles"][:8])) + '</table>')
    p1c = P[BK]["hl"]["piles"][0]
    sic = max(range(len(p1c["rows"])), key=lambda i: len(p1c["rows"][i]))
    secc = P[BK]["hl"]["sections"][sic]
    sbc, sec_e = int(secc["begin_ns"]), int(secc["end_ns"])
    obc = int(P[BK]["hl"]["origin"])
    partsB3 = axis((sbc - obc) / 1e6, (sec_e - obc) / 1e6, 60, 380)
    hB, yhB = hl_strip(P[BK]["hl"], 70, "core", sbc, sec_e)
    figB3 = fig(partsB3 + hB, yhB + 6)
    r0c = int(P[BK]["e2e"]["origin"]) - int(P[BK]["hl"]["origin"])
    wall_b = max(c["finished_rel_ms"] for c in C[BK])
    partsB4 = axis(0.0, wall_b, 60, 3 * 162 + 80)
    sc_, _yend = cu_strip(P[BK]["cu"], 70, "core（全程）", r0c, r0c + int(wall_b * 1e6))
    figB4 = fig(partsB4 + sc_, _yend + 6)
    if BK == "bcap":
        ph = spec_b["phases"]
        bl = [("批内请求数", [(ms, ms + 60, r) for ms, r, _ in wstep_b], 16, "#2a78d6", 16),
              ("批内 token 数", [(ms, ms + 60, tk) for ms, _, tk in wstep_b],
               max((tk for *_, tk in wstep_b), default=1), "#8a6bbf", None)]
        figB_P1, _ = deep_dive(BK, "core · P1 稳态满批 decode（构造相位）",
                               fixed=(ph["P1"][0] * 1e3, ph["P1"][1] * 1e3),
                               extra_lanes=bl, color="#1f7a4f")
        figB_P3, _ = deep_dive(BK, "core · P3 准入风暴（构造相位）",
                               fixed=(ph["P3"][0] * 1e3, min(ph["P3"][1] or 55, 50) * 1e3),
                               extra_lanes=bl, color="#a8541f")
        _db = sqlite3.connect(str(D[BK] / "cap.sqlite"))
        _dm = [(ts - _off_b) / 1e6 for ts, tx in _db.execute(
            "select start,text from NVTX_EVENTS where text like 'agentix.demote%'").fetchall()]
        _qb = [((ts - _off_b) / 1e6, tx.split("::")[-1]) for ts, tx in _db.execute(
            "select start,text from NVTX_EVENTS where text like 'agentix.chunk_begin%'").fetchall()]
        _db.close()
        def in_ph(v, name):
            lo = ph[name][0] * 1e3
            hi = (ph[name][1] if ph[name][1] is not None else wall_b / 1e3) * 1e3
            return lo <= v < hi
        def phstat(name):
            st = [x for x in wstep_b if in_ph(x[0], name)]
            reqs = [r for _, r, _ in st]
            toks = [tk for *_, tk in st]
            adm = {}
            for ts2, qq in _qb:
                if in_ph(ts2, name):
                    adm[qq] = adm.get(qq, 0) + 1
            return (f"<tr><td>{name}</td><td>{len(st):,}</td>"
                    f"<td>{sum(reqs)/max(len(reqs),1):.1f}</td>"
                    f"<td>{sum(toks)/max(len(toks),1):.0f}</td>"
                    f"<td>{'/'.join(f'{k2}:{v2}' for k2, v2 in sorted(adm.items())) or '—'}</td>"
                    f"<td>{sum(1 for v2 in _dm if in_ph(v2, name))}</td></tr>")
        tbl_phase = ('<table><tr><th>相位</th><th>step 数</th><th>批内请求均值</th>'
                     '<th>批内 token 均值</th><th>quantum 段准入（队列:次）</th><th>降级次数</th></tr>'
                     + "".join(phstat(n) for n in ("P1", "P2", "P3", "P4")) + "</table>")
    tbl_layer, layer_note, figB_rt, tbl_concwin = "", "", "", ""
    _pt_file = D.get("bcap", Path("/nonexistent")) / "PT_PROCESS_ANALYSIS.json" if BK == "bcap" else Path("/nonexistent")
    if _pt_file.exists():
        PT = json.loads(_pt_file.read_text())
        _ord = ["norm_in", "qkv_proj", "attn_core", "o_proj", "norm_post",
                "mlp_gate_up", "act_mul", "mlp_down"]
        fr = PT["fragments"]
        _HOOK_US = 5.8   # measured effective per-instance hook cost (macro/steps)
        tbl_layer = ('<table><tr><th>算子 process（模块打点实测）</th><th>fragment 中位数/实例</th>'
                     '<th>host 中位 µs</th><th>host−仪器 µs</th><th>device 中位 µs</th><th>界</th></tr>'
                     + "".join(
            f"<tr><td>{k}</td><td>{fr[k]['med_fragments']:.0f}</td>"
            f"<td>{fr[k]['med_host_us']}</td>"
            f"<td>{max(fr[k]['med_host_us'] - _HOOK_US, 0):.1f}</td>"
            f"<td>{fr[k]['med_device_us']}</td>"
            f"<td>{'device' if fr[k]['med_device_us'] > max(fr[k]['med_host_us'] - _HOOK_US, 0) else 'launch/host'}</td></tr>"
            for k in _ord if k in fr) + '</table>')
        gr = PT["global_rank_top"]
        dr = PT.get("device_rank", [])
        tbl_layer += ('<table><tr><th>排名（host 观测宇宙：NVTX 区间墙钟，异步发射下'
                      '≈Python+发射，不含设备执行）</th><th>顶堆成员</th><th>顶堆时间和 s</th></tr>'
                      + "".join(
            f"<tr><td>#{i+1} {r['process']}</td><td>{r['members']:,}</td>"
            f"<td>{r['sum_ns']/1e9:.2f}</td></tr>" for i, r in enumerate(gr[:5])) + '</table>')
        if dr:
            tbl_layer += ('<table><tr><th>排名（device 归因宇宙：correlation 指派的 kernel '
                          '设备时间）</th><th>device 和 s</th><th>host 和 s</th></tr>' + "".join(
                f"<tr><td>#{i+1} {r['process']}</td><td>{r['device_sum_ns']/1e9:.2f}</td>"
                f"<td>{r['host_sum_ns']/1e9:.2f}</td></tr>" for i, r in enumerate(dr[:6]))
                + '</table>')
        php = PT["phases"]
        _pp = ["qkv_proj", "attn_core", "mlp_down"]
        tbl_layer += ('<table><tr><th>相位 × process（n / 中位 µs）</th>'
                      + "".join(f"<th>{k}</th>" for k in _pp) + '</tr>' + "".join(
            f"<tr><td>{ph}</td>" + "".join(
                (lambda d_: f"<td>{d_['n']:,} / {d_['med_us']}</td>" if d_ else "<td>—</td>")(
                    php.get(ph, {}).get(k)) for k in _pp) + "</tr>"
            for ph in ("P1", "P2", "P3")) + '</table>')
        rt = PT.get("ranked_top_pile_instances", {})
        _e2o2 = int(P[BK]["e2e"]["origin"])
        wall_bb = max(c["finished_rel_ms"] for c in C[BK])
        parts_rt = axis(0.0, wall_bb, 60, 40 + 90 * max(len(rt), 1))
        _yr = 70
        for _pn, _iv in rt.items():
            parts_rt.append(f'<text x="{LEFT-6}" y="{_yr+14}" font-size="15" text-anchor="end" '
                            f'fill="#48607d">{_pn}</text>')
            parts_rt.append(f'<rect x="{LEFT}" y="{_yr}" width="{W-LEFT-RIGHT}" height="70" '
                            f'fill="#fbfbf9" stroke="#eee"/>')
            for _s0, _d0 in _iv:
                _ms = (_s0 - _e2o2) / 1e6
                _x = LEFT + (W - LEFT - RIGHT) * min(max(_ms, 0), wall_bb) / wall_bb
                _w = max((W - LEFT - RIGHT) * (_d0 / 1e6) / wall_bb, 0.6)
                parts_rt.append(f'<rect x="{_x:.1f}" y="{_yr+8}" width="{_w:.1f}" height="54" '
                                f'fill="#a8541f" opacity=".55"/>')
            _yr += 90
        figB_rt = fig(parts_rt, _yr + 6)
        _bkt = [(1, 4), (5, 8), (9, 12), (13, 16)]
        _tot = len(wstep_b) or 1
        _rows_cw = ""
        for lo2, hi2 in _bkt:
            st2 = [x for x in wstep_b if lo2 <= x[1] <= hi2]
            _rows_cw += (f"<tr><td>{lo2}–{hi2} 请求</td><td>{len(st2):,}</td>"
                         f"<td>{100*len(st2)/_tot:.0f} %</td>"
                         f"<td>{(sum(x[2] for x in st2)/max(len(st2),1)):.0f}</td></tr>")
        tbl_concwin = ('<table><tr><th>并发档位（批内请求数）</th><th>step 数</th>'
                       '<th>step 占比</th><th>批内 token 均值</th></tr>' + _rows_cw + '</table>')
        layer_note = ("<b>正式实现（Stage W→T 工作流产物）：</b>process 由模块结构确定"
                      "（PROCESS_TAXONOMY，四门验证通过），trace 为模块打点 eager 仪器臂"
                      "（perf_trace 双臂契约：时序结论以 graph 性能臂为准，本臂供结构与归因；"
                      "仪器臂 wall 47.1 s 对性能臂 37.5 s，开销 +26 % 已披露）。"
                      "fragment 表是 process→fragment→kernel 的实测：qkv/o/mlp 为 device 界"
                      "（GEMM 真算力），attn_core 与两个 norm 为 launch/host 界——"
                      "仪器开销已双尺度量化。宏观三臂差分（同负载同 nsys）：graph 性能臂 37.6 s → eager 无 hook 44.6 s（<b>eager 代价 +7.0 s / +18.6 %</b>，cudagraph 消失的发射开销）→ eager+hook 47.1 s（<b>hook 代价 +2.5 s / +5.6 %</b>，≈1.66 ms/步 ≈ 5.8 µs/实例）。微观裸基准：hook 派发+NVTX 对 = 2.7 µs/实例（nvtx 对本身 0.26 µs）——nsys 与竞争下约 ×2，两尺度自洽。占 norm 类 host 30.8 µs 的 ~9–19 %、attn_core 280 µs 的 ~1–2 %，扣除后界判定不变（norm 仍 ≫ device 2.3 µs）。launch-bound 结论第一次落到算子粒度。两张排名表口径互补：host 观测宇宙由 attn_core 领跑（Python 包装 + 5 fragment 发射），device 归因宇宙由 mlp_gate_up/down 与 qkv 领跑（真算力）——同一批 process、两种「谁最重」，正是 host 节奏主导、GEMM 算力其内的双层结构。")
    if BK == "bcap" and not _pt_file.exists():
        _db = sqlite3.connect(str(D[BK] / "cap.sqlite"))
        _q = ("select n.start,n.end from NVTX_EVENTS n left join StringIds s on n.textId=s.id "
              "where coalesce(n.text,s.value)='gpu_model_runner: forward' and n.end is not null "
              "order by n.start")
        _fw = _db.execute(_q).fetchall()
        def _kname(n):
            n = (n or "?")
            if "rms_norm_0" in n: return "norm_in"
            if "rms_norm_2" in n: return "norm_post"
            if "cutlass" in n or "gemm" in n.lower(): return "gemm"
            if "reshape_and_cache" in n: return "kv_write"
            if "flash_fwd" in n: return "attn_core"
            if "silu" in n: return "act_mul"
            if "rotary" in n or "_poi_fused_3" in n: return "rope"
            if "elementwise" in n: return "resid_ew"
            return "other"
        GEMM_NAME = ["qkv_proj", "o_proj", "mlp_gate_up", "mlp_down"]
        import random as _rnd
        _rnd.seed(7)
        # sample from the CONSTRUCTED pure-decode phase P1 (that is what it is for)
        _e2o = int(P[BK]["e2e"]["origin"])
        _p1 = spec_b["phases"]["P1"]
        _lo, _hi = _e2o + int(_p1[0] * 1e9), _e2o + int(_p1[1] * 1e9)
        _mid = [i for i in range(len(_fw) - 1) if _lo <= _fw[i][0] < _hi]
        if len(_mid) < 8:
            _mid = [i for i in range(len(_fw) // 3, 2 * len(_fw) // 3)]
        proc_t = defaultdict(list)     # per-layer-instance process time (µs)
        frag_n = defaultdict(set)      # kernels per process
        layer_w = []
        for i in _rnd.sample(_mid, min(40, len(_mid))):
            s_, e_ = _fw[i][0], _fw[i + 1][0]
            ks = _db.execute("select k.start,k.end,sv.value from CUPTI_ACTIVITY_KIND_KERNEL k "
                             "left join StringIds sv on k.demangledName=sv.id "
                             "where k.start>=? and k.start<? order by k.start", (s_, e_)).fetchall()
            starts = [j for j, (_a, _b, n) in enumerate(ks) if _kname(n) == "norm_in"]
            for pi in range(len(starts) - 1):
                seg_k = ks[starts[pi]:starts[pi + 1]]
                if not (9 <= len(seg_k) <= 18):
                    continue
                layer_w.append((ks[starts[pi + 1]][0] - seg_k[0][0]) / 1e3)
                gi = 0
                acc = defaultdict(float)
                for _a, _b, n in seg_k:
                    kn = _kname(n)
                    if kn == "gemm":
                        kn = GEMM_NAME[min(gi, 3)]
                        gi += 1
                    acc[kn] += (_b - _a) / 1e3
                    frag_n[kn].add((n or "?")[:60])
                for kn, v in acc.items():
                    proc_t[kn].append(v)
        _db.close()
        def _med(v): return statistics.median(v) if v else 0.0
        def _pct(v, q): return sorted(v)[int(q * (len(v) - 1))] if v else 0.0
        lw = _med(layer_w)
        order = ["norm_in", "qkv_proj", "rope", "kv_write", "attn_core", "o_proj",
                 "norm_post", "mlp_gate_up", "act_mul", "mlp_down", "resid_ew", "other"]
        rows_l = "".join(
            f"<tr><td>{kn}</td><td>{len(frag_n.get(kn, []))}</td>"
            f"<td>{_med(proc_t.get(kn, [])):.2f}</td>"
            f"<td>{100 * _med(proc_t.get(kn, [])) / max(lw, 1e-9):.0f} %</td></tr>"
            for kn in order if kn in proc_t)
        tbl_layer = (f'<table><tr><th>算子 process（层内，按周期位置+名字语义重建）</th>'
                     f'<th>fragment 种类</th><th>中位 µs/层</th><th>占层墙钟</th></tr>{rows_l}'
                     f'<tr><td><b>layer 墙钟（32 层，周期起点差）</b></td><td>—</td>'
                     f'<td>{lw:.1f}</td><td>层间 p10/p90 = {_pct(layer_w, .1):.1f}/{_pct(layer_w, .9):.1f}</td></tr></table>')
        layer_note = (f"<b>过渡实现（正式版将按 workload_profile→perf_trace 工作流重做，见 B_BATCH_TRACE_PLAN 第二部分）：</b>当前为 kernel 序列周期折叠，采样窗仍混入 chunked-prefill 步、注意力核归组不完整，本表数字只示意层级可达性、不作结论。重建依据：P1 相位内采样 {min(40, len(_mid))} 个 step，按 step 起点→下一 step 起点取设备侧完整 "
                      f"kernel 序列（node 级图内 kernel 可见；设备执行拖出 host scope，故不以 host "
                      f"范围截断），以 norm_in 为周期锚切层，每层 ~13 kernel；gemm 按周期内出现"
                      f"次序命名为 qkv/o/gate_up/down。")
    if BK == "bcap":
        dwin = (spec_b["phases"]["P3"][0] * 1e3, min(spec_b["phases"]["P3"][1] or 55, 50) * 1e3)
    else:
        dwin = tuple(audit["windows"]["part4_deepdive"]["core"]["figure_window_s"][i] * 1e3 for i in (0, 1))
    e2oc = int(P[BK]["e2e"]["origin"])
    at_c = kernel_micro_best(D[BK] / "cap.sqlite", e2oc + int(dwin[0] * 1e6),
                             e2oc + int(dwin[1] * 1e6), int(300e6))
    mparts, mye, mbusy, mgemm = kernel_micro_strip(D[BK] / "cap.sqlite", 60, "core", at_c, int(300e6))
    figB4m = fig(mparts, mye + 6)
    import csv as _csv
    _rows = list(_csv.reader((AT / "ncu_focus" / "focus2_raw.csv").open()))
    _h = _rows[0]
    _c = lambda n: _h.index(n)
    ncu_tr = ""
    for r in _rows[2:]:
        ncu_tr += ("<tr><td>" + r[_c('Kernel Name')][:44] + "</td>"
                   f"<td>{float(r[_c('launch__grid_size')]):.0f}×{float(r[_c('launch__block_size')]):.0f}</td>"
                   f"<td>{float(r[_c('gpu__time_duration.sum')])*1e3:.0f}</td>"
                   f"<td>{float(r[_c('lts__t_sector_hit_rate.pct')]):.1f}</td>"
                   f"<td>{float(r[_c('lts__throughput.avg.pct_of_peak_sustained_elapsed')]):.1f}</td>"
                   f"<td>{float(r[_c('sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active')]):.1f}</td>"
                   f"<td>{float(r[_c('sm__throughput.avg.pct_of_peak_sustained_elapsed')]):.1f}</td>"
                   f"<td>{float(r[_c('dram__bytes.sum.per_second')]):.0f}</td>"
                   f"<td>{float(r[_c('gpu__dram_throughput.avg.pct_of_peak_sustained_elapsed')]):.1f}</td>"
                   f"<td>{float(r[_c('sm__warps_active.avg.pct_of_peak_sustained_active')]):.1f}</td></tr>")
    tbl_ncu = ('<table><tr><th>kernel（重放）</th><th>grid×block</th><th>时长 µs</th>'
               '<th>L2 命中 %</th><th>L2 吞吐 %峰</th><th>tensor pipe %</th><th>SM 吞吐 %峰</th>'
               '<th>DRAM GB/s</th><th>DRAM %峰</th><th>warp 占用 %</th></tr>' + ncu_tr + '</table>')
    sig_c = chunk_sig.get("core", (0, 0, 0))
    if BK == "bcap":
        _f2, _l2 = [], []
        for segs_ in CH[BK].values():
            for i2, (b2, e2, _q2) in enumerate(sorted(segs_)):
                (_f2 if i2 == 0 else _l2).append(e2 - b2)
        if _l2:
            sig_c = (statistics.median(_f2), statistics.median(_l2), len(_l2))
    async_core_s = next((b["sum_ns"] / 1e9 for b in W2[BK]["dominant_idle_boundaries"]
                         if "set_async" in b["boundary"]), 0.0)
    prep_core_s = W2[BK]["prepare_inputs_api_split"]["window_union_ns"] / 1e9


    # =================== A6: sticky routing reproduction ===================
    A6 = ""
    _rdir = a.art / "routing"
    _fs = _rdir / "sticky" / "calls_routing_sticky.jsonl"
    _fr = _rdir / "rr" / "calls_routing_rr.jsonl"
    if _fs.exists() and _fr.exists():
        CR = {"S": [json.loads(l) for l in _fs.open()],
              "R": [json.loads(l) for l in _fr.open()]}
        SUMR = {k: json.loads((_rdir / d / f"summary_routing_{d}.json").read_text())["observed"]
                for k, d in (("S", "sticky"), ("R", "rr"))}
        idxR = {k: {(c["program_id"], c["call_index"]): c for c in CR[k]} for k in CR}
        floorR = {ck: min(idxR[k][ck]["finished_rel_ms"] - idxR[k][ck]["first_token_rel_ms"]
                          for k in CR if ck in idxR[k]) for ck in idxR["S"]}
        # TTFT x context buckets
        _bk = [(0, 256), (257, 512), (513, 1024), (1025, 2048), (2049, 2800)]
        def _ttft_med(k, lo, hi):
            v = sorted(c["first_token_rel_ms"] - c["submitted_rel_ms"] for c in CR[k]
                       if lo <= c["context_len"] <= hi)
            return v[len(v) // 2] if v else 0.0, len(v)
        rows_t = ""
        for lo, hi in _bk:
            s_, ns_ = _ttft_med("S", lo, hi)
            r_, nr_ = _ttft_med("R", lo, hi)
            rows_t += (f"<tr><td>{lo}–{hi}</td><td>{ns_}</td><td>{s_:.0f}</td>"
                       f"<td>{r_:.0f}</td><td>{(r_/max(s_,1e-9)):.2f}×</td></tr>")
        tblA6_t = ('<table><tr><th>context 长度档（token）</th><th>n</th>'
                   '<th>sticky TTFT p50 ms</th><th>rr TTFT p50 ms</th><th>rr/sticky</th></tr>'
                   + rows_t + '</table>')
        eS, eR = SUMR["S"], SUMR["R"]
        tblA6_e = ('<table><tr><th></th><th>TTFT mean/p50/p90 ms</th>'
                   '<th>PTL mean/p90 ms/tok</th><th>wall s</th><th>thr tok/s</th></tr>'
                   + "".join(
            f"<tr><td>{lab}</td><td>{e['ttft_ms']['mean']:.0f}/{e['ttft_ms']['p50']:.0f}/"
            f"{e['ttft_ms']['p90']:.0f}</td>"
            f"<td>{e['program_token_latency_ms']['mean']:.1f}/"
            f"{e['program_token_latency_ms']['p90']:.1f}</td>"
            f"<td>{e['wall_s']:.0f}</td><td>{e['throughput_tokens_per_s']:.0f}</td></tr>"
            for lab, e in (("sticky（程序→固定引擎）", eS), ("round-robin（逐调用轮转）", eR)))
                   + '</table>')
        RMETA = [("S", "sticky", 0, 0), ("R", "rr", 0, 0)]
        blocksR, ybR, pwinR = e2e_program_blocks(CR, {"S": {}, "R": {}}, RMETA, floorR)
        figA6_e2e = fig(blocksR, ybR + 4)
        audit["windows"]["A6_blocks"] = {"criterion": "same per-program window rule as A3",
                                         "program_windows_s": pwinR}
        # A4-style band: call set = rr top pile identities (where affinity loss hurts)
        segR = {k: call_top_pile(CR[k]) for k in CR}
        keysR = [(m["pid"], m["idx"]) for m in segR["R"]]
        win_r = int(60e9)
        bn, r0w = -1, 0
        for tt in range(0, max(int(max(m["end"] for m in segR["R"])) - win_r, 1), int(5e9)):
            n = sum(1 for m in segR["R"] if m["start"] < tt + win_r and m["end"] > tt)
            if n > bn:
                bn, r0w = n, tt
        r1w = r0w + win_r
        partsA6 = axis(r0w / 1e6, r1w / 1e6, 60, 900)
        yA6 = 70
        for k in ("S", "R"):
            mem = []
            for pid, ci in keysR:
                r = idxR[k].get((pid, ci))
                if r is None:
                    continue
                mem.append({"pid": pid, "idx": ci, "cls": r["class"],
                            "start": int(r["submitted_rel_ms"] * 1e6),
                            "end": int(r["finished_rel_ms"] * 1e6),
                            "d": int((r["finished_rel_ms"] - r["submitted_rel_ms"]) * 1e6)})
            inw = [m for m in mem if m["start"] < r1w and m["end"] > r0w]
            s_, yA6 = hl_prog_strip(inw, yA6, f'{{"S":"sticky","R":"rr"}}'[0] and ("sticky" if k=="S" else "rr")
                                    + f'（rr 顶堆 call 集，窗内 {len(inw)}/{len(mem)}）', r0w, r1w)
            yA6 += 8
            partsA6 += s_
        figA6_hl = fig(partsA6, yA6 + 6)
        audit["windows"]["A6_band"] = {"criterion": "call set = rr top-pile identities; densest 60 s of rr pile",
                                       "window_s": [r0w / 1e9, r1w / 1e9], "set_size": len(keysR)}
        A6 = f"""
<h2>A6 第三组创新复现 —— sticky 路由（多引擎 KV 亲和）</h2>
<div class="block"><b>设置与复用面</b>
<p>1.5B 级模型（本地 Qwen3-1.7B）双引擎共驻一张 4090（两 CUDA 上下文，各 0.46 显存），
同负载（thr_mixed r0.5 的 25 程序/2,440 调用）同参；唯一变量 = 路由器：<b>sticky</b> =
程序→固定引擎（进程表亲和，论文③）对 <b>round-robin</b> = 逐调用轮转（破坏程序内亲和）。
真实复用面按论文图 7 构造：每程序私有 token 流、call j 的 prompt = 流前 L<sub>j</sub> 个
token 严格递增（cap 2800）——程序内前缀精确嵌套（同引擎命中/异引擎整段重算）、跨程序零共享。
边界：双引擎共享一张卡的算力与带宽（论文为多卡多引擎），故吞吐口径仅作参考、命中效应看
TTFT。</p></div>
{tblA6_e}
<p class="cap">端点总览；命中兑现看 TTFT 列。</p>
{tblA6_t}
<p class="cap">rr/sticky 的 TTFT 比随 context 单调增长。sticky 平坦是命中兑现，rr 线性抬升
是整段冷 prefill——亲和的价值随上下文变贵。</p>
<h3>A6a 端到端 call 时间线（与 A3 同款：每程序 S/R 两行）</h3>
{figA6_e2e}
<p class="cap">rr 行的红段随程序推进逐 call 变宽，S 行始终窄。变宽的部分是被换引擎后重算的
前缀——亲和丢失的代价随上下文增长。</p>
<h3>A6b 高延迟 call 带（与 A4 同款：rr 顶堆身份、同窗对照）</h3>
{figA6_hl}
<p class="cap">rr 臂认定的高延迟 call，在 sticky 带里明显缩短。差值就是冷 prefill 的时间，
亲和路由把它省掉了。</p>"""
    # =================== DOC A: 复现论文机制与学习 ==========================
    docA = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>Agentix 机制复现与学习 · 四臂消融</title><style>
body{{margin:0;font:22px/1.7 "Noto Sans CJK SC",system-ui,sans-serif;color:#1f2f45;background:#fff}}
.wrap{{max-width:1200px;margin:0 auto;padding:26px 22px 60px}}
h1{{font-size:33px;margin:0 0 6px}} h2{{font-size:27px;color:#2f6f9f;margin:36px 0 6px}}
h3{{font-size:22px;margin:20px 0 6px}}
.sub,.cap,.theme{{font-size:20px;color:#48607d;max-width:120ch}}
.cap{{margin:6px 0 0}} .theme{{margin:10px 0 8px}}
.block{{background:#f2f7fb;border:1px solid #c9d6e4;border-radius:6px;padding:12px 16px;margin:10px 0;font-size:20px;max-width:120ch}}
.block.impl{{background:#f4faf6;border-color:#bcd8c6}}
.block.howto{{background:#fbf7ef;border-color:#e2d3ae}}
.pfig{{margin:10px 0;max-width:980px}}
.pfig img{{width:100%;height:auto;border:1px solid #c9d6e4;border-radius:6px;background:#fff}}
.pfig figcaption{{font-size:19px;color:#48607d;margin-top:4px;line-height:1.6}}
.block b{{display:block;margin-bottom:2px;color:#2f6f9f}}
.block p{{margin:4px 0}}
table{{border-collapse:collapse;font-size:20px;margin:10px 0}}
td,th{{border:1px solid #c9d6e4;padding:4px 10px;text-align:right}}
td:first-child,th:first-child{{text-align:left}}
pre.art{{background:#f7f9f7;border:1px solid #cfd9cf;border-radius:6px;padding:12px 14px;
font:18px/1.55 "IBM Plex Mono","Noto Sans Mono CJK SC",monospace;overflow-x:auto;max-width:1150px}}
</style></head><body><div class="wrap">
<h1>Agentix 论文机制复现与学习 —— 方法、消融负载与四臂性能 trace</h1>
<p class="sub">目的：复现论文机制并从中学习。结构：A1 方法与 baseline（学习核心）→ A2 消融
设计与度量 → A3 端到端 call 时间线 → A4 高延迟 call 的程序分堆 → A5 端点全景与论文口径。
数据：LLaMA-3.1-8B · thr_mixed r0.5 · cap16 四臂各一次完整采集（A00 守恒门全过）+
4 臂 × 5 到达率端点。process 层次的深入分析（call 内部 step/scope/kernel）在姊妹文档
《R10_PROCESS》。审计：R10_AUDIT.json。</p>

<h2>A0 负载理解 —— 场景、prog/call/step/scope 定义与生命周期串讲</h2>

<p class="theme"><b>场景先行。</b>本负载取三个真实 agent 场景：<b>工具代理</b>（bfcl——模型
反复调用外部工具，每次生成短，调用之间隔着工具延迟）；<b>多轮会话</b>（sharegpt——人与模型
往返，每轮生成长）；<b>树搜索</b>（lats——MCTS 式搜索，每波 5 路并行展开、近两百次生成连成
深链）。论文图 1 给出这类场景的一般形态（DAG）：</p>
{pf(1)}
<p class="theme"><b>由场景到定义。</b>要说清这三种场景在 serving 引擎里的行为，需要四层
词汇：一个场景实例（会话/任务全程）称为 <b>program</b>（三类共 25 个）；program 内的一次
LLM 请求是 <b>call</b>（共 2,440 个）；引擎的一次连续批迭代是 <b>step</b>（一个 step 同时
服务至多 16 个 call 各一次 decode 迭代，约 1.5 万步/捕获）——一个 call 的服务由几十到上千个
step 拼成，这就是"调度只能改 call 进 step 的顺序、改不了 step 本身"的结构原因；step 内的
引擎阶段是 <b>stage</b>（schedule / prepare / sample 等运行时阶段——batch8 术语下不称 process；模型算子才是 process，由 kernel 经 fragment 组成，姊妹文档 B2 的 DFG 画的就是
它们）。三类场景的区分完全落在前两层：bfcl = call 短而多，sharegpt = call 长而少，
lats = call 洪流 + 波并行：</p>
{compo_tbl}
<p class="cap"><b>表注：</b>三类程序的组成实测（负载规格冻结 JSON 与 trace 三方对账，A00 门）。</p>
{pf(11)}
<h3>A0b 负载场景的生命周期 —— 用四层定义串起来</h3>
<p class="theme">把定义放回场景（下面三张图是各类一个中位规模的真实实例，opt 臂 trace）：
bfcl program 的生命周期是"call（等待→服务）→ 工具延迟 → 下一 call"的串行链，寿命由等待与
工具延迟主导；sharegpt program 是少数长 call 的接力，寿命由服务段主导；lats program 是每波
5 个并行 call 的推进，波内要等最慢一路（关键路径）——它的 call 都小，program 却最长。</p>
{life_html}
{pf(5)}

{METH}

<h2>A2 消融设计与度量</h2>
<p class="theme"><b>负载：</b>即 A0 的三类合成混载（组成表与校准图见 A0）。<b>消融设计：</b>
三个首尾相接的单变量对——素→opt（状态复用）、opt→MLFQ（调用级抢占）、MLFQ→core（程序
身份），每对只差一个变量、均有全链 trace。</p>
{tri_def}
{pf(17)}

<h2>A3 端到端 call 时间线 —— 执行分布与消融的运行时差异</h2>
<p class="theme">本图逐块画出全部 25 个程序：三类中位实例（A0 生命周期）、等待最重的短程序
（A1 走查对象）与 W5 代表 stage 所服务的调用都在其中。方法与消融设计见 A1，这里只看运行时。</p>
{pf(9)}
<div class="block howto"><b>读图规则</b>
<p>每程序一块，块内四行为 素/opt/M/C，块头标窗口（生命周期 ≤40 s 取全程，否则取四臂活动最密
的 30 s，块间无公共轴）。红段 = 首token等待；类别色段 = quantum 段；浅红底 = chunk 未覆盖的
段内等待（仅 M/C 存在）。行尾两个数：等 = Σ<sub>call</sub>（端到端 − 执行底），执行底取同
call 四臂最小驻留，排队、再排队、再 prefill 全部计入；ms/tok = 程序响应 ÷ 产出 token。四行
中等待最短者加粗。顶部绿幅与各类蓝幅给出两指标的聚合值与各自赢家。</p></div>
<div class="block howto"><b>两个指标的区别 —— 指标阶梯</b>
{tbl_ladder}
<p>赢家在 ②→③ 之间翻转：程序等权仍按秒计时 M 赢，除以产出 token 后 C 赢。论文指标原文
（§Metrics）就是 ④："program-level token latency = the average of total program response
time divided by the number of tokens generated"（多线程取关键路径，∝ 平均 JCT）。Σ等待是
调度的杠杆量，token 归一化的程序延迟是目标量——M 压掉洪流的等待秒数，但没有提升它每 token
的服务效率。</p></div>
{fig1}
<p class="cap">顶部绿幅里 Σ等待的赢家是 M、程序延迟的赢家是 C，块内红段逐臂缩短、浅红底从
短程序块移到 lats 块。等待被程序身份重新分配，而论文口径的目标量由 core 拿下——消融的运行时
差异与两本账的分离在同一张图里。</p>
<p class="theme"><b>类内读数：</b>等待均值 bfcl 素 30.1 → opt 13.6 → M 4.4 → C 3.0 s
（目标类上 C 为 opt 的 1/4.5）；sharegpt opt 9.1 s 最短，M 51.7 s 被续段 recompute 惩罚；
lats M 199.7 s 最短，C 294.5 ≈ opt 293.3 s（压后是设计）。逐块加粗因此是"谁受益、谁买单"
的地图：sharegpt 为 quantum 切割买单，lats 为压后买单，与 A2 表第三列一致。</p>
<p class="theme"><b>与论文对照：</b>按论文指标（图内 ④）我们与论文同判——core 全面最优
（mean 20.8、p99 34.7，附录五率全序），论文的 Mixed 面板（三类等比抽样）同样由 Agentix 拿
最大倍数（15×/5.5×/5×）。"M 更优"只出现在论文从不使用的 Σ等待秒数口径。残余偏差三项：论文
MLFQ 用 swap（我们 recompute，故我们的 M 在 sharegpt 上更差）；论文 LATS 的 2.5× 含 ATLAS
gang 与多卡形态（我们未复刻，lats 上 C≈opt）；抽样比不同（论文等比，我们 8/5/12）。</p>

<h2>A4 调度行为对照 —— core 的高延迟程序，同一时间窗里四种方法的时间线分布</h2>
{pf(6)}
<p class="theme"><b>对照对象与看点：</b>主体 = <b>core 认定的高延迟程序</b>（core 最高时长簇
的归属程序，清单见审计文件）；窗口 = core 该簇最密的 60 s；四条带在同一窗内画这些程序的
<b>完整时间线</b>（全部 call，画法同 A3：红=等待、色段=quantum 段、浅红底=chunk 未覆盖
间隙）。分布差异即调度行为：<b>core 带</b>里这些程序的 call 被整体压后、聚拢成密簇（低队准入
+ 大 quantum 少切）；<b>opt/素带</b>里同样这些程序提早铺满全窗（FCFS 让洪流先占批槽——被挤走
的短程序不在本图主体里，它们的代价见 A3）；<b>M 带</b>里被 quantum 切碎成条纹、浅红底密布。
"认得程序身份、让重程序集体让步"这一 agentix 特征，只有在同主体、同窗口的对照里才可见。</p>
{figA4}
<p class="cap">同一批程序在同一窗口里的四种分布：core 带把它们聚拢压后，opt/素带提早铺满，M 带被切成条纹。压后的聚簇正是程序身份在起作用，其他三种排法都给不出这个形状。</p>

{a.fourarm.read_text().replace("<h2>四、论文四臂复现 —— vLLM / vLLM-opt / MLFQ / Agentix 全基线对照</h2>", "<h2>A5 端点全景 —— 论文口径的四臂复现</h2>")}

{A6}

<h3>附·论文评测原图对照（多引擎/扩展性/开销项，本复现范围之外的部分以偏差表衔接）</h3>
{pf(12)}{pf(13)}{pf(14)}{pf(15)}{pf(16)}{pf(18)}{pf(20)}


<h2>记账</h2>
<p class="theme"><b>trace 开销阶梯（量化与消除策略）：</b>nsys 采集 +0.4/0.9/2.3/1.2 %
（素/opt/M/C，同配置无 nsys 端点对照实测）；19 个 host 探针 −0.9 %（噪声内）；模块级 hook
仅存在于 B 的仪器臂。消除策略 = 双臂契约：<b>端点数字全部取自无 nsys 裸跑</b>（A5 的 4×5
campaign），时间线取自 +1 % 级的 nsys 臂，结构归因取自仪器臂并做扣除——host 大占比的两个
主发现（async 输出等待、prepare_inputs 纯 Python）在近零开销的 graph 臂上同样成立，非
trace 伪影。</p>
<p class="theme">窗口与选材标准在 R10_AUDIT.json；A00 守恒门四臂 <code>all_pass</code>；
配对事实 pair_facts_*.json 与本文数字同源。原始 trace：release h22-h23-traces；
本页与端点数据：release h23-r10-reports。</p>
</div></body></html>"""

    if BK == "bcap":
        ver_note = ("<b>数据：受控并发 batch 采集 ctrl_conc16</b>（batch8/16 方法迁移：构造 "
                    "W/P1/P2/P3/P4 并发相位，见 workflow06/B_BATCH_TRACE_PLAN.md；分析窗口是"
                    "构造的、不是搜索的；perf_trace 收尾件——排名 process 时间线与并发窗表——已含于 B4b）。")
    else:
        ver_note = ("<b>版本注：本页为 v0 草稿</b>——基于 r0.5 开环采集；正式版换用受控并发 "
                    "batch 采集（计划见 workflow06/B_BATCH_TRACE_PLAN.md）。")
    if BK == "bcap":
        _adm_tot = {}
        for _ts3, _q3 in _qb:
            _adm_tot[_q3] = _adm_tot.get(_q3, 0) + 1
        adm_note = ("quantum 段准入 " + "/".join(f"{k3}:{v3}" for k3, v3 in sorted(_adm_tot.items()))
                    + f"、降级 {len(_dm)} 次（相位细分见 B4 表）")
    else:
        adm_note = "准入 Q0–Q3 = 97/102/237/2004、降级 151 次"
    # =================== DOC B: process 层次分析（面向优化） ================
    docB = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>Agentix serving 的 process 层次分析</title><style>
body{{margin:0;font:22px/1.7 "Noto Sans CJK SC",system-ui,sans-serif;color:#1f2f45;background:#fff}}
.wrap{{max-width:1200px;margin:0 auto;padding:26px 22px 60px}}
h1{{font-size:33px;margin:0 0 6px}} h2{{font-size:27px;color:#2f6f9f;margin:36px 0 6px}}
h3{{font-size:22px;margin:20px 0 6px}}
.sub,.cap,.theme{{font-size:20px;color:#48607d;max-width:120ch}}
.cap{{margin:6px 0 0}} .theme{{margin:10px 0 8px}}
.block{{background:#f2f7fb;border:1px solid #c9d6e4;border-radius:6px;padding:12px 16px;margin:10px 0;font-size:20px;max-width:120ch}}
.block.impl{{background:#f4faf6;border-color:#bcd8c6}}
.block.howto{{background:#fbf7ef;border-color:#e2d3ae}}
.pfig{{margin:10px 0;max-width:980px}}
.pfig img{{width:100%;height:auto;border:1px solid #c9d6e4;border-radius:6px;background:#fff}}
.pfig figcaption{{font-size:19px;color:#48607d;margin-top:4px;line-height:1.6}}
.block b{{display:block;margin-bottom:2px;color:#2f6f9f}}
.block p{{margin:4px 0}}
table{{border-collapse:collapse;font-size:20px;margin:10px 0}}
td,th{{border:1px solid #c9d6e4;padding:4px 10px;text-align:right}}
td:first-child,th:first-child{{text-align:left}}
pre.art{{background:#f7f9f7;border:1px solid #cfd9cf;border-radius:6px;padding:12px 14px;
font:18px/1.55 "IBM Plex Mono","Noto Sans Mono CJK SC",monospace;overflow-x:auto;max-width:1150px}}
</style></head><body><div class="wrap">
<h1>Agentix serving 的 process 层次分析与 trace —— 面向进一步优化</h1>
<p class="sub">目的：为后续性能优化（动态并发/抢占机制探索，S1–S4 计划）提供分析基座。
对象：agentix_core 臂（论文机制本体）。<b>版本注：本页为 v0 草稿</b>——基于 r0.5 开环采集；正式版将换用受控并发 batch 采集（batch8/16 方法：构造并发相位凸显机制特征，计划见 workflow06/B_BATCH_TRACE_PLAN.md）。process 宇宙分层沿
auto_trace batch8/16 契约（request→forward/iter→scope→kernel，10 % 阈值 + 对数时长五堆聚类
+ 全局排名）。四臂消融与机制学习在姊妹文档《R10_ABLATION》。</p>

<h2>B1 负载场景、process 层次与方法（合并简述）</h2>

<p class="theme"><b>场景先行。</b>本负载取三个真实 agent 场景：<b>工具代理</b>（bfcl——模型
反复调用外部工具，每次生成短，调用之间隔着工具延迟）；<b>多轮会话</b>（sharegpt——人与模型
往返，每轮生成长）；<b>树搜索</b>（lats——MCTS 式搜索，每波 5 路并行展开、近两百次生成连成
深链）。论文图 1 给出这类场景的一般形态（DAG）：</p>
{pf(1)}
<p class="theme"><b>由场景到定义。</b>要说清这三种场景在 serving 引擎里的行为，需要四层
词汇：一个场景实例（会话/任务全程）称为 <b>program</b>（三类共 25 个）；program 内的一次
LLM 请求是 <b>call</b>（共 2,440 个）；引擎的一次连续批迭代是 <b>step</b>（一个 step 同时
服务至多 16 个 call 各一次 decode 迭代，约 1.5 万步/捕获）——一个 call 的服务由几十到上千个
step 拼成，这就是"调度只能改 call 进 step 的顺序、改不了 step 本身"的结构原因；step 内的
引擎阶段是 <b>stage</b>（schedule / prepare / sample 等运行时阶段——batch8 术语下不称 process；模型算子才是 process，由 kernel 经 fragment 组成，B2 的 DFG 画的就是
它们）。三类场景的区分完全落在前两层：bfcl = call 短而多，sharegpt = call 长而少，
lats = call 洪流 + 波并行：</p>
{compo_tbl}
<p class="cap"><b>表注：</b>三类程序的组成实测（负载规格冻结 JSON 与 trace 三方对账，A00 门）。</p>
{pf(11)}
<h3>B1b 负载场景的生命周期 —— 用四层定义串起来</h3>
<p class="theme">把定义放回场景（下面三张图是各类一个中位规模的真实实例，opt 臂 trace）：
bfcl program 的生命周期是"call（等待→服务）→ 工具延迟 → 下一 call"的串行链，寿命由等待与
工具延迟主导；sharegpt program 是少数长 call 的接力，寿命由服务段主导；lats program 是每波
5 个并行 call 的推进，波内要等最慢一路（关键路径）——它的 call 都小，program 却最长。</p>
{life_html}
{pf(5)}
<p class="theme"><b>方法回顾（一段话）：</b>Agentix 用全局进程表记每程序累计服务
{{T<sub>p</sub>, W<sub>p</sub>}}，call 到达时按 p(c<sub>j</sub>) 离散化准入 Q0–Q3、
time quantum 用尽降级、β 抗饿；本采集中该状态机的账本：{adm_note}。
架构与状态机原图：</p>
{pf(8)}{pf(10)}

<h2>B2 负载分析链（W1–W6）：代表 process、DFG 与 trace 探针</h2>
<p class="theme">B1 回答了"负载与方法是什么"；这里回答"对负载做了什么分析、后面的 trace 从哪来"。
方法链：W1 试运行 → W2 热点定位（决定 19 个 host 探针的位置）→ W3 插桩 → W4 代表采集 →
W5 代表集选择 → <b>W6 代表 process 的 DFG</b>。本报告全部时间线的 process 宇宙就是这条链
选出的代表集 + 机制事件；探针开销实测 −0.9 %。</p>
{pf(3)}
{dfg_html_B}
<p class="cap"><b>一句话看图：</b>顺箭头走完一步引擎循环，红虚线是最大的空闲来源（async
输出等待）。<b>图注：</b>节点 = 引擎 stage（运行时阶段，batch8 术语下不称 process）；数字为该臂实测。这张 stage-DFG 是 host 侧分析的骨架，算子 process 层的骨架是 B3b 的 taxonomy。</p>
{tbl_w_B}
{tbl_scope_B}
<p class="cap"><b>表注：</b>core 臂的 host 侧结构：最大单项是 async 输出等待（GPU 已出结果、
host 未消费），其次是 prepare_inputs 内约 80 % 的纯 Python 张量构建。</p>

<h2>B3 call 内部的高延迟：容器层（step/stage）与 process 层分开报告</h2>
<p class="theme">术语纪律（batch8 契约）：<b>process = 由 kernel（经 fragment）组成的算子
单元</b>；step/iter 与 layer 是其上的容器，schedule/update 等是引擎 stage——容器与 stage
不称 process。因此高延迟分两层报告：<b>容器/stage 层</b>（下表与下图：step 实例与引擎
stage 实例的五堆聚类，w05 契约）先定位"时间落在哪个容器"，<b>process 层</b>（B3b：p.*
算子堆）再回答"容器内是哪些算子"。core 臂容器/stage 层全局排名前八：</p>
{tbl_piles_B}
<p class="cap"><b>表注：</b>#1 是重 forward 堆（大批/含 chunked prefill 的 step，
{step_sums['core']:.0f} s，全部高延迟标记）——它不属于任何单个 call，是"批"这一层的容器实例（非 process——其算子构成见 B3b）。</p>
{figB3}
<p class="cap"><b>一句话看图：</b>一条线 = 一个重 forward step 的真实起止，梯形 = 堆包络——
这些就是 call 内部时间最重的<b>容器</b>（step 实例）——它们内部的算子构成见 B3b。<b>图注：</b>窗口为 core 第 1 名 forward（step 容器）堆最密的
分段（审计文件记录）。</p>
<h3>B3b iter 之下：layer 与 fragment（kernel 序列周期折叠）</h3>
<p class="theme">B 的 process 层级到此对齐 batch8 契约的全部深度：request → call → iter(step)
→ scope → <b>layer → 算子 process → fragment（kernel 实例）</b> → kernel 内 NCU 计数器。layer/process/fragment
不靠模块打点（cudagraph 下模块 NVTX 为已验证阴性），而是从 kernel 序列的层周期性重建——一个算子 process（如注意力核）可拥多个 fragment（flash_fwd + combine 两个 kernel），fragment 是 process 内的 kernel 级切片而非 process 本身。术语消歧：此 fragment 是 batch8 契约的 trace 归因单元（process 的碎片区间，严格拥有其发射的 kernel），与 CUDA <code>wmma::fragment</code>（tensor core 下 warp 内每线程的寄存器矩阵片，位于 kernel 内部、只能被 NCU 计数器聚合覆盖）无关，两词撞名纯属巧合。{layer_note}</p>
{tbl_layer}
<p class="cap"><b>表注：</b>gemm 四兄弟（qkv/o/gate_up/down）合计约占层墙钟的大头，注意力核
（2 个 fragment）次之；层间 p10/p90 接近说明 32 层高度均匀——layer 层没有离群热点，
优化空间在层间发射间隙与图外 host 段，而不在某一层内部。</p>
<p class="theme"><b>两个可优化的高延迟来源（数字）：</b>① async 输出等待：GPU 已出 token、
host 未消费的跨步空档，core 臂 {async_core_s:.0f} s / 均 8 ms 级——超过 forward 本身；
② quantum 续段的再 prefill：被切 call 的后续 quantum 段要重算已生成上下文（core 臂
{sig_c[2]} 个续段，首段中位 {sig_c[0]:,.0f} ms 对续段 {sig_c[1]:,.0f} ms）——机制自身的
执行代价。</p>

<h2>B4 call 内部的并发与资源 —— step/kernel 粒度，GPU 内指标</h2>
{figB4}
<p class="cap"><b>一句话看图：</b>到达窗内在飞贴 cap、busy/gemm 稳定——排队 regime 的全程
背景。<b>图注：</b>core 臂全程三 lane（GPU busy / gemm 占比 / 在飞）。</p>
{tbl_phase}
{figB_P1}
{"" if not figB_P1 else '<p class="cap"><b>一句话看图：</b>P1 里批内请求数贴 16、token 数≈请求数（纯 decode）、无降级——干净的满批基线。<b>图注：</b>构造相位 P1（16 个单 quantum 调用同批），上半 step 实例条码，下半六条指标 lane（含新增的批内请求/token 两条）。</p>'}
{figB_P3}
{"" if not figB_P3 else '<p class="cap"><b>一句话看图：</b>P3 里准入分层（Q0 与 Q2/Q3 同窗出现）、降级密集、批内 token 数被 prefill 抬高——机制的全部动作集中在这一窗。<b>图注：</b>构造相位 P3（aged 长调用与 8 个新短程序同时到达）；lane 口径同 P1。</p>'}

<h3>B4b perf_trace 收尾件：排名 process 时间线与并发窗</h3>
{figB_rt}
<p class="cap"><b>一句话看图：</b>全局排名前列 process 的顶堆成员在全程的真实落点——高延迟
process 的时间分布一眼可见（对应参考件 build_ranked_single_batch_timelines）。<b>图注：</b>
每行一个入选 process，矩形 = 顶堆成员实例的起止。</p>
{tbl_concwin}
<p class="cap"><b>表注：</b>并发窗分析（对应参考件 analyze_concurrency_windows，信号 = 每步
批组成标记 w.step）：step 按批内请求数分档的时间结构——构造负载的并发形态由此表与 4.1/
深潜图共同钉定。</p>
{deep_figs['core']}
<p class="cap"><b>一句话看图：</b>红密度高的时段（重 forward 堆成员连片）与在飞贴 cap、
step 率高原同段——高延迟 process 的时间段即并发最重的时间段。<b>图注：</b>上半为窗内全部 step <b>容器</b>的占用条码（红 = 第 1 名重 step 堆成员；容器时间线，非 process 时间线——process 级时间线见 B4b 排名图），下半指标 lane 与其共轴。</p>
{figB4m}
<p class="cap"><b>一句话看图：</b>黄色 gemm 簇背靠背、簇间空白是 step 间 host 空档——kernel
粒度的 process 视图。<b>图注：</b>深潜窗内最忙 300 ms 逐 kernel 展开（黄 = gemm 家族，
蓝 = 其它）；窗内 busy {mbusy:.0f} %、gemm 占 {mgemm:.0f} %。</p>
<p class="theme"><b>GPU 内指标（NCU 逐 kernel 重放，serving GEMM 代表样本）：</b></p>
{tbl_ncu}
<p class="cap"><b>表注：</b>四个代表 GEMM 的墙一致：L2 命中 ~96 %、L2 吞吐 ~76 % 峰、
tensor pipe ~49 %、DRAM 仅 14–20 % 峰（~137–194 GB/s，4090 峰 ~1008）——批内 GEMM 顶在
L2/tensor 而非 DRAM；warp 占用仅 ~16 %（大 tile 少 warp 的 GEMM 形态）。边界：重放样本
4 kernel（launch 过滤后），家族中位与 w03' 一致；逐 step 的 batch 组成无逐事件记录，
step→kernel 归因用 launch-ownership。</p>

<h2>B5 优化机会清单（数据排序，指向 S1 机制卡片计划）</h2>
<table><tr><th>#</th><th>机会</th><th>证据量级（core 臂）</th><th>方向</th></tr>
<tr><td>1</td><td>async 输出等待（host 消费滞后）</td><td>{async_core_s:.0f} s，超过 forward 总和</td><td>host 侧流水化/合并消费；与调度无关</td></tr>
<tr><td>2</td><td>prepare_inputs 纯 Python 张量构建</td><td>~{prep_core_s:.0f} s，其中 CUDA API 仅 ~19 %</td><td>预构建/向量化/图化</td></tr>
<tr><td>3</td><td>quantum 再 prefill（抢占的计算价）</td><td>续段中位 {sig_c[1]:,.0f} ms 对首段 {sig_c[0]:,.0f} ms</td><td>KV 保留式抢占（S1 kvres/驻留机制卡）</td></tr>
<tr><td>4</td><td>排空尾 makespan 项</td><td>core 465 s 对 opt 412 s（r0.8）</td><td>动态并发/尾部调度（S4 E4/E5）</td></tr>
<tr><td>5</td><td>L2/tensor 墙内的批形态</td><td>L2 76 % 峰、tensor 49 %、DRAM 14–20 %</td><td>批大小/图档位定价（S4 E1）</td></tr></table>
<p class="theme">1–2 与调度无关、对四臂同在（消融文档 A 的不变性佐证）；3–5 与抢占/并发机制
直接耦合，对应 PREEMPTION_EXPLORATION_PLAN v3 的 S1 机制卡与 S4 实验菜单。</p>

<h2>记账</h2>
<p class="theme">口径与窗口在 R10_AUDIT.json；A00 守恒门：程序/调用/join 三门全过，G-S 记 8 个空批迭代（0.53 %——构造相位间与工具延迟窗内引擎空转，本负载的预期形态）；
process 宇宙与堆聚类沿 w05/batch8 契约；NCU 重放不进入观测时延计算（契约条款）。
原始 trace：release h22-h23-traces。</p>
</div></body></html>"""

    a.out_ablation.write_text(docA)
    a.out_process.write_text(docB)
    (a.out_ablation.parent / "R10_AUDIT.json").write_text(json.dumps(audit, indent=2))
    print("wrote", a.out_ablation, a.out_ablation.stat().st_size // 1024, "KB;",
          a.out_process, a.out_process.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main()

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
ARM_COLOR = {"plain": "#6b7280", "opt": "#1f2f45", "mlfq": "#a8541f", "core": "#2f6f9f"}

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


def e2e_program_blocks(C, CH, arm_meta, rh=12, bh=8):
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
    SHORT = {"plain": "素", "opt": "opt", "mlfq": "M", "core": "C"}
    out, y = [], 8
    windows = {}
    for pid in pids:
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
            wsum[key] = sum(c["first_token_rel_ms"] - c["submitted_rel_ms"] for c in cs)
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
             f'W6 · 引擎步代表 process 的 DFG（节点数字 = {arm_label} 实测：调用次数 / 时间和）</text>']
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
    TRI = {}
    for k, *_ in ARMS:
        per = defaultdict(lambda: {"wait": [], "res": [], "dres": []})
        for ck, r in idx[k].items():
            per[r["class"]]["wait"].append(r["first_token_rel_ms"] - r["submitted_rel_ms"])
            per[r["class"]]["res"].append(_res(r))
            if ck in idx["opt"]:
                per[r["class"]]["dres"].append(_res(r) - _res(idx["opt"][ck]))
        TRI[k] = {c: {m: sum(v[m]) / max(len(v[m]), 1) for m in v} for c, v in per.items()}
    def tri_row(key, label):
        t = TRI[key]
        cells = "".join(
            f"<td>{t[c]['wait']:.0f} / {t[c]['res']:.0f} / {t[c]['dres']:+.0f}</td>"
            for c in ("bfcl", "sharegpt", "lats"))
        return f"<tr><td>{label}</td>{cells}</tr>"
    tbl_tri = ('<table><tr><th>臂（每调用均值 ms：等待 / 驻留 / 配对驻留差 vs opt）</th>'
               '<th>bfcl</th><th>sharegpt</th><th>lats</th></tr>'
               + "".join(tri_row(k, lab) for k, lab, *_ in ARMS) + "</table>")
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
    blocks, yb, pwin = e2e_program_blocks(C, CH, ARMS)
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
                     f'fill="#48607d">step 实例</text>')
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
             '<th>async 输出等待（和 / 均）</th><th>W5 代表集覆盖 host</th></tr>'
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
                f'{kb[0]}#{kb[1]}，bfcl）</th><th>等待 ms</th><th>驻留 ms</th>'
                '<th>quantum 段数</th><th>端到端 ms</th></tr>'
                + "".join(walk_row(k, lab) for k, lab, *_ in ARMS) + "</table>")

    e_sr, e_cp, e_pi = (pairs[k]["endpoint"]["speedup"] for k in
                        ("state_reuse", "call_preempt", "program_identity"))
    _compo_raw = compo_section(Path("experiments/h23-agentix-8b/workloads/thr_mixed_r0.5.json"))
    _mt = re.search(r"<table>.*?</table>", _compo_raw, re.S)
    compo_tbl = _mt.group(0) if _mt else ""
    life_html = class_lifecycle_figs(C["opt"])
    for _old, _new in (
        ("<b>bfcl 的生命周期：</b>", "<b>一句话看图：</b>红多彩少、段间有空隙——寿命被等待与工具延迟主导。<b>bfcl 的生命周期：</b>"),
        ("<b>sharegpt 的生命周期：</b>", "<b>一句话看图：</b>彩段远长于红段——寿命被长 decode 服务主导。<b>sharegpt 的生命周期：</b>"),
        ("<b>lats 的生命周期：</b>", "<b>一句话看图：</b>五行并行波逐波推进——每波等最慢一路，寿命=关键路径。<b>lats 的生命周期：</b>"),
    ):
        life_html = life_html.replace(_old, _new)
    sig_m = chunk_sig.get("mlfq", (0, 0, 0))
    tri_def = f"""
<div class="block howto"><b>三个时间量的定义与这张表的读法</b>
<p><b>等待</b>：提交→首 token（排队+首段 prefill）——调度直接重分配的量。<b>驻留</b>：首 token→
完成——服务 + 机制附加（quantum 间再排队、续段再 prefill）混在其中，二者在单臂内不可再分
（chunk 标记打在客户端续发时刻，续段的引擎内排队被包在段内）。<b>配对驻留差</b>：同一调用
（同 program、同 index，两侧逐个对齐）的驻留减去 opt 臂驻留——把"机制附加"从驻留里干净
剥出来的办法：素行的 +差 = 关缓存后的重复 prefill；M/C 行的 +差 = 抢占的再排队+再 prefill。</p>
<p><b>读法：竖读一列</b> = 同类负载在四臂间的时间重分配（bfcl 列等待
{TRI['plain']['bfcl']['wait']:.0f}→{TRI['opt']['bfcl']['wait']:.0f}→
{TRI['mlfq']['bfcl']['wait']:.0f}→{TRI['core']['bfcl']['wait']:.0f} ms——两级抢占把短程序
等待压掉 ~90 %）；<b>横读一行</b> = 该臂把时间花在哪；<b>第三列单独读</b> = 机制的驻留代价
（MLFQ 的 sharegpt 行最大：长 decode 被 quantum 反复切，附加 {TRI['mlfq']['sharegpt']['dres']:+.0f} ms/调用；
core 只切 132 个调用，附加集中在 lats）。<b>合计校验</b>：等待+驻留 ≈ 该类平均调用端到端。</p>
<p><b>执行不变性的三条独立证据：</b>① 同调用两侧 <code>produced_tokens</code> 逐个相等
（2,440/2,440）；② 两侧都未被抢占的同调用，驻留比中位 = MLFQ {inv['mlfq']:.2f}（n={inv_n['mlfq']}）/
core {inv['core']:.2f}（n={inv_n['core']}）；③ step 宇宙（step 堆、kernel 显微）四臂同形。
配对驻留差为 0 的行（opt 自身）与 ≈0 的格（core·bfcl/sharegpt 的未抢占主体）是①②在表内的体现。</p>
<p><b>机制的执行代价（第三列的机理）：</b>被切调用的续段要重 prefill 已生成上下文——MLFQ 续段
quantum 墙钟中位 {sig_m[1]:,.0f} ms 对首段 {sig_m[0]:,.0f} ms（{sig_m[2]:,} 个续段）。这份代价
把 MLFQ 等待坍缩省下的时间吃掉大半，mean 停在 1.03×。</p></div>
{tbl_tri}
<p class="cap"><b>表注：</b>素/opt 无 quantum 机制，第三列 = 缓存差（素）与 0（opt 基准）；
lats 列 core 行等待 {TRI['core']['lats']['wait']:.0f} ms 是刻意抬高（程序身份压后长程序）。</p>"""

    _PAPER = {
        1: ("_page_0_Figure_9.jpeg",
            "看四种 agent 程序如何由 LLM 调用与工具/人类中断连成 DAG——\"program\" 这一层就从这里来。",
            "单线程（Chatbot/ReAct）在调用与中断间循环，多线程（MoA/MCTS）成 DAG。1.1 的三类负载"
            "正是它的实例化：bfcl≈ReAct 工具链、sharegpt≈Chatbot、lats≈MCTS 树搜索。"),
        2: ("_page_1_Figure_0.jpeg",
            "看同一批 4 程序在 2 槽引擎里三种排法的甘特图——等待如何被顺序制造、又被程序信息消掉。",
            "轴的语义（对照原文图注）：横轴一格 = 一次 decode 迭代；纵轴两行 = max batch size 2 的两个"
            "批槽，即每个 decode 步最多打包 2 个 call 各一次 decode 迭代；(a) 表中每个 call 的长度即它"
            "需要的 decode 迭代数。(b) FCFS 里长调用把 D 挡到 t≈4（调用级队头阻塞，共等 18 单位）；(c) MLFQ 抢占了长调用"
            "但 A/B 的后续调用又插队（程序级阻塞，仍 18 单位）；(d) PLAS 压后 A/B 的后续调用，等待降到"
            "12 单位。第二部分的 per-program 块就是这张图的 16 槽实盘版：素/opt 行对应 (b)，M 行对应"
            " (c)，C 行对应 (d)。"),
        4: ("_page_3_Figure_0.jpeg",
            "看稳态 1 小时里引擎中的在飞调用量——等待缩短反而让在飞量升高。",
            "程序完成上一调用越快、下一调用来得越快（闭环 λ=N/W）。这解释了 4.1 全程图里四臂在飞都顶"
            "着 cap：排队 regime 下调度不改变\"忙\"，只改变\"谁在忙\"；也解释了附录里开环复现测不到"
            "论文吞吐比的原因。"),
        5: ("_page_3_Figure_5.jpeg",
            "看压力升高后程序时间的构成——等待占了大头。",
            "各类 agent 负载在中高负载下程序大部分寿命在等待。这是整份报告\"优化等待而非执行\"的动机，"
            "与 A2 时间量表里等待列被机制大规模重分配、配对驻留差揭示机制附加的实测一致。"),
        6: ("_page_4_Figure_0.jpeg",
            "看短调用/短程序的等待÷执行比冲到 10–50 倍——两级队头阻塞的直接证据。",
            "左列按调用（FCFS 蓝线在短 decode 端最高=调用级阻塞），右列按程序（FCFS 与 MLFQ 都在少调用"
            "程序端最高=程序级阻塞），Agentix 绿线两端压平。第三部分的调用堆四联图是同一现象的堆视角：""比值高的调用正是被抬进最高时长堆的短程序调用。"),
        7: ("_page_4_Figure_6.jpeg",
            "看程序内 vs 程序间的前缀命中率——程序内高、程序间低。",
            "同一程序的调用共享累积上下文（KV 可复用），跨程序几乎不共享。这就是消融第一对"
            "（素→opt，1.60×）收益的机会来源。为什么程序感知调度没有把命中变成执行差（图 17 蓝段"
            "等高）：程序内下一 call 的间隔由工具/思考延迟主导（调度不可压缩），命中能否兑现由"
            "KV 容量压力决定；论文把跨 call 的 KV 亲和交给进程表驱动的 sticky 路由（多引擎）与"
            "swap 内核（图 18），不交给 PLAS。单引擎同缓存下三臂兑现命中相近——我们的配对驻留比"
            "中位 1.00 是其实测；而素臂关缓存后执行确实变长，说明缓存差异存在时是可见的。"),
        70: ("_page_4_Figure_7.jpeg",
            "看跨程序命中率的补充面板——跨程序几乎无前缀可共享。",
            "与上图合为论文 Fig.7 的两个面板：状态复用的收益边界在程序边界处截止。"),
        3: ("_page_2_Figure_13.jpeg",
            "看 agent 基础设施的两层——上层程序编排状态，下层 serving 引擎执行调用。",
            "我们的 19 个 host 探针打在下层引擎步循环里（DFG 的节点），程序/调用账本记在上层"
            "（A00 守恒门核对的三方之一）——分析链正是沿这张图的层界布设的。"),
        8: ("_page_5_Figure_0.jpeg",
            "看 Agentix 的系统架构——全局进程表喂给调度器与负载均衡。",
            "本复现是它的单引擎切片：进程表 {T<sub>p</sub>, W<sub>p</sub>} 在客户端重建，"
            "调度决策进入 vLLM 的 priority 通道；多引擎负载均衡（图上半）不在单卡范围（见附录偏差表）。"),
        9: ("_page_6_Figure_0.jpeg",
            "看 best/worst 两种排法的 makespan 差——这份自由度只来自程序内并行（多线程 agent）。",
            "第二部分 lats 块的 5 路波形状由它解释：每波要等最慢线程完成才能推进，"
            "所以 lats 的寿命=关键路径而非调用之和；也因此压后 lats 个别调用（浅红底）不一定拖慢整程序。"),
        10: ("_page_7_Figure_0.jpeg",
            "看一次 LLM 调用在离散化优先级下的生命周期状态机。",
            "准入按 p(c<sub>j</sub>) 定级、quantum 用尽降级、β 触发提升——1.2③ 的机制原文。我们账本里"
            "admission Q0–Q3 = 97/102/237/2004、降级 151 次就是这台状态机在本负载上的运行记录。"),
        11: ("_page_8_Figure_8.jpeg",
            "看三类负载的输入/输出长度与每程序调用数分布——我们的合成负载按此校准。",
            "(a) ShareGPT 长输出、(b) BFCL 短输出多调用、(c) LATS 海量小调用、(d) 每程序调用数分布。"
            "1.1 组成表的每一列（调用/程序、prompt/输出均值）逐项对照此图取值。"),
        12: ("_page_9_Figure_0.jpeg",
            "看四条线随到达率的分离与排序——附录端点表是这张图在 4090 上的重测。",
            "论文主结果：同 token 延迟下 Agentix 吞吐最高，Mixed 负载上对 vLLM 至多 15×。"
            "我们的复现保排序与形态（低载并拢、高载分离），数值比收窄的归因见附录三层口径。"),
        13: ("_page_10_Figure_0.jpeg",
            "看 P95/P99 尾延迟——\"MLFQ 追 mean 不追尾\"在尾部口径最清楚。",
            "我们的对应实测：p99 加速 program_identity 对 1.85×、附录 p90 面板里 MLFQ 与 Agentix "
            "的间距在所有 r 保持——收益向尾部集中的次序与此图相同。"),
        14: ("_page_10_Figure_6.jpeg",
            "看多引擎下不同负载均衡策略的延迟——需要多卡。",
            "属于附录偏差表\"1× 4090 vs 4× A100\"一行的范围：本复现不含多引擎路由，"
            "此图仅作完整性对照。"),
        15: ("_page_11_Figure_0.jpeg",
            "看同 SLO 下最大到达率随引擎副本数线性扩展。",
            "反向解释了单卡的可持续 r 低于论文测试台：论文的高到达率依赖副本扩展，"
            "我们的 r=0.2–0.8 程序/秒是单副本可持续区间。"),
        16: ("_page_11_Figure_2.jpeg",
            "看离线批处理的 makespan 缩短——与我们\"makespan 守恒\"发现的边界对照。",
            "论文此图的缩短来自 swap 内核与 gang 调度（图 17/18 的机制）；本复现被抢占者走 recompute、"
            "未启用 swap 内核，makespan 持平（附录完成吞吐表）——两个结果在各自机制配置下都成立。"),
        17: ("_page_11_Figure_4.jpeg",
            "看每根柱子的分段——蓝色 Execution 三臂等高（调度不碰执行），红色 Wait 差异巨大（调度只重分配等待）。",
            "(a) ShareGPT、(b) LATS，柱段 = Execution/Scheduler/Swap/Wait。1 槽微型例先拆常见误读：会话 A 正生成"
            "400 token，B/C 刚到各要 20 token——FCFS 让 B/C 等完 A 全程；MLFQ 每 32 token 抢占 A，但 A 的"
            "下一轮调用又从 Q0 插到更晚的新会话前；PLAS 记得 A 已得 400 服务、压其入低队列。三种排法三种"
            " wait，与程序内是否多线程无关——单线程只锁死'同程序调用必须串行'（故 ATLAS 无增量），"
            "程序间重排照常发生。两点常被误读：其一，"
            "ShareGPT 是单线程 agent，但三臂延迟依然不同（Wait 0.55/0.36/0.21 s/tok）——调度的"
            "作用面是跨程序的排队竞争，与程序内是否多线程无关；单线程只意味着 ATLAS 的程序内"
            "机制无事可做（退化为 PLAS）。其二，(b) 里 MLFQ 的 Wait 反而高于 vLLM-OPT——追短"
            "调用会让程序整体停滞，与我们 sharegpt 类上 MLFQ 最差（49.4 对 opt 24.3 ms/tok）"
            "同构。蓝段等高即 1.4 执行不变性的论文侧对照。"),
        18: ("_page_11_Figure_10.jpeg",
            "看 swap 内核减少换出次数与时间。",
            "本复现用 recompute 处置被抢占者，此项收益未包含——它是附录偏差表"
            "\"swap→recompute\"一行的论文侧依据。"),
        19: ("_page_16_Picture_9.jpeg",
            "看两程序玩具例里 ATLAS 与 MLFQ 的差异——不让长调用打断短关键路径程序。",
            "MLFQ 下 A 的并行小调用持续打断 B（等 5 步）；ATLAS 把 A 的第三路降级，B 先完成（等 3 步）。"
            "这是 lats 类多线程程序上程序身份的第二重价值（本复现的 core 臂用同一进程表覆盖）。"),
        20: ("_page_16_Figure_11.jpeg",
            "看与最优策略（SRPT）的差距——Agentix 领先基线但仍留缺口。",
            "仿真中 Agentix 优于各基线、距 SRPT 仍有可见空间：这为后续工作（更细粒度的抢占机制与"
            "动态并发控制，本项目 S1–S4 计划）标出了上限方向。"),
    }
    def pf(n, num=None):
        fname, lead, body = _PAPER[n]
        num = num if num else (7 if n == 70 else n)
        return paper_fig(fname, f"<b>一句话看图：</b>{lead} <b>论文图 {num}（原图）：</b>{body}")
    cw = pairs["call_preempt"]["class_wait_ms"]
    ml_a = pairs["program_identity"]["mlfq"]
    METH = f"""
<h2>A1 论文的方法与 baseline 的对比 —— 负载带来的消融机会（多图）</h2>
<div class="block"><b>① 论点</b>
<p>三类负载（组成见 A2）结构不对称，使三种优化各有独立杠杆：bfcl 的密集短调用给"排序"最大杠杆；
sharegpt 的长 decode 调用是"quantum 抢占"的作用面；lats 的调用洪流制造两级队头阻塞——只有认得
"程序身份"的调度才能区分"洪流的第 180 个调用"与"新程序的第 1 个调用"。三个机会互不重叠，
四臂因此可以首尾相接地逐对消融。</p></div>
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
β=2.0 未触发）；证据角色是 lats 等待被刻意抬到 p50 {cw['core']['lats']['p50']:.0f} ms，换
mean {e_pi['mean']:.2f}× / p99 {e_pi['p99']:.2f}×。下方状态机原图即该机制本体，玩具例原图
给出它在多线程（lats）上的第二重价值——注意边界：这重价值只作用于多线程程序，对单线程的 sharegpt/bfcl，ATLAS 退化为 PLAS，调度只在程序之间重排等待（论文图 17a 的蓝段等高、红段悬殊即此意）。</p></div>
{pf(10)}{pf(19)}
<div class="block howto"><b>④ 双向看图与边界</b>
<p>顺论文图 2 走读：(b) FCFS 里 D 被挡到 t≈4，(d) PLAS 压后 A/B 的后续调用让 C/D 提前。
<b>再看我们的图</b>：A3 的 per-program 块把它扩到 16 槽实盘——素/opt 行对应 (b)，M 行对应
(c)，C 行对应 (d)；D 的提前 = 短程序块红段逐臂消失，B 的垫后 = lats 块 C 行的浅红底。边界：
这些差异只在"槽被占满"时存在——A5 的 r=0.2 端点三缓存臂并拢，前提失效则图示差异消失。</p></div>
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
    # call set fixed by the AGENTIX arm's top-latency pile identities; the SAME
    # calls are drawn in every arm over the SAME window — the scheduling
    # behaviour (core packing them late) becomes directly visible.
    core_keys = [(m["pid"], m["idx"]) for m in seg["core"]]
    kset = set(core_keys)
    # window: densest 60 s of the CORE pile (same rel window for all arms)
    win_c = int(60e9)
    best_n, aw0 = -1, 0
    for tt in range(0, int(max(m["end"] for m in seg["core"])) - win_c, int(5e9)):
        n = sum(1 for m in seg["core"] if m["start"] < tt + win_c and m["end"] > tt)
        if n > best_n:
            best_n, aw0 = n, tt
    aw1 = aw0 + win_c
    partsA4 = axis(aw0 / 1e6, aw1 / 1e6, 60, 1800)
    yA4 = 70
    for key, label, *_ in ARMS:
        mem = []
        for pid, ci in kset:
            r = idx[key].get((pid, ci))
            if r is None:
                continue
            mem.append({"pid": pid, "idx": ci, "cls": r["class"],
                        "start": int(r["submitted_rel_ms"] * 1e6),
                        "end": int(r["finished_rel_ms"] * 1e6),
                        "d": int((r["finished_rel_ms"] - r["submitted_rel_ms"]) * 1e6)})
        inw = [m for m in mem if m["start"] < aw1 and m["end"] > aw0]
        s, yA4 = hl_prog_strip(inw, yA4, f'{SHORTN[key]}（core 顶堆 call 集，窗内 {len(inw)}/{len(mem)}）',
                               aw0, aw1)
        yA4 += 8
        partsA4 += s
    audit["windows"]["A4"] = {"criterion": "call set = core top-pile identities; "
                              "window = densest 60 s of the core pile, same for all arms",
                              "window_s": [aw0 / 1e9, aw1 / 1e9], "set_size": len(kset)}
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
                 '<th>async 输出等待（和 / 均）</th><th>W5 代表集覆盖 host</th></tr>')
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
    tbl_layer, layer_note = "", ""
    _pt_file = D.get("bcap", Path("/nonexistent")) / "PT_PROCESS_ANALYSIS.json" if BK == "bcap" else Path("/nonexistent")
    if _pt_file.exists():
        PT = json.loads(_pt_file.read_text())
        _ord = ["norm_in", "qkv_proj", "attn_core", "o_proj", "norm_post",
                "mlp_gate_up", "act_mul", "mlp_down"]
        fr = PT["fragments"]
        tbl_layer = ('<table><tr><th>算子 process（模块打点实测）</th><th>fragment 中位数/实例</th>'
                     '<th>host 中位 µs</th><th>device 中位 µs</th><th>界</th></tr>' + "".join(
            f"<tr><td>{k}</td><td>{fr[k]['med_fragments']:.0f}</td>"
            f"<td>{fr[k]['med_host_us']}</td><td>{fr[k]['med_device_us']}</td>"
            f"<td>{'device' if fr[k]['med_device_us'] > fr[k]['med_host_us'] else 'launch/host'}</td></tr>"
            for k in _ord if k in fr) + '</table>')
        gr = PT["global_rank_top"]
        tbl_layer += ('<table><tr><th>全局排名（10 % 契约入选）</th><th>顶堆成员</th>'
                      '<th>顶堆时间和 s</th></tr>' + "".join(
            f"<tr><td>#{i+1} {r['process']}</td><td>{r['members']:,}</td>"
            f"<td>{r['sum_ns']/1e9:.2f}</td></tr>" for i, r in enumerate(gr[:5])) + '</table>')
        php = PT["phases"]
        _pp = ["qkv_proj", "attn_core", "mlp_down"]
        tbl_layer += ('<table><tr><th>相位 × process（n / 中位 µs）</th>'
                      + "".join(f"<th>{k}</th>" for k in _pp) + '</tr>' + "".join(
            f"<tr><td>{ph}</td>" + "".join(
                (lambda d_: f"<td>{d_['n']:,} / {d_['med_us']}</td>" if d_ else "<td>—</td>")(
                    php.get(ph, {}).get(k)) for k in _pp) + "</tr>"
            for ph in ("P1", "P2", "P3")) + '</table>')
        layer_note = ("<b>正式实现（Stage W→T 工作流产物）：</b>process 由模块结构确定"
                      "（PROCESS_TAXONOMY，四门验证通过），trace 为模块打点 eager 仪器臂"
                      "（perf_trace 双臂契约：时序结论以 graph 性能臂为准，本臂供结构与归因；"
                      "仪器臂 wall 47.1 s 对性能臂 37.5 s，开销 +26 % 已披露）。"
                      "fragment 表是 process→fragment→kernel 的实测：qkv/o/mlp 为 device 界"
                      "（GEMM 真算力），attn_core 与两个 norm 为 launch/host 界——"
                      "launch-bound 结论第一次落到算子粒度，这正是 B5 机会清单 1–2 项的微观形态。")
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
引擎阶段是 <b>scope</b>（schedule / prepare / forward / sample 等，姊妹文档 B2 的 DFG 画的就是
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
<p class="theme"><b>代表性 process 的构成：</b>本部分逐块画出全部 25 个 program——它是三种
代表集的并集：含负载特点的（1.1b 的三类中位实例）、高延迟的（等待最重的短程序，
如 1.3 走查的 {kb[0]}）、以及 W5 从 host 侧选出的代表 process 所服务的调用。方法描述与
消融设计见 A1，本部分只看运行时差异。</p>
{pf(9)}
<div class="block howto"><b>怎么读下面的截图</b>
<p>缩写：素 = vLLM 关缓存/关分块；opt = vLLM 全优化 FCFS；MLFQ = 调用级多级反馈队列；
core = 程序级（Agentix）。红段 = 等待；<span style="background:{REQUEUE}">浅红底</span> =
chunk 段未覆盖的间隙（再排队的可见部分，仅 MLFQ/core 两臂存在；续段内部的排队与再 prefill
不可再分，其总量由 A2 表的"配对驻留差"列量化）；类别色段 = quantum 段（客户端续发窗口）
（<span style="color:#eb6834">橙 bfcl</span> / <span style="color:#2a78d6">蓝 sharegpt</span> /
<span style="color:#1baf7a">绿 lats</span>）。<b>排版：每个 program 一块</b>——块头标出
程序号·类别·调用数与该块自己的时间窗；块内四行紧凑相邻，自上而下 素 / opt / M（MLFQ）/
C（core），同一到达序列下同一程序在四种策略里的直接对比。<b>每块的窗口独立选择</b>
（该程序自己最繁忙的时段），块与块之间比例尺不同、无公共时间轴——比较只在块内上下四行之间
进行，不跨块比长短。</p></div>
<p class="theme"><b>运行时效果（图证）：</b>全程短程序等待合计
素 {wait_sums['plain']:.0f} s → opt {wait_sums['opt']:.0f} s → MLFQ {wait_sums['mlfq']:.0f} s →
core {wait_sums['core']:.0f} s。逐块看三次相邻行对比：素→opt 红段整体缩短（状态复用，
{e_sr['mean']:.2f}×）；opt→M 红段几乎清零、但 sharegpt/lats 块浮出浅红底（等待变成了再排队，
mean 只有 {e_cp['mean']:.2f}×、p90 {e_cp['p90']:.2f}× 的原因在图内可见）；M→C 浅红底从
bfcl/sharegpt 块移到 lats 块（长程序买单，{e_pi['mean']:.2f}×/p99 {e_pi['p99']:.2f}×）。
四行色段密度同形；被 quantum 切分的调用色段略胀（续段再 prefill，机制的计算价），
未被碰过的调用色段逐毫秒相同。</p>
{fig1}
<p class="cap"><b>一句话看图：</b>每块四行上下对看——红段（等待）逐臂缩短，浅红底（再排队）在 M/C 行出现并从短程序块转移到 lats 块；行尾标两个数：该程序的全程等待总和与程序 token 延迟，四行中<b>等待总和最短者加粗</b>——等待是 Agentix 方法的优化对象与动机。<b>图注：</b>行尾"等 x s" = 该程序全部调用（提交→首token）之和；"y ms/tok" = 程序响应时间 ÷ 产出 token 数，均不随窗口裁剪。加粗按等待判据后请注意读法：<b>Σ等待最短多在 M 行</b>（无程序区分的即时抢占让谁都最快拿首 token），C 行紧随其后且在短程序块接近最短——Agentix 的动机是"短程序不为长程序买单"，不是"所有程序等待皆最短"。第二个数保留以并置完成判据：bfcl 块的 ms/tok 赢家多为 C（6/8），sharegpt 块全部为 opt（5/5，MLFQ 的续段再 prefill 惩罚长 decode），lats 块 opt/C 平分（7/5）。等待可与程序内并行重叠、也可被再 prefill 抵消，所以"面向 agent 负载优化全局服务"的判据是程序完成而非等待之和。<b>加粗不总在 C 行不是标记错误</b>——Agentix 优化的是全体程序的统计（mean/p90/p99），不是每个程序：调度是重分配，必有程序付账（sharegpt 为 quantum 切割买单、lats 为压后买单，与 A2 表第三列自洽）；逐块加粗的分布因此是"谁受益、谁买单"的地图——这正是交换单位从 call 到 program 的意义在逐程序粒度的显形。每块窗口 = 该程序生命周期 ≤40 s 取全程（±2 % 边距），
&gt;40 s 取四臂调用活动最密的 30 s；窗口起止标在块头。<br><b>轴注：</b>块头方括号内为
从各自运行起点起算的墙钟秒；块内四行共用该窗口与比例尺；行内每条横条 = 一个 call。</p>


<h2>A4 高延迟 call 的调度行为对照 —— 同一批 call、同一时间窗、四种摆放</h2>
{pf(6)}
<p class="theme"><b>主要观察什么：</b>最高延迟区间（该臂时长最高的 call 簇）按 program 分行
后，看每行的归属与增减：粗行（bfcl/sharegpt——程序短，应尽早离开此区间）与细淡行（lats 的
call——单个短而密，但程序身份长，应当让步）。素/opt 侧大量粗行出现在高延迟区间（短程序的
call 被排队抬进来）；MLFQ 清空粗行但 lats 行反而变密（quantum 间再排队）；core 侧只剩 lats
行——"该等的才在等"。</p>
<p class="theme"><b>每臂构成：</b>{"。".join(pile_comp)}。</p>
{figA4}
<p class="cap"><b>一句话看图：</b>同一批 call（core 顶堆身份）在四条带里的位置与长短——core 带右聚（压后）、opt/素带铺满（占槽）、M 带条纹变长（quantum 切碎）。<b>图注：</b>call 集 = core 臂对数时长聚类最高簇的成员身份（w05 契约）；窗口 = 该簇最密的 60 s，四臂同一相对窗；行标 = 程序号·类别·集内 call 数。</p>

{a.fourarm.read_text().replace("<h2>四、论文四臂复现 —— vLLM / vLLM-opt / MLFQ / Agentix 全基线对照</h2>", "<h2>A5 端点全景 —— 论文口径的四臂复现</h2>")}

<h3>附·论文评测原图对照（多引擎/扩展性/开销项，本复现范围之外的部分以偏差表衔接）</h3>
{pf(12)}{pf(13)}{pf(14)}{pf(15)}{pf(16)}{pf(18)}{pf(20)}


<h2>记账</h2>
<p class="theme">窗口与选材标准在 R10_AUDIT.json；A00 守恒门四臂 <code>all_pass</code>；
配对事实 pair_facts_*.json 与本文数字同源。原始 trace：release h22-h23-traces；
本页与端点数据：release h23-r10-reports。</p>
</div></body></html>"""

    if BK == "bcap":
        ver_note = ("<b>数据：受控并发 batch 采集 ctrl_conc16</b>（batch8/16 方法迁移：构造 "
                    "W/P1/P2/P3/P4 并发相位，见 workflow06/B_BATCH_TRACE_PLAN.md；分析窗口是"
                    "构造的、不是搜索的）。")
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
引擎阶段是 <b>scope</b>（schedule / prepare / forward / sample 等，B2 的 DFG 画的就是
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
输出等待）。<b>图注：</b>节点数字为 core 臂实测（W5 代表集）；这张 DFG 是 B4/B5 一切
call 内部分析的骨架。</p>
{tbl_w_B}
{tbl_scope_B}
<p class="cap"><b>表注：</b>core 臂的 host 侧结构：最大单项是 async 输出等待（GPU 已出结果、
host 未消费），其次是 prepare_inputs 内约 80 % 的纯 Python 张量构建。</p>

<h2>B3 call 内部的高延迟 process —— step/scope 宇宙</h2>
<p class="theme">一个 call 的服务由几十到上千个 step 拼成；高延迟分析从 call 下潜到 step：
把全部 scope 实例按类型聚 10 % 阈值、对数时长五堆并全局排名（w05 契约），最高堆就是
call 内部的高延迟 process。core 臂全局排名前八：</p>
{tbl_piles_B}
<p class="cap"><b>表注：</b>#1 是重 forward 堆（大批/含 chunked prefill 的 step，
{step_sums['core']:.0f} s，全部高延迟标记）——它不属于任何单个 call，是"批"这一层的
process。</p>
{figB3}
<p class="cap"><b>一句话看图：</b>一条线 = 一个重 forward step 的真实起止，梯形 = 堆包络——
这些就是 call 内部的高延迟 process 本体。<b>图注：</b>窗口为 core 第 1 名 forward 堆最密的
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
{deep_figs['core']}
<p class="cap"><b>一句话看图：</b>红密度高的时段（重 forward 堆成员连片）与在飞贴 cap、
step 率高原同段——高延迟 process 的时间段即并发最重的时间段。<b>图注：</b>上半为窗内全部
step 实例的条码时间线（红 = 第 1 名重 forward 堆成员），下半四条指标 lane 与其共轴。</p>
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

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
        out.append(f'<text x="4" y="{y+15}" font-size="17" font-weight="600" fill="#1f2f45">'
                   f'{pid}·{cls}·{ncalls} 调用 · 窗 [{w0/1e3:.1f}, {w1/1e3:.1f}] s（宽 {(w1-w0)/1e3:.1f} s）</text>')
        y += 22
        R2 = 185   # right margin reserved for the per-arm annotations
        X = lambda t: LEFT + (W - LEFT - R2) * (max(min(t, w1), w0) - w0) / (w1 - w0)
        for key, _lab, *_ in arm_meta:
            out.append(f'<text x="{LEFT-6}" y="{y+bh+1}" font-size="15" text-anchor="end" '
                       f'fill="{ARM_COLOR[key]}">{SHORT[key]}</text>')
            best = ptl[key] <= pmin + 1e-9
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
    ap.add_argument("--out", type=Path, required=True)
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
    pairs = {k: json.loads((AT / f"pair_facts_{k}.json").read_text())
             for k in ("state_reuse", "call_preempt", "program_identity")}
    audit = {"purpose": "R10 four-arm edition window/selection criteria", "windows": {}}

    # ---------------- trichotomy table + cross-checks ----------------------
    TRI = {k: tri_stats(C[k], CH[k]) for k, *_ in ARMS}
    def tri_row(key, label):
        t = TRI[key]
        cells = "".join(
            f"<td>{t[c]['wait']:.0f} / {t[c]['engine']:.0f} / {t[c]['requeue']:.0f}</td>"
            for c in ("bfcl", "sharegpt", "lats"))
        return f"<tr><td>{label}</td>{cells}</tr>"
    tbl_tri = ('<table><tr><th>臂（每调用均值 ms：等待 / 引擎内 / quantum 间再排队）</th>'
               '<th>bfcl</th><th>sharegpt</th><th>lats</th></tr>'
               + "".join(tri_row(k, lab) for k, lab, *_ in ARMS) + "</table>")
    # execution invariance: matched calls UNPREEMPTED on both sides —
    # residence ratio should be 1 (per-token step time is policy-blind)
    idx = {k: {(r["program_id"], r["call_index"]): r for r in C[k]} for k, *_ in ARMS}
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
    # step-pile support (opt vs core, both have NCU views; others quoted in text)
    p1 = P["opt"]["hl"]["piles"][0]
    si = max(range(len(p1["rows"])), key=lambda i: len(p1["rows"][i]))
    sec = P["opt"]["hl"]["sections"][si]
    sb, se = int(sec["begin_ns"]), int(sec["end_ns"])
    parts2b = axis((sb - int(P["opt"]["hl"]["origin"])) / 1e6,
                   (se - int(P["opt"]["hl"]["origin"])) / 1e6, 60, 700)
    h1, yh = hl_strip(P["opt"]["hl"], 70, "vLLM-opt（FCFS）", sb, se)
    # same REL window on the core side
    ob_c = int(P["core"]["hl"]["origin"])
    ob_f = int(P["opt"]["hl"]["origin"])
    h2, yh2 = hl_strip(P["core"]["hl"], yh, "agentix_core", sb - ob_f + ob_c, se - ob_f + ob_c)
    fig2b = fig(parts2b + h1 + h2, yh2 + 6)
    step_sums = {k: P[k]["hl"]["piles"][0]["sum_ns"] / 1e9 for k, *_ in ARMS}
    audit["windows"]["part2b"] = {"criterion": "densest section of opt rank-1 forward pile",
                                  "section": si + 1}

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
    def deep_dive(key, label):
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
        hl_pids = {m["pid"] for m in sg if m["start"] / 1e6 < w1 and m["end"] / 1e6 > w0}
        parts = axis(w0, w1, 60, 0)          # height patched at the end
        parts.append(f'<text x="4" y="26" font-size="20" font-weight="600" fill="{ARM_COLOR[key]}">'
                     f'{label} · 高延迟段 [{h0/1e3:.0f},{(h0+win)/1e3:.0f}] s · '
                     f'超cap并发段 [{q0/1e3:.0f},{(q0+win)/1e3:.0f}] s · 图窗 [{w0/1e3:.0f},{w1/1e3:.0f}] s</text>')
        y = 74
        Xd = lambda ms: LEFT + (W - LEFT - RIGHT) * (max(min(ms, w1), w0) - w0) / (w1 - w0)
        # process timelines (zoomed e2e style), high-latency programs flagged
        lanes_p = {}
        for c in C[key]:
            if c["finished_rel_ms"] < w0 or c["submitted_rel_ms"] > w1:
                continue
            lanes_p.setdefault(c["program_id"], {"cls": c["class"], "cs": []})["cs"].append(c)
        order = sorted(lanes_p.items(), key=lambda kv: (
            {"bfcl": 0, "sharegpt": 1, "lats": 2}[kv[1]["cls"]],
            min(x["submitted_rel_ms"] for x in kv[1]["cs"])))
        rh, bh = 11, 7
        for pid, ln in order:
            hlf = pid in hl_pids
            parts.append(f'<text x="{LEFT-6}" y="{y+bh+1}" font-size="14" text-anchor="end" '
                         f'fill="{WAIT if hlf else "#8fa2b6"}"'
                         f'{" font-weight=\"700\"" if hlf else ""}>{pid}·{ln["cls"]}</text>')
            for c in ln["cs"]:
                ft, fin = c["first_token_rel_ms"], c["finished_rel_ms"]
                x0, x1, x2 = Xd(c["submitted_rel_ms"]), Xd(ft), Xd(fin)
                if x1 > x0:
                    parts.append(f'<rect x="{x0:.1f}" y="{y+1}" width="{max(x1-x0,0.5):.1f}" '
                                 f'height="{bh}" fill="{WAIT}" opacity=".85"/>')
                segs = CH[key].get((pid, c["call_index"]))
                if segs:
                    parts.append(f'<rect x="{x1:.1f}" y="{y+1}" width="{max(x2-x1,0.5):.1f}" '
                                 f'height="{bh}" fill="{REQUEUE}" opacity=".9"/>')
                    for b, e, _q in segs:
                        b, e = max(b, ft), min(e, fin)
                        if e <= b:
                            continue
                        parts.append(f'<rect x="{Xd(b):.1f}" y="{y+1}" width="{max(Xd(e)-Xd(b),0.5):.1f}" '
                                     f'height="{bh}" fill="{CLS_COLOR[ln["cls"]]}"/>')
                else:
                    parts.append(f'<rect x="{x1:.1f}" y="{y+1}" width="{max(x2-x1,0.5):.1f}" '
                                 f'height="{bh}" fill="{CLS_COLOR[ln["cls"]]}" opacity=".9"/>')
            y += rh
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

    # ================= assembly ============================================
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
<div class="block howto"><b>三个时间量的定义（本报告所有时间线图共用，必须区分）</b>
<p><b>等待</b>（红段）：提交→首 token，排队 + 首段 prefill——调度直接作用的量。
<b>引擎内 quantum 段</b>（类别色段）：调用被引擎接纳、正在被 step 服务的时段。quantum（原文 time quantum）= 队列发给调用的一次性服务配额，用尽即被抢占并降级——它是服务量的上限，不是队列容量（trace 的
chunk_begin/end 逐段实测，与首token→完成的驻留取交）。<b>quantum 间再排队</b>（浅红底）：quantum 用尽
被抢占后、等待下一个 quantum的时段——它发生在首 token 之后，旧版把它并进彩段，才造成
"调度优化却改变了 busy"的错觉。</p>
<p><b>执行不变性的验证（三条互相独立）：</b>① 同调用两侧 <code>produced_tokens</code> 逐个相等
（2,440/2,440）；② 两侧都未被抢占的同调用，驻留比中位 = MLFQ {inv['mlfq']:.2f}（n={inv_n['mlfq']}）/
core {inv['core']:.2f}（n={inv_n['core']}）——没被机制碰过的调用，服务逐毫秒相同；③ step 宇宙
（第二章 step 堆、第三章 kernel 显微）四臂同形。</p>
<p><b>机制的真实执行代价也在这里现形（不是测量误差）：</b>被 quantum 切分的调用，其后续quantum 段要
重新 prefill 已生成的上下文——MLFQ 的续段 quantum 墙钟中位 {sig_m[1]:,.0f} ms 对首段
{sig_m[0]:,.0f} ms（{sig_m[2]:,} 个续段）。这份再 prefill 是调用级抢占为"随时可抢"支付的
计算价，正是它把等待坍缩省下的时间吃掉、让 MLFQ 的 mean 停在 1.03×。</p></div>
{tbl_tri}
<p class="cap"><b>表注：</b>素/opt 无 quantum 机制，引擎内 ≈ 驻留（再排队恒 0）；MLFQ 把等待压到
bfcl {TRI['mlfq']['bfcl']['wait']:.0f} ms，代价是再排队（sharegpt
{TRI['mlfq']['sharegpt']['requeue']:.0f} ms/调用）+ 续段再 prefill（并入引擎内列，使其略胀）；
core 只对 132 个调用触发 quantum 切分，再排队集中在被压后的长程序。等待列被机制大规模重分配、
引擎内列只随再 prefill 小幅变化——数据合理性由上面三条不变性钉住。</p>"""

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
            "与 1.4 三时间量表里等待列被机制大规模重分配、引擎内列几乎不动的实测一致。"),
        6: ("_page_4_Figure_0.jpeg",
            "看短调用/短程序的等待÷执行比冲到 10–50 倍——两级队头阻塞的直接证据。",
            "左列按调用（FCFS 蓝线在短 decode 端最高=调用级阻塞），右列按程序（FCFS 与 MLFQ 都在少调用"
            "程序端最高=程序级阻塞），Agentix 绿线两端压平。第三部分的调用堆四联图是同一现象的堆视角：""比值高的调用正是被抬进最高时长堆的短程序调用。"),
        7: ("_page_4_Figure_6.jpeg",
            "看程序内 vs 程序间的前缀命中率——程序内高、程序间低。",
            "同一程序的调用共享累积上下文（KV 可复用），跨程序几乎不共享。这就是消融第一对"
            "（素→opt，1.60×）收益的机会来源，也解释了为什么该收益与调度无关、必须先剥离。"),
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
            "(a) ShareGPT、(b) LATS，柱段 = Execution/Scheduler/Swap/Wait。两点常被误读：其一，"
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
<h3>1.2 论文的方法与 baseline 的对比 —— 负载带来的消融机会（多图）</h3>
<div class="block"><b>① 论点</b>
<p>1.1 的三类负载结构不对称，使三种优化各有独立杠杆：bfcl 的密集短调用给"排序"最大杠杆；
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
<b>再看我们的图</b>：第二部分 per-program 块把它扩到 16 槽实盘——素/opt 行对应 (b)，M 行对应
(c)，C 行对应 (d)；D 的提前 = 短程序块红段逐臂消失，B 的垫后 = lats 块 C 行的浅红底。边界：
这些差异只在"槽被占满"时存在——附录 r=0.2 端点三缓存臂并拢，前提失效则图示差异消失。</p></div>
"""
    doc = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>Agentix 四臂复现 · 负载分析与性能 trace</title><style>
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
<h1>Agentix 论文四臂复现 —— 理解负载与优化性能的四部分时间线报告</h1>
<p class="sub">目的：帮助人类和 AI 理解这份 agent serving 负载与其上的性能优化。四部分递进：
<b>第一部分</b> 理解负载（负载特点 + 分析链 W1–W6 + 负载带来的方法消融机会与四方法对比）；
<b>第二部分</b> 代表性 process 的端到端时间线（执行分布 + 消融的运行时差异）；
<b>第三部分</b> 高延迟 process 放大（潜在优化点）；<b>第四部分</b> 并发与资源使用率时间线。
数据：LLaMA-3.1-8B · thr_mixed r0.5 · cap16 · 四臂各一次完整 serving 采集（vLLM素 /
vLLM-opt / MLFQ调用级 / agentix_core，同负载同栈，逐对只差一个变量），A00 守恒门全过；
端点全景（4 臂 × 5 到达率）在附录。窗口与选材标准在 R10_SUMMARY_AUDIT.json；
本版取代旧版（存 git 历史）。</p>

<h2>第一部分 负载理解 —— 负载场景、层次定义与生命周期</h2>
<h3>1.1 几个 agent 负载场景，与由此引出的四层定义</h3>
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
引擎阶段是 <b>scope</b>（schedule / prepare / forward / sample 等，1.3 的 DFG 画的就是
它们）。三类场景的区分完全落在前两层：bfcl = call 短而多，sharegpt = call 长而少，
lats = call 洪流 + 波并行：</p>
{compo_tbl}
<p class="cap"><b>表注：</b>三类程序的组成实测（负载规格冻结 JSON 与 trace 三方对账，A00 门）。</p>
{pf(11)}
<h3>1.1b 负载场景的生命周期 —— 用四层定义串起来</h3>
<p class="theme">把定义放回场景（下面三张图是各类一个中位规模的真实实例，opt 臂 trace）：
bfcl program 的生命周期是"call（等待→服务）→ 工具延迟 → 下一 call"的串行链，寿命由等待与
工具延迟主导；sharegpt program 是少数长 call 的接力，寿命由服务段主导；lats program 是每波
5 个并行 call 的推进，波内要等最慢一路（关键路径）——它的 call 都小，program 却最长。</p>
{life_html}
{pf(5)}

{METH}

<h3>1.3 负载分析链（W1–W6）：代表 process、DFG 与 trace 探针的来源</h3>
<p class="theme">1.1/1.2 回答了"负载与方法是什么"；这里回答"负载是什么""对负载做了什么分析、后面的 trace 从哪来"。
方法链：W1 试运行 → W2 热点定位（决定 19 个 host 探针的位置）→ W3 插桩 → W4 代表采集 →
W5 代表集选择 → <b>W6 代表 process 的 DFG</b>。本报告全部时间线的 process 宇宙就是这条链
选出的代表集 + 机制事件；探针开销实测 −0.9 %。</p>
{tbl_w}
<p class="cap"><b>表注：</b>四臂的 host 侧结构相同：最大单项都是 async 输出等待（GPU 已出
结果、host 未消费的空档），其次是 prepare_inputs 内 ~80 % 的纯 Python 张量构建。两者与调度
策略无关（四臂同量级），是执行侧优化的主目标，但不影响本报告的排序收益结论。</p>
{dfg_html}
<p class="cap"><b>一句话看图：</b>顺箭头走完一步引擎循环，红虚线是最大的空闲来源（async 输出等待）。<b>图注：</b>节点 = 引擎步内的代表 process（W5 选出），边 = 步内顺序依赖；
红虚线边 = 跨步的 async 输出等待（数据依赖：sample 的 token 要回到下一步的 schedule，
但 host 消费滞后）。数字为 opt 臂实测；四臂对照：async 等待
<table><tr><th>臂</th><th>async 输出等待</th><th>#1 forward 堆</th></tr>{async_tbl}</table></p>
{pf(3)}{pf(8)}

<h3>1.4 度量定义：三个时间量 —— 等待 / 引擎内 / quantum 间再排队</h3>
{tri_def}
{pf(17)}

<h2>第二部分 代表性 process 的端到端时间线 —— 执行分布与消融的运行时差异</h2>
<p class="theme"><b>代表性 process 的构成：</b>本部分逐块画出全部 25 个 program——它是三种
代表集的并集：含负载特点的（1.1b 的三类中位实例）、高延迟的（等待最重的短程序，
如 1.3 走查的 {kb[0]}）、以及 W5 从 host 侧选出的代表 process 所服务的调用。方法描述与
消融设计见 1.2，本部分只看运行时差异。</p>
{pf(9)}
<div class="block howto"><b>怎么读下面的截图</b>
<p>缩写：素 = vLLM 关缓存/关分块；opt = vLLM 全优化 FCFS；MLFQ = 调用级多级反馈队列；
core = 程序级（Agentix）。红段 = 等待；<span style="background:{REQUEUE}">浅红底</span> =
quantum 间再排队（仅 MLFQ/core 两臂存在）；类别色段 = 引擎内 quantum 段
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
<p class="cap"><b>一句话看图：</b>每块四行上下对看——红段（等待）逐臂缩短，浅红底（再排队）在 M/C 行出现并从短程序块转移到 lats 块；行尾标两个数：该程序的全程等待总和与程序 token 延迟，四行中 ms/tok 最短者（全局服务判据）加粗。<b>图注：</b>行尾"等 x s" = 该程序全部调用（提交→首token）之和；"y ms/tok" = 程序响应时间 ÷ 产出 token 数，均不随窗口裁剪。两个判据故意并列以暴露一个关键事实：<b>Σ等待几乎总是 M 行最短</b>（quantum 抢占让谁都最快拿到首 token），<b>但加粗多不在 M 行</b>——bfcl 块的 ms/tok 赢家多为 C（6/8），sharegpt 块全部为 opt（5/5，MLFQ 的续段再 prefill 惩罚长 decode），lats 块 opt/C 平分（7/5）。等待可与程序内并行重叠、也可被再 prefill 抵消，所以"面向 agent 负载优化全局服务"的判据是程序完成而非等待之和——这正是交换单位从 call 到 program 的意义在逐程序粒度的显形。每块窗口 = 该程序生命周期 ≤40 s 取全程（±2 % 边距），
&gt;40 s 取四臂调用活动最密的 30 s；窗口起止标在块头。<br><b>轴注：</b>块头方括号内为
从各自运行起点起算的墙钟秒；块内四行共用该窗口与比例尺；行内每条横条 = 一个 call。</p>

<h2>第三部分 高延迟 process 的时间线放大 —— 潜在优化点</h2>
<div class="block howto"><b>怎么读下面的截图</b>
<p>缩写：堆/pile = 时长相近的调用簇（对数时长 Lloyd 聚类取最高簇）；粗深线 = bfcl/sharegpt
调用，细淡线 = lats 调用；梯形 = 堆成员包络。一条线一个调用（起点提交、终点完成）。</p></div>
<p class="theme"><b>主要观察什么：</b>看粗深线（bfcl/sharegpt——程序短，应尽早结束离开
最高堆）与绿色细线（lats 的调用——单个 call 短而密，但程序身份长，应当让步）此消彼长。注意
方向：绿色恰恰是"该让步"的一方——它们单调用虽短，所属程序却最长；让粗线尽早退出高延迟堆、
绿色留在堆里垫后，就是程序级调度生效的形态。<b>各臂读数：</b>{"；".join(pile_notes)}。素臂的
最高堆被排队抬进大量短程序调用；opt 减员但短程序仍在；MLFQ 把短程序清出（等待归零）但堆总
时长没降多少（quantum 间再排队顶替了等待）；core 的最高堆只剩 lats 本身的长调用——高延迟
视角下"该等的才在等"。</p>
<p class="theme"><b>每个堆里有什么 process：</b>{"。".join(pile_comp)}。</p>
{fig2}
<p class="cap"><b>一句话看图：</b>数每条带里的粗深线——最高时长堆中的短程序调用逐臂被清出。<b>图注：</b>窗口为素臂最高调用堆最密的 60 s，四臂同窗。</p>
<h3>支撑：重 forward step 堆两侧同形（服务侧不变的 step 级证据）</h3>
{fig2b}
<p class="cap"><b>一句话看图：</b>上下两带同形（线密度、线长、梯形宽）——step 服务侧没被策略改变。<b>图注：</b>opt 与 core 的全局第 1 名 forward 堆在同一相对窗内逐成员对画：
线密度（步频）、线长（步长）、梯形宽度均一致；四臂第 1 名堆总时长
{" / ".join(f"{lab.split('（')[0]} {step_sums[k]:.0f} s" for k, lab, *_ in ARMS)}——
step 宇宙不随策略变形，与预备节执行不变性的三条验证互为印证。</p>

<h2>第四部分 并发分析 —— 高延迟时段与端到端的并发及资源使用率</h2>
{pf(4)}
<div class="block howto"><b>怎么读下面的截图</b>
<p>缩写：gemm = 批内线性层 kernel 家族；在飞 = 已提交未完成 call 数；cap=16 = 引擎批容量；
step 率 = 每秒引擎迭代数（host 侧节奏指标）。4.1 每个指标一张图、四臂同图叠加（臂色与图例
同第一部分）；4.2 每个方法一张图：上半是图窗内每个 program 的时间线（同端到端画法放大，
红色程序名 = 该臂最高时长调用堆的成员，即高延迟 process），下半是四条指标-时间分布
（GPU busy / gemm 占比 / 在飞 / step 率），与 process 时间线共用同一时间轴。
NCU 资源墙（gemm 家族中位 L2 76 % / SM·tensor 49 % / DRAM 17 %，opt 与 core 臂实测）
是静态参考值，四臂同栈同 kernel 家族。</p></div>
<p class="theme"><b>运行时效果（图证）：</b>4.1 三张叠加图里四条线几乎重叠——busy 与 gemm
的轨迹四臂同形、在飞在到达窗内一起顶着 cap 红线；差别集中在右端排空段的长短（素最长；core
的 lats 排空尾略长于 opt，与附录 makespan 守恒表相符）。4.2 的共轴图把机理落到时间段上：
高延迟 process 的红段/浅红底与在飞贴 cap、step 率高原正好同段——排队不是资源不足
（busy/gemm 并未更高），而是出队顺序把等待集中到了这些 process 上。</p>
<h3>4.1 端到端过程的并发趋势 —— 每指标一图、四臂同图对比</h3>
{fig4_busy}
<p class="cap"><b>一句话看图：</b>四条线轨迹几乎重叠——没有哪个方法靠"更忙"取胜，本部分主题
（收益不来自资源使用率）由此成立。<b>图注：</b>GPU busy 全程分布，0 – {wall_ms/1e3:.0f} s，
四臂叠加，臂色同图例。</p>
{fig4_gemm}
<p class="cap"><b>一句话看图：</b>gemm 占比的四条线同样重叠——step 内部的计算构成不随调度
策略改变。<b>图注：</b>gemm 家族时间占比全程分布，口径同上。</p>
{fig4_inf}
<p class="cap"><b>一句话看图：</b>到达窗内四条线一起压着 cap=16 红线（并发同样打满），右端
排空尾的长短是四臂唯一的形态差别。<b>图注：</b>在飞调用数全程分布；红虚线 = cap=16。</p>
<h3>4.2 每方法深潜 —— 高延迟段与并发段内，process 时间线与指标时间线共轴</h3>
<p class="theme">每图的窗口这样选：先取该臂最高时长调用堆成员活动最密的 10 s（高延迟段），
再取在飞超 cap 时间最长的 10 s（并发段），图窗覆盖两者（若相距过远则取高延迟段）；两段的
起止都标在图题并记入审计文件。</p>
{deep_figs['plain']}
<p class="cap"><b>一句话看图：</b>素臂图窗里红段占满 process 行、在飞持续贴 cap——重复
prefill 把队列堵成常态。<b>图注：</b>红名 = 高延迟堆成员程序（{len(deep_hl['plain'])} 个）；
四条指标 lane 与上方 process 行共用时间轴。</p>
{deep_figs['opt']}
<p class="cap"><b>一句话看图：</b>opt 的红段比素臂短但仍集中在短程序行——调用级队头阻塞
在时间段上的直接显形。<b>图注：</b>红名高延迟程序 {len(deep_hl['opt'])} 个；lane 口径同上。</p>
{deep_figs['mlfq']}
<p class="cap"><b>一句话看图：</b>MLFQ 行里红段消失、浅红底铺开——等待被换成 quantum 间
再排队，而下方 busy/gemm 并未升高。<b>图注：</b>红名高延迟程序 {len(deep_hl['mlfq'])} 个；
lane 口径同上。</p>
{deep_figs['core']}
<p class="cap"><b>一句话看图：</b>core 把浅红底集中到 lats 行、短程序行干净——程序身份把
"谁在等"重新分配，指标 lane 与其它臂同形。<b>图注：</b>红名高延迟程序
{len(deep_hl['core'])} 个；lane 口径同上。</p>

{a.fourarm.read_text().replace("<h2>四、论文四臂复现 —— vLLM / vLLM-opt / MLFQ / Agentix 全基线对照</h2>",
                               "<h2>附：端点全景 —— 论文口径的四臂复现（vLLM / vLLM-opt / MLFQ / Agentix）</h2>")}

<h3>附·论文评测原图对照（多引擎/扩展性/开销项，本复现范围之外的部分以偏差表衔接）</h3>
{pf(12)}{pf(13)}{pf(14)}{pf(15)}{pf(16)}{pf(18)}{pf(20)}

<h2>记账</h2>
<p class="theme">窗口与选材标准全部在 R10_SUMMARY_AUDIT.json；A00 守恒门（程序/调用/引擎步/
join）四臂 <code>all_pass</code>（各捕获 <code>a00_process_view.json</code>）；trace 开销四臂同担；配对事实
pair_facts_*.json 与本报告数字同源。原始 trace：release h22-h23-traces；
本页与端点数据：release h23-r10-reports。</p>
</div></body></html>"""
    a.out.write_text(doc)
    (a.out.parent / "R10_SUMMARY_AUDIT.json").write_text(json.dumps(audit, indent=2))
    print("wrote", a.out, a.out.stat().st_size // 1024, "KB; busy-invariance",
          json.dumps(inv), "; tri core.lats", TRI["core"]["lats"])


if __name__ == "__main__":
    main()

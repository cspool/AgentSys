#!/usr/bin/env python3
"""R10 final report, four-arm edition — REPLACES the 3-model pair edition.

Universe: LLaMA-3.1-8B, thr_mixed r0.5, cap16, four traced arms
(vLLM素 / vLLM-opt FCFS / MLFQ调用级 / agentix_core). Style, outline and figure
geometry follow the frozen skill (workflow06/skill) and reuse the pair-edition
template constants; every figure and number here is rebuilt from the NEW
captures. The pair edition remains in git history.

Core fix this edition carries: the end-to-end lanes now draw THREE quantities
separately — 等待 (submit→首token, red), busy (量子段真实执行, class color),
驻留中的再排队 (quantum-requeue gaps inside the residence, pale red) — so the
"scheduling must not change execution" invariant is checkable in the figure
itself instead of being contradicted by a conflated 彩段.
"""
from __future__ import annotations

import argparse
import json
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
    """Mean 等待 / 引擎内量子段 / 量子间再排队 per class (ms per call)."""
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
        out.append(f'<text x="4" y="{y+15}" font-size="17" font-weight="600" fill="#1f2f45">'
                   f'{pid}·{cls}·{ncalls} 调用 · 窗 [{w0/1e3:.1f}, {w1/1e3:.1f}] s（宽 {(w1-w0)/1e3:.1f} s）</text>')
        y += 22
        X = lambda t: LEFT + (W - LEFT - RIGHT) * (max(min(t, w1), w0) - w0) / (w1 - w0)
        for key, _lab, *_ in arm_meta:
            out.append(f'<text x="{LEFT-6}" y="{y+bh+1}" font-size="15" text-anchor="end" '
                       f'fill="{ARM_COLOR[key]}">{SHORT[key]}</text>')
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
    tbl_tri = ('<table><tr><th>臂（每调用均值 ms：等待 / 引擎内 / 量子间再排队）</th>'
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
    for key, label, *_ in ARMS:
        sg = seg[key]
        inw = [m for m in sg if m["start"] < cw1 and m["end"] > cw0]
        s, y = call_pile_strip(inw, y, f"{label}（窗内 {len(inw)}/{len(sg)} 成员）", cw0, cw1)
        y += 8
        parts2 += s
        short_n = sum(v for k2, v in Counter(m["cls"] for m in sg).items() if k2 != "lats")
        pile_notes.append(f"{label}：{len(sg)} 个调用 / {sum(m['d'] for m in sg)/1e9:.0f} s，短程序成员 {short_n}")
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
    # display the central 5 s so each ~100 ms lane bar is individually readable
    d0 = c0 + (c1 - c0) / 2 - 2500.0
    d1 = d0 + 5000.0
    parts3 = axis(d0, d1, 60, 4 * (3 * 162 + 40) + 40)
    y = 70
    for key, label, *_ in ARMS:
        # cu lane rows are RELATIVE to the capture start (= hl origin);
        # convert the run-relative window via each arm's own offsets
        run0 = int(P[key]["e2e"]["origin"]) - int(P[key]["hl"]["origin"])
        s, y = cu_strip(P[key]["cu"], y, label, run0 + int(d0 * 1e6), run0 + int(d1 * 1e6))
        parts3 += s
        y += 10
    fig3 = fig(parts3, y + 6)
    audit["windows"]["part3"] = {"criterion": "30 s window with max opt time-above-cap16",
                                 "window_s": [c0 / 1e3, c1 / 1e3]}
    micro_parts, ym = [], 60
    micro_stats = {}
    for key, label, *_ in ARMS:
        oe = int(P[key]["e2e"]["origin"])
        at = kernel_micro_best(D[key] / "cap.sqlite", oe + int(c0 * 1e6), oe + int(c1 * 1e6), int(300e6))
        s, ym, busy, gsum = kernel_micro_strip(D[key] / "cap.sqlite", ym, label, at, int(300e6))
        ym += 14
        micro_parts += s
        micro_stats[key] = {"busy_pct": busy, "gemm_pct": gsum}
    fig3b = fig(micro_parts, ym + 6)
    audit["windows"]["part3_micro"] = {"criterion": "busiest 300 ms (max kernel busy) inside part3 window, per arm",
                                       "stats": micro_stats}

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

    # ================= assembly ============================================
    e_sr, e_cp, e_pi = (pairs[k]["endpoint"]["speedup"] for k in
                        ("state_reuse", "call_preempt", "program_identity"))
    compo = compo_section(Path("experiments/h23-agentix-8b/workloads/thr_mixed_r0.5.json"))
    compo = compo.replace("{CHAR_ART}", char_art(C["opt"], C["core"], P["opt"]["hl"])
                          + '<h2 style="font-size:22px">三类负载的真实生命周期（各取一个中位规模的程序实例）</h2>'
                          + class_lifecycle_figs(C["opt"]))
    sig_m = chunk_sig.get("mlfq", (0, 0, 0))
    tri_def = f"""
<div class="block howto"><b>三个时间量的定义（本报告所有时间线图共用，必须区分）</b>
<p><b>等待</b>（红段）：提交→首 token，排队 + 首段 prefill——调度直接作用的量。
<b>引擎内量子段</b>(类别色段)：调用被引擎接纳、正在被 step 服务的时段（trace 的
chunk_begin/end 逐段实测，与首token→完成的驻留取交）。<b>量子间再排队</b>（浅红底）：量子用尽
被抢占后、等待下一个量子的时段——它发生在首 token 之后，旧版把它并进彩段，才造成
"调度优化却改变了 busy"的错觉。</p>
<p><b>执行不变性的验证（三条互相独立）：</b>① 同调用两侧 <code>produced_tokens</code> 逐个相等
（2,440/2,440）；② 两侧都未被抢占的同调用，驻留比中位 = MLFQ {inv['mlfq']:.2f}（n={inv_n['mlfq']}）/
core {inv['core']:.2f}（n={inv_n['core']}）——没被机制碰过的调用，服务逐毫秒相同；③ step 宇宙
（第二章 step 堆、第三章 kernel 显微）四臂同形。</p>
<p><b>机制的真实执行代价也在这里现形（不是测量误差）：</b>被切量子的调用，其后续量子段要
重新 prefill 已生成的上下文——MLFQ 的续段量子墙钟中位 {sig_m[1]:,.0f} ms 对首段
{sig_m[0]:,.0f} ms（{sig_m[2]:,} 个续段）。这份再 prefill 是调用级抢占为"随时可抢"支付的
计算价，正是它把等待坍缩省下的时间吃掉、让 MLFQ 的 mean 停在 1.03×。</p></div>
{tbl_tri}
<p class="cap"><b>表注：</b>素/opt 无量子机制，引擎内 ≈ 驻留（再排队恒 0）；MLFQ 把等待压到
bfcl {TRI['mlfq']['bfcl']['wait']:.0f} ms，代价是再排队（sharegpt
{TRI['mlfq']['sharegpt']['requeue']:.0f} ms/调用）+ 续段再 prefill（并入引擎内列，使其略胀）；
core 只切 132 个调用，再排队集中在被压后的长程序。等待列被机制大规模重分配、
引擎内列只随再 prefill 小幅变化——数据合理性由上面三条不变性钉住。</p>"""

    PF1 = paper_fig("_page_1_Figure_0.jpeg",
        "论文 Fig.2（原图）。横轴 = 时间（decode 步）；纵轴 = 引擎 2 个批槽；色块 = 程序的一次调用。"
        "(b) FCFS：单调用短程序 D 等到 t≈4；(d) PLAS 按程序累计服务重排，C、D 提前。四臂图把这条"
        "对比从 2 槽玩具扩到 16 槽真实引擎：素/opt 两臂是 (b) 的两种工程实现，MLFQ/core 是 (d) 的"
        "两种交换单位（call vs program）。")
    PF2 = paper_fig("_page_7_Figure_0.jpeg",
        "论文原图：程序视角的等待/执行比。FCFS 与调用级 MLFQ 都在『调用数多的程序』端比值最高"
        "（程序级队头阻塞），Agentix 把两端都压低。我们的调用堆四联图是它的堆视角展开。")
    PF3 = paper_fig("_page_10_Figure_0.jpeg",
        "论文 Fig.12（原图）。到达率–延迟曲线四条线的间距即本报告第四章端点表；本章的并发/资源"
        "时间线检验它的前提——四臂在同一资源墙下运行，间距只能来自排序。")

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
<h1>Agentix 论文四臂复现 —— 负载分析、代表 process/DFG 与性能 trace 的时间线解释</h1>
<p class="sub">数据：LLaMA-3.1-8B · thr_mixed r0.5 · cap16 · 四臂各一次完整 serving 采集
（vLLM素 / vLLM-opt / MLFQ调用级 / agentix_core，同负载同栈，逐对只差一个变量），
A00 守恒门全过。窗口与选材标准在 R10_SUMMARY_AUDIT.json；本版取代旧三模型两臂版
（旧版存 git 历史）。方法链：负载分析（W1–W5 代表 process 选择 + W6 DFG）→ 以代表
process 为探针的性能 trace（19 个 host 探针 + 机制事件）→ 本报告的时间线可视化。</p>

{compo}

<h3>预备·负载分析链（W1–W6）：代表 process、DFG 与 trace 探针的来源</h3>
<p class="theme">上面回答了"负载是什么"；这里回答"对负载做了什么分析、后面的 trace 从哪来"。
方法链：W1 试运行 → W2 热点定位（决定 19 个 host 探针的位置）→ W3 插桩 → W4 代表采集 →
W5 代表集选择 → <b>W6 代表 process 的 DFG</b>。本报告全部时间线的 process 宇宙就是这条链
选出的代表集 + 机制事件；探针开销实测 −0.9 %。</p>
{tbl_w}
<p class="cap"><b>表注：</b>四臂的 host 侧结构相同：最大单项都是 async 输出等待（GPU 已出
结果、host 未消费的空档），其次是 prepare_inputs 内 ~80 % 的纯 Python 张量构建。两者与调度
策略无关（四臂同量级），是执行侧优化的主目标，但不影响本报告的排序收益结论。</p>
{dfg_html}
<p class="cap"><b>图注：</b>节点 = 引擎步内的代表 process（W5 选出），边 = 步内顺序依赖；
红虚线边 = 跨步的 async 输出等待（数据依赖：sample 的 token 要回到下一步的 schedule，
但 host 消费滞后）。数字为 opt 臂实测；四臂对照：async 等待
<table><tr><th>臂</th><th>async 输出等待</th><th>#1 forward 堆</th></tr>{async_tbl}</table></p>

<h3>预备·三个时间量：等待 / 引擎内 / 量子间再排队</h3>
{tri_def}

<h2>一、端到端 Process 时间线 —— 同一程序四臂紧凑对排，三个时间量分开画</h2>
<div class="block"><b>论文方法与四臂对应</b>
<p><b>一句话论点：</b>四臂是同一负载下的四种出队规则，收益应全部表现为红段（等待）与浅红底
（再排队）的重分配，色段（busy）四臂同形。</p>
<p><b>Baseline 与缺陷：</b>素臂重复每个前缀的 prefill（等待里含重复计算）；opt 臂消除重复但 FCFS
让 lats 洪流的后续调用排在短程序前面（调用级队头阻塞）；MLFQ 臂按量子抢占消除长占，但准入
不看程序历史，长程序的下一个调用又从 Q0 开始（程序级队头阻塞仍在）。</p>
<p><b>创新点对应：</b>core 用进程表把准入定位到 p(c<sub>j</sub>) = Σ<sub>k&lt;j</sub> t<sub>k</sub>
对应的队列——动机是程序级阻塞，机制是离散化准入 + 量子降级，证据是下图 lats 车道的浅红底
（被压后的再排队）与短程序车道红段消失同时发生。</p></div>
{PF1}
<div class="block howto"><b>怎么读下面的截图</b>
<p>缩写：素 = vLLM 关缓存/关分块；opt = vLLM 全优化 FCFS；MLFQ = 调用级多级反馈队列；
core = 程序级（Agentix）。红段 = 等待；<span style="background:{REQUEUE}">浅红底</span> =
量子间再排队（仅 MLFQ/core 两臂存在）；类别色段 = 引擎内量子段
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
四行色段密度同形；被切量子的调用色段略胀（续段再 prefill，机制的计算价），
未被碰过的调用色段逐毫秒相同。</p>
{fig1}
<p class="cap"><b>图注：</b>每块窗口 = 该程序生命周期 ≤40 s 取全程（±2 % 边距），
&gt;40 s 取四臂调用活动最密的 30 s；窗口起止标在块头。<br><b>轴注：</b>块头方括号内为
从各自运行起点起算的墙钟秒；块内四行共用该窗口与比例尺；行内每条横条 = 一个 call。</p>

<h2>二、高延迟 Process 时间线 —— 最高时长调用堆的四臂迁移</h2>
{PF2}
<div class="block howto"><b>怎么读下面的截图</b>
<p>缩写：堆/pile = 时长相近的调用簇（对数时长 Lloyd 聚类取最高簇）；粗深线 = bfcl/sharegpt
调用，细淡线 = lats 调用；梯形 = 堆成员包络。一条线一个调用（起点提交、终点完成）。</p></div>
<p class="theme"><b>运行时效果（图证）：</b>{"；".join(pile_notes)}。素臂的最高堆被排队抬进了
大量短程序调用；opt 减员但短程序仍在；MLFQ 把短程序清出（等待归零）但堆的总时长没降多少
（再排队顶替了等待）；core 的最高堆只剩 lats 本身的长调用——高延迟视角下"该等的才在等"。</p>
{fig2}
<p class="cap"><b>图注：</b>窗口为素臂最高调用堆最密的 60 s，四臂同窗。</p>
<h3>支撑：重 forward step 堆两侧同形（服务侧不变的 step 级证据）</h3>
{fig2b}
<p class="cap"><b>图注：</b>opt 与 core 的全局第 1 名 forward 堆在同一相对窗内逐成员对画：
线密度（步频）、线长（步长）、梯形宽度均一致；四臂第 1 名堆总时长
{" / ".join(f"{lab.split('（')[0]} {step_sums[k]:.0f} s" for k, lab, *_ in ARMS)}——
step 宇宙不随策略变形，与预备节执行不变性的三条验证互为印证。</p>

<h2>三、并发分析时间线 —— 四臂顶着同一面资源墙</h2>
{PF3}
<div class="block howto"><b>怎么读下面的截图</b>
<p>缩写：gemm = 批内线性层 kernel 家族；在飞 = 已提交未完成 call 数；cap=16 = 引擎批容量；
L2/SM(tensor)/DRAM = NCU 对 gemm 家族重放的中位利用率（在 opt/core 两臂实测，素/MLFQ 同栈
同 kernel 家族）。趋势图三条 lane：GPU busy %、gemm 占比 %、在飞数；显微图为窗内最忙 300 ms
的逐 kernel 展开。</p></div>
<p class="theme"><b>运行时效果（图证）：</b>四臂 busy/gemm 两条 lane 同形、在飞 lane 都贴着
cap=16 红线——资源使用率与并发两个自由度都被排除；显微图四臂 gemm 突发同样致密
（busy {" / ".join(f"{v['busy_pct']:.0f}%" for v in micro_stats.values())}），
突发间都是 step 间 host 空隙。剩下的唯一解释是出队顺序——这就是第四章端点差距的机理。</p>
{fig3}
<p class="cap"><b>图注：</b>取 opt 臂在飞超 cap 时间最长的 30 s 窗，展示其中部 5 s 的细节（每根竖条 ≈ 100 ms 的一个采样窗口，可逐根对比，不是趋势线）；四臂同相对窗同比例尺。</p>
{fig3b}
<p class="cap"><b>图注：</b>每臂取窗内最忙 300 ms；黄行 = gemm 家族、蓝行 = 其它 kernel，
右侧竖条 = NCU 资源墙（opt/core 实测值）。</p>

{a.fourarm.read_text()}

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

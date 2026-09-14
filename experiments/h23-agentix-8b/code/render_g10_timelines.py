#!/usr/bin/env python3
"""G10 deliverable: three data-driven timeline views + synthesis, rendered to HTML/SVG.

Views (AutoTrace G10: two-view report generalised to the serving chain's three
timeline axes; every mark is drawn from the capture, nothing is hand-placed):

  V1  end-to-end timeline    — GPU busy % (0.5 s bins) with the concurrent-request
                               count on the same clock; phase-colored busy area.
  V2  high-latency timeline  — every request as a horizontal span (queue_wait +
                               decode), rows grouped by class, instances beyond
                               median + 3*MAD (per class, decode) highlighted.
  V3  concurrency timeline   — in-flight request count band, colored by the w01'
                               concurrency buckets that partition GPU time.

Inputs: capture sqlite (kernels), analysis/request_segments.csv (w02', aligned
clock), analysis/concurrency_windows.csv (w01'). Output: one self-contained HTML.
"""

from __future__ import annotations

import argparse
import bisect
import csv
import json
import sqlite3
import statistics
from collections import defaultdict
from pathlib import Path

BUCKET_COLORS = {"1": "var(--s3)", "2-3": "var(--s6)", "4-7": "var(--s4)",
                 "8-15": "var(--s2)", "16-31": "var(--s1)", "32+": "var(--s7)", "0": "var(--mut)"}


def load_kernels(sq: Path):
    db = sqlite3.connect(str(sq))
    ks = [(s, e) for s, e in db.execute("select start, end from CUPTI_ACTIVITY_KIND_KERNEL")]
    ks += [(s, e) for s, e in db.execute("select start, end from CUPTI_ACTIVITY_KIND_MEMCPY")]
    db.close()
    ks.sort()
    return ks


def union_busy(iv):
    tot = 0
    cur_s = cur_e = None
    for s, e in iv:
        if cur_e is None or s > cur_e:
            if cur_e is not None:
                tot += cur_e - cur_s
            cur_s, cur_e = s, e
        else:
            cur_e = max(cur_e, e)
    if cur_e is not None:
        tot += cur_e - cur_s
    return tot


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--capture-dir", type=Path, required=True)
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args()
    d = a.capture_dir
    ks = load_kernels(next(d.glob("*.sqlite")))
    seg = list(csv.DictReader((d / "analysis" / "request_segments.csv").open()))
    conc_rows = list(csv.DictReader((d / "analysis" / "concurrency_windows.csv").open()))
    w01 = json.loads((d / "analysis" / "w01_serving_conservation.json").read_text())

    t0 = min(int(float(r["submit_ns"])) for r in seg)
    t1 = max(int(float(r["finish_ns"])) for r in seg)
    span = t1 - t0

    # ---- V1 series: busy % per 0.5 s + concurrency
    BIN = 500_000_000
    nbins = span // BIN + 1
    subs = sorted(int(float(r["submit_ns"])) for r in seg)
    fins = sorted(int(float(r["finish_ns"])) for r in seg)
    busy_pct, conc_series = [], []
    for i in range(nbins):
        lo, hi = t0 + i * BIN, min(t0 + (i + 1) * BIN, t1)
        if hi <= lo:
            break
        j0 = bisect.bisect_left(ks, (lo - 10**9,))
        b = union_busy([(max(s, lo), min(e, hi)) for s, e in ks[j0:j0 + 200000] if e > lo and s < hi])
        busy_pct.append(100 * b / (hi - lo))
        mid = (lo + hi) // 2
        conc_series.append(bisect.bisect_right(subs, mid) - bisect.bisect_right(fins, mid))

    # ---- V2: request spans + high-latency flags (per class decode median+3MAD)
    by_class = defaultdict(list)
    for r in seg:
        by_class[r["class"]].append(r)
    hl_thr = {}
    for cls, rows in by_class.items():
        vals = [float(r["decode_ns"]) for r in rows]
        med = statistics.median(vals)
        mad = statistics.median([abs(v - med) for v in vals]) or 1.0
        hl_thr[cls] = med + 3 * mad
    lanes = []
    for cls in sorted(by_class):
        rows = sorted(by_class[cls], key=lambda r: int(float(r["submit_ns"])))
        for r in rows:
            lanes.append({"cls": cls, "sub": int(float(r["submit_ns"])) - t0,
                          "first": int(float(r["first_token_ns"])) - t0,
                          "fin": int(float(r["finish_ns"])) - t0,
                          "hl": float(r["decode_ns"]) > hl_thr[cls],
                          "pid": r["program_id"], "ci": r["call_index"]})
    n_hl = sum(1 for l in lanes if l["hl"])

    # ---- render SVG helpers
    W, PAD = 1000, 46

    def x(ns):
        return PAD + (W - 2 * PAD) * ns / span

    def polyline(vals, y0, h, vmax):
        pts = " ".join(f"{PAD + (W - 2 * PAD) * i / max(len(vals) - 1, 1):.1f},{y0 + h - h * min(v, vmax) / vmax:.1f}"
                       for i, v in enumerate(vals))
        return pts

    dur_s = span / 1e9
    xticks = "".join(
        f'<line x1="{x(sec*1e9):.0f}" y1="0" x2="{x(sec*1e9):.0f}" y2="16" class="tick"/>' +
        f'<text x="{x(sec*1e9):.0f}" y="30" class="tl">{sec:.0f}s</text>'
        for sec in [0, dur_s*0.25, dur_s*0.5, dur_s*0.75, dur_s] )

    # V1 svg
    H1 = 190
    v1 = [f'<svg viewBox="0 0 {W} {H1}" class="tlsvg" role="img" aria-label="end-to-end timeline">']
    for gy in (25, 50, 75, 100):
        yy = 20 + 120 - 120 * gy / 100
        v1.append(f'<line x1="{PAD}" y1="{yy:.0f}" x2="{W-PAD}" y2="{yy:.0f}" class="grid"/>'
                  f'<text x="{PAD-6}" y="{yy+4:.0f}" class="tl" text-anchor="end">{gy}</text>')
    v1.append(f'<polyline points="{polyline(busy_pct,20,120,100)}" class="line-busy"/>')
    peak_c = max(conc_series) or 1
    v1.append(f'<polyline points="{polyline(conc_series,20,120,peak_c)}" class="line-conc"/>')
    v1.append(f'<g transform="translate(0,{H1-38})">{xticks}</g>')
    v1.append(f'<text x="{PAD}" y="14" class="lg"><tspan class="c-busy">— GPU busy %</tspan>'
              f'  <tspan class="c-conc" dx="14">— 在飞请求数（峰值 {peak_c}）</tspan></text></svg>')

    # V2 svg: one row per request
    ROWH = 3
    H2 = 40 + ROWH * len(lanes) + 30
    v2 = [f'<svg viewBox="0 0 {W} {H2}" class="tlsvg" role="img" aria-label="high-latency timeline">']
    ycur = 34
    cls_color = {"sharegpt": "var(--s1)", "bfcl": "var(--s3)", "lats": "var(--s4)",
                 "chat": "var(--s1)", "agent": "var(--s3)"}
    cur_cls = None
    for l in lanes:
        if l["cls"] != cur_cls:
            cur_cls = l["cls"]
            ycur += 12
            v2.append(f'<text x="{PAD}" y="{ycur-2}" class="clab">{cur_cls}（高延迟 '
                      f'{sum(1 for q in lanes if q["cls"]==cur_cls and q["hl"])}/{sum(1 for q in lanes if q["cls"]==cur_cls)}）</text>')
        col = "var(--hl)" if l["hl"] else cls_color.get(l["cls"], "var(--s5)")
        op = "0.95" if l["hl"] else "0.45"
        v2.append(f'<rect x="{x(l["sub"]):.1f}" y="{ycur}" width="{max(x(l["fin"])-x(l["sub"]),0.8):.1f}" height="{ROWH-0.8}" fill="{col}" opacity="{op}"><title>{l["pid"]}#{l["ci"]} {l["cls"]}{" HIGH-LATENCY" if l["hl"] else ""}</title></rect>')
        ycur += ROWH
    v2.append(f'<g transform="translate(0,{H2-30})">{xticks}</g>')
    v2.append(f'<text x="{PAD}" y="14" class="lg">每行 = 一个 LLM 请求（提交→完成）；<tspan class="c-hl">■ 高延迟实例（decode &gt; 类中位 + 3×MAD，共 {n_hl}/{len(lanes)}）</tspan></text></svg>')

    # V3 svg: concurrency band colored by bucket
    def bucket_of(c):
        for lo, hi, n in [(0,0,"0"),(1,1,"1"),(2,3,"2-3"),(4,7,"4-7"),(8,15,"8-15"),(16,31,"16-31"),(32,10**9,"32+")]:
            if lo <= c <= hi:
                return n
    H3 = 170
    v3 = [f'<svg viewBox="0 0 {W} {H3}" class="tlsvg" role="img" aria-label="concurrency timeline">']
    bw = (W - 2 * PAD) / max(len(conc_series), 1)
    for i, c in enumerate(conc_series):
        h = 110 * min(c, peak_c) / peak_c
        v3.append(f'<rect x="{PAD+i*bw:.1f}" y="{130-h:.1f}" width="{bw+0.4:.1f}" height="{h:.1f}" fill="{BUCKET_COLORS[bucket_of(c)]}" opacity="0.9"><title>t={i*0.5:.1f}s 并发={c}</title></rect>')
    v3.append(f'<g transform="translate(0,{H3-32})">{xticks}</g>')
    gpu_share = {r["concurrent_requests"]: r["gpu_share_pct"] for r in conc_rows}
    leg = "  ".join(f'<tspan style="fill:{BUCKET_COLORS[k]}">■ {k} 并发（GPU 时间 {gpu_share.get(k,"0")}%）</tspan>' for k in ["1","2-3","4-7","8-15","16-31"] if k in gpu_share or k in [b for b in map(bucket_of, conc_series)])
    v3.append(f'<text x="{PAD}" y="14" class="lg">{leg}</text></svg>')

    mean_busy_active = statistics.mean([b for b, c in zip(busy_pct, conc_series) if c > 0]) if any(conc_series) else 0
    html = f'''<title>Agentix Serving 时间线 G10</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono&display=swap">
<style>
:root {{ --paper:#fafaf8; --card:#fff; --line:#e3e5e0; --ink:#14181a; --ink2:#5a625f; --mut:#c9cec9;
  --s1:#2a78d6; --s2:#eb6834; --s3:#1baf7a; --s4:#eda100; --s5:#e87ba4; --s6:#008300; --s7:#4a3aa7; --hl:#e34948; --accent:#0f6b63; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --paper:#15181a; --card:#1c2023; --line:#32383b; --ink:#eef0ee; --ink2:#a9b1ad; --mut:#3a413c;
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s5:#d55181; --s6:#008300; --s7:#9085e9; --hl:#e66767; --accent:#43b0a5; }} }}
:root[data-theme="dark"] {{ --paper:#15181a; --card:#1c2023; --line:#32383b; --ink:#eef0ee; --ink2:#a9b1ad; --mut:#3a413c;
  --s1:#3987e5; --s2:#d95926; --s3:#199e70; --s4:#c98500; --s5:#d55181; --s6:#008300; --s7:#9085e9; --hl:#e66767; --accent:#43b0a5; }}
body {{ margin:0; background:var(--paper); color:var(--ink); font-family:"IBM Plex Sans",sans-serif; font-size:15px; line-height:1.6; }}
.wrap {{ max-width:1080px; margin:0 auto; padding:36px 26px 60px; }}
h1 {{ font-family:Archivo,sans-serif; font-size:clamp(26px,4vw,36px); margin:0 0 8px; }}
h2 {{ font-family:Archivo,sans-serif; font-size:19px; margin:34px 0 6px; }}
.eyebrow {{ font-family:"IBM Plex Mono",monospace; font-size:12px; letter-spacing:.13em; text-transform:uppercase; color:var(--accent); }}
.sub {{ color:var(--ink2); max-width:70ch; }}
.panel {{ background:var(--card); border:1px solid var(--line); border-radius:8px; padding:14px 16px; margin-top:10px; overflow-x:auto; }}
.tlsvg {{ width:100%; height:auto; display:block; }}
.tick {{ stroke:var(--line); }} .grid {{ stroke:var(--line); stroke-dasharray:2 3; }}
.tl {{ font:11px "IBM Plex Mono",monospace; fill:var(--ink2); text-anchor:middle; }}
.lg {{ font:12.5px "IBM Plex Sans",sans-serif; fill:var(--ink2); }}
.clab {{ font:11px "IBM Plex Mono",monospace; fill:var(--ink2); }}
.line-busy {{ fill:none; stroke:var(--s1); stroke-width:1.6; }} .c-busy {{ fill:var(--s1); }}
.line-conc {{ fill:none; stroke:var(--s2); stroke-width:1.4; }} .c-conc {{ fill:var(--s2); }}
.c-hl {{ fill:var(--hl); }}
code {{ font-family:"IBM Plex Mono",monospace; font-size:.9em; }}
</style>
<div class="wrap">
<p class="eyebrow">h23 · AutoTrace G10 · capture {a.label}</p>
<h1>Agentix Serving 时间线</h1>
<p class="sub">LLaMA-3.1-8B · vLLM 0.29 · 单卡 RTX 4090。三视图均从捕获数据直接渲染（{len(seg)} 个请求、
{len(ks):,} 个 GPU 项、窗口 {dur_s:.0f} s）；坐标为对齐后的 nsys 时钟（对齐 spread 见 w02'）。</p>

<h2>V1 · 端到端时间线</h2>
<p class="sub">GPU busy（0.5 s 分箱，联合区间）与在飞请求数同钟叠放。</p>
<div class="panel">{''.join(v1)}</div>

<h2>V2 · 高延迟时间线</h2>
<p class="sub">每行一个请求（提交→完成），按程序类分组；红色 = decode 超过类中位数 + 3×MAD 的高延迟实例。</p>
<div class="panel">{''.join(v2)}</div>

<h2>V3 · 并发分析时间线</h2>
<p class="sub">在飞请求数按 w01' 并发桶着色；图例给出每桶占 GPU 时间的份额（两轴互证）。</p>
<div class="panel">{''.join(v3)}</div>

<h2>综合（G10 synthesis）</h2>
<p class="sub">① 有请求在飞的时段 GPU busy 均值 {mean_busy_active:.1f} %（全窗 {w01["gpu_busy_pct"]} %）——
V1 中 busy 曲线跟随并发曲线起落，尾部长平台是单个 LATS 程序独占（V3 尾段绿色低并发带）。
② 高延迟实例 {n_hl}/{len(seg)}（{100*n_hl/len(seg):.1f} %）集中在并发峰段（V2 红块与 V1 峰对齐）：
批越大单请求 decode 越慢——这是共享批的代价，而非排队（w02' 队列占比很小）。
③ V3 的时间轴视角与 GPU 时间份额互证：高并发桶时段短但吞吐密度高，低并发长尾贡献 wall 却浪费容量——
正是 w05'' 机会窗口「提高批驻留有吞吐余量、无延迟收益」的可视化形态。</p>
<p class="sub" style="font-family:'IBM Plex Mono',monospace;font-size:12px">
数据：{d}/analysis/(request_segments.csv · concurrency_windows.csv · w01_serving_conservation.json)</p>
</div>'''
    a.out.write_text(html)
    print(json.dumps({"out": str(a.out), "requests": len(seg), "high_latency": n_hl,
                      "bins": len(busy_pct), "peak_conc": peak_c}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

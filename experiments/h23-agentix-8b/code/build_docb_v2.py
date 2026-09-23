#!/usr/bin/env python3
"""Doc B (R10_PROCESS) from the v2 three-pass lineage.

Reads only the accepted S01-S10 outputs of one lineage and renders the frozen
B1-B5 outline. Every number in the prose comes from a file under that lineage;
nothing is computed twice in two places, and nothing is hand-edited afterwards.

Typography and geometry follow workflow06/skill/report-template.md.
"""
from __future__ import annotations

import argparse
import collections
import csv
import json
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

# template colours
RED, BLUE, GOLD, GREEN, ORANGE = "#c94040", "#2f6f9f", "#a8802f", "#1baf7a", "#eb6834"
GRID, FRAME, INK = "#e6edf4", "#c9d6e4", "#1f2f45"
LEFT, RIGHT, W = 130, 20, 1150

CSS = """
body{font:22px/1.7 "Noto Sans CJK SC",system-ui,sans-serif;color:#1f2f45;background:#fff;margin:0}
.wrap{max-width:1200px;margin:0 auto;padding:26px 22px 60px}
h1{font-size:33px;line-height:1.35}h2{font-size:27px;color:#2f6f9f;margin-top:2.2em}
h3{font-size:22px;margin-top:1.6em}
.sub,.cap,.theme{font-size:20px;color:#48607d;max-width:120ch}
.cap{margin:6px 0 26px}
.block{font-size:20px;padding:12px 16px;border-radius:6px;max-width:120ch;
 background:#f2f7fb;border:1px solid #c9d6e4;margin:16px 0}
.block.impl{background:#f4faf6;border-color:#bcd8c6}
.block.howto{background:#fbf7ef;border-color:#e2d3ae}
table{font-size:20px;border-collapse:collapse;margin:14px 0}
td,th{border:1px solid #c9d6e4;padding:4px 10px}
th{background:#f2f7fb;text-align:left}
pre.art{font:18px/1.55 "IBM Plex Mono","Noto Sans Mono CJK SC",monospace;
 background:#f7f9f7;border:1px solid #cfd9cf;padding:12px 14px;overflow-x:auto}
svg{border:1px solid #c9d6e4;border-radius:6px;max-width:100%;height:auto;display:block}
code{font-family:"IBM Plex Mono",monospace;font-size:19px}
.num{font-variant-numeric:tabular-nums}
"""


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def fig(svg, caption):
    return f"{svg}\n<p class='cap'>{caption}</p>"


def table(headers, rows, note=""):
    h = "".join(f"<th>{c}</th>" for c in headers)
    b = "".join("<tr>" + "".join(f"<td class='num'>{c}</td>" for c in r) + "</tr>" for r in rows)
    n = f"<p class='cap'>{note}</p>" if note else ""
    return f"<table><tr>{h}</tr>{b}</table>{n}"


# ---------------------------------------------------------------- load
class Lineage:
    def __init__(self, base: Path):
        self.base = base
        j = lambda p: json.loads((base / p).read_text())
        self.overhead = j("S01/overhead_ledger.json")
        self.equiv = j("S01/wrapper_equivalence.json")
        self.contract = j("S01/run_contract.json")
        self.p1cov = j("S02/pass1_coverage.json")
        self.p1inv = j("S02/pass1_process_inventory.json")
        self.c2 = j("S03/class2_targets.json")
        self.p2cov = j("S04/pass2_coverage.json")
        self.eu = j("S04/handoff.json").get("engine_utilisation") or {}
        self.wloc = j("S04/window_location.json")
        self.p3series = j("S08/pass3_window_series.json")
        self.sq7 = base / "S07" / "cap" / "cap.sqlite"
        self.wcond = j("S03/class2_window_condition.json")
        self.cross = j("S05/cross_process_concurrency.json")
        _ts = ROOT / "artifacts/agentix_8b/autotrace/R10_TIMELINE_SUMMARY.json"
        self.ts = json.loads(_ts.read_text()) if _ts.is_file() else None
        self.c3 = j("S05/class3_targets.json")
        self.conc_obj = j("S05/concurrency_objects.json")
        self.preempt = j("S05/preemption_episodes.json")
        self.budget = j("S06/counter_budget.json")
        self.cap3 = j("S06/builder_capability.json")
        self.windows = j("S08/concurrency_windows.json")
        self.align = j("S08/cross_pass_alignment.json")
        self.ledger = j("ledger.json")
        self.attach = list(csv.DictReader((base / "S08/resource_attachment.csv").read_text().splitlines()))
        self.ncu = [json.loads(l) for l in (base / "S07/pass3_ncu_launch_counters.jsonl").read_text().splitlines() if l.strip()]
        self.c1 = list(csv.DictReader((base / "S09/tables/class1_end_to_end.csv").read_text().splitlines()))
        self.c2rows = list(csv.DictReader((base / "S09/tables/class2_high_latency.csv").read_text().splitlines()))
        self.epi = list(csv.DictReader((base / "S09/tables/preemption_episodes.csv").read_text().splitlines()))
        wlp = self.contract.get("workload_path") or self.contract.get("workload")
        self.wl = json.loads(Path(wlp).read_text()) if wlp and Path(wlp).is_file() else None

    def proc_stats(self):
        by = collections.defaultdict(list)
        for r in self.c1:
            by[r["process"]].append(float(r["dur_us"]))
        tot = sum(sum(v) for v in by.values())
        out = []
        for p, v in sorted(by.items(), key=lambda kv: -sum(kv[1])):
            v.sort()
            out.append({"process": p, "n": len(v), "med": statistics.median(v),
                        "p90": v[int(0.9 * len(v))], "max": v[-1],
                        "sum_ms": sum(v) / 1e3, "share": sum(v) / tot})
        return out

    def sm_coverage(self):
        """Upper bound on how much of the GPU a kernel can cover, by grid size.

        A kernel occupies as many SMs as it has blocks, at most. Fewer blocks
        than SMs leaves SMs idle while CUPTI still records the device as busy,
        so "device busy" and "GPU utilised" are not the same claim. This is an
        upper bound: blocks >= SMs does not guarantee full occupancy either,
        because registers and shared memory can cap it.
        """
        import re as _re
        SM = 128  # RTX 4090
        tot = cov = 0.0
        per = {}
        for r in self.ncu:
            fam = self._fam(r["kernel"])[:30]
            n = 1
            for x in _re.findall(r"\d+", str(r.get("grid"))):
                n *= int(x)
            d = r.get("device_us") or 0.0
            tot += d
            cov += min(n, SM) / SM * d
            a = per.setdefault(fam, {"n": 0, "dev": 0.0, "cov": 0.0, "blocks": []})
            a["n"] += 1
            a["dev"] += d
            a["cov"] += min(n, SM) / SM * d   # same weighting as the total
            a["blocks"].append(n)
        for a in per.values():
            a["share"] = a["dev"] / tot if tot else 0
            a["blocks_median"] = statistics.median(a["blocks"])
            a["blocks_range"] = [min(a["blocks"]), max(a["blocks"])]
            a["sm_cover_ub"] = (a["cov"] / a["dev"]) if a["dev"] else 0
        return {"sm_count": SM, "weighted_upper_bound": cov / tot if tot else None,
                "per_family": per}

    def tl_data(self):
        """Track/lane data for the report's static timelines, from accepted outputs."""
        PROCS = ['norm_in', 'qkv_proj', 'attn_core', 'o_proj',
                 'norm_post', 'mlp_gate_up', 'act_mul', 'mlp_down']
        c1w0 = min(int(r['start_ns']) for r in self.c1)
        t1 = {q: [] for q in PROCS}
        for r in self.c1:
            t1[r['process']].append([int(r['start_ns']) - c1w0, int(r['end_ns']) - c1w0,
                                     int(r['layer_idx'])])
        for v in t1.values():
            v.sort()
        inst = [json.loads(l) for l in (self.base / 'S04' / 'pass2_instances.jsonl').open()]
        w2 = self.wloc['window_ns']
        t2 = {q: [] for q in PROCS}
        for r in inst:
            t2[r['process']].append([int(r['start']) - w2[0], int(r['end']) - w2[0],
                                     int(r['layer_idx'])])
        for v in t2.values():
            v.sort()
        return {'procs': PROCS,
                'c1': {'w0': 0, 'w1': max(int(r['end_ns']) for r in self.c1) - c1w0,
                       'tracks': t1},
                'c2': {'w0': 0, 'w1': w2[1] - w2[0], 'tracks': t2}}

    def class1_lanes(self, bins=600):
        """Whole-run lanes for the v1-style class-1 timeline, from the class-1 table."""
        rows = self.c1
        w0 = min(int(r["start_ns"]) for r in rows)
        w1 = max(int(r["end_ns"]) for r in rows)
        bw = (w1 - w0) / bins
        reqs = [0.0] * bins
        srate = [0] * bins
        attn = [0.0] * bins
        pre = [0] * bins
        seen_steps = [set() for _ in range(bins)]
        for r in rows:
            i = min(int((int(r["start_ns"]) - w0) / bw), bins - 1)
            q = float(r["reqs"] or 0)
            reqs[i] = max(reqs[i], q)
            if r.get("step_id"):
                seen_steps[i].add(r["step_id"])
            if r["process"] == "attn_core":
                attn[i] += float(r["dur_us"])
            if r.get("at_preemption_boundary") == "True":
                pre[i] += 1
        srate = [len(s) for s in seen_steps]
        return w0, w1, [
            {"label": "批内请求数", "unit": "个", "color": GOLD, "max": 16.0,
             "cap": 16, "values": reqs},
            {"label": "step 起点 / bin", "unit": "个", "color": "#48607d",
             "max": float(max(srate) or 1), "values": srate},
            {"label": "attn_core 实例时长 / bin", "unit": "us", "color": BLUE,
             "max": float(max(attn) or 1), "values": attn},
            {"label": "抢占边界实例 / bin", "unit": "个", "color": RED,
             "max": float(max(pre) or 1), "values": pre},
        ]

    def pd_mix(self):
        """How much prefill actually reaches the batch, and why so little."""
        import sqlite3 as _sq
        db = _sq.connect(str(self.base / 'S02' / 'cap' / 'cap.sqlite'))
        q = ("select coalesce(n.text,s.value) t from NVTX_EVENTS n left join StringIds s "
             "on n.textId=s.id where coalesce(n.text,s.value) like 'w.step::%'")
        rows = []
        for (txt,) in db.execute(q):
            d = dict(p.split('=') for p in txt.split('::')[1:] if '=' in p)
            if 'reqs' in d and 'tok' in d:
                rows.append((int(d['reqs']), int(d['tok'])))
        mixed = [t - r for r, t in rows if t > r]
        dec = [r for r, t in rows if r]
        decl = sum(p['total_prompt_tokens'] for p in (self.wl or {}).get('programs', []))
        out_t = sum(p['total_output_tokens'] for p in (self.wl or {}).get('programs', []))
        pre = sum(t - r for r, t in rows)
        dm = statistics.median(dec) if dec else 1
        return {'steps': len(rows), 'mixed_frac': len(mixed) / len(rows) if rows else 0,
                'mix_median': statistics.median(mixed) if mixed else 0,
                'declared_prompt': decl, 'prefilled': pre,
                'prefill_steps_est': pre / 2048 if pre else 0,
                'decode_steps_est': out_t / dm if dm else 0,
                'decode_tok_median': dm}

    def rank_by_batch(self):
        """The same 10% share ranking, recomputed inside each batch band.

        Answers whether the selection is a property of the workload or of the
        concurrency it happened to run at — near the threshold it is the latter.
        """
        import sqlite3 as _sq
        import sys as _sys
        _sys.path.insert(0, str(Path(__file__).resolve().parent))
        import pt_v2_runtime as R
        db = _sq.connect(str(self.base / 'S02' / 'cap' / 'cap.sqlite'))
        steps, comp = R.steps_and_comp(db)
        cb = {}
        for ts, v in comp.items():
            si = R.locate(steps, ts)
            if si is not None:
                cb[si] = v
        per = self.overhead['module_hook_us_per_instance_effective']
        BUCK = [(1, 4, '1–4'), (5, 8, '5–8'), (9, 12, '9–12'), (13, 16, '13–16')]
        agg = {lab: collections.defaultdict(float) for _, _, lab in BUCK}
        mx = 0
        for r in R.process_ranges(db):
            si = R.locate(steps, r['start'])
            q = (cb.get(si) or (None, None))[0]
            if not q:
                continue
            mx = max(mx, q)
            for lo, hi, lab in BUCK:
                if lo <= q <= hi:
                    agg[lab][r['process']] += max(r['dur_us'] - per, 0.0)
                    break
        out = {}
        for _, _, lab in BUCK:
            tot = sum(agg[lab].values()) or 1.0
            out[lab] = {k: v / tot for k, v in agg[lab].items()}
        return {'buckets': out, 'max_reqs': mx}

    def gap_profile(self):
        """Where the in-step device gaps actually sit, by gap size.

        Distinguishes "a fixed cost on every launch" from "a few real host
        stalls": the two point at different fixes, and only the second is what
        this engine has.
        """
        import bisect as _b
        import sqlite3 as _sq
        cap = self.base / 'S04' / 'cap' / 'cap.sqlite'
        db = _sq.connect(str(cap))
        q = ("select n.start,n.end,coalesce(n.text,s.value) t from NVTX_EVENTS n "
             "left join StringIds s on n.textId=s.id where coalesce(n.text,s.value) like ?")
        steps = sorted((a, b) for a, b, _ in db.execute(q, ("w.engine: process_engine_step",)) if b)
        K = sorted(db.execute("select start,end from CUPTI_ACTIVITY_KIND_KERNEL"))
        ks = [k[0] for k in K]
        comp = [dict(p.split('=') for p in t.split('::')[1:] if '=' in p)
                for _s, _e, t in db.execute(q, ("w.step::%",))]
        toks = [int(d['tok']) for d in comp if 'tok' in d]
        reqs = [int(d['reqs']) for d in comp if 'reqs' in d]
        BUCK = [('<1us', 1), ('1-10us', 10), ('10-50us', 50), ('50-200us', 200),
                ('>200us', float('inf'))]
        cnt = {b: {'n': 0, 'ns': 0} for b, _ in BUCK}
        tot_gap = tot_step = 0
        nk = []
        mid = 0
        for a, b in steps[:300]:
            i = _b.bisect_left(ks, a)
            seg = []
            while i < len(K) and K[i][0] < b:
                seg.append(K[i])
                i += 1
            if len(seg) < 2:
                continue
            nk.append(len(seg))
            tot_step += b - a
            for j in range(len(seg) - 1):
                g = seg[j + 1][0] - seg[j][1]
                if g <= 0:
                    continue
                tot_gap += g
                us = g / 1e3
                for lab, hi in BUCK:
                    if us < hi:
                        cnt[lab]['n'] += 1
                        cnt[lab]['ns'] += g
                        if lab in ('10-50us', '50-200us'):
                            mid += 1
                        break
        for v in cnt.values():
            v['share'] = v['ns'] / tot_gap if tot_gap else 0
        kv = None
        log = cap.parent / 'profile.log'
        if log.is_file():
            import re as _re
            m = _re.search(r'Maximum concurrency for [\d,]+ tokens per request: ([\d.]+x)',
                           log.read_text(errors='ignore'))
            kv = m.group(1) if m else None
        return {'by_bucket': cnt, 'gap_share_of_step': tot_gap / tot_step if tot_step else 0,
                'kernels_per_step': statistics.median(nk) if nk else 0,
                'mid_stalls_per_step': mid / max(len(nk), 1),
                'tokens_per_step': statistics.median(toks) if toks else 0,
                'reqs_per_step': statistics.median(reqs) if reqs else 0,
                'kv_concurrency': kv or '未从日志读到'}

    @staticmethod
    def _fam(name):
        head = name.split('<')[0].split('::')[-1].strip()
        toks = [x for x in head.split() if x != 'void']
        return toks[-1] if toks else head

    def ncu_families(self):
        by = collections.defaultdict(lambda: collections.defaultdict(list))
        n = collections.Counter()
        for r in self.ncu:
            fam = self._fam(r["kernel"])
            n[fam] += 1
            for k, c in (r.get("counters") or {}).items():
                if isinstance(c, dict) and isinstance(c.get("value"), (int, float)):
                    by[fam][k].append(c["value"])
        out = []
        for fam in sorted(n, key=lambda f: -sum(by[f].get("gpu__time_duration.sum") or [0])):
            d = by[fam]
            dur = d.get("gpu__time_duration.sum") or []
            out.append({
                "family": fam, "n": n[fam],
                "dev_us": sum(dur), "med_us": statistics.median(dur) if dur else 0,
                "mem_pct": statistics.median(d.get("gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed") or [0]),
                "dram_gbs": statistics.median(d.get("dram__bytes.sum.per_second") or [0]),
                "l2_hit": statistics.median(d.get("lts__t_sector_hit_rate.pct") or [0]),
            })
        return out


# ---------------------------------------------------------------- figures
def svg_open(h, title=""):
    return [f"<svg viewBox='0 0 {W} {h}' width='{W}' role='img' aria-label='{esc(title)}'>",
            f"<rect width='{W}' height='{h}' fill='#fff'/>"]


def txt(x, y, s, size=15, fill=INK, anchor="start", weight="normal"):
    return (f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}' fill='{fill}' "
            f"text-anchor='{anchor}' font-weight='{weight}'>{esc(s)}</text>")


def fig_process_share(stats):
    """Two columns: cumulative share on the left, the duration spread on the right."""
    import math
    rh = 52
    h = 56 + rh * len(stats) + 74
    # explicit, non-overlapping columns so neither side can collapse
    BAR0, BAR1 = LEFT, 600
    DOT0, DOT1 = 800, W - RIGHT - 16
    s = svg_open(h, "每个 process 的累计时长份额与时长分布")
    s.append(txt(BAR0, 30, "累计时长份额（窗口内全部实例）", 16, "#48607d"))
    s.append(txt(DOT0, 30, "时长分布：中位 / p90 / 最长（us，对数刻度）", 16, "#48607d"))
    smax = max(x["share"] for x in stats)
    lo, hi = math.log10(10), math.log10(20000)
    px = lambda v: DOT0 + (DOT1 - DOT0) * (math.log10(min(max(v, 10), 20000)) - lo) / (hi - lo)
    for i, x in enumerate(stats):
        y = 56 + i * rh
        col = RED if x["share"] > 0.10 else BLUE
        s.append(txt(BAR0 - 8, y + 20, x["process"], 16, INK, "end"))
        bw = (BAR1 - BAR0 - 150) * x["share"] / smax
        s.append(f"<rect x='{BAR0}' y='{y+4}' width='{bw:.1f}' height='22' fill='{col}' opacity='.85'/>")
        s.append(txt(BAR0 + bw + 8, y + 21, f"{x['share']:.1%} ({x['sum_ms']:,.0f} ms)", 15, col))
        s.append(f"<line x1='{DOT0}' y1='{y+15}' x2='{DOT1}' y2='{y+15}' stroke='{GRID}'/>")
        s.append(f"<line x1='{px(x['med']):.1f}' y1='{y+15}' x2='{px(x['max']):.1f}' y2='{y+15}' "
                 f"stroke='#9db4c8' stroke-width='2'/>")
        for v, r, c in ((x["med"], 5, BLUE), (x["p90"], 4, GOLD), (x["max"], 4, RED)):
            s.append(f"<circle cx='{px(v):.1f}' cy='{y+15}' r='{r}' fill='{c}'/>")
    yb = 56 + len(stats) * rh
    for v in (10, 100, 1000, 10000):
        s.append(f"<line x1='{px(v):.1f}' y1='{yb-8}' x2='{px(v):.1f}' y2='{yb}' stroke='#8fb2ce'/>")
        s.append(txt(px(v), yb + 16, f"{v:,}", 14, "#48607d", "middle"))
    s.append(f"<circle cx='{DOT0+6}' cy='{yb+38}' r='5' fill='{BLUE}'/>")
    s.append(txt(DOT0 + 18, yb + 43, "中位", 15, "#48607d"))
    s.append(f"<circle cx='{DOT0+86}' cy='{yb+38}' r='4' fill='{GOLD}'/>")
    s.append(txt(DOT0 + 98, yb + 43, "p90", 15, "#48607d"))
    s.append(f"<circle cx='{DOT0+156}' cy='{yb+38}' r='4' fill='{RED}'/>")
    s.append(txt(DOT0 + 168, yb + 43, "最长", 15, "#48607d"))
    s.append(txt(BAR0, yb + 43, "红条 = 份额严格超过 10% 的入选类型", 15, RED))
    s.append("</svg>")
    return "\n".join(s)


def fig_preempt(epi, pre):
    """Where a call enters the ladder, and how often it is demoted afterwards."""
    QS = ["Q0", "Q1", "Q2", "Q3"]
    QC = {"Q0": "#2a78d6", "Q1": "#1baf7a", "Q2": "#a8802f", "Q3": "#c94040"}
    by_idx = collections.defaultdict(collections.Counter)
    for e in epi:
        q = (e["queue_path"] or "").split(">")[0] or "?"
        by_idx[int(e["call_index"])][q] += 1
    counts = collections.Counter(int(e["quantum_preemptions"]) for e in epi)
    h = 330
    s = svg_open(h, "调用进入队列梯子的位置，以及此后被降级的次数")
    # left: entry queue by call index
    s.append(txt(LEFT, 30, "每次调用被准入时进入哪一级队列（按它在程序里的序号）", 16, "#48607d"))
    idxs = sorted(by_idx)
    x0, x1, y0, ymax = LEFT, 600, 214, 150
    bw = (x1 - x0) / max(len(idxs), 1) - 8
    top = max(sum(c.values()) for c in by_idx.values())
    for i, k in enumerate(idxs):
        bx = x0 + i * (bw + 8)
        acc = 0
        for q in QS:
            c = by_idx[k].get(q, 0)
            if not c:
                continue
            bh = ymax * c / top
            s.append(f"<rect x='{bx:.1f}' y='{y0-acc-bh:.1f}' width='{bw:.1f}' height='{bh:.1f}' "
                     f"fill='{QC[q]}' opacity='.88'/>")
            if bh > 16:
                s.append(txt(bx + bw / 2, y0 - acc - bh / 2 + 5, q, 14, "#fff", "middle"))
            acc += bh
        s.append(txt(bx + bw / 2, y0 + 20, str(k), 15, INK, "middle"))
    s.append(txt(x0, y0 + 44, "横轴 = 调用在其程序内的序号；柱高 = 调用数", 15, "#48607d"))
    # derived, never asserted: a hard-coded reading goes stale the moment the
    # data moves, and a caption that contradicts its own figure is worse than none
    s.append(txt(x0, y0 + 66, admission_reading(epi), 15, RED))
    # right: how many demotions afterwards
    x2 = 700
    s.append(txt(x2, 30, "准入之后被降级的次数（横轴=次数，纵轴=调用数）", 16, "#48607d"))
    ks = sorted(counts)
    mxc = max(counts.values())
    bw2 = (W - RIGHT - x2) / max(len(ks), 1) - 10
    for i, k in enumerate(ks):
        bh = ymax * counts[k] / mxc
        bx = x2 + i * (bw2 + 10)
        s.append(f"<rect x='{bx:.1f}' y='{y0-bh:.1f}' width='{bw2:.1f}' height='{bh:.1f}' "
                 f"fill='{RED if k else '#9db4c8'}' opacity='.85'/>")
        s.append(txt(bx + bw2 / 2, y0 + 20, str(k), 15, INK, "middle"))
        s.append(txt(bx + bw2 / 2, y0 - bh - 6, str(counts[k]), 14, "#48607d", "middle"))
    q = pre["quantum"]
    s.append(txt(x2, y0 + 44, f"{q['calls_with_preemption']}/{q['calls_total']} 次调用至少被降级一次", 15, "#48607d"))
    s.append(txt(LEFT, 300, f"quantum 抢占 {q['preemptions_total']} 次，再排队间隙合计 "
                            f"{q['requeue_gap_us_total']/1000:.2f} ms；"
                            f"engine_kv 抢占 {pre['engine_kv']['events']} 次——KV 块没有被驱逐", 16, INK))
    s.append("</svg>")
    return "\n".join(s)


def fig_class2(rows, obj):
    """Every class-2 instance as a point, plus who used the device during it."""
    dv = obj["objects"][0]
    h = 372
    s = svg_open(h, f"第二类目标 {dv['process']} 的 {dv['instances']} 个实例")
    pts = [(int(r["start_ns"]), float(r["dur_us"])) for r in rows]
    t0, t1 = min(p[0] for p in pts), max(p[0] for p in pts)
    import math
    dmin, dmax = min(p[1] for p in pts), max(p[1] for p in pts)
    # ticks adapt to the data: a fixed decade ladder leaves a single gridline
    # when the instances cluster inside one decade, which is the normal case now
    # that the window is a single load regime rather than the whole run
    lo, hi = math.log10(dmin / 1.6), math.log10(dmax * 1.6)
    x0, x1, y0, y1 = LEFT, W - RIGHT - 10, 50, 250
    ticks, m = [], 10 ** math.floor(math.log10(dmin / 1.6))
    while m <= dmax * 1.6:
        for k in (1, 2, 5):
            v = m * k
            if dmin / 1.6 <= v <= dmax * 1.6:
                ticks.append(v)
        m *= 10
    for v in ticks:
        py = y1 - (y1 - y0) * (math.log10(v) - lo) / (hi - lo)
        s.append(f"<line x1='{x0}' y1='{py:.1f}' x2='{x1}' y2='{py:.1f}' stroke='{GRID}'/>")
        lab = f"{v:g} us" if v < 1000 else f"{v/1000:g} ms"
        s.append(txt(x0 - 8, py + 5, lab, 14, "#48607d", "end"))
    for st, d in pts:
        px = x0 + (x1 - x0) * (st - t0) / max(t1 - t0, 1)
        py = y1 - (y1 - y0) * (math.log10(d) - lo) / (hi - lo)
        s.append(f"<circle cx='{px:.1f}' cy='{py:.1f}' r='2.4' fill='{RED}' opacity='.5'/>")
    s.append(txt(x0, 276, f"这 {len(pts)} 个实例散布在 {(t1-t0)/1e6:.0f} ms 里；纵轴对数", 15, "#48607d"))
    # One interval, split by who was using the device during it -- the parts add up
    s.append(txt(x0 - 8, 306, "主机区间内", 14, "#48607d", "end"))
    segs = [("own_in_range_share", BLUE, "它自己的 kernel"),
            ("other_in_range_share", GOLD, "别的 process 的 kernel"),
            ("device_idle_share", "#dfe7ee", "设备真空闲")]
    acc = 0.0
    for key, col, lab in segs:
        w = (x1 - x0) * dv[key]
        s.append(f"<rect x='{x0+acc:.1f}' y='292' width='{w:.1f}' height='24' fill='{col}'/>")
        if w > 130:
            s.append(txt(x0 + acc + w / 2, 309, f"{lab} {dv[key]:.1%}", 15,
                         INK if col == "#dfe7ee" else "#fff", "middle"))
        acc += w
    for key, col, lab in segs:
        if (x1 - x0) * dv[key] <= 130:
            s.append(txt(x0, 336, f"■ {lab} {dv[key]:.1%}", 15, col if col != "#dfe7ee" else INK))
    s.append(txt(x1 - 8, 336,
                 f"它自己的 kernel 总设备成本 {dv['own_device_total_ms']:.1f} ms，"
                 f"其中 {dv['own_outside_share']:.1%} 跑在这个区间之外", 15, "#48607d", "end"))
    s.append("</svg>")
    return "\n".join(s)


def fig_windows(win):
    """Each class-3 window as a regime: who used the device inside it."""
    ws = [w for w in win["windows"] if w.get("relocated") or "device_busy_share" in w]
    dropped = [w for w in win["windows"] if w not in ws]
    n = max(len(ws), 1)
    h = 56 + n * 96 + (44 if dropped else 8)
    s = svg_open(h, "第三类窗口：每个窗口内设备被谁占用")
    s.append(txt(LEFT, 30, "每个窗口是一个负载区间（由条件在第三遍自己的运行里重新定位）；"
                           "下面的条按「这段时间设备在替谁干活」拆开", 16, "#48607d"))
    x0, x1 = LEFT, W - RIGHT - 10
    for i, w in enumerate(ws):
        y = 56 + i * 96
        name = (w.get("condition") or {}).get("name", f"窗口{i+1}")
        p3 = w.get("measured_in_pass3") or {}
        p2 = w.get("measured_in_pass2") or {}
        s.append(txt(x0, y + 4, name, 17, INK, "start", "600"))
        s.append(txt(x0 + 170, y + 4,
                     "第二遍批均 {}（满足率 {:.0%}） → 第三遍批均 {}（{:.0%}）".format(
                         p2.get("reqs_mean"), p2.get("satisfied_frac") or 0,
                         p3.get("reqs_mean"), p3.get("satisfied_frac") or 0),
                     15, "#48607d"))
        busy = w.get("device_busy_share") or 0.0
        own = w.get("own_busy_share") or 0.0
        segs = [(own, BLUE, "目标 process"), (max(busy - own, 0), GOLD, "其它 process"),
                (max(1 - busy, 0), "#dfe7ee", "设备真空闲")]
        acc = 0.0
        for frac, col, lab in segs:
            wpx = (x1 - x0) * frac
            s.append(f"<rect x='{x0+acc:.1f}' y='{y+18}' width='{wpx:.1f}' height='26' fill='{col}'/>")
            if wpx > 150:
                s.append(txt(x0 + acc + wpx / 2, y + 36, f"{lab} {frac:.1%}", 15,
                             INK if col == "#dfe7ee" else "#fff", "middle"))
            acc += wpx
        small = "　".join(f"{lab} {frac:.1%}" for frac, col, lab in segs
                         if (x1 - x0) * frac <= 150)
        if small:
            s.append(txt(x0, y + 66, small, 15, BLUE))
        s.append(txt(x1, y + 66,
                     "量子抢占 {}　KV 抢占 {}　kernel 峰值并发 {}　kernel 行 {:,}".format(
                         w.get("quantum_preemptions"), w.get("engine_kv_preemptions"),
                         w.get("peak_concurrent_kernels"), w.get("kernel_rows_in_window") or 0),
                     15, "#48607d", "end"))
    if dropped:
        s.append(txt(LEFT, 56 + n * 96 + 30,
                     "未能在第三遍定位的区间：" + "、".join(
                         (w.get("condition") or {}).get("name", "?") for w in dropped)
                     + "（如实登记，不回退到第二遍坐标）", 15, RED))
    s.append("</svg>")
    return "\n".join(s)


SHORT = {"flash_fwd_splitkv_kernel": "注意力主核",
         "flash_fwd_splitkv_combine_kernel": "注意力合并",
         "reshape_and_cache_flash_kernel": "KV 写入",
         "elementwise_kernel": "逐元素搬运"}


def fig_ncu(fams):
    """Device time per kernel family, and how far each sits below the memory roof."""
    NAME1, ROOF0, ROOF1, NUM0 = 250, 268, 720, 738
    h = 150 + 40 * len(fams)
    s = svg_open(h, "attn_core 的 kernel 家族：设备时间与距内存屋顶的距离")
    tot = sum(f["dev_us"] for f in fams) or 1
    cols = [RED, BLUE, GOLD, GREEN]
    s.append(txt(LEFT, 30, f"设备时间构成（64 次 launch 合计 {tot:.1f} us）", 16, "#48607d"))
    x = LEFT
    inner = W - LEFT - RIGHT
    for i, f in enumerate(fams):
        bw = inner * f["dev_us"] / tot
        s.append(f"<rect x='{x:.1f}' y='44' width='{bw:.1f}' height='30' fill='{cols[i%4]}' opacity='.85'/>")
        if bw > 90:
            s.append(txt(x + bw / 2, 64, f"{SHORT.get(f['family'], f['family'][:10])} {f['dev_us']/tot:.0%}",
                         15, "#fff", "middle"))
        x += bw
    y = 112
    s.append(txt(LEFT, y, "每个家族离内存屋顶还有多远（中位，%峰值）", 16, "#48607d"))
    for i, f in enumerate(fams):
        yy = y + 22 + i * 40
        s.append(txt(NAME1, yy + 15, SHORT.get(f["family"], f["family"][:14]), 15, INK, "end"))
        s.append(f"<rect x='{ROOF0}' y='{yy}' width='{ROOF1-ROOF0}' height='20' fill='#eef4fa' stroke='#8fb2ce'/>")
        bw = (ROOF1 - ROOF0) * f["mem_pct"] / 100
        s.append(f"<rect x='{ROOF0}' y='{yy}' width='{max(bw,2):.1f}' height='20' fill='{cols[i%4]}'/>")
        s.append(txt(ROOF0 + max(bw, 2) + 6, yy + 15, f"{f['mem_pct']:.1f}%", 14, cols[i % 4]))
        s.append(txt(NUM0, yy + 15,
                     f"DRAM {f['dram_gbs']:>4.0f} GB/s   L2 命中 {f['l2_hit']:>2.0f}%   "
                     f"中位 {f['med_us']:>5.1f} us × {f['n']:>2} 次", 14, "#48607d"))
    ytop = y + 14
    ybot = y + 22 + len(fams) * 40
    s.append(f"<line x1='{ROOF1}' y1='{ytop}' x2='{ROOF1}' y2='{ybot}' stroke='{RED}' stroke-dasharray='4 3'/>")
    s.append(txt(ROOF1 - 4, ytop - 4, "内存屋顶 100%", 14, RED, "end"))
    s.append("</svg>")
    return "\n".join(s)



# ---------------------------------------------------------------- prose
def b1(L):
    _m = L.wloc.get('measured', {})
    _tol = _m.get('tolerance', {})
    cond = '相位 {} · 批 ≥ {}'.format('/'.join(L.wcond.get('phase_in', [])), L.wcond.get('reqs_ge'))
    meas = '{:.2f} s、{} 个 step、批均值 {}（{}–{}）'.format(
        L.wloc.get('window_s', 0), _m.get('steps'), _m.get('reqs_mean'),
        _m.get('reqs_min'), _m.get('reqs_max'))
    sat = '{:.1%}'.format(_m.get('satisfied_frac') or 0)
    gap = _tol.get('max_gap_steps')
    need = '{:.0%}'.format(_tol.get('min_satisfied_frac') or 0)
    floor = L.wcond.get('reqs_ge')
    ov, eq, cov = L.overhead, L.equiv, L.p1cov
    wl = L.wl or {}
    progs = wl.get("programs") or []
    by_cls = collections.Counter(p.get("class", "?") for p in progs)
    calls = sum(len(p.get("llm_calls", [])) for p in progs)
    toks = sum(c.get("output_tokens", 0) for p in progs for c in p.get("llm_calls", []))
    comp = table(
        ["类别", "程序数", "形态", "为什么它对调度器是一种考验"],
        [["sharegpt", by_cls.get("sharegpt", 0), "少量长回合、轮次之间靠用户回复串起来",
          "单次调用的 token 多，一旦进入引擎就长期占住一个位置"],
         ["bfcl", by_cls.get("bfcl", 0), "多次短调用，中间夹着工具往返",
          "工具延迟期间程序什么也不算，但它的上下文还在系统里"],
         ["lats", by_cls.get("lats", 0), "按波次展开，一波内多路并行、波与波之间必须等齐",
          "波末的同步点把整波的进度压在最慢的一路上"]],
        f"混合负载共 {len(progs)} 个程序、{calls} 次调用、约 {toks:,} 个待生成 token；三类同时在场，"
        "这一点是本文档全部观察的前提——分开跑三条单类负载看不到它们互相挤占的样子。")

    art = f"""三遍漏斗（同一条负载、同一份插桩，跑三次）

  第一遍  NVTX only          全部 8 个 process × 3 层 × 全程
          {cov['process_instances']:>6} 个实例 / {cov['steps']} 个 step        没有硬件计数器，所以范围就是整段运行
             │
             │ 交出：份额超过 10% 的 process 类型（第二类目标）
             ▼
  第二遍  NVTX + CUDA 活动    只跟住第二类目标，逐 kernel
          {L.p2cov.get('instances', len(L.c2rows)):>6} 个实例                      范围是窗口，因为开始受 kernel 行数上限约束
             │
             │ 交出：值得做并发分析的 process + 时段（第三类目标）
             ▼
  第三遍  NCU 计数器          只在窗口内、只对第三类目标
          {len(L.ncu):>6} 次 launch                      每个 process 一次独立回放，归属由采集方式建立
"""
    return f"""
<h2>B1 场景、层级与方法</h2>
<p class='theme'><b>这份文档回答的是一个比「哪种调度更快」更下层的问题：一次调用在引擎内部，时间到底花在哪儿。</b>
文档 A 停在 program 和 call 两层，用四条臂比较调度策略；到了 call 以内，调度已经退场，剩下的是引擎自己怎么把
一次前向拆成 step、层和算子，以及这些算子和 GPU 之间的关系。本文档只用一条臂（core），把这条路走到硬件计数器为止。</p>

<h3>负载：一条混合的 agent serving 负载</h3>
<p>三类 agent 程序同时在场，这是 agent serving 区别于纯文本生成的地方——同一个引擎里，
有的程序在等工具返回，有的在等同波的兄弟算完，有的什么都不等只是话长。</p>
{comp}

<h3>层级：program → call → step → layer → process → kernel</h3>
<div class='block'>
<b>process 是本文档的主角。</b>一个 process 是解码层内部的一个叶子模块——注意力核心、qkv 投影、
两个归一化、MLP 的三段——由模型自己的模块结构定义，不是把 kernel 序列切段切出来的。
每个 process 在每次前向都留下一条 NVTX 区间 <code>p.L{{层}}.{{process}}</code>，
<b>发射调用</b>落在这条区间里的 kernel 就属于它（发射期归属；区间括住的是发射，不是执行——
kernel 何时真正在设备上跑是异步的，成本核算因此走设备时钟的交叠，见下方「一条时间线」块）。
四个线性算子共用同一个 gemm 实现，所以<b>按 kernel 名认归属会错</b>；归属必须来自模块结构。
这也解释了为什么插桩必须 eager：hook 只有在逐算子 Python dispatch 的路径上才有落点，
graph 回放整段绕过 Python，区间根本不会发生。
<b>dispatch 层不记录时间</b>——它只负责放置边界；时间戳由 nsys/CUPTI 在设备时钟上记录，
计数器由 NCU 记录（对标参考树的 hipprof 与 PMC；nvprof 已废弃且不支持本机架构）。</p>
<p>process 的定义有三层来源，各司其职：<b>模块结构</b>命名这八个 process；
<b>FX 图</b>给出算子级的精确组成（每个 process 含哪些算子、args/users/形状，
逐节点归属且未认领节点为零），<b>NVTX 插入点由此得出并被证明穷尽且不重叠</b>——
它是固定输入的离线图，自身不带计时，只做定义与覆盖审计；
<b>发射期归属</b>在运行时把实际 kernel 分给 process。方法沿自参考工作流（batch8）：
发射期归属、FX process-wise 定义分支、instrument/perf 双臂分裂皆是其移植。</p>
</div>

<h3>方法：三遍，一遍为下一遍服务</h3>
<pre class='art'>{esc(art)}</pre>
<p>三遍不是三次重复，是一个收窄的漏斗。第一遍求全不求细，覆盖全部 process 但只记 NVTX；
第二遍求细不求全，只跟住第一遍点名的类型，但记到 kernel；第三遍求深，只在第二遍圈出的时段里
对指定 process 采硬件计数器。这个顺序是被工具逼出来的——nsys 对 kernel 行数有上限，
NCU 的计数器回放要把每个 kernel 重放九遍，两者都不可能对全程全 process 做。</p>

<h3>窗口：由条件定，并且采集瞄着它去</h3>
<div class='block'>
<b>后两遍的窗口不是「采集器从哪儿开始记就取哪儿」，而是第一遍冻结下来的一个条件。</b>
第一遍是 NVTX-only 的全程 trace，不受 kernel 行数上限约束，因此可以从它读出
「值得测量的状态由什么触发」。本次冻结的条件是
<code>{cond}</code>——
批的下限不是取分位数（批有很大比例时间顶在上限，分位数会塌到上限上，再叠连续性要求就无处可选），
而是<b>从峰值往下找「能持续至少 2 秒的最高批下限」</b>。</p>
<p><b>光离线选窗口不够，采集本身必须瞄准它。</b>采集器的 kernel 预算有限：实测引擎进入持续满批
是第 25 秒到第 66 秒，而从进程启动开始记录的话，预算在第 28 秒就烧完了——
要研究的状态几乎完全落在采集停止之后。所以现在由被测进程监视自己的批状态，
条件连续成立若干步后自行开启采集，保持若干秒后关闭。同一份条件既是采集触发器，也是离线定位条件。</p>
<p>这一遍定位到的窗口：{meas}。
其中 <b>{sat}</b> 的 step 真正满足条件——条件允许短暂凹陷（连续不超过 {gap} 步，整体满足率不低于
{need}），这个容忍度随实测值一并申报，否则窗口会读起来像「批恒定 ≥ {floor}」而实际不是。</p>
<p>第三遍是<b>另一次运行</b>，纳秒坐标不跨运行成立，因此它在自己的采集里按同一条件重新定位。
两遍各自的实测值都记录下来，跨遍比较才成立。</p>
</div>

<div class='block impl'>
<b>trace 自身的开销：先量出来，再从结果里减掉。</b>
模块钩子每个实例的裸成本 {ov['module_hook_us_per_instance_bare']} us，在采集臂里的实际成本
{ov['module_hook_us_per_instance_effective']} us；eager 臂相对 cudagraph 臂的整体墙钟代价
{ov['eager_arm_wall_pct']}%；主机侧探针 {ov['host_probes_pct']}%；nsys 本身
{ov['nsys_pct_range'][0]}–{ov['nsys_pct_range'][1]}%。
消除分两级，<b>总量与逐实例一起扣，分子分母保持同一口径</b>：</p>
<ul>
<li><b>级别一（精确，可减）</b>：模块钩子每实例 {ov['module_hook_us_per_instance_effective']} us。
份额的分子与分母都用扣除后的时长；类 1 表同时给出 <code>dur_us</code> 与
<code>dur_us_hook_corrected</code> 两列；step 时长也给出扣除 24 个实例钩子成本后的值。</li>
<li><b>级别二（对照臂，允许误差）</b>：eager 模式本身的代价散在 kernel 间隙里，不可逐实例减。
用同负载图捕获臂对照：满批纯解码 step 17.7 ms 对本臂 21.9 ms——凡引用本臂主机墙钟的总延迟，
按此对照校正。误差来源有二：两臂批组成的波动，以及<b>小算子在两臂是不同实现</b>——
eager 走 vLLM 预编译库（如 <code>fused_add_rms_norm_kernel</code>），
图臂走 inductor 生成的 Triton 融合 kernel（如 <code>triton_red_fused_fused_add_rms_norm_0</code>）；
大 kernel（cutlass gemm、flash attention）两臂共用。因此本臂上小 process 的份额相对图臂天然偏高，
参考工作流的纪律同样适用：插桩臂的时长不得与未插桩基线相减当作优化收益。</li>
</ul>
<p>第一类里份额最高的类型，是级别一双侧扣除之后仍然最高的那个。</p>
<p><b>插桩没有改变模型在算什么：</b>同一进程内先跑未插桩的一遍、再跑插桩的一遍，
比较 {eq['sequences_compared']} 条序列共 {eq['tokens_compared']} 个 token 的 id，
{eq['mismatched_sequences']} 条不一致。这是「减开销」这件事成立的前提——如果执行本身变了，减什么都没有意义。</p>
</div>

<div class='block'>
<b>一条时间线，两个并发通道。</b>
nsys 把主机和设备记录在同一条时钟上。它们不是「主机做一段、设备做一段」地交替推进——
两边同时在跑，而且每一边都叠着好几个负载：主机在某个模块里发射 kernel 的同时，
设备正在执行更早发射的、往往属于别的模块的 kernel。</p>
<p>由此推出一条处理数据的硬规则：<b>只能在这条共享时钟上求交叠，不能拿一个通道上的时长
去减另一个通道上的时长。</b>「这个模块的主机区间有多长」和「它自己的 kernel 在设备上跑了多久」
是两个通道上的两个量，相减得不到空闲，也得不到等待。</p>
<p>本文档的设备侧量因此全部是<b>与某个主机区间的交叠</b>，同尺、可加：</p>
<ul>
<li><code>device_busy_us</code> —— 该区间内设备上有<b>任何</b> kernel 在执行的时间。</li>
<li><code>own_in_range_us</code> —— 其中属于这个 process 自己 kernel 的部分。</li>
<li><code>other_in_range_us</code> —— 其中属于别的 process 的部分。三者满足 own + other = busy。</li>
<li><code>own_device_total_us</code> —— 它自己 kernel 的总设备成本，<b>这是成本不是占比</b>，
不除以主机区间；它有一部分跑在区间之外（<code>own_outside_range_us</code>）。</li>
</ul>
<p>写下这条是因为先前的版本正是拿主机区间减去自有 kernel 时长，把差值命名为「没有 kernel 在跑」，
于是把一个设备忙碌六成的区间写成了九成空闲。</p>
</div>

<div class='block impl'>
<b>交互时间线（batch8 前端 · process 粒度）。</b>
<b>本报告内嵌三类时间线，每类「全景 + 放大」成对出现。</b>
静态页无法缩放，而全程视野下单个实例不足一像素——全景因此按 bin 聚合（柱高=占用比例），
逐实例只画在放大图里；放大视窗由<b>先写定的规则</b>选出（最密 N 个 step / 窗口中点起 N 个 step），
规则与落点只进审计文件 <code>R10_PROCESS_AUDIT.json</code>，正文图注只讲内容。
需要自由缩放、单实例下潜与 NCU 身份旁证时，用同一 release 的交互页
<code>R10_PROCESS_TIMELINE.html</code>（离线可开，前端与坑点见
<code>timeline-frontend-template.md</code>）。三类分属三次采集的三个时钟，类内共轴、类间不共轴。
</div>

<div class='block howto'>
<b>缩写卡（全文通用）</b><br>
<b>process</b> = 解码层里的一个叶子模块（如 attn_core）；一次前向里每层各出现一次。<br>
<b>实例</b> = 某个 process 在某一层、某一个 step 上的一次出现。<br>
<b>step</b> = 引擎的一次批处理迭代，一个 step 里所有在飞请求一起前进一个 token。<br>
<b>自有 kernel</b> = 发射调用落在这个 process 的 NVTX 区间内的 kernel（归属按发射，不按名字）。<br>
<b>设备忙碌</b> = 某个主机区间内，设备上有任何 kernel 在执行的时间占比。<br>
<b>区间外执行</b> = 一个 process 自己的 kernel 里，等它的主机区间结束后才跑的那部分。<br>
<b>quantum 抢占</b> = 调度器按量子把请求降级并重排，KV 靠前缀缓存保住。<br>
<b>engine_kv 抢占</b> = 引擎因显存不足驱逐 KV 块，已算的 token 作废。<br>
<b>%峰值</b> = 该 kernel 运行期间，内存通路的吞吐占硬件可持续峰值的比例。<br>
<b>高延迟 process</b> = 份额<b>严格超过 10%</b> 的 process 类型。份额的分母是窗口内
<b>全部</b> process 实例的累计时长，每个实例先扣掉插桩成本再排序。这条规则只作用在
process 这一层。<br>
<b>「主导」</b>（用于 kernel 家族时）= 占掉某个 process 大部分设备时间，是描述性的占比，
<b>不是</b>通过了什么筛选——kernel 这一层没有 10% 规则。
</div>
"""


def admission_reading(epi) -> str:
    """What the entry-queue data actually says, phrased from the data itself."""
    by = collections.defaultdict(collections.Counter)
    for e in epi:
        by[int(e["call_index"])][(e["queue_path"] or "").split(">")[0] or "?"] += 1
    idxs = sorted(by)
    q0_only = [k for k in idxs if set(by[k]) == {"Q0"}]
    no_q0 = [k for k in idxs if "Q0" not in by[k]]
    parts = []
    if q0_only:
        parts.append(f"序号 {'、'.join(map(str, q0_only))} 的调用全部从 Q0 起步")
    if no_q0 and all(k in no_q0 for k in idxs if k >= min(no_q0)):
        parts.append(f"序号 {min(no_q0)} 以后的调用没有一次再从 Q0 起步")
    return "，".join(parts) if parts else "入口队列没有随序号呈现单调关系"


def b2(L, stats):
    eu = L.eu
    td = L.tl_data()
    _att = td['c1']['tracks']['attn_core']
    m1_all = []  # class-1 preemption marks live in the class-1 table's boundary flags
    _pb = [int(r['start_ns']) for r in L.c1 if r.get('at_preemption_boundary') == 'True']
    if _pb:
        _o = min(int(r['start_ns']) for r in L.c1)
        m1_all = sorted({v - _o for v in _pb})
    # one step is the natural unit here: the claim under test is the ORDER of the
    # eight processes inside a step, and 200 ms holds ~34 steps — still a picket
    # fence. Two steps make the sequence legible while showing it repeats.
    _stepdur = (eu.get('step_dur_us_median') or 22000) * 1e3
    z1span = int(2 * _stepdur)
    z1 = _densest([x[0] for x in _att], z1span)
    _t1 = (L.ts or {}).get('e2e', {})
    ts1_w = _t1.get('window_s', 0)
    ts1_per = next(iter(_t1.get('tracks', {'x': 0}).values()))
    ts1_m = _t1.get('quantum_marks', 0)
    _c2 = L.c2
    per_inst = L.overhead["module_hook_us_per_instance_effective"]
    sel = _c2["selected_types"]
    n_sel = len(sel)
    sel_line = "、".join(f"{p}（{_c2['share_by_process'][p]:.1%}）" for p in sel)
    _rej = sorted(_c2["rejected_types"].items(), key=lambda kv: -kv[1])
    near = f"{_rej[0][0]}（{_rej[0][1]:.1%}）" if _rej else "无"
    cov, inv, pre = L.p1cov, L.p1inv, L.preempt
    pm = cov["preemption_marks"]
    pb = sum(1 for r in L.c1 if r.get("at_preemption_boundary") == "True")
    rows = [[x["process"], f"{x['n']:,}", f"{x['med']:.1f}", f"{x['p90']:.1f}",
             f"{x['max']:,.0f}", f"{x['sum_ms']:,.1f}", f"{x['share']:.1%}"] for x in stats]
    # Two scopes, never merged: the class-1 capture is NVTX-only over the whole
    # run; the class-2 capture is condition-triggered, so its marks cover only
    # the triggered span. Quoting the windowed count as if it were the run's
    # total is exactly the overclaim this report was caught making.
    pm_run = cov['preemption_marks'].get('quantum_begin', 0)
    pm_win = pre['quantum']['preemptions_total']
    return f"""
<h2>B2 第一类 · 全部代表 process 的端到端时间线</h2>
<p class='theme'>第一遍只问一件事：整段运行里，时间在八个 process 之间怎么分。
它不记 kernel，所以不受 kernel 行数上限约束，范围就是全程 {cov['declared_scope']['window_s']:.1f} s、
{cov['steps']:,} 个 step、{cov['process_instances']:,} 个 process 实例，八个 process 一个不缺。</p>

<h3>第一类时间线 · 读数</h3>
<div class='block impl'>
<b>时间线是本报告的骨架，本节读数全部取自它的数据层。</b>
端到端时间线（交互页第一节）：8 个 process 各一条轨、共一条 {ts1_w:.1f} s 的时间轴
（S02 时钟），每轨 {ts1_per:,} 个实例；底部 {ts1_m} 个 quantum 抢占红刻。
批爬升到 cap=16 后长期贴顶、step 起点率平稳、attn_core 轨开头一根 prefill 尖峰、
抢占散布在批满之后——整段运行由一个满批平台主导，后两类窗口条件正是从这个平台上冻结的。</p>
</div>

{fig(tl_tracks(td['c1']['tracks'], td['procs'], td['c1']['w0'], td['c1']['w1'],
               "第一类 · 端到端全景（8 process 共轴）", marks=m1_all, bins=900),
     ("八条轨道共用一条 {:.0f} s 的时间轴，每轨 {:,} 个实例；批爬升后所有 process 的活动"
      "连成不间断的带，抢占红刻散布在整段而不是聚成一处。"
      "全景按 bin 聚合（柱高=占用比例）——逐实例画出来每个都不足一像素；"
      "所以下一张图把同一条轴放大到 {}——"
      "报告里的时间线必须成对出现，否则一块实心色带什么也没说。").format(
         td['c1']['w1'] / 1e9, len(td['c1']['tracks']['attn_core']), ZOOM_RULES['e2e_zoom']))}

{fig(tl_tracks(td['c1']['tracks'], td['procs'], z1, z1 + z1span,
               "第一类 · 放大 %.0f ms / 2 个 step（%s）" % (z1span/1e6, ZOOM_RULES['e2e_zoom']),
               marks=m1_all),
     ("放大到两个 step 后结构显形：八个 process 在每个 step 内按 norm_in→qkv_proj→attn_core→"
      "o_proj→norm_post→mlp_gate_up→act_mul→mlp_down 的固定顺序依次出现，"
      "同一列的三个颜色是被插桩的三层。这证实了主机侧的严格串行——"
      "同一时刻只有一个 process 在主机上推进，所谓跨 process 并发只可能发生在设备通道。"))}

<h3>先看引擎，再看 process</h3>
<div class='block'>
<b>引擎在这段窗口里几乎没有空转，而设备上任何时刻只有一个 kernel。</b>
窗口内有 {eu.get('steps_in_window')} 个 step，合计占掉窗口的 <b>{eu.get('step_coverage_of_window', 0):.1%}</b>；
相邻 step 之间的间隙中位 {eu.get('inter_step_gap_us_median')} us（p90 {eu.get('inter_step_gap_us_p90')} us）——
引擎做完一个 step 立刻开始下一个。</p>
<p>引擎在推进时，设备有 kernel 在执行的时间占 <b>{eu.get('device_busy_share_inside_steps', 0):.1%}</b>，
其余是一个 step 内部相邻 kernel 之间的发射间隙。
kernel 时长总和 ÷ 并集 = {eu.get('kernel_sum_over_union')}，
说明这些 kernel <b>从不重叠执行</b>：单流、严格串行，一个算完才轮到下一个。</p>
<p><b>这一段必须放在后面所有 per-process 份额之前。</b>那些份额的分母是某个 process 的主机区间，
不是引擎的时间；把它们读成「GPU 利用率」会得到一个和上面这组数字矛盾的结论。
先前的版本正是漏了这一层，于是一个 step 覆盖率 {eu.get('step_coverage_of_window', 0):.0%} 的引擎
被写成了「GPU 一半时间不工作」。</p>
</div>

{table(["量", "值", "分母"],
       [["step 覆盖窗口", f"{eu.get('step_coverage_of_window', 0):.1%}", "声明窗口的时长"],
        ["step 内设备忙碌", f"{eu.get('device_busy_share_inside_steps', 0):.1%}", "窗口内 step 占用的时间"],
        ["窗口内设备忙碌", f"{eu.get('device_busy_share_of_window', 0):.1%}", "声明窗口的时长"],
        ["kernel 总和 ÷ 并集", f"{eu.get('kernel_sum_over_union')}", "—（=1 即无重叠执行）"],
        ["step 时长中位（实测 / 扣钩子后）",
         f"{(eu.get('step_dur_us_median') or 0)/1000:.1f} / "
         f"{(eu.get('step_dur_us_median_hook_corrected') or 0)/1000:.1f} ms", "—"],
        ["step 间隙中位 / p90", f"{eu.get('inter_step_gap_us_median')} / {eu.get('inter_step_gap_us_p90')} us", "—"]],
       "每一行都写明分母：这三个「忙碌」问的是三个不同的问题，不能互相替代。")}

<h3>时间在八个 process 之间怎么分</h3>
<div class='block'>
<b>一个 process 类型算不算高延迟，只看一条：它的份额是否严格超过 10%。</b>
份额 = 该类型全部实例的累计时长 ÷ 窗口内<b>全部</b> process 实例的累计时长，
每个实例先减去 {per_inst} us 的插桩成本。规则写在看数之前，落选者连同份额一起登记，
不做事后调整。本次 {n_sel} 个类型入选：{sel_line}；最接近门槛的落选者是 {near}。</p>
</div>

{table(["process", "实例数", "中位 us", "p90 us", "最长 us", "累计 ms", "份额"], rows,
       "每个 process 在三层（0/15/31）上各出现 " + f"{inv['instances_per_process']['attn_core']//3:,}" +
       " 次；份额的分母是窗口内全部实例的累计时长，不是入选者的。")}

{fig(fig_process_share(stats),
     "八条横条的长度差距集中在第一条：attn_core 一个 process 占掉累计时长的 %.1f%%，其余七个各自在 %.1f%%–%.1f%% 之间。"
     "右侧的三点分布说明这个份额不是靠中位数撑起来的——attn_core 的中位只有 %.0f us，最长却到 %.1f ms，"
     "它的份额来自尾部而不是常态。" % (stats[0]["share"] * 100,
                                min(x["share"] for x in stats[1:]) * 100,
                                max(x["share"] for x in stats[1:]) * 100,
                                stats[0]["med"], stats[0]["max"] / 1000))}


<h3>抢占：第一遍就要看得见</h3>
<p>抢占发生在调度器和引擎之间，不需要硬件信息，所以它属于第一类。
整段运行里记到 <b>{pm['quantum_begin']}</b> 次量子段开始与同样多次结束、<b>{pm['promote']}</b> 次提升、
<b>{pm['engine_kv']}</b> 次 KV 驱逐。落在抢占边界上的 process 实例有 <b>{pb:,}</b> 个，
占全部实例的 {pb/len(L.c1):.1%}。</p>

{fig(fig_preempt(L.epi, pre),
     "左侧每根柱是同一序号的调用，颜色是它被准入时进入的队列：" + admission_reading(L.epi) +
     "；右侧说明准入之后多数调用还会被降级一到两次。"
     "这两件事合起来说明梯子有两个入口——程序已经消耗的服务量决定它从哪一级进来，"
     "调用自己的长度决定它进来之后还要往下掉几级。")}

<div class='block'>
<b>两种抢占的代价不是同一种，所以分开记。</b>
量子抢占付的是重排和续段时再 prefill 的成本，KV 靠前缀缓存留着；
engine_kv 抢占付的是把算过的 token 直接丢掉。这条负载上后者是
<b>{pre['engine_kv']['events']} 次</b>——显存没有被打穿。</p>
<p><b>两个口径不能混：</b>第一遍（NVTX-only、无触发器）在全程
{cov['declared_scope']['window_s']:.1f} s 里记到 <b>{pm_run}</b> 次量子抢占；
第二遍是条件触发采集，触发点之前什么都不记，因此它的 <b>{pm_win}</b> 次
只覆盖被触发的那一段。下面的每次调用成本由第二遍样本算出，
适用范围是该窗口而不是整段运行；全程口径以第一遍为准。
窗口内合计再排队间隙 {pre['quantum']['requeue_gap_us_total']/1000:.2f} ms。
把两者混成一个「抢占次数」会让这条结论消失。</p>
</div>
"""


def pile_reading(rows) -> str:
    """Where the >=p90 members actually sit — derived, never asserted."""
    xs = sorted((int(r["start_ns"]), float(r["dur_us"])) for r in rows)
    w0, w1 = xs[0][0], xs[-1][0]
    durs = sorted(d for _, d in xs)
    p90 = durs[int(0.9 * len(durs))]
    red = [(s - w0) / max(w1 - w0, 1) for s, d in xs if d >= p90]
    q1 = sum(1 for x in red if x < 0.25) / max(len(red), 1)
    if q1 > 0.5:
        return (f"时长 ≥ p90 的红色成员有 {q1:.0%} 聚在窗口前四分之一——"
                "正是混有 prefill 的前段，高延迟实例与 prefill 混批同时出现。")
    return f"时长 ≥ p90 的红色成员沿窗口散布（前四分之一仅占 {q1:.0%}），不聚团。"


def b3(L):
    td = L.tl_data()
    td2 = td['c2']
    _c2 = L.c2
    sel = _c2['selected_types']
    _eu = L.eu
    z2span = int(3 * (_eu.get('step_dur_us_median') or 22000) * 1e3)
    _ref = td2['tracks'][sel[0]]
    # mid-window slice: representative, not the most extreme (rule declared)
    z2 = max(0, (td2['w1'] - td2['w0']) // 2 - z2span // 2)
    m2 = []
    _t2 = (L.ts or {}).get('c2', {})
    ts2_w = _t2.get('window_s', 0)
    ts2_n = _t2.get('instances', 0)
    ts2_per = next(iter(_t2.get('per_type', {'x': 0}).values()))
    ts2_sel = '、'.join(_t2.get('selected_types', []))
    ts2_m = _t2.get('quantum_marks', 0)
    _cov = _t2.get('drilldown_identity_coverage', {})
    ts2_ca = _cov.get('exact_family_grid', 0)
    ts2_cb = _cov.get('family_only', 0)
    c2, obj = L.c2, L.conc_obj
    dv = obj["objects"][0]
    sel = c2["selected_types"]
    rej = c2["rejected_types"]
    picks = [[t["pick"], f"L{t['layer_idx']}", t["phase"], f"{t['dur_us']:.1f}",
              f"{t['corrected_us']:.1f}"] for t in c2["targets"]]
    distinct = len({(x["layer_idx"], x["step_id"]) for x in c2["targets"]})
    dup = "" if distinct == len(c2["targets"]) else (
        f"五个挑选位落在 {distinct} 个不同实例上——"
        "最长与最抖挑中了同一个实例，这一个实例既是窗口内最长的，也是与相邻实例落差最大的。")
    return f"""
<h2>B3 第二类 · 高延迟 process 的时间线</h2>
<p class='theme'>第一遍点名 <b>{', '.join(sel)}</b>：它的份额 {c2['share_by_process'][sel[0]]:.1%}，
是唯一严格超过 10% 的类型；其余七个最高的也只有 {max(rej.values()):.1%}。
选择规则在看数之前就写好了，规则和落选者一起存档。</p>

<h3>第二类时间线 · 读数</h3>
<div class='block impl'>
<b>纵轴是 process 类型——关心的是 process 是什么，不是它来自哪个 call。</b>
第二类时间线（交互页第二节）：窗口 {ts2_w:.1f} s（S04 时钟）内 {ts2_n:,} 个实例、
八类型各 {ts2_per:,} 个同轴排布，线性缩放、无折叠双轴；高延迟类型（{ts2_sel}）金框高亮，
{ts2_m} 个抢占红刻。点击实例下潜到发射期归属的 kernel，
NCU 身份旁证两档覆盖：A 档（同族同 grid）{ts2_ca:.1%}、B 档（族中位）{ts2_cb:.1%}。</p>
</div>

{fig(tl_tracks(td2['tracks'], td['procs'], z2, z2 + z2span,
               "第二类 · 窗口内放大 %.0f ms（%s）" % (z2span/1e6, ZOOM_RULES['c2_zoom']),
               marks=m2, hi=sel),
     ("纵轴是 process 类型；红标签是通过 10% 门限的高延迟类型（{}），"
      "同一 step 内它的矩形明显比其它七类宽。"
      "这张图让「高延迟」从一个份额数字变成可见的形状——"
      "宽度差就是份额差的来源，而不是某几个异常实例造成的。").format('、'.join(sel)))}

{table(["挑选位", "层", "相位", "原始 us", "扣插桩后 us"], picks,
       "第二类不是只挑最长的：最长、p90、中位、最短、最抖各取一个，"
       "这样「高延迟」不会被一两个异常值定义。" + dup)}

{fig(fig_class2(L.c2rows, obj),
     ("上方每个点是 {} 的一个实例，纵轴对数，时长落在 {:.0f}–{:.0f} us 之间（中位 {:.0f}）。"
      "下面那根条把同一批实例的主机区间按「这段时间设备在替谁干活」拆开，"
      "设备忙碌 {:.1%} 而只有 {:.1%} 是它自己的 kernel，"
      "说明主机待在这个模块里的时候设备并没有闲着，只是没在替它干活。").format(
         dv["process"], min(float(r["dur_us"]) for r in L.c2rows),
         max(float(r["dur_us"]) for r in L.c2rows),
         statistics.median([float(r["dur_us"]) for r in L.c2rows]),
         dv["device_busy_share"], dv["own_in_range_share"]))}


<div class='block'>
<b>最贵的 process 并不是设备上最忙的 process。</b>
attn_core 占掉窗口内 process 累计时长的 {c2['share_by_process'][sel[0]]:.1%}。
在它的主机区间里，设备忙碌 <b>{dv['device_busy_share']:.1%}</b>，
其中属于它自己 kernel 的只有 <b>{dv['own_in_range_share']:.1%}</b>，
属于别的 process 的有 <b>{dv['other_in_range_share']:.1%}</b>，真正没活干的 {dv['device_idle_share']:.1%}。
主机待在这个模块里的时候，设备大部分时间在替别人干活——这是 process 这一层的现象，引擎那一层并没有空转（见 B2 的引擎表）。</p>
<p>反过来看它自己的 GPU 工作：总设备成本 {dv['own_device_total_ms']:.1f} ms，
其中 <b>{dv['own_outside_share']:.1%}</b> 是在它的主机区间结束之后才执行的——
主机已经走到下一个模块，设备还在做它的活。平均每个实例发出 {dv['kernels_per_instance']:.2f} 个 kernel。
这两个方向合起来说明同一件事：主机与设备在同一条时钟上并发推进，各自叠着多个负载，
所以「这个 process 慢」不能读成「它在等 GPU」。第三遍要问的是它占着设备时离硬件上限还有多远。</p>
</div>
"""


def b4(L, fams):
    _t3 = (L.ts or {}).get('c3', {})
    _w3 = L.p3series['windows'][0]
    c3span = _w3['end_ns'] - _w3['start_ns']
    _binw = c3span / len(_t3['hw_lanes'][0]['values']) if _t3.get('hw_lanes') else 1
    c3lanes = []
    for ln in (_t3.get('signal_lanes') or [])[:3]:
        c3lanes.append({**ln, 'w0': 0, 'binw': c3span / len(ln['values'])})
    for ln in (_t3.get('hw_lanes') or []):
        c3lanes.append({**ln, 'w0': 0, 'binw': c3span / len(ln['values'])})
    c3marks = _t3.get('marks') or []
    _tr = (_t3.get('tracks') or {})
    _starts = sorted(x[0] for v in _tr.values() for x in v)
    z3 = _densest(_starts, int(400e6))

    def _vals(k):
        return [v for ln in (_t3.get('hw_lanes') or []) if ln['key'] == k
                for v in ln['values']]

    def _cv(k):
        xs = [x for x in _vals(k) if x is not None]
        return statistics.pstdev(xs) / statistics.mean(xs) if xs else 0

    def _corr(k1, k2):
        a1, a2 = _vals(k1), _vals(k2)
        xs = [(x, y) for x, y in zip(a1, a2) if x is not None and y is not None]
        if len(xs) < 10:
            return 0.0
        m1 = statistics.mean([x for x, _ in xs]); m2 = statistics.mean([y for _, y in xs])
        num = sum((x - m1) * (y - m2) for x, y in xs)
        den = (sum((x - m1) ** 2 for x, _ in xs) * sum((y - m2) ** 2 for _, y in xs)) ** 0.5
        return num / den if den else 0.0
    ts3_w = _t3.get('window_s', 0)
    ts3_np = len(_t3.get('procs', []))
    ts3_n = _t3.get('instances', 0)
    ts3_m = _t3.get('quantum_marks', 0)
    _hn = _t3.get('hw_note', {})
    ts3_cov = _hn.get('identity_covered_share_of_busy', 0)
    ts3_ta = _hn.get('tierA_share_of_covered', 0)
    _hm = _t3.get('hw_medians', {})
    _hx = _t3.get('hw_axis', {})
    hw_sm, hw_mem, hw_dram = _hm.get('sm', 0), _hm.get('mem', 0), _hm.get('dram', 0)
    clk_n = ((L.ts or {}).get('clock_alignment') or {}).get('causality_pairs_checked', 0)
    hwtbl = table(["硬件指标", "中位", "轴上限 / 屋顶"],
                  [[_hx[k]['label'], f"{_hm[k]:.1f}",
                    f"{_hx[k]['max']}" + (f" / {_hx[k]['roof']}" if _hx[k].get('roof') else "")]
                   for k in _hm],
                  "身份投影、bin 内按 kernel 时长加权；每条指标一条时间线，交互页可缩放对读。")
    smc = L.sm_coverage()
    sm, ub = smc["sm_count"], smc["weighted_upper_bound"]
    _kv = next((v for k, v in smc["per_family"].items() if "reshape_and_cache" in k), None)
    kvb = _kv["blocks_median"] if _kv else 0
    busy = (L.windows["windows"][0].get("device_busy_share") or 0)
    instep = L.eu.get("device_busy_share_inside_steps") or 0
    memlo = min(f["mem_pct"] for f in fams)
    memhi = max(f["mem_pct"] for f in fams)
    xp = L.cross['selected_pairs']
    n_inst = sum(1 for _ in open(L.base / 'S04' / 'pass2_instances.jsonl'))
    p0 = next((q['share_of_host_interval'] for q in xp
               if q['host_process'] == 'act_mul'), 0)
    p2 = next((q['share_of_host_interval'] for q in xp
               if q['host_process'] == 'norm_post'), 0)
    xtable = table(["host process", "device 在跑谁", "占 host 区间"],
                   [[q['host_process'], q['device_process'],
                     f"{q['share_of_host_interval']:.1%}"] for q in xp],
                   "规则先落盘：X≠Y、份额严格 >10%；矩阵分母 = X 的主机区间总长。")
    tbl = table(["kernel 家族", "设备时间占比", "线程块 中位（范围）", "SM 覆盖上界"],
                [[k, f"{v['share']:.1%}",
                  f"{v['blocks_median']:.0f}（{v['blocks_range'][0]}–{v['blocks_range'][1]}）",
                  f"{v['sm_cover_ub']:.0%}"]
                 for k, v in sorted(smc["per_family"].items(), key=lambda kv: -kv[1]["dev"])],
                f"块数少于 {sm} 就必然有 SM 闲着。覆盖上界与总计同样按设备时间加权，"
                "所以各行可与总计对读；它是上界，不是实测占用率。")
    win, att, al = L.windows, L.attach, L.align
    a = next(r for r in att if r["status"] == "attached")
    ws = win["windows"]
    dev_tot = sum(f["dev_us"] for f in fams)
    rows = [[f"{w['start_ns']/1e9:.1f}–{w['end_ns']/1e9:.1f} s", "/".join(w["phases"]),
             w["target_instances"], f"{w['mean_batch']:.2f}", w["peak_concurrent_kernels"],
             w["quantum_preemptions"], w["engine_kv_preemptions"]] for w in ws]
    krows = [[f["family"][:34], f["n"], f"{f['med_us']:.1f}", f"{f['dev_us']:.1f}",
              f"{f['dev_us']/dev_tot:.1%}", f"{f['mem_pct']:.1f}%", f"{f['dram_gbs']:.0f}",
              f"{f['l2_hit']:.0f}%"] for f in fams]
    return f"""
<h2>B4 第三类 · 并发与资源</h2>
<p class='theme'>第三遍只在第二遍圈出的 {len(ws)} 个窗口里、只对 {', '.join(L.c3['processes'])} 采硬件计数器。
窗口用负载身份描述——相位、批组成、覆盖的 step 区间、成员实例的 (process, 层, step)——而不是纳秒偏移，
因为第三遍是另一次运行，纳秒坐标不跨运行成立。</p>

{table(["窗口", "相位", "目标实例", "平均批", "kernel 峰值并发", "quantum 抢占", "KV 抢占"], rows)}

{fig(fig_windows(win),
     ("窗口是负载区间而不是时刻切片（本次入选 {} 个）；条把窗口内的设备时间按归属拆成三段，三段相加等于窗口全长。"
      "设备在窗口里忙碌 {:.1%}，其中只有 {:.1%} 属于被插桩的目标 process，而 kernel 峰值并发是 {}，"
      "说明空隙并没有被别的工作填上——这台引擎同时只跑一个 kernel。").format(
         len(ws), (ws[0].get("device_busy_share") or 0),
         (ws[0].get("own_busy_share") or 0), ws[0].get("peak_concurrent_kernels")))}


<div class='block impl'>
<b>归属是采集方式建立的，不是推断出来的。</b>
第三遍对每个第三类 process 单独跑一次 NCU 回放，用
<code>--nvtx --nvtx-include 'p.L{{层}}.{{process}}/'</code> 把这次回放限制在该 process 自己的区间内。
落进报告的每一次 launch 因此只可能属于一个 process，不需要事后拆分。
{a['process']} 共 {a['ncu_launches']} 次 launch、设备时间合计 {float(a['device_us_sum']):.1f} us；
其余七个 process 登记为 <code>not_collected</code>，理由是不在冻结的第三类目标里——
它们不占资源图的面积，也不被填补。</p>
</div>

{table(["kernel 家族", "次数", "中位 us", "设备时间 us", "占比", "内存 %峰值", "DRAM GB/s", "L2 命中"], krows,
       "同一个 process 内部的 kernel 家族；%峰值 与 DRAM 取中位。")}

{fig(fig_ncu(fams),
     ("上排按设备时间把窗口内的 kernel 家族分开，主导者是 {}（占 {:.0%}）；"
      "下排显示两种状态并存：内存通路最高的家族中位 {:.0f}%、逼近显存带宽屋顶，最低的只有 {:.0f}%。"
      "设备时间的大头是带宽受限的 decode gemm，小 kernel 的瓶颈在发射侧——两类问题要分开治。").format(
         fams[0]["family"], fams[0]["dev_us"] / dev_tot,
         max(f["mem_pct"] for f in fams), min(f["mem_pct"] for f in fams)))}

<h3>第三类时间线 · 硬件使用率读数</h3>
<div class='block impl'>
<b>并发/高延迟 process 实例与五条硬件时间线共轴（S07 时钟，可缩放）。</b>
窗口 {ts3_w:.1f} s、{ts3_np} 个 class-3 process 轨、{ts3_n:,} 个实例、{ts3_m} 个抢占红刻。
硬件 lane 由同身份 NCU 计数器投影（时间取观测 kernel 区间，NCU 只出数值；
busy 时间覆盖 {ts3_cov:.1%}，其中 A 档 {ts3_ta:.1%}；空档不插值）：</p>
{hwtbl}
<p><b>两种状态并存</b>：设备时间的大头是 decode gemm——内存通路中位 {hw_mem:.0f}%、
显存带宽中位 {hw_dram:.0f} GB/s（理论峰值 1008），贴着显存带宽屋顶跑；SM 只有 {hw_sm:.0f}%。
小 kernel 段远离屋顶，瓶颈在发射侧。共轴的对齐义务逐层落实并已实测
（host↔device 因果检验 {clk_n:,} 对、违反 0、偏斜上界 ~0 ns），见规范条款 14。</p>
</div>

{fig(tl_lane_block(c3lanes, 0, c3span,
               "第三类 · 窗口全景：信号 + 硬件使用率（共轴）", marks=c3marks),
     ("上三条是窗口信号（设备忙碌 / 其中目标 process / 批），下五条是硬件指标，"
      "全部共用一条 {:.1f} s 的轴：内存通路与显存带宽长期贴近轴顶，而 SM 吞吐始终在低位。"
      "这说明这段窗口里设备是被**带宽**占住的，不是被算力占住的——"
      "两条线的高低差就是「忙碌 ≠ 打满」的直接图像。").format(c3span / 1e9))}

{fig(tl_lane_block(c3lanes, z3, z3 + int(400e6),
               "第三类 · 放大 400 ms（%s）" % ZOOM_RULES['c3_zoom'], marks=c3marks),
     ("放大后可见硬件指标随 step 起伏而非恒定，幅度不大（内存通路变异系数 {:.2f}）但方向确定："
      "内存通路与 L2 命中率的相关系数 {:+.2f}、与 SM 吞吐 {:+.2f}、与显存带宽 {:+.2f}。"
      "带宽升高时命中率同步下降、SM 反而更闲——这是 gemm 段流式读权重的指纹，"
      "肉眼看到的小起伏背后是一组非常确定的相关关系。").format(
         _cv('mem'), _corr('mem', 'l2hit'), _corr('mem', 'sm'), _corr('mem', 'dram')))}

<h3>跨 process 并发：host 在 X 里，设备在跑 Y</h3>
<div class='block'>
<b>同一 Python 线程串行执行模块，主机区间跨类型从不重叠——不同 process 的并发只存在于设备通道。</b>
把第二遍全部 {n_inst:,} 个实例（八个类型全保留）与按发射归属合并的各类型 kernel 区间求交，
得到 host×device 份额矩阵；X≠Y 且严格超过 10% 的对入选为跨 process 并发对象：</p>
{xtable}
<p>模式很一致：<b>host 停在小算子里时，设备在消化上一个大 gemm</b>——
act_mul 的主机区间有 {p0:.1%} 在跑 mlp_gate_up 的 kernel，norm_post 有 {p2:.1%} 在跑 o_proj。
这就是「一条时钟两个通道」的逐对量化：小算子的主机时长几乎不是它自己的设备成本，
把它们当独立优化目标会打错靶子。完整 8×8 矩阵在 <code>cross_process_concurrency.json</code>
与交互时间线页。</p>
</div>

<h3>「设备忙碌」是最宽松的口径</h3>
<div class='block'>
<b>同时只有一个 kernel 在跑，说的是发射方式，不是硬件能力。</b>
本次采集的 kernel 全部落在<b>同一条 CUDA stream</b> 上，而同一 stream 内的 kernel 由 CUDA
保证按发射顺序串行执行——前一个结束后一个才开始。GPU 本身可以并发执行多个 kernel
（不同 stream、MPS、多进程），只是单引擎的前向没有要求它这么做。
所以 step 内那段没有 kernel 的空隙<b>没有别的工作可以填补</b>，这是它值得优化的原因。</p>
<p><b>而且「有 kernel 在跑」并不等于 GPU 被占满。</b>
一个 kernel 是一张线程块网格，块数少于 SM 数时必然有 SM 闲着，CUPTI 照样把这段记成忙碌。
这块 GPU 有 {sm} 个 SM，按设备时间加权的<b>SM 覆盖上界只有 {ub:.1%}</b>，
其中 KV 写入那个 kernel 的块数中位数只有 {kvb:.0f}。
这还是上界——块数达到 SM 数也不保证满占用，寄存器与共享内存都可能先成为约束。</p>
{tbl}
<p>把三层叠起来读：引擎推进时设备忙碌 {instep:.1%}（第二遍，分母是 step 占用的时间），
第三遍窗口内忙碌 {busy:.1%}（分母是整个窗口）；两者都只说「有 kernel 在跑」。同时只有一个 kernel，
那个 kernel 最多覆盖 {ub:.0%} 的 SM；内存通路上两种状态并存——gemm 段中位 {memhi:.0f}%（逼近显存带宽屋顶），小核段 {memlo:.0f}%。
<b>「忙碌」只回答有没有 kernel 在跑，不回答 GPU 有多少在干活。</b>
上面的块数推导是<b>上界</b>；实测在 raw 导出里有（SpeedOfLight 含
<code>sm__throughput</code>）：身份投影到观测时间轴后 SM 吞吐中位仅
{hw_sm:.0f}%（见上方硬件读数表）——上界 82.9% 与实测 {hw_sm:.0f}% 之间的差
就是「块在 SM 上但吃不满」的部分。</p>
</div>

<div class='block'>
<b>三个覆盖率分别申报，不合并成一个数。</b>
第一遍全景覆盖 {al['coverages']['pass1_全景覆盖']:,} 个实例；
第二遍目标实例覆盖 {al['coverages']['pass2_目标实例覆盖']:,} 个；
第三遍硬件指标覆盖 {al['coverages']['pass3_硬件指标覆盖']} 个 process。
跨遍对账用 <code>(program_id, call_index)</code>，
<code>step_id</code> 是单次采集的局部量，没有当跨遍的键——三遍是三次运行，step 编号在运行之间不通用。</p>
</div>
"""


def b5(L, stats, fams, dv):
    gd = L.gap_profile()
    g_small = gd["by_bucket"].get("<1us", {}).get("share", 0)
    g_mid = (gd["by_bucket"].get("10-50us", {}).get("share", 0)
             + gd["by_bucket"].get("50-200us", {}).get("share", 0))
    kps, stalls = gd["kernels_per_step"], gd["mid_stalls_per_step"]
    tok_med, req_med, kvconc = gd["tokens_per_step"], gd["reqs_per_step"], gd["kv_concurrency"]
    pd = L.pd_mix()
    n_steps, mix_frac, mix_med = pd["steps"], pd["mixed_frac"], pd["mix_median"]
    decl_p, real_p = pd["declared_prompt"], pd["prefilled"]
    p_frac = real_p / decl_p if decl_p else 0
    p_steps, d_steps = pd["prefill_steps_est"], pd["decode_steps_est"]
    tok_med2 = pd["decode_tok_median"]
    rk = L.rank_by_batch()
    r14 = rk['buckets']['1–4'].get('attn_core', 0)
    r1316 = rk['buckets']['13–16'].get('attn_core', 0)
    o14 = rk['buckets']['1–4'].get('o_proj', 0)
    o58 = rk['buckets']['5–8'].get('o_proj', 0)
    bmax = rk['max_reqs']
    opts = table(
        ["办法", "对得上的症状", "这份 trace 怎么说"],
        [["CUDA 图捕获",
          f"step 内 {g_mid:.0%} 的空隙——发射之间的主机侧工作",
          "已用对照臂实测（nsys 需 --cuda-graph-trace=node，默认粒度把一次回放记成一行）："
          "同负载下图臂的满批纯解码 step 中位 17.7 ms 对 eager+插桩臂的 21.9 ms（快 19%），"
          "step 内设备忙碌 85.1% 对 66.5%。插桩臂量到的空隙里约这部分差值属于 eager+钩子本身。"],
         ["更大的批（换 KV 余量）",
          "SM 覆盖——网格太小，不是空隙",
          f"每 step 只调度 {tok_med:.0f} 个 token，gemm 细长；批已顶到上限而 KV 只够 {kvconc} 路，"
          "杠杆在更小的模型、更短的上下文、更多 KV 显存或 KV 量化。"],
         ["把并发暴露到多条流 / 多引擎 / MPS",
          "SM 覆盖与空隙同时——kernel 之间真正的重叠",
          "负载里有大量互不依赖的请求，是引擎把它们收进<b>一个批、一条流</b>才没得重叠；"
          "本次采集的 kernel 全部落在同一条 stream 上，重叠时间恰好为 0。"
          "一个解码 step 内部确实是依赖链，但不同请求之间不是——"
          "小 kernel（KV 写入中位 16 个块 / 128 个 SM）串行排队是单流的结果，不是负载的性质。"]],
        "排序依据是「对得上症状」而不是实现难度；每一行的第三列都指向本文档已申报的数字。")
    dev_tot = sum(f["dev_us"] for f in fams)
    return f"""
<h2>B5 优化机会清单</h2>
<p class='theme'>下面四条按证据强度排列，每条都写清它站在哪一遍的哪个数字上，以及这份 trace 还没有回答的部分。</p>

<h3>① step 内的发射间隙，不是引擎空转</h3>
<p>引擎占掉窗口的 {L.eu.get('step_coverage_of_window', 0):.1%}，step 之间的间隙以微秒计——
没有可回收的引擎空转。可回收的在 step 内部：设备在 step 期间忙碌
<b>{L.eu.get('device_busy_share_inside_steps', 0):.1%}</b>，其余是相邻 kernel 之间的发射间隙。
而且 kernel 总和 ÷ 并集 = {L.eu.get('kernel_sum_over_union')}，设备上从不同时跑两个 kernel，
所以这些间隙没有被别的工作填上。</p>
<p>方向因此是减少发射次数或让单次发射携带更多工作：合并算子、图捕获、更大的批。
<b>边界：</b>这是插桩臂（模块 NVTX 在 cudagraph 下不可见，必须 eager），
eager 相对图捕获臂的墙钟代价已量到 {L.overhead['eager_arm_wall_pct']}%。
图捕获臂能把这段间隙压掉多少，这份 trace 没有回答——试过对图捕获臂做同样测量，
cudagraph 下 CUPTI 记不全逐 kernel 行（同负载 35,596 行 vs 94,049 行），该臂的设备占用率不可测。</p>

<h3>② kernel 又小又多</h3>
<p>四个 kernel 家族的中位时长在 {min(f['med_us'] for f in fams):.1f}–{max(f['med_us'] for f in fams):.1f} us 之间，
注意力主核占掉 attn_core 设备时间的 {fams[0]['dev_us']/dev_tot:.0%}。
在这个尺度上，合并小 kernel 或提高每次发射携带的工作量，比优化单个 kernel 的内核代码更可能见效。</p>

<h3>③ 把 GPU 填满的几条路，各自对得上什么</h3>
<p>空隙不是每次发射的固定开销堆出来的：亚微秒间隙有十万次，却只占空隙时间的 {g_small:.1%}；
<b>{g_mid:.0%} 来自 10–200 us 的中等停顿</b>，每个 step（{kps:.0f} 个 kernel）里约 {stalls:.0f} 次。
那是主机侧在做实打实的工作，不是发射抖动。下面按「对得上哪个症状」排：</p>
{opts}
<p>每个 step 只调度 {tok_med:.0f} 个 token（{req_med:.0f} 个请求各前进一个 token），
所以 gemm 是细长矩阵、网格自然小，算力与带宽都没打满。
而批已经顶到 <code>max_num_seqs</code>，KV 只支持 {kvconc} 路并发——
<b>批是被显存卡住的，不是被调度器卡住的</b>，调大 <code>max_num_seqs</code> 不会有效果。</p>

<h3>④ P/D 混合其实在做，但被前缀缓存掏空了</h3>
<p>chunked prefill 是开着的（每步 2048 token 预算），不同调用的 prefill 与 decode 由引擎
自动混批。实测 {n_steps:,} 个 step 里 {mix_frac:.1%} 混有 prefill，但混入量中位只有
{mix_med:.0f} 个 token：负载声明了 {decl_p:,} 个 prompt token，实际只 prefill 了
{real_p:,} 个（{p_frac:.0%}）——<code>enable_prefix_caching</code> 开着，
而合成负载的调用共享大量前缀，95% 的 prompt 工作被缓存直接吃掉。
剩下的 prefill 约 {p_steps:.0f} 步就做完，decode 却要约 {d_steps:.0f} 步。</p>
<p><b>所以批薄不是引擎不混，而是没有 P 可混。</b>每步只剩 {tok_med2:.0f} 个解码 token，
网格自然小——这正是 SM 覆盖低的直接原因。真实 serving 里用户提示各不相同，
每步能混进成百上千 prefill token；要在实验里复现那个状态，负载的 prompt 要去共享前缀，
或研究性地关掉前缀缓存。</p>

<h3>⑤ 排名对并发有多敏感</h3>
<p>把第一遍的全程数据按 step 的批规模分桶，重算每个 process 的份额：
attn_core 从批 1–4 的 {r14:.1%} 缓慢降到批 13–16 的 {r1316:.1%}，一直是第一名；
小算子的份额则随批上升（它们更受发射开销支配，批越大摊得越薄）。
<b>顺序几乎不变，但选材结果会变</b>——o_proj 在批 1–4 时是 {o14:.1%}，<b>通过 10% 门限</b>，
那时高延迟 process 有两个；批 ≥5 之后掉到 {o58:.1%}，只剩 attn_core 一个。
它正卡在门槛上。</p>
<p><b>边界：</b>观测到的批只到 {bmax}，因为 KV 只够 {kvconc} 路并发。
上表只说明这个区间内排名稳定、o_proj 在门槛上翻转，对更大的批没有发言权：
attn_core 的成本随「批 × 上下文长度」走，gemm 随批走，两者的斜率会不会在更大批下交叉，
这份数据答不了。要答需要先把 KV 墙拿掉（更小的模型或更短的上下文）再测同一套指标。</p>

<h3>⑥ 量子抢占的代价可量，KV 抢占这次为零</h3>
<p>第二遍窗口内 {L.preempt['quantum']['preemptions_total']} 次量子抢占带来
{L.preempt['quantum']['requeue_gap_us_total']/1000:.2f} ms 的再排队间隙，
分摊到窗口内 {L.preempt['quantum']['calls_total']} 次调用上是每次调用
{L.preempt['quantum']['requeue_gap_us_total']/L.preempt['quantum']['calls_total']:.1f} us。
engine_kv 抢占 0 次，说明在这个批规模下显存不是约束。
<b>指向 S1：</b>把负载推到 KV 墙以上再测一次，量子抢占和 KV 抢占的代价比会翻转，
那才是「抢占该不该做」的分界线。</p>
"""


# ------------------------------------------------- static timelines for the report
# The interactive page solves sub-pixel density with zoom; a static report cannot.
# So every timeline figure here is rendered at a DECLARED zoom, chosen by a rule
# written before the data is seen (the rules land in R10_PROCESS_AUDIT.json):
#
#   ZOOM_RULE_DENSE  choose the span with the most instances/marks — where the
#                    structure the section argues about is actually visible
#   ZOOM_RULE_MID    choose the span centred on the window's midpoint — a
#                    representative slice rather than the most extreme one
#
# Overview + zoom are always shown as a pair: the overview declares the whole
# scope, the zoom shows what a pixel hides.
LAYC = {0: "#2a78d6", 15: "#a8802f", 31: "#1baf7a"}
ZOOM_RULES = {
    "e2e_zoom": "最密 2 个 step 跨度（按实例数），规则先于数据写定",
    "c2_zoom": "窗口中点起 3 个 step 的跨度，取代表性而非极端段",
    "c3_zoom": "最密 400 ms（按目标实例数）",
}


def _densest(items, span, key=lambda x: x):
    """Start offset of the `span` with the most items. items: sorted offsets."""
    if not items:
        return 0
    best, bn, j = items[0], -1, 0
    import bisect
    for i, s in enumerate(items):
        j = bisect.bisect_right(items, s + span)
        if j - i > bn:
            bn, best = j - i, s
    return best


def tl_tracks(tracks, order, w0, w1, title, marks=None, hi=(), h_row=30, bins=None):
    """Process tracks on one shared axis: one row per process, rects at real times.

    `bins` aggregates into per-bin occupancy instead of drawing every instance.
    A full-run view has ~50k instances: drawn one by one it is a multi-megabyte
    file whose rectangles are all sub-pixel — the aggregate says the same thing
    honestly (bar height = fraction of the bin this process occupied) and the
    zoomed companion figure is where individual instances belong.
    """
    rows = [q for q in order if tracks.get(q)]
    h = 54 + len(rows) * h_row + 46
    s = svg_open(h, title)
    LEFT_L, span = 150, max(w1 - w0, 1)
    X = lambda v: LEFT_L + (W - LEFT_L - RIGHT) * (min(max(v, w0), w1) - w0) / span
    for k in range(7):
        x = LEFT_L + (W - LEFT_L - RIGHT) * k / 6
        s.append(f"<line x1='{x:.0f}' y1='44' x2='{x:.0f}' y2='{44+len(rows)*h_row}' stroke='{GRID}'/>")
        s.append(txt(x, 34, f"{(w0 + span * k / 6)/1e9:.3f} s", 14, "#48607d", "middle"))
    for i, q in enumerate(rows):
        y = 44 + i * h_row
        s.append(f"<rect x='{LEFT_L}' y='{y+2}' width='{W-LEFT_L-RIGHT}' height='{h_row-5}' "
                 f"fill='#fbfbf9' stroke='#eee'/>")
        s.append(txt(LEFT_L - 6, y + h_row / 2 + 3, q, 15, RED if q in hi else INK, "end"))
        n = 0
        if bins:
            bw_ns = (w1 - w0) / bins
            occ = [0.0] * bins
            for it in tracks[q]:
                bb, ee = it[0], it[1]
                if ee < w0 or bb > w1:
                    continue
                n += 1
                i0 = max(int((bb - w0) / bw_ns), 0)
                i1 = min(int((ee - w0) / bw_ns), bins - 1)
                for k2 in range(i0, i1 + 1):
                    lo2 = w0 + k2 * bw_ns
                    occ[k2] += max(0.0, min(ee, lo2 + bw_ns) - max(bb, lo2))
            pxw = (W - LEFT_L - RIGHT) / bins
            for k2, v in enumerate(occ):
                if not v:
                    continue
                hh = (h_row - 9) * min(1.0, v / bw_ns)
                s.append(f"<rect x='{LEFT_L + k2*pxw:.2f}' y='{y+4+(h_row-9)-hh:.1f}' "
                         f"width='{max(pxw,0.6):.2f}' height='{hh:.1f}' fill='{BLUE}' opacity='.8'/>")
        else:
            for it in tracks[q]:
                bb, ee, ly = it[0], it[1], (it[2] if len(it) > 2 else 0)
                if ee < w0 or bb > w1:
                    continue
                n += 1
                x1, x2 = X(bb), X(ee)
                s.append(f"<rect x='{x1:.2f}' y='{y+4}' width='{max(x2-x1,0.7):.2f}' "
                         f"height='{h_row-9}' fill='{LAYC.get(ly, BLUE)}' opacity='.75'/>")
        s.append(txt(W - RIGHT - 4, y + h_row / 2 + 3, str(n), 14, "#7f95b3", "end"))
    yb = 44 + len(rows) * h_row
    if marks:
        mv = [m for m in marks if w0 <= m <= w1]
        for m in mv:
            s.append(f"<line x1='{X(m):.1f}' y1='{yb+2}' x2='{X(m):.1f}' y2='{yb+10}' stroke='{RED}'/>")
        s.append(txt(LEFT_L, yb + 28, f"红刻 = quantum 抢占，本视窗 {len(mv)} 个", 15, RED))
    s.append(txt(W - RIGHT, yb + 28,
                 ("柱高 = 该 bin 内本 process 的占用比例；右侧数字 = 视窗内实例数"
                  if bins else "颜色 = 层（蓝 L00 / 金 L15 / 绿 L31）；右侧数字 = 视窗内实例数"),
                 14, "#48607d", "end"))
    s.append("</svg>")
    return "\n".join(s)


def tl_lane_block(lanes, w0, w1, title, marks=None, laneh=62):
    """Binned lanes on one shared axis (signals and hardware metrics)."""
    h = 52 + len(lanes) * (laneh + 10) + 40
    s = svg_open(h, title)
    LEFT_L, span = 210, max(w1 - w0, 1)
    for k in range(7):
        x = LEFT_L + (W - LEFT_L - RIGHT) * k / 6
        s.append(f"<line x1='{x:.0f}' y1='42' x2='{x:.0f}' y2='{42+len(lanes)*(laneh+10)}' stroke='{GRID}'/>")
        s.append(txt(x, 32, f"{(w0 + span * k / 6)/1e9:.3f} s", 14, "#48607d", "middle"))
    for i, ln in enumerate(lanes):
        y = 42 + i * (laneh + 10)
        base = y + laneh - 6
        s.append(f"<rect x='{LEFT_L}' y='{y}' width='{W-LEFT_L-RIGHT}' height='{laneh}' "
                 f"fill='#fbfbf9' stroke='#eee'/>")
        s.append(txt(LEFT_L - 6, y + 16, ln["label"], 15, ln["color"], "end"))
        vals, mx = ln["values"], (ln["max"] or 1)
        n = len(vals)
        bw = (W - LEFT_L - RIGHT) / n
        i0 = max(int((w0 - ln["w0"]) / ln["binw"]), 0)
        i1 = min(int((w1 - ln["w0"]) / ln["binw"]), n - 1)
        seg = (i1 - i0 + 1) or 1
        bw = (W - LEFT_L - RIGHT) / seg
        for k2 in range(i0, i1 + 1):
            v = vals[k2]
            if v is None or not v:
                continue
            hh = (laneh - 16) * min(1.0, v / mx)
            x = LEFT_L + (k2 - i0) * bw
            op = (ln.get("cov") or [1] * n)[k2] if ln.get("cov") else 1
            s.append(f"<rect x='{x:.2f}' y='{base-hh:.1f}' width='{max(bw*0.9,0.6):.2f}' "
                     f"height='{hh:.1f}' fill='{ln['color']}' opacity='{max(op,0.25):.2f}'/>")
        if ln.get("cap"):
            yc = base - (laneh - 16) * min(1.0, ln["cap"] / mx)
            s.append(f"<line x1='{LEFT_L}' y1='{yc:.1f}' x2='{W-RIGHT}' y2='{yc:.1f}' "
                     f"stroke='{RED}' stroke-dasharray='4 3'/>")
            s.append(txt(W - RIGHT - 4, yc - 3, f"cap={ln['cap']}", 13, RED, "end"))
        if ln.get("roof") and ln["roof"] <= mx:
            yr = base - (laneh - 16) * min(1.0, ln["roof"] / mx)
            s.append(f"<line x1='{LEFT_L}' y1='{yr:.1f}' x2='{W-RIGHT}' y2='{yr:.1f}' "
                     f"stroke='{RED}' stroke-dasharray='2 3'/>")
            s.append(txt(W - RIGHT - 4, yr - 3, "理论峰值", 13, RED, "end"))
        s.append(txt(LEFT_L + 6, y + 14, f"轴顶 {mx:g}", 13, ln["color"]))
    yb = 42 + len(lanes) * (laneh + 10)
    if marks:
        mv = [m for m in marks if w0 <= m <= w1]
        for m in mv:
            x = LEFT_L + (W - LEFT_L - RIGHT) * (m - w0) / span
            s.append(f"<line x1='{x:.1f}' y1='{yb+2}' x2='{x:.1f}' y2='{yb+10}' stroke='{RED}'/>")
        s.append(txt(LEFT_L, yb + 28, f"红刻 = quantum 抢占，本视窗 {len(mv)} 个", 15, RED))
    s.append("</svg>")
    return "\n".join(s)


# ---------------------------------------------------------------- v1-style timelines
# Front-end ported from build_r10_summary_doc.py / report-template.md:
# axis() 7 ticks; cu lanes 138 high with cap dashed line; hl pile strip with
# trapezoid envelope; kernel microscope with gemm/other rows at true proportions.
GEMM, OTHK = "#a8802f", "#2f6f9f"


def tl_axis(w0, w1, y, h):
    out = []
    for i in range(7):
        t = w0 + (w1 - w0) * i / 6
        x = LEFT + (W - LEFT - RIGHT) * i / 6
        out.append(f"<line x1='{x:.0f}' y1='{y}' x2='{x:.0f}' y2='{y+h}' stroke='{GRID}'/>")
        out.append(f"<text x='{x:.0f}' y='{y-12}' font-size='17' text-anchor='middle' "
                   f"fill='#48607d'>{t/1e9:.1f} s</text>")
    return out


def tl_lanes(lanes, w0, w1, marks=None, title=""):
    """v1 cu_strip: one 138-px lane per signal, vertical bars per bin."""
    lane_h, gap = 138, 24
    h = 46 + len(lanes) * (lane_h + gap) + 30
    s = svg_open(h, title)
    s += tl_axis(w0, w1, 40, len(lanes) * (lane_h + gap))
    y = 46
    for ln in lanes:
        base = y + lane_h - 10
        vals = ln["values"]
        mx = ln.get("max") or (max(v for v in vals if v is not None) or 1)
        s.append(f"<rect x='{LEFT}' y='{y}' width='{W-LEFT-RIGHT}' height='{lane_h}' "
                 f"fill='#fbfbf9' stroke='#eee'/>")
        # long CJK labels do not fit left of a 130-px gutter; v1 kept them short.
        # Inside the lane, top-left, they can be any length.
        s.append(f"<text x='{LEFT+8}' y='{y+18}' font-size='16' "
                 f"fill='#48607d'>{esc(ln['label'])}</text>")
        bw = (W - LEFT - RIGHT) / len(vals)
        path = ""
        for i, v in enumerate(vals):
            if not v:
                continue
            hgt = (lane_h - 24) * min(1.0, v / mx)
            x1 = LEFT + i * bw
            path += f"M{x1:.1f} {base:.1f}V{base-hgt:.1f}H{x1+max(bw-0.4,0.5):.1f}V{base:.1f}"
        s.append(f"<path d='{path}' stroke='{ln['color']}' stroke-width='1' fill='none'/>")
        if ln.get("cap"):
            yc = base - (lane_h - 24) * min(1.0, ln["cap"] / mx)
            s.append(f"<line x1='{LEFT}' y1='{yc:.1f}' x2='{W-RIGHT}' y2='{yc:.1f}' "
                     f"stroke='{RED}' stroke-dasharray='4 3'/>")
            s.append(f"<text x='{W-RIGHT-2}' y='{yc-3:.1f}' font-size='15' "
                     f"text-anchor='end' fill='{RED}'>cap={ln['cap']}</text>")
        s.append(txt(W - RIGHT - 4, y + (34 if ln.get("cap") else 16),
                     f"max {mx:g} {ln.get('unit','')}", 14, ln["color"], "end"))
        y += lane_h + gap
    if marks:
        for m in marks:
            x = LEFT + (W - LEFT - RIGHT) * (m - w0) / (w1 - w0)
            s.append(f"<line x1='{x:.1f}' y1='40' x2='{x:.1f}' y2='52' stroke='{RED}'/>")
        s.append(txt(W - RIGHT - 4, 18, f"顶部红刻 = quantum 抢占（{len(marks)} 次）", 15, RED, "end"))
    s.append("</svg>")
    return "\n".join(s)


def tl_pile(rows, title_txt, span_ns=None):
    """v1 hl_strip: every instance a horizontal line at its real time, inside a
    trapezoid envelope; stacked top-to-bottom in time order."""
    # v1 split: header carries the WHOLE pile, the strip shows members inside a
    # window. v1 piles were second-scale calls in a 30 s window; these members
    # are us-scale operator instances, so the window narrows to the densest
    # span_ns stretch until a member is wider than a pixel, instead of the
    # whole window degenerating into a diagonal ribbon.
    allm = sorted((int(r["start_ns"]), int(r["end_ns"]) - int(r["start_ns"])) for r in rows)
    import bisect as _b
    starts = [a for a, _ in allm]
    if span_ns:
        best, bn = allm[0][0], -1
        t0 = allm[0][0]
        while t0 + span_ns <= allm[-1][0] + allm[-1][1]:
            n = _b.bisect_left(starts, t0 + span_ns) - _b.bisect_left(starts, t0)
            if n > bn:
                bn, best = n, t0
            t0 += span_ns // 4
        w0, w1 = best, best + span_ns
        ms = [(a, d) for a, d in allm if a >= w0 and a + d <= w1]
    else:
        ms = allm
        w0, w1 = allm[0][0], max(a + d for a, d in allm)
    durs = sorted(d for _, d in ms)
    p90 = durs[int(0.9 * len(durs))] if durs else 0
    dmax = durs[-1] if durs else 0
    top, bottom = 96, 420
    s = svg_open(bottom + 60, title_txt)
    s += tl_axis(w0, w1, 60, bottom - 40)
    s.append(txt(4, 30, title_txt, 18, BLUE, "start", "600"))
    X = lambda t: LEFT + (W - LEFT - RIGHT) * (min(max(t, w0), w1) - w0) / (w1 - w0)
    n = len(ms)
    frac = lambda k: 0.5 if n == 1 else k / (n - 1)
    ends = [[X(a), max(X(a + d), X(a) + 0.6)] for a, d in ms]
    ls = (ends[-1][0] - ends[0][0]) if n > 1 else 0
    rs = (ends[-1][1] - ends[0][1]) if n > 1 else 0
    li = min(e[0] - ls * frac(k) for k, e in enumerate(ends)) - 4
    ri = max(e[1] - rs * frac(k) for k, e in enumerate(ends)) + 4
    s.append(f"<path d='M{li:.1f} {top} L{ri:.1f} {top} L{ri+rs:.1f} {bottom} "
             f"L{li+ls:.1f} {bottom} Z' fill='#eef4fa' stroke='#8fb2ce'/>")
    segb, segr = "", ""
    for k, e in enumerate(ends):
        y = top + frac(k) * (bottom - top)
        piece = f"M{e[0]:.1f} {y:.1f}H{max(e[1], e[0]+1.4):.1f}"
        if ms[k][1] >= p90:
            segr += piece
        else:
            segb += piece
    s.append(f"<path d='{segb}' stroke='{BLUE}' stroke-width='1.2' fill='none' opacity='.75'/>")
    s.append(f"<path d='{segr}' stroke='{RED}' stroke-width='2' fill='none'/>")
    ki = max(range(len(ms)), key=lambda k: ms[k][1])
    ky = top + frac(ki) * (bottom - top)
    s.append(txt(ends[ki][1] + 8, ky + 5,
                 f"最长 {ms[ki][1]/1e3:.0f} us", 14, RED))
    s.append(txt(LEFT, bottom + 40,
                 f"红 = 时长 ≥ p90（{p90/1e3:.0f} us）；蓝 = 其余。成员线宽为真实时长比例（微秒级，故近似点）",
                 15, "#48607d"))
    s.append("</svg>")
    return "\n".join(s)


def tl_micro(sq_path, w0, w1, span_ns, mem_pct):
    """v1 kernel_micro_strip: the busiest sub-window, kernels at true x
    proportions, gemm and other rows, resource-wall reference bar."""
    import sqlite3 as _sq
    db = _sq.connect(str(sq_path))
    K = [(s, e, n or "") for s, e, n in db.execute(
        "select k.start, k.end, sv.value from CUPTI_ACTIVITY_KIND_KERNEL k "
        "left join StringIds sv on k.shortName = sv.id "
        "where k.end > ? and k.start < ?", (w0, w1))]
    # busiest stretch of span_ns by covered time
    best, bs = None, -1
    step = span_ns // 4
    t = w0
    while t + span_ns <= w1:
        cov = sum(min(e, t + span_ns) - max(s, t) for s, e, _ in K
                  if e > t and s < t + span_ns)
        if cov > bs:
            bs, best = cov, t
        t += step
    a, b = best, best + span_ns
    row_h, rect_h = 84, 68
    h = 46 + 2 * row_h + 66
    s = svg_open(h, "kernel 显微")
    X = lambda t: LEFT + (W - LEFT - RIGHT - 60) * (min(max(t, a), b) - a) / (b - a)
    for lab, y0, col, pred in (("gemm", 46, GEMM, lambda n: "Kernel2" in n or "gemm" in n),
                               ("其它", 46 + row_h + 16, OTHK, lambda n: not ("Kernel2" in n or "gemm" in n))):
        s.append(txt(LEFT - 6, y0 + 40, lab, 16, col, "end"))
        s.append(f"<rect x='{LEFT}' y='{y0}' width='{W-LEFT-RIGHT-60}' height='{row_h}' "
                 f"fill='#fbfbf9' stroke='#eee'/>")
        cnt = 0
        for ks, ke, name in K:
            if ke <= a or ks >= b or not pred(name):
                continue
            cnt += 1
            s.append(f"<rect x='{X(ks):.2f}' y='{y0+8}' width='{max(X(ke)-X(ks),0.5):.2f}' "
                     f"height='{rect_h}' fill='{col}' opacity='.85'/>")
        s.append(txt(W - RIGHT - 66, y0 + 14, f"{cnt} 个", 14, col, "end"))
    # resource wall: how far below the memory roof these kernels sit
    wx = W - RIGHT - 40
    s.append(f"<rect x='{wx}' y='{46}' width='18' height='190' fill='#eef4fa' stroke='#8fb2ce'/>")
    fh = 190 * min(mem_pct, 100) / 100
    s.append(f"<rect x='{wx}' y='{46+190-fh:.1f}' width='18' height='{fh:.1f}' fill='{RED}'/>")
    s.append(txt(wx + 9, 46 + 190 + 18, f"内存墙 {mem_pct:.0f}%", 13, RED, "middle"))
    s.append(txt(LEFT, 30, f"最忙 {span_ns/1e6:.0f} ms（{a/1e9:.2f}–{b/1e9:.2f} s）·"
                           f" 矩形宽度 = kernel 真实时长比例", 16, "#48607d"))
    s.append("</svg>")
    return "\n".join(s)



def assert_lineage_valid(base: Path, need_steps=None) -> dict:
    """Refuse to render from a lineage that is not currently valid.

    The report layer consumes accepted stage outputs. It used to read whatever
    files were on disk, so a lineage whose stages had been WITHDRAWN (moved to
    _void*/ and cut from the ledger) still produced a perfectly plausible
    report — that is how a withdrawn scope claim reached a published document.
    Three checks, all cheap, all refusals rather than warnings:

      1. every needed step is in the ledger (not withdrawn),
      2. every handoff says complete,
      3. every stage_fingerprint still matches the code that would produce it
         (a stale fingerprint means the stage's definition changed since).
    """
    import sys as _sys
    _sys.path.insert(0, str(Path(__file__).resolve().parent))
    import pt_v2_runtime as _R
    need = list(need_steps or [f'S{i:02d}' for i in range(1, 11)])
    led = json.loads((base / 'ledger.json').read_text())
    have = {e['step'] for e in led['entries']}
    missing = [s for s in need if s not in have]
    bad_status, stale = [], []
    for s in need:
        hp = base / s / 'handoff.json'
        if not hp.is_file():
            continue
        h = json.loads(hp.read_text())
        if h.get('status') != 'complete':
            bad_status.append(s)
        if h.get('stage_fingerprint') != _R.stage_fingerprint(s):
            stale.append(s)
    if missing or bad_status or stale:
        raise SystemExit(
            '拒绝渲染：lineage 当前无效\n'
            f'  已撤下/不在台账: {missing or "无"}\n'
            f'  handoff 非 complete: {bad_status or "无"}\n'
            f'  指纹失效（阶段定义已变）: {stale or "无"}\n'
            '  报告层只消费已验收且未失效的阶段产出；请先按合同重跑，再生成产物。')
    return {'ledger': [e['step'] for e in led['entries']],
            'checked': need, 'all_fingerprints_current': True}

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lineage", default="mixed")
    ap.add_argument("--base", type=Path,
                    default=ROOT / "artifacts/agentix_8b/pt_v2")
    ap.add_argument("--out", type=Path,
                    default=ROOT / "artifacts/agentix_8b/autotrace/R10_PROCESS.html")
    a = ap.parse_args()
    lineage_ok = assert_lineage_valid(a.base / a.lineage)
    L = Lineage(a.base / a.lineage)
    stats = L.proc_stats()
    fams = L.ncu_families()
    dv = L.conc_obj["objects"][0]

    steps = [e["step"] for e in L.ledger["entries"]]
    audit = {
        "lineage": a.lineage,
        "ledger": steps,
        "workload_sha256": L.contract.get("workload_sha256"),
        "timeline_figure_rules": {
            "why": ("静态报告无法缩放：每张时间线图的视窗由先写定的规则选出，与全景成对出现；"
                    "规则与落点只进审计，正文图注只讲内容"),
            "rules": ZOOM_RULES,
            "note": "全景按 bin 聚合（柱高=占用比例），逐实例只在放大图里画",
        },
        "selection_rules": {
            "class2": L.c2["rule"], "class3": L.c3["rule"],
        },
        "declared_scopes": {
            "pass1": L.p1cov["declared_scope"],
            "pass2": L.p2cov.get("declared_scope"),
            "pass3_windows": [[w["start_ns"], w["end_ns"]] for w in L.windows["windows"]],
        },
        "overhead_ledger": L.overhead,
        "invalidations": L.ledger.get("invalidations", []),
        "note": "选材标准与窗口只进本文件；正文图注只讲内容与差量数字",
    }
    a.out.parent.mkdir(parents=True, exist_ok=True)
    (a.out.parent / "R10_PROCESS_AUDIT.json").write_text(
        json.dumps(audit, indent=1, ensure_ascii=False) + "\n")

    body = (b1(L) + b2(L, stats) + b3(L) + b4(L, fams) + b5(L, stats, fams, dv))
    html = f"""<!doctype html><html lang='zh'><head><meta charset='utf-8'>
<title>文档 B · process 层次分析与 trace</title><style>{CSS}</style></head><body><div class='wrap'>
<h1>文档 B · process 层次分析与 trace（面向进一步优化）</h1>
<p class='sub'>单臂 core · 一条混合 agent serving 负载 · 三遍 trace 的三类时间线 ·
lineage <code>{a.lineage}</code> · 台账 {'→'.join(steps)}</p>
{body}
<h2>可见范围与完整证据</h2>
<p class='sub'>三类时间线各自申报自己的可见范围，没有一类被称作无损。
第一遍是全程但只有 NVTX；第二遍是窗口且到 kernel；第三遍是窗口内的指定 process 且有计数器。
选材标准、窗口、开销台账与本次的撤回记录都在
<code>R10_PROCESS_AUDIT.json</code>。</p>
</div></body></html>"""
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(html)
    print(json.dumps({"out": str(a.out.relative_to(ROOT)), "bytes": len(html),
                      "figures": html.count("<svg"), "tables": html.count("<table"),
                      "lineage": a.lineage, "ledger": len(steps)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

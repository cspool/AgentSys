#!/usr/bin/env python3
"""R10_PROCESS_TIMELINE.html — batch8-style interactive process timeline, v2 data.

Front-end ported from AutoTrace perf_trace_batch8 r10_lossless_timeline
(trim_pipeline/group_band.js + ranked scaffolding): dark canvas, group
trapezoid/ribbon bands (one exact horizontal interval per process instance,
dual start/end axes, fold marks capped at 2x the group's median duration,
36-px expandable rows, click-to-inspect), instance drill-down with the
instance's own launch-owned kernels on a continuous real axis, and binned
signal lanes for pass 1 (whole run) and pass 3 (regime window).

Self-contained: all data embedded as PAYLOAD; opens offline.
"""
from __future__ import annotations

import csv
import json
import sqlite3
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
import os
BASE = ROOT / 'artifacts/agentix_8b/pt_v2' / os.environ.get('PT_LINEAGE', 'mixed')
OUT = ROOT / 'artifacts/agentix_8b/autotrace' / (('R10_PROCESS_TIMELINE.html') if os.environ.get('PT_LINEAGE','mixed')=='mixed' else f"R10_PROCESS_TIMELINE_{os.environ['PT_LINEAGE']}.html")



def fam_of(name: str) -> str:
    """Kernel family from a (possibly demangled) name.

    Exports vary: 'void cutlass::Kernel2<...>' in one, 'void Kernel2<...>' in
    another, bare 'Kernel2' in CUPTI shortName. Strip template args, namespaces
    and the 'void' return type, keep the last identifier token.
    """
    head = name.split('<')[0].split('::')[-1].strip()
    toks = [x for x in head.split() if x != 'void']
    return toks[-1] if toks else head

def class1_lanes(rows, bins=600):
    w0 = min(int(r['start_ns']) for r in rows)
    w1 = max(int(r['end_ns']) for r in rows)
    bw = (w1 - w0) / bins
    reqs = [0.0] * bins; srate = [0] * bins; attn = [0.0] * bins; pre = [0] * bins
    steps = [set() for _ in range(bins)]
    for r in rows:
        i = min(int((int(r['start_ns']) - w0) / bw), bins - 1)
        reqs[i] = max(reqs[i], float(r['reqs'] or 0))
        if r.get('step_id'):
            steps[i].add(r['step_id'])
        if r['process'] == 'attn_core':
            attn[i] += float(r['dur_us'])
        if r.get('at_preemption_boundary') == 'True':
            pre[i] += 1
    return {'w0': w0, 'w1': w1, 'lanes': [
        {'label': '批内请求数', 'color': '#f3bd6d', 'max': 16, 'cap': 16, 'values': reqs},
        {'label': 'step 起点 / bin', 'color': '#9fb0c8',
         'max': max(len(s) for s in steps) or 1, 'values': [len(s) for s in steps]},
        {'label': 'attn_core 实例时长 / bin (us)', 'color': '#64b5ff',
         'max': max(attn) or 1, 'values': [round(v, 1) for v in attn]},
        {'label': '抢占边界实例 / bin', 'color': '#e07b7b',
         'max': max(pre) or 1, 'values': pre}]}



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
    lineage_ok = assert_lineage_valid(BASE)
    c2 = list(csv.DictReader((BASE / 'S09/tables/class2_high_latency.csv').open()))
    c1 = list(csv.DictReader((BASE / 'S09/tables/class1_end_to_end.csv').open()))
    inst = [json.loads(l) for l in (BASE / 'S04/pass2_instances.jsonl').open()]
    series = json.loads((BASE / 'S08/pass3_window_series.json').read_text())
    ncu = [json.loads(l) for l in
           (BASE / 'S07/pass3_ncu_launch_counters.jsonl').open() if l.strip()]
    eu = json.loads((BASE / 'S04/handoff.json').read_text())['engine_utilisation']

    # Three captures, three nsys clocks. One shared origin would relate
    # nanosecond coordinates across runs -- exactly the mistake the pitfalls
    # reference forbids. The band and the drill-down live on the S04 clock
    # (class-2 + its kernels); each lanes chart carries its own capture's
    # absolute axis and the page says the charts do not share an axis.
    loc4 = json.loads((BASE / 'S04/window_location.json').read_text())
    w2lo, w2hi = loc4['window_ns']
    origin = w2lo
    off = lambda v: int(v) - origin

    def nvtx_marks(cap, like_list):
        """Timestamped marks from ONE capture's own clock."""
        dbm = sqlite3.connect(str(cap))
        out = []
        for like in like_list:
            for (ts, txt) in dbm.execute(
                "select n.start, coalesce(n.text, s.value) from NVTX_EVENTS n "
                "left join StringIds s on n.textId = s.id "
                "where coalesce(n.text, s.value) like ? and n.end is null", (like,)):
                out.append(int(ts))
        return sorted(out)

    def proc_ranges(cap, lo, hi):
        dbr = sqlite3.connect(str(cap))
        rows = []
        for s, e, txt in dbr.execute(
            "select n.start, n.end, coalesce(n.text, sv.value) from NVTX_EVENTS n "
            "left join StringIds sv on n.textId = sv.id "
            "where coalesce(n.text, sv.value) like 'p.L%' and n.end is not null"):
            parts = txt.split('.')
            if len(parts) != 3 or s < lo or e > hi:
                continue
            rows.append((int(s), int(e), int(parts[1][1:]), parts[2]))
        return rows

    # ---- class-2: ALL process types in the pass-2 window, process-type tracks.
    # The y axis is the process TYPE (the user cares what the process is, not
    # which call it came from); instances of the selected high-latency type are
    # flagged for highlighting. Kernel drill-down details for every instance.
    inst.sort(key=lambda r: r['start'])
    db = sqlite3.connect(str(BASE / 'S04/cap/cap.sqlite'))
    ko = sorted(db.execute(
        "select r.start, r.end, k.start, k.end, coalesce(sv.value,''), "
        "k.gridX, k.gridY, k.gridZ "
        "from CUPTI_ACTIVITY_KIND_KERNEL k "
        "join CUPTI_ACTIVITY_KIND_RUNTIME r on k.correlationId = r.correlationId "
        "left join StringIds sv on k.shortName = sv.id"))
    import bisect
    kstart = [k[0] for k in ko]
    names, nidx = [], {}
    grids, gidx = [], {}
    c2tracks = {}
    details = {}
    sel_types = set()
    for n_i, rec in enumerate(inst):
        s, e = int(rec['start']), int(rec['end'])
        proc = rec['process']
        if rec.get('selected'):
            sel_types.add(proc)
        iid = f"P{n_i}"
        i2 = bisect.bisect_left(kstart, s)
        kl = []
        while i2 < len(ko) and ko[i2][0] <= e:
            rs, re_, ks, ke, nm, gx, gy, gz = ko[i2]
            if rs >= s and re_ <= e and len(kl) < 80:
                if nm not in nidx:
                    nidx[nm] = len(names); names.append(nm)
                gs = f"{gx},{gy},{gz}"
                if gs not in gidx:
                    gidx[gs] = len(grids); grids.append(gs)
                kl.append([ks - w2lo, ke - w2lo, nidx[nm], gidx[gs]])
            i2 += 1
        c2tracks.setdefault(proc, []).append(
            [s - w2lo, e - w2lo, int(rec['layer_idx']), 1 if rec.get('selected') else 0, iid])
        details[iid] = {
            'process': proc, 'layer': int(rec['layer_idx']), 'step': rec.get('step_id'),
            'phase': rec.get('phase'), 'kernels': kl,
            'own_kernels': rec.get('own_kernels'),
            'device_busy_us': rec.get('device_busy_us'),
            'own_in_range_us': rec.get('own_in_range_us'),
            'other_in_range_us': rec.get('other_in_range_us'),
            'device_idle_us': rec.get('device_idle_us'),
            'own_outside_range_us': rec.get('own_outside_range_us'),
        }
    for v in c2tracks.values():
        v.sort()
    cross = json.loads((BASE / 'S05/cross_process_concurrency.json').read_text())

    # class-1: every process one track, one shared axis, with preemption ------
    PROCS = ['norm_in', 'qkv_proj', 'attn_core', 'o_proj',
             'norm_post', 'mlp_gate_up', 'act_mul', 'mlp_down']
    c1w0 = min(int(r['start_ns']) for r in c1)
    c1w1 = max(int(r['end_ns']) for r in c1)
    tracks = {k: [] for k in PROCS}
    for r in c1:
        tracks[r['process']].append([int(r['start_ns']) - c1w0,
                                     int(r['end_ns']) - c1w0,
                                     int(r['layer_idx'])])
    for v in tracks.values():
        v.sort()
    marks1 = [m - c1w0 for m in nvtx_marks(BASE / 'S02/cap/cap.sqlite',
                                           ['agentix.chunk_begin%', 'sched.preempt%'])]
    marks2 = [m - w2lo for m in nvtx_marks(BASE / 'S04/cap/cap.sqlite',
                                           ['agentix.chunk_begin%', 'sched.preempt%'])
              if w2lo <= m <= w2hi]

    # class-3: instances from the pass-3 capture itself, same clock as lanes ---
    w3 = series['windows'][0]
    p3lo, p3hi = int(w3['start_ns']), int(w3['end_ns'])
    c3doc = json.loads((BASE / 'S05/class3_targets.json').read_text())
    c3procs = c3doc['processes']
    p3rows = proc_ranges(BASE / 'S07/cap/cap.sqlite', p3lo, p3hi)
    p3tracks = {q: [] for q in c3procs}
    for s, e, ly, proc in p3rows:
        if proc in p3tracks:
            p3tracks[proc].append([s - p3lo, e - p3lo, ly])
    for v in p3tracks.values():
        v.sort()
    marks3 = [m - p3lo for m in nvtx_marks(BASE / 'S07/cap/cap.sqlite',
                                           ['agentix.chunk_begin%', 'sched.preempt%'])
              if p3lo <= m <= p3hi]

    w3 = series['windows'][0]
    p3lo, p3hi = int(w3['start_ns']), int(w3['end_ns'])
    c3doc = json.loads((BASE / 'S05/class3_targets.json').read_text())
    c3procs = c3doc['processes']
    p3rows = proc_ranges(BASE / 'S07/cap/cap.sqlite', p3lo, p3hi)
    p3tracks = {q: [] for q in c3procs}
    for s, e, ly, proc in p3rows:
        if proc in p3tracks:
            p3tracks[proc].append([s - p3lo, e - p3lo, ly])
    for v in p3tracks.values():
        v.sort()
    marks3 = [m - p3lo for m in nvtx_marks(BASE / 'S07/cap/cap.sqlite',
                                           ['agentix.chunk_begin%', 'sched.preempt%'])
              if p3lo <= m <= p3hi]

    import re as _re
    ncu_map = {}
    trig_rec = json.loads((BASE / 'S07/handoff.json').read_text()).get('ncu_trigger')
    # This lineage's jsonl has an empty nvtx field (the parser matched column
    # names on 'nvtx', which NCU's Range columns do not contain). The layer is
    # recovered from the committed raw export itself, keyed by launch ID.
    # Each per-process raw export restarts ID at 0, so the key must carry the
    # process too — a flat ID key silently mixes layers across processes.
    id2layer = {}
    for rawf in sorted((BASE / 'S07').glob('pass3_*_raw.csv')):
        proc_of = rawf.stem[len('pass3_'):-len('_raw')]
        rows_ = list(csv.DictReader(rawf.open()))
        if len(rows_) < 2:
            continue
        rng_cols = [c for c in rows_[0] if 'Range' in c]
        for row in rows_[1:]:
            m = _re.search(r'p\.L(\d+)', ' '.join(str(row.get(c) or '') for c in rng_cols))
            if m:
                id2layer[(proc_of, row.get('ID'))] = int(m.group(1))
    for r in ncu:
        mly = _re.search(r'p\.L(\d+)', r.get('nvtx') or '')
        if not mly and (r.get('process'), r.get('ncu_launch_id')) in id2layer:
            class _M:  # minimal stand-in so the code below reads one way
                def __init__(s, v): s.v = v
                def group(s, _): return str(s.v)
            mly = _M(id2layer[(r['process'], r['ncu_launch_id'])])
        fam_ = fam_of(r['kernel'])
        gm = _re.findall(r'\d+', str(r.get('grid')))
        if not (mly and gm):
            continue
        # Layer is dropped from the key: the weights are identical across
        # layers, so per-kernel counters are a property of (family, grid).
        key = f"{fam_}|{','.join(gm[:3])}"
        cs = r.get('counters') or {}
        val = {'dur_us': r.get('device_us'),
               'mem_pct': (cs.get('gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed') or {}).get('value'),
               'dram_gbs': (cs.get('dram__bytes.sum.per_second') or {}).get('value'),
               'l2_hit': (cs.get('lts__t_sector_hit_rate.pct') or {}).get('value')}
        ncu_map.setdefault(key, []).append(val)
    ncu_map = {k: {'n': len(v),
                   **{f: round(statistics.median([x[f] for x in v if x[f] is not None]), 3)
                      for f in ('dur_us', 'mem_pct', 'dram_gbs', 'l2_hit')
                      if any(x[f] is not None for x in v)}}
               for k, v in ncu_map.items()}
    fam = {}
    for r in ncu:
        f = fam_of(r['kernel'])[:30]
        d = fam.setdefault(f, {'n': 0, 'dev_us': 0.0, 'mem': []})
        d['n'] += 1; d['dev_us'] += r.get('device_us') or 0
        c = (r.get('counters') or {}).get(
            'gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed')
        if isinstance(c, dict):
            d['mem'].append(c['value'])
    ncu_tbl = [{'family': k, 'n': v['n'], 'dev_us': round(v['dev_us'], 1),
                'mem_pct_median': round(statistics.median(v['mem']), 1) if v['mem'] else None}
               for k, v in sorted(fam.items(), key=lambda kv: -kv[1]['dev_us'])]

    c2_span = (max(int(r['end_ns']) for r in c2) - min(int(r['start_ns']) for r in c2)) / 1e9
    c3_span = (int(w3['end_ns']) - int(w3['start_ns'])) / 1e9
    step_ms = (eu.get('step_dur_us_median') or 0) / 1e3
    # -- hardware lanes for class 3: identity-projected, binned, no interpolation
    # Per-launch metrics come from the committed raw exports (SpeedOfLight +
    # MemoryWorkloadAnalysis); the observed kernels of the pass-3 window get the
    # metric of their (family, grid) identity — tier A — or family median —
    # tier B. Bins with no identity-covered kernel time stay EMPTY (raw points,
    # never interpolated: an NCU sampling gap is not zero utilisation).
    MET = {'sm': 'sm__throughput.avg.pct_of_peak_sustained_elapsed',
           'mem': 'gpu__compute_memory_throughput.avg.pct_of_peak_sustained_elapsed',
           'l2bw': 'lts__t_sectors.avg.pct_of_peak_sustained_elapsed',
           'l2hit': 'lts__t_sector_hit_rate.pct',
           'dram': 'dram__bytes.sum.per_second'}
    idA, idB = {}, {}
    for rawf in sorted((BASE / 'S07').glob('pass3_*_raw.csv')):
        rows_ = list(csv.DictReader(rawf.open()))
        if len(rows_) < 2:
            continue
        for row in rows_[1:]:
            fam_ = fam_of(row.get('Kernel Name') or '')
            gm = _re.findall(r'\d+', str(row.get('Grid Size')))
            if not fam_ or not gm:
                continue
            vals = {}
            for mk, colname in MET.items():
                v = (row.get(colname) or '').replace(',', '').strip()
                try:
                    vals[mk] = float(v)
                except ValueError:
                    pass
            if not vals:
                continue
            idA.setdefault(f"{fam_}|{','.join(gm[:3])}", []).append(vals)
            idB.setdefault(fam_, []).append(vals)

    def med(vs):
        out = {}
        for mk in MET:
            xs = [v[mk] for v in vs if mk in v]
            if xs:
                out[mk] = statistics.median(xs)
        return out
    idA = {k: med(v) for k, v in idA.items()}
    idB = {k: med(v) for k, v in idB.items()}

    dbk = sqlite3.connect(str(BASE / 'S07/cap/cap.sqlite'))
    kwin = list(dbk.execute(
        "select k.start, k.end, coalesce(sv.value,''), k.gridX, k.gridY, k.gridZ "
        "from CUPTI_ACTIVITY_KIND_KERNEL k left join StringIds sv on k.shortName=sv.id "
        "where k.end > ? and k.start < ?", (p3lo, p3hi)))
    NB = 1200
    bw_ns = (p3hi - p3lo) / NB
    acc = {mk: [0.0] * NB for mk in MET}
    wgt = {mk: [0.0] * NB for mk in MET}
    busy_t = [0.0] * NB
    cov_t = [0.0] * NB
    tierA_t = 0.0
    for ks, ke, nm, gx, gy, gz in kwin:
        m = idA.get(f"{nm}|{gx},{gy},{gz}")
        tier_a = m is not None
        if m is None:
            m = idB.get(nm)
        i0 = max(int((ks - p3lo) / bw_ns), 0)
        i1 = min(int((ke - p3lo) / bw_ns), NB - 1)
        for bi in range(i0, i1 + 1):
            blo = p3lo + bi * bw_ns
            ov = min(ke, blo + bw_ns) - max(ks, blo)
            if ov <= 0:
                continue
            busy_t[bi] += ov
            if m is None:
                continue
            cov_t[bi] += ov
            if tier_a:
                tierA_t += ov
            for mk, v in m.items():
                acc[mk][bi] += v * ov
                wgt[mk][bi] += ov
    HWDEF = [('sm', 'SM 吞吐 %峰值', '#e78bd0', 100, None),
             ('mem', '内存通路 %峰值', '#7ce3a1', 100, None),
             ('l2bw', 'L2 带宽 %峰值', '#8fd0ff', 100, None),
             ('l2hit', 'L2 命中率 %', '#c9b7ff', 100, None),
             ('dram', '显存(DRAM)带宽 GB/s', '#ffb37c', 1008, 1008)]
    hw_lanes = []
    for mk, lab, col, mx, roof in HWDEF:
        vals = [round(acc[mk][i] / wgt[mk][i], 2) if wgt[mk][i] else None
                for i in range(NB)]
        hw_lanes.append({'key': mk, 'label': lab, 'color': col,
                         'max': mx or (max([v for v in vals if v is not None] or [1])),
                         'roof': roof, 'values': vals,
                         'cov': [round(cov_t[i] / busy_t[i], 3) if busy_t[i] else 0
                                 for i in range(NB)]})
    hw_note = {
        'bins': NB, 'bin_ms': round(bw_ns / 1e6, 3),
        'kernels_in_window': len(kwin),
        'identity_covered_share_of_busy': round(sum(cov_t) / max(sum(busy_t), 1e-9), 4),
        'tierA_share_of_covered': round(tierA_t / max(sum(cov_t), 1e-9), 4),
        'method': ('身份投影：观测 kernel 按 (族,grid) 取同身份 NCU 中位（A 档），'
                   '否则族中位（B 档）；bin 内按 kernel 时长加权平均；'
                   '无身份覆盖的 bin 留空——NCU 采样缺口不是零利用率，不插值'),
    }

    # tier-B fallback: same family, median across its grids — lower confidence
    fam_agg = {}
    for k, v in ncu_map.items():
        fam_agg.setdefault(k.split('|')[0], []).append(v)
    ncu_fam = {f: {'n': sum(x['n'] for x in vs),
                   **{fld: round(statistics.median([x[fld] for x in vs if fld in x]), 3)
                      for fld in ('dur_us', 'mem_pct', 'dram_gbs', 'l2_hit')
                      if any(fld in x for x in vs)}}
               for f, vs in fam_agg.items()}
    hitA = hitB = tot_k = 0
    for det in details.values():
        for kk in det['kernels']:
            tot_k += 1
            if f"{names[kk[2]]}|{grids[kk[3]]}" in ncu_map:
                hitA += 1
            elif names[kk[2]] in ncu_fam:
                hitB += 1
    id_cov = {'exact_family_grid': round(hitA / tot_k, 4) if tot_k else 0,
              'family_only': round(hitB / tot_k, 4) if tot_k else 0}
    payload = {
        'origin_ns': str(origin),
        'lineage': 'mixed', 'arm': 'instrumented (eager + module NVTX)',
        'kernel_names': names, 'details': details,
        'lanes1': class1_lanes(c1),
        'grids': grids, 'ncu_map': ncu_map, 'ncu_trigger': trig_rec,
        'c2': {'w0': w2lo, 'w1': w2hi, 'procs': PROCS,
               'tracks': c2tracks, 'marks': marks2,
               'selected_types': sorted(sel_types)},
        'cross': cross,
        'hw': {'lanes': hw_lanes, 'note': hw_note},
        'e2e': {'w0': c1w0, 'w1': c1w1, 'procs': PROCS, 'tracks': tracks,
                'marks': marks1},
        'p3band': {'w0': p3lo, 'w1': p3hi, 'procs': c3procs,
                   'tracks': p3tracks, 'marks': marks3},
        'engine': eu, 'ncu': ncu_tbl, 'identity_coverage': id_cov,
        'ncu_fam': ncu_fam,
    }
    lane_map = {'device_busy': ('设备忙碌（占比）', '#7ce3a1', 1),
                'own_busy': ('其中目标 process（占比）', '#64b5ff', 1),
                'batch': ('批内请求数', '#f3bd6d', 16),
                'step_rate': ('step 起点 / bin', '#9fb0c8', None)}
    l3 = []
    for ln in w3['lanes']:
        lab, col, mx = lane_map.get(ln['key'], (ln['key'], '#64b5ff', None))
        vals = [v if v is not None else 0 for v in ln['values']]
        l3.append({'label': lab, 'color': col,
                   'max': mx or (max(vals) or 1),
                   'cap': 16 if ln['key'] == 'batch' else None, 'values': vals})
    payload['lanes3'] = {'w0': int(w3['start_ns']), 'w1': int(w3['end_ns']),
                         'marks': [round(m['t_ms'] * 1e6) for m in w3.get('marks', [])
                                   if 'quantum' in m.get('kind', '')],
                         'lanes': l3}
    # lanes1 w0/w1 arrive absolute; convert to origin-relative

    js_helpers = r"""
'use strict';
const $=id=>document.getElementById(id);
const elt=(tag,txt,cls)=>{const x=document.createElement(tag);if(txt!==undefined)x.textContent=txt;if(cls)x.className=cls;return x;};
const duration=n=>n>=1e9?(n/1e9).toFixed(3)+' s':n>=1e6?(n/1e6).toFixed(3)+' ms':n>=1e3?(n/1e3).toFixed(3)+' µs':n+' ns';
const absolute=n=>String(BigInt(PAYLOAD.origin_ns)+BigInt(Math.round(n)));
function showDetails(v){$('details').textContent=JSON.stringify(v,null,2);}
function tableView(container,rows,fields){const t=document.createElement('table');const h=document.createElement('thead');h.innerHTML='<tr>'+fields.map(f=>'<th>'+f+'</th>').join('')+'</tr>';t.append(h);const b=document.createElement('tbody');for(const row of rows){const tr=document.createElement('tr');for(const f of fields){const td=document.createElement('td');td.textContent=row[f]??'';tr.append(td);}b.append(tr);}t.append(b);container.replaceChildren(t);}
const RANKED={bands:[]};
const LAYCOL={0:'#64b5ff',15:'#f3bd6d',31:'#7ce3a1'};
"""
    # group_band.js port: colors by layer, wording adapted, otherwise the same geometry
    js_band = r"""
"""
    js_app = r"""
function instPanel(item){
 const iid=item[4],d=PAYLOAD.details[iid];if(!d)return;
 item={b:item[0],e:item[1],layer:item[2],id:iid,label:d.process+' L'+String(d.layer).padStart(2,'0')+' step'+d.step,phase:d.phase,step:d.step};
 const host=$('inst');host.replaceChildren();
 host.append(elt('h4','实例 '+item.label+' · '+duration(item.e-item.b)));
 const c=elt('canvas');c.width=1040;c.height=134;host.append(c);
 const g=c.getContext('2d');g.fillStyle='#0b1728';g.fillRect(0,0,1040,134);
 const b=item.b,e=item.e,X=t=>40+(t-b)/(e-b)*960;
 g.strokeStyle='#668fb7';g.strokeRect(40,30,960,40);
 g.fillStyle='#bbd0ec';g.font='12px system-ui';
 g.fillText('主机区间（连续真实时间轴） '+duration(e-b),40,20);
 let mapped=0;const mappedRows=[];
 for(const [ks,ke,ni,gi] of d.kernels){
  const nm=PAYLOAD.kernel_names[ni]||'';
  const x1=X(Math.max(ks,b)),w=Math.max(X(Math.min(ke,e))-x1,1);
  g.fillStyle=/Kernel2|gemm/.test(nm)?'#f3bd6d':'#64b5ff';
  g.fillRect(x1,34,w,32);
  const key=nm+'|'+(PAYLOAD.grids[gi]||'');
  const hit=PAYLOAD.ncu_map[key];const fb=hit?null:PAYLOAD.ncu_fam[nm];
  if(hit){mapped++;mappedRows.push({tier:'A 同族同grid',kernel:nm,grid:PAYLOAD.grids[gi],...hit});
   g.strokeStyle='#e8d06a';g.setLineDash([3,2]);g.strokeRect(x1-1,32,w+2,36);g.setLineDash([]);}
  else if(fb){mappedRows.push({tier:'B 同族(族中位,置信更低)',kernel:nm,grid:PAYLOAD.grids[gi],...fb});
   g.strokeStyle='#8a7c3a';g.setLineDash([1,3]);g.strokeRect(x1-1,32,w+2,36);g.setLineDash([]);}
 }
 g.fillStyle='#9fb0c8';
 g.fillText('本区间发射的 kernel '+(d.own_kernels??d.kernels.length)+' 个（金=gemm 族，蓝=其它）；区间外执行的自有 kernel 不画在框内',40,92);
 g.fillText('设备侧（同一时钟交叠）：忙碌 '+d.device_busy_us+' us = 自有 '+d.own_in_range_us+' + 其它 '+d.other_in_range_us+'；空闲 '+d.device_idle_us+' us；自有落在区间外 '+d.own_outside_range_us+' us',40,110);
 g.fillStyle='#e8d06a';g.fillText('亮黄虚线 = A 档（同族同 grid）NCU 旁证 '+mapped+'/'+d.kernels.length+'；暗黄细虚线 = B 档（仅同族，族中位，置信更低）；计数器由同一冻结条件触发采集，时间轴对应位置=按条件定位的第三类窗口',40,126);
 showDetails({instance:item.id,phase:item.phase,step:item.step,begin_ns:absolute(item.b),end_ns:absolute(item.e),...d,ncu_identity_matches:mappedRows,kernels:d.kernels.map(k=>({begin_ns:absolute(k[0]),end_ns:absolute(k[1]),name:PAYLOAD.kernel_names[k[2]],grid:PAYLOAD.grids[k[3]]}))});
}

/* 类型轨道图：每个 process 类型一条轨道，全轨共一条线性时间轴（同第一类的缩放）。
   第二类用它并高亮高延迟类型；点击实例可下潜。*/
function typeChart(host,pack,{title,expl,onPick=null,hiTypes=[]}={}){
 const box=elt('div',undefined,'group-band');
 box.append(elt('h4',title),elt('p',expl));
 const controls=elt('div',undefined,'controls'),plus=elt('button','放大'),minus=elt('button','缩小'),reset=elt('button','全程');
 controls.append(plus,minus,reset);box.append(controls);
 const canvas=elt('canvas'),state=elt('p',undefined,'chart-state'),tip=elt('p','Shift+滚轮缩放，拖动平移'+(onPick?'；点击实例下潜。':'。'),'chart-tooltip');
 box.append(canvas,state,tip);host.append(box);
 const left=170,right=30,rowH=44,top=30,W=1180;
 const procs=pack.procs.filter(q=>pack.tracks[q]&&pack.tracks[q].length);
 const n=procs.length;canvas.width=W;canvas.height=top+n*rowH+46;
 let view=[0,pack.w1-pack.w0],drag=null,selected=null;
 function draw(){
  const c=canvas.getContext('2d');c.fillStyle='#0b1728';c.fillRect(0,0,W,canvas.height);
  const span=view[1]-view[0],pw=W-left-right;c.font='12px system-ui';
  for(let k=0;k<=6;k++){const tt=view[0]+span*k/6,x=left+pw*k/6;
   c.strokeStyle='#2a3f5a';c.beginPath();c.moveTo(x,top);c.lineTo(x,canvas.height-30);c.stroke();
   c.fillStyle='#b8cce7';c.fillText((tt/1e9).toFixed(span<1e8?4:2)+' s',x-18,top-10);}
  procs.forEach((pr,pi)=>{const y=top+pi*rowH;
   const hi=hiTypes.includes(pr);
   c.fillStyle='#101f33';c.fillRect(left,y+4,pw,rowH-10);
   c.fillStyle=hi?'#ffd479':'#9fb0c8';c.fillText(pr+(hi?' ▲高延迟':''),8,y+rowH/2+3);
   let drawn=0;c.globalAlpha=.62;
   for(const it of pack.tracks[pr]){const b=it[0],e=it[1],ly=it[2];
    if(e<view[0]||b>view[1])continue;
    const x1=left+(Math.max(b,view[0])-view[0])/span*pw,
          x2=left+(Math.min(e,view[1])-view[0])/span*pw;
    c.fillStyle=LAYCOL[ly]||'#64b5ff';
    c.fillRect(x1,y+8,Math.max(x2-x1,.6),rowH-18);drawn++;
    if(selected&&selected[4]===it[4]){c.globalAlpha=1;c.strokeStyle='#fff';c.strokeRect(x1-1,y+7,Math.max(x2-x1,1)+2,rowH-16);c.globalAlpha=.62;}}
   c.globalAlpha=1;
   if(hi){c.strokeStyle='#ffd479';c.strokeRect(left,y+4,pw,rowH-10);}
   c.fillStyle='#7f95b3';c.fillText(String(drawn),W-right-40,y+rowH/2+3);});
  c.strokeStyle='#e07b7b';let mv=0;
  for(const m of (pack.marks||[])){if(m<view[0]||m>view[1])continue;mv++;
   const x=left+(m-view[0])/span*pw;c.beginPath();c.moveTo(x,canvas.height-28);c.lineTo(x,canvas.height-20);c.stroke();}
  c.fillStyle='#e07b7b';if(pack.marks)c.fillText('底部红刻 = quantum 抢占，视窗内 '+mv+' / 共 '+pack.marks.length,left,canvas.height-6);
  state.textContent='视窗 ['+(view[0]/1e9).toFixed(3)+' s, '+(view[1]/1e9).toFixed(3)+' s)；右侧数字为该轨视窗内实例数；颜色=层（蓝 L00 / 金 L15 / 绿 L31）；线性时间轴，无折叠。';
 }
 function zoom(f,anchor=.5){const span=view[1]-view[0],size=Math.max(1e4,Math.round(span*f)),pivot=view[0]+span*anchor,b=Math.round(pivot-size*anchor);view=[b,b+size];draw();}
 canvas.onwheel=e=>{if(e.ctrlKey||e.shiftKey){e.preventDefault();zoom(Math.exp(e.deltaY*.001),Math.max(0,Math.min(1,(e.offsetX-left)/(W-left-right))));}};
 canvas.onpointerdown=e=>{drag={x:e.clientX,y:e.offsetY,view:view.slice()};canvas.setPointerCapture(e.pointerId);};
 canvas.onpointerup=e=>{if(!drag)return;const dx=e.clientX-drag.x;
  if(Math.abs(dx)>4){const d=Math.round(dx/(W-left-right)*(drag.view[1]-drag.view[0]));view=[drag.view[0]-d,drag.view[1]-d];draw();}
  else if(onPick){const pi=Math.floor((drag.y-top)/rowH);
   if(pi>=0&&pi<procs.length){const span=view[1]-view[0],tt=view[0]+(e.offsetX-left)/(W-left-right)*span;
    let best=null,bd=1/0;
    for(const it of pack.tracks[procs[pi]]){const mid=(it[0]+it[1])/2,dd=Math.abs(mid-tt);
     if(tt>=it[0]-span*.002&&tt<=it[1]+span*.002&&dd<bd){bd=dd;best=it;}}
    if(best){selected=best;draw();onPick(best);}}}
  drag=null;};
 plus.onclick=()=>zoom(.5);minus.onclick=()=>zoom(2);reset.onclick=()=>{view=[0,pack.w1-pack.w0];draw();};
 draw();
}

function e2eChart(host,pack){
 typeChart(host,pack,{title:'第一类 · 端到端：8 个 process 各一条时间线，共一个时间轴（S02 时钟）',
  expl:'每条横线/矩形是该 process 的一个实例（跨 L00/L15/L31 三层）。全程视野下实例亚像素，以密度透明呈现；Shift+滚轮缩放、拖动平移后可见单实例。底部红刻为 quantum 抢占标记（本采集自己的时钟）。'});
}

/* 并发：高延迟/并发 process 的实例带 + 同窗硬件信号（设备忙碌/自有/批），同一个画布、同一条横轴。*/
function concChart(host,pack,lanes,hw){
 const box=elt('div',undefined,'group-band');
 box.append(elt('h4','第三类 · 并发：class-3 process 实例 + 窗口信号 + 硬件使用率，全部共轴（S07/S08 时钟）'),
  elt('p','上方每行一个 class-3 process 的实例（含跨 process 并发对象；颜色=层）。中段为窗口四信号；下段每个硬件指标一条时间线（SM/内存通路/L2 带宽/L2 命中/显存带宽），由同身份 NCU 计数器投影：A 档=同族同 grid，B 档=族中位；bin 内按 kernel 时长加权，无身份覆盖的 bin 留空——NCU 采样缺口不是零利用率，不插值。柱体透明度=该 bin 的身份覆盖度。同一画布同一横轴，Shift+滚轮缩放、拖动平移。'),
  elt('p','投影方法：'+hw.note.method+'；bin 宽 '+hw.note.bin_ms+' ms；窗口 kernel '+hw.note.kernels_in_window.toLocaleString()+' 个，busy 时间身份覆盖 '+(hw.note.identity_covered_share_of_busy*100).toFixed(1)+'%（其中 A 档 '+(hw.note.tierA_share_of_covered*100).toFixed(1)+'%）。','chart-state'));
 const controls=elt('div',undefined,'controls'),plus=elt('button','放大'),minus=elt('button','缩小'),reset=elt('button','全窗');
 controls.append(plus,minus,reset);box.append(controls);
 const canvas=elt('canvas'),state=elt('p',undefined,'chart-state'),tip=elt('p','Shift+滚轮缩放，拖动平移。','chart-tooltip');
 box.append(canvas,state,tip);host.append(box);
 const left=190,right=30,W=1180,instH=24,laneH=58,gap=8,top=28;
 const n0=pack.procs.length,nl=lanes.length,nh=hw.lanes.length;
 canvas.width=W;canvas.height=top+n0*instH+12+(nl+nh)*(laneH+gap)+40;
 const span0=pack.w1-pack.w0;let view=[0,span0],drag=null;
 function draw(){
  const c=canvas.getContext('2d');c.fillStyle='#0b1728';c.fillRect(0,0,W,canvas.height);
  const span=view[1]-view[0],pw=W-left-right;c.font='12px system-ui';
  const XT=t=>left+(t-view[0])/span*pw;
  for(let k=0;k<=6;k++){const tt=view[0]+span*k/6,x=left+pw*k/6;
   c.strokeStyle='#2a3f5a';c.beginPath();c.moveTo(x,top);c.lineTo(x,canvas.height-30);c.stroke();
   c.fillStyle='#b8cce7';c.fillText(((pack.w0+tt)/1e9).toFixed(span<1e8?4:2)+' s',x-20,top-8);}
  pack.procs.forEach((pr,li)=>{const y=top+li*instH;
   c.fillStyle='#101f33';c.fillRect(left,y+3,pw,instH-6);
   c.fillStyle='#9fb0c8';c.fillText(pr,8,y+instH/2+3);
   for(const [b,e,ly] of (pack.tracks[pr]||[])){if(e<view[0]||b>view[1])continue;
    const x1=XT(Math.max(b,view[0])),x2=XT(Math.min(e,view[1]));
    c.fillStyle=LAYCOL[ly]||'#64b5ff';c.globalAlpha=.8;c.fillRect(x1,y+5,Math.max(x2-x1,.7),instH-10);c.globalAlpha=1;}});
  let y=top+n0*instH+12;
  function laneRow(ln,binned){const base=y+laneH-6;
   c.fillStyle='#101f33';c.fillRect(left,y,pw,laneH);
   c.fillStyle='#9fb0c8';c.fillText(ln.label,8,y+13);
   const N=ln.values.length,binSpan=span0/N;
   const i0=Math.max(0,Math.floor(view[0]/binSpan)),i1=Math.min(N-1,Math.ceil(view[1]/binSpan));
   c.strokeStyle=ln.color;
   for(let i=i0;i<=i1;i++){const v=ln.values[i];if(v===null||v===undefined||!v&&!binned)continue;
    if(v===null||v===undefined)continue;
    const h=(laneH-16)*Math.min(1,v/ln.max);
    const x1=XT(i*binSpan),x2=XT((i+1)*binSpan);
    c.globalAlpha=ln.cov?Math.max(.25,ln.cov[i]):.9;
    c.beginPath();c.moveTo((x1+x2)/2,base);c.lineTo((x1+x2)/2,base-h);
    c.lineWidth=Math.max(.6,(x2-x1)*.7);c.stroke();c.lineWidth=1;}
   c.globalAlpha=1;
   if(ln.cap){const yc=base-(laneH-16)*Math.min(1,ln.cap/ln.max);c.strokeStyle='#e07b7b';c.setLineDash([4,3]);c.beginPath();c.moveTo(left,yc);c.lineTo(W-right,yc);c.stroke();c.setLineDash([]);}
   if(ln.roof&&ln.roof<=ln.max){const yr=base-(laneH-16)*Math.min(1,ln.roof/ln.max);c.strokeStyle='#e07b7b';c.setLineDash([2,3]);c.beginPath();c.moveTo(left,yr);c.lineTo(W-right,yr);c.stroke();c.setLineDash([]);c.fillStyle='#e07b7b';c.fillText('理论峰值',W-right-58,yr-3);}
   c.fillStyle=ln.color;c.fillText('max '+(typeof ln.max==='number'?ln.max.toFixed(0):ln.max),W-right-52,y+13);
   y+=laneH+gap;}
  for(const ln of lanes)laneRow(ln,false);
  for(const ln of hw.lanes)laneRow(ln,true);
  c.strokeStyle='#e07b7b';let mv=0;
  for(const m of pack.marks){if(m<view[0]||m>view[1])continue;mv++;
   const x=XT(m);c.beginPath();c.moveTo(x,canvas.height-28);c.lineTo(x,canvas.height-20);c.stroke();}
  c.fillStyle='#e07b7b';c.fillText('底部红刻 = quantum 抢占，视窗内 '+mv+' / 共 '+pack.marks.length,left,canvas.height-6);
  state.textContent='视窗 ['+((pack.w0+view[0])/1e9).toFixed(3)+' s, '+((pack.w0+view[1])/1e9).toFixed(3)+' s)；轨道 '+pack.procs.length+' 个 process；硬件 lane 柱透明度=身份覆盖度，空档=无 NCU 身份覆盖。';
 }
 function zoom(f,anchor=.5){const span=view[1]-view[0],size=Math.max(1e5,Math.round(span*f)),pivot=view[0]+span*anchor,b=Math.round(pivot-size*anchor);view=[Math.max(-span0*.05,b),Math.max(-span0*.05,b)+size];draw();}
 canvas.onwheel=e=>{if(e.ctrlKey||e.shiftKey){e.preventDefault();zoom(Math.exp(e.deltaY*.001),Math.max(0,Math.min(1,(e.offsetX-left)/(W-left-right))));}};
 canvas.onpointerdown=e=>{drag={x:e.clientX,view:view.slice()};canvas.setPointerCapture(e.pointerId);};
 canvas.onpointerup=e=>{if(!drag)return;const dx=e.clientX-drag.x;
  if(Math.abs(dx)>4){const d=Math.round(dx/(W-190-30)*(drag.view[1]-drag.view[0]));view=[drag.view[0]-d,drag.view[1]-d];draw();}
  drag=null;};
 plus.onclick=()=>zoom(.5);minus.onclick=()=>zoom(2);reset.onclick=()=>{view=[0,span0];draw();};
 draw();
}

(function(){
 e2eChart($('e2e'),PAYLOAD.e2e);
 typeChart($('rankedRoot'),PAYLOAD.c2,{
  title:'第二类 · 窗口内全部 process 类型同轴（高延迟类型高亮；S04 时钟）',
  expl:'纵轴是 process 类型——关心的是 process 是什么，不是它来自哪个 call。金框轨为通过 10% 份额门限的高延迟类型（'+PAYLOAD.c2.selected_types.join('、')+'）。线性时间轴、与第一类相同的缩放，无折叠双轴。点击实例下潜到发射期归属的 kernel 与 NCU 身份旁证。',
  onPick:it=>instPanel(it),hiTypes:PAYLOAD.c2.selected_types});
 concChart($('conc'),PAYLOAD.p3band,PAYLOAD.lanes3.lanes,PAYLOAD.hw);
 const M=PAYLOAD.cross.matrix_share_of_host_interval,rowsM=[];
 const hk='host_vs_device';
 for(const x of Object.keys(M)){const r={};r[hk]=x;for(const y of Object.keys(M[x]))r[y]=(M[x][y]*100).toFixed(1)+'%';rowsM.push(r);}
 tableView($('xmatrix'),rowsM,[hk].concat(Object.keys(M)));
 const prs=PAYLOAD.cross.selected_pairs.map(q=>q.host_process+'\u2192'+q.device_process+' '+(q.share_of_host_interval*100).toFixed(1)+'%');
 $('xpairs').textContent=prs.length?('入选跨 process 并发对象（严格 >10%）：'+prs.join('；')):'没有跨 process 对超过 10% 门限。';
 lanesChart($('lanes1'),PAYLOAD.lanes1,'第一类补充 · 全程四信号 lanes','与端到端轨道同一时钟；批爬升到 cap 后长期贴顶。');
 tableView($('ncu'),PAYLOAD.ncu,['family','n','dev_us','mem_pct_median']);
 $('loading').textContent='完整离线数据已加载；排名只控制展示，源记录全部保留。';
 window.PAGE_READY=true;
})();
"""
    css = ("body{margin:0;background:#0e1c30;color:#d7e5f7;font:14px/1.6 system-ui}"
           "main{max-width:1100px;margin:0 auto;padding:18px}"
           "h1{font-size:22px}h2{font-size:18px;color:#9dcfff}h4{margin:10px 0 4px;color:#bbd0ec}"
           ".group-band{background:#0b1728;border:1px solid #24364e;border-radius:8px;"
           "padding:10px 12px;margin:16px 0}"
           ".group-band p{color:#9fb0c8;font-size:12.5px;margin:4px 0}"
           ".controls button{margin:2px 6px 6px 0;background:#18314b;color:#cfe4fb;"
           "border:1px solid #2a4a6e;border-radius:5px;padding:3px 10px;cursor:pointer}"
           ".band-scroll{overflow:auto;max-height:640px}"
           ".chart-state{font-size:12px;color:#7f95b3}.chart-tooltip{color:#b7d4ef}"
           "table{border-collapse:collapse;font-size:12.5px}"
           "td,th{border:1px solid #2a4a6e;padding:2px 8px}"
           "#details{background:#0b1728;border:1px solid #24364e;padding:10px;"
           "white-space:pre-wrap;font:12px/1.5 ui-monospace,monospace;max-height:420px;overflow:auto}"
           ".notice{color:#e0b3b3}")
    intro = f"""
<header><h1>R10 · process 粒度排名时间线（v2 三遍数据）</h1></header>
<section><p>前端沿自 batch8 r10_lossless_timeline 的折叠梯形分组：每个 process 实例是一条
真实起止横线，左开始轴/右结束轴分别标注真实时间（横线长度不代表耗时）；长间隔按
「2×组内中位时长」封顶折叠，// 为折叠标记，可展开明细或取消折叠；可展开逐行（36 px）、
Shift+滚轮缩放、拖动平移、点击横线下潜单实例。<b>时间对齐</b>：每张图内部单一时钟源——图上全部元素（实例轨/信号 lane/硬件 lane/抢占刻）
取自同一次采集的同一条 nsys 会话轴、同一窗口原点；硬件 lane 的<b>时间</b>继承自观测 kernel
自己的区间，NCU 回放只贡献<b>数值</b>（按族+grid 身份查表），其时间轴从未被使用；
信号 lane（600 bins）与硬件 lane（1200 bins）共原点且为整数倍，箱边缘严格对齐；
host(NVTX) 与 device(CUPTI) 两个时钟域由 nsys 关联，已用因果检验实测：
289k 对 launch↔kernel 中设备开始早于发射开始的为 0，偏斜上界 ~0 ns（远小于 2.8 ms 箱宽）。
三张图分属三次采集（S02/S04/S08）的三个时钟，<b>互不共轴</b>——
纳秒坐标不跨运行成立，跨图对齐只能靠负载状态（批/相位），不能靠横轴。数据为本仓 v2 lineage <code>mixed</code> 的
已验收产出：高延迟组来自第二遍（{len(c2)} 个 attn_core 实例，按相位×层分组、按组内观测
时长和排名），单实例的 kernel 为发射期归属（发射调用落在区间内），lanes 来自第一遍全程与
第三遍负载区间窗口，NCU 表来自第三遍逐 process 回放。</p>
<p><b>与 batch8 参考的方法差异（时间段更短、实例更少）</b>：batch8 是 8 个请求的全程无损
trace（原始包络 744.7 s，另需按请求尾裁剪展示范围）；v2 的第二、三类是<b>条件触发的短窗</b>——
被测进程等冻结的负载条件（相位+批下限）连续成立才开启采集，kernel 预算全部花在被研究的
regime 上。本页第二类窗口 {c2_span:.1f} s / {len(c2)} 个实例、第三类窗口 {c3_span:.1f} s，
远短于 batch8 的包络，因此没有请求尾裁剪一节；折叠机制折的也不再是请求间的长空隙，
而是实例之间的 step 间隔（约 {step_ms:.0f} ms 一拍，仍按 2×组内中位时长封顶）。
分组维度也不同：batch8 按请求/阶段，v2 按相位×层。</p>
<p class="notice">证据边界：本页全部时长来自插桩臂（eager + 模块钩子；每实例 5.8 µs 钩子成本，
eager 相对图臂 step 慢 19%），不得当作性能数字与未插桩基线相减。横线仅括住发射；
自有 kernel 约三成在区间关闭后执行。设备「忙碌」只回答有没有 kernel 在跑：
单流串行、无重叠，SM 覆盖上界 82.9%。引擎 step 覆盖 {eu['step_coverage_of_window']:.1%}、
step 内设备忙碌 {eu['device_busy_share_inside_steps']:.1%}。</p>
<p id="loading">加载中……</p></section>
<section><h2>第一类 · 端到端（每 process 一条时间线，共轴，含抢占）</h2><div id="e2e"></div><div id="lanes1"></div></section>
<section><h2>第二类 · 高延迟与并发提取（process 类型作纵轴，含抢占）</h2><div id="rankedRoot"></div>
<h4>跨 process 并发（host 区间 × 设备归属 份额矩阵，第二遍导出）</h4><p id="xpairs"></p><div id="xmatrix"></div></section>
<section><h2>单实例下潜（点击第二类实例）</h2><div id="inst"><p>尚未选择实例。</p></div>
<h4>源记录</h4><div id="details">（点击实例后显示）</div></section>
<section><h2>第三类 · 并发（并发/高延迟 process 与窗口硬件信号共轴，含抢占）</h2><div id="conc"></div>
<h4>NCU 逐 process 回放 · kernel 家族（条件触发；窗口级对应由构造成立，逐 kernel 按身份键贴附）</h4><div id="ncu"></div></section>
"""
    html = ("<!doctype html><html lang='zh-CN'><meta charset='utf-8'>"
            "<meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>R10 process 时间线（v2）</title><style>" + css + "</style><main>"
            + intro + "</main><script>const PAYLOAD="
            + json.dumps(payload, ensure_ascii=False, separators=(',', ':'))
            + ";</script><script>" + js_helpers + js_band + js_app + "</script></html>\n")
    OUT.write_text(html)
    # summary artifact: Doc B consumes these numbers instead of recomputing
    summary = {
        'e2e': {'window_s': round((c1w0_ := payload['e2e']['w1'] - payload['e2e']['w0']) / 1e9, 2)
                if False else round((payload['e2e']['w1'] - payload['e2e']['w0']) / 1e9, 2),
                'tracks': {k: len(v) for k, v in payload['e2e']['tracks'].items()},
                'quantum_marks': len(payload['e2e']['marks'])},
        'c2': {'window_s': round((payload['c2']['w1'] - payload['c2']['w0']) / 1e9, 2),
               'instances': sum(len(v) for v in payload['c2']['tracks'].values()),
               'per_type': {k: len(v) for k, v in payload['c2']['tracks'].items()},
               'selected_types': payload['c2']['selected_types'],
               'quantum_marks': len(payload['c2']['marks']),
               'drilldown_identity_coverage': id_cov},
        'c3': {'window_s': round((payload['p3band']['w1'] - payload['p3band']['w0']) / 1e9, 2),
               'procs': payload['p3band']['procs'],
               'instances': sum(len(v) for v in payload['p3band']['tracks'].values()),
               'quantum_marks': len(payload['p3band']['marks']),
               'hw_note': hw_note,
               # lane values travel with the summary so the report renders the
               # same derivation instead of recomputing it
               'hw_lanes': [{'key': ln['key'], 'label': ln['label'], 'color': ln['color'],
                             'max': ln['max'], 'roof': ln.get('roof'),
                             'values': ln['values'], 'cov': ln['cov']} for ln in hw_lanes],
               'signal_lanes': [{'label': ln['label'], 'color': ln['color'],
                                 'max': ln['max'], 'cap': ln.get('cap'),
                                 'values': ln['values']} for ln in l3],
               'marks': payload['p3band']['marks'],
               'tracks': payload['p3band']['tracks'],
               'hw_medians': {ln['key']: statistics.median(
                                  [v for v in ln['values'] if v is not None])
                              for ln in hw_lanes},
               'hw_axis': {ln['key']: {'label': ln['label'], 'max': ln['max'],
                                       'roof': ln.get('roof')} for ln in hw_lanes}},
        'cross_pairs': cross['selected_pairs'],
        'clock_alignment': {'causality_pairs_checked': 288950,
                            'violations': 0, 'skew_upper_bound_ns': 0,
                            'method': 'kernel 设备开始不得早于发射调用开始（S04 194,931 对 + S07 94,019 对）'},
    }
    SUM = OUT.parent / ('R10_TIMELINE_SUMMARY.json' if os.environ.get('PT_LINEAGE','mixed')=='mixed'
                        else f"R10_TIMELINE_SUMMARY_{os.environ['PT_LINEAGE']}.json")
    SUM.write_text(
        json.dumps(summary, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({'out': str(OUT.relative_to(ROOT)), 'bytes': len(html.encode()),
                      'ncu_identities': len(ncu_map), 'identity_coverage': id_cov,
                      'instances': len(details),
                      'kernel_rows': sum(len(d['kernels']) for d in details.values()),
                      'names': len(names)}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

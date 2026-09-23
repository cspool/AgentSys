"""v2 pass-1 analysis for the interactive workload: where does step time go?

Outputs: per-step device-busy share (kernel union / step span) over the serving
span, split by step duration class; NVTX process-type latency shares.
"""
import json, sqlite3, sys
from collections import defaultdict

db = sqlite3.connect(sys.argv[1])
db.row_factory = sqlite3.Row

def nvtx_ranges(like):
    q = """SELECT ne.start, ne.end, COALESCE(ne.text, s.value) t
           FROM NVTX_EVENTS ne LEFT JOIN StringIds s ON ne.textId = s.id
           WHERE COALESCE(ne.text, s.value) LIKE ? AND ne.end IS NOT NULL"""
    return [(r["start"], r["end"], r["t"]) for r in db.execute(q, (like,))]

steps = sorted(nvtx_ranges("w.engine: process_engine_step%"))
kerns = sorted((r["start"], r["end"]) for r in db.execute(
    "SELECT start, end FROM CUPTI_ACTIVITY_KIND_KERNEL"))
print(f"steps={len(steps)} kernels={len(kerns)}")
if not steps or not kerns:
    sys.exit("no data")

# serving span = steps overlapping kernels (skip load/warmup idle steps)
k0, k1 = kerns[0][0], kerns[-1][1]

def union_in(lo, hi):
    tot, cur_s, cur_e = 0, None, None
    import bisect
    i = bisect.bisect_left(kerns, (lo, -1)) 
    while i > 0 and kerns[i-1][1] > lo: i -= 1
    for s, e in kerns[i:]:
        if s >= hi: break
        s, e = max(s, lo), min(e, hi)
        if e <= s: continue
        if cur_s is None: cur_s, cur_e = s, e
        elif s <= cur_e: cur_e = max(cur_e, e)
        else: tot += cur_e - cur_s; cur_s, cur_e = s, e
    if cur_s is not None: tot += cur_e - cur_s
    return tot

rows = []
for s, e, _ in steps:
    if e < k0 or s > k1: continue
    dur = e - s
    if dur <= 0: continue
    busy = union_in(s, e)
    rows.append((dur, busy))
rows = [r for r in rows if r[1] > 0]          # steps that ran kernels
tot_dur = sum(r[0] for r in rows); tot_busy = sum(r[1] for r in rows)
rows.sort()
med = rows[len(rows)//2]
print(f"serving steps(with kernels)={len(rows)}")
print(f"overall: step_time={tot_dur/1e9:.2f}s device_busy={tot_busy/1e9:.2f}s "
      f"busy_share={tot_busy/tot_dur:.1%} host_gap_share={1-tot_busy/tot_dur:.1%}")
print(f"median step: dur={med[0]/1e3:.0f}us busy={med[1]/med[0]:.1%}")
# 短步(decode 小批量)与长步(prefill)分开
import statistics
durs = [r[0] for r in rows]
thr = statistics.median(durs) * 2
short = [r for r in rows if r[0] <= thr]; long_ = [r for r in rows if r[0] > thr]
for name, grp in (("short(decode-like)", short), ("long(prefill-like)", long_)):
    if not grp: continue
    d = sum(r[0] for r in grp); b = sum(r[1] for r in grp)
    print(f"{name}: n={len(grp)} time_share={d/tot_dur:.1%} busy={b/d:.1%} gap={1-b/d:.1%}")

# process 类型份额(modproc NVTX: 形如 p.LXX.type/)
proc = defaultdict(int)
for s, e, t in nvtx_ranges("p.L%"):
    ty = t.split(".", 2)[-1].rstrip("/")
    proc[ty] += e - s
top = sorted(proc.items(), key=lambda kv: -kv[1])[:8]
ptot = sum(proc.values()) or 1
print("\nprocess host-interval shares (of all module time):")
for ty, ns in top:
    print(f"  {ty:>14}: {ns/ptot:.1%}")

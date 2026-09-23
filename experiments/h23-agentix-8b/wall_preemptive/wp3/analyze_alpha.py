"""抢占时机对照分析。
三臂等功(K/D/ΣBURST/duty 逐字相同), 唯一变量是 BURST 落在测量窗的前半还是后半。
整体吞吐 STP = G_v + G_p。
"""
import glob, json, os, re, statistics, sys

SOLO_V = 6.696          # MPK solo(MPS) ms/token
SOLO_P = {'tc': 27286.6, 'dram': 6527.4}   # 抢占者满配额(64TPC) solo, MPS

def victim_lat(ax, arm, rep):
    p = f"/tmp/mpk_alpha_{ax}_{arm}_r{rep}.log"
    if not os.path.exists(p): return None
    m = re.findall(r'per-token latency: ([0-9.]+)', open(p, errors='ignore').read())
    return float(m[-1]) if m else None

rows = []
for f in sorted(glob.glob('out/alpha_*_r*.json')):
    d = json.load(open(f))
    m = re.match(r'alpha_([a-z]+)_([a-z_]+)_r(\d+)\.json', os.path.basename(f))
    ax, arm, rep = m.group(1), m.group(2), int(m.group(3))
    lat = victim_lat(ax, arm, rep)
    if not d.get('onset_detected') or lat is None: 
        rows.append(dict(ax=ax, arm=arm, rep=rep, bad=True)); continue
    gv = SOLO_V / lat
    gp = d['win_rate'] / SOLO_P[ax]
    rows.append(dict(ax=ax, arm=arm, rep=rep, bad=False, lat=lat, gv=gv,
                     win_rate=d['win_rate'], gp=gp, stp=gv+gp,
                     K=d['K'], duty=d['duty'], n_sw=d['n_applied'], win=d['win_secs']))

print(f"{'轴':<6}{'臂':<8}{'rep':>4}{'K':>4}{'duty':>7}{'切换':>5}{'受害者ms':>10}{'G_v':>8}{'抢占者/s':>10}{'G_p':>8}{'STP':>8}")
for r in rows:
    if r['bad']: print(f"{r['ax']:<6}{r['arm']:<8}{r['rep']:>4}  -- 数据不全"); continue
    print(f"{r['ax']:<6}{r['arm']:<8}{r['rep']:>4}{r['K']:>4}{r['duty']:>7.3f}{r['n_sw']:>5}"
          f"{r['lat']:>10.3f}{r['gv']:>8.4f}{r['win_rate']:>10.0f}{r['gp']:>8.4f}{r['stp']:>8.4f}")

ok = [r for r in rows if not r['bad']]
if len(ok) >= 3:
    print("\n=== 按臂聚合 ===")
    print(f"{'臂':<8}{'n':>3}{'G_v':>9}{'G_p':>9}{'STP':>9}")
    byarm = {}
    for r in ok: byarm.setdefault(r['arm'], []).append(r)
    for arm in ['early', 'spread', 'late']:
        v = byarm.get(arm, [])
        if not v: continue
        print(f"{arm:<8}{len(v):>3}{statistics.mean(x['gv'] for x in v):>9.4f}"
              f"{statistics.mean(x['gp'] for x in v):>9.4f}{statistics.mean(x['stp'] for x in v):>9.4f}")
    if 'late' in byarm and 'early' in byarm:
        dl = statistics.mean(x['stp'] for x in byarm['late'])
        de = statistics.mean(x['stp'] for x in byarm['early'])
        print(f"\nΔSTP(late - early) = {dl-de:+.4f}   (wall-aware 减 anti-wall)")
json.dump(rows, open('out/ALPHA.json','w'), ensure_ascii=False, indent=1)

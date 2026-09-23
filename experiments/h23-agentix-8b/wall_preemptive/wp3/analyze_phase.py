"""相位择时对照分析。整体吞吐 STP = G_v + G_p。"""
import glob, json, os, re, statistics
SOLO_V = 815.76           # 受害者 solo iter/s (两次独立测量 813.43 / 815.76, 差 0.3%)
SOLO_P = {'tc': 26900.0, 'dram': 6527.4}   # 抢占者满配额 solo
rows=[]
for f in sorted(glob.glob('out/co_*_r*.json')):
    m=re.match(r'co_([a-z]+)_([a-z0-9]+)_r(\d+)\.json', os.path.basename(f))
    if not m: continue
    ax,arm,rep=m.group(1),m.group(2),int(m.group(3))
    c=json.load(open(f))
    vf=f'out/vic_{ax}_{arm}_r{rep}.json'
    if not os.path.exists(vf): rows.append(dict(ax=ax,arm=arm,rep=rep,bad='受害者缺')); continue
    v=json.load(open(vf))
    gv=v['throughput_iter_per_s']/SOLO_V
    gp=c['win_rate']/SOLO_P[ax]
    rows.append(dict(ax=ax,arm=arm,rep=rep,bad=None,
        K=c['K'], duty=c['duty'], alpha=c['alpha_realized'], torn=c['beacon_torn'],
        ep=c['n_epoch'], epf=c['n_epoch_fire'],
        v_iter=v['throughput_iter_per_s'], gv=gv, p_rate=c['win_rate'], gp=gp, stp=gv+gp,
        v_med0=v['median_ms']['0'], v_med1=v['median_ms']['1']))
print(f"{'臂':<7}{'rep':>4}{'K':>4}{'duty':>7}{'实测α':>8}{'受害者it/s':>11}{'G_v':>8}{'抢占者/s':>10}{'G_p':>8}{'STP':>8}{'信标撕裂':>9}")
for r in rows:
    if r['bad']: print(f"{r['arm']:<7}{r['rep']:>4}  {r['bad']}"); continue
    print(f"{r['arm']:<7}{r['rep']:>4}{r['K']:>4}{r['duty']:>7.3f}{r['alpha']:>8.3f}"
          f"{r['v_iter']:>11.1f}{r['gv']:>8.4f}{r['p_rate']:>10.0f}{r['gp']:>8.4f}{r['stp']:>8.4f}{r['torn']:>9}")
ok=[r for r in rows if not r['bad']]
if ok:
    print("\n=== 按臂聚合 ===")
    by={}
    for r in ok: by.setdefault(r['arm'],[]).append(r)
    print(f"{'臂':<7}{'n':>3}{'实测α':>8}{'G_v':>9}{'G_p':>9}{'STP':>9}")
    for arm in ['a100','a050','a000']:
        v=by.get(arm,[])
        if not v: continue
        print(f"{arm:<7}{len(v):>3}{statistics.mean(x['alpha'] for x in v):>8.3f}"
              f"{statistics.mean(x['gv'] for x in v):>9.4f}{statistics.mean(x['gp'] for x in v):>9.4f}"
              f"{statistics.mean(x['stp'] for x in v):>9.4f}")
    if 'a100' in by and 'a000' in by:
        d=statistics.mean(x['stp'] for x in by['a100'])-statistics.mean(x['stp'] for x in by['a000'])
        b=statistics.mean(x['stp'] for x in by['a000'])
        print(f"\nΔSTP(a100 wall-aware − a000 anti-wall) = {d:+.4f}  ({100*d/b:+.2f}%)")
json.dump(rows, open('out/PHASE_RESULT.json','w'), ensure_ascii=False, indent=1)

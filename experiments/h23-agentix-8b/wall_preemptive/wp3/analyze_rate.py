"""产出率感知抢占分析。受害者效用货币 = serving token/s = Σ_ph B_d(ph) x n_iter(ph)/secs。"""
import glob, json, os, re, statistics
BD={'2':64,'5':1}; SOLO_P=26900.0
sv=json.load(open('out/solo_pod_w25.json'))
SOLO_V=sum(BD[p]*sv['n_iter'][p] for p in BD)/sv['secs']
rows=[]
for f in sorted(glob.glob('out/m_pod_w25_susp_tc_*_co.json')):
    m=re.match(r'm_pod_w25_susp_tc_(a\d+)_r(\d+)_co\.json', os.path.basename(f))
    if not m: continue
    arm,rep=m.group(1),int(m.group(2))
    vf=f.replace('_co.json','_vic.json')
    if not os.path.exists(vf): continue
    c=json.load(open(f)); v=json.load(open(vf))
    tok=sum(BD[p]*v['n_iter'].get(p,0) for p in BD)/v['secs']
    gv=tok/SOLO_V; gp=c['win_rate']/SOLO_P
    rows.append(dict(arm=arm,rep=rep,tok=tok,gv=gv,gp=gp,stp=gv+gp,duty=c['duty'],susp=v.get('suspended_s',0)))
print(f"solo 受害者 = {SOLO_V:.0f} tok/s (全饱和 38.6k <-> 长尾排空 6.2k, 对比 6.2x, 均 GPU-busy)")
NAME={'a100':'产出率感知(抢低产出时刻)','a050':'相位盲(on-demand)','a000':'反向(抢高产出时刻)'}
print(f"{'臂':<24}{'rep':>4}{'duty':>7}{'挂起s':>7}{'tok/s':>8}{'G_v':>8}{'G_p':>8}{'STP':>8}")
for r in rows:
    print(f"{NAME[r['arm']]:<24}{r['rep']:>4}{r['duty']:>7.3f}{r['susp']:>7.1f}{r['tok']:>8.0f}{r['gv']:>8.4f}{r['gp']:>8.4f}{r['stp']:>8.4f}")
by={}
for r in rows: by.setdefault(r['arm'],[]).append(r)
agg={a:{k:statistics.mean(x[k] for x in v) for k in ('gv','gp','stp')} for a,v in by.items()}
if 'a100' in agg and 'a000' in agg:
    d=(agg['a100']['stp']-agg['a000']['stp'])/agg['a000']['stp']
    dv=(agg['a100']['gv']-agg['a000']['gv'])/agg['a000']['gv']
    print(f"\n感知 vs 反向: STP {100*d:+.1f}%  受害者token {100*dv:+.1f}%")
if 'a100' in agg and 'a050' in agg:
    d=(agg['a100']['stp']-agg['a050']['stp'])/agg['a050']['stp']
    dv=(agg['a100']['gv']-agg['a050']['gv'])/agg['a050']['gv']
    print(f"感知 vs 盲:   STP {100*d:+.1f}%  受害者token {100*dv:+.1f}%")

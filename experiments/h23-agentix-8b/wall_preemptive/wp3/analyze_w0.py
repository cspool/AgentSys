"""W=0 场景: wall-p 感知调度 vs 相位盲调度的吞吐差。
受害者效用 = 忙相位(全饱和,ph=2)迭代速率; 工具期(ph=3)本就零产出。
a100=感知(全部对齐空闲窗) a050=相位盲均匀(现实 on-demand) a000=最差(全打忙相)"""
import glob, json, os, re, statistics
SOLO_P=26900.0
sv=json.load(open('out/solo_pod_w23.json'))
SOLO_V=sv['n_iter']['2']/sv['secs']
rows=[]
for f in sorted(glob.glob('out/m_pod_w23_susp_tc_*_co.json')):
    m=re.match(r'm_pod_w23_susp_tc_(a\d+)_r(\d+)_co\.json', os.path.basename(f))
    if not m: continue
    arm,rep=m.group(1),int(m.group(2))
    vf=f.replace('_co.json','_vic.json')
    if not os.path.exists(vf): continue
    c=json.load(open(f)); v=json.load(open(vf))
    gv=(v['n_iter']['2']/v['secs'])/SOLO_V
    gp=c['win_rate']/SOLO_P
    rows.append(dict(arm=arm,rep=rep,gv=gv,gp=gp,stp=gv+gp,K=c['K'],duty=c['duty'],
                     alpha=c['alpha_realized'],susp=v.get('suspended_s',0)))
print(f"solo 受害者忙相速率 = {SOLO_V:.1f} iter/s")
print(f"{'臂':<6}{'rep':>4}{'K':>5}{'duty':>7}{'α':>6}{'挂起s':>7}{'G_v(忙相)':>10}{'G_p':>8}{'STP':>8}")
for r in rows:
    print(f"{r['arm']:<6}{r['rep']:>4}{r['K']:>5}{r['duty']:>7.3f}{r['alpha']:>6.2f}{r['susp']:>7.1f}"
          f"{r['gv']:>10.4f}{r['gp']:>8.4f}{r['stp']:>8.4f}")
# 按 duty 分轮: rep1/2=0.405, rep3/4=0.467
for tag,sel in [('轮1 duty~0.405', lambda r: r['rep']<=2), ('轮2 duty~0.467', lambda r: r['rep']>=3)]:
    sub=[r for r in rows if sel(r)]
    if not sub: continue
    print(f"\n===== {tag} =====")
    by={}
    for r in sub: by.setdefault(r['arm'],[]).append(r)
    import statistics as st
    NAME={'a100':'wall-p 感知(对齐空闲)','a050':'相位盲均匀(on-demand)','a000':'最差(全打忙相)'}
    agg={}
    for arm in ['a100','a050','a000']:
        v=by.get(arm)
        if not v: continue
        f=lambda k: st.mean(x[k] for x in v)
        agg[arm]=dict(gv=f('gv'),gp=f('gp'),stp=f('stp'))
        print(f"{NAME[arm]:<22}{len(v):>3}{f('gv'):>9.4f}{f('gp'):>9.4f}{f('stp'):>9.4f}")
    if 'a100' in agg and 'a050' in agg:
        dd=(agg['a100']['stp']-agg['a050']['stp'])/agg['a050']['stp']
        dv=(agg['a100']['gv']-agg['a050']['gv'])/agg['a050']['gv']
        print(f"  感知 vs 相位盲: STP {100*dd:+.1f}%  受害者 {100*dv:+.1f}%  目标>=30%: {'达成' if dd>=0.30 or dv>=0.30 else '未达成'}")
    if 'a100' in agg and 'a000' in agg:
        dd=(agg['a100']['stp']-agg['a000']['stp'])/agg['a000']['stp']
        print(f"  感知 vs 最差:   STP {100*dd:+.1f}%")

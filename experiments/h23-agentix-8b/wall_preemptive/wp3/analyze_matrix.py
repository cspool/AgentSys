"""五机制 x 抢占时机 矩阵分析。整体吞吐 STP = G_v + G_p。
三臂 K/duty 构造性等同, 唯一变量是 BURST 落在受害者的哪个墙型相位。"""
import glob, json, os, re, statistics
SOLO_P={'tc':26900.0,'dram':6527.4}
def solo_v(mech):
    p=f'out/solo_{mech}.json'
    return json.load(open(p))['throughput_iter_per_s'] if os.path.exists(p) else None
MECH_DESC={'serial':'无kernel内并发','streams':'流级(L3 channel)','hfuse':'CTA内warp分区',
           'pod2':'SM内 2 CTA','pod4':'SM内 4 CTA'}
rows=[]
for f in sorted(glob.glob('out/m_*_co.json')):
    if '_w02_' in f or '_w12_' in f: continue  # 其他 wave 的对照单独分析
    m=re.match(r'm_([a-z0-9]+)_(?:w01_)?([a-z]+)_(a\d+)_r(\d+)_co\.json', os.path.basename(f))
    if not m: continue
    mech,ax,arm,rep=m.group(1),m.group(2),m.group(3),int(m.group(4))
    vf=f.replace('_co.json','_vic.json')
    if not os.path.exists(vf): continue
    c=json.load(open(f)); v=json.load(open(vf)); sv=solo_v(mech)
    if not sv: continue
    gv=v['throughput_iter_per_s']/sv; gp=c['win_rate']/SOLO_P[ax]
    rows.append(dict(mech=mech,ax=ax,arm=arm,rep=rep,gv=gv,gp=gp,stp=gv+gp,
                     K=c['K'],duty=c['duty'],alpha=c['alpha_realized'],torn=c['beacon_torn']))
if not rows: print("暂无完成的格子"); raise SystemExit
by={}
for r in rows: by.setdefault((r['mech'],r['ax'],r['arm']),[]).append(r)
print(f"{'机制':<8}{'并发层':<16}{'轴':<5}{'臂':<7}{'n':>3}{'K':>5}{'duty':>7}{'α':>6}{'G_v':>8}{'G_p':>8}{'STP':>8}")
for mech in ['serial','streams','hfuse','pod2','pod4']:
    for ax in ['tc','dram']:
        for arm in ['a100','a050','a000']:
            v=by.get((mech,ax,arm))
            if not v: continue
            f=lambda k: statistics.mean(x[k] for x in v)
            print(f"{mech:<8}{MECH_DESC[mech]:<16}{ax:<5}{arm:<7}{len(v):>3}{f('K'):>5.0f}{f('duty'):>7.3f}"
                  f"{f('alpha'):>6.2f}{f('gv'):>8.4f}{f('gp'):>8.4f}{f('stp'):>8.4f}")
print(f"\n{'机制':<8}{'并发层':<16}{'轴':<5}{'ΔSTP(a100-a000)':>17}{'%':>8}{'臂内sd':>9}{'效应/噪声':>10}")
summ={}
for mech in ['serial','streams','hfuse','pod2','pod4']:
    for ax in ['tc','dram']:
        a1,a0=by.get((mech,ax,'a100')),by.get((mech,ax,'a000'))
        if not (a1 and a0): continue
        m1=statistics.mean(x['stp'] for x in a1); m0=statistics.mean(x['stp'] for x in a0)
        sd=max([statistics.stdev([x['stp'] for x in a1]) if len(a1)>1 else 0,
                statistics.stdev([x['stp'] for x in a0]) if len(a0)>1 else 0, 1e-6])
        d=m1-m0
        print(f"{mech:<8}{MECH_DESC[mech]:<16}{ax:<5}{d:>+17.4f}{100*d/m0:>8.2f}{sd:>9.5f}{abs(d)/sd:>10.1f}")
        summ[f'{mech}|{ax}']=dict(delta=d,pct=100*d/m0,sd=sd,a100=m1,a000=m0,n=len(a1))
json.dump({'rows':rows,'summary':summ}, open('out/MATRIX5.json','w'), ensure_ascii=False, indent=1)

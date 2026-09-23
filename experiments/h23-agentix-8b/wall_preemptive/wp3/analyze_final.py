"""最终矩阵: 抢占者资源轴 x 抢占时机 alpha -> 整体吞吐 STP"""
import glob, json, os, re, statistics
SOLO_V=815.76; SOLO_P={'tc':26900.0,'dram':6527.4}
R={}
for f in sorted(glob.glob('out/co_*_r*.json')):
    m=re.match(r'co_([a-z]+)_(a\d+)_r(\d+)\.json', os.path.basename(f))
    if not m: continue
    ax,arm,rep=m.group(1),m.group(2),int(m.group(3))
    c=json.load(open(f)); vf=f'out/vic_{ax}_{arm}_r{rep}.json'
    if not os.path.exists(vf): continue
    v=json.load(open(vf))
    gv=v['throughput_iter_per_s']/SOLO_V; gp=c['win_rate']/SOLO_P[ax]
    R.setdefault((ax,arm),[]).append(dict(gv=gv,gp=gp,stp=gv+gp,K=c['K'],duty=c['duty'],
                                          alpha=c['alpha_realized'],torn=c['beacon_torn']))
def ms(v,k): return statistics.mean(x[k] for x in v)
def sd(v,k): return statistics.stdev(x[k] for x in v) if len(v)>1 else 0.0
print("最终矩阵 —— 受害者 = POD 融合 kernel 方波(真实论文负载), 全程并发, MPS 合并 context")
print(f"{'抢占者轴':<9}{'臂':<7}{'n':>3}{'α':>6}{'K':>5}{'duty':>7}{'G_v':>9}{'G_p':>9}{'STP':>9}{'STP_sd':>9}")
for ax in ['tc','dram']:
    for arm in ['a100','a050','a000']:
        v=R.get((ax,arm))
        if not v: continue
        print(f"{ax:<9}{arm:<7}{len(v):>3}{ms(v,'alpha'):>6.2f}{ms(v,'K'):>5.0f}{ms(v,'duty'):>7.3f}"
              f"{ms(v,'gv'):>9.4f}{ms(v,'gp'):>9.4f}{ms(v,'stp'):>9.4f}{sd(v,'stp'):>9.5f}")
print()
out={}
for ax in ['tc','dram']:
    a1,a0=R.get((ax,'a100')),R.get((ax,'a000'))
    if not (a1 and a0): continue
    d=ms(a1,'stp')-ms(a0,'stp'); base=ms(a0,'stp')
    # 臂内合并标准差作为噪声尺度
    noise=max(sd(a1,'stp'), sd(a0,'stp'), 1e-6)
    print(f"{ax:>5} 轴: ΔSTP(a100−a000) = {d:+.4f} ({100*d/base:+.2f}%)  臂内sd={noise:.5f}  效应/噪声 = {abs(d)/noise:.1f}x")
    out[ax]=dict(delta=d, pct=100*d/base, noise=noise, ratio=abs(d)/noise,
                 a100=ms(a1,'stp'), a000=ms(a0,'stp'),
                 gv100=ms(a1,'gv'), gv000=ms(a0,'gv'), gp100=ms(a1,'gp'), gp000=ms(a0,'gp'))
if len(out)==2:
    flip = out['tc']['delta']*out['dram']['delta'] < 0
    mono=True
    for ax in ['tc','dram']:
        g=[ms(R[(ax,a)],'gp') for a in ['a000','a050','a100'] if (ax,a) in R]
        mono = mono and (g==sorted(g) or g==sorted(g,reverse=True))
    print(f"\n判决性判据:")
    print(f"  1) 两轴 ΔSTP 符号翻转: {'成立' if flip else '不成立'}  ({out['tc']['delta']:+.4f} vs {out['dram']['delta']:+.4f})")
    print(f"  2) 各轴 α 剂量-反应单调: {'成立' if mono else '不成立'}")
    print(f"  => {'可归因为资源正交性' if (flip and mono) else '不得归因为正交性, 只报时机有收益'}")
    print(f"\n  同等抢占预算下, 两种时机的整体吞吐差距 = {out['tc']['pct']-out['dram']['pct']:.2f} 个百分点")
json.dump({'cells':{f'{k[0]}|{k[1]}':v for k,v in R.items()},'summary':out},
          open('out/FINAL_MATRIX.json','w'), ensure_ascii=False, indent=1)

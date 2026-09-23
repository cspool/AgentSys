"""真实负载 wall 抢占: 干净迭代 vs 被命中迭代 的中位数对比

高并发比例(rho 0.2-0.66)下, "取前 8 个同相位未命中迭代做局部基线"会失效
——大部分迭代都被命中, 找不到干净基线, 配对值被污染成 ~0 甚至负数。
改为: 把整段运行里**从未被任何 burst 覆盖**的迭代作为该相位基线, 与被覆盖的迭代比中位数。
"""
import json, statistics, os, sys

def rows(pfx, mode):
    v=json.load(open(f'{pfx}_{mode}_victim.json')); b=json.load(open(f'{pfx}_{mode}_burst.json'))
    c=json.load(open(f'{pfx}_{mode}_ctl.json'))
    it=v['iters']; hit=set()
    for burst in b['bursts']:
        t0=burst['t_abs']; t1=t0+burst['busy_ms']/1000
        for k,i in enumerate(it):
            if i['t_abs']-i['ms']/1000 < t1 and t0 < i['t_abs']: hit.add(k)
    span=max(i['t_abs'] for i in it)-min(i['t_abs']-i['ms']/1000 for i in it)
    out={'W':v['wall_phase'],'hit_wall':c['hit_wall'],'k':c['k'],
         'rho':sum(x['busy_ms'] for x in b['bursts'])/1000/span,'tp':len(it)/span,
         'burst':statistics.median([x['busy_ms'] for x in b['bursts']]),
         'e2e':statistics.median([x['e2e_ms'] for x in b['bursts']]),'ph':{},'total_dist_s':0.0}
    for p in sorted({i['ph'] for i in it}):
        cl=[i['ms'] for k,i in enumerate(it) if i['ph']==p and k not in hit]
        dt=[i['ms'] for k,i in enumerate(it) if i['ph']==p and k in hit]
        if not cl or not dt: continue
        cM,dM=statistics.median(cl),statistics.median(dt)
        out['ph'][p]={'clean':cM,'hit':dM,'d':dM-cM,'pct':(dM/cM-1)*100,'n_hit':len(dt)}
        out['total_dist_s'] += (dM-cM)*len(dt)/1000
    return out

CO=[('tc','dram','TC(每SM私有)'),('dram','tc','DRAM(GPU全局)'),('fp32','dram','FP32(每SM私有)')]
print(f"{'共跑者':<16}{'策略':<14}{'落墙':>9}{'rho':>6}{'正交相扰动':>20}{'重叠相扰动':>20}{'总扰动':>9}{'吞吐':>9}")
print('-'*106)
summ={}
for co,orth,desc in CO:
    over=[p for p in ('tc','dram') if p!=orth][0]
    for m in ('valve','random_defer','wall_aware'):
        if not os.path.isfile(f'R_{co}_{m}_victim.json'): continue
        r=rows(f'R_{co}',m); summ[(co,m)]=r
        o=r['ph'].get(orth,{}); v=r['ph'].get(over,{})
        print(f"{desc:<16}{m:<14}{r['hit_wall']:>4}/{r['k']:<4}{r['rho']:>6.2f}"
              f"{o.get('d',float('nan')):>11.3f}ms({o.get('pct',0):+.1f}%)"
              f"{v.get('d',float('nan')):>11.3f}ms({v.get('pct',0):+.1f}%)"
              f"{r['total_dist_s']:>8.3f}s{r['tp']:>8.1f}/s")
    print()
print('='*106)
print(f"{'共跑者':<16}{'正交/重叠 扰动比':>20}{'总扰动 wa/valve':>18}{'吞吐比 wa/valve':>18}")
for co,orth,desc in CO:
    va,wa=summ.get((co,'valve')),summ.get((co,'wall_aware'))
    if not(va and wa): continue
    over=[p for p in ('tc','dram') if p!=orth][0]
    ratio=va['ph'][over]['d']/va['ph'][orth]['d'] if va['ph'].get(orth,{}).get('d') else float('nan')
    print(f"{desc:<16}{ratio:>19.2f}×{wa['total_dist_s']/va['total_dist_s']:>17.3f}{wa['tp']/va['tp']:>18.4f}")

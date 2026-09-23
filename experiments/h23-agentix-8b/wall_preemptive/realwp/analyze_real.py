"""真实负载 wall 抢占的逐事件配对分析 + 绝对吞吐

配对: 每个 burst 对上它命中的受害者迭代, 以该迭代之前**同相位未命中**的 8 个为局部基线。
跨共跑者/跨策略比较一律同时给绝对吞吐(逐事件扰动只在同一组内可比)。
"""
import json, os, statistics, sys, glob

def load(pfx, mode):
    v = json.load(open(f'{pfx}_{mode}_victim.json'))
    b = json.load(open(f'{pfx}_{mode}_burst.json'))
    c = json.load(open(f'{pfx}_{mode}_ctl.json'))
    return v, b, c

def paired(v, b):
    it = v['iters']; hits = {}
    for burst in b['bursts']:
        bt = burst['t_abs']
        cand = [k for k, i in enumerate(it) if i['t_abs'] - i['ms']/1000 <= bt <= i['t_abs']]
        if not cand: continue
        k = cand[0]; itk = it[k]
        prev = [j['ms'] for j in it[max(0, k-60):k] if j['ph'] == itk['ph']][-8:]
        if len(prev) < 4: continue
        hits.setdefault(itk['ph'], []).append(itk['ms'] - statistics.median(prev))
    return hits

pfxs = sys.argv[1:] or sorted({os.path.basename(f).rsplit('_',2)[0]
                               for f in glob.glob('R_*_victim.json')})
print(f"{'共跑者':<8}{'策略':<14}{'落墙':>9}{'命中':>6}"
      f"{'正交相扰动':>11}{'重叠相扰动':>11}{'加权每次':>10}{'受害者吞吐':>11}{'抢占e2e':>9}")
print('-'*92)
res = {}
for pfx in pfxs:
    co = pfx.split('_')[1]
    for mode in ('valve', 'random_defer', 'wall_aware'):
        try: v, b, c = load(pfx, mode)
        except FileNotFoundError: continue
        if not v.get('victim_outlasted_controller', True):
            print(f"{co:<8}{mode:<14}  !! 受害者早退, 数据无效"); continue
        W = v['wall_phase']; other = [p for p in {i['ph'] for i in v['iters']} if p != W][0]
        h = paired(v, b)
        allh = h.get(W, []) + h.get(other, [])
        if not allh: print(f"{co:<8}{mode:<14}  无配对命中"); continue
        it = v['iters']
        span = max(i['t_abs'] for i in it) - min(i['t_abs'] - i['ms']/1000 for i in it)
        tp = len(it)/span
        e2e = statistics.median([x['e2e_ms'] for x in b['bursts']])
        mw = statistics.median(h[W]) if h.get(W) else float('nan')
        mo = statistics.median(h[other]) if h.get(other) else float('nan')
        res[(co, mode)] = dict(per=sum(allh)/len(allh), tp=tp, e2e=e2e, n=len(allh))
        print(f"{co:<8}{mode:<14}{c['hit_wall']:>4}/{c['k']:<4}{len(allh):>6}"
              f"{mw:>9.3f}ms{mo:>9.3f}ms{sum(allh)/len(allh):>8.3f}ms{tp:>10.1f}/s{e2e:>8.0f}ms")
    print()
print('='*92)
print(f"{'共跑者':<8}{'wall_aware vs valve':>22}{'vs random_defer':>18}{'吞吐比(wa/valve)':>18}")
for co in sorted({k[0] for k in res}):
    wa = res.get((co,'wall_aware')); vl = res.get((co,'valve')); rd = res.get((co,'random_defer'))
    if not (wa and vl): continue
    f1 = vl['per']/wa['per'] if wa['per'] else float('nan')
    f2 = rd['per']/wa['per'] if rd and wa['per'] else float('nan')
    print(f"{co:<8}{f1:>21.2f}×{f2:>17.2f}×{wa['tp']/vl['tp']:>17.4f}")

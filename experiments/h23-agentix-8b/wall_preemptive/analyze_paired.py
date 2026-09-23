"""逐事件局部配对分析:每个 burst 对上它真正命中的受害者迭代,
以该迭代之前同相的 8 个未命中迭代为局部基线 → 免疫热漂移,分辨力提升。
要求两端记录同源绝对时钟(time.time)。"""
import json, statistics, sys

prefix = sys.argv[1] if len(sys.argv) > 1 else 'wc'
print(f"{'策略':>12} {'命中':>6} {'墙态':>6} {'饱和':>6} "
      f"{'墙态扰动':>10} {'饱和扰动':>10} {'加权每次':>9} {'抢占者e2e':>10}")
out = {}
for mode in ('valve', 'wall_aware', 'random_defer'):
    try:
        v = json.load(open(f'{prefix}_{mode}_victim.json'))
        b = json.load(open(f'{prefix}_{mode}_burst.json'))
    except FileNotFoundError:
        print(f"{mode:>11}  数据缺"); continue
    iters = [i for i in v['iters'] if 't_abs' in i]
    if not iters:
        print(f"{mode:>11}  无绝对时钟(旧数据)"); continue
    hits = {'w': [], 's': []}
    for burst in b['bursts']:
        bt = burst.get('t_abs')
        if bt is None:
            continue
        # 命中:burst 起点落在该迭代 [t_abs-ms, t_abs] 区间
        cand = [k for k, i in enumerate(iters)
                if i['t_abs'] - i['ms']/1000 <= bt <= i['t_abs']]
        if not cand:
            continue
        k = cand[0]; it = iters[k]
        # 局部基线:该迭代之前同相、未被任何 burst 命中的 8 个
        prev = [j['ms'] for j in iters[max(0, k-40):k] if j['ph'] == it['ph']][-8:]
        if len(prev) < 4:
            continue
        hits[it['ph']].append(it['ms'] - statistics.median(prev))
    tot_n = len(hits['w']) + len(hits['s'])
    if tot_n == 0:
        print(f"{mode:>11}  无配对命中"); continue
    mw = statistics.median(hits['w']) if hits['w'] else float('nan')
    ms_ = statistics.median(hits['s']) if hits['s'] else float('nan')
    wsum = sum(hits['w']) + sum(hits['s'])
    e2e = [x.get('e2e_ms', float('nan')) for x in b['bursts'] if 'e2e_ms' in x]
    e2e_med = statistics.median(e2e) if e2e else float('nan')
    out[mode] = dict(n=tot_n, nw=len(hits['w']), ns=len(hits['s']),
                     mw=mw, ms=ms_, per=wsum/tot_n, e2e=e2e_med)
    print(f"{mode:>11} {tot_n:>6} {len(hits['w']):>8} {len(hits['s']):>8} "
          f"{mw:>10.2f}ms {ms_:>10.2f}ms {wsum/tot_n:>8.2f}ms {e2e_med:>9.0f}ms")
if 'valve' in out and 'wall_aware' in out:
    wa = out['wall_aware']['per']
    print(f"\n→ 对 Valve 的优势: {out['valve']['per']/wa:.2f}×" if wa else "")
    if 'random_defer' in out:
        rd = out['random_defer']
        print(f"→ 对 random_defer(同推迟预算、不看状态)的优势: {rd['per']/wa:.2f}×"
              f"   ← 这一项才证明收益来自墙感知而非推迟本身")
        print(f"   落墙态: valve {out['valve']['nw']}/{out['valve']['n']}, "
              f"random_defer {rd['nw']}/{rd['n']}, wall_aware {out['wall_aware']['nw']}/{out['wall_aware']['n']}")
    print(f"\n帕累托(受害者扰动 ↓ / 抢占者 e2e 延迟 ↑):")
    for m, d in out.items():
        print(f"   {m:>12}: 扰动 {d['per']:.2f}ms, 抢占者 e2e {d['e2e']:.0f}ms")

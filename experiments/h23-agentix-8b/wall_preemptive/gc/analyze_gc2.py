"""逐事件局部配对分析(支持 resize 臂)。"""
import json, os, statistics, sys, glob
pfx = sys.argv[1] if len(sys.argv) > 1 else 'R12'
order = ['valve', 'random_defer', 'wall_aware', 'wall_aware_resize']
found = [m for m in order if os.path.isfile(f'{pfx}_{m}_victim.json')]
print(f"{'策略':<20}{'命中':>6}{'落墙':>6}{'墙态扰动':>11}{'饱和扰动':>11}"
      f"{'加权每次':>10}{'±SE':>8}{'抢占busy':>9}{'抢占e2e':>9}{'抢占分区':>12}")
print('-'*104)
out = {}
for m in found:
    v = json.load(open(f'{pfx}_{m}_victim.json')); b = json.load(open(f'{pfx}_{m}_burst.json'))
    iters = [i for i in v['iters'] if 't_abs' in i]; hits = {'w': [], 's': []}
    for burst in b['bursts']:
        bt = burst['t_abs']
        cand = [k for k, i in enumerate(iters) if i['t_abs']-i['ms']/1000 <= bt <= i['t_abs']]
        if not cand: continue
        k = cand[0]; it = iters[k]
        prev = [j['ms'] for j in iters[max(0, k-40):k] if j['ph'] == it['ph']][-8:]
        if len(prev) < 4: continue
        hits[it['ph']].append(it['ms'] - statistics.median(prev))
    allh = hits['w'] + hits['s']; n = len(allh)
    if not n: print(f"{m:<20} 无配对命中"); continue
    e2e = [x['e2e_ms'] for x in b['bursts']]; busy = [x['busy_ms'] for x in b['bursts']]
    sz = {}
    for x in b['bursts']: sz[x.get('pre_sm', '-')] = sz.get(x.get('pre_sm', '-'), 0) + 1
    out[m] = dict(n=n, nw=len(hits['w']), per=sum(allh)/n,
                  se=statistics.pstdev(allh)/n**0.5,
                  e2e=statistics.median(e2e), busy=statistics.median(busy))
    print(f"{m:<20}{n:>6}{len(hits['w']):>6}"
          f"{(statistics.median(hits['w']) if hits['w'] else float('nan')):>10.2f}ms"
          f"{(statistics.median(hits['s']) if hits['s'] else float('nan')):>10.2f}ms"
          f"{sum(allh)/n:>9.2f}ms{statistics.pstdev(allh)/n**0.5:>7.2f}ms"
          f"{statistics.median(busy):>8.0f}ms{statistics.median(e2e):>8.0f}ms"
          f"{str(sz):>12}")
print()
for ph, name in (('w', '访存墙'), ('s', '全饱和')):
    row = []
    for m in found:
        v = json.load(open(f'{pfx}_{m}_victim.json'))
        x = sorted(i['ms'] for i in v['iters'] if i['ph'] == ph)
        row.append(f"{m}={x[len(x)//2]:.1f}ms" if x else f"{m}=NA")
    print(f"受害者 {name} 中位数: " + '  '.join(row))
print()
if 'wall_aware' in out and 'wall_aware_resize' in out:
    A, B = out['wall_aware'], out['wall_aware_resize']
    print(f"resize vs wall_aware: 扰动 {A['per']:.2f} -> {B['per']:.2f} ms ({B['per']/A['per']:.2f}×), "
          f"抢占者 e2e {A['e2e']:.0f} -> {B['e2e']:.0f} ms ({B['e2e']/A['e2e']:.2f}×)")
    print("  两个轴同时改善 = 帕累托前沿外推" if B['per'] <= A['per'] and B['e2e'] <= A['e2e']
          else "  仅沿前沿移动")
if 'valve' in out:
    for m in ('wall_aware', 'wall_aware_resize'):
        if m in out and out[m]['per']:
            print(f"{m} 对 valve 的扰动优势: {out['valve']['per']/out[m]['per']:.2f}×")

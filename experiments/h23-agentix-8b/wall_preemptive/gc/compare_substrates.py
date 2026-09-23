"""把两种空间共享基底下的三臂结果并排:
  MPS (双进程, SM 共享, 硬件 CILP)  vs  Green Context (单进程, SM 不相交分区)
负载/burst工作量/到达序列/K 完全相同, 唯一变量是基底。
用法: python3 compare_substrates.py <mps_prefix> <gc_prefix>
"""
import json, os, statistics, sys

MODES = ('valve', 'random_defer', 'wall_aware')


def paired(prefix, root):
    out = {}
    for mode in MODES:
        try:
            v = json.load(open(os.path.join(root, f'{prefix}_{mode}_victim.json')))
            b = json.load(open(os.path.join(root, f'{prefix}_{mode}_burst.json')))
        except FileNotFoundError:
            continue
        iters = [i for i in v['iters'] if 't_abs' in i]
        hits = {'w': [], 's': []}
        for burst in b['bursts']:
            bt = burst.get('t_abs')
            if bt is None:
                continue
            cand = [k for k, i in enumerate(iters)
                    if i['t_abs'] - i['ms']/1000 <= bt <= i['t_abs']]
            if not cand:
                continue
            k = cand[0]; it = iters[k]
            prev = [j['ms'] for j in iters[max(0, k-40):k] if j['ph'] == it['ph']][-8:]
            if len(prev) < 4:
                continue
            hits[it['ph']].append(it['ms'] - statistics.median(prev))
        n = len(hits['w']) + len(hits['s'])
        if not n:
            continue
        allh = hits['w'] + hits['s']
        e2e = [x['e2e_ms'] for x in b['bursts'] if 'e2e_ms' in x]
        busy = [x['busy_ms'] for x in b['bursts'] if 'busy_ms' in x]
        out[mode] = dict(
            n=n, nw=len(hits['w']), ns=len(hits['s']),
            mw=statistics.median(hits['w']) if hits['w'] else float('nan'),
            ms=statistics.median(hits['s']) if hits['s'] else float('nan'),
            per=sum(allh)/n,
            sd=statistics.pstdev(allh) if len(allh) > 1 else float('nan'),
            se=(statistics.pstdev(allh)/len(allh)**0.5) if len(allh) > 1 else float('nan'),
            e2e=statistics.median(e2e) if e2e else float('nan'),
            busy=statistics.median(busy) if busy else float('nan'))
    return out


def phase_med(prefix, root, mode, ph):
    try:
        v = json.load(open(os.path.join(root, f'{prefix}_{mode}_victim.json')))
    except FileNotFoundError:
        return float('nan')
    x = sorted(i['ms'] for i in v['iters'] if i['ph'] == ph)
    return x[len(x)//2] if x else float('nan')


mps_pfx = sys.argv[1] if len(sys.argv) > 1 else 'S12'
gc_pfx  = sys.argv[2] if len(sys.argv) > 2 else 'G12'
here = os.path.dirname(os.path.abspath(__file__))
parent = os.path.dirname(here)

subs = [('MPS / SM 共享 (双进程)', mps_pfx, parent),
        ('GreenCtx / SM 不相交 (单进程)', gc_pfx, here)]

print(f"{'基底':<30}{'策略':<14}{'命中':>6}{'落墙':>6}{'墙态扰动':>10}{'饱和扰动':>10}"
      f"{'加权每次':>10}{'±SE':>8}{'抢占busy':>9}{'抢占e2e':>9}")
print('-' * 112)
res = {}
for label, pfx, root in subs:
    r = paired(pfx, root)
    res[label] = r
    for mode in MODES:
        d = r.get(mode)
        if not d:
            continue
        print(f"{label:<30}{mode:<14}{d['n']:>6}{d['nw']:>6}"
              f"{d['mw']:>9.2f}ms{d['ms']:>9.2f}ms{d['per']:>9.2f}ms"
              f"{d['se']:>7.2f}ms{d['busy']:>8.0f}ms{d['e2e']:>8.0f}ms")
    print()

print('=' * 112)
print(f"{'基底':<30}{'vs Valve':>12}{'vs random_defer':>18}{'抢占者 e2e 代价':>18}")
print('-' * 112)
for label, pfx, root in subs:
    r = res[label]
    if 'wall_aware' not in r:
        continue
    wa = r['wall_aware']['per']
    v = r['valve']['per'] / wa if 'valve' in r and wa else float('nan')
    rd = r['random_defer']['per'] / wa if 'random_defer' in r and wa else float('nan')
    print(f"{label:<30}{v:>11.2f}×{rd:>17.2f}×{r['wall_aware']['e2e']:>15.0f}ms")

print()
print('受害者单相位中位数 (无抢占时的基线, 反映静态分区本身的代价):')
print(f"{'基底':<30}{'访存墙':>12}{'全饱和':>12}")
for label, pfx, root in subs:
    print(f"{label:<30}{phase_med(pfx, root, 'valve', 'w'):>10.1f}ms"
          f"{phase_med(pfx, root, 'valve', 's'):>10.1f}ms")

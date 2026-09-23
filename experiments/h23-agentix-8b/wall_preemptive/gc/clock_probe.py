"""green context 下受害者与抢占者用不相交的 SM, 为什么抢占仍有扰动?
候选残余耦合: (a) SM 时钟/功耗, (b) L2, (c) DRAM 带宽。
本探针在受害者两种相位下分别注入 burst, 同步采样 SM 时钟与功耗,
看扰动是否跟随时钟下降 —— 若是, 机制就是功耗墙而非资源争用。
"""
import argparse, json, statistics, subprocess, threading, time
import torch, triton
import triton.language as tl
from torch.cuda.green_contexts import GreenContext


@triton.jit
def stream_fma(x, y, n, reps, inner, GRID: tl.constexpr, BLOCK: tl.constexpr):
    pid = tl.program_id(0); step = GRID * BLOCK * 4
    for _ in range(reps):
        i = pid * BLOCK * 4
        while i < n:
            base = i + tl.arange(0, BLOCK)
            o0, o1, o2, o3 = base, base+BLOCK, base+2*BLOCK, base+3*BLOCK
            m0, m1, m2, m3 = o0 < n, o1 < n, o2 < n, o3 < n
            v0 = tl.load(x+o0, mask=m0); v1 = tl.load(x+o1, mask=m1)
            v2 = tl.load(x+o2, mask=m2); v3 = tl.load(x+o3, mask=m3)
            for _ in range(inner):
                v0 = v0*1.000001+0.000001; v1 = v1*1.000001+0.000001
                v2 = v2*1.000001+0.000001; v3 = v3*1.000001+0.000001
            tl.store(y+o0, v0, mask=m0); tl.store(y+o1, v1, mask=m1)
            tl.store(y+o2, v2, mask=m2); tl.store(y+o3, v3, mask=m3)
            i += step


@triton.jit
def fma_full(x, n, reps, BLOCK: tl.constexpr):
    pid = tl.program_id(0); offs = pid*BLOCK + tl.arange(0, BLOCK); mask = offs < n
    v = tl.load(x+offs, mask=mask)
    for _ in range(reps): v = v*1.000001+0.000001
    tl.store(x+offs, v, mask=mask)


ap = argparse.ArgumentParser()
ap.add_argument('--sm-preemptor', type=int, default=32)
ap.add_argument('--n', type=int, default=120_000_000)
ap.add_argument('--reps-file', default='../reps_v6.json')
ap.add_argument('--burst-reps', type=int, default=1485188)
ap.add_argument('--iters', type=int, default=24, help='每相位的迭代数(前一半无 burst, 后一半有)')
ap.add_argument('--out', default='clock_probe.json')
a = ap.parse_args()

BLOCK, GRID, N = 256, 128*6, a.n
nsm = torch.cuda.get_device_properties(0).multi_processor_count
cache = json.load(open(a.reps_file))
PH = {'w': (cache[f'60:{N}'], 60), 's': (cache[f'290:{N}'], 290)}

vx = torch.randn(N, device='cuda'); vy = torch.empty_like(vx)
bn = GRID * BLOCK; bx = torch.randn(bn, device='cuda')
gc_p = GreenContext.create(a.sm_preemptor, 0)
gc_v = GreenContext.create(nsm - a.sm_preemptor, 0)
st_v, st_p = gc_v.Stream(), gc_p.Stream()

SAMPLES, SAMPLING = [], threading.Event()


def sampler():
    while SAMPLING.is_set():
        try:
            o = subprocess.run(
                ['nvidia-smi', '--query-gpu=clocks.sm,clocks.mem,power.draw,temperature.gpu,'
                 'utilization.gpu', '--format=csv,noheader,nounits', '-i', '0'],
                capture_output=True, text=True, timeout=2).stdout.strip()
            p = [x.strip() for x in o.split(',')]
            SAMPLES.append({'t': time.time(), 'sm_mhz': float(p[0]), 'mem_mhz': float(p[1]),
                            'power_w': float(p[2]), 'temp_c': float(p[3]), 'util': float(p[4])})
        except Exception:
            pass
        time.sleep(0.02)


BURST_ON = threading.Event()
STOP = threading.Event()


def preemptor():
    gc_p.set_context()
    with torch.cuda.stream(st_p):
        fma_full[(bn//BLOCK,)](bx, bn, 8, BLOCK=BLOCK); st_p.synchronize()
        while not STOP.is_set():
            if BURST_ON.wait(timeout=0.05):
                fma_full[(bn//BLOCK,)](bx, bn, a.burst_reps, BLOCK=BLOCK)
                st_p.synchronize()
    gc_p.pop_context()


tp = threading.Thread(target=preemptor, daemon=True); tp.start()
SAMPLING.set(); ts = threading.Thread(target=sampler, daemon=True); ts.start()

gc_v.set_context()
rows = []
with torch.cuda.stream(st_v):
    for ph, (reps, inner) in PH.items():
        stream_fma[(GRID,)](vx, vy, N, 1, inner, GRID=GRID, BLOCK=BLOCK)
    st_v.synchronize()
    for ph, (reps, inner) in PH.items():
        for k in range(a.iters):
            burst = (k % 2 == 1)   # 交替注入: 消除热漂移与顺序混淆
            if burst: BURST_ON.set()
            t0 = time.time()
            s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
            s.record(st_v); stream_fma[(GRID,)](vx, vy, N, reps, inner, GRID=GRID, BLOCK=BLOCK)
            e.record(st_v); st_v.synchronize()
            t1 = time.time()
            if burst: BURST_ON.clear()
            win = [x for x in SAMPLES if t0 + (t1-t0)*0.3 <= x['t'] <= t1]
            rows.append({'ph': ph, 'burst': burst, 'ms': s.elapsed_time(e), 'nsamp': len(win),
                         'sm_mhz': statistics.mean([x['sm_mhz'] for x in win]) if win else None,
                         'power_w': statistics.mean([x['power_w'] for x in win]) if win else None,
                         'temp_c': statistics.mean([x['temp_c'] for x in win]) if win else None})
STOP.set(); SAMPLING.clear(); gc_v.pop_context()
json.dump({'sm_preemptor': a.sm_preemptor, 'rows': rows}, open(a.out, 'w'))

print(f"{'相位':<8}{'burst':<8}{'迭代ms':>10}{'SM时钟MHz':>12}{'功耗W':>9}{'温度C':>8}")
base = {}
for ph in ('w', 's'):
    for bflag in (False, True):
        g = [r for r in rows if r['ph'] == ph and r['burst'] == bflag and r['sm_mhz']]
        if not g: continue
        m = statistics.median([r['ms'] for r in g])
        c = statistics.mean([r['sm_mhz'] for r in g])
        p = statistics.mean([r['power_w'] for r in g])
        t = statistics.mean([r['temp_c'] for r in g])
        base.setdefault(ph, {})[bflag] = (m, c, p)
        print(f"{'访存墙' if ph=='w' else '全饱和':<8}{'有' if bflag else '无':<8}"
              f"{m:>10.1f}{c:>12.0f}{p:>9.1f}{t:>8.1f}")
print()
for ph in ('w', 's'):
    if ph in base and False in base[ph] and True in base[ph]:
        (m0, c0, p0), (m1, c1, p1) = base[ph][False], base[ph][True]
        print(f"{'访存墙' if ph=='w' else '全饱和'}: 迭代 +{m1-m0:.2f}ms ({(m1/m0-1)*100:+.1f}%), "
              f"SM时钟 {c1-c0:+.0f}MHz ({(c1/c0-1)*100:+.1f}%), 功耗 {p1-p0:+.1f}W")

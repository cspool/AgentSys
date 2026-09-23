"""wall_preemptive victim: alternates WALL <-> SATURATED phases and publishes
its current state, so a wall-aware scheduler can time its preemptions.
Same kernel family as victim6 (only arithmetic intensity changes), so the two
phases differ solely in which resources are saturated."""
import argparse, json, os, time
import torch
import triton
import triton.language as tl


@triton.jit
def stream_fma(x, y, n, reps, inner, GRID: tl.constexpr, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    step = GRID * BLOCK * 4
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


ap = argparse.ArgumentParser()
ap.add_argument('--wall-inner', type=int, default=60)       # 深访存墙:算力16%/VRAM86%
                                                            # (对齐真实 decode 相位 SM13.6%/DRAM85.9%)
ap.add_argument('--sat-inner', type=int, default=290)       # 全饱和:算力74%/VRAM83%
ap.add_argument('--pattern', default='w,w,s',               # 墙:饱和 时间占比
                help='每个循环的相序,w=wall s=saturated')
ap.add_argument('--cycles', type=int, default=200)
ap.add_argument('--n', type=int, default=120_000_000)
ap.add_argument('--reps-file', default='reps_v6.json')
ap.add_argument('--state-file', default='/tmp/wp_state.json')
ap.add_argument('--out', required=True)
a = ap.parse_args()

BLOCK, GRID, N = 256, 128*6, a.n
x = torch.randn(N, device='cuda'); y = torch.empty_like(x)
cache = json.load(open(a.reps_file)) if os.path.isfile(a.reps_file) else {}
REPS = {}
for ph, inner in (('w', a.wall_inner), ('s', a.sat_inner)):
    key = f"{inner}:{N}"
    if key not in cache:
        raise SystemExit(f"reps 未校准: {key} — 先跑 victim6.py --inner {inner} --report-rate")
    REPS[ph] = (cache[key], inner)
    stream_fma[(GRID,)](x, y, N, 1, inner, GRID=GRID, BLOCK=BLOCK)
torch.cuda.synchronize()

def pub(ph):
    tmp = a.state_file + '.tmp'
    with open(tmp, 'w') as f:
        json.dump({'phase': 'wall' if ph == 'w' else 'saturated', 't': time.time()}, f)
    os.replace(tmp, a.state_file)

pattern = a.pattern.split(',')
iters, t0 = [], time.monotonic()
for c in range(a.cycles):
    for ph in pattern:
        reps, inner = REPS[ph]
        pub(ph)
        ts = time.monotonic() - t0
        s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
        s.record(); stream_fma[(GRID,)](x, y, N, reps, inner, GRID=GRID, BLOCK=BLOCK)
        e.record(); torch.cuda.synchronize()
        iters.append({'t': ts, 't_abs': time.time(), 'ph': ph,
                      'ms': s.elapsed_time(e)})
mk = time.monotonic() - t0
json.dump({'pattern': a.pattern, 'makespan_s': mk, 'iters': iters}, open(a.out, 'w'))
try: os.remove(a.state_file)
except FileNotFoundError: pass
for ph in ('w', 's'):
    v = sorted(i['ms'] for i in iters if i['ph'] == ph)
    print(f"  {ph}: n={len(v)} med={v[len(v)//2]:.1f}ms")
print(f"makespan={mk:.1f}s")

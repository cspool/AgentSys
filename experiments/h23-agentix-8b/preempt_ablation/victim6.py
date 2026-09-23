"""Realistic victim: ONE kernel family, arithmetic intensity is the only knob.
True DRAM streaming (480MB working set >> 72MB L2, grid-stride, one touch per
pass) with `inner` FMAs per element:

  intensity = inner/4 FLOP/byte ; 4090 ridge ~82 FLOP/byte
  inner ~100 -> memory wall  (<50% compute, >80% DRAM)
  inner ~330 -> all-saturated(>80% compute, >80% DRAM)
  inner ~600 -> compute wall (>80% compute, <50% DRAM)

Same code path for all three states => no structural confound.
"""
import argparse, json, os, time
import torch
import triton
import triton.language as tl


@triton.jit
def stream_fma(x, y, n, reps, inner, GRID: tl.constexpr, BLOCK: tl.constexpr):
    """4-way ILP: four independent FMA chains per thread so the SM is
    throughput-bound, not FMA-latency-bound."""
    pid = tl.program_id(0)
    step = GRID * BLOCK * 4
    for _ in range(reps):
        i = pid * BLOCK * 4
        while i < n:
            base = i + tl.arange(0, BLOCK)
            o0, o1 = base, base + BLOCK
            o2, o3 = base + 2 * BLOCK, base + 3 * BLOCK
            m0, m1 = o0 < n, o1 < n
            m2, m3 = o2 < n, o3 < n
            v0 = tl.load(x + o0, mask=m0)
            v1 = tl.load(x + o1, mask=m1)
            v2 = tl.load(x + o2, mask=m2)
            v3 = tl.load(x + o3, mask=m3)
            for _ in range(inner):
                v0 = v0 * 1.000001 + 0.000001
                v1 = v1 * 1.000001 + 0.000001
                v2 = v2 * 1.000001 + 0.000001
                v3 = v3 * 1.000001 + 0.000001
            tl.store(y + o0, v0, mask=m0)
            tl.store(y + o1, v1, mask=m1)
            tl.store(y + o2, v2, mask=m2)
            tl.store(y + o3, v3, mask=m3)
            i += step


ap = argparse.ArgumentParser()
ap.add_argument('--inner', type=int, required=True)
ap.add_argument('--n', type=int, default=120_000_000)
ap.add_argument('--target-ms', type=float, default=180.0)
ap.add_argument('--cycles', type=int, default=600)
ap.add_argument('--reps-file', default='reps_v6.json')
ap.add_argument('--report-rate', action='store_true')
ap.add_argument('--out', default=None)
a = ap.parse_args()

BLOCK, GRID = 256, 128 * 6          # 满占用:6 blocks/SM x 256 thr
N = a.n
x = torch.randn(N, device='cuda'); y = torch.empty_like(x)


def timed(reps):
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record(); stream_fma[(GRID,)](x, y, N, reps, a.inner, GRID=GRID, BLOCK=BLOCK)
    e.record(); torch.cuda.synchronize()
    return s.elapsed_time(e)


stream_fma[(GRID,)](x, y, N, 1, a.inner, GRID=GRID, BLOCK=BLOCK)
torch.cuda.synchronize()
key = f"{a.inner}:{N}"
cache = json.load(open(a.reps_file)) if os.path.isfile(a.reps_file) else {}
if key in cache:
    reps = cache[key]; ms = timed(reps)
else:
    reps = 1
    while True:
        ms = timed(reps)
        if ms >= a.target_ms * 0.85 or reps > 4096:
            break
        reps = max(int(reps * min(6, a.target_ms / max(ms, 0.05) * 0.9)), reps + 1)
    cache[key] = reps; json.dump(cache, open(a.reps_file, 'w'))

FLOP = N * reps * a.inner * 2
BYTES = N * reps * 8                       # 读 x + 写 y(下界,未计 write-allocate)
sm_pct = FLOP / (ms/1e3) / 82.6e12 * 100
bw_pct = BYTES / (ms/1e3) / 1008e9 * 100
print(f"inner={a.inner} reps={reps} kernel={ms:.1f}ms | 算力 {sm_pct:.0f}%  DRAM {bw_pct:.0f}%",
      flush=True)
if a.report_rate:
    raise SystemExit(0)

iters, t0 = [], time.monotonic()
for c in range(a.cycles):
    iters.append({'t': time.monotonic()-t0, 'ph': f'i{a.inner}', 'ms': timed(reps)})
if a.out:
    json.dump({'inner': a.inner, 'reps': reps, 'sm_pct': sm_pct, 'bw_pct': bw_pct,
               'makespan_s': time.monotonic()-t0, 'iters': iters}, open(a.out, 'w'))
v = sorted(i['ms'] for i in iters)
print(f"n={len(iters)} med={v[len(v)//2]:.2f}ms")

"""Three-axis victim: tensor cores / FP32 CUDA cores / VRAM bandwidth.
On Ada these are independent hardware, so W (resource-seconds destroyed per ms
of delay) can range from 1 (single wall) to 3 (all three saturated).

Knobs:  --dots  accumulating tl.dot per tile  -> tensor-core load
        --inner FP32 FMA chain per element    -> CUDA-core load
        --n     streaming footprint (>> L2)   -> VRAM load
"""
import argparse, json, os, time
import torch
import triton
import triton.language as tl


@triton.jit
def multi_res(x, y, am_ptr, bm_ptr, n, reps, inner, dots,
              M: tl.constexpr, GRID: tl.constexpr, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    ra = tl.arange(0, M)
    am = tl.load(am_ptr + ra[:, None] * M + ra[None, :])
    bm = tl.load(bm_ptr + ra[:, None] * M + ra[None, :])
    acc = tl.zeros((M, M), dtype=tl.float32)
    step = GRID * BLOCK * 4
    for _ in range(reps):
        i = pid * BLOCK * 4
        while i < n:
            base = i + tl.arange(0, BLOCK)
            o0, o1, o2, o3 = base, base + BLOCK, base + 2*BLOCK, base + 3*BLOCK
            m0, m1, m2, m3 = o0 < n, o1 < n, o2 < n, o3 < n
            v0 = tl.load(x + o0, mask=m0); v1 = tl.load(x + o1, mask=m1)
            v2 = tl.load(x + o2, mask=m2); v3 = tl.load(x + o3, mask=m3)
            for _ in range(inner):
                v0 = v0 * 1.000001 + 0.000001
                v1 = v1 * 1.000001 + 0.000001
                v2 = v2 * 1.000001 + 0.000001
                v3 = v3 * 1.000001 + 0.000001
            for _ in range(dots):
                acc = tl.dot(am, bm, acc)          # tensor cores(累加,不可外提)
            g = tl.sum(acc) * 1e-30
            tl.store(y + o0, v0 + g, mask=m0); tl.store(y + o1, v1 + g, mask=m1)
            tl.store(y + o2, v2 + g, mask=m2); tl.store(y + o3, v3 + g, mask=m3)
            i += step


ap = argparse.ArgumentParser()
ap.add_argument('--inner', type=int, default=0)
ap.add_argument('--dots', type=int, default=0)
ap.add_argument('--n', type=int, default=120_000_000)
ap.add_argument('--tile', type=int, default=32)
ap.add_argument('--target-ms', type=float, default=180.0)
ap.add_argument('--cycles', type=int, default=600)
ap.add_argument('--reps-file', default='reps_v7.json')
ap.add_argument('--report-rate', action='store_true')
ap.add_argument('--out', default=None)
a = ap.parse_args()

BLOCK, GRID, M = 256, 128 * 6, a.tile
N = a.n
x = torch.randn(N, device='cuda'); y = torch.empty_like(x)
am = torch.randn(M, M, device='cuda', dtype=torch.bfloat16)
bm = torch.randn(M, M, device='cuda', dtype=torch.bfloat16)


def timed(reps):
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record()
    multi_res[(GRID,)](x, y, am, bm, N, reps, a.inner, a.dots,
                       M=M, GRID=GRID, BLOCK=BLOCK)
    e.record(); torch.cuda.synchronize()
    return s.elapsed_time(e)


timed(1)
key = f"{a.inner}:{a.dots}:{N}:{M}"
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

n_tiles = (N / (BLOCK * 4)) * reps * GRID / GRID   # 每 kernel 的 tile 迭代次数
iters_total = reps * (N / (GRID * BLOCK * 4)) * GRID
FP32 = N * reps * a.inner * 2
TC = iters_total * a.dots * 2 * M**3
BYTES = N * reps * 8
fp32_pct = FP32/(ms/1e3)/82.6e12*100
tc_pct = TC/(ms/1e3)/165.2e12*100        # Ada bf16 dense tensor peak
bw_pct = BYTES/(ms/1e3)/1008e9*100
print(f"inner={a.inner} dots={a.dots} reps={reps} kernel={ms:.1f}ms | "
      f"FP32 {fp32_pct:.0f}%  TC {tc_pct:.0f}%  VRAM {bw_pct:.0f}%", flush=True)
if a.report_rate:
    raise SystemExit(0)

iters, t0 = [], time.monotonic()
for c in range(a.cycles):
    iters.append({'t': time.monotonic()-t0, 'ms': timed(reps)})
if a.out:
    json.dump({'inner': a.inner, 'dots': a.dots, 'reps': reps,
               'fp32_pct': fp32_pct, 'tc_pct': tc_pct, 'bw_pct': bw_pct,
               'iters': iters}, open(a.out, 'w'))
v = sorted(i['ms'] for i in iters)
print(f"n={len(iters)} med={v[len(v)//2]:.2f}ms")

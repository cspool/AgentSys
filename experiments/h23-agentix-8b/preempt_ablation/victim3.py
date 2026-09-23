"""L2-resident vs streaming victims for the weight-swap (H2D) collision test.
l2   : 30MB working set, fits 4090's 72MB L2 -> L2-hit-bound
dram : 0.9GB streaming -> DRAM-bound, L2 useless
Long kernels (~250ms) via triton internal loop; frozen reps; timestamped."""
import argparse, json, time, os
import torch
import triton
import triton.language as tl


@triton.jit
def sweep(x, y, n, reps, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    mask = offs < n
    for _ in range(reps):
        v = tl.load(x + offs, mask=mask)
        tl.store(y + offs, v * 1.0001, mask=mask)


ap = argparse.ArgumentParser()
ap.add_argument('--mode', choices=['l2', 'dram'], required=True)
ap.add_argument('--seconds', type=float, default=45.0)
ap.add_argument('--target-ms', type=float, default=250.0)
ap.add_argument('--reps-file', default=None)
ap.add_argument('--out', required=True)
a = ap.parse_args()

BLOCK = 1024
n = 7_500_000 if a.mode == 'l2' else 120_000_000    # 30MB vs 0.9GB (fp32)
x = torch.randn(n, device='cuda'); y = torch.empty_like(x)
grid = (triton.cdiv(n, BLOCK),)
def launch(reps):
    sweep[grid](x, y, n, reps, BLOCK=BLOCK)

launch(8); torch.cuda.synchronize()          # JIT 预热
if a.reps_file and os.path.isfile(a.reps_file):
    reps = int(open(a.reps_file).read().strip())
else:
    reps = 8
    while True:
        s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
        s.record(); launch(reps); e.record(); torch.cuda.synchronize()
        ms = s.elapsed_time(e)
        if ms >= a.target_ms * 0.8 or reps > 100_000_000:
            break
        reps = int(reps * max(2, a.target_ms / max(ms, 0.1) * 0.9))
    if a.reps_file:
        open(a.reps_file, 'w').write(str(reps))
print(f"reps={reps}", flush=True)

iters, t0 = [], time.monotonic()
while time.monotonic() - t0 < a.seconds:
    ts = time.monotonic() - t0
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record(); launch(reps); e.record(); torch.cuda.synchronize()
    iters.append({'t': ts, 'ms': s.elapsed_time(e)})
json.dump({'mode': a.mode, 'reps': reps, 'iters': iters}, open(a.out, 'w'))
v = sorted(i['ms'] for i in iters)
print(f"{a.mode}: n={len(iters)} med={v[len(v)//2]:.1f}ms max={v[-1]:.1f}")

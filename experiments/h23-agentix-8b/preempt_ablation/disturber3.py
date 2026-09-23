"""Burst-size sweep disturber: K bursts of a FIXED work size W (ms, solo).
Used to fit victim_inflation = intercept + slope * W per victim phase,
separating per-switch tax (slope, time-slice driven) from fixed cost."""
import argparse, json, time
import torch
import triton
import triton.language as tl


@triton.jit
def fma_full(x, n, reps, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    mask = offs < n
    v = tl.load(x + offs, mask=mask)
    for _ in range(reps):
        v = v * 1.000001 + 0.000001
    tl.store(x + offs, v, mask=mask)


ap = argparse.ArgumentParser()
ap.add_argument('--work-ms', type=float, required=True)
ap.add_argument('--k', type=int, default=40)
ap.add_argument('--period', type=float, default=1.4)
ap.add_argument('--reps-file', default='burst_reps_sweep.json')
ap.add_argument('--out', required=True)
a = ap.parse_args()

BLOCK = 256
n = 128 * 6 * BLOCK
x = torch.randn(n, device='cuda')
fma_full[(n // BLOCK,)](x, n, 8, BLOCK=BLOCK)
torch.cuda.synchronize()

import os
key = f"{a.work_ms}"
cache = json.load(open(a.reps_file)) if os.path.isfile(a.reps_file) else {}
if key in cache:
    reps = cache[key]
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record(); fma_full[(n // BLOCK,)](x, n, reps, BLOCK=BLOCK); e.record()
    torch.cuda.synchronize(); solo = s.elapsed_time(e)
else:
    reps = 1000
    while True:
        s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
        s.record(); fma_full[(n // BLOCK,)](x, n, reps, BLOCK=BLOCK); e.record()
        torch.cuda.synchronize(); solo = s.elapsed_time(e)
        if solo >= a.work_ms * 0.9:
            break
        reps = max(int(reps * min(4, a.work_ms / max(solo, 0.02))), reps + 200)
    cache[key] = reps
    json.dump(cache, open(a.reps_file, 'w'))
print(f"W={a.work_ms}ms reps={reps} solo={solo:.3f}ms", flush=True)

log = []
t0 = time.monotonic()
for i in range(a.k):
    tgt = t0 + (i + 1) * a.period
    while time.monotonic() < tgt:
        time.sleep(0.002)
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record(); fma_full[(n // BLOCK,)](x, n, reps, BLOCK=BLOCK); e.record()
    torch.cuda.synchronize()
    log.append({'i': i, 't': time.monotonic() - t0, 'busy_ms': s.elapsed_time(e)})
json.dump({'work_ms': a.work_ms, 'reps': reps, 'solo_ms': solo, 'k': a.k,
           'bursts': log}, open(a.out, 'w'))
b = sorted(x['busy_ms'] for x in log)
print(f"contended burst med={b[len(b)//2]:.2f}ms (solo {solo:.2f})")

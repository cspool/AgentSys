"""Overload disturber: FULL-GPU compute bursts that CANNOT run concurrently
with a saturating victim -> the driver must CILP-preempt the victim.
Each burst ~15ms of full-occupancy FMA; K bursts on a fixed schedule.
Per-burst own-busy time recorded (to subtract displaced-work from inflation)."""
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
ap.add_argument('--k', type=int, default=30)
ap.add_argument('--period', type=float, default=1.5)
ap.add_argument('--burst-ms', type=float, default=15.0)
ap.add_argument('--out', required=True)
a = ap.parse_args()

BLOCK = 256
n = 128 * 6 * BLOCK          # 128 SM x 6 block/SM 满占用
x = torch.randn(n, device='cuda')
fma_full[(n // BLOCK,)](x, n, 8, BLOCK=BLOCK)
torch.cuda.synchronize()
# 校准 burst 时长
reps = 1000
while True:
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record(); fma_full[(n // BLOCK,)](x, n, reps, BLOCK=BLOCK); e.record()
    torch.cuda.synchronize()
    ms = s.elapsed_time(e)
    if ms >= a.burst_ms * 0.8:
        break
    reps = int(reps * max(2, a.burst_ms / max(ms, 0.05)))
print(f"burst reps={reps} ~{ms:.1f}ms", flush=True)

log = []
t0 = time.monotonic()
for i in range(a.k):
    target = t0 + (i + 1) * a.period
    while time.monotonic() < target:
        time.sleep(0.002)
    ts = time.monotonic()
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record(); fma_full[(n // BLOCK,)](x, n, reps, BLOCK=BLOCK); e.record()
    torch.cuda.synchronize()
    log.append({'i': i, 't': ts - t0, 'busy_ms': s.elapsed_time(e),
                'wall_ms': (time.monotonic() - ts) * 1e3})
json.dump({'k': a.k, 'bursts': log}, open(a.out, 'w'))
med = sorted(b['busy_ms'] for b in log)[a.k // 2]
print(f"full-GPU disturber: {a.k} bursts busy_med={med:.1f}ms")

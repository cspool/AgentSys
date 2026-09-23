"""Equal-count hardware-preemption disturber: an independent CUDA context that
wakes K times on a fixed schedule and launches a tiny burst. Each wake forces
the driver to context-switch the victim in/out (CILP on consumer GPUs).
Burst work is negligible (~us) so the measured cost is the switch, not the
burst's own footprint.
"""
import argparse, json, time
import torch

ap = argparse.ArgumentParser()
ap.add_argument('--k', type=int, default=40)
ap.add_argument('--period', type=float, default=1.0)
ap.add_argument('--out', required=True)
a = ap.parse_args()
x = torch.randn(1024, device='cuda')
torch.cuda.synchronize()
log = []
t0 = time.monotonic()
for i in range(a.k):
    target = t0 + (i + 1) * a.period
    while time.monotonic() < target:
        time.sleep(0.002)
    s = time.monotonic()
    for _ in range(4):
        x = x * 1.0001 + 0.0001
    torch.cuda.synchronize()
    log.append({'i': i, 't': s - t0, 'burst_ms': (time.monotonic() - s) * 1e3})
json.dump({'k': a.k, 'bursts': log}, open(a.out, 'w'))
print(f"disturber: {a.k} bursts, burst_ms_med="
      f"{sorted(b['burst_ms'] for b in log)[a.k//2]:.2f}")

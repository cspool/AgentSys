"""Weight-swap proxy disturber: K pinned-host->GPU copies of 1GB each,
on a fixed schedule. Simulates residency swap-in traffic + L2 write-allocate
pollution. Timestamped per copy."""
import argparse, json, time
import torch

ap = argparse.ArgumentParser()
ap.add_argument('--k', type=int, default=20)
ap.add_argument('--period', type=float, default=2.0)
ap.add_argument('--gb', type=float, default=1.0)
ap.add_argument('--out', required=True)
a = ap.parse_args()
n = int(a.gb * (1 << 30) // 4)
host = torch.randn(n, pin_memory=True)
dev = torch.empty(n, device='cuda')
torch.cuda.synchronize()
log = []
t0 = time.monotonic()
for i in range(a.k):
    target = t0 + (i + 1) * a.period
    while time.monotonic() < target:
        time.sleep(0.002)
    s = time.monotonic()
    dev.copy_(host, non_blocking=True)
    torch.cuda.synchronize()
    log.append({'i': i, 't': s - t0, 'copy_ms': (time.monotonic() - s) * 1e3})
json.dump({'k': a.k, 'bursts': log}, open(a.out, 'w'))
print(f"swapper: {a.k} copies med={sorted(b['copy_ms'] for b in log)[a.k//2]:.0f}ms")

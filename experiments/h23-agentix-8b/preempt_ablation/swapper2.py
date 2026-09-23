"""S2': realistic swap-in proxy — each burst ALLOCATES a fresh GB tensor
(cudaMalloc path, device-synchronizing), copies pinned H2D, then frees.
This is what real model wake/load does; allocation is the big collision."""
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
torch.cuda.synchronize()
# 禁用缓存分配器复用:每次都真 cudaMalloc
log = []
t0 = time.monotonic()
for i in range(a.k):
    target = t0 + (i + 1) * a.period
    while time.monotonic() < target:
        time.sleep(0.002)
    ts = time.monotonic()
    torch.cuda.empty_cache()               # 逼下一次走真实 cudaMalloc
    dev = torch.empty(n, device='cuda')    # cudaMalloc(设备同步)
    dev.copy_(host, non_blocking=True)
    torch.cuda.synchronize()
    del dev
    log.append({'i': i, 't': ts - t0, 'copy_ms': (time.monotonic() - ts) * 1e3})
json.dump({'k': a.k, 'bursts': log}, open(a.out, 'w'))
print(f"swapper2: {a.k} alloc+copy med="
      f"{sorted(b['copy_ms'] for b in log)[a.k//2]:.0f}ms")

"""Victim workload with a chosen resource wall; per-iteration event timing.

--mode dram : triad on ~0.9GB tensors  -> HBM-saturated, SM ~5%
--mode gemm : 4096^3 bf16 matmul loop  -> SM-saturated, DRAM partial slack
Both use full-occupancy grids so CILP state size is comparable (declared).
"""
import argparse, json, time
import torch

ap = argparse.ArgumentParser()
ap.add_argument('--mode', choices=['dram', 'gemm'], required=True)
ap.add_argument('--seconds', type=float, default=45.0)
ap.add_argument('--out', required=True)
a = ap.parse_args()

torch.cuda.init()
if a.mode == 'dram':
    n = 120_000_000                       # 3 x 0.45GB bf16
    x = torch.randn(n, device='cuda', dtype=torch.bfloat16)
    y = torch.randn(n, device='cuda', dtype=torch.bfloat16)
    z = torch.empty_like(x)
    def it():
        torch.add(x, y, out=z)
else:
    m = 4096
    x = torch.randn(m, m, device='cuda', dtype=torch.bfloat16)
    y = torch.randn(m, m, device='cuda', dtype=torch.bfloat16)
    def it():
        torch.matmul(x, y)

for _ in range(10):
    it()
torch.cuda.synchronize()
iters, t0 = [], time.monotonic()
while time.monotonic() - t0 < a.seconds:
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record(); it(); e.record(); torch.cuda.synchronize()
    iters.append(s.elapsed_time(e))
json.dump({'mode': a.mode, 'iters_ms': iters, 'wall_s': time.monotonic() - t0},
          open(a.out, 'w'))
print(f"{a.mode}: n_iter={len(iters)} med={sorted(iters)[len(iters)//2]:.3f}ms")

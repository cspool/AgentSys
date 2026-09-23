"""Long-kernel victims (~300ms each) so mid-kernel bursts FORCE hardware
preemption (CILP). dram: streaming loop over 0.9GB (HBM wall). sm: register
FMA chain (SM wall). Per-kernel event timing."""
import argparse, json, time
import torch
import triton
import triton.language as tl


@triton.jit
def dram_loop(x, y, n, reps, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    mask = offs < n
    for _ in range(reps):
        v = tl.load(x + offs, mask=mask)
        tl.store(y + offs, v * 1.0001, mask=mask)


@triton.jit
def sm_loop(x, n, reps, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    mask = offs < n
    v = tl.load(x + offs, mask=mask)
    for _ in range(reps):
        v = v * 1.000001 + 0.000001
    tl.store(x + offs, v, mask=mask)


ap = argparse.ArgumentParser()
ap.add_argument('--mode', choices=['dram', 'sm'], required=True)
ap.add_argument('--seconds', type=float, default=45.0)
ap.add_argument('--target-ms', type=float, default=300.0)
ap.add_argument('--out', required=True)
ap.add_argument('--reps-file', default=None,
                help='冻结校准:存在则读同一 reps,否则校准后写入(臂间可比性)')
a = ap.parse_args()

BLOCK = 1024
if a.mode == 'dram':
    n = 120_000_000
    x = torch.randn(n, device='cuda'); y = torch.empty_like(x)
    grid = (triton.cdiv(n, BLOCK),)
    def launch(reps):
        dram_loop[grid](x, y, n, reps, BLOCK=BLOCK)
else:
    n = 1024 * 1024
    x = torch.randn(n, device='cuda')
    grid = (triton.cdiv(n, BLOCK),)
    def launch(reps):
        sm_loop[grid](x, n, reps, BLOCK=BLOCK)

# 预热:触发 Triton JIT(首跑含编译,不能进校准)
launch(8)
torch.cuda.synchronize()
# 校准 reps 到 target-ms(或读冻结值)
import os as _os
if a.reps_file and _os.path.isfile(a.reps_file):
    reps = int(open(a.reps_file).read().strip())
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record(); launch(reps); e.record(); torch.cuda.synchronize()
    ms = s.elapsed_time(e)
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
print(f"calibrated reps={reps} kernel={ms:.0f}ms", flush=True)

iters, t0 = [], time.monotonic()
while time.monotonic() - t0 < a.seconds:
    ts = time.monotonic() - t0
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record(); launch(reps); e.record(); torch.cuda.synchronize()
    iters.append({'t': ts, 'ms': s.elapsed_time(e)})
json.dump({'mode': a.mode, 'reps': reps, 'iters': iters,
           'wall_s': time.monotonic() - t0}, open(a.out, 'w'))
v = sorted(x['ms'] for x in iters)
print(f"{a.mode}: n={len(iters)} med={v[len(v)//2]:.1f}ms "
      f"min={v[0]:.1f} max={v[-1]:.1f}")

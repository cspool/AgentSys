"""Victim with (a) a BALANCED wall (both SM and DRAM near-saturated) and
(b) explicit per-block lifetime control at FIXED working set and total work.

modes:
  dram      : streaming, DRAM-saturated / SM idle        (single wall)
  sm        : register FMA chain, SM-saturated / DRAM idle(single wall)
  balanced  : ~ridge-point arithmetic intensity -> BOTH high (no wall)
Block lifetime: --chunks-per-block c; grid = n/(BLOCK*c); block life ~ c*reps.
Working set (n) and total work (n*reps) are invariant in c -> clean mechanism test.
"""
import argparse, json, os, time
import torch
import triton
import triton.language as tl


@triton.jit
def k_stream(x, y, n, reps, cpb, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    for c in range(cpb):
        offs = (pid * cpb + c) * BLOCK + tl.arange(0, BLOCK)
        mask = offs < n
        for _ in range(reps):
            v = tl.load(x + offs, mask=mask)
            tl.store(y + offs, v * 1.0001, mask=mask)


@triton.jit
def k_fma(x, n, reps, cpb, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    for c in range(cpb):
        offs = (pid * cpb + c) * BLOCK + tl.arange(0, BLOCK)
        mask = offs < n
        v = tl.load(x + offs, mask=mask)
        for _ in range(reps):
            v = v * 1.000001 + 0.000001
        tl.store(x + offs, v, mask=mask)


@triton.jit
def k_balanced(x, y, n, reps, cpb, inner, BLOCK: tl.constexpr):
    """load -> `inner` FMAs -> store, repeated `reps` times.
    inner tunes arithmetic intensity toward the roofline ridge."""
    pid = tl.program_id(0)
    for c in range(cpb):
        offs = (pid * cpb + c) * BLOCK + tl.arange(0, BLOCK)
        mask = offs < n
        for _ in range(reps):
            v = tl.load(x + offs, mask=mask)
            for _ in range(inner):
                v = v * 1.000001 + 0.000001
            tl.store(y + offs, v, mask=mask)


ap = argparse.ArgumentParser()
ap.add_argument('--mode', choices=['dram', 'sm', 'balanced'], required=True)
ap.add_argument('--chunks-per-block', type=int, default=1)
ap.add_argument('--inner', type=int, default=330)
ap.add_argument('--n', type=int, default=0, help='覆盖工作集元素数')
ap.add_argument('--target-ms', type=float, default=200.0)
ap.add_argument('--cycles', type=int, default=300)
ap.add_argument('--reps-file', default=None)
ap.add_argument('--phase-file', default='/tmp/victim5_phase.txt')
ap.add_argument('--report-rate', action='store_true',
                help='仅测算力/带宽达成率后退出(用于校准 balanced)')
ap.add_argument('--out', default=None)
a = ap.parse_args()

BLOCK = 1024
N = a.n or {'dram': 120_000_000, 'sm': 1_048_576, 'balanced': 120_000_000}[a.mode]
cpb = a.chunks_per_block
total_chunks = (N + BLOCK - 1) // BLOCK
grid = ((total_chunks + cpb - 1) // cpb,)
x = torch.randn(N, device='cuda')
y = torch.empty_like(x) if a.mode != 'sm' else x


def launch(reps):
    if a.mode == 'dram':
        k_stream[grid](x, y, N, reps, cpb, BLOCK=BLOCK)
    elif a.mode == 'sm':
        k_fma[grid](x, N, reps, cpb, BLOCK=BLOCK)
    else:
        k_balanced[grid](x, y, N, reps, cpb, a.inner, BLOCK=BLOCK)


def timed(reps):
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record(); launch(reps); e.record(); torch.cuda.synchronize()
    return s.elapsed_time(e)


launch(1); torch.cuda.synchronize()          # JIT
key = f"{a.mode}:{cpb}:{a.inner}:{N}"
cache = json.load(open(a.reps_file)) if (a.reps_file and os.path.isfile(a.reps_file)) else {}
if key in cache:
    reps = cache[key]; ms = timed(reps)
else:
    reps = 1
    while True:
        ms = timed(reps)
        if ms >= a.target_ms * 0.85 or reps > 50_000_000:
            break
        reps = max(int(reps * min(8, a.target_ms / max(ms, 0.02) * 0.9)), reps + 1)
    if a.reps_file:
        cache[key] = reps; json.dump(cache, open(a.reps_file, 'w'))
# 达成率(roofline):4090 fp32 82.6 TFLOPS / DRAM 1008 GB/s
FLOP = {'dram': N*reps*1, 'sm': N*reps*2, 'balanced': N*reps*a.inner*2}[a.mode]
BYTES = {'dram': N*reps*8, 'sm': N*8, 'balanced': N*reps*8}[a.mode]
sm_pct = FLOP/(ms/1e3)/82.6e12*100
bw_pct = BYTES/(ms/1e3)/1008e9*100
print(f"{a.mode} cpb={cpb} reps={reps} kernel={ms:.1f}ms grid={grid[0]} "
      f"block_life~{ms/max(grid[0]/128,1):.2f}ms | SM {sm_pct:.0f}% DRAM {bw_pct:.0f}%", flush=True)
if a.report_rate:
    raise SystemExit(0)

iters, t0 = [], time.monotonic()
with open(a.phase_file, 'w') as f:
    f.write(a.mode)
for c in range(a.cycles):
    ts = time.monotonic() - t0
    iters.append({'t': ts, 'ph': a.mode, 'ms': timed(reps)})
mk = time.monotonic() - t0
if a.out:
    json.dump({'mode': a.mode, 'cpb': cpb, 'reps': reps, 'grid': grid[0],
               'sm_pct': sm_pct, 'bw_pct': bw_pct, 'makespan_s': mk,
               'iters': iters}, open(a.out, 'w'))
v = sorted(i['ms'] for i in iters)
print(f"n={len(iters)} med={v[len(v)//2]:.2f}ms makespan={mk:.1f}s")

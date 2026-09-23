"""Phase-alternating victim with FIXED total iterations.
Phases cycle by pattern (e.g. dram,dram,sm). Before each kernel the current
phase is written to a flag file so the disturber can time its bursts.
Overall disturbance metric = total makespan for the fixed iteration count."""
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


@triton.jit
def fma(x, n, reps, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    mask = offs < n
    v = tl.load(x + offs, mask=mask)
    for _ in range(reps):
        v = v * 1.000001 + 0.000001
    tl.store(x + offs, v, mask=mask)


BLOCK = 1024
KER = {}


def make_kernels():
    nd = 120_000_000
    xd = torch.randn(nd, device='cuda'); yd = torch.empty_like(xd)
    nl = 7_500_000
    xl = torch.randn(nl, device='cuda'); yl = torch.empty_like(xl)
    ns = 1024 * 1024
    xs = torch.randn(ns, device='cuda')
    KER['dram'] = lambda r: sweep[(triton.cdiv(nd, BLOCK),)](xd, yd, nd, r, BLOCK=BLOCK)
    KER['l2'] = lambda r: sweep[(triton.cdiv(nl, BLOCK),)](xl, yl, nl, r, BLOCK=BLOCK)
    KER['sm'] = lambda r: fma[(triton.cdiv(ns, BLOCK),)](xs, ns, r, BLOCK=BLOCK)


ap = argparse.ArgumentParser()
ap.add_argument('--pattern', required=True, help='逗号相序,如 dram,dram,sm')
ap.add_argument('--cycles', type=int, required=True)
ap.add_argument('--target-ms', type=float, default=250.0)
ap.add_argument('--reps-file', required=True)
ap.add_argument('--phase-file', default='/tmp/victim_phase.txt')
ap.add_argument('--out', required=True)
a = ap.parse_args()

make_kernels()
for k in KER.values():
    k(8)
torch.cuda.synchronize()

if os.path.isfile(a.reps_file):
    reps = json.load(open(a.reps_file))
else:
    reps = {}
    for name, k in KER.items():
        r = 8
        while True:
            s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
            s.record(); k(r); e.record(); torch.cuda.synchronize()
            ms = s.elapsed_time(e)
            if ms >= a.target_ms * 0.8 or r > 200_000_000:
                break
            r = int(r * max(2, a.target_ms / max(ms, 0.1) * 0.9))
        reps[name] = r
    json.dump(reps, open(a.reps_file, 'w'))
print('reps:', reps, flush=True)

pattern = a.pattern.split(',')
iters = []
t0 = time.monotonic()
for c in range(a.cycles):
    for ph in pattern:
        with open(a.phase_file + '.tmp', 'w') as f:
            f.write(ph)
        os.replace(a.phase_file + '.tmp', a.phase_file)
        ts = time.monotonic() - t0
        s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
        s.record(); KER[ph](reps[ph]); e.record(); torch.cuda.synchronize()
        iters.append({'t': ts, 'ph': ph, 'ms': s.elapsed_time(e)})
mk = time.monotonic() - t0
json.dump({'pattern': a.pattern, 'cycles': a.cycles, 'makespan_s': mk,
           'iters': iters}, open(a.out, 'w'))
print(f"makespan={mk:.2f}s n={len(iters)}")

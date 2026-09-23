"""Trigger-driven preemptor: fires exactly when the controller writes the
trigger file, so both policies inject the SAME number of events with the SAME
work — only the timing differs."""
import argparse, json, os, time
import torch, triton
import triton.language as tl


@triton.jit
def fma_full(x, n, reps, BLOCK: tl.constexpr):
    pid = tl.program_id(0); offs = pid*BLOCK + tl.arange(0, BLOCK); mask = offs < n
    v = tl.load(x+offs, mask=mask)
    for _ in range(reps): v = v*1.000001+0.000001
    tl.store(x+offs, v, mask=mask)


ap = argparse.ArgumentParser()
ap.add_argument('--reps', type=int, required=True)
ap.add_argument('--k', type=int, default=40)
ap.add_argument('--trigger', default='/tmp/wp_trigger')
ap.add_argument('--out', required=True)
a = ap.parse_args()
BLOCK = 256; n = 128*6*BLOCK
x = torch.randn(n, device='cuda')
fma_full[(n//BLOCK,)](x, n, 8, BLOCK=BLOCK); torch.cuda.synchronize()
try: os.remove(a.trigger)
except FileNotFoundError: pass
log, seen, t0 = [], -1, time.time()
while len(log) < a.k and time.time() - t0 < 600:
    try:
        i = int(open(a.trigger).read().strip())
    except Exception:
        time.sleep(0.002); continue
    if i == seen:
        time.sleep(0.002); continue
    seen = i
    ts = time.time()
    trig_mtime = os.path.getmtime(a.trigger)
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record(); fma_full[(n//BLOCK,)](x, n, a.reps, BLOCK=BLOCK); e.record()
    torch.cuda.synchronize()
    log.append({'i': i, 't': ts-t0, 't_abs': ts, 'busy_ms': s.elapsed_time(e),
                'e2e_ms': (time.time()-trig_mtime)*1000})
json.dump({'k': len(log), 'bursts': log}, open(a.out, 'w'))
v = sorted(b['busy_ms'] for b in log)
print(f"disturber4: fired={len(log)} busy_med={v[len(v)//2]:.1f}ms" if v else "no fire")

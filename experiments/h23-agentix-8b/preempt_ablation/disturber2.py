"""Equal-count full-GPU bursts with PLACEMENT STRATEGY:
uniform: fire at each scheduled tick regardless of phase
comp   : fire only when victim phase == 'sm' (complementary window);
         if no window before next tick, fire anyway (forced, logged)
adv    : same but phase == 'dram'
Burst work equal by frozen reps."""
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
ap.add_argument('--strategy', choices=['uniform', 'sm_only', 'dram_only'], required=True)
ap.add_argument('--k', type=int, default=24)
ap.add_argument('--period', type=float, default=1.6)
ap.add_argument('--burst-reps', type=int, required=True)
ap.add_argument('--phase-file', default='/tmp/victim_phase.txt')
ap.add_argument('--out', required=True)
a = ap.parse_args()

BLOCK = 256
n = 128 * 6 * BLOCK
x = torch.randn(n, device='cuda')
fma_full[(n // BLOCK,)](x, n, 8, BLOCK=BLOCK)
torch.cuda.synchronize()


import os as _os


def phase():
    try:
        if time.time() - _os.path.getmtime(a.phase_file) > 2.5:
            return 'ENDED'          # 受害者相位文件停更 → 已结束
        return open(a.phase_file).read().strip()
    except Exception:
        return '?'


want = {'sm_only': 'sm', 'dram_only': 'dram'}.get(a.strategy)
log = []
t0 = time.monotonic()
for i in range(a.k):
    tick = t0 + (i + 1) * a.period
    deadline = tick + a.period * 0.95
    while time.monotonic() < tick:
        time.sleep(0.002)
    forced = False
    if want:
        while phase() not in (want, 'ENDED') and time.monotonic() < deadline:
            time.sleep(0.003)
        forced = phase() != want
    ph = phase()
    post_victim = ph == 'ENDED'
    ts = time.monotonic()
    s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
    s.record(); fma_full[(n // BLOCK,)](x, n, a.burst_reps, BLOCK=BLOCK); e.record()
    torch.cuda.synchronize()
    log.append({'i': i, 't': ts - t0, 'fired_phase': ph, 'forced': forced,
                'post_victim': post_victim, 'busy_ms': s.elapsed_time(e)})
json.dump({'strategy': a.strategy, 'k': a.k, 'bursts': log}, open(a.out, 'w'))
pur = sum(1 for b in log if b['fired_phase'] == (want or b['fired_phase']))
print(f"{a.strategy}: K={a.k} 落点纯度={pur}/{a.k} "
      f"forced={sum(1 for b in log if b['forced'])}")

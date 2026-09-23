"""wall_preemptive, 单进程 green-context 版。

与双进程 MPS 版的唯一结构差异: victim 与 preemptor 是同一进程里的两个线程,
各自绑定一个 green context。因此:
  - 不再需要 MPS(跨进程并发的唯一手段), 空间共享由 green context 直接给出;
  - 分区绑定到不相交的物理 SM(MPS 的 active-thread-percentage 做不到);
  - 相位发布与触发都在进程内, 去掉了文件轮询抖动与跨进程时钟对齐问题。

负载、burst 工作量、到达序列、三条策略与 MPS 版逐字一致, 输出 schema 也一致,
因此 analyze_paired.py 可以直接复用。

substrate:
  none  — 两个 torch stream, 同一个 context, 不做任何分区(对照:说明为什么需要基底)
  split — 静态 green context: victim 拿 128-P 个 SM, preemptor 拿 P 个
"""
import argparse, json, os, random, statistics, threading, time
import torch, triton
import triton.language as tl
from torch.cuda.green_contexts import GreenContext, SUPPORTED


# ---- 与 victim8.py 逐字相同的 kernel(同一 kernel 家族, 只有算术强度变) ----
@triton.jit
def stream_fma(x, y, n, reps, inner, GRID: tl.constexpr, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    step = GRID * BLOCK * 4
    for _ in range(reps):
        i = pid * BLOCK * 4
        while i < n:
            base = i + tl.arange(0, BLOCK)
            o0, o1, o2, o3 = base, base+BLOCK, base+2*BLOCK, base+3*BLOCK
            m0, m1, m2, m3 = o0 < n, o1 < n, o2 < n, o3 < n
            v0 = tl.load(x+o0, mask=m0); v1 = tl.load(x+o1, mask=m1)
            v2 = tl.load(x+o2, mask=m2); v3 = tl.load(x+o3, mask=m3)
            for _ in range(inner):
                v0 = v0*1.000001+0.000001; v1 = v1*1.000001+0.000001
                v2 = v2*1.000001+0.000001; v3 = v3*1.000001+0.000001
            tl.store(y+o0, v0, mask=m0); tl.store(y+o1, v1, mask=m1)
            tl.store(y+o2, v2, mask=m2); tl.store(y+o3, v3, mask=m3)
            i += step


# ---- 与 disturber4.py 逐字相同的 burst kernel ----
@triton.jit
def fma_full(x, n, reps, BLOCK: tl.constexpr):
    pid = tl.program_id(0); offs = pid*BLOCK + tl.arange(0, BLOCK); mask = offs < n
    v = tl.load(x+offs, mask=mask)
    for _ in range(reps): v = v*1.000001+0.000001
    tl.store(x+offs, v, mask=mask)


ap = argparse.ArgumentParser()
ap.add_argument('--substrate', choices=['none', 'split'], default='split')
ap.add_argument('--sm-preemptor', type=int, default=32)
ap.add_argument('--mode', choices=['valve', 'wall_aware', 'random_defer'], required=True)
ap.add_argument('--wall-inner', type=int, default=60)
ap.add_argument('--sat-inner', type=int, default=290)
ap.add_argument('--pattern', default='w,s')
ap.add_argument('--cycles', type=int, default=400)
ap.add_argument('--n', type=int, default=120_000_000)
ap.add_argument('--reps-file', default='../reps_v6.json')
ap.add_argument('--burst-reps', type=int, default=1485188)   # burst_reps_e.json["12.0"]
ap.add_argument('--k', type=int, default=300)
ap.add_argument('--period', type=float, default=2.0)
ap.add_argument('--cool', type=float, default=0.074)
ap.add_argument('--deadline-frac', type=float, default=0.9)
ap.add_argument('--seed', type=int, default=20260921)
ap.add_argument('--delay-file', default=None)
ap.add_argument('--prefix', required=True)
a = ap.parse_args()

dev = torch.device('cuda:0')
torch.cuda.init()
nsm = torch.cuda.get_device_properties(0).multi_processor_count
BLOCK, GRID, N = 256, 128*6, a.n

# ---- 校准的 reps(与 MPS 版共用同一份, 保证受害者负载逐字相同) ----
cache = json.load(open(a.reps_file))
REPS = {}
for ph, inner in (('w', a.wall_inner), ('s', a.sat_inner)):
    key = f"{inner}:{N}"
    if key not in cache:
        raise SystemExit(f"reps 未校准: {key}")
    REPS[ph] = (cache[key], inner)

# ---- 在 primary context 下分配, green context 共享同一地址空间 ----
vx = torch.randn(N, device=dev); vy = torch.empty_like(vx)
bn = GRID * BLOCK
bx = torch.randn(bn, device=dev)

# ---- 基底 ----
gc_v = gc_p = None
if a.substrate == 'split':
    if not SUPPORTED:
        raise SystemExit('此 PyTorch 未编译 green context 支持')
    gc_p = GreenContext.create(a.sm_preemptor, 0)
    gc_v = GreenContext.create(nsm - a.sm_preemptor, 0)
    st_v, st_p = gc_v.Stream(), gc_p.Stream()
else:
    st_v, st_p = torch.cuda.Stream(), torch.cuda.Stream()

# ---- 进程内共享状态(替代 /tmp 文件, 去掉轮询抖动) ----
PHASE = 'w'
TRIG = {'i': -1, 't': 0.0}
TRIG_CV = threading.Condition()
STOP = threading.Event()
victim_log, burst_log = [], []


def victim_thread():
    global PHASE
    if gc_v is not None:
        gc_v.set_context()
    with torch.cuda.stream(st_v):
        for ph, (reps, inner) in REPS.items():
            stream_fma[(GRID,)](vx, vy, N, 1, inner, GRID=GRID, BLOCK=BLOCK)
        torch.cuda.synchronize()
        pattern = a.pattern.split(',')
        t0 = time.monotonic()
        for c in range(a.cycles):
            if STOP.is_set():
                break
            for ph in pattern:
                reps, inner = REPS[ph]
                PHASE = ph
                ts = time.monotonic() - t0
                s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
                s.record(st_v)
                stream_fma[(GRID,)](vx, vy, N, reps, inner, GRID=GRID, BLOCK=BLOCK)
                e.record(st_v); st_v.synchronize()
                victim_log.append({'t': ts, 't_abs': time.time(), 'ph': ph,
                                   'ms': s.elapsed_time(e)})
    if gc_v is not None:
        gc_v.pop_context()


def preemptor_thread():
    if gc_p is not None:
        gc_p.set_context()
    with torch.cuda.stream(st_p):
        fma_full[(bn//BLOCK,)](bx, bn, 8, BLOCK=BLOCK); st_p.synchronize()
        seen = -1
        while not STOP.is_set() and len(burst_log) < a.k:
            with TRIG_CV:
                if TRIG['i'] == seen:
                    TRIG_CV.wait(timeout=0.05)
                    continue
                seen = TRIG['i']; trig_t = TRIG['t']
            ts = time.time()
            s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
            s.record(st_p)
            fma_full[(bn//BLOCK,)](bx, bn, a.burst_reps, BLOCK=BLOCK)
            e.record(st_p); st_p.synchronize()
            burst_log.append({'i': seen, 't_abs': ts, 'busy_ms': s.elapsed_time(e),
                              'e2e_ms': (time.time() - trig_t) * 1000})
    if gc_p is not None:
        gc_p.pop_context()


# ---- 到达序列:两臂同种子 → 同一泊松序列 ----
_rng = random.Random(a.seed)
_sched, _acc = [], 0.0
for _ in range(a.k):
    _acc += max(0.15, min(_rng.expovariate(1.0 / a.period), a.period * 3))
    _sched.append(_acc)

_defers = []
if a.mode == 'random_defer' and a.delay_file:
    _defers = [e['delay_ms'] for e in json.load(open(a.delay_file))['events']]
    random.Random(a.seed + 1).shuffle(_defers)

ctl_log = []


def controller_thread():
    t0 = time.time()
    for i in range(a.k):
        tick = t0 + _sched[i]
        while time.time() < tick:
            time.sleep(0.002)
        budget = (_sched[i+1] - _sched[i]) if i + 1 < len(_sched) else a.period
        deadline = tick + budget * a.deadline_frac
        forced = False
        if a.mode == 'wall_aware':
            while PHASE != 'w' and time.time() < deadline:
                time.sleep(0.003)
            forced = PHASE != 'w'
        elif a.mode == 'random_defer':
            d = _defers[i % len(_defers)] / 1000.0 if _defers else 0.0
            tgt = min(tick + d, deadline)
            while time.time() < tgt:
                time.sleep(0.003)
        ph = PHASE
        with TRIG_CV:
            TRIG['i'] = i; TRIG['t'] = time.time()
            TRIG_CV.notify_all()
        ctl_log.append({'i': i, 't': time.time() - t0, 'fired_phase': 'wall' if ph == 'w' else 'saturated',
                        'forced': forced, 'delay_ms': (time.time() - tick) * 1000})
        if a.mode == 'valve':
            time.sleep(a.cool)
    STOP.set()
    with TRIG_CV:
        TRIG_CV.notify_all()


tv = threading.Thread(target=victim_thread, daemon=True)
tp = threading.Thread(target=preemptor_thread, daemon=True)
tc = threading.Thread(target=controller_thread, daemon=True)
tv.start(); time.sleep(1.0)      # 让受害者先进入稳态
tp.start(); time.sleep(0.5)
tc.start()
tc.join(); tp.join(timeout=30); tv.join(timeout=60)

json.dump({'pattern': a.pattern, 'substrate': a.substrate, 'sm_preemptor': a.sm_preemptor,
           'iters': victim_log}, open(f'{a.prefix}_{a.mode}_victim.json', 'w'))
json.dump({'k': len(burst_log), 'bursts': burst_log}, open(f'{a.prefix}_{a.mode}_burst.json', 'w'))
json.dump({'mode': a.mode, 'k': a.k, 'events': ctl_log,
           'hit_wall': sum(1 for e in ctl_log if e['fired_phase'] == 'wall'),
           'forced': sum(1 for e in ctl_log if e['forced']),
           'mean_delay_ms': sum(e['delay_ms'] for e in ctl_log) / max(len(ctl_log), 1)},
          open(f'{a.prefix}_{a.mode}_ctl.json', 'w'))

for ph in ('w', 's'):
    v = sorted(i['ms'] for i in victim_log if i['ph'] == ph)
    if v: print(f"  victim {ph}: n={len(v)} med={v[len(v)//2]:.1f}ms")
bb = sorted(b['busy_ms'] for b in burst_log)
ee = sorted(b['e2e_ms'] for b in burst_log)
print(f"  burst: n={len(bb)} busy_med={bb[len(bb)//2]:.1f}ms e2e_med={ee[len(ee)//2]:.0f}ms" if bb else "  burst: none")
print(f"  {a.mode}[{a.substrate}/P={a.sm_preemptor}]: 落墙态={sum(1 for e in ctl_log if e['fired_phase']=='wall')}/{len(ctl_log)} "
      f"强发={sum(1 for e in ctl_log if e['forced'])} 平均延迟={sum(e['delay_ms'] for e in ctl_log)/max(len(ctl_log),1):.0f}ms")

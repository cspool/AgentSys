"""wall_preemptive, 按需分区(resize)版。

与 wp_gc.py(静态分区)的差异只有一处: 分区不再全程扣住。
  - 平时受害者独占整卡(primary ctx, 128 SM);
  - 抢占触发时才切到分区, 抢占者拿一块, 受害者拿补集;
  - burst 结束立刻还回整卡。
预建分区池, 切换代价实测 4.26us, 所以按需切换是可行的。

受害者的一个相位被切成 --chunks 个等工作量的 chunk 串行发射, 分区变更在 chunk 边界生效。
这是为了让分区变更有一个现实的生效粒度(真实 decode step 每步发射上百个小 kernel,
而我们的合成受害者一个相位就是一个 162ms 的大 kernel, 粒度不真实)。
总工作量与 wp_gc.py 逐字相同, 只是发射被切开。

策略:
  valve              到达即抢占, 抢占者固定拿 sat 分区
  random_defer       同推迟预算、与状态无关(公平性对照)
  wall_aware         推迟到墙态, 抢占者固定拿 sat 分区
  wall_aware_resize  推迟到墙态, 且**在墙态给抢占者更大的分区**(受害者反正用不上那些 SM)
"""
import argparse, json, random, statistics, threading, time
import torch, triton
import triton.language as tl
from torch.cuda.green_contexts import GreenContext, SUPPORTED


@triton.jit
def stream_fma(x, y, n, reps, inner, GRID: tl.constexpr, BLOCK: tl.constexpr):
    pid = tl.program_id(0); step = GRID * BLOCK * 4
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


@triton.jit
def fma_full(x, n, reps, BLOCK: tl.constexpr):
    pid = tl.program_id(0); offs = pid*BLOCK + tl.arange(0, BLOCK); mask = offs < n
    v = tl.load(x+offs, mask=mask)
    for _ in range(reps): v = v*1.000001+0.000001
    tl.store(x+offs, v, mask=mask)


ap = argparse.ArgumentParser()
ap.add_argument('--mode', required=True,
                choices=['valve', 'wall_aware', 'random_defer', 'wall_aware_resize'])
ap.add_argument('--sm-pre-sat', type=int, default=32, help='饱和态(或不看状态时)给抢占者的 SM')
ap.add_argument('--sm-pre-wall', type=int, default=64, help='墙态给抢占者的 SM(仅 resize 用)')
ap.add_argument('--chunks', type=int, default=16)
ap.add_argument('--wall-inner', type=int, default=60)
ap.add_argument('--sat-inner', type=int, default=290)
ap.add_argument('--pattern', default='w,s')
ap.add_argument('--cycles', type=int, default=1500)
ap.add_argument('--n', type=int, default=120_000_000)
ap.add_argument('--reps-file', default='../reps_v6.json')
ap.add_argument('--burst-reps', type=int, default=1485188)
ap.add_argument('--k', type=int, default=300)
ap.add_argument('--period', type=float, default=1.5)
ap.add_argument('--cool', type=float, default=0.074)
ap.add_argument('--deadline-frac', type=float, default=0.9)
ap.add_argument('--seed', type=int, default=20260921)
ap.add_argument('--delay-file', default=None)
ap.add_argument('--prefix', required=True)
a = ap.parse_args()

if not SUPPORTED:
    raise SystemExit('此 PyTorch 未编译 green context 支持')
dev = torch.device('cuda:0'); torch.cuda.init()
NSM = torch.cuda.get_device_properties(0).multi_processor_count
BLOCK, GRID, N = 256, 128*6, a.n
cache = json.load(open(a.reps_file))
REPS = {}
for ph, inner in (('w', a.wall_inner), ('s', a.sat_inner)):
    key = f"{inner}:{N}"
    if key not in cache:
        raise SystemExit(f"reps 未校准: {key}")
    REPS[ph] = (cache[key], inner)

vx = torch.randn(N, device=dev); vy = torch.empty_like(vx)
bn = GRID * BLOCK; bx = torch.randn(bn, device=dev)

# ---- 预建分区池(一次性) ----
t_pool = time.time()
PRE_SIZES = sorted({a.sm_pre_sat, a.sm_pre_wall})
GC_PRE, GC_VIC = {}, {}
for p in PRE_SIZES:
    GC_PRE[p] = GreenContext.create(p, 0)
    GC_VIC[NSM - p] = GreenContext.create(NSM - p, 0)
ST_PRE = {p: GC_PRE[p].Stream() for p in PRE_SIZES}
ST_VIC = {s: GC_VIC[s].Stream() for s in GC_VIC}
ST_FULL = torch.cuda.Stream()                       # 整卡(primary ctx)
pool_ms = (time.time() - t_pool) * 1000

PHASE = 'w'
VICTIM_SM = NSM                                     # 平时整卡
TRIG = {'i': -1, 't': 0.0, 'psm': a.sm_pre_sat}
CV = threading.Condition()
STOP = threading.Event()
victim_log, burst_log, ctl_log = [], [], []


def victim_launch(sm, reps, inner):
    """在 sm 对应的分区上发射一个 chunk, 返回耗时 ms。每 chunk 同步, 避免跨分区并发。"""
    if sm >= NSM:
        st, gc = ST_FULL, None
    else:
        st, gc = ST_VIC[sm], GC_VIC[sm]
    if gc is not None:
        gc.set_context()
    try:
        with torch.cuda.stream(st):
            s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
            s.record(st)
            stream_fma[(GRID,)](vx, vy, N, reps, inner, GRID=GRID, BLOCK=BLOCK)
            e.record(st); st.synchronize()
        return s.elapsed_time(e)
    finally:
        if gc is not None:
            gc.pop_context()


def victim_thread():
    global PHASE
    for sm in list(ST_VIC) + [NSM]:                       # 各分区预热
        for ph, (reps, inner) in REPS.items():
            victim_launch(sm, 1, inner)
    pattern = a.pattern.split(',')
    t0 = time.monotonic()
    for c in range(a.cycles):
        if STOP.is_set():
            break
        for ph in pattern:
            reps, inner = REPS[ph]
            PHASE = ph
            ts = time.monotonic() - t0
            per, rem = reps // a.chunks, reps % a.chunks
            tot, sms = 0.0, []
            for k in range(a.chunks):
                r = per + (rem if k == a.chunks - 1 else 0)
                if r <= 0:
                    continue
                sm = VICTIM_SM
                sms.append(sm)
                tot += victim_launch(sm, r, inner)
            victim_log.append({'t': ts, 't_abs': time.time(), 'ph': ph, 'ms': tot,
                               'sm_min': min(sms) if sms else NSM,
                               'sm_shrunk_chunks': sum(1 for s in sms if s < NSM)})


def preemptor_thread():
    global VICTIM_SM
    for p in PRE_SIZES:                                   # 各分区预热
        GC_PRE[p].set_context()
        with torch.cuda.stream(ST_PRE[p]):
            fma_full[(bn//BLOCK,)](bx, bn, 8, BLOCK=BLOCK); ST_PRE[p].synchronize()
        GC_PRE[p].pop_context()
    seen = -1
    while not STOP.is_set() and len(burst_log) < a.k:
        with CV:
            if TRIG['i'] == seen:
                CV.wait(timeout=0.05); continue
            seen = TRIG['i']; trig_t = TRIG['t']; psm = TRIG['psm']
        ts = time.time()
        GC_PRE[psm].set_context()
        try:
            with torch.cuda.stream(ST_PRE[psm]):
                s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
                s.record(ST_PRE[psm])
                fma_full[(bn//BLOCK,)](bx, bn, a.burst_reps, BLOCK=BLOCK)
                e.record(ST_PRE[psm]); ST_PRE[psm].synchronize()
            busy = s.elapsed_time(e)
        finally:
            GC_PRE[psm].pop_context()
        VICTIM_SM = NSM                                   # 立刻还回整卡
        burst_log.append({'i': seen, 't_abs': ts, 'busy_ms': busy, 'pre_sm': psm,
                          'e2e_ms': (time.time() - trig_t) * 1000})


_rng = random.Random(a.seed)
_sched, _acc = [], 0.0
for _ in range(a.k):
    _acc += max(0.15, min(_rng.expovariate(1.0 / a.period), a.period * 3))
    _sched.append(_acc)
_defers = []
if a.mode == 'random_defer' and a.delay_file:
    _defers = [e['delay_ms'] for e in json.load(open(a.delay_file))['events']]
    random.Random(a.seed + 1).shuffle(_defers)


def controller_thread():
    global VICTIM_SM
    t0 = time.time()
    for i in range(a.k):
        tick = t0 + _sched[i]
        while time.time() < tick:
            time.sleep(0.002)
        budget = (_sched[i+1] - _sched[i]) if i + 1 < len(_sched) else a.period
        deadline = tick + budget * a.deadline_frac
        forced = False
        if a.mode in ('wall_aware', 'wall_aware_resize'):
            while PHASE != 'w' and time.time() < deadline:
                time.sleep(0.003)
            forced = PHASE != 'w'
        elif a.mode == 'random_defer':
            d = _defers[i % len(_defers)] / 1000.0 if _defers else 0.0
            tgt = min(tick + d, deadline)
            while time.time() < tgt:
                time.sleep(0.003)
        ph = PHASE
        psm = a.sm_pre_sat
        if a.mode == 'wall_aware_resize' and ph == 'w' and not forced:
            psm = a.sm_pre_wall                            # 墙态: 给抢占者更大的分区
        VICTIM_SM = NSM - psm                              # 受害者下一个 chunk 起缩到补集
        with CV:
            TRIG['i'] = i; TRIG['t'] = time.time(); TRIG['psm'] = psm
            CV.notify_all()
        ctl_log.append({'i': i, 't': time.time() - t0, 'forced': forced, 'pre_sm': psm,
                        'fired_phase': 'wall' if ph == 'w' else 'saturated',
                        'delay_ms': (time.time() - tick) * 1000})
        if a.mode == 'valve':
            time.sleep(a.cool)
    STOP.set()
    with CV:
        CV.notify_all()


tv = threading.Thread(target=victim_thread, daemon=True)
tp = threading.Thread(target=preemptor_thread, daemon=True)
tc = threading.Thread(target=controller_thread, daemon=True)
tv.start(); time.sleep(2.0)
tp.start(); time.sleep(1.0)
tc.start()
tc.join(); tp.join(timeout=60); tv.join(timeout=90)

json.dump({'pattern': a.pattern, 'substrate': 'resize', 'chunks': a.chunks,
           'sm_pre_sat': a.sm_pre_sat, 'sm_pre_wall': a.sm_pre_wall,
           'pool_build_ms': pool_ms, 'iters': victim_log},
          open(f'{a.prefix}_{a.mode}_victim.json', 'w'))
json.dump({'k': len(burst_log), 'bursts': burst_log}, open(f'{a.prefix}_{a.mode}_burst.json', 'w'))
json.dump({'mode': a.mode, 'k': a.k, 'events': ctl_log,
           'hit_wall': sum(1 for e in ctl_log if e['fired_phase'] == 'wall'),
           'forced': sum(1 for e in ctl_log if e['forced']),
           'mean_delay_ms': sum(e['delay_ms'] for e in ctl_log) / max(len(ctl_log), 1)},
          open(f'{a.prefix}_{a.mode}_ctl.json', 'w'))

for ph in ('w', 's'):
    v = sorted(i['ms'] for i in victim_log if i['ph'] == ph)
    if v: print(f"  victim {ph}: n={len(v)} med={v[len(v)//2]:.1f}ms")
if burst_log:
    bb = sorted(b['busy_ms'] for b in burst_log); ee = sorted(b['e2e_ms'] for b in burst_log)
    sz = {}
    for b in burst_log: sz[b['pre_sm']] = sz.get(b['pre_sm'], 0) + 1
    print(f"  burst: n={len(bb)} busy_med={bb[len(bb)//2]:.1f}ms e2e_med={ee[len(ee)//2]:.0f}ms 分区分布={sz}")
print(f"  {a.mode}[resize/chunks={a.chunks}]: 落墙态={sum(1 for e in ctl_log if e['fired_phase']=='wall')}/{len(ctl_log)} "
      f"强发={sum(1 for e in ctl_log if e['forced'])} 平均延迟={sum(e['delay_ms'] for e in ctl_log)/max(len(ctl_log),1):.0f}ms "
      f"建池={pool_ms:.0f}ms")

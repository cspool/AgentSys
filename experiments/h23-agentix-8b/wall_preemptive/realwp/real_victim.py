"""真实负载的 wall 抢占对照 (GPU1)

受害者 = 真实 kernel 的相位交替, 三种墙型组合可选:
  tc_dram   : TC 墙(fp16 GEMM) <-> DRAM 访存墙(SDPA decode)   <- 最贴真实 prefill/decode
  fp32_dram : FP32 算力墙(fp32 GEMM) <-> DRAM 访存墙
  tc_sat    : TC 墙 <-> 全饱和(fp16 GEMM 小尺寸, TC+L2 双高)
抢占者 = 真实 kernel, 资源亲和可选 (fp32 / tc / dram)

墙型画像(walls/REAL_WALLS.json, ncu 实测, --cache-control none):
  TC 墙      fp16 GEMM 6144^3       TC 49.2(=可达峰值100%) L2 54 L1 30 DRAM 18
  FP32 算力墙 fp32 GEMM 512x8192^2  FMA 73 SM 82 smem 42 L1 43 L2 29 DRAM 32
  DRAM 访存墙 SDPA decode B=32 KV64M DRAM 93.1 TC 36 L2 36 L1 15
  全饱和      fp16 GEMM 2048^3(热)   TC 46(94%) L2 72 L1 34 DRAM 0.05
"""
import argparse, json, random, statistics, threading, time
import torch
import torch.nn.functional as F

# ---------- 真实 kernel 工厂 ----------
def mk_gemm(M, N, K, dtype=torch.float16):
    a = torch.randn(M, K, device='cuda', dtype=dtype)
    b = torch.randn(K, N, device='cuda', dtype=dtype)
    return lambda: torch.matmul(a, b)

def mk_decode(B, H, Hkv, S_kv, D, dtype=torch.float16):
    q = torch.randn(B, H, 1, D, device='cuda', dtype=dtype)
    k = torch.randn(B, Hkv, S_kv, D, device='cuda', dtype=dtype)
    v = torch.randn(B, Hkv, S_kv, D, device='cuda', dtype=dtype)
    return lambda: F.scaled_dot_product_attention(q, k, v, enable_gqa=(H != Hkv))

# 各墙型的受害者相位 (名字 -> 构造器)
PHASE = {
    'tc'   : lambda: mk_gemm(6144, 6144, 6144),                        # TC 墙
    'fp32' : lambda: mk_gemm(512, 8192, 8192, torch.float32),          # FP32 算力墙
    'dram' : lambda: mk_decode(64, 32, 8, 16384, 128),                 # DRAM 访存墙(96.96%), ~4.7ms, 与 tc 相位时长配平
    'sat'  : lambda: mk_gemm(2048, 2048, 2048),                        # 全饱和
}
# 抢占者: 资源亲和不同, 工作量对齐到相近量级
CO = {
    'fp32' : lambda: mk_gemm(512, 4096, 4096, torch.float32),
    'tc'   : lambda: mk_gemm(2048, 2048, 4096),
    'dram' : lambda: mk_decode(16, 32, 8, 4096, 128),
}

ap = argparse.ArgumentParser()
ap.add_argument('--walls', default='tc_dram',
                choices=['tc_dram', 'fp32_dram', 'tc_sat'])
ap.add_argument('--co', default='fp32', choices=list(CO))
ap.add_argument('--co-reps', type=int, default=1, help='每次抢占事件里共跑 kernel 的连发次数, 用来把并发比例抬上去')
ap.add_argument('--mode', required=True, choices=['valve', 'wall_aware', 'random_defer'])
ap.add_argument('--wall-phase', default=None,
                help='哪个相位算"墙态"(wall_aware 会等它); 默认取 --walls 的第二个')
ap.add_argument('--k', type=int, default=200)
ap.add_argument('--period', type=float, default=0.4)
ap.add_argument('--cool', type=float, default=0.02)
ap.add_argument('--deadline-frac', type=float, default=0.9)
ap.add_argument('--seed', type=int, default=20260922)
ap.add_argument('--cycles', type=int, default=200000)  # 必须远大于需求: 受害者要活过控制器
ap.add_argument('--delay-file', default=None)
ap.add_argument('--prefix', required=True)
a = ap.parse_args()

pa, pb = a.walls.split('_')
WALL = a.wall_phase or pb          # 默认后者是"墙态"
seq = [pa, pb]
fns = {n: PHASE[n]() for n in seq}
co_fn = CO[a.co]()

PHASE_NOW = seq[0]
TRIG = {'i': -1, 't': 0.0}
CV = threading.Condition()
STOP = threading.Event()
v_log, c_log, ctl_log = [], [], []

def victim_thread():
    global PHASE_NOW
    st = torch.cuda.Stream()
    with torch.cuda.stream(st):
        for n in seq: fns[n]()
        st.synchronize()
        for _ in range(a.cycles):
            if STOP.is_set(): break
            for n in seq:
                PHASE_NOW = n
                s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
                s.record(st); fns[n](); e.record(st); st.synchronize()
                v_log.append({'t_abs': time.time(), 'ph': n, 'ms': s.elapsed_time(e)})

def preemptor_thread():
    st = torch.cuda.Stream()
    with torch.cuda.stream(st):
        co_fn(); st.synchronize()
        seen = -1
        while not STOP.is_set() and len(c_log) < a.k:
            with CV:
                if TRIG['i'] == seen:
                    CV.wait(timeout=0.05); continue
                seen = TRIG['i']; trig_t = TRIG['t']
            ts = time.time()
            s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
            s.record(st)
            for _ in range(a.co_reps): co_fn()
            e.record(st); st.synchronize()
            c_log.append({'i': seen, 't_abs': ts, 'busy_ms': s.elapsed_time(e),
                          'e2e_ms': (time.time()-trig_t)*1000})

_rng = random.Random(a.seed); _sched=[]; _acc=0.0
for _ in range(a.k):
    _acc += max(0.05, min(_rng.expovariate(1.0/a.period), a.period*3)); _sched.append(_acc)
_defers = []
if a.mode == 'random_defer' and a.delay_file:
    _defers = [e['delay_ms'] for e in json.load(open(a.delay_file))['events']]
    random.Random(a.seed+1).shuffle(_defers)

def controller_thread():
    t0 = time.time()
    for i in range(a.k):
        tick = t0 + _sched[i]
        while time.time() < tick: time.sleep(0.001)
        budget = (_sched[i+1]-_sched[i]) if i+1 < len(_sched) else a.period
        deadline = tick + budget*a.deadline_frac
        forced = False
        if a.mode == 'wall_aware':
            while PHASE_NOW != WALL and time.time() < deadline: time.sleep(0.001)
            forced = PHASE_NOW != WALL
        elif a.mode == 'random_defer':
            d = _defers[i % len(_defers)]/1000.0 if _defers else 0.0
            tgt = min(tick+d, deadline)
            while time.time() < tgt: time.sleep(0.001)
        ph = PHASE_NOW
        with CV:
            TRIG['i']=i; TRIG['t']=time.time(); CV.notify_all()
        ctl_log.append({'i':i,'fired_phase':ph,'forced':forced,
                        'delay_ms':(time.time()-tick)*1000})
        if a.mode == 'valve': time.sleep(a.cool)
    STOP.set()
    with CV: CV.notify_all()

tv=threading.Thread(target=victim_thread,daemon=True)
tp=threading.Thread(target=preemptor_thread,daemon=True)
tc=threading.Thread(target=controller_thread,daemon=True)
tv.start(); time.sleep(2.0); tp.start(); time.sleep(0.5); tc.start()
victim_alive_at_end = tv.is_alive()
tc.join(); tp.join(timeout=60); tv.join(timeout=60)
if not victim_alive_at_end:
    print("!!! 校验失败: 受害者早于控制器结束 -> PHASE_NOW 冻结, 落墙统计无效. 增大 --cycles 重跑")

json.dump({'walls':a.walls,'wall_phase':WALL,'co':a.co,
           'victim_outlasted_controller': victim_alive_at_end,'iters':v_log},
          open(f'{a.prefix}_{a.mode}_victim.json','w'))
json.dump({'k':len(c_log),'bursts':c_log}, open(f'{a.prefix}_{a.mode}_burst.json','w'))
json.dump({'mode':a.mode,'k':a.k,'events':ctl_log,
           'hit_wall':sum(1 for e in ctl_log if e['fired_phase']==WALL),
           'forced':sum(1 for e in ctl_log if e['forced'])},
          open(f'{a.prefix}_{a.mode}_ctl.json','w'))
for n in seq:
    v=sorted(i['ms'] for i in v_log if i['ph']==n)
    if v: print(f"  victim {n}: n={len(v)} med={v[len(v)//2]:.2f}ms")
bb=sorted(x['busy_ms'] for x in c_log); ee=sorted(x['e2e_ms'] for x in c_log)
print(f"  burst({a.co}): n={len(bb)} busy_med={bb[len(bb)//2]:.2f}ms e2e_med={ee[len(ee)//2]:.0f}ms" if bb else "  burst: none")
_span=(max(i["t_abs"] for i in v_log)-min(i["t_abs"]-i["ms"]/1000 for i in v_log)) if v_log else 1
_rho=sum(x["busy_ms"] for x in c_log)/1000/_span if _span>0 else 0
print(f"  并发比例 rho={_rho:.2f}")
print(f"  {a.mode}[{a.walls}, 墙态={WALL}]: 落墙={sum(1 for e in ctl_log if e['fired_phase']==WALL)}/{len(ctl_log)} "
      f"强发={sum(1 for e in ctl_log if e['forced'])}")

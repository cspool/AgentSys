"""抢占时机对照 (受害者 = MPK megakernel)。

MPK 一次生成里 KV 上下文单调增长, 受害者因此从"偏算力"漂到"偏 DRAM"。
于是测量窗的前半/后半就是两个 wall 档位, 无需外加相位。

三个臂在构造上完全等功 —— 事件数 K、单次时长 D、总 BURST 时长、占空比逐字相同,
唯一差别是 BURST 落在前半还是后半:
  late   (wall-aware): 全部 BURST 落后半(受害者让出算力时下手)
  spread (普通抢占)  : 前后半各一半
  early  (anti-wall) : 全部落前半

抢占者靠自身速率骤降自动检测受害者起点, 不需要跨进程同步。
全程并发: 窗口内任何时刻都在 BASE 或 BURST 配额下发射, 绝不停。
"""
import argparse, json, sys, time, torch
sys.path.insert(0, '/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3')
from common.quota import TpcMaskKnob, mono_ns

ap = argparse.ArgumentParser()
ap.add_argument('--arm', required=True, choices=['late', 'spread', 'early', 'base_only', 'burst_only'])
ap.add_argument('--axis', default='tc', choices=['tc', 'dram'])
ap.add_argument('--base-tpcs', type=int, default=8)
ap.add_argument('--burst-tpcs', type=int, default=32)
ap.add_argument('--max-secs', type=float, default=200)
ap.add_argument('--win-secs', type=float, default=48)   # 测量窗(在受害者窗口内)
ap.add_argument('--lead-secs', type=float, default=2)   # 受害者起点后的静默期
ap.add_argument('--n-events', type=int, default=16)
ap.add_argument('--burst-ms', type=int, default=500)
ap.add_argument('--onset-frac', type=float, default=0.92)
ap.add_argument('--onset-n', type=int, default=3)
ap.add_argument('--chunk', type=int, default=16); ap.add_argument('--depth', type=int, default=3)
ap.add_argument('--out', required=True)
a = ap.parse_args()

dev = torch.device('cuda'); torch.zeros(1, device=dev)
if a.axis == 'tc':
    A = torch.randn(1024,2048,device=dev,dtype=torch.float16); B = torch.randn(2048,1024,device=dev,dtype=torch.float16)
    op = lambda: A @ B; work = 2*1024*2048*1024; unit='FLOP'
else:
    import torch.nn.functional as F
    q=torch.randn(8,32,1,128,device=dev,dtype=torch.float16); k=torch.randn(8,8,4096,128,device=dev,dtype=torch.float16)
    v=torch.randn(8,8,4096,128,device=dev,dtype=torch.float16)
    op = lambda: F.scaled_dot_product_attention(q,k,v,enable_gqa=True); work=2*8*8*4096*128*2; unit='BYTE'

s = torch.cuda.Stream()
knob = TpcMaskKnob(s, base_tpcs=a.base_tpcs, burst_tpcs=a.burst_tpcs)

# ---- 事件表: 三臂等功, 只差落在前半还是后半 ----
def build_events():
    K, D = a.n_events, a.burst_ms/1000.0
    half = a.win_secs/2
    if a.arm == 'base_only':  return []
    if a.arm == 'burst_only': return [(0.0, a.win_secs)]
    if a.arm == 'late':   slots = [half + (i+0.5)*half/K for i in range(K)]
    elif a.arm == 'early':slots = [(i+0.5)*half/K for i in range(K)]
    else:                 slots = [(i+0.5)*half/(K//2) for i in range(K//2)] + \
                                  [half + (i+0.5)*half/(K//2) for i in range(K//2)]
    assert len(slots) == K, f"K 不一致: {len(slots)}"
    return [(t, t+D) for t in slots]
EV = build_events()
tot_burst = sum(e-b for b,e in EV)
assert a.arm in ('base_only','burst_only') or abs(tot_burst - a.n_events*a.burst_ms/1000.0) < 1e-6

# ---- 预热 + solo 基线(受害者到来之前) ----
pool = [torch.cuda.Event() for _ in range(a.depth+1)]
with torch.cuda.stream(s):
    for _ in range(30): op()
torch.cuda.synchronize()

t0 = time.perf_counter(); deadline = t0 + a.max_secs
buckets=[]; n_b=0; b_start=t0; inflight=[]
onset=None; win_end=None; lvl='BASE'; ev_i=0; applied=[]
BK=0.2
solo_rate=None; solo_acc=[]

with torch.cuda.stream(s):
    while True:
        now = time.perf_counter()
        if now >= deadline: break
        if win_end and now >= win_end: break
        while len(inflight) < a.depth:
            for _ in range(a.chunk): op()
            e = pool.pop(0) if pool else torch.cuda.Event()
            e.record(s); inflight.append((e, a.chunk))
        rest=[]
        for e,c in inflight:
            if e.query(): n_b += c; pool.append(e)
            else: rest.append((e,c))
        inflight = rest
        if now - b_start >= BK:
            r = n_b/(now-b_start)
            buckets.append(dict(t=round(b_start-t0,3), n=n_b, rate=round(r,1), lvl=lvl))
            # 受害者起点检测: 连续 2 桶掉到 solo 的 onset_frac 以下
            if onset is None:
                if len(solo_acc) < 25: solo_acc.append(r)
                else:
                    if solo_rate is None:
                        solo_acc.sort(); solo_rate = solo_acc[len(solo_acc)//2]
                    if len(buckets) >= a.onset_n and all(x['rate'] < a.onset_frac*solo_rate for x in buckets[-a.onset_n:]):
                        onset = now
                        win_end = onset + a.lead_secs + a.win_secs
            n_b=0; b_start=now
        # 事件驱动
        if onset is not None:
            rel = now - (onset + a.lead_secs)
            if 0 <= rel:
                want = 'BASE'
                for bgn,end in EV:
                    if bgn <= rel < end: want='BURST'; break
                if want != lvl:
                    knob.set_quota(want); lvl=want; applied.append((round(rel,4), want))
knob.set_quota('BASE')
torch.cuda.synchronize()
dur = time.perf_counter()-t0
win = [b for b in buckets if onset and b['t'] >= (onset-t0)+a.lead_secs]
tot_win = sum(b['n'] for b in win); t_win = a.win_secs if win else 0
res = dict(arm=a.arm, axis=a.axis, unit=unit, base_tpcs=a.base_tpcs, burst_tpcs=a.burst_tpcs,
           onset_detected=onset is not None, solo_rate=solo_rate,
           K=len(EV), burst_total_s=round(tot_burst,3),
           duty=round(tot_burst/a.win_secs,4) if a.win_secs else None,
           n_applied=len(applied), win_secs=t_win, win_calls=tot_win,
           win_rate=round(tot_win/t_win,1) if t_win else None,
           win_work_per_s=round(tot_win*work/t_win/1e12,4) if t_win else None,
           total_secs=round(dur,2), buckets=buckets, applied=applied)
print(json.dumps({k:v for k,v in res.items() if k not in ('buckets','applied')}, ensure_ascii=False))
json.dump(res, open(a.out,'w'), ensure_ascii=False, indent=1)

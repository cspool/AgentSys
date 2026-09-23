"""按受害者相位择时的抢占者。

受害者(POD 方波)每 phase_ms 切换一次相位并发布到信标。抢占者跟随相位, 按事件表改配额。
三臂等功由构造保证: 每臂"施放事件的 epoch 数"相同, 每个施放 epoch 内偏移多重集相同,
单次 BURST 时长相同 => K, ΣBURST, duty 全部逐字相同, 唯一变量是事件落在哪个相位。

  a100 (wall-aware): 只在 DRAM 相 epoch 施放   —— 受害者吃带宽时, 算力型抢占者下手
  a050 (普通抢占)  : 两种 epoch 各施放一半
  a000 (anti-wall) : 只在 TC 相 epoch 施放
"""
import argparse, json, sys, time, torch
sys.path.insert(0, '/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3')
from common.quota import TpcMaskKnob
from common.beacon import PhaseBeacon, mono_ns

ap = argparse.ArgumentParser()
ap.add_argument('--mode', default='quota', choices=['quota','cilp'],
    help='quota=改自身TPC配额(温和); cilp=独立context+BURST发射/BASE静默 => 硬件指令级抢占受害者(最快最重)')
ap.add_argument('--arm', required=True, choices=['a100','a050','a000','base_only','burst_only'])
ap.add_argument('--axis', default='tc', choices=['tc','dram'])
ap.add_argument('--base-tpcs', type=int, default=8)
ap.add_argument('--burst-tpcs', type=int, default=32)
ap.add_argument('--secs', type=float, default=70)
ap.add_argument('--warmup', type=float, default=10)
ap.add_argument('--offsets-ms', default='100,230,360,490')
ap.add_argument('--burst-ms', type=int, default=90)
ap.add_argument('--beacon', default='/tmp/wp3_phase')
ap.add_argument('--orth-phase', type=int, default=0, help='wall-aware 应当下手的相位键(墙态)')
ap.add_argument('--anti-phase', type=int, default=1, help='wall-aware 应当避开的相位键(全饱和或另一墙)')
ap.add_argument('--chunk', type=int, default=16); ap.add_argument('--depth', type=int, default=3)
ap.add_argument('--suspend-victim', default=None, help='挂起门路径; BURST 期间挂起受害者(经典抢占), 自身配额抬到 burst')
ap.add_argument('--out', required=True)
a = ap.parse_args()

dev = torch.device('cuda'); torch.zeros(1, device=dev)
if a.axis == 'tc':
    A=torch.randn(1024,2048,device=dev,dtype=torch.float16); B=torch.randn(2048,1024,device=dev,dtype=torch.float16)
    op=lambda: A@B; work=2*1024*2048*1024; unit='FLOP'
else:
    import torch.nn.functional as F
    q=torch.randn(8,32,1,128,device=dev,dtype=torch.float16); k=torch.randn(8,8,4096,128,device=dev,dtype=torch.float16)
    v=torch.randn(8,8,4096,128,device=dev,dtype=torch.float16)
    op=lambda: F.scaled_dot_product_attention(q,k,v,enable_gqa=True); work=2*8*8*4096*128*2; unit='BYTE'

s = torch.cuda.Stream()
knob = TpcMaskKnob(s, a.base_tpcs, a.burst_tpcs) if a.mode=='quota' else None
_vgate = None
if a.suspend_victim:
    from common.gate import SuspendGate
    _vgate = SuspendGate(a.suspend_victim)
bc = PhaseBeacon(a.beacon)
OFFS = [int(x)/1000.0 for x in a.offsets_ms.split(',')]
DB = a.burst_ms/1000.0
DRAM, TC = a.orth_phase, a.anti_phase   # 语义: DRAM=该抢的相位, TC=该避的相位(名字沿用旧代码)

pool=[torch.cuda.Event() for _ in range(a.depth+1)]
with torch.cuda.stream(s):
    for _ in range(30): op()
torch.cuda.synchronize()

t0=time.perf_counter(); t_start=t0+a.warmup; deadline=t_start+a.secs
inflight=[]; n_done=0; n_win=0
cur_ph=None; ep_t0=None; ep_idx=0; ep_fire=False; ep_kind=None
lvl='BASE'; events=[]; n_ep={DRAM:0, TC:0}; n_ep_fire={DRAM:0, TC:0}
phase_time={DRAM:0.0, TC:0.0}; last_ph_t=None; torn=0; sched=[]
with torch.cuda.stream(s):
    while True:
        now=time.perf_counter()
        if now>=deadline: break
        _may_launch = (a.mode=='quota') or (lvl=='BURST')
        while _may_launch and len(inflight)<a.depth:
            for _ in range(a.chunk): op()
            e=pool.pop(0) if pool else torch.cuda.Event(); e.record(s); inflight.append((e,a.chunk))
        rest=[]
        for e,c in inflight:
            if e.query():
                n_done+=c
                if now>=t_start: n_win+=c
                pool.append(e)
            else: rest.append((e,c))
        inflight=rest
        r=bc.read()
        if r is None: torn+=1
        else:
            ph=r[0]
            if ph!=cur_ph:
                if last_ph_t is not None and cur_ph in phase_time: phase_time[cur_ph]+=now-last_ph_t
                last_ph_t=now; cur_ph=ph; ep_t0=now; ep_kind=ph
                if now>=t_start:
                    n_ep[ph]=n_ep.get(ph,0)+1
                    i=n_ep[ph]
                    if a.arm=='a100':   ep_fire=(ph==DRAM)
                    elif a.arm=='a000': ep_fire=(ph==TC)
                    elif a.arm=='a050': ep_fire=(i%2==0)            # 两相各施放一半
                    elif a.arm=='burst_only': ep_fire=True
                    else: ep_fire=False
                    if ep_fire: n_ep_fire[ph]=n_ep_fire.get(ph,0)+1
                else: ep_fire=False
                sched=[(ep_t0+o, ep_t0+o+DB) for o in OFFS] if ep_fire else []
        want='BASE'
        if a.arm=='burst_only' and now>=t_start: want='BURST'
        else:
            for bgn,end in sched:
                if bgn<=now<end: want='BURST'; break
        if want!=lvl:
            if knob is not None: knob.set_quota(want)
            if _vgate is not None: _vgate.set(want=='BURST')   # 经典抢占: BURST=挂起受害者
            lvl=want
            if now>=t_start: events.append((round(now-t_start,4), want, ep_kind))
if last_ph_t is not None and cur_ph in phase_time: phase_time[cur_ph]+=time.perf_counter()-last_ph_t
(knob.set_quota('BASE') if knob is not None else None)
if _vgate is not None: _vgate.set(False)
torch.cuda.synchronize()
win=time.perf_counter()-t_start
burst_s=sum(e-b for b,e in [] ) # 由事件对重建
bs=[]; 
for i in range(0,len(events)-1):
    if events[i][1]=='BURST' and events[i+1][1]=='BASE': bs.append(events[i+1][0]-events[i][0])
K=sum(1 for e in events if e[1]=='BURST')
res=dict(arm=a.arm, axis=a.axis, unit=unit, base_tpcs=a.base_tpcs, burst_tpcs=a.burst_tpcs,
         win_secs=round(win,3), win_calls=n_win, win_rate=round(n_win/win,1),
         win_work_per_s=round(n_win*work/win/1e12,4),
         K=K, burst_total_s=round(sum(bs),3), duty=round(sum(bs)/win,4),
         n_epoch=dict(n_ep), n_epoch_fire=dict(n_ep_fire),
         alpha_realized=round(n_ep_fire.get(DRAM,0)/max(1,sum(n_ep_fire.values())),4),
         phase_time={str(k):round(v,2) for k,v in phase_time.items()},
         beacon_torn=torn, events=events[:40])
print(json.dumps({k:v for k,v in res.items() if k!='events'}, ensure_ascii=False))
json.dump(res, open(a.out,'w'), ensure_ascii=False, indent=1)

"""E15 v6: 干净重写的测量核。同配置4臂; 稳态窗口测量(跳过前25s); 无静默退避(装不下即fail);
固定渲染常数; 逐tick醒集日志。臂: R1驻留+排队 / RB丢弃重建 / RS换出停放 / RSr惰性(压力才让位)。"""
import argparse,threading,time,json,random,traceback
import torch,numpy as np
ap=argparse.ArgumentParser()
ap.add_argument('--arm',required=True,choices=['R1','RB','RS','RSr'])
ap.add_argument('--dur',type=float,default=120.0)
ap.add_argument('--warm',type=float,default=25.0)
ap.add_argument('--pool',type=int,default=64)
ap.add_argument('--vision-gb',type=float,default=6.0)
ap.add_argument('--seed',type=int,default=7)
ap.add_argument('--out',default='')
a=ap.parse_args()
dev='cuda'; FRAME=1/60.0
from transformers import AutoModelForCausalLM, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
NL,NKV,HD,L=28,8,128,3000
SLAB=NL*NKV*L*HD*2*2/1e9
sR=torch.cuda.Stream(priority=-1); sL=torch.cuda.Stream(); sV=torch.cuda.Stream()
# ---- 显存布局(先算后配, 装不下即fail) ----
free0=torch.cuda.mem_get_info()[0]/1e9
BUDGET=free0-2.2   # 激活/杂项
if a.arm=='R1':
    # 席位slabs + 醒集merged副本 + 常驻视觉ws
    AW=10; SEATS=int((BUDGET-a.vision_gb-AW*SLAB)/SLAB)
elif a.arm=='RSr':
    AW=10; SEATS=None  # 惰性: slabs无界增长直至压力(其语义), merged=AW
else:
    AW=14; SEATS=None
    # RS: 醒集slabs(AW) + merged(AW) + 常驻ws; RB: 同RS但无host无ws常驻
need = (a.vision_gb + AW*SLAB + (SEATS or 0)*SLAB + AW*SLAB) if a.arm=='R1' else \
       (AW*SLAB*2 + (a.vision_gb if a.arm=='RS' else 0))
assert need<=BUDGET, f"布局超预算 {need:.1f}>{BUDGET:.1f}"
print(f"arm={a.arm} 预算{BUDGET:.1f}GB 布局{need:.1f}GB AW={AW} SEATS={SEATS}", flush=True)
rng=random.Random(a.seed)
N=a.pool
def dev_pair():
    return (torch.randn(NL,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,
            torch.randn(NL,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02)
dev_slab={}; host_slab={}
if a.arm in ('RS','RSr'):
    for i in range(N):
        host_slab[i]=(torch.empty(NL,NKV,L,HD,dtype=torch.bfloat16,pin_memory=True),
                      torch.empty(NL,NKV,L,HD,dtype=torch.bfloat16,pin_memory=True))
resident=set(range(SEATS)) if a.arm=='R1' else None
adm_q=[i for i in range(N) if a.arm=='R1' and i>=SEATS]
with torch.cuda.stream(sL):
    if a.arm=='R1':
        for i in resident: dev_slab[i]=dev_pair()
sL.synchronize()
phase={i:('wait',rng.uniform(0,10)) for i in range(N)}  # 相对时刻
rounds={i:0 for i in range(N)}; RND=5
merged=[None]; members=[[]]
pause=threading.Event(); idle=threading.Event()
stop=False
frames=[]; tok_log=[]  # (t, tokens_delta)
vlat=[]; awake_log=[]; eps=[0]
def assemble(mem):
    merged[0]=None; members[0]=[]
    torch.cuda.empty_cache()
    with torch.cuda.stream(sL):
        c=DynamicCache()
        for li in range(NL):
            if not mem: break
            k=torch.stack([dev_slab[g][0][li] for g in mem])
            v=torch.stack([dev_slab[g][1][li] for g in mem])
            c.update(k,v,li)
    sL.synchronize()
    merged[0]=c if mem else None; members[0]=list(mem)
def th_sched():
    t0=time.perf_counter()
    while not stop:
        time.sleep(1.0)
        now=time.perf_counter()-t0; changed=False
        for i in range(N):
            if resident is not None and i not in resident: continue
            st_,te=phase[i]
            if now>=te:
                changed=True
                if st_=='wait':
                    phase[i]=('awake',now+rng.uniform(2,3))
                    if i not in dev_slab:
                        with torch.cuda.stream(sL):
                            if a.arm in ('RS','RSr'):
                                k=torch.empty(NL,NKV,L,HD,dtype=torch.bfloat16,device=dev); v=torch.empty_like(k)
                                k.copy_(host_slab[i][0],non_blocking=True); v.copy_(host_slab[i][1],non_blocking=True)
                                dev_slab[i]=(k,v)
                            elif a.arm=='RB':
                                dev_slab[i]=dev_pair()   # 重建(GPU代价真实发生)
                        sL.synchronize()
                else:
                    phase[i]=('wait',now+rng.uniform(6,10)); rounds[i]+=1
                    if a.arm=='RS' and i in dev_slab:      # 主动停放
                        with torch.cuda.stream(sL):
                            host_slab[i][0].copy_(dev_slab[i][0],non_blocking=True)
                            host_slab[i][1].copy_(dev_slab[i][1],non_blocking=True)
                        sL.synchronize(); del dev_slab[i]
                    elif a.arm=='RB' and i in dev_slab:
                        del dev_slab[i]                     # 丢弃
                    # RSr: 滞留(压力才走); R1: 常驻
                    if rounds[i]>=RND:
                        rounds[i]=0; eps[0]+=1
                        if resident is not None:
                            resident.discard(i); adm_q.append(i)
                            if i in dev_slab: del dev_slab[i]
                            nx=adm_q.pop(0); resident.add(nx)
                            with torch.cuda.stream(sL): dev_slab[nx]=dev_pair()
                            sL.synchronize()
                            phase[nx]=('wait',now+rng.uniform(0,2))
        # RSr 压力让位: 设备slabs超预算时逐出等待者(其"被动"语义)
        if a.arm=='RSr':
            capn=int((BUDGET-AW*SLAB)/SLAB)
            waiters=[i for i in dev_slab if phase[i][0]=='wait']
            while len(dev_slab)>capn and waiters:
                i=waiters.pop()
                with torch.cuda.stream(sL):
                    host_slab[i][0].copy_(dev_slab[i][0],non_blocking=True)
                    host_slab[i][1].copy_(dev_slab[i][1],non_blocking=True)
                sL.synchronize(); del dev_slab[i]
        awake=[i for i in range(N) if (resident is None or i in resident)
               and phase[i][0]=='awake' and i in dev_slab][:AW]
        awake_log.append((now,len(awake)))
        if changed or (merged[0] is not None and merged[0].get_seq_length()>L+300):
            idle.clear(); pause.set(); idle.wait(timeout=5)
            try: assemble(awake)
            except Exception: traceback.print_exc()
            finally: pause.clear()
def th_llm():
    t0=time.perf_counter()
    while not stop:
        if pause.is_set() or merged[0] is None or not members[0]:
            idle.set(); time.sleep(0.002); continue
        idle.clear()
        c=merged[0]; B=len(members[0]); S=c.get_seq_length()
        d=torch.zeros(B,1,dtype=torch.long,device=dev)
        with torch.cuda.stream(sL), torch.inference_mode():
            for _ in range(4):
                pos=torch.full((B,1),S,dtype=torch.long,device=dev)
                model(input_ids=d,past_key_values=c,position_ids=pos,cache_position=pos[0]); S+=1
        sL.synchronize()
        tok_log.append((time.perf_counter()-t0, B*4))
UNIT_MS=0.17  # 2048 GEMM 固定常数(消除每次校准漂移)
x=torch.randn(2048,2048,device=dev,dtype=torch.bfloat16); y=torch.randn_like(x); rout=torch.empty_like(x)
R_ITER=max(1,int(5.0/UNIT_MS))
def th_render():
    nxt=time.perf_counter()
    while not stop:
        nxt+=FRAME
        with torch.cuda.stream(sR):
            t0=time.perf_counter()
            for _ in range(R_ITER): torch.mm(x,y,out=rout)
            ev=torch.cuda.Event(); ev.record(sR)
        while not ev.query(): time.sleep(0.001)
        frames.append((time.perf_counter(),(time.perf_counter()-t0)*1000))
        dl=nxt-time.perf_counter()
        if dl>0: time.sleep(dl)
        else: nxt=time.perf_counter()
def th_vision():
    vx=torch.randn(4096,4096,device=dev,dtype=torch.bfloat16); vy=torch.randn_like(vx); vout=torch.empty_like(vx)
    ws=torch.empty(int(a.vision_gb*1e9/2),dtype=torch.bfloat16,device=dev) if a.arm in ('R1','RS') else None
    while not stop:
        time.sleep(8.0)
        if stop: break
        t_arr=time.perf_counter()
        w=ws
        if w is None:
            try: w=torch.empty(int(a.vision_gb*1e9/2),dtype=torch.bfloat16,device=dev)
            except torch.OutOfMemoryError:
                # RSr/RB: 压力让位后重试一次
                if a.arm=='RSr':
                    torch.cuda.empty_cache()
                try: w=torch.empty(int(a.vision_gb*1e9/2),dtype=torch.bfloat16,device=dev)
                except torch.OutOfMemoryError:
                    vlat.append((time.perf_counter(),-1)); continue
        with torch.cuda.stream(sV):
            for _ in range(max(1,int(300/(UNIT_MS*4)))): torch.mm(vx,vy,out=vout)
        sV.synchronize()
        if ws is None: del w; torch.cuda.empty_cache()
        vlat.append((time.perf_counter(),(time.perf_counter()-t_arr)*1000))
def wrap(f):
    def g():
        try: f()
        except Exception: traceback.print_exc()
    return g
ths=[threading.Thread(target=wrap(f)) for f in (th_sched,th_llm,th_render,th_vision)]
T0=time.perf_counter()
for t in ths: t.start()
time.sleep(a.dur); stop=True; pause.clear()
for t in ths: t.join(timeout=25)
WALL=time.perf_counter()-T0
CUT=a.warm
tok_ss=sum(n for t,n in tok_log if t>=CUT)
fr_ss=[m for t,m in frames if (t-T0)>=CUT]
vl_ss=[v for t,v in vlat if (t-T0)>=CUT and v>0]
aw_ss=[n for t,n in awake_log if t>=CUT]
out=dict(arm=a.arm,seed=a.seed,
         llm_tps=tok_ss/(WALL-CUT),
         p99=float(np.percentile(fr_ss,99)) if fr_ss else -1,
         miss=float(100*np.mean(np.array(fr_ss)>FRAME*1000)) if fr_ss else -1,
         vision_ms=float(np.mean(vl_ss)) if vl_ss else -1,
         vision_fail=sum(1 for t,v in vlat if v<0),
         awake_mean=float(np.mean(aw_ss)) if aw_ss else 0,
         eps=eps[0])
print(json.dumps(out,indent=1))
if a.out: json.dump(out,open(a.out,'w'))

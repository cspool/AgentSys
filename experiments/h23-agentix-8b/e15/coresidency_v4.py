"""E15 v4: agent等待循环下的显存仲裁。agent: decode(~2s)/工具等待(~6s)循环, 错相。
R1 驻留(等待者KV占GPU, 准入33封顶) / RB 丢弃重建(等待即丢, 唤醒重prefill 450ms GPU)
/ RS 换出停放(等待D2H 18ms, 唤醒H2D+并入) —— 全臂: 渲染60fps(P优先级)+视觉6GB突发每8s。
decode: 合并批(唤醒集一个cache), 成员变化时重组(设备内拷贝~ms级)。
指标: LLM聚合tok/s(主) / 唤醒时延 / 帧P99&miss / 视觉时延。"""
import argparse,threading,time,json,random
import torch,numpy as np
ap=argparse.ArgumentParser()
ap.add_argument('--arm',required=True,choices=['R1','RB','RS'])
ap.add_argument('--dur',type=float,default=45.0)
ap.add_argument('--pool',type=int,default=96)
ap.add_argument('--vision-gb',type=float,default=6.0)
ap.add_argument('--out',default='')
a=ap.parse_args()
dev='cuda'; FRAME=1/60.0
from transformers import AutoModelForCausalLM, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
NL,NKV,HD,L=28,8,128,3000
SLAB=NL*2*NKV*HD*2*L/1e9
free,_=torch.cuda.mem_get_info()
POOL=free/1e9-2.5
CAP_R1=int((POOL-a.vision_gb)/SLAB)          # R1 静态保留视觉工作区
CAP_AWAKE=int((POOL-a.vision_gb-1.0)/SLAB)   # RS/RB decode集显存上限(同样让出视觉工作区)
N = a.pool
print(f"SLAB {SLAB:.3f}GB 池 {POOL:.1f}GB  R1准入{CAP_R1}  唤醒集上限{CAP_AWAKE}  agent池{N}", flush=True)
sR=torch.cuda.Stream(priority=-1); sL=torch.cuda.Stream(); sV=torch.cuda.Stream()
# 每agent一个 host pinned 槽(RS用); 设备驻留槽(R1用)
host_slab=[ (torch.empty(NL,NKV,L,HD,dtype=torch.bfloat16,pin_memory=True),
             torch.empty(NL,NKV,L,HD,dtype=torch.bfloat16,pin_memory=True)) for _ in range(N if a.arm=='RS' else 0)]
dev_slab={}   # R1: agent -> (K,V) 常驻
if a.arm=='R1':
    with torch.cuda.stream(sL):
        for i in range(CAP_R1):
            dev_slab[i]=(torch.randn(NL,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,
                         torch.randn(NL,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02)
    sL.synchronize()
# RS: pinned 槽不做内容初始化(吞吐物理与内容无关)
REBUILD_S=3.0*0.150   # 1.7B? 用8B常数太贵; 1.7B重建3k tok ~ 3*48ms=145ms
REBUILD_S=0.145
# agent 状态机(错相): awake期 U(1.5,2.5)s, wait期 U(4,8)s
rng=random.Random(7)
admitted = list(range(CAP_R1)) if a.arm=='R1' else list(range(N))
phase={i:('wait', rng.uniform(0,6)) for i in admitted}   # 初始随机相位
merged=None; members=[]
pause=threading.Event(); idle=threading.Event()
stop=False; frames=[]; tok=[0]; vlat=[]; wake_lat=[]; rebuild_gpu_s=[0.0]
def build_merged(mem):
    """按成员集重组合并cache: R1 从dev_slab拷; RS 从host H2D; RB 计重建GPU时间(合并进prefill计时)。"""
    global merged,members
    t0=time.perf_counter()
    with torch.cuda.stream(sL):
        c=DynamicCache()
        B=len(mem)
        if B>0:
            for li in range(NL):
                k=torch.empty(B,NKV,L,HD,dtype=torch.bfloat16,device=dev)
                v=torch.empty(B,NKV,L,HD,dtype=torch.bfloat16,device=dev)
                for bi,ag in enumerate(mem):
                    if a.arm=='R1':
                        k[bi]=dev_slab[ag][0][li]; v[bi]=dev_slab[ag][1][li]
                    elif a.arm=='RS':
                        k[bi].copy_(host_slab[ag][0][li],non_blocking=True)
                        v[bi].copy_(host_slab[ag][1][li],non_blocking=True)
                    else:
                        k[bi].normal_(0,0.02); v[bi].normal_(0,0.02)  # RB: 内容重建(计时另算)
                c.update(k,v,li)
    sL.synchronize()
    merged=c; members=list(mem)
    return (time.perf_counter()-t0)
def th_sched():
    """0.25s tick: 推进状态机, 重组合并批。"""
    global merged
    nwake_pending=[]
    while not stop:
        time.sleep(0.25)
        now=time.perf_counter()
        changed=False; awake=[]
        for i in admitted:
            st,t_end=phase[i]
            if now>=t_end:
                if st=='wait':
                    phase[i]=('awake', now+rng.uniform(1.5,2.5)); changed=True
                    if a.arm=='RB': rebuild_gpu_s[0]+=REBUILD_S
                else:
                    phase[i]=('wait', now+rng.uniform(4,8)); changed=True
            if phase[i][0]=='awake': awake.append(i)
        awake=awake[:CAP_AWAKE if a.arm!='R1' else CAP_R1]
        if changed or merged is None:
            t0=time.perf_counter()
            idle.clear(); pause.set(); idle.wait(timeout=5)
            bt=build_merged(awake)
            pause.clear()
            wake_lat.append((time.perf_counter()-t0)*1000)
def th_llm():
    p0=[L]
    while not stop:
        if pause.is_set() or merged is None or len(members)==0:
            idle.set(); time.sleep(0.002); continue
        idle.clear()
        B=len(members)
        d=torch.zeros(B,1,dtype=torch.long,device=dev)
        S=merged.get_seq_length()
        with torch.cuda.stream(sL), torch.inference_mode():
            for _ in range(4):
                pos=torch.full((B,1),S,dtype=torch.long,device=dev)
                model(input_ids=d,past_key_values=merged,position_ids=pos,cache_position=pos[0]); S+=1
        sL.synchronize()
        # RB 的重建GPU时间: 从decode时间中扣(模拟同卡串行)
        if rebuild_gpu_s[0]>0:
            tpay=min(rebuild_gpu_s[0],0.5); rebuild_gpu_s[0]-=tpay; time.sleep(tpay)
        tok[0]+=B*4
x=torch.randn(2048,2048,device=dev,dtype=torch.bfloat16); y=torch.randn_like(x); rout=torch.empty_like(x)
torch.mm(x,y,out=rout); torch.cuda.synchronize()
t0=time.perf_counter(); torch.mm(x,y,out=rout); torch.cuda.synchronize(); unit=(time.perf_counter()-t0)*1000
R_ITER=max(1,int(5.0/unit))
def th_render():
    nxt=time.perf_counter()
    while not stop:
        nxt+=FRAME
        with torch.cuda.stream(sR):
            t0=time.perf_counter()
            for _ in range(R_ITER): torch.mm(x,y,out=rout)
            ev=torch.cuda.Event(); ev.record(sR)
        while not ev.query(): time.sleep(0.001)
        frames.append((time.perf_counter()-t0)*1000)
        d=nxt-time.perf_counter()
        if d>0: time.sleep(d)
        else: nxt=time.perf_counter()
def th_vision():
    vx=torch.randn(4096,4096,device=dev,dtype=torch.bfloat16); vy=torch.randn_like(vx); vout=torch.empty_like(vx)
    ws_static=torch.empty(int(a.vision_gb*1e9/2),dtype=torch.bfloat16,device=dev) if a.arm=='R1' else None
    while not stop:
        time.sleep(8.0)
        if stop: break
        t_arr=time.perf_counter()
        if a.arm=='R1': ws=ws_static
        else:
            try: ws=torch.empty(int(a.vision_gb*1e9/2),dtype=torch.bfloat16,device=dev)
            except torch.OutOfMemoryError: vlat.append(-1); continue
        with torch.cuda.stream(sV):
            for _ in range(max(1,int(300/(unit*4)))): torch.mm(vx,vy,out=vout)
        sV.synchronize()
        if a.arm!='R1': del ws; torch.cuda.empty_cache()
        vlat.append((time.perf_counter()-t_arr)*1000)
import traceback
def wrap(f):
    def g():
        try: f()
        except Exception: traceback.print_exc()
    return g
ths=[threading.Thread(target=wrap(f)) for f in (th_sched,th_llm,th_render,th_vision)]
t0=time.perf_counter()
for t in ths: t.start()
time.sleep(a.dur); stop=True; pause.clear()
for t in ths: t.join(timeout=20)
dur=time.perf_counter()-t0
fr=np.array(frames[5:]); good=[v for v in vlat if v>0]
out=dict(arm=a.arm,admitted=len(admitted),cap=CAP_R1 if a.arm=='R1' else CAP_AWAKE,
         p99=float(np.percentile(fr,99)),miss=float(100*np.mean(fr>FRAME*1000)),
         llm_tps=tok[0]/dur, avg_awake=float(np.mean([len(members)])),
         regroup_ms=float(np.mean(wake_lat)) if wake_lat else 0,
         vision_ms=float(np.mean(good)) if good else -1, vision_fail=sum(1 for v in vlat if v<0))
print(json.dumps(out,indent=1))
if a.out: json.dump(out,open(a.out,'w'))

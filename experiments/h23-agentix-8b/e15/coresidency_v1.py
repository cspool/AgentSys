"""E15 v1: 端侧多模态共驻仲裁 harness。单进程单卡三流:
R 渲染代理(16.67ms 帧节拍, 定额GEMM ~5ms solo, 硬SLO) /
L LLM decode(Qwen3-1.7B, B=8@3k 合成KV, 软吞吐) /
V 视觉突发(每2s一次 ~300ms 大GEMM 串, 软时延)。
臂: A 无仲裁 / P 渲染高优先级 / E1 P+突发期LLM门控 / S 静态SM分区(smctrl) /
E2 本方案: 渲染小分区保留+优先级+视觉切块+LLM节流(不停摆)。
指标: 帧 P50/P99/miss%(预算16.67ms), LLM tok/s, 视觉突发完成时延。"""
import argparse,threading,time,json,sys
import torch
sys.path.insert(0,'/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3/common')
ap=argparse.ArgumentParser()
ap.add_argument('--arm',required=True,choices=['A','P','E1','S','E2'])
ap.add_argument('--dur',type=float,default=20.0)
ap.add_argument('--render-ms',type=float,default=5.0)
ap.add_argument('--out',default='')
a=ap.parse_args()
torch.cuda.init()
dev='cuda'
FRAME=1/60.0
# ---- 校准渲染核与视觉块 ----
def gemm_ms(n,iters=1,stream=None):
    x=torch.randn(n,n,device=dev,dtype=torch.bfloat16); y=torch.randn(n,n,device=dev,dtype=torch.bfloat16)
    s=stream or torch.cuda.current_stream()
    with torch.cuda.stream(s):
        for _ in range(3): x@y
        torch.cuda.synchronize(); t0=time.perf_counter()
        for _ in range(iters): x@y
        torch.cuda.synchronize()
    return (time.perf_counter()-t0)/iters*1000, (x,y)
# 渲染: 找单次 ~a.render_ms 的 GEMM 重复数(用 2048 核)
base_ms,rmat=gemm_ms(2048)
R_ITER=max(1,int(a.render_ms/base_ms))
# 视觉: 4096 大核
vb_ms,vmat=gemm_ms(4096)
V_ITER=max(1,int(300/vb_ms))          # ~300ms 突发
V_CHUNK=max(1,int(8/vb_ms)) or 1      # E2: 每块 ~8ms
print(f"校准: render核 {base_ms:.2f}ms x{R_ITER} ≈{base_ms*R_ITER:.1f}ms | 视觉核 {vb_ms:.1f}ms x{V_ITER}≈{vb_ms*V_ITER:.0f}ms, E2块={V_CHUNK}核", flush=True)
# ---- LLM ----
from transformers import AutoModelForCausalLM, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
NL,NKV,HD=28,8,128; B,L=8,3000
cache=DynamicCache()
for i in range(NL):
    cache.update(torch.randn(B,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,
                 torch.randn(B,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,i)
dummy=torch.zeros(B,1,dtype=torch.long,device=dev)
# ---- 流与优先级 ----
prio_hi,prio_lo=torch.cuda.Stream(priority=-1),0
if a.arm in ('P','E1','E2','S'):
    sR=torch.cuda.Stream(priority=-1)
else:
    sR=torch.cuda.Stream()
sL=torch.cuda.Stream(); sV=torch.cuda.Stream()
if a.arm=='S':
    from smctrl import SmCtrl
    sc=SmCtrl(0)
    T=sc.total_tpcs
    RT=max(8,int(T*0.35))
    sc.set_stream(sR, 0, RT)            # 渲染按工作量定尺寸(~35%)
    sc.set_stream(sL, RT, T)
    sc.set_stream(sV, RT, T)
    print(f"S臂: TPC总{T}, 渲染[0,{RT}), 其余共享", flush=True)
if a.arm=='E2':
    from smctrl import SmCtrl
    sc=SmCtrl(0)
    T=sc.total_tpcs
    sc.set_stream(sR, 0, max(6,T//10))           # 渲染保留 ~1/10
    # L/V 不设掩码(全卡), 靠优先级+节流
stop=False
vision_active=threading.Event()
frames=[]; llm_tok=[0]; vlat=[]
def th_render():
    x,y=rmat
    nxt=time.perf_counter()
    while not stop:
        nxt+=FRAME
        with torch.cuda.stream(sR):
            t0=time.perf_counter()
            for _ in range(R_ITER): x@y
            ev=torch.cuda.Event(); ev.record(sR)
        while not ev.query():
            time.sleep(0.001)
        frames.append((time.perf_counter()-t0)*1000)
        d=nxt-time.perf_counter()
        if d>0: time.sleep(d)
        else: nxt=time.perf_counter()
def th_llm():
    p0=L
    while not stop:
        if a.arm=='E1' and vision_active.is_set():
            time.sleep(0.002); continue
        if a.arm=='E2' and vision_active.is_set():
            time.sleep(0.004)                     # 节流: 突发期降速不停摆
        with torch.cuda.stream(sL), torch.inference_mode():
            for _ in range(8):
                pos=torch.full((B,1),p0,dtype=torch.long,device=dev)
                model(input_ids=dummy,past_key_values=cache,position_ids=pos,cache_position=pos[0])
                p0+=1
        sL.synchronize()
        llm_tok[0]+=B*8
def th_vision():
    x,y=vmat
    while not stop:
        time.sleep(2.0)
        if stop: break
        vision_active.set(); t0=time.perf_counter()
        with torch.cuda.stream(sV):
            if a.arm=='E2':
                for i in range(V_ITER):
                    x@y
                    if (i+1)%V_CHUNK==0:
                        sV.synchronize()          # 切块+让出
                        time.sleep(0.002)
            else:
                for _ in range(V_ITER): x@y
        sV.synchronize()
        vlat.append((time.perf_counter()-t0)*1000)
        vision_active.clear()
ths=[threading.Thread(target=f) for f in (th_render,th_llm,th_vision)]
t0=time.perf_counter()
for t in ths: t.start()
time.sleep(a.dur); stop=True
for t in ths: t.join(timeout=10)
dur=time.perf_counter()-t0
import numpy as np
fr=np.array(frames[5:])
miss=100*np.mean(fr>FRAME*1000)
out=dict(arm=a.arm,frames=len(fr),p50=float(np.percentile(fr,50)),p99=float(np.percentile(fr,99)),
         miss_pct=float(miss), llm_tps=llm_tok[0]/dur,
         vision_ms=float(np.mean(vlat)) if vlat else -1, n_vision=len(vlat))
print(json.dumps(out,indent=1))
if a.out: json.dump(out,open(a.out,'w'))

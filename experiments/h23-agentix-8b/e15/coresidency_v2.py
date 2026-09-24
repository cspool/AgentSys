"""E15 v2: 显存维仲裁。渲染(P优先级,硬SLO) + LLM(KV池尽显存, B=池/344MB) + 视觉突发(8GB瞬时工作区,每2s~300ms)。
臂: R1 静态保留8GB(基线) / R2 按需让渡(突发时切片换出pinned, 恢复换回) / R3 预告让渡(200ms预告窗内重叠换出)。
指标: LLM tok/s(主) / 视觉E2E时延(含等内存) / 帧P99&miss。精度: 换出换回=同字节。"""
import argparse,threading,time,json
import torch,numpy as np
ap=argparse.ArgumentParser()
ap.add_argument('--arm',required=True,choices=['R1','R2','R3'])
ap.add_argument('--dur',type=float,default=24.0)
ap.add_argument('--vision-gb',type=float,default=8.0)
ap.add_argument('--out',default='')
a=ap.parse_args()
dev='cuda'; FRAME=1/60.0
from transformers import AutoModelForCausalLM, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
NL,NKV,HD,L=28,8,128,3000
SLAB=NL*2*NKV*HD*2*L/1e9     # GB/agent
free,_=torch.cuda.mem_get_info()
POOL=(free/1e9)-2.5  # 留2.5GB给激活/渲染/杂项
B_full=int(POOL/SLAB); B_res=int((POOL-a.vision_gb)/SLAB)
B0 = B_res if a.arm=='R1' else B_full
YIELD = B_full-B_res         # 突发需让出的agent数
print(f"SLAB={SLAB:.3f}GB 池={POOL:.1f}GB -> B_full={B_full} B_res={B_res} 让渡{YIELD}", flush=True)
def make_cache(B):
    c=DynamicCache()
    for i in range(NL):
        c.update(torch.randn(B,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,
                 torch.randn(B,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,i)
    return c
cache=make_cache(B0); curB=[B0]
host_buf=[( torch.empty(YIELD,NKV,L,HD,dtype=torch.bfloat16,pin_memory=True),
            torch.empty(YIELD,NKV,L,HD,dtype=torch.bfloat16,pin_memory=True)) for _ in range(NL)] if a.arm!='R1' else None
lock=threading.Lock()
pause_req=threading.Event(); llm_idle=threading.Event(); reset_p=threading.Event()
def yield_mem():
    """切片换出后 YIELD 个 agent -> pinned host, 缓存缩为 B_res。返回耗时ms。"""
    global cache
    t0=time.perf_counter()
    pause_req.set(); llm_idle.wait(timeout=5)
    if True:
        for l in cache.layers:   # 裁回 L(丢弃合成decode尾巴)
            l.keys=l.keys[:,:,:L,:].contiguous(); l.values=l.values[:,:,:L,:].contiguous()
        for i,l in enumerate(cache.layers):
            host_buf[i][0][:].copy_(l.keys[B_res:],non_blocking=True)
            host_buf[i][1][:].copy_(l.values[B_res:],non_blocking=True)
        torch.cuda.synchronize()
        for l in cache.layers:
            l.keys=l.keys[:B_res].contiguous(); l.values=l.values[:B_res].contiguous()
        torch.cuda.empty_cache(); curB[0]=B_res
    reset_p.set()
    pause_req.clear()
    return (time.perf_counter()-t0)*1000
def restore_mem():
    global cache
    t0=time.perf_counter()
    pause_req.set(); llm_idle.wait(timeout=5)
    if True:
        for i,l in enumerate(cache.layers):
            k=torch.empty(B_full,NKV,L,HD,dtype=torch.bfloat16,device=dev)
            v=torch.empty(B_full,NKV,L,HD,dtype=torch.bfloat16,device=dev)
            k[:B_res]=l.keys; v[:B_res]=l.values
            k[B_res:].copy_(host_buf[i][0],non_blocking=True); v[B_res:].copy_(host_buf[i][1],non_blocking=True)
            l.keys=k; l.values=v
        torch.cuda.synchronize(); curB[0]=B_full
    reset_p.set()
    pause_req.clear()
    return (time.perf_counter()-t0)*1000
# 渲染
r_ms=5.0
x=torch.randn(2048,2048,device=dev,dtype=torch.bfloat16); y=torch.randn(2048,2048,device=dev,dtype=torch.bfloat16)
rout=torch.empty(2048,2048,device=dev,dtype=torch.bfloat16)
with torch.cuda.stream(torch.cuda.current_stream()):
    for _ in range(3): x@y
torch.cuda.synchronize()
t0=time.perf_counter(); x@y; torch.cuda.synchronize(); unit=(time.perf_counter()-t0)*1000
R_ITER=max(1,int(r_ms/unit))
sR=torch.cuda.Stream(priority=-1); sL=torch.cuda.Stream(); sV=torch.cuda.Stream()
stop=False; frames=[]; tok=[0]; vlat=[]; ylog=[]
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
def th_llm():
    p0=L; dummy=None
    while not stop:
        if pause_req.is_set():
            llm_idle.set(); time.sleep(0.002); continue
        llm_idle.clear()
        if reset_p.is_set(): p0=L; reset_p.clear()
        B=curB[0]
        if dummy is None or dummy.shape[0]!=B:
            dummy=torch.zeros(B,1,dtype=torch.long,device=dev)
        with torch.cuda.stream(sL), torch.inference_mode():
            for _ in range(4):
                pos=torch.full((B,1),p0,dtype=torch.long,device=dev)
                model(input_ids=dummy,past_key_values=cache,position_ids=pos,cache_position=pos[0])
                p0+=1
        sL.synchronize()
        tok[0]+=B*4
        if p0>L+800: p0=L
def th_vision():
    vx=torch.randn(4096,4096,device=dev,dtype=torch.bfloat16)
    vy=torch.randn(4096,4096,device=dev,dtype=torch.bfloat16)
    vout=torch.empty(4096,4096,device=dev,dtype=torch.bfloat16)
    ws_static=torch.empty(int(a.vision_gb*1e9/2),dtype=torch.bfloat16,device=dev) if a.arm=='R1' else None
    while not stop:
        time.sleep(2.0)
        if stop: break
        t_arr=time.perf_counter()
        if a.arm=='R3':
            ymies=yield_mem(); time.sleep(max(0,0.2-ymies/1000))  # 预告窗200ms内完成换出
            t_arr=time.perf_counter()                             # 预告后到达
        elif a.arm=='R2':
            ymies=yield_mem()
        else: ymies=0
        ylog.append(ymies)
        if a.arm=='R1':
            ws=ws_static
        else:
            try:
                ws=torch.empty(int(a.vision_gb*1e9/2),dtype=torch.bfloat16,device=dev)
            except torch.OutOfMemoryError:
                vlat.append(-1); restore_mem(); continue
        with torch.cuda.stream(sV):
            n=int(300/ (unit*4))
            for _ in range(max(1,n)): torch.mm(vx,vy,out=vout)
        sV.synchronize()
        if a.arm!='R1':
            del ws; torch.cuda.empty_cache()
        vlat.append((time.perf_counter()-t_arr)*1000)
        if a.arm!='R1': restore_mem()
ths=[threading.Thread(target=f) for f in (th_render,th_llm,th_vision)]
t0=time.perf_counter()
for t in ths: t.start()
time.sleep(a.dur); stop=True
for t in ths: t.join(timeout=15)
dur=time.perf_counter()-t0
fr=np.array(frames[5:])
out=dict(arm=a.arm,B0=B0,B_full=B_full,B_res=B_res,
         p99=float(np.percentile(fr,99)),miss=float(100*np.mean(fr>FRAME*1000)),
         llm_tps=tok[0]/dur, vision_ms=float(np.mean([v for v in vlat if v>0])) if vlat else -1,
         vision_fail=sum(1 for v in vlat if v<0), yield_ms=float(np.mean(ylog)) if ylog else 0)
print(json.dumps(out,indent=1))
if a.out: json.dump(out,open(a.out,'w'))

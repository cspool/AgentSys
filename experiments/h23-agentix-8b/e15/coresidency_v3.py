"""E15 v3: 双组KV弹性让渡。cache_A(常驻 B_res) + cache_B(可让渡 YIELD个);
让渡=暂停decode->D2H(cache_B)->释放->恢复A组decode; 归还=alloc+H2D->双组decode。
R1 静态保留(仅A组, 视觉工作区常驻) / R2 按需让渡 / R3 预告让渡(300ms预告窗重叠D2H)。
视觉: 每8s一次, 6GB工作区+~300ms计算。渲染: 60fps 5ms核, 高优先级。"""
import argparse,threading,time,json
import torch,numpy as np
ap=argparse.ArgumentParser()
ap.add_argument('--arm',required=True,choices=['R1','R2','R3'])
ap.add_argument('--dur',type=float,default=32.0)
ap.add_argument('--vision-gb',type=float,default=6.0)
ap.add_argument('--period',type=float,default=8.0)
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
B_full=int(POOL/SLAB); B_res=int((POOL-a.vision_gb-0.8)/SLAB)  # 让渡组多留0.8GB余量
YIELD=B_full-B_res
print(f"SLAB {SLAB:.3f}GB 池 {POOL:.1f}GB -> A组{B_res} + B组{YIELD}", flush=True)
SEQ_MAX=L+600
sR=torch.cuda.Stream(priority=-1); sL=torch.cuda.Stream(); sV=torch.cuda.Stream()
def mk(B):
    c=DynamicCache()
    with torch.cuda.stream(sL):
        for i in range(NL):
            c.update(torch.randn(B,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,
                     torch.randn(B,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,i)
    sL.synchronize()
    return c
cacheA=mk(B_res)
cacheB=mk(YIELD) if a.arm!='R1' else None
HB_N=YIELD*NKV*SEQ_MAX*HD
hostB=[(torch.empty(HB_N,dtype=torch.bfloat16,pin_memory=True),
        torch.empty(HB_N,dtype=torch.bfloat16,pin_memory=True)) for _ in range(NL)] if a.arm!='R1' else None
B_active=[B_res+(YIELD if a.arm!='R1' else 0)]
pause=threading.Event(); idle=threading.Event()
DBG=[0]
def yield_B():
    global cacheB
    t0=time.perf_counter()
    idle.clear(); pause.set(); idle.wait(timeout=5)
    S=cacheB.get_seq_length()
    n=YIELD*NKV*S*HD
    with torch.cuda.stream(sL):
        for i,l in enumerate(cacheB.layers):
            hostB[i][0][:n].copy_(l.keys.reshape(-1),non_blocking=True)
            hostB[i][1][:n].copy_(l.values.reshape(-1),non_blocking=True)
    torch.cuda.synchronize()
    cacheB=None; torch.cuda.empty_cache()
    B_active[0]=B_res; pause.clear()
    return (time.perf_counter()-t0)*1000, S
def restore_B(S):
    global cacheB
    t0=time.perf_counter()
    idle.clear(); pause.set(); idle.wait(timeout=5)
    c=DynamicCache()
    with torch.cuda.stream(sL):
        for i in range(NL):
            n=YIELD*NKV*S*HD
            k=torch.empty(YIELD,NKV,S,HD,dtype=torch.bfloat16,device=dev)
            v=torch.empty(YIELD,NKV,S,HD,dtype=torch.bfloat16,device=dev)
            k.reshape(-1).copy_(hostB[i][0][:n],non_blocking=True); v.reshape(-1).copy_(hostB[i][1][:n],non_blocking=True)
            c.update(k,v,i)
    torch.cuda.synchronize()
    cacheB=c; B_active[0]=B_res+YIELD; pause.clear()
    return (time.perf_counter()-t0)*1000
# 渲染
x=torch.randn(2048,2048,device=dev,dtype=torch.bfloat16); y=torch.randn_like(x); rout=torch.empty_like(x)
for _ in range(3): torch.mm(x,y,out=rout)
torch.cuda.synchronize(); t0=time.perf_counter(); torch.mm(x,y,out=rout); torch.cuda.synchronize()
unit=(time.perf_counter()-t0)*1000; R_ITER=max(1,int(5.0/unit))

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
    pA=[L]; pB=[L]; dA=torch.zeros(B_res,1,dtype=torch.long,device=dev)
    dB=torch.zeros(YIELD,1,dtype=torch.long,device=dev) if a.arm!='R1' else None
    while not stop:
        if pause.is_set():
            idle.set(); time.sleep(0.002); continue
        idle.clear()
        with torch.cuda.stream(sL), torch.inference_mode():
            for _ in range(4):
                pos=torch.full((B_res,1),pA[0],dtype=torch.long,device=dev)
                model(input_ids=dA,past_key_values=cacheA,position_ids=pos,cache_position=pos[0]); pA[0]+=1
            if cacheB is not None:
                pB[0]=cacheB.get_seq_length()
                for _ in range(4):
                    pos=torch.full((YIELD,1),pB[0],dtype=torch.long,device=dev)
                    model(input_ids=dB,past_key_values=cacheB,position_ids=pos,cache_position=pos[0]); pB[0]+=1
        sL.synchronize()
        tok[0]+=B_res*4+(YIELD*4 if cacheB is not None else 0)
        DBG[0]+=1
        if DBG[0]%50==0: print(f"[L] iter{DBG[0]} tok={tok[0]}",flush=True)
        if pA[0]>SEQ_MAX-8:  # 裁回, 防溢出
            with torch.cuda.stream(sL):
                for l in cacheA.layers:
                    l.keys=l.keys[:,:,:L,:].contiguous(); l.values=l.values[:,:,:L,:].contiguous()
            sL.synchronize(); pA[0]=L
        if cacheB is not None and cacheB.get_seq_length()>SEQ_MAX-8:
            with torch.cuda.stream(sL):
                for l in cacheB.layers:
                    l.keys=l.keys[:,:,:L,:].contiguous(); l.values=l.values[:,:,:L,:].contiguous()
            sL.synchronize()
def th_vision():
    vx=torch.randn(4096,4096,device=dev,dtype=torch.bfloat16); vy=torch.randn_like(vx); vout=torch.empty_like(vx)
    ws_static=torch.empty(int(a.vision_gb*1e9/2),dtype=torch.bfloat16,device=dev) if a.arm=='R1' else None
    while not stop:
        time.sleep(a.period)
        if stop: break
        print(f"[V] burst start t={time.perf_counter():.1f}",flush=True)
        if a.arm=='R3':
            ym,S=yield_B(); time.sleep(max(0,0.3-ym/1000)); ylog.append(ym)
            t_arr=time.perf_counter()
        else:
            t_arr=time.perf_counter()
            if a.arm=='R2':
                ym,S=yield_B(); ylog.append(ym)
        if a.arm=='R1': ws=ws_static
        else:
            try: ws=torch.empty(int(a.vision_gb*1e9/2),dtype=torch.bfloat16,device=dev)
            except torch.OutOfMemoryError:
                vlat.append(-1); restore_B(S); continue
        with torch.cuda.stream(sV):
            n=max(1,int(300/(unit*4)))
            for _ in range(n): torch.mm(vx,vy,out=vout)
        sV.synchronize()
        if a.arm!='R1': del ws; torch.cuda.empty_cache()
        vlat.append((time.perf_counter()-t_arr)*1000)
        if a.arm!='R1':
            print(f"[V] restore begin",flush=True); rm=restore_B(S)
            print(f"[V] restore done {rm:.0f}ms",flush=True)
import traceback
def wrap(f):
    def g():
        try: f()
        except Exception:
            traceback.print_exc()
    return g
ths=[threading.Thread(target=wrap(f)) for f in (th_render,th_llm,th_vision)]
t0=time.perf_counter()
for t in ths: t.start()
time.sleep(a.dur); stop=True; pause.clear()
for t in ths: t.join(timeout=20)
dur=time.perf_counter()-t0
fr=np.array(frames[5:])
good=[v for v in vlat if v>0]
out=dict(arm=a.arm,B_res=B_res,YIELD=YIELD,
         p99=float(np.percentile(fr,99)),miss=float(100*np.mean(fr>FRAME*1000)),
         llm_tps=tok[0]/dur, vision_ms=float(np.mean(good)) if good else -1,
         vision_fail=sum(1 for v in vlat if v<0), n_vision=len(vlat),
         yield_ms=float(np.mean(ylog)) if ylog else 0)
print(json.dumps(out,indent=1))
if a.out: json.dump(out,open(a.out,'w'))

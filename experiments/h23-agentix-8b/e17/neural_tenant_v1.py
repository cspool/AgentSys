"""C5-min: 双神经租户共驻。神经渲染=每帧串行DiT式GEMM链(10fps,100ms预算,算力密度可扫);
agent LLM = B=8@3k 批量decode 持续。臂: A2自由 / P2渲染高优先级 / G2门控(帧窗内LLM暂停)。
指标: 神经帧P99/miss + LLM tok/s。交付: 优先级定律的失效边界曲线。"""
import argparse,threading,time,json
import torch,numpy as np
ap=argparse.ArgumentParser()
ap.add_argument('--arm',required=True,choices=['A2','P2','G2'])
ap.add_argument('--frame-ms',type=float,default=40.0)   # 每帧solo算力
ap.add_argument('--dur',type=float,default=60.0)
ap.add_argument('--llm-mode',default='decode',choices=['decode','prefill'])
ap.add_argument('--chunk',type=int,default=512)
ap.add_argument('--out',default='')
a=ap.parse_args()
dev='cuda'; PERIOD=0.1  # 10fps
from transformers import AutoModelForCausalLM, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
NL,NKV,HD,L,B=28,8,128,3000,8
cache=DynamicCache()
for i in range(NL):
    cache.update(torch.randn(B,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,
                 torch.randn(B,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,i)
sN=torch.cuda.Stream(priority=-1 if a.arm in ('P2','G2') else 0)
sL=torch.cuda.Stream()
nx=torch.randn(4096,4096,device=dev,dtype=torch.bfloat16); ny=torch.randn_like(nx); no=torch.empty_like(nx)
torch.mm(nx,ny,out=no); torch.cuda.synchronize()
t0=time.perf_counter(); torch.mm(nx,ny,out=no); torch.cuda.synchronize()
unit=(time.perf_counter()-t0)*1000
STEPS=max(1,int(a.frame_ms/unit))
stop=False; frames=[]; tok=[0]; in_frame=threading.Event()
def th_neural():
    nxt=time.perf_counter()
    while not stop:
        nxt+=PERIOD
        in_frame.set()
        with torch.cuda.stream(sN):
            t0=time.perf_counter()
            for _ in range(STEPS): torch.mm(nx,ny,out=no)
            ev=torch.cuda.Event(); ev.record(sN)
        while not ev.query(): time.sleep(0.001)
        frames.append((time.perf_counter()-t0)*1000)
        in_frame.clear()
        d=nxt-time.perf_counter()
        if d>0: time.sleep(d)
        else: nxt=time.perf_counter()
def th_llm():
    S=[L]; d=torch.zeros(B,1,dtype=torch.long,device=dev)
    pf=torch.zeros(1,a.chunk,dtype=torch.long,device=dev) if a.llm_mode=='prefill' else None
    pc=None
    while not stop:
        if a.arm=='G2' and in_frame.is_set():
            time.sleep(0.002); continue
        if a.llm_mode=='prefill':
            with torch.cuda.stream(sL), torch.inference_mode():
                pc=DynamicCache()
                pos=torch.arange(a.chunk,device=dev).unsqueeze(0)
                model(input_ids=pf,past_key_values=pc,position_ids=pos,cache_position=pos[0])
            sL.synchronize(); del pc
            tok[0]+=a.chunk
        else:
            with torch.cuda.stream(sL), torch.inference_mode():
                for _ in range(4):
                    pos=torch.full((B,1),S[0],dtype=torch.long,device=dev)
                    model(input_ids=d,past_key_values=cache,position_ids=pos,cache_position=pos[0]); S[0]+=1
            sL.synchronize()
            tok[0]+=B*4
        if S[0]>L+400:
            with torch.cuda.stream(sL), torch.inference_mode():
                for l in cache.layers:
                    l.keys=l.keys[:,:,:L,:].contiguous(); l.values=l.values[:,:,:L,:].contiguous()
            sL.synchronize(); S[0]=L
import traceback
def wrap(f):
    def g():
        try: f()
        except Exception: traceback.print_exc()
    return g
ths=[threading.Thread(target=wrap(f)) for f in (th_neural,th_llm)]
T0=time.perf_counter()
for t in ths: t.start()
time.sleep(a.dur); stop=True
for t in ths: t.join(timeout=15)
dur=time.perf_counter()-T0
fr=np.array(frames[30:])
out=dict(arm=a.arm,frame_ms=a.frame_ms,steps=STEPS,mode=a.llm_mode,chunk=a.chunk,
         p99=float(np.percentile(fr,99)),miss=float(100*np.mean(fr>PERIOD*1000)),
         llm_tps=tok[0]/dur)
print(json.dumps(out))
if a.out: json.dump(out,open(a.out,'w'))

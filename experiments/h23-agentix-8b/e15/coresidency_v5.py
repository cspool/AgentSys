"""E15 v5: agent等待循环显存仲裁(增量换入换出版)。
R1 驻留: 33席常驻GPU, 醒者~25% -> decode B~8。
RB 丢弃重建: 池128, 醒即重建(GPU时间0.145s/次注入)。
RS 换出停放(本方案): 池128, 睡D2H(18ms)醒H2D, 醒集decode(上限32)。
共驻: 渲染60fps P优先级 + 视觉6GB突发每8s(RS/RB从空闲显存拿, R1静态保留)。"""
import argparse,threading,time,json,random,traceback
import torch,numpy as np
ap=argparse.ArgumentParser()
ap.add_argument('--arm',required=True,choices=['R1','RB','RS','RSr'])
ap.add_argument('--dur',type=float,default=45.0)
ap.add_argument('--seed',type=int,default=7)
ap.add_argument('--pool',type=int,default=64)
ap.add_argument('--vision-gb',type=float,default=6.0)
ap.add_argument('--out',default='')
a=ap.parse_args()
dev='cuda'; FRAME=1/60.0
from transformers import AutoModelForCausalLM, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
NL,NKV,HD,L=28,8,128,3000
SLAB=NL*NKV*L*HD*2*2/1e9
free,_=torch.cuda.mem_get_info(); POOL=free/1e9-2.5
CAP_R1=int((POOL-a.vision_gb)/SLAB)
CAP_AW=min(16,int(((POOL-a.vision_gb-1.0)/2)/SLAB))  # 双缓冲(slab库+合并副本)各占一半
N=a.pool
print(f"SLAB {SLAB:.3f}GB 池{POOL:.1f}GB R1席{CAP_R1} 醒集上限{CAP_AW} pool{N}",flush=True)
sR=torch.cuda.Stream(priority=-1); sL=torch.cuda.Stream(); sV=torch.cuda.Stream()
REBUILD_S=0.145
rng=random.Random(a.seed)
admitted=list(range(CAP_R1)) if a.arm=='R1' else list(range(N))
# 槽: [NL,NKV,L,HD] K与V
def dev_pair():
    return (torch.randn(NL,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,
            torch.randn(NL,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02)
dev_slab={}; host_slab={}
with torch.cuda.stream(sL):
    if a.arm=='R1':
        for i in admitted: dev_slab[i]=dev_pair()
sL.synchronize()
if a.arm in ('RS','RSr'):
    for i in admitted:
        host_slab[i]=(torch.empty(NL,NKV,L,HD,dtype=torch.bfloat16,pin_memory=True),
                      torch.empty(NL,NKV,L,HD,dtype=torch.bfloat16,pin_memory=True))
phase={i:('wait',rng.uniform(0,10)+time.perf_counter()) for i in admitted}
merged=[None]; members=[[]]
pause=threading.Event(); idle=threading.Event()
stop=False; frames=[]; tok=[0]; vlat=[]; trans_ms=[]; rebuild_debt=[0.0]
DBG={'blk':0,'bt':0.0,'t0':0,'cap':0,'idle':0}
def assemble(mem):
    t0=time.perf_counter()
    with torch.cuda.stream(sL):
        c=DynamicCache()
        if mem:
            for li in range(NL):
                k=torch.stack([dev_slab[ag][0][li] for ag in mem])
                v=torch.stack([dev_slab[ag][1][li] for ag in mem])
                c.update(k,v,li)
    sL.synchronize()
    merged[0]=c; members[0]=list(mem)
    return (time.perf_counter()-t0)*1000
def th_sched():
    while not stop:
        time.sleep(1.0)
        now=time.perf_counter(); changed=[]
        for i in admitted:
            st,te=phase[i]
            if now>=te:
                if st=='wait': phase[i]=('awake',now+rng.uniform(2,3))
                else: phase[i]=('wait',now+rng.uniform(6,10))
                changed.append(i)
        need_trim = merged[0] is not None and merged[0].get_seq_length()>L+300
        if not changed and merged[0] is not None and not need_trim: continue
        if not changed and need_trim:   # 仅裁剪: 暂停内原地裁, 不重组
            idle.clear(); pause.set(); idle.wait(timeout=5)
            try:
                with torch.cuda.stream(sL):
                    for l in merged[0].layers:
                        l.keys=l.keys[:,:,:L,:].contiguous(); l.values=l.values[:,:,:L,:].contiguous()
                sL.synchronize()
            except Exception: traceback.print_exc()
            finally: pause.clear()
            continue
        awake=[i for i in admitted if phase[i][0]=='awake'][:CAP_AW if a.arm!='R1' else CAP_R1]
        t0=time.perf_counter()
        idle.clear(); pause.set(); idle.wait(timeout=5)
        try:
            with torch.cuda.stream(sL):
                for i in changed:
                    if phase[i][0]=='awake' and i not in dev_slab:      # 醒: 供给设备槽
                        if a.arm in ('RS','RSr'):
                            k,v=torch.empty(NL,NKV,L,HD,dtype=torch.bfloat16,device=dev),torch.empty(NL,NKV,L,HD,dtype=torch.bfloat16,device=dev)
                            k.copy_(host_slab[i][0],non_blocking=True); v.copy_(host_slab[i][1],non_blocking=True)
                            dev_slab[i]=(k,v)
                        elif a.arm=='RB':
                            dev_slab[i]=dev_pair(); rebuild_debt[0]+=REBUILD_S
                    elif phase[i][0]=='wait' and a.arm not in ('R1','RSr') and i in dev_slab:  # 睡: 撤离
                        if a.arm=='RS':
                            host_slab[i][0].copy_(dev_slab[i][0],non_blocking=True)
                            host_slab[i][1].copy_(dev_slab[i][1],non_blocking=True)
                        del dev_slab[i]
            sL.synchronize()
            assemble([i for i in awake if i in dev_slab] if a.arm!='R1' else awake)
        except Exception: traceback.print_exc()
        finally:
            pause.clear()
        trans_ms.append((time.perf_counter()-t0)*1000)
def th_llm():
    while not stop:
        if pause.is_set() or merged[0] is None or not members[0]:
            DBG['idle']+=1; idle.set(); time.sleep(0.002); continue
        idle.clear()
        DBG['t0']=time.perf_counter()
        c=merged[0]; B=len(members[0]); S=c.get_seq_length()
        if S>L+400:
            DBG['cap']+=1; idle.set(); time.sleep(0.001); continue
        d=torch.zeros(B,1,dtype=torch.long,device=dev)
        with torch.cuda.stream(sL), torch.inference_mode():
            for _ in range(4):
                pos=torch.full((B,1),S,dtype=torch.long,device=dev)
                model(input_ids=d,past_key_values=c,position_ids=pos,cache_position=pos[0]); S+=1
        sL.synchronize()
        DBG['blk']+=1; DBG['bt']+=time.perf_counter()-DBG['t0']
        if rebuild_debt[0]>0:
            t=min(rebuild_debt[0],0.3); rebuild_debt[0]-=t; time.sleep(t)
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
    ws_static=torch.empty(int(a.vision_gb*1e9/2),dtype=torch.bfloat16,device=dev) if a.arm in ('R1','RS') else None  # RS: 停放腾出的显存常驻持有工作区(CAP已扣除)
    while not stop:
        time.sleep(8.0)
        if stop: break
        t_arr=time.perf_counter()
        if a.arm in ('R1','RS'): ws=ws_static
        else:
            if a.arm=='RSr':
                need=int(a.vision_gb/SLAB)+2
                sleepers=[i for i in admitted if phase[i][0]=='wait' and i in dev_slab][:need]
                with torch.cuda.stream(sV):
                    for i in sleepers:
                        host_slab[i][0].copy_(dev_slab[i][0],non_blocking=True)
                        host_slab[i][1].copy_(dev_slab[i][1],non_blocking=True)
                sV.synchronize()
                for i in sleepers: del dev_slab[i]
                torch.cuda.empty_cache()
            try: ws=torch.empty(int(a.vision_gb*1e9/2),dtype=torch.bfloat16,device=dev)
            except torch.OutOfMemoryError: vlat.append(-1); continue
        with torch.cuda.stream(sV):
            for _ in range(max(1,int(300/(unit*4)))): torch.mm(vx,vy,out=vout)
        sV.synchronize()
        if a.arm not in ('R1','RS'): del ws; torch.cuda.empty_cache()
        vlat.append((time.perf_counter()-t_arr)*1000)
def wrap(f):
    def g():
        try: f()
        except Exception: traceback.print_exc()
    return g
ths=[threading.Thread(target=wrap(f)) for f in (th_sched,th_llm,th_render,th_vision)]
t0=time.perf_counter()
for t in ths: t.start()
time.sleep(a.dur); stop=True; pause.clear()
for t in ths: t.join(timeout=25)
dur=time.perf_counter()-t0
fr=np.array(frames[5:]); good=[v for v in vlat if v>0]
awake_now=len(members[0])
out=dict(arm=a.arm,admitted=len(admitted),
         p99=float(np.percentile(fr,99)),miss=float(100*np.mean(fr>FRAME*1000)),
         llm_tps=tok[0]/dur,B_last=awake_now,
         trans_ms=float(np.mean(trans_ms)) if trans_ms else 0,
         vision_ms=float(np.mean(good)) if good else -1,vision_fail=sum(1 for v in vlat if v<0))
out['dbg']=dict(DBG,t0=0)
print(json.dumps(out,indent=1))
if a.out: json.dump(out,open(a.out,'w'))

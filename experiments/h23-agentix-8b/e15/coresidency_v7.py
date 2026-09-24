"""E15 v7: 固定行槽持久合并批(无assemble/无pause)。
decode 常驻 [AW,NKV,L,HD] cache 连续运行; 醒=行级H2D换入, 睡=行级D2H停放(RS)/丢弃(RB)/滞留(RSr)。
吞吐计有效token = 占用行x4/块。R1: 席位+排队, 行槽=醒集。稳态窗口测量。"""
import argparse,threading,time,json,random,traceback
import torch,numpy as np
ap=argparse.ArgumentParser()
ap.add_argument('--arm',required=True,choices=['R1','RB','RS','RSr'])
ap.add_argument('--dur',type=float,default=120.0)
ap.add_argument('--warm',type=float,default=25.0)
ap.add_argument('--pool',type=int,default=64)
ap.add_argument('--vision-gb',type=float,default=6.0)
ap.add_argument('--period',type=float,default=8.0)
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
free0=torch.cuda.mem_get_info()[0]/1e9
BUDGET=free0-2.2
# 行槽数: 全臂同一AW(同配置); R1另有席位约束
AW=14
fixed = a.vision_gb + AW*SLAB   # 常驻ws(R1/RS) + 行槽
if a.arm=='R1':
    SEATS=int((BUDGET-fixed-3.0)/SLAB)    # 席位slabs(驻留语义, 留1.5GB concat/trim瞬态)
elif a.arm=='RSr':
    SEATS=None; LAZY_CAP=int((BUDGET-AW*SLAB-2.5)/SLAB)  # 惰性滞留上限(无常驻ws)
else: SEATS=None
print(f"arm={a.arm} 预算{BUDGET:.1f} AW={AW} SEATS={SEATS}",flush=True)
rng=random.Random(a.seed); N=a.pool
def dev_pair():
    return (torch.randn(NL,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,
            torch.randn(NL,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02)
host_slab={}; lazy_slab={}
if a.arm in ('RS','RSr'):
    for i in range(N):
        host_slab[i]=(torch.empty(NL,NKV,L,HD,dtype=torch.bfloat16,pin_memory=True),
                      torch.empty(NL,NKV,L,HD,dtype=torch.bfloat16,pin_memory=True))
resident=set(range(SEATS)) if a.arm=='R1' else None
adm_q=[i for i in range(N) if a.arm=='R1' and i>=(SEATS or 0)]
seat_slab={}
with torch.cuda.stream(sL):
    if a.arm=='R1':
        for i in resident: seat_slab[i]=dev_pair()
sL.synchronize()
# 固定行槽 cache
mc=DynamicCache()
with torch.cuda.stream(sL):
    for li in range(NL):
        mc.update(torch.zeros(AW,NKV,L,HD,dtype=torch.bfloat16,device=dev),
                  torch.zeros(AW,NKV,L,HD,dtype=torch.bfloat16,device=dev),li)
sL.synchronize()
BASE=[ (l.keys,l.values) for l in mc.layers ]   # 底座引用(decode append后会换新tensor, 须用行拷贝前L列)
row_of={}; free_rows=list(range(AW))
occ=[0]  # 占用行数
lock=threading.Lock()
def row_load(i,r):
    """把 agent i 的KV装入行r(前L列)。"""
    with torch.cuda.stream(sL), torch.inference_mode():
        for li,l in enumerate(mc.layers):
            if a.arm=='R1':
                l.keys[r,:,:L,:]=seat_slab[i][0][li]; l.values[r,:,:L,:]=seat_slab[i][1][li]
            elif a.arm in ('RS','RSr') and i in lazy_slab:
                l.keys[r,:,:L,:]=lazy_slab[i][0][li]; l.values[r,:,:L,:]=lazy_slab[i][1][li]
            elif a.arm in ('RS','RSr'):
                l.keys[r,:,:L,:].copy_(host_slab[i][0][li],non_blocking=True)
                l.values[r,:,:L,:].copy_(host_slab[i][1][li],non_blocking=True)
            else:
                l.keys[r,:,:L,:].normal_(0,0.02); l.values[r,:,:L,:].normal_(0,0.02)
        if a.arm=='RB':
            for _ in range(144): torch.mm(REB_X,REB_Y,out=REB_O)   # 真实重建GPU代价(~144ms@1.7B/3k)
    if a.arm in ('RS','RSr') and i in lazy_slab: del lazy_slab[i]
def row_save(i,r):
    with torch.cuda.stream(sL), torch.inference_mode():
        if a.arm=='RS':
            for li,l in enumerate(mc.layers):
                host_slab[i][0][li].copy_(l.keys[r,:,:L,:],non_blocking=True)
                host_slab[i][1][li].copy_(l.values[r,:,:L,:],non_blocking=True)
        elif a.arm=='RSr':
            while len(lazy_slab)>=max(1,LAZY_CAP-AW):   # 先逐出再分配
                j=next(iter(lazy_slab)); kj,vj=lazy_slab.pop(j)
                for li in range(NL):
                    host_slab[j][0][li].copy_(kj[li]); host_slab[j][1][li].copy_(vj[li])
                del kj,vj
            k=torch.empty(NL,NKV,L,HD,dtype=torch.bfloat16,device=dev); v=torch.empty_like(k)
            for li,l in enumerate(mc.layers):
                k[li]=l.keys[r,:,:L,:]; v[li]=l.values[r,:,:L,:]
            lazy_slab[i]=(k,v)
        # RB: 丢弃 = 不保存; R1: seat_slab 常驻已是真身, 无需保存(合成)
stop=False; frames=[]; tok_log=[]; vlat=[]; awake_log=[]; eps=[0]
rounds={i:0 for i in range(N)}; RND=5
phase={i:('wait',rng.uniform(0,10)) for i in range(N)}
def th_sched():
    t0=time.perf_counter()
    while not stop:
        time.sleep(0.5)
        now=time.perf_counter()-t0
        for i in range(N):
            if resident is not None and i not in resident: continue
            st_,te=phase[i]
            if now<te: continue
            if st_=='wait':
                with lock:
                    if free_rows:
                        r=free_rows.pop(); row_of[i]=r
                        row_load(i,r); occ[0]=AW-len(free_rows)
                        phase[i]=('awake',now+rng.uniform(2,3))
                    else:
                        phase[i]=('wait',now+0.3)   # 无空行, 稍后再醒
            else:
                with lock:
                    r=row_of.pop(i); row_save(i,r); free_rows.append(r)
                    occ[0]=AW-len(free_rows)
                phase[i]=('wait',now+rng.uniform(6,10)); rounds[i]+=1
                if rounds[i]>=RND:
                    rounds[i]=0; eps[0]+=1
                    if resident is not None:
                        resident.discard(i); adm_q.append(i)
                        del seat_slab[i]
                        nx=adm_q.pop(0); resident.add(nx)
                        with torch.cuda.stream(sL): seat_slab[nx]=dev_pair()
                        phase[nx]=('wait',now+rng.uniform(0,2))
        # RSr 惰性上限: 超限逐出最旧滞留者到host
        if a.arm=='RSr':
            while len(lazy_slab)> (LAZY_CAP-AW):
                i=next(iter(lazy_slab))
                k,v=lazy_slab.pop(i)
                for li in range(NL):
                    host_slab[i][0][li].copy_(k[li]); host_slab[i][1][li].copy_(v[li])
                del k,v
        sL.synchronize()
        awake_log.append((now,occ[0]))
def th_llm():
    t0=time.perf_counter(); S=[L]
    d=torch.zeros(AW,1,dtype=torch.long,device=dev)
    while not stop:
        if S[0]>L+400:
            with lock:
                with torch.cuda.stream(sL), torch.inference_mode():
                    for l in mc.layers:
                        l.keys=l.keys[:,:,:L,:].contiguous(); l.values=l.values[:,:,:L,:].contiguous()
                sL.synchronize(); S[0]=L
        try:
            with torch.cuda.stream(sL), torch.inference_mode():
                for _ in range(4):
                    pos=torch.full((AW,1),S[0],dtype=torch.long,device=dev)
                    model(input_ids=d,past_key_values=mc,position_ids=pos,cache_position=pos[0]); S[0]+=1
            sL.synchronize()
            tok_log.append((time.perf_counter()-t0, occ[0]*4))
        except torch.OutOfMemoryError:
            torch.cuda.empty_cache(); time.sleep(0.05)   # 有效token=占用行
REB_X=torch.randn(4096,4096,device=dev,dtype=torch.bfloat16)
REB_Y=torch.randn_like(REB_X); REB_O=torch.empty_like(REB_X)
UNIT_MS=0.17
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
        time.sleep(a.period)
        if stop: break
        t_arr=time.perf_counter()
        w=ws
        if w is None:
            for att in range(2):
                try:
                    w=torch.empty(int(a.vision_gb*1e9/2),dtype=torch.bfloat16,device=dev); break
                except torch.OutOfMemoryError:
                    if a.arm=='RSr':   # 压力让位: 清滞留
                        lazy_slab.clear(); torch.cuda.empty_cache()
                    else: torch.cuda.empty_cache()
            if w is None: vlat.append((time.perf_counter(),-1)); continue
        with torch.cuda.stream(sV):
            for _ in range(max(1,int(300/(UNIT_MS*4)))): torch.mm(vx,vy,out=vout)
        sV.synchronize()
        if ws is None: del w
        vlat.append((time.perf_counter(),(time.perf_counter()-t_arr)*1000))
def wrap(f):
    def g():
        try: f()
        except Exception: traceback.print_exc()
    return g
ths=[threading.Thread(target=wrap(f)) for f in (th_sched,th_llm,th_render,th_vision)]
T0=time.perf_counter()
for t in ths: t.start()
time.sleep(a.dur); stop=True
for t in ths: t.join(timeout=25)
WALL=time.perf_counter()-T0; CUT=a.warm
tok_ss=sum(n for t,n in tok_log if t>=CUT)
fr_ss=[m for t,m in frames if (t-T0)>=CUT]
vl_ss=[v for t,v in vlat if (t-T0)>=CUT and v>0]
aw_ss=[n for t,n in awake_log if t>=CUT]
out=dict(arm=a.arm,seed=a.seed,llm_tps=tok_ss/(WALL-CUT),
         p99=float(np.percentile(fr_ss,99)) if fr_ss else -1,
         miss=float(100*np.mean(np.array(fr_ss)>FRAME*1000)) if fr_ss else -1,
         vision_ms=float(np.mean(vl_ss)) if vl_ss else -1,
         vision_fail=sum(1 for _,v in vlat if v<0),
         awake_mean=float(np.mean(aw_ss)) if aw_ss else 0, eps=eps[0])
print(json.dumps(out,indent=1))
if a.out: json.dump(out,open(a.out,'w'))

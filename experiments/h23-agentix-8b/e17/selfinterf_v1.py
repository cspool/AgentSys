"""E17 v1: 自干扰闭环最小实验。
UI代理: 渲染线程60fps推进帧号(真实GPU渲染核, 高优先级流); 帧号=UI时钟。
agent: 捕获帧号(截图) -> 真实LLM decode K token(思考) -> 动作; 有效 iff 帧差<=τ。
失败重试(螺旋)。臂: A自由 / B静态限速(每agent动作间隔下限) / C截止期slot仲裁(串行观测-动作窗)。
指标: goodput(有效动作/min), 成功率, 重试放大系数, 帧miss, 陈旧度分布。"""
import argparse,threading,time,json,random
import torch,numpy as np
ap=argparse.ArgumentParser()
ap.add_argument('--arm',required=True,choices=['A','B','C'])
ap.add_argument('--agents',type=int,default=4)
ap.add_argument('--dur',type=float,default=90.0)
ap.add_argument('--warm',type=float,default=15.0)
ap.add_argument('--tau-ms',type=float,default=900.0)   # 陈旧窗: 独占推理(~650ms)可过, 争用则超
ap.add_argument('--think-tok',type=int,default=48)
ap.add_argument('--rate-b',type=float,default=2.2)     # B臂: 每agent动作最小间隔(s)
ap.add_argument('--seed',type=int,default=7)
ap.add_argument('--out',default='')
a=ap.parse_args()
dev='cuda'; FRAME=1/60.0
from transformers import AutoModelForCausalLM, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
NL,NKV,HD,L=28,8,128,1500
sR=torch.cuda.Stream(priority=-1); 
UNIT_MS=0.17
x=torch.randn(2048,2048,device=dev,dtype=torch.bfloat16); y=torch.randn_like(x); rout=torch.empty_like(x)
R_ITER=max(1,int(5.0/UNIT_MS))
frame_idx=[0]; stop=False; frames=[]
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
        frame_idx[0]+=1                      # UI时钟按实际完成的帧推进
        d=nxt-time.perf_counter()
        if d>0: time.sleep(d)
        else: nxt=time.perf_counter()
# agent 基建: 每agent一个1500-tok合成KV + 独立流
class Agent:
    def __init__(s_,i):
        s_.i=i; s_.stream=torch.cuda.Stream()
        s_.cache=DynamicCache()
        with torch.cuda.stream(s_.stream):
            for li in range(NL):
                s_.cache.update(torch.randn(1,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,
                                torch.randn(1,NKV,L,HD,dtype=torch.bfloat16,device=dev)*0.02,li)
        s_.stream.synchronize()
        s_.S=L; s_.ok=0; s_.fail=0; s_.retries=0; s_.acts=0; s_.stale=[]
    @torch.inference_mode()
    def think(s_):
        d=torch.zeros(1,1,dtype=torch.long,device=dev)
        with torch.cuda.stream(s_.stream):
            for _ in range(a.think_tok):
                pos=torch.full((1,1),s_.S,dtype=torch.long,device=dev)
                model(input_ids=d,past_key_values=s_.cache,position_ids=pos,cache_position=pos[0]); s_.S+=1
        s_.stream.synchronize()
        if s_.S>L+300:
            with torch.cuda.stream(s_.stream), torch.inference_mode():
                for l in s_.cache.layers:
                    l.keys=l.keys[:,:,:L,:].contiguous(); l.values=l.values[:,:,:L,:].contiguous()
            s_.stream.synchronize(); s_.S=L
slot_lock=threading.Lock()   # C臂: 观测-动作窗互斥slot
TAU_F=a.tau_ms/1000/FRAME
t_start=[0]
def th_agent(ag):
    rng=random.Random(a.seed*100+ag.i)
    while not stop:
        if a.arm=='C':
            with slot_lock:                    # 声明窗: 窗内独占agent算力
                if stop: return
                obs=frame_idx[0]; ag.think(); act=frame_idx[0]
        else:
            obs=frame_idx[0]; ag.think(); act=frame_idx[0]
        ag.acts+=1; stale=act-obs; ag.stale.append(stale)
        if stale<=TAU_F:
            ag.ok+=1
            time.sleep(rng.uniform(0.5,1.5))   # 成功后下一任务间歇
            if a.arm=='B': time.sleep(max(0,a.rate_b-1.0))
        else:
            ag.fail+=1; ag.retries+=1          # 失败立即重试(螺旋)
            if a.arm=='B': time.sleep(max(0,a.rate_b-0.0))
agents=[Agent(i) for i in range(a.agents)]
ths=[threading.Thread(target=th_render)]+[threading.Thread(target=th_agent,args=(g,)) for g in agents]
T0=time.perf_counter(); t_start[0]=T0
for t in ths: t.start()
time.sleep(a.dur); stop=True
for t in ths: t.join(timeout=20)
dur=time.perf_counter()-T0
fr=np.array(frames[int(a.warm/FRAME):])
ok=sum(g.ok for g in agents); fail=sum(g.fail for g in agents); acts=sum(g.acts for g in agents)
stale_all=[s for g in agents for s in g.stale]
out=dict(arm=a.arm,agents=a.agents,tau_ms=a.tau_ms,
         goodput_per_min=ok/(dur/60), succ=ok/max(acts,1),
         retry_amp=acts/max(ok,1),                     # 每有效动作平均尝试次数(螺旋放大系数)
         stale_p50_ms=float(np.percentile(stale_all,50))*FRAME*1000 if stale_all else -1,
         stale_p95_ms=float(np.percentile(stale_all,95))*FRAME*1000 if stale_all else -1,
         frame_p99=float(np.percentile(fr,99)), frame_miss=float(100*np.mean(fr>FRAME*1000)))
print(json.dumps(out,indent=1))
if a.out: json.dump(out,open(a.out,'w'))

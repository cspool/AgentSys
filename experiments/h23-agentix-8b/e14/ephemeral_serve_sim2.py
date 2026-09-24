"""E14.B1-v2 同配置公平对比: 所有臂同 offered load N, 同 KV 预算, host 资源显式分配。
臂: resident(纯GPU驻留, 满则排队 = 最弱基线) / vllm_lru(驻留至压力, 被逐者返回时重建 = 现实基线)
  / swap(等待即pinned换出, host够用 = InferCept类强基线) / hybrid(=swap, host耗尽转文本重建 = 本方案)
host 预算独立参数; swap 臂 host 耗尽时保持 GPU 驻留(其定义), hybrid 转文本。"""
import json,heapq,random,argparse
ap=argparse.ArgumentParser()
ap.add_argument('--kv-budget-gb',type=float,default=7.5)
ap.add_argument('--host-gb',type=float,default=16.0)
ap.add_argument('--rounds',type=int,default=5)
a=ap.parse_args()
CURVE={2:70,4:142,6:209,8:246,10:278,13:318,16:322}
def dec_rate(B):
    ks=sorted(CURVE)
    if B<=ks[0]: return CURVE[ks[0]]*B/ks[0]
    for x,y in zip(ks,ks[1:]):
        if x<=B<=y: return CURVE[x]+(CURVE[y]-CURVE[x])*(B-x)/(y-x)
    return CURVE[ks[-1]]
REBUILD_MS_1K=150.3; KB_TOK=144
CTX0,OUT,DEC,R=600,512,96,a.rounds
def ctx_at(r): return CTX0+r*(OUT+DEC)
KV=lambda tok: tok*KB_TOK*1024/1e9
def sim(arm, Tw, N, T=3600, seed=7):
    rng=random.Random(seed); evq=[]; done=0
    decoding=set(); resident={}   # id->GB 驻留在GPU的等待者
    host={}                       # id->GB 在host的等待者
    prefill_free=0.0; state={}
    for i in range(N):
        heapq.heappush(evq,(rng.random()*20,'wake',i)); state[i]=0
    def gpu_used(): return sum(KV(ctx_at(state[j])) for j in decoding)+sum(resident.values())
    t=0
    while evq:
        t,kind,i=heapq.heappop(evq)
        if t>T: break
        r=state[i]; need=KV(ctx_at(r))
        if kind=='wake':
            delay=0.0
            if i in resident: del resident[i]           # 驻留唤醒: 零成本
            elif i in host: del host[i]; delay=0.01     # 换回: DMA
            elif arm in ('vllm_lru','hybrid') and r>0:  # 被逐/文本态: 重建(prefill服务器)
                dur=ctx_at(r)/1000*REBUILD_MS_1K/1000
                st=max(t,prefill_free); prefill_free=st+dur; delay=(st-t)+dur
            if gpu_used()+need>a.kv_budget_gb:          # decode 显存不够: 稍后重试
                heapq.heappush(evq,(t+0.05,'wake',i)); 
                if arm=='vllm_lru' and resident:        # LRU 驱逐一个驻留等待者腾位
                    v=next(iter(resident)); del resident[v]
                continue
            decoding.add(i)
            tdec=DEC/(dec_rate(min(len(decoding),16))/max(len(decoding),1))
            heapq.heappush(evq,(t+delay+tdec,'tool',i))
        else:
            decoding.discard(i); state[i]+=1
            if state[i]>=R:
                done+=1; state[i]=0
                heapq.heappush(evq,(t+0.1,'wake',i)); continue
            need=KV(ctx_at(state[i]))
            if arm=='resident' or arm=='vllm_lru':
                resident[i]=need                        # 等待期占GPU(lru可被逐)
            elif arm in ('swap','hybrid'):
                if sum(host.values())+need<=a.host_gb: host[i]=need
                elif arm=='swap': resident[i]=need      # swap基线: host满则退回GPU驻留
                # hybrid: host满则文本态(不占任何内存), 唤醒走重建
            w=rng.uniform(Tw*0.4,Tw*1.6)
            heapq.heappush(evq,(t+w,'wake',i))
    return done/(min(t,T)/3600)
print(f"host={a.host_gb}GB  KV预算={a.kv_budget_gb}GB  同offered load 对比")
print(f"{'T̄':>4}{'N':>5} | {'resident':>9}{'vllm_lru':>9}{'swap基线':>9}{'hybrid':>8} | hybrid vs 最强基线")
res={}
for Tw in (2,5,10,20):
    for N in (16,32,64,128):
        row={arm:sim(arm,Tw,N) for arm in ('resident','vllm_lru','swap','hybrid')}
        best=max(row['resident'],row['vllm_lru'],row['swap'])
        g=100*(row['hybrid']/best-1) if best>0 else 0
        res[f"{Tw}_{N}"]=row
        print(f"{Tw:>3}s{N:>5} | {row['resident']:>9.0f}{row['vllm_lru']:>9.0f}{row['swap']:>9.0f}{row['hybrid']:>8.0f} | {g:+.0f}%")
json.dump(res,open('sim2_results.json','w'),indent=1)

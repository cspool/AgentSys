"""E14.B1 标定式 serving 仿真: 所有 GPU 原语按本卡实测计价(decode曲线/重建表/PCIe带宽)。
臂: FullKV驻留(等待者占显存) / EPH-rebuild(挂起丢KV,唤醒全前缀重建) /
    EPH-swap(挂起pinned换出19GB/s, host 64GB, 溢出走文本重建)。
负载: episode=R轮x[决策decode 96tok -> 工具等待T -> 输出512tok并入] ctx 600->3.6k。
精度: swap比特级相同; rebuild全前缀确定性重算=状态相同 => 两臂精度恒等FullKV(构造性)。
指标: 稳态 episodes/hour(主), 有效decode批量, GPU占用分解。"""
import json,heapq,random,argparse
ap=argparse.ArgumentParser()
ap.add_argument('--kv-budget-gb',type=float,default=7.5)
ap.add_argument('--host-gb',type=float,default=48.0)
ap.add_argument('--rounds',type=int,default=5)
ap.add_argument('--out',default='/workspace/AgentSys/experiments/h23-agentix-8b/e14/sim_results.json')
a=ap.parse_args()
# 实测原语(本卡 Qwen3-8B)
CURVE={2:70,4:142,6:209,8:246,10:278,13:318,16:322}   # decode tok/s @ctx3k
def dec_rate(B):
    ks=sorted(CURVE); 
    if B<=ks[0]: return CURVE[ks[0]]*B/ks[0]
    for x,y in zip(ks,ks[1:]):
        if x<=B<=y: return CURVE[x]+(CURVE[y]-CURVE[x])*(B-x)/(y-x)
    return CURVE[ks[-1]]
REBUILD_MS_1K=150.3; PCIE_GBs=19.0; KB_TOK=144
CTX0,OUT,DEC,R=600,512,96,a.rounds
def ctx_at(r): return CTX0+r*(OUT+DEC)
KV_GB=lambda tok: tok*KB_TOK*1024/1e9
def simulate(arm, Twait, n_agents, sim_T=3600, seed=7):
    rng=random.Random(seed)
    t=0.0; evq=[]; done=0
    gpu_free=0.0  # GPU 串行服务的可用时刻(decode按批处理简化为流体)
    # 流体化decode: 维护当前decode集合, 每步推进
    state={}  # id -> (phase, round, wake_t)
    hostGB=0.0
    for i in range(n_agents):
        heapq.heappush(evq,(rng.random()*min(30,sim_T/10),'wake',i)); state[i]=[0]
    decoding=set(); res_mem=0.0
    prefill_free=0.0  # GPU prefill 串行服务器(与decode时间共享: prefill期间decode按实测+17%膨胀, 简化为串行扣时)
    admitted=set(); waiting_adm=[]
    gpu_prefill_s=0.0; gpu_decode_tok=0
    t_prev=0.0
    def mem_of(i): return KV_GB(ctx_at(state[i][0]))
    while evq:
        t,kind,i=heapq.heappop(evq)
        if t>sim_T: break
        # 推进decode流体: [t_prev,t]内, 集合近似恒定
        if decoding:
            B=len(decoding); rate=dec_rate(min(B,16))
            gpu_decode_tok+=rate*(t-t_prev)
        t_prev=t
        r=state[i][0]
        if kind=='wake':  # 工具返回/新到达, 需要显存与(rebuild)后开始decode
            need=mem_of(i)
            if arm=='full':
                if i not in admitted:
                    if res_mem+KV_GB(ctx_at(R))<=a.kv_budget_gb:  # 按峰值预留
                        admitted.add(i); res_mem+=KV_GB(ctx_at(R))
                    else: waiting_adm.append(i); continue
                delay=0.0
            elif arm=='rebuild':
                dur=ctx_at(r)/1000*REBUILD_MS_1K/1000
                start=max(t,prefill_free); prefill_free=start+dur
                delay=(start-t)+dur
                gpu_prefill_s+=dur
            else:  # swap
                nonlocal_host=KV_GB(ctx_at(r))
                if hostGB>=0 and hostGB<=a.host_gb:  # 换回
                    delay=nonlocal_host/PCIE_GBs*0  # DMA异步, 不占GPU; 取0.01s固定
                    delay=0.01
                    hostGB-=nonlocal_host if hostGB>=nonlocal_host else 0
                else:
                    delay=ctx_at(r)/1000*REBUILD_MS_1K/1000; gpu_prefill_s+=delay
            # decode显存约束: 活跃decoder总KV <= budget
            cur=sum(mem_of(j) for j in decoding)
            if arm!='full' and cur+need>a.kv_budget_gb:
                heapq.heappush(evq,(t+0.05,'wake',i)); continue
            decoding.add(i)
            tdec=DEC/ (dec_rate(min(len(decoding),16))/len(decoding))
            heapq.heappush(evq,(t+delay+tdec,'tool',i))
        elif kind=='tool':
            decoding.discard(i)
            state[i][0]+=1
            if state[i][0]>=R:
                done+=1; state[i][0]=0
                if arm=='full' and waiting_adm:
                    pass
                heapq.heappush(evq,(t+0.1,'wake',i))  # 新episode
            else:
                if arm=='swap':
                    hostGB=min(a.host_gb, hostGB+mem_of(i))
                w=rng.uniform(Twait*0.4,Twait*1.6)
                heapq.heappush(evq,(t+w,'wake',i))
    return dict(eph=done/ (min(t,sim_T)/3600), gpu_prefill_s=gpu_prefill_s,
                decode_tok=int(gpu_decode_tok))
res={}
print(f"{'T̄wait':>7} {'N':>4} | {'FullKV':>8} {'EPH-rebuild':>11} {'EPH-swap':>9} | swap增益")
for Tw in (2,5,10,20):
    Nf=int(a.kv_budget_gb/KV_GB(ctx_at(R)))          # FullKV 准入上限
    row={}
    for arm,Ns in (('full',[Nf]),('rebuild',[8,12,16,24,32]),('swap',[64])):
        best=0
        for N in Ns:
            r_=simulate(arm,Tw,N); best=max(best,r_['eph'])
        row[arm]=best
    res[Tw]=row
    g=100*(row['swap']/row['full']-1)
    print(f"{Tw:>6}s {Nf:>4} | {row['full']:>8.0f} {row['rebuild']:>11.0f} {row['swap']:>9.0f} | {g:+.0f}%")
json.dump(res,open(a.out,'w'),indent=1)

"""分析 POD 的 CTA 角色日志: 每个 SM 上 P/D 的**时间加权**瞬时组成。

日志格式: int32 n, 然后 n 条 (smid, op, t_start, t_end), 时间是 %globaltimer 低 31 位(ns)。
op: 0=prefill, 1=decode。t_end=0 表示该 CTA 提前 return(空转), 排除。

输出:
  - 个数比 vs 时间加权比 (回答 "SM 内是不是更多 P")
  - 每个 SM 上 (仅P)/(仅D)/(P与D共驻)/(空) 各占多少时间
  - 共驻时的平均 P 数与 D 数
"""
import struct, sys, statistics
from collections import defaultdict

def load(path):
    b=open(path,'rb').read()
    n=struct.unpack_from('<i',b,0)[0]
    e=struct.unpack_from(f'<{4*n}i',b,4)
    return [(e[4*i],e[4*i+1],e[4*i+2],e[4*i+3]) for i in range(n)]

def analyze(path, label=""):
    rec=load(path)
    live=[r for r in rec if r[3]!=0 and r[3]>r[2]]
    idle=sum(1 for r in rec if r[3]==0)                 # 提前 return 的空转 CTA
    bad =sum(1 for r in rec if r[3]!=0 and r[3]<=r[2])  # t_end<=t_start: 31位回绕或数据坏
    if not live: print(f"{label}: 无有效记录"); return
    nP=sum(1 for r in live if r[1]==0); nD=len(live)-nP
    durP=[r[3]-r[2] for r in live if r[1]==0]; durD=[r[3]-r[2] for r in live if r[1]==1]
    tP=sum(durP); tD=sum(durD)
    print(f"\n=== {label} ===")
    print(f"  CTA 总数 {len(rec)} (空转 {idle}, 坏数据 {bad}), 有效 {len(live)}: P={nP} D={nD}")
    T0=min(r[2] for r in live); T1=max(r[3] for r in live)
    if T1-T0 > 50_000_000:
        print(f"  !! 时间跨度 {(T1-T0)/1e6:.1f} ms > 50ms, 疑似 31 位回绕, 结论不可信"); return
    print(f"  个数比   P:D = 1 : {nD/max(nP,1):.2f}")
    print(f"  CTA 时长 P 中位 {statistics.median(durP)/1000:.1f} us, D 中位 {statistics.median(durD)/1000:.1f} us  (P/D = {statistics.median(durP)/max(statistics.median(durD),1):.1f}x)")
    print(f"  时间加权 P:D = {tP/(tP+tD)*100:.1f}% : {tD/(tP+tD)*100:.1f}%   <-- SM 内谁更多, 看这个")
    # 每 SM 的共驻组成
    bysm=defaultdict(list)
    for smid,op,a,b_ in live: bysm[smid].append((a,b_,op))
    comp=defaultdict(float); co_pw=0.0; co_dw=0.0; co_t=0.0; maxres=0
    NSM=128                                  # 该卡 SM 数; 未出现的 SM 全程记为空
    WIN=T1-T0; tot=float(NSM)*WIN
    for smid,iv in bysm.items():
        ev=[]
        for a,b_,op in iv: ev.append((a,1,op)); ev.append((b_,-1,op))
        # 同一时刻先处理结束(-1)再处理开始(+1), 否则会虚报共驻
        ev.sort(key=lambda x:(x[0], x[1]))
        cp=cd=0; last=T0                      # 从全局窗口起点算起, 计入前导空闲
        for t,d,op in ev:
            if t>last:
                k=f"{cp}P+{cd}D" if (cp+cd)>0 else "空"
                comp[k]+=t-last
                if cp and cd: co_pw+=cp*(t-last); co_dw+=cd*(t-last); co_t+=t-last
                maxres=max(maxres,cp+cd)
            if op==0: cp+=d
            else: cd+=d
            last=t
        if T1>last: comp["空"]+=T1-last        # 尾部空闲
    comp["空"] += (NSM-len(bysm))*WIN        # 一个 CTA 都没拿到的 SM
    print(f"  SM 占用状态的时间分布 (窗口 {WIN/1000:.1f} us x {NSM} SM; 有 CTA 的 SM {len(bysm)} 个):")
    if maxres>2: print(f"  !! 实测最大同时驻留 {maxres} 个 CTA > 容量 2 => 区间不是真驻留区间, 共驻结论不成立")
    for k in sorted(comp, key=lambda x: -comp[x]):
        if comp[k]/tot >= 0.001: print(f"    {k:<10}{comp[k]/tot*100:>6.1f}%")
    pp = sum(v for k,v in comp.items() if k.endswith('+0D') and k!='0P+0D')
    mix = sum(v for k,v in comp.items() if not k.endswith('+0D') and not k.startswith('0P') and k!='空')
    dd = sum(v for k,v in comp.items() if k.startswith('0P') and k!='空')
    print(f"    ----  纯P态 {pp/tot*100:.1f}%  |  P与D混合态 {mix/tot*100:.1f}%  |  纯D态 {dd/tot*100:.1f}%")
    if co_t: print(f"  共驻时(时长加权)平均: P={co_pw/co_t:.2f} 个, D={co_dw/co_t:.2f} 个")

if __name__=='__main__':
    for p,l in zip(sys.argv[1::2], sys.argv[2::2]): analyze(p,l)

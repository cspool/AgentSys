import json,re,string,statistics as stt,sys
import sys
rs=json.load(open(sys.argv[1] if len(sys.argv)>1 else '/workspace/AgentSys/experiments/h23-agentix-8b/e13/ablation_results.json'))
def norm(x):
    x=x.lower().strip(); x=re.sub(r'\b(a|an|the)\b',' ',x)
    x=''.join(c for c in x if c not in string.punctuation); return ' '.join(x.split())
def ok(p,g): return norm(g) in norm(p)
RHOS=[0.1,0.25]
print(f"n={len(rs)}  上下文均值 {stt.mean(r['n_ctx'] for r in rs):.0f} tok (跨度占 {100*stt.mean(r['n_span']/r['n_ctx'] for r in rs):.0f}%)")
for st in ('early','mid','late','all'):
    sub=[r for r in rs if st=='all' or r['stratum']==st]
    qa=stt.mean(ok(r['ansA'],r['gold']) for r in sub)
    line=f"{st:<6} A:{100*qa:3.0f}%"
    for rho in RHOS:
        for arm in ['E','E2','H']:
            q=stt.mean(ok(r[f'ans_{arm}@{rho}'],r['gold']) for r in sub)
            line+=f"  {arm}@{rho}:{100*q:3.0f}%"
    print(line)
print("\n=== 全臂 (all) ===")
nctx=stt.mean(r['n_ctx'] for r in rs)
qa=stt.mean(ok(r['ansA'],r['gold']) for r in rs)
for rho in RHOS:
    print(f"-- ρ={rho} --")
    for arm in ['B','B2','C','D','E','E2','G','H','F']:
        q=stt.mean(ok(r[f'ans_{arm}@{rho}'],r['gold']) for r in rs)
        kv=stt.mean(r[f'kv_{arm}@{rho}'] for r in rs)
        print(f"  {arm}: 质量 {100*q:3.0f}% (Δ vs A {100*(q-qa):+3.0f}pp)  KV {100*kv/nctx:3.0f}%  显存降 {100*(1-kv/nctx):3.0f}%")

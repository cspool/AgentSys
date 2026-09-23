"""E13 终局汇总: 各任务族x各臂 质量/显存/吞吐(由H3曲线插值) 一张表。"""
import json,re,string,statistics as stt,os
def norm(x):
    x=x.lower().strip(); x=re.sub(r'\b(a|an|the)\b',' ',x)
    x=''.join(c for c in x if c not in string.punctuation); return ' '.join(x.split())
def ok(p,g): return norm(g) in norm(p)
def load(f):
    p=f'/workspace/AgentSys/experiments/h23-agentix-8b/e13/{f}'
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else None
# H3 实测: (ctx, tok/s) 定8GB预算
H3=[(238,5171),(465,3331),(770,2562),(1554,1095)]
def tput(ctx):
    for (x0,y0),(x1,y1) in zip(H3,H3[1:]):
        if x0<=ctx<=x1: return y0+(y1-y0)*(ctx-x0)/(x1-x0)
    return H3[0][1] if ctx<H3[0][0] else H3[-1][1]
def row(tag, rs, arm, rho=None):
    key=f'ans_{arm}@{rho}' if rho else f'ans_{arm}'
    kvk=f'kv_{arm}@{rho}' if rho else f'kv_{arm}_ans'
    sub=[r for r in rs if key in r and r[key]!='SKIP']
    if not sub: return
    qa=stt.mean(ok(r['ansA'],r['gold']) for r in sub)
    q=stt.mean(ok(r[key],r['gold']) for r in sub)
    kv=stt.mean(r.get(kvk,0) for r in sub); nc=stt.mean(r['n_ctx'] for r in sub)
    tp=tput(kv); tp0=tput(nc)
    print(f"{tag:<28} A={100*qa:3.0f}% 臂={100*q:3.0f}% (Δ{100*(q-qa):+4.0f}pp)  KV {100*kv/nc:3.0f}%  "
          f"显存降 {100*(1-kv/nc):3.0f}%  吞吐 {tp:5.0f} vs {tp0:4.0f} = {tp/tp0:.2f}x")
hp3=load('ablation_v3.jsonl') or load('ablation_v3')  # v3无jsonl(旧版), 退回json
if hp3 is None:
    import json as j; hp3=j.load(open('/workspace/AgentSys/experiments/h23-agentix-8b/e13/ablation_v3.json'))
hp4=load('ablation_v4.jsonl'); hp6=load('ablation_v6.jsonl'); loc=load('ablation_local.jsonl')
print("=== HotpotQA(多跳,难) ===")
row('H@0.1 v3(问句评分+护盾)', hp3, 'H', 0.1)
row('E@0.1 v3(全局消费分)', hp3, 'E', 0.1)
row('I v4(极化,宽判官)', hp4, 'I', 0.1)
if hp6: row('I v6(极化,严格判官)', hp6, 'I', 0.1)
if loc:
    print("=== 本地单跳(易) ===")
    for arm in ('E','H','I'): row(f'{arm}@0.1 local', loc, arm, 0.1)
    row('E@0.25 local', loc, 'E', 0.25)

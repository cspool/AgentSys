"""B3 verify快验证实测: draft(部分上下文下生成的答案token)在全量上下文下教师强制打分。
指标: 全接受率(逐token argmax全中=输出恒等常规decode), 前缀接受长度, verify边际耗时 vs decode耗时。"""
import json,time,torch,pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
tok=AutoTokenizer.from_pretrained(M)
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
NOTHINK="<think>\n\n</think>\n\n"
SYS="<|im_start|>system\nYou answer questions using the provided search results. Be concise.<|im_end|>\n"
ANS_SUF="\nGive the final short answer to the question now, nothing else.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK
def ids(s): return tok(s, return_tensors='pt', add_special_tokens=False).input_ids.to('cuda')
# 与 stream_ablation.build_samples 同逻辑重建样本(同序)
import random
df=pd.read_parquet('/data3/docker_model/AgentSys/_datasets/hotpot_dev_distractor.parquet')
data=[]
for _,row in df.iterrows():
    ctx=row['context']; sf=row['supporting_facts']
    data.append(dict(question=row['question'], answer=row['answer'],
        supporting_facts=[[t,i] for t,i in zip(sf['title'], sf['sent_id'])],
        context=[[t, list(sents)] for t,sents in zip(ctx['title'], ctx['sentences'])]))
random.Random(7).shuffle(data)
strata={'early':(0,),'mid':(4,),'late':(8,)}; NPS=20; out=[]
for ex in data:
    if ex['answer'].lower() in ('yes','no'): continue
    titles={t for t,_ in ex['supporting_facts']}
    paras=ex['context']; gold=[p for p in paras if p[0] in titles]; dis=[p for p in paras if p[0] not in titles]
    if len(gold)<2 or len(dis)<6: continue
    for st,(pos,) in strata.items():
        if sum(1 for s_ in out if s_['stratum']==st)>=NPS: continue
        d=dis[:]; order=(d[:pos]+gold+d[pos:])[:10]
        out.append(dict(q=ex['question'], ans=ex['answer'], stratum=st, paras=[(t,' '.join(s)) for t,s in order])); break
    if all(sum(1 for s_ in out if s_['stratum']==st)>=NPS for st in strata): break
res=json.load(open('/workspace/AgentSys/experiments/h23-agentix-8b/e11/out_hotpot_answer2.json'))
assert len(out)==len(res)
mis=sum(o['ans']!=r['gold'] for o,r in zip(out,res)); print('对齐错位:',mis); assert mis==0
stats={st:[] for st in ('early','mid','late')}
@torch.inference_mode()
def verify(sample, r):
    if r['stop_at'] is None or r['stop_at']>=r['n_paras']-1: return None
    draft=r['ansB2'].replace('<|im_end|>','').strip()
    dids=ids(draft)[0]
    if dids.numel()<1: return None
    c=DynamicCache()
    full=SYS+f"<|im_start|>user\nQuestion: {sample['q']}\nSearch results (arriving incrementally):\n"
    full+=''.join(f"[{k+1}] {t}: {x}\n" for k,(t,x) in enumerate(sample['paras']))
    o=model(input_ids=ids(full+ANS_SUF), past_key_values=c)
    torch.cuda.synchronize(); t0=time.perf_counter()
    o2=model(input_ids=dids.view(1,-1), past_key_values=c)
    torch.cuda.synchronize(); tv=time.perf_counter()-t0
    preds=torch.cat([o.logits[0,-1:].argmax(-1), o2.logits[0,:-1].argmax(-1)])
    match=(preds==dids)
    k=0
    for m in match.tolist():
        if m: k+=1
        else: break
    del c
    return dict(n=dids.numel(), acc_prefix=k, full=k==dids.numel(), t_verify=tv, t_dec=r['t_ansA'])
for s,r in zip(out,res):
    v=verify(s,r)
    if v: stats[r['stratum']].append(v)
print(f"{'层':<6}{'n':>3}{'全接受':>7}{'前缀接受均值':>10}{'verify均值':>10}{'decode均值':>10}{'加速比':>7}")
allv=[]
for st in ('early','mid','late'):
    v=stats[st]; allv+=v
    if not v: continue
    fa=sum(x['full'] for x in v)/len(v); pf=sum(x['acc_prefix']/x['n'] for x in v)/len(v)
    tv=sum(x['t_verify'] for x in v)/len(v); td=sum(x['t_dec'] for x in v)/len(v)
    print(f"{st:<6}{len(v):>3}{100*fa:>6.0f}%{100*pf:>9.0f}%{tv*1000:>8.1f}ms{td*1000:>8.0f}ms{td/tv:>6.1f}x")
fa=sum(x['full'] for x in allv)/len(allv); pf=sum(x['acc_prefix']/x['n'] for x in allv)/len(allv)
tv=sum(x['t_verify'] for x in allv)/len(allv); td=sum(x['t_dec'] for x in allv)/len(allv)
print(f"{'all':<6}{len(allv):>3}{100*fa:>6.0f}%{100*pf:>9.0f}%{tv*1000:>8.1f}ms{td*1000:>8.0f}ms{td/tv:>6.1f}x")

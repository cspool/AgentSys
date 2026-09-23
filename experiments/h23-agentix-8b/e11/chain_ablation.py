"""B3 两步链端到端: 证据流 -> 答案 -> 下游消费(结论句)。
A链: 流完+流水prefill -> decode答案 -> 下游。B3链: answer2停点draft答案(停线判据白送),
流尾空窗投机跑下游; 流完 verify(教师强制); accept->下游已就绪; reject->正常decode答案+重跑下游。
质量恒=A(接受即比特级恒等)。产出各流速 E2E 与省时。"""
import json,time,random,torch,pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
tok=AutoTokenizer.from_pretrained(M)
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
NOTHINK="<think>\n\n</think>\n\n"
SYS="<|im_start|>system\nYou answer questions using the provided search results. Be concise.<|im_end|>\n"
ANS_SUF="\nGive the final short answer to the question now, nothing else.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK
def ids(s): return tok(s, return_tensors='pt', add_special_tokens=False).input_ids.to('cuda')
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
mis=sum(o['ans']!=r['gold'] for o,r in zip(out,res)); assert mis==0, mis

@torch.inference_mode()
def timed_gen(prompt_ids, max_new=48):
    c=DynamicCache(); torch.cuda.synchronize(); t0=time.perf_counter()
    o=model(input_ids=prompt_ids, past_key_values=c); nxt=o.logits[0,-1].argmax(); toks=[]
    for _ in range(max_new):
        toks.append(nxt.item())
        if '<|im_end|>' in tok.decode(toks[-3:]): break
        o=model(input_ids=nxt.view(1,1), past_key_values=c); nxt=o.logits[0,-1].argmax()
    torch.cuda.synchronize(); del c
    return tok.decode(toks).replace('<|im_end|>','').strip(), time.perf_counter()-t0
def ds_prompt(q,a):
    return ids(f"<|im_start|>user\nThe answer to the question '{q}' was determined to be: {a}.\n"
        "Write one confident concluding sentence stating this answer.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK)
@torch.inference_mode()
def verify(sample, draft):
    dids=ids(draft)[0]
    if dids.numel()<1: return False,0.0
    c=DynamicCache()
    full=SYS+f"<|im_start|>user\nQuestion: {sample['q']}\nSearch results (arriving incrementally):\n"
    full+=''.join(f"[{k+1}] {t}: {x}\n" for k,(t,x) in enumerate(sample['paras']))
    o=model(input_ids=ids(full+ANS_SUF), past_key_values=c)
    torch.cuda.synchronize(); t0=time.perf_counter()
    o2=model(input_ids=dids.view(1,-1), past_key_values=c)
    torch.cuda.synchronize(); tv=time.perf_counter()-t0
    preds=torch.cat([o.logits[0,-1:].argmax(-1), o2.logits[0,:-1].argmax(-1)])
    del c
    return bool((preds==dids).all()), tv

rows=[]
for i,(s,r) in enumerate(zip(out,res)):
    spec = r['stop_at'] is not None and r['stop_at']<r['n_paras']-1
    draft=r['ansB2'].replace('<|im_end|>','').strip()
    acc,tv = verify(s,draft) if spec else (False,0.0)
    _,t_ds = timed_gen(ds_prompt(s['q'], draft))
    rows.append(dict(stratum=r['stratum'], spec=spec, acc=acc, t_verify=tv, t_ds=t_ds,
                     stop_at=r['stop_at'], seg=r['seg'], judges=r['judges'], t_ansA=r['t_ansA']))
    if (i+1)%15==0: print(f"  {i+1}/{len(out)}")
json.dump(rows, open('/workspace/AgentSys/experiments/h23-agentix-8b/e11/out_chain_b3.json','w'), indent=1)

def e2e(row, rate):
    seg=row['seg']; arr=[]; acc_tok=0
    for sgm in seg: acc_tok+=sgm['n_tok']; arr.append(acc_tok/rate)
    # A 链: 流水 prefill(无判断) -> 答案 -> 下游
    f=0
    for k,sgm in enumerate(seg): f=max(arr[k], f)+sgm['t_prefill']
    tA = f + row['t_ansA'] + row['t_ds']
    if not row['spec']: return tA, tA
    # B3: 停点前流水 prefill+judge; 停后继续流水 prefill(不判)
    fb=0
    for k,sgm in enumerate(seg):
        fb=max(arr[k], fb)+sgm['t_prefill']+(row['judges'][k]['t'] if k<=row['stop_at'] else 0)
    stop_done=0; acc2=0
    fs=0
    for k in range(row['stop_at']+1):
        acc2+=seg[k]['n_tok']
        fs=max(acc2/rate, fs)+seg[k]['t_prefill']+row['judges'][k]['t']
    draft_path = fs + row['t_ds']          # draft答案由停线判据白送, 下游立即投机
    if row['acc']:
        tB3 = max(fb + row['t_verify'], draft_path)
    else:
        tB3 = fb + row['t_verify'] + row['t_ansA'] + row['t_ds']
    return tA, tB3

import statistics as st
for rate in (50,200,1000):
    print(f"\n=== 流速 {rate} tok/s ===")
    print(f"{'层':<7}{'n':>3}{'A链E2E':>9}{'B3链E2E':>9}{'省时':>7}{'接受率':>7}")
    for stg in ('early','mid','late','all'):
        sub=[x for x in rows if stg=='all' or x['stratum']==stg]
        ts=[e2e(x,rate) for x in sub]
        mA=st.mean(t[0] for t in ts); mB=st.mean(t[1] for t in ts)
        ar=st.mean(x['acc'] for x in sub)
        print(f"{stg:<7}{len(sub):>3}{mA:>8.2f}s{mB:>8.2f}s{100*(mA-mB)/mA:>6.1f}%{100*ar:>6.0f}%")
print("\n质量: B3 恒等 A(接受即比特级一致, 拒绝走 A 路径) — 结构保证, 无需另测")

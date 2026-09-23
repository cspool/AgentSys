"""E13-H1: 工具跨度是否"消费即冷却", 消费轮注意力能否预测答案轮需求。
每轮=工具段prefill+消费短注(生成后crop); 终局答案轮。eager attention 抓注意力。
产出: 冷却倍数(新鲜跨度 vs 已消费跨度的 per-token 注意力), 答案轮质量热区,
mass-capture@rho(按消费分留 top-rho 能捕获答案轮多少注意力质量) vs 随机/位置基线。"""
import json,random,time,torch,pandas as pd,numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
tok=AutoTokenizer.from_pretrained(M)
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda',
                                           attn_implementation='eager'); model.eval()
NOTHINK="<think>\n\n</think>\n\n"
SYS="<|im_start|>system\nYou answer questions using the provided search results. Be concise.<|im_end|>\n"
ANS_SUF="\nGive the final short answer to the question now, nothing else.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK
NOTE_SUF="\nState the key fact from the latest result in one short sentence.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK
def ids(s): return tok(s, return_tensors='pt', add_special_tokens=False).input_ids.to('cuda')
# 样本(同 e11 逻辑)
df=pd.read_parquet('/data3/docker_model/AgentSys/_datasets/hotpot_dev_distractor.parquet')
data=[]
for _,row in df.iterrows():
    ctx=row['context']; sf=row['supporting_facts']
    data.append(dict(question=row['question'], answer=row['answer'],
        supporting_facts=[[t,i] for t,i in zip(sf['title'], sf['sent_id'])],
        context=[[t, list(sents)] for t,sents in zip(ctx['title'], ctx['sentences'])]))
random.Random(7).shuffle(data)
strata={'early':(0,),'mid':(4,),'late':(8,)}; NPS=4; samples=[]
for ex in data:
    if ex['answer'].lower() in ('yes','no'): continue
    titles={t for t,_ in ex['supporting_facts']}
    paras=ex['context']; gold=[p for p in paras if p[0] in titles]; dis=[p for p in paras if p[0] not in titles]
    if len(gold)<2 or len(dis)<6: continue
    for st,(pos,) in strata.items():
        if sum(1 for s_ in samples if s_['stratum']==st)>=NPS: continue
        d=dis[:]; order=(d[:pos]+gold+d[pos:])[:10]
        samples.append(dict(q=ex['question'], ans=ex['answer'], stratum=st,
            paras=[(t,' '.join(s),(t in titles)) for t,s in order])); break
    if all(sum(1 for s_ in samples if s_['stratum']==st)>=NPS for st in strata): break
print(f"episodes: {len(samples)}")

@torch.inference_mode()
def gen_with_attn(cache, suffix, max_new, K_ctx):
    """生成并累计 对前K_ctx个key 的注意力(mean over layers/heads/steps)。返回文本与得分向量。"""
    acc=torch.zeros(K_ctx, device='cuda'); steps=0
    o=model(input_ids=ids(suffix), past_key_values=cache, output_attentions=True)
    for a in o.attentions:  # [1,H,q,K]
        acc+=a[0,:,:,:K_ctx].mean(dim=(0,1)).sum(dim=0)*0+a[0,:,:,:K_ctx].mean(dim=0).mean(dim=0); steps+=1
    nxt=o.logits[0,-1].argmax(); toks=[]
    for _ in range(max_new):
        toks.append(nxt.item())
        if '<|im_end|>' in tok.decode(toks[-3:]): break
        o=model(input_ids=nxt.view(1,1), past_key_values=cache, output_attentions=True)
        for a in o.attentions:
            acc+=a[0,:,0,:K_ctx].mean(dim=0); steps+=1
        nxt=o.logits[0,-1].argmax()
    return tok.decode(toks).replace('<|im_end|>','').strip(), (acc/max(steps,1)).float().cpu().numpy()

res=[]
t0=time.time()
for ep,s in enumerate(samples):
    cache=DynamicCache()
    head=SYS+f"<|im_start|>user\nQuestion: {s['q']}\nSearch results (arriving incrementally):\n"
    model(input_ids=ids(head), past_key_values=cache)
    spans=[]  # (start,end,is_gold)
    cons_scores={}  # k -> 消费轮对整个上下文的得分向量
    for k,(t,x,g) in enumerate(s['paras']):
        st_=cache.get_seq_length()
        model(input_ids=ids(f"[{k+1}] {t}: {x}\n"), past_key_values=cache)
        en=cache.get_seq_length(); spans.append((st_,en,g))
        L=cache.get_seq_length()
        _,sc=gen_with_attn(cache, NOTE_SUF, 16, L)
        cache.crop(L); cons_scores[k]=sc
    L=cache.get_seq_length()
    ans,ans_sc=gen_with_attn(cache, ANS_SUF, 24, L)
    # 统计
    rec=dict(stratum=s['stratum'], gold=s['ans'], ans=ans)
    fresh=[]; old=[]
    for k,(st_,en,g) in enumerate(spans):
        fresh.append(cons_scores[k][st_:en].mean())
        for j in range(k+1,len(spans)):
            old.append(cons_scores[j][st_:en].mean())
    rec['fresh_att']=float(np.mean(fresh)); rec['old_att']=float(np.mean(old))
    gm=[ans_sc[st_:en].sum() for st_,en,g in spans if g]; dm=[ans_sc[st_:en].sum() for st_,en,g in spans if not g]
    gpt=[ans_sc[st_:en].mean() for st_,en,g in spans if g]; dpt=[ans_sc[st_:en].mean() for st_,en,g in spans if not g]
    rec['gold_mass']=float(np.sum(gm)); rec['dis_mass']=float(np.sum(dm))
    rec['gold_pertok']=float(np.mean(gpt)); rec['dis_pertok']=float(np.mean(dpt))
    # mass-capture@rho: 每跨度按消费分留 top-rho, 捕获答案轮该跨度注意力质量的比例
    for rho in (0.1,0.25):
        cap_c=[]; cap_r=[]; cap_p=[]
        rng=np.random.RandomState(0)
        for k,(st_,en,g) in enumerate(spans):
            n=en-st_; keep=max(1,int(n*rho))
            a_ans=ans_sc[st_:en]; tot=a_ans.sum()+1e-9
            idx_c=np.argsort(cons_scores[k][st_:en])[-keep:]
            idx_r=rng.choice(n,keep,replace=False)
            half=keep//2; idx_p=np.r_[np.arange(min(half,n)), np.arange(max(0,n-(keep-half)),n)]
            cap_c.append(a_ans[idx_c].sum()/tot); cap_r.append(a_ans[idx_r].sum()/tot); cap_p.append(a_ans[np.unique(idx_p)].sum()/tot)
        rec[f'cap_cons@{rho}']=float(np.mean(cap_c)); rec[f'cap_rand@{rho}']=float(np.mean(cap_r)); rec[f'cap_pos@{rho}']=float(np.mean(cap_p))
    res.append(rec)
    print(f"  ep{ep} {s['stratum']:<6} 冷却比 {rec['fresh_att']/max(rec['old_att'],1e-9):5.1f}x  "
          f"cap@0.1 消费{rec['cap_cons@0.1']:.2f}/随机{rec['cap_rand@0.1']:.2f}/位置{rec['cap_pos@0.1']:.2f}")
    del cache; torch.cuda.empty_cache()
json.dump(res, open('/workspace/AgentSys/experiments/h23-agentix-8b/e13/h1_results.json','w'), indent=1)
import statistics as stt
print(f"\n=== H1 汇总 (n={len(res)}, {time.time()-t0:.0f}s) ===")
print(f"冷却倍数(新鲜/已消费 per-token 注意力): {stt.mean(r['fresh_att'] for r in res)/stt.mean(r['old_att'] for r in res):.1f}x")
print(f"答案轮 gold/干扰 per-token 注意力比: {stt.mean(r['gold_pertok'] for r in res)/stt.mean(r['dis_pertok'] for r in res):.1f}x")
for rho in (0.1,0.25):
    print(f"mass-capture@{rho}: 消费分 {stt.mean(r[f'cap_cons@{rho}'] for r in res):.2f}  "
          f"随机 {stt.mean(r[f'cap_rand@{rho}'] for r in res):.2f}  位置 {stt.mean(r[f'cap_pos@{rho}'] for r in res):.2f}")

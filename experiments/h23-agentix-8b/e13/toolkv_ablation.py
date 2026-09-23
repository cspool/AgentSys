"""E13 主消融: 工具语义KV压缩。
遍1(eager): 全KV episode, 抓每跨度消费轮注意力分+全局累计分, 得A臂答案。
遍2(重放): B 消费分留top-ρ / C 位置(首尾) / D 随机 / E 全局H2O(同总预算) / F 全丢+答案时语义换入top2跨度。
notes 全程 crop(消费事件只用于评分)。显式 position 续推(evict后 cache短于真实位置)。"""
import argparse,json,random,time,copy
import torch,numpy as np,pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
ap=argparse.ArgumentParser()
ap.add_argument('--n-per-stratum',type=int,default=20)
ap.add_argument('--rhos',default='0.1,0.25')
ap.add_argument('--smoke',type=int,default=0)
ap.add_argument('--out',default='/workspace/AgentSys/experiments/h23-agentix-8b/e13/ablation_results.json')
a=ap.parse_args()
RHOS=[float(x) for x in a.rhos.split(',')]
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
tok=AutoTokenizer.from_pretrained(M)
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda',
                                           attn_implementation='eager'); model.eval()
NOTHINK="<think>\n\n</think>\n\n"
SYS="<|im_start|>system\nYou answer questions using the provided search results. Be concise.<|im_end|>\n"
ANS_SUF="\nGive the final short answer to the question now, nothing else.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK
NOTE_SUF="\nState the key fact from the latest result in one short sentence.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK
def ids(s): return tok(s, return_tensors='pt', add_special_tokens=False).input_ids.to('cuda')
df=pd.read_parquet('/data3/docker_model/AgentSys/_datasets/hotpot_dev_distractor.parquet')
data=[]
for _,row in df.iterrows():
    ctx=row['context']; sf=row['supporting_facts']
    data.append(dict(question=row['question'], answer=row['answer'],
        supporting_facts=[[t,i] for t,i in zip(sf['title'], sf['sent_id'])],
        context=[[t, list(sents)] for t,sents in zip(ctx['title'], ctx['sentences'])]))
random.Random(7).shuffle(data)
strata={'early':(0,),'mid':(4,),'late':(8,)}; samples=[]
for ex in data:
    if ex['answer'].lower() in ('yes','no'): continue
    titles={t for t,_ in ex['supporting_facts']}
    paras=ex['context']; gold=[p for p in paras if p[0] in titles]; dis=[p for p in paras if p[0] not in titles]
    if len(gold)<2 or len(dis)<6: continue
    for st,(pos,) in strata.items():
        if sum(1 for s_ in samples if s_['stratum']==st)>=a.n_per_stratum: continue
        d=dis[:]; order=(d[:pos]+gold+d[pos:])[:10]
        samples.append(dict(q=ex['question'], ans=ex['answer'], stratum=st,
            paras=[(t,' '.join(s),(t in titles)) for t,s in order])); break
    if all(sum(1 for s_ in samples if s_['stratum']==st)>=a.n_per_stratum for st in strata): break
if a.smoke: samples=samples[:a.smoke]
print(f"episodes: {len(samples)}", flush=True)

@torch.inference_mode()
def fwd(cache, tid, pos_start, attn=False):
    n=tid.shape[1]
    pos=torch.arange(pos_start,pos_start+n,device='cuda').unsqueeze(0)
    return model(input_ids=tid, past_key_values=cache, position_ids=pos,
                 cache_position=pos[0], output_attentions=attn)
@torch.inference_mode()
def gen(cache, suffix, pos_start, max_new=24, attn=False, K_ctx=0):
    acc=torch.zeros(K_ctx,device='cuda') if attn else None; steps=0
    o=fwd(cache, ids(suffix), pos_start, attn); p=pos_start+ids(suffix).shape[1]
    if attn:
        for at in o.attentions: acc+=at[0,:,:,:K_ctx].mean(dim=0).mean(dim=0); steps+=1
    nxt=o.logits[0,-1].argmax(); toks=[]
    for _ in range(max_new):
        toks.append(nxt.item())
        if '<|im_end|>' in tok.decode(toks[-3:]): break
        o=fwd(cache, nxt.view(1,1), p, attn); p+=1
        if attn:
            for at in o.attentions: acc+=at[0,:,0,:K_ctx].mean(dim=0); steps+=1
        nxt=o.logits[0,-1].argmax()
    txt=tok.decode(toks).replace('<|im_end|>','').strip()
    return (txt,(acc/max(steps,1)).float().cpu().numpy()) if attn else (txt,None)

def keep_sets(spans, cons, glob, rho, rng):
    """返回各臂的 keep 索引(全局坐标, 含头部全部)。spans=[(st,en,g)]"""
    out={}
    n_head=spans[0][0]
    head=np.arange(n_head)
    tot_span=sum(en-st for st,en,_ in spans)
    def per_span(pick):
        ks=[head]
        for k,(st,en,g) in enumerate(spans):
            n=en-st; keep=max(1,int(round(n*rho)))
            ks.append(st+pick(k,n,keep))
        return np.sort(np.concatenate(ks))
    out['B']=per_span(lambda k,n,keep: np.sort(np.argsort(cons[k])[-keep:]))
    def posp(k,n,keep):
        h=keep//2; return np.unique(np.r_[np.arange(min(h,n)), np.arange(max(0,n-(keep-h)),n)])
    out['C']=per_span(posp)
    out['D']=per_span(lambda k,n,keep: np.sort(rng.choice(n,keep,replace=False)))
    budget=max(1,int(round(tot_span*rho)))
    allidx=np.concatenate([np.arange(st,en) for st,en,_ in spans])
    sc=np.concatenate([glob[st:en] for st,en,_ in spans])
    out['E']=np.sort(np.concatenate([head, allidx[np.argsort(sc)[-budget:]]]))
    return out

results=[]; t0=time.time()
for ep,s in enumerate(samples):
    # ---- 遍1: 全KV + 评分 ----
    cache=DynamicCache()
    head=SYS+f"<|im_start|>user\nQuestion: {s['q']}\nSearch results (arriving incrementally):\n"
    hid=ids(head); fwd(cache,hid,0); pos=hid.shape[1]
    spans=[]; cons={}; span_ids=[]
    globacc=None; pfacc=None
    for k,(t,x,g) in enumerate(s['paras']):
        tid=ids(f"[{k+1}] {t}: {x}\n"); span_ids.append(tid)
        st_=pos; o=fwd(cache,tid,pos,attn=True); pos+=tid.shape[1]; spans.append((st_,pos,g))
        L0=cache.get_seq_length()
        psc=np.zeros(L0)
        for at in o.attentions: psc[:L0]+=at[0,:,:,:L0].mean(dim=0).mean(dim=0).float().cpu().numpy()
        if pfacc is None: pfacc=np.zeros(0)
        pfacc=np.pad(pfacc,(0,L0-pfacc.shape[0])); pfacc+=psc
        L=cache.get_seq_length()
        _,sc=gen(cache, NOTE_SUF, pos, 16, attn=True, K_ctx=L)
        cache.crop(L); cons[k]=sc[st_:pos]
        if globacc is None: globacc=np.zeros(0)
        globacc=np.pad(globacc,(0,L-globacc.shape[0])); globacc[:L]+=sc
    L=cache.get_seq_length()
    ansA,_=gen(cache, ANS_SUF, pos, 24)
    del cache; torch.cuda.empty_cache()
    rec=dict(stratum=s['stratum'], gold=s['ans'], ansA=ansA, n_ctx=int(pos),
             n_span=sum(en-st for st,en,_ in spans))
    # ---- 遍2: 各臂重放 ----
    rng=np.random.RandomState(ep)
    for rho in RHOS:
        ks=keep_sets(spans, cons, globacc, rho, rng)
        ks['G']=np.sort(np.concatenate([np.arange(spans[0][0]), np.concatenate([np.arange(st,en) for st,en,_ in spans])[np.argsort(np.concatenate([pfacc[st:en] for st,en,_ in spans]))[-max(1,int(round(sum(en-st for st,en,_ in spans)*rho))):]]]))
        for arm,keep in ks.items():
            c=DynamicCache(); fwd(c,hid,0); p=hid.shape[1]
            for k,tid in enumerate(span_ids):
                fwd(c,tid,p); p+=tid.shape[1]
                st_,en,_=spans[k]
                gk=np.concatenate([keep[keep<st_], keep[(keep>=st_)&(keep<en)]])
                cur=np.arange(c.get_seq_length())
                prev_keep=keep[keep<st_]
                local=np.concatenate([np.arange(prev_keep.shape[0]), 
                      prev_keep.shape[0]+ (keep[(keep>=st_)&(keep<en)]-st_) ]) if False else None
                # 简化: 每跨度后从头算当前cache里的保留映射
                # cache 当前内容 = head + 各已处理跨度的保留 + 本跨度全量
                # 本跨度保留局部索引:
                kk=keep[(keep>=st_)&(keep<en)]-st_
                base=c.get_seq_length()-tid.shape[1]
                keep_local=np.concatenate([np.arange(base), base+kk])
                ki=torch.as_tensor(keep_local,device='cuda',dtype=torch.long)
                for lyr in c.layers:
                    lyr.keys=lyr.keys[:,:,ki,:].contiguous(); lyr.values=lyr.values[:,:,ki,:].contiguous()
            ansX,_=gen(c, ANS_SUF, p, 24)
            rec[f'ans_{arm}@{rho}']=ansX; rec[f'kv_{arm}@{rho}']=int(c.get_seq_length())
            del c
        # F: 全丢+答案时语义换入 top2 跨度(按消费分跨度均值)
        rank=np.argsort([cons[k].mean() for k in range(len(spans))])[::-1][:2]
        c=DynamicCache(); fwd(c,hid,0); p=hid.shape[1]
        kv_between=hid.shape[1]  # 轮间仅头部
        for k in sorted(rank):
            tid=span_ids[k]; st_,en,_=spans[k]
            n=tid.shape[1]
            posr=torch.arange(st_,en,device='cuda').unsqueeze(0)
            model(input_ids=tid, past_key_values=c, position_ids=posr, cache_position=posr[0])
        ansF,_=gen(c, ANS_SUF, p, 24)
        rec[f'ans_F@{rho}']=ansF; rec[f'kv_F@{rho}']=kv_between
        del c; torch.cuda.empty_cache()
    results.append(rec)
    if (ep+1)%5==0: print(f"  {ep+1}/{len(samples)} ({time.time()-t0:.0f}s)", flush=True)
json.dump(results, open(a.out,'w'), indent=1)
# 汇总
import re,string,statistics as stt
def norm(x):
    x=x.lower().strip(); x=re.sub(r'\b(a|an|the)\b',' ',x)
    x=''.join(ch for ch in x if ch not in string.punctuation); return ' '.join(x.split())
def ok(p,g): return norm(g) in norm(p)
print(f"\n=== E13 消融汇总 (n={len(results)}) ===")
qA=stt.mean(ok(r['ansA'],r['gold']) for r in results)
nctx=stt.mean(r['n_ctx'] for r in results)
print(f"A 全KV: 质量 {100*qA:.0f}%  上下文均值 {nctx:.0f} tok")
for rho in RHOS:
    print(f"-- ρ={rho} --")
    for arm in 'BCDEFG':
        q=stt.mean(ok(r[f'ans_{arm}@{rho}'],r['gold']) for r in results)
        kv=stt.mean(r[f'kv_{arm}@{rho}'] for r in results)
        print(f"  {arm}: 质量 {100*q:3.0f}%  保留KV {kv:5.0f} tok ({100*kv/nctx:.0f}%)  显存降 {100*(1-kv/nctx):.0f}%")

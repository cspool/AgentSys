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
ap.add_argument('--data',default='hotpot',choices=['hotpot','local'])
ap.add_argument('--arms',default='')
ap.add_argument('--cache',default='/workspace/AgentSys/experiments/h23-agentix-8b/e13/pass1_cache')
ap.add_argument('--no-cache',action='store_true')
ap.add_argument('--judge',default='note',choices=['note','strict'])
ap.add_argument('--model',default='/data3/docker_model/AgentSys/Qwen3-1.7B')
ap.add_argument('--device-map',default='cuda')
a=ap.parse_args()
RHOS=[float(x) for x in a.rhos.split(',')]
M=a.model
tok=AutoTokenizer.from_pretrained(M)
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map=a.device_map,
                                           attn_implementation='eager'); model.eval()
NOTHINK="<think>\n\n</think>\n\n"
SYS="<|im_start|>system\nYou answer questions using the provided search results. Be concise.<|im_end|>\n"
ANS_SUF="\nGive the final short answer to the question now, nothing else.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK
LIST_SUF="\nBased on the numbered results, which ones do you need to re-read in full to answer the question? Reply with at most 3 numbers, comma-separated, nothing else.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK
NOTE_SUF="\nState what the latest result contributes to answering the question, in one short sentence; if nothing, say irrelevant.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK
if a.judge=='strict':
    NOTE_SUF="\nDoes the latest result contain information required to answer the question? Reply exactly YES or NO.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK
def ids(s): return tok(s, return_tensors='pt', add_special_tokens=False).input_ids.to('cuda')
def build_local(nps):
    import json as _j
    pool=[]
    for conv in _j.load(open('/data3/docker_model/AgentSys/_datasets/ShareGPT_V3_unfiltered_cleaned_split.json')):
        for m in conv.get('conversations',[]):
            t=m.get('value','').strip().replace('\n',' ')
            if 220<len(t)<400: pool.append(t)
        if len(pool)>2000: break
    rng=random.Random(7); rng.shuffle(pool)
    CITIES=['Zurich','Osaka','Porto','Tallinn','Cusco','Windhoek','Tromso','Davao','Leipzig','Ottawa',
            'Bergen','Quito','Sapporo','Ghent','Tucson','Cork','Malmo','Split','Nagoya','Basel']
    NAMES=['Ilse Brandt','Tomas Vela','Aiko Mori','Ruth Okafor','Pavel Novak','Greta Lindh','Omar Sayed']
    strata={'early':1,'mid':5,'late':9}; out=[]; pi=0
    for i in range(nps*3):
        st=list(strata)[i%3]; pos=strata[st]
        code=f"AX-{rng.randint(100,999)}"; city=rng.choice(CITIES); name=rng.choice(NAMES)
        yr=rng.randint(1988,2024); bud=rng.randint(12,940)
        gold=(f"Internal briefing: the project codenamed {code} was directed by {name} and launched in "
              f"{yr}. Its operations were headquartered in {city}, with an initial budget of {bud} million dollars.")
        q=f"In which city was the project codenamed {code} headquartered?"
        paras=[('Note', pool[pi+k], False) for k in range(9)]; pi+=9
        paras.insert(pos, ('Briefing', gold, True))
        out.append(dict(q=q, ans=city, stratum=st, paras=paras[:10]))
    return out

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
if a.data=='local': samples=build_local(a.n_per_stratum)
if a.smoke: samples=samples[:a.smoke]
import os,hashlib
os.makedirs(a.cache,exist_ok=True)
def ckey(ep): return os.path.join(a.cache, f"{a.data}_{ep}_{hashlib.md5((M+NOTE_SUF).encode()).hexdigest()[:8]}.npz")
# 增量输出: 已有结果跳过
done={}
if os.path.exists(a.out+'.jsonl'):
    for ln in open(a.out+'.jsonl'):
        try: r=json.loads(ln); done[r['_ep']]=r
        except Exception: pass
print(f"resume: {len(done)} episodes already done", flush=True)
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

def smooth(x,k=7):
    if x.shape[0]<=1: return x
    pad=k//2; xp=np.pad(x,(pad,pad),mode='edge')
    from numpy.lib.stride_tricks import sliding_window_view
    return sliding_window_view(xp,k).max(axis=1)

def keep_sets(spans, cons, glob, rho, rng, notes=None):
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
    # v2: 平滑分(实体完整性)
    out['B2']=per_span(lambda k,n,keep: np.sort(np.argsort(smooth(cons[k]))[-keep:]))
    sc2=np.concatenate([smooth(glob[st:en]) for st,en,_ in spans])
    out['E2']=np.sort(np.concatenate([head, allidx[np.argsort(sc2)[-budget:]]]))
    # H: E2 + 近期护盾(最后2跨度全保, 预算只作用于其余跨度)
    ns=len(spans); shield={ns-1,ns-2}
    rest=[(st,en) for k,(st,en,_) in enumerate(spans) if k not in shield]
    sh=[np.arange(st,en) for k,(st,en,_) in enumerate(spans) if k in shield]
    if rest:
        ridx=np.concatenate([np.arange(st,en) for st,en in rest])
        rsc=np.concatenate([smooth(glob[st:en]) for st,en in rest])
        bud=max(1,int(round(sum(en-st for st,en in rest)*rho)))
        kept=ridx[np.argsort(rsc)[-bud:]]
    else: kept=np.zeros(0,dtype=int)
    out['H']=np.sort(np.concatenate([head]+sh+[kept]))
    if notes is not None:
        ki=[head]
        for k,(st,en,_) in enumerate(spans):
            rel=('NO' not in notes[k].upper()) if a.judge=='strict' else ('irrelevant' not in notes[k].lower())
            ki.append(np.arange(st,en) if rel else np.arange(st,min(st+4,en)))
        out['I']=np.sort(np.concatenate(ki))
    return out

results=[]; t0=time.time()
outf=open(a.out+'.jsonl','a')
for ep,s in enumerate(samples):
    if ep in done:
        results.append(done[ep]); continue
    # ---- 遍1: 全KV + 评分(可缓存) ----
    ck=ckey(ep)
    cached=None
    if (not a.no_cache) and os.path.exists(ck):
        z=np.load(ck, allow_pickle=True)
        cached=dict(z); 
    cache=DynamicCache()
    head=SYS+f"<|im_start|>user\nQuestion: {s['q']}\nSearch results (arriving incrementally):\n"
    hid=ids(head)
    spans=[]; cons={}; span_ids=[]; notes=[]
    globacc=None; pfacc=None
    if cached is not None:
        meta=json.loads(str(cached['meta']))
        spans=[tuple(x) for x in meta['spans']]; notes=meta['notes']; ansA=meta['ansA']; pos=meta['pos']
        cons={k:cached[f'cons{k}'] for k in range(len(spans))}
        globacc=cached['glob']; pfacc=cached['pf']
        span_ids=[ids(f"[{k+1}] {t}: {x}\n") for k,(t,x,g) in enumerate(s['paras'])]
        del cache
    else:
        fwd(cache,hid,0); pos=hid.shape[1]
    need_pf = (not a.arms) or ('G' in a.arms.split(','))
    if cached is None:
        for k,(t,x,g) in enumerate(s['paras']):
            tid=ids(f"[{k+1}] {t}: {x}\n"); span_ids.append(tid)
            st_=pos; o=fwd(cache,tid,pos,attn=need_pf); pos+=tid.shape[1]; spans.append((st_,pos,g))
            L0=cache.get_seq_length()
            if need_pf:
                psc=np.zeros(L0)
                for at in o.attentions: psc[:L0]+=at[0,:,:,:L0].mean(dim=0).mean(dim=0).float().cpu().numpy()
                if pfacc is None: pfacc=np.zeros(0)
                pfacc=np.pad(pfacc,(0,L0-pfacc.shape[0])); pfacc+=psc
            del o
            L=cache.get_seq_length()
            ntxt,sc=gen(cache, NOTE_SUF, pos, 16, attn=True, K_ctx=L)
            cache.crop(L); cons[k]=sc[st_:pos]; notes.append(ntxt)
            if globacc is None: globacc=np.zeros(0)
            globacc=np.pad(globacc,(0,L-globacc.shape[0])); globacc[:L]+=sc
        L=cache.get_seq_length()
        ansA,_=gen(cache, ANS_SUF, pos, 24)
        del cache; torch.cuda.empty_cache()
        if not a.no_cache:
            np.savez(ck, glob=globacc, pf=pfacc if pfacc is not None else np.zeros(1),
                     meta=json.dumps(dict(spans=[list(x) for x in spans], notes=notes, ansA=ansA, pos=int(pos))),
                     **{f'cons{k}':v for k,v in cons.items()})
    rec=dict(stratum=s['stratum'], gold=s['ans'], ansA=ansA, n_ctx=int(pos), notes=notes,
             gold_spans=[k for k,(_,_,g) in enumerate(spans) if g],
             n_span=sum(en-st for st,en,_ in spans))
    # ---- 遍2: 各臂重放 ----
    rng=np.random.RandomState(ep)
    for rho in RHOS:
        ks=keep_sets(spans, cons, globacc, rho, rng, notes)
        if ((not a.arms) or 'G' in a.arms.split(',')) and pfacc is not None: ks['G']=np.sort(np.concatenate([np.arange(spans[0][0]), np.concatenate([np.arange(st,en) for st,en,_ in spans])[np.argsort(np.concatenate([pfacc[st:en] for st,en,_ in spans]))[-max(1,int(round(sum(en-st for st,en,_ in spans)*rho))):]]]))
        for arm,keep in ks.items():
            if a.arms and arm not in a.arms.split(','): continue
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
                ki=torch.as_tensor(keep_local,dtype=torch.long)
                for lyr in c.layers:
                    kd=ki.to(lyr.keys.device)
                    lyr.keys=lyr.keys[:,:,kd,:].contiguous(); lyr.values=lyr.values[:,:,kd,:].contiguous()
            ansX,_=gen(c, ANS_SUF, p, 24)
            rec[f'ans_{arm}@{rho}']=ansX; rec[f'kv_{arm}@{rho}']=int(c.get_seq_length())
            del c
        if a.arms and 'F' not in a.arms.split(','):
            results_skipF=True
        # F: 全丢+答案时语义换入 top2 跨度(按消费分跨度均值)
        # J: 语义按需换页(与rho无关, 只算一次): 轮间全存根(每跨度前8tok), 答案时模型点名换入
        if rho==RHOS[0] and ((not a.arms) or 'J' in a.arms.split(',')):
            import re as _re
            c=DynamicCache(); fwd(c,hid,0); p=hid.shape[1]
            for k,tid in enumerate(span_ids):
                fwd(c,tid,p); p+=tid.shape[1]
                st_,en,_=spans[k]
                stub=min(8,tid.shape[1])
                base=c.get_seq_length()-tid.shape[1]
                ki=torch.as_tensor(np.r_[np.arange(base), base+np.arange(stub)],dtype=torch.long)
                for lyr in c.layers:
                    kd=ki.to(lyr.keys.device)
                    lyr.keys=lyr.keys[:,:,kd,:].contiguous(); lyr.values=lyr.values[:,:,kd,:].contiguous()
            kv_between=int(c.get_seq_length())
            Lst=c.get_seq_length()
            req_txt,_=gen(c, LIST_SUF, p, 12)
            c.crop(Lst)
            req=[int(x)-1 for x in _re.findall(r'\d+', req_txt)][:3]
            req=[k for k in req if 0<=k<len(spans)]
            for k in sorted(set(req)):
                st_,en,_=spans[k]
                posr=torch.arange(st_,en,device='cuda').unsqueeze(0)
                model(input_ids=span_ids[k], past_key_values=c, position_ids=posr, cache_position=posr[0])
            ansJ,_=gen(c, ANS_SUF, p, 24)
            rec['ans_J']=ansJ; rec['kv_J_between']=kv_between; rec['kv_J_ans']=int(c.get_seq_length())
            rec['req_J']=req
            del c; torch.cuda.empty_cache()
        if a.arms and 'F' not in a.arms.split(','):
            rec[f'ans_F@{rho}']='SKIP'; rec[f'kv_F@{rho}']=0; continue
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
    rec['_ep']=ep
    results.append(rec)
    outf.write(json.dumps(rec)+'\n'); outf.flush()
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
    for arm in ['B','B2','C','D','E','E2','G','H','I','F']:
        try: q=stt.mean(ok(r[f'ans_{arm}@{rho}'],r['gold']) for r in results if r[f'ans_{arm}@{rho}']!='SKIP')
        except Exception: continue
        kv=stt.mean(r[f'kv_{arm}@{rho}'] for r in results)
        print(f"  {arm}: 质量 {100*q:3.0f}%  保留KV {kv:5.0f} tok ({100*kv/nctx:.0f}%)  显存降 {100*(1-kv/nctx):.0f}%")

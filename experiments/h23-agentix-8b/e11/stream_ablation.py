"""E11 消融: 流式增量消费 vs 阻塞全量消费 —— 更短时间完成相同/近似质量的任务?

场景: 下游 agent 读上游(agent/工具)流式输出回答问题。HotpotQA distractor: 10 段落
(2 金段+8 干扰) = 天然的"搜索结果列表"; 金段位置分层(早/中/晚)检验早停的质量风险。

三臂(消融拆分两个机制):
  A  阻塞全量: 等全部到达 -> 全量 prefill -> 答
  B1 仅重叠  : 段落边到边 prefill(Stream2LLM 类策略), 不早停
  B2 重叠+早停: 每段 prefill 后跑廉价 YES/NO 判断, 够则截断上游流

计时: GPU 段(prefill/judge/answer)实测; 到达时刻 A_k = 累计token/流速 解析;
任务墙钟 = 离散事件流水核算 => 一次 GPU 跑, 任意流速复算。
"""
import argparse, json, random, re, string, time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache

ap = argparse.ArgumentParser()
ap.add_argument('--model', default='/data3/docker_model/AgentSys/Qwen3-1.7B')
ap.add_argument('--data', default='/data3/docker_model/AgentSys/_datasets/hotpot_dev_distractor_v1.json')
ap.add_argument('--n-per-stratum', type=int, default=20)
ap.add_argument('--seed', type=int, default=7)
ap.add_argument('--out', required=True)
ap.add_argument('--smoke', type=int, default=0)
ap.add_argument('--stop-rule', default='first', choices=['first','consec2','answer2'],
    help='early-stop 判据: first=首个YES即停(朴素); consec2=连续两段YES才停; answer2=暂定答案自一致(连续两段答案相同且非UNKNOWN才停)')
a = ap.parse_args()

tok = AutoTokenizer.from_pretrained(a.model)
model = AutoModelForCausalLM.from_pretrained(a.model, dtype=torch.bfloat16, device_map='cuda')
model.eval()
DEV='cuda'
NOTHINK = "<think>\n\n</think>\n\n"

def ids(s): return tok(s, return_tensors='pt', add_special_tokens=False).input_ids.to(DEV)

@torch.inference_mode()
def prefill(cache, s):
    t0=time.perf_counter()
    i=ids(s)
    model(input_ids=i, past_key_values=cache)
    torch.cuda.synchronize()
    return time.perf_counter()-t0, i.shape[1]

@torch.inference_mode()
def gen(cache, prompt_s, max_new, stop_strs):
    """在 cache 上追加 prompt 并贪心生成; 返回 (text, secs, n_prompt, n_gen). 调用者负责 crop。"""
    t0=time.perf_counter()
    i=ids(prompt_s)
    out=model(input_ids=i, past_key_values=cache)
    npr=i.shape[1]; toks=[]
    nxt=out.logits[0,-1].argmax()
    for _ in range(max_new):
        toks.append(nxt.item())
        txt=tok.decode(toks)
        if any(ss in txt for ss in stop_strs): break
        out=model(input_ids=nxt.view(1,1), past_key_values=cache)
        nxt=out.logits[0,-1].argmax()
    torch.cuda.synchronize()
    return tok.decode(toks), time.perf_counter()-t0, npr, len(toks)

def norm(s):
    s=s.lower().strip()
    return ''.join(c for c in s if c not in string.punctuation).strip()

def load_data():
    if a.data.endswith('.parquet'):
        import pandas as pd
        df=pd.read_parquet(a.data); data=[]
        for _,row in df.iterrows():
            ctx=row['context']; sf=row['supporting_facts']
            data.append(dict(question=row['question'], answer=row['answer'],
                supporting_facts=[[t,i] for t,i in zip(sf['title'], sf['sent_id'])],
                context=[[t, list(sents)] for t,sents in zip(ctx['title'], ctx['sentences'])]))
        return data
    return json.load(open(a.data))

CITIES=['Zurich','Osaka','Porto','Tallinn','Cusco','Windhoek','Tromso','Davao','Leipzig','Ottawa',
        'Bergen','Quito','Sapporo','Ghent','Tucson','Cork','Malmo','Split','Nagoya','Basel']
NAMES=['Ilse Brandt','Tomas Vela','Aiko Mori','Ruth Okafor','Pavel Novak','Greta Lindh','Omar Sayed',
       'Nina Costa','Jonas Meyer','Lea Fontaine','Marta Vidal','Kenji Sato','Ana Petrov','Lars Holm',
       'Dana Weiss','Igor Bela','Mia Larsen','Sam Ortiz','Eva Novo','Timo Aalto']
def build_local_samples():
    """本地 NIAH-检索式任务: 金事实段 + ShareGPT 真实段落做干扰。答案精确可验, 金段位置可控。
    (HotpotQA 因网络不可达暂替; 单金段单跳为简化, 已注记)"""
    import json as _j, random
    rng=random.Random(a.seed)
    sg=_j.load(open('/data3/docker_model/AgentSys/_datasets/ShareGPT_V3_unfiltered_cleaned_split.json'))
    pool=[]
    for conv in sg:
        for m in conv.get('conversations',[]):
            t=m.get('value','')
            if 300<len(t)<700 and '```' not in t and 'http' not in t:
                pool.append(' '.join(t.split()))
        if len(pool)>4000: break
    rng.shuffle(pool)
    strata={'early':1,'mid':5,'late':9}
    out=[]; pi=0
    for i in range(a.n_per_stratum*3):
        st=list(strata)[i%3]; pos=strata[st]
        code=f"AX-{rng.randint(100,999)}"; city=rng.choice(CITIES); name=rng.choice(NAMES)
        yr=rng.randint(1988,2024); bud=rng.randint(12,940)
        gold=(f"Internal briefing: the project codenamed {code} was directed by {name} and launched in "
              f"{yr}. Its operations were headquartered in {city}, with an initial budget of {bud} million dollars.")
        q=f"In which city was the project codenamed {code} headquartered?"
        paras=[('Note', pool[pi+k]) for k in range(9)]; pi+=9
        paras.insert(pos, ('Briefing', gold))
        out.append(dict(q=q, ans=city, stratum=st, paras=paras[:10]))
    return out

def build_samples():
    if a.data=='local': return build_local_samples()
    data=load_data()
    random.Random(a.seed).shuffle(data)
    strata={'early':(0,), 'mid':(4,), 'late':(8,)}
    out=[]
    for ex in data:
        if ex['answer'].lower() in ('yes','no'): continue
        titles={t for t,_ in ex['supporting_facts']}
        paras=ex['context']
        gold=[p for p in paras if p[0] in titles]; dis=[p for p in paras if p[0] not in titles]
        if len(gold)<2 or len(dis)<6: continue
        for st,(pos,) in strata.items():
            cnt=sum(1 for s_ in out if s_['stratum']==st)
            if cnt>=a.n_per_stratum: continue
            d=dis[:]; order=d[:pos]+gold+d[pos:]
            order=order[:10]
            out.append(dict(q=ex['question'], ans=ex['answer'], stratum=st,
                            paras=[(t, ' '.join(sents)) for t,sents in order]))
            break
        if all(sum(1 for s_ in out if s_['stratum']==st)>=a.n_per_stratum for st in strata): break
    return out

SYS="<|im_start|>system\nYou answer questions using the provided search results. Be concise.<|im_end|>\n"
def user_head(q): return f"<|im_start|>user\nQuestion: {q}\nSearch results (arriving incrementally):\n"
ANS_SUF="\nGive the final short answer to the question now, nothing else.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK
TENT_SUF="\nBased only on the results so far, give your best short answer to the question. If the results so far do not contain the answer, reply exactly UNKNOWN. Answer only, nothing else.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK
JDG_SUF="\nJudging only from the results so far: can the question already be answered with confidence? Reply exactly YES or NO.<|im_end|>\n<|im_start|>assistant\n"+NOTHINK

@torch.inference_mode()
def run_sample(s):
    """一次 GPU 遍历同时产出三臂所需的全部实测段与决策。"""
    r=dict(stratum=s['stratum'], gold=s['ans'], n_paras=len(s['paras']))
    cache=DynamicCache()
    t_head,n_head=prefill(cache, SYS+user_head(s['q']))
    seg=[]; judges=[]; stop_at=None; L=cache.get_seq_length()
    for k,(title,text) in enumerate(s['paras']):
        ptxt=f"[{k+1}] {title}: {text}\n"
        tp,np_=prefill(cache, ptxt)
        seg.append(dict(k=k, n_tok=np_, t_prefill=tp))
        Lk=cache.get_seq_length()
        if a.stop_rule=='answer2':
            jtxt,tj,njp,njg=gen(cache, TENT_SUF, 16, ['<|im_end|>','\n'])
            cache.crop(Lk)
            tent=jtxt.strip(); unk=(not tent) or 'UNKNOWN' in tent.upper()
            judges.append(dict(k=k, t=tj, n=njp+njg, yes=not unk, tent=tent))
            if stop_at is None and not unk and k>0:
                prev=judges[-2].get('tent','')
                if prev and 'UNKNOWN' not in prev.upper() and norm(tent)==norm(prev): stop_at=k
        else:
            jtxt,tj,njp,njg=gen(cache, JDG_SUF, 4, ['YES','NO'])
            cache.crop(Lk)
            yes='YES' in jtxt.upper()
            judges.append(dict(k=k, t=tj, n=njp+njg, yes=yes))
            if stop_at is None:
                if a.stop_rule=='first' and yes: stop_at=k
                elif a.stop_rule=='consec2' and yes and k>0 and judges[-2]['yes']: stop_at=k
    # 全量答案(A 与 B1 共用: 同一 KV 内容)
    ansA,tA,nAp,nAg=gen(cache, ANS_SUF, 32, ['<|im_end|>','\n'])
    r.update(t_head=t_head,n_head=n_head,seg=seg,judges=judges,stop_at=stop_at,
             ansA=ansA.strip(), t_ansA=tA, n_ansA=nAp+nAg)
    # B2 的答案: 只含前 stop_at+1 段的 KV -> 重建
    if stop_at is not None and stop_at < len(s['paras'])-1:
        c2=DynamicCache(); prefill(c2, SYS+user_head(s['q']))
        for k in range(stop_at+1):
            t,tt=s['paras'][k]; prefill(c2, f"[{k+1}] {t}: {tt}\n")
        ansB,tB,_,_=gen(c2, ANS_SUF, 32, ['<|im_end|>','\n'])
        r.update(ansB2=ansB.strip(), t_ansB2=tB)
        del c2
    else:
        r.update(ansB2=r['ansA'], t_ansB2=tA)
    del cache; torch.cuda.empty_cache()
    return r

def account(r, rate):
    """离散事件核算三臂墙钟(秒)。流从 t=0 开始; head 的 prefill 在流前完成(不计)。"""
    seg=r['seg']; n=len(seg)
    arr=[]; acc=0
    for sgm in seg: acc+=sgm['n_tok']; arr.append(acc/rate)
    # A: 全部到齐后串行 prefill 全文 + 答
    tA = arr[-1] + sum(s_['t_prefill'] for s_ in seg) + r['t_ansA']
    # B1: 流水线 prefill(无判断)
    f=0
    for k,sgm in enumerate(seg): f=max(arr[k], f)+sgm['t_prefill']
    tB1 = f + r['t_ansA']
    # B2: 流水线 prefill+judge, 在 stop_at 截断
    stop = r['stop_at'] if r['stop_at'] is not None else n-1
    f=0
    for k in range(stop+1):
        f=max(arr[k], f)+seg[k]['t_prefill']+r['judges'][k]['t']
    tB2 = f + r['t_ansB2']
    return tA, tB1, tB2

samples=build_samples()
if a.smoke: samples=samples[:a.smoke]
print(f"样本 {len(samples)} (分层 early/mid/late)")
res=[]
for i,s in enumerate(samples):
    r=run_sample(s); res.append(r)
    if (i+1)%10==0: print(f"  {i+1}/{len(samples)}")
json.dump(res, open(a.out,'w'), ensure_ascii=False, indent=1)

# 汇总
def ok(pred,gold): return norm(gold) in norm(pred)
for rate in (50, 200, 1000):
    print(f"\n=== 上游流速 {rate} tok/s ===")
    print(f"{'层':<7}{'n':>3}{'A时间':>8}{'B1时间':>8}{'B2时间':>8}{'B2省时':>8}{'A质量':>7}{'B2质量':>7}{'早停段':>7}")
    import statistics as st
    for stg in ('early','mid','late','all'):
        sub=[r for r in res if stg=='all' or r['stratum']==stg]
        if not sub: continue
        ts=[account(r,rate) for r in sub]
        mA=st.mean(t[0] for t in ts); mB1=st.mean(t[1] for t in ts); mB2=st.mean(t[2] for t in ts)
        qA=st.mean(ok(r['ansA'],r['gold']) for r in sub); qB=st.mean(ok(r['ansB2'],r['gold']) for r in sub)
        sp=st.mean((r['stop_at'] if r['stop_at'] is not None else r['n_paras'])+1 for r in sub)
        print(f"{stg:<7}{len(sub):>3}{mA:>8.2f}{mB1:>8.2f}{mB2:>8.2f}{100*(mA-mB2)/mA:>7.1f}%{100*qA:>6.0f}%{100*qB:>6.0f}%{sp:>7.1f}")

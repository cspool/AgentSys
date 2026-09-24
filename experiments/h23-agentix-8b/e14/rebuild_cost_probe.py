"""E14.A 工具KV重建成本量化(时间 x 保真度)。
变量: 跨度长度 / 上下文位置(前缀长度) / 批量重建数k / 前缀完整度(全量 vs 存根态)。
对照: 全量重prefill, host KV回传(PCIe), 工具等待窗。
保真度: 在压缩前缀上重建的KV vs 原始全前缀KV 的余弦相似 + 下游答案一致性。
"""
import argparse,time,json,random
import torch,numpy as np,pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
ap=argparse.ArgumentParser()
ap.add_argument('--model',default='/data3/docker_model/AgentSys/Qwen3-8B')
ap.add_argument('--device-map',default='cuda')
ap.add_argument('--out',default='/workspace/AgentSys/experiments/h23-agentix-8b/e14/rebuild_cost.json')
a=ap.parse_args()
tok=AutoTokenizer.from_pretrained(a.model)
model=AutoModelForCausalLM.from_pretrained(a.model, dtype=torch.bfloat16, device_map=a.device_map); model.eval()
cfg=model.config
NL=cfg.num_hidden_layers; NKV=cfg.num_key_value_heads
HD=getattr(cfg,'head_dim',cfg.hidden_size//cfg.num_attention_heads)
BPT=NL*2*NKV*HD*2
print(f"模型 {a.model.split('/')[-1]}: {NL}层 kv{NKV} hd{HD} -> {BPT/1024:.0f} KB/token", flush=True)
def ids(s): return tok(s,return_tensors='pt',add_special_tokens=False).input_ids.to('cuda')
@torch.inference_mode()
def fwd(c,t,p0):
    n=t.shape[1]; pos=torch.arange(p0,p0+n,device='cuda').unsqueeze(0)
    return model(input_ids=t,past_key_values=c,position_ids=pos,cache_position=pos[0])
def newcache(): return DynamicCache()

# 真实工具输出语料(HotpotQA 段落)
df=pd.read_parquet('/data3/docker_model/AgentSys/_datasets/hotpot_dev_distractor.parquet')
paras=[]
for _,r in df.head(300).iterrows():
    for t_,sents in zip(r['context']['title'], r['context']['sentences']):
        paras.append(f"[{t_}] "+' '.join(sents))
    if len(paras)>400: break
rng=random.Random(7); rng.shuffle(paras)
def make_span(target_len):
    s=''; 
    while ids(s).shape[1]<target_len and paras:
        s+=paras[rng.randrange(len(paras))]+"\n"
    t=ids(s)[:,:target_len]
    return t
res={'model':a.model,'bytes_per_token':BPT,'runs':[]}

@torch.inference_mode()
def timeit(fn,warm=1,rep=3):
    for _ in range(warm): fn()
    torch.cuda.synchronize(); t0=time.perf_counter()
    for _ in range(rep): fn()
    torch.cuda.synchronize(); return (time.perf_counter()-t0)/rep

print("\n=== A1 重建时间 vs 跨度长度 x 前缀长度 ===", flush=True)
print(f"{'跨度':>6}{'前缀':>7}{'重建ms':>9}{'ms/1k':>8}", flush=True)
for prefix_len in (512, 2048, 8192):
    pref=make_span(prefix_len)
    for span_len in (128, 256, 512, 1024):
        sp=make_span(span_len)
        def run():
            c=newcache(); fwd(c,pref,0); fwd(c,sp,prefix_len); del c
        t_both=timeit(run)
        def run0():
            c=newcache(); fwd(c,pref,0); del c
        t_pref=timeit(run0)
        t=max(t_both-t_pref,1e-6)
        res['runs'].append(dict(kind='rebuild',prefix=prefix_len,span=span_len,ms=t*1000))
        print(f"{span_len:>6}{prefix_len:>7}{t*1000:>9.1f}{t*1000/span_len*1000:>8.1f}", flush=True)

print("\n=== A2 批量重建(k个512跨度一次性) ===", flush=True)
pref=make_span(2048)
for k in (1,2,4,8):
    sp=make_span(512*k)
    def run():
        c=newcache(); fwd(c,pref,0); fwd(c,sp,2048); del c
    def run0():
        c=newcache(); fwd(c,pref,0); del c
    t=max(timeit(run)-timeit(run0),1e-6)
    res['runs'].append(dict(kind='batch',k=k,tokens=512*k,ms=t*1000))
    print(f"  k={k} ({512*k} tok): {t*1000:.1f} ms  ({t*1000/(512*k)*1000:.1f} ms/1k)", flush=True)

print("\n=== A3 重建 vs host KV 回传(同等跨度) ===", flush=True)
for span_len in (512, 2048):
    nbytes=span_len*BPT
    host=[(torch.empty(1,NKV,span_len,HD,dtype=torch.bfloat16,pin_memory=True),
           torch.empty(1,NKV,span_len,HD,dtype=torch.bfloat16,pin_memory=True)) for _ in range(NL)]
    def xfer():
        for k_,v_ in host:
            k_.to('cuda',non_blocking=True); v_.to('cuda',non_blocking=True)
    t_x=timeit(xfer)
    pref=make_span(2048); sp=make_span(span_len)
    def run():
        c=newcache(); fwd(c,pref,0); fwd(c,sp,2048); del c
    def run0():
        c=newcache(); fwd(c,pref,0); del c
    t_r=max(timeit(run)-timeit(run0),1e-6)
    res['runs'].append(dict(kind='vs_transfer',span=span_len,rebuild_ms=t_r*1000,
                            transfer_ms=t_x*1000,mb=nbytes/1e6))
    print(f"  {span_len} tok ({nbytes/1e6:.0f} MB): 重建 {t_r*1000:.1f}ms | pinned回传 {t_x*1000:.1f}ms "
          f"({nbytes/1e9/t_x:.1f} GB/s) | 比值 {t_r/t_x:.2f}x", flush=True)
    del host

print("\n=== A4 保真度: 存根态前缀上重建 vs 原始全前缀 ===", flush=True)
@torch.inference_mode()
def span_kv(prefix_tokens, span_tokens, pos0, stub_frac=None):
    c=newcache()
    if stub_frac is None:
        fwd(c,prefix_tokens,0)
    else:  # 存根态: 前缀只留头部+每512段前8token
        keep=[]; n=prefix_tokens.shape[1]
        head=min(64,n); keep+=list(range(head))
        for st in range(head,n,512): keep+=list(range(st,min(st+8,n)))
        fwd(c,prefix_tokens,0)
        ki=torch.as_tensor(keep,dtype=torch.long)
        for lyr in c.layers:
            kd=ki.to(lyr.keys.device)
            lyr.keys=lyr.keys[:,:,kd,:].contiguous(); lyr.values=lyr.values[:,:,kd,:].contiguous()
    L0=c.get_seq_length()
    fwd(c,span_tokens,pos0)
    out=[(l.keys[:,:,L0:,:].float().cpu(), l.values[:,:,L0:,:].float().cpu()) for l in c.layers]
    del c; torch.cuda.empty_cache(); return out
for prefix_len in (2048, 8192):
    pref=make_span(prefix_len); sp=make_span(512)
    full=span_kv(pref,sp,prefix_len,None)
    stub=span_kv(pref,sp,prefix_len,0.1)
    cos_k=[];cos_v=[]
    for (k1,v1),(k2,v2) in zip(full,stub):
        cos_k.append(torch.nn.functional.cosine_similarity(k1.flatten(),k2.flatten(),dim=0).item())
        cos_v.append(torch.nn.functional.cosine_similarity(v1.flatten(),v2.flatten(),dim=0).item())
    res['runs'].append(dict(kind='fidelity',prefix=prefix_len,cos_k=float(np.mean(cos_k)),
                            cos_v=float(np.mean(cos_v)),cos_k_min=float(np.min(cos_k))))
    print(f"  前缀{prefix_len}: K余弦 {np.mean(cos_k):.4f}(最低层 {np.min(cos_k):.4f}) "
          f"V余弦 {np.mean(cos_v):.4f}", flush=True)

print("\n=== A5 恢复预算: 各等待窗可重建 token 数 ===", flush=True)
ms1k=np.mean([r['ms']/r['span']*1000 for r in res['runs'] if r['kind']=='rebuild' and r['span']>=512])
for w in (0.29,1.09,3.0,6.0):
    print(f"  等待{w:>4.2f}s -> 可重建 {w*1000/ms1k*1000:>7.0f} token  ({w*1000/ms1k*1000*BPT/1e9:.2f} GB 等效KV)", flush=True)
res['ms_per_1k']=float(ms1k)
json.dump(res,open(a.out,'w'),indent=1)
print(f"\n均值 {ms1k:.1f} ms/1k token -> 写入 {a.out}", flush=True)

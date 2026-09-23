"""E13-H3: 定KV显存预算下, 全KV vs ToolKV压缩上下文的批量decode吞吐(实测)。
合成KV(随机bf16)按各臂实测平均上下文长度构造; 批量=预算/每episode KV; 测32步decode tok/s。"""
import time,torch,argparse
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
ap=argparse.ArgumentParser()
ap.add_argument('--budget-gb',type=float,default=8.0)
ap.add_argument('--lens',default='full:1220,rho25:380,rho10:200')
ap.add_argument('--steps',type=int,default=32)
a=ap.parse_args()
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
tok=AutoTokenizer.from_pretrained(M)
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
cfg=model.config
NL=cfg.num_hidden_layers; NKV=cfg.num_key_value_heads; HD=getattr(cfg,'head_dim',cfg.hidden_size//cfg.num_attention_heads)
bytes_per_tok=NL*2*NKV*HD*2
print(f"模型: {NL}层 kv_heads={NKV} head_dim={HD} -> {bytes_per_tok/1024:.0f} KB/token")
@torch.inference_mode()
def bench(B, L, steps):
    c=DynamicCache()
    dummy=torch.zeros(B,1,dtype=torch.long,device='cuda')
    # 预填合成KV
    for i in range(NL):
        k=torch.randn(B,NKV,L,HD,dtype=torch.bfloat16,device='cuda')*0.02
        v=torch.randn(B,NKV,L,HD,dtype=torch.bfloat16,device='cuda')*0.02
        c.update(k,v,i)
    pos=torch.full((B,1),L,dtype=torch.long,device='cuda')
    o=model(input_ids=dummy, past_key_values=c, position_ids=pos, cache_position=pos[0])
    torch.cuda.synchronize(); t0=time.perf_counter()
    for s_ in range(steps):
        p=torch.full((B,1),L+1+s_,dtype=torch.long,device='cuda')
        o=model(input_ids=dummy, past_key_values=c, position_ids=p, cache_position=p[0])
    torch.cuda.synchronize(); dt=time.perf_counter()-t0
    del c; torch.cuda.empty_cache()
    return B*steps/dt
budget=a.budget_gb*1e9
rows=[]
for spec in a.lens.split(','):
    name,L=spec.split(':'); L=int(L)
    B=max(1,int(budget/(L*bytes_per_tok)))
    B=min(B,512)
    tp=bench(B,L,a.steps)
    rows.append((name,L,B,tp))
    print(f"{name:>6}: ctx {L:5d} tok  批量 {B:4d}  decode {tp:8.0f} tok/s")
base=rows[0][3]
for name,L,B,tp in rows[1:]:
    print(f"{name} vs full: 吞吐 {tp/base:.2f}x  (+{100*(tp/base-1):.0f}%)")

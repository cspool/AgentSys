"""T1 层设计假设实测: KV 换出/回传(PCIe) vs 重 prefill, Qwen3-1.7B, 1.5k token 上下文。"""
import time, torch
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
tok=AutoTokenizer.from_pretrained(M)
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
text=("The quick brown fox jumps over the lazy dog. "*220)
ids=tok(text, return_tensors='pt').input_ids[:, :1500].to('cuda')
with torch.inference_mode():
    for _ in range(2):     # 预热
        c=DynamicCache(); model(input_ids=ids, past_key_values=c)
    torch.cuda.synchronize()
    t0=time.perf_counter(); c=DynamicCache(); model(input_ids=ids, past_key_values=c)
    torch.cuda.synchronize(); t_prefill=time.perf_counter()-t0
    layers=list(c.to_legacy_cache()) if hasattr(c,"to_legacy_cache") else [(l.keys,l.values) for l in c.layers]
    nbytes=sum(k.numel()*k.element_size()+v.numel()*v.element_size() for k,v in layers)
    # 换出 T0->T1 (pinned host)
    torch.cuda.synchronize(); t0=time.perf_counter()
    host=[(k.to('cpu', non_blocking=False), v.to('cpu', non_blocking=False)) for k,v in layers]
    torch.cuda.synchronize(); t_out=time.perf_counter()-t0
    # 回传 T1->T0
    torch.cuda.synchronize(); t0=time.perf_counter()
    back=[(k.to('cuda', non_blocking=False), v.to('cuda', non_blocking=False)) for k,v in host]
    torch.cuda.synchronize(); t_in=time.perf_counter()-t0
print(f"KV 体量: {nbytes/1048576:.0f} MB ({nbytes/1500/1024:.0f} KB/token)")
print(f"重 prefill(T2->T0): {t_prefill*1000:.1f} ms")
print(f"换出(T0->T1):      {t_out*1000:.1f} ms  ({nbytes/t_out/1e9:.1f} GB/s)")
print(f"回传(T1->T0):      {t_in*1000:.1f} ms  ({nbytes/t_in/1e9:.1f} GB/s)")
print(f"T1 回传相对重 prefill 便宜: {t_prefill/t_in:.1f}x")

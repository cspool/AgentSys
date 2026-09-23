"""E13 机械件: DynamicCache 中段驱逐 + 显式 position 续推。自测: 藏码召回。
陷阱: 驱逐后 cache 长度 < 真实位置, 后续 forward 必须显式传 position_ids/cache_position。"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
tok=AutoTokenizer.from_pretrained(M)
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
def ids(s): return tok(s, return_tensors='pt', add_special_tokens=False).input_ids.to('cuda')

def evict(cache, keep_idx):
    """按 keep_idx(升序 LongTensor) 保留 cache 条目, 其余驱逐。返回新长度。"""
    for lyr in cache.layers:
        lyr.keys=lyr.keys[:,:,keep_idx,:].contiguous()
        lyr.values=lyr.values[:,:,keep_idx,:].contiguous()
    return keep_idx.numel()

@torch.inference_mode()
def fwd(cache, token_ids, pos_start):
    n=token_ids.shape[1]
    pos=torch.arange(pos_start, pos_start+n, device='cuda').unsqueeze(0)
    return model(input_ids=token_ids, past_key_values=cache,
                 position_ids=pos, cache_position=pos[0])

@torch.inference_mode()
def gen(cache, suffix, pos_start, max_new=24):
    o=fwd(cache, ids(suffix), pos_start); p=pos_start+ids(suffix).shape[1]
    nxt=o.logits[0,-1].argmax(); toks=[]
    for _ in range(max_new):
        toks.append(nxt.item())
        if '<|im_end|>' in tok.decode(toks[-3:]): break
        o=fwd(cache, nxt.view(1,1), p); p+=1
        nxt=o.logits[0,-1].argmax()
    return tok.decode(toks).replace('<|im_end|>','').strip()

# 自测: 头部(系统+问题前置) + 跨度A(藏码) + 大段填充跨度B + 问句
head="<|im_start|>user\nRemember: the secret code is 7391.\n"
filler="Background: "+("the weather report mentions rain, wind, mild temperatures and scattered clouds across the region. "*30)
tail="\nWhat is the secret code? Answer with the number only.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
c=DynamicCache()
n_head=ids(head).shape[1]; fwd(c, ids(head), 0)
n_fill=ids(filler).shape[1]; fwd(c, ids(filler), n_head)
Ltrue=n_head+n_fill
print(f"head {n_head} tok + filler {n_fill} tok = {Ltrue}")
# 情形1: 不驱逐(对照)
import copy
ans_full=gen(copy.deepcopy(c), tail, Ltrue)
# 情形2: 驱逐整个 filler 跨度(留头部), 位置继续从 Ltrue
keep=torch.arange(0, n_head, device='cuda')
c2=copy.deepcopy(c); newlen=evict(c2, keep)
ans_evict=gen(c2, tail, Ltrue)
# 情形3: 驱逐 filler 但错误地用 cache 长度当位置(演示陷阱)
c3=copy.deepcopy(c); evict(c3, keep)
ans_wrongpos=gen(c3, tail, n_head)
print(f"全KV        : {ans_full!r}")
print(f"驱逐+对位置 : {ans_evict!r}  (cache {Ltrue}->{newlen})")
print(f"驱逐+错位置 : {ans_wrongpos!r}")
ok = '7391' in ans_full and '7391' in ans_evict
print("PASS" if ok else "FAIL")

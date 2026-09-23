"""机制3 流式共享前缀: N 个 fan-out 孩子共读父输出。
基线 = 每孩子独立 prefill [父输出+自己指令]; 共享 = 父 KV 建一次, 孩子只 prefill 后缀(crop 复用)。
测: 总 prefill 算力、孩子 TTFT、输出一致性(贪心下应近同)。单用户桌面场景, GPU0。"""
import copy, time, torch
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
tok=AutoTokenizer.from_pretrained(M)
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
NOTHINK="<think>\n\n</think>\n\n"
def ids(s): return tok(s, return_tensors='pt', add_special_tokens=False).input_ids.to('cuda')

parent_report=("Quarterly operations report. "+"The logistics division processed 4210 shipments with a 2.1 percent delay rate. "
 "Warehouse B in Leipzig reached 91 percent capacity. The new routing system cut fuel costs by 8 percent. "
 "Customer complaints fell to 37 cases, mostly about packaging. Staff turnover was 5 percent. "
 "The Osaka hub opened in March and handled 830 shipments. Two safety incidents were recorded, both minor. "
 "IT migrated the tracking database with 40 minutes of downtime. Next quarter targets 5000 shipments. ")*4
HEAD="<|im_start|>system\nYou are a helpful analyst.<|im_end|>\n<|im_start|>user\nUpstream agent report:\n"
KIDS=[("summary","\nTask: summarize the report in one sentence."),
      ("numbers","\nTask: list every number mentioned with its meaning, briefly."),
      ("risk","\nTask: name the single biggest operational risk."),
      ("qa","\nTask: how many shipments did the Osaka hub handle?")]
SUF="<|im_end|>\n<|im_start|>assistant\n"+NOTHINK

@torch.inference_mode()
def prefill(c,s):
    t0=time.perf_counter(); i=ids(s); model(input_ids=i, past_key_values=c)
    torch.cuda.synchronize(); return time.perf_counter()-t0, i.shape[1]
@torch.inference_mode()
def gen(c, max_new=48):
    t0=time.perf_counter(); toks=[]
    out_ids=ids(SUF); out=model(input_ids=out_ids, past_key_values=c)
    nxt=out.logits[0,-1].argmax()
    for _ in range(max_new):
        toks.append(nxt.item())
        if '<|im_end|>' in tok.decode(toks[-3:]): break
        out=model(input_ids=nxt.view(1,1), past_key_values=c); nxt=out.logits[0,-1].argmax()
    torch.cuda.synchronize(); return tok.decode(toks).replace('<|im_end|>','').strip(), time.perf_counter()-t0

n_parent=ids(HEAD+parent_report).shape[1]
print(f"父上下文 {n_parent} token, 孩子 {len(KIDS)} 个\n")
# 基线: 每孩子独立全量
tot_base=0; outs_base={}
for name,instr in KIDS:
    c=DynamicCache(); tp,_=prefill(c, HEAD+parent_report+instr)
    o,tg=gen(c); outs_base[name]=o; tot_base+=tp
    print(f"  基线 {name:<8} prefill {tp*1000:6.1f}ms  gen {tg*1000:6.1f}ms")
    del c
# 共享: 父建一次, 孩子 crop 复用
c=DynamicCache(); t_parent,_=prefill(c, HEAD+parent_report)
L=c.get_seq_length(); tot_shared=t_parent; outs_sh={}
for name,instr in KIDS:
    tp,_=prefill(c, instr)
    o,tg=gen(c); outs_sh[name]=o; tot_shared+=tp
    c.crop(L)
    print(f"  共享 {name:<8} 后缀prefill {tp*1000:5.1f}ms  gen {tg*1000:6.1f}ms")
match=sum(outs_base[k]==outs_sh[k] for k,_ in KIDS)
print(f"\n父 prefill 一次 {t_parent*1000:.1f}ms | 基线总 prefill {tot_base*1000:.1f}ms | 共享总 {tot_shared*1000:.1f}ms")
print(f"prefill 算力节省 {100*(tot_base-tot_shared)/tot_base:.1f}%  (理论 ~{100*(len(KIDS)-1)/len(KIDS):.0f}%)")
print(f"输出一致性: {match}/{len(KIDS)} 完全相同")
for k,_ in KIDS: print(f"  [{k}] {outs_sh[k][:70]}")

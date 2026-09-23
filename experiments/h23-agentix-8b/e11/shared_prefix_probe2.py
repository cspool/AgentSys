"""机制3 流式共享前缀 v2: 加 warmup, 父上下文三档长度, 找算力收益的交叉点。"""
import time, torch
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
M='/data3/docker_model/AgentSys/Qwen3-1.7B'
tok=AutoTokenizer.from_pretrained(M)
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
NOTHINK="<think>\n\n</think>\n\n"
def ids(s): return tok(s, return_tensors='pt', add_special_tokens=False).input_ids.to('cuda')
BASE=("The logistics division processed 4210 shipments with a 2.1 percent delay rate. "
 "Warehouse B in Leipzig reached 91 percent capacity. The new routing system cut fuel costs by 8 percent. "
 "Customer complaints fell to 37 cases, mostly about packaging. Staff turnover was 5 percent. "
 "The Osaka hub opened in March and handled 830 shipments. Two safety incidents were recorded, both minor. "
 "IT migrated the tracking database with 40 minutes of downtime. Next quarter targets 5000 shipments. ")
HEAD="<|im_start|>system\nYou are a helpful analyst.<|im_end|>\n<|im_start|>user\nUpstream agent report:\n"
KIDS=[("summary","\nTask: summarize the report in one sentence."),
      ("numbers","\nTask: state the delay rate and the fuel cost reduction."),
      ("risk","\nTask: name the single biggest operational risk."),
      ("qa","\nTask: how many shipments did the Osaka hub handle?")]
SUF="<|im_end|>\n<|im_start|>assistant\n"+NOTHINK

@torch.inference_mode()
def prefill(c,s):
    i=ids(s); torch.cuda.synchronize(); t0=time.perf_counter()
    model(input_ids=i, past_key_values=c)
    torch.cuda.synchronize(); return time.perf_counter()-t0
@torch.inference_mode()
def gen(c, max_new=24):
    toks=[]; out=model(input_ids=ids(SUF), past_key_values=c); nxt=out.logits[0,-1].argmax()
    for _ in range(max_new):
        toks.append(nxt.item())
        if '<|im_end|>' in tok.decode(toks[-3:]): break
        out=model(input_ids=nxt.view(1,1), past_key_values=c); nxt=out.logits[0,-1].argmax()
    return tok.decode(toks).replace('<|im_end|>','').strip()

# warmup
c=DynamicCache(); prefill(c,HEAD+BASE); gen(c,4); del c

for rep in (2,8,24):
    report="Quarterly operations report. "+BASE*rep
    n=ids(HEAD+report).shape[1]
    tot_b=0; outs_b={}
    for name,instr in KIDS:
        c=DynamicCache(); tot_b+=prefill(c,HEAD+report+instr); outs_b[name]=gen(c); del c
    c=DynamicCache(); tp=prefill(c,HEAD+report); L=c.get_seq_length(); tot_s=tp
    outs_s={}
    for name,instr in KIDS:
        tot_s+=prefill(c,instr); outs_s[name]=gen(c); c.crop(L)
    del c
    match=sum(outs_b[k]==outs_s[k] for k,_ in KIDS)
    qa_ok=('830' in outs_s['qa'], '830' in outs_b['qa'])
    print(f"父{n:5d}tok  基线总prefill {tot_b*1000:7.1f}ms  共享总 {tot_s*1000:7.1f}ms"
          f"  节省 {100*(tot_b-tot_s)/tot_b:+6.1f}%  逐字一致 {match}/4  qa对(共享/基线) {qa_ok}")

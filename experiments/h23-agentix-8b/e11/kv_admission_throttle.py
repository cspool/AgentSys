"""8B 形态(b)节流: 后台prefill的chunk大小=占用粒度, 扫描其对关键路径decode膨胀的控制力。"""
import threading, time, torch
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
M='/data3/docker_model/AgentSys/Llama-3.1-8B'
tok=AutoTokenizer.from_pretrained(M)
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
def ids(s): return tok(s, return_tensors='pt', add_special_tokens=False).input_ids.to('cuda')
CTX="Quarterly operations report. "+("The logistics division processed 4210 shipments with a 2.1 percent delay rate. "
 "Warehouse B in Leipzig reached 91 percent capacity. The Osaka hub opened in March and handled 830 shipments. ")*90
A_PROMPT="<|im_start|>user\nWrite a long story about a logistics robot.<|im_end|>\n<|im_start|>assistant\n"
B_IDS=ids(CTX); N_DEC=128
@torch.inference_mode()
def decode_A(stream, out):
    with torch.cuda.stream(stream):
        c=DynamicCache(); o=model(input_ids=ids(A_PROMPT), past_key_values=c); nxt=o.logits[0,-1].argmax()
        stream.synchronize(); t0=time.perf_counter()
        for _ in range(N_DEC):
            o=model(input_ids=nxt.view(1,1), past_key_values=c); nxt=o.logits[0,-1].argmax()
        stream.synchronize(); out['t']=time.perf_counter()-t0
@torch.inference_mode()
def prefill_B(stream, out, chunk, gap_ms=0.0):
    with torch.cuda.stream(stream):
        c=DynamicCache(); stream.synchronize(); t0=time.perf_counter()
        for i in range(0, B_IDS.shape[1], chunk):
            model(input_ids=B_IDS[:,i:i+chunk], past_key_values=c)
            if gap_ms: stream.synchronize(); time.sleep(gap_ms/1000)
        stream.synchronize(); out['t']=time.perf_counter()-t0
s1,s2=torch.cuda.Stream(),torch.cuda.Stream()
r={}; decode_A(s1,r); prefill_B(s2,{}, 512)  # warmup
a0={}; decode_A(s1,a0)
print(f"solo A: {a0['t']/N_DEC*1000:.1f}ms/tok ({a0['t']*1000:.0f}ms)")
for chunk,gap in ((512,0),(128,0),(64,0),(128,20),(64,20)):
    ac,bc={},{}
    th=[threading.Thread(target=decode_A,args=(s1,ac)), threading.Thread(target=prefill_B,args=(s2,bc,chunk,gap))]
    for t in th: t.start()
    for t in th: t.join()
    print(f"chunk={chunk:4d} gap={gap:2d}ms: A膨胀 {100*(ac['t']-a0['t'])/a0['t']:+5.1f}%  B完成 {bc['t']*1000:5.0f}ms")

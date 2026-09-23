"""机制4形态(b): 他agent bs=1 decode(访存瓶颈)时, 并发转换prefill能否搭便车。
A=前台decode 128 tok(关键路径), B=2.6k tok转换prefill。solo各测, 再双线程双stream并发。
指标: A每token延迟膨胀 %, B完成时间, 及'B激活时TTFT=0'的换算。"""
import threading, time, torch
from transformers import AutoModelForCausalLM, AutoTokenizer, DynamicCache
M='/data3/docker_model/AgentSys/Llama-3.1-8B'
tok=AutoTokenizer.from_pretrained(M)
model=AutoModelForCausalLM.from_pretrained(M, dtype=torch.bfloat16, device_map='cuda'); model.eval()
def ids(s): return tok(s, return_tensors='pt', add_special_tokens=False).input_ids.to('cuda')
CTX="Quarterly operations report. "+("The logistics division processed 4210 shipments with a 2.1 percent delay rate. "
 "Warehouse B in Leipzig reached 91 percent capacity. The Osaka hub opened in March and handled 830 shipments. ")*90
A_PROMPT="<|im_start|>user\nWrite a long story about a logistics robot.<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
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
def prefill_B(stream, out, chunk=512):
    with torch.cuda.stream(stream):
        c=DynamicCache(); stream.synchronize(); t0=time.perf_counter()
        for i in range(0, B_IDS.shape[1], chunk):
            model(input_ids=B_IDS[:,i:i+chunk], past_key_values=c)
        stream.synchronize(); out['t']=time.perf_counter()-t0

s1,s2=torch.cuda.Stream(),torch.cuda.Stream()
r={}; decode_A(s1,r); prefill_B(s2,r2:={})  # warmup
a0={}; decode_A(s1,a0); b0={}; prefill_B(s2,b0)
print(f"solo: A decode {N_DEC}tok {a0['t']*1000:.0f}ms ({a0['t']/N_DEC*1000:.2f}ms/tok) | B prefill {B_IDS.shape[1]}tok {b0['t']*1000:.0f}ms")
ac,bc={},{}
th=[threading.Thread(target=decode_A,args=(s1,ac)), threading.Thread(target=prefill_B,args=(s2,bc))]
t0=time.perf_counter()
for t in th: t.start()
for t in th: t.join()
wall=time.perf_counter()-t0
infl=100*(ac['t']-a0['t'])/a0['t']
print(f"并发: A {ac['t']*1000:.0f}ms (膨胀 {infl:+.1f}%) | B {bc['t']*1000:.0f}ms | 墙钟 {wall*1000:.0f}ms vs 串行 {(a0['t']+b0['t'])*1000:.0f}ms")
print(f"判决: B激活时TTFT 0ms(已预转换) vs 延付 {b0['t']*1000:.0f}ms; 代价=关键路径decode慢 {infl:.1f}%")

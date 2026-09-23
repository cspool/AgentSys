import json, sys, torch, triton, triton.language as tl
@triton.jit
def fma_full(x, n, reps, BLOCK: tl.constexpr):
    pid = tl.program_id(0); offs = pid*BLOCK + tl.arange(0, BLOCK); mask = offs < n
    v = tl.load(x+offs, mask=mask)
    for _ in range(reps): v = v*1.000001+0.000001
    tl.store(x+offs, v, mask=mask)
BLOCK=256; n=128*6*BLOCK
x=torch.randn(n, device='cuda')
fma_full[(n//BLOCK,)](x,n,8,BLOCK=BLOCK); torch.cuda.synchronize()
cache=json.load(open(sys.argv[1])); out={}
for k, reps in cache.items():
    ts=[]
    for _ in range(12):
        s=torch.cuda.Event(enable_timing=True); e=torch.cuda.Event(enable_timing=True)
        s.record(); fma_full[(n//BLOCK,)](x,n,reps,BLOCK=BLOCK); e.record(); torch.cuda.synchronize()
        ts.append(s.elapsed_time(e))
    ts.sort(); out[k]=ts[len(ts)//2]
    print(f"W_label={k} reps={reps} 真solo={ts[len(ts)//2]:.3f}ms")
json.dump(out, open(sys.argv[2],'w'))

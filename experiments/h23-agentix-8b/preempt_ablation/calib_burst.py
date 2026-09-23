import torch, triton, triton.language as tl, json
@triton.jit
def fma_full(x, n, reps, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid*BLOCK + tl.arange(0, BLOCK); mask = offs < n
    v = tl.load(x+offs, mask=mask)
    for _ in range(reps): v = v*1.000001+0.000001
    tl.store(x+offs, v, mask=mask)
BLOCK=256; n=128*6*BLOCK
x=torch.randn(n, device='cuda')
fma_full[(n//BLOCK,)](x,n,8,BLOCK=BLOCK); torch.cuda.synchronize()
r=1000
while True:
    s=torch.cuda.Event(enable_timing=True); e=torch.cuda.Event(enable_timing=True)
    s.record(); fma_full[(n//BLOCK,)](x,n,r,BLOCK=BLOCK); e.record(); torch.cuda.synchronize()
    ms=s.elapsed_time(e)
    if ms>=12: break
    r=int(r*max(2,15/max(ms,.05)))
open('burst_reps.txt','w').write(str(r))
print('burst reps',r,f'{ms:.1f}ms')

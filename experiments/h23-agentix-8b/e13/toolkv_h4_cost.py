"""E13-H4: 压缩操作成本. 手术(28层 index_select)+评分池化, vs 工具等待窗(秒级)与重prefill。
部署中评分注意力由引擎正常计算顺带产出(只需暴露), 此处测纯手术与池化开销。"""
import time,torch
NL,NKV,HD=28,8,128
def bench_surgery(L=1220, keep=380, iters=50):
    ks=[torch.randn(1,NKV,L,HD,dtype=torch.bfloat16,device='cuda') for _ in range(NL)]
    vs=[torch.randn(1,NKV,L,HD,dtype=torch.bfloat16,device='cuda') for _ in range(NL)]
    idx=torch.randperm(L,device='cuda')[:keep].sort().values
    torch.cuda.synchronize(); t0=time.perf_counter()
    for _ in range(iters):
        for k,v in zip(ks,vs):
            _=k[:,:,idx,:].contiguous(); _=v[:,:,idx,:].contiguous()
    torch.cuda.synchronize()
    return (time.perf_counter()-t0)/iters*1000
def bench_pool(L=1220, heads=16, steps=16, iters=50):
    att=[torch.rand(1,heads,1,L,device='cuda') for _ in range(NL)]
    acc=torch.zeros(L,device='cuda')
    torch.cuda.synchronize(); t0=time.perf_counter()
    for _ in range(iters):
        for _s in range(steps):
            for a in att: acc+=a[0,:,0,:].mean(dim=0)
    torch.cuda.synchronize()
    return (time.perf_counter()-t0)/iters*1000
s=bench_surgery(); p=bench_pool()
print(f"手术(1220->380tok, 28层K+V): {s:.2f} ms/次")
print(f"评分池化(16步x28层): {p:.2f} ms/消费轮")
print(f"合计 ~{s+p:.1f} ms  vs 工具等待窗 1000-10000 ms  vs 重prefill(1.5k tok) 48 ms")
print(f"=> 压缩成本 {(s+p)/1000*100:.1f}% 个最短等待窗, 藏入等待窗成立")

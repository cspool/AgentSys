"""配额动态范围门禁: BASE 与 BURST 两档下抢占者的绝对吞吐之比必须 >= 1.5,
否则配额这个自变量没有动态范围, 抢占时机的任何差异都无从产生。"""
import argparse, json, sys, time, torch
sys.path.insert(0, '/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3')
from common.quota import TpcMaskKnob

ap = argparse.ArgumentParser()
ap.add_argument('--axis', default='tc'); ap.add_argument('--secs', type=float, default=6)
ap.add_argument('--tpcs', default='2,4,8,16,32,48,64'); ap.add_argument('--out', default=None)
a = ap.parse_args()
dev = torch.device('cuda'); torch.zeros(1, device=dev)
if a.axis == 'tc':
    A = torch.randn(1024,2048,device=dev,dtype=torch.float16); B = torch.randn(2048,1024,device=dev,dtype=torch.float16)
    op = lambda: A @ B
else:
    import torch.nn.functional as F
    q=torch.randn(8,32,1,128,device=dev,dtype=torch.float16); k=torch.randn(8,8,4096,128,device=dev,dtype=torch.float16)
    v=torch.randn(8,8,4096,128,device=dev,dtype=torch.float16)
    op = lambda: F.scaled_dot_product_attention(q,k,v,enable_gqa=True)
s = torch.cuda.Stream()
knob = TpcMaskKnob(s, base_tpcs=2, burst_tpcs=64)
res = {}
print(f"{'TPC':>5}{'SM':>5}{'calls/s':>12}{'相对64TPC':>11}")
ref = None
for n in [int(x) for x in a.tpcs.split(',')]:
    knob.levels['BASE'] = n; knob.set_quota('BASE')
    with torch.cuda.stream(s):
        for _ in range(30): op()
    torch.cuda.synchronize()
    t0=time.perf_counter(); cnt=0
    with torch.cuda.stream(s):
        while time.perf_counter()-t0 < a.secs:
            for _ in range(16): op()
            cnt += 16
            torch.cuda.current_stream().synchronize()
    r = cnt/(time.perf_counter()-t0)
    if n == 64: ref = r
    res[n] = round(r,1)
    print(f"{n:>5}{n*2:>5}{r:>12.0f}{'':>11}")
if ref:
    print(f"\n{'TPC':>5}{'相对64TPC':>11}{'理想':>8}")
    for n, r in res.items(): print(f"{n:>5}{r/ref:>11.3f}{n/64:>8.3f}")
if a.out: json.dump(dict(axis=a.axis, rates=res, ref64=ref), open(a.out,'w'), indent=1)

"""最小共驻探针: 在受害者常驻时, 外来 kernel 还能不能拿到 SM。
用法: corunner_probe.py --secs 20 [--tag solo|contended]
输出: 达成的 GEMM 次数/秒, 以及 %smid 直方图覆盖的 SM 数。
"""
import argparse, json, time, torch

ap = argparse.ArgumentParser()
ap.add_argument('--secs', type=float, default=20)
ap.add_argument('--tag', default='solo')
ap.add_argument('--out', default=None)
a = ap.parse_args()

dev = torch.device('cuda')
torch.zeros(1, device=dev)
props = torch.cuda.get_device_properties(0)
# 小 GEMM: 单发约 150-300us, 便于观察被挤占
A = torch.randn(1024, 2048, device=dev, dtype=torch.float16)
B = torch.randn(2048, 1024, device=dev, dtype=torch.float16)

s = torch.cuda.Stream()
# 预热
with torch.cuda.stream(s):
    for _ in range(20): A @ B
torch.cuda.synchronize()

n = 0
t0 = time.perf_counter()
deadline = t0 + a.secs
evts = []
with torch.cuda.stream(s):
    while time.perf_counter() < deadline:
        for _ in range(50):
            A @ B
        n += 50
        torch.cuda.current_stream().synchronize()
t1 = time.perf_counter()
dur = t1 - t0
flops = 2 * 1024 * 2048 * 1024
res = dict(tag=a.tag, secs=round(dur, 3), gemms=n,
           rate_per_s=round(n / dur, 2),
           tflops=round(n * flops / dur / 1e12, 3),
           sm_count=props.multi_processor_count)
print(json.dumps(res, ensure_ascii=False))
if a.out: json.dump(res, open(a.out, 'w'), ensure_ascii=False, indent=1)

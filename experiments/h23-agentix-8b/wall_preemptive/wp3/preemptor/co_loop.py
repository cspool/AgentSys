"""抢占者: 自补充发射循环 + 分桶速率。
全程并发的基础件 —— stream 上恒保持 depth 个 kernel 在飞, 不 sync 不 sleep。
分桶速率用于事后判定"受害者在场 vs 不在场"的区间, 以及算 rho。
"""
import argparse, json, time, torch

ap = argparse.ArgumentParser()
ap.add_argument('--secs', type=float, default=60)
ap.add_argument('--bucket-ms', type=int, default=200)
ap.add_argument('--axis', default='tc', choices=['tc', 'fp32', 'dram'])
ap.add_argument('--depth', type=int, default=3)
ap.add_argument('--chunk', type=int, default=16)
ap.add_argument('--tag', default='run')
ap.add_argument('--out', default=None)
a = ap.parse_args()

dev = torch.device('cuda')
torch.zeros(1, device=dev)

def make_op(axis):
    if axis == 'tc':
        A = torch.randn(1024, 2048, device=dev, dtype=torch.float16)
        B = torch.randn(2048, 1024, device=dev, dtype=torch.float16)
        return (lambda: A @ B), 2 * 1024 * 2048 * 1024, 'FLOP'
    if axis == 'fp32':
        A = torch.randn(512, 2048, device=dev, dtype=torch.float32)
        B = torch.randn(2048, 512, device=dev, dtype=torch.float32)
        return (lambda: A @ B), 2 * 512 * 2048 * 512, 'FLOP'
    import torch.nn.functional as F
    q = torch.randn(8, 32, 1, 128, device=dev, dtype=torch.float16)
    k = torch.randn(8, 8, 4096, 128, device=dev, dtype=torch.float16)
    v = torch.randn(8, 8, 4096, 128, device=dev, dtype=torch.float16)
    nbytes = 2 * 8 * 8 * 4096 * 128 * 2
    return (lambda: F.scaled_dot_product_attention(q, k, v, enable_gqa=True)), nbytes, 'BYTE'

op, work_per_call, unit = make_op(a.axis)
s = torch.cuda.Stream()
with torch.cuda.stream(s):
    for _ in range(30): op()
torch.cuda.synchronize()

bucket = a.bucket_ms / 1000.0
CHUNK = a.chunk                      # 每个 chunk 提交 CHUNK 次 op, 只记一个 event
pool = [torch.cuda.Event() for _ in range(a.depth + 1)]
t0 = time.perf_counter(); deadline = t0 + a.secs
buckets = []; n_bucket = 0; b_start = t0
inflight = []                        # [(event, count)]
with torch.cuda.stream(s):
    while True:
        now = time.perf_counter()
        if now >= deadline: break
        while len(inflight) < a.depth:          # 自补充: 保持 depth 个 chunk 在飞
            for _ in range(CHUNK): op()
            e = pool.pop(0) if pool else torch.cuda.Event()
            e.record(s); inflight.append((e, CHUNK))
        rest = []
        for e, c in inflight:                   # 非阻塞回收
            if e.query(): n_bucket += c; pool.append(e)
            else: rest.append((e, c))
        inflight = rest
        if now - b_start >= bucket:
            buckets.append(dict(t=round(b_start - t0, 3), n=n_bucket,
                                rate=round(n_bucket / (now - b_start), 1)))
            n_bucket = 0; b_start = now
torch.cuda.synchronize()
dur = time.perf_counter() - t0
tot = sum(b['n'] for b in buckets)
res = dict(tag=a.tag, axis=a.axis, unit=unit, secs=round(dur, 3), calls=tot,
           rate_per_s=round(tot / dur, 1),
           work_per_s=round(tot * work_per_call / dur / 1e12, 4),
           bucket_ms=a.bucket_ms, buckets=buckets)
print(json.dumps({k: v for k, v in res.items() if k != 'buckets'}, ensure_ascii=False))
if a.out: json.dump(res, open(a.out, 'w'), ensure_ascii=False, indent=1)

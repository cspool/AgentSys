"""并发干扰矩阵: 受害者相位 x 共跑者资源类型 x 并发比例 rho

纠正此前 harness 的两个人为限制:
  1. 并发比例只扫到 0.15 —— 因为共跑者是每 1.5s 一次的 50ms burst。
     真实共置 serving 里 LC/BE 基本全程共存, rho ~ 1。本探针把 rho 扫到 1.0。
  2. "抢占"其实没有位移(受害者没失去资源), 语义是共存。本探针只研究共存干扰,
     位移式抢占(KV recompute/swap)另案。

rho 的实现: 共跑者按 on/off 方波占空, 周期 CO_PERIOD; rho=1 即连续运行。
两侧吞吐都记, 因为干扰是双向的。
"""
import argparse, json, statistics, threading, time
import torch, triton
import triton.language as tl


# ---- 受害者: 与 victim6/8 同一 kernel 族, 只调算术强度 ----
@triton.jit
def stream_fma(x, y, n, reps, inner, GRID: tl.constexpr, BLOCK: tl.constexpr):
    pid = tl.program_id(0); step = GRID * BLOCK * 4
    for _ in range(reps):
        i = pid * BLOCK * 4
        while i < n:
            base = i + tl.arange(0, BLOCK)
            o0, o1, o2, o3 = base, base+BLOCK, base+2*BLOCK, base+3*BLOCK
            m0, m1, m2, m3 = o0 < n, o1 < n, o2 < n, o3 < n
            v0 = tl.load(x+o0, mask=m0); v1 = tl.load(x+o1, mask=m1)
            v2 = tl.load(x+o2, mask=m2); v3 = tl.load(x+o3, mask=m3)
            for _ in range(inner):
                v0 = v0*1.000001+0.000001; v1 = v1*1.000001+0.000001
                v2 = v2*1.000001+0.000001; v3 = v3*1.000001+0.000001
            tl.store(y+o0, v0, mask=m0); tl.store(y+o1, v1, mask=m1)
            tl.store(y+o2, v2, mask=m2); tl.store(y+o3, v3, mask=m3)
            i += step


# ---- 共跑者三型: 只有主资源不同 ----
@triton.jit
def co_fp32(z, n, reps, BLOCK: tl.constexpr):          # 纯寄存器 FMA, 不碰内存
    pid = tl.program_id(0); offs = pid*BLOCK + tl.arange(0, BLOCK); m = offs < n
    v = tl.load(z+offs, mask=m)
    for _ in range(reps): v = v*1.000001+0.000001
    tl.store(z+offs, v, mask=m)

@triton.jit
def co_stream(x, y, n, reps, GRID: tl.constexpr, BLOCK: tl.constexpr):  # 流式, 算术强度极低
    pid = tl.program_id(0); step = GRID * BLOCK
    for _ in range(reps):
        i = pid * BLOCK
        while i < n:
            offs = i + tl.arange(0, BLOCK); m = offs < n
            v = tl.load(x+offs, mask=m)
            tl.store(y+offs, v*1.000001+0.000001, mask=m)
            i += step


ap = argparse.ArgumentParser()
ap.add_argument('--victim', choices=['memwall', 'compwall', 'saturated'], required=True)
ap.add_argument('--co', choices=['none', 'fp32', 'dram', 'l2'], required=True)
ap.add_argument('--rho', type=float, required=True)          # 并发比例 0..1
ap.add_argument('--secs', type=float, default=45.0)
ap.add_argument('--co-period', type=float, default=0.2)      # 方波周期
ap.add_argument('--n', type=int, default=120_000_000)
ap.add_argument('--reps-file', default='../reps_v6.json')
ap.add_argument('--out', required=True)
a = ap.parse_args()

BLOCK, GRID, N = 256, 128*6, a.n
INNER = {'memwall': 60, 'compwall': 600, 'saturated': 290}[a.victim]
REPS = json.load(open(a.reps_file))[f"{INNER}:{N}"]
# 把受害者一次迭代切小, 便于在 45s 内取到足够样本
CHUNK = max(1, REPS // 16)

dev = 'cuda'
vx = torch.randn(N, device=dev); vy = torch.empty_like(vx)
# 共跑者数据规模决定它的主资源
CO_N = {'fp32': GRID*BLOCK,            # 786KB, 落 L2, 纯算
        'l2':   10_000_000,            # 40MB, 落 72MB L2 内 -> L2 带宽
        'dram': 120_000_000}           # 480MB, 远超 L2 -> DRAM 带宽
CO_REPS = {'fp32': 400_000, 'l2': 40, 'dram': 4}

STOP = threading.Event()
v_log, co_log = [], []


def victim_thread():
    s_v = torch.cuda.Stream()
    with torch.cuda.stream(s_v):
        stream_fma[(GRID,)](vx, vy, N, 1, INNER, GRID=GRID, BLOCK=BLOCK); s_v.synchronize()
        while not STOP.is_set():
            s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
            s.record(s_v)
            stream_fma[(GRID,)](vx, vy, N, CHUNK, INNER, GRID=GRID, BLOCK=BLOCK)
            e.record(s_v); s_v.synchronize()
            v_log.append({'t': time.time(), 'ms': s.elapsed_time(e)})


def co_thread():
    if a.co == 'none' or a.rho <= 0:
        return
    s_c = torch.cuda.Stream()
    n = CO_N[a.co]; reps = CO_REPS[a.co]
    cx = torch.randn(n, device=dev)
    cy = torch.empty_like(cx) if a.co in ('l2', 'dram') else None
    with torch.cuda.stream(s_c):
        if a.co == 'fp32':
            co_fp32[(n//BLOCK,)](cx, n, 8, BLOCK=BLOCK)
        else:
            co_stream[(GRID,)](cx, cy, n, 1, GRID=GRID, BLOCK=BLOCK)
        s_c.synchronize()
        on = a.co_period * a.rho
        while not STOP.is_set():
            t_on = time.time()
            while time.time() - t_on < on and not STOP.is_set():
                s = torch.cuda.Event(enable_timing=True); e = torch.cuda.Event(enable_timing=True)
                s.record(s_c)
                if a.co == 'fp32':
                    co_fp32[(n//BLOCK,)](cx, n, reps, BLOCK=BLOCK)
                else:
                    co_stream[(GRID,)](cx, cy, n, reps, GRID=GRID, BLOCK=BLOCK)
                e.record(s_c); s_c.synchronize()
                co_log.append({'t': time.time(), 'ms': s.elapsed_time(e)})
            if a.rho < 1.0:
                time.sleep(max(0.0, a.co_period - on))


tv = threading.Thread(target=victim_thread, daemon=True)
tc = threading.Thread(target=co_thread, daemon=True)
tv.start(); time.sleep(2.0)
t0 = time.time(); tc.start()
while time.time() - t0 < a.secs:
    time.sleep(0.2)
STOP.set(); tc.join(timeout=20); tv.join(timeout=20)

v = [i['ms'] for i in v_log if i['t'] > t0 + 1]
c = [i['ms'] for i in co_log]
# 实测并发比例: 共跑者实际在跑的时间 / 窗口
co_busy = sum(c)/1000
win = (max([i['t'] for i in v_log]) - (t0+1)) if v_log else 1
res = {'victim': a.victim, 'co': a.co, 'rho_set': a.rho,
       'rho_measured': co_busy/win if win > 0 else 0,
       'v_n': len(v), 'v_med_ms': statistics.median(v) if v else None,
       'v_tp': len(v)/win if win > 0 else 0,
       'co_n': len(c), 'co_med_ms': statistics.median(c) if c else None,
       'co_tp': len(c)/win if win > 0 else 0, 'window_s': win}
json.dump(res, open(a.out, 'w'))
print(f"{a.victim:<10} co={a.co:<5} rho设={a.rho:.2f} 实测={res['rho_measured']:.2f}  "
      f"受害者 {res['v_med_ms']:.1f}ms x{res['v_n']} (tp {res['v_tp']:.2f}/s)  "
      f"共跑者 {(res['co_med_ms'] or 0):.1f}ms x{res['co_n']} (tp {res['co_tp']:.2f}/s)")

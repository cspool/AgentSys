"""用真实 kernel 构造 wall 负载 (不再用合成 microbenchmark)

口径(按用户 2026-09-22 的纠正):
  wall = 某个资源接近满载(>=80%), **其他资源使用也较高(40-60%)**。
  副轴 <20% 判为不合格 —— 那是只用一种资源的合成 kernel, 不是真实负载的墙。

真实 kernel 来源:
  prefill 型 : F.scaled_dot_product_attention, 长 seq, causal   -> TC/算力
  decode  型 : SDPA, q 只有 1 个 token, 大 batch + 长 KV        -> DRAM
  GEMM    型 : torch.matmul, 尺寸控制工作集落在/超出 72MB L2   -> L2 或 DRAM
"""
import argparse, json, time
import torch
import torch.nn.functional as F

def timeit(fn, warm=3, rep=10):
    for _ in range(warm): fn()
    torch.cuda.synchronize()
    t0 = time.perf_counter()
    for _ in range(rep): fn()
    torch.cuda.synchronize()
    return (time.perf_counter() - t0) / rep * 1000

def mk_prefill(B, H, Hkv, S, D, dtype=torch.float16):
    q = torch.randn(B, H, S, D, device='cuda', dtype=dtype)
    k = torch.randn(B, Hkv, S, D, device='cuda', dtype=dtype)
    v = torch.randn(B, Hkv, S, D, device='cuda', dtype=dtype)
    return lambda: F.scaled_dot_product_attention(q, k, v, is_causal=True, enable_gqa=(H != Hkv))

def mk_decode(B, H, Hkv, S_kv, D, dtype=torch.float16):
    q = torch.randn(B, H, 1, D, device='cuda', dtype=dtype)
    k = torch.randn(B, Hkv, S_kv, D, device='cuda', dtype=dtype)
    v = torch.randn(B, Hkv, S_kv, D, device='cuda', dtype=dtype)
    return lambda: F.scaled_dot_product_attention(q, k, v, is_causal=False, enable_gqa=(H != Hkv))

def mk_gemm(M, N, K, dtype=torch.float16):
    a = torch.randn(M, K, device='cuda', dtype=dtype)
    b = torch.randn(K, N, device='cuda', dtype=dtype)
    return lambda: torch.matmul(a, b)

CONFIGS = {
  # ---- prefill: llama-3-8b tp1 头配置, 扫 seq ----
  'prefill_s1k' : ('SDPA prefill B=4 H=32 Hkv=8 S=1024',  lambda: mk_prefill(4, 32, 8, 1024, 128)),
  'prefill_s2k' : ('SDPA prefill B=4 H=32 Hkv=8 S=2048',  lambda: mk_prefill(4, 32, 8, 2048, 128)),
  'prefill_s4k' : ('SDPA prefill B=2 H=32 Hkv=8 S=4096',  lambda: mk_prefill(2, 32, 8, 4096, 128)),
  'prefill_s8k' : ('SDPA prefill B=1 H=32 Hkv=8 S=8192',  lambda: mk_prefill(1, 32, 8, 8192, 128)),
  # ---- decode: 扫 batch x KV 长度, 控制 KV 总量 ----
  'decode_kv32m': ('SDPA decode B=16 Hkv=8 S_kv=2048 (KV~32MB, 落 L2)',  lambda: mk_decode(16, 32, 8, 2048, 128)),
  'decode_kv64m': ('SDPA decode B=32 Hkv=8 S_kv=2048 (KV~64MB, 逼近 L2)', lambda: mk_decode(32, 32, 8, 2048, 128)),
  'decode_kv256m':('SDPA decode B=32 Hkv=8 S_kv=8192 (KV~256MB, 超 L2)',  lambda: mk_decode(32, 32, 8, 8192, 128)),
  'decode_kv1g' : ('SDPA decode B=64 Hkv=8 S_kv=16384 (KV~1GB, 深 DRAM)', lambda: mk_decode(64, 32, 8, 16384, 128)),
  # ---- GEMM: 工作集分别落在 L2 内 / 超出 ----
  'gemm_l2'     : ('GEMM 4096x4096x4096 (A+B+C~100MB)', lambda: mk_gemm(4096, 4096, 4096)),
  'gemm_small'  : ('GEMM 2048x2048x2048 (A+B+C~25MB, 落 L2)', lambda: mk_gemm(2048, 2048, 2048)),
  'gemm_big'    : ('GEMM 8192x8192x8192 (A+B+C~400MB, 超 L2)', lambda: mk_gemm(8192, 8192, 8192)),
  # ---- TC 可达峰值校准: 大 K, 强算力受限(数据复用高, 访存少) ----
  'tc_k16k'     : ('GEMM 4096x4096x16384 (大K, 算力受限)',  lambda: mk_gemm(4096, 4096, 16384)),
  'tc_k32k'     : ('GEMM 2048x2048x32768 (更大K)',          lambda: mk_gemm(2048, 2048, 32768)),
  'tc_sq6k'     : ('GEMM 6144x6144x6144',                   lambda: mk_gemm(6144, 6144, 6144)),
  # ---- L2 墙: KV 总量压进 72MB L2, 让 decode 反复重读同一份 KV(真实 serving 行为) ----
  'l2_kv16m'    : ('SDPA decode B=4  Hkv=8 S_kv=1024 (KV~17MB)',  lambda: mk_decode(4, 32, 8, 1024, 128)),
  'l2_kv34m'    : ('SDPA decode B=8  Hkv=8 S_kv=1024 (KV~34MB)',  lambda: mk_decode(8, 32, 8, 1024, 128)),
  'l2_kv50m'    : ('SDPA decode B=12 Hkv=8 S_kv=1024 (KV~50MB)',  lambda: mk_decode(12, 32, 8, 1024, 128)),
  'l2_kv67m'    : ('SDPA decode B=16 Hkv=8 S_kv=1024 (KV~67MB)',  lambda: mk_decode(16, 32, 8, 1024, 128)),
  'l2_kv100m'   : ('SDPA decode B=24 Hkv=8 S_kv=1024 (KV~100MB)', lambda: mk_decode(24, 32, 8, 1024, 128)),
  # ---- L2 墙: 固定 KV 总量 ~34MB(稳落 L2), 提高并行度 ----
  'l2p_b16'     : ('decode B=16 S_kv=512  (KV~34MB, 并行x2)', lambda: mk_decode(16, 32, 8, 512, 128)),
  'l2p_b32'     : ('decode B=32 S_kv=256  (KV~34MB, 并行x4)', lambda: mk_decode(32, 32, 8, 256, 128)),
  'l2p_b64'     : ('decode B=64 S_kv=128  (KV~34MB, 并行x8)', lambda: mk_decode(64, 32, 8, 128, 128)),
  'l2p_b128'    : ('decode B=128 S_kv=128 (KV~67MB, 并行x16)', lambda: mk_decode(128, 32, 8, 128, 128)),
  # ---- L2 墙尝试: fp32 GEMM 走 CUDA core 不走 TC, 让 L2 有机会成为唯一饱和轴 ----
  'l2f32_2k'    : ('fp32 GEMM 2048^3 (A+B+C~50MB, 落 L2)',  lambda: mk_gemm(2048, 2048, 2048, torch.float32)),
  'l2f32_3k'    : ('fp32 GEMM 3072^3 (~113MB)',             lambda: mk_gemm(3072, 3072, 3072, torch.float32)),
  'l2f32_skinny': ('fp32 GEMM 512x8192x8192 (瘦长, 低复用)', lambda: mk_gemm(512, 8192, 8192, torch.float32)),
  'l2f16_skinny': ('fp16 GEMM 256x8192x8192 (瘦长, TC 利用低)', lambda: mk_gemm(256, 8192, 8192)),
}

ap = argparse.ArgumentParser()
ap.add_argument('--only', default=None)
ap.add_argument('--prof', action='store_true', help='NCU 模式: 只发射一次')
a = ap.parse_args()

torch.backends.cuda.matmul.allow_tf32 = False
print(f"{'配置':<16}{'说明':<48}{'ms':>9}")
print('-'*76)
for name, (desc, mk) in CONFIGS.items():
    if a.only and name != a.only: continue
    try:
        fn = mk()
        if a.prof:
            fn(); torch.cuda.synchronize(); fn(); torch.cuda.synchronize()
            print(f"{name}  profiled")
        else:
            ms = timeit(fn)
            print(f"{name:<16}{desc:<48}{ms:>8.3f}")
        del fn; torch.cuda.empty_cache()
    except Exception as e:
        print(f"{name:<16}{desc:<48}  FAIL {type(e).__name__}: {str(e)[:60]}")

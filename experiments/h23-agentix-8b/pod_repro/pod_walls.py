"""用 POD 的真实负载(prefill/decode 混合批 attention)组装不同 wall 类型 — GPU1

POD 的负载天然横跨两类资源:
  prefill attention : 算力/TC 重 (长 seq, 大 M-tile)
  decode  attention : DRAM 重   (1 token/seq, 反复读 KV cache)
因此**同一个 POD kernel** 通过调 (prefill chunk 长度, decode batch, KV 长度, PD 比例)
就能落到不同的 wall —— 这正是"用真实论文负载构造 wall"的形态, 不需要另造合成 kernel。

wall 候选(待 NCU 验收: 目标轴 >=80% 或达可达峰值, 副轴 30-60%):
  W_pref  纯 prefill 重     : 大 S_p, 小 B_d    -> 预期 TC 高
  W_dec   纯 decode 重      : 小 S_p, 大 B_d x 长 KV -> 预期 DRAM 高
  W_mix   混合批(POD 本行)  : 两者都有           -> 预期双轴高(全饱和)
"""
import argparse, json, statistics, time, torch, pod_attn

def mk(B_p, S_p, B_d, S_kv, H=32, Hkv=8, D=128, seed=7):
    g = torch.Generator(device='cuda').manual_seed(seed)
    t = lambda *s: torch.randn(*s, device='cuda', dtype=torch.float16, generator=g)
    return dict(q_p=t(B_p,S_p,H,D), k_p=t(B_p,S_p,Hkv,D), v_p=t(B_p,S_p,Hkv,D),
                q_d=t(B_d,1,H,D),   k_d=t(B_d,S_kv,Hkv,D), v_d=t(B_d,S_kv,Hkv,D),
                cs_p=torch.full((B_p,), S_p, dtype=torch.int32, device='cuda'),
                cs_d=torch.full((B_d,), S_kv, dtype=torch.int32, device='cuda'))

def pod_call(d, fp):
    return lambda: pod_attn.true_fused_attn_with_kvcache(
        d['q_p'], d['k_p'], d['v_p'], d['q_d'], d['k_d'], d['v_d'],
        cache_seqlens_p=d['cs_p'], cache_seqlens_d=d['cs_d'],
        causal=True, fused_params=fp)

def fa_prefill(d):
    return lambda: pod_attn.flash_attn_with_kvcache(d['q_p'], d['k_p'], d['v_p'],
                                                    cache_seqlens=d['cs_p'], causal=True)
def fa_decode(d):
    return lambda: pod_attn.flash_attn_with_kvcache(d['q_d'], d['k_d'], d['v_d'],
                                                    cache_seqlens=d['cs_d'], causal=False)

# 每个 wall 一组形状 (B_p, S_p, B_d, S_kv)
WALLS = {
  'W_pref':  (2, 4096,  1,  512),   # prefill 主导
  'W_dec' :  (1,  128, 64, 8192),   # decode 主导
  'W_mix' :  (1, 2048, 16, 4096),   # 混合批 = POD 的目标场景
}
KERNELS = {'pod': pod_call, 'fa_p': lambda d,_: fa_prefill(d), 'fa_d': lambda d,_: fa_decode(d)}

ap = argparse.ArgumentParser()
ap.add_argument('--wall', default=None, choices=list(WALLS))
ap.add_argument('--kernel', default='pod', choices=list(KERNELS))
ap.add_argument('--fp', type=int, default=15)
ap.add_argument('--prof', action='store_true')
a = ap.parse_args()

def timeit(fn, warm=5, rep=20):
    for _ in range(warm): fn()
    torch.cuda.synchronize(); t0=time.perf_counter()
    for _ in range(rep): fn()
    torch.cuda.synchronize(); return (time.perf_counter()-t0)/rep*1000

names = [a.wall] if a.wall else list(WALLS)
if not a.prof: print(f"{'wall':<9}{'形状(B_p,S_p,B_d,S_kv)':<26}{'kernel':<7}{'ms':>9}")
for w in names:
    B_p,S_p,B_d,S_kv = WALLS[w]
    d = mk(B_p,S_p,B_d,S_kv)
    fn = KERNELS[a.kernel](d, a.fp)
    if a.prof:
        fn(); torch.cuda.synchronize(); fn(); torch.cuda.synchronize()
        print(f"{w}/{a.kernel} profiled")
    else:
        print(f"{w:<9}{str((B_p,S_p,B_d,S_kv)):<26}{a.kernel:<7}{timeit(fn):>8.3f}")
    del d, fn; torch.cuda.empty_cache()

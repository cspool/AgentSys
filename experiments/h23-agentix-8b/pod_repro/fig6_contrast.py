"""POD 论文 Fig.6/Fig.11 的四配置对照 (sm_89 适配版)。

  FA_Serial : prefill 与 decode 串行两次 kernel 调用 (FlashAttention 基线)
  FA_Streams: 两条 CUDA stream 各跑一个, 靠流并发
  FA_HFuse  : HFuse 融合 (fused_params=64) —— POD 论文的对照融合方法
  POD       : SM-aware CTA 调度 (fused_params=15/8/9/10/11 取最优)

口径: 混合批(一个 prefill 请求 + 一批 decode 请求)的端到端 kernel 时间。
"""
import argparse, json, statistics, time, torch, pod_attn

ap = argparse.ArgumentParser()
ap.add_argument('--reps', type=int, default=50)
ap.add_argument('--warm', type=int, default=10)
ap.add_argument('--out', default='FIG6.json')
a = ap.parse_args()

def mk(B_p,S_p,B_d,S_kv,H=32,Hkv=4,D=128):
    g=torch.Generator(device='cuda').manual_seed(7)
    t=lambda *s: torch.randn(*s, device='cuda', dtype=torch.float16, generator=g)
    return dict(q_p=t(B_p,S_p,H,D),k_p=t(B_p,S_p,Hkv,D),v_p=t(B_p,S_p,Hkv,D),
                q_d=t(B_d,1,H,D),  k_d=t(B_d,S_kv,Hkv,D),v_d=t(B_d,S_kv,Hkv,D),
                cs_p=torch.full((B_p,),S_p,dtype=torch.int32,device='cuda'),
                cs_d=torch.full((B_d,),S_kv,dtype=torch.int32,device='cuda'))

def t_ms(fn, warm, reps):
    for _ in range(warm): fn()
    torch.cuda.synchronize()
    ts=[]
    for _ in range(reps):
        torch.cuda.synchronize(); t0=time.perf_counter(); fn(); torch.cuda.synchronize()
        ts.append((time.perf_counter()-t0)*1000)
    return statistics.median(ts)

s1, s2 = torch.cuda.Stream(), torch.cuda.Stream()

def arms(d):
    fa_p = lambda: pod_attn.flash_attn_with_kvcache(d['q_p'],d['k_p'],d['v_p'],cache_seqlens=d['cs_p'],causal=True)
    fa_d = lambda: pod_attn.flash_attn_with_kvcache(d['q_d'],d['k_d'],d['v_d'],cache_seqlens=d['cs_d'],causal=False)
    def serial():
        fa_p(); fa_d()
    def streams():
        ev = torch.cuda.Event()
        with torch.cuda.stream(s1): fa_p()
        with torch.cuda.stream(s2): fa_d()
        torch.cuda.current_stream().wait_stream(s1); torch.cuda.current_stream().wait_stream(s2)
    def fused(fp):
        return lambda: pod_attn.true_fused_attn_with_kvcache(
            d['q_p'],d['k_p'],d['v_p'],d['q_d'],d['k_d'],d['v_d'],
            cache_seqlens_p=d['cs_p'],cache_seqlens_d=d['cs_d'],causal=True,fused_params=fp)
    return serial, streams, fused

SHAPES = [
    ("chunk512_d16x4k",  1, 512,  16, 4096),
    ("chunk1k_d32x4k",   1, 1024, 32, 4096),
    ("chunk2k_d16x8k",   1, 2048, 16, 8192),
    ("chunk512_d64x2k",  1, 512,  64, 2048),
    # POD 的设计区间: 大 prefill chunk 与大量 decode 同批, 两者都吃满
    ("chunk2k_d32x8k",   1, 2048, 32, 8192),
    ("chunk4k_d16x8k",   1, 4096, 16, 8192),
    ("chunk4k_d32x4k",   1, 4096, 32, 4096),
    ("chunk1k_d64x8k",   1, 1024, 64, 8192),
]
POD_FPS = [15, 8, 9, 10, 11]
res = {}
print(f"{'形状':<18}{'FA_Serial':>11}{'FA_Streams':>11}{'FA_HFuse':>10}{'POD':>9}{'POD最优fp':>10}{'POD/Serial':>11}{'POD/HFuse':>10}")
for name,B_p,S_p,B_d,S_kv in SHAPES:
    d = mk(B_p,S_p,B_d,S_kv)
    serial, streams, fused = arms(d)
    r = {}
    r['FA_Serial']  = t_ms(serial, a.warm, a.reps)
    r['FA_Streams'] = t_ms(streams, a.warm, a.reps)
    try: r['FA_HFuse'] = t_ms(fused(64), a.warm, a.reps)
    except Exception as e: r['FA_HFuse'] = None; r['hfuse_err']=str(e)[:80]
    best=(None,1e9)
    for fp in POD_FPS:
        try:
            v=t_ms(fused(fp), a.warm, a.reps)
            r[f'POD_fp{fp}']=v
            if v<best[1]: best=(fp,v)
        except Exception as e: r[f'POD_fp{fp}']=None
    r['POD']=best[1] if best[0] else None; r['POD_best_fp']=best[0]
    res[name]=r
    f=lambda x: f"{x:>10.4f}" if isinstance(x,float) else f"{'—':>10}"
    print(f"{name:<18}{r['FA_Serial']:>11.4f}{r['FA_Streams']:>11.4f}"
          f"{f(r['FA_HFuse'])}{f(r['POD'])}{str(r['POD_best_fp']):>10}"
          f"{r['FA_Serial']/r['POD']:>11.3f}{(r['FA_HFuse']/r['POD'] if r['FA_HFuse'] else 0):>10.3f}")
    del d; torch.cuda.empty_cache()
json.dump(res, open(a.out,'w'), ensure_ascii=False, indent=1)
print(f"\n-> {a.out}")

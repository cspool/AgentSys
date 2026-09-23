"""POD sm_89 适配的三项验证 (方案 D: 锁死 kBlockM 与 warps=4, 只砍 kBlockN)

V1 硬证伪指标: 实际派发的 true_fused_tb_fwd_kernel 的 launch__occupancy_limit_shared_mem 必须 >= 2
              报 1 即适配无效。墙钟加速比**不是**有效证伪器 —— 即使 1 CTA/SM, 融合本身也省掉
              一次 launch 和一段 wave 尾巴, 照样"提速"。
V2 正确性闸门: DecodeSplit=true 且 ngroups>=4 时与 flash_attn 参考实现逐元素比对
              (把 Warps_d 降到 1 的方案会在此静默失败 —— oaccum 线程布局硬编码 128 线程)
V3 机制验证 : 证明同一 SM 上真有 prefill 与 decode 共驻, 而不只是"能跑"
"""
import argparse, json, sys, torch
import pod_attn

ap = argparse.ArgumentParser()
ap.add_argument('--mode', default='all', choices=['all', 'v2', 'shapes'])
ap.add_argument('--fp', type=int, default=15)
a = ap.parse_args()

dt = torch.float16
def mk(B_p, S_p, B_d, S_kv, H=32, Hkv=8, D=128):
    g = torch.Generator(device='cuda').manual_seed(1234)
    t = lambda *s: torch.randn(*s, device='cuda', dtype=dt, generator=g)
    return dict(
        q_p=t(B_p,S_p,H,D), k_p=t(B_p,S_p,Hkv,D), v_p=t(B_p,S_p,Hkv,D),
        q_d=t(B_d,1,H,D),   k_d=t(B_d,S_kv,Hkv,D), v_d=t(B_d,S_kv,Hkv,D),
        cs_p=torch.full((B_p,), S_p, dtype=torch.int32, device='cuda'),
        cs_d=torch.full((B_d,), S_kv, dtype=torch.int32, device='cuda'))

# ---- V2: 正确性 ----
def v2(cfgname, B_p, S_p, B_d, S_kv, H, Hkv, fps):
    d = mk(B_p, S_p, B_d, S_kv, H, Hkv)
    ref_p = pod_attn.flash_attn_with_kvcache(d['q_p'], d['k_p'], d['v_p'],
                                            cache_seqlens=d['cs_p'], causal=True)
    ref_d = pod_attn.flash_attn_with_kvcache(d['q_d'], d['k_d'], d['v_d'],
                                            cache_seqlens=d['cs_d'], causal=False)
    torch.cuda.synchronize()
    print(f"  [{cfgname}] B_p={B_p} S_p={S_p} B_d={B_d} S_kv={S_kv} H={H} Hkv={Hkv} ngroups={H//Hkv}")
    for fp in fps:
        try:
            op, od = pod_attn.true_fused_attn_with_kvcache(
                d['q_p'], d['k_p'], d['v_p'], d['q_d'], d['k_d'], d['v_d'],
                cache_seqlens_p=d['cs_p'], cache_seqlens_d=d['cs_d'],
                causal=True, fused_params=fp)
            torch.cuda.synchronize()
            ep = (op.float()-ref_p.float()).abs().max().item()
            ed = (od.float()-ref_d.float()).abs().max().item()
            nan = bool(torch.isnan(op).any() or torch.isnan(od).any())
            ok = (ep < 2e-2 and ed < 2e-2 and not nan)
            print(f"     fp={fp:<3} maxΔ prefill={ep:.5f} decode={ed:.5f} nan={nan}  {'PASS' if ok else 'FAIL'}")
        except Exception as e:
            print(f"     fp={fp:<3} EXCEPTION {type(e).__name__}: {str(e)[:110]}")

if a.mode in ('all','v2'):
    print("=== V2 正确性闸门 (与 flash_attn 参考实现比对) ===")
    FPS = [15, 8, 9, 10, 11, 64]
    # DecodeSplit 由 batch*heads*mblocks 与 SM 数的关系决定; 小 B_d + 长 KV 更容易触发 split
    v2("小batch长KV(易触发 DecodeSplit)", 1, 1024,  4, 8192, 32, 8, FPS)
    v2("论文典型(Yi-6B 形状)",            1,  512, 16, 4096, 32, 4, FPS)
    v2("大batch短KV",                     2,  256, 32, 1024, 32, 8, FPS)
    v2("MQA ngroups=32",                  1,  512,  8, 4096, 32, 1, FPS)
    # 4CTA 路径(decode 不 split): 大 decode batch + 短 KV, 走 P(64,16,2)+D(16,16,1)=24KB
    v2("4CTA路径 B_d=128 KV=1024",         1,  512,128, 1024, 32, 4, FPS)
    v2("4CTA路径 B_d=256 KV=512",          1,  512,256,  512, 32, 4, FPS)

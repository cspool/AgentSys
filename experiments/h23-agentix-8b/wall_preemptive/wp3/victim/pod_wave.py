"""受害者: POD 融合 kernel 的方波负载 (真实论文实现, 非合成 kernel)。

墙型由 POD 自身的批组成决定, 每 phase_ms 在两档之间切换:
  phase 1 (TC 相)  : prefill 重 —— 大 chunk, 少 decode  => 算力/TC 主导
  phase 0 (DRAM 相): decode 重 —— 小 chunk, 大 batch 长 KV => 访存主导
相位通过 PhaseBeacon 发布给抢占者, 并记录每次迭代的墙钟用于算 G_v。
全程连续发射, 不 sleep。
"""
import argparse, json, sys, time, torch, pod_attn
sys.path.insert(0, '/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3')
from common.beacon import PhaseBeacon, mono_ns

ap = argparse.ArgumentParser()
ap.add_argument('--secs', type=float, default=120)
ap.add_argument('--phase-ms', type=int, default=600)
ap.add_argument('--fp', type=int, default=15)
# 不同的真实并发机制(全部来自 POD 论文的实现与对照)
#   serial  : FA-2 prefill 与 decode 串行两次 kernel —— 无 kernel 内并发
#   streams : 两条 CUDA stream —— 流级并发(L3 channel 层)
#   hfuse   : fp=64, HFuse 把两 kernel 合进同一 CTA 用 warp 分区 —— CTA 内并发
#   pod2    : fp=9,  SM-aware CTA 调度, 每 SM 2 个 CTA
#   pod4    : fp=11, SM-aware CTA 调度, 每 SM 4 个 CTA
#   greenctx: TPC 动态 resize —— Bullet/green-context 的真正机制。prefill 与 decode 各占一组
#             互不重叠的 TPC, 且**每次相位切换时按两侧当前负载重新划分配额**(对应 Bullet 的
#             set_adaptive_num_tpcs)。用 libsmctrl 给两条 stream 打互补 mask, 不依赖 Bullet 服务端。
#   gcstatic: 同上但配额固定 50/50, 作为 resize 的对照(论文主张 resize 优于静态切分)
ap.add_argument('--mech', default='pod', choices=['pod','serial','streams','hfuse','pod2','pod4','greenctx','gcstatic'])
ap.add_argument('--beacon', default='/tmp/wp3_phase')
ap.add_argument('--single-phase', type=int, default=-1, help='>=0 时固定在该相位(用于墙型画像/门禁)')
ap.add_argument('--wave', default='01', help='方波在哪两个相位间交替, 如 01=TC/DRAM 互比, 02=TC墙/全饱和, 12=DRAM墙/全饱和')
ap.add_argument('--gc-split', type=int, default=32, help='gcstatic: 固定切分点')
ap.add_argument('--gc-min-tpc', type=int, default=4, help='resize 时任一侧的 TPC 下限(保证两侧都不饿死)')
ap.add_argument('--suspend-gate', default=None, help='挂起门文件; 门=1 时受害者真正停止发射并等待恢复')
ap.add_argument('--out', required=True)
a = ap.parse_args()

dev = torch.device('cuda'); torch.zeros(1, device=dev)
def mk(B_p,S_p,B_d,S_kv,H=32,Hkv=4,D=128):
    g=torch.Generator(device='cuda').manual_seed(7)
    t=lambda *s: torch.randn(*s, device='cuda', dtype=torch.float16, generator=g)
    return dict(q_p=t(B_p,S_p,H,D),k_p=t(B_p,S_p,Hkv,D),v_p=t(B_p,S_p,Hkv,D),
                q_d=t(B_d,1,H,D),  k_d=t(B_d,S_kv,Hkv,D),v_d=t(B_d,S_kv,Hkv,D),
                cs_p=torch.full((B_p,),S_p,dtype=torch.int32,device='cuda'),
                cs_d=torch.full((B_d,),S_kv,dtype=torch.int32,device='cuda'))

# 两档墙型 (来自 POD 自身负载, 已在 fig6 对照中验证可跑)
# 计划文档第5层要求受害者三态齐备: 算力墙 / 访存墙 / **全饱和**(命题的对照臂, 无空闲维)。
# 全饱和 = 大 prefill + 大 decode 同批: TC 与 DRAM 双高(POD 的目标场景本身)。
WALLS = {1: ("TC相_prefill重",  (1, 4096, 4,  2048)),
         0: ("DRAM相_decode重", (1, 256,  64, 8192)),
         2: ("全饱和_双高",      (1, 4096, 64, 8192)),
         3: ("工具期_空闲W0",     None)}   # agent 等 tool_use: KV 驻留但零 GPU 产出
D = {k: mk(*v[1]) for k, v in WALLS.items() if v[1] is not None}

_FP = {'pod': a.fp, 'hfuse': 64, 'pod2': 9, 'pod4': 11}
_s1, _s2 = torch.cuda.Stream(), torch.cuda.Stream()
_gc = None; _gc_log = []
if a.mech in ('greenctx', 'gcstatic'):
    import sys as _sys
    _sys.path.insert(0, '/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3')
    from common.smctrl import SmCtrl
    _gc = SmCtrl(0)
    _gc.set_stream(_s1, 0, a.gc_split)                  # prefill 侧 TPC
    _gc.set_stream(_s2, a.gc_split, _gc.total_tpcs)     # decode 侧 TPC, 与上面互不重叠

def _gc_resize(ph):
    """按该相位两侧的实际工作量(以 CTA block 数计)重划 TPC 配额。
    prefill_blocks = ceil(S_p/kBlockM_p) * B_p * H ;  decode_blocks = B_d * H
    这是 Bullet set_adaptive_num_tpcs 的同构简化: 配额正比于待办工作量, 两侧各留下限。"""
    if _gc is None or a.mech != 'greenctx': return None
    if WALLS[ph][1] is None: return None
    B_p, S_p, B_d, S_kv = WALLS[ph][1]
    H = 32; BM_P = 128
    wp = -(-S_p // BM_P) * B_p * H
    wd = B_d * H
    T = _gc.total_tpcs
    n_p = int(round(T * wp / float(wp + wd)))
    n_p = max(a.gc_min_tpc, min(T - a.gc_min_tpc, n_p))
    _gc.set_stream(_s1, 0, n_p)
    _gc.set_stream(_s2, n_p, T)
    _gc_log.append((ph, n_p, T - n_p, wp, wd))
    return n_p
def call(ph):
    d = D[ph]
    if a.mech == 'serial':
        pod_attn.flash_attn_with_kvcache(d['q_p'],d['k_p'],d['v_p'],cache_seqlens=d['cs_p'],causal=True)
        return pod_attn.flash_attn_with_kvcache(d['q_d'],d['k_d'],d['v_d'],cache_seqlens=d['cs_d'],causal=False)
    if a.mech in ('streams', 'greenctx', 'gcstatic'):
        with torch.cuda.stream(_s1):
            pod_attn.flash_attn_with_kvcache(d['q_p'],d['k_p'],d['v_p'],cache_seqlens=d['cs_p'],causal=True)
        with torch.cuda.stream(_s2):
            pod_attn.flash_attn_with_kvcache(d['q_d'],d['k_d'],d['v_d'],cache_seqlens=d['cs_d'],causal=False)
        torch.cuda.current_stream().wait_stream(_s1); torch.cuda.current_stream().wait_stream(_s2)
        return None
    return pod_attn.true_fused_attn_with_kvcache(
        d['q_p'],d['k_p'],d['v_p'],d['q_d'],d['k_d'],d['v_d'],
        cache_seqlens_p=d['cs_p'],cache_seqlens_d=d['cs_d'],causal=True,fused_params=_FP[a.mech])

for ph in [k for k in WALLS if WALLS[k][1] is not None]:   # 预热各计算档
    for _ in range(20): call(ph)
torch.cuda.synchronize()

bc = PhaseBeacon(a.beacon, create=True)
_gate = None
if a.suspend_gate:
    from common.gate import SuspendGate
    _gate = SuspendGate(a.suspend_gate, create=True)
_susp_total = 0.0; _n_susp = 0
_gc_resize(a.single_phase if a.single_phase is not None and a.single_phase>=0 else 0)
fixed = a.single_phase if a.single_phase >= 0 else None
_wave = [int(c) for c in a.wave]
assert len(_wave)==2 and all(w in WALLS for w in _wave)
ph = fixed if fixed is not None else _wave[0]
assert fixed is None or fixed in WALLS
bc.publish(ph)
t0 = time.perf_counter(); deadline = t0 + a.secs
iters = {k: [] for k in WALLS}; n_switch = 0; last_sw = t0
while True:
    now = time.perf_counter()
    if now >= deadline: break
    if fixed is None and (now - last_sw) * 1000 >= a.phase_ms:
        ph = _wave[1] if ph == _wave[0] else _wave[0]; _gc_resize(ph); bc.publish(ph); n_switch += 1; last_sw = now
    if _gate is not None and _gate.suspended():
        # 经典抢占语义: 停止发射, 等待恢复令。相位钟按墙钟继续走(调度器视角)。
        _n_susp += 1; su0 = time.perf_counter()
        while _gate.suspended() and time.perf_counter() < deadline:
            time.sleep(0.0002)
            now2 = time.perf_counter()
            if fixed is None and (now2 - last_sw) * 1000 >= a.phase_ms:
                ph = _wave[1] if ph == _wave[0] else _wave[0]; _gc_resize(ph); bc.publish(ph)
                n_switch += 1; last_sw = now2
        _susp_total += time.perf_counter() - su0
        continue
    if WALLS[ph][1] is None:          # 工具期: 零发射, KV 仍驻留
        time.sleep(0.0005); continue
    s = time.perf_counter(); call(ph); torch.cuda.synchronize()
    iters[ph].append((s - t0, (time.perf_counter() - s) * 1000))
dur = time.perf_counter() - t0
bc.close()
res = dict(secs=round(dur,3), mech=a.mech, suspended_s=round(_susp_total,3), n_suspends=_n_susp, gc_resizes=len(_gc_log), gc_alloc=_gc_log[:6], fp=a.fp, phase_ms=a.phase_ms, n_switch=n_switch,
           single_phase=fixed, walls={str(k): v[0] for k, v in WALLS.items()},
           shapes={str(k): v[1] for k, v in WALLS.items()},
           n_iter={str(k): len(v) for k, v in iters.items()},
           iters={str(k): v for k, v in iters.items()})
import statistics
summ = {k: (round(statistics.median(x[1] for x in v),4) if v else None) for k,v in iters.items()}
res['median_ms'] = {str(k): v for k,v in summ.items()}
res['throughput_iter_per_s'] = round(sum(len(v) for v in iters.values())/dur, 2)
print(json.dumps({k:v for k,v in res.items() if k!='iters'}, ensure_ascii=False))
json.dump(res, open(a.out,'w'), ensure_ascii=False)

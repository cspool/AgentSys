#!/usr/bin/env bash
# L2 墙候选: POD decode 相位, KV 总量压进 72MB L2 => 流读全命中 L2, DRAM 应大幅回落。
# 口径: L2 >= 80% 且为主轴, 副轴(TC/DRAM) 30-60% => L2 墙成立。
# 注意: NCU 不支持 MPS, 必须在无 MPS 环境跑; --cache-control none 保留 L2 常驻。
set -u
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
export CUDA_VISIBLE_DEVICES=${GPU:-0}; unset CUDA_MPS_PIPE_DIRECTORY
VP=/data3/docker_cache/AgentSys/envs/pod_attn/bin/python
M="lts__t_sectors.avg.pct_of_peak_sustained_elapsed,\
dram__throughput.avg.pct_of_peak_sustained_elapsed,\
sm__pipe_tensor_op_hmma_cycles_active.avg.pct_of_peak_sustained_active,\
l1tex__t_sectors.avg.pct_of_peak_sustained_elapsed,\
sm__pipe_fma_cycles_active.avg.pct_of_peak_sustained_active"
# 三个 KV 档: 33MB(稳进 L2) / 67MB(贴着 72MB) / 268MB(对照, 必穿透 DRAM)
declare -A CFG=( [kv33MB]="1 256 8 2048" [kv67MB]="1 256 16 2048" [kv268MB]="1 256 64 8192" )
for tag in kv33MB kv67MB kv268MB; do
  set -- ${CFG[$tag]}
  cat > /tmp/l2probe.py <<PYEOF
import torch, pod_attn
B_p,S_p,B_d,S_kv = $1,$2,$3,$4
H,Hkv,D=32,4,128
g=torch.Generator(device='cuda').manual_seed(7)
t=lambda *s: torch.randn(*s, device='cuda', dtype=torch.float16, generator=g)
q_p,k_p,v_p=t(B_p,S_p,H,D),t(B_p,S_p,Hkv,D),t(B_p,S_p,Hkv,D)
q_d,k_d,v_d=t(B_d,1,H,D),t(B_d,S_kv,Hkv,D),t(B_d,S_kv,Hkv,D)
cs_p=torch.full((B_p,),S_p,dtype=torch.int32,device='cuda'); cs_d=torch.full((B_d,),S_kv,dtype=torch.int32,device='cuda')
kv_mb = 2*B_d*S_kv*Hkv*D*2/1e6
print(f"KV total = {kv_mb:.0f} MB")
for _ in range(30):   # 预热并让 KV 驻留 L2
    pod_attn.true_fused_attn_with_kvcache(q_p,k_p,v_p,q_d,k_d,v_d,cache_seqlens_p=cs_p,cache_seqlens_d=cs_d,causal=True,fused_params=15)
torch.cuda.synchronize()
PYEOF
  timeout 400 ncu --csv --cache-control none --kernel-name regex:true_fused_tb_fwd_kernel \
    --launch-skip 24 --launch-count 4 --metrics "$M" $VP /tmp/l2probe.py > /tmp/l2_${tag}.csv 2>&1
  echo "$tag rc=$?"
done
python3 - <<'PY'
import csv, statistics
S={'lts__t_sectors.avg.pct_of_peak_sustained_elapsed':'L2',
   'dram__throughput.avg.pct_of_peak_sustained_elapsed':'DRAM',
   'sm__pipe_tensor_op_hmma_cycles_active.avg.pct_of_peak_sustained_active':'TC',
   'l1tex__t_sectors.avg.pct_of_peak_sustained_elapsed':'L1',
   'sm__pipe_fma_cycles_active.avg.pct_of_peak_sustained_active':'FMA'}
print(f"{'档':<10}{'L2':>7}{'DRAM':>7}{'TC':>6}{'TC/峰':>7}{'L1':>6}{'FMA':>6}   判定")
for tag in ['kv33MB','kv67MB','kv268MB']:
    L=open(f'/tmp/l2_{tag}.csv',errors='ignore').read().splitlines()
    h=next((i for i,l in enumerate(L) if l.startswith('"ID"')), None)
    if h is None: print(f"{tag:<10}  无输出"); continue
    agg={}
    for r in csv.DictReader(L[h:]):
        k=S.get(r['Metric Name'])
        if k:
            try: agg.setdefault(k,[]).append(float(r['Metric Value'].replace(',','')))
            except ValueError: pass
    v={k:statistics.mean(x) for k,x in agg.items()}
    tcn=v.get('TC',0)/49.0*100
    l2=v.get('L2',0); dr=v.get('DRAM',0)
    # v3 口径: 差值 >=30pp 即疑似墙(算墙); 加主轴 >=80% 为严格墙
    second = max(dr, tcn)
    gap = l2 - second
    verdict = ("严格 L2 墙" if (gap>=30 and l2>=80) else
               "疑似 L2 墙" if gap>=30 else
               f"非墙(差值 {gap:.0f}pp <30)")
    print(f"{tag:<10}{l2:>7.1f}{dr:>7.1f}{v.get('TC',0):>6.1f}{tcn:>7.1f}{v.get('L1',0):>6.1f}{v.get('FMA',0):>6.1f}   {verdict}")
PY
echo L2PROBE_DONE

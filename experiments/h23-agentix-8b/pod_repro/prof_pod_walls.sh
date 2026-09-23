#!/usr/bin/env bash
# 用 NCU 给 POD 真实负载组成的 wall 做资源画像 — GPU1
# 验收标准(用户口径): 目标轴 >=80% 或达该轴可达峰值, 其余各轴 30-60%; 副轴 <20% 则该 wall 不成立。
# 4090 上 TC 的可达峰值实测 = 49% (fp16 输入 + fp32 累加走半速), 故 TC 轴以 49% 为 100%。
set -u
cd "$(dirname "$0")"
PY=/data3/docker_cache/AgentSys/envs/pod_attn/bin/python
export CUDA_VISIBLE_DEVICES=1
M="sm__pipe_tensor_op_hmma_cycles_active.avg.pct_of_peak_sustained_active,\
sm__pipe_fma_cycles_active.avg.pct_of_peak_sustained_active,\
dram__throughput.avg.pct_of_peak_sustained_elapsed,\
lts__t_sectors.avg.pct_of_peak_sustained_elapsed,\
l1tex__t_sectors.avg.pct_of_peak_sustained_elapsed,\
smsp__inst_executed.avg.pct_of_peak_sustained_active"
# --cache-control none: 默认的 all 会在每次 replay 前刷 L2, 让 L2 常驻负载假报高 DRAM
for W in W_pref W_dec W_mix; do
  for K in pod fa_p fa_d; do
    ncu --csv --cache-control none --kernel-name regex:'(fused|flash)' --launch-count 4 \
        --metrics "$M" $PY pod_walls.py --wall $W --kernel $K --prof > /tmp/pw_${W}_${K}.csv 2>&1
  done
done
$PY - <<'PYX'
import csv, glob, os, json, statistics
TC_PEAK = 49.0   # 4090 实测可达峰值
SHORT = {'sm__pipe_tensor_op_hmma_cycles_active.avg.pct_of_peak_sustained_active':'TC',
         'sm__pipe_fma_cycles_active.avg.pct_of_peak_sustained_active':'FMA',
         'dram__throughput.avg.pct_of_peak_sustained_elapsed':'DRAM',
         'lts__t_sectors.avg.pct_of_peak_sustained_elapsed':'L2',
         'l1tex__t_sectors.avg.pct_of_peak_sustained_elapsed':'L1',
         'smsp__inst_executed.avg.pct_of_peak_sustained_active':'INST'}
out={}
print(f"{'wall/kernel':<18}{'TC':>7}{'TC/峰':>7}{'FMA':>7}{'DRAM':>7}{'L2':>7}{'L1':>7}{'INST':>7}   判定")
for f in sorted(glob.glob('/tmp/pw_*.csv')):
    tag=os.path.basename(f)[3:-4]
    lines=open(f).read().splitlines()
    h=next((i for i,l in enumerate(lines) if l.startswith('"ID"')), None)
    if h is None: print(f"{tag:<18}  无 NCU 输出"); continue
    agg={}
    for r in csv.DictReader(lines[h:]):
        s=SHORT.get(r['Metric Name'])
        if s:
            try: agg.setdefault(s,[]).append(float(r['Metric Value'].replace(',','')))
            except ValueError: pass
    if not agg: print(f"{tag:<18}  无匹配指标"); continue
    v={k:statistics.mean(x) for k,x in agg.items()}
    tcn = v.get('TC',0)/TC_PEAK*100
    axes={'TC':tcn,'FMA':v.get('FMA',0),'DRAM':v.get('DRAM',0),'L2':v.get('L2',0),'L1':v.get('L1',0)}
    top=max(axes,key=axes.get); side=[a for a in axes if a!=top]
    ok = axes[top]>=80 and all(axes[a]>=20 for a in side if axes[a]==max(axes[s] for s in side))
    verdict = f"{top} 墙" if axes[top]>=80 else f"无墙(最高{top}={axes[top]:.0f}%)"
    print(f"{tag:<18}{v.get('TC',0):>7.1f}{tcn:>7.1f}{v.get('FMA',0):>7.1f}{v.get('DRAM',0):>7.1f}"
          f"{v.get('L2',0):>7.1f}{v.get('L1',0):>7.1f}{v.get('INST',0):>7.1f}   {verdict}")
    out[tag]={**v,'TC_norm':tcn,'top':top,'verdict':verdict}
json.dump(out, open('POD_WALLS.json','w'), indent=1, ensure_ascii=False)
print("\n-> POD_WALLS.json")
PYX

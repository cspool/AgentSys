#!/usr/bin/env bash
set -u
cd "$(dirname "$0")"
export CUDA_VISIBLE_DEVICES=0
PY=/data3/docker_cache/AgentSys/envs/pod_attn/bin/python
echo "########## V2: 正确性闸门 ##########"
$PY verify_ada.py --mode v2 2>&1 | tail -40
echo
echo "########## V1: 占用率硬证伪指标 ##########"
M="launch__occupancy_limit_shared_mem,launch__occupancy_limit_warps,launch__shared_mem_per_block_dynamic,launch__block_size,launch__grid_size"
ncu --csv --kernel-name regex:true_fused --launch-count 3 --metrics "$M" \
    $PY verify_ada.py --mode v2 > /tmp/v1.csv 2>&1
$PY - <<'PYX'
import csv
lines=open('/tmp/v1.csv').read().splitlines()
h=next((i for i,l in enumerate(lines) if l.startswith('"ID"')), None)
if h is None: print("  无 NCU 输出 (kernel 名未匹配?)"); raise SystemExit
rows=list(csv.DictReader(lines[h:]))
seen=set()
for r in rows:
    key=(r['Kernel Name'][:40], r['Metric Name'])
    if r['Metric Name']=='launch__occupancy_limit_shared_mem':
        v=float(r['Metric Value'])
        print(f"  occupancy_limit_shared_mem = {v:.0f}  -> {'PASS 1P+1D 可共驻' if v>=2 else 'FAIL 仍只 1 CTA/SM, 适配无效'}")
    elif r['Metric Name'] in ('launch__shared_mem_per_block_dynamic','launch__block_size','launch__occupancy_limit_warps'):
        if key not in seen:
            seen.add(key); print(f"  {r['Metric Name']:<42} {r['Metric Value']}")
PYX

echo
echo "########## V3: 共驻机制验证 (无需改 POD 源码) ##########"
# 思路: fused kernel 的 block=128(4 warp)。若实测每 SM 活跃 warp 明显 >4,
#       则该 SM 上同时驻留 >=2 个 CTA; POD 的 ticket 轮转决定角色, 故共驻的即 P 与 D。
#       Ada 每 SM 峰值 48 warp -> 4 warp = 8.33%。
M3="sm__warps_active.avg.pct_of_peak_sustained_active,launch__block_size,launch__grid_size,sm__ctas_launched.sum"
ncu --csv --cache-control none --kernel-name regex:true_fused --launch-count 3 --metrics "$M3" \
    $PY verify_ada.py --mode v2 > /tmp/v3.csv 2>&1
$PY - <<'PYX'
import csv
lines=open('/tmp/v3.csv').read().splitlines()
h=next((i for i,l in enumerate(lines) if l.startswith('"ID"')), None)
if h is None:
    print("  无 NCU 输出"); raise SystemExit
rows=list(csv.DictReader(lines[h:]))
by={}
for r in rows:
    by.setdefault(r['ID'], {})[r['Metric Name']] = r['Metric Value']
for i,(lid,m) in enumerate(by.items()):
    try:
        pct=float(m['sm__warps_active.avg.pct_of_peak_sustained_active'].replace(',',''))
        blk=float(m['launch__block_size'].replace(',',''))
    except (KeyError, ValueError):
        continue
    warps_sm = pct/100*48          # Ada 每 SM 峰值 48 warp
    ctas_sm  = warps_sm/(blk/32)
    print(f"  launch{lid}: block={blk:.0f}  活跃 warp/SM={warps_sm:.2f}  -> CTA/SM={ctas_sm:.2f}  "
          f"{'PASS 共驻(>1 CTA/SM)' if ctas_sm>1.3 else 'FAIL 实测未共驻'}")
PYX

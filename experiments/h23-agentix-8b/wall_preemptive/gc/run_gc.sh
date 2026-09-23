#!/usr/bin/env bash
# green-context 基底下的三臂严格对照 + 基底对照
# 负载/burst工作量/到达序列/K 与 MPS 严格长跑 (S12) 逐字相同, 只换空间共享基底
set -u
cd "$(dirname "$0")"
PFX=${PFX:-G12}
K=${K:-300}
PERIOD=${PERIOD:-1.5}
CYC=${CYC:-1500}
P=${P:-32}
export CUDA_VISIBLE_DEVICES=0
COMMON="--substrate split --sm-preemptor $P --k $K --period $PERIOD --cycles $CYC --pattern w,s --prefix $PFX"

echo "=== $PFX: substrate=green_split P=${P}SM K=$K period=$PERIOD ==="
for M in valve wall_aware; do
  echo "--- $M ---"
  python3 wp_gc.py --mode $M $COMMON || exit 1
done
echo "--- random_defer (重放 wall_aware 的推迟预算, 打乱顺序) ---"
python3 wp_gc.py --mode random_defer $COMMON --delay-file ${PFX}_wall_aware_ctl.json || exit 1

echo
echo "=== 基底对照: substrate=none (同 context 两条流, 不分区) ==="
python3 wp_gc.py --mode valve --substrate none --k 40 --period "$PERIOD" \
  --cycles 200 --pattern w,s --prefix ${PFX}NONE || exit 1

echo
echo "=== 配对分析 ==="
python3 ../analyze_paired.py $PFX

#!/usr/bin/env bash
# 按需分区(resize)四臂: 负载/burst工作量/到达序列/K 与 S12(MPS) / G12(静态green) 逐字相同
set -u
cd "$(dirname "$0")"
PFX=${PFX:-R12}; K=${K:-300}; PERIOD=${PERIOD:-1.5}; CYC=${CYC:-1500}
export CUDA_VISIBLE_DEVICES=0
COMMON="--k $K --period $PERIOD --cycles $CYC --chunks 16 --sm-pre-sat 32 --sm-pre-wall 64 --pattern w,s --prefix $PFX"
echo "=== $PFX: substrate=resize(按需分区) K=$K period=$PERIOD ==="
for M in valve wall_aware wall_aware_resize; do
  echo "--- $M ---"; python3 wp_gc2.py --mode $M $COMMON || exit 1
done
echo "--- random_defer (重放 wall_aware 的推迟预算) ---"
python3 wp_gc2.py --mode random_defer $COMMON --delay-file ${PFX}_wall_aware_ctl.json || exit 1
echo; echo "=== 配对分析 ==="; python3 analyze_gc2.py $PFX

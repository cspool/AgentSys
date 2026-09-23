#!/usr/bin/env bash
# 抢占占空比扫描: 同一基底(按需分区)、同一负载, 只改到达率
# 目的: 量化 "系统收益 ≈ D 的压缩倍数 × 抢占占空比" 这条关系
set -u
cd "$(dirname "$0")"
export CUDA_VISIBLE_DEVICES=0
K=300
run() {  # $1=period $2=cycles $3=prefix
  local P=$1 C=$2 PFX=$3
  local COMMON="--k $K --period $P --cycles $C --chunks 16 --sm-pre-sat 32 --sm-pre-wall 64 --pattern w,s --prefix $PFX"
  echo "=== $PFX: period=${P}s cycles=$C ==="
  for M in valve wall_aware; do
    echo "--- $M ---"; python3 wp_gc2.py --mode $M $COMMON || exit 1
  done
  echo "--- random_defer ---"
  python3 wp_gc2.py --mode random_defer $COMMON --delay-file ${PFX}_wall_aware_ctl.json || exit 1
}
run 0.6 900 D06
run 0.3 500 D03
echo "=== 扫描完成 ==="

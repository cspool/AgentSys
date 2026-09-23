#!/usr/bin/env bash
# 并发干扰矩阵: 受害者相位 x 共跑者资源类型 x 并发比例 rho   (只用 GPU 0)
set -u
cd "$(dirname "$0")"
export CUDA_VISIBLE_DEVICES=0
SECS=${SECS:-30}
mkdir -p matrix
for V in memwall compwall saturated; do
  python3 interf_matrix.py --victim $V --co none --rho 0 --secs $SECS \
      --out matrix/${V}_none_0.00.json || exit 1
  for CO in fp32 l2 dram; do
    for R in 0.25 0.50 0.75 1.00; do
      python3 interf_matrix.py --victim $V --co $CO --rho $R --secs $SECS \
          --out matrix/${V}_${CO}_${R}.json || exit 1
    done
  done
done
echo "=== 矩阵完成 ==="

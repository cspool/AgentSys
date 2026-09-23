#!/usr/bin/env bash
# 真实负载 wall 抢占三臂对照 (GPU1)
# 受害者 = TC 墙(fp16 GEMM 6144^3, 2.83ms) <-> DRAM 访存墙(SDPA decode B=64 KV=16k, 4.58ms)
# 并发比例目标 rho~0.4: 每次抢占把共跑 kernel 连发到 ~40ms, 周期 0.1s
# 正交相位因共跑者而异: co=tc->dram, co=dram->tc, co=fp32->dram
set -u
cd "$(dirname "$0")"
export CUDA_VISIBLE_DEVICES=1
K=${K:-300}; P=${P:-0.1}
declare -A ORTH=( [tc]=dram [dram]=tc [fp32]=dram )
declare -A REPS=( [tc]=22   [dram]=6  [fp32]=17 )    # 单次 1.83/6.37/2.32ms -> ~40ms
for CO in tc dram fp32; do
  W=${ORTH[$CO]}; R=${REPS[$CO]}; PFX="R_${CO}"
  echo "===== 共跑者=$CO  正交相位=$W  co_reps=$R ====="
  for M in valve wall_aware; do
    echo "--- $M ---"
    python3 real_victim.py --walls tc_dram --co $CO --co-reps $R --wall-phase $W \
        --mode $M --k $K --period $P --prefix $PFX || exit 1
  done
  echo "--- random_defer ---"
  python3 real_victim.py --walls tc_dram --co $CO --co-reps $R --wall-phase $W \
      --mode random_defer --k $K --period $P --prefix $PFX \
      --delay-file ${PFX}_wall_aware_ctl.json || exit 1
done
echo "=== 真实负载 wall 抢占对照完成 ==="

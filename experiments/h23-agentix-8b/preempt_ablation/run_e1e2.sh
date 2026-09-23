#!/bin/bash
# E1: 单墙(算力/访存)vs 全饱和 —— 用户核心命题
# E2: block 寿命扫描(同为算力核)—— 机制判定 CILP vs CTA-drain vs WFI
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
RF=reps_v5.json
CYC=600
K=60

run_one () {  # tag  victim-args...
  tag=$1; shift
  echo "=== $tag ctrl ==="
  CUDA_VISIBLE_DEVICES=1 $PY victim5.py "$@" --cycles $CYC --reps-file $RF --out e_${tag}_ctrl.json
  for W in 1 4 12; do
    echo "=== $tag W=$W ==="
    CUDA_VISIBLE_DEVICES=1 $PY disturber3.py --work-ms $W --k $K --period 1.4 \
      --reps-file burst_reps_e.json --out e_${tag}_W${W}_log.json &
    DP=$!
    CUDA_VISIBLE_DEVICES=1 $PY victim5.py "$@" --cycles $CYC --reps-file $RF --out e_${tag}_W${W}.json
    wait $DP
  done
}

# ---- E1: 三种墙态 ----
run_one wallSM    --mode sm
run_one wallMEM   --mode dram
run_one balanced  --mode balanced --inner 50

# ---- E2: block 寿命扫描(算力核,footprint 极小,无访存混淆)----
run_one blk177 --mode sm --n 1048576  --chunks-per-block 8
run_one blk22  --mode sm --n 1048576  --chunks-per-block 1
run_one blk2p8 --mode sm --n 8388608  --chunks-per-block 1
run_one blk0p4 --mode sm --n 67108864 --chunks-per-block 1
echo "=== E1+E2 完成 ==="

#!/bin/bash
# D2: burst-size sweep per victim wall — 分离"每单位工作的切换税"与固定成本
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
RF=reps_v4_v1.json
declare -A CYC=( [dram]=390 [l2]=330 [sm]=360 )
for ph in dram l2 sm; do
  C=${CYC[$ph]}
  echo "=== $ph ctrl_a ==="
  CUDA_VISIBLE_DEVICES=0 $PY victim4.py --pattern $ph --cycles $C --reps-file $RF \
    --out sw_${ph}_ctrlA.json
  for W in 1 4 8 16; do
    echo "=== $ph W=${W}ms ==="
    CUDA_VISIBLE_DEVICES=0 $PY disturber3.py --work-ms $W --k 40 --period 1.4 \
      --out sw_${ph}_W${W}_log.json &
    DP=$!
    CUDA_VISIBLE_DEVICES=0 $PY victim4.py --pattern $ph --cycles $C --reps-file $RF \
      --out sw_${ph}_W${W}.json
    wait $DP
  done
  echo "=== $ph ctrl_b ==="
  CUDA_VISIBLE_DEVICES=0 $PY victim4.py --pattern $ph --cycles $C --reps-file $RF \
    --out sw_${ph}_ctrlB.json
done
echo "=== 扫描完成 ==="

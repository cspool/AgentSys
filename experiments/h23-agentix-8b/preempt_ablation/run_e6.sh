#!/bin/bash
# E6: 三资源轴(TC / FP32 / VRAM)—— 维度增加后的 W 放大
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
for cfg in "vramwall:0:0" "tcwall:0:32" "fp32wall:400:0" "triple:200:12"; do
  tag=$(echo $cfg | cut -d: -f1); inner=$(echo $cfg | cut -d: -f2); dots=$(echo $cfg | cut -d: -f3)
  echo "=== $tag(inner=$inner dots=$dots)ctrl ==="
  CUDA_VISIBLE_DEVICES=1 $PY victim7.py --inner $inner --dots $dots --cycles 600 \
    --out t_${tag}_ctrl.json
  for W in 4 12; do
    echo "=== $tag W=$W ==="
    CUDA_VISIBLE_DEVICES=1 $PY disturber3.py --work-ms $W --k 60 --period 1.4 \
      --reps-file burst_reps_e.json --out t_${tag}_W${W}_log.json &
    DP=$!
    CUDA_VISIBLE_DEVICES=1 $PY victim7.py --inner $inner --dots $dots --cycles 600 \
      --out t_${tag}_W${W}.json
    wait $DP
  done
done
echo "=== E6(三轴)完成 ==="

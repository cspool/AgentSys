#!/bin/bash
# E1': 真实负载三态(同一 kernel 族,仅算术强度不同)
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
for cfg in "memwall:120" "saturated:290" "computewall:600"; do
  tag=${cfg%%:*}; inner=${cfg##*:}
  echo "=== $tag(inner=$inner)ctrl ==="
  CUDA_VISIBLE_DEVICES=0 $PY victim6.py --inner $inner --cycles 600 --out r_${tag}_ctrl.json
  for W in 1 4 12; do
    echo "=== $tag W=$W ==="
    CUDA_VISIBLE_DEVICES=0 $PY disturber3.py --work-ms $W --k 60 --period 1.4 \
      --reps-file burst_reps_e.json --out r_${tag}_W${W}_log.json &
    DP=$!
    CUDA_VISIBLE_DEVICES=0 $PY victim6.py --inner $inner --cycles 600 --out r_${tag}_W${W}.json
    wait $DP
  done
done
echo "=== E1' 完成 ==="

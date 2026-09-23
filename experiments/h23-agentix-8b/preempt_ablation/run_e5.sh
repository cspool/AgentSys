#!/bin/bash
# E5: 空间共享(MPS)下的三态 —— 墙态的闲置维能否吸收新工作
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
export CUDA_MPS_PIPE_DIRECTORY=/tmp/mps0
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
for cfg in "xwall:60" "memwall:120" "saturated:290" "computewall:600"; do
  tag=${cfg%%:*}; inner=${cfg##*:}
  echo "=== MPS $tag(inner=$inner)ctrl ==="
  CUDA_VISIBLE_DEVICES=0 $PY victim6.py --inner $inner --cycles 600 --out m_${tag}_ctrl.json
  for W in 4 12; do
    echo "=== MPS $tag W=$W ==="
    CUDA_VISIBLE_DEVICES=0 $PY disturber3.py --work-ms $W --k 60 --period 1.4 \
      --reps-file burst_reps_e.json --out m_${tag}_W${W}_log.json &
    DP=$!
    CUDA_VISIBLE_DEVICES=0 $PY victim6.py --inner $inner --cycles 600 --out m_${tag}_W${W}.json
    wait $DP
  done
done
echo "=== E5(MPS)完成 ==="

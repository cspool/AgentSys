#!/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
BR=$(cat burst_reps.txt)
RF=reps_v4_v1.json
echo "=== L2 ctrl_cold ==="
CUDA_VISIBLE_DEVICES=0 $PY victim4.py --pattern dram,dram,sm --cycles 1600 \
  --reps-file $RF --out l2_ctrl_cold.json
for st in uniform sm_only dram_only; do
  echo "=== L2 $st ==="
  sleep 60
  CUDA_VISIBLE_DEVICES=0 $PY disturber2.py --strategy $st --k 200 --period 4.3 \
    --burst-reps $BR --out l2_${st}_log.json &
  DPID=$!
  CUDA_VISIBLE_DEVICES=0 $PY victim4.py --pattern dram,dram,sm --cycles 1600 \
    --reps-file $RF --out l2_${st}.json
  wait $DPID
done
sleep 60
echo "=== L2 ctrl_hot ==="
CUDA_VISIBLE_DEVICES=0 $PY victim4.py --pattern dram,dram,sm --cycles 1600 \
  --reps-file $RF --out l2_ctrl_hot.json
echo "=== L2 完成 ==="

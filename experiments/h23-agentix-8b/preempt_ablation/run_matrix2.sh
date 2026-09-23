#!/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
for mode in dram sm; do
  echo "=== v2 $mode control ==="
  CUDA_VISIBLE_DEVICES=1 $PY victim2.py --mode $mode --seconds 45 --out v2_${mode}_ctrl.json
  echo "=== v2 $mode disturbed(K=40) ==="
  CUDA_VISIBLE_DEVICES=1 $PY disturber.py --k 40 --period 1.0 --out v2_${mode}_dist_log.json &
  DPID=$!
  CUDA_VISIBLE_DEVICES=1 $PY victim2.py --mode $mode --seconds 45 --out v2_${mode}_dist.json
  wait $DPID
done
echo "=== v2 矩阵完成 ==="

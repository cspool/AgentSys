#!/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
for mode in dram gemm; do
  echo "=== $mode control ==="
  CUDA_VISIBLE_DEVICES=1 $PY victim.py --mode $mode --seconds 45 --out ${mode}_ctrl.json
  echo "=== $mode disturbed(K=40) ==="
  CUDA_VISIBLE_DEVICES=1 $PY disturber.py --k 40 --period 1.0 --out ${mode}_dist_log.json &
  DPID=$!
  CUDA_VISIBLE_DEVICES=1 $PY victim.py --mode $mode --seconds 45 --out ${mode}_dist.json
  wait $DPID
done
echo "=== 矩阵完成 ==="

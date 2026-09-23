#!/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
rm -f reps_l2.txt reps_dram2.txt
for mode in l2 dram; do
  RF=reps_${mode}2.txt
  echo "=== swap $mode control ==="
  CUDA_VISIBLE_DEVICES=0 $PY victim3.py --mode $mode --seconds 45 --reps-file $RF --out sw_${mode}_ctrl.json
  echo "=== swap $mode disturbed(K=20 x 1GB H2D) ==="
  CUDA_VISIBLE_DEVICES=0 $PY swapper.py --k 20 --period 2.0 --out sw_${mode}_log.json &
  DPID=$!
  CUDA_VISIBLE_DEVICES=0 $PY victim3.py --mode $mode --seconds 45 --reps-file $RF --out sw_${mode}_dist.json
  wait $DPID
done
echo "=== swap 矩阵完成 ==="

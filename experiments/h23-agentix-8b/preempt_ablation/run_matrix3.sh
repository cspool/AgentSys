#!/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
rm -f reps_dram.txt reps_sm.txt
for mode in dram sm; do
  echo "=== v4 $mode control ==="
  CUDA_VISIBLE_DEVICES=0 $PY victim2.py --mode $mode --seconds 45 \
    --reps-file reps_$mode.txt --out v4_${mode}_ctrl.json
  echo "=== v4 $mode disturbed ==="
  CUDA_VISIBLE_DEVICES=0 $PY disturber.py --k 40 --period 1.0 --out v4_${mode}_dist_log.json &
  DPID=$!
  CUDA_VISIBLE_DEVICES=0 $PY victim2.py --mode $mode --seconds 45 \
    --reps-file reps_$mode.txt --out v4_${mode}_dist.json
  wait $DPID
done
echo "=== v4 矩阵完成 ==="

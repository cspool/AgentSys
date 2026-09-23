#!/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
for mode in l2 dram; do
  RF=reps_${mode}2.txt
  echo "=== S2p $mode disturbed(alloc+copy) ==="
  CUDA_VISIBLE_DEVICES=0 $PY swapper2.py --k 20 --period 2.0 --out s2p_${mode}_log.json &
  DPID=$!
  CUDA_VISIBLE_DEVICES=0 $PY victim3.py --mode $mode --seconds 45 --reps-file $RF --out s2p_${mode}_dist.json
  wait $DPID
done
echo "=== S2p 完成 ==="

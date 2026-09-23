#!/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
# 受害者复用 victim2(dram/sm 长核,reps 冻结文件已存在则沿用)
for mode in dram sm; do
  echo "=== v6 $mode disturbed(K=30 全卡burst) ==="
  CUDA_VISIBLE_DEVICES=0 $PY disturber_full.py --k 30 --period 1.5 --out v6_${mode}_log.json &
  DPID=$!
  CUDA_VISIBLE_DEVICES=0 $PY victim2.py --mode $mode --seconds 46 \
    --reps-file reps_$mode.txt --out v6_${mode}_dist.json
  wait $DPID
done
echo "=== v6 完成 ==="

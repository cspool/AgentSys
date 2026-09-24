#!/bin/bash
cd /workspace/AgentSys/experiments/h23-agentix-8b/e15
rm -f v8_done.flag
for arm in R1 RB RS RSr; do for seed in 7 21 42; do
  CUDA_VISIBLE_DEVICES=0 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True timeout 260 \
    /data3/docker_cache/AgentSys/envs/mpk/bin/python coresidency_v7.py --arm $arm --dur 120 --seed $seed --out resv8_${arm}_$seed.json >/dev/null 2>&1
done; done
echo DONE > v8_done.flag

#!/bin/bash
cd /workspace/AgentSys/experiments/h23-agentix-8b/e15
rm -f v5f_done.flag
for arm in R1 RB RS RSr; do for seed in 7 21 42; do
  CUDA_VISIBLE_DEVICES=0 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True timeout 260 \
    /data3/docker_cache/AgentSys/envs/mpk/bin/python coresidency_v5.py --arm $arm --dur 90 --seed $seed --out resv7_${arm}_$seed.json >/dev/null 2>&1
done; done
echo DONE > v5f_done.flag

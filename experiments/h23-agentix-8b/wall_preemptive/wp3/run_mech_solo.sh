#!/usr/bin/env bash
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
export CUDA_VISIBLE_DEVICES=${GPU:-1} CUDA_MPS_PIPE_DIRECTORY=/tmp/mps1/pipe
VP=/data3/docker_cache/AgentSys/envs/pod_attn/bin/python
for M in ${MECHS:-serial streams hfuse pod2 pod4}; do
  timeout 150 $VP $R/victim/pod_wave.py --mech $M --secs 60 --out $R/out/solo_${M}${TAG:-}.json 2>&1 | tail -1
  sleep 5
done
echo MECH_SOLO_DONE

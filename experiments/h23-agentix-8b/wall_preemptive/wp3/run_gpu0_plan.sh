#!/usr/bin/env bash
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
export LD_LIBRARY_PATH=/workspace/AgentSys/third_party/BulletServe/csrc/build:${LD_LIBRARY_PATH:-}
# 先取 wave=12 的 solo 锚(DRAM墙 <-> 全饱和)
export CUDA_VISIBLE_DEVICES=0 CUDA_MPS_PIPE_DIRECTORY=/tmp/mps1/pipe
VP=/data3/docker_cache/AgentSys/envs/pod_attn/bin/python
for M in greenctx pod2; do
  timeout 150 $VP $R/victim/pod_wave.py --mech $M --secs 60 --wave 12 --out $R/out/solo_${M}_w12.json 2>&1 | tail -1
  sleep 5
done
# 矩阵: 相位1=DRAM墙(该抢), 相位2=全饱和(该避)
for M in greenctx pod2; do
  for REP in 1 2; do
    GPU=0 MECH=$M AX=tc WAVE=12 ORTH=1 ANTI=2 $R/run_mech_block.sh $REP
  done
done
echo GPU0_PLAN_DONE

#!/usr/bin/env bash
# 真挂起抢占 x 时机: 受害者 BURST 期间真正停止并等恢复; 抢占者同期 64 TPC。
# wave=02 (DRAM墙 <-> 全饱和), ORTH=0 抢墙态 / ANTI=2 抢全饱和。机制: pod4(有杠杆) + pod2(容量墙)。
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
export LD_LIBRARY_PATH=/workspace/AgentSys/third_party/BulletServe/csrc/build:${LD_LIBRARY_PATH:-}
export CUDA_VISIBLE_DEVICES=1 CUDA_MPS_PIPE_DIRECTORY=/tmp/mps1/pipe
VP=/data3/docker_cache/AgentSys/envs/pod_attn/bin/python
for M in pod4 pod2; do
  timeout 150 $VP $R/victim/pod_wave.py --mech $M --secs 60 --wave 02 --out $R/out/solo_${M}_w02_g1.json 2>&1 | tail -1
  sleep 5
done
for M in pod4 pod2; do
  for REP in 1 2; do
    GPU=1 MECH=$M AX=tc WAVE=02 ORTH=0 ANTI=2 SUSP=1 $R/run_mech_block.sh $REP
  done
done
echo GPU1_SUSP_DONE

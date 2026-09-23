#!/usr/bin/env bash
# 锐利版核心对照: wave=02 (相0=DRAM墙 <-> 相2=全饱和), TC 轴抢占者。
# 受害者 TC 占用 37.8% vs 87% (对比度 49pp)。ORTH=0(抢DRAM墙态) ANTI=2(抢全饱和)。
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
export LD_LIBRARY_PATH=/workspace/AgentSys/third_party/BulletServe/csrc/build:${LD_LIBRARY_PATH:-}
export CUDA_VISIBLE_DEVICES=0 CUDA_MPS_PIPE_DIRECTORY=/tmp/mps1/pipe
VP=/data3/docker_cache/AgentSys/envs/pod_attn/bin/python
for M in pod2 greenctx; do
  timeout 150 $VP $R/victim/pod_wave.py --mech $M --secs 60 --wave 02 --out $R/out/solo_${M}_w02.json 2>&1 | tail -1
  sleep 5
done
for M in pod2 greenctx; do
  for REP in 1 2; do
    GPU=0 MECH=$M AX=tc WAVE=02 ORTH=0 ANTI=2 $R/run_mech_block.sh $REP
  done
done
echo GPU0_PLAN2_DONE
# 随后自动跑 L2 驻留探针(需无 MPS 环境, probe 内部自行 unset)
GPU=0 bash $R/probe/l2wall_probe.sh

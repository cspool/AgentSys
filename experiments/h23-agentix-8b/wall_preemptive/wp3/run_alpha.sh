#!/usr/bin/env bash
# 跑一个抢占时机臂: 抢占者先起(自检 solo 基线), 10s 后起受害者 MPK。
set -u
U1=GPU-619e0c86-ae77-e523-7e85-97195a01f08b
export CUDA_VISIBLE_DEVICES=$U1 CUDA_MPS_PIPE_DIRECTORY=/tmp/mps1/pipe
export LD_LIBRARY_PATH=/workspace/AgentSys/third_party/BulletServe/csrc/build:${LD_LIBRARY_PATH:-}
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
VB=/data3/docker_cache/AgentSys/envs/bullet/bin/python
ARM=$1; AX=${2:-tc}; REP=${3:-1}
OUT=$R/out/alpha_${AX}_${ARM}_r${REP}.json
setsid nohup env CUDA_VISIBLE_DEVICES=$U1 CUDA_MPS_PIPE_DIRECTORY=/tmp/mps1/pipe \
  LD_LIBRARY_PATH=$LD_LIBRARY_PATH $VB $R/preemptor/co_alpha.py --arm $ARM --axis $AX \
  --out $OUT > /tmp/alpha_${AX}_${ARM}_r${REP}.log 2>&1 < /dev/null & disown
sleep 10
setsid nohup /tmp/mpk_mps.sh > /tmp/mpk_alpha_${AX}_${ARM}_r${REP}.log 2>&1 < /dev/null & disown
echo "臂=$ARM 轴=$AX rep=$REP 已启动 -> $OUT"

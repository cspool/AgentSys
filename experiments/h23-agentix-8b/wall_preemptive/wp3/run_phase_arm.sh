#!/usr/bin/env bash
# 一个臂: 受害者(POD 方波)先起并预热, 抢占者随后接入, 两者全程并发。
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
export CUDA_VISIBLE_DEVICES=1 CUDA_MPS_PIPE_DIRECTORY=/tmp/mps1/pipe
export LD_LIBRARY_PATH=/workspace/AgentSys/third_party/BulletServe/csrc/build:${LD_LIBRARY_PATH:-}
ARM=$1; AX=${2:-tc}; REP=${3:-1}
VP=/data3/docker_cache/AgentSys/envs/pod_attn/bin/python
CP=/data3/docker_cache/AgentSys/envs/bullet/bin/python
VOUT=$R/out/vic_${AX}_${ARM}_r${REP}.json; COUT=$R/out/co_${AX}_${ARM}_r${REP}.json
rm -f $VOUT $COUT
setsid nohup env CUDA_VISIBLE_DEVICES=1 CUDA_MPS_PIPE_DIRECTORY=/tmp/mps1/pipe \
  $VP $R/victim/pod_wave.py --secs 95 --out $VOUT > /tmp/vic_${AX}_${ARM}_r${REP}.log 2>&1 < /dev/null & disown
sleep 8
setsid nohup env CUDA_VISIBLE_DEVICES=1 CUDA_MPS_PIPE_DIRECTORY=/tmp/mps1/pipe \
  LD_LIBRARY_PATH=$LD_LIBRARY_PATH $CP $R/preemptor/co_phase.py --arm $ARM --axis $AX \
  --secs 70 --warmup 5 --out $COUT > /tmp/co_${AX}_${ARM}_r${REP}.log 2>&1 < /dev/null & disown
for i in $(seq 1 40); do
  if [ -f $VOUT ] && [ -f $COUT ]; then break; fi
  sleep 5
done
echo "  $ARM: 受害者=$([ -f $VOUT ] && echo ok || echo 缺) 抢占者=$([ -f $COUT ] && echo ok || echo 缺)"
for p in $(pgrep -x python3.12); do
  c=$(tr '\0' ' ' < /proc/$p/cmdline 2>/dev/null)
  case "$c" in *pod_wave.py*|*co_phase.py*) kill -KILL $p 2>/dev/null;; esac
done
sleep 8

#!/usr/bin/env bash
# 最快抢占(CILP)矩阵: 等挂起矩阵结束后自动开跑。
# 六机制 x {a100,a000} x 2rep, wave02, 独立 context => 硬件指令级抢占。
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
until grep -q "GPU1_SUSP_DONE" /tmp/gpu1_susp.log 2>/dev/null; do sleep 30; done
export LD_LIBRARY_PATH=/workspace/AgentSys/third_party/BulletServe/csrc/build:${LD_LIBRARY_PATH:-}
export CUDA_VISIBLE_DEVICES=1
VP=/data3/docker_cache/AgentSys/envs/pod_attn/bin/python
# 无 MPS 的 solo 锚(与 cilp 同 context 环境)
for M in serial streams hfuse pod2 pod4 greenctx; do
  [ -f $R/out/solo_${M}_w02_nomps.json ] || timeout 150 env CUDA_MPS_PIPE_DIRECTORY= \
    $VP $R/victim/pod_wave.py --mech $M --secs 60 --wave 02 --out $R/out/solo_${M}_w02_nomps.json 2>&1 | tail -1
  sleep 4
done
for M in serial streams hfuse pod2 pod4 greenctx; do
  for REP in 1 2; do
    GPU=1 MECH=$M AX=tc WAVE=02 ORTH=0 ANTI=2 MODE=cilp ARMS_OVERRIDE="a100 a000" $R/run_mech_block.sh $REP
  done
done
echo GPU1_CILP_DONE

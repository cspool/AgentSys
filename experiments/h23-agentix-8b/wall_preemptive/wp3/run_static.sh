#!/usr/bin/env bash
# 配额动态范围门禁(规格证伪清单#15): 受害者常驻时, BASE 与 BURST 两档抢占者绝对吞吐之比必须 >=1.5
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
for N in 8 16 32 48 64; do
  rm -f $R/out/static_tc_q${N}.json
  ( export CUDA_VISIBLE_DEVICES=GPU-619e0c86-ae77-e523-7e85-97195a01f08b
    export CUDA_MPS_PIPE_DIRECTORY=/tmp/mps1/pipe
    export LD_LIBRARY_PATH=/workspace/AgentSys/third_party/BulletServe/csrc/build
    setsid nohup /data3/docker_cache/AgentSys/envs/bullet/bin/python $R/preemptor/co_alpha.py \
      --arm base_only --axis tc --base-tpcs $N --burst-tpcs $N --win-secs 30 --lead-secs 2 \
      --out $R/out/static_tc_q${N}.json > /tmp/static_q${N}.log 2>&1 < /dev/null & disown ) 
  sleep 10
  setsid nohup /tmp/mpk_mps.sh > /tmp/mpk_static_q${N}.log 2>&1 < /dev/null & disown
  for i in $(seq 1 60); do [ -f $R/out/static_tc_q${N}.json ] && break; sleep 5; done
  pkill -KILL -f "[d]emo.py" 2>/dev/null || true
  pkill -KILL -f "[c]o_alpha.py" 2>/dev/null || true
  sleep 15
done
echo STATIC_DONE

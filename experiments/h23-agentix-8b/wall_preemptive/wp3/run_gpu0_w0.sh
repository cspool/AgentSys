#!/usr/bin/env bash
# W=0 场景: agent 型受害者(全饱和产出 <-> 工具期空闲), 挂起货币 duty 0.433。
# a100 = wall-p 感知调度(抢占全部对齐空闲窗) ; a050 = 相位盲均匀(现实的 on-demand 抢占) ; a000 = 最差
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
export LD_LIBRARY_PATH=/workspace/AgentSys/third_party/BulletServe/csrc/build:${LD_LIBRARY_PATH:-}
for REP in 1 2; do
  GPU=0 MECH=pod AX=tc WAVE=23 ORTH=3 ANTI=2 SUSP=1 VSECS=80 \
    OFFS=80,210,340,465 BMS=130 $R/run_mech_block.sh $REP
done
echo GPU0_W0_DONE

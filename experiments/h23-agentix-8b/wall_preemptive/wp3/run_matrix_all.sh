#!/usr/bin/env bash
# 五机制 x 抢占时机矩阵。每个机制一个 block(三臂随机序), 先 tc 轴。
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
for M in serial streams hfuse pod2 pod4; do
  for REP in 1 2; do
    MECH=$M AX=${AX:-tc} $R/run_mech_block.sh $REP
  done
done
echo MATRIX_ALL_DONE

#!/usr/bin/env bash
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
for AX in tc dram; do
  for REP in 2 3; do
    [ "$AX" = "dram" ] && [ "$REP" = "2" ] && REP=1   # dram 轴从 rep1 起
    AX=$AX $R/run_phase_block.sh $REP
  done
done
# dram 轴补 rep2/3
for REP in 2 3; do AX=dram $R/run_phase_block.sh $REP; done
echo ALL_BLOCKS_DONE

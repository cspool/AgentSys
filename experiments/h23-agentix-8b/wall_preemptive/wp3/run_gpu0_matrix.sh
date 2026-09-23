#!/usr/bin/env bash
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
export LD_LIBRARY_PATH=/workspace/AgentSys/third_party/BulletServe/csrc/build:${LD_LIBRARY_PATH:-}
for M in ${MECHS:-greenctx}; do
  for REP in 1 2; do GPU=0 MECH=$M AX=${AX:-tc} $R/run_mech_block.sh $REP; done
done
echo GPU0_MATRIX_DONE

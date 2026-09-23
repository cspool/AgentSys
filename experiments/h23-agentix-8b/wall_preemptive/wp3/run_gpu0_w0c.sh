#!/usr/bin/env bash
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
export LD_LIBRARY_PATH=/workspace/AgentSys/third_party/BulletServe/csrc/build:${LD_LIBRARY_PATH:-}
for REP in 5 6; do
  GPU=0 MECH=pod AX=tc WAVE=23 ORTH=3 ANTI=2 SUSP=1 VSECS=80 CSECS=76 WARM=2 \
    OFFS=80,210,340,465 BMS=130 $R/run_mech_block.sh $REP
done
echo GPU0_W0C_DONE

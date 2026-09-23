#!/usr/bin/env bash
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
AX=${AX:-tc}; REP=${1:-1}
ARMS=$(python3 -c "
import random; random.seed($REP*13+5)
a=['a100','a050','a000']; random.shuffle(a); print(' '.join(a))")
echo "block $REP 臂序: $ARMS"
for ARM in $ARMS; do $R/run_phase_arm.sh $ARM $AX $REP; done
echo "PHASE_BLOCK_${REP}_DONE"

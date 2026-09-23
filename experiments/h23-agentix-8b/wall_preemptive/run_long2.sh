#!/bin/bash
cd /workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive
MODE=mps K=150 PATTERN=w,w,s CYC=560 PFX=J23 ./run_cmp.sh
MODE=mps K=150 PATTERN=w,s   CYC=840 PFX=J12 ./run_cmp.sh
MODE=mps K=150 PATTERN=w,s,s CYC=560 PFX=J13 ./run_cmp.sh
echo "=== 泊松到达长跑完成 ==="

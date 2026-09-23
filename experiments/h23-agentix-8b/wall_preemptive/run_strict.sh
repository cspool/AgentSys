#!/bin/bash
# 严格公平长跑:三臂(valve / wall_aware / random_defer),同负载同配置
cd /workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive
MODE=mps K=300 PERIOD=1.5 PATTERN=w,s CYC=1700 PFX=S12 ./run_cmp.sh
echo "=== 严格长跑完成 ==="

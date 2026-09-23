#!/bin/bash
# 长跑:MPS 模式 × 三种相位构成 × 两种择时策略,K=150
cd /workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive
export MODE=mps K=150 PERIOD=1.5
MODE=mps K=150 PATTERN=w,w,s   CYC=520 PFX=L23 ./run_cmp.sh
MODE=mps K=150 PATTERN=w,s     CYC=780 PFX=L12 ./run_cmp.sh
MODE=mps K=150 PATTERN=w,s,s   CYC=520 PFX=L13 ./run_cmp.sh
echo "=== 长跑完成 ==="

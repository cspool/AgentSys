#!/usr/bin/env bash
# 产出率感知抢占对照: 受害者 = 全饱和(38.6k tok/s) <-> 长尾排空(6.2k tok/s), 均 GPU-busy。
# a100=抢低产出时刻 / a050=相位盲 / a000=抢高产出时刻。真挂起, duty~0.4, 等功。
R=/workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive/wp3
export LD_LIBRARY_PATH=/workspace/AgentSys/third_party/BulletServe/csrc/build:${LD_LIBRARY_PATH:-}
for REP in 1 2; do
  GPU=0 MECH=pod AX=tc WAVE=25 ORTH=5 ANTI=2 SUSP=1 VSECS=80 CSECS=76 WARM=2 \
    OFFS=80,210,340,465 BMS=130 $R/run_mech_block.sh $REP
done
echo GPU0_RATE_DONE

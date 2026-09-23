#!/bin/bash
# 步骤3:wall_preemptive 负载 + Valve 方法 vs 墙感知方法
# 受害者(离线)= 交替墙态/饱和态的 victim6;抢占需求(在线)= 等量 burst
# 臂:  naive      自由共跑(无抢占管理)
#       valve      在线忙即停离线 + T_cool 冷却(Valve 的择时规则:只看在线忙闲)
#       wallaware  同样次数的抢占,但推迟到受害者处于墙态才执行(我们的规则)
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b
PY=/workspace/AgentSys/.venv-vllm/bin/python
WP=wall_preemptive
VR=valve_repro
OUT=$VR/wallcmp
mkdir -p $OUT
echo "(占位:实现见 wall_ctl.py)"

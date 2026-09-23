#!/bin/bash
# 目标2:同一 wall_preemptive 负载,Valve 择时 vs 墙感知择时
# 等 K、等 burst 工作、同到达序列,唯一变量=落点。编排按事件同步,不用盲等。
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive
PY=/workspace/AgentSys/.venv-vllm/bin/python
DEV=${DEV:-0}
REPS=$(python3 -c "import json;print(json.load(open('burst_reps_e.json'))['12.0'])")
K=40; PERIOD=1.5; COOL=0.074
CYC=260          # 260 cycles x 3 phase x ~163ms ≈ 127s > K*PERIOD=60s + 余量
echo "reps=$REPS K=$K period=${PERIOD}s T_cool=${COOL}s cycles=$CYC dev=$DEV"

wait_state () { for i in $(seq 1 400); do [ -f /tmp/wp_state.json ] && return 0; sleep 0.25; done; return 1; }

echo "=== ctrl ==="
CUDA_VISIBLE_DEVICES=$DEV $PY victim8.py --cycles $CYC --out wc_ctrl.json
for mode in valve wall_aware; do
  echo "=== $mode ==="
  rm -f /tmp/wp_trigger /tmp/wp_state.json
  CUDA_VISIBLE_DEVICES=$DEV $PY disturber4.py --reps $REPS --k $K --out wc_${mode}_burst.json &
  BP=$!
  CUDA_VISIBLE_DEVICES=$DEV $PY victim8.py --cycles $CYC --out wc_${mode}_victim.json &
  VP=$!
  wait_state || { echo "受害者未发布相位"; kill $BP $VP 2>/dev/null; exit 1; }
  sleep 5
  $PY wall_ctl.py --mode $mode --k $K --period $PERIOD --cool $COOL --out wc_${mode}_ctl.json
  wait $VP; kill $BP 2>/dev/null; wait $BP 2>/dev/null
done
echo "=== wallcmp 完成 ==="

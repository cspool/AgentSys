#!/bin/bash
# 目标2-B:同一对照,但开启 MPS 空间共享
# 机理:墙态有闲置维可吸收抢占工作(E5 实测 c≈0),全饱和态只能挤占
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
export CUDA_MPS_PIPE_DIRECTORY=/tmp/mps_wc CUDA_MPS_LOG_DIRECTORY=/tmp/mps_wc_log
cd /workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive
PY=/workspace/AgentSys/.venv-vllm/bin/python
REPS=$(python3 -c "import json;print(json.load(open('burst_reps_e.json'))['12.0'])")
K=40; PERIOD=1.5; COOL=0.074; CYC=260
mkdir -p /tmp/mps_wc /tmp/mps_wc_log
CUDA_VISIBLE_DEVICES=0 nvidia-cuda-mps-control -d
sleep 3
wait_state () { for i in $(seq 1 400); do [ -f /tmp/wp_state.json ] && return 0; sleep 0.25; done; return 1; }
echo "=== MPS ctrl ==="
CUDA_VISIBLE_DEVICES=0 $PY victim8.py --cycles $CYC --out wm_ctrl.json
for mode in valve wall_aware; do
  echo "=== MPS $mode ==="
  rm -f /tmp/wp_trigger /tmp/wp_state.json
  CUDA_VISIBLE_DEVICES=0 $PY disturber4.py --reps $REPS --k $K --out wm_${mode}_burst.json &
  BP=$!
  CUDA_VISIBLE_DEVICES=0 $PY victim8.py --cycles $CYC --out wm_${mode}_victim.json &
  VP=$!
  wait_state || { echo "受害者未发布相位"; kill $BP $VP 2>/dev/null; exit 1; }
  sleep 5
  $PY wall_ctl.py --mode $mode --k $K --period $PERIOD --cool $COOL --out wm_${mode}_ctl.json
  wait $VP; kill $BP 2>/dev/null; wait $BP 2>/dev/null
done
echo quit | nvidia-cuda-mps-control 2>/dev/null
echo "=== MPS 对照完成 ==="

#!/bin/bash
# wall_preemptive 对照(公平性硬要求):
#   等 K、等 burst 工作、同受害者负载、同到达序列;唯一变量=落点规则
#   代价侧:记录墙感知的择时延迟 + 抢占者端到端延迟,收益必须扣除它
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/wall_preemptive
PY=/workspace/AgentSys/.venv-vllm/bin/python
MODE=${MODE:-mps}; K=${K:-40}; PERIOD=${PERIOD:-1.5}; CYC=${CYC:-260}; PFX=${PFX:-s}
PATTERN=${PATTERN:-w,w,s}
COOL=0.074
if [ "$MODE" = "mps" ]; then
  export CUDA_MPS_PIPE_DIRECTORY=/tmp/mps_wc CUDA_MPS_LOG_DIRECTORY=/tmp/mps_wc_log
  mkdir -p /tmp/mps_wc /tmp/mps_wc_log
  pgrep -x nvidia-cuda-mps-control >/dev/null || { CUDA_VISIBLE_DEVICES=0 nvidia-cuda-mps-control -d; sleep 3; }
else
  unset CUDA_MPS_PIPE_DIRECTORY
fi
REPS=$(python3 -c "import json;print(json.load(open('burst_reps_e.json'))['12.0'])")
echo "MODE=$MODE K=$K period=$PERIOD cycles=$CYC pattern=$PATTERN prefix=$PFX reps=$REPS"
wait_state () { for i in $(seq 1 600); do [ -f /tmp/wp_state.json ] && return 0; sleep 0.25; done; return 1; }
echo "=== ${PFX} ctrl ==="
CUDA_VISIBLE_DEVICES=0 $PY victim8.py --cycles $CYC --pattern $PATTERN --out ${PFX}_ctrl.json
for mode in valve wall_aware random_defer; do
  echo "=== ${PFX} $mode ==="
  rm -f /tmp/wp_trigger /tmp/wp_state.json
  CUDA_VISIBLE_DEVICES=0 $PY disturber4.py --reps $REPS --k $K --out ${PFX}_${mode}_burst.json &
  BP=$!
  CUDA_VISIBLE_DEVICES=0 $PY victim8.py --cycles $CYC --pattern $PATTERN --out ${PFX}_${mode}_victim.json &
  VP=$!
  wait_state || { echo "受害者未发布相位"; kill $BP $VP 2>/dev/null; exit 1; }
  sleep 5
  DF=""
  [ "$mode" = "random_defer" ] && DF="--delay-file ${PFX}_wall_aware_ctl.json"
  $PY wall_ctl.py --mode $mode --k $K --period $PERIOD --cool $COOL $DF \
      --out ${PFX}_${mode}_ctl.json
  wait $VP; kill $BP 2>/dev/null; wait $BP 2>/dev/null
done
echo "=== ${PFX} 完成 ==="

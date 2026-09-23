#!/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys
PY=./.venv-vllm/bin/python
VR=experiments/h23-agentix-8b/valve_repro
ON_WL=experiments/h23-agentix-8b/workloads/pt_interactive.json
OFF_WL=experiments/h23-agentix-8b/workloads/pt_big_mixed.json

run_online () {  # $1 outdir
  CUDA_VISIBLE_DEVICES=1 AGENTIX_WALLFLAG=1 \
    AGENTIX_WALLFLAG_PATH=/tmp/agentix_wallflag_online.json \
    $PY experiments/h23-agentix-8b/astra_repro/astra_swap.py \
    --workload $ON_WL --output-dir $1 --policy atlas --enforce-eager \
    --gpu-memory-utilization 0.55 > $1.log 2>&1
}
run_offline () {  # $1 outdir  $2 model-dir
  CUDA_VISIBLE_DEVICES=1 \
    $PY experiments/h23-agentix-8b/astra_repro/astra_swap.py \
    --workload $OFF_WL --output-dir $1 --policy fcfs --enforce-eager \
    --model-dir /data3/docker_model/AgentSys/Qwen3-1.7B \
    --gpu-memory-utilization 0.30 > $1.log 2>&1
}

echo "=== a) online solo ==="
run_online $VR/on_solo
echo "=== b) offline solo ==="
run_offline $VR/off_solo
echo "=== c) colo naive(无抢占)==="
run_offline $VR/off_naive & OFFP=$!
sleep 45   # 等离线引擎起好并进入服务
run_online $VR/on_naive
kill $OFFP 2>/dev/null; wait $OFFP 2>/dev/null
echo "=== d) colo valve(忙停+冷却)==="
rm -f /tmp/agentix_wallflag_online.json
run_offline $VR/off_valve & OFFP=$!
sleep 45
( $PY $VR/valve_ctl.py --offline-pid $OFFP --cool 1.0 --out $VR/valve_events.json ) & CTLP=$!
run_online $VR/on_valve
wait $CTLP 2>/dev/null
kill $OFFP 2>/dev/null; wait $OFFP 2>/dev/null
echo "=== Valve 复现四臂完成 ==="

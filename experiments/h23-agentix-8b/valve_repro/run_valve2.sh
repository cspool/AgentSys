#!/bin/bash
# Valve 正式复现:对称 Qwen3-1.7B 对,5 臂(计算维),T_cool 实测
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys
PY=./.venv-vllm/bin/python
VR=experiments/h23-agentix-8b/valve_repro
ONW=experiments/h23-agentix-8b/workloads/pt_valve_online.json
OFFW=experiments/h23-agentix-8b/workloads/pt_valve_offline.json
Q17=/data3/docker_model/AgentSys/Qwen3-1.7B
OFLAG=/tmp/agentix_wallflag_online.json
PAUSEF=/tmp/valve_pause_offline

on () {  # $1 out
  CUDA_VISIBLE_DEVICES=1 AGENTIX_WALLFLAG=1 AGENTIX_WALLFLAG_PATH=$OFLAG \
    $PY experiments/h23-agentix-8b/astra_repro/astra_swap.py \
    --workload $ONW --output-dir $1 --policy atlas --enforce-eager \
    --model-dir $Q17 --gpu-memory-utilization 0.40 > $1.log 2>&1
}
off () {  # $1 out  $2 extra-env(k=v)
  CUDA_VISIBLE_DEVICES=1 env $2 \
    $PY experiments/h23-agentix-8b/astra_repro/astra_swap.py \
    --workload $OFFW --output-dir $1 --policy fcfs --enforce-eager \
    --model-dir $Q17 --gpu-memory-utilization 0.40 > $1.log 2>&1
}

rm -f $OFLAG $PAUSEF
echo "=== 1/6 on_solo(+T_cool 实测)==="
( sleep 30; $PY $VR/tcool_watch.py $OFLAG $VR/t_cool.json ) & TW=$!
on $VR/v2_on_solo
wait $TW; cat $VR/t_cool.json
TCOOL=$(python3 -c "import json;print(json.load(open('$VR/t_cool.json'))['t_cool_s'])")
echo "T_cool=$TCOOL s"

echo "=== 2/6 off_solo ==="
off $VR/v2_off_solo "X=1"

echo "=== 3/6 colo_naive(自由共跑)==="
rm -f $OFLAG
off $VR/v2_off_naive "X=1" & OP=$!
sleep 40
on $VR/v2_on_naive
kill $OP 2>/dev/null; wait $OP 2>/dev/null

echo "=== 4/6 colo_channel(SIGSTOP 忙停 + T_cool)==="
rm -f $OFLAG
off $VR/v2_off_channel "X=1" & OP=$!
sleep 40
( $PY $VR/valve_ctl.py --offline-pid $OP --flag $OFLAG --cool $TCOOL \
    --out $VR/v2_channel_events.json ) & CP=$!
on $VR/v2_on_channel
wait $CP 2>/dev/null
kill $OP 2>/dev/null; wait $OP 2>/dev/null

echo "=== 5/6 colo_iter(迭代门 KernelPreempt 代理 + T_cool)==="
rm -f $OFLAG $PAUSEF
off $VR/v2_off_iter "AGENTIX_PAUSE_FILE=$PAUSEF" & OP=$!
sleep 40
( $PY $VR/iter_ctl.py $OFLAG $PAUSEF $TCOOL $VR/v2_iter_events.json ) & CP=$!
on $VR/v2_on_iter
wait $CP 2>/dev/null
kill $OP 2>/dev/null; wait $OP 2>/dev/null
rm -f $PAUSEF

echo "=== Valve 正式复现完成 ==="

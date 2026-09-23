#!/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
BR=$(cat burst_reps.txt)
RF=reps_v4_v1.json
# 噪声带:ctrl x2
for r in n1 n2; do
  echo "=== L1 ctrl_$r ==="
  CUDA_VISIBLE_DEVICES=0 $PY victim4.py --pattern dram,dram,sm --cycles 56 \
    --reps-file $RF --out l1_ctrl_$r.json
done
# 长跑电池:每臂 ~20min(cycles=1600),K=200 period=6s;臂间 60s 空冷
for st in uniform comp adv; do
  echo "=== L1 $st(20min)==="
  sleep 60
  CUDA_VISIBLE_DEVICES=0 nvidia-smi dmon -s c -d 30 -c 45 > l1_${st}_clock.log 2>&1 &
  CPID=$!
  CUDA_VISIBLE_DEVICES=0 $PY disturber2.py --strategy $st --k 200 --period 6.0 \
    --burst-reps $BR --out l1_${st}_log.json &
  DPID=$!
  CUDA_VISIBLE_DEVICES=0 $PY victim4.py --pattern dram,dram,sm --cycles 1600 \
    --reps-file $RF --out l1_${st}.json
  wait $DPID; kill $CPID 2>/dev/null
done
sleep 60
echo "=== L1 ctrl_long(漂移核对)==="
CUDA_VISIBLE_DEVICES=0 $PY victim4.py --pattern dram,dram,sm --cycles 1600 \
  --reps-file $RF --out l1_ctrl_long.json
echo "=== L1 完成 ==="

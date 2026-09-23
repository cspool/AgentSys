#!/bin/bash
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys/experiments/h23-agentix-8b/preempt_ablation
PY=/workspace/AgentSys/.venv-vllm/bin/python
BR=$(cat burst_reps.txt)
run_variety () {
  name=$1; pattern=$2; cycles=$3
  RF=reps_v4_${name}.json
  echo "=== $name ctrl ==="
  CUDA_VISIBLE_DEVICES=0 $PY victim4.py --pattern $pattern --cycles $cycles \
    --reps-file $RF --out s1p_${name}_ctrl.json
  for st in uniform comp adv; do
    echo "=== $name $st ==="
    CUDA_VISIBLE_DEVICES=0 $PY disturber2.py --strategy $st --k 24 --period 1.6 \
      --burst-reps $BR --out s1p_${name}_${st}_log.json &
    DPID=$!
    CUDA_VISIBLE_DEVICES=0 $PY victim4.py --pattern $pattern --cycles $cycles \
      --reps-file $RF --out s1p_${name}_${st}.json
    wait $DPID
  done
}
run_variety v1 dram,dram,sm 56
run_variety v2 dram,dram,dram,dram,dram,sm 28
run_variety v3 dram,l2,sm 56
echo "=== S1' 全部完成 ==="

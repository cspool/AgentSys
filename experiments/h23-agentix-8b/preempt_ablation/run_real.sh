#!/bin/bash
# E4-pilot: 真实 LLM serving 三态 × 等量抢占 —— 论文动机实验
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:${LD_LIBRARY_PATH:-}
cd /workspace/AgentSys
PY=./.venv-vllm/bin/python
PA=experiments/h23-agentix-8b/preempt_ablation
WLD=experiments/h23-agentix-8b/workloads

serve () {  # $1 workload  $2 outdir
  CUDA_VISIBLE_DEVICES=1 $PY experiments/h23-agentix-8b/astra_repro/astra_swap.py \
    --workload $WLD/$1.json --output-dir $PA/$2 --policy fcfs --enforce-eager \
    --gpu-memory-utilization 0.86 > $PA/$2.log 2>&1
}

for wl in pt_decode_wall pt_prefill_wall pt_mixed_sat; do
  tag=${wl#pt_}
  echo "=== $tag ctrl(带 dmon 资源画像)==="
  CUDA_VISIBLE_DEVICES=1 nvidia-smi dmon -s u -d 1 -c 200 > $PA/real_${tag}_dmon.log 2>&1 &
  DM=$!
  serve $wl real_${tag}_ctrl
  kill $DM 2>/dev/null
  echo "=== $tag disturbed(K=60 等量 burst)==="
  CUDA_VISIBLE_DEVICES=1 $PY $PA/disturber3.py --work-ms 12 --k 60 --period 1.4 \
    --reps-file $PA/burst_reps_e.json --out $PA/real_${tag}_log.json &
  DP=$!
  serve $wl real_${tag}_dist
  wait $DP
done
echo "=== 真实负载三态完成 ==="

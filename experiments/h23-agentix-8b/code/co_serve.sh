#!/usr/bin/env bash
# Co-residency driver: two vLLM engines (Qwen3-1.7B + Qwen2.5-VL-3B) on ONE GPU,
# launched as children of this script so one nsys session captures both.
# 方案1: reduced concurrency + explicit KV quotas.  方案2: add KV offload env.
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../../.."

OUT=${OUT:?}
WL=${WL:-experiments/h23-agentix-8b/workloads/thr_mixed_r0.2.json}
QWEN3_ARGS=${QWEN3_ARGS:-"--kv-cache-memory-gb 4 --gpu-memory-utilization 0.33 --max-num-seqs 16"}
VL_ARGS=${VL_ARGS:-"--kv-cache-memory-gb 4 --gpu-memory-utilization 0.52 --max-num-seqs 16"}
mkdir -p "$OUT/qwen3" "$OUT/vl"

./.venv-vllm/bin/python experiments/h23-agentix-8b/code/serve_agentix.py \
  --workload "$WL" --policy plas --nvtx --mark-tag "VL_" \
  --model-dir /data3/docker_model/AgentSys/models--Qwen--Qwen2.5-VL-3B-Instruct/snapshots/66285546d2b821cf421d4f5eb2576359d3770cd3 \
  --output-dir "$OUT/vl" $VL_ARGS > "$OUT/vl/run.log" 2>&1 &
VL_PID=$!
sleep 45   # let the bigger model finish loading before the second engine profiles memory
./.venv-vllm/bin/python experiments/h23-agentix-8b/code/serve_agentix.py \
  --workload "$WL" --policy plas --nvtx --mark-tag "Q3_" \
  --model-dir /data3/docker_model/AgentSys/Qwen3-1.7B \
  --output-dir "$OUT/qwen3" $QWEN3_ARGS > "$OUT/qwen3/run.log" 2>&1 &
Q3_PID=$!
wait $VL_PID; VL_EC=$?
wait $Q3_PID; Q3_EC=$?
echo "CO_SERVE_DONE vl=$VL_EC qwen3=$Q3_EC"

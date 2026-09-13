#!/usr/bin/env bash
# Paper-faithful matrix: FCFS vs PLAS vs ATLAS on multi-threaded Mixed workloads
# at the paper's own arrival-rate range for LLaMA-3.1-8B on 1 GPU (Fig. 12).
set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/../../.."
for rate in ${RATES:-0.1 0.2 0.3}; do
  wl="experiments/h23-agentix-8b/workloads/thr_mixed_r${rate}.json"
  for policy in ${POLICIES:-fcfs plas atlas}; do
    out="artifacts/agentix_8b/thr_r${rate}/${policy}"
    [ -f "$out/summary_${policy}.json" ] && { echo "skip ${rate}/${policy}"; continue; }
    mkdir -p "$out"
    echo "=== rate=${rate} policy=${policy} $(date -u +%H:%M:%S)"
    CUDA_VISIBLE_DEVICES=${DEVICE:-1} ./.venv-vllm/bin/python \
      experiments/h23-agentix-8b/code/serve_agentix.py \
      --workload "$wl" --policy "$policy" --output-dir "$out" --max-num-seqs "${SEQS:-64}" \
      > "$out/run.log" 2>&1 || { echo "FAILED ${rate}/${policy}"; tail -3 "$out/run.log"; continue; }
    python3 -c "
import json; s=json.load(open('$out/summary_${policy}.json')); o=s['observed']
print('   programs=%d calls=%d wall=%.0fs thr=%.0f tok/s ptl_mean=%.1fms p90=%.1fms' % (
  o['programs'], o['llm_calls'], o['wall_s'], o['throughput_tokens_per_s'],
  o['program_token_latency_ms']['mean'], o['program_token_latency_ms']['p90']))"
  done
done
echo THR_MATRIX_DONE

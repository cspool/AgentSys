#!/usr/bin/env bash
# Saturated regime: cap the resident batch so requests actually queue, which is
# the regime Agentix's program-level scheduling targets. Same frozen workload per
# policy pair.
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
venv_python="${VENV_PYTHON:-${project_root}/.venv-vllm/bin/python}"
runtime="${project_root}/experiments/h23-agentix-8b/code/serve_agentix.py"
root="${project_root}/artifacts/agentix_8b"

rate=${RATE:-2}
seqs=${SEQS:-"8 16"}
policies=${POLICIES:-"fcfs plas"}

cd "${project_root}"
for ms in ${seqs}; do
  workload="${project_root}/experiments/h23-agentix-8b/workloads/mixed_r${rate}.json"
  for policy in ${policies}; do
    out="${root}/sat_r${rate}_seq${ms}/${policy}"
    mkdir -p "${out}"
    echo "=== rate=${rate} max_num_seqs=${ms} policy=${policy} $(date -u +%H:%M:%S)"
    CUDA_VISIBLE_DEVICES=${DEVICE:-1} "${venv_python}" "${runtime}" \
      --workload "${workload}" --policy "${policy}" --output-dir "${out}" \
      --max-num-seqs "${ms}" \
      > "${out}/run.log" 2>&1 || { echo "FAILED rate=${rate} seqs=${ms} policy=${policy}"; tail -5 "${out}/run.log"; exit 1; }
    python3 -c "
import json
s=json.load(open('${out}/summary_${policy}.json')); o=s['observed']
print('   programs=%d wall=%.0fs thr=%.1f tok/s ptl_mean=%.1fms p90=%.1fms resp_p90=%.0fms' % (
  o['programs'], o['wall_s'], o['throughput_tokens_per_s'], o['program_token_latency_ms']['mean'],
  o['program_token_latency_ms']['p90'], o['program_response_time_ms']['p90']))
"
  done
done
echo "SATURATED_MATRIX_DONE"

#!/usr/bin/env bash
# Agentix-protocol reproduction matrix on one RTX 4090: FCFS vs PLAS at three
# program arrival rates, identical frozen workload per pair.
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
venv_python="${VENV_PYTHON:-${project_root}/.venv-vllm/bin/python}"
runtime="${project_root}/experiments/h23-agentix-8b/code/serve_agentix.py"
root="${project_root}/artifacts/agentix_8b"
rates=${RATES:-"1 2 4"}
policies=${POLICIES:-"fcfs plas"}

cd "${project_root}"
for rate in ${rates}; do
  workload="${project_root}/experiments/h23-agentix-8b/workloads/mixed_r${rate}.json"
  for policy in ${policies}; do
    out="${root}/r${rate}/${policy}"
    mkdir -p "${out}"
    echo "=== rate=${rate} policy=${policy} $(date -u +%H:%M:%S)"
    CUDA_VISIBLE_DEVICES=${DEVICE:-1} "${venv_python}" "${runtime}" \
      --workload "${workload}" \
      --policy "${policy}" \
      --output-dir "${out}" \
      > "${out}/run.log" 2>&1 || { echo "FAILED rate=${rate} policy=${policy}"; tail -5 "${out}/run.log"; exit 1; }
    python3 -c "
import json,sys
s=json.load(open('${out}/summary_${policy}.json'))
o=s['observed']
print('   programs=%d calls=%d wall=%.1fs thr=%.1f prog/s %.0f tok/s ptl_mean=%.1fms p90=%.1fms' % (
  o['programs'], o['llm_calls'], o['wall_s'], o['throughput_programs_per_s'], o['throughput_tokens_per_s'],
  o['program_token_latency_ms']['mean'], o['program_token_latency_ms']['p90']))
"
  done
done
echo "MATRIX_DONE"

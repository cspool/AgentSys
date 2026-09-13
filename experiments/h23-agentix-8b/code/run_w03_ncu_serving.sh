#!/usr/bin/env bash
# w03' / G04 adapted: NCU hardware counters on representative serving kernels.
#
# A serving run launches tens of thousands of kernels, so NCU profiles a bounded
# sample per family instead of a whole iteration: skip warm-up kernels and cap
# the count. Replay durations are hardware attributes only, never latency.
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
venv_python="${VENV_PYTHON:-${project_root}/.venv-vllm/bin/python}"
runtime="${project_root}/experiments/h23-agentix-8b/code/serve_agentix.py"

workload=${1:?usage: run_w03_ncu_serving.sh <workload.json> <policy> [tag]}
policy=${2:?policy}
tag=${3:-"${policy}"}
DEVICE=${DEVICE:-1}
SKIP=${SKIP:-200}
COUNT=${COUNT:-12}

out="${project_root}/artifacts/agentix_8b/autotrace/ncu_${tag}"
mkdir -p "${out}"
cd "${project_root}"

CUDA_VISIBLE_DEVICES=${DEVICE} ncu \
  --launch-skip "${SKIP}" --launch-count "${COUNT}" \
  --section SpeedOfLight --section MemoryWorkloadAnalysis --section Occupancy \
  --metrics gpu__time_duration.sum,dram__bytes_read.sum,dram__bytes_write.sum,lts__t_sector_hit_rate.pct,sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active,sm__inst_executed_pipe_tensor.sum,smsp__inst_executed.sum,launch__waves_per_multiprocessor,launch__registers_per_thread \
  --print-summary per-kernel \
  -f -o "${out}/${tag}" \
  "${venv_python}" "${runtime}" \
    --workload "${workload}" --policy "${policy}" --output-dir "${out}/run" \
  > "${out}/ncu.log" 2>&1 || true

ncu -i "${out}/${tag}.ncu-rep" --csv --page raw > "${out}/${tag}_ncu_raw.csv"
ncu -i "${out}/${tag}.ncu-rep" --csv --page details > "${out}/${tag}_ncu_details.csv"
echo "w03' complete: ${out}"

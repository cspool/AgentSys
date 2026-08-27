#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gpu_python="${project_root}/.venv-gpu/bin/python"
run_id=${1:-run_033}
run_dir="${project_root}/artifacts/gpu_runtime/${run_id}"
report_base="${run_dir}/nsight-dual-gpu"

mkdir -p "${run_dir}"
cd "${project_root}"

nsys profile \
  --force-overwrite=true \
  --trace=cuda,nvtx,osrt \
  --sample=none \
  --cpuctxsw=none \
  --output="${report_base}" \
  "${gpu_python}" -m agentsys.gpu_runtime \
  --run-id "${run_id}" \
  --output-dir "${run_dir}/nsight-runtime" \
  --disable-torch-profiler \
  2>&1 | tee "${run_dir}/nsight-profile.log"

for report in cuda_gpu_kern_sum cuda_api_sum cuda_gpu_mem_time_sum; do
  nsys stats \
    --force-export=true \
    --force-overwrite=true \
    --report "${report}" \
    --format csv \
    --output "${run_dir}/nsight-stats" \
    "${report_base}.nsys-rep"
done

"${gpu_python}" -m agentsys.gpu_runtime_audit \
  --run-id "${run_id}" \
  --run-dir "${run_dir}"

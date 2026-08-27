#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gpu_python="${project_root}/.venv-gpu/bin/python"
run_id=${1:-run_041}
plan=${2:-"${project_root}/artifacts/hybrid_reproduction/run_040/workloads/react_tool/hybrid-plan.json"}
output_dir="${project_root}/artifacts/hybrid_profile/${run_id}"
report_base="${output_dir}/react-tool"

mkdir -p "${output_dir}"
cd "${project_root}"

nsys profile \
  --force-overwrite=true \
  --trace=cuda,nvtx,osrt \
  --sample=none \
  --cpuctxsw=none \
  --output="${report_base}" \
  "${gpu_python}" -m agentsys.hybrid_runtime \
  --plan "${plan}" \
  --output-dir "${output_dir}/native" \
  2>&1 | tee "${output_dir}/profile.log"

for report in cuda_gpu_kern_sum cuda_api_sum cuda_gpu_mem_time_sum nvtx_sum; do
  nsys stats \
    --force-export=true \
    --force-overwrite=true \
    --report "${report}" \
    --format csv \
    --output "${output_dir}/nsight-stats" \
    "${report_base}.nsys-rep"
done

"${gpu_python}" -m agentsys.hybrid_profile_audit \
  --run-id "${run_id}" \
  --profile-dir "${output_dir}"

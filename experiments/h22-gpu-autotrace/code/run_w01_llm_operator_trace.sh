#!/usr/bin/env bash
# w01 / G01, llm strand — operator-wise end-to-end single-GPU trace with the
# real Qwen3-1.7B model (user-supplied transformers) serving every LLM call.
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
gpu_python="${GPU_PYTHON:-/home/descfly/miniconda3/bin/python}"
runtime="${project_root}/experiments/h22-gpu-autotrace/code/single_gpu_hf_llm_agent_runtime.py"

workload=${1:?usage: run_w01_llm_operator_trace.sh <workload> [plan]}
plan=${2:-"${project_root}/artifacts/hybrid_reproduction/run_040/workloads/${workload}/hybrid-plan.json"}

DEVICE=${DEVICE:-1}
NUMA_NODE=${NUMA_NODE:-1}
CPU_AFFINITY=${CPU_AFFINITY:-16-31,48-63}
WARMUP_ITERS=${WARMUP_ITERS:-2}
MEASURED_ITERS=${MEASURED_ITERS:-3}
STRAND=${STRAND:-llm}
MODEL_DIR=${MODEL_DIR:-/data3/docker_model/AgentSys/Qwen3-1.7B}

output_dir="${project_root}/artifacts/gpu_autotrace/${STRAND}/g01_operator_trace/${workload}"
report_base="${output_dir}/${workload}_single_gpu"

mkdir -p "${output_dir}"
cd "${project_root}"

nsys profile \
  --force-overwrite=true \
  --trace=cuda,nvtx,osrt \
  --sample=none \
  --cpuctxsw=none \
  --output="${report_base}" \
  "${gpu_python}" "${runtime}" \
  --plan "${plan}" \
  --model-dir "${MODEL_DIR}" \
  --output-dir "${output_dir}/native" \
  --device "${DEVICE}" \
  --numa-node "${NUMA_NODE}" \
  --cpu-affinity "${CPU_AFFINITY}" \
  --warmup-iters "${WARMUP_ITERS}" \
  --measured-iters "${MEASURED_ITERS}" \
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

echo "w01 llm complete: ${output_dir}"

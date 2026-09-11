#!/usr/bin/env bash
# w03 / G04 — Nsight Compute hardware attributes for the representative
# operator kernels. Rows are indexed by the w02 kernel launch order; NCU replay
# time is never used as latency. One measured iteration is profiled after
# warmup, selected by the NVTX phase range so warmup kernels are excluded.
#
# Representative set: react_tool covers matrix 768, planner_debate covers 896
# and 1024. Together they cover every (op_type, matrix_size) that appears in
# react_moa_mcts, so w04 can map every target operator to a profiled family.
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
gpu_python="${project_root}/.venv-gpu/bin/python"
runtime="${project_root}/experiments/h22-gpu-autotrace/code/single_gpu_agent_runtime.py"

workload=${1:?usage: run_w03_ncu_representative.sh <workload>}
plan=${2:-"${project_root}/artifacts/hybrid_reproduction/run_040/workloads/${workload}/hybrid-plan.json"}
DEVICE=${DEVICE:-1}
NUMA_NODE=${NUMA_NODE:-1}
CPU_AFFINITY=${CPU_AFFINITY:-16-31,48-63}
WARMUP_ITERS=${WARMUP_ITERS:-3}

output_dir="${project_root}/artifacts/gpu_autotrace/g04_ncu_hardware/${workload}"
mkdir -p "${output_dir}"
cd "${project_root}"

ncu \
  --nvtx --nvtx-include "regex:agentsys.autotrace::phase=measured::iter=0/" \
  --section SpeedOfLight \
  --section ComputeWorkloadAnalysis \
  --section MemoryWorkloadAnalysis \
  --section Occupancy \
  --section LaunchStats \
  --section WarpStateStats \
  --section SchedulerStats \
  --metrics gpu__time_duration.sum,dram__bytes_read.sum,dram__bytes_write.sum,lts__t_sector_hit_rate.pct,sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active,sm__inst_executed_pipe_tensor.sum,smsp__inst_executed.sum,launch__waves_per_multiprocessor \
  --print-nvtx-rename kernel \
  -f -o "${output_dir}/${workload}_measured_iter0" \
  "${gpu_python}" "${runtime}" \
  --plan "${plan}" \
  --output-dir "${output_dir}/native" \
  --device "${DEVICE}" \
  --numa-node "${NUMA_NODE}" \
  --cpu-affinity "${CPU_AFFINITY}" \
  --warmup-iters "${WARMUP_ITERS}" \
  --measured-iters 1 \
  2>&1 | tee "${output_dir}/ncu.log"

ncu -i "${output_dir}/${workload}_measured_iter0.ncu-rep" --csv --page raw > "${output_dir}/${workload}_ncu_raw.csv"
ncu -i "${output_dir}/${workload}_measured_iter0.ncu-rep" --csv --page details > "${output_dir}/${workload}_ncu_details.csv"
echo "w03 complete: ${output_dir}"

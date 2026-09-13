#!/usr/bin/env bash
# w03 / G04, llm_vl strand — NCU per-call short sessions (crash containment).
# Each LLM call of the reduced plan is profiled in its own NCU session with
# warmup NVTX suppressed, so a profiler failure loses one call, not the run.
set -uo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
gpu_python="${GPU_PYTHON:-/home/descfly/miniconda3/bin/python}"
runtime="${project_root}/experiments/h22-gpu-autotrace/code/single_gpu_hf_llm_agent_runtime.py"
MODEL_DIR="${MODEL_DIR:?set MODEL_DIR}"
STRAND="${STRAND:-llm_vl}"

workload=${1:?usage: run_w03_vl_ncu_per_call.sh <workload> <call_id...>}
shift
plan="${project_root}/artifacts/gpu_autotrace/${STRAND}/ncu_plans/${workload}/hybrid-plan.json"
outroot="${project_root}/artifacts/gpu_autotrace/${STRAND}/g04_ncu_hardware/${workload}"
cd "${project_root}"

fail=0
for call in "$@"; do
  outdir="${outroot}/call_${call}"
  mkdir -p "${outdir}"
  echo "=== NCU session for ${workload}/${call} $(date -u +%H:%M:%S)"
  AGENTSYS_NVTX_MEASURED_ONLY=1 ncu \
    --nvtx --nvtx-include "regex:agentsys.mllm::${call}::/" \
    --section SpeedOfLight --section MemoryWorkloadAnalysis --section Occupancy \
    --metrics gpu__time_duration.sum,dram__bytes_read.sum,dram__bytes_write.sum,lts__t_sector_hit_rate.pct,sm__pipe_tensor_cycles_active.avg.pct_of_peak_sustained_active,sm__inst_executed_pipe_tensor.sum,smsp__inst_executed.sum,launch__waves_per_multiprocessor,launch__registers_per_thread \
    --print-nvtx-rename kernel \
    -f -o "${outdir}/${call}_measured_iter0" \
    "${gpu_python}" "${runtime}" \
    --plan "${plan}" --model-dir "${MODEL_DIR}" \
    --output-dir "${outdir}/native" \
    --device "${DEVICE:-1}" --numa-node "${NUMA_NODE:-1}" --cpu-affinity "${CPU_AFFINITY:-16-31,48-63}" \
    --warmup-iters 2 --measured-iters 1 \
    > "${outdir}/ncu.log" 2>&1
  ec=$?
  n=$(grep -c "==PROF== Profiling" "${outdir}/ncu.log" || true)
  echo "session ${call}: exit=${ec} kernels=${n}"
  if [ "${ec}" -eq 0 ] && [ "${n}" -gt 0 ]; then
    ncu -i "${outdir}/${call}_measured_iter0.ncu-rep" --csv --page raw > "${outdir}/${call}_ncu_raw.csv" \
      && echo "raw ok ${call}" || { echo "RAW_FAIL ${call}"; fail=1; }
  else
    echo "SESSION_FAIL ${call}"; fail=1
  fi
done
exit ${fail}

#!/usr/bin/env bash
# AutoTrace w01', serving adaptation: nsys capture of one Agentix-protocol run.
#
# Captures the whole process tree: the client harness (client-side NVTX marks per
# request window) and the vLLM EngineCore worker (layerwise NVTX module markers
# when --enable-layerwise-nvtx-tracing is on). Worker-side markers own their
# kernel launches, so operator-level attribution keeps AutoTrace's launch-ownership
# rule inside the worker; request-level attribution is by window intersection and
# is reported as such (continuous batching shares one forward across requests).
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)
venv_python="${VENV_PYTHON:-${project_root}/.venv-vllm/bin/python}"
runtime="${project_root}/experiments/h23-agentix-8b/code/serve_agentix.py"

workload=${1:?usage: run_nsys_serving.sh <workload.json> <policy> [tag]}
policy=${2:?policy}
tag=${3:-"${policy}"}
DEVICE=${DEVICE:-1}

out="${project_root}/artifacts/agentix_8b/autotrace/${tag}"
mkdir -p "${out}"
cd "${project_root}"

# VLLM_ENABLE_V1_MULTIPROCESSING=0 keeps the EngineCore inside the profiled
# process; with the default multiprocessing engine the serving CUDA work runs in
# a child that the capture did not record (verified: CUDA activity stopped after
# warm-up while requests kept being served).
CUDA_VISIBLE_DEVICES=${DEVICE} VLLM_ENABLE_V1_MULTIPROCESSING=0 nsys profile \
  --force-overwrite=true \
  --trace=cuda,nvtx,osrt \
  --sample=none \
  --cpuctxsw=none \
  --trace-fork-before-exec=true \
  --output="${out}/${tag}" \
  "${venv_python}" "${runtime}" \
    --workload "${workload}" \
    --policy "${policy}" \
    --nvtx \
    --enable-layerwise-nvtx-tracing \
    --output-dir "${out}/run" \
  > "${out}/profile.log" 2>&1

nsys stats --force-export=true --force-overwrite=true --report cuda_gpu_kern_sum --format csv \
  --output "${out}/nsight-stats" "${out}/${tag}.nsys-rep"
echo "nsys capture complete: ${out}"

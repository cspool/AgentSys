#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
mllm_root="${project_root}/.references/mllm"
gpu_python="${project_root}/.venv-gpu/bin/python"
micromamba="${project_root}/.tools/micromamba"
micromamba_root="${project_root}/.tools/micromamba-root"
cuda_prefix="${project_root}/.cuda-toolkit"
shutdown_patch="${project_root}/integrations/mllm/patches/cuda-shutdown-order.patch"
micromamba_url="https://github.com/mamba-org/micromamba-releases/releases/download/2.8.1-0/micromamba-linux-64"
micromamba_sha="9689782d863c05a1bf5d2d371ba527104e7a4eb4310c1637d8653b751aed9c82"

test "$(git -C "${mllm_root}" rev-parse HEAD)" = \
  "50ad5a9b6fbea742e38b5b31776c187e50319c8e"
test "$("${gpu_python}" -c 'import importlib.metadata; print(importlib.metadata.version("nvidia-cuda-nvcc-cu12"))')" = \
  "12.8.93"

git -C "${mllm_root}" submodule update --init --checkout \
  mllm/backends/cuda/vendors/cccl \
  mllm/backends/cuda/vendors/cutlass

if git -C "${mllm_root}" apply --reverse --check "${shutdown_patch}" 2>/dev/null; then
  : # Exact patch is already applied.
else
  git -C "${mllm_root}" apply --check "${shutdown_patch}"
  git -C "${mllm_root}" apply "${shutdown_patch}"
fi

nvcc_path=${CUDACXX:-}
if [[ -z ${nvcc_path} ]]; then
  nvcc_path=$(command -v nvcc || true)
fi
if [[ -z ${nvcc_path} && -x ${cuda_prefix}/bin/nvcc ]]; then
  nvcc_path="${cuda_prefix}/bin/nvcc"
fi
if [[ -z ${nvcc_path} || ! -x ${nvcc_path} ]]; then
  mkdir -p "$(dirname "${micromamba}")" "${project_root}/artifacts/gpu_runtime"
  if [[ ! -x ${micromamba} ]]; then
    curl -fL "${micromamba_url}" -o "${micromamba}"
    chmod +x "${micromamba}"
  fi
  echo "${micromamba_sha}  ${micromamba}" | sha256sum --check
  test "$("${micromamba}" --version)" = "2.8.1"
  "${micromamba}" --root-prefix "${micromamba_root}" create --yes \
    --prefix "${cuda_prefix}" \
    --channel nvidia/label/cuda-12.8.1 \
    --channel conda-forge \
    --strict-channel-priority \
    'cuda-nvcc=12.8.93' \
    'cuda-cudart-dev=12.8.90' \
    'cuda-nvml-dev'
  "${micromamba}" --root-prefix "${micromamba_root}" list \
    --prefix "${cuda_prefix}" --explicit \
    > "${project_root}/artifacts/gpu_runtime/cuda-conda-explicit.txt"
  "${micromamba}" --root-prefix "${micromamba_root}" list \
    --prefix "${cuda_prefix}" --json \
    > "${project_root}/artifacts/gpu_runtime/cuda-conda-packages.json"
  nvcc_path="${cuda_prefix}/bin/nvcc"
fi

cuda_root=$(cd "$(dirname "${nvcc_path}")/.." && pwd)
env \
  PATH="${project_root}/.venv/bin:$(dirname "${nvcc_path}"):/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
  CC=clang-16 \
  CXX=clang++-16 \
  CUDACXX="${nvcc_path}" \
  cmake -S "${mllm_root}" -B "${mllm_root}/build-x86-cuda" -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_C_COMPILER=clang-16 \
    -DCMAKE_CXX_COMPILER=clang++-16 \
    -DCMAKE_CUDA_HOST_COMPILER=clang++-16 \
    -DCMAKE_SHARED_LINKER_FLAGS="-L${cuda_root}/targets/x86_64-linux/lib/stubs" \
    -DCMAKE_EXE_LINKER_FLAGS="-L${cuda_root}/targets/x86_64-linux/lib/stubs" \
    -DCMAKE_CUDA_ARCHITECTURES=89 \
    -DCUDAToolkit_ROOT="${cuda_root}" \
    -DMLLM_BUILD_CUDA_BACKEND=ON \
    -DMLLM_ENABLE_TEST=ON \
    -DMLLM_ENABLE_BENCHMARK=OFF \
    -DMLLM_ENABLE_EXAMPLE=OFF \
    -DMLLM_ENABLE_TOOLS=ON \
    -DMLLM_BUILD_EXT_OP_SET=OFF \
    -DMLLM_BUILD_EXT_OP_SET_TEST=OFF \
    -DHWY_ENABLE_TESTS=OFF \
    -DHWY_ENABLE_EXAMPLES=OFF \
    -DHWY_ENABLE_CONTRIB=OFF \
    -DMLLM_CPU_BACKEND_COMPILE_OPTIONS=-march=native \
    -DMLLM_KERNEL_USE_THREADS=ON \
    -DMLLM_KERNEL_THREADS_VENDOR_OPENMP=OFF

for target in MllmCUDABackendCudaOps MllmCUDABackend Mllm-Test-CUDA-DeviceInfo; do
  cmake --build "${mllm_root}/build-x86-cuda" --target "${target}"
done

env \
  LD_LIBRARY_PATH="${mllm_root}/build-x86-cuda/bin:${cuda_root}/lib:${cuda_root}/targets/x86_64-linux/lib" \
  stdbuf -oL -eL "${mllm_root}/build-x86-cuda/bin/Mllm-Test-CUDA-DeviceInfo"

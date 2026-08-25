#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
reference_root="${project_root}/.references"
mkdir -p "${reference_root}"

clone_pinned() {
  local name=$1
  local url=$2
  local commit=$3
  local target="${reference_root}/${name}"
  if [[ ! -d "${target}/.git" ]]; then
    git clone --filter=blob:none --no-checkout "${url}" "${target}"
    git -C "${target}" fetch --depth 1 origin "${commit}"
    git -C "${target}" checkout --detach "${commit}"
  fi
  local observed
  observed=$(git -C "${target}" rev-parse HEAD)
  if [[ "${observed}" != "${commit}" ]]; then
    echo "Reference ${name} commit mismatch: ${observed} (expected ${commit})" >&2
    exit 2
  fi
  echo "${name}: ${observed}"
}

clone_pinned MLX_dev_sys https://github.com/cspool/MLX_dev.git \
  b3a6d59f2ed634ea6181f5a29f3fa96281b1f384
clone_pinned LLM.xpu https://github.com/xinming-wei/LLM.xpu.git \
  689be270aa29bb88447e3867cd97d85a55f454d5
clone_pinned HPTPE https://github.com/wqzustc/High-Performance-Tensor-Processing-Engines.git \
  ebe4db7d2d3c36d10c47683d7689f65f5c4ca3e4
clone_pinned mllm https://github.com/UbiquitousLearning/mllm.git \
  50ad5a9b6fbea742e38b5b31776c187e50319c8e
clone_pinned ramulator2 https://github.com/CMU-SAFARI/ramulator2.git \
  be93be78055d922aa1d4d33e15bcc8f2b0c61a9d


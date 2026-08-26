#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MLLM_ROOT="${PROJECT_ROOT}/.references/mllm"
LOCKED_BIN="${PROJECT_ROOT}/.venv/bin"
BUILD_CONFIG="${PROJECT_ROOT}/experiments/h13-revised-stack/mllm-build-clang16.yaml"

test -x "${LOCKED_BIN}/cmake"
test -x "${LOCKED_BIN}/ninja"
test "$(git -C "${MLLM_ROOT}" rev-parse HEAD)" = "50ad5a9b6fbea742e38b5b31776c187e50319c8e"

# The pinned KleidiAI commit is mirrored by Arm on GitHub. This avoids the
# GitLab endpoint's TLS incompatibility in the project container without
# changing .gitmodules or the pinned revision.
git -C "${MLLM_ROOT}" config \
  submodule.mllm/backends/cpu/vendors/kleidiai.url \
  https://github.com/ARM-software/kleidiai.git
git -C "${MLLM_ROOT}" -c http.version=HTTP/1.1 submodule update --init --recursive \
  third_party/fmt \
  third_party/flatbuffers \
  third_party/googletest \
  third_party/benchmark \
  mllm/ffi/vendors/tvm-ffi \
  mllm/backends/cpu/vendors/kleidiai

env \
  PATH="${LOCKED_BIN}:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" \
  CC=clang-16 \
  CXX=clang++-16 \
  uv run --no-project --isolated --with 'pyyaml>=6.0.2' \
  python "${MLLM_ROOT}/task.py" "${BUILD_CONFIG}"

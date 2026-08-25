#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
source_root="${project_root}/.references/ramulator2"
expected_commit=be93be78055d922aa1d4d33e15bcc8f2b0c61a9d

if [[ ! -d "${source_root}/.git" ]]; then
  git clone --depth 1 --branch v2.0a https://github.com/CMU-SAFARI/ramulator2.git "${source_root}"
fi
observed=$(git -C "${source_root}" rev-parse HEAD)
if [[ "${observed}" != "${expected_commit}" ]]; then
  echo "Ramulator2 commit mismatch: ${observed}" >&2
  exit 2
fi
if ! command -v clang++-16 >/dev/null; then
  echo "clang++-16 is required to build pinned Ramulator2 v2.0a" >&2
  exit 2
fi

CC=clang-16 CXX=clang++-16 "${project_root}/.venv/bin/cmake" \
  -S "${source_root}" -B "${source_root}/build-clang" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release
"${project_root}/.venv/bin/cmake" --build "${source_root}/build-clang" -j4

echo "Built Ramulator2 ${observed}: ${source_root}/build-clang/ramulator2"


#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_ROOT="${PROJECT_ROOT}/.references/verilator5"
EXPECTED_COMMIT="848d926ebd4addacacd294dc84e35d9d4ae8078c"

if [[ ! -d "${SOURCE_ROOT}/.git" ]]; then
  git clone --depth 1 --branch v5.050 https://github.com/verilator/verilator.git "${SOURCE_ROOT}"
fi
test "$(git -C "${SOURCE_ROOT}" rev-parse HEAD)" = "${EXPECTED_COMMIT}"

for tool in autoconf flex bison g++ make; do
  command -v "${tool}" >/dev/null
done

if [[ ! -f "${SOURCE_ROOT}/src/Makefile" ]]; then
  (
    cd "${SOURCE_ROOT}"
    autoconf
    ./configure --prefix="${PROJECT_ROOT}/.tools/verilator-5.050"
  )
fi

make -C "${SOURCE_ROOT}/src" -j "${HPTPE_BUILD_JOBS:-4}" opt
env VERILATOR_ROOT="${SOURCE_ROOT}" "${SOURCE_ROOT}/bin/verilator" --version

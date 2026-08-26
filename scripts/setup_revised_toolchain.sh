#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
chipyard_root=${CHIPYARD_ROOT:-/root/chipyard}
jobs=${AGENTSYS_JOBS:-4}
verify_only=0

if [[ ${1:-} == "--verify-only" ]]; then
  verify_only=1
elif [[ $# -ne 0 ]]; then
  echo "usage: $0 [--verify-only]" >&2
  exit 2
fi

cd "${project_root}"

if [[ ${verify_only} -eq 0 ]]; then
  command -v uv >/dev/null
  command -v clang++-16 >/dev/null
  command -v iverilog >/dev/null
  test -f "${chipyard_root}/env.sh"

  uv python install 3.11
  uv sync --frozen
  bash scripts/bootstrap_references.sh
  bash scripts/build_verilator5.sh
  bash scripts/build_mllm_native.sh
  bash scripts/install_revised_chipyard.sh "${chipyard_root}"
  "${project_root}/.venv/bin/python" scripts/compile_revised_system_trace.py --run-id run_028
  make -C system_sim/software -j"${jobs}" CHIPYARD_ROOT="${chipyard_root}" all

  set +u
  source "${chipyard_root}/env.sh"
  set -u
  make -C "${chipyard_root}/sims/verilator" -j"${jobs}" CONFIG=AgentSysRevisedStaticRocketConfig
  make -C "${chipyard_root}/sims/verilator" -j"${jobs}" CONFIG=AgentSysRevisedDynamicRocketConfig
fi

"${project_root}/.venv/bin/python" -m agentsys.toolchain \
  --config "${project_root}/config/revised-toolchain.json" \
  --level built \
  --output "${project_root}/artifacts/tmp/revised-toolchain-built-check.json"

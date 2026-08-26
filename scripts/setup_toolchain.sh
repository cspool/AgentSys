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
  command -v uv >/dev/null || {
    echo "uv is required to create the pinned Python environment" >&2
    exit 2
  }
  uv python install 3.11
  uv sync --frozen

  bash scripts/bootstrap_references.sh
  AGENTSYS_JOBS="${jobs}" bash scripts/build_ramulator2.sh
  bash scripts/install_agentsys_chipyard.sh "${chipyard_root}"
  "${project_root}/.venv/bin/python" scripts/compile_agent_system_trace.py
  make -C system_sim/software -j"${jobs}" CHIPYARD_ROOT="${chipyard_root}" all

  if [[ ! -f "${chipyard_root}/env.sh" ]]; then
    echo "Chipyard environment file not found: ${chipyard_root}/env.sh" >&2
    exit 2
  fi
  set +u
  source "${chipyard_root}/env.sh"
  set -u
  make -C "${chipyard_root}/sims/verilator" -j"${jobs}" CONFIG=AgentSysStaticRocketConfig
  make -C "${chipyard_root}/sims/verilator" -j"${jobs}" CONFIG=AgentSysDynamicRocketConfig
fi

"${project_root}/.venv/bin/python" -m agentsys.toolchain \
  --level built \
  --output "${project_root}/artifacts/tmp/toolchain-built-check.json"

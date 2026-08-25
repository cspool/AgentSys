#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
chipyard_root=${1:-/root/chipyard}
expected_commit=b5d013190d637e634113cb5179f8c8885df1945a

if [[ ! -d "${chipyard_root}/generators/chipyard/src/main" ]]; then
  echo "Chipyard source tree not found: ${chipyard_root}" >&2
  exit 2
fi
observed_commit=$(git -C "${chipyard_root}" rev-parse HEAD)
if [[ "${observed_commit}" != "${expected_commit}" ]]; then
  echo "Chipyard commit mismatch: ${observed_commit} (expected ${expected_commit})" >&2
  exit 2
fi

apply_compatibility_patch() {
  local repository=$1
  local patch_path=$2
  if git -C "${repository}" apply --check "${patch_path}" 2>/dev/null; then
    git -C "${repository}" apply "${patch_path}"
  elif git -C "${repository}" apply --reverse --check "${patch_path}" 2>/dev/null; then
    return 0
  else
    echo "Compatibility patch does not match ${repository}: ${patch_path}" >&2
    exit 2
  fi
}

apply_compatibility_patch \
  "${chipyard_root}/tools/chisel3" \
  "${project_root}/patches/chipyard/chisel3-stable-deps.patch"
apply_compatibility_patch \
  "${chipyard_root}/tools/treadle" \
  "${project_root}/patches/chipyard/treadle-stable-firrtl.patch"

install_if_changed() {
  local source=$1
  local target=$2
  if [[ ! -f "${target}" ]] || ! cmp -s "${source}" "${target}"; then
    install -D -m 0644 "${source}" "${target}"
  fi
}

scala_target="${chipyard_root}/generators/chipyard/src/main/scala/AgentSysRoCC.scala"
vsrc_target="${chipyard_root}/generators/chipyard/src/main/resources/vsrc"
install_if_changed "${project_root}/system_sim/chipyard/AgentSysRoCC.scala" "${scala_target}"

rtl_files=(
  agentsys_engines.sv
  agentsys_tisa_scheduler.sv
  agentsys_rocc_controller.sv
)
for rtl_file in "${rtl_files[@]}"; do
  install_if_changed \
    "${project_root}/rtl/agentsys/${rtl_file}" \
    "${vsrc_target}/${rtl_file}"
done

echo "Installed AgentSys Chipyard integration at ${observed_commit}"
echo "  Scala: ${scala_target}"
echo "  RTL resources: ${#rtl_files[@]} files in ${vsrc_target}"


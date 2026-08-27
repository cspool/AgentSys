#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
source "${project_root}/scripts/chipyard_paths.sh"
source_root="${project_root}/.references/MLX_dev_active"
chipyard_root=${1:-$(agentsys_chipyard_root "${project_root}")}
export AGENTSYS_CHIPYARD_ROOT=${chipyard_root}

bash "${project_root}/scripts/setup_mlx_active.sh"
agentsys_require_chipyard_source "${chipyard_root}"

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
  "${source_root}/patches/chipyard/chisel3-stable-deps.patch"
apply_compatibility_patch \
  "${chipyard_root}/tools/treadle" \
  "${source_root}/patches/chipyard/treadle-stable-firrtl.patch"

install_if_changed() {
  local source=$1
  local target=$2
  if [[ ! -f ${target} ]] || ! cmp -s "${source}" "${target}"; then
    install -D -m 0644 "${source}" "${target}"
  fi
}

installed_root="${chipyard_root}/generators/chipyard/src/main"
install_if_changed \
  "${source_root}/system_sim/chipyard/MLXRoCC.scala" \
  "${installed_root}/scala/MLXRoCC.scala"
for name in \
  mlx_fp16.sv mlx_fu.sv mlx_register_file.sv mlx_tag_buffer.sv \
  mlx_config_network.sv mlx_data_network.sv mlx_control_logic.sv \
  mlx_pe_top.sv mlx_array_4x4.sv mlx_cycle_model.sv mlx_rocc_controller.sv; do
  install_if_changed \
    "${source_root}/rtl/mlx/${name}" \
    "${installed_root}/resources/vsrc/${name}"
done

cmp "${source_root}/system_sim/chipyard/MLXRoCC.scala" \
  "${installed_root}/scala/MLXRoCC.scala"
for name in \
  mlx_fp16.sv mlx_fu.sv mlx_register_file.sv mlx_tag_buffer.sv \
  mlx_config_network.sv mlx_data_network.sv mlx_control_logic.sv \
  mlx_pe_top.sv mlx_array_4x4.sv mlx_cycle_model.sv mlx_rocc_controller.sv; do
  cmp "${source_root}/rtl/mlx/${name}" \
    "${installed_root}/resources/vsrc/${name}"
done

echo "AgentSys MLX Chipyard overlay verified: 12/12 files"

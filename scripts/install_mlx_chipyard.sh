#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
source_root="${project_root}/.references/MLX_dev_active"
chipyard_root=${1:-/root/chipyard}

bash "${project_root}/scripts/setup_mlx_active.sh"
bash "${source_root}/scripts/install_mlx_chipyard.sh" "${chipyard_root}"

installed_root="${chipyard_root}/generators/chipyard/src/main"
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

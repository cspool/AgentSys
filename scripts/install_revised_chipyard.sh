#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
chipyard_root=${1:-/root/chipyard}
hptpe_root="${project_root}/.references/HPTPE"
expected_chipyard=b5d013190d637e634113cb5179f8c8885df1945a
expected_hptpe=ebe4db7d2d3c36d10c47683d7689f65f5c4ca3e4

test "$(git -C "${chipyard_root}" rev-parse HEAD)" = "${expected_chipyard}"
test "$(git -C "${hptpe_root}" rev-parse HEAD)" = "${expected_hptpe}"

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

scala_root="${chipyard_root}/generators/chipyard/src/main/scala"
vsrc_root="${chipyard_root}/generators/chipyard/src/main/resources/vsrc"
install_if_changed \
  "${project_root}/system_sim/chipyard/AgentSysRevisedRoCC.scala" \
  "${scala_root}/AgentSysRevisedRoCC.scala"
install_if_changed \
  "${project_root}/rtl/agentsys/agentsys_revised_engines.sv" \
  "${vsrc_root}/agentsys_revised_engines.sv"
install_if_changed \
  "${project_root}/rtl/agentsys/agentsys_tisa_scheduler.sv" \
  "${vsrc_root}/agentsys_tisa_scheduler.sv"
install_if_changed \
  "${project_root}/rtl/agentsys/agentsys_revised_rocc_controller.sv" \
  "${vsrc_root}/agentsys_revised_rocc_controller.sv"

hptpe_sources=(
  "OPT1/systolic_array_os/array_opt1_based/sim/timescale.sv:hptpe_timescale.sv"
  "OPT1/systolic_array_os/array_opt1_based/booth_partial_product_generator_pp1.v:hptpe_booth_pp1.v"
  "OPT1/systolic_array_os/array_opt1_based/booth_partial_product_generator.v:hptpe_booth_pp.v"
  "OPT1/systolic_array_os/array_opt1_based/booth_pp_gen.v:hptpe_booth_gen.v"
  "OPT1/systolic_array_os/array_opt1_based/DW02_tree.sv:hptpe_dw02_tree.sv"
  "OPT1/systolic_array_os/array_opt1_based/get_pipline_mulwidth.v:hptpe_pipeline.v"
  "OPT1/systolic_array_os/array_opt1_based/inv_conveter_8.v:hptpe_inv_converter.v"
  "OPT1/systolic_array_os/array_opt1_based/inv_unit_nor_out.v:hptpe_inv_unit_nor.v"
  "OPT1/systolic_array_os/array_opt1_based/inv_unit.v:hptpe_inv_unit.v"
  "OPT1/systolic_array_os/array_opt1_based/opt1_mac.v:hptpe_opt1_mac.v"
  "OPT1/systolic_array_os/array_opt1_based/pe.v:hptpe_pe.v"
  "OPT1/systolic_array_os/array_opt1_based/top.v:hptpe_top.v"
)
for mapping in "${hptpe_sources[@]}"; do
  source_name=${mapping%%:*}
  target_name=${mapping##*:}
  install_if_changed "${hptpe_root}/${source_name}" "${vsrc_root}/${target_name}"
done

echo "Installed revised ordinary-RISC-V + TISA/HPTPE integration"
echo "  Chipyard: ${expected_chipyard}"
echo "  HPTPE: ${expected_hptpe}"
echo "  HPTPE resources: ${#hptpe_sources[@]}"

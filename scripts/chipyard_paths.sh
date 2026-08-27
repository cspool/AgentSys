#!/usr/bin/env bash

AGENTSYS_CHIPYARD_COMMIT=b5d013190d637e634113cb5179f8c8885df1945a

agentsys_chipyard_root() {
  local project_root=$1
  local selected=${AGENTSYS_CHIPYARD_ROOT:-${project_root}/chipyard}
  realpath -m "${selected}"
}

agentsys_chipyard_commit() {
  local chipyard_root=$1
  local git_top
  git_top=$(git -C "${chipyard_root}" rev-parse --show-toplevel 2>/dev/null || true)
  if [[ -n ${git_top} ]] && \
     [[ $(realpath -m "${git_top}") == $(realpath -m "${chipyard_root}") ]]; then
    git -C "${chipyard_root}" rev-parse HEAD
    return
  fi
  local marker=${chipyard_root}/.agentsys-source.json
  if [[ ! -f ${marker} ]]; then
    return 1
  fi
  sed -n 's/.*"upstream_commit": "\([0-9a-f]\{40\}\)".*/\1/p' "${marker}"
}

agentsys_require_chipyard_source() {
  local chipyard_root=$1
  local required=(
    build.sbt
    common.mk
    generators/chipyard/src/main/scala/config/RocketConfigs.scala
  )
  local relative
  for relative in "${required[@]}"; do
    if [[ ! -f ${chipyard_root}/${relative} ]]; then
      echo "Chipyard source is incomplete: ${chipyard_root}/${relative}" >&2
      return 2
    fi
  done
  local observed
  observed=$(agentsys_chipyard_commit "${chipyard_root}" || true)
  if [[ ${observed} != ${AGENTSYS_CHIPYARD_COMMIT} ]]; then
    echo "Chipyard identity mismatch: ${observed:-missing} (expected ${AGENTSYS_CHIPYARD_COMMIT})" >&2
    return 2
  fi
}

agentsys_require_chipyard_build() {
  local chipyard_root=$1
  agentsys_require_chipyard_source "${chipyard_root}"
  local required=(
    generators/rocket-chip/src/main/scala/rocket/RocketCore.scala
    tools/chisel3/build.sbt
    tools/treadle/build.sbt
    env.sh
    esp-tools-install/bin/riscv64-unknown-elf-gcc
  )
  local relative
  for relative in "${required[@]}"; do
    if [[ ! -f ${chipyard_root}/${relative} ]]; then
      echo "Chipyard build prerequisite is missing: ${chipyard_root}/${relative}" >&2
      return 3
    fi
  done
}

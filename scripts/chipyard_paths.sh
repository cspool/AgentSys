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

  local project_root
  project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
  local contract_marker=${project_root}/chipyard/.agentsys-source.json
  if [[ ! -f ${contract_marker} ]]; then
    echo "AgentSys Chipyard build-closure marker is missing: ${contract_marker}" >&2
    return 3
  fi

  local expected observed changed allowed
  while IFS=$'\t' read -r relative expected; do
    observed=$(git -C "${chipyard_root}/${relative}" rev-parse HEAD 2>/dev/null || true)
    if [[ ${observed} != ${expected} ]]; then
      echo "Chipyard gitlink mismatch: ${relative} ${observed:-missing} != ${expected}" >&2
      return 3
    fi
    changed=$(git -C "${chipyard_root}/${relative}" diff --name-only HEAD --)
    allowed=
    if [[ ${relative} == tools/chisel3 || ${relative} == tools/treadle ]]; then
      allowed=build.sbt
    fi
    if [[ ${changed} != ${allowed} ]]; then
      echo "Unexpected tracked Chipyard gitlink changes: ${relative}: ${changed:-none}" >&2
      return 3
    fi
  done < <(python3 - "${contract_marker}" <<'PY'
import json
import sys

marker = json.load(open(sys.argv[1], encoding="utf-8"))
for path, commit in marker["build_gitlinks"].items():
    print(f"{path}\t{commit}")
PY
  )

  while IFS=$'\t' read -r relative expected; do
    observed=$(sha256sum "${chipyard_root}/${relative}" 2>/dev/null | awk '{print $1}')
    if [[ ${observed} != ${expected} ]]; then
      echo "Chipyard patched-file mismatch: ${relative} ${observed:-missing} != ${expected}" >&2
      return 3
    fi
  done < <(python3 - "${contract_marker}" <<'PY'
import json
import sys

marker = json.load(open(sys.argv[1], encoding="utf-8"))
for path, digest in marker["patched_files"].items():
    print(f"{path}\t{digest}")
PY
  )
}

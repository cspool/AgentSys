#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
source "${project_root}/scripts/chipyard_paths.sh"
chipyard_root=$(agentsys_chipyard_root "${project_root}")
export AGENTSYS_CHIPYARD_ROOT=${chipyard_root}
target="${project_root}/.references/MLX_dev_active"
url="https://github.com/cspool/MLX_dev.git"
commit="2a457dfaf8faf9bcda72f92c5d66e9a6a9b3b50f"

mkdir -p "${project_root}/.references"
if [[ ! -d ${target}/.git ]]; then
  git clone --filter=blob:none --no-checkout "${url}" "${target}"
  git -C "${target}" fetch --depth 1 origin "${commit}"
  git -C "${target}" checkout --detach "${commit}"
fi

observed=$(git -C "${target}" rev-parse HEAD)
if [[ ${observed} != ${commit} ]]; then
  echo "MLX active commit mismatch: ${observed} (expected ${commit})" >&2
  exit 2
fi
if [[ -n $(git -C "${target}" status --porcelain --untracked-files=no) ]]; then
  echo "MLX active checkout has tracked modifications" >&2
  exit 3
fi
agentsys_require_chipyard_source "${chipyard_root}"

echo "MLX active: ${observed}"
echo "Chipyard: $(agentsys_chipyard_commit "${chipyard_root}")"

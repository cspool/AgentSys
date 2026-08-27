#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
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
test "$(git -C /root/chipyard rev-parse HEAD)" = \
  "b5d013190d637e634113cb5179f8c8885df1945a"

echo "MLX active: ${observed}"
echo "Chipyard: $(git -C /root/chipyard rev-parse HEAD)"

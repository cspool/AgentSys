#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
source "${project_root}/scripts/chipyard_paths.sh"
chipyard_root=$(agentsys_chipyard_root "${project_root}")
export AGENTSYS_CHIPYARD_ROOT=${chipyard_root}
mlx_python="${project_root}/.venv-mlx/bin/python"

cd "${project_root}"
bash scripts/setup_mlx_active.sh
if [[ ! -x ${mlx_python} ]]; then
  uv venv --python 3.11 .venv-mlx
fi
uv pip install --python "${mlx_python}" \
  'numpy==2.2.6' 'PyYAML==6.0.2'
uv pip install --python "${mlx_python}" --no-deps -e .

"${mlx_python}" - <<'PY'
import importlib.metadata
import json
import os
import subprocess
from pathlib import Path

chipyard_root = Path(os.environ["AGENTSYS_CHIPYARD_ROOT"])
evidence = {
    "python": subprocess.check_output([".venv-mlx/bin/python", "--version"], text=True).strip(),
    "numpy": importlib.metadata.version("numpy"),
    "pyyaml": importlib.metadata.version("PyYAML"),
    "iverilog": subprocess.check_output(["iverilog", "-V"], text=True, stderr=subprocess.STDOUT).splitlines()[0],
    "verilator": subprocess.check_output(["verilator", "--version"], text=True).strip(),
    "riscv_gcc": subprocess.check_output(
        [str(chipyard_root / "esp-tools-install/bin/riscv64-unknown-elf-gcc"), "--version"],
        text=True,
    ).splitlines()[0],
}
path = Path("artifacts/mlx_environment/environment.json")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(evidence, indent=2, sort_keys=True))
PY

uv pip freeze --python "${mlx_python}" > artifacts/mlx_environment/pip-freeze.txt

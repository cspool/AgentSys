#!/usr/bin/env bash
set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
gpu_python="${project_root}/.venv-gpu/bin/python"
verify_only=0

if [[ ${1:-} == "--verify-only" ]]; then
  verify_only=1
elif [[ $# -ne 0 ]]; then
  echo "usage: $0 [--verify-only]" >&2
  exit 2
fi

cd "${project_root}"
if [[ ${verify_only} -eq 0 ]]; then
  uv venv --python 3.11 .venv-gpu
  uv pip install --python "${gpu_python}" \
    --index-url https://download.pytorch.org/whl/cu128 \
    'torch==2.7.0'
  uv pip install --python "${gpu_python}" \
    'numpy==2.2.6' 'nvidia-ml-py==13.610.43' \
    'nvidia-cuda-nvcc-cu12==12.8.93'
  uv pip install --python "${gpu_python}" --no-deps -e .
fi

"${gpu_python}" - <<'PY'
import importlib.metadata
import json
from pathlib import Path
import torch
import pynvml

assert torch.__version__ == "2.7.0+cu128"
assert torch.version.cuda == "12.8"
assert torch.cuda.is_available() and torch.cuda.device_count() == 2
assert all(torch.cuda.get_device_name(i) == "NVIDIA GeForce RTX 4090" for i in range(2))
pynvml.nvmlInit()
driver = pynvml.nvmlSystemGetDriverVersion()
pynvml.nvmlShutdown()
evidence = {
    "torch": torch.__version__,
    "torch_cuda": torch.version.cuda,
    "nccl": list(torch.cuda.nccl.version()),
    "numpy": importlib.metadata.version("numpy"),
    "nvidia_ml_py": importlib.metadata.version("nvidia-ml-py"),
    "nvidia_cuda_nvcc_cu12": importlib.metadata.version("nvidia-cuda-nvcc-cu12"),
    "driver": driver,
    "devices": [torch.cuda.get_device_name(i) for i in range(2)],
}
path = Path("artifacts/gpu_runtime/environment.json")
path.parent.mkdir(parents=True, exist_ok=True)
path.write_text(json.dumps(evidence, indent=2, sort_keys=True) + "\n")
print(json.dumps(evidence, indent=2, sort_keys=True))
PY

uv pip freeze --python "${gpu_python}" > artifacts/gpu_runtime/pip-freeze.txt

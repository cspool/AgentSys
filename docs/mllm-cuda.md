# mllm CUDA integration

`scripts/setup_mllm_cuda.sh` installs a project-local NVIDIA CUDA 12.8.1
compiler environment, initializes mllm's pinned CCCL/CUTLASS submodules, applies
the audited shutdown-order patch, and builds the upstream CUDA backend plus its
device test. It does not install a driver or change `/usr/local/cuda`.

```bash
bash scripts/setup_gpu_runtime.sh
bash scripts/setup_mllm_cuda.sh
.venv-gpu/bin/agentsys-mllm-cuda-audit \
  --run-id run_039 \
  --nvcc .cuda-toolkit/bin/nvcc \
  --recovery-evidence \
  --setup-log artifacts/logs/mllm-cuda-setup-run_039-second.log
```

The official backend at the pinned commit is incomplete: it supplies CUDA/NVML
device discovery and a CUDA allocator, while its four CUDA translation units
are empty and no CUDA op factories are registered. AgentSys therefore treats
it as lifecycle infrastructure. Workload-aware kernels belong to the separately
labeled MIR-to-CUDA adapter and are not presented as upstream mllm inference.

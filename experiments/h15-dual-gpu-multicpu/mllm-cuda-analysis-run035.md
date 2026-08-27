# H15.2 run-035 analysis — nvcc recovered, upstream CMake option defect

## Outcome

Run 035 is a retained partial result: 9/13 gates pass. The project-local CUDA
compiler recovery works, but the locked minimal mllm configuration exposes an
independent upstream CMake defect before target generation.

## Recovered toolchain

- The SHA-pinned micromamba binary reports 2.8.1.
- The explicit environment contains NVIDIA CUDA 12.8.1-label packages,
  including nvcc 12.8.93 and cudart/NVML development 12.8.90.
- `nvcc --version` reports CUDA 12.8 V12.8.93.
- CMake selects clang/clang++ 16, the project-local nvcc, CUDA architecture 89,
  and `MLLM_BUILD_CUDA_BACKEND=ON`.
- `/usr/local/cuda`, the host package database and driver 595.84 remain
  unchanged.

## New failure

With the preregistered `MLLM_ENABLE_TOOLS=OFF`, mllm's top-level CMake still
executes an unconditional `install(TARGETS mllm-params-inspector ...)` command.
That target is only created when tools are enabled, so configuration stops with
"target mllm-params-inspector does not exist." No CUDA library or device-test
target is generated; the four corresponding gates remain false.

This is not a compiler, GPU, submodule or CUDA-link failure. The compiler/cache,
package-lock, source-boundary and prior-regression gates all pass.

## Next change

Retain run 035 and preregister one configuration-only recovery: enable upstream
tools so its own install target exists. No mllm source, CUDA version, compiler,
architecture, target set or capability claim changes.

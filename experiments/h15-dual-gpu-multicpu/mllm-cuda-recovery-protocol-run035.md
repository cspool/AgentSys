# H15.2 recovery protocol — project-local NVIDIA Conda CUDA toolchain (run 035)

This recovery is locked after retaining run 034 and before downloading
micromamba or any Conda CUDA package.

## Single diagnosis-driven change

Keep the mllm commit, CUDA vendor submodules, CMake options and targets from run
034. Replace only the incomplete Python-wheel compiler path with NVIDIA's
official Conda CUDA 12.8.1 packages in a project-local prefix.

## Fixed dependency contract

- Micromamba release `2.8.1-0`, Linux x86-64 standalone binary, SHA-256
  `9689782d863c05a1bf5d2d371ba527104e7a4eb4310c1637d8653b751aed9c82`.
- Channel: `nvidia/label/cuda-12.8.1`, strict priority; conda-forge may provide
  only package-manager runtime dependencies.
- Requested CUDA packages: `cuda-nvcc=12.8.93`,
  `cuda-cudart-dev=12.8.90`, and `cuda-nvml-dev` from the same CUDA 12.8.1
  label. The explicit environment lock is exported as an artifact.
- Prefixes: `.tools/micromamba` and `.cuda-toolkit`; neither modifies the host
  driver or global package database.
- Host compilers: clang/clang++ 16; target architecture: sm_89.

## Gates

The unchanged eight run-034 gates must all pass. In addition:

1. the downloaded micromamba binary matches the fixed SHA and reports 2.8.1;
2. the Conda environment explicitly resolves only CUDA 12.8-series toolkit
   packages for compiler/runtime/NVML development;
3. the build log records the full configure/build commands and the device test
   reports each distinct local RTX 4090 once;
4. the upstream empty-kernel/no-op-factory boundary remains unchanged;
5. no `/usr/local/cuda`, driver, apt package or global environment is mutated.

Success supports only mllm CUDA backend initialization/toolchain availability.
It does not turn the empty upstream CUDA translation units into full inference;
the workload-aware AgentSys adapter remains a separately labeled H15.3 task.

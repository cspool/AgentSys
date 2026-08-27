# H15.2 run-034 analysis — Python CUDA compiler wheel is incomplete

## Outcome

Run 034 is a retained negative result. Three of eight locked gates pass. The
official NVIDIA `nvidia-cuda-nvcc-cu12==12.8.93` Linux wheel installs ptxas,
NVVM, libdevice and CUDA compiler headers, but it does not install an executable
`nvcc` compiler driver. The setup script therefore stops before CMake rather
than silently using a mismatched compiler.

## Passing evidence

- mllm remains at `50ad5a9b6fbea742e38b5b31776c187e50319c8e`.
- CCCL and CUTLASS were downloaded and exactly match the two protocol commits.
- The upstream implementation boundary is machine-audited: all four CUDA
  kernel `.cu` translation units have zero non-comment lines, and
  `CudaBackend.cpp` registers no op factory. The backend currently supplies
  CUDA/NVML device metadata and a `cudaMalloc` allocator scaffold, not complete
  model operators.
- The earlier mllm native suite remains 20/20 executables and 101 gtests, while
  the five-layer paper matrix remains 68/68 at <=10%.

## Failed gates

`nvcc_12_8`, `cuda_cache`, `three_build_targets`, `two_gpu_device_test` and
`cuda_driver_runtime_nvml_link` fail because there is no compiler front-end and
the build was not configured. These are one root cause, not five independent
implementation defects. The 12.8.93 wheel itself is recorded in the artifact;
the absence of `bin/nvcc` is the observed package content.

## Recovery direction

Use NVIDIA's official Conda CUDA 12.8 channel, which distributes the Linux nvcc
front-end separately from the Python compiler-component wheel. The recovery
must be preregistered under a new run ID, use a project-local environment, keep
the same mllm/submodule commits and build options, and retain run 034 unchanged.

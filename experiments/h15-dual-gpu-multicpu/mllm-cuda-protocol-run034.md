# H15.2 protocol — pinned mllm CUDA backend on the local GPUs (run 034)

This protocol is locked before installing a CUDA compiler, initializing the
mllm CUDA vendor submodules or configuring a CUDA build.

## Hypothesis

The pinned upstream mllm commit can build and execute its published CUDA backend
on the two local RTX 4090 devices once a CUDA 12.8 compiler/toolkit is installed.
The result must also identify the exact upstream implementation boundary before
AgentSys adds a workload-execution adapter.

## Fixed source and environment

- mllm: `50ad5a9b6fbea742e38b5b31776c187e50319c8e`.
- CUDA vendor submodules: CCCL `9c40ed11560fa8ffd21abe4cdc8dc3ce875e48e3`
  and CUTLASS `e51efbfe18fe4f4cbb66ab814c55bf4aa0185491`.
- Compiler package: NVIDIA `nvidia-cuda-nvcc-cu12==12.8.93`, matching the
  already locked CUDA 12.8 PyTorch runtime.
- Build directory: `.references/mllm/build-x86-cuda`.
- CMake options: Release, CUDA backend on, compute architecture 89, tests on,
  examples/benchmarks/tools/extensions off, CPU backend retained.
- Targets: `MllmCUDABackendCudaOps`, `MllmCUDABackend`, and
  `Mllm-Test-CUDA-DeviceInfo`.

No paper performance target is introduced in this run. Existing mllm/llm.npu
paper regression remains the five registered run-031 endpoints at <=10%.

## Required evidence and gates

1. The CUDA compiler reports release 12.8 and CMake records a real CUDA compiler.
2. Both CUDA vendor submodules match their pinned commits.
3. `MLLM_BUILD_CUDA_BACKEND=ON` and `CMAKE_CUDA_ARCHITECTURES=89` appear in the
   build cache.
4. All three locked targets build and their binaries/libraries have non-zero
   hashes.
5. The upstream device test exits zero and reports both RTX 4090 devices.
6. The linked CUDA backend depends on CUDA runtime, driver and NVML libraries.
7. The audit explicitly checks the upstream source boundary: its four CUDA
   kernel translation units contain no executable kernel implementation at this
   commit and `CudaBackend` registers no op factory. Therefore this run may
   certify backend initialization/allocation infrastructure, not full mllm CUDA
   model inference.
8. The unchanged native mllm run-023 artifact remains passing (20/20 binaries,
   101 gtests) and the current five-layer matrix remains 68/68 at <=10%.

## Failure and next-step rule

A configure, build, link, device-discovery or boundary-audit failure is retained
as run-034 failure. AgentSys must not label its later MIR-driven CUDA adapter as
an upstream mllm kernel implementation. Only after this audit passes may H15.3
compile Agent calls into real GPU/NUMA execution and merge them with Rocket,
TISA and HPTPE traces.

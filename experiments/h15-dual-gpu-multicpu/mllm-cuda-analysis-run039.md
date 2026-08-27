# H15.2 run-039 analysis — pinned mllm CUDA backend passes

## Outcome

H15.2 is supported within its preregistered boundary. All 13 gates pass. Two
consecutive setup executions exit zero; the second performs no compilation and
still executes the device test successfully.

## Built and executed

- `libMllmCUDABackendCudaOps.so`: 21,368 bytes;
- `libMllmCUDABackend.so`: 202,096 bytes;
- `Mllm-Test-CUDA-DeviceInfo`: 171,808 bytes.

The test reports exactly two NVIDIA GeForce RTX 4090 devices and exits zero.
Dynamic linkage uses project-local cudart 12.8, but resolves `libcuda.so.1` and
`libnvidia-ml.so.1` from the real host driver. nvcc is 12.8.93, CMake targets
sm_89, and the NVIDIA Conda environment remains explicitly locked.

## Framework modification

The project-owned patch enables the one line already marked by upstream as
needed for CUDA: it clears the memory manager in `shutdownContext()` before
static CUDA teardown. The patch SHA-256 is
`8d5514345283fe37f8ece4d0a0bd4d679804afe9eb5e25b90433d0a41afafd3c`;
the audit stores the complete one-line upstream diff. This changes shutdown
ordering only and fixes the run-038 `cudaErrorCudartUnloading` abort.

## Capability boundary

The fixed upstream commit's four CUDA `.cu` files still contain no executable
lines, and its CUDA backend still registers no operator factory. Therefore run
039 certifies the official CUDA backend's build, device metadata, memory
allocator and lifecycle—not full mllm GPU inference. The next stage must label
the MIR-driven real-kernel layer as an AgentSys execution adapter. Existing
mllm/llm.npu paper regression remains 5/5 within the 68/68 matrix at <=10%.

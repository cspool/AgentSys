# H15.2 recovery protocol — remove optional OpenMP link (run 037)

Locked before changing CMake or rerunning the build.

## Single change

Set `MLLM_KERNEL_THREADS_VENDOR_OPENMP=OFF`; retain
`MLLM_KERNEL_USE_THREADS=ON`, so mllm's internal thread pool remains active.
This matches the effective cache of the already passing native mllm build and
removes only the unavailable optional `libomp` dependency.

Every other run-036 condition remains fixed: project-local CUDA 12.8.1 lock,
nvcc 12.8.93, clang/clang++ 16, sm_89, tools on, examples/benchmarks/extensions
off, exact mllm/CCCL/CUTLASS commits, three target names and two-GPU device test.

## Acceptance

All 13 audit gates must pass. The build and test must also rerun a second time
without source edits to demonstrate setup idempotence. Success supports H15.2
only within the source-audited upstream capability boundary.

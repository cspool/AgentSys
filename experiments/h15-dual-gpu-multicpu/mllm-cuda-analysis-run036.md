# H15.2 run-036 analysis — CUDA objects build, OpenMP link fails

Run 036 is retained at 9/13. Enabling tools resolves the run-035 configure
failure. CMake generates successfully, and nvcc compiles all four upstream CUDA
translation units and links `libMllmCUDABackendCudaOps.so` for sm_89.

The next dependency, `MllmRT`, fails at link time. mllm does not find a valid
Clang OpenMP package, but its fallback still adds `-fopenmp`; clang then requests
`-lomp`, which is absent. Therefore `MllmCUDABackend` and the device test cannot
finish, and device/link/build-log gates stay false.

This run proves the local CUDA compiler and CUDA object path work. The failure
is the CPU threading vendor selected for a test whose CUDA backend initialization
does not require OpenMP. The next recovery may disable only
`MLLM_KERNEL_THREADS_VENDOR_OPENMP`, matching the already validated native mllm
build's effective cache, while retaining mllm's own thread pool.

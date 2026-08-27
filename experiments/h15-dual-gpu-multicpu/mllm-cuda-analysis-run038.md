# H15.2 run-038 analysis — backend builds, upstream CUDA shutdown bug

Run 038 reaches 11/13 gates. The added Conda stub path links all three targets;
the executable resolves CUDA runtime, real host driver and NVML. The device test
prints both RTX 4090 devices, then exits with SIGABRT.

The abort is source-localized. `shutdownContext()` contains a commented
`Context::instance().memoryManager()->clearAll()` immediately below the upstream
remark "This line is needed for cuda !!!". Without it, the CUDA buddy pool is
destroyed during static teardown after the driver runtime begins shutdown;
`cudaFree` returns `cudaErrorCudartUnloading` ("driver shutting down") and the
backend's fatal-check macro aborts.

The remaining false gates are the zero-exit device test and the log/device gate.
All build, linkage, compiler, source-boundary, package and non-mutation gates
pass. A new protocol is required before applying the one-line framework fix.

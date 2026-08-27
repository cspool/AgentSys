# H15.2 recovery protocol — satisfy mllm's tools install rule (run 036)

Locked before changing the build command or rerunning CMake.

## Single change

Change only `MLLM_ENABLE_TOOLS=OFF` to `MLLM_ENABLE_TOOLS=ON`. This creates the
`mllm-params-inspector` target referenced by mllm's unconditional install rule.
All run-035 toolchain packages, compiler paths, mllm/CCCL/CUTLASS commits,
clang-16 host compiler, sm_89 architecture, disabled examples/benchmarks, and
the three requested CUDA targets remain unchanged.

## Acceptance

- CMake configure and the three locked target builds exit zero.
- The 13 run-035 audit gates all pass.
- The device test discovers exactly two RTX 4090 devices.
- Linkage resolves cudart, CUDA driver and NVML at runtime.
- Setup is idempotent and retains an explicit Conda lock and complete log.
- The upstream CUDA capability boundary remains
  initialization/device-metadata/allocator scaffold; no empty source is called
  a working model kernel.

A failure is retained. No further CMake option or source patch may be introduced
under run 036.

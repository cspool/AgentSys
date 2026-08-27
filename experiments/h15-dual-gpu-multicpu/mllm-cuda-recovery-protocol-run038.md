# H15.2 recovery protocol — Conda CUDA stub search path (run 038)

Locked before changing CMake or rerunning the build.

Add exactly one CMake library search path:
`.cuda-toolkit/targets/x86_64-linux/lib/stubs`, the existing directory containing
the NVIDIA Conda `libcuda.so` and `libnvidia-ml.so` development stubs. Retain all
run-037 inputs and options unchanged.

Acceptance is 13/13 audit gates followed by a second idempotent setup execution.
The runtime loader must resolve the real host driver/NVML libraries; stub paths
are build-time only. The source-boundary claim remains unchanged.

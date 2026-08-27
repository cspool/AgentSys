# H15.2 run-037 analysis — core links, Conda NVML stub path differs

Run 037 remains 9/13 but advances the build boundary. Disabling optional OpenMP
allows `libMllmRT.so` to link. The CUDA backend then fails only at `-lnvidia-ml`.

The NVIDIA Conda package installs driver/NVML stubs under
`.cuda-toolkit/targets/x86_64-linux/lib/stubs`; mllm hard-codes
`${CUDAToolkit_LIBRARY_DIR}/stubs`, which resolves to the absent
`.cuda-toolkit/lib/stubs` in this layout. Both stub libraries exist at the first
path, so this is a link-search-path mismatch rather than a missing package.

The next recovery may add only the existing Conda target stub directory to
CMake's library search path. No source, package, compiler, target or runtime
claim changes.

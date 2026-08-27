# H15.2 framework patch protocol — CUDA shutdown ordering (run 039)

Locked before creating or applying the integration patch.

## Exact source change

In pinned upstream `mllm/mllm.cpp::shutdownContext()`, replace only:

```cpp
// Context::instance().memoryManager()->clearAll();
```

with:

```cpp
Context::instance().memoryManager()->clearAll();
```

The adjacent upstream comments—`Clean up memory before backend is freed` and
`This line is needed for cuda !!!`—are the source justification. The change is
stored as a project-owned patch, hash-audited, and applied idempotently by the
setup script; the pinned upstream commit identity remains recorded separately.

## Acceptance

- All run-038 build/toolchain inputs stay fixed.
- First patched build/test and a second no-source-edit setup both exit zero.
- Both executions report exactly two RTX 4090 devices.
- All 13 audit gates pass, including real host CUDA/driver/NVML resolution.
- Audit records the exact patch hash and the sole one-line upstream diff.
- Empty CUDA kernels/no op factories remain explicitly classified as scaffold.

Only then is H15.2 supported and H15.3 workload integration allowed.

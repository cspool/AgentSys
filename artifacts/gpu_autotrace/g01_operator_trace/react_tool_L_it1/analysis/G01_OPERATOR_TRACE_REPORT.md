# G01 operator-wise single-GPU trace: `react_tool_L_it1`

Lineage `h22-gpu-autotrace`, workflow w01. Real execution on one RTX 4090
(`0000:b1:00.0`), warmup 3 iterations discarded, 8 measured iterations. Attribution basis: NVTX operator range -> CUDA runtime API launched inside it -> CUPTI kernel/memcpy by correlationId.

## Conservation

| Quantity | Value |
|---|---:|
| Operator instances observed / expected | 128 / 128 |
| Measured wall per iteration (median) | 181,121.8 us |
| GPU busy per iteration (median, union of GPU intervals) | 3.6 % |
| Operator-owned GPU time (total over measured) | 24,575.5 us |
| Call-overhead GPU time (weight init, H2D/D2H, staging) | 27,302.7 us |
| Unattributed GPU items inside measured window | 0 (0.0 us) |
| Kernel launches over measured iterations | 336 |
| Warmup iteration 0 wall | 586,366.3 us |
| Warmup GPU busy (median) | 3.57 % |
| Pass | True |

## Operator-type breakdown (measured iterations)

| op_type | instances | kernel launches | GPU total (us) | GPU share | NVTX CPU total (us) | wall share | GPU per instance (us) |
|---|---:|---:|---:|---:|---:|---:|---:|
| call_overhead | 16 | 32 | 27,302.7 | 52.63 % | 0.0 | 0.0 % | 1,706.4 |
| LinearOp | 48 | 48 | 17,852.5 | 34.41 % | 22,597.0 | 1.56 % | 371.9 |
| RMSNormOp | 32 | 224 | 4,391.5 | 8.47 % | 10,441.9 | 0.72 % | 137.2 |
| TransposeOp | 16 | 16 | 2,148.5 | 4.14 % | 3,850.2 | 0.27 % | 134.3 |
| AddOp | 16 | 16 | 183.0 | 0.35 % | 1,813.6 | 0.13 % | 11.4 |
| ViewOp | 16 | 0 | 0.0 | 0.0 % | 1,288.8 | 0.09 % | 0.0 |

## Kernel-family breakdown (measured iterations)

| family | instances | GPU total (us) | share |
|---|---:|---:|---:|
| memcpy | 32 | 26,795.2 | 51.65 % |
| gemm | 48 | 17,852.5 | 34.41 % |
| copy | 80 | 4,036.0 | 7.78 % |
| elementwise_unary | 64 | 1,251.9 | 2.41 % |
| elementwise_binary | 96 | 1,243.7 | 2.4 % |
| reduce | 32 | 369.9 | 0.71 % |
| rng_init | 16 | 329.0 | 0.63 % |

## Per-operator summary (measured iterations)

| call | idx | op_type | engine | GPU median (us) | GPU min/max (us) | NVTX CPU median (us) | GPU/CPU | kernels |
|---|---:|---|---|---:|---:|---:|---:|---:|
| answer | 6 | RMSNormOp | ve | 142.5 | 141.4/160.2 | 328.3 | 43.9 % | 7 |
| answer | 7 | AddOp | ve | 11.5 | 11.4/11.6 | 105.5 | 9.9 % | 1 |
| answer | 8 | RMSNormOp | ve | 126.7 | 125.1/128.6 | 218.6 | 56.5 % | 7 |
| answer | 10 | LinearOp | me | 371.5 | 370.1/372.2 | 512.0 | 72.4 % | 1 |
| answer | 11 | LinearOp | me | 370.9 | 369.8/425.2 | 449.5 | 82.2 % | 1 |
| answer | 12 | LinearOp | me | 370.4 | 369.7/371.1 | 442.6 | 82.5 % | 1 |
| answer | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 78.4 | 0.0 % | 0 |
| answer | 14 | TransposeOp | de | 133.0 | 132.9/133.3 | 235.8 | 55.8 % | 1 |
| answer |  | call_overhead |  | 2,502.1 | 2,469.3/2,809.7 |  |  % | 2 |
| plan | 6 | RMSNormOp | ve | 143.5 | 142.2/177.3 | 326.3 | 28.2 % | 7 |
| plan | 7 | AddOp | ve | 11.4 | 11.4/11.5 | 105.0 | 10.2 % | 1 |
| plan | 8 | RMSNormOp | ve | 127.2 | 125.7/146.9 | 222.3 | 57.4 % | 7 |
| plan | 10 | LinearOp | me | 371.2 | 369.8/372.2 | 511.2 | 72.9 % | 1 |
| plan | 11 | LinearOp | me | 370.4 | 369.4/371.9 | 448.2 | 82.0 % | 1 |
| plan | 12 | LinearOp | me | 370.4 | 369.0/372.5 | 443.0 | 83.7 % | 1 |
| plan | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 76.8 | 0.0 % | 0 |
| plan | 14 | TransposeOp | de | 133.0 | 132.7/153.6 | 240.2 | 55.8 % | 1 |
| plan |  | call_overhead |  | 855.9 | 838.2/928.2 |  |  % | 2 |

## Per-iteration conservation

| phase | iter | wall (us) | GPU busy % | operator GPU (us) | overhead GPU (us) | launches |
|---|---:|---:|---:|---:|---:|---:|
| warmup | 0 | 586,366.3 | 1.07 | 3,077.0 | 3,222.0 | 42 |
| warmup | 1 | 180,866.6 | 3.59 | 3,090.0 | 3,409.1 | 42 |
| warmup | 2 | 180,144.5 | 3.57 | 3,058.1 | 3,369.8 | 42 |
| measured | 0 | 181,479.6 | 3.56 | 3,051.6 | 3,411.6 | 42 |
| measured | 1 | 181,141.3 | 3.53 | 3,052.4 | 3,350.8 | 42 |
| measured | 2 | 180,531.2 | 3.57 | 3,093.1 | 3,355.4 | 42 |
| measured | 3 | 180,242.8 | 3.53 | 3,049.8 | 3,308.4 | 42 |
| measured | 4 | 181,102.3 | 3.52 | 3,053.5 | 3,321.2 | 42 |
| measured | 5 | 180,968.5 | 3.62 | 3,112.2 | 3,434.7 | 42 |
| measured | 6 | 182,983.3 | 3.74 | 3,107.1 | 3,737.9 | 42 |
| measured | 7 | 181,581.6 | 3.55 | 3,055.8 | 3,382.7 | 42 |

## Reading notes

- `GPU busy %` is the union of all GPU intervals launched inside the iteration divided by the iteration wall.
  The remainder is host-side: Python dispatch, per-operator `cudaEventSynchronize`, CPU tool matmuls, pinned staging.
- `GPU/CPU` per operator compares launch-owned GPU time to the NVTX CPU range, which encloses a synchronize.
- Warmup rows are shown for context only; no measured statistic includes them.
- Plan `/workspace/AgentSys/artifacts/gpu_autotrace/scaled_plans/react_tool_L_it1/hybrid-plan.json` sha256 `bf6a02d9dd666378…`; sqlite sha256 `0d0ce90d227aee70…`.

# G01 operator-wise single-GPU trace: `react_tool_L`

Lineage `h22-gpu-autotrace`, workflow w01. Real execution on one RTX 4090
(`0000:b1:00.0`), warmup 3 iterations discarded, 8 measured iterations. Attribution basis: NVTX operator range -> CUDA runtime API launched inside it -> CUPTI kernel/memcpy by correlationId.

## Conservation

| Quantity | Value |
|---|---:|
| Operator instances observed / expected | 128 / 128 |
| Measured wall per iteration (median) | 237,692.5 us |
| GPU busy per iteration (median, union of GPU intervals) | 40.7 % |
| Operator-owned GPU time (total over measured) | 745,381.3 us |
| Call-overhead GPU time (weight init, H2D/D2H, staging) | 26,924.3 us |
| Unattributed GPU items inside measured window | 0 (0.0 us) |
| Kernel launches over measured iterations | 9760 |
| Warmup iteration 0 wall | 706,804.8 us |
| Warmup GPU busy (median) | 36.65 % |
| Pass | True |

## Operator-type breakdown (measured iterations)

| op_type | instances | kernel launches | GPU total (us) | GPU share | NVTX CPU total (us) | wall share | GPU per instance (us) |
|---|---:|---:|---:|---:|---:|---:|---:|
| LinearOp | 48 | 1536 | 543,095.3 | 70.32 % | 549,072.3 | 28.66 % | 11,314.5 |
| RMSNormOp | 32 | 7168 | 131,056.6 | 16.97 % | 140,118.3 | 7.31 % | 4,095.5 |
| TransposeOp | 16 | 512 | 66,048.9 | 8.55 % | 68,069.5 | 3.55 % | 4,128.1 |
| call_overhead | 16 | 32 | 26,924.3 | 3.49 % | 0.0 | 0.0 % | 1,682.8 |
| AddOp | 16 | 512 | 5,180.6 | 0.67 % | 9,188.2 | 0.48 % | 323.8 |
| ViewOp | 16 | 0 | 0.0 | 0.0 % | 2,502.9 | 0.13 % | 0.0 |

## Kernel-family breakdown (measured iterations)

| family | instances | GPU total (us) | share |
|---|---:|---:|---:|
| gemm | 1536 | 543,095.3 | 70.32 % |
| copy | 2560 | 109,822.9 | 14.22 % |
| elementwise_unary | 2048 | 42,694.9 | 5.53 % |
| elementwise_binary | 2576 | 39,125.3 | 5.07 % |
| memcpy | 32 | 26,462.2 | 3.43 % |
| reduce | 1024 | 10,812.0 | 1.4 % |
| rng_init | 16 | 293.0 | 0.04 % |

## Per-operator summary (measured iterations)

| call | idx | op_type | engine | GPU median (us) | GPU min/max (us) | NVTX CPU median (us) | GPU/CPU | kernels |
|---|---:|---|---|---:|---:|---:|---:|---:|
| answer | 6 | RMSNormOp | ve | 4,150.4 | 4,043.2/4,528.5 | 4,413.8 | 92.3 % | 224 |
| answer | 7 | AddOp | ve | 324.2 | 321.5/325.5 | 570.5 | 54.8 % | 32 |
| answer | 8 | RMSNormOp | ve | 4,020.2 | 4,010.3/4,088.2 | 4,240.0 | 93.3 % | 224 |
| answer | 10 | LinearOp | me | 11,431.8 | 11,126.2/11,458.9 | 11,603.8 | 98.6 % | 32 |
| answer | 11 | LinearOp | me | 11,094.3 | 11,064.6/11,474.8 | 11,235.3 | 99.0 % | 32 |
| answer | 12 | LinearOp | me | 11,456.4 | 11,095.4/11,493.4 | 11,545.0 | 99.1 % | 32 |
| answer | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 153.2 | 0.0 % | 0 |
| answer | 14 | TransposeOp | de | 4,061.3 | 3,987.1/4,399.9 | 4,187.3 | 97.0 % | 32 |
| answer |  | call_overhead |  | 2,512.6 | 2,409.8/2,730.7 |  |  % | 2 |
| plan | 6 | RMSNormOp | ve | 4,126.0 | 4,041.1/4,376.1 | 4,392.6 | 94.0 % | 224 |
| plan | 7 | AddOp | ve | 323.1 | 319.6/331.7 | 561.4 | 58.1 % | 32 |
| plan | 8 | RMSNormOp | ve | 4,017.3 | 4,011.2/4,140.5 | 4,239.2 | 94.6 % | 224 |
| plan | 10 | LinearOp | me | 11,318.9 | 11,076.6/11,440.1 | 11,460.6 | 98.7 % | 32 |
| plan | 11 | LinearOp | me | 11,153.0 | 11,051.1/11,466.2 | 11,279.5 | 99.1 % | 32 |
| plan | 12 | LinearOp | me | 11,474.0 | 11,097.9/11,638.3 | 11,568.4 | 99.1 % | 32 |
| plan | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 154.8 | 0.0 % | 0 |
| plan | 14 | TransposeOp | de | 4,081.6 | 3,987.3/4,303.6 | 4,202.6 | 97.1 % | 32 |
| plan |  | call_overhead |  | 839.5 | 806.3/864.7 |  |  % | 2 |

## Per-iteration conservation

| phase | iter | wall (us) | GPU busy % | operator GPU (us) | overhead GPU (us) | launches |
|---|---:|---:|---:|---:|---:|---:|
| warmup | 0 | 706,804.8 | 14.48 | 98,315.1 | 4,008.5 | 1220 |
| warmup | 1 | 277,129.2 | 36.65 | 98,195.1 | 3,369.6 | 1220 |
| warmup | 2 | 268,072.0 | 36.99 | 95,824.5 | 3,342.5 | 1220 |
| measured | 0 | 239,444.1 | 40.32 | 93,163.8 | 3,371.7 | 1220 |
| measured | 1 | 236,800.9 | 40.69 | 92,986.5 | 3,378.3 | 1220 |
| measured | 2 | 231,283.4 | 41.6 | 92,859.3 | 3,359.8 | 1220 |
| measured | 3 | 234,225.9 | 41.17 | 93,180.6 | 3,249.0 | 1220 |
| measured | 4 | 237,510.2 | 40.84 | 93,661.6 | 3,331.5 | 1220 |
| measured | 5 | 237,874.8 | 40.69 | 93,502.9 | 3,292.2 | 1220 |
| measured | 6 | 259,322.2 | 37.17 | 93,029.6 | 3,371.4 | 1220 |
| measured | 7 | 239,263.6 | 40.36 | 92,997.0 | 3,570.4 | 1220 |

## Reading notes

- `GPU busy %` is the union of all GPU intervals launched inside the iteration divided by the iteration wall.
  The remainder is host-side: Python dispatch, per-operator `cudaEventSynchronize`, CPU tool matmuls, pinned staging.
- `GPU/CPU` per operator compares launch-owned GPU time to the NVTX CPU range, which encloses a synchronize.
- Warmup rows are shown for context only; no measured statistic includes them.
- Plan `/workspace/AgentSys/artifacts/gpu_autotrace/scaled_plans/react_tool_L/hybrid-plan.json` sha256 `87cdbe0db3957ed9…`; sqlite sha256 `e623d672820c1ee9…`.

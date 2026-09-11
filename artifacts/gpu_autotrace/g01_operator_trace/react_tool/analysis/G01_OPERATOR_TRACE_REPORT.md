# G01 operator-wise single-GPU trace: `react_tool`

Lineage `h22-gpu-autotrace`, workflow w01. Real execution on one RTX 4090
(`0000:b1:00.0`), warmup 5 iterations discarded, 20 measured iterations. Attribution basis: NVTX operator range -> CUDA runtime API launched inside it -> CUPTI kernel/memcpy by correlationId.

## Conservation

| Quantity | Value |
|---|---:|
| Operator instances observed / expected | 320 / 320 |
| Measured wall per iteration (median) | 18,484.1 us |
| GPU busy per iteration (median, union of GPU intervals) | 2.8 % |
| Operator-owned GPU time (total over measured) | 3,351.3 us |
| Call-overhead GPU time (weight init, H2D/D2H, staging) | 6,401.6 us |
| Unattributed GPU items inside measured window | 0 (0.0 us) |
| Kernel launches over measured iterations | 840 |
| Warmup iteration 0 wall | 482,739.0 us |
| Warmup GPU busy (median) | 2.77 % |
| Pass | True |

## Operator-type breakdown (measured iterations)

| op_type | instances | kernel launches | GPU total (us) | GPU share | NVTX CPU total (us) | wall share | GPU per instance (us) |
|---|---:|---:|---:|---:|---:|---:|---:|
| call_overhead | 40 | 80 | 6,401.6 | 65.64 % | 0.0 | 0.0 % | 160.0 |
| LinearOp | 120 | 120 | 1,531.6 | 15.7 % | 15,899.1 | 4.26 % | 12.8 |
| RMSNormOp | 80 | 560 | 1,363.6 | 13.98 % | 20,041.5 | 5.37 % | 17.0 |
| TransposeOp | 40 | 40 | 375.8 | 3.85 % | 5,093.8 | 1.37 % | 9.4 |
| AddOp | 40 | 40 | 80.3 | 0.82 % | 4,155.9 | 1.11 % | 2.0 |
| ViewOp | 40 | 0 | 0.0 | 0.0 % | 3,021.8 | 0.81 % | 0.0 |

## Kernel-family breakdown (measured iterations)

| family | instances | GPU total (us) | share |
|---|---:|---:|---:|
| memcpy | 80 | 6,183.1 | 63.4 % |
| gemm | 120 | 1,479.1 | 15.17 % |
| copy | 200 | 824.6 | 8.45 % |
| elementwise_binary | 240 | 522.9 | 5.36 % |
| elementwise_unary | 160 | 281.7 | 2.89 % |
| reduce | 80 | 266.5 | 2.73 % |
| rng_init | 40 | 142.6 | 1.46 % |
| memset | 120 | 52.5 | 0.54 % |

## Per-operator summary (measured iterations)

| call | idx | op_type | engine | GPU median (us) | GPU min/max (us) | NVTX CPU median (us) | GPU/CPU | kernels |
|---|---:|---|---|---:|---:|---:|---:|---:|
| answer | 6 | RMSNormOp | ve | 15.8 | 15.7/96.9 | 269.6 | 7.4 % | 7 |
| answer | 7 | AddOp | ve | 1.4 | 1.4/23.8 | 101.5 | 2.4 % | 1 |
| answer | 8 | RMSNormOp | ve | 15.5 | 15.1/47.3 | 230.7 | 7.1 % | 7 |
| answer | 10 | LinearOp | me | 12.8 | 12.7/13.0 | 152.6 | 8.7 % | 1 |
| answer | 11 | LinearOp | me | 12.7 | 12.6/13.0 | 116.9 | 8.2 % | 1 |
| answer | 12 | LinearOp | me | 12.7 | 12.7/12.8 | 111.3 | 11.3 % | 1 |
| answer | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 72.6 | 0.0 % | 0 |
| answer | 14 | TransposeOp | de | 9.4 | 9.3/9.5 | 127.8 | 7.5 % | 1 |
| answer |  | call_overhead |  | 267.5 | 161.6/282.7 |  |  % | 2 |
| plan | 6 | RMSNormOp | ve | 15.9 | 15.8/16.0 | 272.6 | 5.9 % | 7 |
| plan | 7 | AddOp | ve | 1.4 | 1.4/1.5 | 100.4 | 1.4 % | 1 |
| plan | 8 | RMSNormOp | ve | 15.5 | 15.1/15.5 | 229.3 | 6.8 % | 7 |
| plan | 10 | LinearOp | me | 12.8 | 12.7/13.0 | 149.9 | 8.6 % | 1 |
| plan | 11 | LinearOp | me | 12.7 | 12.6/12.9 | 118.3 | 10.8 % | 1 |
| plan | 12 | LinearOp | me | 12.7 | 12.5/12.8 | 110.3 | 11.4 % | 1 |
| plan | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 72.4 | 0.0 % | 0 |
| plan | 14 | TransposeOp | de | 9.4 | 9.3/9.5 | 127.1 | 7.3 % | 1 |
| plan |  | call_overhead |  | 85.6 | 58.6/91.1 |  |  % | 2 |

## Per-iteration conservation

| phase | iter | wall (us) | GPU busy % | operator GPU (us) | overhead GPU (us) | launches |
|---|---:|---:|---:|---:|---:|---:|
| warmup | 0 | 482,739.0 | 0.11 | 162.8 | 351.5 | 42 |
| warmup | 1 | 18,769.6 | 3.59 | 322.2 | 351.4 | 42 |
| warmup | 2 | 18,568.3 | 2.78 | 160.6 | 355.7 | 42 |
| warmup | 3 | 18,573.7 | 2.77 | 161.2 | 353.2 | 42 |
| warmup | 4 | 18,654.3 | 2.75 | 160.9 | 352.3 | 42 |
| measured | 0 | 18,689.9 | 2.77 | 160.7 | 356.7 | 42 |
| measured | 1 | 18,774.1 | 2.81 | 160.4 | 367.8 | 42 |
| measured | 2 | 18,643.3 | 2.83 | 161.0 | 366.5 | 42 |
| measured | 3 | 18,675.4 | 2.76 | 161.0 | 354.6 | 42 |
| measured | 4 | 22,167.1 | 2.34 | 160.9 | 357.4 | 42 |
| measured | 5 | 21,781.7 | 2.37 | 160.8 | 356.1 | 42 |
| measured | 6 | 18,482.5 | 2.8 | 160.8 | 356.0 | 42 |
| measured | 7 | 18,485.6 | 2.78 | 160.4 | 354.3 | 42 |
| measured | 8 | 18,220.4 | 2.84 | 160.9 | 357.1 | 42 |
| measured | 9 | 17,480.2 | 2.18 | 160.6 | 220.8 | 42 |
| measured | 10 | 17,599.5 | 2.17 | 160.9 | 220.4 | 42 |
| measured | 11 | 17,517.0 | 2.71 | 242.5 | 231.8 | 42 |
| measured | 12 | 18,409.7 | 2.44 | 214.7 | 234.3 | 42 |
| measured | 13 | 17,754.8 | 2.28 | 160.8 | 243.5 | 42 |
| measured | 14 | 17,997.8 | 2.46 | 160.8 | 281.7 | 42 |
| measured | 15 | 18,068.3 | 2.67 | 161.0 | 321.9 | 42 |
| measured | 16 | 18,853.1 | 2.75 | 160.9 | 357.0 | 42 |
| measured | 17 | 18,532.8 | 2.8 | 160.7 | 358.1 | 42 |
| measured | 18 | 18,425.7 | 2.78 | 160.9 | 351.8 | 42 |
| measured | 19 | 18,576.7 | 2.77 | 160.6 | 353.8 | 42 |

## Reading notes

- `GPU busy %` is the union of all GPU intervals launched inside the iteration divided by the iteration wall.
  The remainder is host-side: Python dispatch, per-operator `cudaEventSynchronize`, CPU tool matmuls, pinned staging.
- `GPU/CPU` per operator compares launch-owned GPU time to the NVTX CPU range, which encloses a synchronize.
- Warmup rows are shown for context only; no measured statistic includes them.
- Plan `/workspace/AgentSys/artifacts/hybrid_reproduction/run_040/workloads/react_tool/hybrid-plan.json` sha256 `14a8c7f857db15ac…`; sqlite sha256 `39b30acc23f8af6f…`.

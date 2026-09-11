# G01 operator-wise single-GPU trace: `planner_debate`

Lineage `h22-gpu-autotrace`, workflow w01. Real execution on one RTX 4090
(`0000:b1:00.0`), warmup 5 iterations discarded, 20 measured iterations. Attribution basis: NVTX operator range -> CUDA runtime API launched inside it -> CUPTI kernel/memcpy by correlationId.

## Conservation

| Quantity | Value |
|---|---:|
| Operator instances observed / expected | 800 / 800 |
| Measured wall per iteration (median) | 62,131.8 us |
| GPU busy per iteration (median, union of GPU intervals) | 3.2 % |
| Operator-owned GPU time (total over measured) | 10,980.9 us |
| Call-overhead GPU time (weight init, H2D/D2H, staging) | 27,798.4 us |
| Unattributed GPU items inside measured window | 0 (0.0 us) |
| Kernel launches over measured iterations | 2100 |
| Warmup iteration 0 wall | 540,182.7 us |
| Warmup GPU busy (median) | 2.57 % |
| Pass | True |

## Operator-type breakdown (measured iterations)

| op_type | instances | kernel launches | GPU total (us) | GPU share | NVTX CPU total (us) | wall share | GPU per instance (us) |
|---|---:|---:|---:|---:|---:|---:|---:|
| call_overhead | 100 | 200 | 27,798.4 | 71.68 % | 0.0 | 0.0 % | 278.0 |
| LinearOp | 300 | 300 | 5,634.6 | 14.53 % | 36,880.5 | 2.8 % | 18.8 |
| RMSNormOp | 200 | 1400 | 3,874.9 | 9.99 % | 55,676.5 | 4.22 % | 19.4 |
| TransposeOp | 100 | 100 | 1,229.9 | 3.17 % | 13,430.1 | 1.02 % | 12.3 |
| AddOp | 100 | 100 | 241.5 | 0.62 % | 11,077.3 | 0.84 % | 2.4 |
| ViewOp | 100 | 0 | 0.0 | 0.0 % | 8,373.3 | 0.63 % | 0.0 |

## Kernel-family breakdown (measured iterations)

| family | instances | GPU total (us) | share |
|---|---:|---:|---:|
| memcpy | 200 | 27,104.7 | 69.89 % |
| gemm | 300 | 5,634.6 | 14.53 % |
| copy | 500 | 2,619.8 | 6.76 % |
| elementwise_binary | 600 | 1,396.0 | 3.6 % |
| elementwise_unary | 400 | 827.8 | 2.13 % |
| reduce | 200 | 694.1 | 1.79 % |
| rng_init | 100 | 502.5 | 1.3 % |

## Per-operator summary (measured iterations)

| call | idx | op_type | engine | GPU median (us) | GPU min/max (us) | NVTX CPU median (us) | GPU/CPU | kernels |
|---|---:|---|---|---:|---:|---:|---:|---:|
| critic-a | 6 | RMSNormOp | ve | 19.4 | 19.1/19.6 | 284.2 | 6.6 % | 7 |
| critic-a | 7 | AddOp | ve | 2.0 | 1.9/2.1 | 103.6 | 1.9 % | 1 |
| critic-a | 8 | RMSNormOp | ve | 19.1 | 18.8/19.2 | 247.5 | 7.7 % | 7 |
| critic-a | 10 | LinearOp | me | 19.8 | 19.6/19.9 | 140.0 | 14.1 % | 1 |
| critic-a | 11 | LinearOp | me | 19.7 | 19.5/19.9 | 103.1 | 18.9 % | 1 |
| critic-a | 12 | LinearOp | me | 19.6 | 19.4/19.8 | 96.9 | 18.8 % | 1 |
| critic-a | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 74.4 | 0.0 % | 0 |
| critic-a | 14 | TransposeOp | de | 12.3 | 12.2/12.9 | 127.6 | 9.6 % | 1 |
| critic-a |  | call_overhead |  | 283.2 | 169.4/525.3 |  |  % | 2 |
| critic-b | 6 | RMSNormOp | ve | 19.4 | 19.2/41.5 | 293.3 | 6.7 % | 7 |
| critic-b | 7 | AddOp | ve | 2.0 | 2.0/2.1 | 104.6 | 1.8 % | 1 |
| critic-b | 8 | RMSNormOp | ve | 19.1 | 18.8/19.2 | 249.8 | 7.3 % | 7 |
| critic-b | 10 | LinearOp | me | 19.7 | 19.5/19.8 | 145.6 | 12.9 % | 1 |
| critic-b | 11 | LinearOp | me | 19.7 | 19.5/19.9 | 103.3 | 17.9 % | 1 |
| critic-b | 12 | LinearOp | me | 19.7 | 19.4/19.8 | 97.2 | 18.7 % | 1 |
| critic-b | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 77.6 | 0.0 % | 0 |
| critic-b | 14 | TransposeOp | de | 12.4 | 12.2/13.1 | 131.6 | 9.1 % | 1 |
| critic-b |  | call_overhead |  | 319.8 | 194.7/327.1 |  |  % | 2 |
| critic-merge | 6 | RMSNormOp | ve | 19.4 | 19.3/19.5 | 304.9 | 6.3 % | 7 |
| critic-merge | 7 | AddOp | ve | 2.0 | 2.0/2.1 | 105.4 | 1.9 % | 1 |
| critic-merge | 8 | RMSNormOp | ve | 19.1 | 18.9/19.3 | 242.1 | 7.8 % | 7 |
| critic-merge | 10 | LinearOp | me | 19.8 | 19.5/222.8 | 149.9 | 18.6 % | 1 |
| critic-merge | 11 | LinearOp | me | 19.7 | 19.5/19.9 | 103.8 | 18.1 % | 1 |
| critic-merge | 12 | LinearOp | me | 19.7 | 19.5/19.8 | 98.8 | 18.0 % | 1 |
| critic-merge | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 76.1 | 0.0 % | 0 |
| critic-merge | 14 | TransposeOp | de | 12.4 | 12.2/12.7 | 130.8 | 9.4 % | 1 |
| critic-merge |  | call_overhead |  | 320.0 | 199.1/324.9 |  |  % | 2 |
| planner-final | 6 | RMSNormOp | ve | 17.8 | 17.6/34.4 | 296.3 | 6.1 % | 7 |
| planner-final | 7 | AddOp | ve | 1.7 | 1.7/21.4 | 105.6 | 2.4 % | 1 |
| planner-final | 8 | RMSNormOp | ve | 17.5 | 17.2/17.6 | 249.2 | 6.7 % | 7 |
| planner-final | 10 | LinearOp | me | 14.6 | 14.5/14.6 | 146.8 | 9.5 % | 1 |
| planner-final | 11 | LinearOp | me | 14.6 | 14.5/14.7 | 102.2 | 13.4 % | 1 |
| planner-final | 12 | LinearOp | me | 14.5 | 14.5/154.2 | 96.4 | 18.1 % | 1 |
| planner-final | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 76.5 | 0.0 % | 0 |
| planner-final | 14 | TransposeOp | de | 12.1 | 12.1/12.3 | 130.0 | 9.0 % | 1 |
| planner-final |  | call_overhead |  | 408.4 | 257.2/412.1 |  |  % | 2 |
| planner-seed | 6 | RMSNormOp | ve | 17.8 | 17.5/17.9 | 294.4 | 5.9 % | 7 |
| planner-seed | 7 | AddOp | ve | 1.7 | 1.7/32.8 | 105.9 | 2.8 % | 1 |
| planner-seed | 8 | RMSNormOp | ve | 17.4 | 17.1/131.7 | 243.2 | 9.0 % | 7 |
| planner-seed | 10 | LinearOp | me | 14.6 | 14.5/14.6 | 142.6 | 9.9 % | 1 |
| planner-seed | 11 | LinearOp | me | 14.6 | 14.5/14.7 | 102.9 | 12.9 % | 1 |
| planner-seed | 12 | LinearOp | me | 14.5 | 14.5/14.6 | 98.8 | 13.4 % | 1 |
| planner-seed | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 75.2 | 0.0 % | 0 |
| planner-seed | 14 | TransposeOp | de | 12.1 | 12.1/12.2 | 129.5 | 8.8 % | 1 |
| planner-seed |  | call_overhead |  | 123.7 | 76.1/126.1 |  |  % | 2 |

## Per-iteration conservation

| phase | iter | wall (us) | GPU busy % | operator GPU (us) | overhead GPU (us) | launches |
|---|---:|---:|---:|---:|---:|---:|
| warmup | 0 | 540,182.7 | 0.36 | 524.3 | 1,430.6 | 105 |
| warmup | 1 | 76,935.1 | 2.57 | 521.7 | 1,453.1 | 105 |
| warmup | 2 | 76,024.0 | 2.67 | 574.8 | 1,455.8 | 105 |
| warmup | 3 | 75,931.3 | 2.59 | 521.5 | 1,444.3 | 105 |
| warmup | 4 | 77,384.1 | 2.55 | 521.5 | 1,451.6 | 105 |
| measured | 0 | 73,280.6 | 1.94 | 520.6 | 899.5 | 105 |
| measured | 1 | 74,822.1 | 2.36 | 522.4 | 1,247.0 | 105 |
| measured | 2 | 76,146.4 | 2.59 | 521.1 | 1,454.2 | 105 |
| measured | 3 | 76,001.4 | 2.8 | 673.2 | 1,453.2 | 105 |
| measured | 4 | 76,084.3 | 2.6 | 521.0 | 1,456.7 | 105 |
| measured | 5 | 61,325.2 | 3.46 | 660.9 | 1,460.0 | 105 |
| measured | 6 | 61,047.9 | 3.25 | 521.0 | 1,462.7 | 105 |
| measured | 7 | 61,019.0 | 3.25 | 521.3 | 1,459.5 | 105 |
| measured | 8 | 61,339.4 | 3.61 | 521.0 | 1,690.4 | 105 |
| measured | 9 | 61,994.1 | 3.19 | 521.6 | 1,457.4 | 105 |
| measured | 10 | 61,353.2 | 3.22 | 520.6 | 1,454.8 | 105 |
| measured | 11 | 61,770.3 | 3.21 | 522.0 | 1,458.6 | 105 |
| measured | 12 | 62,269.4 | 3.18 | 522.6 | 1,454.8 | 105 |
| measured | 13 | 61,554.6 | 3.55 | 724.5 | 1,458.5 | 105 |
| measured | 14 | 61,277.8 | 3.28 | 543.2 | 1,463.9 | 105 |
| measured | 15 | 64,091.3 | 3.0 | 521.4 | 1,401.8 | 105 |
| measured | 16 | 66,045.7 | 2.22 | 557.9 | 906.9 | 105 |
| measured | 17 | 69,703.1 | 2.52 | 521.8 | 1,235.7 | 105 |
| measured | 18 | 60,488.5 | 3.28 | 521.8 | 1,463.4 | 105 |
| measured | 19 | 67,578.0 | 2.93 | 521.1 | 1,459.4 | 105 |

## Reading notes

- `GPU busy %` is the union of all GPU intervals launched inside the iteration divided by the iteration wall.
  The remainder is host-side: Python dispatch, per-operator `cudaEventSynchronize`, CPU tool matmuls, pinned staging.
- `GPU/CPU` per operator compares launch-owned GPU time to the NVTX CPU range, which encloses a synchronize.
- Warmup rows are shown for context only; no measured statistic includes them.
- Plan `/workspace/AgentSys/artifacts/hybrid_reproduction/run_040/workloads/planner_debate/hybrid-plan.json` sha256 `aea4721200a14371…`; sqlite sha256 `8697309211081526…`.

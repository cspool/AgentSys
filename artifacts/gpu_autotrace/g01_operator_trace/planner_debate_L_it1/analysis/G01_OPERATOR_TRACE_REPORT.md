# G01 operator-wise single-GPU trace: `planner_debate_L_it1`

Lineage `h22-gpu-autotrace`, workflow w01. Real execution on one RTX 4090
(`0000:b1:00.0`), warmup 3 iterations discarded, 8 measured iterations. Attribution basis: NVTX operator range -> CUDA runtime API launched inside it -> CUPTI kernel/memcpy by correlationId.

## Conservation

| Quantity | Value |
|---|---:|
| Operator instances observed / expected | 320 / 320 |
| Measured wall per iteration (median) | 555,363.5 us |
| GPU busy per iteration (median, union of GPU intervals) | 5.5 % |
| Operator-owned GPU time (total over measured) | 135,468.9 us |
| Call-overhead GPU time (weight init, H2D/D2H, staging) | 108,581.3 us |
| Unattributed GPU items inside measured window | 0 (0.0 us) |
| Kernel launches over measured iterations | 840 |
| Warmup iteration 0 wall | 1,099,381.9 us |
| Warmup GPU busy (median) | 4.3 % |
| Pass | True |

## Operator-type breakdown (measured iterations)

| op_type | instances | kernel launches | GPU total (us) | GPU share | NVTX CPU total (us) | wall share | GPU per instance (us) |
|---|---:|---:|---:|---:|---:|---:|---:|
| call_overhead | 40 | 80 | 108,581.3 | 44.49 % | 0.0 | 0.0 % | 2,714.5 |
| LinearOp | 120 | 120 | 92,129.7 | 37.75 % | 103,267.7 | 2.31 % | 767.7 |
| RMSNormOp | 80 | 560 | 34,152.1 | 13.99 % | 41,747.5 | 0.93 % | 426.9 |
| TransposeOp | 40 | 40 | 8,278.0 | 3.39 % | 12,047.3 | 0.27 % | 207.0 |
| AddOp | 40 | 40 | 909.0 | 0.37 % | 3,823.6 | 0.09 % | 22.7 |
| ViewOp | 40 | 0 | 0.0 | 0.0 % | 2,771.5 | 0.06 % | 0.0 |

## Kernel-family breakdown (measured iterations)

| family | instances | GPU total (us) | share |
|---|---:|---:|---:|
| memcpy | 80 | 106,555.0 | 43.66 % |
| gemm | 120 | 92,067.7 | 37.72 % |
| copy | 200 | 21,551.6 | 8.83 % |
| elementwise_binary | 240 | 10,693.2 | 4.38 % |
| elementwise_unary | 160 | 9,358.7 | 3.83 % |
| reduce | 80 | 2,450.8 | 1.0 % |
| rng_init | 40 | 1,311.1 | 0.54 % |
| memset | 72 | 62.0 | 0.03 % |

## Per-operator summary (measured iterations)

| call | idx | op_type | engine | GPU median (us) | GPU min/max (us) | NVTX CPU median (us) | GPU/CPU | kernels |
|---|---:|---|---|---:|---:|---:|---:|---:|
| critic-a | 6 | RMSNormOp | ve | 517.7 | 515.6/519.2 | 632.7 | 81.8 % | 7 |
| critic-a | 7 | AddOp | ve | 27.1 | 26.5/27.5 | 93.3 | 28.8 % | 1 |
| critic-a | 8 | RMSNormOp | ve | 490.7 | 489.8/494.2 | 559.8 | 87.8 % | 7 |
| critic-a | 10 | LinearOp | me | 852.8 | 851.8/853.6 | 983.9 | 86.6 % | 1 |
| critic-a | 11 | LinearOp | me | 852.8 | 851.7/853.5 | 925.4 | 92.0 % | 1 |
| critic-a | 12 | LinearOp | me | 852.4 | 851.6/903.5 | 922.6 | 92.5 % | 1 |
| critic-a | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 67.3 | 0.0 % | 0 |
| critic-a | 14 | TransposeOp | de | 226.5 | 225.9/226.8 | 317.2 | 71.5 % | 1 |
| critic-a |  | call_overhead |  | 2,574.2 | 2,539.9/2,643.4 |  |  % | 2 |
| critic-b | 6 | RMSNormOp | ve | 517.8 | 516.7/522.1 | 642.1 | 79.5 % | 7 |
| critic-b | 7 | AddOp | ve | 26.9 | 26.8/27.2 | 96.6 | 27.8 % | 1 |
| critic-b | 8 | RMSNormOp | ve | 490.8 | 488.2/511.1 | 560.4 | 87.8 % | 7 |
| critic-b | 10 | LinearOp | me | 852.6 | 852.2/852.9 | 994.3 | 85.3 % | 1 |
| critic-b | 11 | LinearOp | me | 852.3 | 851.6/852.9 | 931.4 | 91.1 % | 1 |
| critic-b | 12 | LinearOp | me | 852.0 | 851.6/852.5 | 922.6 | 92.4 % | 1 |
| critic-b | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 69.4 | 0.0 % | 0 |
| critic-b | 14 | TransposeOp | de | 226.6 | 226.4/226.9 | 318.9 | 70.3 % | 1 |
| critic-b |  | call_overhead |  | 2,951.3 | 2,890.6/3,054.8 |  |  % | 2 |
| critic-merge | 6 | RMSNormOp | ve | 518.1 | 513.6/611.4 | 642.8 | 80.8 % | 7 |
| critic-merge | 7 | AddOp | ve | 27.1 | 26.6/50.2 | 94.9 | 26.1 % | 1 |
| critic-merge | 8 | RMSNormOp | ve | 491.4 | 488.5/493.1 | 562.5 | 87.3 % | 7 |
| critic-merge | 10 | LinearOp | me | 853.0 | 852.2/853.7 | 987.8 | 86.2 % | 1 |
| critic-merge | 11 | LinearOp | me | 852.1 | 851.7/852.6 | 929.2 | 91.7 % | 1 |
| critic-merge | 12 | LinearOp | me | 852.1 | 851.6/975.3 | 924.5 | 92.3 % | 1 |
| critic-merge | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 68.1 | 0.0 % | 0 |
| critic-merge | 14 | TransposeOp | de | 226.4 | 226.2/226.6 | 319.7 | 70.7 % | 1 |
| critic-merge |  | call_overhead |  | 3,013.7 | 2,906.0/3,157.6 |  |  % | 2 |
| planner-final | 6 | RMSNormOp | ve | 320.0 | 316.6/341.7 | 435.1 | 73.8 % | 7 |
| planner-final | 7 | AddOp | ve | 14.8 | 14.7/14.8 | 87.1 | 16.9 % | 1 |
| planner-final | 8 | RMSNormOp | ve | 291.1 | 288.6/292.8 | 357.3 | 81.4 % | 7 |
| planner-final | 10 | LinearOp | me | 636.2 | 634.6/685.2 | 769.1 | 82.8 % | 1 |
| planner-final | 11 | LinearOp | me | 633.2 | 632.7/635.0 | 705.7 | 89.6 % | 1 |
| planner-final | 12 | LinearOp | me | 635.8 | 634.5/638.7 | 703.0 | 90.6 % | 1 |
| planner-final | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 64.6 | 0.0 % | 0 |
| planner-final | 14 | TransposeOp | de | 177.6 | 177.1/177.8 | 266.9 | 63.4 % | 1 |
| planner-final |  | call_overhead |  | 3,820.8 | 3,687.8/4,041.3 |  |  % | 2 |
| planner-seed | 6 | RMSNormOp | ve | 321.4 | 316.7/322.6 | 434.6 | 72.7 % | 7 |
| planner-seed | 7 | AddOp | ve | 14.8 | 14.7/14.9 | 83.1 | 17.6 % | 1 |
| planner-seed | 8 | RMSNormOp | ve | 290.5 | 286.7/325.1 | 357.2 | 81.6 % | 7 |
| planner-seed | 10 | LinearOp | me | 635.8 | 634.9/637.5 | 761.5 | 83.5 % | 1 |
| planner-seed | 11 | LinearOp | me | 635.1 | 632.6/635.9 | 701.5 | 90.5 % | 1 |
| planner-seed | 12 | LinearOp | me | 634.9 | 634.0/635.8 | 698.4 | 90.9 % | 1 |
| planner-seed | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 63.2 | 0.0 % | 0 |
| planner-seed | 14 | TransposeOp | de | 177.7 | 177.2/177.9 | 264.5 | 66.7 % | 1 |
| planner-seed |  | call_overhead |  | 1,133.2 | 1,086.8/1,550.8 |  |  % | 2 |

## Per-iteration conservation

| phase | iter | wall (us) | GPU busy % | operator GPU (us) | overhead GPU (us) | launches |
|---|---:|---:|---:|---:|---:|---:|
| warmup | 0 | 1,099,381.9 | 2.82 | 17,018.8 | 13,939.1 | 105 |
| warmup | 1 | 702,327.5 | 4.3 | 17,045.9 | 13,151.4 | 105 |
| warmup | 2 | 656,309.0 | 4.65 | 17,088.8 | 13,410.1 | 105 |
| measured | 0 | 565,543.7 | 5.41 | 17,053.9 | 13,520.1 | 105 |
| measured | 1 | 554,283.6 | 5.59 | 16,926.3 | 14,080.1 | 105 |
| measured | 2 | 551,497.7 | 5.55 | 16,920.8 | 13,681.3 | 105 |
| measured | 3 | 551,130.8 | 5.55 | 16,887.7 | 13,719.8 | 105 |
| measured | 4 | 579,913.1 | 5.23 | 17,011.5 | 13,346.9 | 105 |
| measured | 5 | 558,873.2 | 5.41 | 16,879.6 | 13,357.2 | 105 |
| measured | 6 | 554,877.6 | 5.49 | 16,909.3 | 13,561.9 | 105 |
| measured | 7 | 555,849.4 | 5.43 | 16,879.7 | 13,313.9 | 105 |

## Reading notes

- `GPU busy %` is the union of all GPU intervals launched inside the iteration divided by the iteration wall.
  The remainder is host-side: Python dispatch, per-operator `cudaEventSynchronize`, CPU tool matmuls, pinned staging.
- `GPU/CPU` per operator compares launch-owned GPU time to the NVTX CPU range, which encloses a synchronize.
- Warmup rows are shown for context only; no measured statistic includes them.
- Plan `/workspace/AgentSys/artifacts/gpu_autotrace/scaled_plans/planner_debate_L_it1/hybrid-plan.json` sha256 `ab556eec6a77a7fd…`; sqlite sha256 `a8190a8bec34de07…`.

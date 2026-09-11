# G01 operator-wise single-GPU trace: `react_moa_mcts`

Lineage `h22-gpu-autotrace`, workflow w01. Real execution on one RTX 4090
(`0000:b1:00.0`), warmup 5 iterations discarded, 20 measured iterations. Attribution basis: NVTX operator range -> CUDA runtime API launched inside it -> CUPTI kernel/memcpy by correlationId.

## Conservation

| Quantity | Value |
|---|---:|
| Operator instances observed / expected | 1600 / 1600 |
| Measured wall per iteration (median) | 142,684.1 us |
| GPU busy per iteration (median, union of GPU intervals) | 2.4 % |
| Operator-owned GPU time (total over measured) | 22,338.2 us |
| Call-overhead GPU time (weight init, H2D/D2H, staging) | 44,784.9 us |
| Unattributed GPU items inside measured window | 0 (0.0 us) |
| Kernel launches over measured iterations | 4200 |
| Warmup iteration 0 wall | 629,585.6 us |
| Warmup GPU busy (median) | 2.09 % |
| Pass | True |

## Operator-type breakdown (measured iterations)

| op_type | instances | kernel launches | GPU total (us) | GPU share | NVTX CPU total (us) | wall share | GPU per instance (us) |
|---|---:|---:|---:|---:|---:|---:|---:|
| call_overhead | 200 | 400 | 44,784.9 | 66.72 % | 0.0 | 0.0 % | 223.9 |
| LinearOp | 600 | 600 | 11,599.6 | 17.28 % | 67,037.6 | 2.48 % | 19.3 |
| RMSNormOp | 400 | 2800 | 7,775.3 | 11.58 % | 97,436.2 | 3.61 % | 19.4 |
| TransposeOp | 200 | 200 | 2,508.5 | 3.74 % | 24,017.5 | 0.89 % | 12.5 |
| AddOp | 200 | 200 | 454.7 | 0.68 % | 20,499.2 | 0.76 % | 2.3 |
| ViewOp | 200 | 0 | 0.0 | 0.0 % | 14,316.5 | 0.53 % | 0.0 |

## Kernel-family breakdown (measured iterations)

| family | instances | GPU total (us) | share |
|---|---:|---:|---:|
| memcpy | 400 | 43,422.3 | 64.69 % |
| gemm | 600 | 11,573.4 | 17.24 % |
| copy | 1000 | 5,222.6 | 7.78 % |
| elementwise_binary | 1200 | 2,919.1 | 4.35 % |
| elementwise_unary | 800 | 1,642.0 | 2.45 % |
| reduce | 400 | 1,338.6 | 1.99 % |
| rng_init | 200 | 979.0 | 1.46 % |
| memset | 60 | 26.2 | 0.04 % |

## Per-operator summary (measured iterations)

| call | idx | op_type | engine | GPU median (us) | GPU min/max (us) | NVTX CPU median (us) | GPU/CPU | kernels |
|---|---:|---|---|---:|---:|---:|---:|---:|
| mcts-actor0 | 6 | RMSNormOp | ve | 19.4 | 19.1/72.1 | 248.4 | 8.2 % | 7 |
| mcts-actor0 | 7 | AddOp | ve | 2.1 | 1.9/2.1 | 102.5 | 2.0 % | 1 |
| mcts-actor0 | 8 | RMSNormOp | ve | 19.1 | 18.9/19.5 | 224.3 | 8.2 % | 7 |
| mcts-actor0 | 10 | LinearOp | me | 20.1 | 20.0/204.8 | 118.5 | 21.8 % | 1 |
| mcts-actor0 | 11 | LinearOp | me | 20.1 | 20.0/20.4 | 101.1 | 19.2 % | 1 |
| mcts-actor0 | 12 | LinearOp | me | 20.0 | 19.8/20.2 | 93.5 | 20.4 % | 1 |
| mcts-actor0 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 70.0 | 0.0 % | 0 |
| mcts-actor0 | 14 | TransposeOp | de | 12.4 | 12.2/12.7 | 121.6 | 10.4 % | 1 |
| mcts-actor0 |  | call_overhead |  | 191.8 | 183.5/325.1 |  |  % | 2 |
| mcts-actor1 | 6 | RMSNormOp | ve | 19.3 | 19.1/19.6 | 243.8 | 7.3 % | 7 |
| mcts-actor1 | 7 | AddOp | ve | 2.0 | 1.9/2.1 | 97.2 | 1.9 % | 1 |
| mcts-actor1 | 8 | RMSNormOp | ve | 19.1 | 18.9/83.3 | 225.6 | 10.0 % | 7 |
| mcts-actor1 | 10 | LinearOp | me | 20.2 | 20.0/20.4 | 125.3 | 15.8 % | 1 |
| mcts-actor1 | 11 | LinearOp | me | 20.2 | 20.0/20.3 | 98.9 | 20.1 % | 1 |
| mcts-actor1 | 12 | LinearOp | me | 20.1 | 19.8/20.3 | 94.5 | 21.0 % | 1 |
| mcts-actor1 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 71.0 | 0.0 % | 0 |
| mcts-actor1 | 14 | TransposeOp | de | 12.5 | 12.2/108.9 | 124.1 | 13.9 % | 1 |
| mcts-actor1 |  | call_overhead |  | 191.0 | 183.3/326.2 |  |  % | 2 |
| mcts-critic | 6 | RMSNormOp | ve | 19.4 | 19.1/133.5 | 243.6 | 10.3 % | 7 |
| mcts-critic | 7 | AddOp | ve | 2.1 | 2.0/47.1 | 102.4 | 4.8 % | 1 |
| mcts-critic | 8 | RMSNormOp | ve | 19.1 | 18.9/19.3 | 220.4 | 8.6 % | 7 |
| mcts-critic | 10 | LinearOp | me | 20.1 | 19.9/20.3 | 114.6 | 15.7 % | 1 |
| mcts-critic | 11 | LinearOp | me | 20.1 | 20.0/20.3 | 100.6 | 19.6 % | 1 |
| mcts-critic | 12 | LinearOp | me | 20.1 | 19.9/20.2 | 95.6 | 20.3 % | 1 |
| mcts-critic | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 69.2 | 0.0 % | 0 |
| mcts-critic | 14 | TransposeOp | de | 12.4 | 12.2/12.6 | 112.8 | 10.3 % | 1 |
| mcts-critic |  | call_overhead |  | 259.6 | 250.8/449.7 |  |  % | 2 |
| mcts-root | 6 | RMSNormOp | ve | 19.4 | 19.2/19.5 | 253.6 | 7.2 % | 7 |
| mcts-root | 7 | AddOp | ve | 2.1 | 2.0/2.1 | 101.5 | 2.0 % | 1 |
| mcts-root | 8 | RMSNormOp | ve | 19.1 | 18.7/19.3 | 216.0 | 8.6 % | 7 |
| mcts-root | 10 | LinearOp | me | 20.1 | 19.9/20.3 | 118.2 | 15.9 % | 1 |
| mcts-root | 11 | LinearOp | me | 20.2 | 19.9/20.3 | 95.7 | 20.2 % | 1 |
| mcts-root | 12 | LinearOp | me | 20.1 | 19.8/20.2 | 93.6 | 20.9 % | 1 |
| mcts-root | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 66.5 | 0.0 % | 0 |
| mcts-root | 14 | TransposeOp | de | 12.3 | 12.2/12.7 | 113.6 | 10.3 % | 1 |
| mcts-root |  | call_overhead |  | 190.9 | 176.6/339.0 |  |  % | 2 |
| moa-map0 | 6 | RMSNormOp | ve | 19.4 | 19.3/19.5 | 255.8 | 7.3 % | 7 |
| moa-map0 | 7 | AddOp | ve | 2.1 | 2.0/2.1 | 101.0 | 2.0 % | 1 |
| moa-map0 | 8 | RMSNormOp | ve | 19.1 | 18.8/19.3 | 219.9 | 8.5 % | 7 |
| moa-map0 | 10 | LinearOp | me | 20.1 | 20.0/20.2 | 114.8 | 16.1 % | 1 |
| moa-map0 | 11 | LinearOp | me | 20.1 | 20.0/20.3 | 97.0 | 19.8 % | 1 |
| moa-map0 | 12 | LinearOp | me | 20.1 | 19.8/20.2 | 95.1 | 20.9 % | 1 |
| moa-map0 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 68.0 | 0.0 % | 0 |
| moa-map0 | 14 | TransposeOp | de | 12.4 | 12.1/12.6 | 114.8 | 10.5 % | 1 |
| moa-map0 |  | call_overhead |  | 153.9 | 142.6/253.1 |  |  % | 2 |
| moa-map1 | 6 | RMSNormOp | ve | 19.4 | 19.2/19.5 | 243.4 | 7.6 % | 7 |
| moa-map1 | 7 | AddOp | ve | 2.1 | 2.0/2.1 | 100.2 | 2.0 % | 1 |
| moa-map1 | 8 | RMSNormOp | ve | 19.1 | 18.9/19.2 | 219.1 | 8.4 % | 7 |
| moa-map1 | 10 | LinearOp | me | 20.2 | 20.0/20.4 | 117.5 | 16.1 % | 1 |
| moa-map1 | 11 | LinearOp | me | 20.1 | 20.0/20.3 | 95.3 | 20.6 % | 1 |
| moa-map1 | 12 | LinearOp | me | 20.1 | 19.9/129.3 | 94.0 | 24.9 % | 1 |
| moa-map1 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 70.2 | 0.0 % | 0 |
| moa-map1 | 14 | TransposeOp | de | 12.3 | 12.1/12.7 | 112.7 | 10.4 % | 1 |
| moa-map1 |  | call_overhead |  | 193.0 | 183.3/327.2 |  |  % | 2 |
| moa-map2 | 6 | RMSNormOp | ve | 19.3 | 19.1/30.0 | 245.4 | 7.6 % | 7 |
| moa-map2 | 7 | AddOp | ve | 2.1 | 2.0/2.1 | 99.2 | 2.1 % | 1 |
| moa-map2 | 8 | RMSNormOp | ve | 19.1 | 18.8/19.3 | 216.4 | 8.6 % | 7 |
| moa-map2 | 10 | LinearOp | me | 20.1 | 19.9/20.2 | 120.3 | 16.0 % | 1 |
| moa-map2 | 11 | LinearOp | me | 20.1 | 20.0/20.3 | 97.6 | 19.8 % | 1 |
| moa-map2 | 12 | LinearOp | me | 20.0 | 19.9/20.2 | 93.9 | 20.8 % | 1 |
| moa-map2 | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 68.4 | 0.0 % | 0 |
| moa-map2 | 14 | TransposeOp | de | 12.4 | 12.1/12.8 | 115.2 | 10.4 % | 1 |
| moa-map2 |  | call_overhead |  | 190.8 | 183.3/325.7 |  |  % | 2 |
| moa-reduce | 6 | RMSNormOp | ve | 19.3 | 19.1/19.5 | 245.1 | 7.5 % | 7 |
| moa-reduce | 7 | AddOp | ve | 2.1 | 2.0/2.1 | 97.8 | 2.0 % | 1 |
| moa-reduce | 8 | RMSNormOp | ve | 19.1 | 18.8/19.3 | 220.9 | 8.5 % | 7 |
| moa-reduce | 10 | LinearOp | me | 20.1 | 20.0/20.3 | 121.4 | 15.3 % | 1 |
| moa-reduce | 11 | LinearOp | me | 20.1 | 20.0/32.2 | 100.1 | 20.7 % | 1 |
| moa-reduce | 12 | LinearOp | me | 20.0 | 19.9/20.2 | 94.2 | 20.3 % | 1 |
| moa-reduce | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 69.8 | 0.0 % | 0 |
| moa-reduce | 14 | TransposeOp | de | 12.4 | 12.3/12.7 | 117.4 | 10.5 % | 1 |
| moa-reduce |  | call_overhead |  | 190.8 | 183.1/324.5 |  |  % | 2 |
| react-answer | 6 | RMSNormOp | ve | 17.9 | 17.7/18.0 | 244.6 | 7.0 % | 7 |
| react-answer | 7 | AddOp | ve | 1.7 | 1.7/1.8 | 97.8 | 1.7 % | 1 |
| react-answer | 8 | RMSNormOp | ve | 17.3 | 17.2/17.6 | 218.3 | 7.7 % | 7 |
| react-answer | 10 | LinearOp | me | 14.6 | 14.6/14.7 | 121.0 | 11.2 % | 1 |
| react-answer | 11 | LinearOp | me | 14.6 | 14.5/14.7 | 99.7 | 14.2 % | 1 |
| react-answer | 12 | LinearOp | me | 14.5 | 14.5/14.6 | 94.2 | 15.2 % | 1 |
| react-answer | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 68.9 | 0.0 % | 0 |
| react-answer | 14 | TransposeOp | de | 12.1 | 12.1/12.3 | 111.1 | 10.1 % | 1 |
| react-answer |  | call_overhead |  | 167.0 | 162.5/286.7 |  |  % | 2 |
| react-plan | 6 | RMSNormOp | ve | 15.9 | 15.7/16.1 | 244.4 | 6.3 % | 7 |
| react-plan | 7 | AddOp | ve | 1.4 | 1.4/1.5 | 97.1 | 1.4 % | 1 |
| react-plan | 8 | RMSNormOp | ve | 15.3 | 15.1/15.6 | 221.8 | 6.8 % | 7 |
| react-plan | 10 | LinearOp | me | 12.9 | 12.8/13.1 | 164.3 | 7.4 % | 1 |
| react-plan | 11 | LinearOp | me | 12.7 | 12.6/12.9 | 117.3 | 10.5 % | 1 |
| react-plan | 12 | LinearOp | me | 12.7 | 12.6/12.8 | 108.4 | 11.5 % | 1 |
| react-plan | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 68.4 | 0.0 % | 0 |
| react-plan | 14 | TransposeOp | de | 9.4 | 9.3/9.4 | 118.7 | 7.7 % | 1 |
| react-plan |  | call_overhead |  | 58.0 | 54.7/90.9 |  |  % | 2 |

## Per-iteration conservation

| phase | iter | wall (us) | GPU busy % | operator GPU (us) | overhead GPU (us) | launches |
|---|---:|---:|---:|---:|---:|---:|
| warmup | 0 | 629,585.6 | 0.62 | 1,081.9 | 2,821.7 | 210 |
| warmup | 1 | 150,998.8 | 2.31 | 1,079.4 | 2,408.4 | 210 |
| warmup | 2 | 148,636.5 | 2.25 | 1,079.0 | 2,268.9 | 210 |
| warmup | 3 | 147,611.5 | 2.09 | 1,078.1 | 2,003.8 | 210 |
| warmup | 4 | 147,532.2 | 2.05 | 1,078.9 | 1,940.2 | 210 |
| measured | 0 | 146,369.3 | 2.0 | 1,077.3 | 1,847.2 | 210 |
| measured | 1 | 146,838.3 | 1.99 | 1,143.2 | 1,772.3 | 210 |
| measured | 2 | 145,527.2 | 1.94 | 1,079.3 | 1,744.3 | 210 |
| measured | 3 | 144,985.0 | 1.94 | 1,079.6 | 1,732.1 | 210 |
| measured | 4 | 146,930.3 | 1.92 | 1,080.0 | 1,746.3 | 210 |
| measured | 5 | 140,383.2 | 2.08 | 1,175.8 | 1,744.9 | 210 |
| measured | 6 | 115,777.4 | 2.43 | 1,079.4 | 1,732.5 | 210 |
| measured | 7 | 116,319.9 | 2.51 | 1,188.5 | 1,732.8 | 210 |
| measured | 8 | 114,418.0 | 2.46 | 1,079.3 | 1,736.1 | 210 |
| measured | 9 | 146,467.0 | 1.93 | 1,079.5 | 1,745.4 | 210 |
| measured | 10 | 145,693.5 | 2.0 | 1,078.5 | 1,839.1 | 210 |
| measured | 11 | 146,197.2 | 1.96 | 1,077.9 | 1,794.0 | 210 |
| measured | 12 | 150,379.2 | 2.49 | 1,089.8 | 2,654.6 | 210 |
| measured | 13 | 151,565.2 | 2.71 | 1,091.5 | 3,017.2 | 210 |
| measured | 14 | 126,297.8 | 3.35 | 1,210.0 | 3,020.5 | 210 |
| measured | 15 | 127,242.8 | 3.19 | 1,079.5 | 2,983.7 | 210 |
| measured | 16 | 127,115.0 | 3.18 | 1,078.9 | 2,967.1 | 210 |
| measured | 17 | 121,902.5 | 3.38 | 1,132.5 | 2,992.4 | 210 |
| measured | 18 | 120,345.4 | 3.53 | 1,264.6 | 2,988.1 | 210 |
| measured | 19 | 119,541.7 | 3.49 | 1,173.3 | 2,994.4 | 210 |

## Reading notes

- `GPU busy %` is the union of all GPU intervals launched inside the iteration divided by the iteration wall.
  The remainder is host-side: Python dispatch, per-operator `cudaEventSynchronize`, CPU tool matmuls, pinned staging.
- `GPU/CPU` per operator compares launch-owned GPU time to the NVTX CPU range, which encloses a synchronize.
- Warmup rows are shown for context only; no measured statistic includes them.
- Plan `/workspace/AgentSys/artifacts/hybrid_reproduction/run_040/workloads/react_moa_mcts/hybrid-plan.json` sha256 `80185d341d878e7b…`; sqlite sha256 `5d8ccc6d09d71ce6…`.

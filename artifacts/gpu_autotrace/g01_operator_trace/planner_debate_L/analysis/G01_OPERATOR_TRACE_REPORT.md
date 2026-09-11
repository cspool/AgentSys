# G01 operator-wise single-GPU trace: `planner_debate_L`

Lineage `h22-gpu-autotrace`, workflow w01. Real execution on one RTX 4090
(`0000:b1:00.0`), warmup 3 iterations discarded, 8 measured iterations. Attribution basis: NVTX operator range -> CUDA runtime API launched inside it -> CUPTI kernel/memcpy by correlationId.

## Conservation

| Quantity | Value |
|---|---:|
| Operator instances observed / expected | 320 / 320 |
| Measured wall per iteration (median) | 1,079,106.6 us |
| GPU busy per iteration (median, union of GPU intervals) | 50.1 % |
| Operator-owned GPU time (total over measured) | 4,207,926.7 us |
| Call-overhead GPU time (weight init, H2D/D2H, staging) | 106,705.2 us |
| Unattributed GPU items inside measured window | 0 (0.0 us) |
| Kernel launches over measured iterations | 24400 |
| Warmup iteration 0 wall | 1,655,711.4 us |
| Warmup GPU busy (median) | 44.35 % |
| Pass | True |

## Operator-type breakdown (measured iterations)

| op_type | instances | kernel launches | GPU total (us) | GPU share | NVTX CPU total (us) | wall share | GPU per instance (us) |
|---|---:|---:|---:|---:|---:|---:|---:|
| LinearOp | 120 | 3840 | 2,858,149.0 | 66.24 % | 2,878,961.1 | 33.39 % | 23,817.9 |
| RMSNormOp | 80 | 17920 | 1,062,142.2 | 24.62 % | 1,082,436.9 | 12.56 % | 13,276.8 |
| TransposeOp | 40 | 1280 | 265,052.5 | 6.14 % | 270,576.6 | 3.14 % | 6,626.3 |
| call_overhead | 40 | 80 | 106,705.2 | 2.47 % | 0.0 | 0.0 % | 2,667.6 |
| AddOp | 40 | 1280 | 22,583.0 | 0.52 % | 27,947.3 | 0.32 % | 564.6 |
| ViewOp | 40 | 0 | 0.0 | 0.0 % | 6,781.2 | 0.08 % | 0.0 |

## Kernel-family breakdown (measured iterations)

| family | instances | GPU total (us) | share |
|---|---:|---:|---:|
| gemm | 3840 | 2,855,280.2 | 66.18 % |
| copy | 6400 | 647,866.1 | 15.02 % |
| elementwise_binary | 6440 | 315,637.7 | 7.32 % |
| elementwise_unary | 5120 | 308,146.5 | 7.14 % |
| memcpy | 80 | 104,791.1 | 2.43 % |
| reduce | 2560 | 78,865.1 | 1.83 % |
| memset | 2304 | 2,868.8 | 0.07 % |
| rng_init | 40 | 1,176.5 | 0.03 % |

## Per-operator summary (measured iterations)

| call | idx | op_type | engine | GPU median (us) | GPU min/max (us) | NVTX CPU median (us) | GPU/CPU | kernels |
|---|---:|---|---|---:|---:|---:|---:|---:|
| critic-a | 6 | RMSNormOp | ve | 16,258.6 | 15,840.5/16,318.9 | 16,533.4 | 98.3 % | 224 |
| critic-a | 7 | AddOp | ve | 646.1 | 643.1/666.1 | 758.1 | 84.4 % | 32 |
| critic-a | 8 | RMSNormOp | ve | 15,802.6 | 15,774.2/15,857.4 | 16,034.1 | 98.4 % | 224 |
| critic-a | 10 | LinearOp | me | 25,815.0 | 25,453.9/26,170.1 | 26,071.3 | 99.2 % | 32 |
| critic-a | 11 | LinearOp | me | 26,283.6 | 25,675.0/27,033.1 | 26,432.5 | 99.4 % | 32 |
| critic-a | 12 | LinearOp | me | 26,721.7 | 25,970.9/26,957.8 | 26,866.9 | 99.4 % | 32 |
| critic-a | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 172.8 | 0.0 % | 0 |
| critic-a | 14 | TransposeOp | de | 7,250.4 | 7,167.1/7,736.3 | 7,397.6 | 98.2 % | 32 |
| critic-a |  | call_overhead |  | 2,558.3 | 2,511.5/2,679.8 |  |  % | 2 |
| critic-b | 6 | RMSNormOp | ve | 15,988.8 | 15,806.3/16,242.3 | 16,341.7 | 98.2 % | 224 |
| critic-b | 7 | AddOp | ve | 644.0 | 638.9/782.0 | 755.8 | 85.5 % | 32 |
| critic-b | 8 | RMSNormOp | ve | 16,076.3 | 15,805.4/16,245.2 | 16,301.2 | 98.6 % | 224 |
| critic-b | 10 | LinearOp | me | 25,796.6 | 25,475.0/26,150.9 | 26,026.5 | 99.1 % | 32 |
| critic-b | 11 | LinearOp | me | 26,637.7 | 25,915.1/26,893.8 | 26,772.5 | 99.3 % | 32 |
| critic-b | 12 | LinearOp | me | 26,952.4 | 25,904.7/27,595.0 | 27,107.5 | 99.4 % | 32 |
| critic-b | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 172.2 | 0.0 % | 0 |
| critic-b | 14 | TransposeOp | de | 7,192.9 | 6,807.9/7,353.5 | 7,344.4 | 98.0 % | 32 |
| critic-b |  | call_overhead |  | 2,891.9 | 2,841.0/3,389.3 |  |  % | 2 |
| critic-merge | 6 | RMSNormOp | ve | 16,005.5 | 15,831.5/16,268.7 | 16,280.7 | 98.3 % | 224 |
| critic-merge | 7 | AddOp | ve | 644.9 | 640.2/657.5 | 759.0 | 84.2 % | 32 |
| critic-merge | 8 | RMSNormOp | ve | 16,079.6 | 15,773.6/16,259.2 | 16,299.6 | 98.7 % | 224 |
| critic-merge | 10 | LinearOp | me | 25,977.0 | 25,470.4/26,303.1 | 26,230.8 | 99.2 % | 32 |
| critic-merge | 11 | LinearOp | me | 26,049.3 | 25,578.9/26,804.7 | 26,358.6 | 99.1 % | 32 |
| critic-merge | 12 | LinearOp | me | 26,848.0 | 25,618.8/27,302.1 | 27,023.8 | 99.3 % | 32 |
| critic-merge | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 162.7 | 0.0 % | 0 |
| critic-merge | 14 | TransposeOp | de | 7,195.5 | 6,735.8/7,766.8 | 7,319.0 | 98.1 % | 32 |
| critic-merge |  | call_overhead |  | 2,884.5 | 2,858.1/2,915.5 |  |  % | 2 |
| planner-final | 6 | RMSNormOp | ve | 9,042.8 | 9,012.4/9,484.9 | 9,327.4 | 97.1 % | 224 |
| planner-final | 7 | AddOp | ve | 431.9 | 431.5/444.2 | 555.2 | 76.1 % | 32 |
| planner-final | 8 | RMSNormOp | ve | 9,525.9 | 8,973.6/9,551.1 | 9,738.5 | 97.8 % | 224 |
| planner-final | 10 | LinearOp | me | 19,883.7 | 19,613.4/20,000.5 | 20,063.7 | 99.2 % | 32 |
| planner-final | 11 | LinearOp | me | 20,034.0 | 19,933.9/20,228.9 | 20,151.6 | 99.4 % | 32 |
| planner-final | 12 | LinearOp | me | 20,439.3 | 19,980.7/20,755.9 | 20,572.4 | 99.4 % | 32 |
| planner-final | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 159.7 | 0.0 % | 0 |
| planner-final | 14 | TransposeOp | de | 5,730.4 | 5,318.7/6,161.6 | 5,879.7 | 97.8 % | 32 |
| planner-final |  | call_overhead |  | 3,694.8 | 3,646.0/4,115.5 |  |  % | 2 |
| planner-seed | 6 | RMSNormOp | ve | 9,107.9 | 9,010.2/9,544.6 | 9,417.9 | 97.0 % | 224 |
| planner-seed | 7 | AddOp | ve | 431.9 | 431.3/443.6 | 595.2 | 70.4 % | 32 |
| planner-seed | 8 | RMSNormOp | ve | 8,992.0 | 8,968.9/9,050.4 | 9,218.7 | 97.5 % | 224 |
| planner-seed | 10 | LinearOp | me | 19,901.1 | 19,861.3/20,271.1 | 20,077.9 | 99.1 % | 32 |
| planner-seed | 11 | LinearOp | me | 20,024.2 | 19,808.3/20,353.0 | 20,136.8 | 99.5 % | 32 |
| planner-seed | 12 | LinearOp | me | 20,449.4 | 19,708.7/21,080.0 | 20,560.3 | 99.4 % | 32 |
| planner-seed | 13 | ViewOp | de | 0.0 | 0.0/0.0 | 167.2 | 0.0 % | 0 |
| planner-seed | 14 | TransposeOp | de | 5,719.8 | 5,301.5/6,216.2 | 5,858.7 | 97.6 % | 32 |
| planner-seed |  | call_overhead |  | 1,099.7 | 1,080.6/1,672.2 |  |  % | 2 |

## Per-iteration conservation

| phase | iter | wall (us) | GPU busy % | operator GPU (us) | overhead GPU (us) | launches |
|---|---:|---:|---:|---:|---:|---:|
| warmup | 0 | 1,655,711.4 | 33.1 | 534,376.8 | 13,671.3 | 3050 |
| warmup | 1 | 1,219,345.3 | 44.35 | 526,960.3 | 13,853.9 | 3050 |
| warmup | 2 | 1,124,368.5 | 48.13 | 527,961.6 | 13,146.6 | 3050 |
| measured | 0 | 1,083,889.7 | 49.93 | 527,667.9 | 13,524.9 | 3050 |
| measured | 1 | 1,080,047.8 | 49.93 | 526,103.5 | 13,143.1 | 3050 |
| measured | 2 | 1,080,541.6 | 50.16 | 528,255.7 | 13,780.5 | 3050 |
| measured | 3 | 1,091,364.8 | 49.14 | 523,032.2 | 13,262.9 | 3050 |
| measured | 4 | 1,072,111.7 | 50.18 | 524,882.5 | 13,075.9 | 3050 |
| measured | 5 | 1,078,165.5 | 50.11 | 527,116.7 | 13,133.8 | 3050 |
| measured | 6 | 1,057,270.3 | 50.87 | 524,649.8 | 13,137.4 | 3050 |
| measured | 7 | 1,077,607.6 | 50.1 | 526,218.4 | 13,646.6 | 3050 |

## Reading notes

- `GPU busy %` is the union of all GPU intervals launched inside the iteration divided by the iteration wall.
  The remainder is host-side: Python dispatch, per-operator `cudaEventSynchronize`, CPU tool matmuls, pinned staging.
- `GPU/CPU` per operator compares launch-owned GPU time to the NVTX CPU range, which encloses a synchronize.
- Warmup rows are shown for context only; no measured statistic includes them.
- Plan `/workspace/AgentSys/artifacts/gpu_autotrace/scaled_plans/planner_debate_L/hybrid-plan.json` sha256 `a459992281edf4f6…`; sqlite sha256 `65cd39b1417a689a…`.

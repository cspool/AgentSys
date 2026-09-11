# G02/G03 call-wise process attribution: `react_moa_mcts`

Lineage `h22-gpu-autotrace`, workflow w02. Consumes the w01 trace only; no re-timing.
Host events aligned to the nsys clock by a constant offset fitted on 1600 operator pairs (spread 24.0 us).

## Conservation

| Quantity | Value |
|---|---:|
| Measured iterations | 20 |
| Sum of process segments minus iteration wall (max abs) | 0 ns |
| GPU work attributed here minus w01 attributed GPU | 0 ns |
| Unnamed gap time | 0.0 us |
| Pass | True |

## Process-type breakdown (share of measured wall)

| process | instances | host total (us) | host share | per instance (us) | GPU total (us) | GPU share | CUDA API share of host | GPU/host |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| host_input_generate | 200 | 2,016,623.4 | 74.68 % | 10,083.1 | 0.0 | 0.0 % | 0.1 % | 0.0 % |
| adapter_dispatch | 200 | 235,764.7 | 8.73 % | 1,178.8 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:RMSNormOp | 400 | 97,436.2 | 3.61 % | 243.6 | 7,775.3 | 11.58 % | 28.1 % | 8.0 % |
| mir_operator:LinearOp | 600 | 67,037.6 | 2.48 % | 111.7 | 11,599.6 | 17.28 % | 24.7 % | 17.3 % |
| token_preprocess_cpu | 200 | 59,118.0 | 2.19 % | 295.6 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| h2d_stage | 200 | 40,168.6 | 1.49 % | 200.8 | 21,334.6 | 31.78 % | 60.7 % | 53.1 % |
| d2h_stage | 200 | 32,711.6 | 1.21 % | 163.6 | 22,087.7 | 32.91 % | 70.5 % | 67.5 % |
| dag_schedule_gap | 220 | 29,714.4 | 1.1 % | 135.1 | 0.0 | 0.0 % | 2.7 % | 0.0 % |
| weight_init | 200 | 28,222.6 | 1.05 % | 141.1 | 1,362.7 | 2.03 % | 22.8 % | 4.8 % |
| mir_operator:TransposeOp | 200 | 24,017.5 | 0.89 % | 120.1 | 2,508.5 | 3.74 % | 22.4 % | 10.4 % |
| mir_operator:AddOp | 200 | 20,499.2 | 0.76 % | 102.5 | 454.7 | 0.68 % | 25.5 % | 2.2 % |
| mir_operator:ViewOp | 200 | 14,316.5 | 0.53 % | 71.6 | 0.0 | 0.0 % | 20.3 % | 0.0 % |
| checksum_complete | 200 | 13,089.3 | 0.48 % | 65.4 | 0.0 | 0.0 % | 2.9 % | 0.0 % |
| inter_operator_dispatch | 1400 | 11,259.7 | 0.42 % | 8.0 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| agent_tool_execute_cpu | 20 | 6,494.7 | 0.24 % | 324.7 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| pre_d2h_alloc | 200 | 2,583.3 | 0.1 % | 12.9 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| iteration_tail_sync | 20 | 1,238.5 | 0.05 % | 61.9 | 0.0 | 0.0 % | 21.1 % | 0.0 % |

## Call breakdown (agent nodes)

| call | kind | wave | matrix | host per iter (us) | host share | GPU per iter (us) | GPU share | GPU/host |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| react-plan | llm | 0 | 768 | 10,088.7 | 7.47 % | 213.3 | 6.36 % | 2.11 % |
| moa-map0 | llm | 0 | 1024 | 13,965.3 | 10.34 % | 350.2 | 10.43 % | 2.51 % |
| moa-map1 | llm | 0 | 1024 | 13,867.4 | 10.27 % | 355.2 | 10.58 % | 2.56 % |
| moa-map2 | llm | 0 | 1024 | 13,916.5 | 10.31 % | 353.3 | 10.53 % | 2.54 % |
| mcts-root | llm | 0 | 1024 | 13,881.1 | 10.28 % | 352.6 | 10.51 % | 2.54 % |
| react-tool | tool | 1 | 256 | 324.7 | 0.24 % | 0.0 | 0.0 % | 0.0 % |
| mcts-actor0 | llm | 1 | 1024 | 14,217.6 | 10.53 % | 366.7 | 10.93 % | 2.58 % |
| mcts-actor1 | llm | 1 | 1024 | 13,829.7 | 10.24 % | 367.4 | 10.95 % | 2.66 % |
| moa-reduce | llm | 1 | 1024 | 13,917.7 | 10.31 % | 354.3 | 10.56 % | 2.55 % |
| react-answer | llm | 2 | 896 | 11,624.6 | 8.61 % | 277.4 | 8.26 % | 2.39 % |
| mcts-critic | llm | 2 | 1024 | 13,833.8 | 10.25 % | 365.8 | 10.9 % | 2.64 % |
| <dag> | dag |  |  | 1,547.6 | 1.15 % | 0.0 | 0.0 % | 0.0 % |

## CUDA runtime API inside the measured window

| API | calls | total (us) | share of wall |
|---|---:|---:|---:|
| cudaEventSynchronize | 2000 | 41,038.9 | 1.52 % |
| cudaLaunchKernel | 4140 | 34,780.3 | 1.29 % |
| cudaEventRecord | 4400 | 17,703.3 | 0.66 % |
| cudaEventCreateWithFlags | 4000 | 7,413.0 | 0.27 % |
| cudaMemcpyAsync | 400 | 5,545.6 | 0.21 % |
| cudaEventDestroy | 4000 | 4,307.9 | 0.16 % |
| cudaEventQuery | 400 | 1,410.9 | 0.05 % |
| cuLaunchKernel | 60 | 600.8 | 0.02 % |
| cudaMemsetAsync | 60 | 564.9 | 0.02 % |
| cudaStreamIsCapturing | 600 | 534.7 | 0.02 % |
| cudaDeviceSynchronize | 20 | 170.7 | 0.01 % |
| cuKernelGetFunction | 60 | 128.1 | 0.0 % |

## Kernel families by process (G03)

| process | family | instances | GPU total (us) | share |
|---|---|---:|---:|---:|
| d2h_stage | memcpy | 200 | 22,087.7 | 32.91 % |
| h2d_stage | memcpy | 200 | 21,334.6 | 31.78 % |
| mir_operator:LinearOp | gemm | 600 | 11,573.4 | 17.24 % |
| mir_operator:RMSNormOp | copy | 800 | 2,714.0 | 4.04 % |
| mir_operator:TransposeOp | copy | 200 | 2,508.5 | 3.74 % |
| mir_operator:RMSNormOp | elementwise_binary | 800 | 2,080.7 | 3.1 % |
| mir_operator:RMSNormOp | elementwise_unary | 800 | 1,642.0 | 2.45 % |
| mir_operator:RMSNormOp | reduce | 400 | 1,338.6 | 1.99 % |
| weight_init | rng_init | 200 | 979.0 | 1.46 % |
| mir_operator:AddOp | elementwise_binary | 200 | 454.7 | 0.68 % |
| weight_init | elementwise_binary | 200 | 383.7 | 0.57 % |
| mir_operator:LinearOp | memset | 60 | 26.2 | 0.04 % |

## Kernel launch order, representative iteration 3 (G03)

| # | call | process | kind | family | GPU (us) | launch latency (us) | grid | block |
|---:|---|---|---|---|---:|---:|---|---|
| 1 | react-plan | h2d_stage | memcpy | memcpy | 49.8 | 10.8 | 0x0x0 | 0x0x0 |
| 2 | react-plan | weight_init | kernel | rng_init | 3.6 | 13.6 | 768x1x1 | 256x1x1 |
| 3 | react-plan | weight_init | kernel | elementwise_binary | 1.4 | 7.0 | 576x1x1 | 128x1x1 |
| 4 | react-plan | mir_operator:RMSNormOp:6 | kernel | copy | 3.6 | 8.7 | 576x1x1 | 128x1x1 |
| 5 | react-plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 2.1 | 6.5 | 576x1x1 | 128x1x1 |
| 6 | react-plan | mir_operator:RMSNormOp:6 | kernel | reduce | 3.2 | 6.2 | 48x1x1 | 32x16x1 |
| 7 | react-plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 6.1 | 1x1x1 | 128x1x1 |
| 8 | react-plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.2 | 5.9 | 1x1x1 | 128x1x1 |
| 9 | react-plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 2.9 | 6.3 | 2304x1x1 | 128x1x1 |
| 10 | react-plan | mir_operator:RMSNormOp:6 | kernel | copy | 1.7 | 6.4 | 576x1x1 | 128x1x1 |
| 11 | react-plan | mir_operator:AddOp:7 | kernel | elementwise_binary | 1.4 | 8.4 | 576x1x1 | 128x1x1 |
| 12 | react-plan | mir_operator:RMSNormOp:8 | kernel | copy | 3.5 | 8.7 | 576x1x1 | 128x1x1 |
| 13 | react-plan | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 2.1 | 6.3 | 576x1x1 | 128x1x1 |
| 14 | react-plan | mir_operator:RMSNormOp:8 | kernel | reduce | 3.0 | 6.0 | 48x1x1 | 32x16x1 |
| 15 | react-plan | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 1.1 | 5.8 | 1x1x1 | 128x1x1 |
| 16 | react-plan | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 1.2 | 5.9 | 1x1x1 | 128x1x1 |
| 17 | react-plan | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 2.9 | 6.0 | 2304x1x1 | 128x1x1 |
| 18 | react-plan | mir_operator:RMSNormOp:8 | kernel | copy | 1.7 | 6.2 | 576x1x1 | 128x1x1 |
| 19 | react-plan | mir_operator:LinearOp:10 | memset | memset | 0.4 | 13.9 | 0x0x0 | 0x0x0 |
| 20 | react-plan | mir_operator:LinearOp:10 | kernel | gemm | 12.4 | 8.6 | 96x2x2 | 128x1x1 |
| 21 | react-plan | mir_operator:LinearOp:11 | memset | memset | 0.4 | 6.9 | 0x0x0 | 0x0x0 |
| 22 | react-plan | mir_operator:LinearOp:11 | kernel | gemm | 12.4 | 8.1 | 96x2x2 | 128x1x1 |
| 23 | react-plan | mir_operator:LinearOp:12 | memset | memset | 0.4 | 7.5 | 0x0x0 | 0x0x0 |
| 24 | react-plan | mir_operator:LinearOp:12 | kernel | gemm | 12.2 | 8.1 | 96x2x2 | 128x1x1 |
| 25 | react-plan | mir_operator:TransposeOp:14 | kernel | copy | 9.3 | 9.6 | 1152x1x1 | 128x1x1 |
| 26 | react-plan | d2h_stage | memcpy | memcpy | 61.4 | 13.5 | 0x0x0 | 0x0x0 |
| 27 | moa-map0 | h2d_stage | memcpy | memcpy | 87.8 | 11.6 | 0x0x0 | 0x0x0 |
| 28 | moa-map0 | weight_init | kernel | rng_init | 5.0 | 78.3 | 768x1x1 | 256x1x1 |
| 29 | moa-map0 | weight_init | kernel | elementwise_binary | 2.0 | 44.9 | 1024x1x1 | 128x1x1 |
| 30 | moa-map0 | mir_operator:RMSNormOp:6 | kernel | copy | 4.3 | 8.4 | 1024x1x1 | 128x1x1 |
| 31 | moa-map0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 3.1 | 6.3 | 1024x1x1 | 128x1x1 |
| 32 | moa-map0 | mir_operator:RMSNormOp:6 | kernel | reduce | 3.5 | 6.8 | 64x1x1 | 32x16x1 |
| 33 | moa-map0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.1 | 6.1 | 1x1x1 | 128x1x1 |
| 34 | moa-map0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.1 | 5.8 | 1x1x1 | 128x1x1 |
| 35 | moa-map0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 3.9 | 6.0 | 4096x1x1 | 128x1x1 |
| 36 | moa-map0 | mir_operator:RMSNormOp:6 | kernel | copy | 2.3 | 6.3 | 1024x1x1 | 128x1x1 |
| 37 | moa-map0 | mir_operator:AddOp:7 | kernel | elementwise_binary | 2.0 | 8.5 | 1024x1x1 | 128x1x1 |
| 38 | moa-map0 | mir_operator:RMSNormOp:8 | kernel | copy | 4.5 | 8.6 | 1024x1x1 | 128x1x1 |
| 39 | moa-map0 | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 3.1 | 6.1 | 1024x1x1 | 128x1x1 |
| 40 | moa-map0 | mir_operator:RMSNormOp:8 | kernel | reduce | 3.2 | 6.0 | 64x1x1 | 32x16x1 |
| 41 | moa-map0 | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 1.0 | 6.0 | 1x1x1 | 128x1x1 |
| 42 | moa-map0 | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 1.1 | 5.9 | 1x1x1 | 128x1x1 |
| 43 | moa-map0 | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 3.9 | 6.2 | 4096x1x1 | 128x1x1 |
| 44 | moa-map0 | mir_operator:RMSNormOp:8 | kernel | copy | 2.3 | 6.3 | 1024x1x1 | 128x1x1 |
| 45 | moa-map0 | mir_operator:LinearOp:10 | kernel | gemm | 20.2 | 9.3 | 8x16x1 | 128x1x1 |
| 46 | moa-map0 | mir_operator:LinearOp:11 | kernel | gemm | 20.2 | 8.5 | 8x16x1 | 128x1x1 |
| 47 | moa-map0 | mir_operator:LinearOp:12 | kernel | gemm | 20.2 | 8.7 | 8x16x1 | 128x1x1 |
| 48 | moa-map0 | mir_operator:TransposeOp:14 | kernel | copy | 12.3 | 9.9 | 2048x1x1 | 128x1x1 |
| 49 | moa-map0 | d2h_stage | memcpy | memcpy | 90.4 | 10.2 | 0x0x0 | 0x0x0 |
| 50 | moa-map1 | h2d_stage | memcpy | memcpy | 85.9 | 11.1 | 0x0x0 | 0x0x0 |
| 51 | moa-map1 | weight_init | kernel | rng_init | 5.1 | 78.2 | 768x1x1 | 256x1x1 |
| 52 | moa-map1 | weight_init | kernel | elementwise_binary | 2.0 | 44.5 | 1024x1x1 | 128x1x1 |
| 53 | moa-map1 | mir_operator:RMSNormOp:6 | kernel | copy | 4.4 | 8.5 | 1024x1x1 | 128x1x1 |
| 54 | moa-map1 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 3.1 | 6.7 | 1024x1x1 | 128x1x1 |
| 55 | moa-map1 | mir_operator:RMSNormOp:6 | kernel | reduce | 3.6 | 6.8 | 64x1x1 | 32x16x1 |
| 56 | moa-map1 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.1 | 6.3 | 1x1x1 | 128x1x1 |
| 57 | moa-map1 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.1 | 6.1 | 1x1x1 | 128x1x1 |
| 58 | moa-map1 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 4.0 | 6.2 | 4096x1x1 | 128x1x1 |
| 59 | moa-map1 | mir_operator:RMSNormOp:6 | kernel | copy | 2.3 | 6.3 | 1024x1x1 | 128x1x1 |
| 60 | moa-map1 | mir_operator:AddOp:7 | kernel | elementwise_binary | 2.1 | 8.7 | 1024x1x1 | 128x1x1 |
| … | | 173 more rows in kernel_launch_order_representative_iteration.csv | | | | | | |

## Per call/process summary (medians over measured iterations)

| call | process | op | host median (us) | host min/max (us) | GPU median (us) | top CUDA API | kernels |
|---|---|---:|---:|---:|---:|---|---:|
| react-plan | adapter_dispatch |  | 1,098.7 | 1,081.1/1,264.9 | 0.0 |  | 0 |
| react-plan | token_preprocess_cpu |  | 305.6 | 271.3/389.3 | 0.0 |  | 0 |
| react-plan | host_input_generate |  | 8,064.4 | 5,040.5/8,513.2 | 0.0 | cudaEventQuery | 0 |
| react-plan | h2d_stage |  | 126.4 | 121.1/201.8 | 53.0 | cudaEventSynchronize | 0 |
| react-plan | weight_init |  | 124.4 | 116.5/197.2 | 5.0 | cudaLaunchKernel | 2 |
| react-plan | mir_operator:RMSNormOp | 6 | 244.4 | 227.2/297.7 | 15.9 | cudaLaunchKernel | 7 |
| react-plan | inter_operator_dispatch |  | 8.1 | 5.7/22.0 | 0.0 |  | 0 |
| react-plan | mir_operator:AddOp | 7 | 97.1 | 94.2/126.9 | 1.4 | cudaLaunchKernel | 1 |
| react-plan | mir_operator:RMSNormOp | 8 | 221.8 | 205.8/256.4 | 15.3 | cudaLaunchKernel | 7 |
| react-plan | mir_operator:LinearOp | 10 | 164.3 | 149.4/223.6 | 12.9 | cudaMemsetAsync | 1 |
| react-plan | mir_operator:LinearOp | 11 | 117.3 | 109.7/152.8 | 12.7 | cuLaunchKernel | 1 |
| react-plan | mir_operator:LinearOp | 12 | 108.4 | 103.2/122.6 | 12.7 | cuLaunchKernel | 1 |
| react-plan | mir_operator:ViewOp | 13 | 68.4 | 64.9/75.6 | 0.0 | cudaEventRecord | 0 |
| react-plan | mir_operator:TransposeOp | 14 | 118.7 | 108.9/145.7 | 9.4 | cudaLaunchKernel | 1 |
| react-plan | pre_d2h_alloc |  | 11.0 | 9.1/23.5 | 0.0 |  | 0 |
| react-plan | d2h_stage |  | 104.2 | 94.7/148.8 | 52.9 | cudaEventSynchronize | 0 |
| react-plan | checksum_complete |  | 60.1 | 55.1/79.2 | 0.0 | cudaEventDestroy | 0 |
| moa-map0 | adapter_dispatch |  | 1,122.2 | 1,082.2/2,009.5 | 0.0 |  | 0 |
| moa-map0 | token_preprocess_cpu |  | 295.1 | 196.3/356.6 | 0.0 |  | 0 |
| moa-map0 | host_input_generate |  | 11,899.7 | 8,915.1/11,981.2 | 0.0 | cudaEventQuery | 0 |
| moa-map0 | h2d_stage |  | 195.6 | 160.3/573.0 | 93.5 | cudaEventSynchronize | 0 |
| moa-map0 | weight_init |  | 130.5 | 121.1/306.5 | 7.0 | cudaLaunchKernel | 2 |
| moa-map0 | mir_operator:RMSNormOp | 6 | 255.8 | 231.0/402.3 | 19.4 | cudaLaunchKernel | 7 |
| moa-map0 | inter_operator_dispatch |  | 7.4 | 5.4/23.2 | 0.0 |  | 0 |
| moa-map0 | mir_operator:AddOp | 7 | 101.0 | 94.1/134.9 | 2.1 | cudaLaunchKernel | 1 |
| moa-map0 | mir_operator:RMSNormOp | 8 | 219.9 | 204.3/279.4 | 19.1 | cudaLaunchKernel | 7 |
| moa-map0 | mir_operator:LinearOp | 10 | 114.8 | 108.7/198.4 | 20.1 | cudaLaunchKernel | 1 |
| moa-map0 | mir_operator:LinearOp | 11 | 97.0 | 92.6/125.0 | 20.1 | cudaLaunchKernel | 1 |
| moa-map0 | mir_operator:LinearOp | 12 | 95.1 | 90.3/106.8 | 20.1 | cudaLaunchKernel | 1 |
| moa-map0 | mir_operator:ViewOp | 13 | 68.0 | 65.3/83.8 | 0.0 | cudaEventRecord | 0 |
| moa-map0 | mir_operator:TransposeOp | 14 | 114.8 | 107.4/155.4 | 12.4 | cudaLaunchKernel | 1 |
| moa-map0 | pre_d2h_alloc |  | 11.6 | 9.2/30.7 | 0.0 |  | 0 |
| moa-map0 | d2h_stage |  | 138.9 | 134.0/240.1 | 91.2 | cudaEventSynchronize | 0 |
| moa-map0 | checksum_complete |  | 59.2 | 54.9/113.9 | 0.0 | cudaEventDestroy | 0 |
| moa-map1 | adapter_dispatch |  | 1,130.1 | 1,080.6/1,286.9 | 0.0 |  | 0 |
| moa-map1 | token_preprocess_cpu |  | 317.5 | 285.2/400.3 | 0.0 |  | 0 |
| moa-map1 | host_input_generate |  | 11,894.7 | 8,912.3/12,097.0 | 0.0 | cudaEventQuery | 0 |
| moa-map1 | h2d_stage |  | 176.1 | 158.6/341.8 | 93.5 | cudaEventSynchronize | 0 |
| moa-map1 | weight_init |  | 134.0 | 120.4/248.8 | 7.1 | cudaLaunchKernel | 2 |
| moa-map1 | mir_operator:RMSNormOp | 6 | 243.4 | 226.9/394.6 | 19.4 | cudaLaunchKernel | 7 |
| moa-map1 | inter_operator_dispatch |  | 7.2 | 5.5/23.8 | 0.0 |  | 0 |
| moa-map1 | mir_operator:AddOp | 7 | 100.2 | 93.7/118.5 | 2.1 | cudaLaunchKernel | 1 |
| moa-map1 | mir_operator:RMSNormOp | 8 | 219.1 | 206.0/312.7 | 19.1 | cudaLaunchKernel | 7 |
| moa-map1 | mir_operator:LinearOp | 10 | 117.5 | 108.9/198.4 | 20.2 | cudaLaunchKernel | 1 |
| moa-map1 | mir_operator:LinearOp | 11 | 95.3 | 93.1/106.3 | 20.1 | cudaLaunchKernel | 1 |
| moa-map1 | mir_operator:LinearOp | 12 | 94.0 | 90.3/201.1 | 20.1 | cudaLaunchKernel | 1 |
| moa-map1 | mir_operator:ViewOp | 13 | 70.2 | 65.9/131.9 | 0.0 | cudaEventRecord | 0 |
| moa-map1 | mir_operator:TransposeOp | 14 | 112.7 | 107.8/156.3 | 12.3 | cudaLaunchKernel | 1 |
| moa-map1 | pre_d2h_alloc |  | 10.5 | 9.0/20.3 | 0.0 |  | 0 |
| moa-map1 | d2h_stage |  | 144.7 | 135.2/223.6 | 90.7 | cudaEventSynchronize | 0 |
| moa-map1 | checksum_complete |  | 63.2 | 55.3/94.2 | 0.0 | cudaEventDestroy | 0 |
| moa-map2 | adapter_dispatch |  | 1,108.3 | 1,077.3/1,239.3 | 0.0 |  | 0 |
| moa-map2 | token_preprocess_cpu |  | 308.9 | 258.7/372.8 | 0.0 |  | 0 |
| moa-map2 | host_input_generate |  | 11,893.1 | 8,884.9/13,125.4 | 0.0 | cudaEventQuery | 0 |
| moa-map2 | h2d_stage |  | 168.0 | 158.5/331.4 | 93.3 | cudaEventSynchronize | 0 |
| moa-map2 | weight_init |  | 130.4 | 118.8/249.7 | 7.0 | cudaLaunchKernel | 2 |
| moa-map2 | mir_operator:RMSNormOp | 6 | 245.4 | 227.1/383.5 | 19.3 | cudaLaunchKernel | 7 |
| moa-map2 | inter_operator_dispatch |  | 7.3 | 5.2/22.5 | 0.0 |  | 0 |
| moa-map2 | mir_operator:AddOp | 7 | 99.2 | 93.6/112.1 | 2.1 | cudaLaunchKernel | 1 |
| moa-map2 | mir_operator:RMSNormOp | 8 | 216.4 | 204.5/252.3 | 19.1 | cudaLaunchKernel | 7 |
| moa-map2 | mir_operator:LinearOp | 10 | 120.3 | 109.7/189.7 | 20.1 | cudaLaunchKernel | 1 |
| moa-map2 | mir_operator:LinearOp | 11 | 97.6 | 93.0/124.1 | 20.1 | cudaLaunchKernel | 1 |
| moa-map2 | mir_operator:LinearOp | 12 | 93.9 | 90.2/115.7 | 20.0 | cudaLaunchKernel | 1 |
| moa-map2 | mir_operator:ViewOp | 13 | 68.4 | 64.7/80.1 | 0.0 | cudaEventRecord | 0 |
| moa-map2 | mir_operator:TransposeOp | 14 | 115.2 | 107.1/146.1 | 12.4 | cudaLaunchKernel | 1 |
| moa-map2 | pre_d2h_alloc |  | 10.8 | 8.7/20.6 | 0.0 |  | 0 |
| moa-map2 | d2h_stage |  | 141.7 | 124.5/345.1 | 90.5 | cudaEventSynchronize | 0 |
| moa-map2 | checksum_complete |  | 66.1 | 55.2/94.7 | 0.0 | cudaEventDestroy | 0 |
| mcts-root | adapter_dispatch |  | 1,105.9 | 1,082.8/1,260.3 | 0.0 |  | 0 |
| mcts-root | token_preprocess_cpu |  | 311.6 | 248.6/410.9 | 0.0 |  | 0 |
| mcts-root | host_input_generate |  | 11,899.4 | 8,913.2/11,998.5 | 0.0 | cudaEventQuery | 0 |
| mcts-root | h2d_stage |  | 170.6 | 160.4/320.6 | 93.6 | cudaEventSynchronize | 0 |
| mcts-root | weight_init |  | 129.4 | 117.7/249.4 | 7.0 | cudaLaunchKernel | 2 |
| mcts-root | mir_operator:RMSNormOp | 6 | 253.6 | 226.5/365.2 | 19.4 | cudaLaunchKernel | 7 |
| mcts-root | inter_operator_dispatch |  | 7.3 | 5.5/20.3 | 0.0 |  | 0 |
| mcts-root | mir_operator:AddOp | 7 | 101.5 | 94.0/118.1 | 2.1 | cudaLaunchKernel | 1 |
| mcts-root | mir_operator:RMSNormOp | 8 | 216.0 | 207.0/246.1 | 19.1 | cudaLaunchKernel | 7 |
| mcts-root | mir_operator:LinearOp | 10 | 118.2 | 107.7/179.6 | 20.1 | cudaLaunchKernel | 1 |
| mcts-root | mir_operator:LinearOp | 11 | 95.7 | 93.6/122.5 | 20.2 | cudaLaunchKernel | 1 |
| mcts-root | mir_operator:LinearOp | 12 | 93.6 | 90.0/145.5 | 20.1 | cudaLaunchKernel | 1 |
| mcts-root | mir_operator:ViewOp | 13 | 66.5 | 64.6/84.2 | 0.0 | cudaEventRecord | 0 |
| mcts-root | mir_operator:TransposeOp | 14 | 113.6 | 107.5/146.3 | 12.3 | cudaLaunchKernel | 1 |
| mcts-root | pre_d2h_alloc |  | 10.5 | 8.9/19.7 | 0.0 |  | 0 |
| mcts-root | d2h_stage |  | 142.6 | 134.8/244.6 | 91.1 | cudaEventSynchronize | 0 |
| mcts-root | checksum_complete |  | 61.2 | 54.2/87.7 | 0.0 | cudaEventDestroy | 0 |
| react-tool | agent_tool_execute_cpu |  | 314.5 | 268.6/402.5 | 0.0 |  | 0 |
| mcts-actor0 | adapter_dispatch |  | 1,766.0 | 1,245.1/1,818.1 | 0.0 |  | 0 |
| mcts-actor0 | token_preprocess_cpu |  | 146.4 | 98.2/184.8 | 0.0 |  | 0 |
| mcts-actor0 | host_input_generate |  | 11,898.5 | 8,867.9/13,086.9 | 0.0 | cudaEventQuery | 0 |
| mcts-actor0 | h2d_stage |  | 178.4 | 160.7/286.8 | 93.8 | cudaEventSynchronize | 0 |
| mcts-actor0 | weight_init |  | 133.6 | 116.6/207.7 | 7.1 | cudaLaunchKernel | 2 |
| mcts-actor0 | mir_operator:RMSNormOp | 6 | 248.4 | 227.7/443.8 | 19.4 | cudaLaunchKernel | 7 |
| mcts-actor0 | inter_operator_dispatch |  | 7.4 | 5.4/22.2 | 0.0 |  | 0 |
| mcts-actor0 | mir_operator:AddOp | 7 | 102.5 | 93.3/136.0 | 2.1 | cudaLaunchKernel | 1 |
| mcts-actor0 | mir_operator:RMSNormOp | 8 | 224.3 | 206.3/348.7 | 19.1 | cudaEventRecord | 7 |
| mcts-actor0 | mir_operator:LinearOp | 10 | 118.5 | 108.8/322.4 | 20.1 | cudaLaunchKernel | 1 |
| mcts-actor0 | mir_operator:LinearOp | 11 | 101.1 | 92.8/206.5 | 20.1 | cudaLaunchKernel | 1 |
| mcts-actor0 | mir_operator:LinearOp | 12 | 93.5 | 89.8/149.2 | 20.0 | cudaLaunchKernel | 1 |
| mcts-actor0 | mir_operator:ViewOp | 13 | 70.0 | 64.6/77.5 | 0.0 | cudaEventRecord | 0 |
| mcts-actor0 | mir_operator:TransposeOp | 14 | 121.6 | 107.3/131.8 | 12.4 | cudaEventSynchronize | 1 |
| mcts-actor0 | pre_d2h_alloc |  | 11.4 | 9.2/17.2 | 0.0 |  | 0 |
| mcts-actor0 | d2h_stage |  | 138.8 | 134.5/219.0 | 90.4 | cudaEventSynchronize | 0 |
| mcts-actor0 | checksum_complete |  | 66.5 | 54.7/87.1 | 0.0 | cudaEventDestroy | 0 |
| mcts-actor1 | adapter_dispatch |  | 1,090.9 | 871.2/1,223.9 | 0.0 |  | 0 |
| mcts-actor1 | token_preprocess_cpu |  | 300.9 | 266.5/361.6 | 0.0 |  | 0 |
| mcts-actor1 | host_input_generate |  | 11,901.9 | 8,897.0/12,510.5 | 0.0 | cudaEventQuery | 0 |
| mcts-actor1 | h2d_stage |  | 172.6 | 158.0/310.5 | 93.6 | cudaEventSynchronize | 0 |
| mcts-actor1 | weight_init |  | 130.4 | 117.6/170.2 | 7.1 | cudaLaunchKernel | 2 |
| mcts-actor1 | mir_operator:RMSNormOp | 6 | 243.8 | 225.2/402.4 | 19.3 | cudaLaunchKernel | 7 |
| mcts-actor1 | inter_operator_dispatch |  | 7.3 | 5.5/15.4 | 0.0 |  | 0 |
| mcts-actor1 | mir_operator:AddOp | 7 | 97.2 | 92.6/216.9 | 2.0 | cudaLaunchKernel | 1 |
| mcts-actor1 | mir_operator:RMSNormOp | 8 | 225.6 | 203.7/259.7 | 19.1 | cudaLaunchKernel | 7 |
| mcts-actor1 | mir_operator:LinearOp | 10 | 125.3 | 108.6/241.6 | 20.2 | cudaLaunchKernel | 1 |
| mcts-actor1 | mir_operator:LinearOp | 11 | 98.9 | 93.5/121.4 | 20.2 | cudaLaunchKernel | 1 |
| mcts-actor1 | mir_operator:LinearOp | 12 | 94.5 | 89.9/113.1 | 20.1 | cudaLaunchKernel | 1 |
| mcts-actor1 | mir_operator:ViewOp | 13 | 71.0 | 65.3/93.8 | 0.0 | cudaEventRecord | 0 |
| mcts-actor1 | mir_operator:TransposeOp | 14 | 124.1 | 108.9/196.5 | 12.5 | cudaLaunchKernel | 1 |
| mcts-actor1 | pre_d2h_alloc |  | 10.4 | 8.9/28.8 | 0.0 |  | 0 |
| mcts-actor1 | d2h_stage |  | 178.1 | 134.9/267.0 | 91.9 | cudaEventSynchronize | 0 |
| mcts-actor1 | checksum_complete |  | 57.3 | 54.4/82.1 | 0.0 | cudaEventDestroy | 0 |
| moa-reduce | adapter_dispatch |  | 1,100.9 | 1,080.7/1,326.1 | 0.0 |  | 0 |
| moa-reduce | token_preprocess_cpu |  | 318.6 | 220.9/391.9 | 0.0 |  | 0 |
| moa-reduce | host_input_generate |  | 11,910.8 | 8,913.4/12,997.9 | 0.0 | cudaEventQuery | 0 |
| moa-reduce | h2d_stage |  | 168.6 | 158.7/260.1 | 91.8 | cudaEventSynchronize | 0 |
| moa-reduce | weight_init |  | 128.6 | 116.3/162.1 | 7.1 | cudaLaunchKernel | 2 |
| moa-reduce | mir_operator:RMSNormOp | 6 | 245.1 | 228.1/309.4 | 19.3 | cudaLaunchKernel | 7 |
| moa-reduce | inter_operator_dispatch |  | 7.2 | 5.3/21.0 | 0.0 |  | 0 |
| moa-reduce | mir_operator:AddOp | 7 | 97.8 | 93.8/143.1 | 2.1 | cudaLaunchKernel | 1 |
| moa-reduce | mir_operator:RMSNormOp | 8 | 220.9 | 203.6/250.2 | 19.1 | cudaLaunchKernel | 7 |
| moa-reduce | mir_operator:LinearOp | 10 | 121.4 | 106.8/262.6 | 20.1 | cudaLaunchKernel | 1 |
| moa-reduce | mir_operator:LinearOp | 11 | 100.1 | 93.4/118.3 | 20.1 | cudaLaunchKernel | 1 |
| moa-reduce | mir_operator:LinearOp | 12 | 94.2 | 90.6/170.1 | 20.0 | cudaLaunchKernel | 1 |
| moa-reduce | mir_operator:ViewOp | 13 | 69.8 | 65.4/305.6 | 0.0 | cudaEventDestroy | 0 |
| moa-reduce | mir_operator:TransposeOp | 14 | 117.4 | 107.5/138.1 | 12.4 | cudaLaunchKernel | 1 |
| moa-reduce | pre_d2h_alloc |  | 11.2 | 9.2/17.7 | 0.0 |  | 0 |
| moa-reduce | d2h_stage |  | 139.0 | 135.2/241.1 | 91.2 | cudaEventSynchronize | 0 |
| moa-reduce | checksum_complete |  | 60.8 | 53.9/75.5 | 0.0 | cudaEventDestroy | 0 |
| react-answer | adapter_dispatch |  | 1,114.0 | 1,081.7/1,298.9 | 0.0 |  | 0 |
| react-answer | token_preprocess_cpu |  | 311.9 | 266.5/357.4 | 0.0 |  | 0 |
| react-answer | host_input_generate |  | 9,054.6 | 6,820.4/10,354.2 | 0.0 | cudaEventQuery | 0 |
| react-answer | h2d_stage |  | 149.7 | 139.7/242.3 | 71.0 | cudaEventSynchronize | 0 |
| react-answer | weight_init |  | 123.6 | 117.4/178.2 | 6.7 | cudaLaunchKernel | 2 |
| react-answer | mir_operator:RMSNormOp | 6 | 244.6 | 225.6/308.2 | 17.9 | cudaLaunchKernel | 7 |
| react-answer | inter_operator_dispatch |  | 7.5 | 5.6/18.5 | 0.0 |  | 0 |
| react-answer | mir_operator:AddOp | 7 | 97.8 | 93.1/105.2 | 1.7 | cudaLaunchKernel | 1 |
| react-answer | mir_operator:RMSNormOp | 8 | 218.3 | 202.7/297.6 | 17.3 | cudaLaunchKernel | 7 |
| react-answer | mir_operator:LinearOp | 10 | 121.0 | 112.9/200.1 | 14.6 | cudaLaunchKernel | 1 |
| react-answer | mir_operator:LinearOp | 11 | 99.7 | 93.2/169.5 | 14.6 | cudaLaunchKernel | 1 |
| react-answer | mir_operator:LinearOp | 12 | 94.2 | 89.4/112.0 | 14.5 | cudaLaunchKernel | 1 |
| react-answer | mir_operator:ViewOp | 13 | 68.9 | 65.4/80.1 | 0.0 | cudaEventRecord | 0 |
| react-answer | mir_operator:TransposeOp | 14 | 111.1 | 106.6/187.8 | 12.1 | cudaLaunchKernel | 1 |
| react-answer | pre_d2h_alloc |  | 10.5 | 8.9/22.8 | 0.0 |  | 0 |
| react-answer | d2h_stage |  | 120.9 | 111.9/196.1 | 69.0 | cudaEventSynchronize | 0 |
| react-answer | checksum_complete |  | 66.8 | 54.2/103.8 | 0.0 | cudaEventDestroy | 0 |
| mcts-critic | adapter_dispatch |  | 1,106.6 | 1,085.2/1,635.9 | 0.0 |  | 0 |
| mcts-critic | token_preprocess_cpu |  | 293.0 | 238.5/365.2 | 0.0 |  | 0 |
| mcts-critic | host_input_generate |  | 11,316.8 | 8,896.2/12,058.6 | 0.0 | cudaEventQuery | 0 |
| mcts-critic | h2d_stage |  | 168.6 | 158.1/296.9 | 92.6 | cudaEventSynchronize | 0 |
| mcts-critic | weight_init |  | 126.2 | 117.4/204.9 | 7.0 | cudaLaunchKernel | 2 |
| mcts-critic | mir_operator:RMSNormOp | 6 | 243.6 | 226.9/391.1 | 19.4 | cudaLaunchKernel | 7 |
| mcts-critic | inter_operator_dispatch |  | 7.3 | 5.3/24.3 | 0.0 |  | 0 |
| mcts-critic | mir_operator:AddOp | 7 | 102.4 | 93.7/176.0 | 2.1 | cudaLaunchKernel | 1 |
| mcts-critic | mir_operator:RMSNormOp | 8 | 220.4 | 204.4/258.3 | 19.1 | cudaLaunchKernel | 7 |
| mcts-critic | mir_operator:LinearOp | 10 | 114.6 | 109.1/175.2 | 20.1 | cudaLaunchKernel | 1 |
| mcts-critic | mir_operator:LinearOp | 11 | 100.6 | 93.1/131.0 | 20.1 | cudaLaunchKernel | 1 |
| mcts-critic | mir_operator:LinearOp | 12 | 95.6 | 90.1/147.4 | 20.1 | cudaLaunchKernel | 1 |
| mcts-critic | mir_operator:ViewOp | 13 | 69.2 | 65.4/80.7 | 0.0 | cudaEventRecord | 0 |
| mcts-critic | mir_operator:TransposeOp | 14 | 112.8 | 107.4/154.1 | 12.4 | cudaLaunchKernel | 1 |
| mcts-critic | pre_d2h_alloc |  | 10.5 | 9.0/19.7 | 0.0 |  | 0 |
| mcts-critic | d2h_stage |  | 141.2 | 134.5/235.1 | 93.4 | cudaEventSynchronize | 0 |
| mcts-critic | checksum_complete |  | 63.5 | 54.5/87.5 | 0.0 | cudaEventDestroy | 0 |
| <dag> | dag_schedule_gap |  | 30.8 | 8.7/1,396.9 | 0.0 |  | 0 |
| <dag> | iteration_tail_sync |  | 60.2 | 52.7/76.3 | 0.0 | cudaDeviceSynchronize | 0 |

## Process inventory (handoff contract)

| process | owner | evidence | what it contains |
|---|---|---|---|
| dag_schedule_gap | dag | gap host | scheduler between calls / before first call |
| adapter_dispatch | llm call | gap host | adapter_start -> token preprocess |
| token_preprocess_cpu | llm call | host event | seeded 256x256 fp32 CPU matmul |
| host_input_generate | llm call | gap host | pinned fp16 tensor alloc + CPU-generator uniform_ |
| h2d_stage | llm call | host event + memcpy | pinned -> device copy, cudaEvent bracket |
| weight_init | llm call | gap host + kernels | torch.cuda.manual_seed + randn weight on device |
| mir_operator:<type> | llm call | NVTX range + kernels | one MIR operator incl. cudaEventSynchronize |
| inter_operator_dispatch | llm call | gap host | Python between operator ranges |
| pre_d2h_alloc | llm call | gap host | pinned output alloc |
| d2h_stage | llm call | host event + memcpy | device -> pinned copy |
| checksum_complete | llm call | gap host | host checksum, adapter_complete |
| agent_tool_execute_cpu | tool call | host event | seeded 256x256 fp32 CPU matmul |
| iteration_tail_sync | dag | gap host | torch.cuda.synchronize + range pop |

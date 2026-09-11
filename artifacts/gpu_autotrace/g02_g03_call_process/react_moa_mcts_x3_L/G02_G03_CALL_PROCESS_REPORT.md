# G02/G03 call-wise process attribution: `react_moa_mcts_x3_L`

Lineage `h22-gpu-autotrace`, workflow w02. Consumes the w01 trace only; no re-timing.
Host events aligned to the nsys clock by a constant offset fitted on 1920 operator pairs (spread 34.2 us).

## Conservation

| Quantity | Value |
|---|---:|
| Measured iterations | 8 |
| Sum of process segments minus iteration wall (max abs) | 0 ns |
| GPU work attributed here minus w01 attributed GPU | 0 ns |
| Unnamed gap time | 0.0 us |
| Pass | True |

## Process-type breakdown (share of measured wall)

| process | instances | host total (us) | host share | per instance (us) | GPU total (us) | GPU share | CUDA API share of host | GPU/host |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| host_input_generate | 240 | 25,652,331.9 | 48.37 % | 106,884.7 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:LinearOp | 720 | 17,490,508.4 | 32.98 % | 24,292.4 | 17,375,384.6 | 65.35 % | 97.4 % | 99.3 % |
| mir_operator:RMSNormOp | 480 | 6,903,717.0 | 13.02 % | 14,382.7 | 6,786,648.1 | 25.53 % | 85.8 % | 98.3 % |
| mir_operator:TransposeOp | 240 | 1,665,680.3 | 3.14 % | 6,940.3 | 1,634,155.3 | 6.15 % | 91.4 % | 98.1 % |
| h2d_stage | 240 | 352,661.3 | 0.67 % | 1,469.4 | 316,400.2 | 1.19 % | 92.7 % | 89.7 % |
| d2h_stage | 240 | 341,434.0 | 0.64 % | 1,422.6 | 327,187.6 | 1.23 % | 96.7 % | 95.8 % |
| adapter_dispatch | 240 | 207,585.7 | 0.39 % | 864.9 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:AddOp | 240 | 164,547.6 | 0.31 % | 685.6 | 135,464.4 | 0.51 % | 42.4 % | 82.3 % |
| token_preprocess_cpu | 240 | 78,080.5 | 0.15 % | 325.3 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| weight_init | 240 | 45,079.9 | 0.09 % | 187.8 | 11,830.6 | 0.04 % | 24.4 % | 26.2 % |
| mir_operator:ViewOp | 240 | 37,665.3 | 0.07 % | 156.9 | 0.0 | 0.0 % | 10.0 % | 0.0 % |
| dag_schedule_gap | 264 | 34,610.7 | 0.07 % | 131.1 | 0.0 | 0.0 % | 2.7 % | 0.0 % |
| inter_operator_dispatch | 1680 | 21,733.1 | 0.04 % | 12.9 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| checksum_complete | 240 | 19,829.5 | 0.04 % | 82.6 | 0.0 | 0.0 % | 2.3 % | 0.0 % |
| agent_tool_execute_cpu | 24 | 7,385.9 | 0.01 % | 307.7 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| pre_d2h_alloc | 240 | 5,035.1 | 0.01 % | 21.0 | 0.0 | 0.0 % | 0.3 % | 0.0 % |
| iteration_tail_sync | 8 | 609.2 | 0.0 % | 76.1 | 0.0 | 0.0 % | 17.5 % | 0.0 % |

## Call breakdown (agent nodes)

| call | kind | wave | matrix | host per iter (us) | host share | GPU per iter (us) | GPU share | GPU/host |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| react-plan#r0 | llm | 0 | 3072 | 115,598.8 | 1.74 % | 48,296.6 | 1.45 % | 41.78 % |
| moa-map0#r0 | llm | 0 | 4096 | 235,950.8 | 3.56 % | 121,903.8 | 3.67 % | 51.66 % |
| moa-map1#r0 | llm | 0 | 4096 | 237,013.7 | 3.58 % | 121,452.8 | 3.65 % | 51.24 % |
| moa-map2#r0 | llm | 0 | 4096 | 237,399.3 | 3.58 % | 121,802.6 | 3.67 % | 51.31 % |
| mcts-root#r0 | llm | 0 | 4096 | 239,845.8 | 3.62 % | 121,467.7 | 3.65 % | 50.64 % |
| react-tool#r0 | tool | 1 | 256 | 307.9 | 0.0 % | 0.0 | 0.0 % | 0.0 % |
| mcts-actor0#r0 | llm | 1 | 4096 | 239,704.6 | 3.62 % | 121,497.7 | 3.66 % | 50.69 % |
| mcts-actor1#r0 | llm | 1 | 4096 | 238,690.7 | 3.6 % | 121,628.4 | 3.66 % | 50.96 % |
| moa-reduce#r0 | llm | 1 | 4096 | 242,396.5 | 3.66 % | 121,666.4 | 3.66 % | 50.19 % |
| react-answer#r0 | llm | 2 | 3584 | 176,754.7 | 2.67 % | 86,354.3 | 2.6 % | 48.86 % |
| mcts-critic#r0 | llm | 2 | 4096 | 237,431.1 | 3.58 % | 121,708.8 | 3.66 % | 51.26 % |
| react-plan#r1 | llm | 3 | 3072 | 118,406.8 | 1.79 % | 48,148.3 | 1.45 % | 40.66 % |
| moa-map0#r1 | llm | 3 | 4096 | 242,478.3 | 3.66 % | 121,688.5 | 3.66 % | 50.19 % |
| moa-map1#r1 | llm | 3 | 4096 | 241,722.5 | 3.65 % | 122,138.8 | 3.68 % | 50.53 % |
| moa-map2#r1 | llm | 3 | 4096 | 239,562.5 | 3.61 % | 121,647.9 | 3.66 % | 50.78 % |
| mcts-root#r1 | llm | 3 | 4096 | 240,810.7 | 3.63 % | 121,792.3 | 3.66 % | 50.58 % |
| react-tool#r1 | tool | 4 | 256 | 289.2 | 0.0 % | 0.0 | 0.0 % | 0.0 % |
| mcts-actor0#r1 | llm | 4 | 4096 | 239,994.5 | 3.62 % | 121,526.8 | 3.66 % | 50.64 % |
| mcts-actor1#r1 | llm | 4 | 4096 | 238,076.3 | 3.59 % | 121,611.6 | 3.66 % | 51.08 % |
| moa-reduce#r1 | llm | 4 | 4096 | 237,364.1 | 3.58 % | 121,801.4 | 3.66 % | 51.31 % |
| react-answer#r1 | llm | 5 | 3584 | 176,080.8 | 2.66 % | 86,721.0 | 2.61 % | 49.25 % |
| mcts-critic#r1 | llm | 5 | 4096 | 239,695.9 | 3.62 % | 121,660.9 | 3.66 % | 50.76 % |
| react-plan#r2 | llm | 6 | 3072 | 116,322.0 | 1.75 % | 48,161.6 | 1.45 % | 41.4 % |
| moa-map0#r2 | llm | 6 | 4096 | 236,628.4 | 3.57 % | 121,175.5 | 3.65 % | 51.21 % |
| moa-map1#r2 | llm | 6 | 4096 | 242,056.4 | 3.65 % | 121,195.7 | 3.65 % | 50.07 % |
| moa-map2#r2 | llm | 6 | 4096 | 241,605.1 | 3.64 % | 121,474.3 | 3.66 % | 50.28 % |
| mcts-root#r2 | llm | 6 | 4096 | 241,697.5 | 3.65 % | 121,610.0 | 3.66 % | 50.31 % |
| react-tool#r2 | tool | 7 | 256 | 326.1 | 0.0 % | 0.0 | 0.0 % | 0.0 % |
| mcts-actor0#r2 | llm | 7 | 4096 | 243,509.1 | 3.67 % | 121,871.3 | 3.67 % | 50.05 % |
| mcts-actor1#r2 | llm | 7 | 4096 | 237,630.6 | 3.58 % | 121,622.7 | 3.66 % | 51.18 % |
| moa-reduce#r2 | llm | 7 | 4096 | 236,441.5 | 3.57 % | 121,741.2 | 3.66 % | 51.49 % |
| react-answer#r2 | llm | 8 | 3584 | 176,565.4 | 2.66 % | 86,651.2 | 2.61 % | 49.08 % |
| mcts-critic#r2 | llm | 8 | 4096 | 235,801.9 | 3.56 % | 121,364.0 | 3.65 % | 51.47 % |
| <dag> | dag |  |  | 4,402.5 | 0.07 % | 0.0 | 0.0 % | 0.0 % |

## CUDA runtime API inside the measured window

| API | calls | total (us) | share of wall |
|---|---:|---:|---:|
| cudaEventSynchronize | 2400 | 24,415,164.4 | 46.04 % |
| cudaLaunchKernel | 144096 | 679,096.6 | 1.28 % |
| cudaMemsetAsync | 18432 | 64,988.6 | 0.12 % |
| cudaEventRecord | 5280 | 24,121.3 | 0.05 % |
| cudaMemcpyAsync | 480 | 11,339.3 | 0.02 % |
| cudaEventCreateWithFlags | 4800 | 11,055.5 | 0.02 % |
| cuLaunchKernel | 2304 | 10,468.5 | 0.02 % |
| cudaEventDestroy | 4800 | 6,228.9 | 0.01 % |
| cudaEventQuery | 480 | 2,266.8 | 0.0 % |
| cuKernelGetFunction | 2304 | 1,067.3 | 0.0 % |
| cudaStreamIsCapturing | 720 | 657.2 | 0.0 % |
| cudaDeviceSynchronize | 8 | 79.0 | 0.0 % |

## Kernel families by process (G03)

| process | family | instances | GPU total (us) | share |
|---|---|---:|---:|---:|
| mir_operator:LinearOp | gemm | 23040 | 17,352,501.3 | 65.27 % |
| mir_operator:RMSNormOp | copy | 30720 | 2,454,078.3 | 9.23 % |
| mir_operator:RMSNormOp | elementwise_unary | 30720 | 2,029,570.9 | 7.63 % |
| mir_operator:RMSNormOp | elementwise_binary | 30720 | 1,793,384.9 | 6.75 % |
| mir_operator:TransposeOp | copy | 7680 | 1,634,155.3 | 6.15 % |
| mir_operator:RMSNormOp | reduce | 15360 | 509,614.0 | 1.92 % |
| d2h_stage | memcpy | 240 | 327,187.6 | 1.23 % |
| h2d_stage | memcpy | 240 | 316,400.2 | 1.19 % |
| mir_operator:AddOp | elementwise_binary | 7680 | 135,464.4 | 0.51 % |
| mir_operator:LinearOp | memset | 18432 | 22,883.3 | 0.09 % |
| weight_init | rng_init | 240 | 7,258.1 | 0.03 % |
| weight_init | elementwise_binary | 240 | 4,572.5 | 0.02 % |

## Kernel launch order, representative iteration 6 (G03)

| # | call | process | kind | family | GPU (us) | launch latency (us) | grid | block |
|---:|---|---|---|---|---:|---:|---|---|
| 1 | react-plan#r0 | h2d_stage | memcpy | memcpy | 776.9 | 25.4 | 0x0x0 | 0x0x0 |
| 2 | react-plan#r0 | weight_init | kernel | rng_init | 18.7 | 90.5 | 768x1x1 | 256x1x1 |
| 3 | react-plan#r0 | weight_init | kernel | elementwise_binary | 11.2 | 39.2 | 9216x1x1 | 128x1x1 |
| 4 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 60.0 | 9.7 | 9216x1x1 | 128x1x1 |
| 5 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 37.6 | 41.9 | 9216x1x1 | 128x1x1 |
| 6 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | reduce | 11.5 | 47.6 | 192x1x1 | 32x16x1 |
| 7 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.0 | 36.1 | 3x1x1 | 128x1x1 |
| 8 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 18.3 | 3x1x1 | 128x1x1 |
| 9 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 30.6 | 6.4 | 36864x1x1 | 128x1x1 |
| 10 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 12.1 | 15.8 | 9216x1x1 | 128x1x1 |
| 11 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 27.9 | 7.4 | 9216x1x1 | 128x1x1 |
| 12 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 39.5 | 22.2 | 9216x1x1 | 128x1x1 |
| 13 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | reduce | 10.3 | 48.2 | 192x1x1 | 32x16x1 |
| 14 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.0 | 47.4 | 3x1x1 | 128x1x1 |
| 15 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 37.1 | 3x1x1 | 128x1x1 |
| 16 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 31.4 | 26.1 | 36864x1x1 | 128x1x1 |
| 17 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 12.3 | 43.5 | 9216x1x1 | 128x1x1 |
| 18 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 28.8 | 35.9 | 9216x1x1 | 128x1x1 |
| 19 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 40.9 | 52.4 | 9216x1x1 | 128x1x1 |
| 20 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | reduce | 10.1 | 80.2 | 192x1x1 | 32x16x1 |
| 21 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.3 | 77.9 | 3x1x1 | 128x1x1 |
| 22 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 68.1 | 3x1x1 | 128x1x1 |
| 23 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 32.0 | 57.1 | 36864x1x1 | 128x1x1 |
| 24 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 12.3 | 75.2 | 9216x1x1 | 128x1x1 |
| 25 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 29.2 | 68.4 | 9216x1x1 | 128x1x1 |
| 26 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 39.8 | 85.5 | 9216x1x1 | 128x1x1 |
| 27 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | reduce | 10.3 | 112.1 | 192x1x1 | 32x16x1 |
| 28 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.0 | 112.3 | 3x1x1 | 128x1x1 |
| 29 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 102.3 | 3x1x1 | 128x1x1 |
| 30 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 31.4 | 91.5 | 36864x1x1 | 128x1x1 |
| 31 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 12.1 | 109.0 | 9216x1x1 | 128x1x1 |
| 32 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 29.3 | 102.9 | 9216x1x1 | 128x1x1 |
| 33 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 39.6 | 120.1 | 9216x1x1 | 128x1x1 |
| 34 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | reduce | 10.6 | 146.8 | 192x1x1 | 32x16x1 |
| 35 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.0 | 147.0 | 3x1x1 | 128x1x1 |
| 36 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 135.4 | 3x1x1 | 128x1x1 |
| 37 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 32.0 | 124.4 | 36864x1x1 | 128x1x1 |
| 38 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 12.1 | 142.6 | 9216x1x1 | 128x1x1 |
| 39 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 29.2 | 136.5 | 9216x1x1 | 128x1x1 |
| 40 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 40.1 | 153.7 | 9216x1x1 | 128x1x1 |
| 41 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | reduce | 10.3 | 175.4 | 192x1x1 | 32x16x1 |
| 42 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.0 | 175.3 | 3x1x1 | 128x1x1 |
| 43 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 165.6 | 3x1x1 | 128x1x1 |
| 44 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 31.6 | 154.9 | 36864x1x1 | 128x1x1 |
| 45 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 12.2 | 172.5 | 9216x1x1 | 128x1x1 |
| 46 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 28.8 | 166.0 | 9216x1x1 | 128x1x1 |
| 47 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 40.2 | 182.4 | 9216x1x1 | 128x1x1 |
| 48 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | reduce | 10.1 | 209.9 | 192x1x1 | 32x16x1 |
| 49 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.0 | 210.2 | 3x1x1 | 128x1x1 |
| 50 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 200.3 | 3x1x1 | 128x1x1 |
| 51 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 32.0 | 188.0 | 36864x1x1 | 128x1x1 |
| 52 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 12.3 | 206.2 | 9216x1x1 | 128x1x1 |
| 53 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 29.4 | 200.1 | 9216x1x1 | 128x1x1 |
| 54 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 40.0 | 217.3 | 9216x1x1 | 128x1x1 |
| 55 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | reduce | 10.5 | 244.4 | 192x1x1 | 32x16x1 |
| 56 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.0 | 244.6 | 3x1x1 | 128x1x1 |
| 57 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 234.8 | 3x1x1 | 128x1x1 |
| 58 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 31.7 | 224.2 | 36864x1x1 | 128x1x1 |
| 59 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 12.1 | 242.2 | 9216x1x1 | 128x1x1 |
| 60 | react-plan#r0 | mir_operator:RMSNormOp:6 | kernel | copy | 28.6 | 236.3 | 9216x1x1 | 128x1x1 |
| … | | 20604 more rows in kernel_launch_order_representative_iteration.csv | | | | | | |

## Per call/process summary (medians over measured iterations)

| call | process | op | host median (us) | host min/max (us) | GPU median (us) | top CUDA API | kernels |
|---|---|---:|---:|---:|---:|---|---:|
| react-plan#r0 | adapter_dispatch |  | 816.0 | 737.6/916.1 | 0.0 |  | 0 |
| react-plan#r0 | token_preprocess_cpu |  | 322.0 | 195.3/393.5 | 0.0 |  | 0 |
| react-plan#r0 | host_input_generate |  | 64,141.7 | 62,664.8/67,537.3 | 0.0 | cudaEventQuery | 0 |
| react-plan#r0 | h2d_stage |  | 913.2 | 868.3/966.6 | 775.2 | cudaEventSynchronize | 0 |
| react-plan#r0 | weight_init |  | 180.3 | 128.5/197.6 | 29.8 | cudaLaunchKernel | 2 |
| react-plan#r0 | mir_operator:RMSNormOp | 6 | 4,311.8 | 4,275.4/4,357.8 | 4,052.1 | cudaEventSynchronize | 224 |
| react-plan#r0 | inter_operator_dispatch |  | 9.7 | 4.9/26.2 | 0.0 |  | 0 |
| react-plan#r0 | mir_operator:AddOp | 7 | 555.7 | 505.1/575.1 | 326.2 | cudaLaunchKernel | 32 |
| react-plan#r0 | mir_operator:RMSNormOp | 8 | 4,250.5 | 4,226.5/4,323.3 | 4,038.8 | cudaEventSynchronize | 224 |
| react-plan#r0 | mir_operator:LinearOp | 10 | 11,628.1 | 11,293.7/11,663.8 | 11,489.6 | cudaEventSynchronize | 32 |
| react-plan#r0 | mir_operator:LinearOp | 11 | 11,436.8 | 11,198.2/11,612.1 | 11,339.5 | cudaEventSynchronize | 32 |
| react-plan#r0 | mir_operator:LinearOp | 12 | 11,320.2 | 11,248.0/11,667.2 | 11,230.8 | cudaEventSynchronize | 32 |
| react-plan#r0 | mir_operator:ViewOp | 13 | 141.2 | 130.0/156.6 | 0.0 | cudaEventRecord | 0 |
| react-plan#r0 | mir_operator:TransposeOp | 14 | 4,326.4 | 4,112.9/4,593.8 | 4,206.5 | cudaEventSynchronize | 32 |
| react-plan#r0 | pre_d2h_alloc |  | 16.5 | 9.2/26.2 | 0.0 |  | 0 |
| react-plan#r0 | d2h_stage |  | 884.6 | 856.8/898.7 | 828.3 | cudaEventSynchronize | 0 |
| react-plan#r0 | checksum_complete |  | 77.2 | 58.3/83.6 | 0.0 | cudaEventDestroy | 0 |
| moa-map0#r0 | adapter_dispatch |  | 796.7 | 721.8/865.1 | 0.0 |  | 0 |
| moa-map0#r0 | token_preprocess_cpu |  | 345.2 | 263.4/362.3 | 0.0 |  | 0 |
| moa-map0#r0 | host_input_generate |  | 110,733.7 | 109,509.4/113,820.3 | 0.0 | cudaEventQuery | 0 |
| moa-map0#r0 | h2d_stage |  | 1,550.1 | 1,523.0/1,643.0 | 1,400.7 | cudaEventSynchronize | 0 |
| moa-map0#r0 | weight_init |  | 187.0 | 140.0/203.7 | 52.0 | cudaLaunchKernel | 2 |
| moa-map0#r0 | mir_operator:RMSNormOp | 6 | 16,422.7 | 16,080.4/16,551.6 | 16,181.0 | cudaEventSynchronize | 224 |
| moa-map0#r0 | inter_operator_dispatch |  | 10.6 | 4.8/36.1 | 0.0 |  | 0 |
| moa-map0#r0 | mir_operator:AddOp | 7 | 696.7 | 689.0/707.7 | 603.6 | cudaLaunchKernel | 32 |
| moa-map0#r0 | mir_operator:RMSNormOp | 8 | 16,015.6 | 15,996.4/16,500.4 | 15,799.7 | cudaEventSynchronize | 224 |
| moa-map0#r0 | mir_operator:LinearOp | 10 | 26,070.8 | 25,692.4/26,369.4 | 25,873.6 | cudaEventSynchronize | 32 |
| moa-map0#r0 | mir_operator:LinearOp | 11 | 26,765.6 | 25,758.4/27,127.5 | 26,612.4 | cudaEventSynchronize | 32 |
| moa-map0#r0 | mir_operator:LinearOp | 12 | 27,209.9 | 26,182.3/27,389.5 | 27,038.2 | cudaEventSynchronize | 32 |
| moa-map0#r0 | mir_operator:ViewOp | 13 | 145.9 | 131.3/171.2 | 0.0 | cudaEventRecord | 0 |
| moa-map0#r0 | mir_operator:TransposeOp | 14 | 7,329.1 | 7,294.0/7,806.6 | 7,201.1 | cudaEventSynchronize | 32 |
| moa-map0#r0 | pre_d2h_alloc |  | 22.9 | 11.7/24.3 | 0.0 |  | 0 |
| moa-map0#r0 | d2h_stage |  | 1,489.1 | 1,470.0/1,698.7 | 1,442.4 | cudaEventSynchronize | 0 |
| moa-map0#r0 | checksum_complete |  | 82.3 | 62.8/94.6 | 0.0 | cudaEventDestroy | 0 |
| moa-map1#r0 | adapter_dispatch |  | 757.2 | 708.2/887.6 | 0.0 |  | 0 |
| moa-map1#r0 | token_preprocess_cpu |  | 349.4 | 284.2/365.4 | 0.0 |  | 0 |
| moa-map1#r0 | host_input_generate |  | 112,577.9 | 109,812.7/115,202.4 | 0.0 | cudaEventQuery | 0 |
| moa-map1#r0 | h2d_stage |  | 1,531.5 | 1,465.9/1,681.4 | 1,376.8 | cudaEventSynchronize | 0 |
| moa-map1#r0 | weight_init |  | 196.8 | 126.3/244.3 | 52.7 | cudaLaunchKernel | 2 |
| moa-map1#r0 | mir_operator:RMSNormOp | 6 | 16,101.1 | 16,070.0/16,579.7 | 15,836.9 | cudaEventSynchronize | 224 |
| moa-map1#r0 | inter_operator_dispatch |  | 13.6 | 5.1/30.9 | 0.0 |  | 0 |
| moa-map1#r0 | mir_operator:AddOp | 7 | 713.4 | 686.5/813.2 | 604.8 | cudaEventSynchronize | 32 |
| moa-map1#r0 | mir_operator:RMSNormOp | 8 | 16,220.9 | 16,015.2/16,540.5 | 15,963.9 | cudaEventSynchronize | 224 |
| moa-map1#r0 | mir_operator:LinearOp | 10 | 26,039.2 | 25,695.9/26,384.2 | 25,857.6 | cudaEventSynchronize | 32 |
| moa-map1#r0 | mir_operator:LinearOp | 11 | 26,256.8 | 26,031.1/27,033.2 | 26,095.3 | cudaEventSynchronize | 32 |
| moa-map1#r0 | mir_operator:LinearOp | 12 | 26,855.5 | 25,858.9/27,382.6 | 26,705.9 | cudaEventSynchronize | 32 |
| moa-map1#r0 | mir_operator:ViewOp | 13 | 152.8 | 126.3/180.1 | 0.0 | cudaEventRecord | 0 |
| moa-map1#r0 | mir_operator:TransposeOp | 14 | 7,337.8 | 6,897.8/7,812.3 | 7,207.2 | cudaEventSynchronize | 32 |
| moa-map1#r0 | pre_d2h_alloc |  | 21.4 | 14.5/25.5 | 0.0 |  | 0 |
| moa-map1#r0 | d2h_stage |  | 1,507.0 | 1,480.0/1,545.2 | 1,446.3 | cudaEventSynchronize | 0 |
| moa-map1#r0 | checksum_complete |  | 84.0 | 62.2/93.9 | 0.0 | cudaEventDestroy | 0 |
| moa-map2#r0 | adapter_dispatch |  | 750.0 | 678.8/958.3 | 0.0 |  | 0 |
| moa-map2#r0 | token_preprocess_cpu |  | 328.2 | 271.6/365.1 | 0.0 |  | 0 |
| moa-map2#r0 | host_input_generate |  | 112,349.8 | 106,393.9/116,142.2 | 0.0 | cudaEventQuery | 0 |
| moa-map2#r0 | h2d_stage |  | 1,576.1 | 1,525.2/1,650.5 | 1,440.7 | cudaEventSynchronize | 0 |
| moa-map2#r0 | weight_init |  | 194.2 | 134.8/212.2 | 52.6 | cudaLaunchKernel | 2 |
| moa-map2#r0 | mir_operator:RMSNormOp | 6 | 16,087.0 | 16,057.5/16,457.4 | 15,836.0 | cudaEventSynchronize | 224 |
| moa-map2#r0 | inter_operator_dispatch |  | 13.8 | 4.7/27.8 | 0.0 |  | 0 |
| moa-map2#r0 | mir_operator:AddOp | 7 | 708.3 | 691.9/766.0 | 603.2 | cudaLaunchKernel | 32 |
| moa-map2#r0 | mir_operator:RMSNormOp | 8 | 16,406.3 | 16,011.6/16,434.0 | 16,174.0 | cudaEventSynchronize | 224 |
| moa-map2#r0 | mir_operator:LinearOp | 10 | 26,040.3 | 25,692.0/26,309.5 | 25,850.7 | cudaEventSynchronize | 32 |
| moa-map2#r0 | mir_operator:LinearOp | 11 | 26,689.0 | 25,758.2/27,157.7 | 26,489.3 | cudaEventSynchronize | 32 |
| moa-map2#r0 | mir_operator:LinearOp | 12 | 26,917.4 | 26,401.2/27,259.1 | 26,763.0 | cudaEventSynchronize | 32 |
| moa-map2#r0 | mir_operator:ViewOp | 13 | 154.9 | 139.0/190.9 | 0.0 | cudaEventRecord | 0 |
| moa-map2#r0 | mir_operator:TransposeOp | 14 | 7,401.0 | 7,296.5/7,793.5 | 7,222.1 | cudaEventSynchronize | 32 |
| moa-map2#r0 | pre_d2h_alloc |  | 21.9 | 13.7/30.8 | 0.0 |  | 0 |
| moa-map2#r0 | d2h_stage |  | 1,522.2 | 1,469.6/1,685.1 | 1,456.7 | cudaEventSynchronize | 0 |
| moa-map2#r0 | checksum_complete |  | 82.3 | 78.7/100.1 | 0.0 | cudaEventDestroy | 0 |
| mcts-root#r0 | adapter_dispatch |  | 791.1 | 738.1/889.6 | 0.0 |  | 0 |
| mcts-root#r0 | token_preprocess_cpu |  | 319.7 | 266.9/383.3 | 0.0 |  | 0 |
| mcts-root#r0 | host_input_generate |  | 112,760.2 | 109,591.2/125,620.8 | 0.0 | cudaEventQuery | 0 |
| mcts-root#r0 | h2d_stage |  | 1,530.2 | 1,510.9/1,584.6 | 1,375.9 | cudaEventSynchronize | 0 |
| mcts-root#r0 | weight_init |  | 194.7 | 173.9/207.1 | 52.9 | cudaLaunchKernel | 2 |
| mcts-root#r0 | mir_operator:RMSNormOp | 6 | 16,112.2 | 16,054.2/16,518.5 | 15,825.2 | cudaEventSynchronize | 224 |
| mcts-root#r0 | inter_operator_dispatch |  | 13.1 | 4.8/36.7 | 0.0 |  | 0 |
| mcts-root#r0 | mir_operator:AddOp | 7 | 699.5 | 690.4/1,072.7 | 604.4 | cudaEventSynchronize | 32 |
| mcts-root#r0 | mir_operator:RMSNormOp | 8 | 16,062.0 | 16,006.1/16,467.0 | 15,807.0 | cudaEventSynchronize | 224 |
| mcts-root#r0 | mir_operator:LinearOp | 10 | 26,047.7 | 25,723.6/26,430.9 | 25,851.5 | cudaEventSynchronize | 32 |
| mcts-root#r0 | mir_operator:LinearOp | 11 | 26,405.4 | 25,819.2/26,770.3 | 26,263.1 | cudaEventSynchronize | 32 |
| mcts-root#r0 | mir_operator:LinearOp | 12 | 26,809.6 | 26,184.3/27,648.7 | 26,638.1 | cudaEventSynchronize | 32 |
| mcts-root#r0 | mir_operator:ViewOp | 13 | 157.1 | 144.4/197.0 | 0.0 | cudaEventRecord | 0 |
| mcts-root#r0 | mir_operator:TransposeOp | 14 | 7,357.2 | 7,075.4/7,889.3 | 7,221.8 | cudaEventSynchronize | 32 |
| mcts-root#r0 | pre_d2h_alloc |  | 18.3 | 14.6/30.8 | 0.0 |  | 0 |
| mcts-root#r0 | d2h_stage |  | 1,497.8 | 1,476.7/1,732.7 | 1,442.1 | cudaEventSynchronize | 0 |
| mcts-root#r0 | checksum_complete |  | 82.5 | 76.7/90.1 | 0.0 | cudaEventDestroy | 0 |
| react-tool#r0 | agent_tool_execute_cpu |  | 314.2 | 193.7/384.3 | 0.0 |  | 0 |
| mcts-actor0#r0 | adapter_dispatch |  | 1,308.2 | 1,288.9/1,487.6 | 0.0 |  | 0 |
| mcts-actor0#r0 | token_preprocess_cpu |  | 213.9 | 189.3/279.3 | 0.0 |  | 0 |
| mcts-actor0#r0 | host_input_generate |  | 113,556.3 | 107,642.6/128,686.7 | 0.0 | cudaEventQuery | 0 |
| mcts-actor0#r0 | h2d_stage |  | 1,533.2 | 1,514.5/1,569.3 | 1,381.0 | cudaEventSynchronize | 0 |
| mcts-actor0#r0 | weight_init |  | 197.3 | 175.5/204.5 | 52.9 | cudaLaunchKernel | 2 |
| mcts-actor0#r0 | mir_operator:RMSNormOp | 6 | 16,141.3 | 16,067.5/16,539.1 | 15,874.6 | cudaEventSynchronize | 224 |
| mcts-actor0#r0 | inter_operator_dispatch |  | 13.2 | 5.3/34.0 | 0.0 |  | 0 |
| mcts-actor0#r0 | mir_operator:AddOp | 7 | 700.3 | 694.6/757.5 | 604.3 | cudaEventSynchronize | 32 |
| mcts-actor0#r0 | mir_operator:RMSNormOp | 8 | 16,054.4 | 15,998.2/16,479.6 | 15,804.2 | cudaEventSynchronize | 224 |
| mcts-actor0#r0 | mir_operator:LinearOp | 10 | 26,033.2 | 25,729.0/26,086.9 | 25,798.7 | cudaEventSynchronize | 32 |
| mcts-actor0#r0 | mir_operator:LinearOp | 11 | 26,678.5 | 26,085.2/27,172.4 | 26,541.2 | cudaEventSynchronize | 32 |
| mcts-actor0#r0 | mir_operator:LinearOp | 12 | 26,758.5 | 26,097.4/27,372.6 | 26,585.1 | cudaEventSynchronize | 32 |
| mcts-actor0#r0 | mir_operator:ViewOp | 13 | 150.2 | 141.5/224.2 | 0.0 | cudaEventRecord | 0 |
| mcts-actor0#r0 | mir_operator:TransposeOp | 14 | 7,411.2 | 6,968.7/7,859.7 | 7,282.9 | cudaEventSynchronize | 32 |
| mcts-actor0#r0 | pre_d2h_alloc |  | 16.7 | 14.5/30.7 | 0.0 |  | 0 |
| mcts-actor0#r0 | d2h_stage |  | 1,523.3 | 1,467.8/1,572.9 | 1,442.1 | cudaEventSynchronize | 0 |
| mcts-actor0#r0 | checksum_complete |  | 82.5 | 78.6/87.3 | 0.0 | cudaEventDestroy | 0 |
| mcts-actor1#r0 | adapter_dispatch |  | 765.7 | 701.9/861.5 | 0.0 |  | 0 |
| mcts-actor1#r0 | token_preprocess_cpu |  | 366.8 | 270.5/390.2 | 0.0 |  | 0 |
| mcts-actor1#r0 | host_input_generate |  | 112,908.4 | 108,602.1/128,498.2 | 0.0 | cudaEventQuery | 0 |
| mcts-actor1#r0 | h2d_stage |  | 1,528.4 | 1,496.9/1,649.1 | 1,380.9 | cudaEventSynchronize | 0 |
| mcts-actor1#r0 | weight_init |  | 200.2 | 169.1/203.1 | 52.8 | cudaLaunchKernel | 2 |
| mcts-actor1#r0 | mir_operator:RMSNormOp | 6 | 16,531.7 | 16,082.1/16,788.5 | 16,263.8 | cudaEventSynchronize | 224 |
| mcts-actor1#r0 | inter_operator_dispatch |  | 13.2 | 5.0/41.5 | 0.0 |  | 0 |
| mcts-actor1#r0 | mir_operator:AddOp | 7 | 703.0 | 684.5/717.4 | 603.4 | cudaLaunchKernel | 32 |
| mcts-actor1#r0 | mir_operator:RMSNormOp | 8 | 16,039.8 | 16,009.2/16,413.8 | 15,820.5 | cudaEventSynchronize | 224 |
| mcts-actor1#r0 | mir_operator:LinearOp | 10 | 25,915.1 | 25,710.9/26,087.0 | 25,686.9 | cudaEventSynchronize | 32 |
| mcts-actor1#r0 | mir_operator:LinearOp | 11 | 26,413.7 | 25,738.5/27,174.4 | 26,197.0 | cudaEventSynchronize | 32 |
| mcts-actor1#r0 | mir_operator:LinearOp | 12 | 26,938.7 | 26,489.2/27,286.8 | 26,787.8 | cudaEventSynchronize | 32 |
| mcts-actor1#r0 | mir_operator:ViewOp | 13 | 149.7 | 142.5/341.6 | 0.0 | cudaEventRecord | 0 |
| mcts-actor1#r0 | mir_operator:TransposeOp | 14 | 7,386.9 | 6,991.1/7,786.6 | 7,247.6 | cudaEventSynchronize | 32 |
| mcts-actor1#r0 | pre_d2h_alloc |  | 19.4 | 11.2/33.2 | 0.0 |  | 0 |
| mcts-actor1#r0 | d2h_stage |  | 1,500.0 | 1,483.2/1,588.3 | 1,438.6 | cudaEventSynchronize | 0 |
| mcts-actor1#r0 | checksum_complete |  | 83.9 | 72.5/104.6 | 0.0 | cudaEventDestroy | 0 |
| moa-reduce#r0 | adapter_dispatch |  | 788.9 | 706.6/1,717.1 | 0.0 |  | 0 |
| moa-reduce#r0 | token_preprocess_cpu |  | 334.0 | 272.6/3,044.0 | 0.0 |  | 0 |
| moa-reduce#r0 | host_input_generate |  | 114,358.6 | 112,209.0/127,586.8 | 0.0 | cudaEventQuery | 0 |
| moa-reduce#r0 | h2d_stage |  | 1,522.5 | 1,517.2/1,599.4 | 1,377.0 | cudaEventSynchronize | 0 |
| moa-reduce#r0 | weight_init |  | 195.9 | 181.5/227.2 | 53.1 | cudaLaunchKernel | 2 |
| moa-reduce#r0 | mir_operator:RMSNormOp | 6 | 16,284.2 | 16,074.0/16,467.4 | 16,021.9 | cudaEventSynchronize | 224 |
| moa-reduce#r0 | inter_operator_dispatch |  | 11.7 | 4.9/39.2 | 0.0 |  | 0 |
| moa-reduce#r0 | mir_operator:AddOp | 7 | 704.5 | 690.7/722.3 | 606.0 | cudaEventSynchronize | 32 |
| moa-reduce#r0 | mir_operator:RMSNormOp | 8 | 16,042.1 | 15,980.8/16,464.5 | 15,817.5 | cudaEventSynchronize | 224 |
| moa-reduce#r0 | mir_operator:LinearOp | 10 | 26,065.2 | 25,773.9/26,455.1 | 25,878.5 | cudaEventSynchronize | 32 |
| moa-reduce#r0 | mir_operator:LinearOp | 11 | 26,245.3 | 25,787.0/27,307.3 | 26,086.2 | cudaEventSynchronize | 32 |
| moa-reduce#r0 | mir_operator:LinearOp | 12 | 26,856.5 | 26,584.3/27,317.3 | 26,692.5 | cudaEventSynchronize | 32 |
| moa-reduce#r0 | mir_operator:ViewOp | 13 | 149.0 | 140.1/164.1 | 0.0 | cudaEventRecord | 0 |
| moa-reduce#r0 | mir_operator:TransposeOp | 14 | 7,393.4 | 7,205.7/7,457.8 | 7,272.9 | cudaEventSynchronize | 32 |
| moa-reduce#r0 | pre_d2h_alloc |  | 18.3 | 12.7/30.0 | 0.0 |  | 0 |
| moa-reduce#r0 | d2h_stage |  | 1,489.7 | 1,470.0/1,747.3 | 1,432.2 | cudaEventSynchronize | 0 |
| moa-reduce#r0 | checksum_complete |  | 82.1 | 78.0/94.4 | 0.0 | cudaEventDestroy | 0 |
| react-answer#r0 | adapter_dispatch |  | 783.9 | 700.3/1,057.1 | 0.0 |  | 0 |
| react-answer#r0 | token_preprocess_cpu |  | 359.5 | 276.0/488.8 | 0.0 |  | 0 |
| react-answer#r0 | host_input_generate |  | 87,888.7 | 82,866.8/92,369.5 | 0.0 | cudaEventQuery | 0 |
| react-answer#r0 | h2d_stage |  | 1,212.1 | 1,193.1/1,257.0 | 1,056.9 | cudaEventSynchronize | 0 |
| react-answer#r0 | weight_init |  | 190.2 | 176.8/211.4 | 39.8 | cudaLaunchKernel | 2 |
| react-answer#r0 | mir_operator:RMSNormOp | 6 | 9,471.9 | 9,436.0/9,866.0 | 9,215.1 | cudaEventSynchronize | 224 |
| react-answer#r0 | inter_operator_dispatch |  | 9.8 | 4.7/19.6 | 0.0 |  | 0 |
| react-answer#r0 | mir_operator:AddOp | 7 | 541.4 | 521.6/584.6 | 432.6 | cudaLaunchKernel | 32 |
| react-answer#r0 | mir_operator:RMSNormOp | 8 | 9,376.2 | 9,319.4/9,834.0 | 9,162.3 | cudaEventSynchronize | 224 |
| react-answer#r0 | mir_operator:LinearOp | 10 | 19,708.3 | 19,655.1/20,029.1 | 19,550.1 | cudaEventSynchronize | 32 |
| react-answer#r0 | mir_operator:LinearOp | 11 | 19,951.0 | 19,760.4/20,004.3 | 19,853.5 | cudaEventSynchronize | 32 |
| react-answer#r0 | mir_operator:LinearOp | 12 | 19,902.0 | 19,591.6/20,665.4 | 19,790.8 | cudaEventSynchronize | 32 |
| react-answer#r0 | mir_operator:ViewOp | 13 | 143.6 | 137.6/160.9 | 0.0 | cudaEventRecord | 0 |
| react-answer#r0 | mir_operator:TransposeOp | 14 | 5,756.0 | 5,422.6/6,378.3 | 5,628.2 | cudaEventSynchronize | 32 |
| react-answer#r0 | pre_d2h_alloc |  | 15.3 | 10.7/31.9 | 0.0 |  | 0 |
| react-answer#r0 | d2h_stage |  | 1,149.1 | 1,142.9/1,187.1 | 1,092.2 | cudaEventSynchronize | 0 |
| react-answer#r0 | checksum_complete |  | 79.5 | 74.3/84.8 | 0.0 | cudaEventDestroy | 0 |
| mcts-critic#r0 | adapter_dispatch |  | 767.9 | 744.1/860.9 | 0.0 |  | 0 |
| mcts-critic#r0 | token_preprocess_cpu |  | 353.6 | 229.4/397.9 | 0.0 |  | 0 |
| mcts-critic#r0 | host_input_generate |  | 112,838.1 | 106,420.7/116,532.1 | 0.0 | cudaEventQuery | 0 |
| mcts-critic#r0 | h2d_stage |  | 1,552.0 | 1,521.6/1,629.5 | 1,381.8 | cudaEventSynchronize | 0 |
| mcts-critic#r0 | weight_init |  | 191.9 | 164.6/289.6 | 52.0 | cudaLaunchKernel | 2 |
| mcts-critic#r0 | mir_operator:RMSNormOp | 6 | 16,402.0 | 16,067.0/16,571.3 | 16,146.6 | cudaEventSynchronize | 224 |
| mcts-critic#r0 | inter_operator_dispatch |  | 12.1 | 5.0/31.0 | 0.0 |  | 0 |
| mcts-critic#r0 | mir_operator:AddOp | 7 | 701.8 | 686.9/733.0 | 603.5 | cudaEventSynchronize | 32 |
| mcts-critic#r0 | mir_operator:RMSNormOp | 8 | 16,368.6 | 16,006.6/16,517.5 | 16,158.6 | cudaEventSynchronize | 224 |
| mcts-critic#r0 | mir_operator:LinearOp | 10 | 26,099.9 | 25,736.2/26,425.1 | 25,876.1 | cudaEventSynchronize | 32 |
| mcts-critic#r0 | mir_operator:LinearOp | 11 | 26,064.4 | 25,984.6/27,116.0 | 25,902.8 | cudaEventSynchronize | 32 |
| mcts-critic#r0 | mir_operator:LinearOp | 12 | 26,672.7 | 26,366.1/27,309.5 | 26,538.7 | cudaEventSynchronize | 32 |
| mcts-critic#r0 | mir_operator:ViewOp | 13 | 163.1 | 134.3/177.7 | 0.0 | cudaEventRecord | 0 |
| mcts-critic#r0 | mir_operator:TransposeOp | 14 | 7,410.7 | 7,316.4/7,893.1 | 7,259.0 | cudaEventSynchronize | 32 |
| mcts-critic#r0 | pre_d2h_alloc |  | 22.0 | 13.1/34.5 | 0.0 |  | 0 |
| mcts-critic#r0 | d2h_stage |  | 1,515.7 | 1,486.7/1,552.3 | 1,444.3 | cudaEventSynchronize | 0 |
| mcts-critic#r0 | checksum_complete |  | 85.1 | 80.9/92.6 | 0.0 | cudaEventDestroy | 0 |
| react-plan#r1 | adapter_dispatch |  | 795.4 | 737.6/984.6 | 0.0 |  | 0 |
| react-plan#r1 | token_preprocess_cpu |  | 360.8 | 273.8/386.0 | 0.0 |  | 0 |
| react-plan#r1 | host_input_generate |  | 65,769.4 | 64,295.8/76,796.6 | 0.0 | cudaEventQuery | 0 |
| react-plan#r1 | h2d_stage |  | 925.6 | 898.4/953.9 | 776.0 | cudaEventSynchronize | 0 |
| react-plan#r1 | weight_init |  | 194.9 | 168.6/250.4 | 29.6 | cudaLaunchKernel | 2 |
| react-plan#r1 | mir_operator:RMSNormOp | 6 | 4,310.7 | 4,301.3/5,139.2 | 4,052.0 | cudaEventSynchronize | 224 |
| react-plan#r1 | inter_operator_dispatch |  | 9.1 | 5.5/20.4 | 0.0 |  | 0 |
| react-plan#r1 | mir_operator:AddOp | 7 | 574.2 | 528.0/872.5 | 325.0 | cudaLaunchKernel | 32 |
| react-plan#r1 | mir_operator:RMSNormOp | 8 | 4,282.1 | 4,217.2/5,008.4 | 4,047.4 | cudaEventSynchronize | 224 |
| react-plan#r1 | mir_operator:LinearOp | 10 | 11,530.0 | 11,285.3/11,658.0 | 11,375.8 | cudaEventSynchronize | 32 |
| react-plan#r1 | mir_operator:LinearOp | 11 | 11,305.6 | 11,237.0/11,612.2 | 11,185.6 | cudaEventSynchronize | 32 |
| react-plan#r1 | mir_operator:LinearOp | 12 | 11,355.1 | 11,250.9/11,647.9 | 11,267.0 | cudaEventSynchronize | 32 |
| react-plan#r1 | mir_operator:ViewOp | 13 | 150.6 | 134.0/234.1 | 0.0 | cudaEventRecord | 0 |
| react-plan#r1 | mir_operator:TransposeOp | 14 | 4,181.2 | 4,113.4/4,461.3 | 4,055.4 | cudaEventSynchronize | 32 |
| react-plan#r1 | pre_d2h_alloc |  | 16.8 | 11.3/29.5 | 0.0 |  | 0 |
| react-plan#r1 | d2h_stage |  | 883.4 | 854.3/901.8 | 821.3 | cudaEventSynchronize | 0 |
| react-plan#r1 | checksum_complete |  | 80.8 | 73.4/96.6 | 0.0 | cudaEventDestroy | 0 |
| moa-map0#r1 | adapter_dispatch |  | 836.9 | 751.2/1,711.2 | 0.0 |  | 0 |
| moa-map0#r1 | token_preprocess_cpu |  | 347.8 | 219.3/393.3 | 0.0 |  | 0 |
| moa-map0#r1 | host_input_generate |  | 112,284.0 | 109,951.0/135,390.6 | 0.0 | cudaEventQuery | 0 |
| moa-map0#r1 | h2d_stage |  | 1,569.7 | 1,512.2/2,035.5 | 1,422.5 | cudaEventSynchronize | 0 |
| moa-map0#r1 | weight_init |  | 184.2 | 173.9/195.7 | 52.0 | cudaLaunchKernel | 2 |
| moa-map0#r1 | mir_operator:RMSNormOp | 6 | 16,151.3 | 16,057.6/16,533.3 | 15,879.6 | cudaEventSynchronize | 224 |
| moa-map0#r1 | inter_operator_dispatch |  | 11.8 | 5.0/50.5 | 0.0 |  | 0 |
| moa-map0#r1 | mir_operator:AddOp | 7 | 699.3 | 689.1/765.5 | 605.3 | cudaEventSynchronize | 32 |
| moa-map0#r1 | mir_operator:RMSNormOp | 8 | 16,073.7 | 16,007.4/16,494.8 | 15,851.5 | cudaEventSynchronize | 224 |
| moa-map0#r1 | mir_operator:LinearOp | 10 | 25,923.0 | 25,706.0/26,323.2 | 25,728.9 | cudaEventSynchronize | 32 |
| moa-map0#r1 | mir_operator:LinearOp | 11 | 26,600.1 | 25,745.5/27,397.9 | 26,459.9 | cudaEventSynchronize | 32 |
| moa-map0#r1 | mir_operator:LinearOp | 12 | 26,881.6 | 26,143.2/27,275.7 | 26,713.4 | cudaEventSynchronize | 32 |
| moa-map0#r1 | mir_operator:ViewOp | 13 | 159.0 | 139.7/173.0 | 0.0 | cudaEventRecord | 0 |
| moa-map0#r1 | mir_operator:TransposeOp | 14 | 7,427.4 | 7,012.5/7,819.7 | 7,294.4 | cudaEventSynchronize | 32 |
| moa-map0#r1 | pre_d2h_alloc |  | 18.4 | 11.8/32.5 | 0.0 |  | 0 |
| moa-map0#r1 | d2h_stage |  | 1,486.9 | 1,464.7/1,590.9 | 1,429.4 | cudaEventSynchronize | 0 |
| moa-map0#r1 | checksum_complete |  | 80.3 | 78.3/90.5 | 0.0 | cudaEventDestroy | 0 |
| moa-map1#r1 | adapter_dispatch |  | 754.4 | 709.9/878.5 | 0.0 |  | 0 |
| moa-map1#r1 | token_preprocess_cpu |  | 337.6 | 260.5/434.8 | 0.0 |  | 0 |
| moa-map1#r1 | host_input_generate |  | 114,586.2 | 109,102.0/132,354.5 | 0.0 | cudaEventQuery | 0 |
| moa-map1#r1 | h2d_stage |  | 1,540.7 | 1,509.8/1,651.6 | 1,388.5 | cudaEventSynchronize | 0 |
| moa-map1#r1 | weight_init |  | 193.8 | 174.4/244.2 | 53.0 | cudaLaunchKernel | 2 |
| moa-map1#r1 | mir_operator:RMSNormOp | 6 | 16,261.6 | 16,034.9/16,552.4 | 15,996.1 | cudaEventSynchronize | 224 |
| moa-map1#r1 | inter_operator_dispatch |  | 13.5 | 5.0/23.6 | 0.0 |  | 0 |
| moa-map1#r1 | mir_operator:AddOp | 7 | 703.4 | 683.7/712.9 | 605.8 | cudaLaunchKernel | 32 |
| moa-map1#r1 | mir_operator:RMSNormOp | 8 | 16,318.8 | 15,995.9/16,533.4 | 16,099.6 | cudaEventSynchronize | 224 |
| moa-map1#r1 | mir_operator:LinearOp | 10 | 26,004.7 | 25,767.8/26,217.2 | 25,821.5 | cudaEventSynchronize | 32 |
| moa-map1#r1 | mir_operator:LinearOp | 11 | 26,897.7 | 26,072.2/27,120.3 | 26,750.0 | cudaEventSynchronize | 32 |
| moa-map1#r1 | mir_operator:LinearOp | 12 | 26,905.1 | 26,152.9/27,699.0 | 26,769.1 | cudaEventSynchronize | 32 |
| moa-map1#r1 | mir_operator:ViewOp | 13 | 149.4 | 133.7/195.3 | 0.0 | cudaEventRecord | 0 |
| moa-map1#r1 | mir_operator:TransposeOp | 14 | 7,348.8 | 7,261.7/7,753.2 | 7,221.3 | cudaEventSynchronize | 32 |
| moa-map1#r1 | pre_d2h_alloc |  | 19.1 | 10.0/41.2 | 0.0 |  | 0 |
| moa-map1#r1 | d2h_stage |  | 1,547.5 | 1,490.8/1,683.7 | 1,469.5 | cudaEventSynchronize | 0 |
| moa-map1#r1 | checksum_complete |  | 83.8 | 72.5/139.6 | 0.0 | cudaEventDestroy | 0 |
| moa-map2#r1 | adapter_dispatch |  | 797.3 | 702.2/1,328.0 | 0.0 |  | 0 |
| moa-map2#r1 | token_preprocess_cpu |  | 335.2 | 267.0/381.4 | 0.0 |  | 0 |
| moa-map2#r1 | host_input_generate |  | 113,025.1 | 107,066.9/134,156.9 | 0.0 | cudaEventQuery | 0 |
| moa-map2#r1 | h2d_stage |  | 1,553.6 | 1,516.6/1,667.8 | 1,399.5 | cudaEventSynchronize | 0 |
| moa-map2#r1 | weight_init |  | 189.1 | 180.8/232.0 | 52.9 | cudaLaunchKernel | 2 |
| moa-map2#r1 | mir_operator:RMSNormOp | 6 | 16,232.8 | 16,064.2/16,576.4 | 15,969.1 | cudaEventSynchronize | 224 |
| moa-map2#r1 | inter_operator_dispatch |  | 13.6 | 5.3/32.0 | 0.0 |  | 0 |
| moa-map2#r1 | mir_operator:AddOp | 7 | 705.7 | 694.8/745.0 | 604.4 | cudaEventSynchronize | 32 |
| moa-map2#r1 | mir_operator:RMSNormOp | 8 | 16,053.8 | 16,013.8/16,433.2 | 15,818.9 | cudaEventSynchronize | 224 |
| moa-map2#r1 | mir_operator:LinearOp | 10 | 26,038.5 | 25,778.4/26,136.9 | 25,844.3 | cudaEventSynchronize | 32 |
| moa-map2#r1 | mir_operator:LinearOp | 11 | 26,134.0 | 25,723.4/27,366.6 | 25,991.1 | cudaEventSynchronize | 32 |
| moa-map2#r1 | mir_operator:LinearOp | 12 | 27,021.1 | 26,151.0/27,610.6 | 26,852.6 | cudaEventSynchronize | 32 |
| moa-map2#r1 | mir_operator:ViewOp | 13 | 149.6 | 140.0/280.5 | 0.0 | cudaEventRecord | 0 |
| moa-map2#r1 | mir_operator:TransposeOp | 14 | 7,374.0 | 7,296.2/7,474.1 | 7,244.3 | cudaEventSynchronize | 32 |
| moa-map2#r1 | pre_d2h_alloc |  | 19.8 | 12.9/37.7 | 0.0 |  | 0 |
| moa-map2#r1 | d2h_stage |  | 1,519.4 | 1,473.7/1,821.3 | 1,452.1 | cudaEventSynchronize | 0 |
| moa-map2#r1 | checksum_complete |  | 81.5 | 78.5/103.0 | 0.0 | cudaEventDestroy | 0 |
| mcts-root#r1 | adapter_dispatch |  | 804.5 | 766.8/926.0 | 0.0 |  | 0 |
| mcts-root#r1 | token_preprocess_cpu |  | 349.9 | 278.7/394.7 | 0.0 |  | 0 |
| mcts-root#r1 | host_input_generate |  | 113,466.2 | 110,322.8/131,382.1 | 0.0 | cudaEventQuery | 0 |
| mcts-root#r1 | h2d_stage |  | 1,533.0 | 1,524.3/1,597.0 | 1,385.6 | cudaEventSynchronize | 0 |
| mcts-root#r1 | weight_init |  | 192.8 | 174.5/203.2 | 52.6 | cudaLaunchKernel | 2 |
| mcts-root#r1 | mir_operator:RMSNormOp | 6 | 16,099.2 | 16,064.8/16,539.6 | 15,835.9 | cudaEventSynchronize | 224 |
| mcts-root#r1 | inter_operator_dispatch |  | 12.2 | 4.9/35.5 | 0.0 |  | 0 |
| mcts-root#r1 | mir_operator:AddOp | 7 | 701.1 | 686.5/1,121.7 | 604.1 | cudaEventSynchronize | 32 |
| mcts-root#r1 | mir_operator:RMSNormOp | 8 | 16,336.8 | 15,993.6/16,450.5 | 16,126.1 | cudaEventSynchronize | 224 |
| mcts-root#r1 | mir_operator:LinearOp | 10 | 26,086.2 | 25,707.4/26,409.2 | 25,882.3 | cudaEventSynchronize | 32 |
| mcts-root#r1 | mir_operator:LinearOp | 11 | 26,532.3 | 25,862.4/27,076.7 | 26,402.7 | cudaEventSynchronize | 32 |
| mcts-root#r1 | mir_operator:LinearOp | 12 | 27,061.4 | 25,802.1/27,894.7 | 26,833.7 | cudaEventSynchronize | 32 |
| mcts-root#r1 | mir_operator:ViewOp | 13 | 154.2 | 128.3/207.7 | 0.0 | cudaEventRecord | 0 |
| mcts-root#r1 | mir_operator:TransposeOp | 14 | 7,367.8 | 7,301.2/7,833.0 | 7,220.1 | cudaEventSynchronize | 32 |
| mcts-root#r1 | pre_d2h_alloc |  | 22.5 | 13.1/37.0 | 0.0 |  | 0 |
| mcts-root#r1 | d2h_stage |  | 1,517.2 | 1,488.7/1,737.5 | 1,460.4 | cudaEventSynchronize | 0 |
| mcts-root#r1 | checksum_complete |  | 88.6 | 78.5/91.8 | 0.0 | cudaEventDestroy | 0 |
| react-tool#r1 | agent_tool_execute_cpu |  | 276.2 | 254.1/357.4 | 0.0 |  | 0 |
| mcts-actor0#r1 | adapter_dispatch |  | 1,318.2 | 1,294.9/1,400.9 | 0.0 |  | 0 |
| mcts-actor0#r1 | token_preprocess_cpu |  | 201.5 | 190.9/281.2 | 0.0 |  | 0 |
| mcts-actor0#r1 | host_input_generate |  | 112,372.3 | 107,815.0/137,386.2 | 0.0 | cudaEventQuery | 0 |
| mcts-actor0#r1 | h2d_stage |  | 1,551.9 | 1,495.8/2,045.6 | 1,401.2 | cudaEventSynchronize | 0 |
| mcts-actor0#r1 | weight_init |  | 189.5 | 167.2/210.6 | 52.8 | cudaLaunchKernel | 2 |
| mcts-actor0#r1 | mir_operator:RMSNormOp | 6 | 16,447.2 | 16,055.6/16,583.9 | 16,193.3 | cudaEventSynchronize | 224 |
| mcts-actor0#r1 | inter_operator_dispatch |  | 13.7 | 4.7/39.6 | 0.0 |  | 0 |
| mcts-actor0#r1 | mir_operator:AddOp | 7 | 706.9 | 694.6/741.2 | 604.8 | cudaEventSynchronize | 32 |
| mcts-actor0#r1 | mir_operator:RMSNormOp | 8 | 16,210.8 | 15,984.9/16,480.7 | 15,993.2 | cudaEventSynchronize | 224 |
| mcts-actor0#r1 | mir_operator:LinearOp | 10 | 26,082.0 | 25,725.8/26,394.1 | 25,895.5 | cudaEventSynchronize | 32 |
| mcts-actor0#r1 | mir_operator:LinearOp | 11 | 26,298.6 | 26,031.1/27,036.8 | 26,171.6 | cudaEventSynchronize | 32 |
| mcts-actor0#r1 | mir_operator:LinearOp | 12 | 26,455.6 | 25,846.7/27,839.4 | 26,305.4 | cudaEventSynchronize | 32 |
| mcts-actor0#r1 | mir_operator:ViewOp | 13 | 160.9 | 137.2/239.4 | 0.0 | cudaEventRecord | 0 |
| mcts-actor0#r1 | mir_operator:TransposeOp | 14 | 7,353.9 | 7,045.7/7,403.1 | 7,211.8 | cudaEventSynchronize | 32 |
| mcts-actor0#r1 | pre_d2h_alloc |  | 20.1 | 12.0/34.8 | 0.0 |  | 0 |
| mcts-actor0#r1 | d2h_stage |  | 1,490.3 | 1,468.2/1,522.9 | 1,431.0 | cudaEventSynchronize | 0 |
| mcts-actor0#r1 | checksum_complete |  | 83.1 | 75.4/93.3 | 0.0 | cudaEventDestroy | 0 |
| mcts-actor1#r1 | adapter_dispatch |  | 786.3 | 730.4/868.6 | 0.0 |  | 0 |
| mcts-actor1#r1 | token_preprocess_cpu |  | 329.0 | 267.0/408.6 | 0.0 |  | 0 |
| mcts-actor1#r1 | host_input_generate |  | 113,281.0 | 107,999.4/118,298.5 | 0.0 | cudaEventQuery | 0 |
| mcts-actor1#r1 | h2d_stage |  | 1,530.7 | 1,484.7/1,622.8 | 1,383.9 | cudaEventSynchronize | 0 |
| mcts-actor1#r1 | weight_init |  | 192.8 | 172.2/215.4 | 52.8 | cudaLaunchKernel | 2 |
| mcts-actor1#r1 | mir_operator:RMSNormOp | 6 | 16,396.9 | 16,089.9/16,484.5 | 16,133.0 | cudaEventSynchronize | 224 |
| mcts-actor1#r1 | inter_operator_dispatch |  | 13.5 | 5.6/36.5 | 0.0 |  | 0 |
| mcts-actor1#r1 | mir_operator:AddOp | 7 | 715.2 | 692.7/741.1 | 607.5 | cudaLaunchKernel | 32 |
| mcts-actor1#r1 | mir_operator:RMSNormOp | 8 | 16,223.9 | 15,989.0/16,533.6 | 15,987.1 | cudaEventSynchronize | 224 |
| mcts-actor1#r1 | mir_operator:LinearOp | 10 | 25,931.9 | 25,735.9/26,155.2 | 25,747.0 | cudaEventSynchronize | 32 |
| mcts-actor1#r1 | mir_operator:LinearOp | 11 | 26,257.5 | 25,725.9/27,133.6 | 26,115.5 | cudaEventSynchronize | 32 |
| mcts-actor1#r1 | mir_operator:LinearOp | 12 | 27,097.0 | 26,486.6/27,675.3 | 26,933.6 | cudaEventSynchronize | 32 |
| mcts-actor1#r1 | mir_operator:ViewOp | 13 | 158.1 | 139.8/172.5 | 0.0 | cudaEventRecord | 0 |
| mcts-actor1#r1 | mir_operator:TransposeOp | 14 | 7,354.9 | 7,304.2/7,799.4 | 7,222.7 | cudaEventSynchronize | 32 |
| mcts-actor1#r1 | pre_d2h_alloc |  | 20.8 | 13.6/33.5 | 0.0 |  | 0 |
| mcts-actor1#r1 | d2h_stage |  | 1,507.6 | 1,492.5/1,564.0 | 1,449.9 | cudaEventSynchronize | 0 |
| mcts-actor1#r1 | checksum_complete |  | 85.8 | 84.0/90.9 | 0.0 | cudaEventDestroy | 0 |
| moa-reduce#r1 | adapter_dispatch |  | 821.9 | 731.2/955.8 | 0.0 |  | 0 |
| moa-reduce#r1 | token_preprocess_cpu |  | 305.0 | 212.1/365.2 | 0.0 |  | 0 |
| moa-reduce#r1 | host_input_generate |  | 112,796.6 | 108,773.7/116,444.4 | 0.0 | cudaEventQuery | 0 |
| moa-reduce#r1 | h2d_stage |  | 1,577.1 | 1,519.4/1,635.8 | 1,426.7 | cudaEventSynchronize | 0 |
| moa-reduce#r1 | weight_init |  | 192.5 | 169.1/208.4 | 52.8 | cudaLaunchKernel | 2 |
| moa-reduce#r1 | mir_operator:RMSNormOp | 6 | 16,436.5 | 16,095.3/16,529.9 | 16,185.3 | cudaEventSynchronize | 224 |
| moa-reduce#r1 | inter_operator_dispatch |  | 12.6 | 4.7/27.4 | 0.0 |  | 0 |
| moa-reduce#r1 | mir_operator:AddOp | 7 | 703.6 | 689.9/755.7 | 605.8 | cudaEventSynchronize | 32 |
| moa-reduce#r1 | mir_operator:RMSNormOp | 8 | 16,319.5 | 16,001.6/16,521.5 | 16,112.7 | cudaEventSynchronize | 224 |
| moa-reduce#r1 | mir_operator:LinearOp | 10 | 26,073.3 | 25,728.1/26,110.0 | 25,882.0 | cudaEventSynchronize | 32 |
| moa-reduce#r1 | mir_operator:LinearOp | 11 | 26,570.3 | 25,770.5/26,997.6 | 26,435.8 | cudaEventSynchronize | 32 |
| moa-reduce#r1 | mir_operator:LinearOp | 12 | 26,943.8 | 26,151.4/27,293.2 | 26,784.1 | cudaEventSynchronize | 32 |
| moa-reduce#r1 | mir_operator:ViewOp | 13 | 148.6 | 139.5/156.1 | 0.0 | cudaEventRecord | 0 |
| moa-reduce#r1 | mir_operator:TransposeOp | 14 | 7,359.3 | 7,283.0/7,453.6 | 7,224.3 | cudaEventSynchronize | 32 |
| moa-reduce#r1 | pre_d2h_alloc |  | 19.3 | 11.2/35.7 | 0.0 |  | 0 |
| moa-reduce#r1 | d2h_stage |  | 1,516.9 | 1,470.9/1,699.3 | 1,432.8 | cudaEventSynchronize | 0 |
| moa-reduce#r1 | checksum_complete |  | 81.6 | 76.7/98.9 | 0.0 | cudaEventDestroy | 0 |
| react-answer#r1 | adapter_dispatch |  | 800.4 | 715.8/847.9 | 0.0 |  | 0 |
| react-answer#r1 | token_preprocess_cpu |  | 334.5 | 252.5/404.5 | 0.0 |  | 0 |
| react-answer#r1 | host_input_generate |  | 86,411.6 | 82,573.7/90,302.3 | 0.0 | cudaEventQuery | 0 |
| react-answer#r1 | h2d_stage |  | 1,206.2 | 1,161.8/1,706.0 | 1,062.0 | cudaEventSynchronize | 0 |
| react-answer#r1 | weight_init |  | 178.3 | 142.4/206.2 | 39.8 | cudaLaunchKernel | 2 |
| react-answer#r1 | mir_operator:RMSNormOp | 6 | 9,452.0 | 9,419.0/9,835.8 | 9,208.6 | cudaEventSynchronize | 224 |
| react-answer#r1 | inter_operator_dispatch |  | 10.1 | 5.0/24.9 | 0.0 |  | 0 |
| react-answer#r1 | mir_operator:AddOp | 7 | 569.2 | 525.2/600.4 | 433.4 | cudaLaunchKernel | 32 |
| react-answer#r1 | mir_operator:RMSNormOp | 8 | 9,714.7 | 9,342.5/9,804.4 | 9,507.1 | cudaEventSynchronize | 224 |
| react-answer#r1 | mir_operator:LinearOp | 10 | 19,668.9 | 19,649.8/19,880.9 | 19,516.5 | cudaEventSynchronize | 32 |
| react-answer#r1 | mir_operator:LinearOp | 11 | 19,894.0 | 19,674.4/20,445.7 | 19,770.0 | cudaEventSynchronize | 32 |
| react-answer#r1 | mir_operator:LinearOp | 12 | 20,398.7 | 19,604.8/20,809.8 | 20,284.9 | cudaEventSynchronize | 32 |
| react-answer#r1 | mir_operator:ViewOp | 13 | 150.7 | 137.6/164.8 | 0.0 | cudaEventRecord | 0 |
| react-answer#r1 | mir_operator:TransposeOp | 14 | 5,878.5 | 5,433.2/5,959.0 | 5,742.3 | cudaEventSynchronize | 32 |
| react-answer#r1 | pre_d2h_alloc |  | 18.5 | 10.7/32.8 | 0.0 |  | 0 |
| react-answer#r1 | d2h_stage |  | 1,161.2 | 1,143.5/1,216.5 | 1,105.9 | cudaEventSynchronize | 0 |
| react-answer#r1 | checksum_complete |  | 81.0 | 68.3/90.5 | 0.0 | cudaEventDestroy | 0 |
| mcts-critic#r1 | adapter_dispatch |  | 796.3 | 684.1/930.9 | 0.0 |  | 0 |
| mcts-critic#r1 | token_preprocess_cpu |  | 318.3 | 277.8/376.7 | 0.0 |  | 0 |
| mcts-critic#r1 | host_input_generate |  | 113,866.3 | 111,154.3/122,237.1 | 0.0 | cudaEventQuery | 0 |
| mcts-critic#r1 | h2d_stage |  | 1,548.0 | 1,513.5/1,691.1 | 1,406.8 | cudaEventSynchronize | 0 |
| mcts-critic#r1 | weight_init |  | 189.7 | 147.4/205.3 | 51.8 | cudaLaunchKernel | 2 |
| mcts-critic#r1 | mir_operator:RMSNormOp | 6 | 16,452.9 | 16,063.9/16,564.9 | 16,194.9 | cudaEventSynchronize | 224 |
| mcts-critic#r1 | inter_operator_dispatch |  | 13.0 | 4.7/29.2 | 0.0 |  | 0 |
| mcts-critic#r1 | mir_operator:AddOp | 7 | 705.3 | 688.9/774.1 | 604.9 | cudaEventSynchronize | 32 |
| mcts-critic#r1 | mir_operator:RMSNormOp | 8 | 16,037.0 | 16,004.7/16,409.4 | 15,823.0 | cudaEventSynchronize | 224 |
| mcts-critic#r1 | mir_operator:LinearOp | 10 | 25,765.1 | 25,672.7/26,102.8 | 25,560.8 | cudaEventSynchronize | 32 |
| mcts-critic#r1 | mir_operator:LinearOp | 11 | 26,591.6 | 26,045.6/26,970.2 | 26,432.8 | cudaEventSynchronize | 32 |
| mcts-critic#r1 | mir_operator:LinearOp | 12 | 26,922.6 | 25,908.8/27,560.1 | 26,797.1 | cudaEventSynchronize | 32 |
| mcts-critic#r1 | mir_operator:ViewOp | 13 | 147.3 | 135.0/165.1 | 0.0 | cudaEventRecord | 0 |
| mcts-critic#r1 | mir_operator:TransposeOp | 14 | 7,563.7 | 7,276.2/7,896.4 | 7,442.8 | cudaEventSynchronize | 32 |
| mcts-critic#r1 | pre_d2h_alloc |  | 20.6 | 11.9/34.1 | 0.0 |  | 0 |
| mcts-critic#r1 | d2h_stage |  | 1,522.5 | 1,472.5/1,567.2 | 1,464.3 | cudaEventSynchronize | 0 |
| mcts-critic#r1 | checksum_complete |  | 82.5 | 77.9/87.5 | 0.0 | cudaEventDestroy | 0 |
| react-plan#r2 | adapter_dispatch |  | 764.8 | 730.0/829.3 | 0.0 |  | 0 |
| react-plan#r2 | token_preprocess_cpu |  | 323.3 | 268.7/365.1 | 0.0 |  | 0 |
| react-plan#r2 | host_input_generate |  | 65,402.8 | 63,428.9/66,776.1 | 0.0 | cudaEventQuery | 0 |
| react-plan#r2 | h2d_stage |  | 935.7 | 888.0/1,015.6 | 810.3 | cudaEventSynchronize | 0 |
| react-plan#r2 | weight_init |  | 186.4 | 140.8/201.2 | 29.8 | cudaLaunchKernel | 2 |
| react-plan#r2 | mir_operator:RMSNormOp | 6 | 4,344.7 | 4,281.8/4,402.4 | 4,096.8 | cudaEventSynchronize | 224 |
| react-plan#r2 | inter_operator_dispatch |  | 9.0 | 4.9/18.4 | 0.0 |  | 0 |
| react-plan#r2 | mir_operator:AddOp | 7 | 555.0 | 508.8/583.1 | 326.2 | cudaLaunchKernel | 32 |
| react-plan#r2 | mir_operator:RMSNormOp | 8 | 4,246.9 | 4,221.9/4,278.3 | 4,033.5 | cudaEventSynchronize | 224 |
| react-plan#r2 | mir_operator:LinearOp | 10 | 11,331.1 | 11,292.1/11,630.6 | 11,194.4 | cudaEventSynchronize | 32 |
| react-plan#r2 | mir_operator:LinearOp | 11 | 11,425.6 | 11,212.6/11,620.5 | 11,340.1 | cudaEventSynchronize | 32 |
| react-plan#r2 | mir_operator:LinearOp | 12 | 11,315.4 | 11,239.2/11,740.6 | 11,220.3 | cudaEventSynchronize | 32 |
| react-plan#r2 | mir_operator:ViewOp | 13 | 141.7 | 127.5/159.5 | 0.0 | cudaEventRecord | 0 |
| react-plan#r2 | mir_operator:TransposeOp | 14 | 4,128.5 | 4,108.1/4,614.6 | 4,008.8 | cudaEventSynchronize | 32 |
| react-plan#r2 | pre_d2h_alloc |  | 18.0 | 8.9/30.9 | 0.0 |  | 0 |
| react-plan#r2 | d2h_stage |  | 875.2 | 856.6/928.9 | 821.2 | cudaEventSynchronize | 0 |
| react-plan#r2 | checksum_complete |  | 75.2 | 65.3/83.6 | 0.0 | cudaEventDestroy | 0 |
| moa-map0#r2 | adapter_dispatch |  | 817.0 | 747.5/891.0 | 0.0 |  | 0 |
| moa-map0#r2 | token_preprocess_cpu |  | 274.5 | 262.1/391.6 | 0.0 |  | 0 |
| moa-map0#r2 | host_input_generate |  | 112,808.4 | 106,496.0/115,966.9 | 0.0 | cudaEventQuery | 0 |
| moa-map0#r2 | h2d_stage |  | 1,535.9 | 1,476.3/1,884.4 | 1,378.1 | cudaEventSynchronize | 0 |
| moa-map0#r2 | weight_init |  | 185.0 | 139.9/201.5 | 52.0 | cudaLaunchKernel | 2 |
| moa-map0#r2 | mir_operator:RMSNormOp | 6 | 16,076.3 | 16,053.9/16,422.2 | 15,826.5 | cudaEventSynchronize | 224 |
| moa-map0#r2 | inter_operator_dispatch |  | 11.0 | 4.8/29.2 | 0.0 |  | 0 |
| moa-map0#r2 | mir_operator:AddOp | 7 | 700.1 | 687.8/850.8 | 607.5 | cudaEventSynchronize | 32 |
| moa-map0#r2 | mir_operator:RMSNormOp | 8 | 16,087.2 | 16,004.0/16,528.2 | 15,837.7 | cudaEventSynchronize | 224 |
| moa-map0#r2 | mir_operator:LinearOp | 10 | 26,053.8 | 25,696.4/26,453.3 | 25,864.7 | cudaEventSynchronize | 32 |
| moa-map0#r2 | mir_operator:LinearOp | 11 | 26,114.7 | 25,773.3/26,921.1 | 25,981.5 | cudaEventSynchronize | 32 |
| moa-map0#r2 | mir_operator:LinearOp | 12 | 26,753.6 | 26,116.2/27,213.7 | 26,629.8 | cudaEventSynchronize | 32 |
| moa-map0#r2 | mir_operator:ViewOp | 13 | 145.5 | 129.4/166.2 | 0.0 | cudaEventRecord | 0 |
| moa-map0#r2 | mir_operator:TransposeOp | 14 | 7,339.0 | 6,973.1/7,813.2 | 7,222.3 | cudaEventSynchronize | 32 |
| moa-map0#r2 | pre_d2h_alloc |  | 20.3 | 8.6/30.6 | 0.0 |  | 0 |
| moa-map0#r2 | d2h_stage |  | 1,496.4 | 1,476.6/1,577.0 | 1,440.8 | cudaEventSynchronize | 0 |
| moa-map0#r2 | checksum_complete |  | 79.8 | 64.3/87.3 | 0.0 | cudaEventDestroy | 0 |
| moa-map1#r2 | adapter_dispatch |  | 800.2 | 719.1/1,036.6 | 0.0 |  | 0 |
| moa-map1#r2 | token_preprocess_cpu |  | 343.2 | 295.2/384.9 | 0.0 |  | 0 |
| moa-map1#r2 | host_input_generate |  | 112,839.2 | 107,211.9/138,736.2 | 0.0 | cudaEventQuery | 0 |
| moa-map1#r2 | h2d_stage |  | 1,585.2 | 1,525.1/1,680.6 | 1,417.2 | cudaEventSynchronize | 0 |
| moa-map1#r2 | weight_init |  | 193.9 | 138.1/210.6 | 53.0 | cudaLaunchKernel | 2 |
| moa-map1#r2 | mir_operator:RMSNormOp | 6 | 16,114.7 | 16,070.9/16,547.7 | 15,852.9 | cudaEventSynchronize | 224 |
| moa-map1#r2 | inter_operator_dispatch |  | 12.9 | 4.6/27.1 | 0.0 |  | 0 |
| moa-map1#r2 | mir_operator:AddOp | 7 | 710.0 | 685.1/726.4 | 603.4 | cudaEventSynchronize | 32 |
| moa-map1#r2 | mir_operator:RMSNormOp | 8 | 16,366.8 | 15,998.2/16,438.1 | 16,148.9 | cudaEventSynchronize | 224 |
| moa-map1#r2 | mir_operator:LinearOp | 10 | 25,936.6 | 25,696.7/26,112.2 | 25,717.8 | cudaEventSynchronize | 32 |
| moa-map1#r2 | mir_operator:LinearOp | 11 | 26,285.1 | 25,842.0/26,844.4 | 26,123.7 | cudaEventSynchronize | 32 |
| moa-map1#r2 | mir_operator:LinearOp | 12 | 27,033.6 | 25,836.2/27,305.7 | 26,820.4 | cudaEventSynchronize | 32 |
| moa-map1#r2 | mir_operator:ViewOp | 13 | 145.5 | 137.8/169.8 | 0.0 | cudaEventRecord | 0 |
| moa-map1#r2 | mir_operator:TransposeOp | 14 | 7,352.8 | 7,005.6/7,735.7 | 7,222.2 | cudaEventSynchronize | 32 |
| moa-map1#r2 | pre_d2h_alloc |  | 19.2 | 9.0/34.1 | 0.0 |  | 0 |
| moa-map1#r2 | d2h_stage |  | 1,487.8 | 1,467.1/1,569.2 | 1,431.2 | cudaEventSynchronize | 0 |
| moa-map1#r2 | checksum_complete |  | 82.0 | 64.9/102.1 | 0.0 | cudaEventDestroy | 0 |
| moa-map2#r2 | adapter_dispatch |  | 798.7 | 725.0/862.6 | 0.0 |  | 0 |
| moa-map2#r2 | token_preprocess_cpu |  | 283.4 | 253.5/385.2 | 0.0 |  | 0 |
| moa-map2#r2 | host_input_generate |  | 111,502.1 | 107,724.6/139,734.9 | 0.0 | cudaEventQuery | 0 |
| moa-map2#r2 | h2d_stage |  | 1,528.4 | 1,481.0/1,608.1 | 1,381.0 | cudaEventSynchronize | 0 |
| moa-map2#r2 | weight_init |  | 185.5 | 143.8/207.5 | 52.5 | cudaLaunchKernel | 2 |
| moa-map2#r2 | mir_operator:RMSNormOp | 6 | 16,115.6 | 16,057.6/16,503.6 | 15,861.0 | cudaEventSynchronize | 224 |
| moa-map2#r2 | inter_operator_dispatch |  | 11.0 | 5.2/35.6 | 0.0 |  | 0 |
| moa-map2#r2 | mir_operator:AddOp | 7 | 700.3 | 688.8/773.9 | 604.9 | cudaEventSynchronize | 32 |
| moa-map2#r2 | mir_operator:RMSNormOp | 8 | 16,053.4 | 15,999.9/16,784.2 | 15,839.5 | cudaEventSynchronize | 224 |
| moa-map2#r2 | mir_operator:LinearOp | 10 | 26,030.6 | 25,698.9/26,143.3 | 25,824.0 | cudaEventSynchronize | 32 |
| moa-map2#r2 | mir_operator:LinearOp | 11 | 26,618.3 | 25,730.4/26,942.5 | 26,459.1 | cudaEventSynchronize | 32 |
| moa-map2#r2 | mir_operator:LinearOp | 12 | 26,934.0 | 26,151.4/27,587.5 | 26,772.9 | cudaEventSynchronize | 32 |
| moa-map2#r2 | mir_operator:ViewOp | 13 | 154.1 | 139.8/176.2 | 0.0 | cudaEventRecord | 0 |
| moa-map2#r2 | mir_operator:TransposeOp | 14 | 7,343.4 | 7,071.8/7,800.1 | 7,222.1 | cudaEventSynchronize | 32 |
| moa-map2#r2 | pre_d2h_alloc |  | 17.7 | 8.6/35.4 | 0.0 |  | 0 |
| moa-map2#r2 | d2h_stage |  | 1,489.1 | 1,476.0/1,532.2 | 1,436.1 | cudaEventSynchronize | 0 |
| moa-map2#r2 | checksum_complete |  | 81.5 | 63.2/89.1 | 0.0 | cudaEventDestroy | 0 |
| mcts-root#r2 | adapter_dispatch |  | 790.2 | 769.3/2,253.0 | 0.0 |  | 0 |
| mcts-root#r2 | token_preprocess_cpu |  | 302.2 | 271.7/372.7 | 0.0 |  | 0 |
| mcts-root#r2 | host_input_generate |  | 111,311.7 | 109,616.0/135,969.8 | 0.0 | cudaEventQuery | 0 |
| mcts-root#r2 | h2d_stage |  | 1,534.8 | 1,518.1/1,966.6 | 1,406.8 | cudaEventSynchronize | 0 |
| mcts-root#r2 | weight_init |  | 177.5 | 156.5/203.2 | 52.6 | cudaLaunchKernel | 2 |
| mcts-root#r2 | mir_operator:RMSNormOp | 6 | 16,278.6 | 16,091.2/16,476.3 | 16,020.2 | cudaEventSynchronize | 224 |
| mcts-root#r2 | inter_operator_dispatch |  | 12.2 | 5.0/26.9 | 0.0 |  | 0 |
| mcts-root#r2 | mir_operator:AddOp | 7 | 708.5 | 692.2/772.4 | 603.2 | cudaEventSynchronize | 32 |
| mcts-root#r2 | mir_operator:RMSNormOp | 8 | 16,202.9 | 16,002.6/16,504.4 | 15,989.9 | cudaEventSynchronize | 224 |
| mcts-root#r2 | mir_operator:LinearOp | 10 | 26,021.7 | 25,707.4/26,401.8 | 25,831.8 | cudaEventSynchronize | 32 |
| mcts-root#r2 | mir_operator:LinearOp | 11 | 26,106.3 | 25,743.4/26,644.9 | 25,966.4 | cudaEventSynchronize | 32 |
| mcts-root#r2 | mir_operator:LinearOp | 12 | 26,912.0 | 26,180.1/27,365.4 | 26,765.4 | cudaEventSynchronize | 32 |
| mcts-root#r2 | mir_operator:ViewOp | 13 | 151.5 | 141.3/183.1 | 0.0 | cudaEventRecord | 0 |
| mcts-root#r2 | mir_operator:TransposeOp | 14 | 7,385.3 | 7,171.3/7,921.9 | 7,249.0 | cudaEventSynchronize | 32 |
| mcts-root#r2 | pre_d2h_alloc |  | 18.5 | 9.5/35.3 | 0.0 |  | 0 |
| mcts-root#r2 | d2h_stage |  | 1,507.3 | 1,479.5/1,550.3 | 1,454.5 | cudaEventSynchronize | 0 |
| mcts-root#r2 | checksum_complete |  | 80.7 | 66.1/90.7 | 0.0 | cudaEventDestroy | 0 |
| react-tool#r2 | agent_tool_execute_cpu |  | 337.2 | 269.1/359.3 | 0.0 |  | 0 |
| mcts-actor0#r2 | adapter_dispatch |  | 1,297.9 | 1,263.6/1,477.4 | 0.0 |  | 0 |
| mcts-actor0#r2 | token_preprocess_cpu |  | 194.8 | 161.0/252.7 | 0.0 |  | 0 |
| mcts-actor0#r2 | host_input_generate |  | 113,045.1 | 107,939.5/138,257.3 | 0.0 | cudaEventQuery | 0 |
| mcts-actor0#r2 | h2d_stage |  | 1,561.0 | 1,526.3/1,888.1 | 1,387.3 | cudaEventSynchronize | 0 |
| mcts-actor0#r2 | weight_init |  | 190.5 | 168.8/203.8 | 52.8 | cudaLaunchKernel | 2 |
| mcts-actor0#r2 | mir_operator:RMSNormOp | 6 | 16,081.3 | 16,051.8/17,098.1 | 15,829.6 | cudaEventSynchronize | 224 |
| mcts-actor0#r2 | inter_operator_dispatch |  | 12.0 | 5.0/98.5 | 0.0 |  | 0 |
| mcts-actor0#r2 | mir_operator:AddOp | 7 | 718.1 | 690.0/759.2 | 603.9 | cudaEventSynchronize | 32 |
| mcts-actor0#r2 | mir_operator:RMSNormOp | 8 | 16,389.9 | 16,004.7/16,507.7 | 16,155.7 | cudaEventSynchronize | 224 |
| mcts-actor0#r2 | mir_operator:LinearOp | 10 | 26,032.4 | 25,721.9/26,391.6 | 25,831.2 | cudaEventSynchronize | 32 |
| mcts-actor0#r2 | mir_operator:LinearOp | 11 | 26,606.8 | 25,750.1/27,087.5 | 26,461.4 | cudaEventSynchronize | 32 |
| mcts-actor0#r2 | mir_operator:LinearOp | 12 | 27,113.3 | 26,496.4/27,336.3 | 26,927.1 | cudaEventSynchronize | 32 |
| mcts-actor0#r2 | mir_operator:ViewOp | 13 | 150.8 | 137.5/169.2 | 0.0 | cudaEventRecord | 0 |
| mcts-actor0#r2 | mir_operator:TransposeOp | 14 | 7,357.2 | 7,300.0/7,867.5 | 7,223.3 | cudaEventSynchronize | 32 |
| mcts-actor0#r2 | pre_d2h_alloc |  | 20.1 | 12.8/36.3 | 0.0 |  | 0 |
| mcts-actor0#r2 | d2h_stage |  | 1,512.4 | 1,490.4/1,608.6 | 1,456.6 | cudaEventSynchronize | 0 |
| mcts-actor0#r2 | checksum_complete |  | 82.5 | 77.5/91.4 | 0.0 | cudaEventDestroy | 0 |
| mcts-actor1#r2 | adapter_dispatch |  | 763.5 | 721.1/922.2 | 0.0 |  | 0 |
| mcts-actor1#r2 | token_preprocess_cpu |  | 295.5 | 265.8/363.5 | 0.0 |  | 0 |
| mcts-actor1#r2 | host_input_generate |  | 113,163.7 | 110,459.1/117,333.3 | 0.0 | cudaEventQuery | 0 |
| mcts-actor1#r2 | h2d_stage |  | 1,536.6 | 1,523.2/1,640.1 | 1,385.2 | cudaEventSynchronize | 0 |
| mcts-actor1#r2 | weight_init |  | 188.9 | 159.2/210.3 | 53.1 | cudaLaunchKernel | 2 |
| mcts-actor1#r2 | mir_operator:RMSNormOp | 6 | 16,095.8 | 16,048.9/16,548.0 | 15,850.8 | cudaEventSynchronize | 224 |
| mcts-actor1#r2 | inter_operator_dispatch |  | 11.9 | 5.0/31.9 | 0.0 |  | 0 |
| mcts-actor1#r2 | mir_operator:AddOp | 7 | 704.0 | 682.8/831.3 | 612.1 | cudaEventSynchronize | 32 |
| mcts-actor1#r2 | mir_operator:RMSNormOp | 8 | 16,079.5 | 15,997.9/16,511.0 | 15,816.6 | cudaEventSynchronize | 224 |
| mcts-actor1#r2 | mir_operator:LinearOp | 10 | 26,207.5 | 25,688.1/26,421.7 | 26,025.2 | cudaEventSynchronize | 32 |
| mcts-actor1#r2 | mir_operator:LinearOp | 11 | 26,248.8 | 25,798.8/26,859.7 | 26,093.2 | cudaEventSynchronize | 32 |
| mcts-actor1#r2 | mir_operator:LinearOp | 12 | 26,895.5 | 26,162.9/27,631.2 | 26,739.4 | cudaEventSynchronize | 32 |
| mcts-actor1#r2 | mir_operator:ViewOp | 13 | 155.5 | 129.8/182.1 | 0.0 | cudaEventRecord | 0 |
| mcts-actor1#r2 | mir_operator:TransposeOp | 14 | 7,352.6 | 7,003.1/7,815.5 | 7,221.4 | cudaEventSynchronize | 32 |
| mcts-actor1#r2 | pre_d2h_alloc |  | 23.6 | 10.5/36.2 | 0.0 |  | 0 |
| mcts-actor1#r2 | d2h_stage |  | 1,550.5 | 1,475.4/1,706.8 | 1,494.0 | cudaEventSynchronize | 0 |
| mcts-actor1#r2 | checksum_complete |  | 85.3 | 70.5/106.2 | 0.0 | cudaEventDestroy | 0 |
| moa-reduce#r2 | adapter_dispatch |  | 805.4 | 742.9/905.0 | 0.0 |  | 0 |
| moa-reduce#r2 | token_preprocess_cpu |  | 313.3 | 268.8/371.4 | 0.0 |  | 0 |
| moa-reduce#r2 | host_input_generate |  | 112,494.7 | 107,760.3/115,100.7 | 0.0 | cudaEventQuery | 0 |
| moa-reduce#r2 | h2d_stage |  | 1,535.9 | 1,483.6/1,579.0 | 1,388.7 | cudaEventSynchronize | 0 |
| moa-reduce#r2 | weight_init |  | 190.7 | 159.9/198.6 | 52.6 | cudaLaunchKernel | 2 |
| moa-reduce#r2 | mir_operator:RMSNormOp | 6 | 16,090.0 | 16,046.4/16,492.1 | 15,837.3 | cudaEventSynchronize | 224 |
| moa-reduce#r2 | inter_operator_dispatch |  | 12.8 | 4.9/42.3 | 0.0 |  | 0 |
| moa-reduce#r2 | mir_operator:AddOp | 7 | 701.6 | 685.5/744.9 | 604.6 | cudaEventSynchronize | 32 |
| moa-reduce#r2 | mir_operator:RMSNormOp | 8 | 16,311.9 | 15,999.7/16,497.2 | 16,099.7 | cudaEventSynchronize | 224 |
| moa-reduce#r2 | mir_operator:LinearOp | 10 | 26,058.9 | 25,771.0/26,403.6 | 25,849.6 | cudaEventSynchronize | 32 |
| moa-reduce#r2 | mir_operator:LinearOp | 11 | 26,449.7 | 25,768.3/27,033.7 | 26,267.9 | cudaEventSynchronize | 32 |
| moa-reduce#r2 | mir_operator:LinearOp | 12 | 27,083.0 | 26,750.1/27,410.2 | 26,943.4 | cudaEventSynchronize | 32 |
| moa-reduce#r2 | mir_operator:ViewOp | 13 | 169.2 | 143.0/393.8 | 0.0 | cudaEventRecord | 0 |
| moa-reduce#r2 | mir_operator:TransposeOp | 14 | 7,357.4 | 7,266.7/7,824.1 | 7,227.5 | cudaEventSynchronize | 32 |
| moa-reduce#r2 | pre_d2h_alloc |  | 20.9 | 9.2/50.7 | 0.0 |  | 0 |
| moa-reduce#r2 | d2h_stage |  | 1,511.0 | 1,473.3/1,619.8 | 1,449.9 | cudaEventSynchronize | 0 |
| moa-reduce#r2 | checksum_complete |  | 82.6 | 66.9/119.7 | 0.0 | cudaEventDestroy | 0 |
| react-answer#r2 | adapter_dispatch |  | 751.0 | 681.3/847.8 | 0.0 |  | 0 |
| react-answer#r2 | token_preprocess_cpu |  | 352.0 | 229.9/365.3 | 0.0 |  | 0 |
| react-answer#r2 | host_input_generate |  | 87,256.1 | 83,748.5/90,718.1 | 0.0 | cudaEventQuery | 0 |
| react-answer#r2 | h2d_stage |  | 1,205.6 | 1,141.6/1,309.7 | 1,054.7 | cudaEventSynchronize | 0 |
| react-answer#r2 | weight_init |  | 182.6 | 148.5/209.4 | 39.8 | cudaLaunchKernel | 2 |
| react-answer#r2 | mir_operator:RMSNormOp | 6 | 9,478.4 | 9,428.2/9,903.6 | 9,226.5 | cudaEventSynchronize | 224 |
| react-answer#r2 | inter_operator_dispatch |  | 11.4 | 4.7/23.9 | 0.0 |  | 0 |
| react-answer#r2 | mir_operator:AddOp | 7 | 567.1 | 518.1/602.6 | 432.5 | cudaLaunchKernel | 32 |
| react-answer#r2 | mir_operator:RMSNormOp | 8 | 9,426.0 | 9,320.8/9,816.4 | 9,201.7 | cudaEventSynchronize | 224 |
| react-answer#r2 | mir_operator:LinearOp | 10 | 19,984.3 | 19,670.7/20,109.4 | 19,821.9 | cudaEventSynchronize | 32 |
| react-answer#r2 | mir_operator:LinearOp | 11 | 19,891.7 | 19,664.5/20,400.3 | 19,788.7 | cudaEventSynchronize | 32 |
| react-answer#r2 | mir_operator:LinearOp | 12 | 20,100.8 | 19,747.7/21,008.7 | 20,007.8 | cudaEventSynchronize | 32 |
| react-answer#r2 | mir_operator:ViewOp | 13 | 148.4 | 139.1/158.0 | 0.0 | cudaEventRecord | 0 |
| react-answer#r2 | mir_operator:TransposeOp | 14 | 5,874.1 | 5,466.3/5,950.3 | 5,761.0 | cudaEventSynchronize | 32 |
| react-answer#r2 | pre_d2h_alloc |  | 20.3 | 12.1/40.2 | 0.0 |  | 0 |
| react-answer#r2 | d2h_stage |  | 1,169.2 | 1,137.7/1,199.7 | 1,111.4 | cudaEventSynchronize | 0 |
| react-answer#r2 | checksum_complete |  | 81.5 | 78.1/95.9 | 0.0 | cudaEventDestroy | 0 |
| mcts-critic#r2 | adapter_dispatch |  | 817.0 | 749.0/846.1 | 0.0 |  | 0 |
| mcts-critic#r2 | token_preprocess_cpu |  | 324.6 | 275.6/363.0 | 0.0 |  | 0 |
| mcts-critic#r2 | host_input_generate |  | 111,374.6 | 108,872.6/113,131.5 | 0.0 | cudaEventQuery | 0 |
| mcts-critic#r2 | h2d_stage |  | 1,532.3 | 1,488.6/1,672.2 | 1,381.6 | cudaEventSynchronize | 0 |
| mcts-critic#r2 | weight_init |  | 188.9 | 144.0/201.5 | 52.0 | cudaLaunchKernel | 2 |
| mcts-critic#r2 | mir_operator:RMSNormOp | 6 | 16,479.0 | 16,058.5/16,527.9 | 16,204.2 | cudaEventSynchronize | 224 |
| mcts-critic#r2 | inter_operator_dispatch |  | 12.5 | 4.9/31.0 | 0.0 |  | 0 |
| mcts-critic#r2 | mir_operator:AddOp | 7 | 713.1 | 692.2/822.9 | 605.4 | cudaEventSynchronize | 32 |
| mcts-critic#r2 | mir_operator:RMSNormOp | 8 | 16,028.5 | 16,000.9/16,452.4 | 15,807.4 | cudaEventSynchronize | 224 |
| mcts-critic#r2 | mir_operator:LinearOp | 10 | 26,076.4 | 25,695.2/26,401.8 | 25,874.0 | cudaEventSynchronize | 32 |
| mcts-critic#r2 | mir_operator:LinearOp | 11 | 26,143.6 | 25,767.8/26,934.3 | 25,981.8 | cudaEventSynchronize | 32 |
| mcts-critic#r2 | mir_operator:LinearOp | 12 | 26,947.1 | 25,790.8/27,482.0 | 26,802.5 | cudaEventSynchronize | 32 |
| mcts-critic#r2 | mir_operator:ViewOp | 13 | 156.9 | 145.5/204.0 | 0.0 | cudaEventRecord | 0 |
| mcts-critic#r2 | mir_operator:TransposeOp | 14 | 7,411.4 | 6,919.2/7,812.9 | 7,281.3 | cudaEventSynchronize | 32 |
| mcts-critic#r2 | pre_d2h_alloc |  | 22.2 | 12.4/39.2 | 0.0 |  | 0 |
| mcts-critic#r2 | d2h_stage |  | 1,491.7 | 1,472.2/1,588.7 | 1,435.9 | cudaEventSynchronize | 0 |
| mcts-critic#r2 | checksum_complete |  | 81.4 | 72.4/91.0 | 0.0 | cudaEventDestroy | 0 |
| <dag> | dag_schedule_gap |  | 41.6 | 7.9/1,788.2 | 0.0 |  | 0 |
| <dag> | iteration_tail_sync |  | 78.9 | 49.1/108.6 | 0.0 | cudaDeviceSynchronize | 0 |

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

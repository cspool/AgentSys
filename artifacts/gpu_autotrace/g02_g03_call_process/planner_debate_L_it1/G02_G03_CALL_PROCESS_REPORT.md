# G02/G03 call-wise process attribution: `planner_debate_L_it1`

Lineage `h22-gpu-autotrace`, workflow w02. Consumes the w01 trace only; no re-timing.
Host events aligned to the nsys clock by a constant offset fitted on 320 operator pairs (spread 38.6 us).

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
| host_input_generate | 40 | 4,109,523.7 | 91.9 % | 102,738.1 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:LinearOp | 120 | 103,267.7 | 2.31 % | 860.6 | 92,129.7 | 37.75 % | 89.7 % | 89.2 % |
| h2d_stage | 40 | 59,005.0 | 1.32 % | 1,475.1 | 51,962.0 | 21.29 % | 91.2 % | 88.1 % |
| d2h_stage | 40 | 56,611.6 | 1.27 % | 1,415.3 | 54,593.0 | 22.37 % | 97.1 % | 96.4 % |
| mir_operator:RMSNormOp | 80 | 41,747.5 | 0.93 % | 521.8 | 34,152.1 | 13.99 % | 65.0 % | 81.8 % |
| adapter_dispatch | 40 | 41,266.0 | 0.92 % | 1,031.6 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| token_preprocess_cpu | 40 | 14,175.8 | 0.32 % | 354.4 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:TransposeOp | 40 | 12,047.3 | 0.27 % | 301.2 | 8,278.0 | 3.39 % | 68.4 % | 68.7 % |
| dag_schedule_gap | 48 | 9,334.0 | 0.21 % | 194.5 | 0.0 | 0.0 % | 1.7 % | 0.0 % |
| weight_init | 40 | 8,733.0 | 0.2 % | 218.3 | 2,026.2 | 0.83 % | 22.9 % | 23.2 % |
| mir_operator:AddOp | 40 | 3,823.6 | 0.09 % | 95.6 | 909.0 | 0.37 % | 30.4 % | 23.8 % |
| checksum_complete | 40 | 3,371.7 | 0.08 % | 84.3 | 0.0 | 0.0 % | 2.5 % | 0.0 % |
| agent_tool_execute_cpu | 8 | 2,859.6 | 0.06 % | 357.4 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:ViewOp | 40 | 2,771.5 | 0.06 % | 69.3 | 0.0 | 0.0 % | 19.4 % | 0.0 % |
| inter_operator_dispatch | 280 | 2,258.7 | 0.05 % | 8.1 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| pre_d2h_alloc | 40 | 611.5 | 0.01 % | 15.3 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| iteration_tail_sync | 8 | 561.0 | 0.01 % | 70.1 | 0.0 | 0.0 % | 18.7 % | 0.0 % |

## Call breakdown (agent nodes)

| call | kind | wave | matrix | host per iter (us) | host share | GPU per iter (us) | GPU share | GPU/host |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| planner-seed | llm | 0 | 3584 | 94,093.5 | 16.83 % | 5,015.4 | 16.44 % | 5.33 % |
| critic-a | llm | 0 | 4096 | 122,445.2 | 21.9 % | 6,780.0 | 22.22 % | 5.54 % |
| critic-b | llm | 0 | 4096 | 123,509.0 | 22.09 % | 6,830.7 | 22.39 % | 5.53 % |
| planner-tool | tool | 1 | 256 | 357.4 | 0.06 % | 0.0 | 0.0 % | 0.0 % |
| critic-merge | llm | 1 | 4096 | 123,412.8 | 22.08 % | 6,832.8 | 22.4 % | 5.54 % |
| planner-final | llm | 2 | 3584 | 93,941.4 | 16.81 % | 5,047.3 | 16.55 % | 5.37 % |
| <dag> | dag |  |  | 1,236.9 | 0.22 % | 0.0 | 0.0 % | 0.0 % |

## CUDA runtime API inside the measured window

| API | calls | total (us) | share of wall |
|---|---:|---:|---:|
| cudaEventSynchronize | 400 | 224,794.9 | 5.03 % |
| cudaLaunchKernel | 792 | 6,723.1 | 0.15 % |
| cudaEventRecord | 880 | 3,713.5 | 0.08 % |
| cudaMemcpyAsync | 80 | 1,781.7 | 0.04 % |
| cudaEventCreateWithFlags | 800 | 1,693.0 | 0.04 % |
| cudaEventDestroy | 800 | 829.4 | 0.02 % |
| cudaMemsetAsync | 72 | 608.9 | 0.01 % |
| cudaEventQuery | 80 | 399.5 | 0.01 % |
| cuLaunchKernel | 48 | 378.7 | 0.01 % |
| cudaStreamIsCapturing | 120 | 120.4 | 0.0 % |
| cuKernelGetFunction | 48 | 105.5 | 0.0 % |
| cudaDeviceSynchronize | 8 | 67.3 | 0.0 % |

## Kernel families by process (G03)

| process | family | instances | GPU total (us) | share |
|---|---|---:|---:|---:|
| mir_operator:LinearOp | gemm | 120 | 92,067.7 | 37.72 % |
| d2h_stage | memcpy | 40 | 54,593.0 | 22.37 % |
| h2d_stage | memcpy | 40 | 51,962.0 | 21.29 % |
| mir_operator:RMSNormOp | copy | 160 | 13,273.5 | 5.44 % |
| mir_operator:RMSNormOp | elementwise_unary | 160 | 9,358.7 | 3.83 % |
| mir_operator:RMSNormOp | elementwise_binary | 160 | 9,069.0 | 3.72 % |
| mir_operator:TransposeOp | copy | 40 | 8,278.0 | 3.39 % |
| mir_operator:RMSNormOp | reduce | 80 | 2,450.8 | 1.0 % |
| weight_init | rng_init | 40 | 1,311.1 | 0.54 % |
| mir_operator:AddOp | elementwise_binary | 40 | 909.0 | 0.37 % |
| weight_init | elementwise_binary | 40 | 715.2 | 0.29 % |
| mir_operator:LinearOp | memset | 72 | 62.0 | 0.03 % |

## Kernel launch order, representative iteration 7 (G03)

| # | call | process | kind | family | GPU (us) | launch latency (us) | grid | block |
|---:|---|---|---|---|---:|---:|---|---|
| 1 | planner-seed | h2d_stage | memcpy | memcpy | 1,043.9 | 26.6 | 0x0x0 | 0x0x0 |
| 2 | planner-seed | weight_init | kernel | rng_init | 28.1 | 97.0 | 768x1x1 | 256x1x1 |
| 3 | planner-seed | weight_init | kernel | elementwise_binary | 14.8 | 49.3 | 12544x1x1 | 128x1x1 |
| 4 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 85.1 | 9.0 | 12544x1x1 | 128x1x1 |
| 5 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 70.7 | 67.8 | 12544x1x1 | 128x1x1 |
| 6 | planner-seed | mir_operator:RMSNormOp:6 | kernel | reduce | 21.1 | 113.5 | 224x1x1 | 32x16x1 |
| 7 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 111.4 | 4x1x1 | 128x1x1 |
| 8 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.1 | 93.6 | 4x1x1 | 128x1x1 |
| 9 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 88.1 | 73.3 | 50176x1x1 | 128x1x1 |
| 10 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 54.9 | 135.2 | 12544x1x1 | 128x1x1 |
| 11 | planner-seed | mir_operator:AddOp:7 | kernel | elementwise_binary | 14.7 | 7.9 | 12544x1x1 | 128x1x1 |
| 12 | planner-seed | mir_operator:RMSNormOp:8 | kernel | copy | 52.7 | 7.4 | 12544x1x1 | 128x1x1 |
| 13 | planner-seed | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 70.6 | 43.0 | 12544x1x1 | 128x1x1 |
| 14 | planner-seed | mir_operator:RMSNormOp:8 | kernel | reduce | 22.4 | 94.0 | 224x1x1 | 32x16x1 |
| 15 | planner-seed | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 1.2 | 102.4 | 4x1x1 | 128x1x1 |
| 16 | planner-seed | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 1.1 | 91.1 | 4x1x1 | 128x1x1 |
| 17 | planner-seed | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 88.1 | 78.3 | 50176x1x1 | 128x1x1 |
| 18 | planner-seed | mir_operator:RMSNormOp:8 | kernel | copy | 55.0 | 151.3 | 12544x1x1 | 128x1x1 |
| 19 | planner-seed | mir_operator:LinearOp:10 | kernel | gemm | 636.4 | 8.5 | 448x7x1 | 128x1x1 |
| 20 | planner-seed | mir_operator:LinearOp:11 | kernel | gemm | 635.9 | 6.8 | 448x7x1 | 128x1x1 |
| 21 | planner-seed | mir_operator:LinearOp:12 | kernel | gemm | 635.7 | 6.7 | 448x7x1 | 128x1x1 |
| 22 | planner-seed | mir_operator:TransposeOp:14 | kernel | copy | 177.9 | 17.1 | 25088x1x1 | 128x1x1 |
| 23 | planner-seed | d2h_stage | memcpy | memcpy | 1,110.6 | 19.2 | 0x0x0 | 0x0x0 |
| 24 | critic-a | h2d_stage | memcpy | memcpy | 1,375.0 | 26.3 | 0x0x0 | 0x0x0 |
| 25 | critic-a | weight_init | kernel | rng_init | 36.2 | 96.6 | 768x1x1 | 256x1x1 |
| 26 | critic-a | weight_init | kernel | elementwise_binary | 19.9 | 47.0 | 16384x1x1 | 128x1x1 |
| 27 | critic-a | mir_operator:RMSNormOp:6 | kernel | copy | 114.2 | 10.4 | 16384x1x1 | 128x1x1 |
| 28 | critic-a | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 145.8 | 97.4 | 16384x1x1 | 128x1x1 |
| 29 | critic-a | mir_operator:RMSNormOp:6 | kernel | reduce | 36.6 | 213.8 | 256x1x1 | 32x16x1 |
| 30 | critic-a | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.4 | 226.3 | 4x1x1 | 128x1x1 |
| 31 | critic-a | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.1 | 208.4 | 4x1x1 | 128x1x1 |
| 32 | critic-a | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 128.2 | 188.7 | 65536x1x1 | 128x1x1 |
| 33 | critic-a | mir_operator:RMSNormOp:6 | kernel | copy | 90.6 | 296.4 | 16384x1x1 | 128x1x1 |
| 34 | critic-a | mir_operator:AddOp:7 | kernel | elementwise_binary | 27.0 | 19.6 | 16384x1x1 | 128x1x1 |
| 35 | critic-a | mir_operator:RMSNormOp:8 | kernel | copy | 86.9 | 7.7 | 16384x1x1 | 128x1x1 |
| 36 | critic-a | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 145.1 | 72.0 | 16384x1x1 | 128x1x1 |
| 37 | critic-a | mir_operator:RMSNormOp:8 | kernel | reduce | 36.8 | 199.8 | 256x1x1 | 32x16x1 |
| 38 | critic-a | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 1.2 | 223.1 | 4x1x1 | 128x1x1 |
| 39 | critic-a | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 1.1 | 211.3 | 4x1x1 | 128x1x1 |
| 40 | critic-a | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 128.5 | 198.1 | 65536x1x1 | 128x1x1 |
| 41 | critic-a | mir_operator:RMSNormOp:8 | kernel | copy | 91.4 | 300.7 | 16384x1x1 | 128x1x1 |
| 42 | critic-a | mir_operator:LinearOp:10 | memset | memset | 0.9 | 15.2 | 0x0x0 | 0x0x0 |
| 43 | critic-a | mir_operator:LinearOp:10 | kernel | gemm | 851.0 | 9.1 | 32x32x3 | 128x1x1 |
| 44 | critic-a | mir_operator:LinearOp:11 | memset | memset | 0.9 | 6.2 | 0x0x0 | 0x0x0 |
| 45 | critic-a | mir_operator:LinearOp:11 | kernel | gemm | 850.8 | 6.9 | 32x32x3 | 128x1x1 |
| 46 | critic-a | mir_operator:LinearOp:12 | memset | memset | 0.9 | 5.4 | 0x0x0 | 0x0x0 |
| 47 | critic-a | mir_operator:LinearOp:12 | kernel | gemm | 850.8 | 6.8 | 32x32x3 | 128x1x1 |
| 48 | critic-a | mir_operator:TransposeOp:14 | kernel | copy | 226.5 | 9.3 | 32768x1x1 | 128x1x1 |
| 49 | critic-a | d2h_stage | memcpy | memcpy | 1,486.7 | 14.2 | 0x0x0 | 0x0x0 |
| 50 | critic-b | h2d_stage | memcpy | memcpy | 1,446.8 | 25.0 | 0x0x0 | 0x0x0 |
| 51 | critic-b | weight_init | kernel | rng_init | 35.7 | 95.6 | 768x1x1 | 256x1x1 |
| 52 | critic-b | weight_init | kernel | elementwise_binary | 20.0 | 42.6 | 16384x1x1 | 128x1x1 |
| 53 | critic-b | mir_operator:RMSNormOp:6 | kernel | copy | 112.0 | 10.4 | 16384x1x1 | 128x1x1 |
| 54 | critic-b | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 147.9 | 93.5 | 16384x1x1 | 128x1x1 |
| 55 | critic-b | mir_operator:RMSNormOp:6 | kernel | reduce | 37.5 | 214.2 | 256x1x1 | 32x16x1 |
| 56 | critic-b | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.3 | 227.4 | 4x1x1 | 128x1x1 |
| 57 | critic-b | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.1 | 209.9 | 4x1x1 | 128x1x1 |
| 58 | critic-b | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 127.7 | 187.8 | 65536x1x1 | 128x1x1 |
| 59 | critic-b | mir_operator:RMSNormOp:6 | kernel | copy | 90.5 | 290.0 | 16384x1x1 | 128x1x1 |
| 60 | critic-b | mir_operator:AddOp:7 | kernel | elementwise_binary | 27.2 | 8.4 | 16384x1x1 | 128x1x1 |
| … | | 64 more rows in kernel_launch_order_representative_iteration.csv | | | | | | |

## Per call/process summary (medians over measured iterations)

| call | process | op | host median (us) | host min/max (us) | GPU median (us) | top CUDA API | kernels |
|---|---|---:|---:|---:|---:|---|---:|
| planner-seed | adapter_dispatch |  | 917.9 | 858.8/1,169.9 | 0.0 |  | 0 |
| planner-seed | token_preprocess_cpu |  | 377.1 | 328.6/396.4 | 0.0 |  | 0 |
| planner-seed | host_input_generate |  | 85,546.3 | 83,590.7/91,617.9 | 0.0 | cudaEventQuery | 0 |
| planner-seed | h2d_stage |  | 1,263.4 | 1,200.3/1,649.5 | 1,090.0 | cudaEventSynchronize | 0 |
| planner-seed | weight_init |  | 200.9 | 183.9/346.6 | 43.0 | cudaLaunchKernel | 2 |
| planner-seed | mir_operator:RMSNormOp | 6 | 434.6 | 424.5/490.6 | 321.4 | cudaEventSynchronize | 7 |
| planner-seed | inter_operator_dispatch |  | 6.7 | 4.7/21.3 | 0.0 |  | 0 |
| planner-seed | mir_operator:AddOp | 7 | 83.1 | 79.7/93.8 | 14.8 | cudaLaunchKernel | 1 |
| planner-seed | mir_operator:RMSNormOp | 8 | 357.2 | 352.6/388.1 | 290.5 | cudaEventSynchronize | 7 |
| planner-seed | mir_operator:LinearOp | 10 | 761.5 | 751.2/774.9 | 635.8 | cudaEventSynchronize | 1 |
| planner-seed | mir_operator:LinearOp | 11 | 701.5 | 696.2/708.4 | 635.1 | cudaEventSynchronize | 1 |
| planner-seed | mir_operator:LinearOp | 12 | 698.4 | 694.0/702.9 | 634.9 | cudaEventSynchronize | 1 |
| planner-seed | mir_operator:ViewOp | 13 | 63.2 | 60.9/72.4 | 0.0 | cudaEventRecord | 0 |
| planner-seed | mir_operator:TransposeOp | 14 | 264.5 | 259.4/277.4 | 177.7 | cudaEventSynchronize | 1 |
| planner-seed | pre_d2h_alloc |  | 15.0 | 12.0/16.4 | 0.0 |  | 0 |
| planner-seed | d2h_stage |  | 1,170.1 | 1,152.8/1,189.7 | 1,118.5 | cudaEventSynchronize | 0 |
| planner-seed | checksum_complete |  | 77.6 | 70.8/90.6 | 0.0 | cudaEventDestroy | 0 |
| critic-a | adapter_dispatch |  | 896.1 | 838.4/939.9 | 0.0 |  | 0 |
| critic-a | token_preprocess_cpu |  | 395.3 | 362.1/466.6 | 0.0 |  | 0 |
| critic-a | host_input_generate |  | 113,567.7 | 108,124.4/117,215.3 | 0.0 | cudaEventQuery | 0 |
| critic-a | h2d_stage |  | 1,575.9 | 1,516.0/1,615.6 | 1,406.7 | cudaEventSynchronize | 0 |
| critic-a | weight_init |  | 204.5 | 181.8/268.1 | 55.9 | cudaLaunchKernel | 2 |
| critic-a | mir_operator:RMSNormOp | 6 | 632.7 | 619.4/646.7 | 517.7 | cudaEventSynchronize | 7 |
| critic-a | inter_operator_dispatch |  | 6.8 | 4.7/20.3 | 0.0 |  | 0 |
| critic-a | mir_operator:AddOp | 7 | 93.3 | 86.8/106.6 | 27.1 | cudaEventSynchronize | 1 |
| critic-a | mir_operator:RMSNormOp | 8 | 559.8 | 555.6/562.5 | 490.7 | cudaEventSynchronize | 7 |
| critic-a | mir_operator:LinearOp | 10 | 983.9 | 977.5/990.5 | 852.8 | cudaEventSynchronize | 1 |
| critic-a | mir_operator:LinearOp | 11 | 925.4 | 922.5/935.9 | 852.8 | cudaEventSynchronize | 1 |
| critic-a | mir_operator:LinearOp | 12 | 922.6 | 917.0/979.5 | 852.4 | cudaEventSynchronize | 1 |
| critic-a | mir_operator:ViewOp | 13 | 67.3 | 62.5/69.2 | 0.0 | cudaEventRecord | 0 |
| critic-a | mir_operator:TransposeOp | 14 | 317.2 | 307.4/324.9 | 226.5 | cudaEventSynchronize | 1 |
| critic-a | pre_d2h_alloc |  | 15.3 | 11.8/16.8 | 0.0 |  | 0 |
| critic-a | d2h_stage |  | 1,526.2 | 1,506.7/1,585.9 | 1,479.4 | cudaEventSynchronize | 0 |
| critic-a | checksum_complete |  | 81.4 | 67.9/124.8 | 0.0 | cudaEventDestroy | 0 |
| critic-b | adapter_dispatch |  | 919.0 | 825.0/1,245.4 | 0.0 |  | 0 |
| critic-b | token_preprocess_cpu |  | 384.4 | 295.5/487.7 | 0.0 |  | 0 |
| critic-b | host_input_generate |  | 113,021.5 | 109,265.7/117,918.7 | 0.0 | cudaEventQuery | 0 |
| critic-b | h2d_stage |  | 1,591.8 | 1,513.3/1,807.7 | 1,415.4 | cudaEventSynchronize | 0 |
| critic-b | weight_init |  | 214.5 | 189.1/455.2 | 55.6 | cudaLaunchKernel | 2 |
| critic-b | mir_operator:RMSNormOp | 6 | 642.1 | 627.8/744.9 | 517.8 | cudaEventSynchronize | 7 |
| critic-b | inter_operator_dispatch |  | 7.1 | 5.0/23.0 | 0.0 |  | 0 |
| critic-b | mir_operator:AddOp | 7 | 96.6 | 90.6/110.0 | 26.9 | cudaLaunchKernel | 1 |
| critic-b | mir_operator:RMSNormOp | 8 | 560.4 | 552.6/577.7 | 490.8 | cudaEventSynchronize | 7 |
| critic-b | mir_operator:LinearOp | 10 | 994.3 | 984.1/1,040.0 | 852.6 | cudaEventSynchronize | 1 |
| critic-b | mir_operator:LinearOp | 11 | 931.4 | 925.6/968.3 | 852.3 | cudaEventSynchronize | 1 |
| critic-b | mir_operator:LinearOp | 12 | 922.6 | 917.7/926.3 | 852.0 | cudaEventSynchronize | 1 |
| critic-b | mir_operator:ViewOp | 13 | 69.4 | 61.6/87.8 | 0.0 | cudaEventRecord | 0 |
| critic-b | mir_operator:TransposeOp | 14 | 318.9 | 312.4/358.1 | 226.6 | cudaEventSynchronize | 1 |
| critic-b | pre_d2h_alloc |  | 16.2 | 14.2/19.3 | 0.0 |  | 0 |
| critic-b | d2h_stage |  | 1,542.9 | 1,513.5/1,733.1 | 1,490.8 | cudaEventSynchronize | 0 |
| critic-b | checksum_complete |  | 86.2 | 77.8/130.1 | 0.0 | cudaEventDestroy | 0 |
| planner-tool | agent_tool_execute_cpu |  | 364.6 | 310.6/407.9 | 0.0 |  | 0 |
| critic-merge | adapter_dispatch |  | 1,444.7 | 1,419.8/1,467.3 | 0.0 |  | 0 |
| critic-merge | token_preprocess_cpu |  | 242.4 | 233.7/272.3 | 0.0 |  | 0 |
| critic-merge | host_input_generate |  | 113,184.3 | 110,844.9/120,190.7 | 0.0 | cudaEventQuery | 0 |
| critic-merge | h2d_stage |  | 1,584.9 | 1,552.6/1,645.8 | 1,418.6 | cudaEventSynchronize | 0 |
| critic-merge | weight_init |  | 214.5 | 193.8/267.8 | 55.7 | cudaLaunchKernel | 2 |
| critic-merge | mir_operator:RMSNormOp | 6 | 642.8 | 628.2/739.7 | 518.1 | cudaEventSynchronize | 7 |
| critic-merge | inter_operator_dispatch |  | 7.5 | 5.2/23.5 | 0.0 |  | 0 |
| critic-merge | mir_operator:AddOp | 7 | 94.9 | 91.2/254.7 | 27.1 | cudaLaunchKernel | 1 |
| critic-merge | mir_operator:RMSNormOp | 8 | 562.5 | 557.1/575.0 | 491.4 | cudaEventSynchronize | 7 |
| critic-merge | mir_operator:LinearOp | 10 | 987.8 | 979.1/1,005.4 | 853.0 | cudaEventSynchronize | 1 |
| critic-merge | mir_operator:LinearOp | 11 | 929.2 | 927.6/932.7 | 852.1 | cudaEventSynchronize | 1 |
| critic-merge | mir_operator:LinearOp | 12 | 924.5 | 923.0/1,046.0 | 852.1 | cudaEventSynchronize | 1 |
| critic-merge | mir_operator:ViewOp | 13 | 68.1 | 65.6/142.4 | 0.0 | cudaEventSynchronize | 0 |
| critic-merge | mir_operator:TransposeOp | 14 | 319.7 | 312.2/329.5 | 226.4 | cudaEventSynchronize | 1 |
| critic-merge | pre_d2h_alloc |  | 15.4 | 13.7/18.2 | 0.0 |  | 0 |
| critic-merge | d2h_stage |  | 1,537.1 | 1,512.0/1,628.0 | 1,483.1 | cudaEventSynchronize | 0 |
| critic-merge | checksum_complete |  | 83.5 | 81.1/91.7 | 0.0 | cudaEventDestroy | 0 |
| planner-final | adapter_dispatch |  | 924.9 | 874.2/971.2 | 0.0 |  | 0 |
| planner-final | token_preprocess_cpu |  | 370.3 | 303.7/414.6 | 0.0 |  | 0 |
| planner-final | host_input_generate |  | 86,389.7 | 84,731.7/87,895.7 | 0.0 | cudaEventQuery | 0 |
| planner-final | h2d_stage |  | 1,265.8 | 1,209.6/1,309.9 | 1,106.8 | cudaEventSynchronize | 0 |
| planner-final | weight_init |  | 203.6 | 196.5/220.2 | 43.2 | cudaLaunchKernel | 2 |
| planner-final | mir_operator:RMSNormOp | 6 | 435.1 | 426.0/453.7 | 320.0 | cudaEventSynchronize | 7 |
| planner-final | inter_operator_dispatch |  | 7.0 | 4.3/12.3 | 0.0 |  | 0 |
| planner-final | mir_operator:AddOp | 7 | 87.1 | 79.8/96.8 | 14.8 | cudaLaunchKernel | 1 |
| planner-final | mir_operator:RMSNormOp | 8 | 357.3 | 351.7/360.9 | 291.1 | cudaEventSynchronize | 7 |
| planner-final | mir_operator:LinearOp | 10 | 769.1 | 759.6/813.3 | 636.2 | cudaEventSynchronize | 1 |
| planner-final | mir_operator:LinearOp | 11 | 705.7 | 701.3/714.6 | 633.2 | cudaEventSynchronize | 1 |
| planner-final | mir_operator:LinearOp | 12 | 703.0 | 694.2/707.5 | 635.8 | cudaEventSynchronize | 1 |
| planner-final | mir_operator:ViewOp | 13 | 64.6 | 59.6/90.4 | 0.0 | cudaEventRecord | 0 |
| planner-final | mir_operator:TransposeOp | 14 | 266.9 | 263.7/366.0 | 177.6 | cudaEventSynchronize | 1 |
| planner-final | pre_d2h_alloc |  | 15.0 | 13.0/16.0 | 0.0 |  | 0 |
| planner-final | d2h_stage |  | 1,187.8 | 1,162.6/1,443.4 | 1,139.5 | cudaEventSynchronize | 0 |
| planner-final | checksum_complete |  | 81.1 | 77.3/91.9 | 0.0 | cudaEventDestroy | 0 |
| <dag> | dag_schedule_gap |  | 39.9 | 13.2/1,012.8 | 0.0 |  | 0 |
| <dag> | iteration_tail_sync |  | 63.4 | 54.0/100.3 | 0.0 | cudaDeviceSynchronize | 0 |

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

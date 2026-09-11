# G02/G03 call-wise process attribution: `react_tool_L`

Lineage `h22-gpu-autotrace`, workflow w02. Consumes the w01 trace only; no re-timing.
Host events aligned to the nsys clock by a constant offset fitted on 128 operator pairs (spread 12.9 us).

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
| host_input_generate | 16 | 1,075,201.4 | 56.13 % | 67,200.1 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:LinearOp | 48 | 549,072.3 | 28.66 % | 11,439.0 | 543,095.3 | 70.32 % | 95.0 % | 98.9 % |
| mir_operator:RMSNormOp | 32 | 140,118.3 | 7.31 % | 4,378.7 | 131,056.6 | 16.97 % | 50.4 % | 93.5 % |
| mir_operator:TransposeOp | 16 | 68,069.5 | 3.55 % | 4,254.3 | 66,048.9 | 8.55 % | 86.0 % | 97.0 % |
| adapter_dispatch | 16 | 19,059.7 | 0.99 % | 1,191.2 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| h2d_stage | 16 | 15,375.8 | 0.8 % | 961.0 | 12,878.3 | 1.67 % | 88.2 % | 83.8 % |
| d2h_stage | 16 | 14,643.7 | 0.76 % | 915.2 | 13,583.9 | 1.76 % | 95.1 % | 92.8 % |
| mir_operator:AddOp | 16 | 9,188.2 | 0.48 % | 574.3 | 5,180.6 | 0.67 % | 29.8 % | 56.4 % |
| dag_schedule_gap | 24 | 8,483.4 | 0.44 % | 353.5 | 0.0 | 0.0 % | 0.5 % | 0.0 % |
| token_preprocess_cpu | 16 | 4,827.8 | 0.25 % | 301.7 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| weight_init | 16 | 3,145.8 | 0.16 % | 196.6 | 462.1 | 0.06 % | 24.9 % | 14.7 % |
| agent_tool_execute_cpu | 8 | 2,680.3 | 0.14 % | 335.0 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:ViewOp | 16 | 2,502.9 | 0.13 % | 156.4 | 0.0 | 0.0 % | 9.9 % | 0.0 % |
| checksum_complete | 16 | 1,363.7 | 0.07 % | 85.2 | 0.0 | 0.0 % | 2.5 % | 0.0 % |
| inter_operator_dispatch | 112 | 1,206.2 | 0.06 % | 10.8 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| iteration_tail_sync | 8 | 454.0 | 0.02 % | 56.8 | 0.0 | 0.0 % | 20.6 % | 0.0 % |
| pre_d2h_alloc | 16 | 332.0 | 0.02 % | 20.8 | 0.0 | 0.0 % | 0.0 % | 0.0 % |

## Call breakdown (agent nodes)

| call | kind | wave | matrix | host per iter (us) | host share | GPU per iter (us) | GPU share | GPU/host |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| plan | llm | 0 | 3072 | 117,318.6 | 48.99 % | 48,249.7 | 49.98 % | 41.13 % |
| lookup | tool | 1 | 256 | 335.0 | 0.14 % | 0.0 | 0.0 % | 0.0 % |
| answer | llm | 2 | 3072 | 120,694.8 | 50.4 % | 48,288.6 | 50.02 % | 40.01 % |
| <dag> | dag |  |  | 1,117.2 | 0.47 % | 0.0 | 0.0 % | 0.0 % |

## CUDA runtime API inside the measured window

| API | calls | total (us) | share of wall |
|---|---:|---:|---:|
| cudaEventSynchronize | 160 | 631,473.8 | 32.96 % |
| cudaLaunchKernel | 9760 | 47,096.4 | 2.46 % |
| cudaEventRecord | 352 | 1,631.8 | 0.09 % |
| cudaMemcpyAsync | 32 | 815.5 | 0.04 % |
| cudaEventCreateWithFlags | 320 | 745.1 | 0.04 % |
| cudaEventDestroy | 320 | 436.4 | 0.02 % |
| cudaEventQuery | 32 | 152.0 | 0.01 % |
| cudaDeviceSynchronize | 8 | 57.4 | 0.0 % |
| cudaStreamIsCapturing | 48 | 46.0 | 0.0 % |

## Kernel families by process (G03)

| process | family | instances | GPU total (us) | share |
|---|---|---:|---:|---:|
| mir_operator:LinearOp | gemm | 1536 | 543,095.3 | 70.32 % |
| mir_operator:TransposeOp | copy | 512 | 66,048.9 | 8.55 % |
| mir_operator:RMSNormOp | copy | 2048 | 43,774.0 | 5.67 % |
| mir_operator:RMSNormOp | elementwise_unary | 2048 | 42,694.9 | 5.53 % |
| mir_operator:RMSNormOp | elementwise_binary | 2048 | 33,775.6 | 4.37 % |
| d2h_stage | memcpy | 16 | 13,583.9 | 1.76 % |
| h2d_stage | memcpy | 16 | 12,878.3 | 1.67 % |
| mir_operator:RMSNormOp | reduce | 1024 | 10,812.0 | 1.4 % |
| mir_operator:AddOp | elementwise_binary | 512 | 5,180.6 | 0.67 % |
| weight_init | rng_init | 16 | 293.0 | 0.04 % |
| weight_init | elementwise_binary | 16 | 169.1 | 0.02 % |

## Kernel launch order, representative iteration 5 (G03)

| # | call | process | kind | family | GPU (us) | launch latency (us) | grid | block |
|---:|---|---|---|---|---:|---:|---|---|
| 1 | plan | h2d_stage | memcpy | memcpy | 805.1 | 25.1 | 0x0x0 | 0x0x0 |
| 2 | plan | weight_init | kernel | rng_init | 18.2 | 88.4 | 768x1x1 | 256x1x1 |
| 3 | plan | weight_init | kernel | elementwise_binary | 10.6 | 39.6 | 9216x1x1 | 128x1x1 |
| 4 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 58.3 | 9.2 | 9216x1x1 | 128x1x1 |
| 5 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 39.0 | 40.5 | 9216x1x1 | 128x1x1 |
| 6 | plan | mir_operator:RMSNormOp:6 | kernel | reduce | 10.9 | 52.9 | 192x1x1 | 32x16x1 |
| 7 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 39.7 | 3x1x1 | 128x1x1 |
| 8 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 21.6 | 3x1x1 | 128x1x1 |
| 9 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 29.8 | 6.7 | 36864x1x1 | 128x1x1 |
| 10 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 12.3 | 15.2 | 9216x1x1 | 128x1x1 |
| 11 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 28.3 | 7.4 | 9216x1x1 | 128x1x1 |
| 12 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 39.8 | 22.4 | 9216x1x1 | 128x1x1 |
| 13 | plan | mir_operator:RMSNormOp:6 | kernel | reduce | 10.1 | 48.1 | 192x1x1 | 32x16x1 |
| 14 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.0 | 47.5 | 3x1x1 | 128x1x1 |
| 15 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 37.0 | 3x1x1 | 128x1x1 |
| 16 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 31.5 | 25.8 | 36864x1x1 | 128x1x1 |
| 17 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 12.4 | 34.5 | 9216x1x1 | 128x1x1 |
| 18 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 28.8 | 26.8 | 9216x1x1 | 128x1x1 |
| 19 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 40.4 | 43.2 | 9216x1x1 | 128x1x1 |
| 20 | plan | mir_operator:RMSNormOp:6 | kernel | reduce | 10.0 | 70.2 | 192x1x1 | 32x16x1 |
| 21 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.6 | 69.3 | 3x1x1 | 128x1x1 |
| 22 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 59.3 | 3x1x1 | 128x1x1 |
| 23 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 32.1 | 48.2 | 36864x1x1 | 128x1x1 |
| 24 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 12.1 | 66.5 | 9216x1x1 | 128x1x1 |
| 25 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 29.0 | 56.2 | 9216x1x1 | 128x1x1 |
| 26 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 40.8 | 73.1 | 9216x1x1 | 128x1x1 |
| 27 | plan | mir_operator:RMSNormOp:6 | kernel | reduce | 10.0 | 101.0 | 192x1x1 | 32x16x1 |
| 28 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.4 | 100.9 | 3x1x1 | 128x1x1 |
| 29 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 91.1 | 3x1x1 | 128x1x1 |
| 30 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 31.7 | 80.5 | 36864x1x1 | 128x1x1 |
| 31 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 12.1 | 98.4 | 9216x1x1 | 128x1x1 |
| 32 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 28.7 | 92.6 | 9216x1x1 | 128x1x1 |
| 33 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 39.4 | 109.3 | 9216x1x1 | 128x1x1 |
| 34 | plan | mir_operator:RMSNormOp:6 | kernel | reduce | 10.5 | 135.9 | 192x1x1 | 32x16x1 |
| 35 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.1 | 136.5 | 3x1x1 | 128x1x1 |
| 36 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 126.4 | 3x1x1 | 128x1x1 |
| 37 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 31.9 | 115.5 | 36864x1x1 | 128x1x1 |
| 38 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 12.1 | 133.6 | 9216x1x1 | 128x1x1 |
| 39 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 29.7 | 127.4 | 9216x1x1 | 128x1x1 |
| 40 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 40.5 | 145.0 | 9216x1x1 | 128x1x1 |
| 41 | plan | mir_operator:RMSNormOp:6 | kernel | reduce | 10.6 | 172.7 | 192x1x1 | 32x16x1 |
| 42 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.1 | 173.6 | 3x1x1 | 128x1x1 |
| 43 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 163.5 | 3x1x1 | 128x1x1 |
| 44 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 31.3 | 152.8 | 36864x1x1 | 128x1x1 |
| 45 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 12.1 | 170.3 | 9216x1x1 | 128x1x1 |
| 46 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 29.9 | 164.6 | 9216x1x1 | 128x1x1 |
| 47 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 40.1 | 181.8 | 9216x1x1 | 128x1x1 |
| 48 | plan | mir_operator:RMSNormOp:6 | kernel | reduce | 10.0 | 209.1 | 192x1x1 | 32x16x1 |
| 49 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.0 | 209.0 | 3x1x1 | 128x1x1 |
| 50 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 198.8 | 3x1x1 | 128x1x1 |
| 51 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 32.2 | 188.2 | 36864x1x1 | 128x1x1 |
| 52 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 12.1 | 206.9 | 9216x1x1 | 128x1x1 |
| 53 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 29.5 | 201.4 | 9216x1x1 | 128x1x1 |
| 54 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 40.2 | 219.1 | 9216x1x1 | 128x1x1 |
| 55 | plan | mir_operator:RMSNormOp:6 | kernel | reduce | 10.0 | 246.2 | 192x1x1 | 32x16x1 |
| 56 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.3 | 246.6 | 3x1x1 | 128x1x1 |
| 57 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 236.7 | 3x1x1 | 128x1x1 |
| 58 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 31.8 | 225.9 | 36864x1x1 | 128x1x1 |
| 59 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 12.1 | 244.2 | 9216x1x1 | 128x1x1 |
| 60 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 29.1 | 238.8 | 9216x1x1 | 128x1x1 |
| … | | 1164 more rows in kernel_launch_order_representative_iteration.csv | | | | | | |

## Per call/process summary (medians over measured iterations)

| call | process | op | host median (us) | host min/max (us) | GPU median (us) | top CUDA API | kernels |
|---|---|---:|---:|---:|---:|---|---:|
| plan | adapter_dispatch |  | 948.6 | 884.9/1,023.1 | 0.0 |  | 0 |
| plan | token_preprocess_cpu |  | 359.6 | 301.3/399.0 | 0.0 |  | 0 |
| plan | host_input_generate |  | 66,353.5 | 62,848.8/67,192.7 | 0.0 | cudaEventQuery | 0 |
| plan | h2d_stage |  | 963.9 | 940.7/999.5 | 810.5 | cudaEventSynchronize | 0 |
| plan | weight_init |  | 194.3 | 184.9/197.9 | 28.9 | cudaLaunchKernel | 2 |
| plan | mir_operator:RMSNormOp | 6 | 4,392.6 | 4,297.4/4,644.4 | 4,126.0 | cudaEventSynchronize | 224 |
| plan | inter_operator_dispatch |  | 9.0 | 5.0/23.1 | 0.0 |  | 0 |
| plan | mir_operator:AddOp | 7 | 561.4 | 527.2/578.2 | 323.1 | cudaLaunchKernel | 32 |
| plan | mir_operator:RMSNormOp | 8 | 4,239.2 | 4,218.3/4,499.0 | 4,017.3 | cudaEventSynchronize | 224 |
| plan | mir_operator:LinearOp | 10 | 11,460.6 | 11,232.5/11,613.6 | 11,318.9 | cudaEventSynchronize | 32 |
| plan | mir_operator:LinearOp | 11 | 11,279.5 | 11,142.0/11,556.0 | 11,153.0 | cudaEventSynchronize | 32 |
| plan | mir_operator:LinearOp | 12 | 11,568.4 | 11,209.7/11,736.8 | 11,474.0 | cudaEventSynchronize | 32 |
| plan | mir_operator:ViewOp | 13 | 154.8 | 137.7/189.9 | 0.0 | cudaEventRecord | 0 |
| plan | mir_operator:TransposeOp | 14 | 4,202.6 | 4,099.4/4,430.6 | 4,081.6 | cudaEventSynchronize | 32 |
| plan | pre_d2h_alloc |  | 20.8 | 16.5/26.0 | 0.0 |  | 0 |
| plan | d2h_stage |  | 902.3 | 857.6/1,118.7 | 832.9 | cudaEventSynchronize | 0 |
| plan | checksum_complete |  | 85.5 | 75.8/92.7 | 0.0 | cudaEventDestroy | 0 |
| lookup | agent_tool_execute_cpu |  | 325.8 | 310.4/377.2 | 0.0 |  | 0 |
| answer | adapter_dispatch |  | 1,447.6 | 1,387.8/1,483.5 | 0.0 |  | 0 |
| answer | token_preprocess_cpu |  | 252.2 | 226.3/283.6 | 0.0 |  | 0 |
| answer | host_input_generate |  | 66,401.1 | 63,862.2/85,877.5 | 0.0 | cudaEventQuery | 0 |
| answer | h2d_stage |  | 958.3 | 926.3/990.8 | 801.5 | cudaEventSynchronize | 0 |
| answer | weight_init |  | 192.4 | 183.4/252.4 | 28.9 | cudaLaunchKernel | 2 |
| answer | mir_operator:RMSNormOp | 6 | 4,413.8 | 4,307.9/4,932.3 | 4,150.4 | cudaEventSynchronize | 224 |
| answer | inter_operator_dispatch |  | 10.3 | 4.7/21.1 | 0.0 |  | 0 |
| answer | mir_operator:AddOp | 7 | 570.5 | 547.9/742.5 | 324.2 | cudaLaunchKernel | 32 |
| answer | mir_operator:RMSNormOp | 8 | 4,240.0 | 4,223.9/4,841.7 | 4,020.2 | cudaEventSynchronize | 224 |
| answer | mir_operator:LinearOp | 10 | 11,603.8 | 11,289.7/11,625.1 | 11,431.8 | cudaEventSynchronize | 32 |
| answer | mir_operator:LinearOp | 11 | 11,235.3 | 11,177.9/11,565.0 | 11,094.3 | cudaEventSynchronize | 32 |
| answer | mir_operator:LinearOp | 12 | 11,545.0 | 11,187.3/11,647.5 | 11,456.4 | cudaEventSynchronize | 32 |
| answer | mir_operator:ViewOp | 13 | 153.2 | 142.3/170.4 | 0.0 | cudaEventRecord | 0 |
| answer | mir_operator:TransposeOp | 14 | 4,187.3 | 4,122.4/4,525.2 | 4,061.3 | cudaEventSynchronize | 32 |
| answer | pre_d2h_alloc |  | 20.7 | 18.2/24.2 | 0.0 |  | 0 |
| answer | d2h_stage |  | 907.7 | 862.9/953.4 | 842.7 | cudaEventSynchronize | 0 |
| answer | checksum_complete |  | 85.3 | 81.8/91.9 | 0.0 | cudaEventDestroy | 0 |
| <dag> | dag_schedule_gap |  | 69.3 | 11.8/1,017.5 | 0.0 |  | 0 |
| <dag> | iteration_tail_sync |  | 56.9 | 51.9/64.3 | 0.0 | cudaDeviceSynchronize | 0 |

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

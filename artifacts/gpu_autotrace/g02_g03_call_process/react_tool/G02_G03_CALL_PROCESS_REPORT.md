# G02/G03 call-wise process attribution: `react_tool`

Lineage `h22-gpu-autotrace`, workflow w02. Consumes the w01 trace only; no re-timing.
Host events aligned to the nsys clock by a constant offset fitted on 320 operator pairs (spread 14.3 us).

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
| host_input_generate | 40 | 209,911.7 | 56.26 % | 5,247.8 | 0.0 | 0.0 % | 0.1 % | 0.0 % |
| adapter_dispatch | 40 | 49,043.6 | 13.14 % | 1,226.1 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| dag_schedule_gap | 60 | 25,172.8 | 6.75 % | 419.5 | 0.0 | 0.0 % | 0.4 % | 0.0 % |
| mir_operator:RMSNormOp | 80 | 20,041.5 | 5.37 % | 250.5 | 1,363.6 | 13.98 % | 29.0 % | 6.8 % |
| mir_operator:LinearOp | 120 | 15,899.1 | 4.26 % | 132.5 | 1,531.6 | 15.7 % | 31.0 % | 9.6 % |
| token_preprocess_cpu | 40 | 9,484.9 | 2.54 % | 237.1 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| h2d_stage | 40 | 6,920.2 | 1.85 % | 173.0 | 2,982.0 | 30.58 % | 50.0 % | 43.1 % |
| agent_tool_execute_cpu | 20 | 6,382.7 | 1.71 % | 319.1 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| weight_init | 40 | 5,908.7 | 1.58 % | 147.7 | 218.5 | 2.24 % | 22.9 % | 3.7 % |
| d2h_stage | 40 | 5,491.9 | 1.47 % | 137.3 | 3,201.1 | 32.82 % | 63.6 % | 58.3 % |
| mir_operator:TransposeOp | 40 | 5,093.8 | 1.37 % | 127.3 | 375.8 | 3.85 % | 23.9 % | 7.4 % |
| mir_operator:AddOp | 40 | 4,155.9 | 1.11 % | 103.9 | 80.3 | 0.82 % | 27.1 % | 1.9 % |
| mir_operator:ViewOp | 40 | 3,021.8 | 0.81 % | 75.5 | 0.0 | 0.0 % | 20.4 % | 0.0 % |
| checksum_complete | 40 | 2,716.2 | 0.73 % | 67.9 | 0.0 | 0.0 % | 3.1 % | 0.0 % |
| inter_operator_dispatch | 280 | 2,306.4 | 0.62 % | 8.2 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| iteration_tail_sync | 20 | 1,044.5 | 0.28 % | 52.2 | 0.0 | 0.0 % | 20.8 % | 0.0 % |
| pre_d2h_alloc | 40 | 539.8 | 0.14 % | 13.5 | 0.0 | 0.0 % | 0.0 % | 0.0 % |

## Call breakdown (agent nodes)

| call | kind | wave | matrix | host per iter (us) | host share | GPU per iter (us) | GPU share | GPU/host |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| plan | llm | 0 | 768 | 8,485.6 | 45.48 % | 239.7 | 49.16 % | 2.82 % |
| lookup | tool | 1 | 256 | 319.1 | 1.71 % | 0.0 | 0.0 % | 0.0 % |
| answer | llm | 2 | 768 | 8,541.1 | 45.78 % | 247.9 | 50.84 % | 2.9 % |
| <dag> | dag |  |  | 1,310.9 | 7.03 % | 0.0 | 0.0 % | 0.0 % |

## CUDA runtime API inside the measured window

| API | calls | total (us) | share of wall |
|---|---:|---:|---:|
| cudaLaunchKernel | 720 | 6,190.4 | 1.66 % |
| cudaEventSynchronize | 400 | 5,365.6 | 1.44 % |
| cudaEventRecord | 880 | 3,981.3 | 1.07 % |
| cuLaunchKernel | 120 | 1,901.1 | 0.51 % |
| cudaEventCreateWithFlags | 800 | 1,581.8 | 0.42 % |
| cudaMemcpyAsync | 80 | 1,178.3 | 0.32 % |
| cudaEventDestroy | 800 | 920.1 | 0.25 % |
| cudaMemsetAsync | 120 | 915.7 | 0.25 % |
| cudaEventQuery | 80 | 306.9 | 0.08 % |
| cuKernelGetFunction | 120 | 149.1 | 0.04 % |
| cudaDeviceSynchronize | 20 | 114.4 | 0.03 % |
| cudaStreamIsCapturing | 120 | 111.5 | 0.03 % |

## Kernel families by process (G03)

| process | family | instances | GPU total (us) | share |
|---|---|---:|---:|---:|
| d2h_stage | memcpy | 40 | 3,201.1 | 32.82 % |
| h2d_stage | memcpy | 40 | 2,982.0 | 30.58 % |
| mir_operator:LinearOp | gemm | 120 | 1,479.1 | 15.17 % |
| mir_operator:RMSNormOp | copy | 160 | 448.8 | 4.6 % |
| mir_operator:TransposeOp | copy | 40 | 375.8 | 3.85 % |
| mir_operator:RMSNormOp | elementwise_binary | 160 | 366.6 | 3.76 % |
| mir_operator:RMSNormOp | elementwise_unary | 160 | 281.7 | 2.89 % |
| mir_operator:RMSNormOp | reduce | 80 | 266.5 | 2.73 % |
| weight_init | rng_init | 40 | 142.6 | 1.46 % |
| mir_operator:AddOp | elementwise_binary | 40 | 80.3 | 0.82 % |
| weight_init | elementwise_binary | 40 | 75.9 | 0.78 % |
| mir_operator:LinearOp | memset | 120 | 52.5 | 0.54 % |

## Kernel launch order, representative iteration 7 (G03)

| # | call | process | kind | family | GPU (us) | launch latency (us) | grid | block |
|---:|---|---|---|---|---:|---:|---|---|
| 1 | plan | h2d_stage | memcpy | memcpy | 81.0 | 15.3 | 0x0x0 | 0x0x0 |
| 2 | plan | weight_init | kernel | rng_init | 3.6 | 82.6 | 768x1x1 | 256x1x1 |
| 3 | plan | weight_init | kernel | elementwise_binary | 1.5 | 37.9 | 576x1x1 | 128x1x1 |
| 4 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 3.6 | 9.3 | 576x1x1 | 128x1x1 |
| 5 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 2.1 | 8.5 | 576x1x1 | 128x1x1 |
| 6 | plan | mir_operator:RMSNormOp:6 | kernel | reduce | 3.1 | 8.4 | 48x1x1 | 32x16x1 |
| 7 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 7.8 | 1x1x1 | 128x1x1 |
| 8 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.2 | 8.3 | 1x1x1 | 128x1x1 |
| 9 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 2.9 | 7.7 | 2304x1x1 | 128x1x1 |
| 10 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 1.7 | 7.1 | 576x1x1 | 128x1x1 |
| 11 | plan | mir_operator:AddOp:7 | kernel | elementwise_binary | 1.4 | 9.2 | 576x1x1 | 128x1x1 |
| 12 | plan | mir_operator:RMSNormOp:8 | kernel | copy | 3.2 | 10.2 | 576x1x1 | 128x1x1 |
| 13 | plan | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 2.1 | 21.5 | 576x1x1 | 128x1x1 |
| 14 | plan | mir_operator:RMSNormOp:8 | kernel | reduce | 2.9 | 7.9 | 48x1x1 | 32x16x1 |
| 15 | plan | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 1.1 | 8.6 | 1x1x1 | 128x1x1 |
| 16 | plan | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 1.2 | 7.2 | 1x1x1 | 128x1x1 |
| 17 | plan | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 2.9 | 7.6 | 2304x1x1 | 128x1x1 |
| 18 | plan | mir_operator:RMSNormOp:8 | kernel | copy | 1.7 | 6.9 | 576x1x1 | 128x1x1 |
| 19 | plan | mir_operator:LinearOp:10 | memset | memset | 0.4 | 13.3 | 0x0x0 | 0x0x0 |
| 20 | plan | mir_operator:LinearOp:10 | kernel | gemm | 12.4 | 9.7 | 96x2x2 | 128x1x1 |
| 21 | plan | mir_operator:LinearOp:11 | memset | memset | 0.4 | 7.9 | 0x0x0 | 0x0x0 |
| 22 | plan | mir_operator:LinearOp:11 | kernel | gemm | 12.3 | 9.0 | 96x2x2 | 128x1x1 |
| 23 | plan | mir_operator:LinearOp:12 | memset | memset | 0.4 | 6.9 | 0x0x0 | 0x0x0 |
| 24 | plan | mir_operator:LinearOp:12 | kernel | gemm | 12.4 | 9.6 | 96x2x2 | 128x1x1 |
| 25 | plan | mir_operator:TransposeOp:14 | kernel | copy | 9.3 | 12.5 | 1152x1x1 | 128x1x1 |
| 26 | plan | d2h_stage | memcpy | memcpy | 90.5 | 13.9 | 0x0x0 | 0x0x0 |
| 27 | answer | h2d_stage | memcpy | memcpy | 82.4 | 15.5 | 0x0x0 | 0x0x0 |
| 28 | answer | weight_init | kernel | rng_init | 3.6 | 18.2 | 768x1x1 | 256x1x1 |
| 29 | answer | weight_init | kernel | elementwise_binary | 1.4 | 8.5 | 576x1x1 | 128x1x1 |
| 30 | answer | mir_operator:RMSNormOp:6 | kernel | copy | 3.5 | 9.0 | 576x1x1 | 128x1x1 |
| 31 | answer | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 2.1 | 7.4 | 576x1x1 | 128x1x1 |
| 32 | answer | mir_operator:RMSNormOp:6 | kernel | reduce | 3.1 | 8.0 | 48x1x1 | 32x16x1 |
| 33 | answer | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 7.4 | 1x1x1 | 128x1x1 |
| 34 | answer | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.2 | 7.1 | 1x1x1 | 128x1x1 |
| 35 | answer | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 2.9 | 7.2 | 2304x1x1 | 128x1x1 |
| 36 | answer | mir_operator:RMSNormOp:6 | kernel | copy | 1.7 | 7.2 | 576x1x1 | 128x1x1 |
| 37 | answer | mir_operator:AddOp:7 | kernel | elementwise_binary | 1.4 | 9.5 | 576x1x1 | 128x1x1 |
| 38 | answer | mir_operator:RMSNormOp:8 | kernel | copy | 3.5 | 9.1 | 576x1x1 | 128x1x1 |
| 39 | answer | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 2.1 | 7.4 | 576x1x1 | 128x1x1 |
| 40 | answer | mir_operator:RMSNormOp:8 | kernel | reduce | 3.0 | 7.7 | 48x1x1 | 32x16x1 |
| 41 | answer | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 1.2 | 7.5 | 1x1x1 | 128x1x1 |
| 42 | answer | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 1.2 | 7.1 | 1x1x1 | 128x1x1 |
| 43 | answer | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 2.9 | 7.2 | 2304x1x1 | 128x1x1 |
| 44 | answer | mir_operator:RMSNormOp:8 | kernel | copy | 1.8 | 7.4 | 576x1x1 | 128x1x1 |
| 45 | answer | mir_operator:LinearOp:10 | memset | memset | 0.4 | 12.1 | 0x0x0 | 0x0x0 |
| 46 | answer | mir_operator:LinearOp:10 | kernel | gemm | 12.3 | 9.8 | 96x2x2 | 128x1x1 |
| 47 | answer | mir_operator:LinearOp:11 | memset | memset | 0.4 | 7.3 | 0x0x0 | 0x0x0 |
| 48 | answer | mir_operator:LinearOp:11 | kernel | gemm | 12.2 | 9.1 | 96x2x2 | 128x1x1 |
| 49 | answer | mir_operator:LinearOp:12 | memset | memset | 0.4 | 7.5 | 0x0x0 | 0x0x0 |
| 50 | answer | mir_operator:LinearOp:12 | kernel | gemm | 12.3 | 9.8 | 96x2x2 | 128x1x1 |
| 51 | answer | mir_operator:TransposeOp:14 | kernel | copy | 9.4 | 11.9 | 1152x1x1 | 128x1x1 |
| 52 | answer | d2h_stage | memcpy | memcpy | 90.2 | 14.0 | 0x0x0 | 0x0x0 |

## Per call/process summary (medians over measured iterations)

| call | process | op | host median (us) | host min/max (us) | GPU median (us) | top CUDA API | kernels |
|---|---|---:|---:|---:|---:|---|---:|
| plan | adapter_dispatch |  | 1,151.5 | 971.1/1,203.1 | 0.0 |  | 0 |
| plan | token_preprocess_cpu |  | 319.5 | 288.6/356.1 | 0.0 |  | 0 |
| plan | host_input_generate |  | 5,103.5 | 5,038.9/8,194.8 | 0.0 | cudaEventQuery | 0 |
| plan | h2d_stage |  | 178.8 | 125.3/218.8 | 80.6 | cudaEventSynchronize | 0 |
| plan | weight_init |  | 149.6 | 118.4/177.8 | 5.0 | cudaLaunchKernel | 2 |
| plan | mir_operator:RMSNormOp | 6 | 272.6 | 227.8/297.2 | 15.9 | cudaLaunchKernel | 7 |
| plan | inter_operator_dispatch |  | 7.8 | 5.4/18.7 | 0.0 |  | 0 |
| plan | mir_operator:AddOp | 7 | 100.4 | 92.4/112.8 | 1.4 | cudaLaunchKernel | 1 |
| plan | mir_operator:RMSNormOp | 8 | 229.3 | 204.8/255.5 | 15.5 | cudaLaunchKernel | 7 |
| plan | mir_operator:LinearOp | 10 | 149.9 | 126.3/178.1 | 12.8 | cuLaunchKernel | 1 |
| plan | mir_operator:LinearOp | 11 | 118.3 | 105.9/131.8 | 12.7 | cuLaunchKernel | 1 |
| plan | mir_operator:LinearOp | 12 | 110.3 | 103.7/132.9 | 12.7 | cudaEventRecord | 1 |
| plan | mir_operator:ViewOp | 13 | 72.4 | 67.0/138.4 | 0.0 | cudaEventRecord | 0 |
| plan | mir_operator:TransposeOp | 14 | 127.1 | 112.1/162.9 | 9.4 | cudaLaunchKernel | 1 |
| plan | pre_d2h_alloc |  | 13.9 | 10.8/14.9 | 0.0 |  | 0 |
| plan | d2h_stage |  | 144.5 | 98.7/241.6 | 90.2 | cudaEventSynchronize | 0 |
| plan | checksum_complete |  | 70.4 | 55.9/83.0 | 0.0 | cudaEventDestroy | 0 |
| lookup | agent_tool_execute_cpu |  | 324.1 | 275.9/366.5 | 0.0 |  | 0 |
| answer | adapter_dispatch |  | 1,301.4 | 1,255.6/1,813.0 | 0.0 |  | 0 |
| answer | token_preprocess_cpu |  | 156.1 | 104.1/186.5 | 0.0 |  | 0 |
| answer | host_input_generate |  | 5,090.4 | 5,031.3/8,124.6 | 0.0 | cudaEventQuery | 0 |
| answer | h2d_stage |  | 181.3 | 127.4/317.1 | 81.6 | cudaEventSynchronize | 0 |
| answer | weight_init |  | 149.9 | 118.7/174.0 | 5.0 | cudaLaunchKernel | 2 |
| answer | mir_operator:RMSNormOp | 6 | 269.6 | 228.1/298.3 | 15.8 | cudaLaunchKernel | 7 |
| answer | inter_operator_dispatch |  | 7.9 | 5.3/26.1 | 0.0 |  | 0 |
| answer | mir_operator:AddOp | 7 | 101.5 | 92.9/161.8 | 1.4 | cudaLaunchKernel | 1 |
| answer | mir_operator:RMSNormOp | 8 | 230.7 | 207.4/290.8 | 15.5 | cudaLaunchKernel | 7 |
| answer | mir_operator:LinearOp | 10 | 152.6 | 127.6/174.0 | 12.8 | cudaEventRecord | 1 |
| answer | mir_operator:LinearOp | 11 | 116.9 | 105.9/853.4 | 12.7 | cuLaunchKernel | 1 |
| answer | mir_operator:LinearOp | 12 | 111.3 | 102.4/139.4 | 12.7 | cuLaunchKernel | 1 |
| answer | mir_operator:ViewOp | 13 | 72.6 | 65.9/87.7 | 0.0 | cudaEventRecord | 0 |
| answer | mir_operator:TransposeOp | 14 | 127.8 | 110.2/143.9 | 9.4 | cudaLaunchKernel | 1 |
| answer | pre_d2h_alloc |  | 13.8 | 10.8/18.7 | 0.0 |  | 0 |
| answer | d2h_stage |  | 144.9 | 97.2/175.8 | 90.3 | cudaEventSynchronize | 0 |
| answer | checksum_complete |  | 69.6 | 54.9/83.9 | 0.0 | cudaEventDestroy | 0 |
| <dag> | dag_schedule_gap |  | 62.0 | 7.2/1,244.5 | 0.0 |  | 0 |
| <dag> | iteration_tail_sync |  | 49.5 | 42.2/78.3 | 0.0 | cudaDeviceSynchronize | 0 |

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

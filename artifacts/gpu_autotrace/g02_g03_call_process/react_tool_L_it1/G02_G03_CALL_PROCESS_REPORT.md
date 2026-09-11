# G02/G03 call-wise process attribution: `react_tool_L_it1`

Lineage `h22-gpu-autotrace`, workflow w02. Consumes the w01 trace only; no re-timing.
Host events aligned to the nsys clock by a constant offset fitted on 128 operator pairs (spread 14.6 us).

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
| host_input_generate | 16 | 1,330,547.1 | 91.76 % | 83,159.2 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| adapter_dispatch | 16 | 23,458.2 | 1.62 % | 1,466.1 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:LinearOp | 48 | 22,597.0 | 1.56 % | 470.8 | 17,852.5 | 34.41 % | 78.5 % | 79.0 % |
| h2d_stage | 16 | 16,157.0 | 1.11 % | 1,009.8 | 13,387.2 | 25.8 % | 86.8 % | 82.9 % |
| d2h_stage | 16 | 14,254.5 | 0.98 % | 890.9 | 13,408.0 | 25.85 % | 94.5 % | 94.1 % |
| mir_operator:RMSNormOp | 32 | 10,441.9 | 0.72 % | 326.3 | 4,391.5 | 8.47 % | 21.3 % | 42.1 % |
| dag_schedule_gap | 24 | 10,249.2 | 0.71 % | 427.0 | 0.0 | 0.0 % | 0.4 % | 0.0 % |
| token_preprocess_cpu | 16 | 5,244.8 | 0.36 % | 327.8 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:TransposeOp | 16 | 3,850.2 | 0.27 % | 240.6 | 2,148.5 | 4.14 % | 51.3 % | 55.8 % |
| weight_init | 16 | 3,638.2 | 0.25 % | 227.4 | 507.5 | 0.98 % | 23.2 % | 14.0 % |
| agent_tool_execute_cpu | 8 | 3,283.2 | 0.23 % | 410.4 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:AddOp | 16 | 1,813.6 | 0.13 % | 113.3 | 183.0 | 0.35 % | 24.5 % | 10.1 % |
| checksum_complete | 16 | 1,457.0 | 0.1 % | 91.1 | 0.0 | 0.0 % | 2.3 % | 0.0 % |
| mir_operator:ViewOp | 16 | 1,288.8 | 0.09 % | 80.5 | 0.0 | 0.0 % | 17.9 % | 0.0 % |
| inter_operator_dispatch | 112 | 955.1 | 0.07 % | 8.5 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| iteration_tail_sync | 8 | 521.5 | 0.04 % | 65.2 | 0.0 | 0.0 % | 20.9 % | 0.0 % |
| pre_d2h_alloc | 16 | 273.7 | 0.02 % | 17.1 | 0.0 | 0.0 % | 0.0 % | 0.0 % |

## Call breakdown (agent nodes)

| call | kind | wave | matrix | host per iter (us) | host share | GPU per iter (us) | GPU share | GPU/host |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| plan | llm | 0 | 3072 | 89,288.0 | 49.26 % | 3,228.7 | 49.79 % | 3.62 % |
| lookup | tool | 1 | 256 | 410.4 | 0.23 % | 0.0 | 0.0 % | 0.0 % |
| answer | llm | 2 | 3072 | 90,209.1 | 49.77 % | 3,256.1 | 50.21 % | 3.61 % |
| <dag> | dag |  |  | 1,346.3 | 0.74 % | 0.0 | 0.0 % | 0.0 % |

## CUDA runtime API inside the measured window

| API | calls | total (us) | share of wall |
|---|---:|---:|---:|
| cudaEventSynchronize | 160 | 44,428.0 | 3.06 % |
| cudaLaunchKernel | 336 | 3,207.9 | 0.22 % |
| cudaEventRecord | 352 | 1,645.8 | 0.11 % |
| cudaEventCreateWithFlags | 320 | 713.2 | 0.05 % |
| cudaMemcpyAsync | 32 | 639.3 | 0.04 % |
| cudaEventDestroy | 320 | 381.7 | 0.03 % |
| cudaEventQuery | 32 | 163.5 | 0.01 % |
| cudaDeviceSynchronize | 8 | 64.6 | 0.0 % |
| cudaStreamIsCapturing | 48 | 53.8 | 0.0 % |

## Kernel families by process (G03)

| process | family | instances | GPU total (us) | share |
|---|---|---:|---:|---:|
| mir_operator:LinearOp | gemm | 48 | 17,852.5 | 34.41 % |
| d2h_stage | memcpy | 16 | 13,408.0 | 25.85 % |
| h2d_stage | memcpy | 16 | 13,387.2 | 25.8 % |
| mir_operator:TransposeOp | copy | 16 | 2,148.5 | 4.14 % |
| mir_operator:RMSNormOp | copy | 64 | 1,887.5 | 3.64 % |
| mir_operator:RMSNormOp | elementwise_unary | 64 | 1,251.9 | 2.41 % |
| mir_operator:RMSNormOp | elementwise_binary | 64 | 882.2 | 1.7 % |
| mir_operator:RMSNormOp | reduce | 32 | 369.9 | 0.71 % |
| weight_init | rng_init | 16 | 329.0 | 0.63 % |
| mir_operator:AddOp | elementwise_binary | 16 | 183.0 | 0.35 % |
| weight_init | elementwise_binary | 16 | 178.5 | 0.34 % |

## Kernel launch order, representative iteration 1 (G03)

| # | call | process | kind | family | GPU (us) | launch latency (us) | grid | block |
|---:|---|---|---|---|---:|---:|---|---|
| 1 | plan | h2d_stage | memcpy | memcpy | 811.0 | 25.5 | 0x0x0 | 0x0x0 |
| 2 | plan | weight_init | kernel | rng_init | 20.5 | 97.8 | 768x1x1 | 256x1x1 |
| 3 | plan | weight_init | kernel | elementwise_binary | 11.4 | 32.9 | 9216x1x1 | 128x1x1 |
| 4 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 53.9 | 10.9 | 9216x1x1 | 128x1x1 |
| 5 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 37.0 | 32.0 | 9216x1x1 | 128x1x1 |
| 6 | plan | mir_operator:RMSNormOp:6 | kernel | reduce | 11.6 | 36.1 | 192x1x1 | 32x16x1 |
| 7 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.7 | 17.7 | 3x1x1 | 128x1x1 |
| 8 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.1 | 6.8 | 3x1x1 | 128x1x1 |
| 9 | plan | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 24.6 | 7.3 | 36864x1x1 | 128x1x1 |
| 10 | plan | mir_operator:RMSNormOp:6 | kernel | copy | 13.5 | 7.9 | 9216x1x1 | 128x1x1 |
| 11 | plan | mir_operator:AddOp:7 | kernel | elementwise_binary | 11.4 | 9.1 | 9216x1x1 | 128x1x1 |
| 12 | plan | mir_operator:RMSNormOp:8 | kernel | copy | 36.1 | 9.1 | 9216x1x1 | 128x1x1 |
| 13 | plan | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 37.8 | 24.0 | 9216x1x1 | 128x1x1 |
| 14 | plan | mir_operator:RMSNormOp:8 | kernel | reduce | 11.3 | 41.7 | 192x1x1 | 32x16x1 |
| 15 | plan | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 1.8 | 37.2 | 3x1x1 | 128x1x1 |
| 16 | plan | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 1.1 | 23.7 | 3x1x1 | 128x1x1 |
| 17 | plan | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 25.2 | 7.4 | 36864x1x1 | 128x1x1 |
| 18 | plan | mir_operator:RMSNormOp:8 | kernel | copy | 13.2 | 14.0 | 9216x1x1 | 128x1x1 |
| 19 | plan | mir_operator:LinearOp:10 | kernel | gemm | 371.8 | 11.3 | 48x24x1 | 128x1x1 |
| 20 | plan | mir_operator:LinearOp:11 | kernel | gemm | 370.5 | 9.8 | 48x24x1 | 128x1x1 |
| 21 | plan | mir_operator:LinearOp:12 | kernel | gemm | 369.4 | 8.5 | 48x24x1 | 128x1x1 |
| 22 | plan | mir_operator:TransposeOp:14 | kernel | copy | 132.7 | 11.4 | 18432x1x1 | 128x1x1 |
| 23 | plan | d2h_stage | memcpy | memcpy | 823.9 | 12.5 | 0x0x0 | 0x0x0 |
| 24 | answer | h2d_stage | memcpy | memcpy | 819.6 | 26.7 | 0x0x0 | 0x0x0 |
| 25 | answer | weight_init | kernel | rng_init | 20.5 | 104.3 | 768x1x1 | 256x1x1 |
| 26 | answer | weight_init | kernel | elementwise_binary | 11.1 | 37.8 | 9216x1x1 | 128x1x1 |
| 27 | answer | mir_operator:RMSNormOp:6 | kernel | copy | 52.2 | 11.5 | 9216x1x1 | 128x1x1 |
| 28 | answer | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 36.6 | 30.2 | 9216x1x1 | 128x1x1 |
| 29 | answer | mir_operator:RMSNormOp:6 | kernel | reduce | 11.6 | 33.7 | 192x1x1 | 32x16x1 |
| 30 | answer | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.6 | 17.2 | 3x1x1 | 128x1x1 |
| 31 | answer | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.1 | 7.6 | 3x1x1 | 128x1x1 |
| 32 | answer | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 24.8 | 7.1 | 36864x1x1 | 128x1x1 |
| 33 | answer | mir_operator:RMSNormOp:6 | kernel | copy | 13.5 | 7.7 | 9216x1x1 | 128x1x1 |
| 34 | answer | mir_operator:AddOp:7 | kernel | elementwise_binary | 11.6 | 16.8 | 9216x1x1 | 128x1x1 |
| 35 | answer | mir_operator:RMSNormOp:8 | kernel | copy | 36.9 | 12.6 | 9216x1x1 | 128x1x1 |
| 36 | answer | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 37.4 | 20.6 | 9216x1x1 | 128x1x1 |
| 37 | answer | mir_operator:RMSNormOp:8 | kernel | reduce | 11.2 | 33.2 | 192x1x1 | 32x16x1 |
| 38 | answer | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 1.6 | 25.9 | 3x1x1 | 128x1x1 |
| 39 | answer | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 1.1 | 9.6 | 3x1x1 | 128x1x1 |
| 40 | answer | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 25.6 | 6.5 | 36864x1x1 | 128x1x1 |
| 41 | answer | mir_operator:RMSNormOp:8 | kernel | copy | 13.2 | 11.7 | 9216x1x1 | 128x1x1 |
| 42 | answer | mir_operator:LinearOp:10 | kernel | gemm | 372.0 | 11.4 | 48x24x1 | 128x1x1 |
| 43 | answer | mir_operator:LinearOp:11 | kernel | gemm | 371.0 | 8.0 | 48x24x1 | 128x1x1 |
| 44 | answer | mir_operator:LinearOp:12 | kernel | gemm | 370.7 | 12.2 | 48x24x1 | 128x1x1 |
| 45 | answer | mir_operator:TransposeOp:14 | kernel | copy | 133.0 | 11.9 | 18432x1x1 | 128x1x1 |
| 46 | answer | d2h_stage | memcpy | memcpy | 832.7 | 13.1 | 0x0x0 | 0x0x0 |

## Per call/process summary (medians over measured iterations)

| call | process | op | host median (us) | host min/max (us) | GPU median (us) | top CUDA API | kernels |
|---|---|---:|---:|---:|---:|---|---:|
| plan | adapter_dispatch |  | 1,134.4 | 1,052.3/1,167.4 | 0.0 |  | 0 |
| plan | token_preprocess_cpu |  | 424.2 | 341.5/436.4 | 0.0 |  | 0 |
| plan | host_input_generate |  | 82,907.2 | 82,542.1/83,365.5 | 0.0 | cudaEventQuery | 0 |
| plan | h2d_stage |  | 993.1 | 934.6/1,080.0 | 824.2 | cudaEventSynchronize | 0 |
| plan | weight_init |  | 227.7 | 176.5/251.2 | 31.7 | cudaLaunchKernel | 2 |
| plan | mir_operator:RMSNormOp | 6 | 326.3 | 298.1/1,948.6 | 143.5 | cudaLaunchKernel | 7 |
| plan | inter_operator_dispatch |  | 7.6 | 5.7/16.5 | 0.0 |  | 0 |
| plan | mir_operator:AddOp | 7 | 105.0 | 102.4/134.5 | 11.4 | cudaEventRecord | 1 |
| plan | mir_operator:RMSNormOp | 8 | 222.3 | 211.4/265.9 | 127.2 | cudaLaunchKernel | 7 |
| plan | mir_operator:LinearOp | 10 | 511.2 | 496.6/518.0 | 371.2 | cudaEventSynchronize | 1 |
| plan | mir_operator:LinearOp | 11 | 448.2 | 446.5/473.9 | 370.4 | cudaEventSynchronize | 1 |
| plan | mir_operator:LinearOp | 12 | 443.0 | 439.2/445.9 | 370.4 | cudaEventSynchronize | 1 |
| plan | mir_operator:ViewOp | 13 | 76.8 | 74.4/103.4 | 0.0 | cudaEventRecord | 0 |
| plan | mir_operator:TransposeOp | 14 | 240.2 | 227.5/257.1 | 133.0 | cudaEventSynchronize | 1 |
| plan | pre_d2h_alloc |  | 17.1 | 14.7/18.7 | 0.0 |  | 0 |
| plan | d2h_stage |  | 877.6 | 866.2/893.5 | 826.2 | cudaEventSynchronize | 0 |
| plan | checksum_complete |  | 92.1 | 76.8/103.3 | 0.0 | cudaEventDestroy | 0 |
| lookup | agent_tool_execute_cpu |  | 406.6 | 364.1/461.2 | 0.0 |  | 0 |
| answer | adapter_dispatch |  | 1,795.7 | 1,764.8/1,907.5 | 0.0 |  | 0 |
| answer | token_preprocess_cpu |  | 247.6 | 199.9/285.0 | 0.0 |  | 0 |
| answer | host_input_generate |  | 83,383.3 | 83,046.1/83,964.0 | 0.0 | cudaEventQuery | 0 |
| answer | h2d_stage |  | 1,012.0 | 944.9/1,148.0 | 817.5 | cudaEventSynchronize | 0 |
| answer | weight_init |  | 230.7 | 191.1/258.8 | 31.7 | cudaLaunchKernel | 2 |
| answer | mir_operator:RMSNormOp | 6 | 328.3 | 299.9/352.6 | 142.5 | cudaLaunchKernel | 7 |
| answer | inter_operator_dispatch |  | 7.9 | 5.5/18.6 | 0.0 |  | 0 |
| answer | mir_operator:AddOp | 7 | 105.5 | 101.4/169.7 | 11.5 | cudaLaunchKernel | 1 |
| answer | mir_operator:RMSNormOp | 8 | 218.6 | 208.5/254.2 | 126.7 | cudaLaunchKernel | 7 |
| answer | mir_operator:LinearOp | 10 | 512.0 | 494.7/526.4 | 371.5 | cudaEventSynchronize | 1 |
| answer | mir_operator:LinearOp | 11 | 449.5 | 445.3/516.1 | 370.9 | cudaEventSynchronize | 1 |
| answer | mir_operator:LinearOp | 12 | 442.6 | 438.6/482.0 | 370.4 | cudaEventSynchronize | 1 |
| answer | mir_operator:ViewOp | 13 | 78.4 | 75.4/87.3 | 0.0 | cudaEventRecord | 0 |
| answer | mir_operator:TransposeOp | 14 | 235.8 | 227.5/257.9 | 133.0 | cudaEventSynchronize | 1 |
| answer | pre_d2h_alloc |  | 16.8 | 15.3/20.3 | 0.0 |  | 0 |
| answer | d2h_stage |  | 885.4 | 865.3/1,041.2 | 831.7 | cudaEventSynchronize | 0 |
| answer | checksum_complete |  | 91.4 | 80.2/101.3 | 0.0 | cudaEventDestroy | 0 |
| <dag> | dag_schedule_gap |  | 76.8 | 14.7/1,242.1 | 0.0 |  | 0 |
| <dag> | iteration_tail_sync |  | 64.8 | 62.9/68.1 | 0.0 | cudaDeviceSynchronize | 0 |

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

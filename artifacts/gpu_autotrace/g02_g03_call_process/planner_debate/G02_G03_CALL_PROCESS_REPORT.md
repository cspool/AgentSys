# G02/G03 call-wise process attribution: `planner_debate`

Lineage `h22-gpu-autotrace`, workflow w02. Consumes the w01 trace only; no re-timing.
Host events aligned to the nsys clock by a constant offset fitted on 800 operator pairs (spread 22.3 us).

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
| host_input_generate | 100 | 922,181.0 | 69.9 % | 9,221.8 | 0.0 | 0.0 % | 0.1 % | 0.0 % |
| adapter_dispatch | 100 | 123,846.7 | 9.39 % | 1,238.5 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:RMSNormOp | 200 | 55,676.5 | 4.22 % | 278.4 | 3,874.9 | 9.99 % | 28.4 % | 7.0 % |
| mir_operator:LinearOp | 300 | 36,880.5 | 2.8 % | 122.9 | 5,634.6 | 14.53 % | 24.7 % | 15.3 % |
| dag_schedule_gap | 120 | 30,606.8 | 2.32 % | 255.1 | 0.0 | 0.0 % | 1.3 % | 0.0 % |
| token_preprocess_cpu | 100 | 30,574.0 | 2.32 % | 305.7 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| h2d_stage | 100 | 24,936.5 | 1.89 % | 249.4 | 13,093.8 | 33.76 % | 61.6 % | 52.5 % |
| d2h_stage | 100 | 19,930.3 | 1.51 % | 199.3 | 14,010.9 | 36.13 % | 73.5 % | 70.3 % |
| weight_init | 100 | 17,358.3 | 1.32 % | 173.6 | 693.8 | 1.79 % | 22.6 % | 4.0 % |
| mir_operator:TransposeOp | 100 | 13,430.1 | 1.02 % | 134.3 | 1,229.9 | 3.17 % | 22.0 % | 9.2 % |
| mir_operator:AddOp | 100 | 11,077.3 | 0.84 % | 110.8 | 241.5 | 0.62 % | 26.3 % | 2.2 % |
| mir_operator:ViewOp | 100 | 8,373.3 | 0.63 % | 83.7 | 0.0 | 0.0 % | 23.5 % | 0.0 % |
| checksum_complete | 100 | 7,896.7 | 0.6 % | 79.0 | 0.0 | 0.0 % | 2.8 % | 0.0 % |
| agent_tool_execute_cpu | 20 | 7,089.6 | 0.54 % | 354.5 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| inter_operator_dispatch | 700 | 6,513.8 | 0.49 % | 9.3 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| pre_d2h_alloc | 100 | 1,421.0 | 0.11 % | 14.2 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| iteration_tail_sync | 20 | 1,399.9 | 0.11 % | 70.0 | 0.0 | 0.0 % | 21.8 % | 0.0 % |

## Call breakdown (agent nodes)

| call | kind | wave | matrix | host per iter (us) | host share | GPU per iter (us) | GPU share | GPU/host |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| planner-seed | llm | 0 | 896 | 11,618.4 | 17.61 % | 341.4 | 17.61 % | 2.94 % |
| critic-a | llm | 0 | 1024 | 13,297.7 | 20.16 % | 412.8 | 21.29 % | 3.1 % |
| critic-b | llm | 0 | 1024 | 13,845.4 | 20.99 % | 416.5 | 21.48 % | 3.01 % |
| planner-tool | tool | 1 | 256 | 354.5 | 0.54 % | 0.0 | 0.0 % | 0.0 % |
| critic-merge | llm | 1 | 1024 | 13,619.4 | 20.65 % | 430.9 | 22.22 % | 3.16 % |
| planner-final | llm | 2 | 896 | 11,623.9 | 17.62 % | 337.4 | 17.4 % | 2.9 % |
| <dag> | dag |  |  | 1,600.3 | 2.43 % | 0.0 | 0.0 % | 0.0 % |

## CUDA runtime API inside the measured window

| API | calls | total (us) | share of wall |
|---|---:|---:|---:|
| cudaEventSynchronize | 1000 | 25,453.2 | 1.93 % |
| cudaLaunchKernel | 2100 | 20,355.6 | 1.54 % |
| cudaEventRecord | 2200 | 10,843.3 | 0.82 % |
| cudaEventCreateWithFlags | 2000 | 4,368.8 | 0.33 % |
| cudaMemcpyAsync | 200 | 3,542.1 | 0.27 % |
| cudaEventDestroy | 2000 | 2,528.6 | 0.19 % |
| cudaEventQuery | 200 | 916.4 | 0.07 % |
| cudaStreamIsCapturing | 300 | 283.7 | 0.02 % |
| cudaDeviceSynchronize | 20 | 206.1 | 0.02 % |

## Kernel families by process (G03)

| process | family | instances | GPU total (us) | share |
|---|---|---:|---:|---:|
| d2h_stage | memcpy | 100 | 14,010.9 | 36.13 % |
| h2d_stage | memcpy | 100 | 13,093.8 | 33.76 % |
| mir_operator:LinearOp | gemm | 300 | 5,634.6 | 14.53 % |
| mir_operator:RMSNormOp | copy | 400 | 1,389.8 | 3.58 % |
| mir_operator:TransposeOp | copy | 100 | 1,229.9 | 3.17 % |
| mir_operator:RMSNormOp | elementwise_binary | 400 | 963.2 | 2.48 % |
| mir_operator:RMSNormOp | elementwise_unary | 400 | 827.8 | 2.13 % |
| mir_operator:RMSNormOp | reduce | 200 | 694.1 | 1.79 % |
| weight_init | rng_init | 100 | 502.5 | 1.3 % |
| mir_operator:AddOp | elementwise_binary | 100 | 241.5 | 0.62 % |
| weight_init | elementwise_binary | 100 | 191.3 | 0.49 % |

## Kernel launch order, representative iteration 12 (G03)

| # | call | process | kind | family | GPU (us) | launch latency (us) | grid | block |
|---:|---|---|---|---|---:|---:|---|---|
| 1 | planner-seed | h2d_stage | memcpy | memcpy | 117.5 | 16.5 | 0x0x0 | 0x0x0 |
| 2 | planner-seed | weight_init | kernel | rng_init | 5.0 | 20.1 | 768x1x1 | 256x1x1 |
| 3 | planner-seed | weight_init | kernel | elementwise_binary | 1.8 | 9.8 | 784x1x1 | 128x1x1 |
| 4 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 4.0 | 10.2 | 784x1x1 | 128x1x1 |
| 5 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 2.6 | 7.7 | 784x1x1 | 128x1x1 |
| 6 | planner-seed | mir_operator:RMSNormOp:6 | kernel | reduce | 3.3 | 8.9 | 56x1x1 | 32x16x1 |
| 7 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 7.3 | 1x1x1 | 128x1x1 |
| 8 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.2 | 7.4 | 1x1x1 | 128x1x1 |
| 9 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 3.4 | 7.6 | 3136x1x1 | 128x1x1 |
| 10 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 2.0 | 7.8 | 784x1x1 | 128x1x1 |
| 11 | planner-seed | mir_operator:AddOp:7 | kernel | elementwise_binary | 1.7 | 12.3 | 784x1x1 | 128x1x1 |
| 12 | planner-seed | mir_operator:RMSNormOp:8 | kernel | copy | 4.0 | 11.7 | 784x1x1 | 128x1x1 |
| 13 | planner-seed | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 2.6 | 7.8 | 784x1x1 | 128x1x1 |
| 14 | planner-seed | mir_operator:RMSNormOp:8 | kernel | reduce | 3.2 | 8.3 | 56x1x1 | 32x16x1 |
| 15 | planner-seed | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 1.2 | 7.4 | 1x1x1 | 128x1x1 |
| 16 | planner-seed | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 1.2 | 7.1 | 1x1x1 | 128x1x1 |
| 17 | planner-seed | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 3.4 | 8.2 | 3136x1x1 | 128x1x1 |
| 18 | planner-seed | mir_operator:RMSNormOp:8 | kernel | copy | 2.0 | 7.6 | 784x1x1 | 128x1x1 |
| 19 | planner-seed | mir_operator:LinearOp:10 | kernel | gemm | 14.6 | 12.3 | 7x14x1 | 128x1x1 |
| 20 | planner-seed | mir_operator:LinearOp:11 | kernel | gemm | 14.6 | 10.2 | 7x14x1 | 128x1x1 |
| 21 | planner-seed | mir_operator:LinearOp:12 | kernel | gemm | 14.5 | 9.9 | 7x14x1 | 128x1x1 |
| 22 | planner-seed | mir_operator:TransposeOp:14 | kernel | copy | 12.1 | 13.2 | 1568x1x1 | 128x1x1 |
| 23 | planner-seed | d2h_stage | memcpy | memcpy | 123.6 | 15.7 | 0x0x0 | 0x0x0 |
| 24 | critic-a | h2d_stage | memcpy | memcpy | 148.5 | 15.9 | 0x0x0 | 0x0x0 |
| 25 | critic-a | weight_init | kernel | rng_init | 5.1 | 83.5 | 768x1x1 | 256x1x1 |
| 26 | critic-a | weight_init | kernel | elementwise_binary | 2.0 | 35.1 | 1024x1x1 | 128x1x1 |
| 27 | critic-a | mir_operator:RMSNormOp:6 | kernel | copy | 4.4 | 9.4 | 1024x1x1 | 128x1x1 |
| 28 | critic-a | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 3.1 | 7.4 | 1024x1x1 | 128x1x1 |
| 29 | critic-a | mir_operator:RMSNormOp:6 | kernel | reduce | 3.6 | 8.9 | 64x1x1 | 32x16x1 |
| 30 | critic-a | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.1 | 7.5 | 1x1x1 | 128x1x1 |
| 31 | critic-a | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.1 | 6.9 | 1x1x1 | 128x1x1 |
| 32 | critic-a | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 4.0 | 7.2 | 4096x1x1 | 128x1x1 |
| 33 | critic-a | mir_operator:RMSNormOp:6 | kernel | copy | 2.3 | 7.5 | 1024x1x1 | 128x1x1 |
| 34 | critic-a | mir_operator:AddOp:7 | kernel | elementwise_binary | 2.0 | 9.1 | 1024x1x1 | 128x1x1 |
| 35 | critic-a | mir_operator:RMSNormOp:8 | kernel | copy | 4.6 | 9.9 | 1024x1x1 | 128x1x1 |
| 36 | critic-a | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 3.1 | 7.4 | 1024x1x1 | 128x1x1 |
| 37 | critic-a | mir_operator:RMSNormOp:8 | kernel | reduce | 3.2 | 8.8 | 64x1x1 | 32x16x1 |
| 38 | critic-a | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 1.1 | 6.9 | 1x1x1 | 128x1x1 |
| 39 | critic-a | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 1.1 | 7.5 | 1x1x1 | 128x1x1 |
| 40 | critic-a | mir_operator:RMSNormOp:8 | kernel | elementwise_binary | 3.9 | 8.5 | 4096x1x1 | 128x1x1 |
| 41 | critic-a | mir_operator:RMSNormOp:8 | kernel | copy | 2.3 | 7.3 | 1024x1x1 | 128x1x1 |
| 42 | critic-a | mir_operator:LinearOp:10 | kernel | gemm | 19.9 | 12.6 | 8x16x1 | 128x1x1 |
| 43 | critic-a | mir_operator:LinearOp:11 | kernel | gemm | 19.6 | 9.4 | 8x16x1 | 128x1x1 |
| 44 | critic-a | mir_operator:LinearOp:12 | kernel | gemm | 19.6 | 9.0 | 8x16x1 | 128x1x1 |
| 45 | critic-a | mir_operator:TransposeOp:14 | kernel | copy | 12.8 | 11.7 | 2048x1x1 | 128x1x1 |
| 46 | critic-a | d2h_stage | memcpy | memcpy | 162.0 | 15.4 | 0x0x0 | 0x0x0 |
| 47 | critic-b | h2d_stage | memcpy | memcpy | 152.8 | 16.0 | 0x0x0 | 0x0x0 |
| 48 | critic-b | weight_init | kernel | rng_init | 5.1 | 19.1 | 768x1x1 | 256x1x1 |
| 49 | critic-b | weight_init | kernel | elementwise_binary | 2.1 | 9.5 | 1024x1x1 | 128x1x1 |
| 50 | critic-b | mir_operator:RMSNormOp:6 | kernel | copy | 4.3 | 9.5 | 1024x1x1 | 128x1x1 |
| 51 | critic-b | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 3.1 | 7.8 | 1024x1x1 | 128x1x1 |
| 52 | critic-b | mir_operator:RMSNormOp:6 | kernel | reduce | 3.5 | 8.8 | 64x1x1 | 32x16x1 |
| 53 | critic-b | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.1 | 7.6 | 1x1x1 | 128x1x1 |
| 54 | critic-b | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.1 | 7.3 | 1x1x1 | 128x1x1 |
| 55 | critic-b | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 4.0 | 7.6 | 4096x1x1 | 128x1x1 |
| 56 | critic-b | mir_operator:RMSNormOp:6 | kernel | copy | 2.3 | 7.8 | 1024x1x1 | 128x1x1 |
| 57 | critic-b | mir_operator:AddOp:7 | kernel | elementwise_binary | 2.1 | 9.8 | 1024x1x1 | 128x1x1 |
| 58 | critic-b | mir_operator:RMSNormOp:8 | kernel | copy | 4.4 | 13.3 | 1024x1x1 | 128x1x1 |
| 59 | critic-b | mir_operator:RMSNormOp:8 | kernel | elementwise_unary | 3.1 | 22.5 | 1024x1x1 | 128x1x1 |
| 60 | critic-b | mir_operator:RMSNormOp:8 | kernel | reduce | 3.4 | 9.5 | 64x1x1 | 32x16x1 |
| … | | 55 more rows in kernel_launch_order_representative_iteration.csv | | | | | | |

## Per call/process summary (medians over measured iterations)

| call | process | op | host median (us) | host min/max (us) | GPU median (us) | top CUDA API | kernels |
|---|---|---:|---:|---:|---:|---|---:|
| planner-seed | adapter_dispatch |  | 1,175.8 | 1,119.1/2,052.7 | 0.0 |  | 0 |
| planner-seed | token_preprocess_cpu |  | 340.5 | 242.9/385.8 | 0.0 |  | 0 |
| planner-seed | host_input_generate |  | 7,046.1 | 6,853.4/13,582.3 | 0.0 | cudaEventQuery | 0 |
| planner-seed | h2d_stage |  | 224.5 | 152.0/235.8 | 117.0 | cudaEventSynchronize | 0 |
| planner-seed | weight_init |  | 167.4 | 129.0/200.2 | 6.8 | cudaLaunchKernel | 2 |
| planner-seed | mir_operator:RMSNormOp | 6 | 294.4 | 239.9/398.7 | 17.8 | cudaLaunchKernel | 7 |
| planner-seed | inter_operator_dispatch |  | 8.7 | 6.1/23.0 | 0.0 |  | 0 |
| planner-seed | mir_operator:AddOp | 7 | 105.9 | 96.4/163.3 | 1.7 | cudaLaunchKernel | 1 |
| planner-seed | mir_operator:RMSNormOp | 8 | 243.2 | 215.6/444.0 | 17.4 | cudaLaunchKernel | 7 |
| planner-seed | mir_operator:LinearOp | 10 | 142.6 | 125.3/219.0 | 14.6 | cudaLaunchKernel | 1 |
| planner-seed | mir_operator:LinearOp | 11 | 102.9 | 95.1/160.1 | 14.6 | cudaLaunchKernel | 1 |
| planner-seed | mir_operator:LinearOp | 12 | 98.8 | 92.3/174.7 | 14.5 | cudaLaunchKernel | 1 |
| planner-seed | mir_operator:ViewOp | 13 | 75.2 | 69.4/91.8 | 0.0 | cudaEventRecord | 0 |
| planner-seed | mir_operator:TransposeOp | 14 | 129.5 | 113.5/216.5 | 12.1 | cudaLaunchKernel | 1 |
| planner-seed | pre_d2h_alloc |  | 13.0 | 9.6/17.9 | 0.0 |  | 0 |
| planner-seed | d2h_stage |  | 181.4 | 117.3/441.2 | 123.6 | cudaEventSynchronize | 0 |
| planner-seed | checksum_complete |  | 74.9 | 60.2/91.5 | 0.0 | cudaEventDestroy | 0 |
| critic-a | adapter_dispatch |  | 1,169.8 | 1,123.0/1,207.8 | 0.0 |  | 0 |
| critic-a | token_preprocess_cpu |  | 334.4 | 285.5/386.1 | 0.0 |  | 0 |
| critic-a | host_input_generate |  | 9,083.6 | 8,934.4/12,396.9 | 0.0 | cudaEventQuery | 0 |
| critic-a | h2d_stage |  | 260.8 | 171.8/331.4 | 152.5 | cudaEventSynchronize | 0 |
| critic-a | weight_init |  | 165.8 | 127.1/245.4 | 7.1 | cudaLaunchKernel | 2 |
| critic-a | mir_operator:RMSNormOp | 6 | 284.2 | 241.8/472.1 | 19.4 | cudaLaunchKernel | 7 |
| critic-a | inter_operator_dispatch |  | 8.0 | 5.4/22.3 | 0.0 |  | 0 |
| critic-a | mir_operator:AddOp | 7 | 103.6 | 97.7/123.5 | 2.0 | cudaLaunchKernel | 1 |
| critic-a | mir_operator:RMSNormOp | 8 | 247.5 | 214.0/341.3 | 19.1 | cudaLaunchKernel | 7 |
| critic-a | mir_operator:LinearOp | 10 | 140.0 | 117.8/180.3 | 19.8 | cudaLaunchKernel | 1 |
| critic-a | mir_operator:LinearOp | 11 | 103.1 | 95.1/125.1 | 19.7 | cudaLaunchKernel | 1 |
| critic-a | mir_operator:LinearOp | 12 | 96.9 | 91.3/204.6 | 19.6 | cudaEventRecord | 1 |
| critic-a | mir_operator:ViewOp | 13 | 74.4 | 68.0/94.6 | 0.0 | cudaEventRecord | 0 |
| critic-a | mir_operator:TransposeOp | 14 | 127.6 | 115.3/151.2 | 12.3 | cudaLaunchKernel | 1 |
| critic-a | pre_d2h_alloc |  | 13.5 | 9.6/16.4 | 0.0 |  | 0 |
| critic-a | d2h_stage |  | 218.6 | 140.8/233.7 | 162.0 | cudaEventRecord | 0 |
| critic-a | checksum_complete |  | 74.5 | 59.8/150.1 | 0.0 | cudaEventDestroy | 0 |
| critic-b | adapter_dispatch |  | 1,170.3 | 1,103.9/1,297.8 | 0.0 |  | 0 |
| critic-b | token_preprocess_cpu |  | 347.7 | 289.5/390.3 | 0.0 |  | 0 |
| critic-b | host_input_generate |  | 9,280.7 | 8,905.0/16,051.0 | 0.0 | cudaEventQuery | 0 |
| critic-b | h2d_stage |  | 265.7 | 172.7/663.9 | 150.7 | cudaEventSynchronize | 0 |
| critic-b | weight_init |  | 166.0 | 126.1/293.9 | 7.1 | cudaLaunchKernel | 2 |
| critic-b | mir_operator:RMSNormOp | 6 | 293.3 | 247.3/481.4 | 19.4 | cudaLaunchKernel | 7 |
| critic-b | inter_operator_dispatch |  | 8.4 | 5.8/29.2 | 0.0 |  | 0 |
| critic-b | mir_operator:AddOp | 7 | 104.6 | 95.8/184.2 | 2.0 | cudaLaunchKernel | 1 |
| critic-b | mir_operator:RMSNormOp | 8 | 249.8 | 207.1/424.8 | 19.1 | cudaLaunchKernel | 7 |
| critic-b | mir_operator:LinearOp | 10 | 145.6 | 122.0/210.3 | 19.7 | cudaEventRecord | 1 |
| critic-b | mir_operator:LinearOp | 11 | 103.3 | 96.2/178.1 | 19.7 | cudaLaunchKernel | 1 |
| critic-b | mir_operator:LinearOp | 12 | 97.2 | 94.5/172.0 | 19.7 | cudaLaunchKernel | 1 |
| critic-b | mir_operator:ViewOp | 13 | 77.6 | 67.8/440.2 | 0.0 | cudaEventRecord | 0 |
| critic-b | mir_operator:TransposeOp | 14 | 131.6 | 120.8/221.8 | 12.4 | cudaLaunchKernel | 1 |
| critic-b | pre_d2h_alloc |  | 14.1 | 9.6/22.3 | 0.0 |  | 0 |
| critic-b | d2h_stage |  | 219.1 | 141.6/225.3 | 162.0 | cudaEventSynchronize | 0 |
| critic-b | checksum_complete |  | 81.0 | 58.8/105.1 | 0.0 | cudaEventDestroy | 0 |
| planner-tool | agent_tool_execute_cpu |  | 350.3 | 276.9/422.5 | 0.0 |  | 0 |
| critic-merge | adapter_dispatch |  | 1,316.7 | 1,240.1/2,230.7 | 0.0 |  | 0 |
| critic-merge | token_preprocess_cpu |  | 172.0 | 129.9/274.5 | 0.0 |  | 0 |
| critic-merge | host_input_generate |  | 9,180.1 | 8,869.1/12,030.5 | 0.0 | cudaEventQuery | 0 |
| critic-merge | h2d_stage |  | 266.9 | 179.1/336.6 | 151.0 | cudaEventSynchronize | 0 |
| critic-merge | weight_init |  | 175.1 | 127.6/261.3 | 7.1 | cudaLaunchKernel | 2 |
| critic-merge | mir_operator:RMSNormOp | 6 | 304.9 | 238.8/383.6 | 19.4 | cudaLaunchKernel | 7 |
| critic-merge | inter_operator_dispatch |  | 8.1 | 5.2/25.2 | 0.0 |  | 0 |
| critic-merge | mir_operator:AddOp | 7 | 105.4 | 95.5/136.7 | 2.0 | cudaLaunchKernel | 1 |
| critic-merge | mir_operator:RMSNormOp | 8 | 242.1 | 212.3/291.7 | 19.1 | cudaLaunchKernel | 7 |
| critic-merge | mir_operator:LinearOp | 10 | 149.9 | 118.0/341.0 | 19.8 | cudaLaunchKernel | 1 |
| critic-merge | mir_operator:LinearOp | 11 | 103.8 | 96.4/138.7 | 19.7 | cudaLaunchKernel | 1 |
| critic-merge | mir_operator:LinearOp | 12 | 98.8 | 91.6/219.1 | 19.7 | cudaLaunchKernel | 1 |
| critic-merge | mir_operator:ViewOp | 13 | 76.1 | 68.9/94.2 | 0.0 | cudaEventRecord | 0 |
| critic-merge | mir_operator:TransposeOp | 14 | 130.8 | 113.7/153.0 | 12.4 | cudaLaunchKernel | 1 |
| critic-merge | pre_d2h_alloc |  | 14.0 | 10.8/18.7 | 0.0 |  | 0 |
| critic-merge | d2h_stage |  | 219.9 | 143.7/230.8 | 162.1 | cudaEventSynchronize | 0 |
| critic-merge | checksum_complete |  | 78.8 | 59.7/110.0 | 0.0 | cudaEventDestroy | 0 |
| planner-final | adapter_dispatch |  | 1,163.2 | 960.1/1,248.3 | 0.0 |  | 0 |
| planner-final | token_preprocess_cpu |  | 342.9 | 275.1/420.7 | 0.0 |  | 0 |
| planner-final | host_input_generate |  | 7,103.4 | 6,901.2/12,535.1 | 0.0 | cudaEventQuery | 0 |
| planner-final | h2d_stage |  | 227.3 | 171.2/284.1 | 116.4 | cudaEventSynchronize | 0 |
| planner-final | weight_init |  | 176.4 | 130.9/253.7 | 6.8 | cudaLaunchKernel | 2 |
| planner-final | mir_operator:RMSNormOp | 6 | 296.3 | 268.3/447.6 | 17.8 | cudaLaunchKernel | 7 |
| planner-final | inter_operator_dispatch |  | 8.2 | 5.9/46.4 | 0.0 |  | 0 |
| planner-final | mir_operator:AddOp | 7 | 105.6 | 100.7/177.5 | 1.7 | cudaLaunchKernel | 1 |
| planner-final | mir_operator:RMSNormOp | 8 | 249.2 | 225.7/369.0 | 17.5 | cudaLaunchKernel | 7 |
| planner-final | mir_operator:LinearOp | 10 | 146.8 | 120.4/214.4 | 14.6 | cudaLaunchKernel | 1 |
| planner-final | mir_operator:LinearOp | 11 | 102.2 | 96.4/165.3 | 14.6 | cudaLaunchKernel | 1 |
| planner-final | mir_operator:LinearOp | 12 | 96.4 | 92.8/252.3 | 14.5 | cudaLaunchKernel | 1 |
| planner-final | mir_operator:ViewOp | 13 | 76.5 | 69.2/197.3 | 0.0 | cudaEventRecord | 0 |
| planner-final | mir_operator:TransposeOp | 14 | 130.0 | 113.7/185.6 | 12.1 | cudaLaunchKernel | 1 |
| planner-final | pre_d2h_alloc |  | 13.8 | 11.8/40.8 | 0.0 |  | 0 |
| planner-final | d2h_stage |  | 180.4 | 124.6/199.6 | 123.7 | cudaEventSynchronize | 0 |
| planner-final | checksum_complete |  | 78.3 | 60.3/108.2 | 0.0 | cudaEventDestroy | 0 |
| <dag> | dag_schedule_gap |  | 39.2 | 10.5/2,250.1 | 0.0 |  | 0 |
| <dag> | iteration_tail_sync |  | 68.2 | 53.0/85.4 | 0.0 | cudaDeviceSynchronize | 0 |

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

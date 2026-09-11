# G02/G03 call-wise process attribution: `planner_debate_L`

Lineage `h22-gpu-autotrace`, workflow w02. Consumes the w01 trace only; no re-timing.
Host events aligned to the nsys clock by a constant offset fitted on 320 operator pairs (spread 24.5 us).

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
| host_input_generate | 40 | 4,155,143.0 | 48.2 % | 103,878.6 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:LinearOp | 120 | 2,878,961.1 | 33.39 % | 23,991.3 | 2,858,149.0 | 66.24 % | 97.3 % | 99.3 % |
| mir_operator:RMSNormOp | 80 | 1,082,436.9 | 12.56 % | 13,530.5 | 1,062,142.2 | 24.62 % | 84.4 % | 98.1 % |
| mir_operator:TransposeOp | 40 | 270,576.6 | 3.14 % | 6,764.4 | 265,052.5 | 6.14 % | 91.0 % | 98.0 % |
| h2d_stage | 40 | 58,037.8 | 0.67 % | 1,450.9 | 51,479.9 | 1.19 % | 91.4 % | 88.7 % |
| d2h_stage | 40 | 55,809.2 | 0.65 % | 1,395.2 | 53,311.2 | 1.24 % | 96.5 % | 95.5 % |
| adapter_dispatch | 40 | 41,655.8 | 0.48 % | 1,041.4 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:AddOp | 40 | 27,947.3 | 0.32 % | 698.7 | 22,583.0 | 0.52 % | 41.7 % | 80.8 % |
| token_preprocess_cpu | 40 | 13,462.6 | 0.16 % | 336.6 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| dag_schedule_gap | 48 | 9,240.4 | 0.11 % | 192.5 | 0.0 | 0.0 % | 1.8 % | 0.0 % |
| weight_init | 40 | 8,571.7 | 0.1 % | 214.3 | 1,914.1 | 0.04 % | 22.8 % | 22.3 % |
| mir_operator:ViewOp | 40 | 6,781.2 | 0.08 % | 169.5 | 0.0 | 0.0 % | 8.8 % | 0.0 % |
| inter_operator_dispatch | 280 | 4,294.9 | 0.05 % | 15.3 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| checksum_complete | 40 | 3,626.6 | 0.04 % | 90.7 | 0.0 | 0.0 % | 2.1 % | 0.0 % |
| agent_tool_execute_cpu | 8 | 3,014.6 | 0.03 % | 376.8 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| pre_d2h_alloc | 40 | 894.0 | 0.01 % | 22.3 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| iteration_tail_sync | 8 | 545.2 | 0.01 % | 68.2 | 0.0 | 0.0 % | 20.5 % | 0.0 % |

## Call breakdown (agent nodes)

| call | kind | wave | matrix | host per iter (us) | host share | GPU per iter (us) | GPU share | GPU/host |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| planner-seed | llm | 0 | 3584 | 180,272.6 | 16.73 % | 87,038.4 | 16.14 % | 48.28 % |
| critic-a | llm | 0 | 4096 | 239,286.4 | 22.2 % | 121,605.4 | 22.55 % | 50.82 % |
| critic-b | llm | 0 | 4096 | 239,022.0 | 22.18 % | 121,946.0 | 22.61 % | 51.02 % |
| planner-tool | tool | 1 | 256 | 376.8 | 0.03 % | 0.0 | 0.0 % | 0.0 % |
| critic-merge | llm | 1 | 4096 | 239,247.8 | 22.2 % | 121,558.1 | 22.54 % | 50.81 % |
| planner-final | llm | 2 | 3584 | 178,196.1 | 16.54 % | 87,181.1 | 16.16 % | 48.92 % |
| <dag> | dag |  |  | 1,223.2 | 0.11 % | 0.0 | 0.0 % | 0.0 % |

## CUDA runtime API inside the measured window

| API | calls | total (us) | share of wall |
|---|---:|---:|---:|
| cudaEventSynchronize | 400 | 3,950,550.4 | 45.82 % |
| cudaLaunchKernel | 22864 | 107,179.3 | 1.24 % |
| cudaMemsetAsync | 2304 | 8,371.4 | 0.1 % |
| cuLaunchKernel | 1536 | 7,056.4 | 0.08 % |
| cudaEventRecord | 880 | 4,192.3 | 0.05 % |
| cudaEventCreateWithFlags | 800 | 2,004.8 | 0.02 % |
| cudaMemcpyAsync | 80 | 1,928.1 | 0.02 % |
| cudaEventDestroy | 800 | 1,138.4 | 0.01 % |
| cuKernelGetFunction | 1536 | 746.8 | 0.01 % |
| cudaEventQuery | 80 | 375.2 | 0.0 % |
| cudaStreamIsCapturing | 120 | 114.4 | 0.0 % |
| cudaDeviceSynchronize | 8 | 74.8 | 0.0 % |

## Kernel families by process (G03)

| process | family | instances | GPU total (us) | share |
|---|---|---:|---:|---:|
| mir_operator:LinearOp | gemm | 3840 | 2,855,280.2 | 66.18 % |
| mir_operator:RMSNormOp | copy | 5120 | 382,813.5 | 8.87 % |
| mir_operator:RMSNormOp | elementwise_unary | 5120 | 308,146.5 | 7.14 % |
| mir_operator:RMSNormOp | elementwise_binary | 5120 | 292,317.1 | 6.78 % |
| mir_operator:TransposeOp | copy | 1280 | 265,052.5 | 6.14 % |
| mir_operator:RMSNormOp | reduce | 2560 | 78,865.1 | 1.83 % |
| d2h_stage | memcpy | 40 | 53,311.2 | 1.24 % |
| h2d_stage | memcpy | 40 | 51,479.9 | 1.19 % |
| mir_operator:AddOp | elementwise_binary | 1280 | 22,583.0 | 0.52 % |
| mir_operator:LinearOp | memset | 2304 | 2,868.8 | 0.07 % |
| weight_init | rng_init | 40 | 1,176.5 | 0.03 % |
| weight_init | elementwise_binary | 40 | 737.6 | 0.02 % |

## Kernel launch order, representative iteration 1 (G03)

| # | call | process | kind | family | GPU (us) | launch latency (us) | grid | block |
|---:|---|---|---|---|---:|---:|---|---|
| 1 | planner-seed | h2d_stage | memcpy | memcpy | 1,088.1 | 24.9 | 0x0x0 | 0x0x0 |
| 2 | planner-seed | weight_init | kernel | rng_init | 25.1 | 90.4 | 768x1x1 | 256x1x1 |
| 3 | planner-seed | weight_init | kernel | elementwise_binary | 14.0 | 8.6 | 12544x1x1 | 128x1x1 |
| 4 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 84.9 | 14.9 | 12544x1x1 | 128x1x1 |
| 5 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 75.0 | 47.2 | 12544x1x1 | 128x1x1 |
| 6 | planner-seed | mir_operator:RMSNormOp:6 | kernel | reduce | 20.1 | 83.5 | 224x1x1 | 32x16x1 |
| 7 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 71.8 | 4x1x1 | 128x1x1 |
| 8 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 38.4 | 4x1x1 | 128x1x1 |
| 9 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 85.9 | 12.4 | 50176x1x1 | 128x1x1 |
| 10 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 54.6 | 72.4 | 12544x1x1 | 128x1x1 |
| 11 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 39.8 | 98.9 | 12544x1x1 | 128x1x1 |
| 12 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 75.1 | 125.1 | 12544x1x1 | 128x1x1 |
| 13 | planner-seed | mir_operator:RMSNormOp:6 | kernel | reduce | 21.5 | 186.0 | 224x1x1 | 32x16x1 |
| 14 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 196.0 | 4x1x1 | 128x1x1 |
| 15 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 186.1 | 4x1x1 | 128x1x1 |
| 16 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 87.5 | 175.0 | 50176x1x1 | 128x1x1 |
| 17 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 55.8 | 248.8 | 12544x1x1 | 128x1x1 |
| 18 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 40.2 | 282.1 | 12544x1x1 | 128x1x1 |
| 19 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 75.9 | 310.0 | 12544x1x1 | 128x1x1 |
| 20 | planner-seed | mir_operator:RMSNormOp:6 | kernel | reduce | 21.1 | 372.6 | 224x1x1 | 32x16x1 |
| 21 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 383.6 | 4x1x1 | 128x1x1 |
| 22 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 374.0 | 4x1x1 | 128x1x1 |
| 23 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 86.7 | 363.2 | 50176x1x1 | 128x1x1 |
| 24 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 54.2 | 436.5 | 12544x1x1 | 128x1x1 |
| 25 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 42.1 | 471.8 | 12544x1x1 | 128x1x1 |
| 26 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 76.1 | 502.3 | 12544x1x1 | 128x1x1 |
| 27 | planner-seed | mir_operator:RMSNormOp:6 | kernel | reduce | 20.6 | 565.7 | 224x1x1 | 32x16x1 |
| 28 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 576.5 | 4x1x1 | 128x1x1 |
| 29 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 567.3 | 4x1x1 | 128x1x1 |
| 30 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 86.7 | 556.9 | 50176x1x1 | 128x1x1 |
| 31 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 54.8 | 630.1 | 12544x1x1 | 128x1x1 |
| 32 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 39.3 | 666.9 | 12544x1x1 | 128x1x1 |
| 33 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 75.9 | 692.7 | 12544x1x1 | 128x1x1 |
| 34 | planner-seed | mir_operator:RMSNormOp:6 | kernel | reduce | 21.1 | 755.7 | 224x1x1 | 32x16x1 |
| 35 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 766.6 | 4x1x1 | 128x1x1 |
| 36 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 757.1 | 4x1x1 | 128x1x1 |
| 37 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 86.3 | 746.7 | 50176x1x1 | 128x1x1 |
| 38 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 54.1 | 819.6 | 12544x1x1 | 128x1x1 |
| 39 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 40.7 | 855.6 | 12544x1x1 | 128x1x1 |
| 40 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 75.3 | 884.7 | 12544x1x1 | 128x1x1 |
| 41 | planner-seed | mir_operator:RMSNormOp:6 | kernel | reduce | 20.2 | 947.4 | 224x1x1 | 32x16x1 |
| 42 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 957.7 | 4x1x1 | 128x1x1 |
| 43 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 948.3 | 4x1x1 | 128x1x1 |
| 44 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 86.2 | 938.0 | 50176x1x1 | 128x1x1 |
| 45 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 56.9 | 1,010.7 | 12544x1x1 | 128x1x1 |
| 46 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 40.3 | 1,047.1 | 12544x1x1 | 128x1x1 |
| 47 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 76.8 | 1,069.9 | 12544x1x1 | 128x1x1 |
| 48 | planner-seed | mir_operator:RMSNormOp:6 | kernel | reduce | 20.4 | 1,130.9 | 224x1x1 | 32x16x1 |
| 49 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 1,140.7 | 4x1x1 | 128x1x1 |
| 50 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 1,130.5 | 4x1x1 | 128x1x1 |
| 51 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 86.7 | 1,119.7 | 50176x1x1 | 128x1x1 |
| 52 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 53.9 | 1,191.9 | 12544x1x1 | 128x1x1 |
| 53 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 39.6 | 1,226.7 | 12544x1x1 | 128x1x1 |
| 54 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 75.8 | 1,254.3 | 12544x1x1 | 128x1x1 |
| 55 | planner-seed | mir_operator:RMSNormOp:6 | kernel | reduce | 20.5 | 1,317.7 | 224x1x1 | 32x16x1 |
| 56 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 1.2 | 1,328.3 | 4x1x1 | 128x1x1 |
| 57 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_unary | 1.0 | 1,318.8 | 4x1x1 | 128x1x1 |
| 58 | planner-seed | mir_operator:RMSNormOp:6 | kernel | elementwise_binary | 87.2 | 1,308.3 | 50176x1x1 | 128x1x1 |
| 59 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 56.4 | 1,382.0 | 12544x1x1 | 128x1x1 |
| 60 | planner-seed | mir_operator:RMSNormOp:6 | kernel | copy | 39.6 | 1,420.5 | 12544x1x1 | 128x1x1 |
| … | | 3288 more rows in kernel_launch_order_representative_iteration.csv | | | | | | |

## Per call/process summary (medians over measured iterations)

| call | process | op | host median (us) | host min/max (us) | GPU median (us) | top CUDA API | kernels |
|---|---|---:|---:|---:|---:|---|---:|
| planner-seed | adapter_dispatch |  | 914.1 | 833.4/942.2 | 0.0 |  | 0 |
| planner-seed | token_preprocess_cpu |  | 386.8 | 322.0/406.7 | 0.0 |  | 0 |
| planner-seed | host_input_generate |  | 88,650.0 | 85,825.9/100,023.7 | 0.0 | cudaEventQuery | 0 |
| planner-seed | h2d_stage |  | 1,225.7 | 1,176.5/1,877.8 | 1,060.6 | cudaEventSynchronize | 0 |
| planner-seed | weight_init |  | 208.7 | 182.7/496.7 | 39.1 | cudaLaunchKernel | 2 |
| planner-seed | mir_operator:RMSNormOp | 6 | 9,417.9 | 9,299.8/9,806.0 | 9,107.9 | cudaEventSynchronize | 224 |
| planner-seed | inter_operator_dispatch |  | 14.7 | 5.6/41.7 | 0.0 |  | 0 |
| planner-seed | mir_operator:AddOp | 7 | 595.2 | 541.9/823.2 | 431.9 | cudaLaunchKernel | 32 |
| planner-seed | mir_operator:RMSNormOp | 8 | 9,218.7 | 9,187.8/9,271.3 | 8,992.0 | cudaEventSynchronize | 224 |
| planner-seed | mir_operator:LinearOp | 10 | 20,077.9 | 20,050.8/20,439.0 | 19,901.1 | cudaEventSynchronize | 32 |
| planner-seed | mir_operator:LinearOp | 11 | 20,136.8 | 19,927.2/20,462.9 | 20,024.2 | cudaEventSynchronize | 32 |
| planner-seed | mir_operator:LinearOp | 12 | 20,560.3 | 19,793.2/21,219.0 | 20,449.4 | cudaEventSynchronize | 32 |
| planner-seed | mir_operator:ViewOp | 13 | 167.2 | 138.7/219.9 | 0.0 | cudaEventRecord | 0 |
| planner-seed | mir_operator:TransposeOp | 14 | 5,858.7 | 5,420.8/6,370.2 | 5,719.8 | cudaEventSynchronize | 32 |
| planner-seed | pre_d2h_alloc |  | 23.5 | 17.7/32.9 | 0.0 |  | 0 |
| planner-seed | d2h_stage |  | 1,171.4 | 1,146.0/1,212.2 | 1,104.8 | cudaEventSynchronize | 0 |
| planner-seed | checksum_complete |  | 92.5 | 80.0/109.5 | 0.0 | cudaEventDestroy | 0 |
| critic-a | adapter_dispatch |  | 948.9 | 834.4/1,121.8 | 0.0 |  | 0 |
| critic-a | token_preprocess_cpu |  | 354.1 | 316.3/410.1 | 0.0 |  | 0 |
| critic-a | host_input_generate |  | 113,978.4 | 108,960.2/117,808.6 | 0.0 | cudaEventQuery | 0 |
| critic-a | h2d_stage |  | 1,539.8 | 1,518.3/1,656.2 | 1,386.4 | cudaEventSynchronize | 0 |
| critic-a | weight_init |  | 212.0 | 182.1/220.8 | 52.9 | cudaLaunchKernel | 2 |
| critic-a | mir_operator:RMSNormOp | 6 | 16,533.4 | 16,099.7/16,602.7 | 16,258.6 | cudaEventSynchronize | 224 |
| critic-a | inter_operator_dispatch |  | 14.8 | 5.4/165.8 | 0.0 |  | 0 |
| critic-a | mir_operator:AddOp | 7 | 758.1 | 746.9/819.2 | 646.1 | cudaEventSynchronize | 32 |
| critic-a | mir_operator:RMSNormOp | 8 | 16,034.1 | 15,993.6/16,204.9 | 15,802.6 | cudaEventSynchronize | 224 |
| critic-a | mir_operator:LinearOp | 10 | 26,071.3 | 25,654.3/26,370.5 | 25,815.0 | cudaEventSynchronize | 32 |
| critic-a | mir_operator:LinearOp | 11 | 26,432.5 | 25,840.8/27,223.3 | 26,283.6 | cudaEventSynchronize | 32 |
| critic-a | mir_operator:LinearOp | 12 | 26,866.9 | 26,145.4/27,098.3 | 26,721.7 | cudaEventSynchronize | 32 |
| critic-a | mir_operator:ViewOp | 13 | 172.8 | 146.4/207.6 | 0.0 | cudaEventRecord | 0 |
| critic-a | mir_operator:TransposeOp | 14 | 7,397.6 | 7,314.2/7,876.5 | 7,250.4 | cudaEventSynchronize | 32 |
| critic-a | pre_d2h_alloc |  | 21.1 | 16.7/25.3 | 0.0 |  | 0 |
| critic-a | d2h_stage |  | 1,493.2 | 1,481.8/1,611.1 | 1,435.1 | cudaEventSynchronize | 0 |
| critic-a | checksum_complete |  | 88.5 | 75.7/108.2 | 0.0 | cudaEventDestroy | 0 |
| critic-b | adapter_dispatch |  | 944.3 | 851.6/1,182.5 | 0.0 |  | 0 |
| critic-b | token_preprocess_cpu |  | 320.6 | 251.2/388.0 | 0.0 |  | 0 |
| critic-b | host_input_generate |  | 113,853.5 | 109,978.6/117,498.4 | 0.0 | cudaEventQuery | 0 |
| critic-b | h2d_stage |  | 1,544.0 | 1,512.8/2,058.7 | 1,397.3 | cudaEventSynchronize | 0 |
| critic-b | weight_init |  | 195.7 | 189.5/221.0 | 53.6 | cudaLaunchKernel | 2 |
| critic-b | mir_operator:RMSNormOp | 6 | 16,341.7 | 16,080.6/16,509.5 | 15,988.8 | cudaEventSynchronize | 224 |
| critic-b | inter_operator_dispatch |  | 14.9 | 5.5/36.3 | 0.0 |  | 0 |
| critic-b | mir_operator:AddOp | 7 | 755.8 | 733.6/878.8 | 644.0 | cudaEventSynchronize | 32 |
| critic-b | mir_operator:RMSNormOp | 8 | 16,301.2 | 16,024.1/16,468.4 | 16,076.3 | cudaEventSynchronize | 224 |
| critic-b | mir_operator:LinearOp | 10 | 26,026.5 | 25,693.2/26,340.5 | 25,796.6 | cudaEventSynchronize | 32 |
| critic-b | mir_operator:LinearOp | 11 | 26,772.5 | 26,051.7/27,091.6 | 26,637.7 | cudaEventSynchronize | 32 |
| critic-b | mir_operator:LinearOp | 12 | 27,107.5 | 26,040.5/27,768.3 | 26,952.4 | cudaEventSynchronize | 32 |
| critic-b | mir_operator:ViewOp | 13 | 172.2 | 160.6/190.1 | 0.0 | cudaEventRecord | 0 |
| critic-b | mir_operator:TransposeOp | 14 | 7,344.4 | 6,922.7/7,496.8 | 7,192.9 | cudaEventSynchronize | 32 |
| critic-b | pre_d2h_alloc |  | 22.6 | 16.0/32.6 | 0.0 |  | 0 |
| critic-b | d2h_stage |  | 1,515.5 | 1,480.8/1,587.6 | 1,455.4 | cudaEventSynchronize | 0 |
| critic-b | checksum_complete |  | 88.4 | 76.2/105.7 | 0.0 | cudaEventDestroy | 0 |
| planner-tool | agent_tool_execute_cpu |  | 385.9 | 300.7/424.9 | 0.0 |  | 0 |
| critic-merge | adapter_dispatch |  | 1,423.7 | 1,384.6/1,687.7 | 0.0 |  | 0 |
| critic-merge | token_preprocess_cpu |  | 246.6 | 231.7/279.7 | 0.0 |  | 0 |
| critic-merge | host_input_generate |  | 114,651.7 | 109,007.4/117,049.9 | 0.0 | cudaEventQuery | 0 |
| critic-merge | h2d_stage |  | 1,533.5 | 1,524.8/1,559.0 | 1,377.3 | cudaEventSynchronize | 0 |
| critic-merge | weight_init |  | 198.0 | 180.2/220.9 | 53.5 | cudaLaunchKernel | 2 |
| critic-merge | mir_operator:RMSNormOp | 6 | 16,280.7 | 16,088.1/16,532.8 | 16,005.5 | cudaEventSynchronize | 224 |
| critic-merge | inter_operator_dispatch |  | 15.6 | 5.2/34.8 | 0.0 |  | 0 |
| critic-merge | mir_operator:AddOp | 7 | 759.0 | 737.1/829.9 | 644.9 | cudaEventSynchronize | 32 |
| critic-merge | mir_operator:RMSNormOp | 8 | 16,299.6 | 15,987.0/16,495.8 | 16,079.6 | cudaEventSynchronize | 224 |
| critic-merge | mir_operator:LinearOp | 10 | 26,230.8 | 25,653.3/26,497.8 | 25,977.0 | cudaEventSynchronize | 32 |
| critic-merge | mir_operator:LinearOp | 11 | 26,358.6 | 25,768.6/26,957.9 | 26,049.3 | cudaEventSynchronize | 32 |
| critic-merge | mir_operator:LinearOp | 12 | 27,023.8 | 25,769.7/27,586.3 | 26,848.0 | cudaEventSynchronize | 32 |
| critic-merge | mir_operator:ViewOp | 13 | 162.7 | 147.9/193.5 | 0.0 | cudaEventRecord | 0 |
| critic-merge | mir_operator:TransposeOp | 14 | 7,319.0 | 6,872.0/7,922.5 | 7,195.5 | cudaEventSynchronize | 32 |
| critic-merge | pre_d2h_alloc |  | 21.6 | 16.6/24.2 | 0.0 |  | 0 |
| critic-merge | d2h_stage |  | 1,537.8 | 1,488.5/1,778.0 | 1,477.4 | cudaEventSynchronize | 0 |
| critic-merge | checksum_complete |  | 94.1 | 75.5/103.2 | 0.0 | cudaEventDestroy | 0 |
| planner-final | adapter_dispatch |  | 917.7 | 830.9/1,122.7 | 0.0 |  | 0 |
| planner-final | token_preprocess_cpu |  | 373.7 | 298.3/408.2 | 0.0 |  | 0 |
| planner-final | host_input_generate |  | 88,578.9 | 82,905.7/90,101.8 | 0.0 | cudaEventQuery | 0 |
| planner-final | h2d_stage |  | 1,210.5 | 1,161.5/1,275.6 | 1,053.2 | cudaEventSynchronize | 0 |
| planner-final | weight_init |  | 212.8 | 153.1/215.3 | 40.0 | cudaLaunchKernel | 2 |
| planner-final | mir_operator:RMSNormOp | 6 | 9,327.4 | 9,252.6/9,760.3 | 9,042.8 | cudaEventSynchronize | 224 |
| planner-final | inter_operator_dispatch |  | 11.1 | 4.9/27.0 | 0.0 |  | 0 |
| planner-final | mir_operator:AddOp | 7 | 555.2 | 531.3/662.6 | 431.9 | cudaLaunchKernel | 32 |
| planner-final | mir_operator:RMSNormOp | 8 | 9,738.5 | 9,187.6/9,760.6 | 9,525.9 | cudaEventSynchronize | 224 |
| planner-final | mir_operator:LinearOp | 10 | 20,063.7 | 19,766.8/20,159.8 | 19,883.7 | cudaEventSynchronize | 32 |
| planner-final | mir_operator:LinearOp | 11 | 20,151.6 | 20,025.8/20,321.1 | 20,034.0 | cudaEventSynchronize | 32 |
| planner-final | mir_operator:LinearOp | 12 | 20,572.4 | 20,137.9/20,920.0 | 20,439.3 | cudaEventSynchronize | 32 |
| planner-final | mir_operator:ViewOp | 13 | 159.7 | 146.5/171.2 | 0.0 | cudaEventRecord | 0 |
| planner-final | mir_operator:TransposeOp | 14 | 5,879.7 | 5,433.8/6,280.9 | 5,730.4 | cudaEventSynchronize | 32 |
| planner-final | pre_d2h_alloc |  | 19.1 | 17.3/32.6 | 0.0 |  | 0 |
| planner-final | d2h_stage |  | 1,196.2 | 1,145.2/1,357.6 | 1,130.9 | cudaEventSynchronize | 0 |
| planner-final | checksum_complete |  | 86.6 | 70.7/99.8 | 0.0 | cudaEventDestroy | 0 |
| <dag> | dag_schedule_gap |  | 45.5 | 11.3/1,004.9 | 0.0 |  | 0 |
| <dag> | iteration_tail_sync |  | 65.5 | 48.6/100.8 | 0.0 | cudaDeviceSynchronize | 0 |

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

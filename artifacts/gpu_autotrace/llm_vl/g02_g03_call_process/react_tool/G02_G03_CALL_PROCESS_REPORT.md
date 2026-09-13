# G02/G03 call-wise process attribution: `react_tool`

Lineage `h22-gpu-autotrace`, workflow w02. Consumes the w01 trace only; no re-timing.
Host events aligned to the nsys clock by a constant offset fitted on 13104 operator pairs (spread 36.8 us).

## Conservation

| Quantity | Value |
|---|---:|
| Measured iterations | 3 |
| Sum of process segments minus iteration wall (max abs) | 0 ns |
| GPU work attributed here minus w01 attributed GPU | 0 ns |
| Unnamed gap time | 0.0 us |
| Pass | True |

## Process-type breakdown (share of measured wall)

| process | instances | host total (us) | host share | per instance (us) | GPU total (us) | GPU share | CUDA API share of host | GPU/host |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| inter_operator_dispatch | 13098 | 505,767.2 | 3.89 % | 38.6 | 5,642.6 | 0.18 % | 7.1 % | 1.1 % |
| mir_operator:decode_layer00 | 330 | 348,939.2 | 2.68 % | 1,057.4 | 78,968.1 | 2.5 % | 21.4 % | 22.6 % |
| mir_operator:decode_layer01 | 330 | 336,075.4 | 2.59 % | 1,018.4 | 79,232.4 | 2.51 % | 21.8 % | 23.6 % |
| mir_operator:decode_layer02 | 330 | 333,421.8 | 2.56 % | 1,010.4 | 79,181.2 | 2.51 % | 22.1 % | 23.7 % |
| mir_operator:decode_layer16 | 330 | 332,621.6 | 2.56 % | 1,007.9 | 78,823.3 | 2.49 % | 22.0 % | 23.7 % |
| mir_operator:decode_layer15 | 330 | 332,188.7 | 2.56 % | 1,006.6 | 79,085.7 | 2.5 % | 22.1 % | 23.8 % |
| mir_operator:decode_layer18 | 330 | 331,790.9 | 2.55 % | 1,005.4 | 78,515.2 | 2.48 % | 22.0 % | 23.7 % |
| mir_operator:decode_layer21 | 330 | 331,784.3 | 2.55 % | 1,005.4 | 78,564.4 | 2.49 % | 22.2 % | 23.7 % |
| mir_operator:decode_layer07 | 330 | 331,426.8 | 2.55 % | 1,004.3 | 78,928.6 | 2.5 % | 22.1 % | 23.8 % |
| mir_operator:decode_layer08 | 330 | 331,359.9 | 2.55 % | 1,004.1 | 78,906.5 | 2.5 % | 22.3 % | 23.8 % |
| mir_operator:decode_layer34 | 330 | 331,336.8 | 2.55 % | 1,004.1 | 79,055.2 | 2.5 % | 21.9 % | 23.9 % |
| mir_operator:decode_layer30 | 330 | 331,274.9 | 2.55 % | 1,003.9 | 79,073.5 | 2.5 % | 22.1 % | 23.9 % |
| mir_operator:decode_layer03 | 330 | 331,113.3 | 2.55 % | 1,003.4 | 78,806.7 | 2.49 % | 22.0 % | 23.8 % |
| mir_operator:decode_layer35 | 330 | 331,036.8 | 2.55 % | 1,003.1 | 78,465.5 | 2.48 % | 22.1 % | 23.7 % |
| mir_operator:decode_layer17 | 330 | 330,938.0 | 2.55 % | 1,002.8 | 79,036.1 | 2.5 % | 22.1 % | 23.9 % |
| mir_operator:decode_layer24 | 330 | 330,936.2 | 2.55 % | 1,002.8 | 78,395.9 | 2.48 % | 22.1 % | 23.7 % |
| mir_operator:decode_layer19 | 330 | 330,837.2 | 2.54 % | 1,002.5 | 79,110.2 | 2.5 % | 22.0 % | 23.9 % |
| mir_operator:decode_layer31 | 330 | 330,779.0 | 2.54 % | 1,002.4 | 78,521.6 | 2.48 % | 22.2 % | 23.7 % |
| mir_operator:decode_layer20 | 330 | 330,702.8 | 2.54 % | 1,002.1 | 78,845.8 | 2.5 % | 22.0 % | 23.8 % |
| mir_operator:decode_layer10 | 330 | 330,666.3 | 2.54 % | 1,002.0 | 78,856.9 | 2.5 % | 22.1 % | 23.8 % |
| mir_operator:decode_layer29 | 330 | 330,237.0 | 2.54 % | 1,000.7 | 78,792.7 | 2.49 % | 22.2 % | 23.9 % |
| mir_operator:decode_layer06 | 330 | 330,181.0 | 2.54 % | 1,000.5 | 79,231.5 | 2.51 % | 22.1 % | 24.0 % |
| mir_operator:decode_layer04 | 330 | 330,159.0 | 2.54 % | 1,000.5 | 79,048.9 | 2.5 % | 22.0 % | 23.9 % |
| mir_operator:decode_layer14 | 330 | 330,107.9 | 2.54 % | 1,000.3 | 78,762.8 | 2.49 % | 22.1 % | 23.9 % |
| mir_operator:decode_layer22 | 330 | 330,031.7 | 2.54 % | 1,000.1 | 78,924.6 | 2.5 % | 22.1 % | 23.9 % |
| mir_operator:decode_layer09 | 330 | 329,969.8 | 2.54 % | 999.9 | 79,115.4 | 2.5 % | 22.1 % | 24.0 % |
| mir_operator:decode_layer13 | 330 | 329,937.1 | 2.54 % | 999.8 | 78,575.9 | 2.49 % | 22.1 % | 23.8 % |
| mir_operator:decode_layer05 | 330 | 329,920.5 | 2.54 % | 999.8 | 78,727.2 | 2.49 % | 22.2 % | 23.9 % |
| mir_operator:decode_layer27 | 330 | 329,787.0 | 2.54 % | 999.4 | 78,983.3 | 2.5 % | 22.1 % | 23.9 % |
| mir_operator:decode_layer26 | 330 | 329,737.9 | 2.54 % | 999.2 | 79,011.7 | 2.5 % | 22.0 % | 24.0 % |
| mir_operator:decode_layer23 | 330 | 329,665.5 | 2.54 % | 999.0 | 78,916.2 | 2.5 % | 22.1 % | 23.9 % |
| mir_operator:decode_layer28 | 330 | 329,621.1 | 2.54 % | 998.9 | 79,296.1 | 2.51 % | 22.0 % | 24.1 % |
| mir_operator:decode_layer25 | 330 | 329,611.1 | 2.54 % | 998.8 | 79,218.5 | 2.51 % | 22.0 % | 24.0 % |
| mir_operator:decode_layer12 | 330 | 329,605.6 | 2.54 % | 998.8 | 78,853.8 | 2.5 % | 22.0 % | 23.9 % |
| mir_operator:decode_layer11 | 330 | 329,467.5 | 2.53 % | 998.4 | 78,805.1 | 2.49 % | 22.1 % | 23.9 % |
| mir_operator:decode_layer33 | 330 | 328,752.3 | 2.53 % | 996.2 | 79,016.0 | 2.5 % | 22.1 % | 24.0 % |
| mir_operator:decode_layer32 | 330 | 328,707.9 | 2.53 % | 996.1 | 79,384.7 | 2.51 % | 22.1 % | 24.2 % |
| mir_operator:decode_sample | 330 | 204,369.0 | 1.57 % | 619.3 | 2,327.2 | 0.07 % | 92.1 % | 1.1 % |
| mir_operator:decode_head | 330 | 85,423.5 | 0.66 % | 258.9 | 219,330.3 | 6.94 % | 18.9 % | 256.8 % |
| mir_operator:decode_embed | 330 | 17,418.1 | 0.13 % | 52.8 | 603.0 | 0.02 % | 23.0 % | 3.5 % |
| mir_operator:prefill_layer00 | 6 | 8,437.5 | 0.06 % | 1,406.3 | 2,476.2 | 0.08 % | 22.2 % | 29.3 % |
| mir_operator:prefill_layer01 | 6 | 7,800.5 | 0.06 % | 1,300.1 | 2,358.5 | 0.07 % | 22.1 % | 30.2 % |
| mir_operator:prefill_layer02 | 6 | 7,147.2 | 0.05 % | 1,191.2 | 2,347.4 | 0.07 % | 22.2 % | 32.8 % |
| mir_operator:prefill_layer03 | 6 | 6,729.3 | 0.05 % | 1,121.6 | 2,345.4 | 0.07 % | 22.6 % | 34.9 % |
| mir_operator:prefill_layer04 | 6 | 6,693.4 | 0.05 % | 1,115.6 | 2,334.0 | 0.07 % | 22.4 % | 34.9 % |
| mir_operator:prefill_layer05 | 6 | 6,645.0 | 0.05 % | 1,107.5 | 2,332.0 | 0.07 % | 22.7 % | 35.1 % |
| mir_operator:prefill_layer14 | 6 | 6,620.7 | 0.05 % | 1,103.5 | 2,343.5 | 0.07 % | 22.8 % | 35.4 % |
| mir_operator:prefill_layer13 | 6 | 6,609.2 | 0.05 % | 1,101.5 | 2,336.4 | 0.07 % | 22.4 % | 35.4 % |
| mir_operator:prefill_layer16 | 6 | 6,607.4 | 0.05 % | 1,101.2 | 2,331.4 | 0.07 % | 22.4 % | 35.3 % |
| mir_operator:prefill_layer30 | 6 | 6,599.2 | 0.05 % | 1,099.9 | 2,403.3 | 0.08 % | 22.5 % | 36.4 % |
| mir_operator:prefill_layer31 | 6 | 6,594.0 | 0.05 % | 1,099.0 | 2,329.9 | 0.07 % | 22.5 % | 35.3 % |
| mir_operator:prefill_layer15 | 6 | 6,589.6 | 0.05 % | 1,098.3 | 2,597.0 | 0.08 % | 22.7 % | 39.4 % |
| mir_operator:prefill_layer29 | 6 | 6,589.5 | 0.05 % | 1,098.3 | 2,390.1 | 0.08 % | 22.7 % | 36.3 % |
| mir_operator:prefill_layer32 | 6 | 6,562.1 | 0.05 % | 1,093.7 | 2,335.9 | 0.07 % | 22.8 % | 35.6 % |
| mir_operator:prefill_layer33 | 6 | 6,552.0 | 0.05 % | 1,092.0 | 2,339.0 | 0.07 % | 22.7 % | 35.7 % |
| mir_operator:prefill_layer12 | 6 | 6,550.7 | 0.05 % | 1,091.8 | 2,341.2 | 0.07 % | 22.5 % | 35.7 % |
| mir_operator:prefill_layer18 | 6 | 6,542.2 | 0.05 % | 1,090.4 | 2,374.2 | 0.08 % | 22.6 % | 36.3 % |
| mir_operator:prefill_layer28 | 6 | 6,535.3 | 0.05 % | 1,089.2 | 2,340.7 | 0.07 % | 22.7 % | 35.8 % |
| mir_operator:prefill_layer17 | 6 | 6,533.3 | 0.05 % | 1,088.9 | 2,347.1 | 0.07 % | 22.6 % | 35.9 % |
| mir_operator:prefill_layer20 | 6 | 6,529.4 | 0.05 % | 1,088.2 | 2,339.5 | 0.07 % | 22.7 % | 35.8 % |
| mir_operator:prefill_layer34 | 6 | 6,524.9 | 0.05 % | 1,087.5 | 2,346.4 | 0.07 % | 22.7 % | 36.0 % |
| mir_operator:prefill_layer35 | 6 | 6,515.6 | 0.05 % | 1,085.9 | 2,354.8 | 0.07 % | 22.7 % | 36.1 % |
| mir_operator:prefill_layer19 | 6 | 6,514.0 | 0.05 % | 1,085.7 | 2,348.1 | 0.07 % | 22.5 % | 36.0 % |
| mir_operator:prefill_layer11 | 6 | 6,510.4 | 0.05 % | 1,085.1 | 2,349.0 | 0.07 % | 22.9 % | 36.1 % |
| mir_operator:prefill_layer26 | 6 | 6,495.6 | 0.05 % | 1,082.6 | 2,343.3 | 0.07 % | 22.4 % | 36.1 % |
| mir_operator:prefill_layer27 | 6 | 6,450.0 | 0.05 % | 1,075.0 | 2,367.6 | 0.07 % | 22.7 % | 36.7 % |
| mir_operator:prefill_layer24 | 6 | 6,449.3 | 0.05 % | 1,074.9 | 2,341.2 | 0.07 % | 22.6 % | 36.3 % |
| mir_operator:prefill_layer25 | 6 | 6,442.2 | 0.05 % | 1,073.7 | 2,456.9 | 0.08 % | 22.7 % | 38.1 % |
| mir_operator:prefill_layer21 | 6 | 6,410.4 | 0.05 % | 1,068.4 | 2,347.4 | 0.07 % | 22.7 % | 36.6 % |
| mir_operator:prefill_layer10 | 6 | 6,406.7 | 0.05 % | 1,067.8 | 2,452.1 | 0.08 % | 22.7 % | 38.3 % |
| mir_operator:prefill_layer06 | 6 | 6,385.9 | 0.05 % | 1,064.3 | 2,392.1 | 0.08 % | 22.7 % | 37.5 % |
| mir_operator:prefill_layer22 | 6 | 6,379.9 | 0.05 % | 1,063.3 | 2,389.3 | 0.08 % | 22.9 % | 37.4 % |
| mir_operator:prefill_layer23 | 6 | 6,376.5 | 0.05 % | 1,062.7 | 2,333.6 | 0.07 % | 22.4 % | 36.6 % |
| mir_operator:prefill_layer07 | 6 | 6,358.8 | 0.05 % | 1,059.8 | 2,404.4 | 0.08 % | 22.8 % | 37.8 % |
| token_preprocess_cpu | 6 | 6,356.5 | 0.05 % | 1,059.4 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:prefill_layer08 | 6 | 6,282.3 | 0.05 % | 1,047.1 | 2,349.1 | 0.07 % | 22.7 % | 37.4 % |
| mir_operator:prefill_layer09 | 6 | 6,264.7 | 0.05 % | 1,044.1 | 2,343.0 | 0.07 % | 22.6 % | 37.4 % |
| mir_operator:prefill_sample | 6 | 5,317.5 | 0.04 % | 886.3 | 49.3 | 0.0 % | 94.5 % | 0.9 % |
| pre_d2h_alloc | 6 | 3,026.1 | 0.02 % | 504.4 | 4.5 | 0.0 % | 5.3 % | 0.1 % |
| dag_schedule_gap | 9 | 2,537.8 | 0.02 % | 282.0 | 0.0 | 0.0 % | 0.8 % | 0.0 % |
| mir_operator:prefill_head | 6 | 1,655.0 | 0.01 % | 275.8 | 5,635.1 | 0.18 % | 18.9 % | 340.5 % |
| weight_init | 6 | 1,151.3 | 0.01 % | 191.9 | 0.0 | 0.0 % | 1.3 % | 0.0 % |
| d2h_stage | 6 | 865.3 | 0.01 % | 144.2 | 5.6 | 0.0 % | 25.6 % | 0.6 % |
| agent_tool_execute_cpu | 3 | 859.3 | 0.01 % | 286.4 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| host_input_generate | 6 | 716.6 | 0.01 % | 119.4 | 0.0 | 0.0 % | 4.4 % | 0.0 % |
| h2d_stage | 6 | 690.7 | 0.01 % | 115.1 | 2.5 | 0.0 % | 33.5 % | 0.4 % |
| mir_operator:prefill_embed | 6 | 544.5 | 0.0 % | 90.7 | 10.5 | 0.0 % | 18.9 % | 1.9 % |
| iteration_tail_sync | 3 | 350.3 | 0.0 % | 116.8 | 0.0 | 0.0 % | 15.4 % | 0.0 % |
| checksum_complete | 6 | 277.4 | 0.0 % | 46.2 | 0.0 | 0.0 % | 6.4 % | 0.0 % |
| adapter_dispatch | 6 | 31.9 | 0.0 % | 5.3 | 0.0 | 0.0 % | 0.0 % | 0.0 % |

## Call breakdown (agent nodes)

| call | kind | wave | matrix | host per iter (us) | host share | GPU per iter (us) | GPU share | GPU/host |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| plan | llm | 0 | 768 | 1,850,265.6 | 42.7 % | 451,686.8 | 42.88 % | 24.41 % |
| lookup | tool | 1 | 256 | 286.4 | 0.01 % | 0.0 | 0.0 % | 0.0 % |
| answer | llm | 2 | 768 | 2,481,926.3 | 57.27 % | 601,616.3 | 57.12 % | 24.24 % |
| <dag> | dag |  |  | 962.7 | 0.02 % | 0.0 | 0.0 % | 0.0 % |

## CUDA runtime API inside the measured window

| API | calls | total (us) | share of wall |
|---|---:|---:|---:|
| cudaLaunchKernel | 527100 | 2,722,399.4 | 20.94 % |
| cudaStreamSynchronize | 678 | 181,575.4 | 1.4 % |
| cudaMemcpyAsync | 1020 | 14,016.3 | 0.11 % |
| cudaMemsetAsync | 1092 | 7,529.0 | 0.06 % |
| cuLaunchKernel | 1188 | 6,048.0 | 0.05 % |
| cuKernelGetFunction | 1188 | 670.3 | 0.01 % |
| cudaStreamIsCapturing | 390 | 514.9 | 0.0 % |
| cudaEventRecordWithFlags | 36 | 229.9 | 0.0 % |
| cudaEventCreateWithFlags | 24 | 73.5 | 0.0 % |
| cudaEventQuery | 36 | 47.1 | 0.0 % |
| cudaDeviceSynchronize | 3 | 32.3 | 0.0 % |
| cudaEventSynchronize | 12 | 31.0 | 0.0 % |

## Kernel families by process (G03)

| process | family | instances | GPU total (us) | share |
|---|---|---:|---:|---:|
| mir_operator:decode_head | gemv | 330 | 215,612.7 | 6.82 % |
| mir_operator:decode_layer32 | gemv | 2310 | 59,583.4 | 1.89 % |
| mir_operator:decode_layer01 | gemv | 2310 | 59,534.4 | 1.88 % |
| mir_operator:decode_layer28 | gemv | 2310 | 59,458.5 | 1.88 % |
| mir_operator:decode_layer02 | gemv | 2310 | 59,434.0 | 1.88 % |
| mir_operator:decode_layer25 | gemv | 2310 | 59,361.2 | 1.88 % |
| mir_operator:decode_layer09 | gemv | 2310 | 59,356.2 | 1.88 % |
| mir_operator:decode_layer15 | gemv | 2310 | 59,347.2 | 1.88 % |
| mir_operator:decode_layer06 | gemv | 2310 | 59,321.6 | 1.88 % |
| mir_operator:decode_layer34 | gemv | 2310 | 59,312.2 | 1.88 % |
| mir_operator:decode_layer30 | gemv | 2310 | 59,309.0 | 1.88 % |
| mir_operator:decode_layer17 | gemv | 2310 | 59,253.1 | 1.88 % |
| mir_operator:decode_layer19 | gemv | 2310 | 59,201.9 | 1.87 % |
| mir_operator:decode_layer04 | gemv | 2310 | 59,185.9 | 1.87 % |
| mir_operator:decode_layer10 | gemv | 2310 | 59,181.1 | 1.87 % |
| mir_operator:decode_layer23 | gemv | 2310 | 59,175.8 | 1.87 % |
| mir_operator:decode_layer00 | gemv | 2310 | 59,168.9 | 1.87 % |
| mir_operator:decode_layer29 | gemv | 2310 | 59,151.9 | 1.87 % |
| mir_operator:decode_layer11 | gemv | 2310 | 59,139.5 | 1.87 % |
| mir_operator:decode_layer22 | gemv | 2310 | 59,130.0 | 1.87 % |
| mir_operator:decode_layer26 | gemv | 2310 | 59,122.1 | 1.87 % |
| mir_operator:decode_layer33 | gemv | 2310 | 59,120.4 | 1.87 % |
| mir_operator:decode_layer27 | gemv | 2310 | 59,093.3 | 1.87 % |
| mir_operator:decode_layer20 | gemv | 2310 | 59,084.4 | 1.87 % |
| mir_operator:decode_layer03 | gemv | 2310 | 59,071.3 | 1.87 % |
| mir_operator:decode_layer07 | gemv | 2310 | 59,064.8 | 1.87 % |
| mir_operator:decode_layer16 | gemv | 2310 | 59,043.0 | 1.87 % |
| mir_operator:decode_layer05 | gemv | 2310 | 59,037.0 | 1.87 % |
| mir_operator:decode_layer12 | gemv | 2310 | 59,032.3 | 1.87 % |
| mir_operator:decode_layer14 | gemv | 2310 | 59,025.4 | 1.87 % |
| mir_operator:decode_layer08 | gemv | 2310 | 59,021.2 | 1.87 % |
| mir_operator:decode_layer18 | gemv | 2310 | 58,975.2 | 1.87 % |
| mir_operator:decode_layer13 | gemv | 2310 | 58,883.5 | 1.86 % |
| mir_operator:decode_layer21 | gemv | 2310 | 58,868.6 | 1.86 % |
| mir_operator:decode_layer35 | gemv | 2310 | 58,863.8 | 1.86 % |
| mir_operator:decode_layer31 | gemv | 2310 | 58,862.0 | 1.86 % |
| mir_operator:decode_layer24 | gemv | 2310 | 58,807.4 | 1.86 % |
| mir_operator:prefill_head | gemm | 6 | 5,526.3 | 0.17 % |
| mir_operator:decode_layer19 | elementwise_binary | 3630 | 5,205.7 | 0.16 % |
| mir_operator:decode_layer26 | elementwise_binary | 3630 | 5,131.9 | 0.16 % |
| mir_operator:decode_layer06 | elementwise_binary | 3630 | 5,124.8 | 0.16 % |
| mir_operator:decode_layer34 | elementwise_binary | 3630 | 5,108.7 | 0.16 % |
| mir_operator:decode_layer21 | elementwise_binary | 3630 | 5,107.2 | 0.16 % |
| mir_operator:decode_layer25 | elementwise_binary | 3630 | 5,104.6 | 0.16 % |
| mir_operator:decode_layer30 | elementwise_binary | 3630 | 5,103.4 | 0.16 % |
| mir_operator:decode_layer27 | elementwise_binary | 3630 | 5,102.8 | 0.16 % |
| mir_operator:decode_layer28 | elementwise_binary | 3630 | 5,098.1 | 0.16 % |
| mir_operator:decode_layer14 | elementwise_binary | 3630 | 5,096.8 | 0.16 % |
| mir_operator:decode_layer10 | elementwise_binary | 3630 | 5,095.7 | 0.16 % |
| mir_operator:decode_layer12 | elementwise_binary | 3630 | 5,088.0 | 0.16 % |
| mir_operator:decode_layer09 | elementwise_binary | 3630 | 5,083.3 | 0.16 % |
| mir_operator:decode_layer20 | elementwise_binary | 3630 | 5,080.3 | 0.16 % |
| mir_operator:decode_layer04 | elementwise_binary | 3630 | 5,080.0 | 0.16 % |
| mir_operator:decode_layer23 | elementwise_binary | 3630 | 5,079.6 | 0.16 % |
| mir_operator:decode_layer02 | elementwise_binary | 3630 | 5,079.6 | 0.16 % |
| mir_operator:decode_layer22 | elementwise_binary | 3630 | 5,078.9 | 0.16 % |
| mir_operator:decode_layer03 | elementwise_binary | 3630 | 5,074.0 | 0.16 % |
| mir_operator:decode_layer13 | elementwise_binary | 3630 | 5,071.7 | 0.16 % |
| mir_operator:decode_layer05 | elementwise_binary | 3630 | 5,070.0 | 0.16 % |
| mir_operator:decode_layer01 | elementwise_binary | 3630 | 5,069.8 | 0.16 % |
| mir_operator:decode_layer16 | elementwise_binary | 3630 | 5,060.0 | 0.16 % |
| mir_operator:decode_layer17 | elementwise_binary | 3630 | 5,058.0 | 0.16 % |
| mir_operator:decode_layer00 | elementwise_binary | 3630 | 5,057.8 | 0.16 % |
| mir_operator:decode_layer07 | elementwise_binary | 3630 | 5,056.0 | 0.16 % |
| mir_operator:decode_layer31 | elementwise_binary | 3630 | 5,055.6 | 0.16 % |
| mir_operator:decode_layer32 | elementwise_binary | 3630 | 5,053.6 | 0.16 % |
| mir_operator:decode_layer08 | elementwise_binary | 3630 | 5,045.8 | 0.16 % |
| mir_operator:decode_layer11 | elementwise_binary | 3630 | 5,045.4 | 0.16 % |
| mir_operator:decode_layer15 | elementwise_binary | 3630 | 5,044.3 | 0.16 % |
| mir_operator:decode_layer35 | elementwise_binary | 3630 | 5,042.7 | 0.16 % |
| mir_operator:decode_layer33 | elementwise_binary | 3630 | 5,042.3 | 0.16 % |
| mir_operator:decode_layer29 | elementwise_binary | 3630 | 5,039.6 | 0.16 % |
| mir_operator:decode_layer24 | elementwise_binary | 3630 | 5,022.9 | 0.16 % |
| mir_operator:decode_layer18 | elementwise_binary | 3630 | 5,004.6 | 0.16 % |
| mir_operator:decode_layer08 | concat | 1980 | 3,470.7 | 0.11 % |
| mir_operator:decode_layer22 | concat | 1980 | 3,437.0 | 0.11 % |
| mir_operator:decode_layer16 | concat | 1980 | 3,430.5 | 0.11 % |
| mir_operator:decode_layer26 | concat | 1980 | 3,397.1 | 0.11 % |
| mir_operator:decode_layer20 | concat | 1980 | 3,393.1 | 0.11 % |
| mir_operator:decode_layer12 | concat | 1980 | 3,390.5 | 0.11 % |
| mir_operator:decode_layer33 | concat | 1980 | 3,390.1 | 0.11 % |
| mir_operator:decode_layer06 | concat | 1980 | 3,382.7 | 0.11 % |
| mir_operator:decode_layer11 | concat | 1980 | 3,374.0 | 0.11 % |
| mir_operator:decode_layer07 | concat | 1980 | 3,372.7 | 0.11 % |
| mir_operator:decode_layer05 | concat | 1980 | 3,368.5 | 0.11 % |
| mir_operator:decode_layer32 | concat | 1980 | 3,367.8 | 0.11 % |
| mir_operator:decode_layer03 | concat | 1980 | 3,365.2 | 0.11 % |
| mir_operator:decode_layer15 | concat | 1980 | 3,364.4 | 0.11 % |
| mir_operator:decode_layer13 | concat | 1980 | 3,362.2 | 0.11 % |
| mir_operator:decode_layer09 | concat | 1980 | 3,359.6 | 0.11 % |
| mir_operator:decode_layer24 | concat | 1980 | 3,358.1 | 0.11 % |
| mir_operator:decode_layer04 | concat | 1980 | 3,355.3 | 0.11 % |
| mir_operator:decode_layer27 | concat | 1980 | 3,350.7 | 0.11 % |
| mir_operator:decode_layer17 | concat | 1980 | 3,345.7 | 0.11 % |
| mir_operator:decode_layer19 | concat | 1980 | 3,344.8 | 0.11 % |
| mir_operator:decode_layer31 | concat | 1980 | 3,343.0 | 0.11 % |
| mir_operator:decode_layer02 | concat | 1980 | 3,340.9 | 0.11 % |
| mir_operator:decode_layer01 | concat | 1980 | 3,338.7 | 0.11 % |
| mir_operator:decode_layer30 | concat | 1980 | 3,337.3 | 0.11 % |
| mir_operator:decode_layer00 | concat | 1980 | 3,336.7 | 0.11 % |
| mir_operator:decode_layer25 | concat | 1980 | 3,334.0 | 0.11 % |
| mir_operator:decode_layer29 | concat | 1980 | 3,333.2 | 0.11 % |
| mir_operator:decode_layer28 | concat | 1980 | 3,328.0 | 0.11 % |
| mir_operator:decode_layer23 | concat | 1980 | 3,327.0 | 0.11 % |
| mir_operator:decode_layer34 | concat | 1980 | 3,324.5 | 0.11 % |
| mir_operator:decode_layer21 | concat | 1980 | 3,324.2 | 0.11 % |
| mir_operator:decode_layer18 | concat | 1980 | 3,323.7 | 0.11 % |
| mir_operator:decode_layer10 | concat | 1980 | 3,323.0 | 0.11 % |
| mir_operator:decode_layer14 | concat | 1980 | 3,318.6 | 0.11 % |
| mir_operator:decode_layer35 | concat | 1980 | 3,304.1 | 0.1 % |
| mir_operator:decode_layer00 | attention | 660 | 3,241.1 | 0.1 % |
| mir_operator:decode_layer06 | attention | 660 | 3,231.7 | 0.1 % |
| mir_operator:decode_layer32 | attention | 660 | 3,230.8 | 0.1 % |
| mir_operator:decode_layer28 | attention | 660 | 3,206.9 | 0.1 % |
| mir_operator:decode_layer26 | attention | 660 | 3,194.9 | 0.1 % |
| mir_operator:decode_layer33 | attention | 660 | 3,189.8 | 0.1 % |
| mir_operator:decode_layer02 | attention | 660 | 3,189.3 | 0.1 % |
| mir_operator:decode_layer27 | attention | 660 | 3,188.2 | 0.1 % |
| mir_operator:decode_layer07 | attention | 660 | 3,185.4 | 0.1 % |
| mir_operator:decode_layer14 | attention | 660 | 3,183.6 | 0.1 % |
| mir_operator:decode_layer25 | attention | 660 | 3,180.1 | 0.1 % |
| mir_operator:decode_layer20 | attention | 660 | 3,179.8 | 0.1 % |
| mir_operator:decode_layer12 | attention | 660 | 3,174.6 | 0.1 % |
| mir_operator:decode_layer22 | attention | 660 | 3,171.8 | 0.1 % |
| mir_operator:decode_layer34 | attention | 660 | 3,170.7 | 0.1 % |
| mir_operator:decode_layer01 | attention | 660 | 3,169.2 | 0.1 % |
| mir_operator:decode_layer15 | attention | 660 | 3,162.6 | 0.1 % |
| mir_operator:decode_layer05 | attention | 660 | 3,160.3 | 0.1 % |
| mir_operator:decode_layer04 | attention | 660 | 3,159.0 | 0.1 % |
| mir_operator:decode_layer09 | attention | 660 | 3,156.9 | 0.1 % |
| mir_operator:decode_layer23 | attention | 660 | 3,153.4 | 0.1 % |
| mir_operator:decode_layer16 | attention | 660 | 3,152.9 | 0.1 % |
| mir_operator:decode_layer08 | attention | 660 | 3,150.2 | 0.1 % |
| mir_operator:decode_layer13 | attention | 660 | 3,145.6 | 0.1 % |
| mir_operator:decode_layer17 | attention | 660 | 3,144.8 | 0.1 % |
| mir_operator:decode_layer30 | attention | 660 | 3,140.2 | 0.1 % |
| mir_operator:decode_layer24 | attention | 660 | 3,137.8 | 0.1 % |
| mir_operator:decode_layer11 | attention | 660 | 3,136.6 | 0.1 % |
| mir_operator:decode_layer03 | attention | 660 | 3,135.4 | 0.1 % |
| mir_operator:decode_layer35 | attention | 660 | 3,133.7 | 0.1 % |
| mir_operator:decode_layer18 | attention | 660 | 3,131.5 | 0.1 % |
| mir_operator:decode_layer10 | attention | 660 | 3,131.3 | 0.1 % |
| mir_operator:decode_layer31 | attention | 660 | 3,130.7 | 0.1 % |
| mir_operator:decode_layer29 | attention | 660 | 3,126.6 | 0.1 % |
| mir_operator:decode_layer21 | attention | 660 | 3,125.6 | 0.1 % |
| mir_operator:decode_layer19 | attention | 660 | 3,125.4 | 0.1 % |
| mir_operator:decode_layer07 | elementwise_other | 2310 | 3,060.2 | 0.1 % |
| mir_operator:decode_layer08 | elementwise_other | 2310 | 3,055.9 | 0.1 % |
| mir_operator:decode_layer33 | elementwise_other | 2310 | 3,055.2 | 0.1 % |
| mir_operator:decode_layer16 | elementwise_other | 2310 | 3,055.0 | 0.1 % |
| mir_operator:decode_layer03 | elementwise_other | 2310 | 3,050.5 | 0.1 % |
| mir_operator:decode_layer21 | elementwise_other | 2310 | 3,042.4 | 0.1 % |
| mir_operator:decode_layer29 | elementwise_other | 2310 | 3,038.3 | 0.1 % |
| mir_operator:decode_layer26 | elementwise_other | 2310 | 3,038.1 | 0.1 % |
| mir_operator:decode_layer30 | elementwise_other | 2310 | 3,031.6 | 0.1 % |
| mir_operator:decode_layer00 | elementwise_other | 2310 | 3,031.3 | 0.1 % |
| mir_operator:decode_layer14 | elementwise_other | 2310 | 3,030.2 | 0.1 % |
| mir_operator:decode_layer09 | elementwise_other | 2310 | 3,028.5 | 0.1 % |
| mir_operator:decode_layer15 | elementwise_other | 2310 | 3,027.7 | 0.1 % |
| mir_operator:decode_layer02 | elementwise_other | 2310 | 3,026.1 | 0.1 % |
| mir_operator:decode_layer22 | elementwise_other | 2310 | 3,024.9 | 0.1 % |
| mir_operator:decode_layer23 | elementwise_other | 2310 | 3,024.1 | 0.1 % |
| mir_operator:decode_layer04 | elementwise_other | 2310 | 3,023.9 | 0.1 % |
| mir_operator:decode_layer12 | elementwise_other | 2310 | 3,022.7 | 0.1 % |
| mir_operator:decode_layer27 | elementwise_other | 2310 | 3,022.2 | 0.1 % |
| mir_operator:decode_layer25 | elementwise_other | 2310 | 3,020.4 | 0.1 % |
| mir_operator:decode_layer17 | elementwise_other | 2310 | 3,020.1 | 0.1 % |
| mir_operator:decode_layer19 | elementwise_other | 2310 | 3,019.3 | 0.1 % |
| mir_operator:decode_layer06 | elementwise_other | 2310 | 3,018.9 | 0.1 % |
| mir_operator:decode_layer20 | elementwise_other | 2310 | 3,018.3 | 0.1 % |
| mir_operator:decode_layer28 | elementwise_other | 2310 | 3,017.6 | 0.1 % |
| mir_operator:decode_layer11 | elementwise_other | 2310 | 3,016.8 | 0.1 % |
| mir_operator:decode_layer32 | elementwise_other | 2310 | 3,012.0 | 0.1 % |
| mir_operator:decode_layer18 | elementwise_other | 2310 | 3,004.6 | 0.1 % |
| mir_operator:decode_layer13 | elementwise_other | 2310 | 3,003.8 | 0.1 % |
| mir_operator:decode_layer10 | elementwise_other | 2310 | 3,002.5 | 0.1 % |
| mir_operator:decode_layer05 | elementwise_other | 2310 | 3,002.2 | 0.1 % |
| mir_operator:decode_layer01 | elementwise_other | 2310 | 3,000.2 | 0.09 % |
| mir_operator:decode_layer35 | elementwise_other | 2310 | 2,993.5 | 0.09 % |
| mir_operator:decode_layer31 | elementwise_other | 2310 | 2,991.7 | 0.09 % |
| mir_operator:decode_layer34 | elementwise_other | 2310 | 2,991.1 | 0.09 % |
| mir_operator:decode_layer24 | elementwise_other | 2310 | 2,986.4 | 0.09 % |
| inter_operator_dispatch | elementwise_other | 2010 | 2,730.9 | 0.09 % |
| mir_operator:decode_layer04 | copy | 1320 | 2,248.0 | 0.07 % |
| mir_operator:decode_layer27 | copy | 1320 | 2,239.0 | 0.07 % |
| mir_operator:decode_layer28 | copy | 1320 | 2,231.1 | 0.07 % |
| mir_operator:decode_layer19 | copy | 1320 | 2,227.4 | 0.07 % |
| mir_operator:decode_layer33 | copy | 1320 | 2,217.6 | 0.07 % |
| mir_operator:decode_layer25 | copy | 1320 | 2,216.7 | 0.07 % |
| mir_operator:decode_layer30 | copy | 1320 | 2,199.5 | 0.07 % |
| mir_operator:decode_layer17 | copy | 1320 | 2,199.3 | 0.07 % |
| mir_operator:decode_layer07 | copy | 1320 | 2,195.2 | 0.07 % |
| mir_operator:decode_layer23 | copy | 1320 | 2,194.8 | 0.07 % |
| mir_operator:decode_layer12 | copy | 1320 | 2,187.3 | 0.07 % |
| mir_operator:decode_layer08 | copy | 1320 | 2,186.9 | 0.07 % |
| mir_operator:decode_layer35 | copy | 1320 | 2,178.6 | 0.07 % |
| mir_operator:decode_layer34 | copy | 1320 | 2,175.3 | 0.07 % |
| mir_operator:decode_layer15 | copy | 1320 | 2,174.7 | 0.07 % |
| mir_operator:decode_layer26 | copy | 1320 | 2,173.3 | 0.07 % |
| mir_operator:decode_layer06 | copy | 1320 | 2,171.6 | 0.07 % |
| mir_operator:decode_layer03 | copy | 1320 | 2,169.9 | 0.07 % |
| mir_operator:decode_layer10 | copy | 1320 | 2,168.5 | 0.07 % |
| mir_operator:decode_layer32 | copy | 1320 | 2,167.7 | 0.07 % |
| mir_operator:decode_layer31 | copy | 1320 | 2,166.1 | 0.07 % |
| mir_operator:decode_layer14 | copy | 1320 | 2,165.7 | 0.07 % |
| mir_operator:decode_layer00 | copy | 1320 | 2,165.5 | 0.07 % |
| mir_operator:decode_layer09 | copy | 1320 | 2,165.1 | 0.07 % |
| mir_operator:decode_layer29 | copy | 1320 | 2,165.0 | 0.07 % |
| mir_operator:decode_layer01 | copy | 1320 | 2,164.2 | 0.07 % |
| mir_operator:decode_layer05 | copy | 1320 | 2,162.6 | 0.07 % |
| mir_operator:decode_layer13 | copy | 1320 | 2,159.6 | 0.07 % |
| mir_operator:decode_layer20 | copy | 1320 | 2,158.1 | 0.07 % |
| mir_operator:decode_layer02 | copy | 1320 | 2,155.6 | 0.07 % |
| mir_operator:decode_layer21 | copy | 1320 | 2,155.5 | 0.07 % |
| mir_operator:decode_layer18 | copy | 1320 | 2,152.9 | 0.07 % |
| mir_operator:decode_layer11 | copy | 1320 | 2,151.2 | 0.07 % |
| mir_operator:decode_layer22 | copy | 1320 | 2,151.0 | 0.07 % |
| mir_operator:decode_layer16 | copy | 1320 | 2,150.9 | 0.07 % |
| mir_operator:decode_layer24 | copy | 1320 | 2,150.0 | 0.07 % |
| mir_operator:prefill_layer15 | gemm | 42 | 1,937.0 | 0.06 % |
| mir_operator:decode_sample | reduce | 330 | 1,873.2 | 0.06 % |
| mir_operator:prefill_layer25 | gemm | 42 | 1,849.1 | 0.06 % |
| mir_operator:prefill_layer10 | gemm | 42 | 1,842.6 | 0.06 % |
| mir_operator:prefill_layer07 | gemm | 42 | 1,800.6 | 0.06 % |
| mir_operator:prefill_layer30 | gemm | 42 | 1,797.8 | 0.06 % |
| mir_operator:prefill_layer22 | gemm | 42 | 1,784.1 | 0.06 % |
| mir_operator:prefill_layer06 | gemm | 42 | 1,776.3 | 0.06 % |
| mir_operator:prefill_layer00 | gemm | 42 | 1,758.4 | 0.06 % |
| mir_operator:prefill_layer35 | gemm | 42 | 1,752.0 | 0.06 % |
| mir_operator:prefill_layer29 | gemm | 42 | 1,744.8 | 0.06 % |
| mir_operator:prefill_layer19 | gemm | 42 | 1,744.3 | 0.06 % |
| mir_operator:prefill_layer08 | gemm | 42 | 1,744.2 | 0.06 % |
| mir_operator:prefill_layer11 | gemm | 42 | 1,743.9 | 0.06 % |
| mir_operator:prefill_layer17 | gemm | 42 | 1,743.6 | 0.06 % |
| mir_operator:prefill_layer02 | gemm | 42 | 1,742.4 | 0.06 % |
| mir_operator:prefill_layer34 | gemm | 42 | 1,741.3 | 0.06 % |
| mir_operator:prefill_layer14 | gemm | 42 | 1,740.8 | 0.06 % |
| mir_operator:prefill_layer01 | gemm | 42 | 1,740.8 | 0.06 % |
| mir_operator:prefill_layer26 | gemm | 42 | 1,740.2 | 0.06 % |
| mir_operator:prefill_layer03 | gemm | 42 | 1,739.1 | 0.06 % |
| mir_operator:prefill_layer09 | gemm | 42 | 1,738.4 | 0.06 % |
| mir_operator:prefill_layer12 | gemm | 42 | 1,737.9 | 0.05 % |
| mir_operator:prefill_layer18 | gemm | 42 | 1,737.6 | 0.05 % |
| mir_operator:prefill_layer21 | gemm | 42 | 1,737.6 | 0.05 % |
| mir_operator:prefill_layer24 | gemm | 42 | 1,736.5 | 0.05 % |
| mir_operator:prefill_layer28 | gemm | 42 | 1,736.5 | 0.05 % |
| mir_operator:prefill_layer27 | gemm | 42 | 1,734.1 | 0.05 % |
| mir_operator:prefill_layer33 | gemm | 42 | 1,734.0 | 0.05 % |
| mir_operator:prefill_layer20 | gemm | 42 | 1,733.9 | 0.05 % |
| mir_operator:prefill_layer13 | gemm | 42 | 1,733.8 | 0.05 % |
| mir_operator:prefill_layer23 | gemm | 42 | 1,730.7 | 0.05 % |
| mir_operator:prefill_layer04 | gemm | 42 | 1,730.5 | 0.05 % |
| mir_operator:prefill_layer32 | gemm | 42 | 1,730.3 | 0.05 % |
| mir_operator:prefill_layer05 | gemm | 42 | 1,727.9 | 0.05 % |
| mir_operator:prefill_layer16 | gemm | 42 | 1,727.6 | 0.05 % |
| mir_operator:prefill_layer31 | gemm | 42 | 1,724.5 | 0.05 % |
| mir_operator:decode_layer17 | reduce | 660 | 1,512.0 | 0.05 % |
| mir_operator:decode_layer33 | reduce | 660 | 1,507.8 | 0.05 % |
| mir_operator:decode_layer25 | elementwise_unary | 1320 | 1,506.7 | 0.05 % |
| mir_operator:decode_layer27 | elementwise_unary | 1320 | 1,506.4 | 0.05 % |
| mir_operator:decode_layer34 | elementwise_unary | 1320 | 1,505.4 | 0.05 % |
| mir_operator:decode_layer17 | elementwise_unary | 1320 | 1,503.1 | 0.05 % |
| mir_operator:decode_layer32 | elementwise_unary | 1320 | 1,502.9 | 0.05 % |
| mir_operator:decode_layer04 | reduce | 660 | 1,501.6 | 0.05 % |
| mir_operator:decode_layer07 | reduce | 660 | 1,500.8 | 0.05 % |
| mir_operator:decode_layer19 | elementwise_unary | 1320 | 1,497.8 | 0.05 % |
| mir_operator:decode_layer00 | reduce | 660 | 1,497.2 | 0.05 % |
| mir_operator:decode_layer04 | elementwise_unary | 1320 | 1,495.2 | 0.05 % |
| mir_operator:decode_layer25 | reduce | 660 | 1,494.9 | 0.05 % |
| mir_operator:decode_layer06 | reduce | 660 | 1,493.8 | 0.05 % |
| mir_operator:decode_layer07 | elementwise_unary | 1320 | 1,493.6 | 0.05 % |
| mir_operator:decode_layer33 | elementwise_unary | 1320 | 1,492.9 | 0.05 % |
| mir_operator:decode_layer31 | elementwise_unary | 1320 | 1,491.7 | 0.05 % |
| mir_operator:decode_layer15 | elementwise_unary | 1320 | 1,488.8 | 0.05 % |
| mir_operator:decode_layer08 | reduce | 660 | 1,488.4 | 0.05 % |
| mir_operator:decode_layer10 | elementwise_unary | 1320 | 1,488.2 | 0.05 % |
| mir_operator:decode_layer19 | reduce | 660 | 1,487.9 | 0.05 % |
| mir_operator:decode_layer08 | elementwise_unary | 1320 | 1,487.5 | 0.05 % |
| mir_operator:decode_layer06 | elementwise_unary | 1320 | 1,486.4 | 0.05 % |
| mir_operator:decode_layer28 | elementwise_unary | 1320 | 1,485.6 | 0.05 % |
| mir_operator:decode_layer09 | elementwise_unary | 1320 | 1,485.6 | 0.05 % |
| mir_operator:decode_layer23 | reduce | 660 | 1,483.3 | 0.05 % |
| mir_operator:decode_layer12 | elementwise_unary | 1320 | 1,481.4 | 0.05 % |
| mir_operator:decode_layer31 | reduce | 660 | 1,480.7 | 0.05 % |
| mir_operator:decode_layer27 | reduce | 660 | 1,480.7 | 0.05 % |
| mir_operator:decode_layer01 | reduce | 660 | 1,480.6 | 0.05 % |
| mir_operator:decode_layer14 | reduce | 660 | 1,480.4 | 0.05 % |
| mir_operator:decode_layer09 | reduce | 660 | 1,480.2 | 0.05 % |
| mir_operator:decode_layer02 | elementwise_unary | 1320 | 1,480.1 | 0.05 % |
| mir_operator:decode_layer35 | elementwise_unary | 1320 | 1,479.0 | 0.05 % |
| mir_operator:decode_layer26 | reduce | 660 | 1,478.5 | 0.05 % |
| mir_operator:decode_layer23 | elementwise_unary | 1320 | 1,478.0 | 0.05 % |
| mir_operator:decode_layer03 | elementwise_unary | 1320 | 1,478.0 | 0.05 % |
| mir_operator:decode_layer30 | elementwise_unary | 1320 | 1,477.9 | 0.05 % |
| mir_operator:decode_layer13 | reduce | 660 | 1,477.3 | 0.05 % |
| mir_operator:decode_layer12 | reduce | 660 | 1,477.1 | 0.05 % |
| mir_operator:decode_layer15 | reduce | 660 | 1,476.1 | 0.05 % |
| mir_operator:decode_layer26 | elementwise_unary | 1320 | 1,475.7 | 0.05 % |
| mir_operator:decode_layer02 | reduce | 660 | 1,475.6 | 0.05 % |
| mir_operator:decode_layer01 | elementwise_unary | 1320 | 1,475.4 | 0.05 % |
| mir_operator:decode_layer30 | reduce | 660 | 1,474.7 | 0.05 % |
| mir_operator:decode_layer11 | elementwise_unary | 1320 | 1,473.6 | 0.05 % |
| mir_operator:decode_layer13 | elementwise_unary | 1320 | 1,472.1 | 0.05 % |
| mir_operator:decode_layer21 | reduce | 660 | 1,471.9 | 0.05 % |
| mir_operator:decode_layer29 | elementwise_unary | 1320 | 1,471.4 | 0.05 % |
| mir_operator:decode_layer20 | elementwise_unary | 1320 | 1,471.1 | 0.05 % |
| mir_operator:decode_layer22 | elementwise_unary | 1320 | 1,470.8 | 0.05 % |
| mir_operator:decode_layer28 | reduce | 660 | 1,470.5 | 0.05 % |
| mir_operator:decode_layer35 | reduce | 660 | 1,470.0 | 0.05 % |
| mir_operator:decode_layer00 | elementwise_unary | 1320 | 1,469.5 | 0.05 % |
| mir_operator:decode_layer21 | elementwise_unary | 1320 | 1,469.0 | 0.05 % |
| mir_operator:decode_layer11 | reduce | 660 | 1,468.0 | 0.05 % |
| mir_operator:decode_layer16 | elementwise_unary | 1320 | 1,468.0 | 0.05 % |
| mir_operator:decode_layer34 | reduce | 660 | 1,467.5 | 0.05 % |
| mir_operator:decode_layer24 | elementwise_unary | 1320 | 1,467.3 | 0.05 % |
| mir_operator:decode_layer29 | reduce | 660 | 1,466.8 | 0.05 % |
| mir_operator:decode_layer10 | reduce | 660 | 1,466.7 | 0.05 % |
| mir_operator:decode_layer32 | reduce | 660 | 1,466.6 | 0.05 % |
| mir_operator:decode_layer24 | reduce | 660 | 1,465.9 | 0.05 % |
| mir_operator:decode_layer05 | reduce | 660 | 1,463.3 | 0.05 % |
| mir_operator:decode_layer05 | elementwise_unary | 1320 | 1,463.3 | 0.05 % |
| mir_operator:decode_layer16 | reduce | 660 | 1,463.1 | 0.05 % |
| mir_operator:decode_layer18 | elementwise_unary | 1320 | 1,462.8 | 0.05 % |
| mir_operator:decode_layer03 | reduce | 660 | 1,462.4 | 0.05 % |
| mir_operator:decode_layer14 | elementwise_unary | 1320 | 1,462.2 | 0.05 % |
| mir_operator:decode_layer20 | reduce | 660 | 1,460.6 | 0.05 % |
| mir_operator:decode_layer22 | reduce | 660 | 1,460.2 | 0.05 % |
| mir_operator:decode_layer18 | reduce | 660 | 1,460.0 | 0.05 % |
| mir_operator:decode_head | elementwise_binary | 990 | 1,204.3 | 0.04 % |
| mir_operator:decode_head | copy | 660 | 1,065.7 | 0.03 % |
| inter_operator_dispatch | copy | 678 | 756.5 | 0.02 % |
| inter_operator_dispatch | elementwise_binary | 672 | 754.7 | 0.02 % |
| mir_operator:decode_head | elementwise_unary | 660 | 727.8 | 0.02 % |
| mir_operator:decode_head | reduce | 330 | 719.8 | 0.02 % |
| mir_operator:decode_embed | other | 330 | 603.0 | 0.02 % |
| inter_operator_dispatch | concat | 336 | 537.3 | 0.02 % |
| inter_operator_dispatch | memcpy | 660 | 452.7 | 0.01 % |
| inter_operator_dispatch | gemv | 336 | 410.4 | 0.01 % |
| mir_operator:decode_sample | memcpy | 330 | 335.3 | 0.01 % |
| mir_operator:prefill_layer00 | elementwise_binary | 66 | 183.0 | 0.01 % |
| mir_operator:prefill_layer18 | elementwise_binary | 66 | 169.4 | 0.01 % |
| mir_operator:prefill_layer01 | elementwise_binary | 66 | 166.5 | 0.01 % |
| mir_operator:prefill_layer27 | elementwise_binary | 66 | 158.7 | 0.01 % |
| mir_operator:prefill_layer32 | elementwise_binary | 66 | 154.1 | 0.0 % |
| mir_operator:prefill_layer04 | elementwise_binary | 66 | 153.6 | 0.0 % |
| mir_operator:prefill_layer02 | elementwise_binary | 66 | 153.5 | 0.0 % |
| mir_operator:prefill_layer06 | elementwise_binary | 66 | 153.4 | 0.0 % |
| mir_operator:prefill_layer03 | elementwise_binary | 66 | 153.4 | 0.0 % |
| mir_operator:prefill_layer15 | elementwise_binary | 66 | 153.3 | 0.0 % |
| mir_operator:prefill_layer10 | elementwise_binary | 66 | 153.3 | 0.0 % |
| mir_operator:prefill_layer14 | elementwise_binary | 66 | 153.2 | 0.0 % |
| mir_operator:prefill_layer26 | elementwise_binary | 66 | 153.2 | 0.0 % |
| mir_operator:prefill_layer29 | elementwise_binary | 66 | 153.1 | 0.0 % |
| mir_operator:prefill_layer07 | elementwise_binary | 66 | 153.1 | 0.0 % |
| mir_operator:prefill_layer11 | elementwise_binary | 66 | 153.0 | 0.0 % |
| mir_operator:prefill_layer20 | elementwise_binary | 66 | 152.9 | 0.0 % |
| mir_operator:prefill_layer08 | elementwise_binary | 66 | 152.9 | 0.0 % |
| mir_operator:prefill_layer09 | elementwise_binary | 66 | 152.9 | 0.0 % |
| mir_operator:prefill_layer24 | elementwise_binary | 66 | 152.9 | 0.0 % |
| mir_operator:prefill_layer21 | elementwise_binary | 66 | 152.8 | 0.0 % |
| mir_operator:prefill_layer35 | elementwise_binary | 66 | 152.8 | 0.0 % |
| mir_operator:prefill_layer17 | elementwise_binary | 66 | 152.7 | 0.0 % |
| mir_operator:prefill_layer13 | elementwise_binary | 66 | 152.7 | 0.0 % |
| mir_operator:prefill_layer31 | elementwise_binary | 66 | 152.7 | 0.0 % |
| mir_operator:prefill_layer05 | elementwise_binary | 66 | 152.6 | 0.0 % |
| mir_operator:prefill_layer28 | elementwise_binary | 66 | 152.6 | 0.0 % |
| mir_operator:prefill_layer16 | elementwise_binary | 66 | 152.5 | 0.0 % |
| mir_operator:prefill_layer22 | elementwise_binary | 66 | 152.5 | 0.0 % |
| mir_operator:prefill_layer19 | elementwise_binary | 66 | 152.4 | 0.0 % |
| mir_operator:prefill_layer12 | elementwise_binary | 66 | 152.4 | 0.0 % |
| mir_operator:prefill_layer25 | elementwise_binary | 66 | 152.4 | 0.0 % |
| mir_operator:prefill_layer23 | elementwise_binary | 66 | 152.3 | 0.0 % |
| mir_operator:prefill_layer33 | elementwise_binary | 66 | 152.3 | 0.0 % |
| mir_operator:prefill_layer34 | elementwise_binary | 66 | 152.3 | 0.0 % |
| mir_operator:prefill_layer30 | elementwise_binary | 66 | 152.3 | 0.0 % |
| mir_operator:prefill_layer00 | concat | 36 | 148.2 | 0.0 % |
| mir_operator:prefill_layer00 | elementwise_other | 42 | 138.8 | 0.0 % |
| mir_operator:decode_sample | memset | 330 | 118.8 | 0.0 % |
| mir_operator:prefill_layer15 | elementwise_other | 42 | 118.6 | 0.0 % |
| mir_operator:prefill_layer27 | elementwise_other | 42 | 115.4 | 0.0 % |
| mir_operator:prefill_layer27 | concat | 36 | 111.5 | 0.0 % |
| mir_operator:prefill_layer18 | elementwise_other | 42 | 109.0 | 0.0 % |
| mir_operator:prefill_layer18 | concat | 36 | 108.9 | 0.0 % |
| mir_operator:prefill_layer19 | concat | 36 | 108.2 | 0.0 % |
| mir_operator:prefill_layer08 | concat | 36 | 108.2 | 0.0 % |
| mir_operator:prefill_layer33 | concat | 36 | 108.0 | 0.0 % |
| mir_operator:prefill_layer30 | concat | 36 | 108.0 | 0.0 % |
| mir_operator:prefill_layer32 | concat | 36 | 107.9 | 0.0 % |
| mir_operator:prefill_layer01 | concat | 36 | 107.9 | 0.0 % |
| mir_operator:prefill_layer28 | concat | 36 | 107.8 | 0.0 % |
| mir_operator:prefill_layer02 | concat | 36 | 107.8 | 0.0 % |
| mir_operator:prefill_layer24 | concat | 36 | 107.7 | 0.0 % |
| mir_operator:prefill_layer31 | concat | 36 | 107.7 | 0.0 % |
| mir_operator:prefill_layer10 | concat | 36 | 107.7 | 0.0 % |
| mir_operator:prefill_layer22 | concat | 36 | 107.7 | 0.0 % |
| mir_operator:prefill_layer03 | concat | 36 | 107.6 | 0.0 % |
| mir_operator:prefill_layer25 | concat | 36 | 107.6 | 0.0 % |
| mir_operator:prefill_layer15 | concat | 36 | 107.6 | 0.0 % |
| mir_operator:prefill_layer16 | concat | 36 | 107.6 | 0.0 % |
| mir_operator:prefill_layer21 | concat | 36 | 107.5 | 0.0 % |
| mir_operator:prefill_layer29 | concat | 36 | 107.5 | 0.0 % |
| mir_operator:prefill_layer14 | concat | 36 | 107.4 | 0.0 % |
| mir_operator:prefill_layer17 | concat | 36 | 107.4 | 0.0 % |
| mir_operator:prefill_layer34 | concat | 36 | 107.4 | 0.0 % |
| mir_operator:prefill_layer09 | concat | 36 | 107.4 | 0.0 % |
| mir_operator:prefill_layer11 | concat | 36 | 107.3 | 0.0 % |
| mir_operator:prefill_layer26 | concat | 36 | 107.3 | 0.0 % |
| mir_operator:prefill_layer35 | concat | 36 | 107.2 | 0.0 % |
| mir_operator:prefill_layer12 | concat | 36 | 107.2 | 0.0 % |
| mir_operator:prefill_layer13 | concat | 36 | 107.2 | 0.0 % |
| mir_operator:prefill_layer04 | concat | 36 | 107.1 | 0.0 % |
| mir_operator:prefill_layer07 | concat | 36 | 107.0 | 0.0 % |
| mir_operator:prefill_layer05 | concat | 36 | 106.9 | 0.0 % |
| mir_operator:prefill_layer23 | concat | 36 | 106.9 | 0.0 % |
| mir_operator:prefill_layer06 | concat | 36 | 106.7 | 0.0 % |
| mir_operator:prefill_layer20 | concat | 36 | 106.7 | 0.0 % |
| mir_operator:prefill_layer09 | elementwise_other | 42 | 95.6 | 0.0 % |
| mir_operator:prefill_layer03 | elementwise_other | 42 | 95.5 | 0.0 % |
| mir_operator:prefill_layer05 | elementwise_other | 42 | 95.3 | 0.0 % |
| mir_operator:prefill_layer20 | elementwise_other | 42 | 95.3 | 0.0 % |
| mir_operator:prefill_layer31 | elementwise_other | 42 | 95.2 | 0.0 % |
| mir_operator:prefill_layer02 | elementwise_other | 42 | 95.2 | 0.0 % |
| mir_operator:prefill_layer07 | elementwise_other | 42 | 95.1 | 0.0 % |
| mir_operator:prefill_layer13 | elementwise_other | 42 | 95.1 | 0.0 % |
| mir_operator:prefill_layer06 | elementwise_other | 42 | 95.1 | 0.0 % |
| mir_operator:prefill_layer11 | elementwise_other | 42 | 95.0 | 0.0 % |
| mir_operator:prefill_layer33 | elementwise_other | 42 | 95.0 | 0.0 % |
| mir_operator:prefill_layer30 | elementwise_other | 42 | 94.9 | 0.0 % |
| mir_operator:prefill_layer22 | elementwise_other | 42 | 94.9 | 0.0 % |
| mir_operator:prefill_layer35 | elementwise_other | 42 | 94.9 | 0.0 % |
| mir_operator:prefill_layer04 | elementwise_other | 42 | 94.9 | 0.0 % |
| mir_operator:prefill_layer34 | elementwise_other | 42 | 94.8 | 0.0 % |
| mir_operator:prefill_layer21 | elementwise_other | 42 | 94.8 | 0.0 % |
| mir_operator:prefill_layer10 | elementwise_other | 42 | 94.8 | 0.0 % |
| mir_operator:prefill_layer19 | elementwise_other | 42 | 94.7 | 0.0 % |
| mir_operator:prefill_layer16 | elementwise_other | 42 | 94.7 | 0.0 % |
| mir_operator:prefill_layer23 | elementwise_other | 42 | 94.7 | 0.0 % |
| mir_operator:prefill_layer28 | elementwise_other | 42 | 94.7 | 0.0 % |
| mir_operator:prefill_layer17 | elementwise_other | 42 | 94.7 | 0.0 % |
| mir_operator:prefill_layer32 | elementwise_other | 42 | 94.7 | 0.0 % |
| mir_operator:prefill_layer01 | elementwise_other | 42 | 94.6 | 0.0 % |
| mir_operator:prefill_layer08 | elementwise_other | 42 | 94.6 | 0.0 % |
| mir_operator:prefill_layer29 | elementwise_other | 42 | 94.6 | 0.0 % |
| mir_operator:prefill_layer24 | elementwise_other | 42 | 94.6 | 0.0 % |
| mir_operator:prefill_layer25 | elementwise_other | 42 | 94.5 | 0.0 % |
| mir_operator:prefill_layer14 | elementwise_other | 42 | 94.3 | 0.0 % |
| mir_operator:prefill_layer12 | elementwise_other | 42 | 94.3 | 0.0 % |
| mir_operator:prefill_layer26 | elementwise_other | 42 | 94.2 | 0.0 % |
| mir_operator:prefill_layer06 | reduce | 24 | 87.4 | 0.0 % |
| mir_operator:prefill_layer29 | reduce | 24 | 81.5 | 0.0 % |
| mir_operator:prefill_layer00 | attention | 12 | 78.8 | 0.0 % |
| mir_operator:prefill_layer15 | copy | 24 | 78.6 | 0.0 % |
| mir_operator:prefill_layer22 | attention | 12 | 78.5 | 0.0 % |
| mir_operator:prefill_layer09 | attention | 12 | 78.5 | 0.0 % |
| mir_operator:prefill_layer10 | attention | 12 | 78.5 | 0.0 % |
| mir_operator:prefill_layer33 | attention | 12 | 78.5 | 0.0 % |
| mir_operator:prefill_layer06 | attention | 12 | 78.4 | 0.0 % |
| mir_operator:prefill_layer07 | attention | 12 | 78.4 | 0.0 % |
| mir_operator:prefill_layer01 | attention | 12 | 78.4 | 0.0 % |
| mir_operator:prefill_layer32 | attention | 12 | 78.3 | 0.0 % |
| mir_operator:prefill_layer25 | attention | 12 | 78.3 | 0.0 % |
| mir_operator:prefill_layer30 | attention | 12 | 78.3 | 0.0 % |
| mir_operator:prefill_layer05 | attention | 12 | 78.3 | 0.0 % |
| mir_operator:prefill_layer20 | attention | 12 | 78.3 | 0.0 % |
| mir_operator:prefill_layer34 | attention | 12 | 78.3 | 0.0 % |
| mir_operator:prefill_layer31 | attention | 12 | 78.3 | 0.0 % |
| mir_operator:prefill_layer11 | attention | 12 | 78.3 | 0.0 % |
| mir_operator:prefill_layer15 | attention | 12 | 78.3 | 0.0 % |
| mir_operator:prefill_layer29 | attention | 12 | 78.3 | 0.0 % |
| mir_operator:prefill_layer13 | attention | 12 | 78.3 | 0.0 % |
| mir_operator:prefill_layer35 | attention | 12 | 78.3 | 0.0 % |
| mir_operator:prefill_layer24 | attention | 12 | 78.2 | 0.0 % |
| mir_operator:prefill_layer04 | attention | 12 | 78.2 | 0.0 % |
| mir_operator:prefill_layer23 | attention | 12 | 78.2 | 0.0 % |
| mir_operator:prefill_layer12 | attention | 12 | 78.2 | 0.0 % |
| mir_operator:prefill_layer14 | attention | 12 | 78.2 | 0.0 % |
| mir_operator:prefill_layer17 | attention | 12 | 78.2 | 0.0 % |
| mir_operator:prefill_layer08 | attention | 12 | 78.1 | 0.0 % |
| mir_operator:prefill_layer21 | attention | 12 | 78.1 | 0.0 % |
| mir_operator:prefill_layer03 | attention | 12 | 78.1 | 0.0 % |
| mir_operator:prefill_layer28 | attention | 12 | 78.1 | 0.0 % |
| mir_operator:prefill_layer19 | attention | 12 | 78.1 | 0.0 % |
| mir_operator:prefill_layer27 | attention | 12 | 78.0 | 0.0 % |
| mir_operator:prefill_layer16 | attention | 12 | 78.0 | 0.0 % |
| mir_operator:prefill_layer34 | reduce | 24 | 78.0 | 0.0 % |
| mir_operator:prefill_layer02 | attention | 12 | 77.9 | 0.0 % |
| mir_operator:prefill_layer18 | attention | 12 | 77.9 | 0.0 % |
| mir_operator:prefill_layer26 | attention | 12 | 77.9 | 0.0 % |
| mir_operator:prefill_layer30 | reduce | 24 | 77.6 | 0.0 % |
| mir_operator:prefill_layer20 | reduce | 24 | 77.4 | 0.0 % |
| mir_operator:prefill_layer21 | reduce | 24 | 77.4 | 0.0 % |
| mir_operator:prefill_layer12 | reduce | 24 | 77.3 | 0.0 % |
| mir_operator:prefill_layer11 | reduce | 24 | 77.2 | 0.0 % |
| mir_operator:prefill_layer22 | reduce | 24 | 77.2 | 0.0 % |
| mir_operator:prefill_layer33 | reduce | 24 | 77.2 | 0.0 % |
| mir_operator:prefill_layer03 | reduce | 24 | 76.9 | 0.0 % |
| mir_operator:prefill_layer08 | reduce | 24 | 76.8 | 0.0 % |
| mir_operator:prefill_layer05 | reduce | 24 | 76.8 | 0.0 % |
| mir_operator:prefill_layer28 | reduce | 24 | 76.7 | 0.0 % |
| mir_operator:prefill_layer16 | reduce | 24 | 76.7 | 0.0 % |
| mir_operator:prefill_layer31 | reduce | 24 | 76.7 | 0.0 % |
| mir_operator:prefill_layer24 | reduce | 24 | 76.6 | 0.0 % |
| mir_operator:prefill_layer15 | reduce | 24 | 76.4 | 0.0 % |
| mir_operator:prefill_layer32 | reduce | 24 | 76.4 | 0.0 % |
| mir_operator:prefill_layer02 | reduce | 24 | 76.4 | 0.0 % |
| mir_operator:prefill_layer19 | reduce | 24 | 76.3 | 0.0 % |
| mir_operator:prefill_layer17 | reduce | 24 | 76.0 | 0.0 % |
| mir_operator:prefill_layer01 | reduce | 24 | 76.0 | 0.0 % |
| mir_operator:prefill_layer18 | reduce | 24 | 75.9 | 0.0 % |
| mir_operator:prefill_layer23 | reduce | 24 | 75.9 | 0.0 % |
| mir_operator:prefill_layer07 | reduce | 24 | 75.8 | 0.0 % |
| mir_operator:prefill_layer10 | reduce | 24 | 75.7 | 0.0 % |
| mir_operator:prefill_layer25 | reduce | 24 | 75.7 | 0.0 % |
| mir_operator:prefill_layer26 | reduce | 24 | 75.7 | 0.0 % |
| mir_operator:prefill_layer09 | reduce | 24 | 75.6 | 0.0 % |
| mir_operator:prefill_layer04 | reduce | 24 | 75.5 | 0.0 % |
| mir_operator:prefill_layer27 | reduce | 24 | 75.4 | 0.0 % |
| mir_operator:prefill_layer13 | reduce | 24 | 75.3 | 0.0 % |
| mir_operator:prefill_layer35 | reduce | 24 | 75.3 | 0.0 % |
| mir_operator:prefill_layer14 | reduce | 24 | 75.2 | 0.0 % |
| mir_operator:prefill_layer00 | reduce | 24 | 74.1 | 0.0 % |
| mir_operator:prefill_layer29 | copy | 24 | 64.5 | 0.0 % |
| mir_operator:prefill_layer29 | elementwise_unary | 24 | 55.4 | 0.0 % |
| mir_operator:prefill_layer16 | copy | 24 | 49.3 | 0.0 % |
| mir_operator:prefill_layer22 | copy | 24 | 49.3 | 0.0 % |
| mir_operator:prefill_layer34 | copy | 24 | 49.2 | 0.0 % |
| mir_operator:prefill_layer02 | copy | 24 | 49.2 | 0.0 % |
| mir_operator:prefill_layer11 | copy | 24 | 49.2 | 0.0 % |
| mir_operator:prefill_layer19 | copy | 24 | 49.2 | 0.0 % |
| mir_operator:prefill_layer21 | copy | 24 | 49.2 | 0.0 % |
| mir_operator:prefill_layer03 | copy | 24 | 49.2 | 0.0 % |
| mir_operator:prefill_layer08 | copy | 24 | 49.2 | 0.0 % |
| mir_operator:prefill_layer09 | copy | 24 | 49.2 | 0.0 % |
| mir_operator:prefill_layer10 | copy | 24 | 49.2 | 0.0 % |
| mir_operator:prefill_layer24 | copy | 24 | 49.2 | 0.0 % |
| mir_operator:prefill_layer05 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer06 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer14 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer23 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer07 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer25 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer26 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer32 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer04 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer17 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer27 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer01 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer28 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer30 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer33 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer00 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer18 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer31 | copy | 24 | 49.1 | 0.0 % |
| mir_operator:prefill_layer12 | copy | 24 | 49.0 | 0.0 % |
| mir_operator:prefill_layer13 | copy | 24 | 49.0 | 0.0 % |
| mir_operator:prefill_layer35 | copy | 24 | 49.0 | 0.0 % |
| mir_operator:prefill_layer20 | copy | 24 | 49.0 | 0.0 % |
| mir_operator:prefill_sample | reduce | 6 | 40.0 | 0.0 % |
| mir_operator:prefill_head | elementwise_binary | 18 | 39.4 | 0.0 % |
| mir_operator:prefill_layer00 | elementwise_unary | 24 | 35.5 | 0.0 % |
| mir_operator:prefill_layer08 | elementwise_unary | 24 | 34.9 | 0.0 % |
| mir_operator:prefill_layer31 | elementwise_unary | 24 | 34.9 | 0.0 % |
| mir_operator:prefill_layer06 | elementwise_unary | 24 | 34.9 | 0.0 % |
| mir_operator:prefill_layer23 | elementwise_unary | 24 | 34.9 | 0.0 % |
| mir_operator:prefill_layer07 | elementwise_unary | 24 | 34.9 | 0.0 % |
| mir_operator:prefill_layer28 | elementwise_unary | 24 | 34.9 | 0.0 % |
| mir_operator:prefill_layer30 | elementwise_unary | 24 | 34.9 | 0.0 % |
| mir_operator:prefill_layer14 | elementwise_unary | 24 | 34.9 | 0.0 % |
| mir_operator:prefill_layer35 | elementwise_unary | 24 | 34.9 | 0.0 % |
| mir_operator:prefill_layer04 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer03 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer18 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer21 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer24 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer22 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer26 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer01 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer02 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer34 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer05 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer10 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer11 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer16 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer25 | elementwise_unary | 24 | 34.8 | 0.0 % |
| mir_operator:prefill_layer19 | elementwise_unary | 24 | 34.7 | 0.0 % |
| mir_operator:prefill_layer09 | elementwise_unary | 24 | 34.7 | 0.0 % |
| mir_operator:prefill_layer13 | elementwise_unary | 24 | 34.7 | 0.0 % |
| mir_operator:prefill_layer27 | elementwise_unary | 24 | 34.7 | 0.0 % |
| mir_operator:prefill_layer32 | elementwise_unary | 24 | 34.7 | 0.0 % |
| mir_operator:prefill_layer33 | elementwise_unary | 24 | 34.7 | 0.0 % |
| mir_operator:prefill_layer20 | elementwise_unary | 24 | 34.7 | 0.0 % |
| mir_operator:prefill_layer12 | elementwise_unary | 24 | 34.7 | 0.0 % |
| mir_operator:prefill_layer15 | elementwise_unary | 24 | 34.7 | 0.0 % |
| mir_operator:prefill_layer17 | elementwise_unary | 24 | 34.6 | 0.0 % |
| mir_operator:prefill_head | reduce | 6 | 27.6 | 0.0 % |
| mir_operator:prefill_head | copy | 12 | 24.5 | 0.0 % |
| mir_operator:prefill_head | elementwise_unary | 12 | 17.3 | 0.0 % |
| mir_operator:prefill_layer10 | memset | 18 | 15.6 | 0.0 % |
| mir_operator:prefill_layer25 | memset | 18 | 15.4 | 0.0 % |
| mir_operator:prefill_layer21 | memset | 18 | 15.1 | 0.0 % |
| mir_operator:prefill_layer15 | memset | 18 | 12.6 | 0.0 % |
| mir_operator:prefill_layer18 | memset | 18 | 11.7 | 0.0 % |
| mir_operator:prefill_layer20 | memset | 18 | 11.3 | 0.0 % |
| mir_operator:prefill_layer23 | memset | 18 | 10.8 | 0.0 % |
| mir_operator:prefill_layer31 | memset | 18 | 10.8 | 0.0 % |
| mir_operator:prefill_layer26 | memset | 18 | 10.8 | 0.0 % |
| mir_operator:prefill_layer17 | memset | 18 | 10.8 | 0.0 % |
| mir_operator:prefill_layer24 | memset | 18 | 10.8 | 0.0 % |
| mir_operator:prefill_layer06 | memset | 18 | 10.8 | 0.0 % |
| mir_operator:prefill_layer03 | memset | 18 | 10.7 | 0.0 % |
| mir_operator:prefill_layer09 | memset | 18 | 10.7 | 0.0 % |
| mir_operator:prefill_layer27 | memset | 18 | 10.7 | 0.0 % |
| mir_operator:prefill_embed | other | 6 | 10.5 | 0.0 % |
| mir_operator:prefill_layer01 | memset | 18 | 10.4 | 0.0 % |
| mir_operator:prefill_layer29 | memset | 18 | 10.4 | 0.0 % |
| mir_operator:prefill_layer30 | memset | 18 | 10.4 | 0.0 % |
| mir_operator:prefill_layer35 | memset | 18 | 10.4 | 0.0 % |
| mir_operator:prefill_layer04 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer07 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer11 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer12 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer14 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer16 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer32 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer00 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer02 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer05 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer22 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer28 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer34 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer13 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer19 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer33 | memset | 18 | 10.3 | 0.0 % |
| mir_operator:prefill_layer08 | memset | 18 | 10.2 | 0.0 % |
| mir_operator:prefill_sample | memcpy | 6 | 7.2 | 0.0 % |
| d2h_stage | memcpy | 6 | 5.6 | 0.0 % |
| pre_d2h_alloc | memcpy | 12 | 4.5 | 0.0 % |
| h2d_stage | memcpy | 6 | 2.5 | 0.0 % |
| mir_operator:prefill_sample | memset | 6 | 2.1 | 0.0 % |

## Kernel launch order, representative iteration 2 (G03)

| # | call | process | kind | family | GPU (us) | launch latency (us) | grid | block |
|---:|---|---|---|---|---:|---:|---|---|
| 1 | plan | h2d_stage | memcpy | memcpy | 0.4 | 11.0 | 0x0x0 | 0x0x0 |
| 2 | plan | mir_operator:prefill_embed:0 | kernel | other | 1.7 | 15.3 | 192x1x1 | 256x1x1 |
| 3 | plan | inter_operator_dispatch | kernel | elementwise_other | 0.9 | 8.2 | 3x1x1 | 64x1x1 |
| 4 | plan | inter_operator_dispatch | kernel | elementwise_other | 1.0 | 7.1 | 1x1x1 | 128x1x1 |
| 5 | plan | inter_operator_dispatch | kernel | elementwise_other | 0.9 | 6.3 | 3x1x1 | 64x1x1 |
| 6 | plan | inter_operator_dispatch | kernel | copy | 2.4 | 8.5 | 2x1x1 | 128x1x1 |
| 7 | plan | inter_operator_dispatch | kernel | gemv | 1.3 | 8.4 | 6x2x3 | 256x1x1 |
| 8 | plan | inter_operator_dispatch | kernel | concat | 3.0 | 13.9 | 256x2x1 | 512x1x1 |
| 9 | plan | inter_operator_dispatch | kernel | elementwise_other | 1.8 | 6.4 | 72x1x1 | 128x1x1 |
| 10 | plan | inter_operator_dispatch | kernel | elementwise_binary | 1.1 | 6.0 | 72x1x1 | 128x1x1 |
| 11 | plan | inter_operator_dispatch | kernel | elementwise_other | 1.7 | 6.6 | 72x1x1 | 128x1x1 |
| 12 | plan | inter_operator_dispatch | kernel | elementwise_binary | 1.1 | 5.6 | 72x1x1 | 128x1x1 |
| 13 | plan | inter_operator_dispatch | kernel | copy | 1.1 | 5.9 | 72x1x1 | 128x1x1 |
| 14 | plan | inter_operator_dispatch | kernel | copy | 1.1 | 5.1 | 72x1x1 | 128x1x1 |
| 15 | plan | mir_operator:prefill_layer00:1 | kernel | copy | 2.5 | 7.4 | 768x1x1 | 128x1x1 |
| 16 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_unary | 1.7 | 5.5 | 384x1x1 | 128x1x1 |
| 17 | plan | mir_operator:prefill_layer00:1 | kernel | reduce | 4.5 | 6.3 | 12x1x1 | 32x16x1 |
| 18 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 1.1 | 5.8 | 1x1x1 | 128x1x1 |
| 19 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_unary | 1.2 | 5.5 | 1x1x1 | 128x1x1 |
| 20 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.4 | 5.6 | 1536x1x1 | 128x1x1 |
| 21 | plan | mir_operator:prefill_layer00:1 | kernel | copy | 1.5 | 5.4 | 384x1x1 | 128x1x1 |
| 22 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.6 | 5.3 | 768x1x1 | 128x1x1 |
| 23 | plan | mir_operator:prefill_layer00:1 | kernel | gemm | 16.8 | 7.5 | 24x4x1 | 128x1x1 |
| 24 | plan | mir_operator:prefill_layer00:1 | kernel | gemm | 5.1 | 6.0 | 12x1x8 | 128x1x1 |
| 25 | plan | mir_operator:prefill_layer00:1 | kernel | reduce | 1.7 | 6.7 | 8x12x1 | 32x16x1 |
| 26 | plan | mir_operator:prefill_layer00:1 | kernel | gemm | 4.7 | 5.6 | 12x1x8 | 128x1x1 |
| 27 | plan | mir_operator:prefill_layer00:1 | kernel | reduce | 1.6 | 5.6 | 8x12x1 | 32x16x1 |
| 28 | plan | mir_operator:prefill_layer00:1 | kernel | concat | 3.0 | 8.0 | 256x6x1 | 512x1x1 |
| 29 | plan | mir_operator:prefill_layer00:1 | kernel | concat | 2.9 | 6.3 | 256x6x1 | 512x1x1 |
| 30 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.3 | 5.6 | 768x1x1 | 128x1x1 |
| 31 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_other | 2.0 | 6.0 | 384x1x1 | 128x1x1 |
| 32 | plan | mir_operator:prefill_layer00:1 | kernel | concat | 3.8 | 5.8 | 256x2x1 | 512x1x1 |
| 33 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.3 | 5.4 | 768x1x1 | 128x1x1 |
| 34 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_other | 2.5 | 5.6 | 768x1x1 | 128x1x1 |
| 35 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 1.9 | 5.4 | 96x1x1 | 128x1x1 |
| 36 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_other | 1.8 | 5.5 | 48x1x1 | 128x1x1 |
| 37 | plan | mir_operator:prefill_layer00:1 | kernel | concat | 2.7 | 5.7 | 256x2x1 | 512x1x1 |
| 38 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 1.9 | 5.5 | 96x1x1 | 128x1x1 |
| 39 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_other | 1.9 | 5.3 | 96x1x1 | 128x1x1 |
| 40 | plan | mir_operator:prefill_layer00:1 | kernel | concat | 2.3 | 7.1 | 256x2x1 | 512x1x1 |
| 41 | plan | mir_operator:prefill_layer00:1 | kernel | concat | 2.3 | 5.8 | 256x2x1 | 512x1x1 |
| 42 | plan | mir_operator:prefill_layer00:1 | kernel | attention | 8.9 | 7.7 | 3x2x16 | 128x1x1 |
| 43 | plan | mir_operator:prefill_layer00:1 | kernel | attention | 3.8 | 8.2 | 768x1x1 | 128x1x1 |
| 44 | plan | mir_operator:prefill_layer00:1 | kernel | gemm | 16.9 | 8.5 | 32x3x1 | 128x1x1 |
| 45 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_other | 1.6 | 5.8 | 384x1x1 | 128x1x1 |
| 46 | plan | mir_operator:prefill_layer00:1 | kernel | copy | 2.5 | 6.3 | 768x1x1 | 128x1x1 |
| 47 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_unary | 1.7 | 5.4 | 384x1x1 | 128x1x1 |
| 48 | plan | mir_operator:prefill_layer00:1 | kernel | reduce | 4.5 | 5.5 | 12x1x1 | 32x16x1 |
| 49 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 1.1 | 5.4 | 1x1x1 | 128x1x1 |
| 50 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_unary | 1.2 | 5.5 | 1x1x1 | 128x1x1 |
| 51 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.4 | 5.4 | 1536x1x1 | 128x1x1 |
| 52 | plan | mir_operator:prefill_layer00:1 | kernel | copy | 1.5 | 5.2 | 384x1x1 | 128x1x1 |
| 53 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.4 | 5.4 | 768x1x1 | 128x1x1 |
| 54 | plan | mir_operator:prefill_layer00:1 | memset | memset | 0.6 | 10.3 | 0x0x0 | 0x0x0 |
| 55 | plan | mir_operator:prefill_layer00:1 | kernel | gemm | 79.2 | 6.5 | 24x22x2 | 128x1x1 |
| 56 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_other | 3.5 | 61.3 | 2064x1x1 | 128x1x1 |
| 57 | plan | mir_operator:prefill_layer00:1 | memset | memset | 0.6 | 32.1 | 0x0x0 | 0x0x0 |
| 58 | plan | mir_operator:prefill_layer00:1 | kernel | gemm | 76.2 | 29.1 | 24x22x2 | 128x1x1 |
| 59 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 3.9 | 85.0 | 2064x1x1 | 128x1x1 |
| 60 | plan | mir_operator:prefill_layer00:1 | memset | memset | 0.4 | 58.8 | 0x0x0 | 0x0x0 |
| … | | 176704 more rows in kernel_launch_order_representative_iteration.csv | | | | | | |

## Per call/process summary (medians over measured iterations)

| call | process | op | host median (us) | host min/max (us) | GPU median (us) | top CUDA API | kernels |
|---|---|---:|---:|---:|---:|---|---:|
| plan | adapter_dispatch |  | 4.6 | 4.4/4.9 | 0.0 |  | 0 |
| plan | token_preprocess_cpu |  | 881.3 | 794.8/1,190.6 | 0.0 |  | 0 |
| plan | host_input_generate |  | 109.5 | 99.9/115.1 | 0.0 | cudaEventQuery | 0 |
| plan | h2d_stage |  | 99.6 | 97.6/102.8 | 0.4 | cudaEventRecordWithFlags | 0 |
| plan | weight_init |  | 181.4 | 156.8/196.5 | 0.0 | cudaEventDestroy | 0 |
| plan | mir_operator:prefill_embed | 0 | 87.2 | 78.4/100.4 | 1.7 | cudaLaunchKernel | 1 |
| plan | inter_operator_dispatch |  | 20.5 | 17.0/1,716.1 | 0.0 | cudaLaunchKernel | 0.31 |
| plan | mir_operator:prefill_layer00 | 1 | 1,275.0 | 1,234.9/1,354.2 | 367.4 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer01 | 2 | 1,171.5 | 1,139.7/1,191.6 | 363.9 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer02 | 3 | 1,146.0 | 1,097.1/1,155.7 | 366.5 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer03 | 4 | 1,137.3 | 1,041.4/1,142.8 | 364.0 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer04 | 5 | 1,124.9 | 1,039.2/1,133.6 | 365.8 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer05 | 6 | 1,108.5 | 1,072.2/1,139.1 | 363.0 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer06 | 7 | 1,106.6 | 1,043.1/1,120.4 | 364.0 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer07 | 8 | 1,096.8 | 1,030.8/1,141.4 | 363.1 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer08 | 9 | 1,089.5 | 1,024.3/1,146.1 | 364.7 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer09 | 10 | 1,065.0 | 1,019.3/1,161.8 | 364.2 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer10 | 11 | 1,031.4 | 1,026.3/1,138.5 | 363.0 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer11 | 12 | 1,081.9 | 1,035.1/1,142.3 | 365.8 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer12 | 13 | 1,098.9 | 1,026.5/1,135.3 | 364.7 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer13 | 14 | 1,118.0 | 1,042.4/1,119.9 | 362.8 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer14 | 15 | 1,111.9 | 1,031.5/1,141.7 | 364.3 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer15 | 16 | 1,124.2 | 1,027.0/1,131.2 | 366.2 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer16 | 17 | 1,120.6 | 1,027.2/1,131.6 | 364.4 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer17 | 18 | 1,092.9 | 1,032.4/1,126.6 | 365.8 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer18 | 19 | 1,084.9 | 1,050.7/1,126.0 | 361.6 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer19 | 20 | 1,119.3 | 1,035.0/1,123.3 | 365.1 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer20 | 21 | 1,082.6 | 1,039.6/1,149.3 | 363.5 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer21 | 22 | 1,064.8 | 1,042.7/1,121.5 | 366.7 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer22 | 23 | 1,083.3 | 1,034.6/1,107.7 | 364.1 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer23 | 24 | 1,076.5 | 1,036.5/1,094.2 | 364.0 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer24 | 25 | 1,101.3 | 1,040.7/1,146.0 | 362.9 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer25 | 26 | 1,090.4 | 1,045.5/1,132.5 | 365.1 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer26 | 27 | 1,111.3 | 1,036.6/1,123.3 | 364.2 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer27 | 28 | 1,085.9 | 1,038.0/1,137.6 | 364.5 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer28 | 29 | 1,087.0 | 1,061.4/1,136.5 | 366.1 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer29 | 30 | 1,093.1 | 1,088.6/1,135.2 | 365.7 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer30 | 31 | 1,095.5 | 1,077.4/1,129.8 | 365.3 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer31 | 32 | 1,092.5 | 1,060.7/1,128.2 | 363.9 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer32 | 33 | 1,101.0 | 1,024.9/1,133.2 | 364.4 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer33 | 34 | 1,093.7 | 1,022.9/1,113.2 | 365.2 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer34 | 35 | 1,108.6 | 1,015.8/1,113.4 | 364.7 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_layer35 | 36 | 1,092.6 | 1,016.9/1,112.2 | 366.6 | cudaLaunchKernel | 45 |
| plan | mir_operator:prefill_head | 37 | 287.9 | 258.3/292.0 | 828.4 | cudaLaunchKernel | 9 |
| plan | mir_operator:prefill_sample | 38 | 781.4 | 769.6/786.4 | 8.3 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 39 | 58.3 | 46.2/60.0 | 2.1 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 40 | 1,081.5 | 994.0/1,116.1 | 243.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 41 | 985.2 | 955.7/1,065.5 | 238.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 42 | 997.7 | 951.3/1,040.3 | 238.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 43 | 1,031.7 | 951.2/1,040.9 | 238.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 44 | 1,022.9 | 951.1/1,046.6 | 238.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 45 | 1,007.1 | 941.1/1,044.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 46 | 1,032.5 | 993.4/1,033.3 | 237.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 47 | 1,029.7 | 1,004.9/1,030.7 | 238.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 48 | 1,013.8 | 995.0/1,083.1 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 49 | 992.6 | 985.0/1,010.6 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 50 | 999.4 | 945.6/1,015.7 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 51 | 996.4 | 993.4/1,008.9 | 238.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 52 | 1,006.1 | 985.5/1,011.1 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 53 | 1,003.5 | 1,001.3/1,023.3 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 54 | 996.5 | 994.7/1,027.7 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 55 | 1,002.5 | 999.8/1,023.6 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 56 | 1,008.7 | 995.5/1,032.4 | 238.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 57 | 999.8 | 996.2/1,035.2 | 237.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 58 | 1,024.6 | 1,006.5/1,031.3 | 237.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 59 | 1,031.6 | 1,006.6/1,031.9 | 238.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 60 | 1,032.0 | 1,018.0/1,035.0 | 238.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 61 | 1,042.3 | 1,028.3/1,090.3 | 238.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 62 | 1,034.1 | 1,026.9/1,035.2 | 238.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 63 | 1,027.4 | 1,027.2/1,029.8 | 238.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 64 | 1,032.5 | 1,027.6/1,038.8 | 238.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 65 | 1,033.8 | 1,033.2/1,038.3 | 238.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 66 | 1,030.5 | 1,025.7/1,042.7 | 238.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 67 | 1,027.5 | 1,022.5/1,027.7 | 238.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 68 | 1,027.5 | 1,012.1/1,031.9 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 69 | 1,025.6 | 1,018.9/1,029.1 | 238.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 70 | 1,018.4 | 1,007.1/1,019.2 | 238.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 71 | 996.2 | 995.2/1,021.9 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 72 | 997.4 | 995.0/1,024.1 | 238.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 73 | 1,011.8 | 997.1/1,028.0 | 238.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 74 | 998.9 | 996.2/1,032.5 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 75 | 998.6 | 996.1/1,026.2 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 76 | 264.5 | 257.7/269.6 | 642.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 77 | 586.3 | 569.1/604.4 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 78 | 52.8 | 47.5/56.4 | 1.7 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 79 | 1,064.1 | 1,025.9/1,108.3 | 240.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 80 | 1,024.3 | 957.2/1,050.8 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 81 | 1,014.3 | 1,002.0/1,035.0 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 82 | 970.9 | 954.3/1,005.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 83 | 957.5 | 939.1/1,003.8 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 84 | 975.4 | 932.4/1,003.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 85 | 1,005.4 | 911.0/1,032.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 86 | 1,016.9 | 917.3/1,042.7 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 87 | 1,005.2 | 918.3/1,005.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 88 | 997.7 | 983.3/1,006.3 | 279.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 89 | 1,001.8 | 999.8/1,020.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 90 | 1,024.7 | 994.6/1,034.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 91 | 1,026.7 | 997.9/1,038.9 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 92 | 1,026.7 | 992.9/1,029.4 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 93 | 1,020.6 | 997.6/1,036.9 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 94 | 1,017.5 | 995.3/1,034.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 95 | 1,022.2 | 993.5/1,047.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 96 | 1,023.2 | 994.8/1,036.9 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 97 | 1,022.4 | 1,017.8/1,033.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 98 | 1,033.5 | 1,027.3/1,049.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 99 | 1,030.4 | 1,024.0/1,040.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 100 | 1,030.9 | 1,024.2/1,031.4 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 101 | 1,029.3 | 1,023.9/1,033.9 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 102 | 1,024.9 | 1,014.8/1,031.4 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 103 | 1,021.7 | 997.4/1,035.2 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 104 | 1,028.5 | 997.6/1,035.5 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 105 | 1,018.7 | 1,014.4/1,026.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 106 | 1,007.5 | 1,006.1/1,034.4 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 107 | 1,004.4 | 991.0/1,033.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 108 | 1,009.7 | 987.1/1,032.3 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 109 | 1,008.5 | 996.6/1,052.9 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 110 | 1,009.5 | 989.1/1,030.3 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 111 | 1,005.1 | 944.5/1,035.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 112 | 1,007.6 | 911.8/1,039.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 113 | 984.1 | 905.5/1,031.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 114 | 960.3 | 911.9/1,034.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 115 | 265.0 | 226.3/276.2 | 661.8 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 116 | 620.2 | 605.1/731.0 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 117 | 57.1 | 41.3/61.0 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 118 | 1,101.1 | 975.3/1,107.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 119 | 1,039.8 | 945.6/1,114.3 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 120 | 1,011.8 | 947.2/1,059.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 121 | 1,000.9 | 952.5/1,043.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 122 | 1,008.6 | 946.0/1,031.4 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 123 | 1,012.6 | 935.1/1,043.7 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 124 | 1,009.3 | 936.4/1,036.9 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 125 | 1,003.1 | 967.3/1,039.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 126 | 1,003.4 | 983.7/1,042.2 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 127 | 1,007.0 | 1,005.2/1,037.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 128 | 1,027.5 | 1,022.5/1,034.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 129 | 1,031.8 | 1,025.0/1,044.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 130 | 1,034.7 | 994.9/1,054.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 131 | 1,031.3 | 997.8/1,033.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 132 | 1,008.1 | 1,000.4/1,033.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 133 | 1,011.1 | 992.5/1,025.9 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 134 | 1,005.9 | 995.3/1,026.6 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 135 | 1,003.2 | 994.9/1,025.9 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 136 | 1,011.0 | 958.5/1,020.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 137 | 1,010.5 | 913.3/1,026.9 | 238.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 138 | 1,017.1 | 910.4/1,025.6 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 139 | 1,013.4 | 921.1/1,020.9 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 140 | 1,011.3 | 985.1/1,024.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 141 | 1,008.9 | 955.6/1,034.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 142 | 999.7 | 935.3/1,029.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 143 | 1,001.0 | 948.2/1,005.1 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 144 | 994.9 | 993.0/1,000.9 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 145 | 998.8 | 997.5/1,002.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 146 | 997.6 | 988.7/1,006.1 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 147 | 1,027.3 | 992.5/1,679.9 | 238.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 148 | 1,019.9 | 988.6/1,115.8 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 149 | 1,023.4 | 995.1/1,105.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 150 | 1,022.5 | 963.0/1,026.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 151 | 1,015.3 | 940.5/1,037.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 152 | 975.8 | 941.6/1,027.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 153 | 1,004.0 | 919.3/1,028.6 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 154 | 275.1 | 233.6/281.3 | 663.0 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 155 | 619.0 | 611.5/622.8 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 156 | 55.2 | 40.8/60.1 | 1.7 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 157 | 1,091.1 | 953.8/1,092.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 158 | 1,054.2 | 915.6/1,060.6 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 159 | 1,039.6 | 905.9/1,045.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 160 | 1,042.1 | 897.8/1,044.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 161 | 1,033.8 | 938.3/1,035.6 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 162 | 1,031.7 | 974.6/1,043.7 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 163 | 1,035.4 | 999.9/1,037.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 164 | 1,033.7 | 1,000.0/1,075.1 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 165 | 1,039.4 | 1,032.7/1,040.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 166 | 1,011.5 | 996.4/1,033.2 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 167 | 1,013.3 | 1,001.9/1,025.2 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 168 | 1,001.2 | 997.3/1,028.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 169 | 1,002.8 | 992.6/1,027.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 170 | 1,005.0 | 989.9/1,024.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 171 | 1,016.4 | 994.6/1,021.9 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 172 | 1,012.0 | 961.3/1,018.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 173 | 1,028.6 | 1,013.1/1,097.3 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 174 | 1,023.7 | 1,000.7/1,080.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 175 | 1,028.6 | 988.0/1,043.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 176 | 1,026.7 | 996.4/1,030.9 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 177 | 1,049.3 | 998.5/1,054.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 178 | 1,045.8 | 986.3/1,052.2 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 179 | 1,034.7 | 941.8/1,042.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 180 | 1,033.3 | 932.1/1,035.9 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 181 | 1,011.2 | 941.5/1,034.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 182 | 1,004.5 | 935.4/1,029.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 183 | 1,006.1 | 933.6/1,036.3 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 184 | 983.1 | 930.0/1,050.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 185 | 1,003.2 | 905.5/1,036.1 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 186 | 1,029.5 | 913.9/1,031.9 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 187 | 1,021.2 | 905.6/1,035.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 188 | 1,022.5 | 885.7/1,027.3 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 189 | 1,024.9 | 887.6/1,028.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 190 | 1,018.8 | 886.7/1,027.9 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 191 | 1,022.5 | 890.9/1,034.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 192 | 1,030.2 | 886.4/1,050.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 193 | 263.9 | 213.5/282.1 | 665.2 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 194 | 619.6 | 611.8/627.5 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 195 | 57.2 | 41.6/58.8 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 196 | 1,038.4 | 948.1/1,098.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 197 | 975.9 | 907.0/1,056.4 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 198 | 936.2 | 903.7/1,045.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 199 | 958.8 | 895.3/1,027.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 200 | 954.2 | 918.9/1,006.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 201 | 957.4 | 931.7/1,035.5 | 235.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 202 | 958.2 | 893.8/1,036.6 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 203 | 955.5 | 913.8/1,037.9 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 204 | 953.8 | 914.2/997.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 205 | 997.4 | 902.4/1,001.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 206 | 1,000.7 | 908.1/1,001.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 207 | 999.7 | 911.5/1,000.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 208 | 999.9 | 896.9/1,000.3 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 209 | 997.9 | 911.8/1,007.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 210 | 999.7 | 912.8/1,002.9 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 211 | 1,011.6 | 890.6/1,019.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 212 | 1,013.0 | 888.9/1,031.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 213 | 1,000.4 | 906.3/1,012.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 214 | 997.4 | 912.0/1,024.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 215 | 996.6 | 910.2/1,036.8 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 216 | 998.6 | 913.9/1,006.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 217 | 1,023.7 | 909.8/1,026.3 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 218 | 1,030.3 | 910.1/1,075.1 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 219 | 1,026.9 | 909.6/1,033.3 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 220 | 1,029.8 | 896.6/1,029.9 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 221 | 1,022.5 | 913.5/1,025.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 222 | 1,031.2 | 906.5/1,042.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 223 | 1,027.0 | 902.7/1,043.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 224 | 1,030.8 | 912.1/1,031.5 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 225 | 1,029.4 | 988.0/1,064.7 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 226 | 1,012.4 | 1,010.0/1,030.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 227 | 993.4 | 958.2/1,007.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 228 | 987.2 | 950.8/1,001.1 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 229 | 994.8 | 994.6/997.0 | 261.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 230 | 989.9 | 987.4/1,007.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 231 | 1,022.8 | 997.0/1,030.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 232 | 271.3 | 258.5/283.8 | 662.2 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 233 | 599.1 | 594.6/606.2 | 6.9 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 234 | 54.6 | 44.6/58.2 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 235 | 1,083.3 | 1,072.5/1,083.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 236 | 1,029.9 | 1,008.9/1,044.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 237 | 1,021.5 | 1,005.4/1,030.8 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 238 | 1,011.4 | 1,007.6/1,031.8 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 239 | 1,014.2 | 991.9/1,026.3 | 235.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 240 | 1,007.7 | 1,002.6/1,029.3 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 241 | 1,015.4 | 995.1/1,019.6 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 242 | 994.1 | 943.9/1,011.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 243 | 995.4 | 943.9/1,021.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 244 | 994.8 | 938.9/1,017.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 245 | 1,001.9 | 961.6/1,017.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 246 | 1,002.2 | 945.7/1,021.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 247 | 1,003.4 | 942.0/1,010.9 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 248 | 996.1 | 921.1/1,022.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 249 | 1,023.2 | 912.8/1,042.0 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 250 | 1,022.7 | 912.3/1,031.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 251 | 1,021.6 | 936.9/1,031.0 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 252 | 983.9 | 969.9/1,017.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 253 | 1,003.3 | 946.2/1,019.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 254 | 996.0 | 981.1/1,012.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 255 | 996.0 | 968.0/997.1 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 256 | 983.7 | 970.8/1,020.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 257 | 975.6 | 939.8/1,007.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 258 | 954.9 | 954.8/1,018.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 259 | 952.4 | 941.2/1,025.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 260 | 991.3 | 985.9/1,018.4 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 261 | 1,008.3 | 993.8/1,021.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 262 | 1,019.7 | 1,003.8/1,027.0 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 263 | 1,022.7 | 1,020.1/1,034.9 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 264 | 1,022.4 | 966.2/1,025.1 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 265 | 1,017.7 | 946.4/1,023.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 266 | 1,000.6 | 942.5/1,023.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 267 | 986.5 | 947.6/1,022.2 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 268 | 993.4 | 922.8/1,033.4 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 269 | 993.4 | 925.5/1,029.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 270 | 997.7 | 917.7/1,022.7 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 271 | 253.2 | 246.8/256.7 | 662.1 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 272 | 619.9 | 613.7/621.4 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 273 | 51.7 | 43.1/54.9 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 274 | 998.3 | 976.3/1,049.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 275 | 963.6 | 950.5/1,020.0 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 276 | 952.9 | 923.3/1,005.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 277 | 942.3 | 921.5/994.9 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 278 | 919.6 | 916.8/998.6 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 279 | 948.5 | 944.9/982.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 280 | 943.3 | 939.9/1,042.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 281 | 954.8 | 951.8/1,035.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 282 | 1,000.9 | 950.7/1,037.4 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 283 | 1,000.3 | 987.3/1,000.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 284 | 1,024.2 | 956.9/1,025.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 285 | 1,016.5 | 942.4/1,024.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 286 | 1,022.8 | 936.5/1,024.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 287 | 1,021.7 | 939.2/1,026.6 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 288 | 1,020.6 | 940.6/1,028.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 289 | 1,019.9 | 993.5/1,030.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 290 | 1,030.0 | 1,022.3/1,036.8 | 235.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 291 | 1,024.8 | 1,019.5/1,028.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 292 | 1,032.9 | 986.3/1,035.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 293 | 1,013.3 | 993.8/1,022.5 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 294 | 1,001.8 | 992.4/1,004.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 295 | 1,004.1 | 993.3/1,016.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 296 | 996.3 | 982.1/1,011.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 297 | 963.8 | 941.0/990.8 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 298 | 959.4 | 939.0/992.3 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 299 | 939.7 | 927.5/953.1 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 300 | 943.1 | 916.3/998.4 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 301 | 974.5 | 927.4/994.9 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 302 | 1,021.5 | 936.7/1,027.1 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 303 | 1,022.3 | 957.1/1,027.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 304 | 1,021.2 | 995.0/1,022.4 | 238.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 305 | 1,023.3 | 989.5/1,030.9 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 306 | 1,021.6 | 989.7/1,026.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 307 | 996.6 | 988.2/1,027.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 308 | 992.4 | 989.1/1,016.9 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 309 | 1,003.0 | 1,001.2/1,039.3 | 237.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 310 | 262.7 | 241.0/340.7 | 661.7 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 311 | 621.6 | 612.6/622.4 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 312 | 52.6 | 50.6/53.7 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 313 | 1,060.3 | 1,052.2/1,101.2 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 314 | 1,041.3 | 1,035.9/1,053.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 315 | 1,030.1 | 1,011.6/1,048.2 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 316 | 1,032.2 | 1,000.7/1,040.5 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 317 | 1,010.6 | 999.9/1,045.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 318 | 1,029.4 | 999.1/1,034.4 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 319 | 1,026.3 | 997.3/1,044.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 320 | 1,025.2 | 994.8/1,067.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 321 | 1,035.0 | 995.3/1,037.0 | 237.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 322 | 1,030.9 | 992.5/1,031.2 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 323 | 999.3 | 993.2/1,026.2 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 324 | 996.5 | 992.2/1,026.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 325 | 994.6 | 992.7/1,032.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 326 | 994.9 | 990.6/1,025.5 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 327 | 1,014.0 | 981.8/1,063.1 | 235.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 328 | 1,019.3 | 940.1/1,037.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 329 | 987.4 | 935.4/1,045.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 330 | 993.0 | 941.2/1,025.3 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 331 | 988.9 | 942.0/1,029.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 332 | 996.1 | 934.6/1,034.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 333 | 968.1 | 942.2/1,049.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 334 | 1,031.1 | 937.4/1,533.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 335 | 1,025.5 | 939.6/1,150.8 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 336 | 1,042.0 | 941.8/1,079.8 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 337 | 1,032.6 | 940.1/1,062.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 338 | 1,028.4 | 938.2/1,059.3 | 235.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 339 | 1,028.4 | 954.3/1,033.5 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 340 | 1,030.0 | 994.5/1,030.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 341 | 1,026.0 | 990.6/1,051.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 342 | 1,015.5 | 991.6/1,040.3 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 343 | 1,027.6 | 1,012.9/1,035.9 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 344 | 1,019.2 | 1,015.1/1,032.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 345 | 1,021.0 | 990.6/1,026.2 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 346 | 1,022.3 | 991.1/1,031.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 347 | 1,021.8 | 985.1/1,029.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 348 | 1,025.8 | 942.5/1,032.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 349 | 251.4 | 238.0/270.2 | 664.1 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 350 | 619.3 | 617.6/712.8 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 351 | 51.9 | 49.1/57.1 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 352 | 1,057.2 | 1,053.9/1,058.3 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 353 | 1,034.1 | 1,033.3/1,119.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 354 | 1,046.5 | 1,029.6/1,076.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 355 | 1,024.1 | 1,022.2/1,033.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 356 | 1,011.3 | 1,002.1/1,045.1 | 235.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 357 | 998.8 | 991.9/1,029.1 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 358 | 993.3 | 988.2/1,028.8 | 238.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 359 | 997.5 | 994.0/1,001.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 360 | 1,003.0 | 1,001.3/1,014.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 361 | 999.8 | 995.5/1,021.2 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 362 | 1,002.7 | 999.3/1,025.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 363 | 1,010.7 | 992.5/1,017.8 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 364 | 1,020.7 | 995.3/1,027.7 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 365 | 1,024.7 | 1,021.2/1,029.2 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 366 | 1,002.7 | 989.7/1,032.4 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 367 | 988.6 | 984.5/1,026.2 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 368 | 992.7 | 981.7/1,003.9 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 369 | 1,004.4 | 987.5/1,068.7 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 370 | 1,024.8 | 949.9/1,045.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 371 | 1,015.6 | 940.9/1,024.7 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 372 | 997.4 | 934.8/1,026.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 373 | 949.3 | 947.5/1,028.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 374 | 945.7 | 941.3/1,021.6 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 375 | 1,005.0 | 938.5/1,016.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 376 | 940.5 | 936.1/1,020.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 377 | 965.1 | 940.5/1,018.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 378 | 986.7 | 952.5/1,022.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 379 | 1,010.9 | 980.0/1,019.4 | 238.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 380 | 1,019.9 | 1,012.2/1,053.0 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 381 | 1,038.2 | 1,015.2/1,042.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 382 | 1,015.7 | 1,004.3/1,035.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 383 | 1,001.2 | 991.3/1,024.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 384 | 1,011.6 | 1,000.2/1,026.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 385 | 1,016.9 | 993.6/1,017.9 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 386 | 1,026.7 | 995.7/1,027.0 | 238.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 387 | 1,022.7 | 1,022.2/1,022.9 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 388 | 264.7 | 259.8/272.8 | 662.1 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 389 | 617.5 | 613.0/618.8 | 7.2 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 390 | 54.0 | 46.8/57.5 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 391 | 1,092.9 | 1,085.5/1,094.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 392 | 1,043.7 | 982.0/1,056.0 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 393 | 1,021.2 | 958.5/1,043.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 394 | 1,017.8 | 926.1/1,032.6 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 395 | 1,009.7 | 925.2/1,036.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 396 | 1,024.2 | 965.0/1,049.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 397 | 1,022.3 | 984.5/1,033.2 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 398 | 1,017.4 | 940.5/1,029.5 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 399 | 999.5 | 940.0/1,032.2 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 400 | 985.2 | 958.6/1,001.9 | 286.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 401 | 967.5 | 962.3/998.6 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 402 | 968.5 | 961.5/992.1 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 403 | 994.7 | 950.5/1,000.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 404 | 987.6 | 946.1/999.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 405 | 993.3 | 944.7/1,011.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 406 | 987.9 | 977.0/1,002.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 407 | 988.4 | 962.3/998.8 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 408 | 994.2 | 956.5/1,003.0 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 409 | 988.6 | 980.6/1,006.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 410 | 1,019.6 | 998.4/1,021.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 411 | 998.0 | 996.1/1,023.9 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 412 | 1,013.0 | 971.0/1,033.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 413 | 1,001.2 | 945.8/1,020.4 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 414 | 994.4 | 980.1/1,023.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 415 | 999.6 | 998.1/1,020.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 416 | 1,021.2 | 973.3/1,026.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 417 | 1,020.9 | 942.1/1,025.2 | 238.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 418 | 1,013.6 | 950.2/1,023.9 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 419 | 1,014.5 | 957.2/1,028.0 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 420 | 1,014.6 | 952.2/1,023.4 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 421 | 1,026.1 | 952.8/1,070.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 422 | 1,030.5 | 937.2/1,030.5 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 423 | 1,019.5 | 936.2/1,023.2 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 424 | 1,025.3 | 943.0/1,033.4 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 425 | 1,018.8 | 938.7/1,034.3 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 426 | 1,021.8 | 936.2/1,043.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 427 | 257.4 | 247.5/257.5 | 662.7 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 428 | 619.8 | 610.1/621.2 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 429 | 52.2 | 48.5/55.2 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 430 | 1,049.6 | 1,017.7/1,085.6 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 431 | 1,036.3 | 973.3/1,059.7 | 253.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 432 | 1,031.0 | 963.3/1,048.9 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 433 | 1,012.7 | 959.8/1,024.3 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 434 | 1,001.4 | 946.1/1,027.9 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 435 | 1,014.2 | 1,006.2/1,016.5 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 436 | 1,012.8 | 944.8/1,049.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 437 | 1,001.5 | 943.7/1,043.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 438 | 1,002.1 | 987.7/1,035.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 439 | 1,001.2 | 991.0/1,044.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 440 | 996.8 | 992.1/1,035.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 441 | 1,022.5 | 996.0/1,039.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 442 | 1,027.4 | 998.3/1,034.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 443 | 1,016.4 | 997.9/1,029.4 | 237.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 444 | 1,023.7 | 994.4/1,049.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 445 | 1,025.0 | 995.3/1,044.2 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 446 | 1,022.7 | 1,000.2/1,031.1 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 447 | 1,023.2 | 990.4/1,031.3 | 237.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 448 | 1,025.4 | 999.4/1,033.2 | 235.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 449 | 1,016.6 | 995.5/1,042.3 | 238.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 450 | 1,028.5 | 994.7/1,035.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 451 | 1,027.4 | 1,007.1/1,029.6 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 452 | 1,020.8 | 998.7/1,033.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 453 | 1,007.4 | 999.3/1,023.2 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 454 | 1,025.5 | 994.3/1,027.2 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 455 | 1,022.1 | 993.3/1,031.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 456 | 1,022.0 | 996.4/1,045.8 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 457 | 1,039.7 | 1,006.2/1,041.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 458 | 1,023.1 | 1,000.4/1,027.8 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 459 | 1,024.3 | 1,003.7/1,031.3 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 460 | 1,020.7 | 992.7/1,032.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 461 | 1,024.6 | 994.7/1,027.7 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 462 | 998.2 | 995.7/1,029.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 463 | 999.2 | 990.4/1,005.3 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 464 | 989.3 | 988.1/1,033.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 465 | 993.5 | 987.1/1,021.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 466 | 249.2 | 245.3/258.1 | 711.5 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 467 | 671.2 | 621.2/817.1 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 468 | 51.9 | 48.4/54.7 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 469 | 980.3 | 962.5/1,098.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 470 | 981.8 | 962.8/1,057.0 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 471 | 1,015.2 | 995.6/1,041.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 472 | 987.5 | 957.7/1,040.2 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 473 | 995.7 | 954.7/1,036.6 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 474 | 954.1 | 940.9/1,036.6 | 235.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 475 | 999.8 | 935.9/1,035.2 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 476 | 999.3 | 938.8/1,037.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 477 | 1,003.2 | 936.9/1,041.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 478 | 1,013.2 | 932.4/1,032.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 479 | 1,024.7 | 937.8/1,026.3 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 480 | 1,029.6 | 923.8/1,038.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 481 | 1,034.1 | 935.4/1,038.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 482 | 1,028.4 | 989.5/1,037.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 483 | 1,031.4 | 988.5/1,034.3 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 484 | 1,021.3 | 996.9/1,033.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 485 | 1,025.4 | 996.8/1,108.8 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 486 | 1,033.4 | 1,022.9/1,128.3 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 487 | 1,032.9 | 1,016.0/1,070.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 488 | 1,035.1 | 1,031.4/1,044.8 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 489 | 1,026.8 | 1,026.3/1,040.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 490 | 1,028.1 | 1,024.7/1,055.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 491 | 1,030.2 | 1,022.7/1,036.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 492 | 1,025.4 | 945.7/1,034.4 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 493 | 1,028.3 | 992.5/1,038.8 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 494 | 1,023.5 | 992.6/1,037.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 495 | 1,039.2 | 1,012.2/1,049.1 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 496 | 1,029.1 | 1,024.5/1,043.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 497 | 1,023.5 | 1,010.3/1,038.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 498 | 1,014.3 | 1,001.5/1,041.8 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 499 | 1,023.3 | 1,017.8/1,039.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 500 | 1,025.9 | 1,024.9/1,028.9 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 501 | 1,023.1 | 1,007.1/1,029.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 502 | 1,017.2 | 1,014.3/1,041.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 503 | 1,026.5 | 1,013.8/1,042.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 504 | 1,021.8 | 1,021.6/1,078.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 505 | 276.1 | 248.1/279.1 | 662.0 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 506 | 610.7 | 597.9/615.2 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 507 | 57.9 | 46.5/58.1 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 508 | 1,081.6 | 1,060.5/1,099.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 509 | 1,055.7 | 1,040.6/1,090.3 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 510 | 1,043.4 | 1,025.9/1,047.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 511 | 1,033.6 | 1,030.9/1,038.4 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 512 | 1,027.6 | 1,013.1/1,037.2 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 513 | 1,031.3 | 1,016.3/1,036.3 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 514 | 1,018.3 | 1,002.7/1,033.2 | 235.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 515 | 1,019.3 | 1,004.2/1,034.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 516 | 1,025.7 | 1,007.1/1,032.6 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 517 | 1,020.5 | 1,019.2/1,032.5 | 238.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 518 | 1,033.0 | 1,023.9/1,033.4 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 519 | 1,028.8 | 1,011.5/1,038.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 520 | 1,029.9 | 980.5/1,041.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 521 | 1,047.2 | 1,043.2/1,532.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 522 | 1,040.2 | 1,035.8/1,082.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 523 | 1,030.5 | 1,026.4/1,056.6 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 524 | 1,030.7 | 1,027.3/1,030.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 525 | 1,034.9 | 1,023.5/1,036.4 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 526 | 1,031.1 | 1,002.7/1,051.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 527 | 1,027.5 | 994.3/1,039.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 528 | 1,031.6 | 1,019.2/1,031.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 529 | 1,034.5 | 1,028.6/1,057.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 530 | 1,036.6 | 1,028.7/1,037.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 531 | 1,033.8 | 1,028.1/1,037.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 532 | 1,032.4 | 1,021.4/1,095.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 533 | 1,034.5 | 1,023.9/1,041.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 534 | 1,032.7 | 1,018.6/1,034.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 535 | 1,039.3 | 1,016.8/1,041.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 536 | 1,026.5 | 1,024.8/1,036.8 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 537 | 1,025.5 | 1,007.7/1,031.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 538 | 1,008.3 | 1,005.2/1,024.0 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 539 | 1,003.7 | 996.3/1,032.9 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 540 | 994.6 | 990.7/1,027.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 541 | 1,023.7 | 958.7/1,037.2 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 542 | 1,027.0 | 933.8/1,034.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 543 | 1,025.1 | 953.3/1,028.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 544 | 267.2 | 251.2/269.7 | 663.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 545 | 615.7 | 615.2/616.0 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 546 | 56.9 | 54.9/57.5 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 547 | 1,057.3 | 1,038.2/1,075.1 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 548 | 1,028.8 | 1,025.9/1,028.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 549 | 1,014.6 | 1,011.5/1,022.9 | 235.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 550 | 1,009.5 | 1,004.7/1,009.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 551 | 1,030.8 | 1,025.3/1,033.4 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 552 | 1,026.1 | 1,012.1/1,034.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 553 | 1,027.4 | 998.8/1,034.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 554 | 1,029.8 | 997.1/1,033.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 555 | 1,012.1 | 998.9/1,022.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 556 | 1,010.5 | 1,003.1/1,024.8 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 557 | 1,027.4 | 972.8/1,030.1 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 558 | 1,029.6 | 940.5/1,031.6 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 559 | 1,031.1 | 919.3/1,041.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 560 | 1,030.3 | 978.0/1,031.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 561 | 1,028.1 | 1,008.5/1,030.7 | 235.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 562 | 1,032.2 | 1,020.5/1,034.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 563 | 1,028.0 | 1,024.5/1,028.9 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 564 | 1,022.1 | 1,003.6/1,036.0 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 565 | 1,030.6 | 970.8/1,031.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 566 | 1,005.6 | 938.8/1,025.4 | 237.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 567 | 1,001.6 | 937.0/1,034.4 | 338.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 568 | 1,010.6 | 939.2/1,030.5 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 569 | 1,020.2 | 944.7/1,024.4 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 570 | 1,001.7 | 950.9/1,037.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 571 | 997.4 | 942.2/1,031.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 572 | 952.7 | 928.6/1,034.2 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 573 | 967.0 | 913.8/1,029.8 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 574 | 1,004.3 | 939.8/1,035.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 575 | 994.5 | 905.7/1,030.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 576 | 989.6 | 928.6/1,027.8 | 237.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 577 | 1,020.6 | 1,010.6/1,027.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 578 | 1,021.7 | 1,018.7/1,026.6 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 579 | 1,029.8 | 1,029.6/1,560.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 580 | 1,022.8 | 1,020.6/1,054.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 581 | 1,027.4 | 1,024.3/1,033.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 582 | 1,027.1 | 1,019.3/1,029.2 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 583 | 259.6 | 258.9/268.9 | 662.8 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 584 | 620.3 | 618.4/734.6 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 585 | 53.9 | 53.1/56.0 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 586 | 1,084.3 | 1,073.9/1,122.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 587 | 1,045.1 | 1,025.2/1,057.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 588 | 1,034.9 | 1,001.4/1,049.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 589 | 1,004.1 | 994.5/1,052.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 590 | 1,008.7 | 977.3/1,037.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 591 | 1,001.6 | 955.6/1,040.4 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 592 | 1,006.0 | 933.9/1,022.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 593 | 1,005.1 | 943.7/1,110.4 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 594 | 992.9 | 933.1/1,042.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 595 | 995.7 | 941.4/1,037.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 596 | 989.0 | 948.8/1,065.4 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 597 | 1,015.6 | 995.8/1,043.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 598 | 1,016.0 | 990.0/1,045.9 | 279.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 599 | 1,036.9 | 988.8/1,037.0 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 600 | 1,023.8 | 982.8/1,041.0 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 601 | 1,025.9 | 939.4/1,028.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 602 | 1,020.3 | 945.9/1,023.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 603 | 1,019.8 | 990.8/1,025.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 604 | 1,024.2 | 993.4/1,025.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 605 | 1,021.8 | 991.5/1,029.1 | 237.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 606 | 1,006.5 | 990.2/1,039.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 607 | 949.7 | 945.8/1,029.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 608 | 994.2 | 936.5/1,043.2 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 609 | 957.3 | 943.1/1,023.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 610 | 938.6 | 936.4/1,027.0 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 611 | 997.3 | 945.0/1,026.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 612 | 954.5 | 941.4/1,025.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 613 | 995.1 | 931.0/1,028.4 | 237.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 614 | 986.8 | 913.8/1,021.8 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 615 | 972.2 | 940.3/984.5 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 616 | 977.4 | 945.7/998.4 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 617 | 946.1 | 914.8/990.5 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 618 | 947.2 | 913.1/980.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 619 | 985.4 | 934.9/986.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 620 | 968.6 | 939.9/1,001.6 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 621 | 951.0 | 934.5/1,040.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 622 | 248.7 | 229.1/285.8 | 662.5 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 623 | 618.7 | 616.1/634.0 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 624 | 47.4 | 42.8/63.1 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 625 | 1,064.2 | 993.9/1,102.9 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 626 | 1,011.6 | 959.0/1,054.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 627 | 1,001.7 | 945.2/1,046.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 628 | 1,011.7 | 940.5/1,051.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 629 | 1,004.1 | 939.9/1,048.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 630 | 999.8 | 959.8/1,044.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 631 | 1,003.0 | 994.3/1,053.2 | 251.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 632 | 999.0 | 989.8/1,040.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 633 | 991.1 | 989.8/1,031.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 634 | 1,023.2 | 1,020.0/1,026.6 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 635 | 1,020.4 | 1,013.3/1,036.0 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 636 | 1,022.9 | 1,016.1/1,025.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 637 | 1,022.8 | 959.8/1,024.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 638 | 1,020.6 | 1,017.3/1,026.1 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 639 | 1,023.4 | 1,017.5/1,035.0 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 640 | 1,009.0 | 997.1/1,033.6 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 641 | 1,017.9 | 987.0/1,030.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 642 | 1,014.4 | 993.2/1,024.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 643 | 1,007.0 | 974.2/1,033.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 644 | 1,019.5 | 933.4/1,026.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 645 | 1,009.3 | 935.0/1,027.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 646 | 1,018.9 | 936.2/1,032.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 647 | 1,012.8 | 934.7/1,016.5 | 240.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 648 | 996.1 | 928.7/1,011.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 649 | 969.8 | 934.6/1,005.8 | 235.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 650 | 988.8 | 929.0/991.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 651 | 990.4 | 927.3/994.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 652 | 983.4 | 921.7/1,008.5 | 235.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 653 | 984.2 | 931.7/990.6 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 654 | 986.1 | 944.8/992.5 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 655 | 991.0 | 988.6/996.5 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 656 | 985.6 | 985.6/1,012.4 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 657 | 996.6 | 986.3/1,021.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 658 | 986.7 | 985.3/1,026.3 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 659 | 990.3 | 985.8/1,021.0 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 660 | 988.8 | 982.2/1,024.0 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 661 | 242.7 | 237.3/277.6 | 663.8 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 662 | 620.3 | 618.7/626.2 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 663 | 48.7 | 45.3/58.4 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 664 | 1,048.8 | 1,027.3/1,092.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 665 | 1,008.8 | 1,006.5/1,053.3 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 666 | 995.4 | 953.6/1,040.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 667 | 997.7 | 937.3/1,017.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 668 | 987.4 | 941.6/1,031.9 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 669 | 996.7 | 942.2/1,002.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 670 | 992.3 | 926.1/1,034.9 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 671 | 986.0 | 919.9/1,033.5 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 672 | 990.6 | 950.3/1,024.2 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 673 | 1,002.4 | 921.7/1,038.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 674 | 994.4 | 963.6/1,027.6 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 675 | 1,020.4 | 939.3/1,026.0 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 676 | 1,012.3 | 932.2/1,017.4 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 677 | 1,008.6 | 988.8/1,020.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 678 | 1,007.2 | 982.2/1,018.9 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 679 | 1,009.5 | 991.1/1,046.2 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 680 | 1,009.6 | 988.9/1,027.8 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 681 | 1,024.7 | 949.2/1,056.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 682 | 1,020.4 | 934.9/1,029.7 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 683 | 1,000.2 | 947.2/1,021.6 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 684 | 987.6 | 928.0/996.4 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 685 | 995.9 | 931.9/1,007.0 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 686 | 1,017.0 | 926.5/1,026.9 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 687 | 1,011.5 | 929.8/1,015.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 688 | 1,013.7 | 932.3/1,015.5 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 689 | 1,018.4 | 916.8/1,024.0 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 690 | 1,019.8 | 906.5/1,024.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 691 | 1,027.0 | 908.1/1,030.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 692 | 986.6 | 909.5/1,029.4 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 693 | 984.7 | 903.3/1,019.1 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 694 | 983.7 | 901.0/1,014.6 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 695 | 978.7 | 909.6/1,021.4 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 696 | 988.6 | 925.3/1,019.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 697 | 987.5 | 909.8/1,023.2 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 698 | 987.8 | 900.2/1,023.6 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 699 | 997.8 | 905.5/1,017.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 700 | 248.6 | 222.2/252.7 | 662.0 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 701 | 622.9 | 617.6/624.1 | 7.2 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 702 | 46.7 | 41.3/48.1 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 703 | 1,041.4 | 976.2/1,068.4 | 235.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 704 | 1,011.8 | 945.5/1,037.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 705 | 1,011.4 | 940.6/1,031.5 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 706 | 1,021.2 | 951.3/1,031.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 707 | 996.3 | 938.4/1,021.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 708 | 996.4 | 934.1/1,018.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 709 | 988.2 | 952.8/1,017.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 710 | 989.6 | 989.2/1,020.7 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 711 | 990.6 | 990.0/1,024.0 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 712 | 1,014.6 | 992.6/1,028.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 713 | 1,020.8 | 984.8/1,024.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 714 | 1,022.5 | 994.1/1,029.0 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 715 | 1,011.4 | 998.1/1,021.3 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 716 | 995.3 | 990.0/1,012.9 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 717 | 983.7 | 950.6/1,010.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 718 | 985.1 | 938.3/1,011.7 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 719 | 957.8 | 934.5/1,016.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 720 | 992.3 | 944.1/1,010.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 721 | 990.7 | 980.8/1,014.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 722 | 996.6 | 987.7/1,013.8 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 723 | 1,004.0 | 985.6/1,015.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 724 | 998.8 | 990.5/1,012.9 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 725 | 983.0 | 978.4/1,019.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 726 | 994.6 | 967.2/1,011.8 | 238.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 727 | 991.5 | 936.1/1,017.2 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 728 | 983.0 | 928.1/1,019.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 729 | 987.6 | 908.0/1,013.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 730 | 986.8 | 903.8/1,021.2 | 235.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 731 | 981.0 | 891.0/983.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 732 | 961.2 | 900.9/991.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 733 | 955.1 | 903.9/973.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 734 | 929.9 | 906.9/1,015.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 735 | 974.6 | 929.8/1,016.7 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 736 | 974.5 | 959.9/1,034.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 737 | 971.1 | 940.3/1,016.0 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 738 | 988.8 | 943.8/1,015.8 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 739 | 252.6 | 225.5/257.0 | 661.7 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 740 | 623.6 | 618.3/626.3 | 6.9 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 741 | 43.1 | 41.1/44.1 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 742 | 1,053.7 | 956.0/1,079.4 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 743 | 1,037.6 | 937.6/1,045.6 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 744 | 1,020.8 | 940.6/1,034.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 745 | 1,000.3 | 927.9/1,021.6 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 746 | 993.2 | 907.9/1,023.2 | 235.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 747 | 966.2 | 915.0/1,018.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 748 | 975.4 | 906.5/1,014.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 749 | 1,013.0 | 910.5/1,024.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 750 | 1,014.3 | 909.4/1,025.7 | 282.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 751 | 1,014.9 | 908.0/1,019.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 752 | 1,013.9 | 905.0/1,021.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 753 | 1,015.5 | 903.8/1,026.5 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 754 | 931.4 | 905.0/1,017.8 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 755 | 961.4 | 899.6/1,010.8 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 756 | 930.8 | 904.1/1,019.2 | 235.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 757 | 930.0 | 915.3/1,024.3 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 758 | 937.6 | 917.7/985.7 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 759 | 929.1 | 908.4/994.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 760 | 969.4 | 917.3/981.1 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 761 | 994.4 | 946.2/1,005.2 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 762 | 988.1 | 938.5/988.6 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 763 | 985.3 | 939.1/989.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 764 | 985.2 | 939.5/986.9 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 765 | 952.5 | 934.8/993.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 766 | 949.3 | 937.2/987.7 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 767 | 987.2 | 932.6/989.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 768 | 981.1 | 944.7/981.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 769 | 944.0 | 930.3/1,005.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 770 | 937.0 | 931.9/1,022.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 771 | 936.0 | 925.9/1,018.0 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 772 | 936.1 | 934.7/1,012.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 773 | 933.8 | 928.5/1,000.8 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 774 | 938.0 | 925.6/1,042.0 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 775 | 995.4 | 933.0/1,003.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 776 | 987.8 | 923.1/998.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 777 | 981.0 | 903.9/990.4 | 237.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 778 | 243.2 | 229.2/255.6 | 663.2 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 779 | 624.1 | 620.3/625.9 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 780 | 42.7 | 40.0/46.7 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 781 | 1,065.7 | 990.8/1,114.9 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 782 | 1,046.1 | 962.7/1,056.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 783 | 1,039.1 | 944.0/1,058.6 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 784 | 1,029.8 | 997.8/1,033.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 785 | 1,031.1 | 1,012.7/1,038.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 786 | 1,025.6 | 996.6/1,029.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 787 | 1,003.4 | 994.9/1,028.7 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 788 | 1,007.5 | 991.7/1,017.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 789 | 1,007.6 | 992.1/1,032.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 790 | 998.4 | 983.4/1,023.3 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 791 | 1,000.2 | 931.1/1,015.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 792 | 996.6 | 943.6/1,024.4 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 793 | 985.9 | 975.0/996.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 794 | 996.3 | 964.7/1,005.0 | 237.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 795 | 993.4 | 927.1/1,053.5 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 796 | 1,001.6 | 923.2/1,017.4 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 797 | 993.5 | 927.5/1,024.6 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 798 | 1,006.1 | 931.2/1,019.7 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 799 | 1,024.3 | 966.5/1,030.9 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 800 | 1,022.6 | 1,017.3/1,024.1 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 801 | 1,016.2 | 1,007.2/1,018.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 802 | 1,002.2 | 990.8/1,017.6 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 803 | 1,003.1 | 986.2/1,014.0 | 284.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 804 | 1,002.6 | 986.4/1,015.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 805 | 1,001.4 | 983.8/1,019.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 806 | 1,005.9 | 981.8/1,016.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 807 | 997.7 | 979.7/1,039.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 808 | 1,006.3 | 980.9/1,012.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 809 | 992.7 | 989.9/1,002.9 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 810 | 996.0 | 988.8/1,024.1 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 811 | 1,000.3 | 966.2/1,020.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 812 | 998.9 | 990.6/1,011.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 813 | 998.4 | 991.1/1,018.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 814 | 1,016.8 | 997.3/1,023.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 815 | 1,020.4 | 1,011.3/1,026.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 816 | 1,021.5 | 1,015.7/1,033.3 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 817 | 252.1 | 244.1/274.2 | 662.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 818 | 620.4 | 614.0/620.9 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 819 | 44.3 | 44.2/59.0 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 820 | 1,055.4 | 1,044.6/1,059.8 | 237.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 821 | 1,029.6 | 1,027.1/1,032.5 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 822 | 1,022.9 | 963.5/1,030.1 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 823 | 1,000.8 | 963.0/1,020.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 824 | 999.9 | 981.1/1,031.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 825 | 992.8 | 937.7/994.7 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 826 | 977.2 | 935.1/995.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 827 | 992.7 | 926.8/1,001.8 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 828 | 999.8 | 906.7/1,031.3 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 829 | 964.8 | 931.0/1,000.2 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 830 | 944.4 | 935.6/1,003.8 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 831 | 987.5 | 947.0/1,032.3 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 832 | 987.5 | 958.2/1,022.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 833 | 955.0 | 950.5/1,015.1 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 834 | 953.6 | 931.7/1,018.1 | 235.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 835 | 978.4 | 937.3/1,016.9 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 836 | 986.5 | 971.6/1,011.8 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 837 | 995.2 | 987.3/1,019.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 838 | 1,006.7 | 984.9/1,016.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 839 | 1,008.9 | 1,006.0/1,018.7 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 840 | 1,017.1 | 987.1/1,022.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 841 | 1,011.2 | 1,001.0/1,029.0 | 237.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 842 | 985.5 | 974.9/1,034.0 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 843 | 990.5 | 952.8/1,030.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 844 | 1,027.1 | 983.7/1,028.0 | 238.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 845 | 1,023.3 | 1,009.5/1,030.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 846 | 1,020.3 | 1,008.1/1,031.1 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 847 | 1,018.0 | 1,011.8/1,046.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 848 | 1,013.7 | 1,011.9/1,042.9 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 849 | 1,013.2 | 1,010.1/1,033.7 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 850 | 1,014.9 | 994.0/1,030.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 851 | 1,023.2 | 1,016.4/1,040.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 852 | 1,020.2 | 1,017.3/1,031.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 853 | 1,017.0 | 1,014.1/1,036.5 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 854 | 1,018.1 | 1,015.9/1,031.5 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 855 | 1,012.0 | 1,000.8/1,025.9 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 856 | 256.9 | 235.7/276.8 | 662.0 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 857 | 622.0 | 613.3/623.9 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 858 | 45.1 | 43.6/59.2 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 859 | 1,084.9 | 1,033.4/1,090.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 860 | 1,033.9 | 1,011.4/1,056.1 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 861 | 1,012.5 | 1,008.4/1,054.2 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 862 | 1,025.3 | 960.8/1,042.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 863 | 1,011.9 | 965.7/1,037.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 864 | 1,021.5 | 944.7/1,032.8 | 235.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 865 | 1,020.0 | 983.3/1,037.2 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 866 | 1,024.9 | 988.9/1,047.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 867 | 1,026.1 | 992.1/1,030.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 868 | 1,007.1 | 990.3/1,012.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 869 | 987.6 | 948.0/1,019.9 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 870 | 992.1 | 957.4/1,021.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 871 | 992.5 | 982.7/994.9 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 872 | 991.3 | 972.1/1,000.8 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 873 | 990.6 | 983.9/1,002.0 | 235.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 874 | 989.0 | 981.7/992.7 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 875 | 991.5 | 935.4/1,005.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 876 | 980.4 | 910.2/1,000.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 877 | 979.7 | 956.8/1,064.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 878 | 1,014.3 | 923.8/1,030.0 | 237.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 879 | 1,004.3 | 900.8/1,021.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 880 | 1,013.8 | 886.3/1,014.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 881 | 1,005.3 | 891.7/1,021.0 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 882 | 1,003.3 | 886.7/1,019.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 883 | 999.5 | 882.4/1,020.7 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 884 | 999.2 | 909.9/1,052.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 885 | 1,000.2 | 931.5/1,023.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 886 | 1,005.2 | 926.5/1,019.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 887 | 1,005.1 | 969.2/1,022.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 888 | 1,003.4 | 981.2/1,020.8 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 889 | 999.5 | 985.2/1,006.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 890 | 1,002.0 | 949.4/1,009.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 891 | 1,027.6 | 931.0/1,033.4 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 892 | 1,013.3 | 931.3/1,034.3 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 893 | 1,002.1 | 938.3/1,023.1 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 894 | 997.9 | 931.2/1,025.0 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 895 | 262.4 | 224.9/270.9 | 663.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 896 | 608.1 | 607.0/623.9 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 897 | 56.4 | 41.1/58.7 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 898 | 1,014.3 | 1,010.4/1,099.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 899 | 989.7 | 974.8/1,052.7 | 238.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 900 | 965.0 | 937.1/1,038.8 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 901 | 957.7 | 915.6/1,034.8 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 902 | 967.0 | 935.5/1,033.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 903 | 950.7 | 933.9/1,032.3 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 904 | 959.3 | 949.4/1,026.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 905 | 1,015.9 | 949.5/1,024.9 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 906 | 1,026.2 | 946.6/1,035.9 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 907 | 1,016.9 | 957.6/1,031.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 908 | 1,021.3 | 957.3/1,034.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 909 | 1,026.2 | 938.0/1,027.5 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 910 | 1,016.3 | 967.7/1,020.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 911 | 1,019.3 | 1,007.9/1,024.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 912 | 1,020.3 | 1,011.5/1,028.9 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 913 | 1,017.8 | 1,001.0/1,024.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 914 | 1,015.3 | 997.0/1,027.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 915 | 1,021.7 | 992.7/1,025.4 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 916 | 1,015.0 | 1,003.8/1,022.2 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 917 | 996.7 | 993.9/1,026.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 918 | 994.0 | 967.3/1,026.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 919 | 948.8 | 948.3/1,025.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 920 | 941.3 | 929.8/1,024.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 921 | 934.8 | 910.0/1,028.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 922 | 959.4 | 917.3/1,015.4 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 923 | 1,011.0 | 972.1/1,032.3 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 924 | 1,005.3 | 999.6/1,024.8 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 925 | 1,008.4 | 997.4/1,020.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 926 | 999.7 | 995.7/1,009.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 927 | 1,005.9 | 997.5/1,022.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 928 | 1,021.3 | 1,004.0/1,022.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 929 | 1,015.2 | 998.4/1,019.8 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 930 | 1,019.0 | 1,003.9/1,026.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 931 | 1,009.4 | 1,006.0/1,019.4 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 932 | 1,017.1 | 1,011.0/1,028.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 933 | 1,014.3 | 968.7/1,025.6 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 934 | 244.8 | 243.2/261.8 | 661.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 935 | 615.8 | 612.1/621.6 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 936 | 53.7 | 44.5/56.2 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 937 | 1,073.8 | 1,022.6/1,088.9 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 938 | 1,007.1 | 1,001.5/1,048.5 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 939 | 1,005.2 | 1,000.2/1,053.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 940 | 1,000.7 | 963.4/1,041.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 941 | 997.3 | 940.4/1,037.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 942 | 995.3 | 950.2/1,006.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 943 | 995.3 | 927.9/1,003.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 944 | 1,007.5 | 947.3/1,014.3 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 945 | 998.1 | 939.8/1,023.2 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 946 | 993.4 | 935.6/1,030.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 947 | 1,021.5 | 930.1/1,023.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 948 | 962.0 | 941.5/1,027.9 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 949 | 995.2 | 990.6/1,033.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 950 | 1,006.6 | 989.7/1,021.8 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 951 | 1,028.5 | 1,010.7/1,030.5 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 952 | 1,020.0 | 999.4/1,021.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 953 | 1,012.8 | 1,003.4/1,022.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 954 | 1,020.4 | 993.3/1,025.2 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 955 | 1,000.1 | 991.6/1,025.7 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 956 | 999.5 | 988.0/1,024.1 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 957 | 1,000.7 | 994.6/1,018.5 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 958 | 1,001.9 | 991.1/1,018.2 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 959 | 1,015.8 | 986.2/1,020.5 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 960 | 1,000.4 | 948.8/1,026.1 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 961 | 971.4 | 945.2/1,040.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 962 | 932.8 | 931.1/993.9 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 963 | 998.5 | 930.8/1,025.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 964 | 1,018.3 | 928.7/1,032.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 965 | 1,020.9 | 925.4/1,022.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 966 | 1,001.1 | 915.4/1,015.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 967 | 939.0 | 916.2/1,020.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 968 | 941.1 | 913.4/1,015.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 969 | 920.6 | 912.3/1,019.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 970 | 915.2 | 903.8/1,017.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 971 | 941.3 | 904.8/1,023.0 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 972 | 936.0 | 887.4/1,022.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 973 | 248.7 | 236.0/254.2 | 662.1 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 974 | 617.5 | 611.9/623.0 | 6.9 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 975 | 45.7 | 44.9/53.4 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 976 | 997.1 | 948.6/1,049.0 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 977 | 971.1 | 911.3/1,032.9 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 978 | 961.4 | 900.9/1,021.6 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 979 | 1,020.7 | 955.1/1,357.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 980 | 1,019.5 | 947.4/1,020.0 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 981 | 929.0 | 910.9/1,049.5 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 982 | 957.4 | 920.3/969.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 983 | 937.9 | 922.6/970.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 984 | 943.7 | 919.5/958.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 985 | 958.0 | 946.5/977.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 986 | 976.4 | 959.7/1,010.2 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 987 | 990.0 | 961.9/1,005.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 988 | 995.0 | 988.2/1,000.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 989 | 999.2 | 998.5/1,007.2 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 990 | 1,000.8 | 998.9/1,017.5 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 991 | 1,014.7 | 998.6/1,021.5 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 992 | 1,002.6 | 948.5/1,018.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 993 | 1,011.4 | 941.5/1,022.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 994 | 1,017.9 | 931.3/1,022.2 | 235.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 995 | 1,010.0 | 940.0/1,019.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 996 | 988.7 | 954.6/1,005.3 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 997 | 982.6 | 948.8/1,002.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 998 | 984.2 | 961.3/1,024.5 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 999 | 989.2 | 983.9/1,019.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1000 | 981.5 | 935.8/1,033.6 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1001 | 982.4 | 936.1/1,023.7 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1002 | 958.2 | 939.4/1,020.9 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1003 | 934.8 | 921.1/1,022.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1004 | 974.8 | 921.0/999.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1005 | 993.3 | 904.7/1,017.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1006 | 984.5 | 902.7/1,022.6 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1007 | 990.0 | 907.0/1,833.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1008 | 986.1 | 897.0/1,030.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1009 | 989.5 | 907.0/1,026.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1010 | 960.3 | 931.0/1,022.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1011 | 937.1 | 931.5/1,022.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1012 | 266.7 | 229.3/271.1 | 661.7 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1013 | 622.5 | 610.4/626.1 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1014 | 48.2 | 44.0/58.9 | 1.7 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1015 | 1,050.1 | 1,030.6/1,065.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1016 | 1,017.6 | 950.6/1,022.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1017 | 963.0 | 946.5/995.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1018 | 939.4 | 925.0/986.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1019 | 975.0 | 921.1/975.8 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1020 | 961.7 | 936.4/1,002.6 | 235.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1021 | 938.6 | 929.7/998.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1022 | 977.8 | 935.9/1,003.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1023 | 1,000.4 | 970.1/1,004.1 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1024 | 1,019.4 | 992.9/1,031.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1025 | 1,006.5 | 984.2/1,031.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1026 | 995.9 | 986.2/1,026.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1027 | 1,001.3 | 978.5/1,030.1 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1028 | 1,003.0 | 980.1/1,027.9 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1029 | 995.6 | 994.2/1,034.5 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1030 | 1,007.8 | 992.9/1,024.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1031 | 1,017.3 | 1,004.3/1,018.9 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1032 | 1,018.5 | 998.5/1,038.3 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1033 | 1,027.7 | 1,005.5/1,029.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1034 | 989.7 | 987.2/1,024.4 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1035 | 993.5 | 981.9/1,037.6 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1036 | 1,006.0 | 948.2/1,022.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1037 | 988.7 | 944.6/1,032.2 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1038 | 988.1 | 936.7/1,023.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1039 | 991.7 | 935.6/1,049.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1040 | 980.6 | 945.3/1,032.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1041 | 987.5 | 974.3/1,025.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1042 | 989.3 | 977.9/1,009.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1043 | 990.8 | 987.8/1,004.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1044 | 987.8 | 981.2/998.1 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1045 | 996.7 | 979.3/998.0 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1046 | 991.3 | 975.7/993.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1047 | 998.3 | 989.4/1,004.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1048 | 998.9 | 987.5/1,016.1 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1049 | 997.1 | 994.0/1,014.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1050 | 993.2 | 982.3/1,010.3 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1051 | 251.4 | 245.8/252.6 | 662.7 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1052 | 621.5 | 612.8/622.4 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1053 | 45.2 | 43.5/58.3 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1054 | 1,052.7 | 1,008.2/1,074.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1055 | 1,022.8 | 1,014.9/1,035.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1056 | 1,010.5 | 1,002.5/1,030.5 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1057 | 1,015.4 | 992.7/1,016.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1058 | 1,001.6 | 997.2/1,023.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1059 | 1,005.1 | 991.1/1,022.0 | 235.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1060 | 1,007.1 | 999.4/1,019.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1061 | 1,004.2 | 978.7/1,026.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1062 | 1,008.6 | 935.7/1,012.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1063 | 1,002.1 | 990.2/1,023.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1064 | 1,018.4 | 994.8/1,027.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1065 | 1,019.9 | 997.2/1,022.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1066 | 1,024.0 | 993.9/1,027.2 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1067 | 1,015.9 | 995.9/1,020.0 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1068 | 1,022.7 | 981.7/1,023.1 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1069 | 1,013.0 | 946.1/1,014.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1070 | 1,019.6 | 942.6/1,023.5 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1071 | 1,015.7 | 941.6/1,027.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1072 | 1,000.4 | 943.0/1,010.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1073 | 986.8 | 909.9/1,016.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1074 | 950.4 | 912.5/1,013.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1075 | 934.3 | 932.7/1,011.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1076 | 944.4 | 933.9/1,017.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1077 | 949.6 | 933.4/1,015.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1078 | 941.9 | 933.2/1,018.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1079 | 948.6 | 940.2/1,024.8 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1080 | 941.2 | 939.0/996.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1081 | 937.3 | 926.9/945.0 | 235.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1082 | 939.4 | 935.8/941.0 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1083 | 977.6 | 937.8/996.4 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1084 | 988.8 | 962.9/998.5 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1085 | 993.3 | 940.7/994.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1086 | 985.3 | 971.5/1,020.5 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1087 | 992.2 | 925.5/994.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1088 | 983.9 | 917.1/1,006.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1089 | 988.3 | 926.9/1,020.1 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1090 | 252.1 | 242.6/259.5 | 662.7 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1091 | 618.2 | 615.2/618.3 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1092 | 48.6 | 45.1/53.5 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1093 | 1,053.0 | 977.9/1,083.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1094 | 1,042.3 | 941.4/1,044.8 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1095 | 1,028.2 | 944.8/1,031.2 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1096 | 1,020.4 | 930.7/1,023.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1097 | 1,030.7 | 926.1/1,030.9 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1098 | 999.1 | 936.9/1,028.4 | 235.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1099 | 995.4 | 949.6/1,008.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1100 | 969.2 | 953.7/1,001.5 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1101 | 961.3 | 956.2/999.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1102 | 961.9 | 939.2/997.0 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1103 | 961.4 | 946.8/1,001.3 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1104 | 953.7 | 927.0/988.3 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1105 | 968.0 | 938.0/971.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1106 | 973.8 | 933.9/996.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1107 | 986.3 | 934.0/1,003.3 | 235.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1108 | 986.9 | 970.3/1,019.0 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1109 | 991.3 | 983.4/1,031.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1110 | 994.7 | 991.7/1,031.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1111 | 1,027.9 | 982.7/1,029.0 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1112 | 1,020.3 | 994.7/1,029.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1113 | 1,026.6 | 1,025.4/1,029.0 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1114 | 1,025.5 | 1,009.3/1,030.3 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1115 | 1,029.4 | 996.9/1,029.4 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1116 | 1,019.7 | 945.2/1,021.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1117 | 1,002.2 | 940.7/1,002.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1118 | 969.7 | 935.9/990.9 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1119 | 947.3 | 933.2/990.8 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1120 | 961.9 | 929.1/974.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1121 | 937.8 | 917.7/994.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1122 | 930.9 | 925.6/1,024.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1123 | 950.9 | 925.4/1,018.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1124 | 942.0 | 918.7/1,003.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1125 | 932.8 | 921.5/1,020.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1126 | 930.8 | 917.6/1,070.4 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1127 | 929.5 | 919.9/1,074.6 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1128 | 961.2 | 912.3/1,054.6 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1129 | 245.9 | 245.4/248.6 | 661.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1130 | 621.9 | 617.8/624.0 | 6.9 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1131 | 49.0 | 47.0/53.5 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1132 | 1,044.7 | 944.2/1,064.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1133 | 1,016.7 | 934.5/1,033.8 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1134 | 1,001.8 | 943.9/1,027.7 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1135 | 999.5 | 941.2/1,033.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1136 | 998.3 | 967.7/1,030.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1137 | 991.0 | 952.8/1,040.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1138 | 958.8 | 948.4/1,048.9 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1139 | 1,000.0 | 981.2/1,032.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1140 | 991.8 | 975.0/1,026.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1141 | 997.0 | 938.8/999.3 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1142 | 947.4 | 944.6/1,021.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1143 | 930.4 | 909.5/1,032.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1144 | 963.1 | 911.8/1,001.2 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1145 | 956.7 | 923.7/996.8 | 237.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1146 | 996.4 | 939.3/1,010.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1147 | 1,025.2 | 929.2/1,031.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1148 | 1,020.6 | 938.3/1,025.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1149 | 1,011.3 | 1,002.5/1,021.6 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1150 | 1,022.1 | 991.5/1,023.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1151 | 1,018.3 | 992.2/1,029.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1152 | 1,024.6 | 988.9/1,031.7 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1153 | 1,019.5 | 992.4/1,029.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1154 | 1,022.3 | 989.5/1,032.6 | 242.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1155 | 1,020.2 | 982.2/1,030.2 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1156 | 997.7 | 989.2/1,021.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1157 | 990.4 | 960.0/1,030.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1158 | 998.4 | 991.4/1,026.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1159 | 1,001.3 | 964.1/1,025.7 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1160 | 1,021.4 | 987.3/1,031.6 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1161 | 1,023.0 | 1,002.7/1,054.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1162 | 1,020.2 | 990.8/1,032.5 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1163 | 1,031.0 | 990.6/1,037.8 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1164 | 1,023.4 | 990.6/1,026.3 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1165 | 1,023.8 | 990.1/1,026.9 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1166 | 1,016.9 | 990.7/1,021.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1167 | 1,028.2 | 992.3/1,029.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1168 | 256.3 | 253.9/256.6 | 662.0 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1169 | 616.9 | 613.9/617.5 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1170 | 49.6 | 48.9/51.5 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1171 | 1,045.0 | 985.7/1,052.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1172 | 1,006.9 | 1,001.2/1,011.7 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1173 | 1,007.9 | 1,003.5/1,008.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1174 | 1,003.6 | 998.8/1,013.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1175 | 997.1 | 940.1/1,025.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1176 | 991.4 | 941.7/999.3 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1177 | 1,001.4 | 965.5/1,005.0 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1178 | 1,000.5 | 993.6/1,020.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1179 | 994.5 | 938.8/1,021.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1180 | 999.4 | 933.6/1,022.5 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1181 | 1,003.0 | 933.7/1,014.4 | 235.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1182 | 993.9 | 937.2/1,016.2 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1183 | 973.9 | 932.2/1,015.8 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1184 | 940.4 | 924.5/1,024.8 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1185 | 975.6 | 945.3/1,017.6 | 235.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1186 | 1,006.2 | 988.9/1,016.0 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1187 | 1,039.2 | 994.7/1,079.6 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1188 | 994.6 | 988.6/1,034.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1189 | 997.2 | 988.7/1,024.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1190 | 998.2 | 931.9/1,032.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1191 | 994.9 | 946.9/1,035.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1192 | 1,004.4 | 959.7/1,028.9 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1193 | 992.1 | 943.4/1,024.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1194 | 992.0 | 986.6/1,022.9 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1195 | 1,082.3 | 994.2/1,448.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1196 | 1,044.1 | 1,016.7/1,048.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1197 | 1,020.6 | 1,000.9/1,028.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1198 | 990.1 | 988.6/1,024.8 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1199 | 983.9 | 960.4/996.1 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1200 | 989.8 | 941.5/992.0 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1201 | 990.0 | 986.7/995.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1202 | 994.7 | 961.8/996.0 | 235.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1203 | 977.3 | 934.3/983.5 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1204 | 954.7 | 934.3/988.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1205 | 992.9 | 965.1/1,015.7 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1206 | 1,011.1 | 945.5/1,020.9 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1207 | 257.6 | 244.3/262.3 | 662.0 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1208 | 621.5 | 617.2/622.8 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1209 | 46.7 | 46.5/52.7 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1210 | 1,085.9 | 975.0/1,092.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1211 | 1,052.3 | 1,003.9/1,054.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1212 | 1,036.6 | 996.9/1,041.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1213 | 1,028.7 | 995.3/1,035.8 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1214 | 1,024.2 | 966.1/1,035.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1215 | 1,040.5 | 934.7/1,071.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1216 | 1,021.4 | 933.6/1,032.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1217 | 998.4 | 934.8/1,026.0 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1218 | 990.4 | 931.3/1,031.8 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1219 | 991.2 | 932.2/1,032.1 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1220 | 992.5 | 935.0/1,022.3 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1221 | 987.7 | 909.0/997.4 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1222 | 995.3 | 911.5/996.9 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1223 | 994.1 | 943.7/1,017.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1224 | 993.0 | 987.4/1,020.3 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1225 | 1,002.5 | 949.9/1,024.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1226 | 1,013.5 | 943.5/1,018.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1227 | 981.7 | 939.1/1,066.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1228 | 1,003.5 | 940.6/1,029.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1229 | 1,002.8 | 939.3/1,023.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1230 | 1,004.3 | 943.6/1,019.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1231 | 997.0 | 947.2/1,030.2 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1232 | 1,000.5 | 946.3/1,028.2 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1233 | 985.4 | 940.6/1,022.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1234 | 991.6 | 939.9/1,006.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1235 | 990.9 | 987.0/994.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1236 | 1,005.5 | 993.3/1,029.3 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1237 | 952.8 | 933.4/1,034.0 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1238 | 972.6 | 936.7/1,027.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1239 | 992.4 | 929.0/1,026.1 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1240 | 973.5 | 939.4/1,017.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1241 | 938.7 | 915.8/1,019.7 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1242 | 943.0 | 898.4/1,020.8 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1243 | 926.5 | 907.4/1,051.8 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1244 | 953.2 | 929.2/1,030.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1245 | 1,004.3 | 940.5/1,144.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1246 | 243.1 | 241.4/280.0 | 661.9 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1247 | 616.6 | 615.9/621.2 | 6.9 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1248 | 46.0 | 43.2/56.8 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1249 | 1,063.2 | 1,035.1/1,105.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1250 | 1,019.3 | 967.3/1,058.9 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1251 | 1,028.4 | 953.5/1,045.5 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1252 | 1,029.6 | 949.4/1,034.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1253 | 1,033.9 | 944.1/1,050.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1254 | 1,026.4 | 1,008.0/1,032.1 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1255 | 1,025.8 | 991.2/1,031.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1256 | 1,007.1 | 1,004.9/1,033.3 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1257 | 1,028.6 | 992.1/1,029.2 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1258 | 1,006.7 | 1,000.1/1,022.6 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1259 | 1,014.6 | 990.2/1,034.9 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1260 | 1,018.4 | 990.1/1,031.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1261 | 1,024.0 | 994.0/1,037.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1262 | 1,022.9 | 993.0/1,040.2 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1263 | 1,020.9 | 986.5/1,046.4 | 235.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1264 | 1,019.2 | 987.1/1,023.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1265 | 1,021.6 | 993.2/1,025.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1266 | 993.6 | 988.1/1,026.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1267 | 985.1 | 947.5/1,019.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1268 | 987.7 | 966.9/1,026.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1269 | 999.3 | 974.1/1,023.1 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1270 | 1,009.7 | 936.2/1,023.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1271 | 1,022.5 | 984.2/1,041.8 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1272 | 1,015.7 | 1,006.6/1,020.8 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1273 | 1,020.0 | 1,012.3/1,020.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1274 | 1,017.3 | 1,001.9/1,019.9 | 235.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1275 | 1,023.5 | 1,003.5/1,029.7 | 237.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1276 | 1,016.3 | 1,001.3/1,048.7 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1277 | 1,003.4 | 1,000.8/1,024.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1278 | 998.7 | 987.4/1,021.3 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1279 | 1,014.0 | 1,013.4/1,045.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1280 | 1,015.7 | 997.4/1,023.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1281 | 1,017.0 | 987.1/1,022.4 | 237.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1282 | 1,025.1 | 994.0/1,041.0 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1283 | 1,024.0 | 985.6/1,036.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1284 | 1,018.1 | 988.1/1,034.5 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1285 | 256.3 | 245.3/265.4 | 661.8 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1286 | 616.7 | 607.7/619.4 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1287 | 49.7 | 47.8/57.2 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1288 | 1,069.0 | 1,032.4/1,083.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1289 | 1,028.8 | 963.8/1,103.7 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1290 | 1,008.4 | 964.7/1,061.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1291 | 1,022.4 | 956.0/1,045.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1292 | 993.7 | 981.5/1,043.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1293 | 996.5 | 944.2/1,040.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1294 | 995.7 | 937.5/1,027.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1295 | 1,006.7 | 949.4/1,010.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1296 | 1,001.2 | 949.7/1,022.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1297 | 1,004.8 | 942.9/1,014.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1298 | 985.6 | 959.8/1,004.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1299 | 990.6 | 951.6/993.2 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1300 | 972.5 | 948.4/1,007.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1301 | 952.3 | 938.3/966.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1302 | 945.9 | 931.4/969.1 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1303 | 944.9 | 931.8/961.4 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1304 | 953.9 | 949.8/1,027.1 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1305 | 1,029.3 | 936.8/1,042.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1306 | 1,033.1 | 925.9/1,036.4 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1307 | 1,038.1 | 974.0/1,044.5 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1308 | 1,031.2 | 989.7/1,046.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1309 | 1,034.4 | 989.2/1,040.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1310 | 1,027.6 | 992.9/1,039.3 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1311 | 1,033.9 | 993.5/1,086.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1312 | 1,029.7 | 994.8/1,051.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1313 | 1,028.5 | 989.5/1,041.2 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1314 | 1,028.9 | 994.4/1,031.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1315 | 1,019.0 | 989.7/1,033.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1316 | 999.8 | 998.6/1,032.0 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1317 | 1,030.7 | 993.9/1,039.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1318 | 1,005.8 | 984.9/1,033.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1319 | 1,011.7 | 931.0/1,026.5 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1320 | 993.2 | 935.7/1,034.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1321 | 1,019.5 | 929.5/1,033.1 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1322 | 1,018.6 | 915.2/1,028.7 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1323 | 1,003.4 | 935.3/1,030.3 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1324 | 270.6 | 233.7/282.8 | 662.1 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1325 | 613.3 | 607.1/620.3 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1326 | 56.4 | 46.1/57.2 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1327 | 1,070.3 | 1,001.8/1,102.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1328 | 1,020.7 | 965.0/1,055.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1329 | 969.5 | 949.5/1,039.8 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1330 | 952.4 | 947.1/1,044.1 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1331 | 991.7 | 958.8/1,047.2 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1332 | 958.7 | 937.1/1,031.8 | 235.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1333 | 956.4 | 940.5/1,033.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1334 | 950.2 | 938.1/1,024.5 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1335 | 951.8 | 928.7/1,033.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1336 | 948.8 | 946.7/1,030.0 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1337 | 1,015.8 | 936.0/1,026.1 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1338 | 999.4 | 939.9/1,024.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1339 | 1,009.7 | 937.9/1,027.4 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1340 | 1,001.1 | 939.1/1,029.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1341 | 1,006.5 | 961.4/1,039.5 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1342 | 997.7 | 986.3/1,027.7 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1343 | 996.8 | 991.3/1,028.0 | 235.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1344 | 997.9 | 995.3/1,053.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1345 | 999.9 | 988.4/1,029.0 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1346 | 997.0 | 986.6/1,024.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1347 | 993.1 | 945.9/1,019.0 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1348 | 994.2 | 973.1/1,027.8 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1349 | 993.4 | 969.8/1,019.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1350 | 1,003.8 | 992.2/1,027.6 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1351 | 1,005.0 | 991.2/1,024.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1352 | 1,028.9 | 1,000.1/1,033.2 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1353 | 1,029.9 | 986.3/1,058.6 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1354 | 1,028.2 | 1,019.6/1,045.3 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1355 | 1,018.3 | 1,002.9/1,044.4 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1356 | 1,022.9 | 1,005.5/1,030.2 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1357 | 1,022.7 | 1,000.0/1,035.3 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1358 | 1,007.5 | 1,003.6/1,019.1 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1359 | 1,006.3 | 992.7/1,018.8 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1360 | 1,001.7 | 1,001.1/1,019.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1361 | 1,006.3 | 995.3/1,021.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1362 | 1,002.7 | 1,001.2/1,027.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1363 | 251.4 | 249.2/264.4 | 663.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1364 | 620.9 | 613.4/624.6 | 7.2 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1365 | 50.0 | 45.0/60.1 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1366 | 1,015.3 | 1,013.6/1,054.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1367 | 971.0 | 965.0/1,028.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1368 | 954.0 | 942.1/1,009.5 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1369 | 940.9 | 935.6/1,011.9 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1370 | 939.3 | 922.5/954.5 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1371 | 936.1 | 929.2/948.0 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1372 | 950.4 | 921.4/950.8 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1373 | 979.9 | 949.8/993.8 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1374 | 937.2 | 937.0/953.8 | 235.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1375 | 947.3 | 935.5/948.6 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1376 | 938.4 | 937.8/974.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1377 | 934.4 | 908.2/1,006.9 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1378 | 977.5 | 932.8/998.5 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1379 | 934.4 | 922.0/1,003.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1380 | 960.6 | 917.6/1,001.5 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1381 | 932.3 | 923.4/1,006.4 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1382 | 963.4 | 937.1/1,533.4 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1383 | 992.4 | 935.6/1,122.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1384 | 993.7 | 932.5/1,094.0 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1385 | 996.1 | 935.5/1,069.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1386 | 993.1 | 926.6/1,038.8 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1387 | 983.9 | 930.4/1,035.5 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1388 | 995.6 | 986.4/1,028.2 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1389 | 1,010.0 | 991.7/1,026.7 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1390 | 993.8 | 984.6/1,023.2 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1391 | 993.9 | 990.2/1,032.1 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1392 | 972.2 | 926.4/1,021.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1393 | 988.2 | 936.1/1,016.6 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1394 | 1,008.0 | 933.6/1,024.0 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1395 | 986.0 | 931.3/1,003.1 | 237.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1396 | 990.7 | 987.7/999.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1397 | 995.1 | 984.6/1,017.1 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1398 | 990.3 | 984.0/1,016.2 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1399 | 993.4 | 989.6/1,022.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1400 | 1,015.8 | 999.2/1,020.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1401 | 1,015.6 | 998.2/1,018.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1402 | 254.9 | 245.0/264.4 | 662.1 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1403 | 614.3 | 611.8/627.0 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1404 | 51.7 | 46.7/60.3 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1405 | 1,058.4 | 1,016.5/1,081.0 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1406 | 1,015.9 | 993.8/1,046.0 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1407 | 999.5 | 959.9/1,029.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1408 | 1,024.8 | 968.4/1,027.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1409 | 1,028.1 | 947.7/1,029.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1410 | 1,023.4 | 994.1/1,030.2 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1411 | 1,013.6 | 1,011.7/1,023.0 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1412 | 1,029.6 | 1,003.5/1,033.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1413 | 1,031.6 | 1,024.3/1,041.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1414 | 1,022.9 | 997.7/1,029.8 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1415 | 1,022.2 | 1,001.1/1,033.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1416 | 1,026.1 | 995.6/1,035.2 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1417 | 1,021.5 | 990.9/1,038.3 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1418 | 1,021.6 | 988.8/1,034.3 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1419 | 1,017.1 | 988.4/1,036.9 | 235.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1420 | 1,022.0 | 974.5/1,032.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1421 | 1,013.3 | 967.9/1,039.4 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1422 | 1,023.6 | 980.2/1,028.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1423 | 998.0 | 971.5/1,024.0 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1424 | 996.4 | 936.5/1,020.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1425 | 1,002.3 | 938.0/1,022.0 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1426 | 1,014.9 | 932.6/1,030.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1427 | 1,007.6 | 917.7/1,021.7 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1428 | 975.7 | 945.1/1,023.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1429 | 957.1 | 938.5/1,014.5 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1430 | 938.8 | 929.1/1,015.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1431 | 950.5 | 938.1/1,007.5 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1432 | 998.1 | 892.5/1,016.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1433 | 952.5 | 881.2/1,014.3 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1434 | 947.9 | 904.8/1,019.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1435 | 971.2 | 893.3/1,014.8 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1436 | 952.9 | 918.2/988.2 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1437 | 961.5 | 914.3/994.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1438 | 995.1 | 910.9/1,031.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1439 | 999.7 | 910.2/1,016.6 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1440 | 1,010.2 | 899.8/1,025.0 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1441 | 242.6 | 216.3/270.0 | 661.8 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1442 | 618.5 | 610.0/630.6 | 6.9 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1443 | 45.6 | 39.7/58.4 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1444 | 1,013.9 | 950.9/1,053.1 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1445 | 970.9 | 931.8/1,035.5 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1446 | 954.2 | 919.9/1,019.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1447 | 929.7 | 917.6/1,056.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1448 | 944.0 | 896.5/1,017.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1449 | 941.3 | 881.2/1,017.6 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1450 | 906.4 | 892.4/1,015.5 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1451 | 914.6 | 888.3/1,018.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1452 | 924.3 | 886.1/1,020.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1453 | 949.1 | 899.7/1,025.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1454 | 946.3 | 890.3/1,016.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1455 | 940.1 | 898.8/1,014.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1456 | 947.1 | 901.8/1,015.9 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1457 | 946.8 | 908.0/1,017.2 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1458 | 979.7 | 925.4/1,019.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1459 | 1,016.6 | 912.3/1,043.3 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1460 | 1,025.6 | 929.6/1,034.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1461 | 1,019.2 | 934.2/1,050.1 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1462 | 1,020.6 | 929.4/1,037.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1463 | 1,015.9 | 933.8/1,025.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1464 | 1,013.7 | 932.5/1,025.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1465 | 1,025.9 | 1,001.2/1,027.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1466 | 1,017.5 | 1,011.1/1,029.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1467 | 1,015.7 | 995.4/1,025.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1468 | 1,020.4 | 994.0/1,038.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1469 | 1,021.8 | 984.2/1,030.1 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1470 | 1,019.2 | 989.1/1,048.5 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1471 | 1,010.5 | 970.2/1,130.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1472 | 1,022.2 | 931.4/1,042.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1473 | 994.2 | 989.8/1,025.5 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1474 | 1,024.6 | 984.3/1,029.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1475 | 1,020.4 | 989.5/1,022.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1476 | 989.8 | 987.5/1,011.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1477 | 1,008.4 | 986.2/1,017.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1478 | 1,028.2 | 989.4/1,094.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1479 | 1,028.1 | 981.5/1,042.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1480 | 252.0 | 249.6/271.2 | 662.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1481 | 619.1 | 614.0/619.9 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1482 | 43.7 | 43.0/59.3 | 1.7 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1483 | 1,000.9 | 963.4/1,100.6 | 250.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1484 | 1,003.9 | 951.5/1,064.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1485 | 996.7 | 946.2/1,050.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1486 | 1,000.9 | 978.0/1,050.2 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1487 | 1,023.0 | 968.7/1,031.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1488 | 1,022.6 | 944.2/1,099.3 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1489 | 1,021.9 | 994.0/1,047.8 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1490 | 1,025.9 | 1,005.7/1,028.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1491 | 1,019.5 | 980.5/1,063.4 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1492 | 1,024.1 | 1,019.8/1,037.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1493 | 1,020.9 | 1,002.2/1,023.2 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1494 | 1,007.8 | 950.1/1,025.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1495 | 1,016.4 | 985.1/1,022.0 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1496 | 1,022.2 | 1,000.1/1,027.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1497 | 1,018.2 | 995.0/1,020.9 | 235.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1498 | 1,018.3 | 1,007.5/1,020.0 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1499 | 1,029.4 | 987.7/1,043.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1500 | 1,020.2 | 977.4/1,029.7 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1501 | 1,027.9 | 982.9/1,041.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1502 | 1,019.5 | 989.0/1,029.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1503 | 1,020.8 | 989.7/1,021.8 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1504 | 1,024.2 | 984.4/1,039.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1505 | 1,018.2 | 995.7/1,038.3 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1506 | 1,022.7 | 1,017.4/1,027.4 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1507 | 1,024.4 | 1,018.9/1,025.4 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1508 | 1,016.3 | 1,013.8/1,019.5 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1509 | 1,012.8 | 991.4/1,025.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1510 | 1,003.5 | 989.4/1,025.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1511 | 987.8 | 980.6/1,044.5 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1512 | 986.0 | 974.7/1,051.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1513 | 980.3 | 955.1/1,028.3 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1514 | 974.7 | 912.5/1,033.0 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1515 | 975.3 | 911.7/1,033.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1516 | 931.0 | 912.6/1,051.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1517 | 1,013.0 | 889.0/1,028.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1518 | 1,005.8 | 891.3/1,049.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1519 | 237.4 | 220.6/268.9 | 662.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1520 | 620.4 | 608.7/628.9 | 6.9 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1521 | 44.7 | 41.3/59.8 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1522 | 1,058.6 | 940.6/1,106.7 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1523 | 1,031.3 | 917.7/1,039.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1524 | 1,015.0 | 919.7/1,033.0 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1525 | 1,029.7 | 916.6/1,035.2 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1526 | 1,024.6 | 912.8/1,058.9 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1527 | 1,012.9 | 913.7/1,033.3 | 235.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1528 | 982.9 | 923.7/1,038.1 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1529 | 991.3 | 963.3/1,036.0 | 238.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1530 | 998.1 | 954.2/1,036.8 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1531 | 1,020.1 | 944.1/1,043.4 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1532 | 1,021.6 | 939.4/1,035.2 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1533 | 1,004.8 | 907.0/1,032.3 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1534 | 985.2 | 903.5/1,036.6 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1535 | 988.1 | 901.6/1,034.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1536 | 1,011.9 | 913.1/1,017.6 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1537 | 1,001.9 | 928.6/1,015.7 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1538 | 970.1 | 906.6/1,014.4 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1539 | 943.1 | 907.4/1,017.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1540 | 962.3 | 918.6/1,012.8 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1541 | 937.1 | 931.0/1,014.5 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1542 | 989.1 | 910.9/1,028.6 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1543 | 976.2 | 911.8/1,022.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1544 | 988.6 | 914.7/1,020.8 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1545 | 987.9 | 895.6/1,017.3 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1546 | 979.6 | 902.4/1,017.2 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1547 | 984.9 | 898.9/1,021.4 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1548 | 1,052.3 | 914.5/1,076.8 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1549 | 984.5 | 936.9/1,033.2 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1550 | 988.2 | 926.6/1,029.5 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1551 | 945.0 | 936.8/1,024.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1552 | 981.3 | 965.3/1,024.9 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1553 | 1,010.1 | 986.9/1,035.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1554 | 997.1 | 981.5/1,021.1 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1555 | 1,012.7 | 984.8/1,018.8 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1556 | 1,000.6 | 983.3/1,015.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1557 | 999.9 | 982.4/1,017.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1558 | 249.2 | 245.0/273.0 | 661.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1559 | 617.7 | 615.9/620.1 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1560 | 46.0 | 44.7/59.9 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1561 | 1,094.1 | 1,030.4/1,113.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1562 | 1,047.0 | 1,019.2/1,053.8 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1563 | 1,030.4 | 994.4/1,040.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1564 | 1,003.9 | 995.8/1,031.3 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1565 | 1,011.4 | 993.3/1,030.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1566 | 1,015.2 | 1,014.5/1,030.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1567 | 1,029.6 | 1,015.3/1,033.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1568 | 1,021.0 | 986.8/1,024.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1569 | 1,018.0 | 995.6/1,562.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1570 | 1,019.7 | 992.3/1,090.8 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1571 | 1,024.0 | 996.8/1,031.7 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1572 | 1,018.9 | 995.9/1,033.3 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1573 | 1,013.1 | 996.2/1,019.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1574 | 996.9 | 992.9/1,027.8 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1575 | 994.0 | 987.1/1,013.3 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1576 | 990.9 | 984.7/994.4 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1577 | 993.6 | 993.0/1,021.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1578 | 992.2 | 989.8/1,019.6 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1579 | 992.3 | 987.6/994.9 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1580 | 993.0 | 939.3/1,010.0 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1581 | 1,008.1 | 928.3/1,036.9 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1582 | 984.9 | 922.2/1,420.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1583 | 979.1 | 912.4/1,007.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1584 | 995.2 | 934.5/1,005.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1585 | 1,017.5 | 1,006.0/1,021.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1586 | 1,007.9 | 972.3/1,009.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1587 | 1,000.4 | 959.1/1,004.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1588 | 992.8 | 951.1/1,045.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1589 | 995.0 | 991.1/1,001.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1590 | 973.1 | 969.0/1,012.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1591 | 973.5 | 953.4/1,021.2 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1592 | 1,003.3 | 995.0/1,026.0 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1593 | 998.2 | 962.5/999.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1594 | 996.3 | 929.1/1,019.8 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1595 | 1,029.0 | 940.3/1,029.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1596 | 1,025.3 | 942.4/1,026.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1597 | 248.2 | 240.6/268.6 | 661.8 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1598 | 618.0 | 611.7/632.7 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1599 | 52.5 | 44.9/55.1 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1600 | 1,035.0 | 1,032.2/1,063.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1601 | 1,026.1 | 1,022.9/1,082.7 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1602 | 1,033.3 | 1,016.0/1,046.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1603 | 1,024.5 | 1,005.1/1,031.4 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1604 | 1,031.4 | 992.8/1,034.7 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1605 | 1,028.5 | 952.9/1,030.7 | 235.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1606 | 989.7 | 989.6/1,031.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1607 | 984.7 | 942.9/1,028.1 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1608 | 1,004.8 | 973.8/1,026.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1609 | 999.6 | 988.8/1,029.3 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1610 | 1,000.4 | 978.2/1,025.3 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1611 | 1,025.8 | 986.7/1,029.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1612 | 1,022.3 | 988.1/1,055.7 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1613 | 1,020.0 | 985.2/1,038.3 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1614 | 1,023.4 | 985.7/1,030.0 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1615 | 1,025.1 | 983.2/1,029.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1616 | 1,018.6 | 950.7/1,028.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1617 | 1,022.7 | 927.5/1,031.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1618 | 1,031.4 | 926.1/1,048.6 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1619 | 1,034.1 | 908.4/1,039.3 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1620 | 1,029.0 | 900.1/1,034.5 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1621 | 1,032.6 | 907.3/1,048.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1622 | 1,021.3 | 903.9/1,030.9 | 235.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1623 | 1,025.9 | 919.3/1,027.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1624 | 1,018.9 | 989.1/1,029.0 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1625 | 1,020.7 | 1,006.4/1,027.4 | 235.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1626 | 1,030.9 | 988.7/1,031.6 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1627 | 1,031.6 | 1,009.5/1,037.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1628 | 1,027.1 | 1,017.7/1,028.9 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1629 | 1,023.7 | 1,019.0/1,028.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1630 | 1,026.9 | 1,021.0/1,036.2 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1631 | 1,023.2 | 1,022.8/1,023.8 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1632 | 1,026.8 | 1,018.7/1,038.8 | 244.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1633 | 1,017.8 | 1,001.3/1,026.0 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1634 | 1,003.4 | 998.8/1,005.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1635 | 989.6 | 986.9/998.2 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1636 | 256.4 | 241.1/266.3 | 661.5 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1637 | 615.9 | 611.8/618.2 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1638 | 52.1 | 43.3/56.1 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1639 | 1,055.5 | 1,011.8/1,064.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1640 | 1,018.4 | 966.6/1,030.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1641 | 1,000.2 | 990.0/1,001.9 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1642 | 996.1 | 963.4/1,008.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1643 | 995.3 | 989.7/1,006.8 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1644 | 1,000.1 | 944.0/1,001.7 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1645 | 1,005.5 | 938.7/1,013.9 | 235.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1646 | 1,000.7 | 982.5/1,005.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1647 | 1,002.3 | 938.4/1,017.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1648 | 1,005.4 | 970.7/1,006.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1649 | 1,028.4 | 951.8/1,033.6 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1650 | 1,028.8 | 920.7/1,032.8 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1651 | 994.0 | 923.1/1,014.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1652 | 982.8 | 908.4/996.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1653 | 1,000.4 | 923.4/1,020.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1654 | 1,014.1 | 920.9/1,021.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1655 | 997.7 | 932.1/1,037.2 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1656 | 962.3 | 960.3/1,030.2 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1657 | 986.0 | 957.4/1,022.5 | 235.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1658 | 990.5 | 942.5/1,021.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1659 | 1,019.8 | 925.8/1,027.8 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1660 | 991.6 | 935.5/1,025.6 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1661 | 991.9 | 940.9/1,028.1 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1662 | 1,001.8 | 964.7/1,020.6 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1663 | 989.4 | 959.0/1,031.0 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1664 | 978.4 | 955.0/1,027.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1665 | 988.6 | 953.7/1,028.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1666 | 1,020.1 | 945.6/1,026.0 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1667 | 1,020.8 | 965.1/1,025.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1668 | 994.3 | 954.9/1,010.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1669 | 989.5 | 989.3/1,018.9 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1670 | 998.8 | 949.6/1,010.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1671 | 1,001.0 | 960.4/1,023.2 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1672 | 989.5 | 951.2/1,055.8 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1673 | 991.4 | 944.5/1,013.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1674 | 989.1 | 939.8/1,014.8 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1675 | 246.8 | 244.2/249.8 | 661.7 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1676 | 620.0 | 615.9/622.5 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1677 | 49.0 | 48.1/54.3 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1678 | 1,054.7 | 1,009.6/1,098.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1679 | 1,017.3 | 1,008.2/1,048.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1680 | 1,022.7 | 1,009.6/1,030.7 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1681 | 1,015.9 | 1,002.7/1,034.2 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1682 | 1,014.7 | 1,012.7/1,024.9 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1683 | 1,027.2 | 1,000.7/1,030.5 | 235.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1684 | 1,034.6 | 1,011.1/1,071.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1685 | 1,019.5 | 1,003.1/1,032.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1686 | 1,028.1 | 1,003.4/1,034.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1687 | 1,016.9 | 1,003.0/1,040.2 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1688 | 1,018.3 | 964.4/1,026.5 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1689 | 1,015.4 | 987.2/1,025.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1690 | 1,013.5 | 947.6/1,026.2 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1691 | 1,025.9 | 942.1/1,026.4 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1692 | 1,026.4 | 918.9/1,042.2 | 235.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1693 | 1,023.2 | 918.2/1,024.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1694 | 993.7 | 923.4/1,034.6 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1695 | 988.9 | 936.3/1,028.3 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1696 | 983.2 | 939.0/1,026.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1697 | 982.3 | 943.0/1,034.6 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1698 | 991.0 | 941.2/1,032.8 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1699 | 1,011.2 | 996.0/1,030.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1700 | 999.9 | 989.7/1,029.1 | 238.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1701 | 997.4 | 954.6/1,028.3 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1702 | 998.8 | 914.7/1,016.2 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1703 | 998.7 | 922.8/1,003.6 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1704 | 971.2 | 925.8/997.3 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1705 | 990.3 | 917.2/992.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1706 | 992.7 | 917.2/1,007.1 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1707 | 989.9 | 939.9/1,024.0 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1708 | 991.3 | 971.9/1,026.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1709 | 998.5 | 940.9/1,029.9 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1710 | 996.8 | 995.8/1,024.3 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1711 | 1,001.9 | 997.9/1,024.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1712 | 1,002.2 | 1,001.6/1,024.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1713 | 995.7 | 993.7/1,030.8 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1714 | 265.0 | 258.1/269.2 | 661.7 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1715 | 615.3 | 608.8/618.0 | 6.9 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1716 | 57.2 | 55.2/60.8 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1717 | 1,068.4 | 1,042.2/1,107.6 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1718 | 1,038.7 | 1,023.9/1,052.3 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1719 | 1,038.5 | 1,029.7/1,043.5 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1720 | 1,030.0 | 1,018.8/1,036.9 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1721 | 1,033.1 | 1,006.8/1,034.5 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1722 | 1,022.6 | 967.7/1,035.2 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1723 | 992.8 | 966.1/1,024.7 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1724 | 959.0 | 952.0/1,033.0 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1725 | 999.7 | 988.0/1,028.8 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1726 | 1,022.4 | 993.8/1,025.8 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1727 | 1,022.7 | 996.4/1,023.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1728 | 1,011.5 | 989.3/1,033.1 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1729 | 992.5 | 987.9/1,024.6 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1730 | 1,000.6 | 944.0/1,018.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1731 | 979.0 | 944.6/1,027.2 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1732 | 994.0 | 939.1/1,026.9 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1733 | 958.6 | 939.2/1,029.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1734 | 991.6 | 939.0/1,018.1 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1735 | 998.4 | 953.9/1,004.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1736 | 997.3 | 942.9/999.6 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1737 | 970.1 | 942.8/1,004.6 | 236.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1738 | 951.3 | 942.2/1,007.1 | 235.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1739 | 990.9 | 956.6/1,037.6 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1740 | 989.5 | 935.0/1,029.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1741 | 1,004.1 | 960.7/1,028.8 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1742 | 1,005.7 | 990.5/1,030.9 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1743 | 988.0 | 987.6/1,026.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1744 | 995.7 | 985.4/1,023.2 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1745 | 1,019.6 | 983.9/1,021.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1746 | 991.0 | 990.3/1,026.6 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1747 | 1,012.9 | 1,011.4/1,033.3 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1748 | 1,012.7 | 983.7/1,027.0 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1749 | 1,017.2 | 993.2/1,018.4 | 254.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1750 | 1,020.7 | 987.4/1,024.6 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1751 | 999.1 | 976.6/1,023.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1752 | 986.7 | 962.2/993.9 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1753 | 252.9 | 246.8/255.2 | 661.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1754 | 619.0 | 609.4/622.8 | 6.9 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1755 | 52.7 | 44.3/59.7 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1756 | 1,040.4 | 953.6/1,053.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1757 | 956.6 | 939.5/1,008.2 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1758 | 991.5 | 923.1/1,006.3 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1759 | 993.3 | 924.8/1,002.8 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1760 | 992.9 | 938.2/1,013.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1761 | 995.9 | 965.2/1,021.7 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1762 | 992.5 | 992.2/1,027.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1763 | 994.9 | 987.6/1,027.7 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1764 | 998.7 | 987.1/1,024.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1765 | 996.7 | 991.7/1,029.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1766 | 992.1 | 988.9/1,036.9 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1767 | 997.4 | 957.3/1,003.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1768 | 963.0 | 956.2/1,002.6 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1769 | 936.5 | 935.6/1,027.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1770 | 981.9 | 932.5/1,033.1 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1771 | 1,019.8 | 928.4/1,029.4 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1772 | 993.0 | 908.2/1,027.6 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1773 | 997.7 | 899.2/1,008.5 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1774 | 1,004.2 | 909.2/1,015.1 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1775 | 996.7 | 902.9/1,021.9 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1776 | 1,002.0 | 910.3/1,023.5 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1777 | 997.0 | 902.0/1,018.8 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1778 | 980.7 | 904.2/1,020.1 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1779 | 940.6 | 911.4/1,019.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1780 | 946.8 | 906.6/1,014.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1781 | 942.7 | 895.1/1,020.5 | 237.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1782 | 948.7 | 897.9/1,018.6 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1783 | 977.5 | 908.6/1,017.7 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1784 | 999.6 | 911.3/1,019.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1785 | 1,018.4 | 907.6/1,074.6 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1786 | 1,011.2 | 897.9/1,029.6 | 237.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1787 | 1,018.0 | 925.3/1,026.7 | 241.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1788 | 1,014.2 | 930.8/1,070.9 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1789 | 1,041.7 | 951.0/1,060.0 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1790 | 1,039.4 | 940.5/1,098.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1791 | 1,029.7 | 935.3/1,042.0 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1792 | 250.6 | 234.9/277.3 | 661.7 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1793 | 619.3 | 609.9/624.6 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1794 | 45.9 | 41.0/57.9 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1795 | 1,054.4 | 1,000.5/1,082.6 | 237.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1796 | 1,025.6 | 972.6/1,061.3 | 237.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1797 | 1,014.6 | 946.5/1,043.7 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1798 | 1,004.5 | 948.8/1,041.9 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1799 | 1,008.8 | 946.4/1,034.5 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1800 | 1,002.0 | 939.8/1,031.8 | 235.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1801 | 1,003.4 | 923.9/1,038.7 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1802 | 1,006.5 | 930.2/1,037.5 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1803 | 1,004.5 | 906.7/1,024.8 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1804 | 1,004.9 | 908.7/1,022.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1805 | 1,029.9 | 930.2/1,034.8 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1806 | 1,026.9 | 938.4/1,030.4 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1807 | 1,001.8 | 931.6/1,018.2 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1808 | 998.5 | 951.3/1,018.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1809 | 1,006.6 | 932.6/1,026.8 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1810 | 1,024.7 | 932.9/1,030.4 | 237.3 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1811 | 1,020.8 | 980.5/1,035.6 | 237.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1812 | 1,031.3 | 1,021.1/1,032.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1813 | 1,022.4 | 1,020.9/1,028.3 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1814 | 1,027.2 | 1,017.5/1,029.0 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1815 | 1,027.0 | 1,014.0/1,029.9 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1816 | 1,027.7 | 1,017.1/1,029.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1817 | 1,020.8 | 1,009.5/1,030.3 | 238.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1818 | 1,018.2 | 1,017.5/1,028.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1819 | 1,018.6 | 1,017.7/1,021.4 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1820 | 1,013.5 | 1,010.8/1,021.1 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1821 | 1,016.0 | 997.2/1,022.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1822 | 1,014.1 | 998.8/1,016.6 | 237.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1823 | 1,012.5 | 993.6/1,016.5 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1824 | 1,019.2 | 994.8/1,019.6 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1825 | 1,016.2 | 1,004.5/1,018.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1826 | 1,019.9 | 1,014.1/1,026.3 | 235.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1827 | 1,021.6 | 1,010.9/1,025.0 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1828 | 1,021.2 | 1,020.2/1,030.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1829 | 1,017.7 | 991.8/1,021.9 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1830 | 1,010.9 | 989.7/1,028.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1831 | 239.3 | 238.9/267.0 | 661.9 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1832 | 618.9 | 611.6/619.4 | 6.9 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1833 | 44.2 | 42.5/57.2 | 1.8 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1834 | 1,062.3 | 1,045.9/1,098.0 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer01 | 1835 | 1,013.2 | 1,010.0/1,070.3 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer02 | 1836 | 1,028.3 | 1,003.3/1,048.9 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer03 | 1837 | 1,022.8 | 992.2/1,038.5 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer04 | 1838 | 1,002.4 | 997.7/1,044.4 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer05 | 1839 | 997.3 | 967.4/1,037.1 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer06 | 1840 | 1,000.7 | 949.7/1,040.8 | 237.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer07 | 1841 | 990.0 | 937.4/1,036.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer08 | 1842 | 1,011.7 | 991.0/1,019.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer09 | 1843 | 1,014.2 | 1,006.3/1,015.5 | 236.2 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer10 | 1844 | 1,021.6 | 1,019.8/1,029.4 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer11 | 1845 | 1,024.1 | 1,006.0/1,030.8 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer12 | 1846 | 1,031.1 | 991.0/1,075.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer13 | 1847 | 1,032.9 | 995.5/1,036.4 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer14 | 1848 | 1,022.0 | 990.4/1,034.9 | 236.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer15 | 1849 | 1,027.8 | 988.2/1,028.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer16 | 1850 | 1,018.8 | 981.7/1,074.1 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer17 | 1851 | 1,019.7 | 987.3/1,035.3 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer18 | 1852 | 1,015.2 | 1,007.8/1,076.7 | 235.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer19 | 1853 | 1,016.3 | 1,012.1/1,024.2 | 237.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer20 | 1854 | 1,017.0 | 1,001.0/1,017.7 | 235.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer21 | 1855 | 1,012.6 | 1,003.1/1,057.7 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer22 | 1856 | 1,019.0 | 998.1/1,033.8 | 237.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer23 | 1857 | 1,013.0 | 998.5/1,025.6 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer24 | 1858 | 1,016.2 | 1,002.2/1,017.3 | 236.1 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer25 | 1859 | 1,022.3 | 1,020.3/1,023.8 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer26 | 1860 | 1,021.3 | 1,019.1/1,035.1 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer27 | 1861 | 1,029.1 | 1,025.4/1,035.4 | 236.7 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer28 | 1862 | 1,020.4 | 1,015.7/1,031.7 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer29 | 1863 | 1,014.2 | 993.9/1,033.5 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer30 | 1864 | 1,022.4 | 984.5/1,030.2 | 236.4 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer31 | 1865 | 1,028.4 | 979.3/1,030.4 | 237.0 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer32 | 1866 | 1,008.1 | 999.4/1,024.0 | 236.6 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer33 | 1867 | 1,020.8 | 1,012.5/1,023.7 | 236.9 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer34 | 1868 | 1,050.0 | 1,018.6/1,163.2 | 236.8 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_layer35 | 1869 | 1,056.2 | 1,027.9/1,200.0 | 236.5 | cudaLaunchKernel | 43 |
| plan | mir_operator:decode_head | 1870 | 249.1 | 243.6/279.3 | 661.5 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1871 | 620.3 | 609.4/625.0 | 6.9 | cudaStreamSynchronize | 1 |
| plan | pre_d2h_alloc |  | 185.3 | 174.4/212.0 | 0.7 | cudaMemcpyAsync | 0 |
| plan | d2h_stage |  | 123.1 | 122.5/201.2 | 0.9 | cudaEventRecordWithFlags | 0 |
| plan | checksum_complete |  | 45.3 | 42.8/48.0 | 0.0 | cudaEventQuery | 0 |
| lookup | agent_tool_execute_cpu |  | 259.9 | 258.2/341.2 | 0.0 |  | 0 |
| answer | adapter_dispatch |  | 5.7 | 4.0/8.3 | 0.0 |  | 0 |
| answer | token_preprocess_cpu |  | 1,180.1 | 1,127.5/1,182.2 | 0.0 |  | 0 |
| answer | host_input_generate |  | 130.8 | 127.9/133.5 | 0.0 | cudaEventQuery | 0 |
| answer | h2d_stage |  | 131.1 | 127.9/131.7 | 0.4 | cudaEventRecordWithFlags | 0 |
| answer | weight_init |  | 204.5 | 189.4/222.7 | 0.0 | cudaEventDestroy | 0 |
| answer | mir_operator:prefill_embed | 0 | 92.0 | 87.9/98.5 | 1.8 | cudaLaunchKernel | 1 |
| answer | inter_operator_dispatch |  | 20.6 | 17.1/1,334.3 | 0.0 | cudaLaunchKernel | 0.31 |
| answer | mir_operator:prefill_layer00 | 1 | 1,531.9 | 1,505.3/1,536.2 | 420.4 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer01 | 2 | 1,429.9 | 1,425.8/1,442.1 | 418.1 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer02 | 3 | 1,261.0 | 1,221.2/1,266.2 | 417.2 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer03 | 4 | 1,132.7 | 1,127.8/1,147.4 | 417.9 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer04 | 5 | 1,134.0 | 1,125.6/1,136.2 | 412.4 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer05 | 6 | 1,109.0 | 1,087.5/1,128.6 | 412.4 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer06 | 7 | 992.1 | 984.9/1,138.9 | 417.6 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer07 | 8 | 997.4 | 982.9/1,109.4 | 420.0 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer08 | 9 | 1,004.2 | 980.8/1,037.4 | 418.6 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer09 | 10 | 1,009.4 | 979.8/1,029.3 | 416.5 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer10 | 11 | 1,094.1 | 1,006.4/1,109.9 | 413.2 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer11 | 12 | 1,095.5 | 1,028.3/1,127.2 | 416.7 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer12 | 13 | 1,088.2 | 1,080.5/1,121.3 | 416.1 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer13 | 14 | 1,115.8 | 1,083.5/1,129.7 | 416.0 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer14 | 15 | 1,115.0 | 1,102.9/1,117.9 | 417.2 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer15 | 16 | 1,091.9 | 1,090.3/1,124.8 | 419.5 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer16 | 17 | 1,086.3 | 1,084.8/1,156.9 | 412.8 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer17 | 18 | 1,108.0 | 1,055.5/1,117.9 | 417.0 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer18 | 19 | 1,121.5 | 1,029.9/1,129.3 | 421.9 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer19 | 20 | 1,083.6 | 1,028.4/1,124.4 | 417.3 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer20 | 21 | 1,072.7 | 1,059.2/1,126.1 | 414.4 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer21 | 22 | 1,026.5 | 1,025.6/1,129.2 | 412.7 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer22 | 23 | 1,023.2 | 1,016.9/1,114.2 | 411.6 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer23 | 24 | 1,027.4 | 1,020.7/1,121.2 | 411.9 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer24 | 25 | 1,023.8 | 1,017.1/1,120.5 | 416.7 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer25 | 26 | 1,019.6 | 1,009.6/1,144.6 | 416.5 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer26 | 27 | 1,077.8 | 1,042.6/1,104.0 | 416.7 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer27 | 28 | 1,072.8 | 1,024.9/1,090.8 | 417.2 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer28 | 29 | 1,088.2 | 1,065.3/1,096.8 | 414.2 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer29 | 30 | 1,086.2 | 1,069.5/1,116.8 | 417.8 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer30 | 31 | 1,107.3 | 1,075.9/1,113.4 | 418.0 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer31 | 32 | 1,109.5 | 1,081.7/1,121.5 | 413.1 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer32 | 33 | 1,112.1 | 1,074.1/1,116.8 | 413.3 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer33 | 34 | 1,120.3 | 1,077.3/1,124.7 | 415.8 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer34 | 35 | 1,097.3 | 1,073.8/1,116.1 | 417.6 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_layer35 | 36 | 1,100.6 | 1,078.9/1,114.4 | 418.5 | cudaLaunchKernel | 45 |
| answer | mir_operator:prefill_head | 37 | 269.4 | 263.1/284.3 | 1,045.6 | cudaLaunchKernel | 9 |
| answer | mir_operator:prefill_sample | 38 | 994.0 | 990.2/995.9 | 8.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 39 | 47.7 | 45.9/58.2 | 2.0 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 40 | 1,060.4 | 1,041.7/1,121.7 | 244.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 41 | 1,025.3 | 1,017.2/1,058.1 | 239.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 42 | 1,016.1 | 1,006.8/1,044.8 | 238.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 43 | 1,017.4 | 1,003.1/1,028.5 | 238.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 44 | 1,005.9 | 1,002.2/1,041.0 | 239.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 45 | 997.1 | 994.2/1,042.1 | 238.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 46 | 1,031.2 | 990.5/1,032.4 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 47 | 1,027.8 | 986.8/1,048.3 | 238.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 48 | 1,033.4 | 1,008.1/1,043.4 | 238.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 49 | 1,033.2 | 1,014.8/1,036.0 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 50 | 1,027.5 | 1,026.7/1,030.6 | 238.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 51 | 1,025.3 | 1,022.1/1,027.5 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 52 | 1,028.6 | 1,022.8/1,043.3 | 238.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 53 | 1,028.3 | 1,024.7/1,034.0 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 54 | 1,023.1 | 997.6/1,040.2 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 55 | 1,020.2 | 992.2/1,041.7 | 239.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 56 | 1,034.8 | 992.0/1,036.5 | 238.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 57 | 1,020.3 | 994.6/1,037.5 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 58 | 1,013.8 | 994.9/1,031.1 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 59 | 1,023.4 | 998.7/1,030.5 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 60 | 1,016.5 | 999.5/1,031.3 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 61 | 1,020.5 | 985.6/1,031.6 | 238.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 62 | 1,022.6 | 935.8/1,028.8 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 63 | 1,022.1 | 998.2/1,043.5 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 64 | 1,027.9 | 1,012.2/1,033.5 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 65 | 1,029.9 | 1,023.3/1,034.5 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 66 | 1,016.7 | 1,013.7/1,030.8 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 67 | 1,021.2 | 1,020.5/1,047.8 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 68 | 1,010.3 | 1,004.6/1,030.7 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 69 | 1,008.9 | 989.2/1,023.9 | 238.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 70 | 1,022.7 | 991.7/1,039.0 | 238.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 71 | 1,029.3 | 991.2/1,062.2 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 72 | 1,025.8 | 994.9/1,027.6 | 238.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 73 | 1,025.9 | 989.8/1,044.2 | 238.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 74 | 1,009.4 | 988.0/1,028.5 | 238.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 75 | 1,002.1 | 994.8/1,029.2 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 76 | 254.6 | 242.6/269.2 | 643.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 77 | 593.9 | 578.4/606.3 | 7.2 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 78 | 53.3 | 48.3/55.1 | 1.7 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 79 | 1,055.7 | 1,050.2/1,066.5 | 240.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 80 | 1,019.0 | 978.8/1,039.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 81 | 1,012.6 | 960.6/1,032.0 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 82 | 1,001.9 | 953.8/1,037.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 83 | 1,005.5 | 1,002.1/1,018.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 84 | 1,002.4 | 993.3/1,008.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 85 | 1,001.9 | 991.9/1,003.8 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 86 | 1,001.6 | 993.5/1,005.3 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 87 | 997.0 | 991.7/1,022.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 88 | 1,002.9 | 989.3/1,031.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 89 | 991.3 | 986.5/1,016.1 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 90 | 992.3 | 986.5/1,005.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 91 | 996.7 | 990.7/1,005.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 92 | 994.7 | 988.6/998.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 93 | 1,010.1 | 1,008.3/1,027.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 94 | 1,024.1 | 941.7/1,026.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 95 | 1,006.0 | 995.9/1,030.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 96 | 988.8 | 976.5/1,032.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 97 | 984.4 | 937.4/1,036.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 98 | 985.2 | 985.2/1,062.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 99 | 995.8 | 957.9/1,035.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 100 | 1,008.8 | 995.3/1,034.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 101 | 1,019.8 | 958.3/1,021.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 102 | 1,022.8 | 1,002.4/1,029.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 103 | 1,016.9 | 997.9/1,032.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 104 | 1,022.0 | 1,013.1/1,035.1 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 105 | 1,017.2 | 996.4/1,032.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 106 | 1,020.2 | 1,004.2/1,025.0 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 107 | 1,011.5 | 994.3/1,027.4 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 108 | 1,012.6 | 995.5/1,031.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 109 | 1,036.1 | 1,003.8/1,036.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 110 | 1,025.1 | 996.1/1,037.2 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 111 | 1,004.2 | 994.3/1,017.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 112 | 1,003.6 | 985.4/1,031.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 113 | 1,020.9 | 992.2/1,067.4 | 238.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 114 | 1,029.6 | 977.4/1,032.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 115 | 249.8 | 231.5/275.4 | 661.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 116 | 621.6 | 609.4/627.4 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 117 | 45.5 | 42.7/61.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 118 | 1,053.0 | 995.4/1,095.8 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 119 | 1,014.3 | 953.0/1,059.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 120 | 1,030.9 | 948.8/1,043.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 121 | 1,026.4 | 954.9/1,034.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 122 | 1,027.0 | 932.1/1,032.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 123 | 1,022.8 | 907.5/1,038.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 124 | 1,028.2 | 903.5/1,057.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 125 | 1,017.1 | 912.6/1,033.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 126 | 1,004.6 | 916.6/1,027.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 127 | 1,014.4 | 935.5/1,017.0 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 128 | 1,025.4 | 935.7/1,025.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 129 | 1,017.6 | 994.1/1,036.2 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 130 | 1,002.6 | 988.0/1,013.2 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 131 | 991.5 | 991.4/1,039.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 132 | 1,000.3 | 990.8/1,021.4 | 235.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 133 | 998.8 | 998.0/1,021.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 134 | 995.6 | 993.2/1,017.7 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 135 | 997.8 | 984.2/1,021.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 136 | 1,022.8 | 988.1/1,032.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 137 | 1,029.5 | 1,022.6/1,029.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 138 | 1,014.1 | 993.5/1,026.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 139 | 997.1 | 962.6/1,025.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 140 | 999.1 | 929.3/1,024.4 | 235.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 141 | 995.4 | 969.5/1,023.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 142 | 1,000.6 | 997.5/1,020.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 143 | 1,016.9 | 988.8/1,022.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 144 | 1,016.3 | 1,003.6/1,036.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 145 | 1,017.1 | 986.3/1,026.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 146 | 1,026.0 | 988.4/1,034.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 147 | 1,017.2 | 989.7/1,029.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 148 | 1,015.6 | 990.8/1,023.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 149 | 1,012.3 | 989.4/1,028.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 150 | 1,013.4 | 987.3/1,028.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 151 | 1,021.5 | 983.8/1,026.1 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 152 | 1,017.8 | 978.1/1,030.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 153 | 1,018.6 | 1,016.4/1,034.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 154 | 250.6 | 250.2/281.1 | 661.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 155 | 618.3 | 608.7/622.8 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 156 | 45.2 | 44.8/57.4 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 157 | 1,089.0 | 1,083.5/1,106.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 158 | 1,049.0 | 1,012.0/1,050.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 159 | 1,037.6 | 1,002.2/1,043.2 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 160 | 1,029.2 | 1,008.4/1,035.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 161 | 1,027.7 | 1,021.9/1,040.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 162 | 1,034.7 | 999.0/1,038.6 | 235.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 163 | 1,032.9 | 1,005.9/1,433.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 164 | 1,024.9 | 998.4/1,072.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 165 | 1,023.4 | 989.1/1,054.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 166 | 1,028.3 | 1,010.6/1,043.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 167 | 1,020.0 | 1,014.3/1,037.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 168 | 1,024.4 | 1,023.6/1,030.7 | 235.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 169 | 1,019.2 | 1,012.3/1,041.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 170 | 1,039.6 | 1,021.3/1,043.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 171 | 1,013.1 | 989.8/1,017.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 172 | 1,005.8 | 986.5/1,009.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 173 | 1,002.9 | 997.6/1,038.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 174 | 1,005.2 | 991.0/1,023.1 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 175 | 1,028.6 | 1,022.5/1,685.2 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 176 | 1,024.5 | 1,021.5/1,027.8 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 177 | 1,025.6 | 1,021.6/1,037.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 178 | 1,034.1 | 959.1/1,043.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 179 | 1,024.2 | 939.8/1,036.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 180 | 1,017.9 | 940.0/1,033.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 181 | 1,025.4 | 938.1/1,027.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 182 | 1,000.6 | 945.5/1,024.8 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 183 | 1,000.8 | 915.6/1,020.0 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 184 | 1,003.3 | 910.3/1,047.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 185 | 999.8 | 910.3/1,014.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 186 | 1,006.0 | 913.0/1,015.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 187 | 1,001.1 | 961.3/1,015.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 188 | 997.3 | 992.3/1,020.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 189 | 998.3 | 985.3/1,014.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 190 | 1,001.0 | 947.0/1,011.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 191 | 997.0 | 995.1/1,018.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 192 | 997.9 | 990.9/1,023.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 193 | 257.0 | 256.6/260.3 | 661.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 194 | 615.2 | 612.3/621.6 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 195 | 50.6 | 45.6/57.0 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 196 | 1,060.1 | 1,052.9/1,082.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 197 | 1,033.6 | 1,025.9/1,033.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 198 | 1,029.6 | 1,012.0/1,037.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 199 | 1,024.2 | 974.0/1,027.8 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 200 | 1,021.2 | 943.6/1,036.5 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 201 | 1,037.2 | 946.3/1,041.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 202 | 992.4 | 954.5/1,040.0 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 203 | 995.8 | 992.2/1,037.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 204 | 996.4 | 940.3/1,034.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 205 | 988.7 | 980.2/1,034.5 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 206 | 994.6 | 952.3/1,025.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 207 | 1,000.7 | 956.0/1,033.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 208 | 991.5 | 924.2/1,029.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 209 | 974.6 | 932.1/1,033.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 210 | 1,003.2 | 975.8/1,038.3 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 211 | 1,000.2 | 954.4/1,031.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 212 | 1,000.3 | 935.9/1,034.8 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 213 | 942.1 | 936.3/1,029.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 214 | 975.7 | 950.5/1,030.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 215 | 942.7 | 935.5/1,033.3 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 216 | 980.1 | 941.6/1,025.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 217 | 984.6 | 947.4/1,031.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 218 | 990.5 | 943.6/1,030.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 219 | 967.9 | 949.4/1,031.2 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 220 | 948.4 | 947.8/1,032.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 221 | 955.4 | 951.5/1,027.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 222 | 988.4 | 952.9/1,030.5 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 223 | 992.5 | 958.6/1,033.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 224 | 986.6 | 949.1/1,029.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 225 | 997.9 | 983.5/1,034.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 226 | 999.8 | 987.5/1,030.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 227 | 997.4 | 980.9/1,031.0 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 228 | 991.0 | 988.0/1,030.2 | 235.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 229 | 995.7 | 983.1/1,024.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 230 | 996.5 | 980.1/1,064.0 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 231 | 999.2 | 954.1/1,043.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 232 | 272.3 | 226.8/274.3 | 663.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 233 | 594.2 | 588.4/622.7 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 234 | 57.1 | 42.5/60.9 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 235 | 1,061.8 | 992.5/1,098.8 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 236 | 1,031.1 | 962.1/1,051.7 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 237 | 1,018.5 | 948.4/1,018.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 238 | 1,005.1 | 928.3/1,013.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 239 | 1,004.1 | 914.3/1,008.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 240 | 995.6 | 955.9/1,008.0 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 241 | 1,001.3 | 998.4/1,005.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 242 | 1,000.1 | 956.7/1,016.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 243 | 998.7 | 970.1/1,010.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 244 | 984.8 | 977.1/1,010.2 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 245 | 982.4 | 940.9/1,021.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 246 | 986.3 | 970.2/1,011.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 247 | 995.0 | 991.2/1,008.5 | 238.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 248 | 991.7 | 983.2/1,004.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 249 | 1,000.6 | 977.0/1,036.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 250 | 999.8 | 984.7/1,036.5 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 251 | 1,031.9 | 997.0/1,032.2 | 238.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 252 | 1,017.2 | 997.4/1,045.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 253 | 1,020.7 | 992.5/1,039.0 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 254 | 1,012.4 | 1,010.5/1,030.1 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 255 | 1,015.6 | 1,001.3/1,029.4 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 256 | 1,011.5 | 972.6/1,030.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 257 | 1,013.1 | 939.9/1,035.9 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 258 | 1,013.8 | 985.1/1,031.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 259 | 1,005.1 | 998.6/1,032.7 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 260 | 983.1 | 983.0/1,029.5 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 261 | 980.7 | 943.7/1,028.7 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 262 | 993.9 | 900.6/1,037.3 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 263 | 991.5 | 881.7/1,038.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 264 | 995.3 | 911.7/1,047.6 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 265 | 975.5 | 894.6/998.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 266 | 932.1 | 908.3/993.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 267 | 950.9 | 908.4/999.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 268 | 997.2 | 908.6/1,000.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 269 | 1,000.6 | 893.1/1,002.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 270 | 987.9 | 884.8/992.8 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 271 | 256.0 | 214.7/269.5 | 662.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 272 | 623.2 | 612.7/631.0 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 273 | 55.7 | 40.0/60.7 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 274 | 1,071.5 | 939.4/1,095.1 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 275 | 1,024.8 | 928.0/1,053.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 276 | 1,015.4 | 920.1/1,039.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 277 | 1,016.7 | 915.6/1,032.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 278 | 1,006.0 | 953.8/1,034.4 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 279 | 1,005.9 | 933.8/1,039.6 | 235.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 280 | 1,031.0 | 936.0/1,034.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 281 | 1,024.6 | 934.8/1,039.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 282 | 1,036.4 | 929.2/1,359.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 283 | 999.1 | 972.5/1,026.3 | 235.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 284 | 999.5 | 931.6/1,025.1 | 235.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 285 | 959.7 | 925.4/1,024.0 | 235.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 286 | 946.9 | 910.6/1,006.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 287 | 917.8 | 916.5/998.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 288 | 934.9 | 923.1/991.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 289 | 983.8 | 983.2/1,005.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 290 | 999.0 | 989.8/999.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 291 | 1,003.4 | 987.1/1,018.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 292 | 999.2 | 980.9/1,030.2 | 235.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 293 | 1,007.0 | 987.9/1,025.5 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 294 | 1,006.1 | 990.4/1,033.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 295 | 1,010.8 | 995.3/1,017.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 296 | 1,000.1 | 998.7/1,013.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 297 | 1,001.6 | 998.2/1,013.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 298 | 998.8 | 997.0/1,024.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 299 | 1,003.2 | 1,001.5/1,016.6 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 300 | 1,016.6 | 997.1/1,019.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 301 | 1,012.7 | 998.1/1,021.7 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 302 | 1,007.6 | 1,002.3/1,013.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 303 | 1,014.3 | 1,006.1/1,090.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 304 | 1,002.9 | 998.4/1,044.6 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 305 | 1,001.7 | 984.7/1,010.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 306 | 1,001.3 | 932.1/1,035.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 307 | 1,002.2 | 931.1/1,028.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 308 | 1,001.1 | 938.7/1,003.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 309 | 1,000.3 | 946.9/1,004.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 310 | 261.3 | 238.9/275.6 | 662.0 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 311 | 614.3 | 610.4/617.8 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 312 | 57.3 | 43.8/59.6 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 313 | 1,067.6 | 1,049.5/1,069.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 314 | 1,003.3 | 992.8/1,031.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 315 | 999.1 | 999.0/1,009.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 316 | 953.5 | 952.0/988.5 | 235.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 317 | 968.4 | 963.2/1,002.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 318 | 985.3 | 947.8/986.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 319 | 985.5 | 945.1/1,010.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 320 | 1,007.8 | 988.3/1,045.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 321 | 998.8 | 982.8/1,007.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 322 | 992.8 | 943.9/1,016.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 323 | 998.2 | 935.1/998.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 324 | 982.6 | 938.0/1,028.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 325 | 987.2 | 949.2/996.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 326 | 979.3 | 946.2/990.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 327 | 988.1 | 942.5/999.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 328 | 983.6 | 937.8/1,001.6 | 235.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 329 | 1,009.4 | 984.8/1,020.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 330 | 1,022.9 | 990.4/1,023.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 331 | 1,014.2 | 995.5/1,019.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 332 | 1,002.4 | 989.8/1,015.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 333 | 1,001.3 | 996.3/1,030.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 334 | 1,013.4 | 997.1/1,025.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 335 | 992.3 | 968.6/1,002.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 336 | 988.6 | 929.6/1,004.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 337 | 990.0 | 930.3/1,005.1 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 338 | 993.7 | 929.8/998.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 339 | 1,000.4 | 911.5/1,004.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 340 | 1,017.5 | 927.3/1,028.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 341 | 1,016.6 | 981.1/1,023.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 342 | 1,019.7 | 990.3/1,027.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 343 | 1,018.7 | 997.2/1,023.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 344 | 1,026.1 | 1,011.5/1,027.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 345 | 1,020.3 | 992.7/1,027.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 346 | 1,007.5 | 1,002.4/1,020.1 | 246.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 347 | 1,007.1 | 1,001.8/1,020.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 348 | 1,017.7 | 994.0/1,027.4 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 349 | 270.3 | 251.1/270.9 | 662.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 350 | 609.0 | 604.8/657.1 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 351 | 54.9 | 48.3/56.1 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 352 | 1,080.0 | 1,056.1/1,104.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 353 | 1,062.1 | 1,023.9/1,062.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 354 | 1,035.1 | 1,009.8/1,044.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 355 | 1,034.1 | 996.0/1,038.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 356 | 1,010.9 | 1,006.1/1,071.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 357 | 999.3 | 969.8/1,033.0 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 358 | 997.8 | 985.8/1,031.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 359 | 1,021.5 | 942.7/1,029.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 360 | 1,002.6 | 940.9/1,026.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 361 | 998.1 | 939.3/1,040.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 362 | 1,000.3 | 940.6/1,029.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 363 | 992.0 | 942.7/1,032.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 364 | 999.2 | 980.3/1,033.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 365 | 998.5 | 949.8/1,028.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 366 | 995.2 | 944.0/1,028.6 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 367 | 998.5 | 944.7/1,591.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 368 | 998.9 | 974.6/1,154.0 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 369 | 997.1 | 989.1/1,078.2 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 370 | 1,041.1 | 993.7/1,067.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 371 | 999.8 | 995.4/1,050.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 372 | 1,002.3 | 996.1/1,017.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 373 | 999.9 | 995.9/1,030.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 374 | 995.6 | 991.5/1,035.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 375 | 1,022.8 | 996.1/1,023.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 376 | 1,020.1 | 1,012.8/1,030.5 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 377 | 1,022.1 | 1,021.8/1,024.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 378 | 1,022.7 | 996.8/1,026.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 379 | 1,022.8 | 990.9/1,031.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 380 | 1,019.7 | 989.7/1,027.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 381 | 1,022.1 | 1,004.8/1,023.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 382 | 1,023.4 | 1,002.2/1,026.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 383 | 1,010.9 | 991.3/1,027.8 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 384 | 1,018.3 | 987.8/1,064.0 | 302.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 385 | 1,003.0 | 990.9/1,052.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 386 | 1,007.1 | 985.0/1,024.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 387 | 1,000.9 | 947.7/1,019.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 388 | 264.6 | 242.6/267.6 | 661.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 389 | 612.9 | 602.8/624.6 | 7.2 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 390 | 54.0 | 53.8/57.9 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 391 | 1,047.1 | 1,028.0/1,091.6 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 392 | 1,031.8 | 964.7/1,071.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 393 | 1,037.5 | 951.7/1,039.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 394 | 1,031.8 | 944.5/1,038.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 395 | 1,029.5 | 939.8/1,036.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 396 | 1,029.7 | 978.5/1,032.8 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 397 | 1,027.4 | 1,023.1/1,037.8 | 279.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 398 | 1,026.9 | 1,016.7/1,027.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 399 | 1,029.6 | 1,023.9/1,029.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 400 | 1,026.5 | 1,020.2/1,026.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 401 | 1,032.5 | 1,029.2/1,166.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 402 | 1,029.4 | 1,026.6/1,061.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 403 | 1,033.2 | 1,023.2/1,045.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 404 | 1,030.1 | 1,021.4/1,047.5 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 405 | 1,030.1 | 1,019.9/1,035.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 406 | 1,025.3 | 987.3/1,035.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 407 | 1,026.8 | 995.0/1,027.0 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 408 | 1,023.7 | 986.9/1,045.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 409 | 999.4 | 998.2/1,043.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 410 | 994.0 | 983.5/1,034.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 411 | 996.7 | 942.3/1,045.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 412 | 998.4 | 919.5/1,030.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 413 | 990.8 | 926.3/1,038.5 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 414 | 991.2 | 913.1/1,046.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 415 | 993.9 | 915.9/1,038.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 416 | 993.1 | 921.1/1,033.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 417 | 989.0 | 925.2/1,023.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 418 | 986.0 | 891.4/1,032.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 419 | 992.6 | 907.5/1,023.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 420 | 981.9 | 916.6/1,002.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 421 | 988.2 | 955.3/1,003.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 422 | 970.9 | 920.8/1,001.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 423 | 934.5 | 924.5/986.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 424 | 931.3 | 919.1/1,000.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 425 | 931.1 | 925.3/966.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 426 | 924.1 | 914.8/1,014.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 427 | 245.4 | 235.6/266.1 | 661.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 428 | 616.3 | 597.5/622.7 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 429 | 52.4 | 47.5/56.4 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 430 | 1,026.9 | 993.9/1,061.0 | 235.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 431 | 996.0 | 960.0/1,031.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 432 | 1,021.8 | 945.2/1,048.2 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 433 | 1,000.9 | 985.2/1,032.6 | 235.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 434 | 991.0 | 942.0/1,031.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 435 | 957.4 | 951.6/1,028.4 | 235.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 436 | 1,010.5 | 993.3/1,038.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 437 | 1,021.2 | 992.7/1,029.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 438 | 1,026.9 | 987.6/1,034.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 439 | 1,029.3 | 985.8/1,029.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 440 | 1,025.1 | 981.7/1,031.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 441 | 990.6 | 984.8/1,040.4 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 442 | 991.2 | 945.3/1,031.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 443 | 991.6 | 930.5/1,040.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 444 | 982.4 | 944.6/1,033.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 445 | 983.8 | 959.7/1,004.0 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 446 | 990.1 | 984.7/1,033.0 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 447 | 1,008.4 | 994.2/1,029.2 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 448 | 998.2 | 996.2/1,033.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 449 | 998.0 | 991.2/1,025.5 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 450 | 982.3 | 952.4/1,043.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 451 | 996.3 | 945.4/1,046.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 452 | 994.0 | 934.3/1,028.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 453 | 993.0 | 943.2/1,028.8 | 295.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 454 | 990.0 | 938.9/1,036.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 455 | 952.2 | 930.3/1,033.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 456 | 1,001.1 | 965.6/1,033.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 457 | 995.3 | 955.4/1,069.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 458 | 990.1 | 983.7/1,045.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 459 | 988.3 | 981.1/1,042.0 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 460 | 980.4 | 968.2/1,035.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 461 | 981.5 | 936.9/1,026.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 462 | 986.8 | 934.1/1,039.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 463 | 987.7 | 923.5/1,026.5 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 464 | 986.5 | 906.9/1,043.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 465 | 1,003.3 | 902.2/1,031.7 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 466 | 254.4 | 232.4/289.4 | 661.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 467 | 617.1 | 612.8/674.0 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 468 | 50.2 | 42.4/59.6 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 469 | 1,046.9 | 993.8/1,118.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 470 | 971.4 | 934.2/1,038.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 471 | 933.4 | 928.6/1,016.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 472 | 943.5 | 935.7/1,021.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 473 | 946.8 | 936.0/1,020.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 474 | 970.5 | 937.0/1,039.9 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 475 | 935.7 | 931.3/1,052.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 476 | 932.7 | 930.2/1,042.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 477 | 937.1 | 910.2/1,043.6 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 478 | 939.2 | 917.6/1,031.7 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 479 | 946.3 | 901.7/1,044.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 480 | 970.5 | 902.6/1,035.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 481 | 999.7 | 916.6/1,034.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 482 | 988.0 | 933.3/1,034.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 483 | 991.6 | 930.9/1,040.2 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 484 | 982.9 | 941.4/1,041.2 | 245.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 485 | 985.5 | 935.3/1,049.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 486 | 982.8 | 928.6/1,027.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 487 | 988.9 | 930.3/1,035.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 488 | 988.7 | 901.5/1,030.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 489 | 997.5 | 956.0/1,028.1 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 490 | 969.5 | 951.4/1,034.4 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 491 | 941.8 | 941.3/1,029.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 492 | 942.7 | 937.0/1,026.2 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 493 | 981.3 | 942.2/1,030.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 494 | 988.8 | 941.4/1,046.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 495 | 1,017.1 | 932.3/1,107.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 496 | 1,015.0 | 992.2/1,048.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 497 | 1,014.9 | 989.8/1,032.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 498 | 1,007.2 | 984.6/1,027.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 499 | 1,006.3 | 929.4/1,045.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 500 | 986.8 | 967.2/1,008.1 | 235.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 501 | 988.6 | 940.9/1,001.8 | 240.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 502 | 987.3 | 920.6/997.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 503 | 992.3 | 910.1/1,000.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 504 | 985.2 | 906.2/1,022.3 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 505 | 239.2 | 226.0/266.9 | 661.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 506 | 623.7 | 621.1/624.0 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 507 | 43.9 | 40.4/55.9 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 508 | 1,059.7 | 955.6/1,061.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 509 | 1,030.7 | 943.7/1,039.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 510 | 1,025.4 | 932.4/1,073.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 511 | 998.8 | 936.5/1,069.2 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 512 | 986.5 | 936.8/1,040.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 513 | 939.5 | 927.7/1,031.0 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 514 | 932.3 | 931.5/1,041.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 515 | 991.1 | 978.9/1,038.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 516 | 983.8 | 945.0/1,030.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 517 | 978.8 | 929.9/1,031.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 518 | 975.4 | 936.6/1,031.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 519 | 1,008.4 | 966.6/1,029.9 | 282.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 520 | 991.5 | 955.1/1,027.5 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 521 | 990.1 | 951.7/1,003.6 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 522 | 984.2 | 956.5/998.2 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 523 | 992.6 | 987.5/996.8 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 524 | 988.9 | 961.2/996.9 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 525 | 986.5 | 933.1/995.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 526 | 987.6 | 982.3/1,010.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 527 | 1,022.6 | 979.5/1,026.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 528 | 1,019.9 | 990.8/1,029.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 529 | 1,023.7 | 982.0/1,026.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 530 | 1,013.5 | 945.6/1,022.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 531 | 1,017.2 | 1,002.5/1,017.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 532 | 1,013.6 | 1,003.0/1,018.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 533 | 995.3 | 991.4/1,018.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 534 | 1,001.9 | 990.1/1,011.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 535 | 1,007.1 | 988.2/1,012.7 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 536 | 995.9 | 989.4/996.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 537 | 997.6 | 990.9/1,010.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 538 | 983.0 | 940.2/990.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 539 | 984.0 | 905.2/1,014.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 540 | 988.5 | 916.2/1,013.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 541 | 986.5 | 941.9/1,014.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 542 | 1,002.5 | 934.6/1,018.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 543 | 1,025.8 | 917.6/1,028.5 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 544 | 250.1 | 249.0/250.8 | 661.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 545 | 612.5 | 605.2/620.5 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 546 | 44.9 | 44.1/51.5 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 547 | 1,037.1 | 1,008.6/1,071.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 548 | 1,022.1 | 971.9/1,038.1 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 549 | 1,030.1 | 955.3/1,031.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 550 | 1,000.0 | 960.8/1,028.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 551 | 998.9 | 946.9/1,031.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 552 | 986.5 | 956.1/1,028.0 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 553 | 994.4 | 921.5/1,025.3 | 281.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 554 | 1,005.9 | 942.4/1,889.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 555 | 1,023.9 | 950.4/1,115.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 556 | 1,022.8 | 930.1/1,069.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 557 | 1,006.2 | 919.0/1,053.0 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 558 | 987.9 | 925.8/1,062.9 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 559 | 984.6 | 979.8/1,027.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 560 | 985.3 | 960.7/1,006.4 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 561 | 992.9 | 990.1/1,017.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 562 | 1,011.4 | 990.9/1,036.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 563 | 1,023.8 | 1,007.4/1,036.4 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 564 | 1,018.2 | 1,005.0/1,041.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 565 | 1,023.4 | 982.9/1,031.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 566 | 1,023.8 | 983.8/1,039.3 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 567 | 1,019.1 | 980.3/1,032.6 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 568 | 1,025.0 | 978.8/1,033.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 569 | 1,014.8 | 982.2/1,054.8 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 570 | 1,019.4 | 984.4/1,040.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 571 | 999.3 | 985.5/1,028.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 572 | 999.8 | 946.7/1,029.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 573 | 954.2 | 942.2/1,023.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 574 | 936.1 | 924.3/1,025.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 575 | 941.0 | 924.3/1,032.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 576 | 931.3 | 907.9/1,028.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 577 | 954.3 | 937.0/1,028.6 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 578 | 932.0 | 922.3/1,029.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 579 | 911.6 | 911.4/1,037.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 580 | 914.8 | 912.2/1,035.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 581 | 978.3 | 915.0/1,031.3 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 582 | 997.6 | 918.2/1,030.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 583 | 267.8 | 235.5/270.9 | 661.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 584 | 617.7 | 610.9/618.8 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 585 | 53.3 | 47.8/58.9 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 586 | 1,086.3 | 996.2/2,221.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 587 | 1,048.6 | 953.2/1,070.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 588 | 1,033.3 | 973.2/1,079.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 589 | 1,030.2 | 1,004.7/1,095.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 590 | 1,025.5 | 1,002.1/1,050.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 591 | 1,006.6 | 1,003.5/1,028.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 592 | 1,007.6 | 997.1/1,028.8 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 593 | 1,015.3 | 1,013.7/1,035.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 594 | 1,019.4 | 1,001.9/1,033.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 595 | 1,006.5 | 965.0/1,026.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 596 | 995.5 | 940.5/1,022.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 597 | 982.7 | 959.9/1,017.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 598 | 956.7 | 946.4/1,026.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 599 | 955.5 | 919.4/1,022.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 600 | 951.0 | 918.8/1,022.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 601 | 995.4 | 924.0/1,027.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 602 | 1,002.2 | 925.4/1,022.8 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 603 | 1,000.4 | 947.6/1,032.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 604 | 999.2 | 941.8/1,034.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 605 | 1,014.3 | 969.1/1,047.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 606 | 1,024.2 | 999.2/1,025.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 607 | 1,021.4 | 1,003.4/1,025.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 608 | 1,024.3 | 953.5/1,042.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 609 | 1,031.8 | 1,003.5/1,040.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 610 | 1,027.4 | 1,003.7/1,030.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 611 | 1,021.4 | 1,004.4/1,025.5 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 612 | 1,029.8 | 1,003.3/1,030.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 613 | 1,001.2 | 996.5/1,022.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 614 | 998.8 | 998.3/1,029.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 615 | 998.3 | 990.1/1,039.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 616 | 1,005.9 | 948.0/1,033.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 617 | 1,002.0 | 958.1/1,026.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 618 | 1,002.5 | 1,001.3/1,012.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 619 | 1,002.5 | 994.9/1,043.7 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 620 | 1,005.6 | 999.8/1,030.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 621 | 996.7 | 993.6/1,034.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 622 | 264.1 | 250.4/302.8 | 661.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 623 | 617.5 | 613.2/618.7 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 624 | 59.5 | 49.9/59.9 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 625 | 1,071.3 | 1,060.4/1,105.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 626 | 1,037.3 | 1,028.5/1,057.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 627 | 1,044.1 | 1,020.5/1,044.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 628 | 1,040.0 | 1,008.0/1,043.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 629 | 1,029.0 | 1,014.4/1,035.0 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 630 | 1,032.5 | 999.3/1,037.6 | 235.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 631 | 1,030.4 | 1,002.0/1,047.1 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 632 | 1,031.6 | 1,009.0/1,034.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 633 | 1,034.7 | 1,027.9/1,045.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 634 | 1,032.7 | 1,029.6/1,038.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 635 | 1,034.0 | 1,033.9/1,036.2 | 238.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 636 | 1,027.0 | 1,003.7/1,035.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 637 | 1,028.0 | 1,001.4/1,032.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 638 | 1,024.5 | 1,000.1/1,028.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 639 | 1,025.2 | 998.8/1,028.6 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 640 | 1,026.0 | 1,015.8/1,041.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 641 | 1,022.4 | 998.0/1,027.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 642 | 1,033.3 | 1,001.4/1,038.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 643 | 1,026.4 | 1,001.5/1,081.1 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 644 | 1,032.2 | 1,005.3/1,048.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 645 | 1,027.6 | 1,001.8/1,027.8 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 646 | 1,049.1 | 1,029.6/1,049.9 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 647 | 1,026.0 | 1,025.3/1,031.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 648 | 1,029.7 | 1,024.4/1,043.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 649 | 1,027.5 | 1,021.3/1,029.8 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 650 | 1,031.9 | 1,024.9/1,036.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 651 | 1,038.4 | 1,026.8/1,043.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 652 | 1,027.8 | 1,000.6/1,040.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 653 | 1,029.4 | 990.9/1,035.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 654 | 1,028.6 | 998.1/1,030.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 655 | 1,032.0 | 993.5/1,034.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 656 | 1,025.8 | 1,021.7/1,045.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 657 | 1,025.5 | 995.9/1,031.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 658 | 999.5 | 989.4/1,021.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 659 | 993.0 | 992.0/1,033.5 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 660 | 1,001.1 | 982.5/1,027.7 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 661 | 258.9 | 249.4/271.4 | 662.3 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 662 | 613.6 | 610.4/617.2 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 663 | 54.2 | 53.7/58.6 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 664 | 1,070.3 | 1,003.7/1,072.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 665 | 1,028.1 | 960.2/1,044.9 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 666 | 1,027.2 | 959.8/1,029.3 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 667 | 1,023.3 | 948.1/1,047.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 668 | 1,011.3 | 940.2/1,030.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 669 | 965.4 | 949.5/1,003.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 670 | 967.0 | 952.5/1,010.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 671 | 952.2 | 949.4/1,018.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 672 | 1,003.0 | 979.3/1,004.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 673 | 1,009.1 | 1,005.6/1,020.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 674 | 1,005.8 | 1,004.1/1,021.6 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 675 | 1,023.4 | 1,003.0/1,033.6 | 235.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 676 | 1,008.7 | 1,001.7/1,033.7 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 677 | 1,032.7 | 1,005.9/1,032.9 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 678 | 1,028.4 | 1,024.9/1,036.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 679 | 1,036.1 | 1,023.5/1,081.8 | 238.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 680 | 1,020.5 | 1,015.7/1,027.5 | 238.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 681 | 1,025.7 | 1,002.3/1,030.3 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 682 | 1,030.4 | 1,005.8/1,040.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 683 | 1,014.0 | 996.7/1,039.1 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 684 | 1,006.4 | 1,001.3/1,030.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 685 | 1,008.1 | 953.1/1,033.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 686 | 997.9 | 970.5/1,035.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 687 | 1,000.9 | 998.8/1,055.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 688 | 1,023.9 | 996.2/1,029.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 689 | 1,016.5 | 1,006.0/1,023.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 690 | 1,026.6 | 1,000.9/1,030.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 691 | 1,015.6 | 1,000.6/1,031.3 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 692 | 1,005.2 | 998.3/1,022.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 693 | 997.3 | 996.7/1,029.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 694 | 994.4 | 993.5/1,006.0 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 695 | 997.1 | 992.1/997.8 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 696 | 996.1 | 995.0/1,013.2 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 697 | 999.9 | 943.1/1,017.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 698 | 995.8 | 987.1/996.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 699 | 994.1 | 990.7/1,001.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 700 | 261.6 | 238.6/266.1 | 661.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 701 | 618.9 | 618.3/626.3 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 702 | 55.9 | 50.7/57.5 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 703 | 1,043.4 | 976.8/1,066.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 704 | 974.3 | 955.0/1,019.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 705 | 956.2 | 946.8/1,014.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 706 | 941.7 | 935.0/1,003.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 707 | 950.4 | 922.5/1,006.8 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 708 | 972.9 | 921.5/1,009.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 709 | 947.0 | 910.6/998.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 710 | 995.4 | 909.2/1,568.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 711 | 962.1 | 903.2/996.3 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 712 | 960.4 | 920.1/992.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 713 | 950.3 | 921.4/1,004.7 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 714 | 937.6 | 911.9/956.7 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 715 | 958.6 | 946.5/977.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 716 | 995.8 | 952.5/998.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 717 | 992.1 | 933.9/997.1 | 235.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 718 | 988.8 | 928.3/997.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 719 | 993.5 | 948.2/993.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 720 | 986.3 | 974.7/995.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 721 | 994.6 | 975.5/1,001.1 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 722 | 997.3 | 994.2/1,005.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 723 | 999.1 | 994.9/1,025.1 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 724 | 1,005.6 | 992.5/1,039.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 725 | 996.1 | 991.9/1,019.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 726 | 999.8 | 998.2/1,026.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 727 | 996.1 | 992.6/1,051.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 728 | 997.9 | 992.6/1,054.8 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 729 | 993.2 | 990.1/1,034.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 730 | 993.5 | 988.8/1,069.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 731 | 994.3 | 990.2/1,042.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 732 | 994.5 | 993.8/1,037.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 733 | 993.2 | 988.6/1,019.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 734 | 996.5 | 986.6/998.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 735 | 1,008.0 | 990.1/1,017.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 736 | 1,019.1 | 992.7/1,024.2 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 737 | 1,027.0 | 1,025.4/1,032.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 738 | 1,017.8 | 988.4/1,041.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 739 | 266.8 | 256.4/685.0 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 740 | 619.1 | 611.7/619.6 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 741 | 52.9 | 51.3/80.2 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 742 | 1,090.5 | 1,063.1/1,146.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 743 | 1,047.0 | 1,022.6/1,109.2 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 744 | 1,030.1 | 1,015.8/1,093.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 745 | 1,033.3 | 999.6/1,058.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 746 | 1,006.8 | 1,003.6/1,056.0 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 747 | 1,004.1 | 998.6/1,052.0 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 748 | 1,010.2 | 995.7/1,063.5 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 749 | 1,024.5 | 1,002.6/1,039.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 750 | 1,019.3 | 1,001.9/1,031.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 751 | 1,019.2 | 1,000.9/1,029.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 752 | 1,019.8 | 1,003.3/1,033.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 753 | 1,024.7 | 1,023.0/1,030.2 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 754 | 1,034.6 | 1,017.0/1,035.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 755 | 1,021.0 | 1,002.9/1,033.3 | 247.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 756 | 1,008.1 | 996.3/1,011.0 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 757 | 1,005.1 | 996.1/1,023.2 | 235.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 758 | 1,017.9 | 1,000.7/1,035.8 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 759 | 1,018.9 | 982.8/1,030.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 760 | 1,020.4 | 986.5/1,035.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 761 | 1,023.7 | 1,009.1/1,144.4 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 762 | 1,020.9 | 982.8/1,064.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 763 | 1,027.9 | 949.1/1,042.0 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 764 | 1,014.9 | 950.8/1,039.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 765 | 1,021.3 | 937.5/1,040.1 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 766 | 1,025.3 | 944.4/1,030.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 767 | 1,019.8 | 940.3/1,032.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 768 | 1,019.7 | 945.7/1,028.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 769 | 1,020.9 | 942.0/1,036.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 770 | 1,013.1 | 937.3/1,033.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 771 | 1,015.3 | 971.5/1,055.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 772 | 1,018.2 | 945.1/1,036.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 773 | 1,017.5 | 1,006.3/1,031.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 774 | 1,008.9 | 1,000.7/1,043.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 775 | 1,016.7 | 999.4/1,033.7 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 776 | 1,016.4 | 996.3/1,092.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 777 | 1,030.4 | 993.0/1,052.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 778 | 262.0 | 259.6/271.5 | 662.6 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 779 | 615.1 | 614.5/617.8 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 780 | 57.1 | 50.1/59.2 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 781 | 1,073.1 | 1,064.6/1,079.3 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 782 | 1,045.8 | 1,021.6/1,052.0 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 783 | 1,037.6 | 1,008.1/1,055.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 784 | 1,030.0 | 1,006.0/1,065.6 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 785 | 1,030.5 | 1,010.7/1,040.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 786 | 1,023.1 | 971.5/1,030.4 | 235.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 787 | 1,025.5 | 948.1/1,030.0 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 788 | 962.6 | 945.6/1,022.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 789 | 998.8 | 947.3/1,037.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 790 | 1,021.5 | 954.8/1,026.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 791 | 1,011.1 | 994.5/1,024.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 792 | 1,007.9 | 987.7/1,020.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 793 | 1,006.8 | 946.9/1,025.0 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 794 | 1,009.2 | 940.9/1,015.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 795 | 1,000.7 | 936.9/1,018.7 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 796 | 960.0 | 940.6/1,019.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 797 | 1,012.9 | 937.0/1,022.8 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 798 | 1,016.6 | 991.6/1,027.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 799 | 1,012.8 | 964.2/1,031.1 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 800 | 1,018.3 | 933.1/1,032.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 801 | 981.4 | 942.8/1,042.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 802 | 993.5 | 939.7/1,040.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 803 | 992.4 | 945.5/1,026.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 804 | 1,002.6 | 944.9/1,047.4 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 805 | 1,018.4 | 987.7/1,030.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 806 | 1,011.4 | 929.1/1,015.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 807 | 967.9 | 914.7/989.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 808 | 998.0 | 907.8/1,002.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 809 | 1,002.0 | 903.4/1,009.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 810 | 971.5 | 919.9/1,008.1 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 811 | 986.8 | 935.2/995.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 812 | 984.2 | 936.8/1,013.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 813 | 988.0 | 940.0/999.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 814 | 984.1 | 941.0/1,014.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 815 | 1,001.1 | 938.4/1,010.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 816 | 1,004.3 | 953.7/1,016.3 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 817 | 262.9 | 238.4/282.2 | 661.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 818 | 615.5 | 610.5/618.1 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 819 | 53.2 | 49.0/57.1 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 820 | 1,085.1 | 1,014.1/1,086.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 821 | 1,042.2 | 969.9/1,049.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 822 | 1,038.3 | 948.5/1,044.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 823 | 1,026.3 | 928.8/1,048.0 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 824 | 1,021.0 | 920.3/1,059.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 825 | 1,028.9 | 953.6/1,030.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 826 | 1,024.8 | 950.7/1,032.1 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 827 | 1,022.3 | 935.4/1,036.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 828 | 1,023.1 | 922.5/1,033.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 829 | 1,021.4 | 917.0/1,038.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 830 | 1,022.7 | 923.9/1,025.6 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 831 | 1,008.1 | 921.6/1,014.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 832 | 991.3 | 937.9/1,044.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 833 | 987.5 | 946.1/1,042.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 834 | 1,023.7 | 960.3/1,038.2 | 238.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 835 | 994.1 | 952.5/1,000.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 836 | 986.6 | 950.9/1,033.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 837 | 987.2 | 941.8/1,077.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 838 | 986.3 | 949.3/1,038.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 839 | 986.2 | 946.3/1,049.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 840 | 997.7 | 984.5/1,043.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 841 | 1,028.9 | 980.6/1,038.0 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 842 | 1,020.3 | 988.1/1,034.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 843 | 1,018.7 | 987.7/1,027.2 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 844 | 1,029.0 | 990.5/1,038.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 845 | 1,035.0 | 985.7/1,037.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 846 | 1,036.5 | 1,013.3/1,060.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 847 | 1,027.3 | 1,020.2/1,046.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 848 | 1,031.8 | 1,027.7/1,033.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 849 | 1,024.7 | 1,014.4/1,032.3 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 850 | 1,027.2 | 1,019.3/1,032.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 851 | 1,030.9 | 1,014.7/1,045.8 | 238.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 852 | 1,019.5 | 1,017.9/1,031.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 853 | 1,026.0 | 1,017.2/1,028.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 854 | 1,036.5 | 1,007.7/1,036.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 855 | 1,024.7 | 1,012.9/1,039.9 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 856 | 274.6 | 246.8/275.2 | 662.0 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 857 | 614.2 | 611.6/614.9 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 858 | 57.3 | 46.4/57.5 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 859 | 1,073.9 | 1,065.1/1,084.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 860 | 1,029.0 | 1,019.6/1,033.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 861 | 1,019.8 | 1,009.2/1,038.0 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 862 | 1,004.1 | 996.5/1,008.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 863 | 1,013.6 | 997.9/1,027.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 864 | 1,007.9 | 998.8/1,032.1 | 235.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 865 | 1,002.8 | 995.9/1,032.7 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 866 | 1,006.5 | 992.1/1,032.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 867 | 1,000.9 | 995.4/1,028.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 868 | 1,006.1 | 995.1/1,042.6 | 269.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 869 | 1,018.4 | 985.8/1,035.0 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 870 | 999.6 | 982.0/1,034.1 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 871 | 996.8 | 982.2/1,035.6 | 235.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 872 | 1,021.6 | 991.9/1,031.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 873 | 1,018.0 | 994.7/1,030.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 874 | 1,000.3 | 997.3/1,017.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 875 | 993.2 | 981.9/1,016.1 | 235.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 876 | 1,012.9 | 981.9/1,023.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 877 | 997.9 | 947.0/1,022.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 878 | 1,003.6 | 943.0/1,013.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 879 | 995.3 | 990.9/1,025.2 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 880 | 1,004.5 | 991.1/1,025.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 881 | 1,002.6 | 998.9/1,023.5 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 882 | 1,001.3 | 996.7/1,023.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 883 | 1,005.4 | 1,000.5/1,008.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 884 | 1,032.4 | 988.9/1,043.8 | 238.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 885 | 1,024.1 | 943.9/1,035.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 886 | 1,029.6 | 975.0/1,033.2 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 887 | 1,023.4 | 989.8/1,036.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 888 | 1,027.0 | 984.9/1,030.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 889 | 1,006.4 | 1,003.5/1,010.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 890 | 996.4 | 975.0/1,138.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 891 | 996.2 | 993.2/1,087.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 892 | 997.5 | 993.3/1,047.1 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 893 | 998.3 | 991.7/1,024.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 894 | 988.7 | 945.6/1,285.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 895 | 247.1 | 245.7/285.7 | 661.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 896 | 616.7 | 611.2/624.6 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 897 | 54.9 | 46.4/61.3 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 898 | 1,057.3 | 1,003.8/1,077.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 899 | 1,013.8 | 969.4/1,024.1 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 900 | 1,009.8 | 962.1/1,024.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 901 | 998.0 | 950.1/1,014.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 902 | 1,011.2 | 938.5/1,018.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 903 | 1,003.5 | 935.1/1,047.6 | 235.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 904 | 999.7 | 931.9/1,056.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 905 | 1,002.2 | 945.3/1,039.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 906 | 1,027.3 | 936.9/1,043.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 907 | 1,008.3 | 964.0/1,014.0 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 908 | 1,000.3 | 988.1/1,040.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 909 | 1,006.0 | 986.1/1,009.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 910 | 1,001.3 | 986.7/1,001.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 911 | 994.6 | 981.8/1,001.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 912 | 1,000.8 | 990.2/1,018.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 913 | 1,003.5 | 991.3/1,023.2 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 914 | 1,004.2 | 989.8/1,025.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 915 | 1,014.5 | 994.8/1,020.1 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 916 | 1,014.3 | 1,008.4/1,025.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 917 | 1,023.9 | 1,001.9/1,039.8 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 918 | 1,027.8 | 1,014.7/1,039.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 919 | 1,024.4 | 1,021.1/1,027.3 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 920 | 1,023.8 | 1,021.3/1,026.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 921 | 1,022.2 | 1,016.7/1,027.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 922 | 1,023.3 | 1,021.7/1,030.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 923 | 1,025.2 | 1,017.7/1,026.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 924 | 1,020.9 | 1,018.4/1,023.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 925 | 1,026.1 | 998.7/1,032.2 | 235.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 926 | 1,013.9 | 1,000.5/1,024.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 927 | 1,005.3 | 970.2/1,029.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 928 | 986.5 | 943.6/1,041.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 929 | 1,021.5 | 946.4/1,023.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 930 | 1,018.2 | 942.6/1,025.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 931 | 1,021.9 | 997.5/1,026.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 932 | 995.9 | 995.3/1,023.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 933 | 1,017.4 | 1,002.1/1,026.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 934 | 259.8 | 248.1/278.6 | 664.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 935 | 625.4 | 608.1/660.8 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 936 | 57.7 | 45.4/58.8 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 937 | 1,097.5 | 1,063.4/1,106.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 938 | 1,053.8 | 1,009.2/1,062.3 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 939 | 1,034.4 | 999.2/1,046.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 940 | 1,031.1 | 991.1/1,036.0 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 941 | 1,010.2 | 994.5/1,031.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 942 | 1,010.8 | 993.0/1,041.9 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 943 | 1,005.1 | 985.1/1,037.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 944 | 1,025.8 | 939.3/1,028.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 945 | 1,031.0 | 958.1/1,044.5 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 946 | 1,025.6 | 999.7/1,033.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 947 | 1,027.9 | 1,006.7/1,029.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 948 | 1,026.4 | 1,017.3/1,034.8 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 949 | 1,027.0 | 1,022.8/1,028.0 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 950 | 1,026.6 | 997.8/1,037.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 951 | 1,022.5 | 992.7/1,039.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 952 | 1,028.3 | 942.3/1,042.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 953 | 1,024.1 | 944.3/1,036.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 954 | 1,029.8 | 941.2/1,029.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 955 | 1,030.3 | 941.5/1,043.9 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 956 | 1,027.8 | 950.1/1,033.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 957 | 1,038.1 | 953.2/1,138.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 958 | 1,031.7 | 996.0/1,271.7 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 959 | 1,029.5 | 994.0/1,063.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 960 | 1,011.9 | 990.1/1,031.3 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 961 | 1,012.7 | 987.8/1,026.4 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 962 | 1,004.5 | 993.4/1,022.5 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 963 | 1,026.9 | 942.1/1,029.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 964 | 1,025.1 | 938.7/1,033.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 965 | 1,031.8 | 936.2/1,035.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 966 | 1,027.5 | 939.2/1,032.2 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 967 | 1,004.2 | 987.6/1,032.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 968 | 1,030.1 | 989.9/1,036.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 969 | 1,030.8 | 992.7/1,032.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 970 | 1,025.5 | 986.3/1,030.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 971 | 1,031.4 | 992.1/1,033.4 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 972 | 1,038.1 | 996.8/1,055.0 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 973 | 289.8 | 265.9/296.1 | 662.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 974 | 612.8 | 612.6/618.6 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 975 | 60.9 | 60.9/61.0 | 1.7 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 976 | 1,104.7 | 1,080.8/1,113.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 977 | 1,050.8 | 1,015.4/1,155.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 978 | 1,033.0 | 1,003.2/1,075.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 979 | 1,043.3 | 997.0/1,060.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 980 | 1,029.5 | 1,004.6/1,054.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 981 | 1,028.6 | 1,000.0/1,062.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 982 | 1,042.3 | 998.5/1,047.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 983 | 1,037.8 | 1,001.9/1,043.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 984 | 1,039.4 | 1,001.0/1,041.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 985 | 1,034.8 | 961.4/1,046.0 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 986 | 1,029.9 | 951.4/1,049.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 987 | 1,033.7 | 943.5/1,036.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 988 | 1,028.5 | 950.8/1,038.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 989 | 1,025.1 | 942.4/1,031.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 990 | 1,030.0 | 962.5/1,034.8 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 991 | 1,031.9 | 934.5/1,036.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 992 | 1,031.6 | 907.9/1,056.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 993 | 1,026.3 | 938.1/1,041.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 994 | 1,032.4 | 985.9/1,039.4 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 995 | 1,026.6 | 984.1/1,041.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 996 | 1,028.6 | 987.0/1,039.7 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 997 | 1,025.8 | 989.6/1,036.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 998 | 1,024.8 | 992.0/1,027.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 999 | 1,029.9 | 1,016.8/1,030.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1000 | 1,030.9 | 1,019.6/1,045.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1001 | 1,029.6 | 1,019.9/1,030.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1002 | 1,026.3 | 1,021.2/1,029.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1003 | 1,029.1 | 1,017.5/1,029.5 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1004 | 1,020.7 | 992.5/1,028.6 | 238.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1005 | 1,028.4 | 990.1/1,035.4 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1006 | 1,026.2 | 992.7/1,067.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1007 | 1,021.1 | 990.1/1,035.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1008 | 1,025.5 | 989.4/1,028.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1009 | 1,018.0 | 988.0/1,054.1 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1010 | 1,032.9 | 983.9/1,033.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1011 | 1,021.9 | 988.3/1,030.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1012 | 267.2 | 250.1/271.0 | 662.5 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1013 | 615.9 | 615.2/618.4 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1014 | 55.9 | 51.5/56.8 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1015 | 1,053.3 | 1,046.4/1,110.0 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1016 | 1,036.3 | 1,035.3/1,068.2 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1017 | 1,048.4 | 1,047.9/1,091.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1018 | 1,039.6 | 1,037.7/1,050.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1019 | 1,040.9 | 1,038.6/1,041.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1020 | 1,030.6 | 1,029.0/1,034.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1021 | 1,032.1 | 1,031.7/1,047.7 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1022 | 1,033.6 | 1,028.7/1,039.1 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1023 | 1,037.1 | 1,025.3/1,071.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1024 | 1,030.1 | 1,028.8/1,042.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1025 | 1,034.1 | 1,029.1/1,038.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1026 | 1,027.1 | 1,020.7/1,032.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1027 | 1,027.1 | 1,024.0/1,037.4 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1028 | 1,029.3 | 1,022.0/1,031.5 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1029 | 1,009.5 | 1,002.2/1,034.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1030 | 997.5 | 995.8/1,026.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1031 | 998.0 | 994.4/1,021.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1032 | 1,004.1 | 994.0/1,027.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1033 | 1,019.7 | 1,001.7/1,063.2 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1034 | 1,029.3 | 1,002.1/1,039.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1035 | 1,032.2 | 992.4/1,037.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1036 | 1,030.3 | 952.1/1,035.5 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1037 | 1,026.7 | 936.0/1,033.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1038 | 1,029.0 | 943.2/1,029.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1039 | 1,028.2 | 996.7/1,033.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1040 | 1,026.6 | 994.9/1,030.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1041 | 1,023.6 | 992.7/1,034.1 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1042 | 1,031.4 | 991.4/1,039.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1043 | 1,028.1 | 996.8/1,035.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1044 | 1,029.5 | 992.3/1,032.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1045 | 1,016.9 | 1,000.7/1,038.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1046 | 1,003.4 | 995.2/1,031.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1047 | 1,008.7 | 988.9/1,027.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1048 | 1,002.8 | 1,000.7/1,036.2 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1049 | 1,030.1 | 994.4/1,032.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1050 | 1,028.3 | 1,002.0/1,037.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1051 | 274.7 | 266.7/279.2 | 661.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1052 | 609.9 | 602.5/610.6 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1053 | 59.2 | 58.0/66.3 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1054 | 1,071.1 | 1,036.9/1,099.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1055 | 1,034.9 | 1,026.0/1,057.8 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1056 | 1,030.8 | 1,016.0/1,036.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1057 | 1,030.4 | 1,001.9/1,035.0 | 235.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1058 | 1,023.7 | 1,004.5/1,031.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1059 | 1,007.5 | 998.6/1,028.0 | 235.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1060 | 1,017.4 | 1,017.2/1,018.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1061 | 1,026.4 | 1,003.1/1,027.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1062 | 1,024.8 | 1,000.3/1,032.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1063 | 1,021.9 | 948.3/1,028.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1064 | 1,005.1 | 942.1/1,031.8 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1065 | 999.7 | 940.4/1,020.2 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1066 | 1,000.8 | 931.5/1,033.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1067 | 995.3 | 937.8/1,025.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1068 | 996.9 | 964.8/1,023.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1069 | 999.5 | 996.4/1,028.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1070 | 1,019.5 | 993.7/1,027.7 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1071 | 1,029.1 | 994.4/1,062.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1072 | 1,022.9 | 989.1/1,037.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1073 | 1,039.6 | 998.6/1,066.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1074 | 1,040.1 | 993.8/1,075.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1075 | 1,034.1 | 1,022.7/1,045.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1076 | 1,024.8 | 1,024.8/1,034.0 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1077 | 1,024.5 | 1,019.0/1,042.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1078 | 1,030.0 | 1,026.6/1,033.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1079 | 1,028.3 | 1,027.7/1,028.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1080 | 1,021.8 | 1,021.2/1,027.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1081 | 1,023.7 | 1,019.9/1,028.4 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1082 | 1,023.2 | 1,016.5/1,023.3 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1083 | 1,028.1 | 1,025.3/1,030.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1084 | 1,032.8 | 1,023.8/1,037.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1085 | 1,030.6 | 1,030.1/1,033.7 | 235.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1086 | 1,023.0 | 1,020.5/1,029.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1087 | 1,029.2 | 1,022.0/1,030.5 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1088 | 1,025.0 | 1,021.8/1,027.9 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1089 | 1,026.2 | 975.4/1,027.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1090 | 268.5 | 263.1/276.1 | 663.0 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1091 | 616.3 | 609.3/616.5 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1092 | 58.4 | 55.5/67.6 | 1.7 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1093 | 1,065.7 | 1,054.6/1,095.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1094 | 1,042.9 | 1,039.9/1,063.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1095 | 1,029.6 | 1,016.2/1,040.1 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1096 | 1,032.3 | 1,028.3/1,037.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1097 | 1,029.0 | 1,027.5/1,043.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1098 | 1,031.2 | 1,030.1/1,040.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1099 | 1,042.9 | 1,019.6/1,048.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1100 | 1,033.9 | 951.1/1,043.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1101 | 1,042.3 | 968.0/1,047.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1102 | 1,034.2 | 1,005.5/1,038.9 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1103 | 1,035.9 | 1,006.3/1,039.0 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1104 | 1,032.1 | 1,001.7/1,034.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1105 | 1,035.2 | 1,011.2/1,066.4 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1106 | 1,024.8 | 1,008.4/1,033.6 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1107 | 1,032.2 | 1,027.2/1,036.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1108 | 1,028.4 | 1,023.0/1,049.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1109 | 1,034.8 | 1,027.5/1,045.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1110 | 1,030.9 | 1,023.4/1,037.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1111 | 1,027.0 | 1,015.2/1,035.2 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1112 | 1,027.6 | 1,020.3/1,033.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1113 | 1,030.9 | 1,028.7/1,034.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1114 | 1,030.9 | 1,026.3/1,039.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1115 | 1,029.8 | 1,007.8/1,029.8 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1116 | 1,028.1 | 995.0/1,030.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1117 | 1,027.3 | 1,013.1/1,038.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1118 | 1,029.5 | 998.8/1,031.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1119 | 1,028.3 | 1,001.5/1,030.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1120 | 1,026.9 | 997.9/1,032.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1121 | 1,027.7 | 992.8/1,029.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1122 | 1,026.2 | 1,002.2/1,027.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1123 | 1,024.2 | 1,000.6/1,030.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1124 | 1,021.5 | 1,002.0/1,041.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1125 | 1,027.0 | 942.7/1,028.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1126 | 1,027.3 | 942.6/1,028.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1127 | 1,022.8 | 972.6/1,029.1 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1128 | 1,022.1 | 947.0/1,028.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1129 | 259.9 | 258.0/263.6 | 663.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1130 | 613.3 | 611.9/614.2 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1131 | 57.4 | 56.4/59.3 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1132 | 1,065.9 | 1,065.7/1,095.4 | 240.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1133 | 1,046.0 | 1,022.8/1,055.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1134 | 1,035.6 | 1,009.8/1,047.2 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1135 | 1,040.0 | 1,011.1/1,063.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1136 | 1,033.7 | 1,005.4/1,034.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1137 | 1,031.2 | 996.8/1,035.0 | 235.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1138 | 1,023.3 | 972.6/1,048.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1139 | 1,004.6 | 981.2/1,031.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1140 | 1,004.4 | 996.0/1,032.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1141 | 993.2 | 941.3/1,033.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1142 | 1,004.9 | 941.3/1,033.1 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1143 | 997.5 | 977.0/1,028.8 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1144 | 996.3 | 994.1/1,030.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1145 | 1,002.2 | 992.6/1,023.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1146 | 999.0 | 994.1/1,028.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1147 | 1,025.1 | 1,001.2/1,029.3 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1148 | 1,029.3 | 989.3/1,034.1 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1149 | 1,014.6 | 996.9/1,029.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1150 | 1,025.1 | 955.5/1,034.0 | 235.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1151 | 1,024.8 | 941.4/1,030.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1152 | 1,032.0 | 940.1/1,034.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1153 | 1,030.0 | 936.2/1,030.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1154 | 1,029.6 | 912.6/1,033.7 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1155 | 1,028.5 | 951.2/1,029.7 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1156 | 1,027.1 | 924.1/1,028.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1157 | 1,014.1 | 921.8/1,029.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1158 | 993.9 | 929.8/1,025.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1159 | 999.3 | 949.7/1,047.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1160 | 1,019.1 | 1,005.0/1,026.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1161 | 1,009.7 | 1,001.9/1,030.0 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1162 | 990.5 | 989.5/1,033.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1163 | 1,014.9 | 1,011.4/1,022.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1164 | 1,000.8 | 997.7/1,034.8 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1165 | 1,001.6 | 991.5/1,032.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1166 | 995.2 | 953.8/1,030.3 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1167 | 1,032.2 | 940.5/1,045.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1168 | 265.4 | 251.6/268.6 | 661.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1169 | 612.0 | 610.4/613.5 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1170 | 55.6 | 53.2/59.1 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1171 | 1,095.2 | 1,045.4/1,159.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1172 | 1,050.4 | 1,030.9/1,077.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1173 | 1,066.2 | 1,022.9/1,084.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1174 | 1,041.1 | 1,010.9/1,050.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1175 | 1,034.6 | 1,013.2/1,046.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1176 | 1,019.5 | 1,006.5/1,038.6 | 235.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1177 | 1,019.6 | 1,005.8/1,028.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1178 | 1,027.7 | 1,002.4/1,036.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1179 | 1,032.8 | 1,001.6/1,039.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1180 | 1,036.1 | 1,004.2/1,089.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1181 | 1,032.3 | 1,001.8/1,039.6 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1182 | 1,027.4 | 1,022.9/1,041.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1183 | 1,032.4 | 1,031.9/1,041.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1184 | 1,035.5 | 1,020.5/1,042.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1185 | 1,032.7 | 950.5/1,041.3 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1186 | 1,029.0 | 978.1/1,029.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1187 | 1,015.2 | 1,002.6/1,024.6 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1188 | 1,003.9 | 994.0/1,026.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1189 | 1,020.4 | 991.5/1,030.3 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1190 | 1,020.7 | 1,001.4/1,047.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1191 | 1,025.6 | 996.0/1,028.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1192 | 1,034.6 | 998.6/1,036.6 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1193 | 1,029.6 | 1,001.4/1,038.2 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1194 | 1,030.9 | 1,013.4/1,031.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1195 | 1,001.6 | 997.1/1,023.2 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1196 | 1,013.3 | 999.4/1,035.3 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1197 | 1,022.9 | 1,003.3/1,031.5 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1198 | 1,025.9 | 998.2/1,028.3 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1199 | 1,025.7 | 1,025.7/1,028.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1200 | 1,027.0 | 1,023.9/1,036.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1201 | 1,025.9 | 1,022.5/1,027.2 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1202 | 1,023.4 | 1,016.4/1,040.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1203 | 1,030.4 | 989.0/1,040.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1204 | 1,027.3 | 995.0/1,029.5 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1205 | 1,040.1 | 1,004.3/1,040.6 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1206 | 1,028.5 | 994.2/1,031.0 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1207 | 260.2 | 252.7/281.3 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1208 | 612.7 | 612.2/616.9 | 7.2 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1209 | 55.8 | 55.6/68.0 | 1.7 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1210 | 1,064.8 | 1,063.7/1,091.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1211 | 1,042.6 | 1,022.9/1,053.8 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1212 | 1,037.1 | 1,011.0/1,047.5 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1213 | 1,031.2 | 1,027.6/1,045.0 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1214 | 1,029.8 | 1,024.3/1,036.0 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1215 | 1,031.0 | 1,023.3/1,039.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1216 | 1,021.8 | 1,004.4/1,024.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1217 | 1,000.4 | 999.6/1,036.9 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1218 | 1,013.3 | 1,008.5/1,020.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1219 | 1,031.4 | 1,000.8/1,031.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1220 | 1,027.7 | 1,010.9/1,030.9 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1221 | 1,028.7 | 1,000.1/1,029.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1222 | 1,030.2 | 1,004.9/1,034.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1223 | 1,024.6 | 1,006.4/1,037.2 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1224 | 1,031.1 | 1,005.6/1,045.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1225 | 1,028.1 | 1,001.8/2,633.1 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1226 | 1,034.8 | 1,026.9/1,060.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1227 | 1,028.1 | 1,021.8/1,034.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1228 | 1,021.0 | 1,013.8/1,033.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1229 | 1,026.1 | 1,023.9/1,028.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1230 | 1,035.3 | 1,024.0/1,061.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1231 | 1,026.6 | 1,024.1/1,034.5 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1232 | 1,030.2 | 1,020.9/1,042.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1233 | 1,031.8 | 1,025.8/1,032.7 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1234 | 1,034.8 | 1,025.7/1,036.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1235 | 1,028.5 | 1,026.0/1,033.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1236 | 1,027.5 | 1,025.6/1,033.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1237 | 1,033.0 | 1,028.6/1,036.1 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1238 | 1,032.9 | 1,026.1/1,040.2 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1239 | 1,028.1 | 1,017.2/1,040.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1240 | 1,028.0 | 952.8/1,028.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1241 | 1,031.4 | 943.5/1,032.1 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1242 | 1,023.2 | 940.1/1,023.3 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1243 | 1,006.8 | 947.7/1,036.8 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1244 | 992.5 | 950.9/1,025.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1245 | 1,018.0 | 954.2/1,036.1 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1246 | 260.6 | 258.4/271.1 | 661.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1247 | 611.6 | 603.1/613.9 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1248 | 55.9 | 54.5/56.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1249 | 1,037.4 | 1,013.9/1,088.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1250 | 1,030.3 | 970.8/1,061.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1251 | 1,013.4 | 983.6/1,038.5 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1252 | 1,016.2 | 1,014.4/1,036.5 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1253 | 1,037.0 | 1,008.8/1,040.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1254 | 1,033.3 | 1,012.7/1,038.1 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1255 | 1,031.8 | 1,001.1/1,036.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1256 | 1,028.3 | 1,009.1/1,033.2 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1257 | 1,031.6 | 968.8/1,035.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1258 | 1,025.2 | 955.3/1,027.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1259 | 1,010.4 | 986.3/1,031.8 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1260 | 1,022.1 | 998.5/1,025.2 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1261 | 1,010.2 | 998.2/1,023.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1262 | 1,025.8 | 957.1/1,039.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1263 | 1,030.7 | 972.6/1,033.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1264 | 1,028.5 | 943.1/1,035.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1265 | 1,000.4 | 942.3/1,028.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1266 | 988.3 | 941.6/1,030.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1267 | 993.3 | 956.4/1,093.9 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1268 | 992.4 | 944.6/1,040.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1269 | 975.2 | 945.7/1,036.0 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1270 | 948.1 | 940.3/1,034.6 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1271 | 940.8 | 934.7/1,030.8 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1272 | 985.4 | 933.1/1,033.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1273 | 993.2 | 988.5/1,023.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1274 | 1,025.5 | 991.9/1,032.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1275 | 1,021.5 | 965.9/1,033.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1276 | 1,026.2 | 957.5/1,033.3 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1277 | 1,026.5 | 947.0/1,028.7 | 250.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1278 | 1,024.5 | 920.2/1,036.0 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1279 | 1,025.7 | 915.7/1,031.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1280 | 1,031.1 | 919.0/1,032.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1281 | 1,027.5 | 911.0/1,030.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1282 | 1,029.9 | 934.8/1,033.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1283 | 1,018.4 | 914.9/1,033.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1284 | 1,026.1 | 918.9/1,027.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1285 | 272.7 | 240.0/273.5 | 662.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1286 | 622.3 | 613.3/737.4 | 7.4 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1287 | 57.3 | 50.4/57.9 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1288 | 1,101.3 | 1,006.3/1,108.2 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1289 | 1,053.3 | 971.5/1,053.8 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1290 | 1,038.8 | 1,036.5/1,038.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1291 | 1,035.4 | 1,004.1/1,041.9 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1292 | 1,041.2 | 1,013.2/1,041.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1293 | 1,031.8 | 1,005.5/1,044.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1294 | 1,028.3 | 1,002.3/1,029.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1295 | 1,033.3 | 1,004.5/1,042.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1296 | 1,035.9 | 994.7/1,058.6 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1297 | 1,027.0 | 1,000.8/1,032.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1298 | 1,025.5 | 998.7/1,035.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1299 | 1,025.7 | 994.1/1,027.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1300 | 1,027.0 | 1,001.6/1,033.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1301 | 1,024.3 | 990.2/1,028.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1302 | 1,034.5 | 946.8/1,035.2 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1303 | 1,033.3 | 1,027.5/1,038.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1304 | 1,010.7 | 1,005.4/1,026.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1305 | 1,000.3 | 988.4/1,024.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1306 | 1,014.6 | 1,001.3/1,025.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1307 | 1,018.6 | 997.3/1,032.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1308 | 1,002.3 | 995.3/1,024.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1309 | 1,005.5 | 999.5/1,023.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1310 | 1,005.3 | 998.7/1,019.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1311 | 999.7 | 992.9/1,024.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1312 | 1,001.5 | 998.5/1,029.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1313 | 1,010.0 | 1,000.0/1,052.5 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1314 | 1,033.7 | 998.9/1,034.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1315 | 1,023.8 | 994.8/1,033.1 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1316 | 1,016.9 | 992.9/1,022.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1317 | 997.1 | 953.7/1,020.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1318 | 1,003.7 | 938.5/1,029.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1319 | 990.6 | 929.5/1,024.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1320 | 1,001.0 | 944.9/1,019.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1321 | 994.3 | 941.0/1,022.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1322 | 992.9 | 972.9/1,018.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1323 | 975.7 | 957.0/1,017.8 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1324 | 258.7 | 252.4/269.3 | 663.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1325 | 617.0 | 612.8/619.9 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1326 | 56.2 | 54.8/56.4 | 1.7 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1327 | 1,084.5 | 1,014.5/1,091.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1328 | 1,009.7 | 994.4/1,052.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1329 | 998.6 | 982.8/1,076.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1330 | 1,020.2 | 1,004.5/1,034.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1331 | 1,035.6 | 999.8/1,044.2 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1332 | 1,028.6 | 1,000.9/1,037.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1333 | 1,031.7 | 1,001.1/1,040.2 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1334 | 1,025.1 | 997.6/1,032.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1335 | 1,015.8 | 954.9/1,024.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1336 | 998.1 | 946.3/1,019.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1337 | 997.8 | 950.4/1,017.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1338 | 992.8 | 944.8/1,052.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1339 | 1,007.6 | 940.7/1,025.5 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1340 | 970.2 | 943.9/1,029.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1341 | 945.9 | 930.3/1,027.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1342 | 940.2 | 931.3/1,023.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1343 | 941.9 | 932.1/1,026.2 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1344 | 943.8 | 941.3/1,030.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1345 | 979.7 | 943.8/1,021.1 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1346 | 1,016.8 | 942.0/1,025.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1347 | 1,018.1 | 942.2/1,026.8 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1348 | 993.9 | 943.8/1,024.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1349 | 993.4 | 940.4/1,031.0 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1350 | 978.6 | 921.2/1,023.5 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1351 | 944.4 | 916.5/995.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1352 | 942.7 | 920.0/999.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1353 | 969.5 | 930.9/1,020.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1354 | 933.4 | 932.5/941.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1355 | 937.6 | 918.0/943.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1356 | 940.8 | 897.0/942.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1357 | 968.1 | 894.8/982.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1358 | 999.8 | 915.9/1,007.0 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1359 | 992.6 | 917.3/1,000.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1360 | 994.9 | 917.7/995.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1361 | 993.7 | 917.5/1,001.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1362 | 993.4 | 926.4/1,002.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1363 | 247.6 | 244.0/260.9 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1364 | 620.4 | 617.0/624.7 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1365 | 53.2 | 50.5/65.4 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1366 | 1,036.7 | 1,024.5/1,063.8 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1367 | 1,003.7 | 963.2/1,058.0 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1368 | 994.9 | 954.9/997.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1369 | 979.5 | 947.3/1,007.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1370 | 997.1 | 919.8/1,004.4 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1371 | 991.9 | 906.7/1,004.0 | 235.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1372 | 999.6 | 895.2/1,018.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1373 | 999.8 | 895.4/1,024.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1374 | 999.2 | 891.8/1,021.0 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1375 | 1,020.6 | 884.6/1,028.5 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1376 | 983.9 | 896.0/1,026.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1377 | 1,003.7 | 906.6/1,030.6 | 249.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1378 | 998.4 | 909.4/1,141.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1379 | 994.5 | 899.6/1,031.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1380 | 999.7 | 898.1/1,039.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1381 | 994.6 | 925.4/1,029.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1382 | 999.0 | 940.4/1,025.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1383 | 1,009.5 | 925.0/1,024.6 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1384 | 996.1 | 912.9/1,021.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1385 | 996.6 | 912.0/1,022.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1386 | 1,001.0 | 916.2/1,037.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1387 | 1,001.0 | 932.0/1,023.9 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1388 | 1,007.1 | 929.6/1,017.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1389 | 1,022.8 | 916.8/1,031.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1390 | 1,028.3 | 998.8/1,039.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1391 | 997.6 | 990.0/1,126.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1392 | 997.2 | 994.9/1,049.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1393 | 996.5 | 991.8/1,032.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1394 | 999.3 | 991.3/1,105.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1395 | 996.1 | 991.5/1,043.0 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1396 | 994.6 | 981.7/1,036.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1397 | 1,023.7 | 937.2/1,038.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1398 | 1,014.8 | 960.7/1,033.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1399 | 1,040.2 | 937.4/1,051.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1400 | 1,016.6 | 940.7/1,050.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1401 | 980.0 | 935.3/1,031.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1402 | 254.9 | 240.4/270.8 | 662.6 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1403 | 615.1 | 613.9/618.6 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1404 | 54.7 | 51.3/61.3 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1405 | 1,062.7 | 999.2/1,122.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1406 | 1,020.8 | 964.5/1,069.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1407 | 1,006.5 | 1,002.4/1,050.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1408 | 1,007.6 | 954.9/1,053.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1409 | 1,002.2 | 924.0/1,038.5 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1410 | 997.4 | 920.2/1,051.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1411 | 977.9 | 914.8/1,040.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1412 | 993.4 | 937.2/1,043.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1413 | 1,000.1 | 910.3/1,037.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1414 | 1,024.9 | 926.8/1,032.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1415 | 1,030.4 | 990.8/1,465.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1416 | 1,009.8 | 992.8/1,028.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1417 | 997.8 | 991.2/1,026.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1418 | 992.6 | 990.2/1,024.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1419 | 1,002.7 | 968.7/1,025.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1420 | 984.6 | 950.5/1,040.8 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1421 | 991.8 | 945.1/1,022.8 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1422 | 954.7 | 941.6/1,022.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1423 | 940.9 | 938.8/1,026.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1424 | 948.3 | 928.3/1,025.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1425 | 942.9 | 917.6/1,022.6 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1426 | 945.0 | 922.8/1,030.6 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1427 | 944.5 | 921.6/1,052.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1428 | 938.0 | 924.8/1,033.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1429 | 947.8 | 937.7/1,026.9 | 238.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1430 | 940.2 | 917.7/1,033.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1431 | 941.7 | 920.2/1,030.5 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1432 | 938.1 | 928.7/1,034.6 | 235.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1433 | 945.0 | 936.3/1,030.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1434 | 963.4 | 946.5/1,020.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1435 | 946.3 | 934.5/1,023.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1436 | 945.2 | 932.9/1,025.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1437 | 969.1 | 951.4/1,022.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1438 | 1,000.3 | 943.8/1,026.9 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1439 | 998.8 | 942.0/1,019.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1440 | 1,027.8 | 948.7/1,037.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1441 | 270.4 | 260.3/281.7 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1442 | 610.1 | 608.0/614.4 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1443 | 59.3 | 56.8/60.0 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1444 | 1,065.7 | 1,020.2/1,069.3 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1445 | 961.0 | 948.6/1,038.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1446 | 951.5 | 934.9/1,033.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1447 | 950.6 | 925.2/1,056.2 | 238.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1448 | 997.5 | 926.8/1,033.0 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1449 | 998.5 | 927.9/1,025.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1450 | 997.6 | 944.3/1,032.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1451 | 997.7 | 956.6/1,032.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1452 | 995.9 | 950.3/1,033.4 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1453 | 998.7 | 941.3/1,027.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1454 | 1,000.6 | 948.4/1,023.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1455 | 995.7 | 941.0/1,039.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1456 | 1,005.1 | 932.6/1,025.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1457 | 1,004.3 | 965.4/1,031.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1458 | 1,031.1 | 996.3/1,033.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1459 | 1,027.6 | 1,004.9/1,036.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1460 | 1,029.9 | 1,022.1/1,032.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1461 | 1,028.6 | 1,009.5/1,030.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1462 | 1,028.0 | 987.8/1,034.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1463 | 1,024.0 | 1,014.3/1,025.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1464 | 1,033.6 | 1,019.3/1,040.6 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1465 | 1,007.6 | 994.2/1,029.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1466 | 1,030.1 | 989.4/1,048.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1467 | 1,020.8 | 992.6/1,028.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1468 | 1,023.6 | 999.2/1,035.5 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1469 | 1,024.8 | 1,010.7/1,041.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1470 | 1,032.1 | 1,020.1/1,034.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1471 | 1,025.8 | 1,025.3/1,029.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1472 | 1,025.3 | 1,016.8/1,029.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1473 | 1,026.2 | 991.7/1,029.8 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1474 | 1,012.5 | 995.1/1,023.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1475 | 998.9 | 989.5/1,007.3 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1476 | 998.1 | 992.5/1,017.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1477 | 1,017.3 | 987.2/1,024.9 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1478 | 1,005.8 | 995.4/1,024.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1479 | 1,017.2 | 994.9/1,017.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1480 | 263.5 | 250.8/280.6 | 662.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1481 | 614.4 | 604.2/620.4 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1482 | 55.4 | 53.1/59.9 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1483 | 1,058.0 | 1,057.0/1,061.9 | 238.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1484 | 1,031.4 | 1,000.1/1,033.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1485 | 1,007.0 | 947.6/1,041.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1486 | 1,024.8 | 934.3/1,031.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1487 | 1,022.8 | 917.2/1,044.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1488 | 1,027.2 | 916.5/1,029.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1489 | 1,028.6 | 924.0/1,034.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1490 | 1,021.0 | 919.2/1,027.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1491 | 1,022.7 | 933.4/1,036.9 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1492 | 1,029.5 | 960.1/1,038.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1493 | 1,027.2 | 1,003.4/1,032.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1494 | 1,023.7 | 991.8/1,039.3 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1495 | 1,021.9 | 949.2/1,025.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1496 | 1,023.3 | 954.5/1,039.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1497 | 1,023.6 | 1,003.9/1,032.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1498 | 1,002.2 | 1,000.2/1,030.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1499 | 1,038.9 | 995.2/2,265.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1500 | 1,030.3 | 944.8/1,069.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1501 | 1,030.9 | 930.3/1,131.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1502 | 1,033.5 | 930.0/1,052.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1503 | 1,012.8 | 920.6/1,035.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1504 | 1,026.0 | 927.9/1,032.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1505 | 1,017.5 | 967.8/1,041.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1506 | 1,025.1 | 996.0/1,026.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1507 | 1,031.6 | 1,004.8/1,050.9 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1508 | 1,006.3 | 989.9/1,028.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1509 | 1,004.5 | 1,000.0/1,028.7 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1510 | 1,014.0 | 999.2/1,030.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1511 | 1,010.5 | 1,007.6/1,027.0 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1512 | 1,021.4 | 1,003.1/1,034.2 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1513 | 1,002.1 | 976.7/1,027.3 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1514 | 997.8 | 949.4/1,036.4 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1515 | 979.0 | 951.3/1,036.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1516 | 951.2 | 939.9/1,027.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1517 | 1,004.1 | 986.0/1,033.2 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1518 | 972.4 | 961.2/1,035.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1519 | 258.5 | 251.7/273.1 | 661.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1520 | 615.7 | 613.2/617.8 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1521 | 56.3 | 55.2/56.7 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1522 | 1,061.6 | 1,011.4/1,063.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1523 | 993.2 | 964.0/1,033.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1524 | 963.6 | 952.7/1,036.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1525 | 951.6 | 950.7/1,040.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1526 | 956.1 | 943.6/1,060.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1527 | 1,016.9 | 937.6/1,038.1 | 235.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1528 | 1,011.2 | 947.5/1,026.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1529 | 1,013.4 | 930.8/1,024.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1530 | 1,000.9 | 943.6/1,027.2 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1531 | 1,019.5 | 942.4/1,032.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1532 | 1,000.1 | 946.9/1,030.9 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1533 | 1,008.5 | 964.1/1,022.2 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1534 | 1,018.4 | 999.6/1,026.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1535 | 1,026.8 | 1,005.8/1,033.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1536 | 1,026.4 | 1,023.7/1,029.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1537 | 1,027.4 | 1,020.5/1,028.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1538 | 1,026.9 | 1,026.2/1,029.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1539 | 1,030.3 | 1,024.0/1,031.2 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1540 | 1,029.9 | 1,013.0/1,031.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1541 | 1,021.4 | 1,001.3/1,025.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1542 | 1,028.3 | 1,005.4/1,029.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1543 | 1,025.6 | 1,002.7/1,035.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1544 | 1,021.0 | 1,008.6/1,025.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1545 | 1,002.7 | 999.2/1,028.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1546 | 999.1 | 990.6/1,035.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1547 | 991.6 | 958.8/1,034.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1548 | 997.8 | 945.9/1,030.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1549 | 991.5 | 948.6/1,033.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1550 | 997.9 | 989.7/1,036.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1551 | 992.3 | 990.5/1,026.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1552 | 1,001.0 | 998.1/1,031.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1553 | 985.6 | 984.8/1,021.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1554 | 988.4 | 935.4/1,033.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1555 | 989.4 | 938.7/993.6 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1556 | 960.0 | 933.7/992.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1557 | 983.8 | 935.3/1,007.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1558 | 252.1 | 239.7/261.8 | 662.1 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1559 | 622.3 | 610.3/624.5 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1560 | 54.6 | 50.0/55.2 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1561 | 1,030.2 | 940.6/1,057.7 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1562 | 1,013.8 | 938.7/1,041.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1563 | 1,017.4 | 964.7/1,046.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1564 | 1,021.7 | 931.3/1,030.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1565 | 1,009.1 | 969.0/1,039.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1566 | 1,004.3 | 927.7/1,038.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1567 | 1,001.5 | 950.5/1,037.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1568 | 1,006.4 | 932.3/1,027.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1569 | 1,018.8 | 951.7/1,027.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1570 | 1,030.5 | 948.8/1,037.6 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1571 | 1,032.4 | 935.4/1,034.2 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1572 | 1,025.1 | 939.4/1,028.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1573 | 1,030.2 | 937.1/1,034.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1574 | 1,024.0 | 933.7/1,034.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1575 | 1,032.0 | 928.5/1,034.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1576 | 1,028.3 | 973.0/1,039.1 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1577 | 1,026.9 | 994.1/1,068.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1578 | 1,020.9 | 991.4/1,034.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1579 | 1,018.1 | 988.2/1,033.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1580 | 1,026.5 | 986.7/1,027.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1581 | 1,022.8 | 990.3/1,030.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1582 | 1,027.9 | 1,022.9/1,040.6 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1583 | 1,028.6 | 996.6/1,032.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1584 | 1,027.2 | 990.5/1,041.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1585 | 1,054.3 | 998.2/1,068.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1586 | 1,037.4 | 937.6/1,042.9 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1587 | 1,029.1 | 942.3/1,034.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1588 | 1,031.7 | 919.7/1,034.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1589 | 1,013.4 | 904.3/1,034.5 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1590 | 1,003.6 | 914.2/1,031.9 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1591 | 968.5 | 897.7/1,028.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1592 | 944.4 | 889.3/1,031.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1593 | 988.9 | 887.7/1,022.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1594 | 987.4 | 885.2/1,036.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1595 | 999.7 | 902.1/1,028.2 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1596 | 999.8 | 914.1/1,038.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1597 | 255.7 | 223.8/280.7 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1598 | 614.4 | 602.1/622.4 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1599 | 53.5 | 42.9/66.7 | 1.7 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1600 | 1,003.0 | 955.3/1,097.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1601 | 962.0 | 927.7/1,064.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1602 | 1,043.6 | 950.1/1,520.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1603 | 1,030.7 | 958.7/1,040.2 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1604 | 1,010.4 | 990.2/1,032.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1605 | 999.6 | 987.0/1,007.3 | 238.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1606 | 1,011.8 | 962.1/1,016.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1607 | 1,024.8 | 978.1/1,077.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1608 | 1,060.1 | 1,037.2/1,387.5 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1609 | 1,031.7 | 1,029.9/1,046.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1610 | 998.7 | 964.4/1,030.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1611 | 994.5 | 954.7/1,020.5 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1612 | 997.9 | 980.6/1,022.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1613 | 1,011.3 | 988.2/1,029.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1614 | 1,018.8 | 995.3/1,039.5 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1615 | 1,012.9 | 968.3/1,025.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1616 | 1,025.3 | 959.1/1,025.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1617 | 1,016.7 | 961.5/1,026.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1618 | 991.9 | 983.3/1,007.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1619 | 1,000.4 | 981.9/1,035.6 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1620 | 1,015.7 | 997.5/1,018.4 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1621 | 993.3 | 979.4/1,006.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1622 | 996.5 | 992.6/1,012.2 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1623 | 992.0 | 982.8/1,011.6 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1624 | 990.9 | 957.0/1,012.9 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1625 | 946.9 | 933.2/1,011.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1626 | 944.9 | 942.4/1,011.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1627 | 945.1 | 932.0/1,003.4 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1628 | 947.0 | 933.1/993.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1629 | 964.2 | 931.9/965.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1630 | 958.2 | 909.9/984.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1631 | 986.9 | 943.4/2,212.3 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1632 | 988.0 | 951.7/998.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1633 | 1,005.4 | 992.7/1,011.6 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1634 | 988.5 | 945.4/1,005.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1635 | 986.4 | 964.0/1,025.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1636 | 251.7 | 234.7/275.7 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1637 | 621.4 | 613.7/622.0 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1638 | 60.3 | 43.4/65.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1639 | 1,051.5 | 1,048.8/1,099.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1640 | 1,018.4 | 1,012.9/1,054.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1641 | 1,002.2 | 998.0/1,012.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1642 | 1,012.1 | 1,005.3/1,016.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1643 | 1,004.6 | 989.7/1,013.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1644 | 951.1 | 947.5/991.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1645 | 998.2 | 994.6/1,000.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1646 | 993.8 | 968.3/1,028.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1647 | 1,005.7 | 920.7/1,029.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1648 | 1,015.1 | 922.2/1,028.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1649 | 1,022.1 | 919.7/1,028.7 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1650 | 1,014.9 | 901.1/1,028.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1651 | 1,001.2 | 931.8/1,029.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1652 | 986.4 | 986.2/1,027.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1653 | 995.9 | 978.5/1,037.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1654 | 1,001.9 | 988.3/1,029.5 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1655 | 993.7 | 980.3/1,012.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1656 | 992.7 | 980.7/998.0 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1657 | 993.0 | 983.6/1,001.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1658 | 1,000.9 | 973.5/1,006.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1659 | 995.1 | 938.4/1,003.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1660 | 992.5 | 930.6/1,040.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1661 | 981.0 | 922.3/1,033.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1662 | 943.8 | 930.1/1,014.1 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1663 | 930.8 | 914.1/1,018.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1664 | 933.6 | 919.1/1,016.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1665 | 979.5 | 924.8/1,050.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1666 | 924.6 | 918.5/1,029.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1667 | 960.5 | 931.4/1,032.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1668 | 1,029.4 | 942.6/1,030.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1669 | 1,007.3 | 936.6/1,020.4 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1670 | 953.9 | 953.0/991.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1671 | 997.1 | 937.5/997.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1672 | 993.2 | 973.5/994.1 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1673 | 995.9 | 937.4/1,005.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1674 | 993.9 | 920.6/997.5 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1675 | 251.1 | 225.0/267.8 | 662.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1676 | 624.1 | 614.0/624.3 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1677 | 53.1 | 41.0/56.6 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1678 | 1,063.1 | 985.1/1,083.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1679 | 1,037.0 | 984.8/1,043.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1680 | 1,011.3 | 941.4/1,013.4 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1681 | 1,003.8 | 940.6/1,033.9 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1682 | 1,005.7 | 936.7/1,035.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1683 | 1,003.1 | 955.5/1,039.6 | 235.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1684 | 1,005.5 | 988.8/1,013.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1685 | 999.4 | 993.6/1,001.3 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1686 | 995.2 | 989.8/1,010.9 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1687 | 1,007.9 | 980.7/1,010.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1688 | 1,013.2 | 986.3/1,018.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1689 | 1,004.4 | 984.4/1,005.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1690 | 983.9 | 978.2/1,002.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1691 | 995.9 | 949.4/997.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1692 | 993.6 | 975.4/1,012.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1693 | 998.9 | 975.1/1,004.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1694 | 993.2 | 938.5/1,053.3 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1695 | 1,021.1 | 934.0/1,035.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1696 | 1,012.9 | 940.4/1,040.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1697 | 940.1 | 939.1/1,029.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1698 | 948.0 | 920.6/1,052.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1699 | 985.0 | 914.6/1,032.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1700 | 1,020.4 | 900.1/1,036.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1701 | 1,003.4 | 901.2/1,032.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1702 | 1,005.0 | 910.6/1,024.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1703 | 1,029.2 | 906.2/1,032.8 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1704 | 945.4 | 920.4/1,025.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1705 | 956.4 | 908.4/1,032.6 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1706 | 999.8 | 910.4/1,028.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1707 | 1,004.5 | 922.1/1,031.1 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1708 | 998.7 | 905.7/1,030.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1709 | 1,016.5 | 935.0/1,067.5 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1710 | 1,016.1 | 937.0/1,025.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1711 | 1,001.6 | 932.8/1,043.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1712 | 985.3 | 934.4/1,033.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1713 | 944.4 | 934.6/1,035.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1714 | 256.2 | 225.6/273.0 | 661.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1715 | 612.1 | 606.1/631.5 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1716 | 53.8 | 43.7/58.1 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1717 | 1,004.2 | 994.1/1,074.3 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1718 | 967.2 | 960.4/1,035.1 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1719 | 1,005.3 | 918.9/1,026.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1720 | 962.5 | 916.9/1,017.5 | 259.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1721 | 951.9 | 923.0/1,004.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1722 | 949.8 | 920.3/1,017.6 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1723 | 953.9 | 952.6/1,011.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1724 | 990.1 | 953.7/1,008.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1725 | 983.8 | 947.4/999.8 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1726 | 992.7 | 986.6/1,004.1 | 235.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1727 | 1,017.8 | 983.8/1,022.7 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1728 | 1,018.4 | 972.5/1,024.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1729 | 1,014.2 | 966.6/1,032.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1730 | 1,020.3 | 998.2/1,033.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1731 | 1,027.0 | 1,008.9/1,029.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1732 | 1,023.4 | 1,022.7/1,028.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1733 | 1,034.0 | 1,020.4/1,045.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1734 | 1,028.7 | 1,022.6/1,029.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1735 | 1,024.5 | 998.3/1,043.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1736 | 1,020.5 | 996.4/1,026.5 | 279.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1737 | 1,016.3 | 1,015.8/1,035.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1738 | 998.9 | 998.3/1,016.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1739 | 1,008.0 | 1,000.8/1,016.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1740 | 996.2 | 946.9/1,010.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1741 | 992.2 | 947.9/996.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1742 | 981.5 | 947.6/992.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1743 | 980.6 | 941.8/988.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1744 | 988.0 | 935.0/988.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1745 | 981.1 | 926.4/985.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1746 | 940.9 | 913.1/1,008.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1747 | 945.2 | 901.9/1,018.0 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1748 | 942.3 | 896.7/1,013.2 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1749 | 939.1 | 897.6/1,014.2 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1750 | 944.4 | 901.6/1,014.0 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1751 | 976.9 | 909.3/1,015.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1752 | 999.0 | 914.5/1,018.9 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1753 | 248.7 | 245.1/266.0 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1754 | 618.9 | 617.7/627.0 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1755 | 53.1 | 43.8/55.5 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1756 | 1,074.1 | 1,036.4/1,083.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1757 | 1,027.0 | 1,024.9/1,039.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1758 | 1,031.8 | 1,004.8/1,040.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1759 | 1,027.8 | 949.5/1,028.8 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1760 | 1,023.5 | 945.5/1,045.1 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1761 | 1,023.5 | 948.1/1,049.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1762 | 1,025.5 | 949.6/1,035.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1763 | 1,029.2 | 999.1/1,036.8 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1764 | 1,010.5 | 977.3/1,036.8 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1765 | 1,021.9 | 944.5/1,031.3 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1766 | 1,022.3 | 944.4/1,035.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1767 | 1,010.9 | 954.2/1,025.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1768 | 1,010.7 | 996.5/1,029.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1769 | 1,002.1 | 993.5/1,004.2 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1770 | 994.3 | 957.4/1,030.0 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1771 | 1,008.6 | 930.9/1,008.8 | 235.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1772 | 1,000.0 | 919.0/1,010.1 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1773 | 1,002.2 | 948.6/1,005.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1774 | 997.1 | 908.9/1,003.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1775 | 999.4 | 928.7/1,000.4 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1776 | 997.7 | 968.2/997.9 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1777 | 1,001.7 | 931.1/1,001.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1778 | 994.7 | 932.8/996.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1779 | 993.2 | 927.5/1,008.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1780 | 974.6 | 926.7/998.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1781 | 968.8 | 937.5/997.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1782 | 993.6 | 943.8/997.0 | 238.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1783 | 1,000.5 | 996.2/1,019.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1784 | 1,002.2 | 999.1/1,005.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1785 | 1,007.0 | 990.9/1,028.7 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1786 | 1,024.7 | 1,023.3/2,954.0 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1787 | 1,036.5 | 1,027.7/1,038.7 | 238.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1788 | 1,026.2 | 996.4/1,038.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1789 | 1,071.4 | 1,027.2/1,098.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1790 | 1,014.7 | 1,009.6/1,038.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1791 | 1,004.7 | 1,002.4/1,040.1 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1792 | 261.1 | 258.6/275.0 | 661.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1793 | 616.0 | 611.8/623.5 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1794 | 57.4 | 57.4/59.6 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1795 | 1,069.3 | 1,022.9/1,070.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1796 | 1,013.7 | 998.7/1,044.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1797 | 1,006.3 | 999.8/1,042.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1798 | 1,005.6 | 980.6/1,032.1 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1799 | 1,001.4 | 944.8/1,034.3 | 243.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1800 | 1,006.9 | 940.7/1,029.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1801 | 994.9 | 961.4/1,018.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1802 | 969.6 | 964.6/998.6 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1803 | 996.6 | 988.0/997.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1804 | 991.1 | 989.0/996.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1805 | 993.4 | 988.3/1,034.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1806 | 986.9 | 955.3/1,005.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1807 | 969.6 | 954.0/997.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1808 | 996.1 | 990.9/997.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1809 | 993.8 | 916.0/999.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1810 | 997.1 | 913.0/1,006.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1811 | 994.1 | 922.8/1,003.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1812 | 1,001.5 | 957.3/1,022.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1813 | 1,019.7 | 921.9/1,026.0 | 235.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1814 | 1,015.4 | 915.9/1,022.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1815 | 1,019.4 | 941.6/1,022.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1816 | 1,002.8 | 929.3/1,019.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1817 | 998.4 | 946.0/1,023.6 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1818 | 998.2 | 941.8/1,020.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1819 | 1,020.9 | 940.8/1,023.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1820 | 1,009.8 | 944.6/1,023.1 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1821 | 993.9 | 925.5/1,025.2 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1822 | 993.4 | 924.1/1,028.8 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1823 | 991.7 | 945.4/1,023.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1824 | 974.3 | 972.6/1,028.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1825 | 991.9 | 937.0/1,023.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1826 | 1,020.0 | 939.6/1,027.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1827 | 998.1 | 944.8/1,021.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1828 | 992.1 | 936.3/1,017.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1829 | 991.4 | 916.0/1,023.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1830 | 994.9 | 918.0/1,018.5 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1831 | 251.7 | 250.5/264.7 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1832 | 622.6 | 615.5/624.2 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1833 | 54.0 | 53.7/57.0 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1834 | 1,068.6 | 1,065.9/1,095.1 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1835 | 1,028.8 | 1,020.3/1,044.9 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1836 | 1,021.9 | 1,016.3/1,094.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1837 | 998.2 | 961.7/1,049.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1838 | 955.6 | 927.4/1,030.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1839 | 945.3 | 923.5/1,046.2 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1840 | 977.1 | 948.6/1,040.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1841 | 962.4 | 934.9/1,041.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1842 | 958.4 | 905.2/1,034.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1843 | 947.2 | 903.5/1,025.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1844 | 940.1 | 907.4/1,031.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1845 | 986.0 | 887.1/1,031.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1846 | 994.5 | 895.0/1,031.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1847 | 989.4 | 895.6/1,033.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1848 | 992.8 | 899.2/1,027.5 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1849 | 997.6 | 902.5/1,034.5 | 238.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1850 | 1,028.8 | 964.7/1,033.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1851 | 1,013.3 | 928.8/1,026.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1852 | 1,027.7 | 921.3/1,042.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1853 | 995.9 | 947.9/1,030.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1854 | 1,003.7 | 946.1/1,028.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1855 | 999.2 | 942.2/1,043.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1856 | 998.4 | 941.2/1,024.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1857 | 1,012.3 | 980.5/1,022.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1858 | 1,023.2 | 990.3/1,027.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1859 | 997.0 | 994.5/1,025.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1860 | 1,011.6 | 998.2/1,023.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1861 | 1,004.5 | 993.4/1,036.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1862 | 1,005.6 | 998.4/1,030.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1863 | 1,007.2 | 1,004.9/1,012.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1864 | 996.9 | 992.7/1,002.0 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1865 | 1,011.2 | 980.1/1,023.0 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1866 | 1,004.2 | 940.0/1,023.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1867 | 998.1 | 971.8/1,000.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1868 | 1,005.2 | 993.9/1,006.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1869 | 992.5 | 987.7/1,002.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1870 | 261.0 | 256.4/270.2 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1871 | 617.9 | 616.8/618.6 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1872 | 54.8 | 54.4/57.8 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1873 | 1,066.0 | 1,011.8/1,078.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1874 | 1,032.6 | 1,020.7/1,034.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1875 | 1,037.4 | 967.9/1,052.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1876 | 1,035.4 | 951.0/1,036.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1877 | 1,024.6 | 948.6/1,029.8 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1878 | 1,004.4 | 953.1/1,030.0 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1879 | 1,001.9 | 945.8/1,030.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1880 | 1,014.9 | 938.6/1,049.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1881 | 1,017.2 | 935.8/1,025.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1882 | 1,003.4 | 946.1/1,027.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1883 | 997.1 | 964.9/1,017.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1884 | 972.0 | 968.9/1,018.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1885 | 1,016.9 | 927.5/1,017.5 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1886 | 1,002.5 | 941.7/1,027.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1887 | 1,023.6 | 937.7/1,031.2 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1888 | 1,032.5 | 939.5/1,033.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1889 | 1,024.7 | 933.7/1,028.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1890 | 1,028.5 | 989.2/1,036.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1891 | 1,023.8 | 991.1/1,047.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1892 | 1,029.4 | 995.8/1,030.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1893 | 1,024.0 | 1,010.0/1,029.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1894 | 1,009.1 | 1,002.2/1,029.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1895 | 999.9 | 991.3/1,008.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1896 | 1,003.5 | 999.9/1,009.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1897 | 1,003.9 | 997.0/1,004.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1898 | 995.9 | 982.4/996.0 | 235.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1899 | 1,002.6 | 935.1/1,030.7 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1900 | 998.1 | 927.6/1,058.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1901 | 1,007.0 | 928.6/1,027.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1902 | 994.7 | 942.9/1,033.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1903 | 994.3 | 924.3/1,029.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1904 | 997.2 | 926.3/1,043.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1905 | 990.2 | 928.3/1,034.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1906 | 994.2 | 931.2/1,030.8 | 249.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1907 | 1,025.4 | 935.3/1,028.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1908 | 1,016.3 | 1,014.5/1,038.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1909 | 271.6 | 262.8/276.3 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1910 | 616.4 | 612.1/618.0 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1911 | 57.4 | 57.3/59.8 | 1.7 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1912 | 1,086.2 | 1,049.4/1,100.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1913 | 1,054.5 | 1,011.7/1,058.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1914 | 1,042.1 | 999.2/1,097.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1915 | 1,043.1 | 995.9/1,046.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1916 | 1,030.7 | 1,002.4/1,033.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1917 | 1,025.8 | 1,004.8/1,035.9 | 235.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1918 | 1,027.6 | 997.6/1,031.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1919 | 1,026.7 | 1,003.6/1,026.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1920 | 1,030.4 | 1,007.7/1,044.2 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1921 | 1,029.4 | 1,007.1/1,035.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1922 | 1,024.7 | 1,002.6/1,032.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1923 | 1,029.0 | 998.4/1,037.6 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1924 | 1,032.4 | 996.2/1,038.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1925 | 1,028.7 | 996.5/1,035.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1926 | 1,023.7 | 997.4/1,034.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1927 | 1,022.0 | 1,000.4/1,032.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1928 | 1,022.9 | 1,001.7/1,030.1 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1929 | 1,025.1 | 990.6/1,042.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1930 | 1,020.3 | 994.2/1,026.6 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1931 | 1,021.8 | 994.8/1,029.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1932 | 1,019.6 | 1,001.7/1,024.2 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1933 | 1,024.1 | 1,001.0/1,034.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1934 | 1,030.0 | 993.8/1,030.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1935 | 1,024.5 | 1,010.1/1,028.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1936 | 1,027.4 | 993.8/1,031.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1937 | 1,026.7 | 1,014.0/1,026.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1938 | 1,015.7 | 1,006.8/1,024.0 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1939 | 1,001.3 | 993.8/1,030.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1940 | 1,027.6 | 991.9/1,029.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1941 | 1,023.0 | 985.6/1,094.3 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1942 | 1,025.4 | 998.0/1,031.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1943 | 1,018.6 | 1,018.0/1,052.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1944 | 1,028.3 | 1,016.8/1,047.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1945 | 1,024.4 | 1,022.7/1,038.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1946 | 1,024.1 | 1,015.5/1,033.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1947 | 1,021.2 | 1,019.7/1,071.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1948 | 263.9 | 255.8/271.0 | 663.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1949 | 620.8 | 604.1/622.8 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1950 | 56.9 | 56.2/56.9 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1951 | 1,088.5 | 1,084.5/1,109.7 | 238.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1952 | 1,052.9 | 1,023.2/1,063.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1953 | 1,030.1 | 975.2/1,059.0 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1954 | 1,038.8 | 980.6/1,039.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1955 | 1,025.6 | 1,015.5/1,045.9 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1956 | 1,033.3 | 1,020.4/1,047.1 | 238.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1957 | 1,020.2 | 1,020.2/1,033.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1958 | 1,023.1 | 1,008.8/1,025.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1959 | 1,030.6 | 1,014.3/1,031.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1960 | 1,020.8 | 1,006.6/1,024.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 1961 | 1,026.7 | 1,005.0/1,027.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 1962 | 1,024.7 | 998.5/1,030.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 1963 | 1,021.6 | 1,003.1/1,028.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 1964 | 1,029.4 | 1,022.9/1,037.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 1965 | 1,026.7 | 1,022.6/1,033.3 | 235.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 1966 | 1,027.8 | 1,024.3/1,029.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 1967 | 1,023.5 | 1,022.6/1,024.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 1968 | 1,025.8 | 1,001.5/1,028.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 1969 | 1,024.5 | 999.9/1,036.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 1970 | 1,026.6 | 1,004.2/1,034.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 1971 | 1,024.2 | 999.6/1,029.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 1972 | 1,027.9 | 990.4/1,065.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 1973 | 1,025.9 | 988.9/1,038.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 1974 | 1,019.2 | 948.5/1,029.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 1975 | 1,024.3 | 946.8/1,031.3 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 1976 | 1,024.6 | 1,004.6/1,030.0 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 1977 | 1,028.9 | 1,006.0/1,035.4 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 1978 | 1,025.1 | 1,004.2/1,033.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 1979 | 1,024.5 | 998.6/1,026.8 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 1980 | 1,028.7 | 995.9/1,032.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 1981 | 1,021.0 | 1,020.0/1,029.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 1982 | 1,029.8 | 944.5/1,036.2 | 239.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 1983 | 1,023.2 | 938.8/1,039.5 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 1984 | 1,002.1 | 943.2/1,024.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 1985 | 1,002.7 | 935.9/1,033.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 1986 | 1,006.6 | 1,003.2/1,020.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 1987 | 258.3 | 255.0/270.7 | 663.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1988 | 617.8 | 610.8/621.4 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1989 | 56.3 | 50.8/57.0 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1990 | 1,049.3 | 972.8/1,099.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 1991 | 1,033.1 | 944.3/1,052.3 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 1992 | 1,037.1 | 932.8/1,038.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 1993 | 1,033.5 | 929.7/1,036.6 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 1994 | 1,028.3 | 928.7/1,041.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 1995 | 1,022.7 | 995.8/1,025.8 | 236.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 1996 | 1,030.0 | 1,016.5/1,035.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 1997 | 1,023.3 | 1,023.3/1,028.9 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 1998 | 1,023.4 | 1,003.2/1,027.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 1999 | 1,021.6 | 948.2/1,027.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2000 | 1,019.9 | 945.3/1,038.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2001 | 1,024.4 | 942.4/1,029.7 | 238.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2002 | 1,028.1 | 943.8/1,028.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2003 | 1,019.6 | 924.9/1,036.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2004 | 1,023.0 | 941.0/1,025.8 | 235.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2005 | 1,024.1 | 971.1/1,024.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2006 | 1,020.7 | 999.0/1,021.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2007 | 1,022.8 | 994.3/1,054.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2008 | 1,023.4 | 994.9/1,029.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2009 | 1,024.6 | 1,018.5/1,025.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2010 | 1,024.8 | 1,022.3/1,029.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2011 | 1,012.9 | 1,009.5/1,029.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2012 | 998.4 | 995.8/1,029.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2013 | 1,029.6 | 1,028.4/1,061.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2014 | 1,029.9 | 1,018.6/1,034.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2015 | 1,022.4 | 1,019.0/1,025.2 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2016 | 1,027.5 | 1,016.9/1,030.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2017 | 1,052.7 | 1,022.4/1,064.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2018 | 1,023.6 | 1,021.5/1,039.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2019 | 1,018.6 | 999.5/1,036.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2020 | 1,020.7 | 1,001.3/1,031.9 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2021 | 1,018.7 | 1,000.0/1,039.6 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2022 | 1,021.3 | 943.4/1,067.9 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2023 | 1,009.9 | 962.0/1,041.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2024 | 1,020.3 | 989.8/1,046.2 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2025 | 1,022.2 | 993.4/1,030.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2026 | 264.7 | 251.2/277.7 | 664.3 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2027 | 612.6 | 611.0/716.3 | 7.2 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 2028 | 52.2 | 48.0/59.3 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 2029 | 1,053.0 | 1,036.1/1,100.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 2030 | 1,027.1 | 1,003.1/1,054.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 2031 | 1,025.2 | 982.0/1,026.3 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 2032 | 1,007.5 | 973.3/1,029.8 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 2033 | 966.3 | 959.9/1,026.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 2034 | 969.7 | 959.6/1,025.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 2035 | 1,006.7 | 952.4/1,049.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 2036 | 956.3 | 950.8/1,028.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 2037 | 984.9 | 945.1/1,025.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 2038 | 1,006.1 | 944.2/1,018.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2039 | 962.6 | 950.9/1,028.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2040 | 1,017.5 | 951.3/1,025.0 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2041 | 1,024.6 | 966.8/1,039.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2042 | 1,026.9 | 999.4/1,032.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2043 | 1,028.3 | 953.8/1,034.1 | 235.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2044 | 1,020.2 | 949.8/1,028.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2045 | 1,021.5 | 943.1/1,024.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2046 | 1,018.1 | 921.8/1,021.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2047 | 1,024.2 | 930.1/1,027.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2048 | 1,019.8 | 915.0/1,024.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2049 | 1,023.3 | 913.3/1,031.1 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2050 | 1,025.1 | 925.7/1,027.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2051 | 1,014.1 | 920.1/1,027.2 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2052 | 1,001.0 | 926.7/1,024.4 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2053 | 997.6 | 917.4/1,024.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2054 | 1,002.9 | 922.3/1,016.0 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2055 | 997.7 | 921.3/1,019.0 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2056 | 1,011.4 | 935.8/1,015.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2057 | 1,017.5 | 972.9/1,026.8 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2058 | 1,010.6 | 998.7/1,027.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2059 | 1,020.4 | 995.2/1,024.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2060 | 1,019.5 | 943.5/1,020.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2061 | 1,021.2 | 947.5/1,024.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2062 | 1,018.4 | 979.0/1,022.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2063 | 1,015.7 | 979.5/1,028.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2064 | 1,008.1 | 962.7/1,013.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2065 | 263.7 | 262.7/274.6 | 663.0 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2066 | 613.5 | 613.2/618.2 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 2067 | 56.3 | 55.9/57.1 | 1.7 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 2068 | 1,086.1 | 1,009.7/1,110.9 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 2069 | 1,046.2 | 976.0/1,055.3 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 2070 | 1,031.6 | 949.7/1,043.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 2071 | 1,029.1 | 962.8/1,034.9 | 239.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 2072 | 1,037.3 | 960.8/1,072.4 | 238.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 2073 | 1,030.8 | 954.1/1,052.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 2074 | 1,031.3 | 945.7/1,038.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 2075 | 1,021.3 | 954.1/1,027.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 2076 | 1,023.9 | 936.5/1,031.7 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 2077 | 1,029.4 | 943.9/1,030.0 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2078 | 1,021.5 | 998.1/1,027.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2079 | 994.9 | 990.9/1,041.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2080 | 998.8 | 985.9/1,025.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2081 | 990.8 | 975.7/1,058.2 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2082 | 990.9 | 942.8/1,026.8 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2083 | 1,007.7 | 947.1/1,023.4 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2084 | 995.6 | 948.0/1,013.0 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2085 | 989.4 | 942.8/996.8 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2086 | 1,000.4 | 942.2/1,014.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2087 | 994.1 | 946.9/1,022.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2088 | 999.2 | 981.7/1,023.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2089 | 1,020.5 | 992.4/1,024.1 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2090 | 1,019.9 | 996.6/1,025.2 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2091 | 1,017.0 | 993.7/1,027.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2092 | 1,019.0 | 992.0/1,035.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2093 | 997.9 | 993.8/1,017.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2094 | 998.8 | 986.3/1,023.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2095 | 1,002.5 | 999.1/1,017.2 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2096 | 998.4 | 993.2/1,023.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2097 | 1,002.0 | 984.0/1,019.6 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2098 | 1,000.9 | 941.0/1,017.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2099 | 994.8 | 946.7/1,018.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2100 | 999.8 | 947.9/1,016.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2101 | 946.7 | 939.4/1,019.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2102 | 951.3 | 941.5/1,017.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2103 | 997.4 | 946.3/1,016.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2104 | 256.1 | 247.4/259.2 | 663.0 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2105 | 621.7 | 618.4/668.1 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 2106 | 53.1 | 48.4/54.8 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 2107 | 988.8 | 970.0/1,083.2 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 2108 | 953.5 | 939.8/1,050.5 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 2109 | 946.5 | 934.0/1,029.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 2110 | 948.1 | 899.9/1,028.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 2111 | 948.4 | 899.1/1,023.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 2112 | 946.5 | 943.2/1,022.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 2113 | 945.5 | 944.7/1,019.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 2114 | 1,008.4 | 957.4/1,018.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 2115 | 982.7 | 981.3/1,019.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 2116 | 998.9 | 956.6/1,020.0 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2117 | 998.6 | 991.8/1,020.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2118 | 983.9 | 960.1/991.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2119 | 992.0 | 936.7/1,017.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2120 | 985.0 | 940.2/1,029.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2121 | 989.1 | 988.8/1,031.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2122 | 993.6 | 946.2/1,026.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2123 | 987.3 | 960.7/1,001.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2124 | 981.3 | 979.5/987.3 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2125 | 948.6 | 947.2/987.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2126 | 978.0 | 934.8/995.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2127 | 963.7 | 935.9/995.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2128 | 976.6 | 942.4/997.1 | 235.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2129 | 988.2 | 975.2/992.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2130 | 982.2 | 949.5/995.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2131 | 990.0 | 940.2/991.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2132 | 991.7 | 941.4/1,009.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2133 | 1,000.9 | 946.6/1,018.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2134 | 990.9 | 989.8/1,023.0 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2135 | 995.0 | 976.2/1,050.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2136 | 975.2 | 912.9/1,022.8 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2137 | 988.1 | 909.9/1,019.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2138 | 937.9 | 931.2/990.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2139 | 932.8 | 930.4/989.8 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2140 | 941.4 | 928.6/989.3 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2141 | 929.8 | 910.5/994.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2142 | 929.1 | 918.1/997.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2143 | 241.5 | 239.4/245.9 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2144 | 620.8 | 616.1/624.1 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 2145 | 49.9 | 46.2/53.3 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 2146 | 1,010.6 | 957.7/1,075.7 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 2147 | 988.5 | 927.6/1,035.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 2148 | 972.7 | 918.9/1,027.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 2149 | 936.3 | 928.4/1,022.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 2150 | 940.1 | 920.0/1,019.2 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 2151 | 950.8 | 936.2/1,020.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 2152 | 945.6 | 938.4/1,032.3 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 2153 | 939.8 | 937.0/1,022.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 2154 | 942.9 | 940.3/1,022.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 2155 | 943.5 | 939.5/1,019.7 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2156 | 937.2 | 935.3/1,024.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2157 | 917.7 | 915.7/1,018.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2158 | 924.4 | 914.6/1,023.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2159 | 938.4 | 915.7/1,017.8 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2160 | 941.4 | 912.5/1,016.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2161 | 974.8 | 907.7/1,018.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2162 | 987.8 | 916.9/1,021.9 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2163 | 1,008.5 | 934.7/1,018.1 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2164 | 1,016.5 | 942.8/1,021.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2165 | 1,022.7 | 945.7/1,024.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2166 | 1,016.9 | 929.7/1,021.2 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2167 | 1,007.3 | 937.0/1,018.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2168 | 1,022.1 | 939.8/1,035.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2169 | 1,023.7 | 953.8/1,025.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2170 | 1,027.6 | 922.9/1,030.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2171 | 987.6 | 917.3/1,025.7 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2172 | 987.9 | 922.0/1,073.0 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2173 | 991.7 | 920.7/1,045.7 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2174 | 991.4 | 920.4/1,024.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2175 | 992.8 | 920.8/1,020.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2176 | 995.3 | 923.9/1,025.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2177 | 992.8 | 913.1/1,023.1 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2178 | 997.0 | 894.5/1,023.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2179 | 998.0 | 896.8/1,029.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2180 | 995.4 | 895.0/1,021.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2181 | 1,046.6 | 992.7/1,291.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2182 | 257.6 | 241.8/276.8 | 662.0 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2183 | 617.5 | 614.6/622.2 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 2184 | 52.0 | 51.0/54.6 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 2185 | 1,025.0 | 956.8/1,070.0 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 2186 | 974.2 | 915.1/1,043.6 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 2187 | 1,009.6 | 928.1/1,036.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 2188 | 1,036.1 | 921.1/1,036.5 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 2189 | 1,029.6 | 927.5/1,039.1 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 2190 | 1,033.7 | 946.4/1,039.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 2191 | 1,023.8 | 949.6/1,024.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 2192 | 1,022.5 | 932.6/1,023.7 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 2193 | 1,030.7 | 927.6/1,034.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 2194 | 1,026.5 | 934.1/1,037.1 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2195 | 1,027.9 | 938.4/1,028.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2196 | 1,027.0 | 949.5/1,034.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2197 | 1,020.8 | 945.5/1,035.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2198 | 1,028.6 | 914.8/1,037.9 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2199 | 1,024.4 | 917.0/1,028.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2200 | 1,022.5 | 911.6/1,029.1 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2201 | 1,023.7 | 910.7/1,029.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2202 | 1,021.7 | 897.5/1,025.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2203 | 1,019.6 | 912.0/1,038.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2204 | 1,019.5 | 907.8/1,028.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2205 | 1,023.3 | 909.7/1,029.0 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2206 | 1,025.5 | 945.2/1,028.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2207 | 1,021.7 | 985.5/1,023.4 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2208 | 1,021.7 | 946.5/1,023.3 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2209 | 1,018.1 | 946.7/1,024.2 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2210 | 1,019.1 | 938.7/1,026.5 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2211 | 1,020.7 | 939.5/1,028.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2212 | 1,019.2 | 944.0/1,027.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2213 | 1,020.1 | 939.9/1,025.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2214 | 1,018.0 | 942.5/1,021.4 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2215 | 1,018.4 | 936.9/1,023.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2216 | 1,016.2 | 961.7/1,038.7 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2217 | 1,024.7 | 939.0/1,030.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2218 | 1,019.7 | 984.0/1,033.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2219 | 1,022.6 | 1,007.9/3,248.3 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2220 | 1,029.5 | 1,001.8/1,072.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2221 | 261.2 | 250.2/266.2 | 662.0 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2222 | 616.6 | 603.6/619.3 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 2223 | 56.4 | 54.4/57.9 | 1.7 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 2224 | 1,070.8 | 1,064.8/1,096.7 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 2225 | 1,043.5 | 1,033.3/1,052.0 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 2226 | 1,035.0 | 1,032.7/1,043.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 2227 | 1,032.4 | 1,028.8/1,042.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 2228 | 1,030.4 | 1,023.6/1,036.2 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 2229 | 1,025.3 | 1,023.7/1,030.9 | 235.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 2230 | 1,024.1 | 1,001.0/1,042.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 2231 | 1,022.8 | 1,010.6/1,029.8 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 2232 | 1,033.1 | 1,027.7/1,052.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 2233 | 1,028.5 | 1,026.4/1,036.8 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2234 | 1,022.8 | 1,003.4/1,032.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2235 | 1,035.6 | 992.6/1,048.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2236 | 1,023.7 | 1,021.4/1,028.1 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2237 | 1,024.9 | 1,022.0/1,028.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2238 | 1,029.5 | 1,028.0/1,033.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2239 | 1,020.4 | 1,003.6/1,024.2 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2240 | 1,025.3 | 1,001.3/1,039.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2241 | 1,017.6 | 1,005.7/1,019.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2242 | 1,016.7 | 1,000.2/1,028.2 | 235.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2243 | 1,017.3 | 1,003.4/1,031.7 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2244 | 1,015.5 | 998.5/1,028.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2245 | 1,020.8 | 1,001.7/1,033.6 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2246 | 1,020.6 | 1,001.9/1,024.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2247 | 1,018.8 | 978.9/1,032.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2248 | 1,021.6 | 950.0/1,022.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2249 | 1,026.3 | 946.5/1,030.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2250 | 1,021.3 | 942.2/1,029.1 | 238.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2251 | 999.5 | 946.1/1,026.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2252 | 1,024.7 | 1,019.0/1,041.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2253 | 1,010.1 | 996.6/1,021.7 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2254 | 1,006.7 | 994.6/1,021.7 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2255 | 1,017.2 | 1,000.0/1,023.4 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2256 | 1,014.5 | 1,000.0/1,023.3 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2257 | 1,021.7 | 999.7/1,026.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2258 | 1,020.4 | 998.3/1,091.9 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2259 | 1,021.2 | 999.3/1,048.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2260 | 270.6 | 261.6/273.4 | 664.0 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2261 | 615.9 | 615.0/617.5 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 2262 | 57.4 | 56.6/58.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 2263 | 1,077.9 | 1,076.0/1,090.7 | 267.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 2264 | 1,054.6 | 1,029.0/1,056.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 2265 | 1,039.7 | 1,010.8/1,042.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 2266 | 1,032.1 | 1,005.1/1,038.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 2267 | 1,027.1 | 1,004.3/1,050.3 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 2268 | 1,005.6 | 997.0/1,043.2 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 2269 | 1,008.9 | 1,004.1/1,093.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 2270 | 1,011.0 | 1,001.6/1,048.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 2271 | 1,017.0 | 978.5/1,038.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 2272 | 997.9 | 951.0/1,035.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2273 | 1,020.8 | 970.0/1,037.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2274 | 1,030.5 | 950.3/1,042.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2275 | 1,037.5 | 1,000.4/1,040.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2276 | 1,029.5 | 1,001.2/1,035.7 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2277 | 1,032.8 | 1,000.6/1,038.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2278 | 1,034.7 | 976.1/1,036.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2279 | 1,022.6 | 941.9/1,034.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2280 | 1,031.0 | 946.7/1,040.3 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2281 | 1,026.3 | 948.3/1,042.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2282 | 1,033.7 | 942.6/1,035.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2283 | 1,028.9 | 952.9/1,036.7 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2284 | 1,033.2 | 950.9/1,064.8 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2285 | 1,033.1 | 943.5/1,035.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2286 | 1,025.3 | 947.4/1,032.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2287 | 1,029.6 | 936.9/1,035.2 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2288 | 1,024.6 | 932.5/1,038.0 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2289 | 1,028.0 | 1,003.3/1,033.6 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2290 | 1,028.4 | 998.6/1,034.7 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2291 | 1,028.4 | 1,003.9/1,030.2 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2292 | 1,019.6 | 995.4/1,030.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2293 | 1,021.2 | 936.6/1,034.2 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2294 | 1,017.4 | 932.4/1,028.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2295 | 1,024.8 | 935.1/1,036.1 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2296 | 1,022.8 | 934.1/1,028.7 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2297 | 1,022.6 | 938.2/1,024.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2298 | 1,015.2 | 942.1/1,033.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2299 | 269.9 | 262.0/274.2 | 663.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2300 | 620.2 | 616.3/622.4 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 2301 | 54.4 | 49.8/57.5 | 1.7 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 2302 | 1,085.6 | 989.0/1,093.8 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 2303 | 1,039.8 | 952.9/1,051.5 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 2304 | 1,018.4 | 928.4/1,042.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 2305 | 992.8 | 926.7/1,030.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 2306 | 992.9 | 927.0/1,036.1 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 2307 | 998.1 | 900.6/1,025.0 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 2308 | 978.8 | 910.9/1,026.0 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 2309 | 942.6 | 942.5/1,027.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 2310 | 988.5 | 933.3/1,039.7 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 2311 | 995.7 | 942.8/1,031.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2312 | 959.2 | 940.1/1,036.7 | 244.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2313 | 945.8 | 939.1/1,028.2 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2314 | 1,024.1 | 947.6/1,037.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2315 | 997.2 | 981.8/999.2 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2316 | 997.6 | 993.8/1,000.6 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2317 | 994.7 | 994.4/999.5 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2318 | 985.1 | 941.0/1,004.0 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2319 | 994.4 | 940.1/996.5 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2320 | 998.9 | 940.0/1,008.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2321 | 999.0 | 927.2/1,006.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2322 | 998.7 | 956.2/1,029.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2323 | 992.6 | 991.6/1,033.5 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2324 | 1,002.3 | 996.7/1,024.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2325 | 1,003.1 | 995.9/1,021.1 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2326 | 997.8 | 983.3/1,017.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2327 | 1,003.4 | 986.4/1,027.3 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2328 | 1,015.2 | 1,001.1/1,033.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2329 | 1,020.7 | 1,015.9/1,031.5 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2330 | 1,022.3 | 1,020.4/1,056.3 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2331 | 1,028.7 | 997.4/1,038.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2332 | 1,032.9 | 959.8/1,034.2 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2333 | 1,029.6 | 950.8/1,031.8 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2334 | 1,018.9 | 999.3/1,029.1 | 237.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2335 | 1,023.6 | 988.2/1,034.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2336 | 1,025.4 | 984.8/1,029.2 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2337 | 1,014.6 | 990.4/2,139.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2338 | 270.5 | 245.7/282.7 | 661.6 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2339 | 616.0 | 609.1/622.3 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 2340 | 53.9 | 49.0/56.0 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 2341 | 1,068.6 | 1,051.3/1,075.4 | 238.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 2342 | 1,016.3 | 1,013.0/1,062.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 2343 | 1,008.4 | 999.3/1,054.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 2344 | 1,007.2 | 999.8/1,038.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 2345 | 1,003.3 | 986.0/1,048.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 2346 | 997.2 | 989.7/1,041.8 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 2347 | 1,000.3 | 971.3/1,037.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 2348 | 1,001.8 | 973.9/1,035.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 2349 | 998.0 | 934.7/1,037.3 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 2350 | 1,003.7 | 924.1/1,029.4 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2351 | 1,030.0 | 993.2/1,047.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2352 | 965.9 | 941.0/1,038.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2353 | 939.9 | 922.7/1,025.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2354 | 941.0 | 918.7/1,030.6 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2355 | 940.2 | 935.0/1,033.2 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2356 | 947.4 | 923.5/1,021.9 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2357 | 965.5 | 948.0/1,029.2 | 237.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2358 | 943.1 | 913.0/1,035.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2359 | 941.2 | 928.3/1,028.4 | 240.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2360 | 935.7 | 921.1/1,032.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2361 | 987.8 | 916.6/1,026.4 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2362 | 980.8 | 926.1/1,045.6 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2363 | 985.6 | 944.2/1,031.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2364 | 991.3 | 942.6/1,030.4 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2365 | 982.9 | 939.7/1,038.1 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2366 | 1,000.5 | 981.6/1,065.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2367 | 993.9 | 992.4/1,044.2 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2368 | 1,006.1 | 982.4/1,039.6 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2369 | 985.5 | 971.9/1,029.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2370 | 981.4 | 935.1/1,022.4 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2371 | 989.2 | 942.7/1,013.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2372 | 950.3 | 935.4/1,031.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2373 | 932.0 | 931.0/1,025.9 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2374 | 936.9 | 914.3/1,020.6 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2375 | 930.2 | 908.6/1,023.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2376 | 930.4 | 911.5/1,019.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2377 | 233.8 | 226.5/271.4 | 663.0 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2378 | 623.4 | 616.3/624.7 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 2379 | 49.8 | 41.5/53.3 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 2380 | 994.9 | 988.4/1,102.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 2381 | 961.5 | 942.5/1,048.3 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 2382 | 948.0 | 933.5/1,037.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 2383 | 936.9 | 934.1/1,033.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 2384 | 941.4 | 934.0/1,029.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 2385 | 953.7 | 930.4/1,031.7 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 2386 | 949.7 | 934.4/1,048.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 2387 | 948.2 | 936.5/1,031.8 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 2388 | 946.5 | 921.4/1,031.9 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 2389 | 984.7 | 918.1/1,025.2 | 235.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2390 | 990.2 | 915.6/1,033.0 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2391 | 993.8 | 897.1/1,025.4 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2392 | 990.1 | 895.8/1,035.1 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2393 | 985.0 | 902.2/1,024.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2394 | 992.9 | 895.0/1,031.5 | 237.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2395 | 989.9 | 895.1/1,029.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2396 | 1,008.7 | 886.9/1,027.7 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2397 | 1,022.8 | 895.1/1,023.5 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2398 | 1,014.7 | 897.1/1,022.6 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2399 | 1,022.3 | 903.9/1,027.7 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2400 | 1,014.2 | 900.2/1,021.1 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2401 | 1,018.7 | 899.8/1,023.5 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2402 | 1,001.5 | 900.4/1,028.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2403 | 1,022.1 | 919.9/1,029.5 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2404 | 1,025.7 | 1,021.3/1,567.0 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2405 | 1,001.7 | 984.8/1,023.1 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2406 | 989.2 | 957.5/993.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2407 | 988.4 | 945.3/1,010.7 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2408 | 985.9 | 952.1/1,035.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2409 | 955.1 | 946.5/1,020.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2410 | 942.6 | 941.5/1,023.9 | 238.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2411 | 993.8 | 926.5/1,016.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2412 | 988.7 | 919.3/1,025.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2413 | 986.5 | 951.5/1,029.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2414 | 994.2 | 992.8/1,009.7 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2415 | 987.3 | 986.7/1,019.0 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2416 | 247.4 | 241.0/287.7 | 661.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2417 | 623.2 | 617.6/623.5 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 2418 | 51.1 | 45.5/55.1 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 2419 | 1,049.1 | 975.3/1,059.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 2420 | 1,009.2 | 1,001.0/1,018.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 2421 | 986.8 | 969.7/996.4 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 2422 | 952.2 | 939.4/991.5 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 2423 | 953.1 | 941.7/1,006.6 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 2424 | 997.2 | 983.6/1,037.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 2425 | 1,000.7 | 999.2/1,080.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 2426 | 1,023.3 | 996.7/1,030.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 2427 | 1,029.3 | 1,024.5/1,056.1 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 2428 | 1,024.0 | 1,020.1/1,028.8 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2429 | 1,026.9 | 1,022.0/1,066.2 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2430 | 1,026.1 | 1,019.2/1,034.1 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2431 | 1,028.1 | 1,024.3/1,028.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2432 | 1,017.6 | 1,017.3/1,027.8 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2433 | 1,025.9 | 1,022.1/1,033.9 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2434 | 1,029.3 | 1,021.3/1,034.3 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2435 | 1,028.2 | 1,020.8/1,030.7 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2436 | 1,022.3 | 1,021.5/1,023.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2437 | 1,022.7 | 1,019.4/1,030.8 | 236.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2438 | 1,001.9 | 1,000.0/1,020.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2439 | 995.9 | 989.8/1,027.5 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2440 | 991.4 | 985.0/1,033.1 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2441 | 988.9 | 982.4/1,025.8 | 236.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2442 | 980.0 | 912.7/1,032.2 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2443 | 988.5 | 908.4/1,035.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2444 | 986.6 | 918.2/1,028.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2445 | 1,019.7 | 909.2/1,026.6 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2446 | 1,020.2 | 902.6/1,027.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2447 | 996.1 | 909.7/1,032.6 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2448 | 999.7 | 894.7/1,021.7 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2449 | 992.1 | 890.1/1,030.8 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2450 | 962.7 | 887.3/1,029.2 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2451 | 944.9 | 887.3/1,030.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2452 | 949.1 | 942.7/1,031.7 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2453 | 949.8 | 911.7/1,030.8 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2454 | 937.1 | 916.2/1,033.2 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2455 | 247.3 | 219.7/270.1 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2456 | 620.3 | 611.3/623.3 | 6.9 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 2457 | 53.8 | 48.4/58.1 | 1.8 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 2458 | 1,075.8 | 1,033.0/1,104.3 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer01 | 2459 | 1,051.5 | 967.0/1,075.4 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer02 | 2460 | 1,033.0 | 1,015.5/1,050.1 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer03 | 2461 | 1,024.7 | 1,004.7/1,045.9 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer04 | 2462 | 1,029.4 | 1,017.1/1,046.6 | 236.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer05 | 2463 | 1,039.5 | 1,012.2/1,590.1 | 237.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer06 | 2464 | 1,040.6 | 1,016.5/1,097.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer07 | 2465 | 1,036.2 | 1,013.1/1,049.9 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer08 | 2466 | 1,027.5 | 1,001.0/1,098.1 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer09 | 2467 | 1,016.4 | 1,000.4/1,047.7 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer10 | 2468 | 1,024.3 | 1,007.3/1,035.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer11 | 2469 | 1,026.1 | 996.9/1,041.5 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer12 | 2470 | 1,020.9 | 998.2/1,032.9 | 236.8 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer13 | 2471 | 1,020.9 | 996.8/1,032.3 | 237.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer14 | 2472 | 1,019.8 | 1,006.7/1,039.3 | 237.4 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer15 | 2473 | 1,027.9 | 1,026.0/1,030.4 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer16 | 2474 | 1,024.0 | 995.9/1,033.6 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer17 | 2475 | 1,020.8 | 1,002.4/1,037.0 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer18 | 2476 | 1,012.4 | 1,000.2/1,021.8 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer19 | 2477 | 1,022.1 | 1,004.7/1,041.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer20 | 2478 | 1,016.5 | 946.2/1,029.4 | 236.3 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer21 | 2479 | 1,017.7 | 951.6/1,045.2 | 245.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer22 | 2480 | 1,030.9 | 941.3/1,034.0 | 236.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer23 | 2481 | 1,024.0 | 951.1/1,034.5 | 236.6 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer24 | 2482 | 1,022.9 | 981.2/1,036.9 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer25 | 2483 | 1,002.6 | 970.1/1,042.5 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer26 | 2484 | 1,012.3 | 940.5/1,052.7 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer27 | 2485 | 960.4 | 957.0/1,040.1 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer28 | 2486 | 994.0 | 939.9/1,035.1 | 237.0 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer29 | 2487 | 990.0 | 942.8/1,077.9 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer30 | 2488 | 1,028.9 | 979.5/1,031.1 | 237.7 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer31 | 2489 | 1,002.1 | 994.2/1,033.8 | 236.9 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer32 | 2490 | 1,014.4 | 998.8/1,030.4 | 237.2 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer33 | 2491 | 1,017.0 | 1,000.8/1,026.6 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer34 | 2492 | 1,016.3 | 997.9/1,042.3 | 237.1 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_layer35 | 2493 | 1,030.3 | 1,011.2/1,033.2 | 236.5 | cudaLaunchKernel | 43 |
| answer | mir_operator:decode_head | 2494 | 270.0 | 256.4/271.1 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 2495 | 612.1 | 611.9/654.4 | 7.0 | cudaStreamSynchronize | 1 |
| answer | pre_d2h_alloc |  | 757.2 | 246.3/1,450.9 | 0.8 | cudaMemcpyAsync | 0 |
| answer | d2h_stage |  | 134.2 | 125.2/159.0 | 0.9 | cudaEventRecordWithFlags | 0 |
| answer | checksum_complete |  | 45.7 | 43.2/52.4 | 0.0 | cudaEventDestroy | 0 |
| <dag> | dag_schedule_gap |  | 71.5 | 17.9/803.0 | 0.0 |  | 0 |
| <dag> | iteration_tail_sync |  | 106.0 | 103.0/141.2 | 0.0 | cudaDeviceSynchronize | 0 |

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

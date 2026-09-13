# G02/G03 call-wise process attribution: `react_tool`

Lineage `h22-gpu-autotrace`, workflow w02. Consumes the w01 trace only; no re-timing.
Host events aligned to the nsys clock by a constant offset fitted on 10416 operator pairs (spread 10.9 us).

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
| inter_operator_dispatch | 10410 | 442,627.7 | 3.78 % | 42.5 | 4,322.2 | 0.2 % | 6.1 % | 1.0 % |
| mir_operator:decode_layer00 | 330 | 406,155.6 | 3.47 % | 1,230.8 | 68,084.4 | 3.09 % | 23.2 % | 16.8 % |
| mir_operator:decode_layer01 | 330 | 388,129.2 | 3.32 % | 1,176.1 | 67,915.4 | 3.08 % | 23.7 % | 17.5 % |
| mir_operator:decode_layer25 | 330 | 386,603.6 | 3.3 % | 1,171.5 | 68,114.4 | 3.09 % | 23.5 % | 17.6 % |
| mir_operator:decode_layer02 | 330 | 385,462.0 | 3.29 % | 1,168.1 | 68,837.2 | 3.12 % | 23.9 % | 17.9 % |
| mir_operator:decode_layer27 | 330 | 384,573.8 | 3.29 % | 1,165.4 | 67,900.1 | 3.08 % | 23.6 % | 17.7 % |
| mir_operator:decode_layer03 | 330 | 383,487.7 | 3.28 % | 1,162.1 | 68,522.6 | 3.11 % | 23.9 % | 17.9 % |
| mir_operator:decode_layer04 | 330 | 383,014.0 | 3.27 % | 1,160.6 | 68,309.1 | 3.1 % | 23.8 % | 17.8 % |
| mir_operator:decode_layer05 | 330 | 382,669.2 | 3.27 % | 1,159.6 | 68,462.4 | 3.11 % | 23.9 % | 17.9 % |
| mir_operator:decode_layer06 | 330 | 382,474.4 | 3.27 % | 1,159.0 | 68,599.1 | 3.11 % | 23.8 % | 17.9 % |
| mir_operator:decode_layer12 | 330 | 382,414.8 | 3.27 % | 1,158.8 | 68,661.4 | 3.12 % | 23.9 % | 18.0 % |
| mir_operator:decode_layer08 | 330 | 382,355.0 | 3.27 % | 1,158.7 | 68,263.2 | 3.1 % | 23.8 % | 17.9 % |
| mir_operator:decode_layer26 | 330 | 382,071.9 | 3.26 % | 1,157.8 | 68,511.2 | 3.11 % | 23.9 % | 17.9 % |
| mir_operator:decode_layer09 | 330 | 381,855.6 | 3.26 % | 1,157.1 | 68,072.9 | 3.09 % | 24.0 % | 17.8 % |
| mir_operator:decode_layer11 | 330 | 381,850.6 | 3.26 % | 1,157.1 | 68,476.4 | 3.11 % | 23.9 % | 17.9 % |
| mir_operator:decode_layer07 | 330 | 381,796.5 | 3.26 % | 1,157.0 | 68,879.7 | 3.13 % | 23.9 % | 18.0 % |
| mir_operator:decode_layer17 | 330 | 381,795.9 | 3.26 % | 1,157.0 | 69,077.8 | 3.14 % | 24.0 % | 18.1 % |
| mir_operator:decode_layer15 | 330 | 381,524.1 | 3.26 % | 1,156.1 | 68,212.3 | 3.1 % | 24.0 % | 17.9 % |
| mir_operator:decode_layer18 | 330 | 381,336.5 | 3.26 % | 1,155.6 | 68,142.1 | 3.09 % | 23.8 % | 17.9 % |
| mir_operator:decode_layer10 | 330 | 381,092.2 | 3.26 % | 1,154.8 | 67,562.0 | 3.07 % | 23.8 % | 17.7 % |
| mir_operator:decode_layer19 | 330 | 381,064.7 | 3.26 % | 1,154.7 | 68,317.1 | 3.1 % | 23.9 % | 17.9 % |
| mir_operator:decode_layer16 | 330 | 380,807.8 | 3.25 % | 1,154.0 | 67,869.9 | 3.08 % | 23.8 % | 17.8 % |
| mir_operator:decode_layer14 | 330 | 380,740.9 | 3.25 % | 1,153.8 | 67,707.6 | 3.07 % | 24.0 % | 17.8 % |
| mir_operator:decode_layer13 | 330 | 380,591.2 | 3.25 % | 1,153.3 | 68,007.3 | 3.09 % | 23.9 % | 17.9 % |
| mir_operator:decode_layer24 | 330 | 380,524.6 | 3.25 % | 1,153.1 | 68,162.6 | 3.09 % | 23.9 % | 17.9 % |
| mir_operator:decode_layer21 | 330 | 380,474.2 | 3.25 % | 1,153.0 | 68,437.2 | 3.11 % | 24.1 % | 18.0 % |
| mir_operator:decode_layer23 | 330 | 379,759.9 | 3.25 % | 1,150.8 | 68,309.3 | 3.1 % | 23.9 % | 18.0 % |
| mir_operator:decode_layer20 | 330 | 379,643.6 | 3.24 % | 1,150.4 | 68,589.2 | 3.11 % | 23.9 % | 18.1 % |
| mir_operator:decode_layer22 | 330 | 379,514.6 | 3.24 % | 1,150.0 | 68,764.0 | 3.12 % | 24.0 % | 18.1 % |
| mir_operator:decode_sample | 330 | 205,980.0 | 1.76 % | 624.2 | 2,373.1 | 0.11 % | 92.2 % | 1.2 % |
| mir_operator:decode_head | 330 | 75,968.6 | 0.65 % | 230.2 | 219,940.7 | 9.98 % | 19.9 % | 289.5 % |
| mir_operator:decode_embed | 330 | 17,329.8 | 0.15 % | 52.5 | 627.4 | 0.03 % | 23.0 % | 3.6 % |
| mir_operator:prefill_layer00 | 6 | 9,614.8 | 0.08 % | 1,602.5 | 2,381.7 | 0.11 % | 24.0 % | 24.8 % |
| mir_operator:prefill_layer01 | 6 | 8,780.4 | 0.08 % | 1,463.4 | 2,087.8 | 0.09 % | 23.5 % | 23.8 % |
| mir_operator:prefill_layer03 | 6 | 7,934.8 | 0.07 % | 1,322.5 | 1,971.9 | 0.09 % | 23.6 % | 24.9 % |
| mir_operator:prefill_layer02 | 6 | 7,924.8 | 0.07 % | 1,320.8 | 1,982.9 | 0.09 % | 23.6 % | 25.0 % |
| mir_operator:prefill_layer04 | 6 | 7,762.6 | 0.07 % | 1,293.8 | 1,976.1 | 0.09 % | 24.0 % | 25.5 % |
| mir_operator:prefill_layer12 | 6 | 7,555.6 | 0.06 % | 1,259.3 | 2,220.7 | 0.1 % | 23.7 % | 29.4 % |
| mir_operator:prefill_layer15 | 6 | 7,519.9 | 0.06 % | 1,253.3 | 1,973.4 | 0.09 % | 23.8 % | 26.2 % |
| mir_operator:prefill_layer11 | 6 | 7,518.8 | 0.06 % | 1,253.1 | 1,969.8 | 0.09 % | 23.9 % | 26.2 % |
| mir_operator:prefill_layer05 | 6 | 7,503.4 | 0.06 % | 1,250.6 | 1,969.8 | 0.09 % | 24.0 % | 26.3 % |
| mir_operator:prefill_layer10 | 6 | 7,492.2 | 0.06 % | 1,248.7 | 1,997.4 | 0.09 % | 24.1 % | 26.7 % |
| mir_operator:prefill_layer13 | 6 | 7,477.3 | 0.06 % | 1,246.2 | 2,119.9 | 0.1 % | 23.8 % | 28.4 % |
| mir_operator:prefill_layer09 | 6 | 7,440.0 | 0.06 % | 1,240.0 | 1,977.9 | 0.09 % | 24.1 % | 26.6 % |
| mir_operator:prefill_layer06 | 6 | 7,421.7 | 0.06 % | 1,237.0 | 2,128.3 | 0.1 % | 24.1 % | 28.7 % |
| mir_operator:prefill_layer18 | 6 | 7,416.1 | 0.06 % | 1,236.0 | 2,013.4 | 0.09 % | 23.6 % | 27.1 % |
| mir_operator:prefill_layer16 | 6 | 7,397.3 | 0.06 % | 1,232.9 | 1,978.1 | 0.09 % | 23.7 % | 26.7 % |
| mir_operator:prefill_layer08 | 6 | 7,390.3 | 0.06 % | 1,231.7 | 1,990.4 | 0.09 % | 23.9 % | 26.9 % |
| mir_operator:prefill_layer17 | 6 | 7,383.0 | 0.06 % | 1,230.5 | 1,975.2 | 0.09 % | 23.8 % | 26.8 % |
| mir_operator:prefill_layer14 | 6 | 7,362.4 | 0.06 % | 1,227.1 | 1,974.0 | 0.09 % | 24.0 % | 26.8 % |
| mir_operator:prefill_layer27 | 6 | 7,359.2 | 0.06 % | 1,226.5 | 2,215.3 | 0.1 % | 24.3 % | 30.1 % |
| mir_operator:prefill_layer26 | 6 | 7,351.4 | 0.06 % | 1,225.2 | 2,000.0 | 0.09 % | 24.0 % | 27.2 % |
| mir_operator:prefill_layer25 | 6 | 7,317.6 | 0.06 % | 1,219.6 | 2,207.7 | 0.1 % | 24.0 % | 30.2 % |
| mir_operator:prefill_layer19 | 6 | 7,297.4 | 0.06 % | 1,216.2 | 2,091.8 | 0.09 % | 24.0 % | 28.7 % |
| mir_operator:prefill_layer07 | 6 | 7,290.0 | 0.06 % | 1,215.0 | 2,115.9 | 0.1 % | 24.1 % | 29.0 % |
| mir_operator:prefill_layer22 | 6 | 7,284.3 | 0.06 % | 1,214.1 | 1,976.2 | 0.09 % | 24.0 % | 27.1 % |
| mir_operator:prefill_layer24 | 6 | 7,274.8 | 0.06 % | 1,212.5 | 1,975.2 | 0.09 % | 24.2 % | 27.2 % |
| mir_operator:prefill_layer21 | 6 | 7,259.6 | 0.06 % | 1,209.9 | 1,977.3 | 0.09 % | 23.9 % | 27.2 % |
| mir_operator:prefill_layer20 | 6 | 7,257.5 | 0.06 % | 1,209.6 | 1,995.5 | 0.09 % | 24.0 % | 27.5 % |
| mir_operator:prefill_layer23 | 6 | 7,178.2 | 0.06 % | 1,196.4 | 1,978.0 | 0.09 % | 24.0 % | 27.6 % |
| token_preprocess_cpu | 6 | 6,188.6 | 0.05 % | 1,031.4 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| mir_operator:prefill_sample | 6 | 5,292.8 | 0.05 % | 882.1 | 50.3 | 0.0 % | 94.4 % | 0.9 % |
| pre_d2h_alloc | 6 | 4,315.9 | 0.04 % | 719.3 | 4.4 | 0.0 % | 3.8 % | 0.1 % |
| dag_schedule_gap | 9 | 2,614.6 | 0.02 % | 290.5 | 0.0 | 0.0 % | 1.1 % | 0.0 % |
| mir_operator:prefill_head | 6 | 1,487.9 | 0.01 % | 248.0 | 5,608.8 | 0.25 % | 20.2 % | 377.0 % |
| weight_init | 6 | 1,087.3 | 0.01 % | 181.2 | 0.0 | 0.0 % | 1.5 % | 0.0 % |
| agent_tool_execute_cpu | 3 | 824.4 | 0.01 % | 274.8 | 0.0 | 0.0 % | 0.0 % | 0.0 % |
| d2h_stage | 6 | 820.2 | 0.01 % | 136.7 | 5.2 | 0.0 % | 27.3 % | 0.6 % |
| h2d_stage | 6 | 742.4 | 0.01 % | 123.7 | 2.4 | 0.0 % | 33.6 % | 0.3 % |
| host_input_generate | 6 | 737.7 | 0.01 % | 123.0 | 0.0 | 0.0 % | 4.5 % | 0.0 % |
| mir_operator:prefill_embed | 6 | 597.9 | 0.01 % | 99.7 | 10.5 | 0.0 % | 18.1 % | 1.8 % |
| iteration_tail_sync | 3 | 346.7 | 0.0 % | 115.6 | 0.0 | 0.0 % | 12.2 % | 0.0 % |
| checksum_complete | 6 | 296.0 | 0.0 % | 49.3 | 0.0 | 0.0 % | 6.5 % | 0.0 % |
| adapter_dispatch | 6 | 24.8 | 0.0 % | 4.1 | 0.0 | 0.0 % | 0.0 % | 0.0 % |

## Call breakdown (agent nodes)

| call | kind | wave | matrix | host per iter (us) | host share | GPU per iter (us) | GPU share | GPU/host |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| plan | llm | 0 | 768 | 1,669,837.5 | 42.81 % | 315,184.0 | 42.92 % | 18.88 % |
| lookup | tool | 1 | 256 | 274.8 | 0.01 % | 0.0 | 0.0 % | 0.0 % |
| answer | llm | 2 | 768 | 2,229,845.0 | 57.16 % | 419,127.6 | 57.08 % | 18.8 % |
| <dag> | dag |  |  | 987.1 | 0.03 % | 0.0 | 0.0 % | 0.0 % |

## CUDA runtime API inside the measured window

| API | calls | total (us) | share of wall |
|---|---:|---:|---:|
| cudaLaunchKernel | 543144 | 2,648,348.5 | 22.63 % |
| cudaStreamSynchronize | 678 | 184,129.5 | 1.57 % |
| cudaMemcpyAsync | 690 | 8,770.8 | 0.07 % |
| cudaMemsetAsync | 504 | 4,907.9 | 0.04 % |
| cuLaunchKernel | 588 | 3,088.2 | 0.03 % |
| cudaStreamIsCapturing | 390 | 567.9 | 0.0 % |
| cuKernelGetFunction | 588 | 385.7 | 0.0 % |
| cudaEventRecordWithFlags | 36 | 230.4 | 0.0 % |
| cudaEventCreateWithFlags | 24 | 72.9 | 0.0 % |
| cudaEventQuery | 36 | 47.2 | 0.0 % |
| cudaEventSynchronize | 12 | 37.5 | 0.0 % |
| cudaEventDestroy | 24 | 26.5 | 0.0 % |

## Kernel families by process (G03)

| process | family | instances | GPU total (us) | share |
|---|---|---:|---:|---:|
| mir_operator:decode_head | gemv | 330 | 216,165.0 | 9.81 % |
| mir_operator:decode_layer07 | gemv | 2310 | 41,549.2 | 1.89 % |
| mir_operator:decode_layer17 | gemv | 2310 | 41,424.6 | 1.88 % |
| mir_operator:decode_layer06 | gemv | 2310 | 41,361.9 | 1.88 % |
| mir_operator:decode_layer20 | gemv | 2310 | 41,339.7 | 1.88 % |
| mir_operator:decode_layer26 | gemv | 2310 | 41,312.5 | 1.88 % |
| mir_operator:decode_layer05 | gemv | 2310 | 41,267.0 | 1.87 % |
| mir_operator:decode_layer02 | gemv | 2310 | 41,238.6 | 1.87 % |
| mir_operator:decode_layer03 | gemv | 2310 | 41,225.8 | 1.87 % |
| mir_operator:decode_layer19 | gemv | 2310 | 41,196.6 | 1.87 % |
| mir_operator:decode_layer22 | gemv | 2310 | 41,176.8 | 1.87 % |
| mir_operator:decode_layer11 | gemv | 2310 | 41,150.8 | 1.87 % |
| mir_operator:decode_layer12 | gemv | 2310 | 41,146.5 | 1.87 % |
| mir_operator:decode_layer21 | gemv | 2310 | 41,122.3 | 1.87 % |
| mir_operator:decode_layer08 | gemv | 2310 | 41,118.7 | 1.87 % |
| mir_operator:decode_layer15 | gemv | 2310 | 41,116.2 | 1.87 % |
| mir_operator:decode_layer04 | gemv | 2310 | 41,111.0 | 1.87 % |
| mir_operator:decode_layer23 | gemv | 2310 | 41,055.7 | 1.86 % |
| mir_operator:decode_layer24 | gemv | 2310 | 41,007.8 | 1.86 % |
| mir_operator:decode_layer25 | gemv | 2310 | 40,996.3 | 1.86 % |
| mir_operator:decode_layer18 | gemv | 2310 | 40,905.9 | 1.86 % |
| mir_operator:decode_layer27 | gemv | 2310 | 40,886.1 | 1.86 % |
| mir_operator:decode_layer00 | gemv | 2310 | 40,852.7 | 1.85 % |
| mir_operator:decode_layer01 | gemv | 2310 | 40,846.6 | 1.85 % |
| mir_operator:decode_layer16 | gemv | 2310 | 40,831.8 | 1.85 % |
| mir_operator:decode_layer13 | gemv | 2310 | 40,814.0 | 1.85 % |
| mir_operator:decode_layer09 | gemv | 2310 | 40,781.8 | 1.85 % |
| mir_operator:decode_layer10 | gemv | 2310 | 40,665.5 | 1.85 % |
| mir_operator:decode_layer14 | gemv | 2310 | 40,627.4 | 1.84 % |
| mir_operator:decode_layer02 | elementwise_binary | 5610 | 8,406.0 | 0.38 % |
| mir_operator:decode_layer06 | elementwise_binary | 5610 | 8,354.9 | 0.38 % |
| mir_operator:decode_layer22 | elementwise_binary | 5610 | 8,353.5 | 0.38 % |
| mir_operator:decode_layer17 | elementwise_binary | 5610 | 8,322.9 | 0.38 % |
| mir_operator:decode_layer12 | elementwise_binary | 5610 | 8,302.3 | 0.38 % |
| mir_operator:decode_layer13 | elementwise_binary | 5610 | 8,298.7 | 0.38 % |
| mir_operator:decode_layer20 | elementwise_binary | 5610 | 8,292.2 | 0.38 % |
| mir_operator:decode_layer09 | elementwise_binary | 5610 | 8,285.1 | 0.38 % |
| mir_operator:decode_layer04 | elementwise_binary | 5610 | 8,285.0 | 0.38 % |
| mir_operator:decode_layer26 | elementwise_binary | 5610 | 8,283.2 | 0.38 % |
| mir_operator:decode_layer07 | elementwise_binary | 5610 | 8,280.3 | 0.38 % |
| mir_operator:decode_layer23 | elementwise_binary | 5610 | 8,276.1 | 0.38 % |
| mir_operator:decode_layer11 | elementwise_binary | 5610 | 8,262.0 | 0.38 % |
| mir_operator:decode_layer08 | elementwise_binary | 5610 | 8,251.3 | 0.37 % |
| mir_operator:decode_layer16 | elementwise_binary | 5610 | 8,251.2 | 0.37 % |
| mir_operator:decode_layer21 | elementwise_binary | 5610 | 8,250.9 | 0.37 % |
| mir_operator:decode_layer25 | elementwise_binary | 5610 | 8,238.4 | 0.37 % |
| mir_operator:decode_layer15 | elementwise_binary | 5610 | 8,230.6 | 0.37 % |
| mir_operator:decode_layer03 | elementwise_binary | 5610 | 8,224.0 | 0.37 % |
| mir_operator:decode_layer18 | elementwise_binary | 5610 | 8,215.9 | 0.37 % |
| mir_operator:decode_layer19 | elementwise_binary | 5610 | 8,206.9 | 0.37 % |
| mir_operator:decode_layer00 | elementwise_binary | 5610 | 8,205.0 | 0.37 % |
| mir_operator:decode_layer01 | elementwise_binary | 5610 | 8,189.2 | 0.37 % |
| mir_operator:decode_layer14 | elementwise_binary | 5610 | 8,186.6 | 0.37 % |
| mir_operator:decode_layer24 | elementwise_binary | 5610 | 8,169.0 | 0.37 % |
| mir_operator:decode_layer10 | elementwise_binary | 5610 | 8,163.6 | 0.37 % |
| mir_operator:decode_layer05 | elementwise_binary | 5610 | 8,151.3 | 0.37 % |
| mir_operator:decode_layer27 | elementwise_binary | 5610 | 8,149.0 | 0.37 % |
| mir_operator:prefill_head | gemm | 6 | 5,499.9 | 0.25 % |
| mir_operator:decode_layer17 | copy | 2640 | 4,330.1 | 0.2 % |
| mir_operator:decode_layer07 | copy | 2640 | 4,237.9 | 0.19 % |
| mir_operator:decode_layer11 | copy | 2640 | 4,234.9 | 0.19 % |
| mir_operator:decode_layer06 | copy | 2640 | 4,234.6 | 0.19 % |
| mir_operator:decode_layer22 | copy | 2640 | 4,234.6 | 0.19 % |
| mir_operator:decode_layer19 | copy | 2640 | 4,227.4 | 0.19 % |
| mir_operator:decode_layer26 | copy | 2640 | 4,221.2 | 0.19 % |
| mir_operator:decode_layer18 | copy | 2640 | 4,213.2 | 0.19 % |
| mir_operator:decode_layer08 | copy | 2640 | 4,212.9 | 0.19 % |
| mir_operator:decode_layer23 | copy | 2640 | 4,211.8 | 0.19 % |
| mir_operator:decode_layer04 | copy | 2640 | 4,202.4 | 0.19 % |
| mir_operator:decode_layer20 | copy | 2640 | 4,202.2 | 0.19 % |
| mir_operator:decode_layer02 | copy | 2640 | 4,202.0 | 0.19 % |
| mir_operator:decode_layer09 | copy | 2640 | 4,201.7 | 0.19 % |
| mir_operator:decode_layer16 | copy | 2640 | 4,201.6 | 0.19 % |
| mir_operator:decode_layer15 | copy | 2640 | 4,201.6 | 0.19 % |
| mir_operator:decode_layer25 | copy | 2640 | 4,199.5 | 0.19 % |
| mir_operator:decode_layer13 | copy | 2640 | 4,198.6 | 0.19 % |
| mir_operator:decode_layer24 | copy | 2640 | 4,196.5 | 0.19 % |
| mir_operator:decode_layer00 | copy | 2640 | 4,195.2 | 0.19 % |
| mir_operator:decode_layer01 | copy | 2640 | 4,189.7 | 0.19 % |
| mir_operator:decode_layer21 | copy | 2640 | 4,186.1 | 0.19 % |
| mir_operator:decode_layer05 | copy | 2640 | 4,181.8 | 0.19 % |
| mir_operator:decode_layer12 | copy | 2640 | 4,181.5 | 0.19 % |
| mir_operator:decode_layer10 | copy | 2640 | 4,173.5 | 0.19 % |
| mir_operator:decode_layer03 | copy | 2640 | 4,158.0 | 0.19 % |
| mir_operator:decode_layer14 | copy | 2640 | 4,157.1 | 0.19 % |
| mir_operator:decode_layer27 | copy | 2640 | 4,142.5 | 0.19 % |
| mir_operator:decode_layer05 | attention | 660 | 3,335.4 | 0.15 % |
| mir_operator:decode_layer11 | attention | 660 | 3,305.5 | 0.15 % |
| mir_operator:decode_layer02 | attention | 660 | 3,273.0 | 0.15 % |
| mir_operator:decode_layer12 | elementwise_other | 2310 | 3,271.7 | 0.15 % |
| mir_operator:decode_layer23 | attention | 660 | 3,242.1 | 0.15 % |
| mir_operator:decode_layer17 | elementwise_other | 2310 | 3,241.8 | 0.15 % |
| mir_operator:decode_layer12 | attention | 660 | 3,240.8 | 0.15 % |
| mir_operator:decode_layer18 | attention | 660 | 3,239.8 | 0.15 % |
| mir_operator:decode_layer03 | attention | 660 | 3,235.9 | 0.15 % |
| mir_operator:decode_layer03 | elementwise_other | 2310 | 3,234.2 | 0.15 % |
| mir_operator:decode_layer00 | attention | 660 | 3,229.6 | 0.15 % |
| mir_operator:decode_layer07 | attention | 660 | 3,229.1 | 0.15 % |
| mir_operator:decode_layer27 | attention | 660 | 3,225.8 | 0.15 % |
| mir_operator:decode_layer08 | attention | 660 | 3,205.7 | 0.15 % |
| mir_operator:decode_layer02 | elementwise_other | 2310 | 3,203.5 | 0.15 % |
| mir_operator:decode_layer22 | elementwise_other | 2310 | 3,203.4 | 0.15 % |
| mir_operator:decode_layer17 | attention | 660 | 3,202.3 | 0.15 % |
| mir_operator:decode_layer24 | elementwise_other | 2310 | 3,194.3 | 0.15 % |
| mir_operator:decode_layer22 | attention | 660 | 3,185.8 | 0.14 % |
| mir_operator:decode_layer21 | elementwise_other | 2310 | 3,183.9 | 0.14 % |
| mir_operator:decode_layer25 | attention | 660 | 3,182.1 | 0.14 % |
| mir_operator:decode_layer14 | attention | 660 | 3,178.9 | 0.14 % |
| mir_operator:decode_layer21 | attention | 660 | 3,177.1 | 0.14 % |
| mir_operator:decode_layer19 | attention | 660 | 3,174.9 | 0.14 % |
| mir_operator:decode_layer01 | attention | 660 | 3,174.7 | 0.14 % |
| mir_operator:decode_layer04 | elementwise_other | 2310 | 3,173.9 | 0.14 % |
| mir_operator:decode_layer24 | attention | 660 | 3,173.0 | 0.14 % |
| mir_operator:decode_layer09 | elementwise_other | 2310 | 3,171.9 | 0.14 % |
| mir_operator:decode_layer14 | elementwise_other | 2310 | 3,170.6 | 0.14 % |
| mir_operator:decode_layer26 | attention | 660 | 3,167.8 | 0.14 % |
| mir_operator:decode_layer09 | attention | 660 | 3,161.3 | 0.14 % |
| mir_operator:decode_layer10 | attention | 660 | 3,161.1 | 0.14 % |
| mir_operator:decode_layer20 | attention | 660 | 3,158.5 | 0.14 % |
| mir_operator:decode_layer13 | attention | 660 | 3,155.4 | 0.14 % |
| mir_operator:decode_layer11 | elementwise_other | 2310 | 3,148.0 | 0.14 % |
| mir_operator:decode_layer15 | elementwise_other | 2310 | 3,146.8 | 0.14 % |
| mir_operator:decode_layer26 | elementwise_other | 2310 | 3,144.9 | 0.14 % |
| mir_operator:decode_layer06 | attention | 660 | 3,141.7 | 0.14 % |
| mir_operator:decode_layer16 | elementwise_other | 2310 | 3,138.7 | 0.14 % |
| mir_operator:decode_layer19 | elementwise_other | 2310 | 3,135.6 | 0.14 % |
| mir_operator:decode_layer04 | attention | 660 | 3,135.5 | 0.14 % |
| mir_operator:decode_layer00 | elementwise_other | 2310 | 3,133.7 | 0.14 % |
| mir_operator:decode_layer20 | elementwise_other | 2310 | 3,132.1 | 0.14 % |
| mir_operator:decode_layer15 | attention | 660 | 3,131.0 | 0.14 % |
| mir_operator:decode_layer13 | elementwise_other | 2310 | 3,124.6 | 0.14 % |
| mir_operator:decode_layer16 | attention | 660 | 3,122.8 | 0.14 % |
| mir_operator:decode_layer27 | elementwise_other | 2310 | 3,122.2 | 0.14 % |
| mir_operator:decode_layer23 | elementwise_other | 2310 | 3,120.8 | 0.14 % |
| mir_operator:decode_layer06 | elementwise_other | 2310 | 3,120.7 | 0.14 % |
| mir_operator:decode_layer07 | elementwise_other | 2310 | 3,116.1 | 0.14 % |
| mir_operator:decode_layer05 | elementwise_other | 2310 | 3,116.0 | 0.14 % |
| mir_operator:decode_layer08 | elementwise_other | 2310 | 3,113.1 | 0.14 % |
| mir_operator:decode_layer18 | elementwise_other | 2310 | 3,109.5 | 0.14 % |
| mir_operator:decode_layer10 | elementwise_other | 2310 | 3,105.0 | 0.14 % |
| mir_operator:decode_layer01 | elementwise_other | 2310 | 3,100.0 | 0.14 % |
| mir_operator:decode_layer25 | elementwise_other | 2310 | 3,093.4 | 0.14 % |
| mir_operator:decode_layer22 | elementwise_unary | 2640 | 3,039.6 | 0.14 % |
| mir_operator:decode_layer01 | elementwise_unary | 2640 | 3,000.7 | 0.14 % |
| mir_operator:decode_layer17 | elementwise_unary | 2640 | 2,991.2 | 0.14 % |
| mir_operator:decode_layer21 | elementwise_unary | 2640 | 2,975.2 | 0.14 % |
| mir_operator:decode_layer25 | elementwise_unary | 2640 | 2,975.2 | 0.14 % |
| mir_operator:decode_layer02 | elementwise_unary | 2640 | 2,974.2 | 0.14 % |
| mir_operator:decode_layer13 | elementwise_unary | 2640 | 2,971.3 | 0.13 % |
| mir_operator:decode_layer04 | elementwise_unary | 2640 | 2,965.4 | 0.13 % |
| mir_operator:decode_layer18 | elementwise_unary | 2640 | 2,960.4 | 0.13 % |
| mir_operator:decode_layer07 | elementwise_unary | 2640 | 2,960.4 | 0.13 % |
| mir_operator:decode_layer23 | elementwise_unary | 2640 | 2,956.0 | 0.13 % |
| mir_operator:decode_layer20 | elementwise_unary | 2640 | 2,954.0 | 0.13 % |
| mir_operator:decode_layer18 | reduce | 1320 | 2,952.9 | 0.13 % |
| mir_operator:decode_layer19 | elementwise_unary | 2640 | 2,951.6 | 0.13 % |
| mir_operator:decode_layer15 | elementwise_unary | 2640 | 2,951.2 | 0.13 % |
| mir_operator:decode_layer06 | elementwise_unary | 2640 | 2,950.8 | 0.13 % |
| mir_operator:decode_layer05 | elementwise_unary | 2640 | 2,950.1 | 0.13 % |
| mir_operator:decode_layer00 | elementwise_unary | 2640 | 2,948.8 | 0.13 % |
| mir_operator:decode_layer08 | elementwise_unary | 2640 | 2,948.4 | 0.13 % |
| mir_operator:decode_layer26 | elementwise_unary | 2640 | 2,944.8 | 0.13 % |
| mir_operator:decode_layer09 | elementwise_unary | 2640 | 2,942.6 | 0.13 % |
| mir_operator:decode_layer03 | elementwise_unary | 2640 | 2,926.4 | 0.13 % |
| mir_operator:decode_layer24 | elementwise_unary | 2640 | 2,923.8 | 0.13 % |
| mir_operator:decode_layer17 | reduce | 1320 | 2,920.0 | 0.13 % |
| mir_operator:decode_layer22 | reduce | 1320 | 2,919.2 | 0.13 % |
| mir_operator:decode_layer11 | elementwise_unary | 2640 | 2,918.9 | 0.13 % |
| mir_operator:decode_layer16 | elementwise_unary | 2640 | 2,916.2 | 0.13 % |
| mir_operator:decode_layer12 | elementwise_unary | 2640 | 2,915.4 | 0.13 % |
| mir_operator:decode_layer27 | elementwise_unary | 2640 | 2,914.9 | 0.13 % |
| mir_operator:decode_layer20 | reduce | 1320 | 2,910.2 | 0.13 % |
| mir_operator:decode_layer10 | elementwise_unary | 2640 | 2,909.7 | 0.13 % |
| mir_operator:decode_layer14 | elementwise_unary | 2640 | 2,907.1 | 0.13 % |
| mir_operator:decode_layer09 | reduce | 1320 | 2,897.0 | 0.13 % |
| mir_operator:decode_layer02 | reduce | 1320 | 2,894.7 | 0.13 % |
| mir_operator:decode_layer19 | reduce | 1320 | 2,894.0 | 0.13 % |
| mir_operator:decode_layer07 | reduce | 1320 | 2,890.7 | 0.13 % |
| mir_operator:decode_layer05 | reduce | 1320 | 2,890.5 | 0.13 % |
| mir_operator:decode_layer00 | reduce | 1320 | 2,890.2 | 0.13 % |
| mir_operator:decode_layer14 | reduce | 1320 | 2,883.4 | 0.13 % |
| mir_operator:decode_layer24 | reduce | 1320 | 2,878.6 | 0.13 % |
| mir_operator:decode_layer11 | reduce | 1320 | 2,878.0 | 0.13 % |
| mir_operator:decode_layer26 | reduce | 1320 | 2,877.2 | 0.13 % |
| mir_operator:decode_layer01 | reduce | 1320 | 2,876.7 | 0.13 % |
| mir_operator:decode_layer13 | reduce | 1320 | 2,874.8 | 0.13 % |
| mir_operator:decode_layer15 | reduce | 1320 | 2,871.0 | 0.13 % |
| mir_operator:decode_layer16 | reduce | 1320 | 2,871.0 | 0.13 % |
| mir_operator:decode_layer08 | reduce | 1320 | 2,868.0 | 0.13 % |
| mir_operator:decode_layer06 | reduce | 1320 | 2,866.4 | 0.13 % |
| mir_operator:decode_layer03 | reduce | 1320 | 2,866.3 | 0.13 % |
| mir_operator:decode_layer21 | reduce | 1320 | 2,865.8 | 0.13 % |
| mir_operator:decode_layer04 | reduce | 1320 | 2,865.1 | 0.13 % |
| mir_operator:decode_layer12 | reduce | 1320 | 2,862.1 | 0.13 % |
| mir_operator:decode_layer23 | reduce | 1320 | 2,851.6 | 0.13 % |
| mir_operator:decode_layer25 | reduce | 1320 | 2,847.9 | 0.13 % |
| mir_operator:decode_layer10 | reduce | 1320 | 2,844.4 | 0.13 % |
| mir_operator:decode_layer27 | reduce | 1320 | 2,840.3 | 0.13 % |
| mir_operator:decode_layer12 | concat | 1320 | 2,741.2 | 0.12 % |
| mir_operator:decode_layer21 | concat | 1320 | 2,675.8 | 0.12 % |
| mir_operator:decode_layer03 | concat | 1320 | 2,651.9 | 0.12 % |
| mir_operator:decode_layer22 | concat | 1320 | 2,651.2 | 0.12 % |
| mir_operator:decode_layer02 | concat | 1320 | 2,645.1 | 0.12 % |
| mir_operator:decode_layer17 | concat | 1320 | 2,644.9 | 0.12 % |
| mir_operator:decode_layer09 | concat | 1320 | 2,631.5 | 0.12 % |
| mir_operator:decode_layer00 | concat | 1320 | 2,629.2 | 0.12 % |
| mir_operator:decode_layer24 | concat | 1320 | 2,619.6 | 0.12 % |
| mir_operator:decode_layer27 | concat | 1320 | 2,619.3 | 0.12 % |
| mir_operator:decode_layer07 | concat | 1320 | 2,616.1 | 0.12 % |
| mir_operator:decode_layer20 | concat | 1320 | 2,600.4 | 0.12 % |
| mir_operator:decode_layer14 | concat | 1320 | 2,596.6 | 0.12 % |
| mir_operator:decode_layer23 | concat | 1320 | 2,595.1 | 0.12 % |
| mir_operator:decode_layer25 | concat | 1320 | 2,581.7 | 0.12 % |
| mir_operator:decode_layer11 | concat | 1320 | 2,578.4 | 0.12 % |
| mir_operator:decode_layer04 | concat | 1320 | 2,570.8 | 0.12 % |
| mir_operator:decode_layer05 | concat | 1320 | 2,570.3 | 0.12 % |
| mir_operator:decode_layer13 | concat | 1320 | 2,569.8 | 0.12 % |
| mir_operator:decode_layer06 | concat | 1320 | 2,568.2 | 0.12 % |
| mir_operator:decode_layer15 | concat | 1320 | 2,563.9 | 0.12 % |
| mir_operator:decode_layer26 | concat | 1320 | 2,559.6 | 0.12 % |
| mir_operator:decode_layer08 | concat | 1320 | 2,545.1 | 0.12 % |
| mir_operator:decode_layer18 | concat | 1320 | 2,544.5 | 0.12 % |
| mir_operator:decode_layer10 | concat | 1320 | 2,539.2 | 0.12 % |
| mir_operator:decode_layer01 | concat | 1320 | 2,537.7 | 0.12 % |
| mir_operator:decode_layer16 | concat | 1320 | 2,536.6 | 0.12 % |
| mir_operator:decode_layer19 | concat | 1320 | 2,530.1 | 0.11 % |
| mir_operator:decode_sample | reduce | 330 | 1,911.8 | 0.09 % |
| mir_operator:prefill_layer12 | gemm | 42 | 1,469.1 | 0.07 % |
| mir_operator:prefill_layer25 | gemm | 42 | 1,413.9 | 0.06 % |
| inter_operator_dispatch | elementwise_other | 1008 | 1,391.5 | 0.06 % |
| mir_operator:prefill_layer07 | gemm | 42 | 1,357.5 | 0.06 % |
| mir_operator:prefill_layer00 | gemm | 42 | 1,334.6 | 0.06 % |
| mir_operator:prefill_layer27 | gemm | 42 | 1,333.3 | 0.06 % |
| mir_operator:prefill_layer01 | gemm | 42 | 1,299.0 | 0.06 % |
| mir_operator:prefill_layer13 | gemm | 42 | 1,280.0 | 0.06 % |
| mir_operator:decode_head | elementwise_binary | 990 | 1,273.0 | 0.06 % |
| mir_operator:prefill_layer19 | gemm | 42 | 1,260.9 | 0.06 % |
| mir_operator:prefill_layer26 | gemm | 42 | 1,249.2 | 0.06 % |
| mir_operator:prefill_layer20 | gemm | 42 | 1,246.2 | 0.06 % |
| mir_operator:prefill_layer08 | gemm | 42 | 1,239.8 | 0.06 % |
| mir_operator:prefill_layer06 | gemm | 42 | 1,238.8 | 0.06 % |
| mir_operator:prefill_layer10 | gemm | 42 | 1,233.9 | 0.06 % |
| mir_operator:prefill_layer02 | gemm | 42 | 1,233.6 | 0.06 % |
| mir_operator:prefill_layer18 | gemm | 42 | 1,233.4 | 0.06 % |
| mir_operator:prefill_layer09 | gemm | 42 | 1,229.0 | 0.06 % |
| mir_operator:prefill_layer23 | gemm | 42 | 1,229.0 | 0.06 % |
| mir_operator:prefill_layer16 | gemm | 42 | 1,229.0 | 0.06 % |
| mir_operator:prefill_layer21 | gemm | 42 | 1,228.6 | 0.06 % |
| mir_operator:prefill_layer22 | gemm | 42 | 1,227.7 | 0.06 % |
| mir_operator:prefill_layer04 | gemm | 42 | 1,227.0 | 0.06 % |
| mir_operator:prefill_layer24 | gemm | 42 | 1,226.6 | 0.06 % |
| mir_operator:prefill_layer15 | gemm | 42 | 1,226.1 | 0.06 % |
| mir_operator:prefill_layer17 | gemm | 42 | 1,225.9 | 0.06 % |
| mir_operator:prefill_layer14 | gemm | 42 | 1,224.8 | 0.06 % |
| mir_operator:prefill_layer03 | gemm | 42 | 1,223.6 | 0.06 % |
| mir_operator:prefill_layer05 | gemm | 42 | 1,222.5 | 0.06 % |
| mir_operator:prefill_layer11 | gemm | 42 | 1,221.1 | 0.06 % |
| inter_operator_dispatch | copy | 1008 | 1,144.7 | 0.05 % |
| mir_operator:decode_head | copy | 660 | 1,064.0 | 0.05 % |
| mir_operator:decode_head | elementwise_unary | 660 | 730.9 | 0.03 % |
| inter_operator_dispatch | elementwise_binary | 672 | 724.1 | 0.03 % |
| mir_operator:decode_head | reduce | 330 | 707.7 | 0.03 % |
| mir_operator:decode_embed | other | 330 | 627.4 | 0.03 % |
| inter_operator_dispatch | concat | 336 | 518.5 | 0.02 % |
| inter_operator_dispatch | gemv | 336 | 410.4 | 0.02 % |
| mir_operator:decode_sample | memcpy | 330 | 340.3 | 0.02 % |
| mir_operator:prefill_layer00 | elementwise_binary | 102 | 309.8 | 0.01 % |
| mir_operator:prefill_layer27 | elementwise_binary | 102 | 293.7 | 0.01 % |
| mir_operator:prefill_layer19 | elementwise_binary | 102 | 285.1 | 0.01 % |
| mir_operator:prefill_layer13 | elementwise_binary | 102 | 269.1 | 0.01 % |
| mir_operator:prefill_layer06 | elementwise_binary | 102 | 258.7 | 0.01 % |
| mir_operator:prefill_layer01 | elementwise_binary | 102 | 243.0 | 0.01 % |
| mir_operator:prefill_layer18 | elementwise_binary | 102 | 233.7 | 0.01 % |
| mir_operator:prefill_layer10 | elementwise_binary | 102 | 230.3 | 0.01 % |
| mir_operator:prefill_layer09 | elementwise_binary | 102 | 218.3 | 0.01 % |
| mir_operator:prefill_layer08 | elementwise_binary | 102 | 218.2 | 0.01 % |
| mir_operator:prefill_layer12 | elementwise_binary | 102 | 218.2 | 0.01 % |
| mir_operator:prefill_layer16 | elementwise_binary | 102 | 218.0 | 0.01 % |
| mir_operator:prefill_layer04 | elementwise_binary | 102 | 217.8 | 0.01 % |
| mir_operator:prefill_layer07 | elementwise_binary | 102 | 217.8 | 0.01 % |
| mir_operator:prefill_layer25 | elementwise_binary | 102 | 217.7 | 0.01 % |
| mir_operator:prefill_layer14 | elementwise_binary | 102 | 217.7 | 0.01 % |
| mir_operator:prefill_layer20 | elementwise_binary | 102 | 217.7 | 0.01 % |
| mir_operator:prefill_layer17 | elementwise_binary | 102 | 217.6 | 0.01 % |
| mir_operator:prefill_layer02 | elementwise_binary | 102 | 217.6 | 0.01 % |
| mir_operator:prefill_layer21 | elementwise_binary | 102 | 217.5 | 0.01 % |
| mir_operator:prefill_layer22 | elementwise_binary | 102 | 217.4 | 0.01 % |
| mir_operator:prefill_layer11 | elementwise_binary | 102 | 217.4 | 0.01 % |
| mir_operator:prefill_layer03 | elementwise_binary | 102 | 217.3 | 0.01 % |
| mir_operator:prefill_layer23 | elementwise_binary | 102 | 217.3 | 0.01 % |
| mir_operator:prefill_layer24 | elementwise_binary | 102 | 217.2 | 0.01 % |
| mir_operator:prefill_layer26 | elementwise_binary | 102 | 217.1 | 0.01 % |
| mir_operator:prefill_layer05 | elementwise_binary | 102 | 217.0 | 0.01 % |
| mir_operator:prefill_layer15 | elementwise_binary | 102 | 216.7 | 0.01 % |
| mir_operator:prefill_layer00 | reduce | 39 | 172.6 | 0.01 % |
| mir_operator:prefill_layer06 | reduce | 39 | 145.4 | 0.01 % |
| mir_operator:prefill_layer00 | copy | 48 | 143.7 | 0.01 % |
| mir_operator:prefill_layer27 | reduce | 39 | 134.8 | 0.01 % |
| inter_operator_dispatch | memcpy | 330 | 133.0 | 0.01 % |
| mir_operator:prefill_layer13 | reduce | 39 | 132.8 | 0.01 % |
| mir_operator:prefill_layer06 | copy | 48 | 127.9 | 0.01 % |
| mir_operator:prefill_layer27 | copy | 48 | 124.8 | 0.01 % |
| mir_operator:prefill_layer00 | elementwise_other | 42 | 121.6 | 0.01 % |
| mir_operator:decode_sample | memset | 330 | 121.0 | 0.01 % |
| mir_operator:prefill_layer20 | reduce | 39 | 118.5 | 0.01 % |
| mir_operator:prefill_layer12 | reduce | 39 | 118.5 | 0.01 % |
| mir_operator:prefill_layer26 | reduce | 39 | 118.4 | 0.01 % |
| mir_operator:prefill_layer14 | reduce | 39 | 118.3 | 0.01 % |
| mir_operator:prefill_layer16 | reduce | 39 | 118.3 | 0.01 % |
| mir_operator:prefill_layer18 | reduce | 39 | 118.3 | 0.01 % |
| mir_operator:prefill_layer02 | reduce | 39 | 118.2 | 0.01 % |
| mir_operator:prefill_layer08 | reduce | 39 | 118.2 | 0.01 % |
| mir_operator:prefill_layer10 | reduce | 39 | 118.1 | 0.01 % |
| mir_operator:prefill_layer07 | reduce | 39 | 118.1 | 0.01 % |
| mir_operator:prefill_layer22 | reduce | 39 | 118.0 | 0.01 % |
| mir_operator:prefill_layer24 | reduce | 39 | 118.0 | 0.01 % |
| mir_operator:prefill_layer25 | reduce | 39 | 118.0 | 0.01 % |
| mir_operator:prefill_layer04 | reduce | 39 | 118.0 | 0.01 % |
| mir_operator:prefill_layer11 | reduce | 39 | 118.0 | 0.01 % |
| mir_operator:prefill_layer17 | reduce | 39 | 118.0 | 0.01 % |
| mir_operator:prefill_layer03 | reduce | 39 | 117.9 | 0.01 % |
| mir_operator:prefill_layer21 | reduce | 39 | 117.8 | 0.01 % |
| mir_operator:prefill_layer01 | reduce | 39 | 117.8 | 0.01 % |
| mir_operator:prefill_layer23 | reduce | 39 | 117.7 | 0.01 % |
| mir_operator:prefill_layer09 | reduce | 39 | 117.5 | 0.01 % |
| mir_operator:prefill_layer15 | reduce | 39 | 117.5 | 0.01 % |
| mir_operator:prefill_layer05 | reduce | 39 | 117.5 | 0.01 % |
| mir_operator:prefill_layer19 | reduce | 39 | 117.4 | 0.01 % |
| mir_operator:prefill_layer00 | concat | 24 | 116.6 | 0.01 % |
| mir_operator:prefill_layer25 | elementwise_other | 42 | 114.6 | 0.01 % |
| mir_operator:prefill_layer01 | copy | 48 | 108.6 | 0.0 % |
| mir_operator:prefill_layer18 | copy | 48 | 108.5 | 0.0 % |
| mir_operator:prefill_layer13 | copy | 48 | 107.6 | 0.0 % |
| mir_operator:prefill_layer06 | elementwise_unary | 48 | 104.9 | 0.0 % |
| mir_operator:prefill_layer00 | elementwise_unary | 48 | 102.8 | 0.0 % |
| mir_operator:prefill_layer19 | copy | 48 | 99.9 | 0.0 % |
| mir_operator:prefill_layer07 | elementwise_other | 42 | 98.2 | 0.0 % |
| mir_operator:prefill_layer23 | copy | 48 | 94.0 | 0.0 % |
| mir_operator:prefill_layer24 | copy | 48 | 94.0 | 0.0 % |
| mir_operator:prefill_layer07 | copy | 48 | 94.0 | 0.0 % |
| mir_operator:prefill_layer04 | copy | 48 | 94.0 | 0.0 % |
| mir_operator:prefill_layer17 | copy | 48 | 94.0 | 0.0 % |
| mir_operator:prefill_layer20 | copy | 48 | 94.0 | 0.0 % |
| mir_operator:prefill_layer08 | copy | 48 | 94.0 | 0.0 % |
| mir_operator:prefill_layer14 | copy | 48 | 94.0 | 0.0 % |
| mir_operator:prefill_layer21 | copy | 48 | 93.9 | 0.0 % |
| mir_operator:prefill_layer09 | copy | 48 | 93.9 | 0.0 % |
| mir_operator:prefill_layer10 | copy | 48 | 93.9 | 0.0 % |
| mir_operator:prefill_layer11 | copy | 48 | 93.9 | 0.0 % |
| mir_operator:prefill_layer25 | copy | 48 | 93.9 | 0.0 % |
| mir_operator:prefill_layer05 | copy | 48 | 93.8 | 0.0 % |
| mir_operator:prefill_layer15 | copy | 48 | 93.7 | 0.0 % |
| mir_operator:prefill_layer03 | copy | 48 | 93.7 | 0.0 % |
| mir_operator:prefill_layer26 | copy | 48 | 93.6 | 0.0 % |
| mir_operator:prefill_layer22 | copy | 48 | 93.6 | 0.0 % |
| mir_operator:prefill_layer02 | copy | 48 | 93.6 | 0.0 % |
| mir_operator:prefill_layer16 | copy | 48 | 93.5 | 0.0 % |
| mir_operator:prefill_layer12 | copy | 48 | 93.4 | 0.0 % |
| mir_operator:prefill_layer10 | elementwise_other | 42 | 91.3 | 0.0 % |
| mir_operator:prefill_layer17 | elementwise_other | 42 | 89.7 | 0.0 % |
| mir_operator:prefill_layer02 | elementwise_other | 42 | 89.7 | 0.0 % |
| mir_operator:prefill_layer13 | elementwise_other | 42 | 89.6 | 0.0 % |
| mir_operator:prefill_layer21 | elementwise_other | 42 | 89.6 | 0.0 % |
| mir_operator:prefill_layer23 | elementwise_other | 42 | 89.5 | 0.0 % |
| mir_operator:prefill_layer08 | elementwise_other | 42 | 89.4 | 0.0 % |
| mir_operator:prefill_layer22 | elementwise_other | 42 | 89.4 | 0.0 % |
| mir_operator:prefill_layer06 | elementwise_other | 42 | 89.4 | 0.0 % |
| mir_operator:prefill_layer04 | elementwise_other | 42 | 89.3 | 0.0 % |
| mir_operator:prefill_layer11 | elementwise_other | 42 | 89.3 | 0.0 % |
| mir_operator:prefill_layer18 | elementwise_other | 42 | 89.3 | 0.0 % |
| mir_operator:prefill_layer27 | elementwise_other | 42 | 89.3 | 0.0 % |
| mir_operator:prefill_layer12 | elementwise_other | 42 | 89.3 | 0.0 % |
| mir_operator:prefill_layer05 | elementwise_other | 42 | 89.3 | 0.0 % |
| mir_operator:prefill_layer14 | elementwise_other | 42 | 89.3 | 0.0 % |
| mir_operator:prefill_layer24 | elementwise_other | 42 | 89.3 | 0.0 % |
| mir_operator:prefill_layer26 | elementwise_other | 42 | 89.3 | 0.0 % |
| mir_operator:prefill_layer15 | elementwise_other | 42 | 89.2 | 0.0 % |
| mir_operator:prefill_layer03 | elementwise_other | 42 | 89.2 | 0.0 % |
| mir_operator:prefill_layer19 | elementwise_other | 42 | 89.1 | 0.0 % |
| mir_operator:prefill_layer01 | elementwise_other | 42 | 89.1 | 0.0 % |
| mir_operator:prefill_layer16 | elementwise_other | 42 | 89.0 | 0.0 % |
| mir_operator:prefill_layer20 | elementwise_other | 42 | 89.0 | 0.0 % |
| mir_operator:prefill_layer09 | elementwise_other | 42 | 88.7 | 0.0 % |
| mir_operator:prefill_layer25 | concat | 24 | 83.8 | 0.0 % |
| mir_operator:prefill_layer03 | concat | 24 | 83.8 | 0.0 % |
| mir_operator:prefill_layer24 | concat | 24 | 83.8 | 0.0 % |
| mir_operator:prefill_layer11 | concat | 24 | 83.7 | 0.0 % |
| mir_operator:prefill_layer27 | concat | 24 | 83.7 | 0.0 % |
| mir_operator:prefill_layer15 | concat | 24 | 83.7 | 0.0 % |
| mir_operator:prefill_layer17 | concat | 24 | 83.7 | 0.0 % |
| mir_operator:prefill_layer19 | concat | 24 | 83.7 | 0.0 % |
| mir_operator:prefill_layer16 | concat | 24 | 83.6 | 0.0 % |
| mir_operator:prefill_layer10 | concat | 24 | 83.6 | 0.0 % |
| mir_operator:prefill_layer26 | concat | 24 | 83.6 | 0.0 % |
| mir_operator:prefill_layer01 | concat | 24 | 83.6 | 0.0 % |
| mir_operator:prefill_layer13 | concat | 24 | 83.6 | 0.0 % |
| mir_operator:prefill_layer18 | concat | 24 | 83.6 | 0.0 % |
| mir_operator:prefill_layer23 | concat | 24 | 83.6 | 0.0 % |
| mir_operator:prefill_layer08 | concat | 24 | 83.6 | 0.0 % |
| mir_operator:prefill_layer20 | concat | 24 | 83.6 | 0.0 % |
| mir_operator:prefill_layer04 | concat | 24 | 83.5 | 0.0 % |
| mir_operator:prefill_layer12 | concat | 24 | 83.5 | 0.0 % |
| mir_operator:prefill_layer14 | concat | 24 | 83.5 | 0.0 % |
| mir_operator:prefill_layer21 | concat | 24 | 83.5 | 0.0 % |
| mir_operator:prefill_layer22 | concat | 24 | 83.5 | 0.0 % |
| mir_operator:prefill_layer09 | concat | 24 | 83.5 | 0.0 % |
| mir_operator:prefill_layer06 | concat | 24 | 83.5 | 0.0 % |
| mir_operator:prefill_layer02 | concat | 24 | 83.5 | 0.0 % |
| mir_operator:prefill_layer05 | concat | 24 | 83.5 | 0.0 % |
| mir_operator:prefill_layer07 | concat | 24 | 83.4 | 0.0 % |
| mir_operator:prefill_layer27 | attention | 12 | 77.4 | 0.0 % |
| mir_operator:prefill_layer13 | elementwise_unary | 48 | 77.1 | 0.0 % |
| mir_operator:prefill_layer09 | attention | 12 | 77.0 | 0.0 % |
| mir_operator:prefill_layer00 | attention | 12 | 77.0 | 0.0 % |
| mir_operator:prefill_layer13 | attention | 12 | 76.9 | 0.0 % |
| mir_operator:prefill_layer07 | attention | 12 | 76.9 | 0.0 % |
| mir_operator:prefill_layer25 | attention | 12 | 76.9 | 0.0 % |
| mir_operator:prefill_layer23 | attention | 12 | 76.8 | 0.0 % |
| mir_operator:prefill_layer08 | attention | 12 | 76.8 | 0.0 % |
| mir_operator:prefill_layer01 | attention | 12 | 76.7 | 0.0 % |
| mir_operator:prefill_layer04 | attention | 12 | 76.7 | 0.0 % |
| mir_operator:prefill_layer05 | attention | 12 | 76.7 | 0.0 % |
| mir_operator:prefill_layer26 | attention | 12 | 76.7 | 0.0 % |
| mir_operator:prefill_layer02 | attention | 12 | 76.7 | 0.0 % |
| mir_operator:prefill_layer03 | attention | 12 | 76.7 | 0.0 % |
| mir_operator:prefill_layer15 | attention | 12 | 76.7 | 0.0 % |
| mir_operator:prefill_layer17 | attention | 12 | 76.6 | 0.0 % |
| mir_operator:prefill_layer21 | attention | 12 | 76.6 | 0.0 % |
| mir_operator:prefill_layer16 | attention | 12 | 76.6 | 0.0 % |
| mir_operator:prefill_layer19 | attention | 12 | 76.6 | 0.0 % |
| mir_operator:prefill_layer06 | attention | 12 | 76.5 | 0.0 % |
| mir_operator:prefill_layer24 | attention | 12 | 76.5 | 0.0 % |
| mir_operator:prefill_layer11 | attention | 12 | 76.4 | 0.0 % |
| mir_operator:prefill_layer18 | attention | 12 | 76.4 | 0.0 % |
| mir_operator:prefill_layer14 | attention | 12 | 76.4 | 0.0 % |
| mir_operator:prefill_layer10 | attention | 12 | 76.4 | 0.0 % |
| mir_operator:prefill_layer12 | attention | 12 | 76.4 | 0.0 % |
| mir_operator:prefill_layer22 | attention | 12 | 76.3 | 0.0 % |
| mir_operator:prefill_layer20 | attention | 12 | 76.2 | 0.0 % |
| mir_operator:prefill_layer19 | elementwise_unary | 48 | 76.0 | 0.0 % |
| mir_operator:prefill_layer27 | elementwise_unary | 48 | 74.9 | 0.0 % |
| mir_operator:prefill_layer02 | elementwise_unary | 48 | 67.0 | 0.0 % |
| mir_operator:prefill_layer09 | elementwise_unary | 48 | 66.9 | 0.0 % |
| mir_operator:prefill_layer14 | elementwise_unary | 48 | 66.9 | 0.0 % |
| mir_operator:prefill_layer18 | elementwise_unary | 48 | 66.9 | 0.0 % |
| mir_operator:prefill_layer23 | elementwise_unary | 48 | 66.9 | 0.0 % |
| mir_operator:prefill_layer20 | elementwise_unary | 48 | 66.9 | 0.0 % |
| mir_operator:prefill_layer26 | elementwise_unary | 48 | 66.9 | 0.0 % |
| mir_operator:prefill_layer07 | elementwise_unary | 48 | 66.9 | 0.0 % |
| mir_operator:prefill_layer10 | elementwise_unary | 48 | 66.9 | 0.0 % |
| mir_operator:prefill_layer16 | elementwise_unary | 48 | 66.9 | 0.0 % |
| mir_operator:prefill_layer12 | elementwise_unary | 48 | 66.8 | 0.0 % |
| mir_operator:prefill_layer25 | elementwise_unary | 48 | 66.8 | 0.0 % |
| mir_operator:prefill_layer01 | elementwise_unary | 48 | 66.8 | 0.0 % |
| mir_operator:prefill_layer11 | elementwise_unary | 48 | 66.8 | 0.0 % |
| mir_operator:prefill_layer15 | elementwise_unary | 48 | 66.8 | 0.0 % |
| mir_operator:prefill_layer22 | elementwise_unary | 48 | 66.7 | 0.0 % |
| mir_operator:prefill_layer24 | elementwise_unary | 48 | 66.7 | 0.0 % |
| mir_operator:prefill_layer08 | elementwise_unary | 48 | 66.7 | 0.0 % |
| mir_operator:prefill_layer05 | elementwise_unary | 48 | 66.7 | 0.0 % |
| mir_operator:prefill_layer03 | elementwise_unary | 48 | 66.7 | 0.0 % |
| mir_operator:prefill_layer21 | elementwise_unary | 48 | 66.6 | 0.0 % |
| mir_operator:prefill_layer04 | elementwise_unary | 48 | 66.6 | 0.0 % |
| mir_operator:prefill_layer17 | elementwise_unary | 48 | 66.6 | 0.0 % |
| mir_operator:prefill_sample | reduce | 6 | 40.4 | 0.0 % |
| mir_operator:prefill_head | elementwise_binary | 18 | 39.0 | 0.0 % |
| mir_operator:prefill_head | reduce | 6 | 27.6 | 0.0 % |
| mir_operator:prefill_head | copy | 12 | 25.0 | 0.0 % |
| mir_operator:prefill_layer25 | memset | 6 | 22.0 | 0.0 % |
| mir_operator:prefill_head | elementwise_unary | 12 | 17.4 | 0.0 % |
| mir_operator:prefill_embed | other | 6 | 10.5 | 0.0 % |
| mir_operator:prefill_sample | memcpy | 6 | 7.6 | 0.0 % |
| mir_operator:prefill_layer12 | memset | 6 | 5.4 | 0.0 % |
| mir_operator:prefill_layer26 | memset | 6 | 5.3 | 0.0 % |
| d2h_stage | memcpy | 6 | 5.2 | 0.0 % |
| pre_d2h_alloc | memcpy | 12 | 4.4 | 0.0 % |
| mir_operator:prefill_layer08 | memset | 6 | 3.8 | 0.0 % |
| mir_operator:prefill_layer22 | memset | 6 | 3.6 | 0.0 % |
| mir_operator:prefill_layer20 | memset | 6 | 3.5 | 0.0 % |
| mir_operator:prefill_layer27 | memset | 6 | 3.4 | 0.0 % |
| mir_operator:prefill_layer06 | memset | 6 | 3.2 | 0.0 % |
| mir_operator:prefill_layer02 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer11 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer18 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer21 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer00 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer01 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer03 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer04 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer07 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer13 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer16 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer19 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer23 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer05 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer09 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer14 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer17 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer24 | memset | 6 | 3.1 | 0.0 % |
| mir_operator:prefill_layer10 | memset | 6 | 3.0 | 0.0 % |
| mir_operator:prefill_layer15 | memset | 6 | 3.0 | 0.0 % |
| h2d_stage | memcpy | 6 | 2.4 | 0.0 % |
| mir_operator:prefill_sample | memset | 6 | 2.2 | 0.0 % |

## Kernel launch order, representative iteration 2 (G03)

| # | call | process | kind | family | GPU (us) | launch latency (us) | grid | block |
|---:|---|---|---|---|---:|---:|---|---|
| 1 | plan | h2d_stage | memcpy | memcpy | 0.4 | 12.5 | 0x0x0 | 0x0x0 |
| 2 | plan | mir_operator:prefill_embed:0 | kernel | other | 1.9 | 18.0 | 192x1x1 | 256x1x1 |
| 3 | plan | inter_operator_dispatch | kernel | elementwise_other | 0.9 | 7.6 | 3x1x1 | 64x1x1 |
| 4 | plan | inter_operator_dispatch | kernel | copy | 1.5 | 8.3 | 1x1x1 | 128x1x1 |
| 5 | plan | inter_operator_dispatch | kernel | gemv | 1.3 | 9.2 | 6x2x1 | 256x1x1 |
| 6 | plan | inter_operator_dispatch | kernel | concat | 2.6 | 7.8 | 256x2x1 | 512x1x1 |
| 7 | plan | inter_operator_dispatch | kernel | elementwise_other | 1.7 | 6.4 | 24x1x1 | 128x1x1 |
| 8 | plan | inter_operator_dispatch | kernel | elementwise_binary | 1.1 | 5.3 | 24x1x1 | 128x1x1 |
| 9 | plan | inter_operator_dispatch | kernel | elementwise_other | 1.6 | 6.6 | 24x1x1 | 128x1x1 |
| 10 | plan | inter_operator_dispatch | kernel | elementwise_binary | 1.1 | 4.9 | 24x1x1 | 128x1x1 |
| 11 | plan | inter_operator_dispatch | kernel | copy | 1.1 | 5.4 | 24x1x1 | 128x1x1 |
| 12 | plan | inter_operator_dispatch | kernel | copy | 1.1 | 5.4 | 24x1x1 | 128x1x1 |
| 13 | plan | mir_operator:prefill_layer00:1 | kernel | copy | 2.5 | 8.4 | 768x1x1 | 128x1x1 |
| 14 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_unary | 1.7 | 5.7 | 384x1x1 | 128x1x1 |
| 15 | plan | mir_operator:prefill_layer00:1 | kernel | reduce | 4.5 | 5.7 | 12x1x1 | 32x16x1 |
| 16 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 1.1 | 16.5 | 1x1x1 | 128x1x1 |
| 17 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_unary | 1.2 | 18.3 | 1x1x1 | 128x1x1 |
| 18 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.5 | 9.5 | 1536x1x1 | 128x1x1 |
| 19 | plan | mir_operator:prefill_layer00:1 | kernel | copy | 1.5 | 7.4 | 384x1x1 | 128x1x1 |
| 20 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.4 | 9.6 | 768x1x1 | 128x1x1 |
| 21 | plan | mir_operator:prefill_layer00:1 | kernel | gemm | 16.9 | 21.7 | 32x3x1 | 128x1x1 |
| 22 | plan | mir_operator:prefill_layer00:1 | kernel | copy | 18.0 | 13.9 | 768x1x1 | 128x1x1 |
| 23 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_unary | 10.2 | 14.4 | 384x1x1 | 128x1x1 |
| 24 | plan | mir_operator:prefill_layer00:1 | kernel | reduce | 17.5 | 9.5 | 192x1x1 | 32x16x1 |
| 25 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 20.0 | 8.1 | 3x1x1 | 128x1x1 |
| 26 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_unary | 6.6 | 15.0 | 3x1x1 | 128x1x1 |
| 27 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 20.3 | 8.5 | 1536x1x1 | 128x1x1 |
| 28 | plan | mir_operator:prefill_layer00:1 | kernel | copy | 15.1 | 11.0 | 384x1x1 | 128x1x1 |
| 29 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 25.5 | 13.2 | 768x1x1 | 128x1x1 |
| 30 | plan | mir_operator:prefill_layer00:1 | kernel | gemm | 10.7 | 117.9 | 24x1x5 | 128x1x1 |
| 31 | plan | mir_operator:prefill_layer00:1 | kernel | reduce | 2.0 | 117.3 | 32x12x1 | 32x16x1 |
| 32 | plan | mir_operator:prefill_layer00:1 | kernel | copy | 2.3 | 81.1 | 384x1x1 | 128x1x1 |
| 33 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_unary | 1.3 | 67.3 | 192x1x1 | 128x1x1 |
| 34 | plan | mir_operator:prefill_layer00:1 | kernel | reduce | 2.5 | 51.4 | 96x1x1 | 32x16x1 |
| 35 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 1.1 | 36.4 | 2x1x1 | 128x1x1 |
| 36 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_unary | 1.2 | 25.3 | 2x1x1 | 128x1x1 |
| 37 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.0 | 13.8 | 768x1x1 | 128x1x1 |
| 38 | plan | mir_operator:prefill_layer00:1 | kernel | copy | 1.3 | 4.9 | 192x1x1 | 128x1x1 |
| 39 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.1 | 4.9 | 384x1x1 | 128x1x1 |
| 40 | plan | mir_operator:prefill_layer00:1 | kernel | gemm | 10.0 | 6.1 | 24x1x5 | 128x1x1 |
| 41 | plan | mir_operator:prefill_layer00:1 | kernel | reduce | 1.9 | 9.9 | 32x12x1 | 32x16x1 |
| 42 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.3 | 5.6 | 768x1x1 | 128x1x1 |
| 43 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_other | 2.0 | 5.3 | 384x1x1 | 128x1x1 |
| 44 | plan | mir_operator:prefill_layer00:1 | kernel | concat | 3.8 | 5.8 | 256x2x1 | 512x1x1 |
| 45 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.3 | 5.0 | 768x1x1 | 128x1x1 |
| 46 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_other | 2.4 | 6.3 | 768x1x1 | 128x1x1 |
| 47 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.0 | 5.2 | 384x1x1 | 128x1x1 |
| 48 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_other | 1.9 | 5.3 | 192x1x1 | 128x1x1 |
| 49 | plan | mir_operator:prefill_layer00:1 | kernel | concat | 2.8 | 6.3 | 256x2x1 | 512x1x1 |
| 50 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_binary | 2.0 | 5.3 | 384x1x1 | 128x1x1 |
| 51 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_other | 2.0 | 5.2 | 384x1x1 | 128x1x1 |
| 52 | plan | mir_operator:prefill_layer00:1 | kernel | concat | 3.4 | 6.9 | 256x2x1 | 512x1x1 |
| 53 | plan | mir_operator:prefill_layer00:1 | kernel | concat | 3.3 | 5.5 | 256x2x1 | 512x1x1 |
| 54 | plan | mir_operator:prefill_layer00:1 | kernel | attention | 8.8 | 9.3 | 3x2x16 | 128x1x1 |
| 55 | plan | mir_operator:prefill_layer00:1 | kernel | attention | 3.8 | 6.5 | 768x1x1 | 128x1x1 |
| 56 | plan | mir_operator:prefill_layer00:1 | kernel | gemm | 17.0 | 8.2 | 32x3x1 | 128x1x1 |
| 57 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_other | 1.5 | 7.0 | 384x1x1 | 128x1x1 |
| 58 | plan | mir_operator:prefill_layer00:1 | kernel | copy | 2.5 | 5.9 | 768x1x1 | 128x1x1 |
| 59 | plan | mir_operator:prefill_layer00:1 | kernel | elementwise_unary | 1.7 | 5.3 | 384x1x1 | 128x1x1 |
| 60 | plan | mir_operator:prefill_layer00:1 | kernel | reduce | 4.5 | 5.9 | 12x1x1 | 32x16x1 |
| … | | 181582 more rows in kernel_launch_order_representative_iteration.csv | | | | | | |

## Per call/process summary (medians over measured iterations)

| call | process | op | host median (us) | host min/max (us) | GPU median (us) | top CUDA API | kernels |
|---|---|---:|---:|---:|---:|---|---:|
| plan | adapter_dispatch |  | 4.7 | 3.9/4.9 | 0.0 |  | 0 |
| plan | token_preprocess_cpu |  | 755.8 | 712.8/1,232.4 | 0.0 |  | 0 |
| plan | host_input_generate |  | 111.2 | 107.1/113.8 | 0.0 | cudaEventQuery | 0 |
| plan | h2d_stage |  | 106.0 | 105.7/118.7 | 0.4 | cudaMemcpyAsync | 0 |
| plan | weight_init |  | 163.0 | 144.3/178.7 | 0.0 | cudaEventDestroy | 0 |
| plan | mir_operator:prefill_embed | 0 | 97.1 | 94.9/102.5 | 1.7 | cudaLaunchKernel | 1 |
| plan | inter_operator_dispatch |  | 20.4 | 17.0/2,596.5 | 0.0 | cudaLaunchKernel | 0.32 |
| plan | mir_operator:prefill_layer00 | 1 | 1,479.3 | 1,374.9/1,508.2 | 433.3 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer01 | 2 | 1,313.3 | 1,261.8/1,358.1 | 314.2 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer02 | 3 | 1,292.8 | 1,270.2/1,336.4 | 314.5 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer03 | 4 | 1,329.3 | 1,322.4/1,361.8 | 315.1 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer04 | 5 | 1,294.2 | 1,291.9/1,318.5 | 313.6 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer05 | 6 | 1,321.9 | 1,286.0/1,322.3 | 313.6 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer06 | 7 | 1,274.4 | 1,257.3/1,342.6 | 312.8 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer07 | 8 | 1,269.4 | 1,195.3/1,325.2 | 312.7 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer08 | 9 | 1,286.9 | 1,175.2/1,314.3 | 315.0 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer09 | 10 | 1,324.3 | 1,179.9/1,358.7 | 316.0 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer10 | 11 | 1,326.3 | 1,177.6/1,404.9 | 315.5 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer11 | 12 | 1,281.6 | 1,188.0/1,323.9 | 313.8 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer12 | 13 | 1,285.2 | 1,195.3/1,286.6 | 314.7 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer13 | 14 | 1,247.8 | 1,193.2/1,267.7 | 318.9 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer14 | 15 | 1,208.1 | 1,205.4/1,219.6 | 313.6 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer15 | 16 | 1,206.4 | 1,200.5/1,219.8 | 314.0 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer16 | 17 | 1,207.1 | 1,200.7/1,213.1 | 314.6 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer17 | 18 | 1,233.5 | 1,202.5/1,255.8 | 312.6 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer18 | 19 | 1,224.0 | 1,183.0/1,268.8 | 314.7 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer19 | 20 | 1,221.9 | 1,178.5/1,225.6 | 313.7 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer20 | 21 | 1,180.4 | 1,174.1/1,213.4 | 314.9 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer21 | 22 | 1,200.3 | 1,165.6/1,204.4 | 315.5 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer22 | 23 | 1,188.4 | 1,175.9/1,198.1 | 314.5 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer23 | 24 | 1,181.4 | 1,143.1/1,186.3 | 313.4 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer24 | 25 | 1,179.6 | 1,155.3/1,182.3 | 314.1 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer25 | 26 | 1,185.7 | 1,165.2/1,230.6 | 315.0 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer26 | 27 | 1,171.3 | 1,140.1/1,247.2 | 318.5 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_layer27 | 28 | 1,214.3 | 1,198.7/1,215.8 | 428.4 | cudaLaunchKernel | 60 |
| plan | mir_operator:prefill_head | 29 | 248.9 | 231.6/259.3 | 825.2 | cudaLaunchKernel | 9 |
| plan | mir_operator:prefill_sample | 30 | 773.1 | 772.9/776.6 | 8.3 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 31 | 51.0 | 49.4/57.2 | 2.0 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 32 | 1,175.4 | 1,166.2/1,285.2 | 207.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 33 | 1,096.4 | 1,090.0/1,239.7 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 34 | 1,089.4 | 1,072.5/1,220.3 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 35 | 1,079.6 | 1,054.8/1,201.1 | 203.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 36 | 1,075.4 | 1,059.7/1,196.1 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 37 | 1,113.3 | 1,087.7/1,195.7 | 204.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 38 | 1,132.5 | 1,122.4/1,135.2 | 204.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 39 | 1,151.5 | 1,103.4/1,247.8 | 206.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 40 | 1,181.9 | 1,072.8/1,284.2 | 204.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 41 | 1,203.3 | 1,062.1/1,253.7 | 204.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 42 | 1,202.9 | 1,044.6/1,228.7 | 204.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 43 | 1,231.8 | 1,045.2/1,285.7 | 299.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 44 | 1,215.0 | 1,040.6/1,598.9 | 205.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 45 | 1,229.3 | 1,058.5/1,246.6 | 203.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 46 | 1,200.1 | 1,037.3/1,243.9 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 47 | 1,203.8 | 1,038.7/1,206.9 | 204.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 48 | 1,180.5 | 1,037.2/1,201.2 | 204.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 49 | 1,166.3 | 1,034.5/1,203.9 | 204.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 50 | 1,208.4 | 1,046.5/1,244.5 | 204.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 51 | 1,203.5 | 1,058.3/1,223.3 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 52 | 1,195.9 | 1,042.5/1,206.3 | 203.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 53 | 1,203.4 | 1,046.3/1,255.6 | 204.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 54 | 1,231.4 | 1,050.1/1,236.9 | 204.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 55 | 1,211.7 | 1,051.5/1,225.7 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 56 | 1,200.7 | 1,097.7/1,216.3 | 203.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 57 | 1,200.3 | 1,131.1/1,220.5 | 203.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 58 | 1,160.0 | 1,117.6/1,197.8 | 204.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 59 | 1,158.0 | 1,128.7/1,184.4 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 60 | 234.5 | 229.3/236.7 | 651.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 61 | 597.8 | 595.2/607.6 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 62 | 52.9 | 45.8/60.6 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 63 | 1,231.6 | 1,155.0/1,290.4 | 204.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 64 | 1,150.5 | 1,143.6/1,280.8 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 65 | 1,196.7 | 1,139.9/1,224.4 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 66 | 1,198.1 | 1,104.8/1,218.4 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 67 | 1,210.0 | 1,114.4/1,221.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 68 | 1,189.4 | 1,095.9/1,209.8 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 69 | 1,189.5 | 1,114.1/1,193.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 70 | 1,169.7 | 1,118.7/1,217.4 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 71 | 1,190.9 | 1,119.0/1,214.6 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 72 | 1,200.9 | 1,192.9/1,242.8 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 73 | 1,196.1 | 1,192.9/1,211.0 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 74 | 1,202.2 | 1,178.2/1,220.9 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 75 | 1,188.8 | 1,158.6/1,208.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 76 | 1,179.4 | 1,169.8/1,210.0 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 77 | 1,169.1 | 1,160.4/1,200.3 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 78 | 1,168.1 | 1,127.4/1,202.2 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 79 | 1,167.8 | 1,076.1/1,231.1 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 80 | 1,161.9 | 1,070.1/1,266.3 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 81 | 1,211.7 | 1,063.6/1,221.4 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 82 | 1,172.4 | 1,038.4/1,212.3 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 83 | 1,112.3 | 1,036.9/1,132.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 84 | 1,080.3 | 1,044.9/1,101.0 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 85 | 1,107.5 | 1,079.4/1,164.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 86 | 1,115.0 | 1,108.0/1,145.8 | 273.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 87 | 1,130.1 | 1,118.2/1,175.0 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 88 | 1,156.0 | 1,136.9/1,175.9 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 89 | 1,125.4 | 1,118.7/1,164.2 | 203.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 90 | 1,122.4 | 1,095.4/1,158.4 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 91 | 233.1 | 216.4/239.6 | 662.4 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 92 | 620.4 | 614.5/624.6 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 93 | 55.9 | 49.5/57.5 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 94 | 1,194.2 | 1,187.9/1,275.9 | 204.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 95 | 1,130.1 | 1,130.1/1,209.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 96 | 1,170.0 | 1,095.8/1,220.9 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 97 | 1,164.5 | 1,087.4/1,221.5 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 98 | 1,178.3 | 1,100.3/1,213.9 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 99 | 1,158.2 | 1,111.5/1,197.0 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 100 | 1,192.6 | 1,069.3/1,210.9 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 101 | 1,182.2 | 1,050.2/1,195.2 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 102 | 1,164.8 | 1,053.6/1,199.4 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 103 | 1,151.6 | 1,059.6/1,193.8 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 104 | 1,166.4 | 1,062.5/1,202.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 105 | 1,172.9 | 1,050.9/1,196.4 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 106 | 1,178.8 | 1,053.1/1,224.0 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 107 | 1,176.9 | 1,057.3/1,202.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 108 | 1,198.8 | 1,087.9/1,206.2 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 109 | 1,193.0 | 1,064.2/1,236.0 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 110 | 1,180.1 | 1,050.4/1,203.3 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 111 | 1,174.0 | 1,051.7/1,175.9 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 112 | 1,167.2 | 1,064.3/1,178.2 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 113 | 1,208.2 | 1,076.7/1,210.6 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 114 | 1,197.2 | 1,081.3/1,232.7 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 115 | 1,197.0 | 1,078.9/1,213.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 116 | 1,202.5 | 1,081.6/1,213.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 117 | 1,208.7 | 1,112.7/1,227.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 118 | 1,203.0 | 1,064.0/1,209.2 | 283.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 119 | 1,196.9 | 1,045.9/1,226.8 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 120 | 1,198.0 | 1,085.8/1,201.4 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 121 | 1,202.4 | 1,084.9/1,210.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 122 | 232.6 | 214.6/245.1 | 661.4 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 123 | 623.3 | 615.5/623.3 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 124 | 52.6 | 47.5/57.8 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 125 | 1,276.0 | 1,123.0/1,281.3 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 126 | 1,226.6 | 1,145.9/1,256.4 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 127 | 1,197.5 | 1,193.0/1,212.6 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 128 | 1,195.6 | 1,183.2/1,251.9 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 129 | 1,144.5 | 1,122.7/1,213.5 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 130 | 1,108.7 | 1,105.3/1,258.3 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 131 | 1,121.7 | 1,107.2/1,220.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 132 | 1,202.5 | 1,152.2/1,252.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 133 | 1,204.2 | 1,146.5/1,209.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 134 | 1,192.2 | 1,173.0/1,207.7 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 135 | 1,213.9 | 1,212.7/1,229.9 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 136 | 1,205.7 | 1,198.8/1,256.5 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 137 | 1,202.6 | 1,195.4/1,216.2 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 138 | 1,198.0 | 1,194.7/1,209.1 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 139 | 1,213.4 | 1,184.1/1,223.3 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 140 | 1,198.1 | 1,130.6/1,208.9 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 141 | 1,201.4 | 1,076.1/1,210.5 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 142 | 1,201.5 | 1,051.5/1,215.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 143 | 1,195.6 | 1,058.6/1,245.6 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 144 | 1,185.6 | 1,045.4/1,224.9 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 145 | 1,113.2 | 1,038.6/1,124.9 | 201.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 146 | 1,104.2 | 1,037.7/1,125.3 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 147 | 1,098.4 | 1,039.8/1,174.5 | 204.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 148 | 1,138.7 | 1,057.0/1,180.4 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 149 | 1,114.6 | 1,076.5/1,186.9 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 150 | 1,089.4 | 1,089.3/1,168.3 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 151 | 1,108.6 | 1,074.4/1,178.1 | 203.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 152 | 1,189.7 | 1,069.1/1,203.6 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 153 | 223.1 | 214.6/248.9 | 661.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 154 | 620.0 | 604.8/628.5 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 155 | 52.3 | 44.5/55.2 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 156 | 1,239.3 | 1,141.3/1,242.9 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 157 | 1,143.6 | 1,066.7/1,184.9 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 158 | 1,169.9 | 1,051.7/1,215.5 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 159 | 1,172.8 | 1,038.6/1,209.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 160 | 1,202.0 | 1,043.8/1,219.8 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 161 | 1,207.6 | 1,069.0/1,209.8 | 204.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 162 | 1,220.7 | 1,078.6/1,253.0 | 203.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 163 | 1,194.3 | 1,055.4/1,225.7 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 164 | 1,185.4 | 1,063.1/1,223.6 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 165 | 1,174.1 | 1,051.8/1,209.3 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 166 | 1,169.1 | 1,040.8/1,207.7 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 167 | 1,160.7 | 1,040.9/1,204.6 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 168 | 1,168.2 | 1,033.5/1,205.0 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 169 | 1,164.7 | 1,046.3/1,195.6 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 170 | 1,145.6 | 1,057.9/1,218.4 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 171 | 1,059.5 | 1,045.1/1,228.9 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 172 | 1,098.4 | 1,055.8/1,203.7 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 173 | 1,150.9 | 1,060.9/1,198.0 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 174 | 1,106.1 | 1,055.8/1,209.4 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 175 | 1,085.5 | 1,045.7/1,196.5 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 176 | 1,079.2 | 1,069.4/1,195.8 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 177 | 1,150.4 | 1,092.0/1,194.8 | 205.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 178 | 1,159.4 | 1,083.1/1,213.4 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 179 | 1,168.5 | 1,106.1/1,214.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 180 | 1,109.4 | 1,081.7/1,200.5 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 181 | 1,151.4 | 1,074.5/1,194.9 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 182 | 1,166.6 | 1,075.2/1,197.1 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 183 | 1,167.4 | 1,075.9/1,200.0 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 184 | 230.3 | 211.6/232.5 | 663.9 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 185 | 622.7 | 621.6/633.0 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 186 | 49.1 | 47.4/49.9 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 187 | 1,226.8 | 1,099.5/1,282.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 188 | 1,109.2 | 1,060.1/1,250.0 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 189 | 1,133.8 | 1,051.2/1,210.6 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 190 | 1,142.7 | 1,082.4/1,204.5 | 201.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 191 | 1,095.4 | 1,054.8/1,209.9 | 201.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 192 | 1,128.2 | 1,051.5/1,151.6 | 203.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 193 | 1,187.2 | 1,052.3/1,203.3 | 203.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 194 | 1,198.3 | 1,056.9/1,199.8 | 306.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 195 | 1,195.4 | 1,052.0/1,196.0 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 196 | 1,188.7 | 1,043.6/1,204.9 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 197 | 1,200.0 | 1,060.4/1,225.4 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 198 | 1,193.9 | 1,079.2/1,234.1 | 201.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 199 | 1,181.1 | 1,096.0/1,187.2 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 200 | 1,179.6 | 1,082.1/1,198.9 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 201 | 1,178.6 | 1,076.8/1,200.7 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 202 | 1,169.1 | 1,070.0/1,173.0 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 203 | 1,164.6 | 1,052.2/1,171.1 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 204 | 1,167.4 | 1,050.0/1,173.0 | 204.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 205 | 1,177.5 | 1,049.8/1,178.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 206 | 1,170.9 | 1,052.6/1,221.6 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 207 | 1,205.0 | 1,039.8/1,206.2 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 208 | 1,195.8 | 1,042.1/1,201.6 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 209 | 1,194.7 | 1,068.1/1,197.9 | 204.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 210 | 1,176.1 | 1,041.5/1,187.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 211 | 1,163.6 | 1,048.4/1,176.7 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 212 | 1,159.9 | 1,101.2/1,168.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 213 | 1,160.9 | 1,110.5/1,193.3 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 214 | 1,162.5 | 1,099.6/1,205.5 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 215 | 226.4 | 223.8/229.3 | 661.2 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 216 | 618.1 | 613.2/625.0 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 217 | 49.1 | 48.8/50.2 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 218 | 1,208.0 | 1,124.2/1,280.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 219 | 1,168.4 | 1,068.7/1,244.1 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 220 | 1,161.0 | 1,058.8/1,212.0 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 221 | 1,178.6 | 1,088.9/1,212.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 222 | 1,182.9 | 1,177.8/1,202.8 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 223 | 1,212.3 | 1,170.6/1,537.5 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 224 | 1,207.4 | 1,179.7/1,777.8 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 225 | 1,251.2 | 1,205.8/1,295.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 226 | 1,220.8 | 1,213.4/1,268.4 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 227 | 1,214.6 | 1,211.1/1,234.5 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 228 | 1,203.7 | 1,201.9/1,207.0 | 201.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 229 | 1,195.7 | 1,168.1/1,202.3 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 230 | 1,199.2 | 1,123.6/1,207.2 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 231 | 1,195.9 | 1,130.0/1,205.2 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 232 | 1,204.4 | 1,088.8/1,204.6 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 233 | 1,231.3 | 1,192.8/1,514.4 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 234 | 1,114.3 | 1,076.9/1,165.0 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 235 | 1,097.0 | 1,077.6/1,172.5 | 207.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 236 | 1,158.9 | 1,086.8/1,186.6 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 237 | 1,128.3 | 1,091.8/1,212.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 238 | 1,106.4 | 1,100.4/1,203.5 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 239 | 1,102.8 | 1,094.8/1,204.6 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 240 | 1,095.7 | 1,050.9/1,196.2 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 241 | 1,073.3 | 1,071.6/1,164.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 242 | 1,081.6 | 1,070.0/1,239.9 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 243 | 1,075.1 | 1,060.0/1,201.8 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 244 | 1,094.3 | 1,087.7/1,189.7 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 245 | 1,090.6 | 1,041.9/1,164.8 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 246 | 214.4 | 205.0/234.7 | 661.4 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 247 | 620.8 | 608.7/626.4 | 7.3 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 248 | 48.3 | 44.5/56.2 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 249 | 1,146.9 | 1,127.6/1,253.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 250 | 1,085.4 | 1,069.5/1,185.8 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 251 | 1,062.0 | 1,055.9/1,186.9 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 252 | 1,082.1 | 1,056.0/1,210.0 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 253 | 1,176.5 | 1,051.3/1,184.5 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 254 | 1,156.7 | 1,049.6/1,189.3 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 255 | 1,097.5 | 1,049.9/1,223.4 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 256 | 1,117.0 | 1,053.3/1,220.7 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 257 | 1,106.2 | 1,061.9/1,204.7 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 258 | 1,154.3 | 1,100.7/1,201.5 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 259 | 1,165.8 | 1,085.9/1,197.7 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 260 | 1,148.0 | 1,078.5/1,203.5 | 201.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 261 | 1,092.9 | 1,065.0/1,202.1 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 262 | 1,074.6 | 1,062.1/1,191.1 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 263 | 1,066.9 | 1,054.8/1,222.7 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 264 | 1,113.9 | 1,038.9/1,200.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 265 | 1,076.7 | 1,054.4/1,192.2 | 206.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 266 | 1,089.5 | 1,077.7/1,101.1 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 267 | 1,123.6 | 1,105.3/1,124.8 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 268 | 1,104.9 | 1,100.6/1,124.5 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 269 | 1,117.8 | 1,111.2/1,122.4 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 270 | 1,112.8 | 1,106.3/1,120.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 271 | 1,107.6 | 1,098.9/1,112.3 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 272 | 1,102.0 | 1,081.7/1,142.6 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 273 | 1,096.5 | 1,079.5/1,103.5 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 274 | 1,106.2 | 1,086.5/1,131.7 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 275 | 1,081.3 | 1,080.3/1,198.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 276 | 1,091.4 | 1,070.3/1,198.2 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 277 | 217.5 | 202.1/238.8 | 661.2 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 278 | 620.5 | 617.8/626.4 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 279 | 49.9 | 43.6/54.3 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 280 | 1,167.8 | 1,129.1/1,280.5 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 281 | 1,113.4 | 1,065.0/1,218.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 282 | 1,103.3 | 1,061.4/1,241.4 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 283 | 1,117.7 | 1,052.6/1,203.5 | 201.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 284 | 1,115.9 | 1,051.7/1,204.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 285 | 1,124.1 | 1,046.8/1,216.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 286 | 1,139.1 | 1,058.1/1,179.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 287 | 1,126.6 | 1,050.6/1,192.5 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 288 | 1,101.8 | 1,043.1/1,202.0 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 289 | 1,112.1 | 1,058.8/1,207.5 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 290 | 1,098.6 | 1,070.4/1,200.4 | 201.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 291 | 1,127.6 | 1,080.8/1,206.9 | 201.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 292 | 1,111.7 | 1,070.7/1,219.5 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 293 | 1,104.2 | 1,068.2/1,221.8 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 294 | 1,126.2 | 1,071.0/1,209.1 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 295 | 1,205.3 | 1,081.2/1,239.3 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 296 | 1,164.5 | 1,074.1/1,218.3 | 209.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 297 | 1,159.8 | 1,061.9/1,215.4 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 298 | 1,147.1 | 1,071.3/1,200.0 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 299 | 1,125.0 | 1,085.9/1,210.8 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 300 | 1,110.8 | 1,046.2/1,215.5 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 301 | 1,103.8 | 1,047.9/1,225.0 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 302 | 1,104.0 | 1,048.2/1,226.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 303 | 1,101.5 | 1,044.0/1,272.5 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 304 | 1,102.8 | 1,041.9/1,232.1 | 201.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 305 | 1,074.7 | 1,043.2/1,208.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 306 | 1,079.7 | 1,042.4/1,212.4 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 307 | 1,074.3 | 1,049.3/1,210.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 308 | 220.3 | 210.9/252.4 | 661.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 309 | 606.3 | 583.4/636.7 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 310 | 53.6 | 51.3/62.6 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 311 | 1,264.8 | 1,128.5/1,296.8 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 312 | 1,218.5 | 1,086.3/1,285.2 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 313 | 1,223.3 | 1,086.3/1,251.0 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 314 | 1,206.8 | 1,085.8/1,220.0 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 315 | 1,199.8 | 1,077.7/1,207.8 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 316 | 1,195.5 | 1,090.6/1,284.8 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 317 | 1,206.7 | 1,077.9/1,235.9 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 318 | 1,209.2 | 1,092.0/1,238.5 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 319 | 1,202.5 | 1,107.3/1,213.7 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 320 | 1,217.3 | 1,093.7/1,245.2 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 321 | 1,219.4 | 1,082.3/1,249.0 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 322 | 1,204.9 | 1,065.6/1,221.0 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 323 | 1,199.9 | 1,052.1/1,228.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 324 | 1,201.9 | 1,052.6/1,226.0 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 325 | 1,177.1 | 1,160.5/1,198.7 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 326 | 1,180.0 | 1,090.2/1,254.9 | 203.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 327 | 1,201.6 | 1,081.7/1,229.2 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 328 | 1,194.5 | 1,102.9/1,204.1 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 329 | 1,152.1 | 1,100.3/1,172.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 330 | 1,087.1 | 1,072.8/1,179.9 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 331 | 1,104.4 | 1,086.1/1,171.9 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 332 | 1,098.3 | 1,081.9/1,165.6 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 333 | 1,141.8 | 1,071.2/1,189.9 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 334 | 1,143.5 | 1,091.0/1,215.9 | 201.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 335 | 1,162.4 | 1,080.7/1,255.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 336 | 1,177.0 | 1,083.6/1,210.2 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 337 | 1,189.8 | 1,103.6/1,204.0 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 338 | 1,201.4 | 1,154.2/1,206.9 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 339 | 238.8 | 228.8/242.9 | 662.1 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 340 | 614.5 | 613.1/617.7 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 341 | 59.5 | 57.1/60.8 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 342 | 1,288.9 | 1,273.6/1,290.1 | 204.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 343 | 1,238.2 | 1,220.2/1,244.7 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 344 | 1,226.6 | 1,200.8/1,227.3 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 345 | 1,184.2 | 1,179.4/1,216.4 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 346 | 1,186.5 | 1,171.6/1,211.2 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 347 | 1,200.8 | 1,173.0/1,245.8 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 348 | 1,200.2 | 1,194.3/1,218.9 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 349 | 1,174.0 | 1,165.2/1,213.4 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 350 | 1,161.9 | 1,114.5/1,202.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 351 | 1,171.0 | 1,101.6/1,209.2 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 352 | 1,115.4 | 1,097.2/1,222.7 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 353 | 1,129.8 | 1,128.9/1,258.4 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 354 | 1,109.9 | 1,088.1/1,215.7 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 355 | 1,106.6 | 1,083.1/1,229.1 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 356 | 1,096.9 | 1,081.5/1,207.6 | 283.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 357 | 1,122.6 | 1,075.4/1,176.5 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 358 | 1,081.0 | 1,079.1/1,175.4 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 359 | 1,074.3 | 1,068.1/1,172.9 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 360 | 1,122.1 | 1,095.8/1,218.3 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 361 | 1,084.0 | 1,078.9/1,209.2 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 362 | 1,104.0 | 1,074.7/1,211.7 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 363 | 1,078.6 | 1,050.3/1,239.1 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 364 | 1,076.9 | 1,045.4/1,217.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 365 | 1,093.0 | 1,053.1/1,208.6 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 366 | 1,100.0 | 1,061.1/1,203.1 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 367 | 1,217.7 | 1,100.1/1,321.3 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 368 | 1,202.3 | 1,097.9/1,258.6 | 203.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 369 | 1,116.2 | 1,098.8/1,227.9 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 370 | 229.1 | 213.3/237.2 | 663.1 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 371 | 622.0 | 613.9/626.7 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 372 | 49.5 | 46.7/53.0 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 373 | 1,170.5 | 1,149.7/1,194.2 | 295.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 374 | 1,139.5 | 1,099.0/1,193.1 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 375 | 1,173.5 | 1,087.8/1,186.4 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 376 | 1,164.7 | 1,146.3/1,179.1 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 377 | 1,165.6 | 1,119.1/1,193.8 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 378 | 1,175.6 | 1,171.9/1,606.9 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 379 | 1,175.5 | 1,111.2/1,351.6 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 380 | 1,128.2 | 1,113.4/1,237.5 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 381 | 1,151.6 | 1,114.5/1,220.1 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 382 | 1,159.7 | 1,154.7/1,229.9 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 383 | 1,097.9 | 1,088.2/1,216.7 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 384 | 1,081.1 | 1,079.5/1,259.1 | 201.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 385 | 1,077.8 | 1,076.0/1,216.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 386 | 1,073.6 | 1,072.2/1,169.8 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 387 | 1,072.9 | 1,072.8/1,204.3 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 388 | 1,107.6 | 1,065.5/1,204.4 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 389 | 1,173.1 | 1,050.9/1,207.8 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 390 | 1,201.8 | 1,053.5/1,497.1 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 391 | 1,168.5 | 1,071.8/1,240.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 392 | 1,129.4 | 1,043.8/1,235.1 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 393 | 1,097.8 | 1,041.0/1,200.9 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 394 | 1,093.2 | 1,042.3/1,208.7 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 395 | 1,106.9 | 1,044.9/1,206.7 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 396 | 1,182.9 | 1,040.4/1,201.2 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 397 | 1,195.4 | 1,036.1/1,199.8 | 201.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 398 | 1,206.5 | 1,055.8/1,216.7 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 399 | 1,172.7 | 1,062.7/1,199.3 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 400 | 1,172.5 | 1,100.5/1,244.9 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 401 | 240.9 | 226.4/246.6 | 667.0 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 402 | 630.1 | 613.3/730.0 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 403 | 53.6 | 52.7/58.1 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 404 | 1,285.2 | 1,172.9/1,295.3 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 405 | 1,226.0 | 1,108.4/1,234.9 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 406 | 1,213.5 | 1,114.2/1,225.2 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 407 | 1,213.7 | 1,112.2/1,218.1 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 408 | 1,198.5 | 1,103.1/1,255.6 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 409 | 1,200.8 | 1,061.8/1,218.4 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 410 | 1,205.0 | 1,035.9/1,260.4 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 411 | 1,201.8 | 1,066.3/1,213.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 412 | 1,172.2 | 1,039.2/1,209.6 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 413 | 1,204.3 | 1,037.0/1,206.0 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 414 | 1,169.1 | 1,073.7/1,195.5 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 415 | 1,185.0 | 1,089.4/1,204.5 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 416 | 1,106.7 | 1,084.0/1,256.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 417 | 1,160.0 | 1,102.6/1,171.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 418 | 1,200.6 | 1,138.6/1,202.1 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 419 | 1,197.4 | 1,098.4/1,204.6 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 420 | 1,199.0 | 1,104.4/1,220.1 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 421 | 1,197.0 | 1,095.3/1,198.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 422 | 1,177.5 | 1,063.9/1,224.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 423 | 1,176.1 | 1,045.6/1,201.5 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 424 | 1,202.8 | 1,055.4/1,231.2 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 425 | 1,209.4 | 1,074.3/1,211.6 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 426 | 1,222.2 | 1,073.1/1,230.9 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 427 | 1,205.8 | 1,142.7/1,209.3 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 428 | 1,208.7 | 1,121.4/1,247.2 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 429 | 1,203.8 | 1,111.5/1,206.0 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 430 | 1,203.7 | 1,103.1/1,217.4 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 431 | 1,212.4 | 1,111.8/1,220.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 432 | 242.6 | 229.8/247.8 | 661.5 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 433 | 615.5 | 613.6/620.1 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 434 | 60.3 | 60.1/63.9 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 435 | 1,290.2 | 1,174.3/1,295.9 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 436 | 1,223.0 | 1,168.8/1,228.3 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 437 | 1,204.3 | 1,184.0/1,260.0 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 438 | 1,219.8 | 1,110.0/1,223.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 439 | 1,214.0 | 1,045.3/1,219.1 | 201.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 440 | 1,197.1 | 1,048.1/1,206.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 441 | 1,142.1 | 1,044.8/1,210.6 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 442 | 1,135.5 | 1,050.7/1,197.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 443 | 1,135.3 | 1,086.3/1,216.8 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 444 | 1,114.6 | 1,050.3/1,217.8 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 445 | 1,105.0 | 1,049.5/1,204.7 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 446 | 1,083.3 | 1,047.6/1,249.6 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 447 | 1,149.7 | 1,096.9/1,217.9 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 448 | 1,170.1 | 1,048.5/1,208.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 449 | 1,189.1 | 1,053.8/1,202.6 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 450 | 1,175.3 | 1,043.4/1,221.6 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 451 | 1,200.4 | 1,049.6/1,202.2 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 452 | 1,173.0 | 1,051.1/1,211.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 453 | 1,166.4 | 1,049.8/1,205.1 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 454 | 1,222.7 | 1,044.9/1,247.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 455 | 1,179.9 | 1,045.8/1,218.7 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 456 | 1,150.1 | 1,074.2/1,208.0 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 457 | 1,113.8 | 1,071.5/1,225.2 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 458 | 1,094.4 | 1,051.8/1,202.1 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 459 | 1,125.2 | 1,123.9/1,209.5 | 205.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 460 | 1,179.6 | 1,128.7/1,182.6 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 461 | 1,163.8 | 1,150.8/1,174.5 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 462 | 1,167.0 | 1,161.8/1,170.7 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 463 | 236.0 | 224.7/239.4 | 663.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 464 | 624.4 | 618.2/716.0 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 465 | 56.5 | 49.1/56.9 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 466 | 1,258.9 | 1,249.6/1,313.9 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 467 | 1,190.3 | 1,190.0/1,239.8 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 468 | 1,220.6 | 1,130.9/1,227.7 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 469 | 1,216.9 | 1,107.3/1,221.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 470 | 1,205.5 | 1,155.9/1,211.7 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 471 | 1,210.2 | 1,139.0/1,254.2 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 472 | 1,200.5 | 1,097.4/1,247.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 473 | 1,215.8 | 1,079.7/1,223.8 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 474 | 1,204.7 | 1,084.2/1,250.2 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 475 | 1,183.4 | 1,080.5/1,246.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 476 | 1,167.7 | 1,074.2/1,213.1 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 477 | 1,131.3 | 1,076.9/1,224.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 478 | 1,120.0 | 1,068.3/1,237.9 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 479 | 1,115.4 | 1,067.3/1,204.5 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 480 | 1,059.2 | 1,056.0/1,219.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 481 | 1,063.5 | 1,048.9/1,200.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 482 | 1,046.0 | 1,037.3/1,217.4 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 483 | 1,045.5 | 1,045.0/1,250.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 484 | 1,050.4 | 1,041.1/1,209.9 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 485 | 1,061.8 | 1,044.2/1,206.9 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 486 | 1,118.9 | 1,053.0/1,233.9 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 487 | 1,101.3 | 1,045.2/1,208.5 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 488 | 1,111.2 | 1,081.7/1,225.6 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 489 | 1,122.4 | 1,049.6/1,210.6 | 204.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 490 | 1,138.0 | 1,057.6/1,225.8 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 491 | 1,104.6 | 1,054.5/1,259.8 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 492 | 1,104.9 | 1,052.8/1,211.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 493 | 1,099.2 | 1,045.0/1,209.9 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 494 | 219.5 | 214.5/261.3 | 663.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 495 | 619.7 | 614.0/721.8 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 496 | 56.8 | 49.9/70.0 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 497 | 1,206.8 | 1,141.7/1,311.6 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 498 | 1,184.5 | 1,061.6/1,245.5 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 499 | 1,221.3 | 1,070.5/1,228.7 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 500 | 1,167.5 | 1,091.0/1,221.5 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 501 | 1,177.0 | 1,056.7/1,233.5 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 502 | 1,174.2 | 1,049.4/1,213.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 503 | 1,157.8 | 1,074.5/1,203.7 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 504 | 1,155.2 | 1,077.3/1,218.9 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 505 | 1,174.8 | 1,077.6/1,199.7 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 506 | 1,120.2 | 1,099.8/1,175.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 507 | 1,114.0 | 1,101.8/1,173.6 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 508 | 1,095.5 | 1,071.1/1,172.3 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 509 | 1,099.8 | 1,078.2/1,212.1 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 510 | 1,106.6 | 1,077.4/1,170.2 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 511 | 1,172.5 | 1,069.2/1,184.8 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 512 | 1,206.3 | 1,082.3/1,206.4 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 513 | 1,194.3 | 1,077.5/1,208.1 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 514 | 1,201.2 | 1,199.8/1,304.5 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 515 | 1,212.8 | 1,209.4/1,377.5 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 516 | 1,196.3 | 1,063.5/1,234.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 517 | 1,201.1 | 1,063.5/1,252.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 518 | 1,204.3 | 1,084.5/1,210.5 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 519 | 1,197.9 | 1,052.2/1,208.5 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 520 | 1,194.4 | 1,049.9/1,198.0 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 521 | 1,217.7 | 1,050.0/1,238.9 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 522 | 1,166.4 | 1,041.9/1,200.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 523 | 1,205.8 | 1,171.5/1,502.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 524 | 1,168.7 | 1,128.2/1,248.5 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 525 | 237.6 | 207.8/239.1 | 663.7 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 526 | 619.0 | 616.2/745.8 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 527 | 55.1 | 42.1/55.2 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 528 | 1,229.8 | 1,128.3/1,299.2 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 529 | 1,210.7 | 1,181.4/1,224.7 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 530 | 1,215.1 | 1,212.7/1,219.9 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 531 | 1,196.4 | 1,171.9/1,204.5 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 532 | 1,192.0 | 1,178.0/1,192.1 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 533 | 1,186.9 | 1,164.9/1,197.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 534 | 1,207.4 | 1,196.5/1,232.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 535 | 1,195.8 | 1,189.6/1,253.1 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 536 | 1,215.1 | 1,201.9/1,226.5 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 537 | 1,182.7 | 1,159.4/1,209.9 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 538 | 1,177.1 | 1,099.8/1,200.2 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 539 | 1,194.7 | 1,055.6/1,203.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 540 | 1,178.0 | 1,081.4/1,204.2 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 541 | 1,126.7 | 1,098.6/1,209.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 542 | 1,191.2 | 1,188.2/1,235.0 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 543 | 1,199.0 | 1,193.7/1,212.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 544 | 1,230.9 | 1,195.9/1,248.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 545 | 1,202.6 | 1,184.0/1,237.9 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 546 | 1,192.9 | 1,110.5/1,198.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 547 | 1,197.0 | 1,105.0/1,204.6 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 548 | 1,192.7 | 1,107.7/1,209.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 549 | 1,191.0 | 1,081.3/1,193.9 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 550 | 1,181.2 | 1,097.3/1,200.1 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 551 | 1,153.7 | 1,134.5/1,193.8 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 552 | 1,176.4 | 1,159.4/1,244.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 553 | 1,181.4 | 1,168.9/1,210.6 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 554 | 1,200.2 | 1,194.6/1,752.7 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 555 | 1,206.5 | 1,173.2/1,244.9 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 556 | 237.5 | 232.2/247.1 | 663.8 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 557 | 620.3 | 606.0/625.5 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 558 | 54.4 | 49.8/55.5 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 559 | 1,245.4 | 1,243.2/1,280.3 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 560 | 1,219.2 | 1,216.2/1,227.9 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 561 | 1,188.1 | 1,185.6/1,222.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 562 | 1,167.2 | 1,092.7/1,220.7 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 563 | 1,134.0 | 1,082.5/1,180.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 564 | 1,171.5 | 1,076.7/1,191.7 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 565 | 1,177.6 | 1,071.2/1,213.8 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 566 | 1,187.0 | 1,078.6/1,196.4 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 567 | 1,180.4 | 1,092.5/1,195.9 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 568 | 1,169.6 | 1,105.6/1,195.5 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 569 | 1,159.7 | 1,113.2/1,206.7 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 570 | 1,207.1 | 1,068.9/1,214.3 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 571 | 1,283.3 | 1,192.9/1,410.7 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 572 | 1,226.6 | 1,122.7/1,342.5 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 573 | 1,138.1 | 1,105.9/1,194.0 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 574 | 1,178.2 | 1,097.6/1,195.5 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 575 | 1,159.1 | 1,072.1/1,210.3 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 576 | 1,161.9 | 1,074.4/1,210.2 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 577 | 1,160.4 | 1,077.9/1,215.4 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 578 | 1,113.5 | 1,113.2/1,244.4 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 579 | 1,098.1 | 1,079.4/1,223.2 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 580 | 1,128.3 | 1,073.7/1,170.5 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 581 | 1,110.2 | 1,085.9/1,177.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 582 | 1,089.9 | 1,075.8/1,166.4 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 583 | 1,120.7 | 1,082.9/1,178.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 584 | 1,163.0 | 1,106.8/1,173.2 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 585 | 1,165.1 | 1,110.6/1,168.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 586 | 1,186.9 | 1,093.2/1,212.2 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 587 | 240.5 | 222.5/265.1 | 661.5 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 588 | 618.2 | 612.2/625.3 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 589 | 56.3 | 45.3/73.9 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 590 | 1,272.3 | 1,173.1/1,664.2 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 591 | 1,196.2 | 1,157.9/1,243.6 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 592 | 1,190.7 | 1,110.8/1,213.9 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 593 | 1,182.8 | 1,118.5/1,721.4 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 594 | 1,150.5 | 1,084.4/1,177.7 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 595 | 1,128.7 | 1,072.2/1,192.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 596 | 1,174.1 | 1,099.1/1,254.0 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 597 | 1,184.0 | 1,171.7/1,232.2 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 598 | 1,185.4 | 1,161.0/1,226.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 599 | 1,174.5 | 1,158.0/1,208.9 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 600 | 1,201.8 | 1,174.4/1,226.1 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 601 | 1,194.9 | 1,167.2/1,577.5 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 602 | 1,193.7 | 1,139.0/1,294.2 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 603 | 1,196.4 | 1,099.8/1,224.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 604 | 1,197.9 | 1,104.6/1,269.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 605 | 1,119.7 | 1,097.6/1,184.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 606 | 1,139.6 | 1,067.4/1,175.1 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 607 | 1,166.5 | 1,068.6/1,177.0 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 608 | 1,154.5 | 1,102.9/1,174.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 609 | 1,103.3 | 1,046.7/1,181.9 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 610 | 1,112.3 | 1,042.2/1,185.7 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 611 | 1,140.7 | 1,061.7/1,154.4 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 612 | 1,106.9 | 1,092.0/1,112.5 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 613 | 1,095.8 | 1,078.1/1,107.4 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 614 | 1,086.4 | 1,070.1/1,088.0 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 615 | 1,072.2 | 1,070.1/1,086.9 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 616 | 1,077.8 | 1,071.0/1,114.4 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 617 | 1,098.5 | 1,097.4/1,170.5 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 618 | 225.0 | 222.4/235.4 | 663.0 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 619 | 622.2 | 621.9/622.4 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 620 | 53.9 | 48.2/58.0 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 621 | 1,221.5 | 1,134.4/1,288.3 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 622 | 1,123.4 | 1,103.9/1,222.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 623 | 1,134.7 | 1,128.9/1,210.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 624 | 1,180.3 | 1,088.3/1,207.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 625 | 1,182.1 | 1,090.8/1,210.9 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 626 | 1,200.3 | 1,088.2/1,207.1 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 627 | 1,206.7 | 1,081.2/1,241.2 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 628 | 1,211.6 | 1,079.4/1,230.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 629 | 1,212.7 | 1,050.2/1,258.5 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 630 | 1,204.3 | 1,048.0/1,226.9 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 631 | 1,202.9 | 1,043.5/1,208.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 632 | 1,203.8 | 1,203.3/1,222.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 633 | 1,198.4 | 1,056.4/1,224.4 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 634 | 1,193.1 | 1,076.2/1,212.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 635 | 1,168.3 | 1,082.9/1,216.2 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 636 | 1,181.2 | 1,090.9/1,202.6 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 637 | 1,175.6 | 1,079.5/1,206.8 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 638 | 1,175.5 | 1,078.9/1,251.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 639 | 1,100.9 | 1,052.7/1,178.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 640 | 1,098.6 | 1,046.4/1,172.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 641 | 1,099.8 | 1,078.9/1,149.9 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 642 | 1,099.2 | 1,078.5/1,116.5 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 643 | 1,094.6 | 1,073.7/1,127.8 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 644 | 1,119.6 | 1,050.2/1,177.8 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 645 | 1,170.9 | 1,064.6/1,180.0 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 646 | 1,167.7 | 1,046.5/6,252.9 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 647 | 1,154.7 | 1,055.4/1,239.8 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 648 | 1,152.6 | 1,045.5/1,233.9 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 649 | 233.5 | 206.2/251.4 | 663.7 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 650 | 619.6 | 611.9/622.5 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 651 | 50.6 | 45.8/64.8 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 652 | 1,262.9 | 1,162.3/1,345.2 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 653 | 1,220.5 | 1,092.9/1,234.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 654 | 1,187.3 | 1,160.9/1,263.0 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 655 | 1,184.7 | 1,167.4/1,223.4 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 656 | 1,189.0 | 1,169.5/1,210.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 657 | 1,210.5 | 1,181.7/1,216.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 658 | 1,216.7 | 1,157.4/1,361.9 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 659 | 1,220.4 | 1,136.5/1,225.6 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 660 | 1,210.9 | 1,201.3/1,367.2 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 661 | 1,199.7 | 1,163.0/1,314.2 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 662 | 1,213.1 | 1,179.5/1,219.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 663 | 1,184.2 | 1,183.6/1,205.5 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 664 | 1,179.2 | 1,172.9/1,219.9 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 665 | 1,173.9 | 1,172.7/1,206.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 666 | 1,199.2 | 1,167.7/1,217.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 667 | 1,206.9 | 1,161.8/1,251.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 668 | 1,232.7 | 1,116.0/1,269.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 669 | 1,214.5 | 1,147.5/1,220.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 670 | 1,207.4 | 1,164.4/1,227.4 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 671 | 1,213.8 | 1,209.9/1,217.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 672 | 1,208.0 | 1,172.9/1,744.3 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 673 | 1,216.0 | 1,186.7/1,420.7 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 674 | 1,193.4 | 1,118.3/1,228.4 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 675 | 1,187.0 | 1,083.9/1,218.2 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 676 | 1,171.7 | 1,116.3/1,202.4 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 677 | 1,179.4 | 1,086.0/1,192.0 | 203.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 678 | 1,171.4 | 1,084.4/1,181.8 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 679 | 1,152.5 | 1,090.4/1,219.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 680 | 229.6 | 221.1/243.5 | 663.1 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 681 | 615.8 | 612.7/783.8 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 682 | 60.0 | 55.6/61.6 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 683 | 1,211.3 | 1,198.0/1,264.9 | 204.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 684 | 1,144.1 | 1,133.9/1,197.2 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 685 | 1,138.8 | 1,126.4/1,209.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 686 | 1,210.8 | 1,115.2/1,246.1 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 687 | 1,205.5 | 1,112.4/1,223.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 688 | 1,213.4 | 1,098.6/1,216.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 689 | 1,228.6 | 1,079.4/1,250.3 | 203.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 690 | 1,204.6 | 1,088.1/1,215.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 691 | 1,210.0 | 1,096.3/1,215.6 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 692 | 1,210.8 | 1,092.4/1,212.4 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 693 | 1,201.0 | 1,084.3/1,219.3 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 694 | 1,119.0 | 1,084.4/1,165.6 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 695 | 1,106.9 | 1,102.2/1,116.4 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 696 | 1,107.2 | 1,080.9/1,121.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 697 | 1,103.2 | 1,081.7/1,109.7 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 698 | 1,098.3 | 1,085.0/1,106.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 699 | 1,099.7 | 1,090.8/1,188.6 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 700 | 1,110.5 | 1,106.6/1,190.9 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 701 | 1,126.2 | 1,105.0/1,139.9 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 702 | 1,112.3 | 1,107.2/1,118.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 703 | 1,128.8 | 1,105.0/1,131.7 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 704 | 1,111.2 | 1,098.8/1,213.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 705 | 1,113.1 | 1,097.6/1,192.5 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 706 | 1,191.9 | 1,094.8/1,234.1 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 707 | 1,173.1 | 1,122.7/1,176.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 708 | 1,169.4 | 1,088.6/1,169.8 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 709 | 1,171.5 | 1,078.5/1,173.5 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 710 | 1,183.8 | 1,093.2/1,185.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 711 | 250.7 | 225.5/322.2 | 663.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 712 | 612.3 | 609.6/616.8 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 713 | 64.7 | 56.6/67.4 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 714 | 1,304.8 | 1,267.2/1,336.0 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 715 | 1,249.9 | 1,206.2/1,255.3 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 716 | 1,222.3 | 1,215.9/1,254.0 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 717 | 1,193.5 | 1,164.2/1,216.3 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 718 | 1,180.4 | 1,112.3/1,180.4 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 719 | 1,196.2 | 1,126.3/1,226.6 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 720 | 1,186.8 | 1,123.6/1,253.0 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 721 | 1,191.5 | 1,117.0/1,296.3 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 722 | 1,169.0 | 1,117.0/1,290.4 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 723 | 1,242.9 | 1,102.8/1,246.4 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 724 | 1,145.1 | 1,128.6/1,196.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 725 | 1,201.3 | 1,114.3/1,241.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 726 | 1,157.4 | 1,116.2/1,224.9 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 727 | 1,131.3 | 1,111.2/1,159.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 728 | 1,154.4 | 1,112.1/1,165.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 729 | 1,173.8 | 1,113.4/1,176.1 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 730 | 1,174.9 | 1,133.6/1,199.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 731 | 1,181.0 | 1,165.2/1,219.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 732 | 1,158.3 | 1,151.7/1,171.7 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 733 | 1,172.6 | 1,112.9/1,176.9 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 734 | 1,140.7 | 1,103.5/1,169.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 735 | 1,172.0 | 1,107.4/1,173.3 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 736 | 1,169.0 | 1,110.8/1,188.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 737 | 1,183.2 | 1,111.7/1,204.1 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 738 | 1,169.8 | 1,115.6/1,189.3 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 739 | 1,176.8 | 1,173.0/1,200.9 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 740 | 1,206.1 | 1,204.1/1,233.3 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 741 | 1,201.5 | 1,181.6/1,227.2 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 742 | 247.0 | 225.5/256.7 | 661.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 743 | 618.9 | 615.0/622.6 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 744 | 57.7 | 53.4/62.0 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 745 | 1,295.1 | 1,251.7/1,334.8 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 746 | 1,239.7 | 1,188.5/1,243.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 747 | 1,222.4 | 1,183.0/1,231.7 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 748 | 1,212.4 | 1,170.6/1,248.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 749 | 1,219.0 | 1,112.9/1,224.9 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 750 | 1,212.8 | 1,129.8/1,225.3 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 751 | 1,194.7 | 1,122.8/1,227.5 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 752 | 1,198.5 | 1,114.4/1,212.3 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 753 | 1,198.4 | 1,135.5/1,212.2 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 754 | 1,224.0 | 1,116.0/1,225.6 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 755 | 1,181.9 | 1,141.9/1,195.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 756 | 1,206.4 | 1,168.6/1,218.0 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 757 | 1,214.7 | 1,205.2/1,265.3 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 758 | 1,262.6 | 1,177.8/1,421.4 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 759 | 1,199.8 | 1,189.7/1,231.9 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 760 | 1,210.6 | 1,210.3/1,214.2 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 761 | 1,211.6 | 1,194.2/1,217.7 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 762 | 1,207.9 | 1,189.4/1,209.2 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 763 | 1,206.0 | 1,169.7/1,215.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 764 | 1,172.2 | 1,157.4/1,226.9 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 765 | 1,169.6 | 1,137.5/1,231.1 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 766 | 1,177.2 | 1,154.8/1,204.2 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 767 | 1,184.9 | 1,104.0/1,221.5 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 768 | 1,138.7 | 1,077.4/1,201.1 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 769 | 1,098.2 | 1,068.9/1,174.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 770 | 1,099.2 | 1,085.8/1,182.1 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 771 | 1,113.9 | 1,078.8/1,265.7 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 772 | 1,147.6 | 1,073.5/1,179.3 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 773 | 233.7 | 211.8/242.3 | 662.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 774 | 623.7 | 613.9/631.5 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 775 | 56.6 | 45.5/61.4 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 776 | 1,215.3 | 1,105.5/1,276.9 | 203.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 777 | 1,198.8 | 1,094.9/1,218.4 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 778 | 1,192.4 | 1,069.8/1,192.7 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 779 | 1,177.2 | 1,051.6/1,179.3 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 780 | 1,164.7 | 1,057.4/1,183.8 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 781 | 1,105.4 | 1,053.2/1,173.4 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 782 | 1,115.5 | 1,048.9/1,151.4 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 783 | 1,145.2 | 1,062.4/1,170.5 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 784 | 1,115.2 | 1,054.7/1,180.4 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 785 | 1,080.5 | 1,078.5/1,102.4 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 786 | 1,071.1 | 1,063.1/1,102.1 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 787 | 1,051.8 | 1,042.7/1,085.1 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 788 | 1,055.8 | 1,047.8/1,527.0 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 789 | 1,051.8 | 1,047.2/1,522.2 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 790 | 1,079.7 | 1,053.0/1,497.5 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 791 | 1,131.0 | 1,062.8/1,476.2 | 205.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 792 | 1,223.6 | 1,049.6/1,296.4 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 793 | 1,210.4 | 1,167.9/1,434.0 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 794 | 1,203.9 | 1,203.2/1,208.3 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 795 | 1,213.4 | 1,168.0/1,261.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 796 | 1,181.5 | 1,164.0/1,221.4 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 797 | 1,177.4 | 1,171.1/1,203.5 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 798 | 1,180.1 | 1,171.3/1,217.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 799 | 1,169.5 | 1,168.1/1,193.7 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 800 | 1,176.3 | 1,172.3/1,206.4 | 201.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 801 | 1,171.9 | 1,161.5/1,195.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 802 | 1,143.8 | 1,115.5/1,179.9 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 803 | 1,111.5 | 1,074.7/1,167.1 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 804 | 221.3 | 219.4/244.9 | 662.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 805 | 621.1 | 617.2/627.4 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 806 | 50.0 | 49.9/57.4 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 807 | 1,153.3 | 1,148.3/1,332.4 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 808 | 1,101.8 | 1,098.8/1,228.1 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 809 | 1,106.1 | 1,077.6/1,195.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 810 | 1,129.6 | 1,108.6/1,178.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 811 | 1,124.5 | 1,088.4/1,215.9 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 812 | 1,116.7 | 1,080.1/1,173.9 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 813 | 1,104.4 | 1,084.7/1,169.4 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 814 | 1,148.7 | 1,131.7/1,194.6 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 815 | 1,107.3 | 1,085.3/1,207.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 816 | 1,144.9 | 1,081.2/1,206.4 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 817 | 1,205.1 | 1,086.7/1,225.5 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 818 | 1,216.4 | 1,076.4/1,223.5 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 819 | 1,204.0 | 1,107.4/1,206.3 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 820 | 1,203.0 | 1,114.1/1,209.3 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 821 | 1,197.9 | 1,179.4/1,212.0 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 822 | 1,197.0 | 1,196.3/1,226.4 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 823 | 1,205.8 | 1,198.0/1,222.6 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 824 | 1,205.5 | 1,198.3/1,209.9 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 825 | 1,215.2 | 1,201.1/1,217.3 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 826 | 1,224.7 | 1,192.2/1,229.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 827 | 1,205.8 | 1,176.3/1,207.2 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 828 | 1,202.0 | 1,166.2/1,203.1 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 829 | 1,204.5 | 1,196.6/1,205.8 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 830 | 1,201.9 | 1,198.6/1,234.5 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 831 | 1,211.7 | 1,195.6/1,250.5 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 832 | 1,192.2 | 1,167.0/1,207.8 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 833 | 1,203.5 | 1,159.6/1,206.0 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 834 | 1,207.4 | 1,180.6/1,218.0 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 835 | 236.4 | 221.7/243.0 | 663.1 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 836 | 617.9 | 617.4/629.4 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 837 | 56.4 | 49.6/58.0 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 838 | 1,224.8 | 1,218.0/1,265.1 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 839 | 1,197.2 | 1,192.2/1,225.7 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 840 | 1,176.0 | 1,118.8/1,219.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 841 | 1,182.2 | 1,161.5/1,213.9 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 842 | 1,195.0 | 1,109.5/1,205.8 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 843 | 1,200.5 | 1,125.1/1,219.7 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 844 | 1,206.4 | 1,110.3/1,215.5 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 845 | 1,203.9 | 1,138.3/1,207.2 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 846 | 1,211.3 | 1,133.3/1,260.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 847 | 1,206.9 | 1,105.8/1,209.9 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 848 | 1,212.7 | 1,100.7/1,236.9 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 849 | 1,230.6 | 1,096.6/1,256.1 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 850 | 1,209.7 | 1,097.3/1,211.1 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 851 | 1,214.3 | 1,077.7/1,225.6 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 852 | 1,205.3 | 1,070.7/1,205.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 853 | 1,198.0 | 1,073.0/1,214.1 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 854 | 1,200.4 | 1,106.1/1,202.1 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 855 | 1,197.5 | 1,099.2/1,199.9 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 856 | 1,211.1 | 1,100.7/1,234.8 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 857 | 1,172.7 | 1,108.4/1,249.2 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 858 | 1,165.9 | 1,093.7/1,203.9 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 859 | 1,171.3 | 1,095.0/1,195.7 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 860 | 1,129.8 | 1,113.6/1,199.1 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 861 | 1,212.2 | 1,209.8/1,224.8 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 862 | 1,223.2 | 1,202.4/1,720.8 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 863 | 1,205.5 | 1,200.4/1,243.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 864 | 1,209.0 | 1,190.2/1,219.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 865 | 1,181.0 | 1,119.3/1,201.5 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 866 | 237.5 | 232.7/241.8 | 661.4 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 867 | 616.5 | 614.4/619.6 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 868 | 56.2 | 45.7/60.9 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 869 | 1,213.8 | 1,121.8/1,304.9 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 870 | 1,140.7 | 1,078.4/1,231.6 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 871 | 1,160.6 | 1,091.0/1,211.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 872 | 1,196.6 | 1,075.2/1,242.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 873 | 1,205.8 | 1,081.9/1,226.7 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 874 | 1,216.5 | 1,083.5/1,236.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 875 | 1,204.7 | 1,081.2/1,211.6 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 876 | 1,201.3 | 1,113.6/1,227.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 877 | 1,228.2 | 1,116.8/1,657.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 878 | 1,198.9 | 1,169.0/1,240.1 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 879 | 1,195.1 | 1,168.6/1,199.9 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 880 | 1,216.8 | 1,178.0/1,243.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 881 | 1,199.3 | 1,183.8/1,220.7 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 882 | 1,185.9 | 1,168.9/1,243.2 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 883 | 1,190.5 | 1,166.8/1,222.0 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 884 | 1,174.4 | 1,138.7/1,199.6 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 885 | 1,182.0 | 1,139.6/1,210.7 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 886 | 1,170.2 | 1,081.9/1,198.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 887 | 1,136.4 | 1,110.7/1,208.2 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 888 | 1,126.6 | 1,044.6/1,236.1 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 889 | 1,123.6 | 1,044.9/1,208.7 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 890 | 1,104.7 | 1,043.0/1,202.0 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 891 | 1,112.0 | 1,052.4/1,195.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 892 | 1,135.6 | 1,045.6/1,198.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 893 | 1,106.1 | 1,054.3/1,170.2 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 894 | 1,106.8 | 1,072.9/1,164.6 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 895 | 1,095.5 | 1,092.3/1,161.3 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 896 | 1,100.6 | 1,047.3/1,201.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 897 | 230.2 | 201.0/255.1 | 663.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 898 | 615.4 | 614.2/622.2 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 899 | 51.8 | 42.7/63.3 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 900 | 1,243.0 | 1,179.4/1,297.2 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 901 | 1,186.1 | 1,096.4/1,241.8 | 204.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 902 | 1,108.7 | 1,084.1/1,224.8 | 209.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 903 | 1,105.7 | 1,077.7/1,211.3 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 904 | 1,117.7 | 1,073.1/1,211.2 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 905 | 1,111.4 | 1,107.5/1,205.3 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 906 | 1,140.6 | 1,100.4/1,148.6 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 907 | 1,152.7 | 1,133.1/1,191.1 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 908 | 1,095.4 | 1,086.2/1,202.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 909 | 1,082.2 | 1,073.7/1,203.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 910 | 1,068.5 | 1,067.6/1,205.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 911 | 1,069.0 | 1,050.9/1,213.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 912 | 1,056.5 | 1,054.6/1,198.8 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 913 | 1,051.6 | 1,036.3/1,215.9 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 914 | 1,071.4 | 1,055.1/1,187.9 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 915 | 1,076.8 | 1,052.4/1,176.9 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 916 | 1,099.3 | 1,097.7/1,169.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 917 | 1,166.2 | 1,164.0/1,376.3 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 918 | 1,162.5 | 1,159.7/1,185.0 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 919 | 1,187.7 | 1,160.6/1,209.0 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 920 | 1,171.3 | 1,156.6/1,208.5 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 921 | 1,195.0 | 1,122.0/1,221.2 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 922 | 1,203.4 | 1,115.8/1,226.0 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 923 | 1,195.3 | 1,114.1/1,204.8 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 924 | 1,199.0 | 1,128.5/1,208.3 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 925 | 1,166.5 | 1,165.6/1,225.3 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 926 | 1,166.7 | 1,155.4/1,207.8 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 927 | 1,139.9 | 1,104.6/1,202.8 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 928 | 211.0 | 207.8/234.3 | 662.2 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 929 | 626.0 | 618.1/627.6 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 930 | 48.1 | 45.2/56.2 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 931 | 1,299.4 | 1,180.0/1,396.3 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 932 | 1,228.0 | 1,111.6/1,601.5 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 933 | 1,205.4 | 1,096.9/1,231.3 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 934 | 1,202.5 | 1,072.1/1,227.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 935 | 1,209.9 | 1,075.4/1,226.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 936 | 1,209.4 | 1,051.1/1,215.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 937 | 1,202.2 | 1,072.2/1,211.9 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 938 | 1,204.7 | 1,058.4/1,208.0 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 939 | 1,203.0 | 1,045.6/1,216.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 940 | 1,194.5 | 1,041.8/1,206.0 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 941 | 1,202.7 | 1,036.6/1,210.3 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 942 | 1,203.5 | 1,043.5/1,229.3 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 943 | 1,212.1 | 1,050.6/1,219.5 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 944 | 1,210.4 | 1,049.7/1,215.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 945 | 1,189.2 | 1,058.7/1,204.8 | 242.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 946 | 1,173.9 | 1,033.3/1,202.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 947 | 1,202.0 | 1,044.5/1,202.3 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 948 | 1,165.4 | 1,037.2/1,210.8 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 949 | 1,167.3 | 1,041.6/1,206.4 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 950 | 1,175.5 | 1,040.2/1,203.7 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 951 | 1,195.2 | 1,037.2/1,226.6 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 952 | 1,193.8 | 1,035.4/1,642.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 953 | 1,187.9 | 1,038.2/1,200.9 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 954 | 1,182.6 | 1,077.3/1,199.5 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 955 | 1,186.9 | 1,034.3/1,210.6 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 956 | 1,175.4 | 1,035.2/1,210.8 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 957 | 1,174.5 | 1,040.6/1,201.2 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 958 | 1,184.1 | 1,037.3/1,195.0 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 959 | 244.4 | 193.3/259.4 | 667.4 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 960 | 632.7 | 601.8/729.1 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 961 | 49.7 | 41.2/60.8 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 962 | 1,259.5 | 1,121.8/1,273.7 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 963 | 1,199.3 | 1,057.9/1,200.9 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 964 | 1,181.3 | 1,053.5/1,201.2 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 965 | 1,169.2 | 1,085.3/1,175.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 966 | 1,166.4 | 1,042.7/1,189.0 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 967 | 1,160.5 | 1,043.3/1,200.2 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 968 | 1,168.4 | 1,044.1/1,237.0 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 969 | 1,167.3 | 1,040.1/1,210.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 970 | 1,116.1 | 1,039.3/1,206.7 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 971 | 1,076.9 | 1,044.0/1,195.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 972 | 1,084.9 | 1,033.3/1,202.3 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 973 | 1,084.4 | 1,067.4/1,221.5 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 974 | 1,081.0 | 1,078.1/1,254.2 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 975 | 1,055.2 | 1,049.4/1,201.6 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 976 | 1,089.4 | 1,061.0/1,228.9 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 977 | 1,111.8 | 1,082.4/1,245.4 | 218.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 978 | 1,118.5 | 1,067.3/1,207.6 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 979 | 1,157.7 | 1,068.6/1,208.8 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 980 | 1,164.7 | 1,073.9/1,186.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 981 | 1,170.6 | 1,074.1/1,179.2 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 982 | 1,114.7 | 1,098.7/1,167.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 983 | 1,145.3 | 1,112.2/1,155.9 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 984 | 1,156.6 | 1,116.9/1,211.9 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 985 | 1,126.9 | 1,068.6/1,178.1 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 986 | 1,105.1 | 1,064.5/1,114.1 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 987 | 1,120.9 | 1,070.7/1,171.5 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 988 | 1,083.5 | 1,035.1/1,141.6 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 989 | 1,078.8 | 1,069.0/1,183.4 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 990 | 227.2 | 199.5/228.2 | 661.2 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 991 | 618.1 | 610.8/631.2 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 992 | 48.3 | 39.4/58.0 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 993 | 1,174.6 | 1,121.1/1,252.8 | 204.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 994 | 1,104.2 | 1,077.6/1,238.8 | 205.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 995 | 1,136.7 | 1,075.4/1,214.4 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 996 | 1,061.4 | 1,042.2/1,190.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 997 | 1,060.2 | 1,046.9/1,172.2 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 998 | 1,057.6 | 1,045.8/1,162.3 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 999 | 1,064.6 | 1,039.1/1,177.2 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1000 | 1,059.8 | 1,043.5/1,164.2 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1001 | 1,083.9 | 1,058.1/1,221.0 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1002 | 1,094.8 | 1,056.0/1,183.1 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1003 | 1,137.2 | 1,059.1/1,195.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1004 | 1,201.5 | 1,083.8/1,213.9 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1005 | 1,161.5 | 1,064.1/1,202.2 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1006 | 1,165.8 | 1,082.2/1,203.5 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1007 | 1,143.7 | 1,078.0/1,196.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1008 | 1,107.7 | 1,081.4/1,184.5 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1009 | 1,156.5 | 1,092.7/1,159.9 | 201.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1010 | 1,155.1 | 1,098.9/1,161.7 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1011 | 1,161.0 | 1,105.7/1,193.8 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1012 | 1,127.3 | 1,126.4/1,210.3 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1013 | 1,169.3 | 1,098.4/1,225.5 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1014 | 1,153.8 | 1,105.0/1,194.4 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1015 | 1,157.1 | 1,083.9/1,171.1 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1016 | 1,162.6 | 1,065.3/1,178.3 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1017 | 1,161.6 | 1,060.1/1,174.9 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1018 | 1,159.6 | 1,048.7/1,167.8 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1019 | 1,152.1 | 1,072.3/1,199.9 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1020 | 1,156.5 | 1,111.6/1,187.1 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1021 | 228.8 | 224.0/255.5 | 661.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1022 | 617.7 | 614.4/622.3 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1023 | 46.6 | 42.6/63.5 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1024 | 1,235.4 | 1,142.4/1,290.2 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1025 | 1,211.0 | 1,057.8/1,240.7 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1026 | 1,202.5 | 1,041.5/1,212.4 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1027 | 1,202.1 | 1,039.4/1,210.5 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1028 | 1,194.1 | 1,037.5/1,213.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1029 | 1,192.9 | 1,044.0/1,217.0 | 203.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1030 | 1,201.8 | 1,032.7/1,204.2 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1031 | 1,200.1 | 1,033.7/1,220.5 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1032 | 1,198.8 | 1,079.1/1,212.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1033 | 1,201.5 | 1,169.7/1,754.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1034 | 1,163.5 | 1,139.5/1,184.1 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1035 | 1,154.7 | 1,113.3/1,178.3 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1036 | 1,158.8 | 1,081.3/1,169.6 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1037 | 1,113.0 | 1,078.1/1,171.8 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1038 | 1,162.1 | 1,064.7/1,170.5 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1039 | 1,157.2 | 1,070.7/1,175.2 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1040 | 1,165.3 | 1,103.1/1,193.2 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1041 | 1,156.7 | 1,078.4/1,203.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1042 | 1,147.4 | 1,075.0/1,201.2 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1043 | 1,165.5 | 1,061.7/1,197.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1044 | 1,183.8 | 1,066.7/1,195.8 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1045 | 1,152.0 | 1,069.9/1,170.6 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1046 | 1,110.8 | 1,076.0/1,138.1 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1047 | 1,096.6 | 1,055.7/1,100.8 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1048 | 1,096.2 | 1,073.6/1,107.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1049 | 1,081.4 | 1,069.5/1,150.6 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1050 | 1,105.3 | 1,094.6/1,164.3 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1051 | 1,120.3 | 1,070.4/1,181.3 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1052 | 232.8 | 228.0/246.9 | 663.2 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1053 | 623.4 | 616.4/730.9 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1054 | 48.8 | 47.5/58.6 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1055 | 1,280.0 | 1,129.1/1,300.8 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1056 | 1,225.4 | 1,102.2/1,234.4 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1057 | 1,207.4 | 1,074.2/1,219.9 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1058 | 1,216.1 | 1,052.3/1,217.9 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1059 | 1,201.3 | 1,049.0/1,225.3 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1060 | 1,195.1 | 1,073.4/1,202.5 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1061 | 1,199.6 | 1,063.2/1,207.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1062 | 1,195.3 | 1,124.7/1,205.1 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1063 | 1,172.3 | 1,138.1/1,214.1 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1064 | 1,180.4 | 1,095.4/1,185.9 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1065 | 1,168.7 | 1,092.6/1,206.3 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1066 | 1,163.7 | 1,095.8/1,206.9 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1067 | 1,152.5 | 1,096.4/1,215.4 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1068 | 1,121.6 | 1,102.8/1,201.2 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1069 | 1,128.5 | 1,068.0/1,243.5 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1070 | 1,110.5 | 1,078.9/1,208.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1071 | 1,096.6 | 1,072.2/1,208.9 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1072 | 1,106.2 | 1,072.5/1,214.0 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1073 | 1,102.3 | 1,072.7/1,212.0 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1074 | 1,157.7 | 1,103.2/1,203.7 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1075 | 1,111.4 | 1,050.8/1,210.2 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1076 | 1,129.5 | 1,044.3/1,232.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1077 | 1,098.2 | 1,044.0/1,242.7 | 205.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1078 | 1,115.6 | 1,042.2/1,204.0 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1079 | 1,167.9 | 1,049.9/1,239.8 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1080 | 1,145.1 | 1,072.6/1,220.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1081 | 1,115.3 | 1,076.9/1,179.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1082 | 1,094.6 | 1,049.4/1,287.3 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1083 | 213.1 | 204.9/242.5 | 661.8 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1084 | 615.9 | 609.5/627.5 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1085 | 45.5 | 45.3/58.7 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1086 | 1,140.5 | 1,139.8/1,281.3 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1087 | 1,095.7 | 1,075.0/1,271.5 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1088 | 1,083.6 | 1,073.8/1,233.0 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1089 | 1,081.6 | 1,046.2/1,215.3 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1090 | 1,076.8 | 1,052.0/1,210.7 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1091 | 1,094.1 | 1,088.3/1,207.3 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1092 | 1,200.5 | 1,068.6/1,228.4 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1093 | 1,202.3 | 1,078.9/1,223.3 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1094 | 1,203.9 | 1,100.8/1,211.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1095 | 1,214.3 | 1,090.8/1,225.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1096 | 1,184.8 | 1,103.0/1,430.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1097 | 1,116.3 | 1,092.2/1,156.7 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1098 | 1,174.2 | 1,108.0/1,177.5 | 205.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1099 | 1,114.8 | 1,106.4/1,159.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1100 | 1,099.9 | 1,067.7/1,166.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1101 | 1,092.8 | 1,038.4/1,331.7 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1102 | 1,073.2 | 1,040.6/1,746.6 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1103 | 1,049.5 | 1,042.3/1,234.6 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1104 | 1,064.2 | 1,033.0/1,223.6 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1105 | 1,039.9 | 1,033.6/1,217.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1106 | 1,051.9 | 1,050.6/1,205.6 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1107 | 1,129.6 | 1,092.8/1,223.4 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1108 | 1,175.2 | 1,154.0/1,200.2 | 204.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1109 | 1,176.5 | 1,161.5/1,193.4 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1110 | 1,162.6 | 1,109.8/1,199.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1111 | 1,157.5 | 1,083.3/1,192.6 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1112 | 1,166.6 | 1,080.4/1,218.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1113 | 1,167.0 | 1,047.3/1,218.4 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1114 | 225.5 | 216.8/232.1 | 661.8 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1115 | 621.3 | 621.2/621.5 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1116 | 46.9 | 44.9/56.5 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1117 | 1,233.4 | 1,137.1/1,242.1 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1118 | 1,188.4 | 1,068.2/1,204.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1119 | 1,185.6 | 1,103.2/1,206.5 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1120 | 1,147.1 | 1,050.5/1,198.4 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1121 | 1,101.2 | 1,059.2/1,201.3 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1122 | 1,112.9 | 1,051.9/1,198.9 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1123 | 1,126.4 | 1,056.9/1,211.3 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1124 | 1,093.3 | 1,071.2/1,199.6 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1125 | 1,083.6 | 1,069.7/1,208.3 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1126 | 1,074.9 | 1,060.8/1,178.1 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1127 | 1,132.5 | 1,053.3/1,174.0 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1128 | 1,168.9 | 1,067.7/1,169.0 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1129 | 1,171.9 | 1,051.7/1,196.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1130 | 1,154.5 | 1,051.8/1,206.6 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1131 | 1,161.7 | 1,067.6/1,215.8 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1132 | 1,159.8 | 1,066.3/1,201.8 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1133 | 1,177.5 | 1,053.1/1,194.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1134 | 1,155.2 | 1,064.8/1,200.7 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1135 | 1,158.7 | 1,055.7/1,208.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1136 | 1,161.9 | 1,071.0/1,194.6 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1137 | 1,162.2 | 1,065.0/1,188.0 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1138 | 1,165.2 | 1,082.6/1,192.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1139 | 1,159.6 | 1,054.3/1,205.6 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1140 | 1,196.9 | 1,072.9/1,220.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1141 | 1,183.6 | 1,086.1/1,196.2 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1142 | 1,196.5 | 1,076.5/1,201.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1143 | 1,199.8 | 1,085.9/1,202.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1144 | 1,201.1 | 1,054.0/1,204.2 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1145 | 232.5 | 224.2/235.1 | 661.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1146 | 619.8 | 617.0/622.1 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1147 | 50.3 | 50.0/54.8 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1148 | 1,246.3 | 1,159.0/1,271.5 | 204.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1149 | 1,213.6 | 1,083.6/1,230.5 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1150 | 1,200.8 | 1,067.0/1,227.1 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1151 | 1,200.3 | 1,055.8/1,209.3 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1152 | 1,170.2 | 1,065.1/1,202.3 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1153 | 1,173.7 | 1,063.4/1,207.4 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1154 | 1,168.9 | 1,058.4/1,210.6 | 204.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1155 | 1,153.0 | 1,057.4/1,203.0 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1156 | 1,099.4 | 1,080.7/1,209.5 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1157 | 1,141.1 | 1,091.5/1,218.1 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1158 | 1,156.3 | 1,154.5/1,249.1 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1159 | 1,107.3 | 1,082.0/1,193.1 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1160 | 1,100.7 | 1,098.4/1,167.4 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1161 | 1,108.5 | 1,070.7/1,169.3 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1162 | 1,106.5 | 1,086.9/1,177.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1163 | 1,113.3 | 1,111.0/1,140.5 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1164 | 1,105.2 | 1,097.4/1,114.2 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1165 | 1,102.2 | 1,081.5/1,136.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1166 | 1,104.6 | 1,072.4/1,127.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1167 | 1,087.5 | 1,055.5/1,115.7 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1168 | 1,087.0 | 1,052.3/1,103.3 | 206.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1169 | 1,076.8 | 1,049.3/1,156.7 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1170 | 1,084.9 | 1,038.3/1,199.2 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1171 | 1,080.2 | 1,047.2/1,192.4 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1172 | 1,082.0 | 1,033.4/1,193.4 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1173 | 1,083.9 | 1,050.7/1,204.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1174 | 1,111.3 | 1,058.8/1,208.2 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1175 | 1,119.2 | 1,113.5/1,240.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1176 | 236.2 | 208.3/242.6 | 661.6 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1177 | 617.0 | 615.1/625.4 | 7.0 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1178 | 52.0 | 45.8/54.8 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1179 | 1,207.4 | 1,185.8/1,277.8 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1180 | 1,172.0 | 1,165.4/1,219.3 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1181 | 1,178.7 | 1,116.0/1,202.2 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1182 | 1,166.2 | 1,102.7/1,171.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1183 | 1,120.1 | 1,099.7/1,197.0 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1184 | 1,113.1 | 1,103.3/1,207.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1185 | 1,204.5 | 1,108.4/1,208.3 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1186 | 1,172.0 | 1,093.4/1,237.1 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1187 | 1,118.7 | 1,070.8/1,187.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1188 | 1,108.1 | 1,074.5/1,170.2 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1189 | 1,112.6 | 1,069.4/1,187.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1190 | 1,110.0 | 1,070.4/1,175.1 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1191 | 1,109.8 | 1,074.7/1,164.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1192 | 1,098.6 | 1,061.5/1,172.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1193 | 1,090.7 | 1,048.4/1,192.2 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1194 | 1,102.4 | 1,039.4/1,234.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1195 | 1,077.6 | 1,060.8/1,205.0 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1196 | 1,106.2 | 1,080.1/1,207.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1197 | 1,100.6 | 1,082.3/1,206.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1198 | 1,135.0 | 1,072.1/1,215.6 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1199 | 1,156.5 | 1,066.8/1,200.0 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1200 | 1,165.5 | 1,044.9/1,203.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1201 | 1,162.5 | 1,044.1/1,210.1 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1202 | 1,170.1 | 1,051.7/1,238.0 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1203 | 1,165.0 | 1,082.6/1,208.5 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1204 | 1,120.3 | 1,069.3/1,202.7 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1205 | 1,100.4 | 1,050.2/1,202.9 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1206 | 1,159.9 | 1,072.1/1,219.2 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1207 | 227.1 | 209.6/245.0 | 661.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1208 | 614.3 | 611.5/616.9 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1209 | 46.7 | 46.4/56.2 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1210 | 1,281.9 | 1,193.0/1,286.4 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1211 | 1,211.6 | 1,184.3/1,224.3 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1212 | 1,176.4 | 1,169.5/1,215.7 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1213 | 1,210.6 | 1,119.6/1,309.8 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1214 | 1,194.6 | 1,115.7/1,220.2 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1215 | 1,195.3 | 1,106.4/1,199.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1216 | 1,194.3 | 1,109.7/1,195.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1217 | 1,125.6 | 1,121.6/1,211.9 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1218 | 1,114.0 | 1,070.4/1,202.4 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1219 | 1,109.0 | 1,044.4/1,192.7 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1220 | 1,115.5 | 1,083.6/1,196.6 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1221 | 1,119.1 | 1,101.8/1,209.4 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1222 | 1,119.7 | 1,096.0/1,204.3 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1223 | 1,108.0 | 1,091.3/1,174.9 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1224 | 1,105.5 | 1,092.8/1,197.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1225 | 1,112.2 | 1,081.9/1,191.1 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1226 | 1,104.4 | 1,063.5/1,206.4 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1227 | 1,111.2 | 1,067.7/1,193.5 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1228 | 1,102.2 | 1,081.7/1,195.4 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1229 | 1,161.0 | 1,053.6/1,201.3 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1230 | 1,140.7 | 1,048.0/1,234.9 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1231 | 1,102.0 | 1,067.4/1,198.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1232 | 1,067.1 | 1,066.3/1,193.6 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1233 | 1,071.5 | 1,048.2/1,192.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1234 | 1,116.1 | 1,043.1/1,197.0 | 201.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1235 | 1,197.0 | 1,048.5/1,197.6 | 201.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1236 | 1,196.3 | 1,051.0/1,199.3 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1237 | 1,189.4 | 1,049.2/1,195.4 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1238 | 224.1 | 203.7/228.9 | 663.4 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1239 | 625.8 | 624.5/737.7 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1240 | 48.4 | 44.8/52.8 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1241 | 1,250.5 | 1,098.7/1,286.3 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1242 | 1,194.2 | 1,062.4/1,226.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1243 | 1,176.1 | 1,075.2/1,208.0 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1244 | 1,189.8 | 1,066.7/1,202.9 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1245 | 1,105.2 | 1,081.4/1,106.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1246 | 1,105.6 | 1,074.9/1,113.6 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1247 | 1,091.0 | 1,074.2/1,147.6 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1248 | 1,079.8 | 1,048.9/1,227.0 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1249 | 1,112.7 | 1,069.0/1,180.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1250 | 1,099.0 | 1,086.3/1,186.7 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1251 | 1,107.3 | 1,078.9/1,173.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1252 | 1,105.1 | 1,086.0/1,166.0 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1253 | 1,105.8 | 1,077.6/1,203.9 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1254 | 1,096.4 | 1,059.9/1,209.6 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1255 | 1,104.2 | 1,047.1/1,216.5 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1256 | 1,092.9 | 1,046.3/1,236.7 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1257 | 1,105.5 | 1,042.9/1,210.7 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1258 | 1,105.2 | 1,043.7/1,201.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1259 | 1,205.5 | 1,065.6/1,216.9 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1260 | 1,199.6 | 1,050.7/1,237.6 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1261 | 1,177.1 | 1,076.4/1,218.4 | 276.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1262 | 1,178.6 | 1,175.7/1,202.4 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1263 | 1,181.6 | 1,167.3/1,211.7 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1264 | 1,197.0 | 1,165.5/1,221.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1265 | 1,195.5 | 1,167.3/1,217.0 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1266 | 1,163.6 | 1,162.7/1,201.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1267 | 1,195.2 | 1,172.5/1,207.3 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1268 | 1,175.1 | 1,172.0/1,206.8 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1269 | 224.4 | 211.9/227.2 | 661.5 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1270 | 621.3 | 620.0/802.6 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1271 | 47.0 | 42.7/50.5 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1272 | 1,244.5 | 1,140.6/1,274.7 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1273 | 1,199.4 | 1,092.8/1,328.1 | 201.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1274 | 1,211.0 | 1,186.2/1,708.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1275 | 1,152.7 | 1,095.8/1,235.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1276 | 1,111.4 | 1,084.8/1,207.8 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1277 | 1,089.5 | 1,062.8/1,249.7 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1278 | 1,079.3 | 1,062.1/1,209.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1279 | 1,085.5 | 1,054.9/1,202.9 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1280 | 1,070.4 | 1,061.4/1,196.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1281 | 1,077.7 | 1,052.4/1,151.8 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1282 | 1,098.6 | 1,046.4/1,116.9 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1283 | 1,097.7 | 1,073.6/1,121.1 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1284 | 1,103.1 | 1,100.0/1,196.7 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1285 | 1,145.1 | 1,106.5/1,231.2 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1286 | 1,145.5 | 1,100.4/1,212.6 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1287 | 1,108.9 | 1,097.4/1,219.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1288 | 1,130.2 | 1,105.0/1,199.7 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1289 | 1,150.9 | 1,100.3/1,205.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1290 | 1,172.6 | 1,117.0/1,204.2 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1291 | 1,167.5 | 1,053.0/1,223.8 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1292 | 1,134.0 | 1,061.0/1,192.3 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1293 | 1,118.0 | 1,064.3/1,138.4 | 204.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1294 | 1,104.4 | 1,073.1/1,139.9 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1295 | 1,094.5 | 1,066.5/1,110.7 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1296 | 1,096.2 | 1,062.4/1,101.5 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1297 | 1,088.3 | 1,085.5/1,107.4 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1298 | 1,081.2 | 1,065.8/1,095.4 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1299 | 1,083.4 | 1,075.4/1,084.5 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1300 | 211.9 | 210.4/224.2 | 661.4 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1301 | 619.2 | 615.9/623.7 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1302 | 45.8 | 44.4/47.8 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1303 | 1,209.1 | 1,168.1/1,281.8 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1304 | 1,147.3 | 1,111.5/1,216.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1305 | 1,126.3 | 1,097.0/1,882.8 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1306 | 1,139.6 | 1,097.9/1,209.0 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1307 | 1,112.0 | 1,108.9/1,252.6 | 277.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1308 | 1,102.2 | 1,086.6/1,203.5 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1309 | 1,075.0 | 1,072.7/1,144.9 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1310 | 1,075.7 | 1,075.1/1,100.6 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1311 | 1,060.9 | 1,060.6/1,110.2 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1312 | 1,086.1 | 1,053.0/1,132.3 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1313 | 1,101.4 | 1,089.1/1,104.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1314 | 1,098.4 | 1,039.6/1,144.9 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1315 | 1,109.6 | 1,047.6/1,185.4 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1316 | 1,099.1 | 1,041.2/1,166.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1317 | 1,092.4 | 1,053.1/1,158.4 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1318 | 1,079.7 | 1,047.0/1,165.5 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1319 | 1,087.4 | 1,044.8/1,171.7 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1320 | 1,078.9 | 1,046.0/1,172.3 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1321 | 1,075.8 | 1,040.5/1,163.0 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1322 | 1,071.9 | 1,041.6/1,160.7 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1323 | 1,143.4 | 1,054.3/1,201.9 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1324 | 1,160.3 | 1,047.7/1,238.5 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1325 | 1,166.3 | 1,092.4/1,208.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1326 | 1,193.0 | 1,170.6/1,197.5 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1327 | 1,190.9 | 1,165.0/1,193.7 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1328 | 1,190.4 | 1,139.3/1,192.0 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1329 | 1,206.6 | 1,091.7/1,221.6 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1330 | 1,200.8 | 1,056.2/1,207.7 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1331 | 226.1 | 199.3/228.8 | 661.3 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1332 | 619.7 | 619.0/625.0 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1333 | 45.4 | 42.0/49.7 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1334 | 1,273.4 | 1,117.8/1,275.5 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1335 | 1,125.2 | 1,060.9/1,202.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1336 | 1,103.8 | 1,053.4/1,119.3 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1337 | 1,103.8 | 1,049.8/1,105.9 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1338 | 1,075.4 | 1,046.6/1,104.6 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1339 | 1,067.9 | 1,049.1/1,118.1 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1340 | 1,069.2 | 1,041.8/1,122.8 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1341 | 1,076.6 | 1,057.1/1,122.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1342 | 1,110.4 | 1,106.4/1,126.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1343 | 1,102.6 | 1,060.9/1,200.1 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1344 | 1,103.7 | 1,056.9/1,167.8 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1345 | 1,102.2 | 1,056.1/1,172.2 | 201.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1346 | 1,103.0 | 1,060.8/1,163.3 | 204.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1347 | 1,159.3 | 1,054.5/1,200.2 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1348 | 1,196.3 | 1,049.6/1,218.7 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1349 | 1,212.3 | 1,054.1/1,243.1 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1350 | 1,192.0 | 1,042.5/1,195.1 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1351 | 1,181.2 | 1,046.9/1,221.2 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1352 | 1,197.1 | 1,062.9/1,235.3 | 274.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1353 | 1,200.0 | 1,047.1/1,206.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1354 | 1,192.0 | 1,048.0/1,204.4 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1355 | 1,159.0 | 1,048.5/1,195.5 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1356 | 1,152.1 | 1,045.0/1,218.8 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1357 | 1,174.7 | 1,061.4/1,196.5 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1358 | 1,141.9 | 1,073.4/1,153.5 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1359 | 1,122.3 | 1,111.5/1,165.3 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1360 | 1,139.9 | 1,129.0/1,213.9 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1361 | 1,196.3 | 1,119.4/1,214.5 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1362 | 227.8 | 226.1/228.6 | 664.2 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1363 | 626.0 | 621.3/713.1 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1364 | 48.9 | 45.1/59.4 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1365 | 1,285.0 | 1,232.4/1,814.0 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1366 | 1,227.4 | 1,189.5/1,229.6 | 201.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1367 | 1,219.6 | 1,186.1/1,254.8 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1368 | 1,216.6 | 1,216.6/1,225.3 | 201.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1369 | 1,199.9 | 1,186.5/1,254.9 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1370 | 1,203.1 | 1,198.8/1,224.0 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1371 | 1,211.9 | 1,198.3/1,255.6 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1372 | 1,199.0 | 1,177.3/1,227.5 | 201.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1373 | 1,200.4 | 1,167.0/1,208.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1374 | 1,197.4 | 1,133.5/1,218.3 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1375 | 1,203.4 | 1,152.1/1,247.2 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1376 | 1,194.2 | 1,126.3/1,200.5 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1377 | 1,217.2 | 1,157.5/1,253.5 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1378 | 1,205.4 | 1,200.9/1,206.0 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1379 | 1,202.1 | 1,118.7/1,249.9 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1380 | 1,128.4 | 1,084.9/1,198.4 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1381 | 1,104.7 | 1,094.4/1,208.6 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1382 | 1,173.7 | 1,082.7/1,196.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1383 | 1,201.3 | 1,099.3/1,244.2 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1384 | 1,203.6 | 1,081.6/1,211.5 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1385 | 1,174.6 | 1,119.3/1,181.9 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1386 | 1,171.0 | 1,105.6/1,179.5 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1387 | 1,158.1 | 1,133.2/1,171.0 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1388 | 1,169.6 | 1,110.0/1,187.6 | 201.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1389 | 1,160.1 | 1,099.5/1,210.6 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1390 | 1,123.1 | 1,105.3/1,203.5 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1391 | 1,111.5 | 1,084.8/1,232.6 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1392 | 1,111.7 | 1,101.5/1,210.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1393 | 219.5 | 206.9/247.4 | 661.4 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1394 | 622.4 | 615.4/645.0 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1395 | 51.9 | 41.6/60.0 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1396 | 1,169.0 | 1,130.7/1,323.5 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1397 | 1,107.2 | 1,106.5/1,232.4 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1398 | 1,146.4 | 1,104.5/1,202.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1399 | 1,132.0 | 1,087.6/1,187.2 | 201.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1400 | 1,099.5 | 1,077.1/1,182.3 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1401 | 1,185.4 | 1,055.9/1,376.6 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1402 | 1,148.5 | 1,041.9/1,377.5 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1403 | 1,084.1 | 1,046.6/1,225.4 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1404 | 1,075.5 | 1,046.9/1,349.6 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1405 | 1,274.5 | 1,087.0/1,303.0 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1406 | 1,377.4 | 1,073.4/1,777.9 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1407 | 1,112.6 | 1,107.6/1,290.3 | 242.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1408 | 1,086.8 | 1,085.5/1,230.5 | 204.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1409 | 1,082.3 | 1,076.8/1,269.5 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1410 | 1,165.6 | 1,117.0/1,266.5 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1411 | 1,192.8 | 1,121.3/1,226.6 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1412 | 1,202.4 | 1,102.3/1,219.3 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1413 | 1,208.4 | 1,069.5/1,233.9 | 203.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1414 | 1,156.5 | 1,103.3/1,467.1 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1415 | 1,182.0 | 1,155.5/1,595.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1416 | 1,200.2 | 1,190.5/1,209.8 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1417 | 1,190.2 | 1,175.9/1,191.8 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1418 | 1,191.2 | 1,188.7/1,228.5 | 208.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1419 | 1,221.2 | 1,190.5/1,239.9 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1420 | 1,192.4 | 1,178.7/1,207.2 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1421 | 1,195.7 | 1,164.7/1,199.9 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1422 | 1,158.5 | 1,158.4/1,193.7 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1423 | 1,160.8 | 1,113.2/1,179.7 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1424 | 227.8 | 218.5/247.2 | 663.5 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1425 | 625.5 | 610.4/631.7 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1426 | 46.4 | 46.4/62.2 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1427 | 1,233.7 | 1,212.7/1,250.1 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1428 | 1,146.6 | 1,142.3/1,177.4 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1429 | 1,129.6 | 1,124.4/1,211.8 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1430 | 1,118.2 | 1,097.6/1,206.6 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1431 | 1,144.4 | 1,096.2/1,199.3 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1432 | 1,193.7 | 1,102.7/1,219.6 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1433 | 1,189.7 | 1,115.2/1,193.5 | 203.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1434 | 1,165.9 | 1,098.7/1,195.1 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1435 | 1,145.4 | 1,126.9/1,206.3 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1436 | 1,161.6 | 1,098.5/1,202.8 | 202.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1437 | 1,114.1 | 1,105.4/1,223.1 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1438 | 1,173.0 | 1,082.8/1,229.0 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1439 | 1,168.7 | 1,051.9/1,224.1 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1440 | 1,201.3 | 1,035.0/1,234.6 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1441 | 1,194.2 | 1,041.8/1,209.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1442 | 1,123.2 | 1,068.0/1,206.6 | 203.0 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1443 | 1,096.6 | 1,070.0/1,206.4 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1444 | 1,150.8 | 1,098.7/1,240.1 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1445 | 1,136.0 | 1,063.4/1,225.2 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1446 | 1,128.7 | 1,064.8/1,210.4 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1447 | 1,146.2 | 1,093.7/1,212.2 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1448 | 1,196.2 | 1,076.7/1,233.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1449 | 1,178.5 | 1,076.1/1,193.3 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1450 | 1,205.7 | 1,096.5/1,208.0 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1451 | 1,203.1 | 1,102.4/1,225.1 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1452 | 1,205.3 | 1,102.0/1,244.2 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1453 | 1,194.1 | 1,113.4/1,302.5 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1454 | 1,245.1 | 1,072.8/1,297.5 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1455 | 240.2 | 199.1/276.3 | 661.5 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1456 | 630.9 | 595.1/732.8 | 7.1 | cudaStreamSynchronize | 1 |
| plan | mir_operator:decode_embed | 1457 | 52.0 | 43.4/64.6 | 1.9 | cudaLaunchKernel | 1 |
| plan | mir_operator:decode_layer00 | 1458 | 1,262.0 | 1,129.9/1,544.6 | 203.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer01 | 1459 | 1,199.4 | 1,057.8/1,246.3 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer02 | 1460 | 1,204.5 | 1,049.5/1,246.8 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer03 | 1461 | 1,196.1 | 1,042.9/1,248.2 | 202.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer04 | 1462 | 1,200.7 | 1,051.3/1,258.6 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer05 | 1463 | 1,196.9 | 1,049.8/1,214.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer06 | 1464 | 1,222.8 | 1,086.3/1,235.9 | 203.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer07 | 1465 | 1,161.2 | 1,060.2/1,229.9 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer08 | 1466 | 1,163.3 | 1,052.3/1,241.5 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer09 | 1467 | 1,111.4 | 1,052.8/1,194.0 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer10 | 1468 | 1,102.8 | 1,039.8/1,210.6 | 201.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer11 | 1469 | 1,096.0 | 1,039.1/1,382.6 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer12 | 1470 | 1,096.3 | 1,064.2/1,379.8 | 277.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer13 | 1471 | 1,155.6 | 1,099.7/1,236.0 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer14 | 1472 | 1,160.3 | 1,080.9/1,312.0 | 202.9 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer15 | 1473 | 1,195.5 | 1,128.6/1,222.2 | 202.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer16 | 1474 | 1,174.2 | 1,099.6/1,211.5 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer17 | 1475 | 1,175.0 | 1,090.7/1,220.4 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer18 | 1476 | 1,200.5 | 1,106.7/1,205.4 | 203.2 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer19 | 1477 | 1,209.7 | 1,105.9/1,310.9 | 202.7 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer20 | 1478 | 1,223.3 | 1,108.4/1,391.0 | 202.5 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer21 | 1479 | 1,205.2 | 1,094.1/1,212.2 | 202.6 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer22 | 1480 | 1,218.3 | 1,100.6/1,218.3 | 203.1 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer23 | 1481 | 1,223.2 | 1,170.6/1,232.7 | 202.4 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer24 | 1482 | 1,198.0 | 1,187.0/1,215.6 | 202.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer25 | 1483 | 1,201.6 | 1,176.0/1,207.8 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer26 | 1484 | 1,203.9 | 1,167.6/1,212.3 | 203.3 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_layer27 | 1485 | 1,205.6 | 1,166.4/1,215.1 | 202.8 | cudaLaunchKernel | 57 |
| plan | mir_operator:decode_head | 1486 | 228.0 | 226.6/252.3 | 663.0 | cudaLaunchKernel | 9 |
| plan | mir_operator:decode_sample | 1487 | 617.3 | 606.3/619.9 | 7.1 | cudaStreamSynchronize | 1 |
| plan | pre_d2h_alloc |  | 249.4 | 212.6/320.4 | 0.7 | cudaMemcpyAsync | 0 |
| plan | d2h_stage |  | 136.4 | 129.3/140.0 | 0.9 | cudaEventRecordWithFlags | 0 |
| plan | checksum_complete |  | 48.3 | 46.8/48.8 | 0.0 | cudaEventDestroy | 0 |
| lookup | agent_tool_execute_cpu |  | 281.7 | 259.5/283.3 | 0.0 |  | 0 |
| answer | adapter_dispatch |  | 3.6 | 3.4/4.3 | 0.0 |  | 0 |
| answer | token_preprocess_cpu |  | 1,158.2 | 1,156.8/1,172.6 | 0.0 |  | 0 |
| answer | host_input_generate |  | 135.3 | 134.8/135.4 | 0.0 | cudaEventQuery | 0 |
| answer | h2d_stage |  | 136.1 | 128.6/147.3 | 0.4 | cudaEventRecordWithFlags | 0 |
| answer | weight_init |  | 194.5 | 176.0/230.9 | 0.0 | cudaEventDestroy | 0 |
| answer | mir_operator:prefill_embed | 0 | 101.5 | 93.2/108.6 | 1.8 | cudaLaunchKernel | 1 |
| answer | inter_operator_dispatch |  | 20.4 | 17.0/2,626.5 | 0.0 | cudaLaunchKernel | 0.32 |
| answer | mir_operator:prefill_layer00 | 1 | 1,745.2 | 1,725.9/1,781.4 | 369.0 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer01 | 2 | 1,614.7 | 1,612.8/1,619.9 | 344.6 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer02 | 3 | 1,345.2 | 1,329.8/1,350.3 | 344.5 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer03 | 4 | 1,311.3 | 1,295.9/1,314.1 | 342.4 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer04 | 5 | 1,282.5 | 1,280.6/1,294.9 | 345.3 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer05 | 6 | 1,170.8 | 1,127.6/1,274.8 | 342.7 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer06 | 7 | 1,177.0 | 1,114.5/1,256.0 | 352.4 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer07 | 8 | 1,175.3 | 1,124.9/1,199.8 | 358.8 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer08 | 9 | 1,191.7 | 1,159.4/1,262.8 | 344.0 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer09 | 10 | 1,183.3 | 1,129.2/1,264.5 | 344.0 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer10 | 11 | 1,209.4 | 1,121.0/1,253.1 | 346.1 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer11 | 12 | 1,218.0 | 1,212.7/1,294.4 | 342.9 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer12 | 13 | 1,254.7 | 1,253.6/1,280.2 | 346.5 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer13 | 14 | 1,245.4 | 1,243.0/1,280.2 | 344.4 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer14 | 15 | 1,243.0 | 1,209.1/1,277.2 | 344.0 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer15 | 16 | 1,270.9 | 1,260.6/1,361.6 | 343.4 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer16 | 17 | 1,270.2 | 1,189.8/1,316.5 | 344.4 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer17 | 18 | 1,217.0 | 1,183.0/1,291.2 | 345.8 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer18 | 19 | 1,268.1 | 1,202.1/1,270.1 | 346.6 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer19 | 20 | 1,219.5 | 1,186.5/1,265.3 | 344.4 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer20 | 21 | 1,244.2 | 1,168.9/1,276.4 | 345.5 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer21 | 22 | 1,243.0 | 1,159.6/1,286.7 | 343.8 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer22 | 23 | 1,255.0 | 1,164.1/1,302.9 | 344.6 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer23 | 24 | 1,186.8 | 1,150.1/1,330.5 | 343.3 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer24 | 25 | 1,267.1 | 1,183.6/1,306.9 | 344.2 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer25 | 26 | 1,245.3 | 1,182.9/1,307.9 | 343.4 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer26 | 27 | 1,242.9 | 1,234.7/1,315.1 | 343.3 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_layer27 | 28 | 1,234.1 | 1,205.2/1,291.1 | 344.3 | cudaLaunchKernel | 59 |
| answer | mir_operator:prefill_head | 29 | 240.7 | 239.3/268.0 | 1,044.5 | cudaLaunchKernel | 9 |
| answer | mir_operator:prefill_sample | 30 | 992.8 | 977.2/1,000.2 | 8.4 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 31 | 53.1 | 48.8/64.0 | 2.0 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 32 | 1,293.6 | 1,236.7/1,335.4 | 208.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 33 | 1,226.2 | 1,181.2/1,250.6 | 205.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 34 | 1,196.3 | 1,180.3/1,232.3 | 205.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 35 | 1,174.6 | 1,173.5/1,223.3 | 204.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 36 | 1,171.0 | 1,110.0/1,248.5 | 205.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 37 | 1,214.8 | 1,107.9/1,228.8 | 204.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 38 | 1,175.6 | 1,098.7/1,218.2 | 205.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 39 | 1,167.7 | 1,076.9/1,220.1 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 40 | 1,167.7 | 1,075.3/1,198.7 | 205.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 41 | 1,177.0 | 1,081.0/1,179.2 | 204.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 42 | 1,181.8 | 1,074.4/1,200.3 | 204.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 43 | 1,161.7 | 1,074.4/1,221.6 | 204.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 44 | 1,160.2 | 1,091.1/1,204.2 | 204.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 45 | 1,173.8 | 1,143.8/1,193.9 | 204.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 46 | 1,179.8 | 1,079.6/1,195.1 | 205.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 47 | 1,174.2 | 1,084.9/1,194.4 | 204.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 48 | 1,163.7 | 1,128.4/1,176.5 | 204.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 49 | 1,156.3 | 1,130.8/1,168.3 | 204.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 50 | 1,167.9 | 1,096.8/1,213.0 | 204.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 51 | 1,180.8 | 1,097.4/1,204.0 | 203.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 52 | 1,172.5 | 1,111.6/1,211.8 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 53 | 1,194.4 | 1,099.2/1,227.8 | 204.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 54 | 1,197.1 | 1,067.4/1,222.4 | 204.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 55 | 1,202.0 | 1,065.7/1,222.8 | 204.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 56 | 1,209.7 | 1,067.4/1,211.5 | 204.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 57 | 1,163.3 | 1,044.5/1,212.8 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 58 | 1,158.1 | 1,041.6/1,202.7 | 204.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 59 | 1,151.1 | 1,034.8/1,205.5 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 60 | 219.1 | 201.3/229.9 | 653.6 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 61 | 610.0 | 607.6/620.6 | 7.2 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 62 | 50.0 | 40.1/55.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 63 | 1,214.3 | 1,081.6/1,226.7 | 204.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 64 | 1,198.9 | 1,051.7/1,221.7 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 65 | 1,174.6 | 1,044.9/1,215.0 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 66 | 1,167.2 | 1,045.2/1,207.5 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 67 | 1,207.6 | 1,042.1/1,211.1 | 205.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 68 | 1,222.5 | 1,144.1/1,521.7 | 203.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 69 | 1,204.4 | 1,150.7/1,376.3 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 70 | 1,218.7 | 1,156.0/1,224.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 71 | 1,214.0 | 1,172.7/1,228.4 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 72 | 1,175.4 | 1,145.5/1,203.7 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 73 | 1,177.8 | 1,047.7/1,202.6 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 74 | 1,164.7 | 1,065.2/1,195.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 75 | 1,192.2 | 1,105.8/1,193.4 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 76 | 1,191.1 | 1,164.6/1,201.4 | 203.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 77 | 1,194.1 | 1,170.1/1,232.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 78 | 1,199.6 | 1,168.1/1,222.5 | 203.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 79 | 1,210.3 | 1,192.7/1,235.6 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 80 | 1,205.5 | 1,152.4/1,212.7 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 81 | 1,200.2 | 1,103.9/1,204.6 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 82 | 1,196.7 | 1,104.1/1,215.3 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 83 | 1,197.5 | 1,112.3/1,207.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 84 | 1,202.6 | 1,080.0/1,213.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 85 | 1,179.5 | 1,082.2/1,200.3 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 86 | 1,174.0 | 1,047.8/1,203.7 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 87 | 1,177.5 | 1,062.6/1,231.4 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 88 | 1,176.1 | 1,049.2/1,207.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 89 | 1,167.1 | 1,069.3/1,167.3 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 90 | 1,072.2 | 1,072.1/1,150.1 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 91 | 203.9 | 200.9/237.1 | 663.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 92 | 624.3 | 607.2/635.4 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 93 | 49.4 | 45.2/62.3 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 94 | 1,154.8 | 1,144.9/1,259.8 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 95 | 1,112.4 | 1,097.3/1,213.3 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 96 | 1,122.4 | 1,087.8/1,199.9 | 204.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 97 | 1,121.0 | 1,083.9/1,179.0 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 98 | 1,195.2 | 1,085.8/1,206.3 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 99 | 1,173.6 | 1,094.0/1,207.9 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 100 | 1,131.1 | 1,082.6/1,221.3 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 101 | 1,105.0 | 1,070.4/1,226.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 102 | 1,184.0 | 1,072.0/1,405.7 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 103 | 1,168.2 | 1,074.1/1,366.3 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 104 | 1,082.7 | 1,074.7/1,220.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 105 | 1,082.7 | 1,075.8/1,204.2 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 106 | 1,118.5 | 1,093.7/1,197.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 107 | 1,152.3 | 1,086.8/1,172.5 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 108 | 1,122.0 | 1,077.0/1,193.4 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 109 | 1,198.0 | 1,106.3/1,203.3 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 110 | 1,176.5 | 1,094.2/1,196.3 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 111 | 1,175.0 | 1,060.0/1,190.9 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 112 | 1,167.2 | 1,049.7/1,197.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 113 | 1,209.6 | 1,052.4/1,711.1 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 114 | 1,167.2 | 1,046.3/1,304.4 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 115 | 1,079.3 | 1,052.1/1,257.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 116 | 1,145.8 | 1,102.2/1,219.8 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 117 | 1,112.8 | 1,080.8/1,210.1 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 118 | 1,082.8 | 1,063.5/1,216.5 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 119 | 1,074.9 | 1,069.5/1,235.3 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 120 | 1,081.0 | 1,070.5/1,213.4 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 121 | 1,113.0 | 1,102.6/1,228.6 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 122 | 223.7 | 213.8/258.2 | 663.3 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 123 | 617.6 | 614.1/626.8 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 124 | 48.7 | 42.1/69.9 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 125 | 1,252.3 | 1,189.9/1,272.1 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 126 | 1,232.7 | 1,122.6/1,240.8 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 127 | 1,223.3 | 1,175.3/1,227.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 128 | 1,205.8 | 1,191.4/1,214.4 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 129 | 1,212.3 | 1,197.3/1,239.7 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 130 | 1,208.1 | 1,207.3/1,261.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 131 | 1,199.1 | 1,196.0/1,209.3 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 132 | 1,198.5 | 1,193.7/1,207.0 | 204.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 133 | 1,264.2 | 1,173.6/1,313.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 134 | 1,210.1 | 1,195.9/1,226.9 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 135 | 1,200.7 | 1,180.7/1,211.2 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 136 | 1,210.1 | 1,106.0/1,227.9 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 137 | 1,206.6 | 1,112.6/1,266.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 138 | 1,214.1 | 1,089.6/1,219.7 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 139 | 1,196.1 | 1,105.9/1,205.6 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 140 | 1,165.2 | 1,096.9/1,202.1 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 141 | 1,120.2 | 1,107.3/1,167.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 142 | 1,168.8 | 1,090.7/1,189.4 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 143 | 1,112.7 | 1,112.1/1,222.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 144 | 1,112.6 | 1,072.1/1,199.9 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 145 | 1,075.8 | 1,070.4/1,228.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 146 | 1,074.1 | 1,073.9/1,251.6 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 147 | 1,082.0 | 1,075.1/1,214.7 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 148 | 1,078.8 | 1,075.3/1,209.4 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 149 | 1,087.3 | 1,072.8/1,313.2 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 150 | 1,091.0 | 1,045.4/2,392.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 151 | 1,106.0 | 1,044.8/1,236.9 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 152 | 1,105.7 | 1,059.8/1,208.4 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 153 | 227.8 | 209.9/256.7 | 663.6 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 154 | 625.3 | 600.2/633.0 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 155 | 48.4 | 44.6/61.7 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 156 | 1,296.1 | 1,149.7/1,331.1 | 204.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 157 | 1,225.4 | 1,062.0/1,521.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 158 | 1,229.2 | 1,068.9/1,334.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 159 | 1,214.7 | 1,083.6/1,225.0 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 160 | 1,314.8 | 1,220.9/1,395.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 161 | 1,216.4 | 1,207.1/1,229.7 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 162 | 1,224.1 | 1,197.6/1,236.4 | 204.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 163 | 1,221.3 | 1,209.1/1,266.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 164 | 1,212.7 | 1,206.3/1,221.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 165 | 1,212.9 | 1,202.9/1,213.2 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 166 | 1,185.9 | 1,154.4/1,203.1 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 167 | 1,195.2 | 1,109.0/1,207.9 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 168 | 1,171.7 | 1,125.2/1,192.7 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 169 | 1,103.3 | 1,099.7/1,173.1 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 170 | 1,107.6 | 1,099.6/1,113.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 171 | 1,125.0 | 1,105.2/1,132.2 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 172 | 1,097.0 | 1,077.2/1,148.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 173 | 1,105.2 | 1,087.4/1,177.2 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 174 | 1,083.6 | 1,067.9/1,188.4 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 175 | 1,067.2 | 1,063.8/1,176.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 176 | 1,070.9 | 1,056.5/1,213.3 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 177 | 1,049.2 | 1,041.8/1,233.2 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 178 | 1,050.3 | 1,041.3/1,213.9 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 179 | 1,048.1 | 1,044.7/1,210.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 180 | 1,072.5 | 1,067.9/1,226.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 181 | 1,048.3 | 1,047.9/1,206.7 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 182 | 1,054.5 | 1,047.2/1,224.0 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 183 | 1,074.2 | 1,042.5/1,221.4 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 184 | 205.3 | 201.5/246.5 | 662.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 185 | 627.4 | 602.0/630.8 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 186 | 47.2 | 42.7/59.9 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 187 | 1,149.6 | 1,143.7/1,285.3 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 188 | 1,101.1 | 1,088.7/1,219.7 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 189 | 1,086.1 | 1,082.1/1,144.0 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 190 | 1,097.6 | 1,096.1/1,102.4 | 203.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 191 | 1,158.6 | 1,066.2/1,188.0 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 192 | 1,110.3 | 1,081.7/1,220.1 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 193 | 1,157.5 | 1,066.3/1,205.1 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 194 | 1,199.0 | 1,060.8/1,217.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 195 | 1,202.8 | 1,072.2/1,203.0 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 196 | 1,207.1 | 1,055.5/1,211.6 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 197 | 1,198.7 | 1,066.3/1,201.2 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 198 | 1,212.0 | 1,081.3/1,214.0 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 199 | 1,217.8 | 1,088.6/1,227.9 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 200 | 1,203.6 | 1,088.2/1,203.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 201 | 1,209.7 | 1,083.3/1,214.5 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 202 | 1,209.0 | 1,055.8/1,214.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 203 | 1,217.1 | 1,081.5/1,233.4 | 204.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 204 | 1,185.0 | 1,090.7/1,199.7 | 208.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 205 | 1,199.1 | 1,131.4/1,201.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 206 | 1,202.2 | 1,093.0/1,211.1 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 207 | 1,215.7 | 1,081.3/1,240.0 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 208 | 1,199.4 | 1,084.2/1,215.1 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 209 | 1,195.0 | 1,098.2/1,209.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 210 | 1,136.9 | 1,093.6/1,210.3 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 211 | 1,099.6 | 1,074.1/1,196.5 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 212 | 1,107.8 | 1,045.3/1,169.9 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 213 | 1,138.1 | 1,049.0/1,148.0 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 214 | 1,141.0 | 1,072.9/1,160.5 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 215 | 215.5 | 211.5/235.7 | 661.5 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 216 | 622.0 | 610.8/624.2 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 217 | 49.5 | 47.1/58.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 218 | 1,223.6 | 1,156.5/1,252.4 | 204.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 219 | 1,185.3 | 1,170.5/1,240.8 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 220 | 1,189.0 | 1,143.8/1,234.1 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 221 | 1,173.1 | 1,172.1/1,177.8 | 203.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 222 | 1,172.4 | 1,162.7/1,192.1 | 204.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 223 | 1,180.2 | 1,166.6/1,205.4 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 224 | 1,171.3 | 1,155.4/1,206.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 225 | 1,171.5 | 1,098.9/1,189.0 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 226 | 1,169.7 | 1,075.2/1,221.2 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 227 | 1,121.4 | 1,051.4/1,191.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 228 | 1,129.3 | 1,047.9/1,165.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 229 | 1,161.1 | 1,048.9/1,168.9 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 230 | 1,112.0 | 1,041.8/1,134.2 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 231 | 1,087.5 | 1,046.2/1,129.5 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 232 | 1,080.8 | 1,074.0/1,115.0 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 233 | 1,092.0 | 1,089.0/1,227.3 | 204.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 234 | 1,074.2 | 1,071.8/1,173.6 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 235 | 1,074.2 | 1,050.2/1,171.7 | 286.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 236 | 1,126.5 | 1,054.7/1,178.2 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 237 | 1,100.6 | 1,052.1/1,189.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 238 | 1,098.5 | 1,071.1/1,211.8 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 239 | 1,119.3 | 1,082.3/1,198.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 240 | 1,111.0 | 1,096.6/1,207.2 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 241 | 1,099.6 | 1,072.9/1,225.3 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 242 | 1,100.1 | 1,045.5/1,211.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 243 | 1,146.6 | 1,051.1/1,203.7 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 244 | 1,200.9 | 1,047.3/1,212.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 245 | 1,203.1 | 1,067.8/1,203.4 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 246 | 241.8 | 196.3/247.0 | 661.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 247 | 616.4 | 610.8/633.6 | 7.3 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 248 | 54.2 | 43.4/59.0 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 249 | 1,182.2 | 1,120.6/1,243.1 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 250 | 1,102.9 | 1,062.5/1,210.6 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 251 | 1,116.9 | 1,071.6/1,220.1 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 252 | 1,172.6 | 1,091.5/1,209.9 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 253 | 1,167.8 | 1,103.3/1,225.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 254 | 1,115.9 | 1,086.8/1,161.3 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 255 | 1,152.4 | 1,083.3/1,211.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 256 | 1,171.2 | 1,108.2/1,186.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 257 | 1,173.9 | 1,153.7/1,194.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 258 | 1,163.3 | 1,158.1/1,164.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 259 | 1,165.4 | 1,127.7/1,179.1 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 260 | 1,128.0 | 1,098.5/1,193.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 261 | 1,103.7 | 1,101.2/1,169.6 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 262 | 1,135.5 | 1,087.5/1,155.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 263 | 1,106.5 | 1,073.9/1,161.6 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 264 | 1,074.5 | 1,073.8/1,162.7 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 265 | 1,054.2 | 1,052.3/1,172.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 266 | 1,045.0 | 1,036.1/1,159.5 | 207.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 267 | 1,050.2 | 1,045.6/1,471.5 | 230.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 268 | 1,043.7 | 1,040.2/1,235.8 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 269 | 1,056.6 | 1,045.0/1,204.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 270 | 1,041.4 | 1,036.0/1,206.6 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 271 | 1,064.2 | 1,047.1/1,201.2 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 272 | 1,053.1 | 1,041.3/1,197.9 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 273 | 1,046.8 | 1,045.7/1,212.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 274 | 1,089.5 | 1,062.5/1,199.5 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 275 | 1,102.6 | 1,035.3/1,201.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 276 | 1,098.0 | 1,045.1/1,227.1 | 204.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 277 | 213.2 | 212.4/250.4 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 278 | 620.4 | 616.1/626.8 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 279 | 44.0 | 40.7/66.8 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 280 | 1,142.0 | 1,112.0/1,252.9 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 281 | 1,084.4 | 1,055.7/1,199.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 282 | 1,112.5 | 1,049.2/1,192.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 283 | 1,075.3 | 1,060.6/1,178.0 | 261.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 284 | 1,046.4 | 1,037.7/1,147.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 285 | 1,070.0 | 1,045.0/1,125.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 286 | 1,042.7 | 1,042.5/1,205.2 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 287 | 1,067.8 | 1,047.5/1,189.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 288 | 1,047.2 | 1,042.6/1,174.7 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 289 | 1,073.0 | 1,033.2/1,169.2 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 290 | 1,065.0 | 1,043.5/1,204.3 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 291 | 1,067.2 | 1,056.0/1,214.3 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 292 | 1,064.9 | 1,049.4/1,197.4 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 293 | 1,065.5 | 1,041.7/1,204.5 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 294 | 1,079.4 | 1,035.6/1,215.1 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 295 | 1,066.2 | 1,049.2/1,197.3 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 296 | 1,072.0 | 1,046.7/1,172.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 297 | 1,049.3 | 1,029.7/1,170.0 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 298 | 1,057.0 | 1,042.3/1,169.5 | 290.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 299 | 1,073.2 | 1,038.9/1,154.2 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 300 | 1,083.3 | 1,046.7/1,098.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 301 | 1,082.6 | 1,045.7/1,125.7 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 302 | 1,072.5 | 1,050.6/1,118.0 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 303 | 1,069.1 | 1,068.6/1,133.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 304 | 1,075.9 | 1,055.5/1,195.0 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 305 | 1,069.7 | 1,041.1/1,194.4 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 306 | 1,075.0 | 1,054.8/1,196.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 307 | 1,071.3 | 1,064.1/1,205.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 308 | 210.5 | 200.7/227.7 | 662.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 309 | 610.0 | 609.6/613.9 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 310 | 45.9 | 40.7/49.8 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 311 | 1,183.5 | 1,097.9/1,278.2 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 312 | 1,148.8 | 1,130.6/1,226.3 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 313 | 1,176.5 | 1,122.3/1,218.8 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 314 | 1,207.7 | 1,147.7/1,228.2 | 201.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 315 | 1,198.5 | 1,121.6/1,206.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 316 | 1,192.2 | 1,105.0/1,196.7 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 317 | 1,202.2 | 1,098.2/1,207.9 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 318 | 1,206.3 | 1,106.2/1,213.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 319 | 1,184.7 | 1,098.4/1,191.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 320 | 1,160.5 | 1,101.7/1,197.0 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 321 | 1,173.2 | 1,091.2/1,191.3 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 322 | 1,164.0 | 1,120.2/1,257.5 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 323 | 1,180.9 | 1,102.9/1,189.8 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 324 | 1,168.3 | 1,095.9/1,173.6 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 325 | 1,158.8 | 1,092.5/1,169.7 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 326 | 1,170.1 | 1,078.6/1,188.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 327 | 1,165.8 | 1,084.1/1,166.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 328 | 1,167.2 | 1,101.9/1,187.2 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 329 | 1,170.5 | 1,145.2/1,170.9 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 330 | 1,177.4 | 1,141.2/1,187.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 331 | 1,197.7 | 1,180.0/1,383.7 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 332 | 1,195.1 | 1,162.0/1,396.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 333 | 1,202.2 | 1,174.1/1,209.1 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 334 | 1,166.9 | 1,156.0/1,199.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 335 | 1,160.3 | 1,131.3/1,202.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 336 | 1,140.0 | 1,091.5/1,214.9 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 337 | 1,208.9 | 1,094.7/1,235.0 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 338 | 1,199.5 | 1,091.5/1,217.6 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 339 | 235.7 | 217.7/242.9 | 661.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 340 | 614.1 | 612.7/632.0 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 341 | 50.4 | 41.1/54.8 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 342 | 1,273.9 | 1,177.7/1,298.5 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 343 | 1,192.3 | 1,111.2/1,232.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 344 | 1,176.4 | 1,133.1/1,215.2 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 345 | 1,174.5 | 1,157.9/1,222.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 346 | 1,192.5 | 1,150.5/1,226.1 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 347 | 1,160.8 | 1,098.6/1,194.6 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 348 | 1,162.2 | 1,116.1/1,162.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 349 | 1,159.2 | 1,129.8/1,172.4 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 350 | 1,179.0 | 1,113.6/1,221.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 351 | 1,205.5 | 1,118.1/1,256.3 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 352 | 1,205.5 | 1,101.6/1,604.3 | 201.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 353 | 1,209.4 | 1,108.0/1,777.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 354 | 1,164.0 | 1,121.8/1,218.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 355 | 1,170.5 | 1,161.3/1,226.7 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 356 | 1,193.4 | 1,139.3/1,202.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 357 | 1,206.0 | 1,144.7/1,234.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 358 | 1,174.1 | 1,139.6/1,200.8 | 296.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 359 | 1,183.9 | 1,117.0/1,200.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 360 | 1,143.8 | 1,105.0/1,198.4 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 361 | 1,164.5 | 1,109.8/1,199.2 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 362 | 1,159.3 | 1,116.5/1,195.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 363 | 1,181.8 | 1,109.5/1,204.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 364 | 1,146.6 | 1,140.6/1,194.9 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 365 | 1,164.1 | 1,158.5/1,213.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 366 | 1,165.0 | 1,148.4/1,217.8 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 367 | 1,153.3 | 1,132.4/1,170.1 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 368 | 1,163.0 | 1,115.9/1,183.4 | 204.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 369 | 1,136.9 | 1,110.1/1,186.7 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 370 | 234.2 | 217.5/245.8 | 662.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 371 | 616.6 | 615.9/620.8 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 372 | 52.5 | 51.2/61.4 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 373 | 1,288.5 | 1,171.6/1,295.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 374 | 1,192.4 | 1,092.8/1,234.3 | 226.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 375 | 1,124.4 | 1,084.8/1,178.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 376 | 1,143.9 | 1,108.2/1,148.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 377 | 1,105.1 | 1,098.4/1,146.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 378 | 1,119.3 | 1,075.5/1,123.9 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 379 | 1,101.7 | 1,078.7/1,118.1 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 380 | 1,110.7 | 1,061.4/1,110.8 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 381 | 1,098.9 | 1,060.3/1,109.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 382 | 1,091.7 | 1,051.7/1,120.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 383 | 1,081.3 | 1,046.0/1,105.6 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 384 | 1,081.1 | 1,044.4/1,094.9 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 385 | 1,113.6 | 1,069.2/1,136.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 386 | 1,081.7 | 1,050.9/1,089.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 387 | 1,074.6 | 1,048.4/1,081.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 388 | 1,080.2 | 1,044.7/1,086.0 | 207.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 389 | 1,082.5 | 1,037.8/1,155.6 | 204.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 390 | 1,074.5 | 1,047.3/1,166.0 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 391 | 1,070.9 | 1,056.3/1,180.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 392 | 1,077.8 | 1,070.2/1,164.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 393 | 1,083.0 | 1,069.4/1,160.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 394 | 1,135.2 | 1,090.2/1,172.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 395 | 1,113.7 | 1,073.2/1,163.9 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 396 | 1,156.8 | 1,128.4/1,191.0 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 397 | 1,172.5 | 1,098.4/1,200.9 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 398 | 1,115.4 | 1,097.7/1,196.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 399 | 1,138.4 | 1,101.5/1,231.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 400 | 1,127.8 | 1,102.8/1,201.1 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 401 | 234.9 | 225.3/279.4 | 662.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 402 | 621.7 | 602.4/695.9 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 403 | 49.8 | 43.3/66.8 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 404 | 1,253.3 | 1,151.8/1,253.7 | 204.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 405 | 1,172.8 | 1,101.5/1,230.6 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 406 | 1,182.9 | 1,073.5/1,212.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 407 | 1,184.2 | 1,047.7/1,209.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 408 | 1,212.8 | 1,041.7/1,215.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 409 | 1,210.9 | 1,047.1/1,232.2 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 410 | 1,188.4 | 1,059.0/1,228.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 411 | 1,163.9 | 1,041.1/1,194.8 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 412 | 1,150.8 | 1,045.7/1,171.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 413 | 1,104.6 | 1,040.1/1,180.0 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 414 | 1,111.2 | 1,080.8/1,164.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 415 | 1,101.1 | 1,046.0/1,110.7 | 201.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 416 | 1,141.9 | 1,044.6/1,159.2 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 417 | 1,119.7 | 1,040.8/1,177.3 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 418 | 1,106.7 | 1,037.8/1,167.8 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 419 | 1,095.4 | 1,039.3/1,253.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 420 | 1,077.5 | 1,039.2/1,202.6 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 421 | 1,106.1 | 1,068.5/1,232.7 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 422 | 1,187.8 | 1,071.3/1,216.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 423 | 1,209.5 | 1,099.7/1,224.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 424 | 1,196.7 | 1,107.1/1,211.7 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 425 | 1,186.5 | 1,122.0/1,197.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 426 | 1,212.0 | 1,191.1/1,523.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 427 | 1,220.5 | 1,209.0/1,750.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 428 | 1,196.6 | 1,187.0/1,751.1 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 429 | 1,207.4 | 1,158.3/1,768.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 430 | 1,197.5 | 1,091.6/1,790.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 431 | 1,214.6 | 1,108.8/1,779.2 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 432 | 233.3 | 228.4/357.6 | 664.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 433 | 671.9 | 574.4/732.9 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 434 | 54.9 | 50.9/92.9 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 435 | 1,283.3 | 1,232.1/1,497.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 436 | 1,206.4 | 1,180.1/1,222.6 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 437 | 1,164.9 | 1,117.1/1,174.8 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 438 | 1,152.0 | 1,104.3/1,170.0 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 439 | 1,163.3 | 1,090.8/1,166.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 440 | 1,165.2 | 1,106.9/1,197.2 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 441 | 1,175.2 | 1,102.7/1,195.1 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 442 | 1,113.1 | 1,112.6/1,227.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 443 | 1,126.4 | 1,106.2/1,196.7 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 444 | 1,112.9 | 1,106.7/1,195.9 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 445 | 1,122.5 | 1,116.3/1,217.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 446 | 1,102.1 | 1,097.7/1,215.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 447 | 1,103.6 | 1,091.0/1,209.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 448 | 1,116.3 | 1,103.3/1,200.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 449 | 1,182.2 | 1,132.1/1,199.2 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 450 | 1,169.3 | 1,130.3/1,226.4 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 451 | 1,195.7 | 1,095.0/1,218.8 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 452 | 1,202.1 | 1,087.5/1,202.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 453 | 1,193.4 | 1,107.9/1,234.3 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 454 | 1,200.5 | 1,081.7/1,200.8 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 455 | 1,196.4 | 1,084.9/1,204.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 456 | 1,195.4 | 1,098.9/1,196.1 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 457 | 1,186.3 | 1,095.3/1,207.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 458 | 1,180.3 | 1,060.6/1,216.6 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 459 | 1,115.1 | 1,063.4/1,195.7 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 460 | 1,105.7 | 1,065.1/1,176.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 461 | 1,104.5 | 1,070.7/1,118.3 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 462 | 1,099.1 | 1,060.8/1,099.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 463 | 212.8 | 210.2/225.3 | 662.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 464 | 619.9 | 617.5/664.7 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 465 | 49.3 | 44.4/57.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 466 | 1,150.6 | 1,127.2/1,160.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 467 | 1,098.5 | 1,083.7/1,099.0 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 468 | 1,108.9 | 1,070.4/1,116.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 469 | 1,109.0 | 1,081.1/1,135.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 470 | 1,105.2 | 1,079.6/1,106.2 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 471 | 1,075.0 | 1,070.6/1,110.8 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 472 | 1,075.5 | 1,070.5/1,104.2 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 473 | 1,073.2 | 1,068.4/1,086.3 | 203.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 474 | 1,086.5 | 1,048.0/1,099.0 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 475 | 1,075.6 | 1,064.6/1,135.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 476 | 1,073.5 | 1,063.5/1,116.3 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 477 | 1,066.5 | 1,055.8/1,096.8 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 478 | 1,081.4 | 1,063.7/1,099.8 | 252.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 479 | 1,073.9 | 1,071.8/1,094.3 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 480 | 1,086.3 | 1,076.5/1,127.7 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 481 | 1,089.7 | 1,068.0/1,126.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 482 | 1,090.6 | 1,080.3/1,191.0 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 483 | 1,099.0 | 1,055.4/1,182.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 484 | 1,117.8 | 1,045.7/1,170.3 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 485 | 1,107.4 | 1,040.1/1,176.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 486 | 1,080.1 | 1,043.4/1,176.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 487 | 1,090.3 | 1,056.2/1,179.2 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 488 | 1,066.3 | 1,041.1/1,176.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 489 | 1,068.7 | 1,045.9/1,157.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 490 | 1,067.2 | 1,048.4/1,174.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 491 | 1,096.5 | 1,048.0/1,171.6 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 492 | 1,083.5 | 1,044.3/1,206.6 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 493 | 1,101.8 | 1,049.2/1,171.4 | 282.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 494 | 209.7 | 197.6/233.6 | 662.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 495 | 618.2 | 615.9/631.1 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 496 | 46.3 | 41.4/55.6 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 497 | 1,175.9 | 1,108.2/1,230.5 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 498 | 1,115.7 | 1,083.3/1,125.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 499 | 1,115.5 | 1,051.0/1,182.9 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 500 | 1,099.3 | 1,055.2/1,112.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 501 | 1,103.8 | 1,049.4/1,114.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 502 | 1,100.0 | 1,048.3/1,108.9 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 503 | 1,096.6 | 1,040.7/1,109.6 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 504 | 1,074.9 | 1,048.1/1,115.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 505 | 1,045.9 | 1,041.3/1,104.2 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 506 | 1,103.3 | 1,042.2/1,120.2 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 507 | 1,082.3 | 1,045.2/1,110.5 | 201.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 508 | 1,049.5 | 1,047.9/1,099.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 509 | 1,050.2 | 1,044.9/1,106.1 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 510 | 1,062.5 | 1,042.8/1,111.9 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 511 | 1,057.4 | 1,044.1/1,095.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 512 | 1,038.6 | 1,034.2/1,062.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 513 | 1,054.7 | 1,052.7/1,055.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 514 | 1,054.8 | 1,051.0/1,087.1 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 515 | 1,069.4 | 1,044.7/1,160.6 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 516 | 1,081.3 | 1,039.5/1,194.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 517 | 1,095.7 | 1,057.1/1,199.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 518 | 1,106.4 | 1,046.5/1,200.7 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 519 | 1,110.3 | 1,068.6/1,208.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 520 | 1,196.0 | 1,183.8/1,207.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 521 | 1,214.4 | 1,204.9/1,221.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 522 | 1,203.3 | 1,196.0/1,215.9 | 205.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 523 | 1,195.7 | 1,195.5/1,199.7 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 524 | 1,199.2 | 1,191.1/1,200.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 525 | 233.3 | 227.0/242.8 | 662.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 526 | 619.8 | 619.7/623.9 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 527 | 50.4 | 46.9/50.7 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 528 | 1,259.0 | 1,237.4/1,279.6 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 529 | 1,217.2 | 1,204.4/1,219.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 530 | 1,177.8 | 1,167.2/1,210.3 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 531 | 1,200.4 | 1,115.5/1,210.9 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 532 | 1,199.1 | 1,138.3/1,200.8 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 533 | 1,199.3 | 1,183.0/1,208.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 534 | 1,180.9 | 1,172.5/1,209.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 535 | 1,166.3 | 1,140.6/1,226.6 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 536 | 1,122.1 | 1,097.9/1,201.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 537 | 1,167.0 | 1,129.6/1,209.1 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 538 | 1,206.4 | 1,170.3/1,213.7 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 539 | 1,197.2 | 1,151.6/1,218.2 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 540 | 1,208.0 | 1,108.8/1,212.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 541 | 1,195.5 | 1,099.9/1,209.9 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 542 | 1,197.5 | 1,117.5/1,201.6 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 543 | 1,193.1 | 1,094.0/1,230.9 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 544 | 1,196.0 | 1,076.3/1,206.7 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 545 | 1,196.1 | 1,084.0/1,205.0 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 546 | 1,196.2 | 1,073.6/1,214.3 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 547 | 1,184.5 | 1,073.3/1,203.9 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 548 | 1,123.7 | 1,044.6/1,196.3 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 549 | 1,162.2 | 1,046.1/1,200.9 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 550 | 1,165.3 | 1,055.6/1,195.9 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 551 | 1,199.3 | 1,055.7/1,215.0 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 552 | 1,161.2 | 1,073.1/1,196.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 553 | 1,105.0 | 1,093.7/1,164.7 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 554 | 1,113.6 | 1,051.6/1,177.2 | 268.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 555 | 1,121.5 | 1,046.8/1,146.0 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 556 | 223.5 | 200.8/234.2 | 662.5 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 557 | 622.7 | 622.5/630.2 | 7.3 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 558 | 47.6 | 41.6/51.6 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 559 | 1,165.6 | 1,130.6/1,232.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 560 | 1,107.9 | 1,065.2/1,219.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 561 | 1,083.1 | 1,057.8/1,215.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 562 | 1,087.0 | 1,066.7/1,247.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 563 | 1,072.5 | 1,069.0/1,203.2 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 564 | 1,091.2 | 1,057.7/1,206.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 565 | 1,135.2 | 1,048.9/1,202.3 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 566 | 1,152.2 | 1,044.0/1,219.1 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 567 | 1,204.8 | 1,045.8/1,211.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 568 | 1,175.6 | 1,038.7/1,205.3 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 569 | 1,123.5 | 1,045.5/1,198.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 570 | 1,089.7 | 1,047.4/1,187.4 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 571 | 1,099.7 | 1,045.8/1,183.1 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 572 | 1,093.1 | 1,043.1/1,166.3 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 573 | 1,097.4 | 1,048.4/1,166.2 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 574 | 1,132.5 | 1,045.7/1,148.8 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 575 | 1,093.4 | 1,047.1/1,114.5 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 576 | 1,063.5 | 1,045.5/1,158.5 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 577 | 1,111.0 | 1,054.5/1,183.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 578 | 1,062.5 | 1,045.0/1,104.7 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 579 | 1,081.1 | 1,038.3/1,125.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 580 | 1,066.0 | 1,047.9/1,131.2 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 581 | 1,097.7 | 1,053.7/1,102.6 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 582 | 1,099.1 | 1,044.2/1,108.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 583 | 1,108.0 | 1,044.4/1,118.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 584 | 1,114.9 | 1,043.4/1,118.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 585 | 1,096.2 | 1,049.6/1,098.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 586 | 1,095.9 | 1,044.3/1,099.7 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 587 | 226.6 | 195.5/227.3 | 662.3 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 588 | 623.2 | 622.8/631.4 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 589 | 45.4 | 39.7/58.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 590 | 1,139.9 | 1,105.3/1,214.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 591 | 1,083.2 | 1,063.1/1,190.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 592 | 1,053.6 | 1,050.5/1,176.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 593 | 1,052.6 | 1,052.1/1,178.9 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 594 | 1,075.7 | 1,046.1/1,165.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 595 | 1,070.3 | 1,046.7/1,139.3 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 596 | 1,050.0 | 1,047.1/1,110.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 597 | 1,065.0 | 1,042.1/1,131.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 598 | 1,100.4 | 1,046.0/1,139.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 599 | 1,093.2 | 1,047.3/1,163.4 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 600 | 1,075.9 | 1,052.7/1,180.7 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 601 | 1,071.9 | 1,070.2/1,156.3 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 602 | 1,101.6 | 1,075.4/1,102.0 | 203.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 603 | 1,107.1 | 1,082.2/1,200.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 604 | 1,117.2 | 1,093.5/1,223.7 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 605 | 1,159.0 | 1,102.6/1,207.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 606 | 1,169.9 | 1,130.8/1,201.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 607 | 1,124.9 | 1,104.5/1,203.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 608 | 1,107.0 | 1,095.1/1,204.9 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 609 | 1,101.9 | 1,096.0/1,204.3 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 610 | 1,127.9 | 1,097.0/1,202.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 611 | 1,116.7 | 1,092.9/1,217.6 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 612 | 1,096.5 | 1,096.1/1,225.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 613 | 1,101.9 | 1,088.3/1,204.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 614 | 1,103.3 | 1,074.1/1,211.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 615 | 1,196.4 | 1,094.1/1,210.5 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 616 | 1,197.1 | 1,086.0/1,199.2 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 617 | 1,203.2 | 1,074.9/1,224.5 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 618 | 225.2 | 203.2/256.3 | 661.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 619 | 613.6 | 612.4/624.9 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 620 | 48.0 | 47.5/61.1 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 621 | 1,293.3 | 1,160.0/1,316.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 622 | 1,219.2 | 1,091.4/1,267.1 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 623 | 1,210.5 | 1,084.4/1,218.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 624 | 1,209.7 | 1,079.7/1,216.3 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 625 | 1,167.5 | 1,097.2/1,230.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 626 | 1,165.9 | 1,164.7/1,231.0 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 627 | 1,197.3 | 1,160.6/1,227.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 628 | 1,205.3 | 1,162.4/1,211.8 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 629 | 1,205.9 | 1,134.3/1,239.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 630 | 1,223.2 | 1,099.4/1,226.1 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 631 | 1,180.2 | 1,121.9/1,219.6 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 632 | 1,167.1 | 1,158.8/1,204.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 633 | 1,175.6 | 1,168.2/1,195.8 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 634 | 1,179.2 | 1,162.0/1,222.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 635 | 1,210.5 | 1,167.5/1,219.8 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 636 | 1,196.5 | 1,169.2/1,217.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 637 | 1,203.7 | 1,186.1/1,239.2 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 638 | 1,200.5 | 1,193.1/1,232.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 639 | 1,204.6 | 1,197.9/1,218.8 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 640 | 1,205.2 | 1,173.6/1,217.8 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 641 | 1,179.4 | 1,158.3/1,204.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 642 | 1,200.5 | 1,156.5/1,223.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 643 | 1,167.5 | 1,154.2/1,226.5 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 644 | 1,161.9 | 1,110.7/1,225.7 | 267.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 645 | 1,133.8 | 1,112.2/1,202.5 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 646 | 1,201.8 | 1,115.0/1,234.2 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 647 | 1,123.8 | 1,088.2/1,205.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 648 | 1,091.5 | 1,067.8/1,214.3 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 649 | 232.0 | 203.0/240.5 | 661.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 650 | 618.3 | 597.8/626.8 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 651 | 57.0 | 41.5/57.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 652 | 1,164.1 | 1,150.0/1,306.3 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 653 | 1,128.2 | 1,115.1/1,224.6 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 654 | 1,128.5 | 1,108.1/1,212.7 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 655 | 1,167.4 | 1,118.4/1,205.9 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 656 | 1,200.2 | 1,109.9/1,228.1 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 657 | 1,215.6 | 1,106.8/1,219.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 658 | 1,203.2 | 1,105.2/1,203.5 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 659 | 1,213.2 | 1,105.8/1,215.6 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 660 | 1,189.2 | 1,108.2/1,216.1 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 661 | 1,198.5 | 1,085.9/1,209.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 662 | 1,174.6 | 1,100.9/1,210.5 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 663 | 1,177.0 | 1,078.9/1,211.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 664 | 1,169.2 | 1,075.6/1,225.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 665 | 1,181.9 | 1,053.7/1,239.6 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 666 | 1,175.3 | 1,066.0/1,177.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 667 | 1,166.6 | 1,065.1/1,181.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 668 | 1,176.7 | 1,064.1/1,181.3 | 201.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 669 | 1,127.5 | 1,061.5/1,192.4 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 670 | 1,170.2 | 1,120.3/1,176.6 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 671 | 1,179.3 | 1,099.0/1,206.9 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 672 | 1,205.9 | 1,076.6/1,222.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 673 | 1,195.3 | 1,074.5/1,222.1 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 674 | 1,088.7 | 1,068.9/1,211.7 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 675 | 1,111.5 | 1,077.5/1,220.4 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 676 | 1,113.3 | 1,042.5/1,207.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 677 | 1,118.2 | 1,045.3/1,245.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 678 | 1,165.4 | 1,041.3/1,198.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 679 | 1,171.1 | 1,040.8/1,202.6 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 680 | 237.0 | 195.6/257.3 | 663.5 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 681 | 622.9 | 609.3/630.4 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 682 | 55.1 | 39.6/60.3 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 683 | 1,271.2 | 1,118.0/1,289.7 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 684 | 1,151.7 | 1,058.6/1,280.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 685 | 1,219.7 | 1,046.4/1,504.1 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 686 | 1,119.7 | 1,048.5/1,224.6 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 687 | 1,141.7 | 1,045.1/1,242.3 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 688 | 1,116.5 | 1,061.5/1,217.2 | 244.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 689 | 1,097.0 | 1,092.4/1,168.9 | 205.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 690 | 1,096.8 | 1,068.3/1,180.4 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 691 | 1,132.8 | 1,112.2/1,167.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 692 | 1,164.3 | 1,124.2/1,174.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 693 | 1,170.3 | 1,105.0/1,181.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 694 | 1,166.5 | 1,155.7/1,169.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 695 | 1,215.5 | 1,174.1/1,220.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 696 | 1,167.4 | 1,164.8/1,456.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 697 | 1,162.5 | 1,161.2/1,519.8 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 698 | 1,174.5 | 1,160.7/1,539.2 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 699 | 1,178.9 | 1,160.0/1,212.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 700 | 1,178.9 | 1,159.7/1,205.1 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 701 | 1,179.8 | 1,166.7/1,228.1 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 702 | 1,197.3 | 1,119.1/1,547.0 | 305.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 703 | 1,208.9 | 1,132.0/1,241.3 | 205.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 704 | 1,205.3 | 1,143.4/1,214.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 705 | 1,186.8 | 1,109.9/1,197.8 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 706 | 1,176.8 | 1,097.6/1,194.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 707 | 1,157.6 | 1,097.0/1,213.7 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 708 | 1,159.4 | 1,094.7/1,206.3 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 709 | 1,161.4 | 1,146.9/1,184.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 710 | 1,162.3 | 1,140.0/1,164.4 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 711 | 233.6 | 230.7/272.4 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 712 | 617.1 | 614.0/619.3 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 713 | 55.4 | 50.2/58.1 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 714 | 1,264.4 | 1,155.3/1,296.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 715 | 1,188.3 | 1,160.0/1,196.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 716 | 1,177.8 | 1,136.5/1,208.2 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 717 | 1,170.4 | 1,102.4/1,219.6 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 718 | 1,171.6 | 1,092.6/1,232.7 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 719 | 1,169.7 | 1,098.2/1,209.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 720 | 1,205.2 | 1,096.8/1,217.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 721 | 1,205.3 | 1,108.2/1,212.6 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 722 | 1,216.5 | 1,093.9/1,235.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 723 | 1,205.6 | 1,120.2/1,208.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 724 | 1,209.3 | 1,105.3/1,209.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 725 | 1,207.8 | 1,096.4/1,275.9 | 201.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 726 | 1,219.4 | 1,093.1/1,390.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 727 | 1,210.0 | 1,083.8/1,212.1 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 728 | 1,177.0 | 1,111.8/1,229.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 729 | 1,173.3 | 1,050.6/1,212.2 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 730 | 1,169.6 | 1,036.1/1,242.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 731 | 1,196.8 | 1,034.7/1,198.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 732 | 1,171.4 | 1,083.6/1,217.7 | 207.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 733 | 1,202.1 | 1,079.9/1,215.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 734 | 1,198.3 | 1,100.2/1,204.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 735 | 1,197.0 | 1,107.4/1,228.0 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 736 | 1,159.5 | 1,103.6/1,213.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 737 | 1,170.7 | 1,098.1/1,205.8 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 738 | 1,202.8 | 1,095.5/1,405.6 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 739 | 1,202.0 | 1,095.6/1,248.8 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 740 | 1,211.3 | 1,093.7/1,226.4 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 741 | 1,203.4 | 1,109.8/1,220.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 742 | 243.8 | 223.8/253.7 | 661.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 743 | 611.8 | 608.8/620.8 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 744 | 57.0 | 43.0/62.3 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 745 | 1,301.8 | 1,120.9/1,329.4 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 746 | 1,228.4 | 1,062.8/1,232.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 747 | 1,222.7 | 1,047.4/1,234.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 748 | 1,191.9 | 1,042.5/1,219.3 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 749 | 1,188.4 | 1,044.0/1,209.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 750 | 1,117.2 | 1,051.7/1,210.5 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 751 | 1,130.5 | 1,044.5/1,208.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 752 | 1,217.3 | 1,061.4/1,229.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 753 | 1,205.5 | 1,070.7/1,247.4 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 754 | 1,200.3 | 1,058.1/1,213.0 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 755 | 1,188.8 | 1,044.5/1,190.8 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 756 | 1,219.5 | 1,050.5/2,204.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 757 | 1,226.1 | 1,045.3/1,366.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 758 | 1,202.9 | 1,042.8/1,227.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 759 | 1,199.6 | 1,042.8/1,206.9 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 760 | 1,205.3 | 1,046.1/1,233.3 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 761 | 1,230.6 | 1,047.8/1,761.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 762 | 1,143.1 | 1,062.6/1,215.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 763 | 1,111.7 | 1,042.8/1,227.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 764 | 1,090.3 | 1,086.4/1,214.2 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 765 | 1,081.0 | 1,048.8/1,218.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 766 | 1,114.4 | 1,043.5/1,203.6 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 767 | 1,093.1 | 1,043.7/1,199.9 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 768 | 1,068.7 | 1,046.7/1,236.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 769 | 1,096.2 | 1,045.4/1,173.2 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 770 | 1,078.4 | 1,045.1/1,191.3 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 771 | 1,088.7 | 1,084.3/1,207.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 772 | 1,085.9 | 1,077.4/1,214.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 773 | 234.0 | 206.7/237.4 | 661.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 774 | 618.8 | 615.5/769.1 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 775 | 56.5 | 40.8/58.8 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 776 | 1,184.8 | 1,142.1/1,305.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 777 | 1,126.1 | 1,075.7/1,228.5 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 778 | 1,114.3 | 1,057.4/1,221.4 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 779 | 1,071.6 | 1,047.3/1,168.1 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 780 | 1,075.6 | 1,042.5/1,134.6 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 781 | 1,092.4 | 1,074.6/1,115.9 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 782 | 1,128.0 | 1,112.2/1,151.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 783 | 1,115.7 | 1,104.2/1,221.4 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 784 | 1,146.5 | 1,099.9/1,221.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 785 | 1,110.0 | 1,104.3/1,205.1 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 786 | 1,105.2 | 1,099.9/1,211.9 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 787 | 1,109.9 | 1,086.6/1,193.4 | 201.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 788 | 1,096.8 | 1,090.7/1,196.8 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 789 | 1,099.4 | 1,091.7/1,198.4 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 790 | 1,120.7 | 1,081.5/1,203.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 791 | 1,128.1 | 1,083.4/1,153.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 792 | 1,090.5 | 1,067.9/1,100.7 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 793 | 1,082.8 | 1,069.2/1,135.3 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 794 | 1,094.1 | 1,088.7/1,105.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 795 | 1,135.9 | 1,105.3/1,327.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 796 | 1,125.7 | 1,096.6/1,147.0 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 797 | 1,107.9 | 1,091.2/1,180.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 798 | 1,112.4 | 1,075.7/1,185.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 799 | 1,104.5 | 1,067.2/1,172.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 800 | 1,115.6 | 1,102.7/1,205.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 801 | 1,145.9 | 1,129.5/1,208.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 802 | 1,204.8 | 1,190.3/1,251.3 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 803 | 1,214.1 | 1,209.6/1,227.4 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 804 | 229.2 | 225.6/256.5 | 661.3 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 805 | 617.6 | 607.7/619.3 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 806 | 50.7 | 45.1/60.2 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 807 | 1,261.0 | 1,244.7/1,278.7 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 808 | 1,227.0 | 1,220.0/1,232.8 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 809 | 1,215.2 | 1,207.2/1,217.3 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 810 | 1,211.6 | 1,175.6/1,222.5 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 811 | 1,209.0 | 1,193.3/1,209.1 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 812 | 1,208.8 | 1,207.1/1,214.4 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 813 | 1,199.7 | 1,196.0/1,202.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 814 | 1,205.8 | 1,172.8/1,212.3 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 815 | 1,195.8 | 1,181.5/1,204.3 | 206.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 816 | 1,224.0 | 1,182.0/1,230.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 817 | 1,198.3 | 1,173.8/1,202.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 818 | 1,216.2 | 1,195.9/1,222.4 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 819 | 1,210.6 | 1,210.1/1,215.9 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 820 | 1,212.9 | 1,204.7/1,218.8 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 821 | 1,222.1 | 1,202.5/1,478.8 | 201.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 822 | 1,222.2 | 1,200.1/1,281.6 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 823 | 1,207.5 | 1,199.4/1,219.9 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 824 | 1,208.4 | 1,189.6/1,222.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 825 | 1,203.5 | 1,196.2/1,208.9 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 826 | 1,202.1 | 1,194.4/1,205.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 827 | 1,191.8 | 1,171.9/1,209.5 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 828 | 1,198.8 | 1,197.2/1,205.7 | 201.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 829 | 1,205.5 | 1,186.3/1,206.0 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 830 | 1,116.3 | 1,114.8/1,199.5 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 831 | 1,108.8 | 1,108.6/1,199.4 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 832 | 1,142.3 | 1,109.9/1,193.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 833 | 1,188.9 | 1,109.9/1,195.4 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 834 | 1,171.0 | 1,105.6/1,205.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 835 | 238.7 | 237.2/240.8 | 661.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 836 | 610.2 | 602.6/619.5 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 837 | 54.9 | 52.1/56.7 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 838 | 1,274.7 | 1,178.1/1,286.7 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 839 | 1,225.0 | 1,126.5/1,244.5 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 840 | 1,220.8 | 1,165.3/1,251.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 841 | 1,205.1 | 1,157.6/1,258.2 | 201.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 842 | 1,176.8 | 1,104.9/1,400.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 843 | 1,181.1 | 1,114.3/1,216.1 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 844 | 1,194.2 | 1,108.3/1,215.1 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 845 | 1,129.4 | 1,122.7/1,229.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 846 | 1,112.9 | 1,097.6/1,213.7 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 847 | 1,134.8 | 1,117.4/1,215.6 | 204.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 848 | 1,132.3 | 1,099.4/1,210.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 849 | 1,140.8 | 1,094.4/1,214.8 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 850 | 1,215.2 | 1,071.5/1,215.9 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 851 | 1,208.3 | 1,085.8/1,209.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 852 | 1,170.6 | 1,065.6/1,210.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 853 | 1,169.6 | 1,102.2/1,209.0 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 854 | 1,255.8 | 1,124.2/1,325.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 855 | 1,383.5 | 1,152.5/1,414.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 856 | 1,224.6 | 1,101.0/1,244.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 857 | 1,227.0 | 1,071.8/1,227.4 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 858 | 1,212.7 | 1,071.7/1,217.3 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 859 | 1,199.4 | 1,065.4/1,217.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 860 | 1,191.4 | 1,069.2/1,204.9 | 265.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 861 | 1,151.7 | 1,073.9/1,220.3 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 862 | 1,095.6 | 1,084.6/1,171.0 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 863 | 1,136.5 | 1,106.9/1,169.6 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 864 | 1,109.2 | 1,091.4/1,188.9 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 865 | 1,102.1 | 1,092.7/1,179.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 866 | 221.6 | 214.4/246.4 | 661.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 867 | 612.5 | 610.0/622.5 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 868 | 54.8 | 48.1/55.0 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 869 | 1,194.6 | 1,164.6/1,251.4 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 870 | 1,183.3 | 1,103.9/1,199.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 871 | 1,180.3 | 1,102.1/1,222.8 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 872 | 1,215.4 | 1,082.9/1,215.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 873 | 1,215.8 | 1,100.5/1,525.0 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 874 | 1,205.1 | 1,126.0/1,262.9 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 875 | 1,217.8 | 1,105.1/1,231.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 876 | 1,211.5 | 1,099.8/1,224.0 | 283.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 877 | 1,217.4 | 1,137.1/1,218.8 | 204.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 878 | 1,172.9 | 1,171.9/1,183.8 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 879 | 1,162.6 | 1,161.7/1,180.7 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 880 | 1,171.6 | 1,103.7/1,172.2 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 881 | 1,157.5 | 1,113.8/1,188.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 882 | 1,126.3 | 1,101.5/1,137.8 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 883 | 1,108.6 | 1,101.2/1,130.2 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 884 | 1,110.2 | 1,070.9/1,114.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 885 | 1,109.3 | 1,080.3/1,110.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 886 | 1,107.8 | 1,044.4/1,153.2 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 887 | 1,108.1 | 1,044.0/1,108.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 888 | 1,108.2 | 1,038.0/1,109.1 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 889 | 1,091.0 | 1,043.9/1,105.8 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 890 | 1,086.0 | 1,042.2/1,140.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 891 | 1,088.5 | 1,056.1/1,139.2 | 206.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 892 | 1,095.5 | 1,078.9/1,125.4 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 893 | 1,113.1 | 1,107.2/1,198.1 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 894 | 1,193.5 | 1,109.4/1,211.7 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 895 | 1,198.9 | 1,109.7/1,218.1 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 896 | 1,194.6 | 1,152.0/1,206.0 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 897 | 241.8 | 228.8/243.3 | 661.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 898 | 620.8 | 598.8/623.9 | 7.4 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 899 | 53.2 | 48.4/58.3 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 900 | 1,289.5 | 1,248.5/1,378.5 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 901 | 1,248.6 | 1,236.5/1,436.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 902 | 1,245.0 | 1,230.2/1,246.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 903 | 1,211.5 | 1,204.0/1,214.0 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 904 | 1,204.5 | 1,172.7/1,211.8 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 905 | 1,191.6 | 1,188.4/1,223.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 906 | 1,180.9 | 1,173.4/1,206.6 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 907 | 1,174.4 | 1,174.4/1,224.3 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 908 | 1,176.8 | 1,134.9/1,204.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 909 | 1,171.5 | 1,103.7/1,212.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 910 | 1,173.5 | 1,141.7/1,224.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 911 | 1,182.6 | 1,168.9/1,212.9 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 912 | 1,180.6 | 1,167.7/1,196.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 913 | 1,204.1 | 1,174.0/1,207.6 | 201.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 914 | 1,174.0 | 1,168.8/1,210.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 915 | 1,174.5 | 1,164.1/1,218.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 916 | 1,175.2 | 1,169.4/1,207.1 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 917 | 1,182.4 | 1,157.8/1,236.9 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 918 | 1,207.7 | 1,173.3/1,219.8 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 919 | 1,172.2 | 1,162.3/1,195.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 920 | 1,136.8 | 1,111.8/1,179.2 | 250.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 921 | 1,160.9 | 1,106.6/1,179.3 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 922 | 1,164.6 | 1,105.3/1,743.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 923 | 1,170.3 | 1,110.1/1,257.7 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 924 | 1,172.4 | 1,085.2/1,262.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 925 | 1,179.4 | 1,070.5/1,251.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 926 | 1,165.9 | 1,068.7/1,239.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 927 | 1,195.8 | 1,095.6/1,211.5 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 928 | 224.7 | 205.9/256.9 | 661.3 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 929 | 621.0 | 617.7/622.7 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 930 | 52.4 | 46.0/63.9 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 931 | 1,252.8 | 1,125.1/1,300.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 932 | 1,202.6 | 1,120.0/1,253.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 933 | 1,217.7 | 1,192.0/1,223.2 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 934 | 1,216.8 | 1,172.1/1,235.0 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 935 | 1,211.3 | 1,183.1/1,214.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 936 | 1,219.0 | 1,174.9/1,222.6 | 268.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 937 | 1,225.5 | 1,216.4/1,244.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 938 | 1,205.5 | 1,170.7/1,226.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 939 | 1,212.0 | 1,174.0/1,239.8 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 940 | 1,204.4 | 1,177.3/1,213.7 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 941 | 1,175.1 | 1,158.7/1,205.1 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 942 | 1,167.9 | 1,163.0/1,211.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 943 | 1,185.6 | 1,159.8/1,207.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 944 | 1,163.9 | 1,152.8/1,197.5 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 945 | 1,185.9 | 1,133.2/1,192.8 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 946 | 1,167.5 | 1,122.0/1,232.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 947 | 1,189.0 | 1,175.6/1,190.9 | 210.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 948 | 1,173.1 | 1,162.4/1,210.0 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 949 | 1,177.1 | 1,124.9/1,216.7 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 950 | 1,177.8 | 1,100.1/1,244.2 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 951 | 1,166.2 | 1,076.3/1,222.2 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 952 | 1,160.5 | 1,082.0/1,217.0 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 953 | 1,172.8 | 1,081.3/1,208.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 954 | 1,209.7 | 1,129.8/1,224.9 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 955 | 1,195.5 | 1,103.2/1,215.5 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 956 | 1,182.3 | 1,081.0/1,256.6 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 957 | 1,168.5 | 1,168.2/1,207.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 958 | 1,206.9 | 1,161.1/1,211.6 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 959 | 231.7 | 231.6/250.9 | 661.3 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 960 | 619.0 | 604.8/623.1 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 961 | 52.8 | 50.3/61.8 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 962 | 1,272.7 | 1,238.7/1,309.0 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 963 | 1,222.4 | 1,145.6/1,236.9 | 201.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 964 | 1,234.2 | 1,156.4/1,234.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 965 | 1,214.9 | 1,110.9/1,242.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 966 | 1,200.2 | 1,124.2/1,217.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 967 | 1,183.1 | 1,108.1/1,195.2 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 968 | 1,146.3 | 1,115.7/1,176.2 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 969 | 1,175.9 | 1,108.1/1,180.6 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 970 | 1,174.7 | 1,106.6/1,218.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 971 | 1,170.1 | 1,098.8/1,185.5 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 972 | 1,138.8 | 1,098.0/1,194.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 973 | 1,192.2 | 1,145.1/1,209.0 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 974 | 1,179.7 | 1,111.5/1,717.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 975 | 1,101.7 | 1,097.2/1,220.2 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 976 | 1,107.1 | 1,091.9/1,176.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 977 | 1,087.5 | 1,087.5/1,208.1 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 978 | 1,075.6 | 1,062.5/1,168.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 979 | 1,074.5 | 1,069.1/1,206.8 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 980 | 1,072.3 | 1,061.2/1,282.5 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 981 | 1,098.1 | 1,078.0/1,399.3 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 982 | 1,163.1 | 1,070.7/1,205.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 983 | 1,170.0 | 1,045.9/1,222.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 984 | 1,157.2 | 1,039.8/1,208.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 985 | 1,161.2 | 1,050.5/1,209.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 986 | 1,160.0 | 1,040.7/1,180.0 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 987 | 1,155.2 | 1,043.3/1,196.6 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 988 | 1,203.1 | 1,043.4/1,205.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 989 | 1,177.6 | 1,050.0/1,193.1 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 990 | 232.5 | 200.4/241.7 | 663.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 991 | 623.3 | 615.4/630.1 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 992 | 49.7 | 46.4/60.1 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 993 | 1,186.6 | 1,158.4/1,230.9 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 994 | 1,115.5 | 1,102.3/1,154.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 995 | 1,095.7 | 1,084.3/1,109.8 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 996 | 1,079.7 | 1,074.5/1,105.6 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 997 | 1,101.0 | 1,076.7/1,118.7 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 998 | 1,087.9 | 1,053.0/1,111.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 999 | 1,056.3 | 1,037.6/1,106.2 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1000 | 1,057.0 | 1,034.9/1,110.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1001 | 1,073.4 | 1,054.2/1,134.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1002 | 1,115.3 | 1,046.2/1,132.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1003 | 1,077.7 | 1,043.7/1,221.3 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1004 | 1,119.7 | 1,037.1/1,218.4 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1005 | 1,168.8 | 1,041.9/1,229.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1006 | 1,162.0 | 1,051.9/1,245.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1007 | 1,194.9 | 1,035.0/1,212.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1008 | 1,203.7 | 1,043.6/1,214.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1009 | 1,224.1 | 1,034.5/1,246.3 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1010 | 1,210.4 | 1,052.8/1,226.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1011 | 1,202.3 | 1,060.5/1,220.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1012 | 1,211.7 | 1,092.2/1,225.6 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1013 | 1,193.9 | 1,189.7/1,215.2 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1014 | 1,192.5 | 1,189.5/1,242.7 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1015 | 1,206.0 | 1,198.0/1,213.8 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1016 | 1,204.4 | 1,197.4/1,217.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1017 | 1,205.4 | 1,197.0/1,228.2 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1018 | 1,226.8 | 1,185.8/1,228.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1019 | 1,210.7 | 1,206.0/1,244.0 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1020 | 1,209.0 | 1,194.7/1,214.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1021 | 249.7 | 228.3/259.4 | 661.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1022 | 615.3 | 614.7/623.1 | 7.2 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1023 | 58.4 | 48.0/61.0 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1024 | 1,289.1 | 1,273.8/1,291.3 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1025 | 1,220.1 | 1,204.7/1,247.4 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1026 | 1,195.1 | 1,192.6/1,207.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1027 | 1,224.9 | 1,206.0/1,849.5 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1028 | 1,196.7 | 1,167.1/1,230.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1029 | 1,194.3 | 1,190.6/1,224.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1030 | 1,210.6 | 1,194.4/1,212.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1031 | 1,191.5 | 1,169.6/1,212.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1032 | 1,205.5 | 1,114.1/1,207.7 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1033 | 1,197.7 | 1,138.7/1,212.3 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1034 | 1,221.5 | 1,103.7/1,231.7 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1035 | 1,194.7 | 1,143.1/1,215.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1036 | 1,181.1 | 1,142.5/1,202.9 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1037 | 1,183.5 | 1,174.9/1,251.0 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1038 | 1,181.9 | 1,181.4/1,182.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1039 | 1,168.1 | 1,112.6/1,224.3 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1040 | 1,182.7 | 1,147.0/1,317.4 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1041 | 1,215.4 | 1,141.0/1,243.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1042 | 1,184.0 | 1,165.6/1,200.3 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1043 | 1,169.0 | 1,115.1/1,188.6 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1044 | 1,161.3 | 1,095.0/1,215.2 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1045 | 1,202.5 | 1,082.7/1,207.8 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1046 | 1,170.1 | 1,101.1/1,208.9 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1047 | 1,157.0 | 1,107.1/1,208.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1048 | 1,114.1 | 1,109.8/1,524.8 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1049 | 1,127.8 | 1,063.8/1,233.8 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1050 | 1,109.5 | 1,046.2/1,227.0 | 203.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1051 | 1,115.3 | 1,044.2/1,238.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1052 | 224.5 | 203.4/246.5 | 665.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1053 | 613.7 | 606.8/721.2 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1054 | 57.4 | 43.2/65.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1055 | 1,191.3 | 1,113.1/1,311.5 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1056 | 1,137.7 | 1,119.7/1,239.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1057 | 1,107.3 | 1,080.9/1,228.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1058 | 1,099.9 | 1,062.7/1,231.7 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1059 | 1,098.5 | 1,079.6/1,217.2 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1060 | 1,108.9 | 1,072.0/1,213.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1061 | 1,109.5 | 1,054.1/1,235.4 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1062 | 1,094.6 | 1,060.5/1,227.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1063 | 1,109.3 | 1,049.7/1,176.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1064 | 1,091.6 | 1,049.9/1,175.2 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1065 | 1,108.2 | 1,068.9/1,170.7 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1066 | 1,172.9 | 1,041.3/1,178.0 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1067 | 1,151.7 | 1,043.8/1,210.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1068 | 1,109.3 | 1,039.0/1,214.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1069 | 1,104.3 | 1,053.0/1,204.1 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1070 | 1,118.6 | 1,047.7/1,204.0 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1071 | 1,115.1 | 1,089.2/1,207.8 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1072 | 1,127.1 | 1,118.9/1,207.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1073 | 1,206.5 | 1,177.4/1,639.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1074 | 1,184.7 | 1,146.1/1,271.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1075 | 1,176.6 | 1,101.0/1,205.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1076 | 1,145.8 | 1,112.1/1,204.1 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1077 | 1,127.7 | 1,117.4/1,190.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1078 | 1,101.1 | 1,098.5/1,200.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1079 | 1,150.6 | 1,069.4/1,204.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1080 | 1,196.0 | 1,068.3/1,203.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1081 | 1,190.1 | 1,047.8/1,197.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1082 | 1,201.2 | 1,049.0/1,244.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1083 | 227.2 | 197.7/240.1 | 663.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1084 | 624.6 | 615.0/625.3 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1085 | 48.5 | 43.8/55.2 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1086 | 1,147.7 | 1,132.6/1,297.9 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1087 | 1,113.9 | 1,066.2/1,206.7 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1088 | 1,115.0 | 1,083.7/1,191.8 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1089 | 1,094.8 | 1,084.3/1,246.7 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1090 | 1,084.0 | 1,069.7/1,207.9 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1091 | 1,078.2 | 1,077.4/1,207.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1092 | 1,112.4 | 1,056.8/1,206.8 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1093 | 1,178.0 | 1,046.2/1,204.2 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1094 | 1,200.1 | 1,041.2/1,204.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1095 | 1,188.0 | 1,054.0/1,192.2 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1096 | 1,207.7 | 1,045.6/1,215.5 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1097 | 1,193.8 | 1,066.2/1,242.8 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1098 | 1,196.7 | 1,054.0/1,201.8 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1099 | 1,185.4 | 1,045.3/1,208.2 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1100 | 1,198.3 | 1,048.7/1,200.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1101 | 1,248.1 | 1,046.0/1,261.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1102 | 1,214.7 | 1,053.3/1,217.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1103 | 1,207.1 | 1,039.4/1,228.5 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1104 | 1,203.6 | 1,044.6/1,205.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1105 | 1,202.3 | 1,044.8/1,218.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1106 | 1,169.9 | 1,083.0/1,200.1 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1107 | 1,170.9 | 1,049.8/1,201.8 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1108 | 1,195.6 | 1,049.6/1,275.8 | 207.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1109 | 1,175.4 | 1,047.7/1,256.8 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1110 | 1,177.8 | 1,047.1/1,197.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1111 | 1,175.0 | 1,056.5/1,199.6 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1112 | 1,171.3 | 1,048.5/1,190.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1113 | 1,194.9 | 1,044.6/1,195.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1114 | 231.1 | 197.6/245.2 | 662.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1115 | 617.3 | 616.1/633.9 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1116 | 49.1 | 39.4/52.1 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1117 | 1,178.9 | 1,159.0/1,256.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1118 | 1,174.4 | 1,072.3/1,191.9 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1119 | 1,186.9 | 1,084.3/1,222.9 | 201.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1120 | 1,192.3 | 1,176.3/1,222.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1121 | 1,163.1 | 1,161.5/1,170.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1122 | 1,164.7 | 1,111.2/1,165.0 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1123 | 1,170.4 | 1,116.1/1,190.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1124 | 1,169.1 | 1,111.8/1,177.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1125 | 1,175.3 | 1,099.0/1,197.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1126 | 1,187.8 | 1,092.2/1,188.9 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1127 | 1,166.8 | 1,098.5/1,181.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1128 | 1,148.3 | 1,102.1/1,196.9 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1129 | 1,132.7 | 1,099.6/1,195.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1130 | 1,157.3 | 1,156.8/1,204.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1131 | 1,174.6 | 1,170.7/1,193.1 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1132 | 1,187.3 | 1,136.5/1,188.7 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1133 | 1,166.3 | 1,098.8/1,210.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1134 | 1,179.4 | 1,090.8/1,254.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1135 | 1,179.1 | 1,099.7/1,206.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1136 | 1,203.7 | 1,124.3/1,207.6 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1137 | 1,184.0 | 1,075.9/1,204.9 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1138 | 1,166.1 | 1,072.8/1,207.6 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1139 | 1,177.8 | 1,047.5/1,212.9 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1140 | 1,168.4 | 1,052.2/1,231.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1141 | 1,118.5 | 1,048.7/1,223.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1142 | 1,180.4 | 1,071.4/1,200.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1143 | 1,172.9 | 1,070.4/1,186.6 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1144 | 1,167.9 | 1,072.8/1,177.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1145 | 227.8 | 202.3/236.9 | 663.0 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1146 | 627.5 | 617.3/632.6 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1147 | 48.1 | 44.3/52.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1148 | 1,193.6 | 1,148.0/1,250.3 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1149 | 1,147.9 | 1,108.9/1,188.1 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1150 | 1,198.5 | 1,081.4/1,217.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1151 | 1,147.8 | 1,067.7/1,200.8 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1152 | 1,106.8 | 1,040.3/1,246.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1153 | 1,104.2 | 1,057.0/1,240.2 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1154 | 1,105.5 | 1,047.8/1,332.2 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1155 | 1,123.5 | 1,047.0/1,606.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1156 | 1,108.0 | 1,075.0/1,232.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1157 | 1,132.6 | 1,051.2/1,211.4 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1158 | 1,105.3 | 1,049.2/1,206.2 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1159 | 1,125.9 | 1,040.3/1,218.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1160 | 1,131.3 | 1,066.5/1,260.3 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1161 | 1,107.5 | 1,059.2/1,209.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1162 | 1,200.8 | 1,096.6/1,761.7 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1163 | 1,167.3 | 1,107.9/1,198.2 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1164 | 1,202.3 | 1,176.5/1,209.8 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1165 | 1,186.4 | 1,150.9/1,279.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1166 | 1,146.0 | 1,102.1/1,239.0 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1167 | 1,131.4 | 1,107.3/1,216.9 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1168 | 1,134.8 | 1,123.0/1,215.3 | 205.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1169 | 1,171.9 | 1,099.5/1,204.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1170 | 1,184.8 | 1,094.8/1,201.9 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1171 | 1,154.9 | 1,107.7/1,206.3 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1172 | 1,172.6 | 1,117.7/1,187.2 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1173 | 1,146.8 | 1,101.6/1,172.3 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1174 | 1,104.2 | 1,101.7/1,161.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1175 | 1,106.1 | 1,093.5/1,181.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1176 | 222.6 | 212.5/230.8 | 662.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1177 | 619.2 | 618.1/624.8 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1178 | 54.4 | 45.3/56.4 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1179 | 1,185.1 | 1,178.9/1,306.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1180 | 1,137.2 | 1,137.0/1,238.9 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1181 | 1,134.0 | 1,111.1/1,219.3 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1182 | 1,165.7 | 1,106.5/1,209.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1183 | 1,144.7 | 1,109.6/1,212.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1184 | 1,146.0 | 1,143.6/1,221.8 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1185 | 1,111.8 | 1,111.3/1,209.9 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1186 | 1,113.3 | 1,110.5/1,228.3 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1187 | 1,141.6 | 1,111.0/1,242.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1188 | 1,110.8 | 1,101.7/1,222.1 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1189 | 1,132.8 | 1,098.5/1,195.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1190 | 1,103.0 | 1,099.4/1,201.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1191 | 1,112.8 | 1,092.8/1,175.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1192 | 1,129.6 | 1,108.1/1,185.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1193 | 1,105.9 | 1,100.3/1,116.4 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1194 | 1,101.8 | 1,074.4/1,126.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1195 | 1,085.9 | 1,082.3/1,133.4 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1196 | 1,078.0 | 1,072.8/1,113.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1197 | 1,081.6 | 1,051.4/1,115.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1198 | 1,053.3 | 1,041.0/1,114.8 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1199 | 1,044.7 | 1,042.0/1,110.3 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1200 | 1,043.9 | 1,036.6/1,115.8 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1201 | 1,074.0 | 1,067.0/1,103.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1202 | 1,092.9 | 1,065.5/1,113.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1203 | 1,179.2 | 1,048.2/1,184.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1204 | 1,150.3 | 1,039.4/1,199.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1205 | 1,164.7 | 1,074.9/1,181.4 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1206 | 1,161.1 | 1,077.6/1,226.9 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1207 | 224.8 | 213.1/236.9 | 663.3 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1208 | 619.4 | 615.8/622.9 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1209 | 53.8 | 44.4/54.4 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1210 | 1,247.7 | 1,130.0/1,259.3 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1211 | 1,182.6 | 1,072.4/1,319.1 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1212 | 1,209.2 | 1,110.6/1,212.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1213 | 1,211.8 | 1,068.0/1,221.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1214 | 1,213.5 | 1,051.4/1,251.0 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1215 | 1,213.7 | 1,053.2/1,223.8 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1216 | 1,203.3 | 1,046.0/1,210.0 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1217 | 1,208.6 | 1,047.5/1,217.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1218 | 1,214.9 | 1,045.4/1,214.9 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1219 | 1,205.9 | 1,050.0/1,317.2 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1220 | 1,212.1 | 1,049.5/1,567.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1221 | 1,236.8 | 1,068.9/1,239.4 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1222 | 1,185.0 | 1,076.7/1,248.1 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1223 | 1,203.4 | 1,072.8/1,213.4 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1224 | 1,185.4 | 1,102.6/1,214.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1225 | 1,141.1 | 1,075.6/1,209.0 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1226 | 1,126.3 | 1,086.5/1,198.3 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1227 | 1,174.1 | 1,079.6/1,206.6 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1228 | 1,180.8 | 1,077.6/1,209.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1229 | 1,179.0 | 1,067.8/1,198.7 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1230 | 1,190.7 | 1,112.4/1,229.0 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1231 | 1,207.4 | 1,184.5/1,212.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1232 | 1,189.1 | 1,171.2/1,210.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1233 | 1,174.3 | 1,167.2/1,202.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1234 | 1,181.8 | 1,180.8/1,187.1 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1235 | 1,174.2 | 1,174.1/1,174.3 | 204.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1236 | 1,193.4 | 1,135.9/1,194.7 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1237 | 1,202.0 | 1,173.9/1,208.3 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1238 | 240.1 | 235.8/241.5 | 662.3 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1239 | 612.9 | 610.9/613.1 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1240 | 57.9 | 53.3/59.2 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1241 | 1,227.7 | 1,217.0/1,291.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1242 | 1,133.3 | 1,127.6/1,227.8 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1243 | 1,127.6 | 1,123.6/1,211.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1244 | 1,118.5 | 1,076.3/1,205.7 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1245 | 1,223.1 | 1,213.4/1,629.4 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1246 | 1,213.7 | 1,103.1/1,215.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1247 | 1,212.0 | 1,164.7/1,226.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1248 | 1,212.1 | 1,102.1/1,241.3 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1249 | 1,233.8 | 1,089.1/1,243.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1250 | 1,221.5 | 1,106.3/1,235.6 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1251 | 1,210.2 | 1,096.0/1,229.8 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1252 | 1,196.5 | 1,156.4/1,213.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1253 | 1,200.6 | 1,180.4/1,202.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1254 | 1,183.9 | 1,176.1/1,211.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1255 | 1,196.2 | 1,128.4/1,221.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1256 | 1,198.3 | 1,142.5/1,234.4 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1257 | 1,191.7 | 1,131.8/1,216.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1258 | 1,165.7 | 1,111.2/1,203.4 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1259 | 1,152.2 | 1,091.3/1,214.9 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1260 | 1,121.7 | 1,107.7/1,203.7 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1261 | 1,109.3 | 1,083.6/1,215.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1262 | 1,161.4 | 1,119.2/1,219.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1263 | 1,146.2 | 1,098.1/1,186.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1264 | 1,149.0 | 1,092.6/1,173.0 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1265 | 1,109.7 | 1,100.4/1,200.9 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1266 | 1,125.1 | 1,078.7/1,195.8 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1267 | 1,122.9 | 1,095.9/1,178.1 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1268 | 1,100.6 | 1,090.6/1,182.3 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1269 | 225.1 | 215.5/243.5 | 663.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1270 | 615.9 | 607.0/620.9 | 7.2 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1271 | 58.5 | 49.1/59.7 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1272 | 1,208.6 | 1,171.9/1,308.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1273 | 1,185.4 | 1,128.3/1,235.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1274 | 1,142.5 | 1,117.2/1,166.2 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1275 | 1,128.9 | 1,123.9/1,169.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1276 | 1,119.7 | 1,111.6/1,196.4 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1277 | 1,092.9 | 1,084.6/1,184.6 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1278 | 1,107.8 | 1,071.9/1,185.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1279 | 1,063.2 | 1,063.1/1,172.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1280 | 1,061.7 | 1,052.9/1,166.8 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1281 | 1,060.3 | 1,053.4/1,165.7 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1282 | 1,053.6 | 1,048.2/1,165.0 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1283 | 1,093.7 | 1,049.3/1,178.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1284 | 1,075.0 | 1,061.0/1,115.7 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1285 | 1,072.8 | 1,059.0/1,190.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1286 | 1,064.2 | 1,051.5/1,163.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1287 | 1,069.7 | 1,056.4/1,195.9 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1288 | 1,097.2 | 1,079.4/1,197.6 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1289 | 1,182.7 | 1,093.1/1,187.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1290 | 1,175.2 | 1,108.1/1,191.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1291 | 1,197.9 | 1,108.1/1,208.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1292 | 1,200.0 | 1,140.5/1,214.8 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1293 | 1,208.2 | 1,116.2/1,252.1 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1294 | 1,199.6 | 1,089.8/1,222.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1295 | 1,198.8 | 1,116.8/1,220.4 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1296 | 1,172.4 | 1,088.1/1,204.2 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1297 | 1,160.6 | 1,075.7/1,197.5 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1298 | 1,175.9 | 1,100.2/1,199.8 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1299 | 1,102.3 | 1,078.8/1,192.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1300 | 236.2 | 210.4/360.1 | 662.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1301 | 618.4 | 613.5/620.2 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1302 | 48.3 | 48.2/53.9 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1303 | 1,208.5 | 1,183.7/1,313.1 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1304 | 1,123.3 | 1,094.0/1,221.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1305 | 1,094.7 | 1,093.5/1,214.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1306 | 1,095.2 | 1,063.8/1,153.1 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1307 | 1,100.7 | 1,051.7/1,113.2 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1308 | 1,063.1 | 1,050.5/1,112.2 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1309 | 1,053.5 | 1,048.4/1,164.3 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1310 | 1,062.8 | 1,050.0/1,187.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1311 | 1,081.1 | 1,047.4/1,196.9 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1312 | 1,125.2 | 1,092.3/1,157.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1313 | 1,171.3 | 1,056.0/1,202.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1314 | 1,205.1 | 1,051.0/1,212.6 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1315 | 1,199.0 | 1,069.1/1,210.3 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1316 | 1,202.7 | 1,082.4/1,207.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1317 | 1,212.2 | 1,111.2/1,218.0 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1318 | 1,209.8 | 1,167.0/1,224.6 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1319 | 1,198.1 | 1,163.8/1,205.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1320 | 1,232.4 | 1,171.7/1,232.9 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1321 | 1,209.5 | 1,187.4/1,236.2 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1322 | 1,171.0 | 1,150.2/1,206.4 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1323 | 1,172.3 | 1,097.5/1,203.2 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1324 | 1,163.1 | 1,101.7/1,205.5 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1325 | 1,154.9 | 1,098.7/1,214.4 | 204.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1326 | 1,115.5 | 1,102.3/1,214.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1327 | 1,122.1 | 1,085.2/1,207.3 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1328 | 1,125.5 | 1,075.3/1,220.6 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1329 | 1,116.0 | 1,079.7/1,241.9 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1330 | 1,160.7 | 1,111.3/1,225.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1331 | 228.9 | 211.7/247.8 | 663.2 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1332 | 619.7 | 611.1/623.5 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1333 | 51.3 | 45.5/59.8 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1334 | 1,291.0 | 1,180.4/1,310.1 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1335 | 1,222.9 | 1,126.5/1,235.7 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1336 | 1,218.1 | 1,115.4/1,235.1 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1337 | 1,215.8 | 1,109.0/1,240.1 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1338 | 1,232.7 | 1,107.2/1,270.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1339 | 1,203.4 | 1,097.4/1,235.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1340 | 1,204.8 | 1,182.0/1,230.4 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1341 | 1,197.2 | 1,179.8/1,216.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1342 | 1,210.6 | 1,169.7/1,220.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1343 | 1,204.3 | 1,169.6/1,211.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1344 | 1,201.9 | 1,166.2/1,218.8 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1345 | 1,207.1 | 1,176.4/1,222.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1346 | 1,197.1 | 1,160.3/1,251.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1347 | 1,179.1 | 1,176.6/1,242.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1348 | 1,191.4 | 1,107.4/1,199.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1349 | 1,204.5 | 1,071.3/1,227.1 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1350 | 1,206.0 | 1,070.9/1,210.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1351 | 1,200.5 | 1,061.6/1,217.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1352 | 1,202.4 | 1,045.6/1,226.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1353 | 1,204.1 | 1,049.1/1,207.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1354 | 1,210.9 | 1,088.5/1,233.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1355 | 1,184.9 | 1,087.3/1,200.7 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1356 | 1,143.0 | 1,130.4/1,145.7 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1357 | 1,108.3 | 1,106.4/1,200.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1358 | 1,159.3 | 1,098.5/1,188.4 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1359 | 1,179.0 | 1,096.6/1,205.9 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1360 | 1,171.3 | 1,139.5/1,223.0 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1361 | 1,104.5 | 1,074.5/1,166.4 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1362 | 224.0 | 206.4/233.0 | 662.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1363 | 613.7 | 608.5/628.6 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1364 | 48.6 | 43.7/64.2 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1365 | 1,157.7 | 1,146.1/1,283.4 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1366 | 1,091.3 | 1,083.4/1,193.0 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1367 | 1,090.8 | 1,064.4/1,227.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1368 | 1,086.4 | 1,049.6/1,212.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1369 | 1,068.3 | 1,049.4/1,226.7 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1370 | 1,053.2 | 1,051.1/1,221.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1371 | 1,048.5 | 1,047.1/1,176.5 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1372 | 1,065.9 | 1,038.5/1,198.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1373 | 1,089.3 | 1,047.0/1,220.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1374 | 1,075.7 | 1,070.9/1,177.6 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1375 | 1,071.8 | 1,056.9/1,195.6 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1376 | 1,095.7 | 1,064.0/1,182.4 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1377 | 1,099.9 | 1,042.4/1,614.4 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1378 | 1,072.2 | 1,055.3/1,208.6 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1379 | 1,069.0 | 1,039.4/1,183.0 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1380 | 1,061.6 | 1,037.8/1,249.3 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1381 | 1,045.6 | 1,033.7/1,232.5 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1382 | 1,045.3 | 1,040.8/1,280.3 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1383 | 1,051.3 | 1,050.1/1,216.1 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1384 | 1,045.7 | 1,041.5/1,204.5 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1385 | 1,058.4 | 1,045.9/1,185.4 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1386 | 1,078.7 | 1,043.7/1,179.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1387 | 1,070.6 | 1,041.4/1,183.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1388 | 1,051.8 | 1,046.0/1,155.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1389 | 1,065.8 | 1,044.5/1,154.8 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1390 | 1,069.7 | 1,036.3/1,119.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1391 | 1,068.9 | 1,039.8/1,117.4 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1392 | 1,087.3 | 1,037.1/1,113.8 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1393 | 216.6 | 202.2/219.7 | 661.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1394 | 624.0 | 620.7/637.7 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1395 | 44.8 | 41.9/53.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1396 | 1,189.0 | 1,138.5/1,258.8 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1397 | 1,134.3 | 1,063.9/1,208.3 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1398 | 1,175.1 | 1,051.7/1,195.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1399 | 1,163.7 | 1,052.8/1,214.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1400 | 1,166.9 | 1,041.7/1,210.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1401 | 1,179.1 | 1,042.4/1,197.5 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1402 | 1,209.1 | 1,049.7/1,211.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1403 | 1,206.0 | 1,044.8/1,210.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1404 | 1,201.6 | 1,072.7/1,223.3 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1405 | 1,208.8 | 1,077.9/1,238.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1406 | 1,191.6 | 1,148.1/1,199.4 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1407 | 1,205.6 | 1,204.6/1,217.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1408 | 1,208.4 | 1,199.2/1,214.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1409 | 1,204.1 | 1,195.5/1,211.6 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1410 | 1,194.3 | 1,190.4/1,200.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1411 | 1,192.4 | 1,173.2/1,198.2 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1412 | 1,168.8 | 1,162.0/1,218.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1413 | 1,179.9 | 1,135.0/1,208.2 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1414 | 1,194.2 | 1,097.7/1,219.7 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1415 | 1,198.5 | 1,105.5/1,202.9 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1416 | 1,206.7 | 1,171.8/1,213.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1417 | 1,207.5 | 1,102.0/1,210.4 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1418 | 1,194.0 | 1,069.9/1,207.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1419 | 1,180.5 | 1,066.4/1,198.7 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1420 | 1,195.1 | 1,047.4/1,205.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1421 | 1,203.8 | 1,038.8/1,223.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1422 | 1,206.7 | 1,070.1/1,215.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1423 | 1,168.2 | 1,066.1/1,232.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1424 | 220.9 | 206.0/240.8 | 662.5 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1425 | 623.0 | 614.6/625.4 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1426 | 45.0 | 43.9/56.8 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1427 | 1,218.0 | 1,158.2/1,280.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1428 | 1,177.5 | 1,092.6/1,226.8 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1429 | 1,147.6 | 1,087.1/1,206.3 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1430 | 1,170.1 | 1,071.3/1,202.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1431 | 1,191.3 | 1,073.2/1,210.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1432 | 1,171.0 | 1,057.8/1,182.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1433 | 1,164.4 | 1,101.5/1,191.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1434 | 1,165.7 | 1,069.7/1,196.3 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1435 | 1,163.0 | 1,062.5/1,174.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1436 | 1,152.5 | 1,149.2/1,166.1 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1437 | 1,126.0 | 1,110.2/1,171.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1438 | 1,163.5 | 1,095.3/1,174.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1439 | 1,187.4 | 1,168.1/1,246.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1440 | 1,189.5 | 1,164.2/1,214.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1441 | 1,175.5 | 1,167.7/1,225.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1442 | 1,202.7 | 1,107.0/1,229.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1443 | 1,169.8 | 1,078.8/1,214.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1444 | 1,203.9 | 1,111.6/1,213.3 | 246.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1445 | 1,196.7 | 1,098.9/1,198.3 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1446 | 1,196.3 | 1,089.5/1,209.8 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1447 | 1,193.5 | 1,088.5/1,200.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1448 | 1,114.5 | 1,098.3/1,202.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1449 | 1,102.5 | 1,071.5/1,195.6 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1450 | 1,118.6 | 1,105.7/1,224.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1451 | 1,106.3 | 1,100.3/1,217.3 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1452 | 1,163.5 | 1,116.4/1,198.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1453 | 1,178.9 | 1,106.2/1,194.6 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1454 | 1,109.8 | 1,092.1/1,196.4 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1455 | 228.1 | 207.2/236.7 | 663.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1456 | 621.4 | 612.8/628.7 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1457 | 47.9 | 45.9/49.0 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1458 | 1,139.3 | 1,122.3/1,260.2 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1459 | 1,095.3 | 1,089.4/1,192.4 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1460 | 1,111.6 | 1,101.7/1,196.1 | 296.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1461 | 1,153.2 | 1,104.7/1,172.8 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1462 | 1,192.8 | 1,075.2/1,200.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1463 | 1,174.9 | 1,082.0/1,218.2 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1464 | 1,174.2 | 1,076.8/1,206.9 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1465 | 1,142.9 | 1,071.7/1,199.2 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1466 | 1,164.9 | 1,072.8/1,204.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1467 | 1,186.1 | 1,049.0/1,189.6 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1468 | 1,155.3 | 1,055.0/1,200.2 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1469 | 1,099.5 | 1,059.6/1,226.1 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1470 | 1,132.0 | 1,077.1/1,150.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1471 | 1,087.7 | 1,079.6/1,156.6 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1472 | 1,068.8 | 1,050.2/1,162.0 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1473 | 1,075.2 | 1,040.6/1,165.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1474 | 1,074.5 | 1,036.8/1,161.7 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1475 | 1,049.5 | 1,044.2/1,176.1 | 260.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1476 | 1,049.0 | 1,041.7/1,108.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1477 | 1,044.0 | 1,043.5/1,157.1 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1478 | 1,072.5 | 1,053.1/1,167.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1479 | 1,091.7 | 1,042.5/1,124.6 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1480 | 1,051.7 | 1,048.7/1,099.5 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1481 | 1,049.2 | 1,041.4/1,101.4 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1482 | 1,055.1 | 1,045.7/1,098.8 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1483 | 1,059.5 | 1,049.2/1,097.5 | 206.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1484 | 1,076.1 | 1,044.3/1,121.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1485 | 1,062.0 | 1,041.3/1,102.2 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1486 | 202.0 | 199.0/228.6 | 662.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1487 | 622.8 | 615.9/627.0 | 7.0 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1488 | 42.6 | 40.5/43.0 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1489 | 1,151.5 | 1,081.3/1,155.8 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1490 | 1,062.7 | 1,057.4/1,160.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1491 | 1,054.9 | 1,043.4/1,104.6 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1492 | 1,046.4 | 1,045.6/1,082.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1493 | 1,067.2 | 1,057.7/1,115.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1494 | 1,053.7 | 1,049.6/1,724.8 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1495 | 1,053.4 | 1,046.3/1,250.9 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1496 | 1,056.1 | 1,053.3/1,266.7 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1497 | 1,063.1 | 1,054.1/1,241.0 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1498 | 1,076.6 | 1,039.5/1,207.0 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1499 | 1,084.2 | 1,067.2/1,195.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1500 | 1,068.7 | 1,055.7/1,209.5 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1501 | 1,075.0 | 1,041.2/1,203.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1502 | 1,074.9 | 1,043.9/1,195.9 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1503 | 1,100.3 | 1,043.1/1,225.2 | 205.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1504 | 1,071.8 | 1,036.4/1,230.6 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1505 | 1,068.4 | 1,043.8/1,228.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1506 | 1,079.7 | 1,045.6/1,206.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1507 | 1,052.8 | 1,039.2/1,217.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1508 | 1,086.2 | 1,055.8/1,205.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1509 | 1,062.1 | 1,043.7/1,240.9 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1510 | 1,057.4 | 1,055.4/1,206.2 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1511 | 1,049.9 | 1,044.1/1,191.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1512 | 1,059.0 | 1,046.7/1,221.5 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1513 | 1,171.7 | 1,045.0/1,193.7 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1514 | 1,181.0 | 1,047.7/1,201.0 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1515 | 1,168.5 | 1,044.0/1,192.8 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1516 | 1,170.4 | 1,047.7/1,190.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1517 | 231.3 | 198.7/243.2 | 661.6 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1518 | 623.7 | 613.9/628.0 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1519 | 48.4 | 42.2/63.4 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1520 | 1,260.7 | 1,115.3/1,278.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1521 | 1,226.4 | 1,072.3/1,231.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1522 | 1,203.4 | 1,053.5/1,224.0 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1523 | 1,181.2 | 1,050.7/1,188.7 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1524 | 1,142.5 | 1,048.0/1,192.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1525 | 1,116.2 | 1,064.3/1,167.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1526 | 1,118.3 | 1,084.8/1,209.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1527 | 1,155.4 | 1,121.4/1,227.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1528 | 1,220.4 | 1,119.6/1,225.8 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1529 | 1,198.8 | 1,167.4/1,206.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1530 | 1,197.4 | 1,128.7/1,222.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1531 | 1,195.4 | 1,079.2/1,201.5 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1532 | 1,188.4 | 1,063.7/1,198.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1533 | 1,161.5 | 1,114.7/1,195.4 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1534 | 1,160.3 | 1,119.1/1,198.2 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1535 | 1,193.1 | 1,137.2/1,220.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1536 | 1,222.1 | 1,216.5/1,238.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1537 | 1,197.2 | 1,196.6/1,215.0 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1538 | 1,211.2 | 1,195.5/1,229.7 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1539 | 1,199.3 | 1,199.0/1,245.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1540 | 1,200.6 | 1,192.9/1,221.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1541 | 1,200.0 | 1,192.7/1,202.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1542 | 1,207.3 | 1,202.2/1,208.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1543 | 1,211.5 | 1,202.3/1,215.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1544 | 1,190.3 | 1,170.9/1,243.6 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1545 | 1,173.5 | 1,105.5/1,211.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1546 | 1,165.2 | 1,107.8/1,231.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1547 | 1,165.5 | 1,113.8/1,240.8 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1548 | 231.8 | 225.2/257.9 | 662.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1549 | 611.7 | 609.2/618.2 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1550 | 46.6 | 45.5/67.7 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1551 | 1,244.9 | 1,188.7/1,247.2 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1552 | 1,211.1 | 1,133.6/1,223.2 | 201.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1553 | 1,185.7 | 1,107.2/1,225.1 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1554 | 1,174.4 | 1,170.4/1,234.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1555 | 1,186.4 | 1,168.4/1,207.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1556 | 1,170.6 | 1,166.0/1,199.2 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1557 | 1,162.7 | 1,131.7/1,198.3 | 204.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1558 | 1,216.0 | 1,157.8/1,218.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1559 | 1,121.4 | 1,118.5/1,181.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1560 | 1,118.6 | 1,112.2/1,146.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1561 | 1,089.9 | 1,075.8/1,101.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1562 | 1,101.7 | 1,092.6/1,101.8 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1563 | 1,114.9 | 1,077.8/1,151.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1564 | 1,094.5 | 1,073.3/1,109.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1565 | 1,104.7 | 1,076.9/1,127.9 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1566 | 1,103.6 | 1,068.9/1,166.3 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1567 | 1,096.4 | 1,085.1/1,166.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1568 | 1,098.0 | 1,086.1/1,127.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1569 | 1,089.1 | 1,087.9/1,105.9 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1570 | 1,112.5 | 1,084.6/1,124.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1571 | 1,097.1 | 1,073.6/1,171.3 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1572 | 1,099.1 | 1,096.2/1,165.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1573 | 1,098.2 | 1,094.5/1,100.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1574 | 1,082.8 | 1,077.8/1,100.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1575 | 1,077.1 | 1,076.0/1,101.5 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1576 | 1,073.9 | 1,053.3/1,103.2 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1577 | 1,070.8 | 1,060.2/1,109.8 | 294.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1578 | 1,058.1 | 1,038.0/1,098.1 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1579 | 209.2 | 201.1/218.1 | 663.5 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1580 | 625.3 | 617.3/654.4 | 7.2 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1581 | 44.0 | 43.5/54.9 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1582 | 1,157.7 | 1,127.3/1,250.7 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1583 | 1,122.9 | 1,070.6/1,196.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1584 | 1,078.5 | 1,078.5/1,105.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1585 | 1,107.7 | 1,105.8/1,293.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1586 | 1,134.9 | 1,094.8/1,673.4 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1587 | 1,170.8 | 1,102.7/1,218.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1588 | 1,163.3 | 1,080.3/1,226.7 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1589 | 1,151.6 | 1,096.9/1,237.9 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1590 | 1,104.2 | 1,090.6/1,264.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1591 | 1,095.3 | 1,079.0/1,159.5 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1592 | 1,076.9 | 1,045.2/1,082.5 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1593 | 1,053.7 | 1,039.5/1,077.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1594 | 1,046.8 | 1,046.6/1,051.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1595 | 1,055.2 | 1,041.7/1,062.6 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1596 | 1,050.4 | 1,046.2/1,068.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1597 | 1,056.5 | 1,038.4/1,088.0 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1598 | 1,049.9 | 1,044.4/1,065.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1599 | 1,066.5 | 1,043.5/1,077.5 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1600 | 1,069.6 | 1,066.7/1,077.3 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1601 | 1,057.7 | 1,054.0/1,133.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1602 | 1,053.2 | 1,045.4/1,161.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1603 | 1,066.0 | 1,046.9/1,172.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1604 | 1,151.2 | 1,137.8/1,171.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1605 | 1,186.5 | 1,183.3/1,197.3 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1606 | 1,185.3 | 1,174.5/1,200.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1607 | 1,201.9 | 1,161.2/1,208.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1608 | 1,202.7 | 1,172.1/1,232.9 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1609 | 1,222.6 | 1,172.0/1,245.8 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1610 | 228.0 | 214.0/240.9 | 663.0 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1611 | 616.2 | 614.0/638.8 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1612 | 49.9 | 41.6/60.0 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1613 | 1,252.4 | 1,248.1/1,282.8 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1614 | 1,193.5 | 1,179.6/1,375.3 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1615 | 1,199.7 | 1,052.8/1,203.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1616 | 1,206.0 | 1,051.6/1,220.8 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1617 | 1,196.2 | 1,064.3/1,215.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1618 | 1,185.6 | 1,049.7/1,207.9 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1619 | 1,187.6 | 1,043.4/1,240.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1620 | 1,185.7 | 1,068.9/1,216.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1621 | 1,196.1 | 1,046.3/1,219.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1622 | 1,197.2 | 1,040.0/1,209.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1623 | 1,197.4 | 1,048.9/1,201.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1624 | 1,172.0 | 1,042.4/1,195.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1625 | 1,117.5 | 1,045.2/1,458.6 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1626 | 1,157.2 | 1,150.1/1,253.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1627 | 1,202.9 | 1,184.5/1,238.5 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1628 | 1,199.5 | 1,174.2/1,232.1 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1629 | 1,221.1 | 1,217.2/1,222.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1630 | 1,201.6 | 1,187.3/1,215.3 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1631 | 1,197.6 | 1,173.3/1,210.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1632 | 1,203.9 | 1,186.3/1,215.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1633 | 1,201.3 | 1,170.8/1,218.6 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1634 | 1,186.6 | 1,152.1/1,206.2 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1635 | 1,176.7 | 1,118.3/1,237.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1636 | 1,205.7 | 1,125.4/1,207.5 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1637 | 1,220.0 | 1,109.7/1,232.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1638 | 1,202.3 | 1,090.0/1,219.6 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1639 | 1,206.0 | 1,080.6/1,207.5 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1640 | 1,198.4 | 1,075.6/5,794.6 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1641 | 247.2 | 216.1/249.9 | 661.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1642 | 613.7 | 611.0/616.2 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1643 | 57.8 | 53.9/64.6 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1644 | 1,266.0 | 1,145.6/1,292.3 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1645 | 1,236.4 | 1,120.9/1,243.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1646 | 1,218.5 | 1,114.4/1,225.1 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1647 | 1,224.0 | 1,101.7/1,240.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1648 | 1,205.5 | 1,112.2/1,215.2 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1649 | 1,188.9 | 1,138.8/1,293.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1650 | 1,182.1 | 1,106.8/1,226.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1651 | 1,169.7 | 1,108.2/1,222.1 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1652 | 1,162.0 | 1,123.6/1,210.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1653 | 1,158.0 | 1,123.7/1,214.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1654 | 1,186.0 | 1,111.6/1,202.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1655 | 1,191.7 | 1,130.7/1,215.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1656 | 1,185.9 | 1,119.1/1,207.0 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1657 | 1,176.1 | 1,105.9/1,249.4 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1658 | 1,163.7 | 1,106.9/1,212.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1659 | 1,162.9 | 1,105.4/1,229.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1660 | 1,166.3 | 1,105.3/1,216.9 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1661 | 1,172.9 | 1,107.8/1,212.0 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1662 | 1,159.5 | 1,106.0/1,211.6 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1663 | 1,103.9 | 1,087.4/1,216.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1664 | 1,112.9 | 1,073.0/1,215.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1665 | 1,165.9 | 1,044.8/1,267.9 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1666 | 1,162.0 | 1,048.5/1,233.5 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1667 | 1,169.2 | 1,054.2/1,234.7 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1668 | 1,189.2 | 1,056.1/1,208.8 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1669 | 1,203.7 | 1,072.6/1,212.3 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1670 | 1,208.7 | 1,071.2/1,209.1 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1671 | 1,199.5 | 1,099.5/1,229.1 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1672 | 232.1 | 223.7/245.3 | 662.7 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1673 | 606.4 | 604.8/619.9 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1674 | 53.3 | 52.0/79.7 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1675 | 1,289.4 | 1,253.1/1,356.2 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1676 | 1,233.4 | 1,206.3/1,240.0 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1677 | 1,220.1 | 1,169.7/1,223.7 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1678 | 1,208.5 | 1,173.2/1,210.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1679 | 1,219.4 | 1,106.0/1,221.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1680 | 1,220.7 | 1,133.7/1,231.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1681 | 1,206.9 | 1,086.5/1,231.7 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1682 | 1,125.1 | 1,072.0/1,205.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1683 | 1,103.1 | 1,082.6/1,205.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1684 | 1,100.8 | 1,080.4/1,146.0 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1685 | 1,116.3 | 1,077.4/1,162.6 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1686 | 1,102.8 | 1,079.8/1,195.4 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1687 | 1,112.0 | 1,108.2/1,201.1 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1688 | 1,086.6 | 1,079.8/1,207.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1689 | 1,072.6 | 1,069.1/1,189.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1690 | 1,091.4 | 1,063.3/1,202.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1691 | 1,142.1 | 1,066.4/1,239.2 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1692 | 1,201.8 | 1,088.6/1,212.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1693 | 1,200.2 | 1,085.9/1,210.6 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1694 | 1,201.6 | 1,083.7/1,202.8 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1695 | 1,206.6 | 1,151.1/1,220.1 | 213.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1696 | 1,179.4 | 1,142.5/1,207.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1697 | 1,174.1 | 1,093.4/1,214.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1698 | 1,189.4 | 1,096.2/1,208.9 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1699 | 1,180.1 | 1,109.7/1,226.8 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1700 | 1,184.7 | 1,104.8/1,337.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1701 | 1,202.2 | 1,097.8/1,212.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1702 | 1,206.5 | 1,099.8/1,207.9 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1703 | 239.7 | 224.2/241.6 | 663.3 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1704 | 622.0 | 616.8/622.6 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1705 | 58.1 | 48.0/58.6 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1706 | 1,279.9 | 1,176.9/1,286.0 | 203.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1707 | 1,225.4 | 1,117.0/1,227.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1708 | 1,229.0 | 1,078.5/1,237.2 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1709 | 1,207.9 | 1,078.5/1,270.9 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1710 | 1,215.5 | 1,078.0/1,226.4 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1711 | 1,121.7 | 1,090.7/1,221.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1712 | 1,130.7 | 1,090.8/1,217.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1713 | 1,080.4 | 1,055.7/1,227.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1714 | 1,074.3 | 1,051.4/1,207.4 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1715 | 1,105.7 | 1,080.2/1,206.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1716 | 1,095.7 | 1,067.6/1,196.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1717 | 1,160.0 | 1,120.9/1,260.1 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1718 | 1,200.9 | 1,101.0/1,209.1 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1719 | 1,187.6 | 1,125.0/1,204.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1720 | 1,211.5 | 1,136.9/1,215.8 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1721 | 1,192.8 | 1,120.3/1,223.1 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1722 | 1,203.1 | 1,155.2/1,208.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1723 | 1,193.5 | 1,168.9/1,202.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1724 | 1,195.2 | 1,163.2/1,209.1 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1725 | 1,190.0 | 1,167.4/1,249.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1726 | 1,172.0 | 1,124.0/1,214.1 | 204.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1727 | 1,207.6 | 1,170.7/1,530.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1728 | 1,191.3 | 1,158.0/1,207.2 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1729 | 1,206.8 | 1,174.8/1,231.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1730 | 1,194.2 | 1,174.5/1,212.4 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1731 | 1,205.1 | 1,168.5/1,906.0 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1732 | 1,235.2 | 1,215.8/2,219.1 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1733 | 1,212.8 | 1,172.6/1,240.1 | 201.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1734 | 232.2 | 229.7/243.9 | 662.3 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1735 | 615.8 | 599.6/619.0 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1736 | 53.4 | 49.5/58.7 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1737 | 1,294.3 | 1,272.7/1,331.6 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1738 | 1,231.0 | 1,184.3/1,384.1 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1739 | 1,219.6 | 1,181.0/1,238.2 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1740 | 1,212.9 | 1,212.3/1,217.5 | 205.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1741 | 1,206.3 | 1,203.6/1,232.0 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1742 | 1,199.0 | 1,196.6/1,253.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1743 | 1,197.8 | 1,193.5/1,209.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1744 | 1,201.6 | 1,198.2/1,229.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1745 | 1,210.5 | 1,193.1/1,221.9 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1746 | 1,219.2 | 1,196.1/1,484.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1747 | 1,223.8 | 1,200.0/1,395.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1748 | 1,197.0 | 1,176.4/1,207.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1749 | 1,188.7 | 1,170.4/1,209.0 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1750 | 1,192.0 | 1,168.4/1,214.9 | 204.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1751 | 1,192.2 | 1,181.3/1,200.9 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1752 | 1,205.4 | 1,204.0/1,476.9 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1753 | 1,225.0 | 1,198.8/1,444.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1754 | 1,200.7 | 1,189.0/1,221.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1755 | 1,217.8 | 1,199.7/1,226.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1756 | 1,200.3 | 1,178.9/1,218.9 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1757 | 1,203.0 | 1,199.3/1,209.7 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1758 | 1,214.5 | 1,196.2/1,215.9 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1759 | 1,202.0 | 1,167.8/1,207.5 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1760 | 1,197.9 | 1,163.1/1,259.6 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1761 | 1,173.7 | 1,156.5/1,234.4 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1762 | 1,129.0 | 1,110.1/1,220.2 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1763 | 1,105.6 | 1,093.8/1,208.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1764 | 1,085.9 | 1,076.3/1,204.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1765 | 220.9 | 210.4/247.6 | 661.8 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1766 | 619.1 | 605.3/626.6 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1767 | 52.8 | 46.1/60.1 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1768 | 1,190.3 | 1,088.5/1,315.2 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1769 | 1,105.3 | 1,053.9/1,264.4 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1770 | 1,106.5 | 1,095.2/1,238.1 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1771 | 1,182.8 | 1,115.4/1,186.1 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1772 | 1,181.6 | 1,083.8/1,184.6 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1773 | 1,177.3 | 1,109.2/1,182.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1774 | 1,173.5 | 1,125.9/1,190.7 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1775 | 1,172.8 | 1,108.1/1,174.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1776 | 1,153.9 | 1,144.7/1,222.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1777 | 1,113.0 | 1,099.9/1,256.7 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1778 | 1,133.0 | 1,099.7/1,211.7 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1779 | 1,124.5 | 1,076.8/1,180.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1780 | 1,128.1 | 1,079.5/1,128.7 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1781 | 1,111.0 | 1,064.9/1,178.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1782 | 1,113.1 | 1,063.5/1,161.9 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1783 | 1,175.7 | 1,116.6/1,177.7 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1784 | 1,142.8 | 1,096.1/1,143.8 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1785 | 1,168.9 | 1,122.7/1,211.9 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1786 | 1,161.5 | 1,111.6/1,200.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1787 | 1,188.5 | 1,087.8/1,225.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1788 | 1,183.7 | 1,080.8/1,386.8 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1789 | 1,189.5 | 1,154.2/1,487.0 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1790 | 1,216.9 | 1,134.5/1,507.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1791 | 1,207.8 | 1,102.8/1,349.8 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1792 | 1,209.0 | 1,116.8/1,311.4 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1793 | 1,201.5 | 1,111.8/1,234.5 | 203.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1794 | 1,226.3 | 1,101.6/1,232.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1795 | 1,219.9 | 1,091.8/1,279.6 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1796 | 253.1 | 211.5/258.4 | 663.1 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1797 | 613.6 | 613.4/624.7 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1798 | 57.8 | 45.9/60.4 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1799 | 1,295.4 | 1,159.3/1,300.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1800 | 1,227.5 | 1,097.1/1,237.1 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1801 | 1,219.3 | 1,082.2/1,233.9 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1802 | 1,204.1 | 1,044.3/1,246.2 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1803 | 1,221.9 | 1,064.5/1,229.0 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1804 | 1,215.9 | 1,047.5/1,230.3 | 209.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1805 | 1,228.3 | 1,051.7/1,230.1 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1806 | 1,223.8 | 1,128.2/1,242.7 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1807 | 1,220.7 | 1,165.6/1,244.6 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1808 | 1,207.1 | 1,178.3/1,210.4 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1809 | 1,201.8 | 1,162.3/1,210.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1810 | 1,205.5 | 1,156.2/1,267.4 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1811 | 1,193.3 | 1,162.9/1,224.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1812 | 1,227.2 | 1,225.8/1,536.5 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1813 | 1,222.1 | 1,203.4/1,237.8 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1814 | 1,214.5 | 1,206.1/1,217.5 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1815 | 1,214.4 | 1,203.1/1,215.8 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1816 | 1,213.7 | 1,204.3/1,214.4 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1817 | 1,215.6 | 1,214.7/1,239.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1818 | 1,214.9 | 1,146.3/1,229.5 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1819 | 1,210.1 | 1,105.7/1,223.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1820 | 1,229.1 | 1,086.8/1,234.5 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1821 | 1,206.5 | 1,085.9/1,240.3 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1822 | 1,203.5 | 1,081.5/1,227.1 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1823 | 1,206.2 | 1,143.4/1,239.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1824 | 1,193.8 | 1,189.0/1,215.2 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1825 | 1,200.0 | 1,181.1/1,204.2 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1826 | 1,209.5 | 1,168.1/1,232.2 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1827 | 248.0 | 242.7/248.4 | 662.9 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1828 | 613.8 | 610.0/616.4 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1829 | 60.2 | 59.8/62.3 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1830 | 1,275.8 | 1,222.2/1,316.7 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1831 | 1,219.2 | 1,124.2/1,263.6 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1832 | 1,224.9 | 1,134.2/1,270.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1833 | 1,218.8 | 1,099.9/1,228.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1834 | 1,220.4 | 1,072.5/1,226.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1835 | 1,213.6 | 1,076.1/1,220.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1836 | 1,231.2 | 1,084.2/1,269.6 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1837 | 1,213.4 | 1,094.2/1,247.3 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1838 | 1,208.3 | 1,116.8/1,287.5 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1839 | 1,208.8 | 1,091.6/1,304.2 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1840 | 1,151.2 | 1,084.2/1,296.4 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1841 | 1,118.7 | 1,088.8/1,271.1 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1842 | 1,176.2 | 1,078.3/1,258.1 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1843 | 1,179.1 | 1,087.2/1,280.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1844 | 1,174.5 | 1,070.2/1,295.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1845 | 1,188.5 | 1,082.6/1,298.5 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1846 | 1,226.0 | 1,117.8/1,315.6 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1847 | 1,215.6 | 1,105.3/1,284.0 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1848 | 1,237.9 | 1,071.7/1,274.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1849 | 1,213.4 | 1,085.6/1,290.6 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1850 | 1,229.4 | 1,090.4/1,240.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1851 | 1,214.4 | 1,082.0/1,232.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1852 | 1,202.8 | 1,077.7/1,284.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1853 | 1,218.8 | 1,074.3/1,279.6 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1854 | 1,175.9 | 1,106.4/1,221.0 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1855 | 1,133.5 | 1,128.0/1,219.8 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1856 | 1,137.0 | 1,124.5/1,202.3 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1857 | 1,136.3 | 1,100.5/1,218.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1858 | 235.9 | 232.4/245.8 | 662.5 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1859 | 607.1 | 605.4/609.5 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1860 | 58.1 | 54.4/60.2 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1861 | 1,322.1 | 1,157.4/1,334.5 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1862 | 1,205.8 | 1,104.9/1,425.6 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1863 | 1,215.8 | 1,087.0/1,228.4 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1864 | 1,213.3 | 1,085.2/1,230.1 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1865 | 1,225.3 | 1,108.5/1,262.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1866 | 1,200.5 | 1,112.2/1,203.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1867 | 1,169.6 | 1,098.2/1,200.3 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1868 | 1,130.3 | 1,081.7/1,202.3 | 201.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1869 | 1,119.1 | 1,083.8/1,258.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1870 | 1,113.4 | 1,091.7/1,226.1 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1871 | 1,109.3 | 1,082.5/1,207.0 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1872 | 1,093.8 | 1,082.6/1,204.3 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1873 | 1,130.2 | 1,095.4/1,185.9 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1874 | 1,188.8 | 1,131.6/1,207.7 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1875 | 1,174.1 | 1,116.3/1,201.0 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1876 | 1,133.7 | 1,128.2/1,174.1 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1877 | 1,117.8 | 1,112.4/1,175.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1878 | 1,176.7 | 1,112.1/1,185.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1879 | 1,128.4 | 1,107.0/1,175.0 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1880 | 1,116.1 | 1,088.5/1,172.4 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1881 | 1,149.8 | 1,114.5/1,174.8 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1882 | 1,109.8 | 1,095.1/1,210.6 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1883 | 1,112.6 | 1,088.1/1,186.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1884 | 1,110.1 | 1,097.5/1,170.5 | 204.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1885 | 1,105.8 | 1,079.5/1,170.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1886 | 1,121.4 | 1,082.6/1,177.6 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1887 | 1,139.7 | 1,108.3/1,185.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1888 | 1,154.8 | 1,072.8/1,169.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1889 | 236.0 | 212.4/240.8 | 662.4 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1890 | 620.2 | 611.7/691.0 | 7.2 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1891 | 57.9 | 51.6/59.5 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1892 | 1,299.3 | 1,143.9/1,305.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1893 | 1,218.8 | 1,214.0/1,234.5 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1894 | 1,203.4 | 1,136.9/1,220.6 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1895 | 1,194.7 | 1,161.5/1,221.2 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1896 | 1,195.2 | 1,117.2/1,265.1 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1897 | 1,178.0 | 1,119.1/1,227.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1898 | 1,177.1 | 1,113.6/1,218.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1899 | 1,166.7 | 1,112.8/1,220.5 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1900 | 1,196.2 | 1,159.3/1,209.4 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1901 | 1,217.7 | 1,215.2/1,226.0 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1902 | 1,207.3 | 1,202.5/1,211.2 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1903 | 1,206.6 | 1,196.5/1,240.3 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1904 | 1,214.8 | 1,189.3/1,265.1 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1905 | 1,218.7 | 1,172.9/1,222.8 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1906 | 1,207.9 | 1,173.3/1,213.9 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1907 | 1,223.7 | 1,174.0/1,249.1 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1908 | 1,205.5 | 1,171.1/1,257.5 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1909 | 1,218.1 | 1,212.4/1,298.1 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1910 | 1,212.6 | 1,206.1/1,226.2 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1911 | 1,193.7 | 1,154.8/1,203.8 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1912 | 1,169.9 | 1,102.2/1,258.7 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1913 | 1,173.0 | 1,112.9/1,218.1 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1914 | 1,186.7 | 1,153.2/1,203.8 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1915 | 1,177.7 | 1,106.5/1,179.7 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1916 | 1,170.0 | 1,105.8/1,177.2 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1917 | 1,175.1 | 1,117.3/1,202.0 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1918 | 1,171.5 | 1,112.0/1,191.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1919 | 1,150.7 | 1,106.9/1,176.7 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1920 | 232.4 | 229.0/236.4 | 663.5 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1921 | 621.6 | 619.6/624.8 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1922 | 53.0 | 52.8/56.0 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1923 | 1,198.8 | 1,172.1/1,266.7 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1924 | 1,126.8 | 1,119.0/1,197.9 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1925 | 1,190.3 | 1,128.6/1,223.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1926 | 1,205.7 | 1,133.0/1,214.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1927 | 1,210.7 | 1,177.7/1,267.1 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1928 | 1,216.7 | 1,173.2/1,218.1 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1929 | 1,207.0 | 1,195.1/1,241.8 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1930 | 1,208.3 | 1,206.9/1,273.8 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1931 | 1,208.6 | 1,185.4/1,251.9 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1932 | 1,210.3 | 1,173.4/1,214.5 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1933 | 1,171.9 | 1,170.2/1,207.3 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1934 | 1,191.2 | 1,161.6/1,205.6 | 202.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1935 | 1,215.5 | 1,200.8/1,219.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1936 | 1,215.4 | 1,170.1/1,435.2 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1937 | 1,191.8 | 1,150.6/1,247.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1938 | 1,201.1 | 1,114.1/1,858.9 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1939 | 1,228.9 | 1,104.7/1,233.8 | 202.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1940 | 1,212.5 | 1,111.3/1,222.4 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1941 | 1,200.2 | 1,158.0/1,209.5 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1942 | 1,219.6 | 1,201.7/1,240.7 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1943 | 1,201.5 | 1,132.2/1,206.8 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1944 | 1,206.1 | 1,145.7/1,242.9 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1945 | 1,170.9 | 1,121.4/1,199.1 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1946 | 1,197.6 | 1,113.2/1,394.6 | 203.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1947 | 1,203.8 | 1,180.6/1,248.4 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1948 | 1,219.7 | 1,201.4/1,225.5 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1949 | 1,209.5 | 1,209.2/1,213.2 | 202.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1950 | 1,219.9 | 1,215.7/1,224.3 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1951 | 248.6 | 245.8/272.0 | 663.3 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1952 | 613.0 | 606.8/621.0 | 7.1 | cudaStreamSynchronize | 1 |
| answer | mir_operator:decode_embed | 1953 | 58.8 | 53.3/72.7 | 1.9 | cudaLaunchKernel | 1 |
| answer | mir_operator:decode_layer00 | 1954 | 1,312.2 | 1,307.5/1,319.4 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer01 | 1955 | 1,231.2 | 1,201.8/1,301.2 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer02 | 1956 | 1,218.7 | 1,145.3/1,251.6 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer03 | 1957 | 1,232.8 | 1,095.1/1,247.4 | 204.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer04 | 1958 | 1,211.4 | 1,105.5/1,229.8 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer05 | 1959 | 1,183.9 | 1,105.8/1,184.7 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer06 | 1960 | 1,169.9 | 1,108.9/1,210.8 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer07 | 1961 | 1,202.9 | 1,111.0/1,209.6 | 203.1 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer08 | 1962 | 1,213.6 | 1,132.9/1,234.2 | 202.0 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer09 | 1963 | 1,183.1 | 1,147.5/1,248.8 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer10 | 1964 | 1,178.2 | 1,176.7/1,212.4 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer11 | 1965 | 1,174.3 | 1,137.8/1,206.6 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer12 | 1966 | 1,132.5 | 1,106.5/1,216.9 | 203.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer13 | 1967 | 1,115.3 | 1,101.7/1,224.1 | 202.5 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer14 | 1968 | 1,109.3 | 1,107.5/1,208.5 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer15 | 1969 | 1,110.6 | 1,109.1/1,205.1 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer16 | 1970 | 1,164.0 | 1,122.8/1,230.2 | 202.8 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer17 | 1971 | 1,254.8 | 1,110.8/1,840.9 | 254.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer18 | 1972 | 1,217.6 | 1,086.5/1,285.5 | 202.9 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer19 | 1973 | 1,209.9 | 1,080.6/1,290.5 | 202.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer20 | 1974 | 1,204.8 | 1,069.3/1,254.3 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer21 | 1975 | 1,225.2 | 1,073.4/1,518.7 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer22 | 1976 | 1,220.2 | 1,056.4/1,347.4 | 202.6 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer23 | 1977 | 1,216.2 | 1,048.5/1,224.3 | 202.7 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer24 | 1978 | 1,224.3 | 1,041.2/1,229.0 | 203.4 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer25 | 1979 | 1,219.1 | 1,043.8/1,279.9 | 203.2 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer26 | 1980 | 1,216.8 | 1,140.0/1,230.5 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_layer27 | 1981 | 1,218.6 | 1,155.3/1,243.4 | 203.3 | cudaLaunchKernel | 57 |
| answer | mir_operator:decode_head | 1982 | 243.9 | 233.7/248.0 | 662.5 | cudaLaunchKernel | 9 |
| answer | mir_operator:decode_sample | 1983 | 611.6 | 608.6/621.5 | 7.2 | cudaStreamSynchronize | 1 |
| answer | pre_d2h_alloc |  | 308.3 | 265.6/2,959.7 | 0.7 | cudaMemcpyAsync | 0 |
| answer | d2h_stage |  | 139.4 | 129.2/146.1 | 0.9 | cudaEventRecordWithFlags | 0 |
| answer | checksum_complete |  | 50.7 | 49.7/51.8 | 0.0 | cudaEventDestroy | 0 |
| <dag> | dag_schedule_gap |  | 73.1 | 16.2/848.3 | 0.0 |  | 0 |
| <dag> | iteration_tail_sync |  | 118.0 | 110.4/118.3 | 0.0 | cudaDeviceSynchronize | 0 |

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

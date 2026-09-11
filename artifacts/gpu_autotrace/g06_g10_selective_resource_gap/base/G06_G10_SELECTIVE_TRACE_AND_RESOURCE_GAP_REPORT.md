# G06-G10 selective process trace and resource gap: lineage `base`

Lineage `h22-gpu-autotrace`, workflow w05. Admission ledger (sha256 of every upstream handoff) is in `tables_manifest.json`.
Two views follow. The first hides nothing below the 10 % threshold except in the stacks table; the second shows only instances with a
successfully attached hardware metric and says so.

## View A: high-latency process distribution (G06/G07)

### Selection (strictly > 10 % of total process host time)

| workload | process | instances | cumulative (us) | share | median (us) | p90 (us) | max (us) | MAD (us) | GPU-owning | selected |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| react_tool | host_input_generate | 40 | 209,911.7 | 56.26 % | 5,093.9 | 5,136.7 | 8,194.8 | 25.9 | False | **yes** |
| react_tool | adapter_dispatch | 40 | 49,043.6 | 13.14 % | 1,229.3 | 1,315.1 | 1,813.0 | 72.8 | False | **yes** |
| react_tool | dag_schedule_gap | 60 | 25,172.8 | 6.75 % | 62.0 | 1,213.5 | 1,244.5 | 52.1 | False | no |
| react_tool | mir_operator:RMSNormOp | 80 | 20,041.5 | 5.37 % | 247.7 | 287.9 | 298.3 | 20.4 | True | no |
| react_tool | mir_operator:LinearOp | 120 | 15,899.1 | 4.26 % | 119.8 | 154.9 | 853.4 | 11.4 | True | no |
| react_tool | token_preprocess_cpu | 40 | 9,484.9 | 2.54 % | 237.5 | 336.0 | 356.1 | 81.8 | False | no |
| react_tool | h2d_stage | 40 | 6,920.2 | 1.85 % | 179.9 | 195.9 | 317.1 | 6.4 | True | no |
| react_tool | agent_tool_execute_cpu | 20 | 6,382.7 | 1.71 % | 324.1 | 344.2 | 366.5 | 22.2 | False | no |
| react_tool | weight_init | 40 | 5,908.7 | 1.58 % | 149.6 | 169.4 | 177.8 | 6.8 | True | no |
| react_tool | d2h_stage | 40 | 5,491.9 | 1.47 % | 144.8 | 151.6 | 241.6 | 3.0 | True | no |
| react_tool | mir_operator:TransposeOp | 40 | 5,093.8 | 1.37 % | 127.3 | 138.0 | 162.9 | 5.3 | True | no |
| react_tool | mir_operator:AddOp | 40 | 4,155.9 | 1.11 % | 101.1 | 112.8 | 161.8 | 2.1 | True | no |
| react_tool | mir_operator:ViewOp | 40 | 3,021.8 | 0.81 % | 72.5 | 87.7 | 138.4 | 2.3 | False | no |
| react_tool | checksum_complete | 40 | 2,716.2 | 0.73 % | 70.0 | 74.0 | 83.9 | 2.5 | False | no |
| react_tool | inter_operator_dispatch | 280 | 2,306.4 | 0.62 % | 7.8 | 10.3 | 26.1 | 0.8 | False | no |
| react_tool | iteration_tail_sync | 20 | 1,044.5 | 0.28 % | 49.5 | 67.4 | 78.3 | 3.1 | False | no |
| react_tool | pre_d2h_alloc | 40 | 539.8 | 0.14 % | 13.9 | 14.7 | 18.7 | 0.6 | False | no |
| planner_debate | host_input_generate | 100 | 922,181.0 | 69.9 % | 9,087.2 | 11,985.0 | 16,051.0 | 832.9 | False | **yes** |
| planner_debate | adapter_dispatch | 100 | 123,846.7 | 9.39 % | 1,175.9 | 1,317.6 | 2,230.7 | 21.4 | False | no |
| planner_debate | mir_operator:RMSNormOp | 200 | 55,676.5 | 4.22 % | 271.8 | 334.3 | 481.4 | 26.4 | True | no |
| planner_debate | mir_operator:LinearOp | 300 | 36,880.5 | 2.8 % | 110.5 | 159.0 | 341.0 | 14.3 | True | no |
| planner_debate | dag_schedule_gap | 120 | 30,606.8 | 2.32 % | 39.2 | 1,211.1 | 2,250.1 | 13.9 | False | no |
| planner_debate | token_preprocess_cpu | 100 | 30,574.0 | 2.32 % | 332.0 | 370.8 | 420.7 | 27.4 | False | no |
| planner_debate | h2d_stage | 100 | 24,936.5 | 1.89 % | 256.7 | 280.5 | 663.9 | 24.2 | True | no |
| planner_debate | d2h_stage | 100 | 19,930.3 | 1.51 % | 217.6 | 221.5 | 441.2 | 15.5 | True | no |
| planner_debate | weight_init | 100 | 17,358.3 | 1.32 % | 168.7 | 201.7 | 293.9 | 10.7 | True | no |
| planner_debate | mir_operator:TransposeOp | 100 | 13,430.1 | 1.02 % | 129.4 | 148.9 | 221.8 | 3.8 | True | no |
| planner_debate | mir_operator:AddOp | 100 | 11,077.3 | 0.84 % | 104.6 | 123.5 | 184.2 | 3.3 | True | no |
| planner_debate | mir_operator:ViewOp | 100 | 8,373.3 | 0.63 % | 75.8 | 92.5 | 440.2 | 2.1 | False | no |
| planner_debate | checksum_complete | 100 | 7,896.7 | 0.6 % | 76.1 | 91.9 | 150.1 | 4.8 | False | no |
| planner_debate | agent_tool_execute_cpu | 20 | 7,089.6 | 0.54 % | 350.3 | 393.9 | 422.5 | 14.3 | False | no |
| planner_debate | inter_operator_dispatch | 700 | 6,513.8 | 0.49 % | 8.2 | 12.6 | 46.4 | 1.1 | False | no |
| planner_debate | pre_d2h_alloc | 100 | 1,421.0 | 0.11 % | 13.8 | 15.8 | 40.8 | 1.0 | False | no |
| planner_debate | iteration_tail_sync | 20 | 1,399.9 | 0.11 % | 68.2 | 82.7 | 85.4 | 4.7 | False | no |
| react_moa_mcts | host_input_generate | 200 | 2,016,623.4 | 74.68 % | 9,845.2 | 11,968.4 | 13,125.4 | 2,050.9 | False | **yes** |
| react_moa_mcts | adapter_dispatch | 200 | 235,764.7 | 8.73 % | 1,114.6 | 1,276.3 | 2,009.5 | 31.6 | False | no |
| react_moa_mcts | mir_operator:RMSNormOp | 400 | 97,436.2 | 3.61 % | 234.0 | 285.0 | 443.8 | 16.2 | True | no |
| react_moa_mcts | mir_operator:LinearOp | 600 | 67,037.6 | 2.48 % | 103.0 | 140.7 | 322.4 | 9.3 | True | no |
| react_moa_mcts | token_preprocess_cpu | 200 | 59,118.0 | 2.19 % | 302.1 | 355.7 | 410.9 | 28.2 | False | no |
| react_moa_mcts | h2d_stage | 200 | 40,168.6 | 1.49 % | 169.2 | 266.8 | 573.0 | 23.8 | True | no |
| react_moa_mcts | d2h_stage | 200 | 32,711.6 | 1.21 % | 138.9 | 218.8 | 345.1 | 13.0 | True | no |
| react_moa_mcts | dag_schedule_gap | 220 | 29,714.4 | 1.1 % | 30.8 | 72.3 | 1,396.9 | 5.9 | False | no |
| react_moa_mcts | weight_init | 200 | 28,222.6 | 1.05 % | 130.1 | 170.2 | 306.5 | 11.2 | True | no |
| react_moa_mcts | mir_operator:TransposeOp | 200 | 24,017.5 | 0.89 % | 116.1 | 135.8 | 196.5 | 7.4 | True | no |
| react_moa_mcts | mir_operator:AddOp | 200 | 20,499.2 | 0.76 % | 100.3 | 110.6 | 216.9 | 5.0 | True | no |
| react_moa_mcts | mir_operator:ViewOp | 200 | 14,316.5 | 0.53 % | 68.9 | 75.5 | 305.6 | 3.0 | False | no |
| react_moa_mcts | checksum_complete | 200 | 13,089.3 | 0.48 % | 62.1 | 78.2 | 113.9 | 6.8 | False | no |
| react_moa_mcts | inter_operator_dispatch | 1400 | 11,259.7 | 0.42 % | 7.4 | 10.5 | 24.3 | 0.8 | False | no |
| react_moa_mcts | agent_tool_execute_cpu | 20 | 6,494.7 | 0.24 % | 314.5 | 354.1 | 402.5 | 14.9 | False | no |
| react_moa_mcts | pre_d2h_alloc | 200 | 2,583.3 | 0.1 % | 10.7 | 17.2 | 30.7 | 1.6 | False | no |
| react_moa_mcts | iteration_tail_sync | 20 | 1,238.5 | 0.05 % | 60.2 | 70.2 | 76.3 | 4.8 | False | no |

### Five longest instances per selected type (real start/end on the nsys clock)

| workload | process | rank | iter | call | start (ns) | host (us) | GPU (us) | top CUDA API |
|---|---|---:|---:|---|---:|---:|---:|---|
| react_tool | host_input_generate | 1 | 5 | plan | 3486964832 | 8,194.8 | 0.0 | cudaEventQuery |
| react_tool | host_input_generate | 2 | 4 | answer | 3475214616 | 8,124.6 | 0.0 | cudaEventQuery |
| react_tool | host_input_generate | 3 | 16 | plan | 3688982369 | 5,385.4 | 0.0 | cudaEventQuery |
| react_tool | host_input_generate | 4 | 1 | plan | 3408627595 | 5,138.1 | 0.0 | cudaEventQuery |
| react_tool | host_input_generate | 5 | 0 | plan | 3389937065 | 5,136.7 | 0.0 | cudaEventQuery |
| react_tool | adapter_dispatch | 1 | 4 | answer | 3473232280 | 1,813.0 | 0.0 |  |
| react_tool | adapter_dispatch | 2 | 0 | answer | 3398534053 | 1,358.5 | 0.0 |  |
| react_tool | adapter_dispatch | 3 | 7 | answer | 3535826863 | 1,336.8 | 0.0 |  |
| react_tool | adapter_dispatch | 4 | 19 | answer | 3753421234 | 1,321.0 | 0.0 |  |
| react_tool | adapter_dispatch | 5 | 15 | answer | 3679062023 | 1,315.1 | 0.0 |  |
| planner_debate | host_input_generate | 1 | 17 | critic-b | 4768560674 | 16,051.0 | 0.0 | cudaEventQuery |
| planner_debate | host_input_generate | 2 | 16 | planner-seed | 4681327061 | 13,582.3 | 0.0 | cudaEventQuery |
| planner_debate | host_input_generate | 3 | 19 | planner-final | 4927477065 | 12,535.1 | 0.0 | cudaEventQuery |
| planner_debate | host_input_generate | 4 | 4 | critic-a | 3938314045 | 12,396.9 | 0.0 | cudaEventQuery |
| planner_debate | host_input_generate | 5 | 2 | critic-merge | 3819485856 | 12,030.5 | 0.0 | cudaEventQuery |
| react_moa_mcts | host_input_generate | 1 | 9 | moa-map2 | 5229383168 | 13,125.4 | 0.0 | cudaEventQuery |
| react_moa_mcts | host_input_generate | 2 | 1 | mcts-actor0 | 4189560997 | 13,086.9 | 0.0 | cudaEventQuery |
| react_moa_mcts | host_input_generate | 3 | 5 | moa-reduce | 4803560236 | 12,997.9 | 0.0 | cudaEventQuery |
| react_moa_mcts | host_input_generate | 4 | 4 | moa-reduce | 4657728177 | 12,510.8 | 0.0 | cudaEventQuery |
| react_moa_mcts | host_input_generate | 5 | 4 | mcts-actor1 | 4642333826 | 12,510.5 | 0.0 | cudaEventQuery |

### Host/GPU overlap and launch gaps, representative iteration (G07)

| workload | iter | wall (us) | GPU busy | host-only | streams | max concurrent GPU | gaps >= 20 us | gap total (us) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| react_tool | 7 | 18,485.6 | 2.78 % | 82.69 % | 1 | 1 | 27 | 10,744.1 |
| planner_debate | 12 | 62,269.4 | 3.18 % | 85.03 % | 1 | 1 | 90 | 50,698.5 |
| react_moa_mcts | 3 | 144,985.0 | 1.94 % | 90.5 % | 1 | 1 | 102 | 130,640.5 |

Largest GPU launch gaps and the host processes covering them:

| workload | gap start (us) | gap (us) | next GPU item | host processes covering |
|---|---:|---:|---|---|
| react_moa_mcts | 509384.0 | 15,420.2 | mcts-actor0:h2d_stage:memcpy |  |
| react_moa_mcts | 568792.0 | 13,516.8 | mcts-critic:h2d_stage:memcpy |  |
| react_moa_mcts | 479634.1 | 13,484.0 | moa-map2:h2d_stage:memcpy |  |
| react_moa_mcts | 541109.0 | 13,470.9 | moa-reduce:h2d_stage:memcpy |  |
| react_moa_mcts | 526214.2 | 13,459.0 | mcts-actor1:h2d_stage:memcpy |  |
| react_moa_mcts | 449844.9 | 13,448.8 | moa-map0:h2d_stage:memcpy |  |
| react_moa_mcts | 464731.1 | 13,444.6 | moa-map1:h2d_stage:memcpy |  |
| react_moa_mcts | 494543.8 | 13,399.8 | mcts-root:h2d_stage:memcpy |  |
| planner_debate | 843420.6 | 12,516.6 | critic-merge:h2d_stage:memcpy |  |
| react_moa_mcts | 556020.2 | 11,377.7 | react-answer:h2d_stage:memcpy |  |
| planner_debate | 830233.6 | 11,195.6 | critic-b:h2d_stage:memcpy |  |
| planner_debate | 817590.8 | 10,852.8 | critic-a:h2d_stage:memcpy |  |
| planner_debate | 857870.2 | 8,986.6 | planner-final:h2d_stage:memcpy |  |
| react_tool | 145744.4 | 8,324.7 | answer:h2d_stage:memcpy |  |
| planner_debate | 817104.0 | 218.8 | planner-seed:mir_operator:TransposeOp:copy |  |

### High-latency instances (median + 3 MAD per type): 1121 total

| workload | process | iter | call | host (us) | median (us) | excess (us) | class |
|---|---|---:|---|---:|---:|---:|---|
| planner_debate | host_input_generate | 17 | critic-b | 16,051.0 | 9,087.2 | 6,963.8 | sporadic |
| planner_debate | host_input_generate | 16 | planner-seed | 13,582.3 | 9,087.2 | 4,495.2 | sporadic |
| planner_debate | host_input_generate | 19 | planner-final | 12,535.1 | 9,087.2 | 3,448.0 | sporadic |
| planner_debate | host_input_generate | 4 | critic-a | 12,396.9 | 9,087.2 | 3,309.7 | sporadic |
| react_tool | host_input_generate | 5 | plan | 8,194.8 | 5,093.9 | 3,100.9 | sporadic |
| react_tool | host_input_generate | 4 | answer | 8,124.6 | 5,093.9 | 3,030.7 | sporadic |
| planner_debate | host_input_generate | 2 | critic-merge | 12,030.5 | 9,087.2 | 2,943.3 | sporadic |
| planner_debate | host_input_generate | 2 | critic-a | 12,017.9 | 9,087.2 | 2,930.8 | sporadic |
| planner_debate | host_input_generate | 3 | critic-merge | 12,011.4 | 9,087.2 | 2,924.3 | sporadic |
| planner_debate | host_input_generate | 3 | critic-b | 12,008.5 | 9,087.2 | 2,921.4 | sporadic |
| planner_debate | host_input_generate | 3 | critic-a | 12,006.4 | 9,087.2 | 2,919.2 | sporadic |
| planner_debate | host_input_generate | 4 | critic-b | 11,996.2 | 9,087.2 | 2,909.1 | sporadic |
| planner_debate | host_input_generate | 2 | critic-b | 11,985.0 | 9,087.2 | 2,897.9 | sporadic |
| planner_debate | host_input_generate | 1 | critic-a | 11,976.2 | 9,087.2 | 2,889.1 | sporadic |
| planner_debate | host_input_generate | 4 | critic-merge | 11,971.0 | 9,087.2 | 2,883.8 | sporadic |
| planner_debate | host_input_generate | 1 | critic-merge | 11,966.4 | 9,087.2 | 2,879.2 | sporadic |
| planner_debate | host_input_generate | 0 | critic-a | 11,942.9 | 9,087.2 | 2,855.7 | warm_or_first_iteration |
| planner_debate | host_input_generate | 1 | critic-b | 11,934.7 | 9,087.2 | 2,847.5 | sporadic |
| planner_debate | host_input_generate | 0 | critic-merge | 11,929.0 | 9,087.2 | 2,841.9 | warm_or_first_iteration |
| planner_debate | host_input_generate | 0 | critic-b | 11,908.5 | 9,087.2 | 2,821.4 | warm_or_first_iteration |

## View B: resource window (G08)

Only rows with an attached hardware metric are shown with numbers; host-only processes are listed with their status so the coverage is explicit.

| workload | process | selected | share | status | family | SM % | Tensor % | DRAM active % | DRAM BW % peak | L2 % | occupancy % | waves/SM | interpretation |
|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| react_tool | dag_schedule_gap | False | 6.75 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | adapter_dispatch | True | 13.14 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | token_preprocess_cpu | False | 2.54 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | host_input_generate | True | 56.26 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | h2d_stage | False | 1.85 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool | weight_init | False | 1.58 % | profiled | rng_init | 44.0 | 0.0 | 2.22 | 0.0 | 12.81 | 67.78 | 1.0 | underutilised: SM 44 %, DRAM 1 %, L2 13 %, occ 68 % |
| react_tool | weight_init | False | 1.58 % | profiled | elementwise_binary | 2.27 | 0.0 | 40.01 | 0.0 | 18.85 | 25.59 | 0.38 | underutilised: SM 2 %, DRAM 40 %, L2 19 %, occ 25 % |
| react_tool | mir_operator:RMSNormOp | False | 5.37 % | profiled | copy | 2.01 | 0.0 | 39.25 | 0.0 | 22.01 | 29.69 | 0.38 | latency/launch-bound: 0.38 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:RMSNormOp | False | 5.37 % | profiled | elementwise_unary | 0.82 | 0.0 | 27.42 | 0.0 | 13.11 | 16.81 | 0.19 | underutilised: SM 2 %, DRAM 55 %, L2 25 %, occ 25 % |
| react_tool | mir_operator:RMSNormOp | False | 5.37 % | profiled | reduce | 2.63 | 0.0 | 43.36 | 0.0 | 17.06 | 33.23 | 0.12 | underutilised: SM 3 %, DRAM 44 %, L2 17 %, occ 33 % |
| react_tool | mir_operator:RMSNormOp | False | 5.37 % | profiled | elementwise_binary | 6.53 | 0.0 | 25.81 | 0.0 | 13.39 | 38.47 | 0.75 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | inter_operator_dispatch | False | 0.62 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | mir_operator:AddOp | False | 1.11 % | profiled | elementwise_binary | 2.34 | 0.0 | 37.92 | 0.0 | 17.82 | 25.01 | 0.38 | underutilised: SM 2 %, DRAM 38 %, L2 18 %, occ 25 % |
| react_tool | mir_operator:LinearOp | False | 4.26 % | profiled | gemm | 21.05 | 28.66 | 18.34 | 0.0 | 49.56 | 15.03 | 1.5 | underutilised: SM 21 %, DRAM 18 %, L2 50 %, occ 15 % |
| react_tool | mir_operator:ViewOp | False | 0.81 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | mir_operator:TransposeOp | False | 1.37 % | profiled | copy | 5.21 | 0.0 | 13.12 | 0.0 | 78.36 | 68.84 | 0.75 | L2-bandwidth-bound (working set in L2) |
| react_tool | pre_d2h_alloc | False | 0.14 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | d2h_stage | False | 1.47 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool | checksum_complete | False | 0.73 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | agent_tool_execute_cpu | False | 1.71 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | iteration_tail_sync | False | 0.28 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | dag_schedule_gap | False | 2.32 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | adapter_dispatch | False | 9.39 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | token_preprocess_cpu | False | 2.32 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | host_input_generate | True | 69.9 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | h2d_stage | False | 1.89 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate | weight_init | False | 1.32 % | profiled | rng_init | 51.16 | 0.0 | 0.23 | 0.0 | 12.79 | 67.46 | 1.0 | underutilised: SM 51 %, DRAM 0 %, L2 13 %, occ 67 % |
| planner_debate | weight_init | False | 1.32 % | profiled | elementwise_binary | 2.7 | 0.0 | 46.09 | 0.0 | 21.49 | 31.82 | 0.51 | underutilised: SM 3 %, DRAM 47 %, L2 22 %, occ 32 % |
| planner_debate | weight_init | False | 1.32 % | profiled | rng_init | 51.25 | 0.0 | 0.58 | 0.0 | 16.17 | 67.42 | 1.0 | underutilised: SM 51 %, DRAM 1 %, L2 16 %, occ 67 % |
| planner_debate | weight_init | False | 1.32 % | profiled | elementwise_binary | 2.96 | 0.0 | 51.43 | 0.0 | 23.98 | 40.01 | 0.67 | underutilised: SM 3 %, DRAM 51 %, L2 23 %, occ 40 % |
| planner_debate | mir_operator:RMSNormOp | False | 4.22 % | profiled | copy | 8.35 | 0.0 | 45.57 | 0.0 | 26.25 | 38.72 | 0.51 | underutilised: SM 15 %, DRAM 30 %, L2 29 %, occ 47 % |
| planner_debate | mir_operator:RMSNormOp | False | 4.22 % | profiled | elementwise_unary | 0.9 | 0.0 | 29.99 | 0.0 | 13.98 | 20.49 | 0.26 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:RMSNormOp | False | 4.22 % | profiled | reduce | 2.74 | 0.0 | 50.4 | 0.0 | 19.81 | 33.25 | 0.15 | underutilised: SM 3 %, DRAM 52 %, L2 21 %, occ 33 % |
| planner_debate | mir_operator:RMSNormOp | False | 4.22 % | profiled | elementwise_binary | 7.27 | 0.0 | 28.23 | 0.0 | 14.5 | 41.16 | 1.02 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:RMSNormOp | False | 4.22 % | profiled | copy | 9.27 | 0.0 | 51.53 | 0.0 | 29.74 | 48.33 | 0.67 | underutilised: SM 18 %, DRAM 36 %, L2 35 %, occ 60 % |
| planner_debate | mir_operator:RMSNormOp | False | 4.22 % | profiled | elementwise_unary | 0.93 | 0.0 | 31.65 | 0.0 | 14.66 | 26.02 | 0.34 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:RMSNormOp | False | 4.22 % | profiled | reduce | 2.83 | 0.0 | 57.19 | 0.0 | 22.48 | 33.26 | 0.17 | underutilised: SM 3 %, DRAM 57 %, L2 23 %, occ 33 % |
| planner_debate | mir_operator:RMSNormOp | False | 4.22 % | profiled | elementwise_binary | 7.75 | 0.0 | 30.74 | 0.0 | 15.52 | 41.56 | 1.33 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | inter_operator_dispatch | False | 0.49 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | mir_operator:AddOp | False | 0.84 % | profiled | elementwise_binary | 2.76 | 0.0 | 44.01 | 0.0 | 20.5 | 31.86 | 0.51 | underutilised: SM 3 %, DRAM 43 %, L2 20 %, occ 31 % |
| planner_debate | mir_operator:AddOp | False | 0.84 % | profiled | elementwise_binary | 3.19 | 0.0 | 51.74 | 0.0 | 23.89 | 38.96 | 0.67 | underutilised: SM 3 %, DRAM 50 %, L2 23 %, occ 39 % |
| planner_debate | mir_operator:LinearOp | False | 2.8 % | profiled | gemm | 28.57 | 40.97 | 21.1 | 0.0 | 46.6 | 8.33 | 0.77 | tensor-core compute-bound |
| planner_debate | mir_operator:LinearOp | False | 2.8 % | profiled | gemm | 31.48 | 34.17 | 20.26 | 0.0 | 50.65 | 8.33 | 0.5 | underutilised: SM 32 %, DRAM 20 %, L2 51 %, occ 8 % |
| planner_debate | mir_operator:ViewOp | False | 0.63 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | mir_operator:TransposeOp | False | 1.02 % | profiled | copy | 5.37 | 0.0 | 12.63 | 0.0 | 80.56 | 87.96 | 1.02 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:TransposeOp | False | 1.02 % | profiled | copy | 6.98 | 0.0 | 17.13 | 0.0 | 79.66 | 81.21 | 1.33 | L2-bandwidth-bound (working set in L2) |
| planner_debate | pre_d2h_alloc | False | 0.11 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | d2h_stage | False | 1.51 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate | checksum_complete | False | 0.6 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | agent_tool_execute_cpu | False | 0.54 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | iteration_tail_sync | False | 0.11 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | dag_schedule_gap | False | 1.1 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | adapter_dispatch | False | 8.73 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | token_preprocess_cpu | False | 2.19 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | host_input_generate | True | 74.68 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | h2d_stage | False | 1.49 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_moa_mcts | h2d_stage | False | 1.49 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_moa_mcts | weight_init | False | 1.05 % | profiled | rng_init | 51.16 | 0.0 | 0.23 | 0.0 | 12.79 | 67.46 | 1.0 | underutilised: SM 51 %, DRAM 0 %, L2 13 %, occ 67 % |
| react_moa_mcts | weight_init | False | 1.05 % | profiled | elementwise_binary | 2.7 | 0.0 | 46.09 | 0.0 | 21.49 | 31.82 | 0.51 | underutilised: SM 3 %, DRAM 47 %, L2 22 %, occ 32 % |
| react_moa_mcts | weight_init | False | 1.05 % | profiled | rng_init | 51.25 | 0.0 | 0.58 | 0.0 | 16.17 | 67.42 | 1.0 | underutilised: SM 51 %, DRAM 1 %, L2 16 %, occ 67 % |
| react_moa_mcts | weight_init | False | 1.05 % | profiled | elementwise_binary | 2.96 | 0.0 | 51.43 | 0.0 | 23.98 | 40.01 | 0.67 | underutilised: SM 3 %, DRAM 51 %, L2 23 %, occ 40 % |
| react_moa_mcts | weight_init | False | 1.05 % | profiled | rng_init | 44.0 | 0.0 | 2.22 | 0.0 | 12.81 | 67.78 | 1.0 | underutilised: SM 44 %, DRAM 1 %, L2 13 %, occ 68 % |
| react_moa_mcts | weight_init | False | 1.05 % | profiled | elementwise_binary | 2.27 | 0.0 | 40.01 | 0.0 | 18.85 | 25.59 | 0.38 | underutilised: SM 2 %, DRAM 40 %, L2 19 %, occ 25 % |
| react_moa_mcts | mir_operator:RMSNormOp | False | 3.61 % | profiled | copy | 8.35 | 0.0 | 45.57 | 0.0 | 26.25 | 38.72 | 0.51 | underutilised: SM 15 %, DRAM 30 %, L2 29 %, occ 47 % |
| react_moa_mcts | mir_operator:RMSNormOp | False | 3.61 % | profiled | elementwise_unary | 0.9 | 0.0 | 29.99 | 0.0 | 13.98 | 20.49 | 0.26 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:RMSNormOp | False | 3.61 % | profiled | reduce | 2.74 | 0.0 | 50.4 | 0.0 | 19.81 | 33.25 | 0.15 | underutilised: SM 3 %, DRAM 52 %, L2 21 %, occ 33 % |
| react_moa_mcts | mir_operator:RMSNormOp | False | 3.61 % | profiled | elementwise_binary | 7.27 | 0.0 | 28.23 | 0.0 | 14.5 | 41.16 | 1.02 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:RMSNormOp | False | 3.61 % | profiled | copy | 9.27 | 0.0 | 51.53 | 0.0 | 29.74 | 48.33 | 0.67 | underutilised: SM 18 %, DRAM 36 %, L2 35 %, occ 60 % |
| react_moa_mcts | mir_operator:RMSNormOp | False | 3.61 % | profiled | elementwise_unary | 0.93 | 0.0 | 31.65 | 0.0 | 14.66 | 26.02 | 0.34 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:RMSNormOp | False | 3.61 % | profiled | reduce | 2.83 | 0.0 | 57.19 | 0.0 | 22.48 | 33.26 | 0.17 | underutilised: SM 3 %, DRAM 57 %, L2 23 %, occ 33 % |
| react_moa_mcts | mir_operator:RMSNormOp | False | 3.61 % | profiled | elementwise_binary | 7.75 | 0.0 | 30.74 | 0.0 | 15.52 | 41.56 | 1.33 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:RMSNormOp | False | 3.61 % | profiled | copy | 2.01 | 0.0 | 39.25 | 0.0 | 22.01 | 29.69 | 0.38 | latency/launch-bound: 0.38 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:RMSNormOp | False | 3.61 % | profiled | elementwise_unary | 0.82 | 0.0 | 27.42 | 0.0 | 13.11 | 16.81 | 0.19 | underutilised: SM 2 %, DRAM 55 %, L2 25 %, occ 25 % |
| react_moa_mcts | mir_operator:RMSNormOp | False | 3.61 % | profiled | reduce | 2.63 | 0.0 | 43.36 | 0.0 | 17.06 | 33.23 | 0.12 | underutilised: SM 3 %, DRAM 44 %, L2 17 %, occ 33 % |
| react_moa_mcts | mir_operator:RMSNormOp | False | 3.61 % | profiled | elementwise_binary | 6.53 | 0.0 | 25.81 | 0.0 | 13.39 | 38.47 | 0.75 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | inter_operator_dispatch | False | 0.42 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | mir_operator:AddOp | False | 0.76 % | profiled | elementwise_binary | 2.76 | 0.0 | 44.01 | 0.0 | 20.5 | 31.86 | 0.51 | underutilised: SM 3 %, DRAM 43 %, L2 20 %, occ 31 % |
| react_moa_mcts | mir_operator:AddOp | False | 0.76 % | profiled | elementwise_binary | 3.19 | 0.0 | 51.74 | 0.0 | 23.89 | 38.96 | 0.67 | underutilised: SM 3 %, DRAM 50 %, L2 23 %, occ 39 % |
| react_moa_mcts | mir_operator:AddOp | False | 0.76 % | profiled | elementwise_binary | 2.34 | 0.0 | 37.92 | 0.0 | 17.82 | 25.01 | 0.38 | underutilised: SM 2 %, DRAM 38 %, L2 18 %, occ 25 % |
| react_moa_mcts | mir_operator:LinearOp | False | 2.48 % | profiled | gemm | 28.57 | 40.97 | 21.1 | 0.0 | 46.6 | 8.33 | 0.77 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:LinearOp | False | 2.48 % | profiled | gemm | 31.48 | 34.17 | 20.26 | 0.0 | 50.65 | 8.33 | 0.5 | underutilised: SM 32 %, DRAM 20 %, L2 51 %, occ 8 % |
| react_moa_mcts | mir_operator:LinearOp | False | 2.48 % | profiled | gemm | 21.05 | 28.66 | 18.34 | 0.0 | 49.56 | 15.03 | 1.5 | underutilised: SM 21 %, DRAM 18 %, L2 50 %, occ 15 % |
| react_moa_mcts | mir_operator:ViewOp | False | 0.53 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | mir_operator:TransposeOp | False | 0.89 % | profiled | copy | 5.37 | 0.0 | 12.63 | 0.0 | 80.56 | 87.96 | 1.02 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:TransposeOp | False | 0.89 % | profiled | copy | 6.98 | 0.0 | 17.13 | 0.0 | 79.66 | 81.21 | 1.33 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:TransposeOp | False | 0.89 % | profiled | copy | 5.21 | 0.0 | 13.12 | 0.0 | 78.36 | 68.84 | 0.75 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | pre_d2h_alloc | False | 0.1 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | d2h_stage | False | 1.21 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_moa_mcts | d2h_stage | False | 1.21 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_moa_mcts | checksum_complete | False | 0.48 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | agent_tool_execute_cpu | False | 0.24 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | iteration_tail_sync | False | 0.05 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |

### Opportunities (derived, bounded by measured evidence)

| workload | opportunity | current per iter (us) | reference per iter (us) | bound (% of wall) | note |
|---|---|---:|---:|---:|---|
| react_tool | move_input_generation_to_device | 10,495.6 | 10.9 | 56.26 % | seeded CPU-generator uniform_ into pinned fp16 is single-threaded and O(n^2); device randn for the same n^2 is the weight_init GPU time |
| react_tool | remove_per_operator_synchronize | 2,410.6 | 167.6 | 12.02 % | each operator ends with cudaEventSynchronize; the host range minus GPU work is dispatch + sync latency that async launch would hide |
| react_tool | gpu_idle_window | 18,169.1 | 487.6 | 97.39 % | upper bound on wall reduction if all host work were overlapped or removed; single stream, no kernel concurrency observed |
| planner_debate | move_input_generation_to_device | 46,109.1 | 34.7 | 69.9 % | seeded CPU-generator uniform_ into pinned fp16 is single-threaded and O(n^2); device randn for the same n^2 is the weight_init GPU time |
| planner_debate | remove_per_operator_synchronize | 6,271.9 | 549.0 | 8.68 % | each operator ends with cudaEventSynchronize; the host range minus GPU work is dispatch + sync latency that async launch would hide |
| planner_debate | gpu_idle_window | 64,020.7 | 1,939.0 | 97.06 % | upper bound on wall reduction if all host work were overlapped or removed; single stream, no kernel concurrency observed |
| react_moa_mcts | move_input_generation_to_device | 100,831.2 | 68.1 | 74.68 % | seeded CPU-generator uniform_ into pinned fp16 is single-threaded and O(n^2); device randn for the same n^2 is the weight_init GPU time |
| react_moa_mcts | remove_per_operator_synchronize | 11,165.3 | 1,116.9 | 7.44 % | each operator ends with cudaEventSynchronize; the host range minus GPU work is dispatch + sync latency that async launch would hide |
| react_moa_mcts | gpu_idle_window | 131,658.6 | 3,356.2 | 97.51 % | upper bound on wall reduction if all host work were overlapped or removed; single stream, no kernel concurrency observed |

## Tables (G09)

| table | rows | sha256 |
|---|---:|---|
| g06_selection_plan.csv | 51 | b47fb03758cda440… |
| g06_selected_stacks.csv | 20 | 4e975bd3f459518b… |
| g06_global_ranking.csv | 51 | c83881d263b71353… |
| g06_denominators.csv | 3 | fdf986716b928358… |
| g07_process_timeline_representative.csv | 417 | 2a5075d7c003b7f5… |
| g07_kernel_timeline_representative.csv | 400 | 40f45ad2680cb35a… |
| g07_launch_gaps.csv | 219 | f8bfff6496dd79d9… |
| g07_high_latency_instances.csv | 1121 | 2ad204bacb04768a… |
| g07_host_gpu_overlap.csv | 3 | bc5cd178e683f8da… |
| g08_resource_attachment.csv | 92 | dbcc619a2d75a037… |
| g08_opportunities.csv | 9 | b1950184405e712c… |

Visible-range statement (G10): View A stacks show 5 instances per selected type; View B shows every process type but numbers only where a w03 family row attached.
Full per-instance evidence remains in the w01/w02 tables referenced by the admission ledger.

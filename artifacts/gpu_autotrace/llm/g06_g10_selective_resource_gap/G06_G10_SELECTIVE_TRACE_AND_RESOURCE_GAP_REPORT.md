# G06-G10 selective process trace and resource gap: lineage `llm`

Lineage `h22-gpu-autotrace`, workflow w05. Admission ledger (sha256 of every upstream handoff) is in `tables_manifest.json`.
Two views follow. The first hides nothing below the 10 % threshold except in the stacks table; the second shows only instances with a
successfully attached hardware metric and says so.

## View A: high-latency process distribution (G06/G07)

### Selection (strictly > 10 % of total process host time)

| workload | process | instances | cumulative (us) | share | median (us) | p90 (us) | max (us) | MAD (us) | GPU-owning | selected |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| react_tool | mir_operator:decode_layer* | 9240 | 10,723,784.3 | 91.63 % | 1,170.2 | 1,226.8 | 6,252.9 | 49.3 | True | **yes** |
| react_tool | inter_operator_dispatch | 10410 | 442,627.7 | 3.78 % | 20.4 | 40.0 | 2,626.5 | 1.3 | True | no |
| react_tool | mir_operator:prefill_layer* | 168 | 211,765.4 | 1.81 % | 1,245.3 | 1,336.4 | 1,781.4 | 49.8 | True | no |
| react_tool | mir_operator:decode_sample | 330 | 205,980.0 | 1.76 % | 619.2 | 631.4 | 802.6 | 5.3 | True | no |
| react_tool | mir_operator:decode_head | 330 | 75,968.6 | 0.65 % | 229.4 | 248.6 | 360.1 | 11.9 | True | no |
| react_tool | mir_operator:decode_embed | 330 | 17,329.8 | 0.15 % | 52.0 | 61.1 | 92.9 | 5.5 | True | no |
| react_tool | token_preprocess_cpu | 6 | 6,188.6 | 0.05 % | 1,157.5 | 1,172.6 | 1,232.4 | 45.0 | False | no |
| react_tool | mir_operator:prefill_sample | 6 | 5,292.8 | 0.05 % | 876.9 | 992.8 | 1,000.2 | 103.9 | True | no |
| react_tool | pre_d2h_alloc | 6 | 4,315.9 | 0.04 % | 286.9 | 320.4 | 2,959.7 | 35.5 | True | no |
| react_tool | dag_schedule_gap | 9 | 2,614.6 | 0.02 % | 73.1 | 774.2 | 848.3 | 54.6 | False | no |
| react_tool | mir_operator:prefill_head | 6 | 1,487.9 | 0.01 % | 244.8 | 259.3 | 268.0 | 9.3 | True | no |
| react_tool | weight_init | 6 | 1,087.3 | 0.01 % | 177.4 | 194.5 | 230.9 | 15.8 | False | no |
| react_tool | agent_tool_execute_cpu | 3 | 824.4 | 0.01 % | 281.7 | 281.7 | 283.3 | 1.6 | False | no |
| react_tool | d2h_stage | 6 | 820.2 | 0.01 % | 137.9 | 140.0 | 146.1 | 5.1 | True | no |
| react_tool | h2d_stage | 6 | 742.4 | 0.01 % | 123.6 | 136.1 | 147.3 | 15.0 | True | no |
| react_tool | host_input_generate | 6 | 737.7 | 0.01 % | 124.3 | 135.3 | 135.4 | 11.0 | False | no |
| react_tool | mir_operator:prefill_embed | 6 | 597.9 | 0.01 % | 99.3 | 102.5 | 108.6 | 3.8 | True | no |
| react_tool | iteration_tail_sync | 3 | 346.7 | 0.0 % | 118.0 | 118.0 | 118.3 | 0.2 | False | no |
| react_tool | checksum_complete | 6 | 296.0 | 0.0 % | 49.2 | 50.7 | 51.8 | 1.2 | False | no |
| react_tool | adapter_dispatch | 6 | 24.8 | 0.0 % | 4.1 | 4.7 | 4.9 | 0.5 | False | no |
| planner_debate | mir_operator:decode_layer* | 36540 | 44,847,746.7 | 92.17 % | 1,217.9 | 1,303.8 | 6,411.0 | 47.0 | True | **yes** |
| planner_debate | inter_operator_dispatch | 40905 | 1,971,174.8 | 4.05 % | 21.6 | 44.7 | 7,407.8 | 1.8 | True | no |
| planner_debate | mir_operator:decode_sample | 1305 | 808,569.8 | 1.66 % | 615.9 | 627.9 | 811.5 | 6.3 | True | no |
| planner_debate | mir_operator:prefill_layer* | 420 | 543,554.3 | 1.12 % | 1,298.0 | 1,390.8 | 1,911.1 | 63.2 | True | no |
| planner_debate | mir_operator:decode_head | 1305 | 322,680.9 | 0.66 % | 244.1 | 270.4 | 426.9 | 14.9 | True | no |
| planner_debate | mir_operator:decode_embed | 1305 | 75,410.6 | 0.15 % | 58.3 | 66.8 | 115.8 | 5.9 | True | no |
| planner_debate | mir_operator:prefill_sample | 15 | 28,949.4 | 0.06 % | 1,765.8 | 2,686.4 | 2,733.2 | 182.3 | True | no |
| planner_debate | token_preprocess_cpu | 15 | 25,652.5 | 0.05 % | 1,610.2 | 2,443.5 | 2,745.5 | 246.0 | False | no |
| planner_debate | pre_d2h_alloc | 15 | 14,806.9 | 0.03 % | 310.2 | 563.8 | 5,327.1 | 72.2 | True | no |
| planner_debate | dag_schedule_gap | 18 | 4,001.5 | 0.01 % | 91.0 | 830.8 | 1,002.7 | 27.1 | False | no |
| planner_debate | mir_operator:prefill_head | 15 | 3,855.8 | 0.01 % | 260.0 | 279.0 | 300.4 | 19.9 | True | no |
| planner_debate | weight_init | 15 | 2,668.5 | 0.01 % | 173.9 | 206.1 | 243.8 | 21.2 | False | no |
| planner_debate | host_input_generate | 15 | 2,108.5 | 0.0 % | 134.2 | 179.5 | 191.3 | 14.3 | False | no |
| planner_debate | d2h_stage | 15 | 1,958.4 | 0.0 % | 130.7 | 143.6 | 148.4 | 6.8 | True | no |
| planner_debate | h2d_stage | 15 | 1,615.5 | 0.0 % | 105.0 | 128.4 | 132.9 | 12.1 | True | no |
| planner_debate | mir_operator:prefill_embed | 15 | 1,434.4 | 0.0 % | 96.2 | 106.9 | 116.8 | 9.3 | True | no |
| planner_debate | agent_tool_execute_cpu | 3 | 1,099.1 | 0.0 % | 374.3 | 374.3 | 426.0 | 51.7 | False | no |
| planner_debate | checksum_complete | 15 | 720.9 | 0.0 % | 48.2 | 52.0 | 56.7 | 3.3 | False | no |
| planner_debate | iteration_tail_sync | 3 | 532.6 | 0.0 % | 187.1 | 187.1 | 188.4 | 1.3 | False | no |
| planner_debate | adapter_dispatch | 15 | 70.7 | 0.0 % | 4.0 | 4.7 | 11.4 | 0.5 | False | no |
| react_moa_mcts | mir_operator:decode_layer* | 71400 | 81,598,616.7 | 92.16 % | 1,147.6 | 1,212.6 | 5,066.1 | 51.2 | True | **yes** |
| react_moa_mcts | inter_operator_dispatch | 79950 | 3,404,999.8 | 3.85 % | 20.9 | 39.7 | 3,455.8 | 1.4 | True | no |
| react_moa_mcts | mir_operator:decode_sample | 2550 | 1,594,831.6 | 1.8 % | 621.7 | 631.0 | 821.1 | 4.8 | True | no |
| react_moa_mcts | mir_operator:prefill_layer* | 840 | 1,054,123.6 | 1.19 % | 1,260.1 | 1,337.0 | 1,803.4 | 52.4 | True | no |
| react_moa_mcts | mir_operator:decode_head | 2550 | 575,941.4 | 0.65 % | 225.5 | 246.3 | 292.4 | 12.1 | True | no |
| react_moa_mcts | mir_operator:decode_embed | 2550 | 129,622.4 | 0.15 % | 50.0 | 60.2 | 77.0 | 5.5 | True | no |
| react_moa_mcts | mir_operator:prefill_sample | 30 | 65,350.7 | 0.07 % | 2,285.8 | 2,687.1 | 2,722.9 | 342.7 | True | no |
| react_moa_mcts | token_preprocess_cpu | 30 | 42,253.3 | 0.05 % | 1,486.3 | 1,683.8 | 2,215.1 | 152.0 | False | no |
| react_moa_mcts | pre_d2h_alloc | 30 | 41,910.8 | 0.05 % | 340.3 | 3,696.0 | 4,326.3 | 87.4 | True | no |
| react_moa_mcts | mir_operator:prefill_head | 30 | 7,370.2 | 0.01 % | 244.4 | 259.9 | 283.2 | 9.6 | True | no |
| react_moa_mcts | dag_schedule_gap | 33 | 6,431.5 | 0.01 % | 105.1 | 371.1 | 935.1 | 17.7 | False | no |
| react_moa_mcts | weight_init | 30 | 4,765.6 | 0.01 % | 160.0 | 183.5 | 200.8 | 16.9 | False | no |
| react_moa_mcts | d2h_stage | 30 | 3,867.5 | 0.0 % | 125.1 | 134.2 | 200.0 | 8.0 | True | no |
| react_moa_mcts | host_input_generate | 30 | 3,857.7 | 0.0 % | 126.8 | 143.0 | 158.4 | 10.2 | False | no |
| react_moa_mcts | h2d_stage | 30 | 3,161.7 | 0.0 % | 101.5 | 119.3 | 149.1 | 4.9 | True | no |
| react_moa_mcts | mir_operator:prefill_embed | 30 | 2,649.8 | 0.0 % | 89.1 | 98.1 | 102.4 | 7.3 | True | no |
| react_moa_mcts | checksum_complete | 30 | 1,416.9 | 0.0 % | 47.6 | 53.7 | 54.2 | 2.5 | False | no |
| react_moa_mcts | agent_tool_execute_cpu | 3 | 1,084.7 | 0.0 % | 314.8 | 314.8 | 483.5 | 28.4 | False | no |
| react_moa_mcts | iteration_tail_sync | 3 | 388.8 | 0.0 % | 130.3 | 130.3 | 139.1 | 8.8 | False | no |
| react_moa_mcts | adapter_dispatch | 30 | 167.1 | 0.0 % | 4.6 | 9.2 | 9.8 | 0.7 | False | no |

### Five longest instances per selected type (real start/end on the nsys clock)

| workload | process | rank | iter | call | start (ns) | host (us) | GPU (us) | top CUDA API |
|---|---|---:|---:|---|---:|---:|---:|---|
| react_tool | mir_operator:decode_layer* | 1 | 2 | plan | 24456543880 | 6,252.9 | 204.1 | cudaLaunchKernel |
| react_tool | mir_operator:decode_layer* | 2 | 1 | answer | 23325816798 | 5,794.6 | 204.4 | cudaLaunchKernel |
| react_tool | mir_operator:decode_layer* | 3 | 1 | answer | 21646998465 | 2,392.8 | 203.1 | cudaLaunchKernel |
| react_tool | mir_operator:decode_layer* | 4 | 1 | answer | 23439340841 | 2,219.1 | 202.5 | cudaLaunchKernel |
| react_tool | mir_operator:decode_layer* | 5 | 1 | answer | 22322933358 | 2,204.3 | 202.6 | cudaLaunchKernel |
| planner_debate | mir_operator:decode_layer* | 1 | 2 | critic-merge | 82619901669 | 6,411.0 | 220.5 | cudaLaunchKernel |
| planner_debate | mir_operator:decode_layer* | 2 | 1 | planner-seed | 58166043755 | 6,389.9 | 201.8 | cudaLaunchKernel |
| planner_debate | mir_operator:decode_layer* | 3 | 1 | critic-merge | 67681141325 | 5,086.0 | 207.6 | cudaLaunchKernel |
| planner_debate | mir_operator:decode_layer* | 4 | 0 | planner-seed | 42837511596 | 3,815.9 | 204.1 | cudaLaunchKernel |
| planner_debate | mir_operator:decode_layer* | 5 | 0 | critic-merge | 51427161682 | 3,696.5 | 206.9 | cudaLaunchKernel |
| react_moa_mcts | mir_operator:decode_layer* | 1 | 0 | moa-map2 | 79850255857 | 5,066.1 | 309.0 | cudaLaunchKernel |
| react_moa_mcts | mir_operator:decode_layer* | 2 | 1 | moa-map0 | 102999987534 | 5,054.8 | 204.5 | cudaLaunchKernel |
| react_moa_mcts | mir_operator:decode_layer* | 3 | 0 | mcts-actor0 | 86197175087 | 4,898.7 | 209.1 | cudaLaunchKernel |
| react_moa_mcts | mir_operator:decode_layer* | 4 | 2 | moa-map0 | 132589437515 | 4,874.9 | 205.5 | cudaLaunchKernel |
| react_moa_mcts | mir_operator:decode_layer* | 5 | 1 | mcts-critic | 126261820787 | 3,984.5 | 208.7 | cudaLaunchKernel |

### Host/GPU overlap and launch gaps, representative iteration (G07)

| workload | iter | wall (us) | GPU busy | host-only | streams | max concurrent GPU | gaps >= 20 us | gap total (us) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| react_tool | 2 | 3,917,913.0 | 18.77 % | 2.21 % | 1 | 1 | 34391 | 1,329,686.9 |
| planner_debate | 2 | 15,959,036.5 | 18.4 % | 2.42 % | 1 | 1 | 149585 | 5,789,475.4 |
| react_moa_mcts | 0 | 29,411,549.1 | 19.55 % | 2.24 % | 1 | 1 | 249809 | 9,618,344.9 |

Largest GPU launch gaps and the host processes covering them:

| workload | gap start (us) | gap (us) | next GPU item | host processes covering |
|---|---:|---:|---|---|
| react_tool | 8516547.4 | 5,021.5 | plan:mir_operator:decode_layer25:concat |  |
| planner_debate | 36904236.1 | 5,012.8 | critic-a:mir_operator:decode_layer09:copy |  |
| planner_debate | 39870683.2 | 4,850.8 | critic-b:mir_operator:decode_layer09:copy |  |
| planner_debate | 35020291.2 | 4,842.4 | planner-seed:mir_operator:decode_layer01:copy |  |
| planner_debate | 35937401.9 | 4,803.1 | critic-a:mir_operator:decode_layer03:copy |  |
| planner_debate | 38810334.4 | 4,792.4 | critic-b:mir_operator:decode_layer24:copy |  |
| planner_debate | 46428950.6 | 4,775.6 | planner-final:mir_operator:decode_layer15:copy |  |
| planner_debate | 40905029.2 | 4,771.5 | critic-b:mir_operator:decode_layer09:copy |  |
| planner_debate | 34130098.7 | 4,697.8 | planner-seed:mir_operator:decode_layer04:copy |  |
| planner_debate | 43786364.0 | 4,657.4 | critic-merge:mir_operator:decode_layer01:copy |  |
| planner_debate | 37939357.3 | 4,646.4 | critic-a:mir_operator:decode_layer09:copy |  |
| planner_debate | 41448707.9 | 4,580.3 | critic-merge:h2d_stage:memcpy |  |
| planner_debate | 47522556.6 | 4,532.6 | planner-final:mir_operator:decode_layer01:copy |  |
| planner_debate | 41685434.9 | 4,520.2 | critic-merge:mir_operator:decode_layer14:copy |  |
| planner_debate | 48546891.6 | 4,128.4 | planner-final:mir_operator:decode_layer01:copy |  |

### High-latency instances (median + 3 MAD per type): 31508 total

| workload | process | iter | call | host (us) | median (us) | excess (us) | class |
|---|---|---:|---|---:|---:|---:|---|
| planner_debate | inter_operator_dispatch | 0 | planner-seed | 7,407.8 | 21.6 | 7,386.2 | warm_or_first_iteration |
| planner_debate | inter_operator_dispatch | 0 | planner-seed | 5,388.8 | 21.6 | 5,367.2 | warm_or_first_iteration |
| planner_debate | mir_operator:decode_layer* | 2 | critic-merge | 6,411.0 | 1,217.9 | 5,193.1 | sporadic |
| planner_debate | mir_operator:decode_layer* | 1 | planner-seed | 6,389.9 | 1,217.9 | 5,171.9 | sporadic |
| react_tool | mir_operator:decode_layer* | 2 | plan | 6,252.9 | 1,170.2 | 5,082.6 | sporadic |
| planner_debate | pre_d2h_alloc | 0 | critic-b | 5,327.1 | 310.2 | 5,016.8 | warm_or_first_iteration |
| planner_debate | inter_operator_dispatch | 2 | critic-a | 4,895.0 | 21.6 | 4,873.3 | sporadic |
| planner_debate | inter_operator_dispatch | 1 | critic-a | 4,890.2 | 21.6 | 4,868.6 | sporadic |
| planner_debate | inter_operator_dispatch | 1 | planner-final | 4,883.6 | 21.6 | 4,862.0 | sporadic |
| planner_debate | inter_operator_dispatch | 2 | critic-b | 4,752.5 | 21.6 | 4,730.9 | sporadic |
| planner_debate | inter_operator_dispatch | 2 | critic-a | 4,743.6 | 21.6 | 4,722.0 | sporadic |
| planner_debate | inter_operator_dispatch | 2 | critic-b | 4,734.2 | 21.6 | 4,712.5 | sporadic |
| planner_debate | inter_operator_dispatch | 1 | critic-b | 4,732.8 | 21.6 | 4,711.2 | sporadic |
| planner_debate | pre_d2h_alloc | 0 | critic-merge | 5,017.3 | 310.2 | 4,707.0 | warm_or_first_iteration |
| planner_debate | inter_operator_dispatch | 2 | planner-final | 4,723.5 | 21.6 | 4,701.8 | sporadic |
| planner_debate | inter_operator_dispatch | 2 | planner-seed | 4,718.1 | 21.6 | 4,696.5 | sporadic |
| planner_debate | inter_operator_dispatch | 2 | planner-seed | 4,656.5 | 21.6 | 4,634.8 | sporadic |
| planner_debate | inter_operator_dispatch | 2 | critic-b | 4,652.9 | 21.6 | 4,631.3 | sporadic |
| react_tool | mir_operator:decode_layer* | 1 | answer | 5,794.6 | 1,170.2 | 4,624.4 | sporadic |
| planner_debate | inter_operator_dispatch | 1 | planner-final | 4,625.0 | 21.6 | 4,603.3 | sporadic |

## View B: resource window (G08)

Only rows with an attached hardware metric are shown with numbers; host-only processes are listed with their status so the coverage is explicit.

| workload | process | selected | share | status | family | SM % | Tensor % | DRAM active % | DRAM BW % peak | L2 % | occupancy % | waves/SM | interpretation |
|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| react_tool | dag_schedule_gap | False | 0.02 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | adapter_dispatch | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | token_preprocess_cpu | False | 0.05 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | host_input_generate | False | 0.01 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | h2d_stage | False | 0.01 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool | weight_init | False | 0.01 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | mir_operator:prefill_embed | False | 0.01 % | profiled | other | 2.9 | 0.0 | 11.53 | 0.0 | 17.07 | 23.79 | 0.27 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | inter_operator_dispatch | False | 3.78 % | not_collected |  |  |  |  |  |  |  |  | no w03 family row |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 3.99 | 0.0 | 28.07 | 0.0 | 18.88 | 22.25 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.43 | 0.0 | 15.47 | 0.0 | 11.39 | 9.6 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.09 | 0.0 | 35.9 | 0.0 | 14.16 | 49.29 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.15 | 0.0 | 24.34 | 0.0 | 14.46 | 42.9 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.07 | 36.93 | 49.5 | 0.0 | 67.39 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.09 | 0.0 | 40.48 | 0.0 | 16.05 | 22.77 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.11 | 0.0 | 10.91 | 0.0 | 7.18 | 73.94 | 1.33 | underutilised: SM 29 %, DRAM 18 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.69 | 8.1 | 32.37 | 0.0 | 18.71 | 25.28 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.11 | 0.0 | 27.12 | 0.0 | 18.98 | 22.1 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.47 | 0.0 | 14.55 | 0.0 | 11.24 | 9.35 | 0.06 | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.54 | 0.0 | 34.83 | 0.0 | 13.74 | 49.14 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.75 | 0.0 | 23.86 | 0.0 | 14.48 | 42.95 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.12 | 36.88 | 49.85 | 0.0 | 67.72 | 8.33 | 1.0 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 5.99 | 0.0 | 40.47 | 0.0 | 15.77 | 22.78 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.7 | 0.0 | 11.15 | 0.0 | 7.16 | 73.8 | 1.33 | underutilised: SM 31 %, DRAM 17 %, L2 11 %, occ 83 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.68 | 8.23 | 31.75 | 0.0 | 18.66 | 25.25 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.09 | 0.0 | 27.35 | 0.0 | 18.96 | 22.17 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.44 | 0.0 | 14.75 | 0.0 | 7.41 | 9.4 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.17 | 0.0 | 34.9 | 0.0 | 13.73 | 49.29 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.54 | 0.0 | 24.51 | 0.0 | 13.78 | 43.06 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.04 | 36.85 | 50.38 | 0.0 | 67.4 | 8.33 | 1.0 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.07 | 0.0 | 42.67 | 0.0 | 16.84 | 22.69 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.68 | 0.0 | 10.95 | 0.0 | 7.05 | 73.68 | 1.33 | underutilised: SM 30 %, DRAM 16 %, L2 10 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.71 | 8.13 | 32.43 | 0.0 | 18.98 | 25.14 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.1 | 0.0 | 27.11 | 0.0 | 18.7 | 22.24 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.44 | 0.0 | 14.84 | 0.0 | 7.4 | 9.48 | 0.06 | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.14 | 0.0 | 34.17 | 0.0 | 13.5 | 49.11 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.87 | 0.0 | 23.61 | 0.0 | 14.42 | 43.1 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.44 | 37.23 | 49.98 | 0.0 | 67.19 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.07 | 0.0 | 40.37 | 0.0 | 15.97 | 22.85 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.64 | 0.0 | 10.96 | 0.0 | 7.22 | 73.89 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.68 | 8.08 | 31.52 | 0.0 | 18.56 | 25.22 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.11 | 0.0 | 26.91 | 0.0 | 19.0 | 22.27 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.44 | 0.0 | 15.63 | 0.0 | 7.92 | 9.55 | 0.06 | underutilised: SM 1 %, DRAM 46 %, L2 22 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 7.08 | 0.0 | 34.35 | 0.0 | 13.55 | 49.0 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.67 | 0.0 | 23.12 | 0.0 | 14.58 | 43.54 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.5 | 36.99 | 49.77 | 0.0 | 66.8 | 8.33 | 1.0 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.2 | 0.0 | 40.8 | 0.0 | 16.02 | 22.68 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.49 | 0.0 | 10.91 | 0.0 | 7.18 | 73.58 | 1.33 | underutilised: SM 31 %, DRAM 17 %, L2 11 %, occ 85 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.75 | 8.22 | 31.86 | 0.0 | 18.68 | 25.41 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.1 | 0.0 | 28.07 | 0.0 | 18.92 | 22.1 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.44 | 0.0 | 14.63 | 0.0 | 7.49 | 9.59 | 0.06 | underutilised: SM 1 %, DRAM 43 %, L2 20 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 9.88 | 0.0 | 34.52 | 0.0 | 13.6 | 49.1 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.63 | 0.0 | 23.42 | 0.0 | 14.82 | 43.31 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.01 | 36.95 | 49.54 | 0.0 | 67.71 | 8.33 | 1.0 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 5.99 | 0.0 | 40.05 | 0.0 | 17.43 | 22.89 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.79 | 0.0 | 11.09 | 0.0 | 7.14 | 73.81 | 1.33 | underutilised: SM 30 %, DRAM 16 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.69 | 8.39 | 32.01 | 0.0 | 18.7 | 25.21 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.0 | 0.0 | 27.94 | 0.0 | 18.92 | 22.45 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.46 | 0.0 | 15.19 | 0.0 | 7.98 | 9.28 | 0.06 | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.5 | 0.0 | 34.77 | 0.0 | 13.71 | 49.14 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.52 | 0.0 | 23.68 | 0.0 | 14.32 | 43.02 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.61 | 36.85 | 50.19 | 0.0 | 67.52 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.14 | 0.0 | 41.12 | 0.0 | 16.23 | 22.83 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.06 | 0.0 | 10.96 | 0.0 | 7.16 | 65.19 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.69 | 8.35 | 31.94 | 0.0 | 18.89 | 25.16 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.08 | 0.0 | 27.0 | 0.0 | 19.46 | 22.47 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.44 | 0.0 | 15.59 | 0.0 | 7.45 | 9.48 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.0 | 0.0 | 37.0 | 0.0 | 13.81 | 48.93 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.69 | 0.0 | 24.06 | 0.0 | 14.83 | 43.28 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.41 | 37.14 | 50.21 | 0.0 | 67.92 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.25 | 0.0 | 41.85 | 0.0 | 16.36 | 22.83 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.49 | 0.0 | 10.97 | 0.0 | 7.15 | 73.99 | 1.33 | underutilised: SM 31 %, DRAM 17 %, L2 11 %, occ 85 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.64 | 8.26 | 31.75 | 0.0 | 18.64 | 25.4 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.07 | 0.0 | 27.0 | 0.0 | 18.99 | 21.97 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.46 | 0.0 | 15.84 | 0.0 | 7.95 | 9.41 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.43 | 0.0 | 35.26 | 0.0 | 13.86 | 49.17 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.95 | 0.0 | 23.83 | 0.0 | 14.77 | 43.27 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.02 | 37.0 | 49.74 | 0.0 | 67.24 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.07 | 0.0 | 41.05 | 0.0 | 16.25 | 22.83 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.64 | 0.0 | 10.87 | 0.0 | 7.19 | 73.42 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.76 | 8.14 | 32.15 | 0.0 | 18.47 | 24.98 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.07 | 0.0 | 27.06 | 0.0 | 18.8 | 22.24 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.43 | 0.0 | 15.81 | 0.0 | 7.76 | 9.35 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 9.94 | 0.0 | 34.89 | 0.0 | 13.73 | 49.3 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.85 | 0.0 | 24.68 | 0.0 | 14.4 | 43.07 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.6 | 37.31 | 50.06 | 0.0 | 67.98 | 8.33 | 1.0 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.23 | 0.0 | 40.32 | 0.0 | 15.98 | 22.93 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.36 | 0.0 | 11.24 | 0.0 | 7.15 | 74.69 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.77 | 8.1 | 31.7 | 0.0 | 19.06 | 25.28 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.01 | 0.0 | 27.15 | 0.0 | 18.89 | 22.26 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.46 | 0.0 | 15.46 | 0.0 | 7.86 | 9.37 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.15 | 0.0 | 35.9 | 0.0 | 14.15 | 49.29 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 9.05 | 0.0 | 23.58 | 0.0 | 14.33 | 43.14 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.31 | 36.9 | 49.84 | 0.0 | 66.87 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.11 | 0.0 | 41.15 | 0.0 | 16.19 | 22.52 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.5 | 0.0 | 10.91 | 0.0 | 7.1 | 73.52 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.82 | 8.34 | 31.75 | 0.0 | 18.62 | 25.38 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.09 | 0.0 | 27.58 | 0.0 | 18.66 | 22.24 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.45 | 0.0 | 14.43 | 0.0 | 7.4 | 9.57 | 0.06 | underutilised: SM 1 %, DRAM 47 %, L2 22 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.1 | 0.0 | 35.84 | 0.0 | 14.14 | 49.25 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.83 | 0.0 | 23.24 | 0.0 | 14.2 | 43.32 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.17 | 37.07 | 49.58 | 0.0 | 67.95 | 8.33 | 1.0 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.25 | 0.0 | 40.66 | 0.0 | 16.1 | 22.62 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.58 | 0.0 | 10.97 | 0.0 | 7.12 | 73.6 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.83 | 8.29 | 31.69 | 0.0 | 18.59 | 25.16 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.1 | 0.0 | 27.29 | 0.0 | 18.75 | 22.22 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.44 | 0.0 | 14.76 | 0.0 | 7.51 | 9.45 | 0.06 | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 9.99 | 0.0 | 35.84 | 0.0 | 14.11 | 49.25 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.82 | 0.0 | 23.62 | 0.0 | 14.43 | 42.91 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.82 | 36.94 | 49.58 | 0.0 | 67.07 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.19 | 0.0 | 40.48 | 0.0 | 15.94 | 22.52 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.2 | 0.0 | 10.88 | 0.0 | 7.24 | 73.51 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.79 | 8.22 | 32.02 | 0.0 | 18.58 | 24.96 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.12 | 0.0 | 27.44 | 0.0 | 18.85 | 22.24 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.48 | 0.0 | 15.93 | 0.0 | 8.26 | 9.58 | 0.06 | underutilised: SM 1 %, DRAM 46 %, L2 22 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.04 | 0.0 | 36.03 | 0.0 | 14.16 | 49.06 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 9.02 | 0.0 | 23.75 | 0.0 | 14.53 | 43.31 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.72 | 36.69 | 49.6 | 0.0 | 67.13 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.22 | 0.0 | 41.6 | 0.0 | 16.53 | 22.69 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.1 | 0.0 | 11.11 | 0.0 | 7.12 | 73.69 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.8 | 8.12 | 31.75 | 0.0 | 19.09 | 25.31 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.09 | 0.0 | 27.62 | 0.0 | 19.33 | 22.15 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.41 | 0.0 | 14.52 | 0.0 | 9.25 | 9.7 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.1 | 0.0 | 34.4 | 0.0 | 13.53 | 49.2 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 9.01 | 0.0 | 24.14 | 0.0 | 14.58 | 43.1 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.16 | 37.22 | 49.51 | 0.0 | 67.77 | 8.33 | 1.0 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 4.84 | 0.0 | 42.28 | 0.0 | 16.63 | 22.68 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.76 | 0.0 | 11.01 | 0.0 | 7.22 | 73.46 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 16.14 | 8.17 | 31.86 | 0.0 | 18.63 | 25.16 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.08 | 0.0 | 27.64 | 0.0 | 18.78 | 22.23 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.44 | 0.0 | 14.74 | 0.0 | 7.78 | 9.6 | 0.06 | underutilised: SM 1 %, DRAM 46 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.37 | 0.0 | 35.32 | 0.0 | 13.85 | 49.24 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.97 | 0.0 | 23.91 | 0.0 | 14.35 | 42.99 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.6 | 36.97 | 50.22 | 0.0 | 67.63 | 8.33 | 1.0 | underutilised: SM 28 %, DRAM 52 %, L2 57 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.27 | 0.0 | 41.53 | 0.0 | 16.41 | 22.69 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.77 | 0.0 | 11.2 | 0.0 | 7.1 | 73.98 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.85 | 8.19 | 32.4 | 0.0 | 18.73 | 25.32 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.04 | 0.0 | 26.98 | 0.0 | 18.88 | 22.21 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.47 | 0.0 | 14.84 | 0.0 | 7.46 | 9.45 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.13 | 0.0 | 34.52 | 0.0 | 13.62 | 49.07 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.8 | 0.0 | 23.75 | 0.0 | 14.29 | 43.31 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.95 | 37.06 | 49.47 | 0.0 | 67.2 | 8.33 | 1.0 | underutilised: SM 28 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.04 | 0.0 | 42.05 | 0.0 | 16.63 | 22.94 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.39 | 0.0 | 10.91 | 0.0 | 7.13 | 74.35 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 10 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.78 | 8.23 | 31.76 | 0.0 | 19.2 | 25.4 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.08 | 0.0 | 26.81 | 0.0 | 19.0 | 22.12 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.46 | 0.0 | 15.17 | 0.0 | 12.1 | 9.36 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.11 | 0.0 | 35.71 | 0.0 | 14.06 | 48.84 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.77 | 0.0 | 24.06 | 0.0 | 14.14 | 43.46 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.63 | 37.16 | 49.98 | 0.0 | 67.61 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.22 | 0.0 | 42.41 | 0.0 | 16.75 | 22.78 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.53 | 0.0 | 10.87 | 0.0 | 7.05 | 72.96 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.66 | 8.17 | 31.77 | 0.0 | 18.68 | 25.18 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.08 | 0.0 | 26.92 | 0.0 | 19.06 | 22.09 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.27 | 0.0 | 15.55 | 0.0 | 8.02 | 9.52 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 9.96 | 0.0 | 34.95 | 0.0 | 13.76 | 49.41 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.97 | 0.0 | 23.79 | 0.0 | 14.23 | 43.01 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.34 | 37.05 | 49.63 | 0.0 | 67.17 | 8.33 | 1.0 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.0 | 0.0 | 40.65 | 0.0 | 16.33 | 22.65 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.65 | 0.0 | 10.9 | 0.0 | 7.04 | 73.23 | 1.33 | underutilised: SM 30 %, DRAM 18 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.76 | 8.29 | 31.51 | 0.0 | 18.72 | 25.19 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.09 | 0.0 | 27.15 | 0.0 | 19.06 | 22.26 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.47 | 0.0 | 15.51 | 0.0 | 7.96 | 9.33 | 0.06 | underutilised: SM 1 %, DRAM 46 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.26 | 0.0 | 34.59 | 0.0 | 13.57 | 49.19 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.87 | 0.0 | 24.03 | 0.0 | 14.46 | 42.67 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.98 | 37.17 | 50.09 | 0.0 | 67.39 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.25 | 0.0 | 41.78 | 0.0 | 16.56 | 22.32 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.73 | 0.0 | 10.92 | 0.0 | 7.08 | 72.98 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.72 | 8.22 | 31.82 | 0.0 | 18.84 | 25.01 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.05 | 0.0 | 27.09 | 0.0 | 18.94 | 22.1 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.46 | 0.0 | 14.47 | 0.0 | 7.59 | 9.24 | 0.06 | underutilised: SM 1 %, DRAM 46 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.17 | 0.0 | 35.9 | 0.0 | 14.12 | 49.19 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.77 | 0.0 | 24.66 | 0.0 | 14.58 | 42.85 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.25 | 36.94 | 49.25 | 0.0 | 67.07 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.06 | 0.0 | 40.91 | 0.0 | 15.99 | 22.56 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.78 | 0.0 | 10.75 | 0.0 | 6.96 | 73.87 | 1.33 | underutilised: SM 30 %, DRAM 16 %, L2 10 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.67 | 8.2 | 31.8 | 0.0 | 18.78 | 25.03 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.07 | 0.0 | 26.86 | 0.0 | 18.88 | 22.31 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.45 | 0.0 | 14.63 | 0.0 | 7.4 | 9.57 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.11 | 0.0 | 33.99 | 0.0 | 13.36 | 49.08 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.81 | 0.0 | 23.16 | 0.0 | 14.34 | 43.4 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.95 | 36.98 | 49.33 | 0.0 | 67.42 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.24 | 0.0 | 41.36 | 0.0 | 16.32 | 22.72 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.63 | 0.0 | 10.87 | 0.0 | 7.09 | 73.25 | 1.33 | underutilised: SM 29 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.7 | 8.19 | 31.91 | 0.0 | 18.74 | 25.23 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.07 | 0.0 | 26.76 | 0.0 | 19.12 | 22.01 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.45 | 0.0 | 15.45 | 0.0 | 7.89 | 9.48 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.34 | 0.0 | 35.39 | 0.0 | 13.86 | 49.22 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.86 | 0.0 | 24.43 | 0.0 | 14.48 | 43.1 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.01 | 37.11 | 49.62 | 0.0 | 66.96 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.05 | 0.0 | 40.07 | 0.0 | 15.84 | 22.57 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.48 | 0.0 | 10.74 | 0.0 | 7.03 | 73.21 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.88 | 8.2 | 31.62 | 0.0 | 18.79 | 25.29 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.09 | 0.0 | 26.57 | 0.0 | 18.85 | 22.18 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.44 | 0.0 | 14.8 | 0.0 | 7.57 | 9.47 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.02 | 0.0 | 34.52 | 0.0 | 13.58 | 49.14 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.87 | 0.0 | 23.75 | 0.0 | 14.65 | 43.37 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.26 | 37.29 | 49.69 | 0.0 | 67.26 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 57 %, occ 8 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.21 | 0.0 | 40.4 | 0.0 | 16.61 | 22.68 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.72 | 0.0 | 10.92 | 0.0 | 7.12 | 73.99 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 85 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.99 | 8.17 | 31.85 | 0.0 | 18.64 | 25.25 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 1.96 | 0.0 | 26.75 | 0.0 | 19.11 | 22.15 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.45 | 0.0 | 15.51 | 0.0 | 7.87 | 9.43 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 19 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.51 | 0.0 | 34.89 | 0.0 | 13.7 | 48.99 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.9 | 0.0 | 23.9 | 0.0 | 14.42 | 43.56 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.95 | 37.31 | 49.68 | 0.0 | 66.69 | 8.33 | 1.0 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.08 | 0.0 | 39.77 | 0.0 | 15.73 | 22.83 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.52 | 0.0 | 10.78 | 0.0 | 7.12 | 73.34 | 1.33 | underutilised: SM 30 %, DRAM 16 %, L2 10 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.65 | 8.21 | 31.6 | 0.0 | 18.88 | 25.12 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.11 | 0.0 | 27.68 | 0.0 | 18.69 | 22.31 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.43 | 0.0 | 14.84 | 0.0 | 7.64 | 9.39 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.25 | 0.0 | 34.71 | 0.0 | 13.69 | 49.05 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.92 | 0.0 | 23.61 | 0.0 | 14.64 | 43.01 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 33.41 | 37.16 | 49.94 | 0.0 | 67.76 | 8.33 | 1.0 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.09 | 0.0 | 41.99 | 0.0 | 16.45 | 22.83 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.39 | 0.0 | 10.64 | 0.0 | 6.86 | 73.95 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.71 | 8.16 | 31.77 | 0.0 | 18.65 | 25.27 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.08 | 0.0 | 26.76 | 0.0 | 19.28 | 22.23 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.44 | 0.0 | 15.88 | 0.0 | 7.97 | 9.4 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.13 | 0.0 | 35.9 | 0.0 | 14.1 | 48.96 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.13 | 0.0 | 23.86 | 0.0 | 14.92 | 43.26 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.88 | 36.93 | 48.17 | 0.0 | 62.28 | 8.33 | 1.0 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.23 | 0.0 | 41.01 | 0.0 | 16.07 | 22.64 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.69 | 0.0 | 10.97 | 0.0 | 7.23 | 73.66 | 1.33 | underutilised: SM 30 %, DRAM 18 %, L2 10 %, occ 83 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.83 | 8.21 | 31.87 | 0.0 | 18.78 | 25.14 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | copy | 4.11 | 0.0 | 27.03 | 0.0 | 18.93 | 22.18 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_unary | 0.47 | 0.0 | 15.86 | 0.0 | 7.97 | 9.4 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | reduce | 10.05 | 0.0 | 35.9 | 0.0 | 14.12 | 49.21 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_binary | 8.81 | 0.0 | 23.62 | 0.0 | 14.45 | 42.76 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | gemm | 32.88 | 36.83 | 48.03 | 0.0 | 62.61 | 8.33 | 1.0 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | elementwise_other | 6.16 | 0.0 | 41.16 | 0.0 | 16.28 | 22.59 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | concat | 21.39 | 0.0 | 10.8 | 0.0 | 6.95 | 73.07 | 1.33 | underutilised: SM 30 %, DRAM 18 %, L2 11 %, occ 84 % |
| react_tool | mir_operator:prefill_layer* | False | 1.81 % | profiled | attention | 15.74 | 8.18 | 31.93 | 0.0 | 18.51 | 25.12 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_head | False | 0.01 % | profiled | copy | 7.07 | 0.0 | 34.72 | 0.0 | 19.69 | 32.78 | 0.4 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_head | False | 0.01 % | profiled | elementwise_unary | 0.69 | 0.0 | 22.18 | 0.0 | 10.97 | 13.11 | 0.12 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | mir_operator:prefill_head | False | 0.01 % | profiled | reduce | 0.74 | 0.0 | 23.85 | 0.0 | 9.36 | 33.27 | 0.04 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_head | False | 0.01 % | profiled | elementwise_binary | 11.09 | 0.0 | 23.62 | 0.0 | 15.49 | 45.6 | 0.54 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:prefill_head | False | 0.01 % | profiled | gemm | 45.91 | 46.6 | 77.28 | 0.0 | 69.03 | 16.29 | 12.76 | tensor-core compute-bound |
| react_tool | mir_operator:prefill_sample | False | 0.05 % | profiled | reduce | 2.78 | 0.0 | 5.27 | 0.0 | 2.99 | 33.13 | 0.05 | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_embed | False | 0.15 % | profiled | other | 0.25 | 0.0 | 0.34 | 0.0 | 0.7 | 8.31 | 0.01 | latency/launch-bound: 0.01 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.8 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.94 | 7.71 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.94 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.49 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.38 | 0.0 | 74.09 | 0.0 | 46.6 | 15.95 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.78 | 0.0 | 1.27 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.17 | 0.0 | 6.91 | 0.0 | 3.7 | 46.83 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.38 | 12.35 | 6.18 | 0.0 | 3.05 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 2.2 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 1.0 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.93 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.45 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.45 | 0.0 | 74.9 | 0.0 | 46.68 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.2 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.18 | 0.0 | 7.1 | 0.0 | 3.88 | 46.84 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.4 | 12.22 | 6.09 | 0.0 | 3.0 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.77 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.96 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.9 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.49 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.41 | 0.0 | 74.33 | 0.0 | 46.67 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.16 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.11 | 0.0 | 7.15 | 0.0 | 3.88 | 46.82 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.39 | 12.29 | 6.16 | 0.0 | 3.03 | 8.29 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.6 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.98 | 7.37 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.95 | 0.0 | 3.93 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.43 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.5 | 0.0 | 75.31 | 0.0 | 47.3 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.21 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.19 | 0.0 | 7.47 | 0.0 | 4.05 | 46.83 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.39 | 12.37 | 6.14 | 0.0 | 3.04 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 1.01 | 0.0 | 1.63 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 7.32 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.08 | 0.0 | 1.99 | 0.0 | 3.86 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.41 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.53 | 0.0 | 74.41 | 0.0 | 45.92 | 15.94 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.3 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.13 | 0.0 | 6.91 | 0.0 | 3.75 | 47.02 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.39 | 12.15 | 6.16 | 0.0 | 3.0 | 8.29 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.87 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.93 | 7.62 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.08 | 0.0 | 2.0 | 0.0 | 3.87 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.45 | 0.0 | 75.12 | 0.0 | 46.64 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.31 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 3.44 | 0.0 | 7.22 | 0.0 | 4.1 | 46.89 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.38 | 12.19 | 6.12 | 0.0 | 3.02 | 8.31 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 1.0 | 0.0 | 1.82 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.95 | 7.51 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.92 | 31.88 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.62 | 0.0 | 75.76 | 0.0 | 47.35 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.15 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.05 | 0.0 | 7.14 | 0.0 | 3.88 | 46.75 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.38 | 12.35 | 6.15 | 0.0 | 3.02 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 0.87 | 0.0 | 1.57 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.9 | 7.37 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.95 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.51 | 0.0 | 74.85 | 0.0 | 46.99 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.16 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.16 | 0.0 | 7.2 | 0.0 | 3.89 | 46.84 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.39 | 12.39 | 6.11 | 0.0 | 3.24 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.41 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 7.51 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.88 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.81 | 0.0 | 1.43 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.43 | 0.0 | 74.47 | 0.0 | 47.23 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.09 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.11 | 0.0 | 7.06 | 0.0 | 3.85 | 46.73 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.39 | 12.2 | 6.17 | 0.0 | 3.04 | 8.31 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 0.9 | 0.0 | 1.64 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.91 | 7.35 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.92 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.38 | 8.32 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.48 | 0.0 | 75.32 | 0.0 | 47.33 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.13 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.21 | 0.0 | 7.15 | 0.0 | 3.87 | 46.92 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.41 | 12.41 | 6.17 | 0.0 | 3.01 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 1.01 | 0.0 | 1.61 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 7.52 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.94 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.51 | 0.0 | 75.4 | 0.0 | 46.45 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.21 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.09 | 0.0 | 6.91 | 0.0 | 3.76 | 46.59 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.4 | 12.33 | 6.12 | 0.0 | 3.02 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.6 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.88 | 7.64 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.9 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.23 | 0.0 | 74.77 | 0.0 | 46.82 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.17 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.12 | 0.0 | 7.43 | 0.0 | 4.0 | 46.85 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.4 | 12.29 | 6.11 | 0.0 | 3.02 | 8.28 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.84 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 7.39 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.86 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.39 | 0.0 | 74.58 | 0.0 | 46.54 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.41 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.19 | 0.0 | 8.73 | 0.0 | 4.23 | 46.98 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.38 | 12.2 | 6.13 | 0.0 | 3.03 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 0.88 | 0.0 | 1.58 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 7.6 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.9 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.49 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.57 | 0.0 | 74.74 | 0.0 | 46.91 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.14 | 8.25 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.17 | 0.0 | 5.41 | 0.0 | 2.99 | 46.67 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.4 | 12.38 | 6.17 | 0.0 | 3.26 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 0.8 | 0.0 | 1.67 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.01 | 0.0 | 0.42 | 0.0 | 0.91 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.86 | 31.9 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.43 | 0.0 | 75.29 | 0.0 | 47.14 | 15.94 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.72 | 0.0 | 1.13 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.14 | 0.0 | 7.18 | 0.0 | 3.92 | 46.81 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 0.48 | 12.36 | 6.13 | 0.0 | 3.02 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 1.02 | 0.0 | 1.75 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.91 | 7.62 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.91 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.41 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.35 | 0.0 | 75.21 | 0.0 | 47.09 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.2 | 8.25 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.16 | 0.0 | 7.1 | 0.0 | 4.41 | 47.05 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.4 | 12.34 | 6.14 | 0.0 | 3.03 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 0.87 | 0.0 | 1.73 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.91 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.89 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.43 | 0.0 | 75.15 | 0.0 | 46.8 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.19 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.06 | 0.0 | 7.04 | 0.0 | 3.77 | 46.86 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.41 | 12.35 | 6.13 | 0.0 | 2.99 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.53 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.59 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.08 | 0.0 | 1.99 | 0.0 | 3.94 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.56 | 0.0 | 75.09 | 0.0 | 46.54 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.14 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.19 | 0.0 | 7.23 | 0.0 | 3.91 | 46.93 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.4 | 12.3 | 6.17 | 0.0 | 3.04 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 0.87 | 0.0 | 1.62 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.91 | 7.62 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.08 | 0.0 | 1.99 | 0.0 | 3.88 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.56 | 0.0 | 75.26 | 0.0 | 47.33 | 16.04 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.38 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.13 | 0.0 | 6.97 | 0.0 | 3.77 | 46.83 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.39 | 12.33 | 6.14 | 0.0 | 3.04 | 8.29 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.64 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.96 | 7.67 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.92 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.39 | 0.0 | 75.29 | 0.0 | 47.07 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.76 | 0.0 | 1.15 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.09 | 0.0 | 6.99 | 0.0 | 3.77 | 46.82 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.39 | 12.21 | 6.09 | 0.0 | 3.0 | 8.31 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 0.88 | 0.0 | 1.84 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.96 | 0.0 | 3.92 | 31.87 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.48 | 0.0 | 75.43 | 0.0 | 47.01 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.17 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.19 | 0.0 | 7.41 | 0.0 | 4.03 | 46.84 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.41 | 12.3 | 6.15 | 0.0 | 3.25 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 0.87 | 0.0 | 1.57 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.91 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.9 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.45 | 0.0 | 74.63 | 0.0 | 47.01 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.09 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.18 | 0.0 | 7.06 | 0.0 | 4.09 | 47.13 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.4 | 12.28 | 6.12 | 0.0 | 2.99 | 8.31 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 2.25 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.94 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.08 | 0.0 | 1.99 | 0.0 | 3.92 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.44 | 0.0 | 75.29 | 0.0 | 46.43 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.34 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.1 | 0.0 | 7.13 | 0.0 | 3.88 | 46.86 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.36 | 12.31 | 6.11 | 0.0 | 3.02 | 8.31 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 0.9 | 0.0 | 1.63 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.96 | 7.57 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.96 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.51 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.44 | 0.0 | 75.56 | 0.0 | 47.64 | 16.03 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.18 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.06 | 0.0 | 7.1 | 0.0 | 4.1 | 46.58 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.39 | 12.33 | 6.16 | 0.0 | 3.04 | 8.29 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.64 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.95 | 7.33 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.95 | 31.92 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.81 | 0.0 | 1.47 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.5 | 0.0 | 74.96 | 0.0 | 46.97 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.2 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.18 | 0.0 | 2.65 | 0.0 | 1.64 | 46.88 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.39 | 12.38 | 6.08 | 0.0 | 3.0 | 8.29 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 0.77 | 0.0 | 1.14 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.95 | 7.65 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.91 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.39 | 0.0 | 74.12 | 0.0 | 46.16 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.17 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.14 | 0.0 | 7.14 | 0.0 | 3.85 | 46.55 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.37 | 12.41 | 6.19 | 0.0 | 3.05 | 8.29 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.63 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.91 | 7.62 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.94 | 31.91 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.42 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.57 | 0.0 | 74.36 | 0.0 | 46.34 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.31 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.11 | 0.0 | 7.22 | 0.0 | 3.92 | 46.93 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.41 | 12.16 | 6.12 | 0.0 | 2.99 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.89 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.93 | 7.59 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | reduce | 0.09 | 0.0 | 1.95 | 0.0 | 3.92 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.49 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | gemv | 15.5 | 0.0 | 74.74 | 0.0 | 46.78 | 15.94 | 0.67 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | elementwise_other | 0.02 | 0.0 | 0.83 | 0.0 | 1.3 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | concat | 4.16 | 0.0 | 7.06 | 0.0 | 3.83 | 46.68 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_tool | mir_operator:decode_layer* | True | 91.63 % | profiled | attention | 1.37 | 12.33 | 6.15 | 0.0 | 3.03 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_head | False | 0.65 % | profiled | copy | 0.04 | 0.0 | 0.92 | 0.0 | 1.6 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_head | False | 0.65 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.54 | 0.0 | 0.94 | 7.62 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_head | False | 0.65 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.88 | 31.9 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_head | False | 0.65 % | profiled | elementwise_binary | 0.02 | 0.0 | 0.83 | 0.0 | 1.29 | 8.19 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | mir_operator:decode_head | False | 0.65 % | profiled | gemv | 19.59 | 0.0 | 96.88 | 0.0 | 60.77 | 24.5 | 49.46 | DRAM-bandwidth-bound |
| react_tool | mir_operator:decode_sample | False | 1.76 % | profiled | reduce | 2.78 | 0.0 | 5.28 | 0.0 | 3.31 | 33.13 | 0.05 | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| react_tool | pre_d2h_alloc | False | 0.04 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool | d2h_stage | False | 0.01 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool | checksum_complete | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | agent_tool_execute_cpu | False | 0.01 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool | iteration_tail_sync | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | dag_schedule_gap | False | 0.01 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | adapter_dispatch | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | token_preprocess_cpu | False | 0.05 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | host_input_generate | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | h2d_stage | False | 0.0 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate | weight_init | False | 0.01 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | mir_operator:prefill_embed | False | 0.0 % | profiled | other | 5.81 | 0.0 | 9.84 | 0.0 | 32.09 | 49.89 | 0.67 | underutilised: SM 6 %, DRAM 10 %, L2 32 %, occ 50 % |
| planner_debate | mir_operator:prefill_embed | False | 0.0 % | profiled | other | 4.47 | 0.0 | 11.02 | 0.0 | 25.61 | 37.22 | 0.46 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | inter_operator_dispatch | False | 4.05 % | not_collected |  |  |  |  |  |  |  |  | no w03 family row |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.29 | 0.0 | 44.95 | 0.0 | 27.91 | 50.6 | 0.83 | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.77 | 0.0 | 25.21 | 0.0 | 11.96 | 14.67 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.41 | 0.0 | 49.85 | 0.0 | 19.26 | 44.82 | 0.34 | underutilised: SM 2 %, DRAM 49 %, L2 18 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.47 | 0.0 | 38.7 | 0.0 | 22.86 | 65.68 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.04 | 41.73 | 31.53 | 0.0 | 66.48 | 13.94 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.61 | 0.0 | 59.19 | 0.0 | 23.36 | 51.19 | 0.67 | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 53 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.39 | 0.0 | 20.27 | 0.0 | 12.42 | 69.86 | 1.33 | underutilised: SM 39 %, DRAM 26 %, L2 16 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.4 | 12.17 | 31.69 | 0.0 | 26.49 | 33.78 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 4.1 | 0.0 | 45.23 | 0.0 | 27.56 | 50.54 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 32 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.79 | 0.0 | 24.93 | 0.0 | 16.71 | 14.54 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.54 | 0.0 | 50.99 | 0.0 | 20.02 | 44.36 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.6 | 0.0 | 38.87 | 0.0 | 22.85 | 65.44 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.1 | 41.44 | 30.73 | 0.0 | 67.3 | 13.76 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.48 | 0.0 | 59.47 | 0.0 | 23.53 | 51.28 | 0.67 | underutilised: SM 13 %, DRAM 31 %, L2 18 %, occ 56 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 27.6 | 0.0 | 19.89 | 0.0 | 12.32 | 70.12 | 1.33 | underutilised: SM 37 %, DRAM 28 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.46 | 12.01 | 41.38 | 0.0 | 28.19 | 33.7 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.38 | 0.0 | 45.18 | 0.0 | 28.56 | 50.41 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 32 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.77 | 0.0 | 26.18 | 0.0 | 12.49 | 14.51 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.55 | 0.0 | 51.63 | 0.0 | 20.3 | 44.6 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.42 | 0.0 | 39.31 | 0.0 | 22.65 | 65.24 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 38.34 | 41.5 | 31.07 | 0.0 | 67.21 | 13.93 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.6 | 0.0 | 60.73 | 0.0 | 24.1 | 51.07 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.6 | 0.0 | 20.01 | 0.0 | 12.33 | 70.07 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.36 | 12.16 | 41.06 | 0.0 | 27.97 | 33.67 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.42 | 0.0 | 46.13 | 0.0 | 28.04 | 50.53 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.36 | 0.0 | 25.01 | 0.0 | 11.91 | 14.6 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.6 | 0.0 | 51.21 | 0.0 | 20.13 | 44.73 | 0.34 | underutilised: SM 2 %, DRAM 52 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.75 | 0.0 | 38.9 | 0.0 | 23.03 | 65.41 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.19 | 41.7 | 30.85 | 0.0 | 67.16 | 13.83 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.3 | 0.0 | 61.34 | 0.0 | 24.22 | 50.97 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 27.96 | 0.0 | 20.04 | 0.0 | 12.31 | 69.79 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 19 %, occ 75 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.43 | 12.08 | 41.76 | 0.0 | 27.95 | 34.08 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.42 | 0.0 | 45.49 | 0.0 | 28.52 | 50.26 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 32 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.75 | 0.0 | 25.29 | 0.0 | 12.02 | 14.47 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.68 | 0.0 | 50.7 | 0.0 | 19.92 | 44.55 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.18 | 0.0 | 39.07 | 0.0 | 22.96 | 66.12 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.1 | 41.46 | 30.92 | 0.0 | 67.23 | 13.72 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.54 | 0.0 | 58.32 | 0.0 | 23.17 | 51.18 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 56 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.31 | 0.0 | 20.01 | 0.0 | 12.28 | 70.19 | 1.33 | underutilised: SM 40 %, DRAM 28 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.33 | 12.16 | 45.09 | 0.0 | 27.96 | 34.02 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.32 | 0.0 | 45.78 | 0.0 | 28.27 | 50.7 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 65 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.79 | 0.0 | 24.96 | 0.0 | 11.95 | 14.63 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.73 | 0.0 | 50.14 | 0.0 | 19.73 | 44.53 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.56 | 0.0 | 38.73 | 0.0 | 22.47 | 65.77 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.32 | 41.5 | 31.12 | 0.0 | 67.13 | 13.72 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.44 | 0.0 | 60.66 | 0.0 | 23.96 | 50.11 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.38 | 0.0 | 20.19 | 0.0 | 12.29 | 70.09 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.47 | 11.98 | 41.86 | 0.0 | 27.97 | 33.78 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.34 | 0.0 | 44.94 | 0.0 | 28.35 | 50.48 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.76 | 0.0 | 25.45 | 0.0 | 17.94 | 14.36 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.66 | 0.0 | 52.42 | 0.0 | 20.65 | 44.6 | 0.34 | underutilised: SM 2 %, DRAM 52 %, L2 21 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.8 | 0.0 | 39.14 | 0.0 | 22.77 | 65.68 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.19 | 41.77 | 31.4 | 0.0 | 67.1 | 13.84 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.58 | 0.0 | 59.54 | 0.0 | 23.48 | 50.52 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 27.96 | 0.0 | 19.39 | 0.0 | 11.91 | 70.19 | 1.33 | underutilised: SM 38 %, DRAM 28 %, L2 17 %, occ 77 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.49 | 12.27 | 41.48 | 0.0 | 28.01 | 33.79 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.48 | 0.0 | 46.61 | 0.0 | 28.38 | 50.62 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.76 | 0.0 | 25.2 | 0.0 | 11.84 | 14.41 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.52 | 0.0 | 52.24 | 0.0 | 20.53 | 44.59 | 0.34 | underutilised: SM 2 %, DRAM 52 %, L2 21 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.75 | 0.0 | 38.48 | 0.0 | 22.81 | 65.72 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 38.24 | 41.38 | 30.81 | 0.0 | 66.82 | 13.82 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.4 | 0.0 | 59.61 | 0.0 | 23.58 | 50.64 | 0.67 | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 52 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.23 | 0.0 | 19.74 | 0.0 | 12.02 | 70.08 | 1.33 | underutilised: SM 38 %, DRAM 28 %, L2 17 %, occ 77 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.39 | 12.13 | 41.6 | 0.0 | 27.9 | 33.79 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.38 | 0.0 | 44.67 | 0.0 | 28.47 | 50.68 | 0.83 | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 65 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.79 | 0.0 | 25.92 | 0.0 | 12.37 | 14.37 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 3.34 | 0.0 | 51.59 | 0.0 | 20.27 | 44.54 | 0.34 | underutilised: SM 2 %, DRAM 52 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.66 | 0.0 | 38.61 | 0.0 | 22.47 | 65.87 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 38.69 | 41.83 | 31.04 | 0.0 | 67.16 | 13.74 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.69 | 0.0 | 61.02 | 0.0 | 24.12 | 51.07 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 53 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.64 | 0.0 | 19.82 | 0.0 | 12.32 | 70.03 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.42 | 12.16 | 45.02 | 0.0 | 28.13 | 33.91 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.26 | 0.0 | 41.08 | 0.0 | 27.77 | 50.2 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.75 | 0.0 | 26.22 | 0.0 | 20.21 | 14.44 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.5 | 0.0 | 50.24 | 0.0 | 19.73 | 44.74 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.73 | 0.0 | 38.53 | 0.0 | 22.7 | 65.13 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 38.04 | 41.8 | 30.87 | 0.0 | 67.05 | 13.75 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 12.38 | 0.0 | 60.02 | 0.0 | 23.84 | 50.67 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 56 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.02 | 0.0 | 20.22 | 0.0 | 12.38 | 70.16 | 1.33 | underutilised: SM 39 %, DRAM 27 %, L2 16 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.34 | 12.05 | 41.23 | 0.0 | 27.76 | 33.74 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.46 | 0.0 | 45.0 | 0.0 | 28.46 | 50.38 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.79 | 0.0 | 25.27 | 0.0 | 11.98 | 14.47 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.49 | 0.0 | 51.85 | 0.0 | 20.36 | 44.46 | 0.34 | underutilised: SM 2 %, DRAM 52 %, L2 21 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.71 | 0.0 | 38.99 | 0.0 | 22.78 | 65.43 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.22 | 41.18 | 30.66 | 0.0 | 66.97 | 13.89 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 8.96 | 0.0 | 60.74 | 0.0 | 24.02 | 51.72 | 0.67 | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 55 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.63 | 0.0 | 20.17 | 0.0 | 12.28 | 70.1 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.37 | 12.3 | 46.19 | 0.0 | 28.14 | 33.71 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.44 | 0.0 | 45.64 | 0.0 | 28.4 | 50.76 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 32 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.74 | 0.0 | 25.26 | 0.0 | 12.27 | 14.6 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.76 | 0.0 | 49.1 | 0.0 | 19.26 | 44.38 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.41 | 0.0 | 38.77 | 0.0 | 22.9 | 65.87 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.25 | 41.48 | 31.24 | 0.0 | 66.8 | 13.76 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.9 | 0.0 | 58.99 | 0.0 | 23.2 | 50.35 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 55 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.3 | 0.0 | 20.44 | 0.0 | 12.32 | 69.98 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.33 | 12.15 | 46.74 | 0.0 | 27.72 | 33.87 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.04 | 0.0 | 44.92 | 0.0 | 28.04 | 50.56 | 0.83 | underutilised: SM 19 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.75 | 0.0 | 8.61 | 0.0 | 3.73 | 14.41 | 0.15 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.47 | 0.0 | 52.22 | 0.0 | 20.53 | 44.63 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.67 | 0.0 | 38.98 | 0.0 | 22.5 | 65.5 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.09 | 41.69 | 30.99 | 0.0 | 67.21 | 13.93 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.46 | 0.0 | 60.31 | 0.0 | 23.79 | 50.7 | 0.67 | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 56 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.29 | 0.0 | 19.61 | 0.0 | 12.04 | 70.02 | 1.33 | underutilised: SM 40 %, DRAM 29 %, L2 18 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.29 | 12.2 | 42.16 | 0.0 | 27.92 | 33.71 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.42 | 0.0 | 46.72 | 0.0 | 28.22 | 50.62 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.75 | 0.0 | 25.13 | 0.0 | 11.95 | 14.67 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.63 | 0.0 | 50.97 | 0.0 | 20.04 | 44.61 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.73 | 0.0 | 39.59 | 0.0 | 22.46 | 65.77 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.8 | 41.31 | 30.98 | 0.0 | 67.06 | 13.86 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.8 | 0.0 | 59.47 | 0.0 | 23.52 | 50.01 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.91 | 0.0 | 20.33 | 0.0 | 12.41 | 70.35 | 1.33 | underutilised: SM 39 %, DRAM 26 %, L2 16 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.49 | 12.03 | 41.96 | 0.0 | 27.8 | 33.82 | 1.89 | underutilised: SM 18 %, DRAM 20 %, L2 30 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.35 | 0.0 | 46.16 | 0.0 | 28.37 | 50.29 | 0.83 | underutilised: SM 20 %, DRAM 38 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.75 | 0.0 | 25.28 | 0.0 | 12.26 | 14.52 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.45 | 0.0 | 51.6 | 0.0 | 20.26 | 44.4 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.65 | 0.0 | 38.89 | 0.0 | 22.75 | 66.02 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.8 | 41.54 | 30.95 | 0.0 | 67.27 | 13.84 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.7 | 0.0 | 60.81 | 0.0 | 23.99 | 50.77 | 0.67 | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 54 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.29 | 0.0 | 20.0 | 0.0 | 12.25 | 70.44 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.49 | 12.22 | 41.46 | 0.0 | 27.91 | 33.78 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.04 | 0.0 | 44.71 | 0.0 | 28.24 | 50.73 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 65 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.76 | 0.0 | 26.64 | 0.0 | 13.89 | 14.37 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.71 | 0.0 | 50.61 | 0.0 | 19.87 | 44.82 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.3 | 0.0 | 38.4 | 0.0 | 22.63 | 65.52 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.61 | 41.81 | 30.85 | 0.0 | 66.65 | 13.72 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.64 | 0.0 | 59.81 | 0.0 | 23.69 | 50.26 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 53 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.49 | 0.0 | 19.11 | 0.0 | 12.08 | 70.23 | 1.33 | underutilised: SM 37 %, DRAM 29 %, L2 18 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.28 | 12.15 | 46.47 | 0.0 | 27.75 | 34.04 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.23 | 0.0 | 45.06 | 0.0 | 28.35 | 50.56 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.79 | 0.0 | 25.58 | 0.0 | 12.1 | 14.34 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.39 | 0.0 | 50.76 | 0.0 | 19.94 | 44.66 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.17 | 0.0 | 39.38 | 0.0 | 22.66 | 65.8 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.24 | 41.39 | 30.65 | 0.0 | 66.92 | 13.74 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.68 | 0.0 | 60.32 | 0.0 | 23.77 | 50.75 | 0.67 | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 55 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.38 | 0.0 | 20.62 | 0.0 | 12.31 | 69.9 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.41 | 12.2 | 41.62 | 0.0 | 28.3 | 33.74 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.46 | 0.0 | 45.24 | 0.0 | 28.07 | 50.74 | 0.83 | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 63 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.73 | 0.0 | 25.18 | 0.0 | 11.94 | 14.55 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.56 | 0.0 | 50.61 | 0.0 | 19.85 | 44.25 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.36 | 0.0 | 37.98 | 0.0 | 22.57 | 65.63 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.16 | 41.51 | 31.05 | 0.0 | 67.7 | 13.75 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.82 | 0.0 | 60.23 | 0.0 | 23.82 | 50.62 | 0.67 | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 56 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.29 | 0.0 | 20.02 | 0.0 | 12.24 | 70.25 | 1.33 | underutilised: SM 39 %, DRAM 27 %, L2 16 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.41 | 12.02 | 46.56 | 0.0 | 27.71 | 33.8 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.34 | 0.0 | 44.91 | 0.0 | 28.22 | 50.68 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.8 | 0.0 | 8.11 | 0.0 | 3.58 | 14.69 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.67 | 0.0 | 49.9 | 0.0 | 19.57 | 44.54 | 0.34 | underutilised: SM 2 %, DRAM 49 %, L2 19 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.4 | 0.0 | 38.87 | 0.0 | 22.95 | 65.4 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.5 | 41.88 | 30.79 | 0.0 | 66.9 | 13.88 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.61 | 0.0 | 60.31 | 0.0 | 23.86 | 50.98 | 0.67 | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 54 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.19 | 0.0 | 19.89 | 0.0 | 12.35 | 70.32 | 1.33 | underutilised: SM 40 %, DRAM 29 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.19 | 12.27 | 47.08 | 0.0 | 27.69 | 33.78 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.42 | 0.0 | 45.11 | 0.0 | 28.38 | 50.16 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.75 | 0.0 | 26.22 | 0.0 | 12.53 | 14.48 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.75 | 0.0 | 49.66 | 0.0 | 19.49 | 44.42 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.3 | 0.0 | 38.2 | 0.0 | 22.69 | 65.8 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.05 | 41.45 | 30.84 | 0.0 | 67.05 | 13.79 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.86 | 0.0 | 61.17 | 0.0 | 24.28 | 50.82 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.4 | 0.0 | 20.15 | 0.0 | 12.3 | 70.01 | 1.33 | underutilised: SM 40 %, DRAM 26 %, L2 16 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.4 | 12.09 | 44.75 | 0.0 | 27.99 | 25.85 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 7.28 | 0.0 | 45.77 | 0.0 | 28.56 | 50.65 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.75 | 0.0 | 25.28 | 0.0 | 12.12 | 14.48 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.47 | 0.0 | 52.08 | 0.0 | 20.46 | 44.52 | 0.34 | underutilised: SM 2 %, DRAM 53 %, L2 21 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.72 | 0.0 | 39.64 | 0.0 | 22.7 | 65.7 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 38.33 | 41.59 | 30.82 | 0.0 | 67.31 | 13.75 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.64 | 0.0 | 58.92 | 0.0 | 23.25 | 51.06 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 56 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.46 | 0.0 | 20.15 | 0.0 | 12.28 | 70.21 | 1.33 | underutilised: SM 40 %, DRAM 27 %, L2 16 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.42 | 12.18 | 46.67 | 0.0 | 27.97 | 33.72 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.41 | 0.0 | 45.03 | 0.0 | 28.18 | 50.55 | 0.83 | underutilised: SM 20 %, DRAM 36 %, L2 33 %, occ 65 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.74 | 0.0 | 26.54 | 0.0 | 12.57 | 14.46 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.46 | 0.0 | 50.34 | 0.0 | 19.74 | 44.58 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.85 | 0.0 | 38.48 | 0.0 | 22.57 | 65.64 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.36 | 41.84 | 30.72 | 0.0 | 66.95 | 13.76 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.27 | 0.0 | 60.41 | 0.0 | 23.86 | 50.95 | 0.67 | underutilised: SM 13 %, DRAM 31 %, L2 19 %, occ 55 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.81 | 0.0 | 19.98 | 0.0 | 12.17 | 70.25 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 77 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.32 | 12.02 | 41.84 | 0.0 | 27.8 | 33.66 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.1 | 0.0 | 45.31 | 0.0 | 27.43 | 50.63 | 0.83 | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.78 | 0.0 | 25.11 | 0.0 | 11.95 | 14.42 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.47 | 0.0 | 50.96 | 0.0 | 20.04 | 44.55 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.36 | 0.0 | 38.71 | 0.0 | 22.47 | 65.1 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.39 | 41.39 | 31.07 | 0.0 | 67.12 | 13.75 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.12 | 0.0 | 61.31 | 0.0 | 24.28 | 51.02 | 0.67 | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 56 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.51 | 0.0 | 20.18 | 0.0 | 12.35 | 70.05 | 1.33 | underutilised: SM 39 %, DRAM 27 %, L2 16 %, occ 77 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.46 | 12.27 | 41.55 | 0.0 | 28.0 | 33.77 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 7.87 | 0.0 | 46.55 | 0.0 | 28.33 | 50.27 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.75 | 0.0 | 25.32 | 0.0 | 12.08 | 14.46 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.71 | 0.0 | 49.78 | 0.0 | 19.53 | 44.4 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.67 | 0.0 | 38.73 | 0.0 | 22.56 | 65.61 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.12 | 41.62 | 30.9 | 0.0 | 66.99 | 13.75 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.65 | 0.0 | 59.57 | 0.0 | 23.59 | 50.8 | 0.67 | underutilised: SM 14 %, DRAM 31 %, L2 19 %, occ 56 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.55 | 0.0 | 19.6 | 0.0 | 12.07 | 70.11 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.42 | 11.98 | 40.96 | 0.0 | 27.6 | 33.61 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.42 | 0.0 | 45.72 | 0.0 | 28.52 | 49.72 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.75 | 0.0 | 26.45 | 0.0 | 12.37 | 14.65 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.53 | 0.0 | 50.36 | 0.0 | 19.79 | 44.58 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.55 | 0.0 | 38.47 | 0.0 | 22.63 | 65.59 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.77 | 41.89 | 30.96 | 0.0 | 67.46 | 13.8 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.51 | 0.0 | 58.87 | 0.0 | 23.34 | 51.53 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.36 | 0.0 | 20.11 | 0.0 | 12.38 | 70.23 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.3 | 12.16 | 46.49 | 0.0 | 27.89 | 33.64 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.44 | 0.0 | 45.41 | 0.0 | 28.4 | 50.14 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 63 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.75 | 0.0 | 24.82 | 0.0 | 11.81 | 14.42 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.66 | 0.0 | 50.95 | 0.0 | 20.04 | 44.54 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.65 | 0.0 | 38.97 | 0.0 | 22.38 | 65.84 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.36 | 41.41 | 31.05 | 0.0 | 66.81 | 14.01 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.18 | 0.0 | 61.02 | 0.0 | 24.12 | 51.04 | 0.67 | underutilised: SM 13 %, DRAM 31 %, L2 18 %, occ 56 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.48 | 0.0 | 19.94 | 0.0 | 12.35 | 70.23 | 1.33 | underutilised: SM 39 %, DRAM 27 %, L2 16 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.27 | 12.13 | 45.38 | 0.0 | 27.78 | 33.77 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.05 | 0.0 | 43.71 | 0.0 | 28.32 | 50.6 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 63 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.8 | 0.0 | 8.44 | 0.0 | 3.67 | 14.44 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.65 | 0.0 | 51.13 | 0.0 | 20.08 | 44.64 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.84 | 0.0 | 38.93 | 0.0 | 22.91 | 65.47 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 37.16 | 41.66 | 31.0 | 0.0 | 67.01 | 13.81 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.0 | 0.0 | 60.36 | 0.0 | 23.78 | 50.11 | 0.67 | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 56 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.59 | 0.0 | 20.17 | 0.0 | 12.29 | 70.27 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.46 | 12.19 | 45.42 | 0.0 | 27.89 | 33.79 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 8.48 | 0.0 | 45.35 | 0.0 | 28.22 | 50.66 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.75 | 0.0 | 25.02 | 0.0 | 11.87 | 14.35 | 0.15 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 6.47 | 0.0 | 50.78 | 0.0 | 19.94 | 44.65 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 16.41 | 0.0 | 38.74 | 0.0 | 22.75 | 65.4 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 38.11 | 41.97 | 30.91 | 0.0 | 66.97 | 13.74 | 1.0 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 13.77 | 0.0 | 59.8 | 0.0 | 23.64 | 50.58 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 55 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 28.85 | 0.0 | 20.16 | 0.0 | 12.23 | 70.0 | 1.33 | underutilised: SM 40 %, DRAM 28 %, L2 18 %, occ 76 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 22.22 | 12.14 | 45.11 | 0.0 | 27.81 | 34.01 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.33 | 0.0 | 37.65 | 0.0 | 24.14 | 35.29 | 0.5 | underutilised: SM 17 %, DRAM 33 %, L2 31 %, occ 68 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.64 | 0.0 | 20.53 | 0.0 | 9.97 | 11.84 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 27 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.69 | 0.0 | 40.62 | 0.0 | 15.96 | 45.41 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.32 | 0.0 | 35.0 | 0.0 | 20.74 | 65.75 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.75 | 39.73 | 36.11 | 0.0 | 65.23 | 14.26 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.71 | 0.0 | 54.92 | 0.0 | 21.69 | 36.68 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.36 | 0.0 | 14.78 | 0.0 | 9.35 | 70.79 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.19 | 8.98 | 42.19 | 0.0 | 25.55 | 33.41 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 25 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.21 | 0.0 | 37.69 | 0.0 | 24.03 | 35.04 | 0.5 | underutilised: SM 18 %, DRAM 33 %, L2 31 %, occ 68 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.53 | 0.0 | 9.98 | 12.1 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.74 | 0.0 | 41.36 | 0.0 | 16.24 | 45.44 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.18 | 0.0 | 36.1 | 0.0 | 20.78 | 66.53 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.75 | 39.83 | 36.05 | 0.0 | 65.01 | 14.17 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.72 | 0.0 | 52.66 | 0.0 | 20.85 | 36.51 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.51 | 0.0 | 15.67 | 0.0 | 9.71 | 70.92 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.17 | 8.84 | 42.14 | 0.0 | 25.81 | 33.37 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.39 | 0.0 | 38.62 | 0.0 | 23.6 | 35.11 | 0.5 | underutilised: SM 18 %, DRAM 32 %, L2 31 %, occ 67 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.61 | 0.0 | 20.54 | 0.0 | 10.08 | 12.05 | 0.1 | underutilised: SM 2 %, DRAM 59 %, L2 27 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.57 | 0.0 | 40.65 | 0.0 | 15.92 | 45.03 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.47 | 0.0 | 35.8 | 0.0 | 20.86 | 66.74 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.22 | 39.38 | 35.88 | 0.0 | 65.58 | 14.18 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.55 | 0.0 | 53.72 | 0.0 | 21.24 | 36.5 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.66 | 0.0 | 15.65 | 0.0 | 9.76 | 71.17 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.08 | 8.82 | 42.44 | 0.0 | 25.45 | 33.33 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.31 | 0.0 | 37.69 | 0.0 | 23.89 | 35.13 | 0.5 | underutilised: SM 19 %, DRAM 30 %, L2 29 %, occ 69 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.6 | 0.0 | 20.82 | 0.0 | 10.24 | 11.86 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.79 | 0.0 | 41.51 | 0.0 | 16.26 | 45.41 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.15 | 0.0 | 35.62 | 0.0 | 20.47 | 66.79 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.67 | 38.1 | 35.69 | 0.0 | 66.28 | 14.16 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 10.06 | 0.0 | 54.29 | 0.0 | 21.46 | 36.35 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.17 | 0.0 | 15.67 | 0.0 | 9.7 | 71.06 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.27 | 8.78 | 42.52 | 0.0 | 25.61 | 33.35 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.33 | 0.0 | 38.03 | 0.0 | 24.06 | 34.76 | 0.5 | underutilised: SM 19 %, DRAM 31 %, L2 30 %, occ 69 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.41 | 0.0 | 11.19 | 12.02 | 0.1 | underutilised: SM 2 %, DRAM 58 %, L2 26 %, occ 27 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.7 | 0.0 | 39.61 | 0.0 | 15.54 | 45.21 | 0.46 | underutilised: SM 1 %, DRAM 34 %, L2 13 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.34 | 0.0 | 35.18 | 0.0 | 20.49 | 66.68 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.96 | 40.01 | 36.05 | 0.0 | 65.1 | 14.21 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.72 | 0.0 | 53.89 | 0.0 | 21.31 | 36.24 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 24.7 | 0.0 | 15.78 | 0.0 | 9.75 | 70.64 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.18 | 8.83 | 41.82 | 0.0 | 25.6 | 33.18 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.34 | 0.0 | 36.79 | 0.0 | 23.99 | 34.72 | 0.5 | underutilised: SM 18 %, DRAM 32 %, L2 31 %, occ 69 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.66 | 0.0 | 20.77 | 0.0 | 11.14 | 11.99 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.94 | 0.0 | 40.14 | 0.0 | 15.71 | 45.41 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.32 | 0.0 | 35.74 | 0.0 | 20.77 | 66.77 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.24 | 40.19 | 36.22 | 0.0 | 66.17 | 14.23 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.67 | 0.0 | 53.71 | 0.0 | 21.19 | 36.8 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.28 | 0.0 | 16.03 | 0.0 | 9.66 | 70.97 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 13 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.09 | 8.94 | 42.54 | 0.0 | 25.65 | 33.2 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 25 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.25 | 0.0 | 38.56 | 0.0 | 24.45 | 34.94 | 0.5 | underutilised: SM 19 %, DRAM 31 %, L2 29 %, occ 67 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.64 | 0.0 | 21.94 | 0.0 | 10.61 | 11.9 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 27 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.59 | 0.0 | 40.27 | 0.0 | 15.79 | 44.45 | 0.46 | underutilised: SM 1 %, DRAM 32 %, L2 13 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.25 | 0.0 | 36.56 | 0.0 | 20.49 | 66.86 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.69 | 39.88 | 36.34 | 0.0 | 66.41 | 14.23 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.66 | 0.0 | 45.17 | 0.0 | 17.81 | 36.93 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.2 | 0.0 | 15.58 | 0.0 | 9.69 | 70.36 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.13 | 8.91 | 42.55 | 0.0 | 25.66 | 33.42 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.27 | 0.0 | 38.17 | 0.0 | 23.85 | 35.27 | 0.5 | underutilised: SM 18 %, DRAM 31 %, L2 30 %, occ 69 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.82 | 0.0 | 10.16 | 12.15 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.7 | 0.0 | 40.62 | 0.0 | 15.94 | 45.43 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.5 | 0.0 | 35.68 | 0.0 | 20.82 | 66.45 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.79 | 39.71 | 36.09 | 0.0 | 65.77 | 14.14 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.91 | 0.0 | 54.28 | 0.0 | 21.5 | 36.17 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.5 | 0.0 | 15.64 | 0.0 | 9.75 | 70.75 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 13 %, occ 83 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.15 | 8.8 | 42.28 | 0.0 | 25.83 | 33.12 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 5.92 | 0.0 | 38.4 | 0.0 | 23.95 | 34.87 | 0.5 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 67 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.61 | 0.0 | 20.37 | 0.0 | 9.95 | 11.95 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.61 | 0.0 | 41.41 | 0.0 | 16.24 | 45.1 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 12.95 | 0.0 | 35.89 | 0.0 | 20.57 | 65.96 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.11 | 37.31 | 35.9 | 0.0 | 64.86 | 14.2 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.7 | 0.0 | 55.5 | 0.0 | 21.98 | 36.5 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.42 | 0.0 | 15.8 | 0.0 | 9.69 | 71.74 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.28 | 8.91 | 42.3 | 0.0 | 25.62 | 33.51 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.33 | 0.0 | 38.42 | 0.0 | 23.13 | 34.95 | 0.5 | underutilised: SM 17 %, DRAM 33 %, L2 31 %, occ 68 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.72 | 0.0 | 10.08 | 11.96 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.7 | 0.0 | 39.59 | 0.0 | 15.54 | 45.4 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.16 | 0.0 | 35.95 | 0.0 | 20.8 | 66.93 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.86 | 39.34 | 36.09 | 0.0 | 66.08 | 14.23 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.92 | 0.0 | 54.9 | 0.0 | 21.72 | 36.26 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.4 | 0.0 | 15.51 | 0.0 | 9.61 | 71.16 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.28 | 8.76 | 42.41 | 0.0 | 25.75 | 33.14 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.36 | 0.0 | 37.97 | 0.0 | 23.96 | 34.73 | 0.5 | underutilised: SM 18 %, DRAM 31 %, L2 30 %, occ 69 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.61 | 0.0 | 20.79 | 0.0 | 10.02 | 11.99 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.62 | 0.0 | 39.97 | 0.0 | 15.72 | 45.22 | 0.46 | underutilised: SM 1 %, DRAM 34 %, L2 15 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.6 | 0.0 | 35.34 | 0.0 | 21.04 | 65.72 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.37 | 40.05 | 35.88 | 0.0 | 65.69 | 14.19 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.94 | 0.0 | 53.69 | 0.0 | 21.2 | 36.62 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.59 | 0.0 | 15.56 | 0.0 | 9.69 | 70.9 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 13 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.18 | 8.9 | 42.36 | 0.0 | 25.72 | 33.27 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.12 | 0.0 | 37.43 | 0.0 | 24.01 | 35.34 | 0.5 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 67 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.61 | 0.0 | 20.73 | 0.0 | 10.1 | 11.97 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 25 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.55 | 0.0 | 40.79 | 0.0 | 16.02 | 45.39 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 12.89 | 0.0 | 34.74 | 0.0 | 20.44 | 66.93 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.11 | 40.02 | 36.02 | 0.0 | 65.67 | 14.16 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.84 | 0.0 | 54.06 | 0.0 | 21.38 | 36.81 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.41 | 0.0 | 16.02 | 0.0 | 10.2 | 70.77 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.12 | 8.68 | 42.24 | 0.0 | 25.59 | 33.24 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.21 | 0.0 | 37.63 | 0.0 | 23.92 | 35.25 | 0.5 | underutilised: SM 19 %, DRAM 32 %, L2 31 %, occ 69 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.51 | 0.0 | 10.0 | 12.01 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.66 | 0.0 | 40.44 | 0.0 | 15.87 | 45.17 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.63 | 0.0 | 35.74 | 0.0 | 20.67 | 66.52 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.84 | 39.55 | 35.85 | 0.0 | 65.72 | 14.2 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.74 | 0.0 | 54.63 | 0.0 | 21.55 | 36.62 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.48 | 0.0 | 15.72 | 0.0 | 9.71 | 71.05 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.23 | 8.99 | 42.16 | 0.0 | 25.69 | 33.18 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.37 | 0.0 | 38.48 | 0.0 | 23.84 | 34.92 | 0.5 | underutilised: SM 18 %, DRAM 31 %, L2 29 %, occ 68 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.97 | 0.0 | 10.22 | 12.14 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 25 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.56 | 0.0 | 41.51 | 0.0 | 16.84 | 45.48 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.23 | 0.0 | 35.6 | 0.0 | 20.35 | 66.78 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.83 | 37.75 | 36.17 | 0.0 | 65.83 | 14.44 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.67 | 0.0 | 54.33 | 0.0 | 21.57 | 36.21 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.74 | 0.0 | 15.65 | 0.0 | 9.75 | 70.96 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.11 | 8.85 | 42.1 | 0.0 | 25.83 | 33.06 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.33 | 0.0 | 38.05 | 0.0 | 24.07 | 34.71 | 0.5 | underutilised: SM 18 %, DRAM 33 %, L2 31 %, occ 68 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.61 | 0.0 | 9.98 | 11.89 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.6 | 0.0 | 41.57 | 0.0 | 16.34 | 45.05 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.43 | 0.0 | 36.68 | 0.0 | 20.68 | 66.7 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.96 | 39.68 | 36.51 | 0.0 | 66.68 | 14.21 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.78 | 0.0 | 54.28 | 0.0 | 21.47 | 36.44 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.52 | 0.0 | 15.46 | 0.0 | 9.63 | 70.96 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 13 %, occ 83 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.06 | 8.79 | 42.26 | 0.0 | 25.98 | 33.45 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.25 | 0.0 | 38.82 | 0.0 | 24.08 | 35.15 | 0.5 | underutilised: SM 18 %, DRAM 31 %, L2 29 %, occ 69 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.6 | 0.0 | 10.08 | 12.11 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.77 | 0.0 | 40.14 | 0.0 | 15.75 | 45.45 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.1 | 0.0 | 35.08 | 0.0 | 20.56 | 66.66 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.15 | 38.21 | 35.95 | 0.0 | 65.72 | 14.44 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.82 | 0.0 | 54.15 | 0.0 | 21.37 | 36.41 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.12 | 0.0 | 15.39 | 0.0 | 9.55 | 70.85 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.14 | 8.81 | 42.65 | 0.0 | 25.66 | 33.19 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.26 | 0.0 | 37.92 | 0.0 | 24.19 | 35.02 | 0.5 | underutilised: SM 17 %, DRAM 33 %, L2 31 %, occ 68 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.59 | 0.0 | 19.56 | 0.0 | 9.53 | 11.94 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.89 | 0.0 | 40.37 | 0.0 | 15.82 | 45.14 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.14 | 0.0 | 36.27 | 0.0 | 21.12 | 66.14 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.93 | 39.82 | 35.74 | 0.0 | 65.46 | 14.13 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.82 | 0.0 | 55.17 | 0.0 | 21.81 | 36.33 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 24.81 | 0.0 | 15.67 | 0.0 | 9.71 | 70.82 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.36 | 8.69 | 42.45 | 0.0 | 25.48 | 33.17 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.3 | 0.0 | 37.35 | 0.0 | 23.93 | 34.74 | 0.5 | underutilised: SM 18 %, DRAM 31 %, L2 30 %, occ 68 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.67 | 0.0 | 10.08 | 11.91 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.57 | 0.0 | 41.05 | 0.0 | 16.15 | 45.28 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.08 | 0.0 | 36.17 | 0.0 | 20.85 | 66.69 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.01 | 40.02 | 35.9 | 0.0 | 66.5 | 14.19 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 10.05 | 0.0 | 53.41 | 0.0 | 21.11 | 36.71 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.46 | 0.0 | 15.5 | 0.0 | 9.58 | 71.04 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.16 | 8.72 | 41.27 | 0.0 | 24.72 | 32.86 | 1.42 | underutilised: SM 11 %, DRAM 6 %, L2 6 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.21 | 0.0 | 37.35 | 0.0 | 23.97 | 35.21 | 0.5 | underutilised: SM 19 %, DRAM 32 %, L2 30 %, occ 66 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.63 | 0.0 | 20.56 | 0.0 | 12.26 | 11.83 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.55 | 0.0 | 40.97 | 0.0 | 16.11 | 45.17 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 12.93 | 0.0 | 35.2 | 0.0 | 21.03 | 66.38 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.98 | 39.57 | 35.76 | 0.0 | 65.87 | 14.18 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.63 | 0.0 | 54.37 | 0.0 | 21.49 | 37.04 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.12 | 0.0 | 16.14 | 0.0 | 9.72 | 70.99 | 1.33 | underutilised: SM 32 %, DRAM 22 %, L2 14 %, occ 83 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.33 | 8.9 | 42.16 | 0.0 | 25.78 | 33.15 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.14 | 0.0 | 37.87 | 0.0 | 24.15 | 34.85 | 0.5 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 67 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.77 | 0.0 | 10.08 | 11.95 | 0.1 | underutilised: SM 2 %, DRAM 58 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.87 | 0.0 | 39.0 | 0.0 | 15.32 | 45.47 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.4 | 0.0 | 36.06 | 0.0 | 21.11 | 66.9 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.01 | 38.36 | 36.1 | 0.0 | 65.7 | 14.26 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.91 | 0.0 | 54.23 | 0.0 | 21.41 | 36.64 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.45 | 0.0 | 15.13 | 0.0 | 9.38 | 71.01 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.27 | 8.94 | 39.25 | 0.0 | 25.53 | 33.33 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.38 | 0.0 | 37.44 | 0.0 | 23.95 | 34.64 | 0.5 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 68 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.6 | 0.0 | 20.5 | 0.0 | 10.07 | 11.89 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 27 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.95 | 0.0 | 40.29 | 0.0 | 15.82 | 45.13 | 0.46 | underutilised: SM 1 %, DRAM 38 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.2 | 0.0 | 35.57 | 0.0 | 20.34 | 66.97 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.31 | 39.38 | 35.84 | 0.0 | 66.2 | 14.14 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.87 | 0.0 | 54.64 | 0.0 | 21.56 | 36.61 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.36 | 0.0 | 15.67 | 0.0 | 9.77 | 70.96 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.06 | 8.74 | 42.59 | 0.0 | 25.43 | 33.45 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.28 | 0.0 | 38.73 | 0.0 | 23.93 | 35.02 | 0.5 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 67 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.19 | 0.0 | 20.8 | 0.0 | 10.03 | 12.09 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.57 | 0.0 | 40.88 | 0.0 | 16.01 | 45.43 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.27 | 0.0 | 36.13 | 0.0 | 20.8 | 66.05 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.79 | 39.88 | 36.11 | 0.0 | 65.55 | 14.21 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.75 | 0.0 | 53.59 | 0.0 | 21.2 | 36.88 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.53 | 0.0 | 15.95 | 0.0 | 9.71 | 70.96 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.16 | 8.77 | 42.58 | 0.0 | 25.73 | 33.18 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 25 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.31 | 0.0 | 38.72 | 0.0 | 24.2 | 35.24 | 0.5 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 68 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.65 | 0.0 | 10.01 | 11.85 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.6 | 0.0 | 40.1 | 0.0 | 15.74 | 45.04 | 0.46 | underutilised: SM 1 %, DRAM 33 %, L2 13 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.07 | 0.0 | 35.68 | 0.0 | 20.62 | 66.62 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.03 | 39.96 | 36.41 | 0.0 | 66.08 | 14.19 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.73 | 0.0 | 54.27 | 0.0 | 21.39 | 36.56 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.48 | 0.0 | 15.55 | 0.0 | 9.6 | 70.72 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.18 | 8.85 | 42.59 | 0.0 | 25.66 | 33.55 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.31 | 0.0 | 37.8 | 0.0 | 23.79 | 35.21 | 0.5 | underutilised: SM 19 %, DRAM 32 %, L2 30 %, occ 68 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.61 | 0.0 | 20.53 | 0.0 | 9.94 | 12.1 | 0.1 | underutilised: SM 2 %, DRAM 55 %, L2 25 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.6 | 0.0 | 41.05 | 0.0 | 16.14 | 45.47 | 0.46 | underutilised: SM 1 %, DRAM 34 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.44 | 0.0 | 36.21 | 0.0 | 20.75 | 65.99 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.71 | 39.69 | 36.59 | 0.0 | 66.35 | 14.16 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.83 | 0.0 | 54.24 | 0.0 | 21.37 | 36.83 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.4 | 0.0 | 15.65 | 0.0 | 9.8 | 70.86 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.15 | 8.71 | 42.14 | 0.0 | 25.64 | 33.12 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.35 | 0.0 | 35.27 | 0.0 | 23.92 | 35.06 | 0.5 | underutilised: SM 18 %, DRAM 30 %, L2 29 %, occ 69 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.6 | 0.0 | 21.29 | 0.0 | 10.34 | 11.78 | 0.1 | underutilised: SM 2 %, DRAM 59 %, L2 27 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.68 | 0.0 | 40.93 | 0.0 | 16.04 | 45.22 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.38 | 0.0 | 36.25 | 0.0 | 20.95 | 66.53 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.05 | 39.87 | 35.56 | 0.0 | 64.58 | 14.24 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.9 | 0.0 | 45.5 | 0.0 | 18.06 | 36.38 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.43 | 0.0 | 15.93 | 0.0 | 9.65 | 70.5 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.17 | 9.02 | 42.42 | 0.0 | 25.81 | 33.45 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.34 | 0.0 | 38.12 | 0.0 | 24.09 | 34.85 | 0.5 | underutilised: SM 19 %, DRAM 32 %, L2 31 %, occ 69 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.65 | 0.0 | 21.87 | 0.0 | 10.69 | 12.12 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.69 | 0.0 | 40.82 | 0.0 | 15.63 | 45.44 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.5 | 0.0 | 35.31 | 0.0 | 20.66 | 66.1 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.04 | 39.99 | 36.3 | 0.0 | 65.78 | 14.14 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.85 | 0.0 | 53.1 | 0.0 | 20.95 | 36.39 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.56 | 0.0 | 15.98 | 0.0 | 9.68 | 70.84 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.23 | 8.94 | 42.68 | 0.0 | 25.69 | 33.12 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.32 | 0.0 | 37.97 | 0.0 | 24.12 | 34.94 | 0.5 | underutilised: SM 17 %, DRAM 33 %, L2 31 %, occ 67 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.57 | 0.0 | 20.75 | 0.0 | 10.03 | 11.87 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 27 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.94 | 0.0 | 40.19 | 0.0 | 15.78 | 45.08 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.63 | 0.0 | 35.68 | 0.0 | 20.82 | 66.33 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 31.1 | 40.03 | 35.64 | 0.0 | 64.91 | 14.12 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 9.81 | 0.0 | 54.53 | 0.0 | 21.49 | 36.74 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.49 | 0.0 | 15.83 | 0.0 | 9.72 | 70.88 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 17.87 | 8.88 | 42.6 | 0.0 | 25.87 | 33.33 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | copy | 6.13 | 0.0 | 37.46 | 0.0 | 24.04 | 35.07 | 0.5 | underutilised: SM 19 %, DRAM 32 %, L2 31 %, occ 66 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_unary | 0.6 | 0.0 | 20.74 | 0.0 | 10.1 | 11.99 | 0.1 | underutilised: SM 2 %, DRAM 58 %, L2 26 %, occ 28 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | reduce | 9.72 | 0.0 | 41.14 | 0.0 | 16.15 | 45.39 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_binary | 13.16 | 0.0 | 35.28 | 0.0 | 20.67 | 66.76 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | gemm | 30.94 | 39.41 | 36.47 | 0.0 | 66.29 | 14.14 | 1.5 | L2-bandwidth-bound (working set in L2) |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | elementwise_other | 10.01 | 0.0 | 53.9 | 0.0 | 21.24 | 36.45 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | concat | 25.51 | 0.0 | 15.7 | 0.0 | 9.55 | 64.29 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| planner_debate | mir_operator:prefill_layer* | False | 1.12 % | profiled | attention | 18.28 | 8.79 | 42.35 | 0.0 | 25.68 | 33.27 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 25 %, occ 8 % |
| planner_debate | mir_operator:prefill_head | False | 0.01 % | profiled | copy | 9.67 | 0.0 | 51.61 | 0.0 | 28.28 | 55.81 | 1.0 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 63 % |
| planner_debate | mir_operator:prefill_head | False | 0.01 % | profiled | elementwise_unary | 0.94 | 0.0 | 30.91 | 0.0 | 14.4 | 23.47 | 0.29 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_head | False | 0.01 % | profiled | reduce | 1.61 | 0.0 | 50.85 | 0.0 | 19.98 | 33.27 | 0.08 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | mir_operator:prefill_head | False | 0.01 % | profiled | elementwise_binary | 16.63 | 0.0 | 40.27 | 0.0 | 24.31 | 65.06 | 1.33 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_head | False | 0.01 % | profiled | gemm | 46.46 | 45.87 | 52.55 | 0.0 | 72.22 | 16.55 | 37.09 | tensor-core compute-bound |
| planner_debate | mir_operator:prefill_head | False | 0.01 % | profiled | copy | 10.06 | 0.0 | 44.62 | 0.0 | 27.64 | 50.23 | 0.67 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 69 % |
| planner_debate | mir_operator:prefill_head | False | 0.01 % | profiled | elementwise_unary | 0.84 | 0.0 | 28.63 | 0.0 | 13.46 | 17.9 | 0.21 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 27 % |
| planner_debate | mir_operator:prefill_head | False | 0.01 % | profiled | reduce | 1.24 | 0.0 | 37.41 | 0.0 | 14.66 | 33.27 | 0.06 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | mir_operator:prefill_head | False | 0.01 % | profiled | elementwise_binary | 13.86 | 0.0 | 37.78 | 0.0 | 23.46 | 67.74 | 0.92 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_head | False | 0.01 % | profiled | gemm | 41.79 | 42.29 | 65.08 | 0.0 | 66.8 | 16.31 | 19.7 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:prefill_sample | False | 0.06 % | profiled | reduce | 2.79 | 0.0 | 5.27 | 0.0 | 3.04 | 33.13 | 0.05 | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:prefill_sample | False | 0.06 % | profiled | reduce | 2.79 | 0.0 | 5.26 | 0.0 | 3.26 | 33.13 | 0.05 | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_embed | False | 0.15 % | profiled | other | 0.25 | 0.0 | 0.34 | 0.0 | 0.65 | 8.31 | 0.01 | latency/launch-bound: 0.01 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_embed | False | 0.15 % | profiled | other | 0.25 | 0.0 | 0.34 | 0.0 | 0.71 | 8.31 | 0.01 | latency/launch-bound: 0.01 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.26 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.5 | 0.0 | 0.9 | 7.38 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.83 | 31.85 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.36 | 0.0 | 75.45 | 0.0 | 47.34 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.07 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.36 | 0.0 | 13.25 | 0.0 | 6.64 | 56.09 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.53 | 11.32 | 12.49 | 0.0 | 5.34 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.6 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.01 | 0.0 | 0.42 | 0.0 | 0.88 | 7.47 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.85 | 31.91 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.35 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.26 | 0.0 | 75.01 | 0.0 | 47.28 | 15.93 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.14 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.47 | 0.0 | 13.26 | 0.0 | 6.66 | 56.65 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.52 | 11.59 | 12.23 | 0.0 | 5.39 | 8.27 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.61 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.47 | 0.0 | 0.9 | 7.54 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.85 | 31.82 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.4 | 0.0 | 74.9 | 0.0 | 46.57 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.25 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.46 | 0.0 | 13.5 | 0.0 | 7.02 | 56.38 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.47 | 11.21 | 12.17 | 0.0 | 5.22 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.9 | 0.0 | 1.62 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.89 | 7.7 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.97 | 0.0 | 3.84 | 31.85 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.37 | 0.0 | 74.63 | 0.0 | 46.74 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.1 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.49 | 0.0 | 13.35 | 0.0 | 6.62 | 56.19 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.57 | 11.18 | 12.22 | 0.0 | 5.24 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 1.04 | 0.0 | 2.22 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.89 | 7.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.96 | 0.0 | 3.85 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.5 | 0.0 | 74.79 | 0.0 | 47.45 | 16.03 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.28 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.28 | 0.0 | 13.63 | 0.0 | 6.87 | 56.15 | 1.08 | underutilised: SM 5 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.39 | 11.33 | 6.79 | 0.0 | 3.1 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.82 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.89 | 7.48 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.85 | 31.78 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.42 | 0.0 | 74.47 | 0.0 | 46.52 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.08 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.34 | 0.0 | 13.47 | 0.0 | 6.75 | 55.97 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.54 | 11.35 | 12.45 | 0.0 | 5.53 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.76 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.89 | 7.66 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.83 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.43 | 0.0 | 74.85 | 0.0 | 46.57 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.11 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.35 | 0.0 | 13.37 | 0.0 | 6.69 | 56.28 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.54 | 11.27 | 12.29 | 0.0 | 5.23 | 8.27 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.9 | 0.0 | 2.21 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.89 | 7.78 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.97 | 0.0 | 3.85 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.41 | 0.0 | 75.4 | 0.0 | 47.16 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.17 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.49 | 0.0 | 5.29 | 0.0 | 5.95 | 56.59 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.46 | 11.36 | 11.95 | 0.0 | 5.13 | 8.3 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.76 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.89 | 7.5 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.81 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.5 | 0.0 | 75.35 | 0.0 | 46.8 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.13 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.37 | 0.0 | 13.38 | 0.0 | 6.69 | 56.06 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.51 | 11.26 | 12.22 | 0.0 | 5.25 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.87 | 0.0 | 2.22 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.89 | 7.46 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.84 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.54 | 0.0 | 74.36 | 0.0 | 46.97 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.17 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.41 | 0.0 | 13.31 | 0.0 | 6.66 | 56.12 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.48 | 11.25 | 12.71 | 0.0 | 5.44 | 8.3 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.9 | 0.0 | 1.85 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.91 | 7.65 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.83 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.35 | 0.0 | 74.75 | 0.0 | 46.93 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.16 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.44 | 0.0 | 13.38 | 0.0 | 6.7 | 55.94 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.42 | 11.18 | 11.9 | 0.0 | 5.12 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.88 | 0.0 | 1.61 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.88 | 7.7 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.85 | 31.88 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.44 | 0.0 | 75.45 | 0.0 | 47.46 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.09 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.5 | 0.0 | 14.04 | 0.0 | 8.92 | 56.16 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.55 | 11.43 | 12.67 | 0.0 | 5.41 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.59 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.36 | 0.0 | 0.89 | 7.6 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.83 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.34 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.47 | 0.0 | 74.47 | 0.0 | 46.78 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.15 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.35 | 0.0 | 12.93 | 0.0 | 7.09 | 56.1 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.55 | 11.3 | 12.3 | 0.0 | 5.27 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 2.18 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.39 | 0.0 | 0.89 | 7.65 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.85 | 31.82 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.48 | 0.0 | 74.75 | 0.0 | 46.55 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.16 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.52 | 0.0 | 13.26 | 0.0 | 6.72 | 56.09 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.53 | 11.21 | 12.22 | 0.0 | 5.26 | 8.27 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.9 | 0.0 | 1.52 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.89 | 7.59 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.83 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.35 | 0.0 | 75.34 | 0.0 | 47.53 | 15.95 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.11 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.51 | 0.0 | 13.37 | 0.0 | 6.68 | 55.97 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.54 | 11.14 | 12.39 | 0.0 | 5.34 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.9 | 0.0 | 1.62 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.9 | 7.67 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.83 | 31.92 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.44 | 0.0 | 75.34 | 0.0 | 46.76 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.74 | 0.0 | 1.08 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.32 | 0.0 | 13.41 | 0.0 | 6.97 | 56.08 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.55 | 11.46 | 12.62 | 0.0 | 5.39 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.9 | 0.0 | 1.81 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.87 | 7.54 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.85 | 31.89 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.44 | 0.0 | 75.07 | 0.0 | 47.92 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.39 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.39 | 0.0 | 13.41 | 0.0 | 7.21 | 55.81 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.44 | 11.23 | 12.05 | 0.0 | 5.16 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.9 | 0.0 | 1.6 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.88 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.96 | 0.0 | 3.83 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.5 | 0.0 | 74.96 | 0.0 | 47.16 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.07 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.46 | 0.0 | 13.42 | 0.0 | 7.08 | 56.32 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.53 | 11.37 | 13.96 | 0.0 | 5.57 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.6 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.9 | 7.69 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.95 | 0.0 | 3.84 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.51 | 0.0 | 74.79 | 0.0 | 46.67 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.41 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.33 | 0.0 | 13.48 | 0.0 | 6.75 | 56.01 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.48 | 11.4 | 12.31 | 0.0 | 5.31 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.84 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.6 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.99 | 0.0 | 3.87 | 31.85 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.5 | 0.0 | 75.23 | 0.0 | 46.83 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.15 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.5 | 0.0 | 13.11 | 0.0 | 6.85 | 56.62 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.53 | 11.48 | 12.31 | 0.0 | 5.27 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 2.17 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.89 | 7.65 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.82 | 31.91 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.38 | 0.0 | 75.4 | 0.0 | 46.88 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.09 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.51 | 0.0 | 13.49 | 0.0 | 6.72 | 56.29 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.54 | 11.23 | 12.56 | 0.0 | 5.37 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 2.19 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.88 | 7.48 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.83 | 31.91 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.54 | 0.0 | 75.56 | 0.0 | 46.93 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.07 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.47 | 0.0 | 13.38 | 0.0 | 6.64 | 56.44 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.51 | 11.14 | 12.4 | 0.0 | 5.86 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.84 | 0.0 | 1.51 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.89 | 7.66 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.81 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.49 | 0.0 | 74.85 | 0.0 | 47.31 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.07 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.37 | 0.0 | 13.97 | 0.0 | 7.21 | 56.06 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.45 | 11.17 | 11.97 | 0.0 | 5.13 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.9 | 0.0 | 1.78 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.93 | 7.64 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.84 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.6 | 0.0 | 75.12 | 0.0 | 46.73 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.17 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.44 | 0.0 | 13.43 | 0.0 | 6.87 | 56.17 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.56 | 11.44 | 12.13 | 0.0 | 5.19 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.9 | 0.0 | 1.81 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.91 | 7.69 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.81 | 31.87 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.58 | 0.0 | 75.07 | 0.0 | 47.23 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.16 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.35 | 0.0 | 13.44 | 0.0 | 6.74 | 56.58 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.53 | 11.14 | 12.5 | 0.0 | 5.37 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.6 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.89 | 7.46 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.87 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.43 | 0.0 | 75.34 | 0.0 | 46.99 | 16.03 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.38 | 8.25 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.43 | 0.0 | 13.41 | 0.0 | 6.99 | 56.18 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.54 | 11.21 | 12.28 | 0.0 | 5.47 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.9 | 0.0 | 1.62 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.88 | 7.7 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.84 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.47 | 0.0 | 75.45 | 0.0 | 47.21 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.11 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.45 | 0.0 | 13.41 | 0.0 | 6.73 | 56.25 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.55 | 11.23 | 12.27 | 0.0 | 6.13 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 1.02 | 0.0 | 1.66 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.47 | 0.0 | 0.89 | 7.46 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.86 | 31.85 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.34 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.48 | 0.0 | 75.07 | 0.0 | 47.22 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.08 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 5.28 | 0.0 | 13.54 | 0.0 | 6.73 | 56.25 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 0 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.55 | 11.13 | 12.49 | 0.0 | 5.32 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.56 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.94 | 7.52 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.8 | 31.87 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.38 | 0.0 | 74.77 | 0.0 | 46.82 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.72 | 0.0 | 1.23 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.65 | 0.0 | 10.56 | 0.0 | 5.64 | 50.56 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.93 | 12.04 | 9.33 | 0.0 | 4.16 | 8.28 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 2.14 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.64 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.89 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.42 | 0.0 | 74.55 | 0.0 | 46.38 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.15 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.76 | 0.0 | 10.25 | 0.0 | 5.39 | 50.52 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.01 | 11.97 | 9.48 | 0.0 | 4.5 | 8.3 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.88 | 0.0 | 1.61 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.9 | 7.71 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.84 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.41 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.48 | 0.0 | 74.55 | 0.0 | 46.81 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.3 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.78 | 0.0 | 10.45 | 0.0 | 5.57 | 50.44 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.96 | 12.05 | 9.38 | 0.0 | 4.18 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.87 | 0.0 | 1.79 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.39 | 0.0 | 0.91 | 7.71 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.96 | 0.0 | 3.85 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.47 | 0.0 | 74.71 | 0.0 | 46.89 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.26 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.76 | 0.0 | 10.55 | 0.0 | 5.69 | 50.86 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.99 | 12.05 | 9.31 | 0.0 | 4.16 | 8.28 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.87 | 0.0 | 1.81 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.91 | 7.58 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.84 | 31.93 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.42 | 0.0 | 74.25 | 0.0 | 47.7 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.29 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.7 | 0.0 | 10.58 | 0.0 | 5.4 | 50.44 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.95 | 12.04 | 9.34 | 0.0 | 4.14 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.76 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.01 | 0.0 | 0.42 | 0.0 | 0.89 | 7.34 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.85 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.49 | 0.0 | 75.01 | 0.0 | 47.26 | 15.95 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.19 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.84 | 0.0 | 10.4 | 0.0 | 5.3 | 50.69 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.96 | 12.16 | 9.43 | 0.0 | 4.21 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.87 | 0.0 | 1.87 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.92 | 7.67 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.86 | 31.91 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.42 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.52 | 0.0 | 75.57 | 0.0 | 47.04 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.27 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.61 | 0.0 | 3.12 | 0.0 | 1.8 | 50.78 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.95 | 12.09 | 9.23 | 0.0 | 4.11 | 8.27 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.73 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.61 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.86 | 31.88 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.54 | 0.0 | 74.82 | 0.0 | 46.83 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.18 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.77 | 0.0 | 10.72 | 0.0 | 5.45 | 50.47 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.98 | 12.13 | 9.47 | 0.0 | 4.22 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.61 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.97 | 7.67 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.87 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.43 | 0.0 | 74.8 | 0.0 | 47.07 | 15.94 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.29 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.67 | 0.0 | 11.0 | 0.0 | 5.62 | 50.73 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.96 | 11.97 | 9.27 | 0.0 | 4.14 | 8.27 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.6 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.94 | 7.69 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.88 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.37 | 0.0 | 74.61 | 0.0 | 46.96 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.41 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.76 | 0.0 | 10.53 | 0.0 | 5.42 | 50.85 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.0 | 12.18 | 9.48 | 0.0 | 4.45 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.86 | 0.0 | 1.75 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.91 | 7.69 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.84 | 31.89 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.44 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.51 | 0.0 | 75.12 | 0.0 | 46.83 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.18 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.67 | 0.0 | 10.22 | 0.0 | 5.49 | 50.41 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.97 | 12.06 | 9.37 | 0.0 | 4.16 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.87 | 0.0 | 1.56 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.91 | 7.71 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.97 | 0.0 | 3.84 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.45 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.42 | 0.0 | 75.29 | 0.0 | 47.05 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.78 | 0.0 | 1.41 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.71 | 0.0 | 10.61 | 0.0 | 5.67 | 50.36 | 0.92 | underutilised: SM 5 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.01 | 12.06 | 9.55 | 0.0 | 4.25 | 8.3 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.86 | 0.0 | 1.55 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.93 | 7.65 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.86 | 31.82 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.35 | 0.0 | 75.07 | 0.0 | 46.76 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.18 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.79 | 0.0 | 10.38 | 0.0 | 5.54 | 50.33 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.99 | 11.8 | 9.44 | 0.0 | 4.23 | 8.27 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.6 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.5 | 0.0 | 0.88 | 7.71 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.97 | 0.0 | 3.88 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.44 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.44 | 0.0 | 75.21 | 0.0 | 46.94 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.16 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.75 | 0.0 | 11.09 | 0.0 | 5.64 | 50.59 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.98 | 12.11 | 9.45 | 0.0 | 4.22 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.55 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.39 | 0.0 | 0.9 | 7.64 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.82 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.48 | 0.0 | 75.01 | 0.0 | 47.26 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.24 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.72 | 0.0 | 10.75 | 0.0 | 5.44 | 50.75 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.94 | 12.03 | 9.24 | 0.0 | 4.14 | 8.3 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 1.01 | 0.0 | 2.14 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.01 | 0.0 | 0.51 | 0.0 | 0.91 | 7.68 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.95 | 0.0 | 3.82 | 31.85 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.32 | 0.0 | 74.69 | 0.0 | 46.94 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.18 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.71 | 0.0 | 10.41 | 0.0 | 5.36 | 50.67 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.04 | 11.9 | 9.32 | 0.0 | 4.41 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.01 | 0.0 | 0.89 | 0.0 | 1.55 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.01 | 0.0 | 0.4 | 0.0 | 0.91 | 7.47 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.88 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.43 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.49 | 0.0 | 74.71 | 0.0 | 46.62 | 15.94 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.72 | 0.0 | 1.3 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.74 | 0.0 | 3.34 | 0.0 | 1.47 | 50.77 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.96 | 12.05 | 9.27 | 0.0 | 4.12 | 8.28 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.59 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 7.52 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.86 | 31.82 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.46 | 0.0 | 75.24 | 0.0 | 46.62 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.18 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.84 | 0.0 | 10.51 | 0.0 | 5.38 | 50.4 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.98 | 12.08 | 9.52 | 0.0 | 4.24 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.87 | 0.0 | 1.57 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.92 | 7.66 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.85 | 31.82 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.47 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.42 | 0.0 | 75.34 | 0.0 | 47.39 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.1 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.67 | 0.0 | 10.59 | 0.0 | 5.47 | 50.92 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.97 | 12.07 | 10.4 | 0.0 | 4.14 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.81 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.85 | 31.85 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.42 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.34 | 0.0 | 75.29 | 0.0 | 46.6 | 15.94 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.12 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.8 | 0.0 | 10.52 | 0.0 | 5.34 | 50.76 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.97 | 12.1 | 9.38 | 0.0 | 4.16 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.88 | 0.0 | 1.47 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.93 | 7.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.88 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.75 | 0.0 | 1.49 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.39 | 0.0 | 75.31 | 0.0 | 47.36 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.18 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.75 | 0.0 | 10.37 | 0.0 | 5.7 | 51.2 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.97 | 12.01 | 9.36 | 0.0 | 4.18 | 8.27 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.61 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.37 | 0.0 | 0.93 | 7.41 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.87 | 31.9 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.38 | 8.32 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.4 | 0.0 | 74.71 | 0.0 | 47.12 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.42 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.77 | 0.0 | 10.69 | 0.0 | 5.46 | 50.75 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.0 | 11.96 | 9.65 | 0.0 | 4.3 | 8.28 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.62 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.95 | 7.4 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.91 | 31.82 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.33 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.49 | 0.0 | 74.09 | 0.0 | 46.39 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.17 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.79 | 0.0 | 11.29 | 0.0 | 5.8 | 50.7 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.96 | 12.0 | 9.35 | 0.0 | 4.18 | 8.28 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 2.17 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.97 | 7.55 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.96 | 0.0 | 3.89 | 31.78 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.54 | 0.0 | 74.87 | 0.0 | 46.97 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.29 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.81 | 0.0 | 11.15 | 0.0 | 5.67 | 50.78 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.98 | 12.14 | 9.54 | 0.0 | 4.24 | 8.26 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.61 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.91 | 7.71 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.86 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.49 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.47 | 0.0 | 74.66 | 0.0 | 46.56 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.17 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.68 | 0.0 | 10.4 | 0.0 | 5.36 | 50.68 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.98 | 12.08 | 9.23 | 0.0 | 4.12 | 8.28 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.85 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.69 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.09 | 0.0 | 1.97 | 0.0 | 3.86 | 31.87 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.59 | 0.0 | 75.45 | 0.0 | 47.12 | 16.04 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.13 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.65 | 0.0 | 10.69 | 0.0 | 5.5 | 50.49 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.99 | 12.07 | 9.57 | 0.0 | 4.25 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.03 | 0.0 | 0.87 | 0.0 | 1.6 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.87 | 7.57 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.86 | 31.89 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.47 | 0.0 | 74.53 | 0.0 | 46.2 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.16 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.78 | 0.0 | 10.4 | 0.0 | 5.34 | 51.06 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 1.93 | 11.82 | 9.2 | 0.0 | 4.14 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 0.98 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.88 | 7.39 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | reduce | 0.08 | 0.0 | 1.99 | 0.0 | 3.88 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.4 | 8.32 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | gemv | 15.31 | 0.0 | 74.33 | 0.0 | 46.55 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.07 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | concat | 4.72 | 0.0 | 10.75 | 0.0 | 5.47 | 50.73 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| planner_debate | mir_operator:decode_layer* | True | 92.17 % | profiled | attention | 2.01 | 11.95 | 9.47 | 0.0 | 4.22 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_head | False | 0.66 % | profiled | copy | 0.04 | 0.0 | 0.92 | 0.0 | 1.58 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_head | False | 0.66 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 7.65 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_head | False | 0.66 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.85 | 31.91 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_head | False | 0.66 % | profiled | elementwise_binary | 0.02 | 0.0 | 0.81 | 0.0 | 1.05 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_head | False | 0.66 % | profiled | gemv | 19.89 | 0.0 | 97.04 | 0.0 | 61.42 | 24.49 | 49.46 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_head | False | 0.66 % | profiled | copy | 0.04 | 0.0 | 0.93 | 0.0 | 1.62 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_head | False | 0.66 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.51 | 0.0 | 0.98 | 7.51 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_head | False | 0.66 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.93 | 31.87 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_head | False | 0.66 % | profiled | elementwise_binary | 0.02 | 0.0 | 0.81 | 0.0 | 1.05 | 8.25 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_head | False | 0.66 % | profiled | gemv | 19.9 | 0.0 | 94.57 | 0.0 | 59.77 | 24.48 | 49.46 | DRAM-bandwidth-bound |
| planner_debate | mir_operator:decode_sample | False | 1.66 % | profiled | reduce | 2.83 | 0.0 | 5.31 | 0.0 | 3.02 | 33.13 | 0.05 | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | mir_operator:decode_sample | False | 1.66 % | profiled | reduce | 2.79 | 0.0 | 5.23 | 0.0 | 2.99 | 33.13 | 0.05 | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | pre_d2h_alloc | False | 0.03 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate | d2h_stage | False | 0.0 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate | checksum_complete | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | agent_tool_execute_cpu | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate | iteration_tail_sync | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | dag_schedule_gap | False | 0.01 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | adapter_dispatch | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | token_preprocess_cpu | False | 0.05 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | host_input_generate | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | h2d_stage | False | 0.0 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_moa_mcts | h2d_stage | False | 0.0 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_moa_mcts | weight_init | False | 0.01 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | mir_operator:prefill_embed | False | 0.0 % | profiled | other | 5.81 | 0.0 | 9.84 | 0.0 | 32.09 | 49.89 | 0.67 | underutilised: SM 6 %, DRAM 10 %, L2 32 %, occ 50 % |
| react_moa_mcts | mir_operator:prefill_embed | False | 0.0 % | profiled | other | 4.47 | 0.0 | 11.02 | 0.0 | 25.61 | 37.22 | 0.46 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_embed | False | 0.0 % | profiled | other | 2.9 | 0.0 | 11.53 | 0.0 | 17.07 | 23.79 | 0.27 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | inter_operator_dispatch | False | 3.85 % | not_collected |  |  |  |  |  |  |  |  | no w03 family row |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.29 | 0.0 | 44.95 | 0.0 | 27.91 | 50.6 | 0.83 | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.77 | 0.0 | 25.21 | 0.0 | 11.96 | 14.67 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.41 | 0.0 | 49.85 | 0.0 | 19.26 | 44.82 | 0.34 | underutilised: SM 2 %, DRAM 49 %, L2 18 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.47 | 0.0 | 38.7 | 0.0 | 22.86 | 65.68 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.04 | 41.73 | 31.53 | 0.0 | 66.48 | 13.94 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.61 | 0.0 | 59.19 | 0.0 | 23.36 | 51.19 | 0.67 | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 53 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.39 | 0.0 | 20.27 | 0.0 | 12.42 | 69.86 | 1.33 | underutilised: SM 39 %, DRAM 26 %, L2 16 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.4 | 12.17 | 31.69 | 0.0 | 26.49 | 33.78 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.1 | 0.0 | 45.23 | 0.0 | 27.56 | 50.54 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 32 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.79 | 0.0 | 24.93 | 0.0 | 16.71 | 14.54 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.54 | 0.0 | 50.99 | 0.0 | 20.02 | 44.36 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.6 | 0.0 | 38.87 | 0.0 | 22.85 | 65.44 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.1 | 41.44 | 30.73 | 0.0 | 67.3 | 13.76 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.48 | 0.0 | 59.47 | 0.0 | 23.53 | 51.28 | 0.67 | underutilised: SM 13 %, DRAM 31 %, L2 18 %, occ 56 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 27.6 | 0.0 | 19.89 | 0.0 | 12.32 | 70.12 | 1.33 | underutilised: SM 37 %, DRAM 28 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.46 | 12.01 | 41.38 | 0.0 | 28.19 | 33.7 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.38 | 0.0 | 45.18 | 0.0 | 28.56 | 50.41 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 32 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.77 | 0.0 | 26.18 | 0.0 | 12.49 | 14.51 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.55 | 0.0 | 51.63 | 0.0 | 20.3 | 44.6 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.42 | 0.0 | 39.31 | 0.0 | 22.65 | 65.24 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 38.34 | 41.5 | 31.07 | 0.0 | 67.21 | 13.93 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.6 | 0.0 | 60.73 | 0.0 | 24.1 | 51.07 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.6 | 0.0 | 20.01 | 0.0 | 12.33 | 70.07 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.36 | 12.16 | 41.06 | 0.0 | 27.97 | 33.67 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.42 | 0.0 | 46.13 | 0.0 | 28.04 | 50.53 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.36 | 0.0 | 25.01 | 0.0 | 11.91 | 14.6 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.6 | 0.0 | 51.21 | 0.0 | 20.13 | 44.73 | 0.34 | underutilised: SM 2 %, DRAM 52 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.75 | 0.0 | 38.9 | 0.0 | 23.03 | 65.41 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.19 | 41.7 | 30.85 | 0.0 | 67.16 | 13.83 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.3 | 0.0 | 61.34 | 0.0 | 24.22 | 50.97 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 27.96 | 0.0 | 20.04 | 0.0 | 12.31 | 69.79 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 19 %, occ 75 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.43 | 12.08 | 41.76 | 0.0 | 27.95 | 34.08 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.42 | 0.0 | 45.49 | 0.0 | 28.52 | 50.26 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 32 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.75 | 0.0 | 25.29 | 0.0 | 12.02 | 14.47 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.68 | 0.0 | 50.7 | 0.0 | 19.92 | 44.55 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.18 | 0.0 | 39.07 | 0.0 | 22.96 | 66.12 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.1 | 41.46 | 30.92 | 0.0 | 67.23 | 13.72 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.54 | 0.0 | 58.32 | 0.0 | 23.17 | 51.18 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 56 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.31 | 0.0 | 20.01 | 0.0 | 12.28 | 70.19 | 1.33 | underutilised: SM 40 %, DRAM 28 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.33 | 12.16 | 45.09 | 0.0 | 27.96 | 34.02 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.32 | 0.0 | 45.78 | 0.0 | 28.27 | 50.7 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 65 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.79 | 0.0 | 24.96 | 0.0 | 11.95 | 14.63 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.73 | 0.0 | 50.14 | 0.0 | 19.73 | 44.53 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.56 | 0.0 | 38.73 | 0.0 | 22.47 | 65.77 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.32 | 41.5 | 31.12 | 0.0 | 67.13 | 13.72 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.44 | 0.0 | 60.66 | 0.0 | 23.96 | 50.11 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.38 | 0.0 | 20.19 | 0.0 | 12.29 | 70.09 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.47 | 11.98 | 41.86 | 0.0 | 27.97 | 33.78 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.34 | 0.0 | 44.94 | 0.0 | 28.35 | 50.48 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.76 | 0.0 | 25.45 | 0.0 | 17.94 | 14.36 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.66 | 0.0 | 52.42 | 0.0 | 20.65 | 44.6 | 0.34 | underutilised: SM 2 %, DRAM 52 %, L2 21 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.8 | 0.0 | 39.14 | 0.0 | 22.77 | 65.68 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.19 | 41.77 | 31.4 | 0.0 | 67.1 | 13.84 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.58 | 0.0 | 59.54 | 0.0 | 23.48 | 50.52 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 27.96 | 0.0 | 19.39 | 0.0 | 11.91 | 70.19 | 1.33 | underutilised: SM 38 %, DRAM 28 %, L2 17 %, occ 77 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.49 | 12.27 | 41.48 | 0.0 | 28.01 | 33.79 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.48 | 0.0 | 46.61 | 0.0 | 28.38 | 50.62 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.76 | 0.0 | 25.2 | 0.0 | 11.84 | 14.41 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.52 | 0.0 | 52.24 | 0.0 | 20.53 | 44.59 | 0.34 | underutilised: SM 2 %, DRAM 52 %, L2 21 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.75 | 0.0 | 38.48 | 0.0 | 22.81 | 65.72 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 38.24 | 41.38 | 30.81 | 0.0 | 66.82 | 13.82 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.4 | 0.0 | 59.61 | 0.0 | 23.58 | 50.64 | 0.67 | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 52 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.23 | 0.0 | 19.74 | 0.0 | 12.02 | 70.08 | 1.33 | underutilised: SM 38 %, DRAM 28 %, L2 17 %, occ 77 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.39 | 12.13 | 41.6 | 0.0 | 27.9 | 33.79 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.38 | 0.0 | 44.67 | 0.0 | 28.47 | 50.68 | 0.83 | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 65 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.79 | 0.0 | 25.92 | 0.0 | 12.37 | 14.37 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 3.34 | 0.0 | 51.59 | 0.0 | 20.27 | 44.54 | 0.34 | underutilised: SM 2 %, DRAM 52 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.66 | 0.0 | 38.61 | 0.0 | 22.47 | 65.87 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 38.69 | 41.83 | 31.04 | 0.0 | 67.16 | 13.74 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.69 | 0.0 | 61.02 | 0.0 | 24.12 | 51.07 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 53 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.64 | 0.0 | 19.82 | 0.0 | 12.32 | 70.03 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.42 | 12.16 | 45.02 | 0.0 | 28.13 | 33.91 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.26 | 0.0 | 41.08 | 0.0 | 27.77 | 50.2 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.75 | 0.0 | 26.22 | 0.0 | 20.21 | 14.44 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.5 | 0.0 | 50.24 | 0.0 | 19.73 | 44.74 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.73 | 0.0 | 38.53 | 0.0 | 22.7 | 65.13 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 38.04 | 41.8 | 30.87 | 0.0 | 67.05 | 13.75 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 12.38 | 0.0 | 60.02 | 0.0 | 23.84 | 50.67 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 56 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.02 | 0.0 | 20.22 | 0.0 | 12.38 | 70.16 | 1.33 | underutilised: SM 39 %, DRAM 27 %, L2 16 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.34 | 12.05 | 41.23 | 0.0 | 27.76 | 33.74 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.46 | 0.0 | 45.0 | 0.0 | 28.46 | 50.38 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.79 | 0.0 | 25.27 | 0.0 | 11.98 | 14.47 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.49 | 0.0 | 51.85 | 0.0 | 20.36 | 44.46 | 0.34 | underutilised: SM 2 %, DRAM 52 %, L2 21 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.71 | 0.0 | 38.99 | 0.0 | 22.78 | 65.43 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.22 | 41.18 | 30.66 | 0.0 | 66.97 | 13.89 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 8.96 | 0.0 | 60.74 | 0.0 | 24.02 | 51.72 | 0.67 | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 55 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.63 | 0.0 | 20.17 | 0.0 | 12.28 | 70.1 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.37 | 12.3 | 46.19 | 0.0 | 28.14 | 33.71 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.44 | 0.0 | 45.64 | 0.0 | 28.4 | 50.76 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 32 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.74 | 0.0 | 25.26 | 0.0 | 12.27 | 14.6 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.76 | 0.0 | 49.1 | 0.0 | 19.26 | 44.38 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.41 | 0.0 | 38.77 | 0.0 | 22.9 | 65.87 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.25 | 41.48 | 31.24 | 0.0 | 66.8 | 13.76 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.9 | 0.0 | 58.99 | 0.0 | 23.2 | 50.35 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 55 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.3 | 0.0 | 20.44 | 0.0 | 12.32 | 69.98 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.33 | 12.15 | 46.74 | 0.0 | 27.72 | 33.87 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.04 | 0.0 | 44.92 | 0.0 | 28.04 | 50.56 | 0.83 | underutilised: SM 19 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.75 | 0.0 | 8.61 | 0.0 | 3.73 | 14.41 | 0.15 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.47 | 0.0 | 52.22 | 0.0 | 20.53 | 44.63 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.67 | 0.0 | 38.98 | 0.0 | 22.5 | 65.5 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.09 | 41.69 | 30.99 | 0.0 | 67.21 | 13.93 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.46 | 0.0 | 60.31 | 0.0 | 23.79 | 50.7 | 0.67 | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 56 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.29 | 0.0 | 19.61 | 0.0 | 12.04 | 70.02 | 1.33 | underutilised: SM 40 %, DRAM 29 %, L2 18 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.29 | 12.2 | 42.16 | 0.0 | 27.92 | 33.71 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.42 | 0.0 | 46.72 | 0.0 | 28.22 | 50.62 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.75 | 0.0 | 25.13 | 0.0 | 11.95 | 14.67 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.63 | 0.0 | 50.97 | 0.0 | 20.04 | 44.61 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.73 | 0.0 | 39.59 | 0.0 | 22.46 | 65.77 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.8 | 41.31 | 30.98 | 0.0 | 67.06 | 13.86 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.8 | 0.0 | 59.47 | 0.0 | 23.52 | 50.01 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.91 | 0.0 | 20.33 | 0.0 | 12.41 | 70.35 | 1.33 | underutilised: SM 39 %, DRAM 26 %, L2 16 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.49 | 12.03 | 41.96 | 0.0 | 27.8 | 33.82 | 1.89 | underutilised: SM 18 %, DRAM 20 %, L2 30 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.35 | 0.0 | 46.16 | 0.0 | 28.37 | 50.29 | 0.83 | underutilised: SM 20 %, DRAM 38 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.75 | 0.0 | 25.28 | 0.0 | 12.26 | 14.52 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.45 | 0.0 | 51.6 | 0.0 | 20.26 | 44.4 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.65 | 0.0 | 38.89 | 0.0 | 22.75 | 66.02 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.8 | 41.54 | 30.95 | 0.0 | 67.27 | 13.84 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.7 | 0.0 | 60.81 | 0.0 | 23.99 | 50.77 | 0.67 | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 54 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.29 | 0.0 | 20.0 | 0.0 | 12.25 | 70.44 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.49 | 12.22 | 41.46 | 0.0 | 27.91 | 33.78 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.04 | 0.0 | 44.71 | 0.0 | 28.24 | 50.73 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 65 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.76 | 0.0 | 26.64 | 0.0 | 13.89 | 14.37 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.71 | 0.0 | 50.61 | 0.0 | 19.87 | 44.82 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.3 | 0.0 | 38.4 | 0.0 | 22.63 | 65.52 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.61 | 41.81 | 30.85 | 0.0 | 66.65 | 13.72 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.64 | 0.0 | 59.81 | 0.0 | 23.69 | 50.26 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 53 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.49 | 0.0 | 19.11 | 0.0 | 12.08 | 70.23 | 1.33 | underutilised: SM 37 %, DRAM 29 %, L2 18 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.28 | 12.15 | 46.47 | 0.0 | 27.75 | 34.04 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.23 | 0.0 | 45.06 | 0.0 | 28.35 | 50.56 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.79 | 0.0 | 25.58 | 0.0 | 12.1 | 14.34 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.39 | 0.0 | 50.76 | 0.0 | 19.94 | 44.66 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.17 | 0.0 | 39.38 | 0.0 | 22.66 | 65.8 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.24 | 41.39 | 30.65 | 0.0 | 66.92 | 13.74 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.68 | 0.0 | 60.32 | 0.0 | 23.77 | 50.75 | 0.67 | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 55 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.38 | 0.0 | 20.62 | 0.0 | 12.31 | 69.9 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.41 | 12.2 | 41.62 | 0.0 | 28.3 | 33.74 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.46 | 0.0 | 45.24 | 0.0 | 28.07 | 50.74 | 0.83 | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 63 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.73 | 0.0 | 25.18 | 0.0 | 11.94 | 14.55 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.56 | 0.0 | 50.61 | 0.0 | 19.85 | 44.25 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.36 | 0.0 | 37.98 | 0.0 | 22.57 | 65.63 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.16 | 41.51 | 31.05 | 0.0 | 67.7 | 13.75 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.82 | 0.0 | 60.23 | 0.0 | 23.82 | 50.62 | 0.67 | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 56 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.29 | 0.0 | 20.02 | 0.0 | 12.24 | 70.25 | 1.33 | underutilised: SM 39 %, DRAM 27 %, L2 16 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.41 | 12.02 | 46.56 | 0.0 | 27.71 | 33.8 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.34 | 0.0 | 44.91 | 0.0 | 28.22 | 50.68 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.8 | 0.0 | 8.11 | 0.0 | 3.58 | 14.69 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.67 | 0.0 | 49.9 | 0.0 | 19.57 | 44.54 | 0.34 | underutilised: SM 2 %, DRAM 49 %, L2 19 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.4 | 0.0 | 38.87 | 0.0 | 22.95 | 65.4 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.5 | 41.88 | 30.79 | 0.0 | 66.9 | 13.88 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.61 | 0.0 | 60.31 | 0.0 | 23.86 | 50.98 | 0.67 | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 54 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.19 | 0.0 | 19.89 | 0.0 | 12.35 | 70.32 | 1.33 | underutilised: SM 40 %, DRAM 29 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.19 | 12.27 | 47.08 | 0.0 | 27.69 | 33.78 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.42 | 0.0 | 45.11 | 0.0 | 28.38 | 50.16 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.75 | 0.0 | 26.22 | 0.0 | 12.53 | 14.48 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.75 | 0.0 | 49.66 | 0.0 | 19.49 | 44.42 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.3 | 0.0 | 38.2 | 0.0 | 22.69 | 65.8 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.05 | 41.45 | 30.84 | 0.0 | 67.05 | 13.79 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.86 | 0.0 | 61.17 | 0.0 | 24.28 | 50.82 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.4 | 0.0 | 20.15 | 0.0 | 12.3 | 70.01 | 1.33 | underutilised: SM 40 %, DRAM 26 %, L2 16 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.4 | 12.09 | 44.75 | 0.0 | 27.99 | 25.85 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 7.28 | 0.0 | 45.77 | 0.0 | 28.56 | 50.65 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.75 | 0.0 | 25.28 | 0.0 | 12.12 | 14.48 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.47 | 0.0 | 52.08 | 0.0 | 20.46 | 44.52 | 0.34 | underutilised: SM 2 %, DRAM 53 %, L2 21 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.72 | 0.0 | 39.64 | 0.0 | 22.7 | 65.7 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 38.33 | 41.59 | 30.82 | 0.0 | 67.31 | 13.75 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.64 | 0.0 | 58.92 | 0.0 | 23.25 | 51.06 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 56 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.46 | 0.0 | 20.15 | 0.0 | 12.28 | 70.21 | 1.33 | underutilised: SM 40 %, DRAM 27 %, L2 16 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.42 | 12.18 | 46.67 | 0.0 | 27.97 | 33.72 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.41 | 0.0 | 45.03 | 0.0 | 28.18 | 50.55 | 0.83 | underutilised: SM 20 %, DRAM 36 %, L2 33 %, occ 65 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.74 | 0.0 | 26.54 | 0.0 | 12.57 | 14.46 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.46 | 0.0 | 50.34 | 0.0 | 19.74 | 44.58 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.85 | 0.0 | 38.48 | 0.0 | 22.57 | 65.64 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.36 | 41.84 | 30.72 | 0.0 | 66.95 | 13.76 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.27 | 0.0 | 60.41 | 0.0 | 23.86 | 50.95 | 0.67 | underutilised: SM 13 %, DRAM 31 %, L2 19 %, occ 55 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.81 | 0.0 | 19.98 | 0.0 | 12.17 | 70.25 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 77 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.32 | 12.02 | 41.84 | 0.0 | 27.8 | 33.66 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.1 | 0.0 | 45.31 | 0.0 | 27.43 | 50.63 | 0.83 | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.78 | 0.0 | 25.11 | 0.0 | 11.95 | 14.42 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.47 | 0.0 | 50.96 | 0.0 | 20.04 | 44.55 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.36 | 0.0 | 38.71 | 0.0 | 22.47 | 65.1 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.39 | 41.39 | 31.07 | 0.0 | 67.12 | 13.75 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.12 | 0.0 | 61.31 | 0.0 | 24.28 | 51.02 | 0.67 | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 56 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.51 | 0.0 | 20.18 | 0.0 | 12.35 | 70.05 | 1.33 | underutilised: SM 39 %, DRAM 27 %, L2 16 %, occ 77 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.46 | 12.27 | 41.55 | 0.0 | 28.0 | 33.77 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 30 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 7.87 | 0.0 | 46.55 | 0.0 | 28.33 | 50.27 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.75 | 0.0 | 25.32 | 0.0 | 12.08 | 14.46 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.71 | 0.0 | 49.78 | 0.0 | 19.53 | 44.4 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.67 | 0.0 | 38.73 | 0.0 | 22.56 | 65.61 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.12 | 41.62 | 30.9 | 0.0 | 66.99 | 13.75 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.65 | 0.0 | 59.57 | 0.0 | 23.59 | 50.8 | 0.67 | underutilised: SM 14 %, DRAM 31 %, L2 19 %, occ 56 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.55 | 0.0 | 19.6 | 0.0 | 12.07 | 70.11 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.42 | 11.98 | 40.96 | 0.0 | 27.6 | 33.61 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.42 | 0.0 | 45.72 | 0.0 | 28.52 | 49.72 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.75 | 0.0 | 26.45 | 0.0 | 12.37 | 14.65 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.53 | 0.0 | 50.36 | 0.0 | 19.79 | 44.58 | 0.34 | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.55 | 0.0 | 38.47 | 0.0 | 22.63 | 65.59 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.77 | 41.89 | 30.96 | 0.0 | 67.46 | 13.8 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.51 | 0.0 | 58.87 | 0.0 | 23.34 | 51.53 | 0.67 | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.36 | 0.0 | 20.11 | 0.0 | 12.38 | 70.23 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.3 | 12.16 | 46.49 | 0.0 | 27.89 | 33.64 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.44 | 0.0 | 45.41 | 0.0 | 28.4 | 50.14 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 63 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.75 | 0.0 | 24.82 | 0.0 | 11.81 | 14.42 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.66 | 0.0 | 50.95 | 0.0 | 20.04 | 44.54 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.65 | 0.0 | 38.97 | 0.0 | 22.38 | 65.84 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.36 | 41.41 | 31.05 | 0.0 | 66.81 | 14.01 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.18 | 0.0 | 61.02 | 0.0 | 24.12 | 51.04 | 0.67 | underutilised: SM 13 %, DRAM 31 %, L2 18 %, occ 56 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.48 | 0.0 | 19.94 | 0.0 | 12.35 | 70.23 | 1.33 | underutilised: SM 39 %, DRAM 27 %, L2 16 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.27 | 12.13 | 45.38 | 0.0 | 27.78 | 33.77 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.05 | 0.0 | 43.71 | 0.0 | 28.32 | 50.6 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 63 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.8 | 0.0 | 8.44 | 0.0 | 3.67 | 14.44 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.65 | 0.0 | 51.13 | 0.0 | 20.08 | 44.64 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.84 | 0.0 | 38.93 | 0.0 | 22.91 | 65.47 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 37.16 | 41.66 | 31.0 | 0.0 | 67.01 | 13.81 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.0 | 0.0 | 60.36 | 0.0 | 23.78 | 50.11 | 0.67 | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 56 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.59 | 0.0 | 20.17 | 0.0 | 12.29 | 70.27 | 1.33 | underutilised: SM 39 %, DRAM 28 %, L2 17 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.46 | 12.19 | 45.42 | 0.0 | 27.89 | 33.79 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 8.48 | 0.0 | 45.35 | 0.0 | 28.22 | 50.66 | 0.83 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.75 | 0.0 | 25.02 | 0.0 | 11.87 | 14.35 | 0.15 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 6.47 | 0.0 | 50.78 | 0.0 | 19.94 | 44.65 | 0.34 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 16.41 | 0.0 | 38.74 | 0.0 | 22.75 | 65.4 | 1.17 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 38.11 | 41.97 | 30.91 | 0.0 | 66.97 | 13.74 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 13.77 | 0.0 | 59.8 | 0.0 | 23.64 | 50.58 | 0.67 | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 55 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 28.85 | 0.0 | 20.16 | 0.0 | 12.23 | 70.0 | 1.33 | underutilised: SM 40 %, DRAM 28 %, L2 18 %, occ 76 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 22.22 | 12.14 | 45.11 | 0.0 | 27.81 | 34.01 | 1.89 | underutilised: SM 18 %, DRAM 19 %, L2 29 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.33 | 0.0 | 37.65 | 0.0 | 24.14 | 35.29 | 0.5 | underutilised: SM 17 %, DRAM 33 %, L2 31 %, occ 68 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.64 | 0.0 | 20.53 | 0.0 | 9.97 | 11.84 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 27 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.69 | 0.0 | 40.62 | 0.0 | 15.96 | 45.41 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.32 | 0.0 | 35.0 | 0.0 | 20.74 | 65.75 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.75 | 39.73 | 36.11 | 0.0 | 65.23 | 14.26 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.71 | 0.0 | 54.92 | 0.0 | 21.69 | 36.68 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.36 | 0.0 | 14.78 | 0.0 | 9.35 | 70.79 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.19 | 8.98 | 42.19 | 0.0 | 25.55 | 33.41 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 25 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.21 | 0.0 | 37.69 | 0.0 | 24.03 | 35.04 | 0.5 | underutilised: SM 18 %, DRAM 33 %, L2 31 %, occ 68 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.53 | 0.0 | 9.98 | 12.1 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.74 | 0.0 | 41.36 | 0.0 | 16.24 | 45.44 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.18 | 0.0 | 36.1 | 0.0 | 20.78 | 66.53 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.75 | 39.83 | 36.05 | 0.0 | 65.01 | 14.17 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.72 | 0.0 | 52.66 | 0.0 | 20.85 | 36.51 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.51 | 0.0 | 15.67 | 0.0 | 9.71 | 70.92 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.17 | 8.84 | 42.14 | 0.0 | 25.81 | 33.37 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.39 | 0.0 | 38.62 | 0.0 | 23.6 | 35.11 | 0.5 | underutilised: SM 18 %, DRAM 32 %, L2 31 %, occ 67 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.61 | 0.0 | 20.54 | 0.0 | 10.08 | 12.05 | 0.1 | underutilised: SM 2 %, DRAM 59 %, L2 27 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.57 | 0.0 | 40.65 | 0.0 | 15.92 | 45.03 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.47 | 0.0 | 35.8 | 0.0 | 20.86 | 66.74 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.22 | 39.38 | 35.88 | 0.0 | 65.58 | 14.18 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.55 | 0.0 | 53.72 | 0.0 | 21.24 | 36.5 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.66 | 0.0 | 15.65 | 0.0 | 9.76 | 71.17 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.08 | 8.82 | 42.44 | 0.0 | 25.45 | 33.33 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.31 | 0.0 | 37.69 | 0.0 | 23.89 | 35.13 | 0.5 | underutilised: SM 19 %, DRAM 30 %, L2 29 %, occ 69 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.6 | 0.0 | 20.82 | 0.0 | 10.24 | 11.86 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.79 | 0.0 | 41.51 | 0.0 | 16.26 | 45.41 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.15 | 0.0 | 35.62 | 0.0 | 20.47 | 66.79 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.67 | 38.1 | 35.69 | 0.0 | 66.28 | 14.16 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 10.06 | 0.0 | 54.29 | 0.0 | 21.46 | 36.35 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.17 | 0.0 | 15.67 | 0.0 | 9.7 | 71.06 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.27 | 8.78 | 42.52 | 0.0 | 25.61 | 33.35 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.33 | 0.0 | 38.03 | 0.0 | 24.06 | 34.76 | 0.5 | underutilised: SM 19 %, DRAM 31 %, L2 30 %, occ 69 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.41 | 0.0 | 11.19 | 12.02 | 0.1 | underutilised: SM 2 %, DRAM 58 %, L2 26 %, occ 27 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.7 | 0.0 | 39.61 | 0.0 | 15.54 | 45.21 | 0.46 | underutilised: SM 1 %, DRAM 34 %, L2 13 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.34 | 0.0 | 35.18 | 0.0 | 20.49 | 66.68 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.96 | 40.01 | 36.05 | 0.0 | 65.1 | 14.21 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.72 | 0.0 | 53.89 | 0.0 | 21.31 | 36.24 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 24.7 | 0.0 | 15.78 | 0.0 | 9.75 | 70.64 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.18 | 8.83 | 41.82 | 0.0 | 25.6 | 33.18 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.34 | 0.0 | 36.79 | 0.0 | 23.99 | 34.72 | 0.5 | underutilised: SM 18 %, DRAM 32 %, L2 31 %, occ 69 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.66 | 0.0 | 20.77 | 0.0 | 11.14 | 11.99 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.94 | 0.0 | 40.14 | 0.0 | 15.71 | 45.41 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.32 | 0.0 | 35.74 | 0.0 | 20.77 | 66.77 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.24 | 40.19 | 36.22 | 0.0 | 66.17 | 14.23 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.67 | 0.0 | 53.71 | 0.0 | 21.19 | 36.8 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.28 | 0.0 | 16.03 | 0.0 | 9.66 | 70.97 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 13 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.09 | 8.94 | 42.54 | 0.0 | 25.65 | 33.2 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 25 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.25 | 0.0 | 38.56 | 0.0 | 24.45 | 34.94 | 0.5 | underutilised: SM 19 %, DRAM 31 %, L2 29 %, occ 67 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.64 | 0.0 | 21.94 | 0.0 | 10.61 | 11.9 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 27 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.59 | 0.0 | 40.27 | 0.0 | 15.79 | 44.45 | 0.46 | underutilised: SM 1 %, DRAM 32 %, L2 13 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.25 | 0.0 | 36.56 | 0.0 | 20.49 | 66.86 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.69 | 39.88 | 36.34 | 0.0 | 66.41 | 14.23 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.66 | 0.0 | 45.17 | 0.0 | 17.81 | 36.93 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.2 | 0.0 | 15.58 | 0.0 | 9.69 | 70.36 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.13 | 8.91 | 42.55 | 0.0 | 25.66 | 33.42 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.27 | 0.0 | 38.17 | 0.0 | 23.85 | 35.27 | 0.5 | underutilised: SM 18 %, DRAM 31 %, L2 30 %, occ 69 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.82 | 0.0 | 10.16 | 12.15 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.7 | 0.0 | 40.62 | 0.0 | 15.94 | 45.43 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.5 | 0.0 | 35.68 | 0.0 | 20.82 | 66.45 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.79 | 39.71 | 36.09 | 0.0 | 65.77 | 14.14 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.91 | 0.0 | 54.28 | 0.0 | 21.5 | 36.17 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.5 | 0.0 | 15.64 | 0.0 | 9.75 | 70.75 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 13 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.15 | 8.8 | 42.28 | 0.0 | 25.83 | 33.12 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 5.92 | 0.0 | 38.4 | 0.0 | 23.95 | 34.87 | 0.5 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 67 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.61 | 0.0 | 20.37 | 0.0 | 9.95 | 11.95 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.61 | 0.0 | 41.41 | 0.0 | 16.24 | 45.1 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 12.95 | 0.0 | 35.89 | 0.0 | 20.57 | 65.96 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.11 | 37.31 | 35.9 | 0.0 | 64.86 | 14.2 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.7 | 0.0 | 55.5 | 0.0 | 21.98 | 36.5 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.42 | 0.0 | 15.8 | 0.0 | 9.69 | 71.74 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.28 | 8.91 | 42.3 | 0.0 | 25.62 | 33.51 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.33 | 0.0 | 38.42 | 0.0 | 23.13 | 34.95 | 0.5 | underutilised: SM 17 %, DRAM 33 %, L2 31 %, occ 68 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.72 | 0.0 | 10.08 | 11.96 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.7 | 0.0 | 39.59 | 0.0 | 15.54 | 45.4 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.16 | 0.0 | 35.95 | 0.0 | 20.8 | 66.93 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.86 | 39.34 | 36.09 | 0.0 | 66.08 | 14.23 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.92 | 0.0 | 54.9 | 0.0 | 21.72 | 36.26 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.4 | 0.0 | 15.51 | 0.0 | 9.61 | 71.16 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.28 | 8.76 | 42.41 | 0.0 | 25.75 | 33.14 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.36 | 0.0 | 37.97 | 0.0 | 23.96 | 34.73 | 0.5 | underutilised: SM 18 %, DRAM 31 %, L2 30 %, occ 69 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.61 | 0.0 | 20.79 | 0.0 | 10.02 | 11.99 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.62 | 0.0 | 39.97 | 0.0 | 15.72 | 45.22 | 0.46 | underutilised: SM 1 %, DRAM 34 %, L2 15 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.6 | 0.0 | 35.34 | 0.0 | 21.04 | 65.72 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.37 | 40.05 | 35.88 | 0.0 | 65.69 | 14.19 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.94 | 0.0 | 53.69 | 0.0 | 21.2 | 36.62 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.59 | 0.0 | 15.56 | 0.0 | 9.69 | 70.9 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 13 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.18 | 8.9 | 42.36 | 0.0 | 25.72 | 33.27 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.12 | 0.0 | 37.43 | 0.0 | 24.01 | 35.34 | 0.5 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 67 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.61 | 0.0 | 20.73 | 0.0 | 10.1 | 11.97 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 25 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.55 | 0.0 | 40.79 | 0.0 | 16.02 | 45.39 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 12.89 | 0.0 | 34.74 | 0.0 | 20.44 | 66.93 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.11 | 40.02 | 36.02 | 0.0 | 65.67 | 14.16 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.84 | 0.0 | 54.06 | 0.0 | 21.38 | 36.81 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.41 | 0.0 | 16.02 | 0.0 | 10.2 | 70.77 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.12 | 8.68 | 42.24 | 0.0 | 25.59 | 33.24 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.21 | 0.0 | 37.63 | 0.0 | 23.92 | 35.25 | 0.5 | underutilised: SM 19 %, DRAM 32 %, L2 31 %, occ 69 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.51 | 0.0 | 10.0 | 12.01 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.66 | 0.0 | 40.44 | 0.0 | 15.87 | 45.17 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.63 | 0.0 | 35.74 | 0.0 | 20.67 | 66.52 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.84 | 39.55 | 35.85 | 0.0 | 65.72 | 14.2 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.74 | 0.0 | 54.63 | 0.0 | 21.55 | 36.62 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.48 | 0.0 | 15.72 | 0.0 | 9.71 | 71.05 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.23 | 8.99 | 42.16 | 0.0 | 25.69 | 33.18 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.37 | 0.0 | 38.48 | 0.0 | 23.84 | 34.92 | 0.5 | underutilised: SM 18 %, DRAM 31 %, L2 29 %, occ 68 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.97 | 0.0 | 10.22 | 12.14 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 25 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.56 | 0.0 | 41.51 | 0.0 | 16.84 | 45.48 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.23 | 0.0 | 35.6 | 0.0 | 20.35 | 66.78 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.83 | 37.75 | 36.17 | 0.0 | 65.83 | 14.44 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.67 | 0.0 | 54.33 | 0.0 | 21.57 | 36.21 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.74 | 0.0 | 15.65 | 0.0 | 9.75 | 70.96 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.11 | 8.85 | 42.1 | 0.0 | 25.83 | 33.06 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.33 | 0.0 | 38.05 | 0.0 | 24.07 | 34.71 | 0.5 | underutilised: SM 18 %, DRAM 33 %, L2 31 %, occ 68 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.61 | 0.0 | 9.98 | 11.89 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.6 | 0.0 | 41.57 | 0.0 | 16.34 | 45.05 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.43 | 0.0 | 36.68 | 0.0 | 20.68 | 66.7 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.96 | 39.68 | 36.51 | 0.0 | 66.68 | 14.21 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.78 | 0.0 | 54.28 | 0.0 | 21.47 | 36.44 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.52 | 0.0 | 15.46 | 0.0 | 9.63 | 70.96 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 13 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.06 | 8.79 | 42.26 | 0.0 | 25.98 | 33.45 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.25 | 0.0 | 38.82 | 0.0 | 24.08 | 35.15 | 0.5 | underutilised: SM 18 %, DRAM 31 %, L2 29 %, occ 69 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.6 | 0.0 | 10.08 | 12.11 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.77 | 0.0 | 40.14 | 0.0 | 15.75 | 45.45 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.1 | 0.0 | 35.08 | 0.0 | 20.56 | 66.66 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.15 | 38.21 | 35.95 | 0.0 | 65.72 | 14.44 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.82 | 0.0 | 54.15 | 0.0 | 21.37 | 36.41 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.12 | 0.0 | 15.39 | 0.0 | 9.55 | 70.85 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.14 | 8.81 | 42.65 | 0.0 | 25.66 | 33.19 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.26 | 0.0 | 37.92 | 0.0 | 24.19 | 35.02 | 0.5 | underutilised: SM 17 %, DRAM 33 %, L2 31 %, occ 68 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.59 | 0.0 | 19.56 | 0.0 | 9.53 | 11.94 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.89 | 0.0 | 40.37 | 0.0 | 15.82 | 45.14 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.14 | 0.0 | 36.27 | 0.0 | 21.12 | 66.14 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.93 | 39.82 | 35.74 | 0.0 | 65.46 | 14.13 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.82 | 0.0 | 55.17 | 0.0 | 21.81 | 36.33 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 24.81 | 0.0 | 15.67 | 0.0 | 9.71 | 70.82 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.36 | 8.69 | 42.45 | 0.0 | 25.48 | 33.17 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.3 | 0.0 | 37.35 | 0.0 | 23.93 | 34.74 | 0.5 | underutilised: SM 18 %, DRAM 31 %, L2 30 %, occ 68 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.67 | 0.0 | 10.08 | 11.91 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.57 | 0.0 | 41.05 | 0.0 | 16.15 | 45.28 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.08 | 0.0 | 36.17 | 0.0 | 20.85 | 66.69 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.01 | 40.02 | 35.9 | 0.0 | 66.5 | 14.19 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 10.05 | 0.0 | 53.41 | 0.0 | 21.11 | 36.71 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.46 | 0.0 | 15.5 | 0.0 | 9.58 | 71.04 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.16 | 8.72 | 41.27 | 0.0 | 24.72 | 32.86 | 1.42 | underutilised: SM 11 %, DRAM 6 %, L2 6 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.21 | 0.0 | 37.35 | 0.0 | 23.97 | 35.21 | 0.5 | underutilised: SM 19 %, DRAM 32 %, L2 30 %, occ 66 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.63 | 0.0 | 20.56 | 0.0 | 12.26 | 11.83 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.55 | 0.0 | 40.97 | 0.0 | 16.11 | 45.17 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 12.93 | 0.0 | 35.2 | 0.0 | 21.03 | 66.38 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.98 | 39.57 | 35.76 | 0.0 | 65.87 | 14.18 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.63 | 0.0 | 54.37 | 0.0 | 21.49 | 37.04 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.12 | 0.0 | 16.14 | 0.0 | 9.72 | 70.99 | 1.33 | underutilised: SM 32 %, DRAM 22 %, L2 14 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.33 | 8.9 | 42.16 | 0.0 | 25.78 | 33.15 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.14 | 0.0 | 37.87 | 0.0 | 24.15 | 34.85 | 0.5 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 67 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.77 | 0.0 | 10.08 | 11.95 | 0.1 | underutilised: SM 2 %, DRAM 58 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.87 | 0.0 | 39.0 | 0.0 | 15.32 | 45.47 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.4 | 0.0 | 36.06 | 0.0 | 21.11 | 66.9 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.01 | 38.36 | 36.1 | 0.0 | 65.7 | 14.26 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.91 | 0.0 | 54.23 | 0.0 | 21.41 | 36.64 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.45 | 0.0 | 15.13 | 0.0 | 9.38 | 71.01 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.27 | 8.94 | 39.25 | 0.0 | 25.53 | 33.33 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.38 | 0.0 | 37.44 | 0.0 | 23.95 | 34.64 | 0.5 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 68 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.6 | 0.0 | 20.5 | 0.0 | 10.07 | 11.89 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 27 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.95 | 0.0 | 40.29 | 0.0 | 15.82 | 45.13 | 0.46 | underutilised: SM 1 %, DRAM 38 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.2 | 0.0 | 35.57 | 0.0 | 20.34 | 66.97 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.31 | 39.38 | 35.84 | 0.0 | 66.2 | 14.14 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.87 | 0.0 | 54.64 | 0.0 | 21.56 | 36.61 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.36 | 0.0 | 15.67 | 0.0 | 9.77 | 70.96 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.06 | 8.74 | 42.59 | 0.0 | 25.43 | 33.45 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 25 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.28 | 0.0 | 38.73 | 0.0 | 23.93 | 35.02 | 0.5 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 67 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.19 | 0.0 | 20.8 | 0.0 | 10.03 | 12.09 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.57 | 0.0 | 40.88 | 0.0 | 16.01 | 45.43 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.27 | 0.0 | 36.13 | 0.0 | 20.8 | 66.05 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.79 | 39.88 | 36.11 | 0.0 | 65.55 | 14.21 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.75 | 0.0 | 53.59 | 0.0 | 21.2 | 36.88 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.53 | 0.0 | 15.95 | 0.0 | 9.71 | 70.96 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.16 | 8.77 | 42.58 | 0.0 | 25.73 | 33.18 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 25 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.31 | 0.0 | 38.72 | 0.0 | 24.2 | 35.24 | 0.5 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 68 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.62 | 0.0 | 20.65 | 0.0 | 10.01 | 11.85 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.6 | 0.0 | 40.1 | 0.0 | 15.74 | 45.04 | 0.46 | underutilised: SM 1 %, DRAM 33 %, L2 13 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.07 | 0.0 | 35.68 | 0.0 | 20.62 | 66.62 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.03 | 39.96 | 36.41 | 0.0 | 66.08 | 14.19 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.73 | 0.0 | 54.27 | 0.0 | 21.39 | 36.56 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.48 | 0.0 | 15.55 | 0.0 | 9.6 | 70.72 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.18 | 8.85 | 42.59 | 0.0 | 25.66 | 33.55 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.31 | 0.0 | 37.8 | 0.0 | 23.79 | 35.21 | 0.5 | underutilised: SM 19 %, DRAM 32 %, L2 30 %, occ 68 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.61 | 0.0 | 20.53 | 0.0 | 9.94 | 12.1 | 0.1 | underutilised: SM 2 %, DRAM 55 %, L2 25 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.6 | 0.0 | 41.05 | 0.0 | 16.14 | 45.47 | 0.46 | underutilised: SM 1 %, DRAM 34 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.44 | 0.0 | 36.21 | 0.0 | 20.75 | 65.99 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.71 | 39.69 | 36.59 | 0.0 | 66.35 | 14.16 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.83 | 0.0 | 54.24 | 0.0 | 21.37 | 36.83 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.4 | 0.0 | 15.65 | 0.0 | 9.8 | 70.86 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.15 | 8.71 | 42.14 | 0.0 | 25.64 | 33.12 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.35 | 0.0 | 35.27 | 0.0 | 23.92 | 35.06 | 0.5 | underutilised: SM 18 %, DRAM 30 %, L2 29 %, occ 69 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.6 | 0.0 | 21.29 | 0.0 | 10.34 | 11.78 | 0.1 | underutilised: SM 2 %, DRAM 59 %, L2 27 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.68 | 0.0 | 40.93 | 0.0 | 16.04 | 45.22 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.38 | 0.0 | 36.25 | 0.0 | 20.95 | 66.53 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.05 | 39.87 | 35.56 | 0.0 | 64.58 | 14.24 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.9 | 0.0 | 45.5 | 0.0 | 18.06 | 36.38 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.43 | 0.0 | 15.93 | 0.0 | 9.65 | 70.5 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.17 | 9.02 | 42.42 | 0.0 | 25.81 | 33.45 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.34 | 0.0 | 38.12 | 0.0 | 24.09 | 34.85 | 0.5 | underutilised: SM 19 %, DRAM 32 %, L2 31 %, occ 69 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.65 | 0.0 | 21.87 | 0.0 | 10.69 | 12.12 | 0.1 | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.69 | 0.0 | 40.82 | 0.0 | 15.63 | 45.44 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.5 | 0.0 | 35.31 | 0.0 | 20.66 | 66.1 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.04 | 39.99 | 36.3 | 0.0 | 65.78 | 14.14 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.85 | 0.0 | 53.1 | 0.0 | 20.95 | 36.39 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.56 | 0.0 | 15.98 | 0.0 | 9.68 | 70.84 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.23 | 8.94 | 42.68 | 0.0 | 25.69 | 33.12 | 1.42 | underutilised: SM 11 %, DRAM 16 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.32 | 0.0 | 37.97 | 0.0 | 24.12 | 34.94 | 0.5 | underutilised: SM 17 %, DRAM 33 %, L2 31 %, occ 67 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.57 | 0.0 | 20.75 | 0.0 | 10.03 | 11.87 | 0.1 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 27 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.94 | 0.0 | 40.19 | 0.0 | 15.78 | 45.08 | 0.46 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.63 | 0.0 | 35.68 | 0.0 | 20.82 | 66.33 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 31.1 | 40.03 | 35.64 | 0.0 | 64.91 | 14.12 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 9.81 | 0.0 | 54.53 | 0.0 | 21.49 | 36.74 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.49 | 0.0 | 15.83 | 0.0 | 9.72 | 70.88 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 17.87 | 8.88 | 42.6 | 0.0 | 25.87 | 33.33 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 26 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 6.13 | 0.0 | 37.46 | 0.0 | 24.04 | 35.07 | 0.5 | underutilised: SM 19 %, DRAM 32 %, L2 31 %, occ 66 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.6 | 0.0 | 20.74 | 0.0 | 10.1 | 11.99 | 0.1 | underutilised: SM 2 %, DRAM 58 %, L2 26 %, occ 28 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.72 | 0.0 | 41.14 | 0.0 | 16.15 | 45.39 | 0.46 | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 13.16 | 0.0 | 35.28 | 0.0 | 20.67 | 66.76 | 0.83 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 30.94 | 39.41 | 36.47 | 0.0 | 66.29 | 14.14 | 1.5 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 10.01 | 0.0 | 53.9 | 0.0 | 21.24 | 36.45 | 0.5 | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 25.51 | 0.0 | 15.7 | 0.0 | 9.55 | 64.29 | 1.33 | underutilised: SM 33 %, DRAM 22 %, L2 14 %, occ 82 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 18.28 | 8.79 | 42.35 | 0.0 | 25.68 | 33.27 | 1.42 | underutilised: SM 11 %, DRAM 17 %, L2 25 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 3.99 | 0.0 | 28.07 | 0.0 | 18.88 | 22.25 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.43 | 0.0 | 15.47 | 0.0 | 11.39 | 9.6 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.09 | 0.0 | 35.9 | 0.0 | 14.16 | 49.29 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.15 | 0.0 | 24.34 | 0.0 | 14.46 | 42.9 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.07 | 36.93 | 49.5 | 0.0 | 67.39 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.09 | 0.0 | 40.48 | 0.0 | 16.05 | 22.77 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.11 | 0.0 | 10.91 | 0.0 | 7.18 | 73.94 | 1.33 | underutilised: SM 29 %, DRAM 18 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.69 | 8.1 | 32.37 | 0.0 | 18.71 | 25.28 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.11 | 0.0 | 27.12 | 0.0 | 18.98 | 22.1 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.47 | 0.0 | 14.55 | 0.0 | 11.24 | 9.35 | 0.06 | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.54 | 0.0 | 34.83 | 0.0 | 13.74 | 49.14 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.75 | 0.0 | 23.86 | 0.0 | 14.48 | 42.95 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.12 | 36.88 | 49.85 | 0.0 | 67.72 | 8.33 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 5.99 | 0.0 | 40.47 | 0.0 | 15.77 | 22.78 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.7 | 0.0 | 11.15 | 0.0 | 7.16 | 73.8 | 1.33 | underutilised: SM 31 %, DRAM 17 %, L2 11 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.68 | 8.23 | 31.75 | 0.0 | 18.66 | 25.25 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.09 | 0.0 | 27.35 | 0.0 | 18.96 | 22.17 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.44 | 0.0 | 14.75 | 0.0 | 7.41 | 9.4 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.17 | 0.0 | 34.9 | 0.0 | 13.73 | 49.29 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.54 | 0.0 | 24.51 | 0.0 | 13.78 | 43.06 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.04 | 36.85 | 50.38 | 0.0 | 67.4 | 8.33 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.07 | 0.0 | 42.67 | 0.0 | 16.84 | 22.69 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.68 | 0.0 | 10.95 | 0.0 | 7.05 | 73.68 | 1.33 | underutilised: SM 30 %, DRAM 16 %, L2 10 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.71 | 8.13 | 32.43 | 0.0 | 18.98 | 25.14 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.1 | 0.0 | 27.11 | 0.0 | 18.7 | 22.24 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.44 | 0.0 | 14.84 | 0.0 | 7.4 | 9.48 | 0.06 | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.14 | 0.0 | 34.17 | 0.0 | 13.5 | 49.11 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.87 | 0.0 | 23.61 | 0.0 | 14.42 | 43.1 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.44 | 37.23 | 49.98 | 0.0 | 67.19 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.07 | 0.0 | 40.37 | 0.0 | 15.97 | 22.85 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.64 | 0.0 | 10.96 | 0.0 | 7.22 | 73.89 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.68 | 8.08 | 31.52 | 0.0 | 18.56 | 25.22 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.11 | 0.0 | 26.91 | 0.0 | 19.0 | 22.27 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.44 | 0.0 | 15.63 | 0.0 | 7.92 | 9.55 | 0.06 | underutilised: SM 1 %, DRAM 46 %, L2 22 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 7.08 | 0.0 | 34.35 | 0.0 | 13.55 | 49.0 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.67 | 0.0 | 23.12 | 0.0 | 14.58 | 43.54 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.5 | 36.99 | 49.77 | 0.0 | 66.8 | 8.33 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.2 | 0.0 | 40.8 | 0.0 | 16.02 | 22.68 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.49 | 0.0 | 10.91 | 0.0 | 7.18 | 73.58 | 1.33 | underutilised: SM 31 %, DRAM 17 %, L2 11 %, occ 85 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.75 | 8.22 | 31.86 | 0.0 | 18.68 | 25.41 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.1 | 0.0 | 28.07 | 0.0 | 18.92 | 22.1 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.44 | 0.0 | 14.63 | 0.0 | 7.49 | 9.59 | 0.06 | underutilised: SM 1 %, DRAM 43 %, L2 20 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.88 | 0.0 | 34.52 | 0.0 | 13.6 | 49.1 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.63 | 0.0 | 23.42 | 0.0 | 14.82 | 43.31 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.01 | 36.95 | 49.54 | 0.0 | 67.71 | 8.33 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 5.99 | 0.0 | 40.05 | 0.0 | 17.43 | 22.89 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.79 | 0.0 | 11.09 | 0.0 | 7.14 | 73.81 | 1.33 | underutilised: SM 30 %, DRAM 16 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.69 | 8.39 | 32.01 | 0.0 | 18.7 | 25.21 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.0 | 0.0 | 27.94 | 0.0 | 18.92 | 22.45 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.46 | 0.0 | 15.19 | 0.0 | 7.98 | 9.28 | 0.06 | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.5 | 0.0 | 34.77 | 0.0 | 13.71 | 49.14 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.52 | 0.0 | 23.68 | 0.0 | 14.32 | 43.02 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.61 | 36.85 | 50.19 | 0.0 | 67.52 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.14 | 0.0 | 41.12 | 0.0 | 16.23 | 22.83 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.06 | 0.0 | 10.96 | 0.0 | 7.16 | 65.19 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.69 | 8.35 | 31.94 | 0.0 | 18.89 | 25.16 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.08 | 0.0 | 27.0 | 0.0 | 19.46 | 22.47 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.44 | 0.0 | 15.59 | 0.0 | 7.45 | 9.48 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.0 | 0.0 | 37.0 | 0.0 | 13.81 | 48.93 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.69 | 0.0 | 24.06 | 0.0 | 14.83 | 43.28 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.41 | 37.14 | 50.21 | 0.0 | 67.92 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.25 | 0.0 | 41.85 | 0.0 | 16.36 | 22.83 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.49 | 0.0 | 10.97 | 0.0 | 7.15 | 73.99 | 1.33 | underutilised: SM 31 %, DRAM 17 %, L2 11 %, occ 85 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.64 | 8.26 | 31.75 | 0.0 | 18.64 | 25.4 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.07 | 0.0 | 27.0 | 0.0 | 18.99 | 21.97 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.46 | 0.0 | 15.84 | 0.0 | 7.95 | 9.41 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.43 | 0.0 | 35.26 | 0.0 | 13.86 | 49.17 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.95 | 0.0 | 23.83 | 0.0 | 14.77 | 43.27 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.02 | 37.0 | 49.74 | 0.0 | 67.24 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.07 | 0.0 | 41.05 | 0.0 | 16.25 | 22.83 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.64 | 0.0 | 10.87 | 0.0 | 7.19 | 73.42 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.76 | 8.14 | 32.15 | 0.0 | 18.47 | 24.98 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.07 | 0.0 | 27.06 | 0.0 | 18.8 | 22.24 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.43 | 0.0 | 15.81 | 0.0 | 7.76 | 9.35 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.94 | 0.0 | 34.89 | 0.0 | 13.73 | 49.3 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.85 | 0.0 | 24.68 | 0.0 | 14.4 | 43.07 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.6 | 37.31 | 50.06 | 0.0 | 67.98 | 8.33 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.23 | 0.0 | 40.32 | 0.0 | 15.98 | 22.93 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.36 | 0.0 | 11.24 | 0.0 | 7.15 | 74.69 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.77 | 8.1 | 31.7 | 0.0 | 19.06 | 25.28 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.01 | 0.0 | 27.15 | 0.0 | 18.89 | 22.26 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.46 | 0.0 | 15.46 | 0.0 | 7.86 | 9.37 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.15 | 0.0 | 35.9 | 0.0 | 14.15 | 49.29 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 9.05 | 0.0 | 23.58 | 0.0 | 14.33 | 43.14 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.31 | 36.9 | 49.84 | 0.0 | 66.87 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.11 | 0.0 | 41.15 | 0.0 | 16.19 | 22.52 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.5 | 0.0 | 10.91 | 0.0 | 7.1 | 73.52 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.82 | 8.34 | 31.75 | 0.0 | 18.62 | 25.38 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.09 | 0.0 | 27.58 | 0.0 | 18.66 | 22.24 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.45 | 0.0 | 14.43 | 0.0 | 7.4 | 9.57 | 0.06 | underutilised: SM 1 %, DRAM 47 %, L2 22 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.1 | 0.0 | 35.84 | 0.0 | 14.14 | 49.25 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.83 | 0.0 | 23.24 | 0.0 | 14.2 | 43.32 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.17 | 37.07 | 49.58 | 0.0 | 67.95 | 8.33 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.25 | 0.0 | 40.66 | 0.0 | 16.1 | 22.62 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.58 | 0.0 | 10.97 | 0.0 | 7.12 | 73.6 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.83 | 8.29 | 31.69 | 0.0 | 18.59 | 25.16 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.1 | 0.0 | 27.29 | 0.0 | 18.75 | 22.22 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.44 | 0.0 | 14.76 | 0.0 | 7.51 | 9.45 | 0.06 | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.99 | 0.0 | 35.84 | 0.0 | 14.11 | 49.25 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.82 | 0.0 | 23.62 | 0.0 | 14.43 | 42.91 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.82 | 36.94 | 49.58 | 0.0 | 67.07 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.19 | 0.0 | 40.48 | 0.0 | 15.94 | 22.52 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.2 | 0.0 | 10.88 | 0.0 | 7.24 | 73.51 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.79 | 8.22 | 32.02 | 0.0 | 18.58 | 24.96 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.12 | 0.0 | 27.44 | 0.0 | 18.85 | 22.24 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.48 | 0.0 | 15.93 | 0.0 | 8.26 | 9.58 | 0.06 | underutilised: SM 1 %, DRAM 46 %, L2 22 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.04 | 0.0 | 36.03 | 0.0 | 14.16 | 49.06 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 9.02 | 0.0 | 23.75 | 0.0 | 14.53 | 43.31 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.72 | 36.69 | 49.6 | 0.0 | 67.13 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.22 | 0.0 | 41.6 | 0.0 | 16.53 | 22.69 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.1 | 0.0 | 11.11 | 0.0 | 7.12 | 73.69 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.8 | 8.12 | 31.75 | 0.0 | 19.09 | 25.31 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.09 | 0.0 | 27.62 | 0.0 | 19.33 | 22.15 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.41 | 0.0 | 14.52 | 0.0 | 9.25 | 9.7 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.1 | 0.0 | 34.4 | 0.0 | 13.53 | 49.2 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 9.01 | 0.0 | 24.14 | 0.0 | 14.58 | 43.1 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.16 | 37.22 | 49.51 | 0.0 | 67.77 | 8.33 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 4.84 | 0.0 | 42.28 | 0.0 | 16.63 | 22.68 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.76 | 0.0 | 11.01 | 0.0 | 7.22 | 73.46 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 16.14 | 8.17 | 31.86 | 0.0 | 18.63 | 25.16 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.08 | 0.0 | 27.64 | 0.0 | 18.78 | 22.23 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.44 | 0.0 | 14.74 | 0.0 | 7.78 | 9.6 | 0.06 | underutilised: SM 1 %, DRAM 46 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.37 | 0.0 | 35.32 | 0.0 | 13.85 | 49.24 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.97 | 0.0 | 23.91 | 0.0 | 14.35 | 42.99 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.6 | 36.97 | 50.22 | 0.0 | 67.63 | 8.33 | 1.0 | underutilised: SM 28 %, DRAM 52 %, L2 57 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.27 | 0.0 | 41.53 | 0.0 | 16.41 | 22.69 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.77 | 0.0 | 11.2 | 0.0 | 7.1 | 73.98 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.85 | 8.19 | 32.4 | 0.0 | 18.73 | 25.32 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.04 | 0.0 | 26.98 | 0.0 | 18.88 | 22.21 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.47 | 0.0 | 14.84 | 0.0 | 7.46 | 9.45 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.13 | 0.0 | 34.52 | 0.0 | 13.62 | 49.07 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.8 | 0.0 | 23.75 | 0.0 | 14.29 | 43.31 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.95 | 37.06 | 49.47 | 0.0 | 67.2 | 8.33 | 1.0 | underutilised: SM 28 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.04 | 0.0 | 42.05 | 0.0 | 16.63 | 22.94 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.39 | 0.0 | 10.91 | 0.0 | 7.13 | 74.35 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 10 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.78 | 8.23 | 31.76 | 0.0 | 19.2 | 25.4 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.08 | 0.0 | 26.81 | 0.0 | 19.0 | 22.12 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.46 | 0.0 | 15.17 | 0.0 | 12.1 | 9.36 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.11 | 0.0 | 35.71 | 0.0 | 14.06 | 48.84 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.77 | 0.0 | 24.06 | 0.0 | 14.14 | 43.46 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.63 | 37.16 | 49.98 | 0.0 | 67.61 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.22 | 0.0 | 42.41 | 0.0 | 16.75 | 22.78 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.53 | 0.0 | 10.87 | 0.0 | 7.05 | 72.96 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.66 | 8.17 | 31.77 | 0.0 | 18.68 | 25.18 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.08 | 0.0 | 26.92 | 0.0 | 19.06 | 22.09 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.27 | 0.0 | 15.55 | 0.0 | 8.02 | 9.52 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 9.96 | 0.0 | 34.95 | 0.0 | 13.76 | 49.41 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.97 | 0.0 | 23.79 | 0.0 | 14.23 | 43.01 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.34 | 37.05 | 49.63 | 0.0 | 67.17 | 8.33 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.0 | 0.0 | 40.65 | 0.0 | 16.33 | 22.65 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.65 | 0.0 | 10.9 | 0.0 | 7.04 | 73.23 | 1.33 | underutilised: SM 30 %, DRAM 18 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.76 | 8.29 | 31.51 | 0.0 | 18.72 | 25.19 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.09 | 0.0 | 27.15 | 0.0 | 19.06 | 22.26 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.47 | 0.0 | 15.51 | 0.0 | 7.96 | 9.33 | 0.06 | underutilised: SM 1 %, DRAM 46 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.26 | 0.0 | 34.59 | 0.0 | 13.57 | 49.19 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.87 | 0.0 | 24.03 | 0.0 | 14.46 | 42.67 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.98 | 37.17 | 50.09 | 0.0 | 67.39 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.25 | 0.0 | 41.78 | 0.0 | 16.56 | 22.32 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.73 | 0.0 | 10.92 | 0.0 | 7.08 | 72.98 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.72 | 8.22 | 31.82 | 0.0 | 18.84 | 25.01 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.05 | 0.0 | 27.09 | 0.0 | 18.94 | 22.1 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.46 | 0.0 | 14.47 | 0.0 | 7.59 | 9.24 | 0.06 | underutilised: SM 1 %, DRAM 46 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.17 | 0.0 | 35.9 | 0.0 | 14.12 | 49.19 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.77 | 0.0 | 24.66 | 0.0 | 14.58 | 42.85 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.25 | 36.94 | 49.25 | 0.0 | 67.07 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 51 %, L2 57 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.06 | 0.0 | 40.91 | 0.0 | 15.99 | 22.56 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.78 | 0.0 | 10.75 | 0.0 | 6.96 | 73.87 | 1.33 | underutilised: SM 30 %, DRAM 16 %, L2 10 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.67 | 8.2 | 31.8 | 0.0 | 18.78 | 25.03 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.07 | 0.0 | 26.86 | 0.0 | 18.88 | 22.31 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.45 | 0.0 | 14.63 | 0.0 | 7.4 | 9.57 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.11 | 0.0 | 33.99 | 0.0 | 13.36 | 49.08 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.81 | 0.0 | 23.16 | 0.0 | 14.34 | 43.4 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.95 | 36.98 | 49.33 | 0.0 | 67.42 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.24 | 0.0 | 41.36 | 0.0 | 16.32 | 22.72 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.63 | 0.0 | 10.87 | 0.0 | 7.09 | 73.25 | 1.33 | underutilised: SM 29 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.7 | 8.19 | 31.91 | 0.0 | 18.74 | 25.23 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.07 | 0.0 | 26.76 | 0.0 | 19.12 | 22.01 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.45 | 0.0 | 15.45 | 0.0 | 7.89 | 9.48 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.34 | 0.0 | 35.39 | 0.0 | 13.86 | 49.22 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.86 | 0.0 | 24.43 | 0.0 | 14.48 | 43.1 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.01 | 37.11 | 49.62 | 0.0 | 66.96 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 58 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.05 | 0.0 | 40.07 | 0.0 | 15.84 | 22.57 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.48 | 0.0 | 10.74 | 0.0 | 7.03 | 73.21 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.88 | 8.2 | 31.62 | 0.0 | 18.79 | 25.29 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.09 | 0.0 | 26.57 | 0.0 | 18.85 | 22.18 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.44 | 0.0 | 14.8 | 0.0 | 7.57 | 9.47 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.02 | 0.0 | 34.52 | 0.0 | 13.58 | 49.14 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.87 | 0.0 | 23.75 | 0.0 | 14.65 | 43.37 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.26 | 37.29 | 49.69 | 0.0 | 67.26 | 8.33 | 1.0 | underutilised: SM 27 %, DRAM 52 %, L2 57 %, occ 8 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.21 | 0.0 | 40.4 | 0.0 | 16.61 | 22.68 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.72 | 0.0 | 10.92 | 0.0 | 7.12 | 73.99 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 85 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.99 | 8.17 | 31.85 | 0.0 | 18.64 | 25.25 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 1.96 | 0.0 | 26.75 | 0.0 | 19.11 | 22.15 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.45 | 0.0 | 15.51 | 0.0 | 7.87 | 9.43 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 19 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.51 | 0.0 | 34.89 | 0.0 | 13.7 | 48.99 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.9 | 0.0 | 23.9 | 0.0 | 14.42 | 43.56 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.95 | 37.31 | 49.68 | 0.0 | 66.69 | 8.33 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.08 | 0.0 | 39.77 | 0.0 | 15.73 | 22.83 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.52 | 0.0 | 10.78 | 0.0 | 7.12 | 73.34 | 1.33 | underutilised: SM 30 %, DRAM 16 %, L2 10 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.65 | 8.21 | 31.6 | 0.0 | 18.88 | 25.12 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.11 | 0.0 | 27.68 | 0.0 | 18.69 | 22.31 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.43 | 0.0 | 14.84 | 0.0 | 7.64 | 9.39 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.25 | 0.0 | 34.71 | 0.0 | 13.69 | 49.05 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.92 | 0.0 | 23.61 | 0.0 | 14.64 | 43.01 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 33.41 | 37.16 | 49.94 | 0.0 | 67.76 | 8.33 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.09 | 0.0 | 41.99 | 0.0 | 16.45 | 22.83 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.39 | 0.0 | 10.64 | 0.0 | 6.86 | 73.95 | 1.33 | underutilised: SM 30 %, DRAM 17 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.71 | 8.16 | 31.77 | 0.0 | 18.65 | 25.27 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.08 | 0.0 | 26.76 | 0.0 | 19.28 | 22.23 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.44 | 0.0 | 15.88 | 0.0 | 7.97 | 9.4 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.13 | 0.0 | 35.9 | 0.0 | 14.1 | 48.96 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.13 | 0.0 | 23.86 | 0.0 | 14.92 | 43.26 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.88 | 36.93 | 48.17 | 0.0 | 62.28 | 8.33 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.23 | 0.0 | 41.01 | 0.0 | 16.07 | 22.64 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.69 | 0.0 | 10.97 | 0.0 | 7.23 | 73.66 | 1.33 | underutilised: SM 30 %, DRAM 18 %, L2 10 %, occ 83 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.83 | 8.21 | 31.87 | 0.0 | 18.78 | 25.14 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | copy | 4.11 | 0.0 | 27.03 | 0.0 | 18.93 | 22.18 | 0.29 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_unary | 0.47 | 0.0 | 15.86 | 0.0 | 7.97 | 9.4 | 0.06 | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | reduce | 10.05 | 0.0 | 35.9 | 0.0 | 14.12 | 49.21 | 0.5 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_binary | 8.81 | 0.0 | 23.62 | 0.0 | 14.45 | 42.76 | 0.5 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | gemm | 32.88 | 36.83 | 48.03 | 0.0 | 62.61 | 8.33 | 1.0 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | elementwise_other | 6.16 | 0.0 | 41.16 | 0.0 | 16.28 | 22.59 | 0.29 | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | concat | 21.39 | 0.0 | 10.8 | 0.0 | 6.95 | 73.07 | 1.33 | underutilised: SM 30 %, DRAM 18 %, L2 11 %, occ 84 % |
| react_moa_mcts | mir_operator:prefill_layer* | False | 1.19 % | profiled | attention | 15.74 | 8.18 | 31.93 | 0.0 | 18.51 | 25.12 | 0.77 | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | copy | 9.67 | 0.0 | 51.61 | 0.0 | 28.28 | 55.81 | 1.0 | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 63 % |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | elementwise_unary | 0.94 | 0.0 | 30.91 | 0.0 | 14.4 | 23.47 | 0.29 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | reduce | 1.61 | 0.0 | 50.85 | 0.0 | 19.98 | 33.27 | 0.08 | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | elementwise_binary | 16.63 | 0.0 | 40.27 | 0.0 | 24.31 | 65.06 | 1.33 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | gemm | 46.46 | 45.87 | 52.55 | 0.0 | 72.22 | 16.55 | 37.09 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | copy | 10.06 | 0.0 | 44.62 | 0.0 | 27.64 | 50.23 | 0.67 | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 69 % |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | elementwise_unary | 0.84 | 0.0 | 28.63 | 0.0 | 13.46 | 17.9 | 0.21 | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 27 % |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | reduce | 1.24 | 0.0 | 37.41 | 0.0 | 14.66 | 33.27 | 0.06 | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | elementwise_binary | 13.86 | 0.0 | 37.78 | 0.0 | 23.46 | 67.74 | 0.92 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | gemm | 41.79 | 42.29 | 65.08 | 0.0 | 66.8 | 16.31 | 19.7 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | copy | 7.07 | 0.0 | 34.72 | 0.0 | 19.69 | 32.78 | 0.4 | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | elementwise_unary | 0.69 | 0.0 | 22.18 | 0.0 | 10.97 | 13.11 | 0.12 | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | reduce | 0.74 | 0.0 | 23.85 | 0.0 | 9.36 | 33.27 | 0.04 | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | elementwise_binary | 11.09 | 0.0 | 23.62 | 0.0 | 15.49 | 45.6 | 0.54 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_head | False | 0.01 % | profiled | gemm | 45.91 | 46.6 | 77.28 | 0.0 | 69.03 | 16.29 | 12.76 | tensor-core compute-bound |
| react_moa_mcts | mir_operator:prefill_sample | False | 0.07 % | profiled | reduce | 2.79 | 0.0 | 5.27 | 0.0 | 3.04 | 33.13 | 0.05 | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_sample | False | 0.07 % | profiled | reduce | 2.79 | 0.0 | 5.26 | 0.0 | 3.26 | 33.13 | 0.05 | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:prefill_sample | False | 0.07 % | profiled | reduce | 2.78 | 0.0 | 5.27 | 0.0 | 2.99 | 33.13 | 0.05 | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_embed | False | 0.15 % | profiled | other | 0.25 | 0.0 | 0.34 | 0.0 | 0.65 | 8.31 | 0.01 | latency/launch-bound: 0.01 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_embed | False | 0.15 % | profiled | other | 0.25 | 0.0 | 0.34 | 0.0 | 0.71 | 8.31 | 0.01 | latency/launch-bound: 0.01 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_embed | False | 0.15 % | profiled | other | 0.25 | 0.0 | 0.34 | 0.0 | 0.7 | 8.31 | 0.01 | latency/launch-bound: 0.01 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.26 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.5 | 0.0 | 0.9 | 7.38 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.83 | 31.85 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.36 | 0.0 | 75.45 | 0.0 | 47.34 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.07 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.36 | 0.0 | 13.25 | 0.0 | 6.64 | 56.09 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.53 | 11.32 | 12.49 | 0.0 | 5.34 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.6 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.01 | 0.0 | 0.42 | 0.0 | 0.88 | 7.47 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.85 | 31.91 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.35 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.26 | 0.0 | 75.01 | 0.0 | 47.28 | 15.93 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.14 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.47 | 0.0 | 13.26 | 0.0 | 6.66 | 56.65 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.52 | 11.59 | 12.23 | 0.0 | 5.39 | 8.27 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.61 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.47 | 0.0 | 0.9 | 7.54 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.85 | 31.82 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.4 | 0.0 | 74.9 | 0.0 | 46.57 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.25 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.46 | 0.0 | 13.5 | 0.0 | 7.02 | 56.38 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.47 | 11.21 | 12.17 | 0.0 | 5.22 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.9 | 0.0 | 1.62 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.89 | 7.7 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.97 | 0.0 | 3.84 | 31.85 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.37 | 0.0 | 74.63 | 0.0 | 46.74 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.1 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.49 | 0.0 | 13.35 | 0.0 | 6.62 | 56.19 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.57 | 11.18 | 12.22 | 0.0 | 5.24 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 1.04 | 0.0 | 2.22 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.89 | 7.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.96 | 0.0 | 3.85 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.5 | 0.0 | 74.79 | 0.0 | 47.45 | 16.03 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.28 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.28 | 0.0 | 13.63 | 0.0 | 6.87 | 56.15 | 1.08 | underutilised: SM 5 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.39 | 11.33 | 6.79 | 0.0 | 3.1 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.82 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.89 | 7.48 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.85 | 31.78 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.42 | 0.0 | 74.47 | 0.0 | 46.52 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.08 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.34 | 0.0 | 13.47 | 0.0 | 6.75 | 55.97 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.54 | 11.35 | 12.45 | 0.0 | 5.53 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.76 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.89 | 7.66 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.83 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.43 | 0.0 | 74.85 | 0.0 | 46.57 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.11 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.35 | 0.0 | 13.37 | 0.0 | 6.69 | 56.28 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.54 | 11.27 | 12.29 | 0.0 | 5.23 | 8.27 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.9 | 0.0 | 2.21 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.89 | 7.78 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.97 | 0.0 | 3.85 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.41 | 0.0 | 75.4 | 0.0 | 47.16 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.17 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.49 | 0.0 | 5.29 | 0.0 | 5.95 | 56.59 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.46 | 11.36 | 11.95 | 0.0 | 5.13 | 8.3 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.76 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.89 | 7.5 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.81 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.5 | 0.0 | 75.35 | 0.0 | 46.8 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.13 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.37 | 0.0 | 13.38 | 0.0 | 6.69 | 56.06 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.51 | 11.26 | 12.22 | 0.0 | 5.25 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.87 | 0.0 | 2.22 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.89 | 7.46 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.84 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.54 | 0.0 | 74.36 | 0.0 | 46.97 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.17 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.41 | 0.0 | 13.31 | 0.0 | 6.66 | 56.12 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.48 | 11.25 | 12.71 | 0.0 | 5.44 | 8.3 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.9 | 0.0 | 1.85 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.91 | 7.65 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.83 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.35 | 0.0 | 74.75 | 0.0 | 46.93 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.16 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.44 | 0.0 | 13.38 | 0.0 | 6.7 | 55.94 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.42 | 11.18 | 11.9 | 0.0 | 5.12 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.88 | 0.0 | 1.61 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.88 | 7.7 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.85 | 31.88 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.44 | 0.0 | 75.45 | 0.0 | 47.46 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.09 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.5 | 0.0 | 14.04 | 0.0 | 8.92 | 56.16 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.55 | 11.43 | 12.67 | 0.0 | 5.41 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.59 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.36 | 0.0 | 0.89 | 7.6 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.83 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.34 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.47 | 0.0 | 74.47 | 0.0 | 46.78 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.15 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.35 | 0.0 | 12.93 | 0.0 | 7.09 | 56.1 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.55 | 11.3 | 12.3 | 0.0 | 5.27 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 2.18 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.39 | 0.0 | 0.89 | 7.65 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.85 | 31.82 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.48 | 0.0 | 74.75 | 0.0 | 46.55 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.16 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.52 | 0.0 | 13.26 | 0.0 | 6.72 | 56.09 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.53 | 11.21 | 12.22 | 0.0 | 5.26 | 8.27 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.9 | 0.0 | 1.52 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.89 | 7.59 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.83 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.35 | 0.0 | 75.34 | 0.0 | 47.53 | 15.95 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.11 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.51 | 0.0 | 13.37 | 0.0 | 6.68 | 55.97 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.54 | 11.14 | 12.39 | 0.0 | 5.34 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.9 | 0.0 | 1.62 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.9 | 7.67 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.83 | 31.92 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.44 | 0.0 | 75.34 | 0.0 | 46.76 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.74 | 0.0 | 1.08 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.32 | 0.0 | 13.41 | 0.0 | 6.97 | 56.08 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.55 | 11.46 | 12.62 | 0.0 | 5.39 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.9 | 0.0 | 1.81 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.87 | 7.54 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.85 | 31.89 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.44 | 0.0 | 75.07 | 0.0 | 47.92 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.39 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.39 | 0.0 | 13.41 | 0.0 | 7.21 | 55.81 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.44 | 11.23 | 12.05 | 0.0 | 5.16 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.9 | 0.0 | 1.6 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.88 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.96 | 0.0 | 3.83 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.5 | 0.0 | 74.96 | 0.0 | 47.16 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.07 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.46 | 0.0 | 13.42 | 0.0 | 7.08 | 56.32 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.53 | 11.37 | 13.96 | 0.0 | 5.57 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.6 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.9 | 7.69 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.95 | 0.0 | 3.84 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.51 | 0.0 | 74.79 | 0.0 | 46.67 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.41 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.33 | 0.0 | 13.48 | 0.0 | 6.75 | 56.01 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.48 | 11.4 | 12.31 | 0.0 | 5.31 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.84 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.6 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.99 | 0.0 | 3.87 | 31.85 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.5 | 0.0 | 75.23 | 0.0 | 46.83 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.15 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.5 | 0.0 | 13.11 | 0.0 | 6.85 | 56.62 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.53 | 11.48 | 12.31 | 0.0 | 5.27 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 2.17 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.89 | 7.65 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.82 | 31.91 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.38 | 0.0 | 75.4 | 0.0 | 46.88 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.09 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.51 | 0.0 | 13.49 | 0.0 | 6.72 | 56.29 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.54 | 11.23 | 12.56 | 0.0 | 5.37 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 2.19 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.88 | 7.48 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.83 | 31.91 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.54 | 0.0 | 75.56 | 0.0 | 46.93 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.07 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.47 | 0.0 | 13.38 | 0.0 | 6.64 | 56.44 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.51 | 11.14 | 12.4 | 0.0 | 5.86 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.84 | 0.0 | 1.51 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.89 | 7.66 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.81 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.49 | 0.0 | 74.85 | 0.0 | 47.31 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.07 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.37 | 0.0 | 13.97 | 0.0 | 7.21 | 56.06 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.45 | 11.17 | 11.97 | 0.0 | 5.13 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.9 | 0.0 | 1.78 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.93 | 7.64 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.84 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.6 | 0.0 | 75.12 | 0.0 | 46.73 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.17 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.44 | 0.0 | 13.43 | 0.0 | 6.87 | 56.17 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.56 | 11.44 | 12.13 | 0.0 | 5.19 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.9 | 0.0 | 1.81 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.91 | 7.69 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.81 | 31.87 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.58 | 0.0 | 75.07 | 0.0 | 47.23 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.16 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.35 | 0.0 | 13.44 | 0.0 | 6.74 | 56.58 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.53 | 11.14 | 12.5 | 0.0 | 5.37 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.6 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.89 | 7.46 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.87 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.43 | 0.0 | 75.34 | 0.0 | 46.99 | 16.03 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.38 | 8.25 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.43 | 0.0 | 13.41 | 0.0 | 6.99 | 56.18 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.54 | 11.21 | 12.28 | 0.0 | 5.47 | 8.28 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.9 | 0.0 | 1.62 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.88 | 7.7 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.84 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.47 | 0.0 | 75.45 | 0.0 | 47.21 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.11 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.45 | 0.0 | 13.41 | 0.0 | 6.73 | 56.25 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.55 | 11.23 | 12.27 | 0.0 | 6.13 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 1.02 | 0.0 | 1.66 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.47 | 0.0 | 0.89 | 7.46 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.86 | 31.85 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.34 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.48 | 0.0 | 75.07 | 0.0 | 47.22 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.08 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 5.28 | 0.0 | 13.54 | 0.0 | 6.73 | 56.25 | 1.08 | underutilised: SM 6 %, DRAM 0 %, L2 0 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.55 | 11.13 | 12.49 | 0.0 | 5.32 | 8.29 | 0.12 | latency/launch-bound: 0.31 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.56 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.94 | 7.52 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.8 | 31.87 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.38 | 0.0 | 74.77 | 0.0 | 46.82 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.72 | 0.0 | 1.23 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.65 | 0.0 | 10.56 | 0.0 | 5.64 | 50.56 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.93 | 12.04 | 9.33 | 0.0 | 4.16 | 8.28 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 2.14 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.64 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.89 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.42 | 0.0 | 74.55 | 0.0 | 46.38 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.15 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.76 | 0.0 | 10.25 | 0.0 | 5.39 | 50.52 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.01 | 11.97 | 9.48 | 0.0 | 4.5 | 8.3 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.88 | 0.0 | 1.61 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.9 | 7.71 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.84 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.41 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.48 | 0.0 | 74.55 | 0.0 | 46.81 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.3 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.78 | 0.0 | 10.45 | 0.0 | 5.57 | 50.44 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.96 | 12.05 | 9.38 | 0.0 | 4.18 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.87 | 0.0 | 1.79 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.39 | 0.0 | 0.91 | 7.71 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.96 | 0.0 | 3.85 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.47 | 0.0 | 74.71 | 0.0 | 46.89 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.26 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.76 | 0.0 | 10.55 | 0.0 | 5.69 | 50.86 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.99 | 12.05 | 9.31 | 0.0 | 4.16 | 8.28 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.87 | 0.0 | 1.81 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.91 | 7.58 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.84 | 31.93 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.42 | 0.0 | 74.25 | 0.0 | 47.7 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.29 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.7 | 0.0 | 10.58 | 0.0 | 5.4 | 50.44 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.95 | 12.04 | 9.34 | 0.0 | 4.14 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.76 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.01 | 0.0 | 0.42 | 0.0 | 0.89 | 7.34 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.85 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.49 | 0.0 | 75.01 | 0.0 | 47.26 | 15.95 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.19 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.84 | 0.0 | 10.4 | 0.0 | 5.3 | 50.69 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.96 | 12.16 | 9.43 | 0.0 | 4.21 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.87 | 0.0 | 1.87 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.92 | 7.67 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.86 | 31.91 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.42 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.52 | 0.0 | 75.57 | 0.0 | 47.04 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.27 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.61 | 0.0 | 3.12 | 0.0 | 1.8 | 50.78 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.95 | 12.09 | 9.23 | 0.0 | 4.11 | 8.27 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.73 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.61 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.86 | 31.88 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.54 | 0.0 | 74.82 | 0.0 | 46.83 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.18 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.77 | 0.0 | 10.72 | 0.0 | 5.45 | 50.47 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.98 | 12.13 | 9.47 | 0.0 | 4.22 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.61 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.97 | 7.67 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.87 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.36 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.43 | 0.0 | 74.8 | 0.0 | 47.07 | 15.94 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.29 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.67 | 0.0 | 11.0 | 0.0 | 5.62 | 50.73 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.96 | 11.97 | 9.27 | 0.0 | 4.14 | 8.27 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.6 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.94 | 7.69 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.88 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.37 | 0.0 | 74.61 | 0.0 | 46.96 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.41 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.76 | 0.0 | 10.53 | 0.0 | 5.42 | 50.85 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.0 | 12.18 | 9.48 | 0.0 | 4.45 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.86 | 0.0 | 1.75 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.91 | 7.69 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.84 | 31.89 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.44 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.51 | 0.0 | 75.12 | 0.0 | 46.83 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.18 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.67 | 0.0 | 10.22 | 0.0 | 5.49 | 50.41 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.97 | 12.06 | 9.37 | 0.0 | 4.16 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.87 | 0.0 | 1.56 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.91 | 7.71 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.97 | 0.0 | 3.84 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.45 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.42 | 0.0 | 75.29 | 0.0 | 47.05 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.78 | 0.0 | 1.41 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.71 | 0.0 | 10.61 | 0.0 | 5.67 | 50.36 | 0.92 | underutilised: SM 5 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.01 | 12.06 | 9.55 | 0.0 | 4.25 | 8.3 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.86 | 0.0 | 1.55 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.93 | 7.65 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.86 | 31.82 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.35 | 0.0 | 75.07 | 0.0 | 46.76 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.18 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.79 | 0.0 | 10.38 | 0.0 | 5.54 | 50.33 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.99 | 11.8 | 9.44 | 0.0 | 4.23 | 8.27 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.6 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.5 | 0.0 | 0.88 | 7.71 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.97 | 0.0 | 3.88 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.44 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.44 | 0.0 | 75.21 | 0.0 | 46.94 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.16 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.75 | 0.0 | 11.09 | 0.0 | 5.64 | 50.59 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.98 | 12.11 | 9.45 | 0.0 | 4.22 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.55 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.39 | 0.0 | 0.9 | 7.64 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.82 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.48 | 0.0 | 75.01 | 0.0 | 47.26 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.24 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.72 | 0.0 | 10.75 | 0.0 | 5.44 | 50.75 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.94 | 12.03 | 9.24 | 0.0 | 4.14 | 8.3 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 1.01 | 0.0 | 2.14 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.01 | 0.0 | 0.51 | 0.0 | 0.91 | 7.68 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.95 | 0.0 | 3.82 | 31.85 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.32 | 0.0 | 74.69 | 0.0 | 46.94 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.18 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.71 | 0.0 | 10.41 | 0.0 | 5.36 | 50.67 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.04 | 11.9 | 9.32 | 0.0 | 4.41 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.01 | 0.0 | 0.89 | 0.0 | 1.55 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.01 | 0.0 | 0.4 | 0.0 | 0.91 | 7.47 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.88 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.43 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.49 | 0.0 | 74.71 | 0.0 | 46.62 | 15.94 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.72 | 0.0 | 1.3 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.74 | 0.0 | 3.34 | 0.0 | 1.47 | 50.77 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.96 | 12.05 | 9.27 | 0.0 | 4.12 | 8.28 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.59 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 7.52 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.86 | 31.82 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.46 | 0.0 | 75.24 | 0.0 | 46.62 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.18 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.84 | 0.0 | 10.51 | 0.0 | 5.38 | 50.4 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.98 | 12.08 | 9.52 | 0.0 | 4.24 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.87 | 0.0 | 1.57 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.92 | 7.66 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.85 | 31.82 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.47 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.42 | 0.0 | 75.34 | 0.0 | 47.39 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.1 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.67 | 0.0 | 10.59 | 0.0 | 5.47 | 50.92 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.97 | 12.07 | 10.4 | 0.0 | 4.14 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.81 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.85 | 31.85 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.42 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.34 | 0.0 | 75.29 | 0.0 | 46.6 | 15.94 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.12 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.8 | 0.0 | 10.52 | 0.0 | 5.34 | 50.76 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.97 | 12.1 | 9.38 | 0.0 | 4.16 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.88 | 0.0 | 1.47 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.93 | 7.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.97 | 0.0 | 3.88 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.75 | 0.0 | 1.49 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.39 | 0.0 | 75.31 | 0.0 | 47.36 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.18 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.75 | 0.0 | 10.37 | 0.0 | 5.7 | 51.2 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.97 | 12.01 | 9.36 | 0.0 | 4.18 | 8.27 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.61 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.37 | 0.0 | 0.93 | 7.41 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.87 | 31.9 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.38 | 8.32 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.4 | 0.0 | 74.71 | 0.0 | 47.12 | 15.97 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.42 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.77 | 0.0 | 10.69 | 0.0 | 5.46 | 50.75 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.0 | 11.96 | 9.65 | 0.0 | 4.3 | 8.28 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.62 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.95 | 7.4 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.91 | 31.82 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.33 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.49 | 0.0 | 74.09 | 0.0 | 46.39 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.17 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.79 | 0.0 | 11.29 | 0.0 | 5.8 | 50.7 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.96 | 12.0 | 9.35 | 0.0 | 4.18 | 8.28 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 2.17 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.97 | 7.55 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.96 | 0.0 | 3.89 | 31.78 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.54 | 0.0 | 74.87 | 0.0 | 46.97 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.29 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.81 | 0.0 | 11.15 | 0.0 | 5.67 | 50.78 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.98 | 12.14 | 9.54 | 0.0 | 4.24 | 8.26 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.61 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.91 | 7.71 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.86 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.49 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.47 | 0.0 | 74.66 | 0.0 | 46.56 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.17 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.68 | 0.0 | 10.4 | 0.0 | 5.36 | 50.68 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.98 | 12.08 | 9.23 | 0.0 | 4.12 | 8.28 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.85 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.69 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.97 | 0.0 | 3.86 | 31.87 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.59 | 0.0 | 75.45 | 0.0 | 47.12 | 16.04 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.13 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.65 | 0.0 | 10.69 | 0.0 | 5.5 | 50.49 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.99 | 12.07 | 9.57 | 0.0 | 4.25 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.87 | 0.0 | 1.6 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.87 | 7.57 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.86 | 31.89 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.47 | 0.0 | 74.53 | 0.0 | 46.2 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.16 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.78 | 0.0 | 10.4 | 0.0 | 5.34 | 51.06 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.93 | 11.82 | 9.2 | 0.0 | 4.14 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 0.98 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.88 | 7.39 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.99 | 0.0 | 3.88 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.4 | 8.32 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.31 | 0.0 | 74.33 | 0.0 | 46.55 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.07 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.72 | 0.0 | 10.75 | 0.0 | 5.47 | 50.73 | 0.92 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 2.01 | 11.95 | 9.47 | 0.0 | 4.22 | 8.29 | 0.1 | latency/launch-bound: 0.19 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.8 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.94 | 7.71 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.94 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.49 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.38 | 0.0 | 74.09 | 0.0 | 46.6 | 15.95 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.78 | 0.0 | 1.27 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.17 | 0.0 | 6.91 | 0.0 | 3.7 | 46.83 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.38 | 12.35 | 6.18 | 0.0 | 3.05 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 2.2 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 1.0 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.93 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.45 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.45 | 0.0 | 74.9 | 0.0 | 46.68 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.2 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.18 | 0.0 | 7.1 | 0.0 | 3.88 | 46.84 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.4 | 12.22 | 6.09 | 0.0 | 3.0 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.77 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.96 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.9 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.49 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.41 | 0.0 | 74.33 | 0.0 | 46.67 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.16 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.11 | 0.0 | 7.15 | 0.0 | 3.88 | 46.82 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.39 | 12.29 | 6.16 | 0.0 | 3.03 | 8.29 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.6 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.98 | 7.37 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.95 | 0.0 | 3.93 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.43 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.5 | 0.0 | 75.31 | 0.0 | 47.3 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.21 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.19 | 0.0 | 7.47 | 0.0 | 4.05 | 46.83 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.39 | 12.37 | 6.14 | 0.0 | 3.04 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 1.01 | 0.0 | 1.63 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 7.32 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.99 | 0.0 | 3.86 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.41 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.53 | 0.0 | 74.41 | 0.0 | 45.92 | 15.94 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.3 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.13 | 0.0 | 6.91 | 0.0 | 3.75 | 47.02 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.39 | 12.15 | 6.16 | 0.0 | 3.0 | 8.29 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.87 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.93 | 7.62 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 2.0 | 0.0 | 3.87 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.45 | 0.0 | 75.12 | 0.0 | 46.64 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.31 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 3.44 | 0.0 | 7.22 | 0.0 | 4.1 | 46.89 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.38 | 12.19 | 6.12 | 0.0 | 3.02 | 8.31 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 1.0 | 0.0 | 1.82 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.95 | 7.51 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.92 | 31.88 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.62 | 0.0 | 75.76 | 0.0 | 47.35 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.8 | 0.0 | 1.15 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.05 | 0.0 | 7.14 | 0.0 | 3.88 | 46.75 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.38 | 12.35 | 6.15 | 0.0 | 3.02 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.87 | 0.0 | 1.57 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.9 | 7.37 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.95 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.51 | 0.0 | 74.85 | 0.0 | 46.99 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.16 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.16 | 0.0 | 7.2 | 0.0 | 3.89 | 46.84 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.39 | 12.39 | 6.11 | 0.0 | 3.24 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.41 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 7.51 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.88 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.81 | 0.0 | 1.43 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.43 | 0.0 | 74.47 | 0.0 | 47.23 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.09 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.11 | 0.0 | 7.06 | 0.0 | 3.85 | 46.73 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.39 | 12.2 | 6.17 | 0.0 | 3.04 | 8.31 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.9 | 0.0 | 1.64 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.91 | 7.35 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.92 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.38 | 8.32 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.48 | 0.0 | 75.32 | 0.0 | 47.33 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.13 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.21 | 0.0 | 7.15 | 0.0 | 3.87 | 46.92 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.41 | 12.41 | 6.17 | 0.0 | 3.01 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 1.01 | 0.0 | 1.61 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 7.52 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.94 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.51 | 0.0 | 75.4 | 0.0 | 46.45 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.21 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.09 | 0.0 | 6.91 | 0.0 | 3.76 | 46.59 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.4 | 12.33 | 6.12 | 0.0 | 3.02 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.6 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.88 | 7.64 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.9 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.23 | 0.0 | 74.77 | 0.0 | 46.82 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.17 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.12 | 0.0 | 7.43 | 0.0 | 4.0 | 46.85 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.4 | 12.29 | 6.11 | 0.0 | 3.02 | 8.28 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.84 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 7.39 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.86 | 31.84 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.39 | 0.0 | 74.58 | 0.0 | 46.54 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.41 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.19 | 0.0 | 8.73 | 0.0 | 4.23 | 46.98 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.38 | 12.2 | 6.13 | 0.0 | 3.03 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.88 | 0.0 | 1.58 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 7.6 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.9 | 31.83 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.49 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.57 | 0.0 | 74.74 | 0.0 | 46.91 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.14 | 8.25 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.17 | 0.0 | 5.41 | 0.0 | 2.99 | 46.67 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.4 | 12.38 | 6.17 | 0.0 | 3.26 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.8 | 0.0 | 1.67 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.01 | 0.0 | 0.42 | 0.0 | 0.91 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.86 | 31.9 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.43 | 0.0 | 75.29 | 0.0 | 47.14 | 15.94 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.72 | 0.0 | 1.13 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.14 | 0.0 | 7.18 | 0.0 | 3.92 | 46.81 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 0.48 | 12.36 | 6.13 | 0.0 | 3.02 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 1.02 | 0.0 | 1.75 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.91 | 7.62 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.91 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.41 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.35 | 0.0 | 75.21 | 0.0 | 47.09 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.2 | 8.25 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.16 | 0.0 | 7.1 | 0.0 | 4.41 | 47.05 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.4 | 12.34 | 6.14 | 0.0 | 3.03 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.87 | 0.0 | 1.73 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.91 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.98 | 0.0 | 3.89 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.43 | 0.0 | 75.15 | 0.0 | 46.8 | 15.96 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.19 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.06 | 0.0 | 7.04 | 0.0 | 3.77 | 46.86 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.41 | 12.35 | 6.13 | 0.0 | 2.99 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.53 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.59 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.99 | 0.0 | 3.94 | 31.8 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.38 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.56 | 0.0 | 75.09 | 0.0 | 46.54 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.14 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.19 | 0.0 | 7.23 | 0.0 | 3.91 | 46.93 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.4 | 12.3 | 6.17 | 0.0 | 3.04 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.87 | 0.0 | 1.62 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.91 | 7.62 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.99 | 0.0 | 3.88 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.56 | 0.0 | 75.26 | 0.0 | 47.33 | 16.04 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.38 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.13 | 0.0 | 6.97 | 0.0 | 3.77 | 46.83 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.39 | 12.33 | 6.14 | 0.0 | 3.04 | 8.29 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.88 | 0.0 | 1.64 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.96 | 7.67 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.92 | 31.86 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.39 | 0.0 | 75.29 | 0.0 | 47.07 | 15.98 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.76 | 0.0 | 1.15 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.09 | 0.0 | 6.99 | 0.0 | 3.77 | 46.82 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.39 | 12.21 | 6.09 | 0.0 | 3.0 | 8.31 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.88 | 0.0 | 1.84 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.9 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.96 | 0.0 | 3.92 | 31.87 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.37 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.48 | 0.0 | 75.43 | 0.0 | 47.01 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.17 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.19 | 0.0 | 7.41 | 0.0 | 4.03 | 46.84 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.41 | 12.3 | 6.15 | 0.0 | 3.25 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.87 | 0.0 | 1.57 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.91 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.9 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.39 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.45 | 0.0 | 74.63 | 0.0 | 47.01 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.82 | 0.0 | 1.09 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.18 | 0.0 | 7.06 | 0.0 | 4.09 | 47.13 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.4 | 12.28 | 6.12 | 0.0 | 2.99 | 8.31 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 2.25 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.94 | 7.63 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.99 | 0.0 | 3.92 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.76 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.44 | 0.0 | 75.29 | 0.0 | 46.43 | 16.0 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.34 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.1 | 0.0 | 7.13 | 0.0 | 3.88 | 46.86 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.36 | 12.31 | 6.11 | 0.0 | 3.02 | 8.31 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.9 | 0.0 | 1.63 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.42 | 0.0 | 0.96 | 7.57 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.96 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.78 | 0.0 | 1.51 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.44 | 0.0 | 75.56 | 0.0 | 47.64 | 16.03 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.79 | 0.0 | 1.18 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.06 | 0.0 | 7.1 | 0.0 | 4.1 | 46.58 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.39 | 12.33 | 6.16 | 0.0 | 3.04 | 8.29 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.64 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.95 | 7.33 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.95 | 31.92 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.81 | 0.0 | 1.47 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.5 | 0.0 | 74.96 | 0.0 | 46.97 | 16.02 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.81 | 0.0 | 1.2 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.18 | 0.0 | 2.65 | 0.0 | 1.64 | 46.88 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.39 | 12.38 | 6.08 | 0.0 | 3.0 | 8.29 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.77 | 0.0 | 1.14 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.95 | 7.65 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.08 | 0.0 | 1.96 | 0.0 | 3.91 | 31.81 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.8 | 0.0 | 1.4 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.39 | 0.0 | 74.12 | 0.0 | 46.16 | 16.01 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.17 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.14 | 0.0 | 7.14 | 0.0 | 3.85 | 46.55 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.37 | 12.41 | 6.19 | 0.0 | 3.05 | 8.29 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.02 | 0.0 | 0.89 | 0.0 | 1.63 | 8.3 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.41 | 0.0 | 0.91 | 7.62 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.94 | 31.91 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.79 | 0.0 | 1.42 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.57 | 0.0 | 74.36 | 0.0 | 46.34 | 15.99 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.77 | 0.0 | 1.31 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.11 | 0.0 | 7.22 | 0.0 | 3.92 | 46.93 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 77 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.41 | 12.16 | 6.12 | 0.0 | 2.99 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | copy | 0.03 | 0.0 | 0.89 | 0.0 | 1.89 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.43 | 0.0 | 0.93 | 7.59 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | reduce | 0.09 | 0.0 | 1.95 | 0.0 | 3.92 | 31.79 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_binary | 0.04 | 0.0 | 0.77 | 0.0 | 1.49 | 8.31 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | gemv | 15.5 | 0.0 | 74.74 | 0.0 | 46.78 | 15.94 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | elementwise_other | 0.02 | 0.0 | 0.83 | 0.0 | 1.3 | 8.27 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | concat | 4.16 | 0.0 | 7.06 | 0.0 | 3.83 | 46.68 | 0.81 | underutilised: SM 6 %, DRAM 0 %, L2 1 %, occ 76 % |
| react_moa_mcts | mir_operator:decode_layer* | True | 92.16 % | profiled | attention | 1.37 | 12.33 | 6.15 | 0.0 | 3.03 | 8.3 | 0.06 | latency/launch-bound: 0.12 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | copy | 0.04 | 0.0 | 0.92 | 0.0 | 1.58 | 8.26 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 7.65 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | reduce | 0.09 | 0.0 | 1.99 | 0.0 | 3.85 | 31.91 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | elementwise_binary | 0.02 | 0.0 | 0.81 | 0.0 | 1.05 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | gemv | 19.89 | 0.0 | 97.04 | 0.0 | 61.42 | 24.49 | 49.46 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | copy | 0.04 | 0.0 | 0.93 | 0.0 | 1.62 | 8.29 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.51 | 0.0 | 0.98 | 7.51 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.93 | 31.87 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | elementwise_binary | 0.02 | 0.0 | 0.81 | 0.0 | 1.05 | 8.25 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | gemv | 19.9 | 0.0 | 94.57 | 0.0 | 59.77 | 24.48 | 49.46 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | copy | 0.04 | 0.0 | 0.92 | 0.0 | 1.6 | 8.28 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | elementwise_unary | 0.02 | 0.0 | 0.54 | 0.0 | 0.94 | 7.62 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | reduce | 0.09 | 0.0 | 1.98 | 0.0 | 3.88 | 31.9 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | elementwise_binary | 0.02 | 0.0 | 0.83 | 0.0 | 1.29 | 8.19 | 0.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_head | False | 0.65 % | profiled | gemv | 19.59 | 0.0 | 96.88 | 0.0 | 60.77 | 24.5 | 49.46 | DRAM-bandwidth-bound |
| react_moa_mcts | mir_operator:decode_sample | False | 1.8 % | profiled | reduce | 2.83 | 0.0 | 5.31 | 0.0 | 3.02 | 33.13 | 0.05 | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_sample | False | 1.8 % | profiled | reduce | 2.79 | 0.0 | 5.23 | 0.0 | 2.99 | 33.13 | 0.05 | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | mir_operator:decode_sample | False | 1.8 % | profiled | reduce | 2.78 | 0.0 | 5.28 | 0.0 | 3.31 | 33.13 | 0.05 | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| react_moa_mcts | pre_d2h_alloc | False | 0.05 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_moa_mcts | pre_d2h_alloc | False | 0.05 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_moa_mcts | d2h_stage | False | 0.0 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_moa_mcts | d2h_stage | False | 0.0 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_moa_mcts | checksum_complete | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | agent_tool_execute_cpu | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts | iteration_tail_sync | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |

### Opportunities (derived, bounded by measured evidence)

| workload | opportunity | current per iter (us) | reference per iter (us) | bound (% of wall) | note |
|---|---|---:|---:|---:|---|
| react_tool | move_input_generation_to_device | 245.9 | 0.0 | 0.01 % | seeded CPU-generator uniform_ into pinned fp16 is single-threaded and O(n^2); device randn for the same n^2 is the weight_init GPU time |
| react_tool | remove_per_operator_synchronize | 3,747,402.3 | 732,866.9 | 77.28 % | each operator ends with cudaEventSynchronize; the host range minus GPU work is dispatch + sync latency that async launch would hide |
| react_tool | gpu_idle_window | 3,166,632.8 | 734,311.6 | 81.18 % | upper bound on wall reduction if all host work were overlapped or removed; single stream, no kernel concurrency observed |
| planner_debate | move_input_generation_to_device | 702.8 | 0.0 | 0.0 % | seeded CPU-generator uniform_ into pinned fp16 is single-threaded and O(n^2); device randn for the same n^2 is the weight_init GPU time |
| planner_debate | remove_per_operator_synchronize | 15,544,067.3 | 2,932,955.7 | 77.75 % | each operator ends with cudaEventSynchronize; the host range minus GPU work is dispatch + sync latency that async launch would hide |
| planner_debate | gpu_idle_window | 13,280,664.1 | 2,938,873.2 | 81.88 % | upper bound on wall reduction if all host work were overlapped or removed; single stream, no kernel concurrency observed |
| react_moa_mcts | move_input_generation_to_device | 1,285.9 | 0.0 | 0.0 % | seeded CPU-generator uniform_ into pinned fp16 is single-threaded and O(n^2); device randn for the same n^2 is the weight_init GPU time |
| react_moa_mcts | remove_per_operator_synchronize | 28,342,835.5 | 5,744,296.7 | 76.57 % | each operator ends with cudaEventSynchronize; the host range minus GPU work is dispatch + sync latency that async launch would hide |
| react_moa_mcts | gpu_idle_window | 23,758,416.9 | 5,755,853.6 | 80.5 % | upper bound on wall reduction if all host work were overlapped or removed; single stream, no kernel concurrency observed |

## Tables (G09)

| table | rows | sha256 |
|---|---:|---|
| g06_selection_plan.csv | 60 | 99ad9558b4d0b951… |
| g06_selected_stacks.csv | 15 | d942e82ecdc86d3f… |
| g06_global_ranking.csv | 60 | b202b410a1393390… |
| g06_denominators.csv | 3 | 4903985d855548ac… |
| g07_process_timeline_representative.csv | 87689 | 819ca8a370b9b7ce… |
| g07_kernel_timeline_representative.csv | 2289199 | ce90eddc3e11347d… |
| g07_launch_gaps.csv | 433785 | d117b78cd7118b18… |
| g07_high_latency_instances.csv | 31508 | f6ba7f85c8186031… |
| g07_host_gpu_overlap.csv | 3 | fd1a6a45bd418992… |
| g08_resource_attachment.csv | 2811 | 3b29ec37133456a2… |
| g08_opportunities.csv | 9 | 5ac02d19df723fe5… |

Visible-range statement (G10): View A stacks show 5 instances per selected type; View B shows every process type but numbers only where a w03 family row attached.
Full per-instance evidence remains in the w01/w02 tables referenced by the admission ledger.

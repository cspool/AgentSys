# G06-G10 selective process trace and resource gap: lineage `scaled`

Lineage `h22-gpu-autotrace`, workflow w05. Admission ledger (sha256 of every upstream handoff) is in `tables_manifest.json`.
Two views follow. The first hides nothing below the 10 % threshold except in the stacks table; the second shows only instances with a
successfully attached hardware metric and says so.

## View A: high-latency process distribution (G06/G07)

### Selection (strictly > 10 % of total process host time)

| workload | process | instances | cumulative (us) | share | median (us) | p90 (us) | max (us) | MAD (us) | GPU-owning | selected |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| react_tool_L | host_input_generate | 16 | 1,075,201.4 | 56.13 % | 66,353.5 | 67,391.7 | 85,877.5 | 867.4 | False | **yes** |
| react_tool_L | mir_operator:LinearOp | 48 | 549,072.3 | 28.66 % | 11,534.1 | 11,613.6 | 11,736.8 | 103.4 | True | **yes** |
| react_tool_L | mir_operator:RMSNormOp | 32 | 140,118.3 | 7.31 % | 4,307.5 | 4,580.1 | 4,932.3 | 80.0 | True | no |
| react_tool_L | mir_operator:TransposeOp | 16 | 68,069.5 | 3.55 % | 4,202.6 | 4,416.9 | 4,525.2 | 83.2 | True | no |
| react_tool_L | adapter_dispatch | 16 | 19,059.7 | 0.99 % | 1,205.5 | 1,457.7 | 1,483.5 | 248.1 | False | no |
| react_tool_L | h2d_stage | 16 | 15,375.8 | 0.8 % | 962.8 | 974.8 | 999.5 | 11.8 | True | no |
| react_tool_L | d2h_stage | 16 | 14,643.7 | 0.76 % | 907.1 | 952.9 | 1,118.7 | 25.1 | True | no |
| react_tool_L | mir_operator:AddOp | 16 | 9,188.2 | 0.48 % | 569.2 | 581.1 | 742.5 | 10.4 | True | no |
| react_tool_L | dag_schedule_gap | 24 | 8,483.4 | 0.44 % | 69.3 | 995.4 | 1,017.5 | 56.5 | False | no |
| react_tool_L | token_preprocess_cpu | 16 | 4,827.8 | 0.25 % | 292.5 | 366.3 | 399.0 | 48.7 | False | no |
| react_tool_L | weight_init | 16 | 3,145.8 | 0.16 % | 193.2 | 197.9 | 252.4 | 3.2 | True | no |
| react_tool_L | agent_tool_execute_cpu | 8 | 2,680.3 | 0.14 % | 325.8 | 356.6 | 377.2 | 13.1 | False | no |
| react_tool_L | mir_operator:ViewOp | 16 | 2,502.9 | 0.13 % | 154.6 | 170.4 | 189.9 | 6.3 | False | no |
| react_tool_L | checksum_complete | 16 | 1,363.7 | 0.07 % | 85.3 | 91.9 | 92.7 | 3.2 | False | no |
| react_tool_L | inter_operator_dispatch | 112 | 1,206.2 | 0.06 % | 9.5 | 16.4 | 23.1 | 2.7 | False | no |
| react_tool_L | iteration_tail_sync | 8 | 454.0 | 0.02 % | 56.9 | 58.1 | 64.3 | 1.9 | False | no |
| react_tool_L | pre_d2h_alloc | 16 | 332.0 | 0.02 % | 20.7 | 24.1 | 26.0 | 1.9 | False | no |
| planner_debate_L | host_input_generate | 40 | 4,155,143.0 | 48.2 % | 110,979.8 | 116,869.8 | 117,808.6 | 5,980.0 | False | **yes** |
| planner_debate_L | mir_operator:LinearOp | 120 | 2,878,961.1 | 33.39 % | 26,025.8 | 27,060.6 | 27,768.3 | 1,043.3 | True | **yes** |
| planner_debate_L | mir_operator:RMSNormOp | 80 | 1,082,436.9 | 12.56 % | 16,034.1 | 16,495.8 | 16,602.7 | 467.0 | True | **yes** |
| planner_debate_L | mir_operator:TransposeOp | 40 | 270,576.6 | 3.14 % | 7,271.4 | 7,496.8 | 7,922.5 | 396.0 | True | no |
| planner_debate_L | h2d_stage | 40 | 58,037.8 | 0.67 % | 1,523.0 | 1,612.5 | 2,058.7 | 36.6 | True | no |
| planner_debate_L | d2h_stage | 40 | 55,809.2 | 0.65 % | 1,483.7 | 1,570.2 | 1,778.0 | 95.2 | True | no |
| planner_debate_L | adapter_dispatch | 40 | 41,655.8 | 0.48 % | 945.3 | 1,423.5 | 1,687.7 | 75.8 | False | no |
| planner_debate_L | mir_operator:AddOp | 40 | 27,947.3 | 0.32 % | 744.6 | 792.4 | 878.8 | 46.1 | True | no |
| planner_debate_L | token_preprocess_cpu | 40 | 13,462.6 | 0.16 % | 344.9 | 396.0 | 410.1 | 42.8 | False | no |
| planner_debate_L | dag_schedule_gap | 48 | 9,240.4 | 0.11 % | 45.5 | 903.2 | 1,004.9 | 15.1 | False | no |
| planner_debate_L | weight_init | 40 | 8,571.7 | 0.1 % | 206.6 | 220.9 | 496.7 | 11.5 | True | no |
| planner_debate_L | mir_operator:ViewOp | 40 | 6,781.2 | 0.08 % | 166.9 | 191.5 | 219.9 | 12.7 | False | no |
| planner_debate_L | inter_operator_dispatch | 280 | 4,294.9 | 0.05 % | 13.8 | 23.9 | 165.8 | 4.9 | False | no |
| planner_debate_L | checksum_complete | 40 | 3,626.6 | 0.04 % | 89.2 | 103.2 | 109.5 | 5.7 | False | no |
| planner_debate_L | agent_tool_execute_cpu | 8 | 3,014.6 | 0.03 % | 385.9 | 395.4 | 424.9 | 8.5 | False | no |
| planner_debate_L | pre_d2h_alloc | 40 | 894.0 | 0.01 % | 21.9 | 27.2 | 32.9 | 2.6 | False | no |
| planner_debate_L | iteration_tail_sync | 8 | 545.2 | 0.01 % | 65.5 | 74.2 | 100.8 | 8.1 | False | no |
| react_moa_mcts_x3_L | host_input_generate | 240 | 25,652,331.9 | 48.37 % | 111,889.4 | 118,639.9 | 139,734.9 | 2,786.2 | False | **yes** |
| react_moa_mcts_x3_L | mir_operator:LinearOp | 720 | 17,490,508.4 | 32.98 % | 26,101.7 | 27,127.5 | 27,894.7 | 525.5 | True | **yes** |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | 480 | 6,903,717.0 | 13.02 % | 16,085.6 | 16,500.6 | 17,098.1 | 301.6 | True | **yes** |
| react_moa_mcts_x3_L | mir_operator:TransposeOp | 240 | 1,665,680.3 | 3.14 % | 7,347.4 | 7,787.9 | 7,921.9 | 102.5 | True | no |
| react_moa_mcts_x3_L | h2d_stage | 240 | 352,661.3 | 0.67 % | 1,531.4 | 1,628.1 | 2,045.6 | 26.7 | True | no |
| react_moa_mcts_x3_L | d2h_stage | 240 | 341,434.0 | 0.64 % | 1,492.7 | 1,572.7 | 1,821.3 | 29.3 | True | no |
| react_moa_mcts_x3_L | adapter_dispatch | 240 | 207,585.7 | 0.39 % | 801.2 | 1,289.7 | 2,253.0 | 46.6 | False | no |
| react_moa_mcts_x3_L | mir_operator:AddOp | 240 | 164,547.6 | 0.31 % | 699.2 | 749.7 | 1,121.7 | 13.3 | True | no |
| react_moa_mcts_x3_L | token_preprocess_cpu | 240 | 78,080.5 | 0.15 % | 326.6 | 376.0 | 3,044.0 | 42.4 | False | no |
| react_moa_mcts_x3_L | weight_init | 240 | 45,079.9 | 0.09 % | 191.0 | 206.2 | 289.6 | 9.7 | True | no |
| react_moa_mcts_x3_L | mir_operator:ViewOp | 240 | 37,665.3 | 0.07 % | 151.2 | 171.9 | 393.8 | 8.2 | False | no |
| react_moa_mcts_x3_L | dag_schedule_gap | 264 | 34,610.7 | 0.07 % | 41.6 | 105.3 | 1,788.2 | 9.7 | False | no |
| react_moa_mcts_x3_L | inter_operator_dispatch | 1680 | 21,733.1 | 0.04 % | 11.8 | 21.3 | 98.5 | 4.1 | False | no |
| react_moa_mcts_x3_L | checksum_complete | 240 | 19,829.5 | 0.04 % | 82.3 | 91.0 | 139.6 | 3.6 | False | no |
| react_moa_mcts_x3_L | agent_tool_execute_cpu | 24 | 7,385.9 | 0.01 % | 313.7 | 357.7 | 384.3 | 42.5 | False | no |
| react_moa_mcts_x3_L | pre_d2h_alloc | 240 | 5,035.1 | 0.01 % | 19.6 | 32.1 | 50.7 | 5.6 | False | no |
| react_moa_mcts_x3_L | iteration_tail_sync | 8 | 609.2 | 0.0 % | 78.9 | 88.8 | 108.6 | 11.7 | False | no |

### Five longest instances per selected type (real start/end on the nsys clock)

| workload | process | rank | iter | call | start (ns) | host (us) | GPU (us) | top CUDA API |
|---|---|---:|---:|---|---:|---:|---:|---|
| react_tool_L | host_input_generate | 1 | 6 | answer | 5298580515 | 85,877.5 | 0.0 | cudaEventQuery |
| react_tool_L | host_input_generate | 2 | 0 | answer | 3881049144 | 68,027.5 | 0.0 | cudaEventQuery |
| react_tool_L | host_input_generate | 3 | 7 | answer | 5557579357 | 67,391.7 | 0.0 | cudaEventQuery |
| react_tool_L | host_input_generate | 4 | 6 | plan | 5178123098 | 67,192.7 | 0.0 | cudaEventQuery |
| react_tool_L | host_input_generate | 5 | 7 | plan | 5437535248 | 67,008.7 | 0.0 | cudaEventQuery |
| react_tool_L | mir_operator:LinearOp | 1 | 4 | plan | 4802386341 | 11,736.8 | 11,638.3 | cudaEventSynchronize |
| react_tool_L | mir_operator:LinearOp | 2 | 0 | plan | 3860724906 | 11,701.4 | 11,612.7 | cudaEventSynchronize |
| react_tool_L | mir_operator:LinearOp | 3 | 3 | answer | 4684390656 | 11,647.5 | 11,493.4 | cudaEventSynchronize |
| react_tool_L | mir_operator:LinearOp | 4 | 1 | plan | 4100102938 | 11,643.9 | 11,522.2 | cudaEventSynchronize |
| react_tool_L | mir_operator:LinearOp | 5 | 6 | answer | 5396258164 | 11,625.1 | 11,420.9 | cudaEventSynchronize |
| planner_debate_L | host_input_generate | 1 | 4 | critic-a | 10930046254 | 117,808.6 | 0.0 | cudaEventQuery |
| planner_debate_L | host_input_generate | 2 | 3 | critic-b | 10086928526 | 117,498.4 | 0.0 | cudaEventQuery |
| planner_debate_L | host_input_generate | 3 | 1 | critic-a | 7681340652 | 117,266.2 | 0.0 | cudaEventQuery |
| planner_debate_L | host_input_generate | 4 | 2 | critic-merge | 9237079717 | 117,049.9 | 0.0 | cudaEventQuery |
| planner_debate_L | host_input_generate | 5 | 7 | critic-merge | 14613421562 | 116,869.8 | 0.0 | cudaEventQuery |
| planner_debate_L | mir_operator:LinearOp | 1 | 6 | critic-b | 13510267034 | 27,768.3 | 27,595.0 | cudaEventSynchronize |
| planner_debate_L | mir_operator:LinearOp | 2 | 5 | critic-merge | 12683451351 | 27,586.3 | 27,302.1 | cudaEventSynchronize |
| planner_debate_L | mir_operator:LinearOp | 3 | 0 | critic-merge | 7280123009 | 27,482.0 | 27,282.8 | cudaEventSynchronize |
| planner_debate_L | mir_operator:LinearOp | 4 | 4 | critic-merge | 11608485378 | 27,365.5 | 27,221.8 | cudaEventSynchronize |
| planner_debate_L | mir_operator:LinearOp | 5 | 1 | critic-b | 8125292319 | 27,330.9 | 27,154.8 | cudaEventSynchronize |
| planner_debate_L | mir_operator:RMSNormOp | 1 | 4 | critic-a | 11049591628 | 16,602.7 | 16,313.9 | cudaEventSynchronize |
| planner_debate_L | mir_operator:RMSNormOp | 2 | 5 | critic-a | 12117002851 | 16,601.7 | 16,318.9 | cudaEventSynchronize |
| planner_debate_L | mir_operator:RMSNormOp | 3 | 7 | critic-a | 14251357759 | 16,550.1 | 16,266.1 | cudaEventSynchronize |
| planner_debate_L | mir_operator:RMSNormOp | 4 | 0 | critic-a | 6709824649 | 16,534.7 | 16,255.7 | cudaEventSynchronize |
| planner_debate_L | mir_operator:RMSNormOp | 5 | 7 | critic-merge | 14732030464 | 16,532.8 | 16,268.7 | cudaEventSynchronize |
| react_moa_mcts_x3_L | host_input_generate | 1 | 4 | moa-map2#r2 | 54312857988 | 139,734.9 | 0.0 | cudaEventQuery |
| react_moa_mcts_x3_L | host_input_generate | 2 | 4 | moa-map1#r2 | 54050915669 | 138,736.2 | 0.0 | cudaEventQuery |
| react_moa_mcts_x3_L | host_input_generate | 3 | 4 | mcts-actor0#r2 | 54842152484 | 138,257.3 | 0.0 | cudaEventQuery |
| react_moa_mcts_x3_L | host_input_generate | 4 | 4 | mcts-actor0#r1 | 52528420976 | 137,386.2 | 0.0 | cudaEventQuery |
| react_moa_mcts_x3_L | host_input_generate | 5 | 5 | moa-map2#r2 | 61018162158 | 136,597.0 | 0.0 | cudaEventQuery |
| react_moa_mcts_x3_L | mir_operator:LinearOp | 1 | 2 | mcts-root#r1 | 39138416391 | 27,894.7 | 27,759.8 | cudaEventSynchronize |
| react_moa_mcts_x3_L | mir_operator:LinearOp | 2 | 3 | mcts-actor0#r1 | 45985826217 | 27,839.4 | 27,704.8 | cudaEventSynchronize |
| react_moa_mcts_x3_L | mir_operator:LinearOp | 3 | 6 | moa-map1#r1 | 65448198239 | 27,699.0 | 27,557.5 | cudaEventSynchronize |
| react_moa_mcts_x3_L | mir_operator:LinearOp | 4 | 1 | mcts-actor1#r1 | 33037257021 | 27,675.3 | 27,515.5 | cudaEventSynchronize |
| react_moa_mcts_x3_L | mir_operator:LinearOp | 5 | 6 | mcts-root#r0 | 63717942589 | 27,648.7 | 27,469.7 | cudaEventSynchronize |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | 1 | 0 | mcts-actor0#r2 | 28291970076 | 17,098.1 | 15,834.2 | cudaEventSynchronize |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | 2 | 2 | mcts-actor1#r0 | 37325149260 | 16,788.5 | 16,386.3 | cudaEventSynchronize |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | 3 | 4 | moa-map2#r2 | 54471609567 | 16,784.2 | 16,549.1 | cudaEventSynchronize |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | 4 | 6 | mcts-actor1#r0 | 64109589641 | 16,591.1 | 16,338.6 | cudaEventSynchronize |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | 5 | 7 | mcts-actor0#r1 | 72643495674 | 16,583.9 | 16,320.3 | cudaEventSynchronize |

### Host/GPU overlap and launch gaps, representative iteration (G07)

| workload | iter | wall (us) | GPU busy | host-only | streams | max concurrent GPU | gaps >= 20 us | gap total (us) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| react_tool_L | 5 | 237,874.8 | 40.69 % | 57.99 % | 1 | 1 | 19 | 72,415.7 |
| planner_debate_L | 1 | 1,080,047.8 | 49.93 % | 49.23 % | 1 | 1 | 52 | 445,002.0 |
| react_moa_mcts_x3_L | 6 | 6,606,114.8 | 50.34 % | 48.96 % | 1 | 1 | 315 | 3,196,730.7 |

Largest GPU launch gaps and the host processes covering them:

| workload | gap start (us) | gap (us) | next GPU item | host processes covering |
|---|---:|---:|---|---|
| react_moa_mcts_x3_L | 44074466.3 | 125,500.2 | mcts-critic#r1:h2d_stage:memcpy |  |
| react_moa_mcts_x3_L | 43416497.8 | 119,679.1 | mcts-actor1#r1:h2d_stage:memcpy |  |
| planner_debate_L | 1266525.3 | 118,954.0 | critic-a:h2d_stage:memcpy |  |
| react_moa_mcts_x3_L | 42934512.6 | 118,434.4 | mcts-root#r1:h2d_stage:memcpy |  |
| react_moa_mcts_x3_L | 41856238.3 | 117,843.0 | mcts-critic#r0:h2d_stage:memcpy |  |
| react_moa_mcts_x3_L | 42451522.0 | 117,450.5 | moa-map1#r1:h2d_stage:memcpy |  |
| react_moa_mcts_x3_L | 43176782.2 | 116,708.3 | mcts-actor0#r1:h2d_stage:memcpy |  |
| react_moa_mcts_x3_L | 40964251.8 | 116,348.8 | mcts-actor0#r0:h2d_stage:memcpy |  |
| planner_debate_L | 1507603.9 | 116,036.5 | critic-b:h2d_stage:memcpy |  |
| planner_debate_L | 1748394.8 | 115,769.5 | critic-merge:h2d_stage:memcpy |  |
| react_moa_mcts_x3_L | 45627151.3 | 115,662.4 | mcts-actor1#r2:h2d_stage:memcpy |  |
| react_moa_mcts_x3_L | 42694286.5 | 115,508.9 | moa-map2#r1:h2d_stage:memcpy |  |
| react_moa_mcts_x3_L | 43659176.9 | 115,239.7 | moa-reduce#r1:h2d_stage:memcpy |  |
| react_moa_mcts_x3_L | 44677868.9 | 114,794.1 | moa-map1#r2:h2d_stage:memcpy |  |
| react_moa_mcts_x3_L | 41203135.3 | 114,259.4 | mcts-actor1#r0:h2d_stage:memcpy |  |

### High-latency instances (median + 3 MAD per type): 418 total

| workload | process | iter | call | host (us) | median (us) | excess (us) | class |
|---|---|---:|---|---:|---:|---:|---|
| react_moa_mcts_x3_L | host_input_generate | 4 | moa-map2#r2 | 139,734.9 | 111,889.4 | 27,845.5 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 4 | moa-map1#r2 | 138,736.2 | 111,889.4 | 26,846.8 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 4 | mcts-actor0#r2 | 138,257.3 | 111,889.4 | 26,367.8 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 4 | mcts-actor0#r1 | 137,386.2 | 111,889.4 | 25,496.8 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 5 | moa-map2#r2 | 136,597.0 | 111,889.4 | 24,707.5 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 4 | mcts-root#r2 | 135,969.8 | 111,889.4 | 24,080.4 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 1 | moa-map0#r1 | 135,390.6 | 111,889.4 | 23,501.2 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 5 | mcts-actor0#r2 | 134,381.5 | 111,889.4 | 22,492.1 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 4 | moa-map2#r1 | 134,156.9 | 111,889.4 | 22,267.5 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 5 | mcts-root#r2 | 134,051.4 | 111,889.4 | 22,161.9 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 5 | moa-map1#r2 | 133,573.2 | 111,889.4 | 21,683.8 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 4 | moa-map1#r1 | 132,354.5 | 111,889.4 | 20,465.1 | sporadic |
| react_tool_L | host_input_generate | 6 | answer | 85,877.5 | 66,353.5 | 19,524.0 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 4 | mcts-root#r1 | 131,382.1 | 111,889.4 | 19,492.7 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 4 | moa-map0#r1 | 130,175.8 | 111,889.4 | 18,286.4 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 4 | mcts-actor0#r0 | 128,686.7 | 111,889.4 | 16,797.3 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 4 | mcts-actor1#r0 | 128,498.2 | 111,889.4 | 16,608.8 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 1 | moa-reduce#r0 | 127,586.8 | 111,889.4 | 15,697.3 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 4 | moa-reduce#r0 | 126,295.8 | 111,889.4 | 14,406.4 | sporadic |
| react_moa_mcts_x3_L | host_input_generate | 4 | mcts-root#r0 | 125,620.8 | 111,889.4 | 13,731.4 | sporadic |

## View B: resource window (G08)

Only rows with an attached hardware metric are shown with numbers; host-only processes are listed with their status so the coverage is explicit.

| workload | process | selected | share | status | family | SM % | Tensor % | DRAM active % | DRAM BW % peak | L2 % | occupancy % | waves/SM | interpretation |
|---|---|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| react_tool_L | dag_schedule_gap | False | 0.44 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool_L | adapter_dispatch | False | 0.99 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool_L | token_preprocess_cpu | False | 0.25 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool_L | host_input_generate | True | 56.13 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool_L | h2d_stage | False | 0.8 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool_L | h2d_stage | False | 0.8 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool_L | weight_init | False | 0.16 % | profiled | rng_init | 70.33 | 0.0 | 46.24 | 0.0 | 37.25 | 67.79 | 1.0 | SM-issue-bound |
| react_tool_L | weight_init | False | 0.16 % | profiled | elementwise_binary | 4.31 | 0.0 | 92.61 | 0.0 | 32.73 | 86.21 | 8.17 | DRAM-bandwidth-bound |
| react_tool_L | weight_init | False | 0.16 % | profiled | rng_init | 71.21 | 0.0 | 57.52 | 0.0 | 38.31 | 67.82 | 1.0 | SM-issue-bound |
| react_tool_L | weight_init | False | 0.16 % | profiled | elementwise_binary | 5.19 | 0.0 | 93.5 | 0.0 | 30.87 | 87.03 | 10.67 | DRAM-bandwidth-bound |
| react_tool_L | weight_init | False | 0.16 % | profiled | rng_init | 68.72 | 0.0 | 33.72 | 0.0 | 37.25 | 67.7 | 1.0 | SM-issue-bound |
| react_tool_L | weight_init | False | 0.16 % | profiled | elementwise_binary | 5.02 | 0.0 | 88.95 | 0.0 | 33.26 | 84.32 | 6.0 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:RMSNormOp | False | 7.31 % | profiled | copy | 5.31 | 0.0 | 89.5 | 0.0 | 35.76 | 86.92 | 8.17 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:RMSNormOp | False | 7.31 % | profiled | elementwise_unary | 0.96 | 0.0 | 47.22 | 0.0 | 14.99 | 42.45 | 4.08 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:RMSNormOp | False | 7.31 % | profiled | reduce | 2.2 | 0.0 | 90.15 | 0.0 | 34.1 | 58.18 | 0.58 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:RMSNormOp | False | 7.31 % | profiled | elementwise_binary | 7.31 | 0.0 | 46.99 | 0.0 | 14.25 | 47.73 | 16.34 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool_L | mir_operator:RMSNormOp | False | 7.31 % | profiled | copy | 11.18 | 0.0 | 91.08 | 0.0 | 32.38 | 87.72 | 10.67 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:RMSNormOp | False | 7.31 % | profiled | elementwise_unary | 0.89 | 0.0 | 47.39 | 0.0 | 14.06 | 42.57 | 5.33 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:RMSNormOp | False | 7.31 % | profiled | reduce | 2.03 | 0.0 | 90.49 | 0.0 | 30.77 | 66.11 | 0.67 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:RMSNormOp | False | 7.31 % | profiled | elementwise_binary | 7.13 | 0.0 | 47.16 | 0.0 | 13.87 | 48.51 | 21.34 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool_L | mir_operator:RMSNormOp | False | 7.31 % | profiled | copy | 12.59 | 0.0 | 88.06 | 0.0 | 37.8 | 87.67 | 6.0 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:RMSNormOp | False | 7.31 % | profiled | elementwise_unary | 1.0 | 0.0 | 46.99 | 0.0 | 15.64 | 42.21 | 3.0 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:RMSNormOp | False | 7.31 % | profiled | reduce | 2.33 | 0.0 | 87.86 | 0.0 | 34.25 | 49.89 | 0.5 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:RMSNormOp | False | 7.31 % | profiled | elementwise_binary | 7.57 | 0.0 | 46.48 | 0.0 | 14.52 | 47.05 | 12.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool_L | inter_operator_dispatch | False | 0.06 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool_L | mir_operator:AddOp | False | 0.48 % | profiled | elementwise_binary | 4.57 | 0.0 | 92.74 | 0.0 | 33.1 | 85.47 | 8.17 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:AddOp | False | 0.48 % | profiled | elementwise_binary | 5.48 | 0.0 | 93.5 | 0.0 | 31.08 | 87.59 | 10.67 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:AddOp | False | 0.48 % | profiled | elementwise_binary | 4.85 | 0.0 | 63.61 | 0.0 | 23.32 | 85.1 | 6.0 | DRAM-bandwidth-bound |
| react_tool_L | mir_operator:LinearOp | True | 28.66 % | profiled | gemm | 43.79 | 44.86 | 12.03 | 0.0 | 90.94 | 16.44 | 12.25 | tensor-core compute-bound |
| react_tool_L | mir_operator:LinearOp | True | 28.66 % | profiled | gemm | 48.8 | 49.01 | 16.72 | 0.0 | 54.36 | 16.35 | 12.0 | tensor-core compute-bound |
| react_tool_L | mir_operator:LinearOp | True | 28.66 % | profiled | gemm | 47.44 | 48.07 | 12.87 | 0.0 | 74.35 | 15.95 | 4.5 | tensor-core compute-bound |
| react_tool_L | mir_operator:ViewOp | False | 0.13 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool_L | mir_operator:TransposeOp | False | 3.55 % | profiled | copy | 6.19 | 0.0 | 22.7 | 0.0 | 91.87 | 88.33 | 16.33 | L2-bandwidth-bound (working set in L2) |
| react_tool_L | mir_operator:TransposeOp | False | 3.55 % | profiled | copy | 6.3 | 0.0 | 24.87 | 0.0 | 93.18 | 88.49 | 21.33 | L2-bandwidth-bound (working set in L2) |
| react_tool_L | mir_operator:TransposeOp | False | 3.55 % | profiled | copy | 6.12 | 0.0 | 20.34 | 0.0 | 90.91 | 87.69 | 12.0 | L2-bandwidth-bound (working set in L2) |
| react_tool_L | pre_d2h_alloc | False | 0.02 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool_L | d2h_stage | False | 0.76 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool_L | d2h_stage | False | 0.76 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool_L | checksum_complete | False | 0.07 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool_L | agent_tool_execute_cpu | False | 0.14 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_tool_L | iteration_tail_sync | False | 0.02 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate_L | dag_schedule_gap | False | 0.11 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate_L | adapter_dispatch | False | 0.48 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate_L | token_preprocess_cpu | False | 0.16 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate_L | host_input_generate | True | 48.2 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate_L | h2d_stage | False | 0.67 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate_L | h2d_stage | False | 0.67 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate_L | weight_init | False | 0.1 % | profiled | rng_init | 70.33 | 0.0 | 46.24 | 0.0 | 37.25 | 67.79 | 1.0 | SM-issue-bound |
| planner_debate_L | weight_init | False | 0.1 % | profiled | elementwise_binary | 4.31 | 0.0 | 92.61 | 0.0 | 32.73 | 86.21 | 8.17 | DRAM-bandwidth-bound |
| planner_debate_L | weight_init | False | 0.1 % | profiled | rng_init | 71.21 | 0.0 | 57.52 | 0.0 | 38.31 | 67.82 | 1.0 | SM-issue-bound |
| planner_debate_L | weight_init | False | 0.1 % | profiled | elementwise_binary | 5.19 | 0.0 | 93.5 | 0.0 | 30.87 | 87.03 | 10.67 | DRAM-bandwidth-bound |
| planner_debate_L | weight_init | False | 0.1 % | profiled | rng_init | 68.72 | 0.0 | 33.72 | 0.0 | 37.25 | 67.7 | 1.0 | SM-issue-bound |
| planner_debate_L | weight_init | False | 0.1 % | profiled | elementwise_binary | 5.02 | 0.0 | 88.95 | 0.0 | 33.26 | 84.32 | 6.0 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:RMSNormOp | True | 12.56 % | profiled | copy | 5.31 | 0.0 | 89.5 | 0.0 | 35.76 | 86.92 | 8.17 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:RMSNormOp | True | 12.56 % | profiled | elementwise_unary | 0.96 | 0.0 | 47.22 | 0.0 | 14.99 | 42.45 | 4.08 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:RMSNormOp | True | 12.56 % | profiled | reduce | 2.2 | 0.0 | 90.15 | 0.0 | 34.1 | 58.18 | 0.58 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:RMSNormOp | True | 12.56 % | profiled | elementwise_binary | 7.31 | 0.0 | 46.99 | 0.0 | 14.25 | 47.73 | 16.34 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate_L | mir_operator:RMSNormOp | True | 12.56 % | profiled | copy | 11.18 | 0.0 | 91.08 | 0.0 | 32.38 | 87.72 | 10.67 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:RMSNormOp | True | 12.56 % | profiled | elementwise_unary | 0.89 | 0.0 | 47.39 | 0.0 | 14.06 | 42.57 | 5.33 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:RMSNormOp | True | 12.56 % | profiled | reduce | 2.03 | 0.0 | 90.49 | 0.0 | 30.77 | 66.11 | 0.67 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:RMSNormOp | True | 12.56 % | profiled | elementwise_binary | 7.13 | 0.0 | 47.16 | 0.0 | 13.87 | 48.51 | 21.34 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate_L | mir_operator:RMSNormOp | True | 12.56 % | profiled | copy | 12.59 | 0.0 | 88.06 | 0.0 | 37.8 | 87.67 | 6.0 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:RMSNormOp | True | 12.56 % | profiled | elementwise_unary | 1.0 | 0.0 | 46.99 | 0.0 | 15.64 | 42.21 | 3.0 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:RMSNormOp | True | 12.56 % | profiled | reduce | 2.33 | 0.0 | 87.86 | 0.0 | 34.25 | 49.89 | 0.5 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:RMSNormOp | True | 12.56 % | profiled | elementwise_binary | 7.57 | 0.0 | 46.48 | 0.0 | 14.52 | 47.05 | 12.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate_L | inter_operator_dispatch | False | 0.05 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate_L | mir_operator:AddOp | False | 0.32 % | profiled | elementwise_binary | 4.57 | 0.0 | 92.74 | 0.0 | 33.1 | 85.47 | 8.17 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:AddOp | False | 0.32 % | profiled | elementwise_binary | 5.48 | 0.0 | 93.5 | 0.0 | 31.08 | 87.59 | 10.67 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:AddOp | False | 0.32 % | profiled | elementwise_binary | 4.85 | 0.0 | 63.61 | 0.0 | 23.32 | 85.1 | 6.0 | DRAM-bandwidth-bound |
| planner_debate_L | mir_operator:LinearOp | True | 33.39 % | profiled | gemm | 43.79 | 44.86 | 12.03 | 0.0 | 90.94 | 16.44 | 12.25 | tensor-core compute-bound |
| planner_debate_L | mir_operator:LinearOp | True | 33.39 % | profiled | gemm | 48.8 | 49.01 | 16.72 | 0.0 | 54.36 | 16.35 | 12.0 | tensor-core compute-bound |
| planner_debate_L | mir_operator:LinearOp | True | 33.39 % | profiled | gemm | 47.44 | 48.07 | 12.87 | 0.0 | 74.35 | 15.95 | 4.5 | tensor-core compute-bound |
| planner_debate_L | mir_operator:ViewOp | False | 0.08 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate_L | mir_operator:TransposeOp | False | 3.14 % | profiled | copy | 6.19 | 0.0 | 22.7 | 0.0 | 91.87 | 88.33 | 16.33 | L2-bandwidth-bound (working set in L2) |
| planner_debate_L | mir_operator:TransposeOp | False | 3.14 % | profiled | copy | 6.3 | 0.0 | 24.87 | 0.0 | 93.18 | 88.49 | 21.33 | L2-bandwidth-bound (working set in L2) |
| planner_debate_L | mir_operator:TransposeOp | False | 3.14 % | profiled | copy | 6.12 | 0.0 | 20.34 | 0.0 | 90.91 | 87.69 | 12.0 | L2-bandwidth-bound (working set in L2) |
| planner_debate_L | pre_d2h_alloc | False | 0.01 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate_L | d2h_stage | False | 0.65 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate_L | d2h_stage | False | 0.65 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate_L | checksum_complete | False | 0.04 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate_L | agent_tool_execute_cpu | False | 0.03 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| planner_debate_L | iteration_tail_sync | False | 0.01 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts_x3_L | dag_schedule_gap | False | 0.07 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts_x3_L | adapter_dispatch | False | 0.39 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts_x3_L | token_preprocess_cpu | False | 0.15 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts_x3_L | host_input_generate | True | 48.37 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts_x3_L | h2d_stage | False | 0.67 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_moa_mcts_x3_L | h2d_stage | False | 0.67 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_moa_mcts_x3_L | weight_init | False | 0.09 % | profiled | rng_init | 70.33 | 0.0 | 46.24 | 0.0 | 37.25 | 67.79 | 1.0 | SM-issue-bound |
| react_moa_mcts_x3_L | weight_init | False | 0.09 % | profiled | elementwise_binary | 4.31 | 0.0 | 92.61 | 0.0 | 32.73 | 86.21 | 8.17 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | weight_init | False | 0.09 % | profiled | rng_init | 71.21 | 0.0 | 57.52 | 0.0 | 38.31 | 67.82 | 1.0 | SM-issue-bound |
| react_moa_mcts_x3_L | weight_init | False | 0.09 % | profiled | elementwise_binary | 5.19 | 0.0 | 93.5 | 0.0 | 30.87 | 87.03 | 10.67 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | weight_init | False | 0.09 % | profiled | rng_init | 68.72 | 0.0 | 33.72 | 0.0 | 37.25 | 67.7 | 1.0 | SM-issue-bound |
| react_moa_mcts_x3_L | weight_init | False | 0.09 % | profiled | elementwise_binary | 5.02 | 0.0 | 88.95 | 0.0 | 33.26 | 84.32 | 6.0 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | True | 13.02 % | profiled | copy | 5.31 | 0.0 | 89.5 | 0.0 | 35.76 | 86.92 | 8.17 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | True | 13.02 % | profiled | elementwise_unary | 0.96 | 0.0 | 47.22 | 0.0 | 14.99 | 42.45 | 4.08 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | True | 13.02 % | profiled | reduce | 2.2 | 0.0 | 90.15 | 0.0 | 34.1 | 58.18 | 0.58 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | True | 13.02 % | profiled | elementwise_binary | 7.31 | 0.0 | 46.99 | 0.0 | 14.25 | 47.73 | 16.34 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | True | 13.02 % | profiled | copy | 11.18 | 0.0 | 91.08 | 0.0 | 32.38 | 87.72 | 10.67 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | True | 13.02 % | profiled | elementwise_unary | 0.89 | 0.0 | 47.39 | 0.0 | 14.06 | 42.57 | 5.33 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | True | 13.02 % | profiled | reduce | 2.03 | 0.0 | 90.49 | 0.0 | 30.77 | 66.11 | 0.67 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | True | 13.02 % | profiled | elementwise_binary | 7.13 | 0.0 | 47.16 | 0.0 | 13.87 | 48.51 | 21.34 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | True | 13.02 % | profiled | copy | 12.59 | 0.0 | 88.06 | 0.0 | 37.8 | 87.67 | 6.0 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | True | 13.02 % | profiled | elementwise_unary | 1.0 | 0.0 | 46.99 | 0.0 | 15.64 | 42.21 | 3.0 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | True | 13.02 % | profiled | reduce | 2.33 | 0.0 | 87.86 | 0.0 | 34.25 | 49.89 | 0.5 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:RMSNormOp | True | 13.02 % | profiled | elementwise_binary | 7.57 | 0.0 | 46.48 | 0.0 | 14.52 | 47.05 | 12.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_moa_mcts_x3_L | inter_operator_dispatch | False | 0.04 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts_x3_L | mir_operator:AddOp | False | 0.31 % | profiled | elementwise_binary | 4.57 | 0.0 | 92.74 | 0.0 | 33.1 | 85.47 | 8.17 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:AddOp | False | 0.31 % | profiled | elementwise_binary | 5.48 | 0.0 | 93.5 | 0.0 | 31.08 | 87.59 | 10.67 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:AddOp | False | 0.31 % | profiled | elementwise_binary | 4.85 | 0.0 | 63.61 | 0.0 | 23.32 | 85.1 | 6.0 | DRAM-bandwidth-bound |
| react_moa_mcts_x3_L | mir_operator:LinearOp | True | 32.98 % | profiled | gemm | 43.79 | 44.86 | 12.03 | 0.0 | 90.94 | 16.44 | 12.25 | tensor-core compute-bound |
| react_moa_mcts_x3_L | mir_operator:LinearOp | True | 32.98 % | profiled | gemm | 48.8 | 49.01 | 16.72 | 0.0 | 54.36 | 16.35 | 12.0 | tensor-core compute-bound |
| react_moa_mcts_x3_L | mir_operator:LinearOp | True | 32.98 % | profiled | gemm | 47.44 | 48.07 | 12.87 | 0.0 | 74.35 | 15.95 | 4.5 | tensor-core compute-bound |
| react_moa_mcts_x3_L | mir_operator:ViewOp | False | 0.07 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts_x3_L | mir_operator:TransposeOp | False | 3.14 % | profiled | copy | 6.19 | 0.0 | 22.7 | 0.0 | 91.87 | 88.33 | 16.33 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts_x3_L | mir_operator:TransposeOp | False | 3.14 % | profiled | copy | 6.3 | 0.0 | 24.87 | 0.0 | 93.18 | 88.49 | 21.33 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts_x3_L | mir_operator:TransposeOp | False | 3.14 % | profiled | copy | 6.12 | 0.0 | 20.34 | 0.0 | 90.91 | 87.69 | 12.0 | L2-bandwidth-bound (working set in L2) |
| react_moa_mcts_x3_L | pre_d2h_alloc | False | 0.01 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts_x3_L | d2h_stage | False | 0.64 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_moa_mcts_x3_L | d2h_stage | False | 0.64 % | not_collected_memcpy | memcpy |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_moa_mcts_x3_L | checksum_complete | False | 0.04 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts_x3_L | agent_tool_execute_cpu | False | 0.01 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |
| react_moa_mcts_x3_L | iteration_tail_sync | False | 0.0 % | not_collected_cpu_process |  |  |  |  |  |  |  |  | host-side Python/CPU segment; no GPU counters exist for it |

### Opportunities (derived, bounded by measured evidence)

| workload | opportunity | current per iter (us) | reference per iter (us) | bound (% of wall) | note |
|---|---|---:|---:|---:|---|
| react_tool_L | move_input_generation_to_device | 134,400.2 | 57.8 | 56.13 % | seeded CPU-generator uniform_ into pinned fp16 is single-threaded and O(n^2); device randn for the same n^2 is the weight_init GPU time |
| react_tool_L | remove_per_operator_synchronize | 96,118.9 | 93,172.7 | 1.23 % | each operator ends with cudaEventSynchronize; the host range minus GPU work is dispatch + sync latency that async launch would hide |
| react_tool_L | gpu_idle_window | 142,927.4 | 96,538.2 | 59.69 % | upper bound on wall reduction if all host work were overlapped or removed; single stream, no kernel concurrency observed |
| planner_debate_L | move_input_generation_to_device | 519,392.9 | 239.3 | 48.2 % | seeded CPU-generator uniform_ into pinned fp16 is single-threaded and O(n^2); device randn for the same n^2 is the weight_init GPU time |
| planner_debate_L | remove_per_operator_synchronize | 533,337.9 | 525,990.8 | 0.68 % | each operator ends with cudaEventSynchronize; the host range minus GPU work is dispatch + sync latency that async launch would hide |
| planner_debate_L | gpu_idle_window | 538,295.9 | 539,329.0 | 49.95 % | upper bound on wall reduction if all host work were overlapped or removed; single stream, no kernel concurrency observed |
| react_moa_mcts_x3_L | move_input_generation_to_device | 3,206,541.5 | 1,478.8 | 48.37 % | seeded CPU-generator uniform_ into pinned fp16 is single-threaded and O(n^2); device randn for the same n^2 is the weight_init GPU time |
| react_moa_mcts_x3_L | remove_per_operator_synchronize | 3,282,764.8 | 3,241,456.5 | 0.62 % | each operator ends with cudaEventSynchronize; the host range minus GPU work is dispatch + sync latency that async launch would hide |
| react_moa_mcts_x3_L | gpu_idle_window | 3,305,178.1 | 3,323,383.8 | 49.86 % | upper bound on wall reduction if all host work were overlapped or removed; single stream, no kernel concurrency observed |

## Tables (G09)

| table | rows | sha256 |
|---|---:|---|
| g06_selection_plan.csv | 51 | d4958e7c0f60d602… |
| g06_selected_stacks.csv | 40 | 184f5b10007311d4… |
| g06_global_ranking.csv | 51 | 7a5e7bdba5b7d3f9… |
| g06_denominators.csv | 3 | 2ed5cedd5b90443a… |
| g07_process_timeline_representative.csv | 901 | 3ea3f2edd0003da4… |
| g07_kernel_timeline_representative.csv | 25236 | 7faaa024311053de… |
| g07_launch_gaps.csv | 386 | cc649d3f25b4ca21… |
| g07_high_latency_instances.csv | 418 | d0689b3d7114ef7a… |
| g07_host_gpu_overlap.csv | 3 | 08ef59716877772a… |
| g08_resource_attachment.csv | 123 | f49c44c82b1699fd… |
| g08_opportunities.csv | 9 | 2201b36d82584fe5… |

Visible-range statement (G10): View A stacks show 5 instances per selected type; View B shows every process type but numbers only where a w03 family row attached.
Full per-instance evidence remains in the w01/w02 tables referenced by the admission ledger.

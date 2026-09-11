# G05 full-workload process estimate: `react_moa_mcts_x3_L` from react_tool_L + planner_debate_L

Lineage `h22-gpu-autotrace`, workflow w04. Instance counts come from the target plan; per-instance values are w02 medians of the
representative workloads keyed by (call kind, matrix size, process, op type). The target's own w01/w02 evidence is used only to score the estimate.

## Summary

| Quantity | Value |
|---|---:|
| Observed measured wall per iteration | 6,628,561.9 us |
| template_absolute host per iteration | 6,624,162.7 us (-0.07 %) |
| template_scaled conservation error | 0 ns |
| GPU work: template vs observed | 3,313,135.5 vs 3,323,383.8 us (-0.31 %) |
| Template keys covered / missing / nearest-size fallback | 45 / 0 / 0 |
| Instance-count mismatches (plan vs observed) | none |
| Max process error (processes >= 1 % of wall) | 1.0 % |
| Pass | True |

## Process-wise estimate vs observed (per iteration)

| process | n/iter (plan) | n/iter (obs) | template_absolute (us) | template_scaled (us) | observed (us) | abs err | scaled err | template share | observed share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| host_input_generate | 30 | 30 | 3,204,942.3 | 3,207,070.8 | 3,206,541.5 | -0.0 % | 0.0 % | 48.38 % | 48.37 % |
| mir_operator:LinearOp | 90 | 90 | 2,183,959.3 | 2,185,409.7 | 2,186,313.5 | -0.1 % | -0.0 % | 32.97 % | 32.98 % |
| mir_operator:RMSNormOp | 60 | 60 | 862,206.2 | 862,778.8 | 862,964.6 | -0.1 % | -0.0 % | 13.02 % | 13.02 % |
| mir_operator:TransposeOp | 30 | 30 | 206,206.1 | 206,343.1 | 208,210.0 | -1.0 % | -0.9 % | 3.11 % | 3.14 % |
| h2d_stage | 30 | 30 | 43,452.3 | 43,481.1 | 44,082.7 | -1.4 % | -1.4 % | 0.66 % | 0.67 % |
| d2h_stage | 30 | 30 | 42,569.5 | 42,597.8 | 42,679.3 | -0.3 % | -0.2 % | 0.64 % | 0.64 % |
| adapter_dispatch | 30 | 30 | 29,441.7 | 29,461.2 | 25,948.2 | 13.5 % | 13.5 % | 0.44 % | 0.39 % |
| mir_operator:AddOp | 30 | 30 | 21,652.7 | 21,667.0 | 20,568.4 | 5.3 % | 5.3 % | 0.33 % | 0.31 % |
| token_preprocess_cpu | 30 | 30 | 9,636.4 | 9,642.8 | 9,760.1 | -1.3 % | -1.2 % | 0.15 % | 0.15 % |
| weight_init | 30 | 30 | 5,981.0 | 5,985.0 | 5,635.0 | 6.1 % | 6.2 % | 0.09 % | 0.09 % |
| mir_operator:ViewOp | 30 | 30 | 5,017.0 | 5,020.4 | 4,708.2 | 6.6 % | 6.6 % | 0.08 % | 0.07 % |
| inter_operator_dispatch | 210 | 210 | 2,985.5 | 2,987.5 | 2,716.6 | 9.9 % | 10.0 % | 0.05 % | 0.04 % |
| checksum_complete | 30 | 30 | 2,664.1 | 2,665.9 | 2,478.7 | 7.5 % | 7.6 % | 0.04 % | 0.04 % |
| dag_schedule_gap | 33 | 33 | 1,670.9 | 1,672.0 | 4,326.3 | -61.4 % | -61.4 % | 0.03 % | 0.07 % |
| agent_tool_execute_cpu | 3 | 3 | 1,066.2 | 1,066.9 | 923.2 | 15.5 % | 15.6 % | 0.02 % | 0.01 % |
| pre_d2h_alloc | 30 | 30 | 653.5 | 653.9 | 629.4 | 3.8 % | 3.9 % | 0.01 % | 0.01 % |
| iteration_tail_sync | 1 | 1 | 57.9 | 58.0 | 76.1 | -23.9 % | -23.9 % | 0.0 % | 0.0 % |

## Call-wise estimate vs observed (per iteration)

| call | template_absolute (us) | template_scaled (us) | observed (us) | abs err | template GPU (us) | observed GPU (us) | GPU err |
|---|---:|---:|---:|---:|---:|---:|---:|
| <dag> | 1,728.8 | 1,730.0 | 4,402.5 | -60.7 % | 0.0 | 0.0 |  % |
| react-plan#r0 | 118,230.6 | 118,309.2 | 115,598.8 | 2.3 % | 48,442.1 | 48,296.6 | 0.3 % |
| moa-map0#r0 | 238,807.4 | 238,966.0 | 235,950.8 | 1.2 % | 121,185.1 | 121,903.8 | -0.6 % |
| moa-map1#r0 | 238,807.4 | 238,966.0 | 237,013.7 | 0.8 % | 121,185.1 | 121,452.8 | -0.2 % |
| moa-map2#r0 | 238,807.4 | 238,966.0 | 237,399.3 | 0.6 % | 121,185.1 | 121,802.6 | -0.5 % |
| mcts-root#r0 | 238,807.4 | 238,966.0 | 239,845.8 | -0.4 % | 121,185.1 | 121,467.7 | -0.2 % |
| react-tool#r0 | 355.4 | 355.6 | 307.9 | 15.4 % | 0.0 | 0.0 |  % |
| mcts-actor0#r0 | 238,807.4 | 238,966.0 | 239,704.6 | -0.4 % | 121,185.1 | 121,497.7 | -0.3 % |
| mcts-actor1#r0 | 238,807.4 | 238,966.0 | 238,690.7 | 0.0 % | 121,185.1 | 121,628.4 | -0.4 % |
| moa-reduce#r0 | 238,807.4 | 238,966.0 | 242,396.5 | -1.5 % | 121,185.1 | 121,666.4 | -0.4 % |
| react-answer#r0 | 178,432.7 | 178,551.2 | 176,754.7 | 0.9 % | 86,455.9 | 86,354.3 | 0.1 % |
| mcts-critic#r0 | 238,807.4 | 238,966.0 | 237,431.1 | 0.6 % | 121,185.1 | 121,708.8 | -0.4 % |
| react-plan#r1 | 118,230.6 | 118,309.2 | 118,406.8 | -0.1 % | 48,442.1 | 48,148.3 | 0.6 % |
| moa-map0#r1 | 238,807.4 | 238,966.0 | 242,478.3 | -1.5 % | 121,185.1 | 121,688.5 | -0.4 % |
| moa-map1#r1 | 238,807.4 | 238,966.0 | 241,722.5 | -1.2 % | 121,185.1 | 122,138.8 | -0.8 % |
| moa-map2#r1 | 238,807.4 | 238,966.0 | 239,562.5 | -0.3 % | 121,185.1 | 121,647.9 | -0.4 % |
| mcts-root#r1 | 238,807.4 | 238,966.0 | 240,810.7 | -0.8 % | 121,185.1 | 121,792.3 | -0.5 % |
| react-tool#r1 | 355.4 | 355.6 | 289.2 | 22.9 % | 0.0 | 0.0 |  % |
| mcts-actor0#r1 | 238,807.4 | 238,966.0 | 239,994.5 | -0.5 % | 121,185.1 | 121,526.8 | -0.3 % |
| mcts-actor1#r1 | 238,807.4 | 238,966.0 | 238,076.3 | 0.3 % | 121,185.1 | 121,611.6 | -0.4 % |
| moa-reduce#r1 | 238,807.4 | 238,966.0 | 237,364.1 | 0.6 % | 121,185.1 | 121,801.4 | -0.5 % |
| react-answer#r1 | 178,432.7 | 178,551.2 | 176,080.8 | 1.3 % | 86,455.9 | 86,721.0 | -0.3 % |
| mcts-critic#r1 | 238,807.4 | 238,966.0 | 239,695.9 | -0.4 % | 121,185.1 | 121,660.9 | -0.4 % |
| react-plan#r2 | 118,230.6 | 118,309.2 | 116,322.0 | 1.6 % | 48,442.1 | 48,161.6 | 0.6 % |
| moa-map0#r2 | 238,807.4 | 238,966.0 | 236,628.4 | 0.9 % | 121,185.1 | 121,175.5 | 0.0 % |
| moa-map1#r2 | 238,807.4 | 238,966.0 | 242,056.4 | -1.3 % | 121,185.1 | 121,195.7 | -0.0 % |
| moa-map2#r2 | 238,807.4 | 238,966.0 | 241,605.1 | -1.2 % | 121,185.1 | 121,474.3 | -0.2 % |
| mcts-root#r2 | 238,807.4 | 238,966.0 | 241,697.5 | -1.2 % | 121,185.1 | 121,610.0 | -0.3 % |
| react-tool#r2 | 355.4 | 355.6 | 326.1 | 9.0 % | 0.0 | 0.0 |  % |
| mcts-actor0#r2 | 238,807.4 | 238,966.0 | 243,509.1 | -1.9 % | 121,185.1 | 121,871.3 | -0.6 % |
| mcts-actor1#r2 | 238,807.4 | 238,966.0 | 237,630.6 | 0.5 % | 121,185.1 | 121,622.7 | -0.4 % |
| moa-reduce#r2 | 238,807.4 | 238,966.0 | 236,441.5 | 1.0 % | 121,185.1 | 121,741.2 | -0.5 % |
| react-answer#r2 | 178,432.7 | 178,551.2 | 176,565.4 | 1.1 % | 86,455.9 | 86,651.2 | -0.2 % |
| mcts-critic#r2 | 238,807.4 | 238,966.0 | 235,801.9 | 1.3 % | 121,185.1 | 121,364.0 | -0.1 % |

## Constraints honoured

- `template_absolute` is a prediction; `template_scaled` is conserved to the w01 measured wall and is not a direct trace.
- Representative absolute latencies are never reported as target latencies without the matrix-size key matching.
- w03 hardware attributes do not enter this denominator.

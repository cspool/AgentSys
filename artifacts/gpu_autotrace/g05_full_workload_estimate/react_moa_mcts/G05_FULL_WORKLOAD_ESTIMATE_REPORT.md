# G05 full-workload process estimate: `react_moa_mcts` from react_tool + planner_debate

Lineage `h22-gpu-autotrace`, workflow w04. Instance counts come from the target plan; per-instance values are w02 medians of the
representative workloads keyed by (call kind, matrix size, process, op type). The target's own w01/w02 evidence is used only to score the estimate.

## Summary

| Quantity | Value |
|---|---:|
| Observed measured wall per iteration | 135,014.8 us |
| template_absolute host per iteration | 120,692.5 us (-10.61 %) |
| template_scaled conservation error | 0 ns |
| GPU work: template vs observed | 4,053.2 vs 3,356.2 us (+20.77 %) |
| Template keys covered / missing / nearest-size fallback | 45 / 0 / 0 |
| Instance-count mismatches (plan vs observed) | none |
| Max process error (processes >= 1 % of wall) | 68.0 % |
| Pass | True |

## Process-wise estimate vs observed (per iteration)

| process | n/iter (plan) | n/iter (obs) | template_absolute (us) | template_scaled (us) | observed (us) | abs err | scaled err | template share | observed share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| host_input_generate | 10 | 10 | 85,335.9 | 95,462.6 | 100,831.2 | -15.4 % | -5.3 % | 70.71 % | 74.68 % |
| adapter_dispatch | 10 | 10 | 11,893.3 | 13,304.7 | 11,788.2 | 0.9 % | 12.9 % | 9.85 % | 8.73 % |
| mir_operator:RMSNormOp | 20 | 20 | 5,363.1 | 5,999.6 | 4,871.8 | 10.1 % | 23.1 % | 4.44 % | 3.61 % |
| mir_operator:LinearOp | 30 | 30 | 3,326.6 | 3,721.4 | 3,351.9 | -0.8 % | 11.0 % | 2.76 % | 2.48 % |
| token_preprocess_cpu | 10 | 10 | 3,090.6 | 3,457.4 | 2,955.9 | 4.6 % | 17.0 % | 2.56 % | 2.19 % |
| h2d_stage | 10 | 10 | 2,508.8 | 2,806.5 | 2,008.4 | 24.9 % | 39.7 % | 2.08 % | 1.49 % |
| d2h_stage | 10 | 10 | 2,078.7 | 2,325.3 | 1,635.6 | 27.1 % | 42.2 % | 1.72 % | 1.21 % |
| weight_init | 10 | 10 | 1,652.4 | 1,848.5 | 1,411.1 | 17.1 % | 31.0 % | 1.37 % | 1.05 % |
| mir_operator:TransposeOp | 10 | 10 | 1,291.9 | 1,445.3 | 1,200.9 | 7.6 % | 20.4 % | 1.07 % | 0.89 % |
| mir_operator:AddOp | 10 | 10 | 1,041.4 | 1,164.9 | 1,025.0 | 1.6 % | 13.7 % | 0.86 % | 0.76 % |
| checksum_complete | 10 | 10 | 771.7 | 863.3 | 654.5 | 17.9 % | 31.9 % | 0.64 % | 0.48 % |
| mir_operator:ViewOp | 10 | 10 | 755.2 | 844.8 | 715.8 | 5.5 % | 18.0 % | 0.63 % | 0.53 % |
| inter_operator_dispatch | 70 | 70 | 567.5 | 634.9 | 563.0 | 0.8 % | 12.8 % | 0.47 % | 0.42 % |
| dag_schedule_gap | 11 | 11 | 475.3 | 531.7 | 1,485.7 | -68.0 % | -64.2 % | 0.39 % | 1.1 % |
| agent_tool_execute_cpu | 1 | 1 | 338.5 | 378.6 | 324.7 | 4.2 % | 16.6 % | 0.28 % | 0.24 % |
| pre_d2h_alloc | 10 | 10 | 138.6 | 155.1 | 129.2 | 7.3 % | 20.1 % | 0.11 % | 0.1 % |
| iteration_tail_sync | 1 | 1 | 62.9 | 70.4 | 61.9 | 1.6 % | 13.7 % | 0.05 % | 0.05 % |

## Call-wise estimate vs observed (per iteration)

| call | template_absolute (us) | template_scaled (us) | observed (us) | abs err | template GPU (us) | observed GPU (us) | GPU err |
|---|---:|---:|---:|---:|---:|---:|---:|
| <dag> | 538.2 | 602.1 | 1,547.6 | -65.2 % | 0.0 | 0.0 |  % |
| react-plan | 8,329.4 | 9,317.9 | 10,088.7 | -17.4 % | 257.0 | 213.3 | 20.5 % |
| moa-map0 | 12,624.3 | 14,122.4 | 13,965.3 | -9.6 % | 432.0 | 350.2 | 23.4 % |
| moa-map1 | 12,624.3 | 14,122.4 | 13,867.4 | -9.0 % | 432.0 | 355.2 | 21.6 % |
| moa-map2 | 12,624.3 | 14,122.4 | 13,916.5 | -9.3 % | 432.0 | 353.3 | 22.3 % |
| mcts-root | 12,624.3 | 14,122.4 | 13,881.1 | -9.1 % | 432.0 | 352.6 | 22.5 % |
| react-tool | 338.5 | 378.6 | 324.7 | 4.2 % | 0.0 | 0.0 |  % |
| mcts-actor0 | 12,624.3 | 14,122.4 | 14,217.6 | -11.2 % | 432.0 | 366.7 | 17.8 % |
| mcts-actor1 | 12,624.3 | 14,122.4 | 13,829.7 | -8.7 % | 432.0 | 367.4 | 17.6 % |
| moa-reduce | 12,624.3 | 14,122.4 | 13,917.7 | -9.3 % | 432.0 | 354.3 | 21.9 % |
| react-answer | 10,491.9 | 11,736.9 | 11,624.6 | -9.7 % | 339.8 | 277.4 | 22.5 % |
| mcts-critic | 12,624.3 | 14,122.4 | 13,833.8 | -8.7 % | 432.0 | 365.8 | 18.1 % |

## Constraints honoured

- `template_absolute` is a prediction; `template_scaled` is conserved to the w01 measured wall and is not a direct trace.
- Representative absolute latencies are never reported as target latencies without the matrix-size key matching.
- w03 hardware attributes do not enter this denominator.

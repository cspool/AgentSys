# G05 full-workload process estimate: `react_moa_mcts` from react_tool + planner_debate

Lineage `h22-gpu-autotrace`, workflow w04. Instance counts come from the target plan; per-instance values are w02 medians of the
representative workloads keyed by (call kind, matrix size, process, op type). The target's own w01/w02 evidence is used only to score the estimate.

## Summary

| Quantity | Value |
|---|---:|
| Observed measured wall per iteration | 29,514,270.5 us |
| template_absolute host per iteration | 30,581,795.3 us (+3.62 %) |
| template_scaled conservation error | 0 ns |
| GPU work: template vs observed | 5,633,105.8 vs 5,755,853.6 us (-2.13 %) |
| Template keys covered / missing / nearest-size fallback | 216 / 0 / 0 |
| Instance-count mismatches (plan vs observed) | none |
| Max process error (processes >= 1 % of wall) | 49.7 % |
| Pass | True |

## Process-wise estimate vs observed (per iteration)

| process | n/iter (plan) | n/iter (obs) | template_absolute (us) | template_scaled (us) | observed (us) | abs err | scaled err | template share | observed share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| mir_operator:decode_layer00 | 850 | 850 | 1,086,832.7 | 1,048,894.4 | 1,028,277.1 | 5.7 % | 2.0 % | 3.55 % | 3.48 % |
| mir_operator:decode_layer01 | 850 | 850 | 1,045,039.5 | 1,008,560.1 | 987,185.6 | 5.9 % | 2.2 % | 3.42 % | 3.34 % |
| mir_operator:decode_layer02 | 850 | 850 | 1,036,297.0 | 1,000,122.8 | 978,440.2 | 5.9 % | 2.2 % | 3.39 % | 3.32 % |
| mir_operator:decode_layer03 | 850 | 850 | 1,031,523.0 | 995,515.4 | 974,419.4 | 5.9 % | 2.2 % | 3.37 % | 3.3 % |
| mir_operator:decode_layer04 | 850 | 850 | 1,029,488.6 | 993,552.0 | 973,643.6 | 5.7 % | 2.0 % | 3.37 % | 3.3 % |
| mir_operator:decode_layer05 | 850 | 850 | 1,028,916.5 | 993,000.0 | 971,236.6 | 5.9 % | 2.2 % | 3.36 % | 3.29 % |
| mir_operator:decode_layer08 | 850 | 850 | 1,028,732.2 | 992,822.0 | 968,198.5 | 6.3 % | 2.5 % | 3.36 % | 3.28 % |
| mir_operator:decode_layer06 | 850 | 850 | 1,028,671.7 | 992,763.7 | 969,270.5 | 6.1 % | 2.4 % | 3.36 % | 3.28 % |
| mir_operator:decode_layer11 | 850 | 850 | 1,028,006.1 | 992,121.3 | 966,467.3 | 6.4 % | 2.7 % | 3.36 % | 3.27 % |
| mir_operator:decode_layer09 | 850 | 850 | 1,027,412.7 | 991,548.6 | 969,678.3 | 6.0 % | 2.3 % | 3.36 % | 3.29 % |
| mir_operator:decode_layer10 | 850 | 850 | 1,027,194.9 | 991,338.4 | 967,651.2 | 6.2 % | 2.4 % | 3.36 % | 3.28 % |
| mir_operator:decode_layer20 | 850 | 850 | 1,027,031.5 | 991,180.7 | 965,391.1 | 6.4 % | 2.7 % | 3.36 % | 3.27 % |
| mir_operator:decode_layer07 | 850 | 850 | 1,026,846.3 | 991,002.0 | 969,090.5 | 6.0 % | 2.3 % | 3.36 % | 3.28 % |
| mir_operator:decode_layer14 | 850 | 850 | 1,026,037.1 | 990,221.0 | 970,245.2 | 5.8 % | 2.1 % | 3.36 % | 3.29 % |
| mir_operator:decode_layer24 | 850 | 850 | 1,025,991.4 | 990,176.9 | 967,872.7 | 6.0 % | 2.3 % | 3.35 % | 3.28 % |
| mir_operator:decode_layer12 | 850 | 850 | 1,025,923.6 | 990,111.5 | 965,561.3 | 6.3 % | 2.5 % | 3.35 % | 3.27 % |
| mir_operator:decode_layer18 | 850 | 850 | 1,025,860.1 | 990,050.2 | 965,836.6 | 6.2 % | 2.5 % | 3.35 % | 3.27 % |
| mir_operator:decode_layer19 | 850 | 850 | 1,025,364.1 | 989,571.5 | 966,414.4 | 6.1 % | 2.4 % | 3.35 % | 3.27 % |
| mir_operator:decode_layer27 | 850 | 850 | 1,025,285.9 | 989,496.0 | 967,680.1 | 6.0 % | 2.3 % | 3.35 % | 3.28 % |
| mir_operator:decode_layer16 | 850 | 850 | 1,025,213.4 | 989,426.1 | 965,740.5 | 6.2 % | 2.5 % | 3.35 % | 3.27 % |
| mir_operator:decode_layer21 | 850 | 850 | 1,024,931.4 | 989,154.0 | 966,623.4 | 6.0 % | 2.3 % | 3.35 % | 3.28 % |
| mir_operator:decode_layer23 | 850 | 850 | 1,024,794.7 | 989,022.0 | 967,409.1 | 5.9 % | 2.2 % | 3.35 % | 3.28 % |
| mir_operator:decode_layer26 | 850 | 850 | 1,024,794.4 | 989,021.7 | 969,902.7 | 5.7 % | 2.0 % | 3.35 % | 3.29 % |
| mir_operator:decode_layer13 | 850 | 850 | 1,024,702.7 | 988,933.2 | 966,262.2 | 6.0 % | 2.3 % | 3.35 % | 3.27 % |
| mir_operator:decode_layer17 | 850 | 850 | 1,023,916.2 | 988,174.1 | 966,170.8 | 6.0 % | 2.3 % | 3.35 % | 3.27 % |
| mir_operator:decode_layer15 | 850 | 850 | 1,023,734.3 | 987,998.6 | 966,828.3 | 5.9 % | 2.2 % | 3.35 % | 3.28 % |
| mir_operator:decode_layer22 | 850 | 850 | 1,023,116.2 | 987,402.1 | 969,024.0 | 5.6 % | 1.9 % | 3.35 % | 3.28 % |
| mir_operator:decode_layer25 | 850 | 850 | 1,021,204.7 | 985,557.3 | 969,017.6 | 5.4 % | 1.7 % | 3.34 % | 3.28 % |
| inter_operator_dispatch | 26650 | 26650 | 570,535.5 | 550,619.7 | 1,134,999.9 | -49.7 % | -51.5 % | 1.87 % | 3.85 % |
| mir_operator:decode_sample | 850 | 850 | 524,372.3 | 506,067.9 | 531,610.5 | -1.4 % | -4.8 % | 1.71 % | 1.8 % |
| mir_operator:decode_head | 850 | 850 | 205,637.9 | 198,459.6 | 191,980.5 | 7.1 % | 3.4 % | 0.67 % | 0.65 % |
| mir_operator:decode_embed | 850 | 850 | 48,592.7 | 46,896.5 | 43,207.5 | 12.5 % | 8.5 % | 0.16 % | 0.15 % |
| mir_operator:prefill_sample | 10 | 10 | 18,160.8 | 17,526.8 | 21,783.6 | -16.6 % | -19.5 % | 0.06 % | 0.07 % |
| token_preprocess_cpu | 10 | 10 | 16,473.3 | 15,898.3 | 14,084.4 | 17.0 % | 12.9 % | 0.05 % | 0.05 % |
| mir_operator:prefill_layer00 | 10 | 10 | 15,017.8 | 14,493.5 | 13,992.2 | 7.3 % | 3.6 % | 0.05 % | 0.05 % |
| mir_operator:prefill_layer01 | 10 | 10 | 13,851.9 | 13,368.4 | 12,970.1 | 6.8 % | 3.1 % | 0.05 % | 0.04 % |
| mir_operator:prefill_layer02 | 10 | 10 | 13,401.7 | 12,933.9 | 12,739.0 | 5.2 % | 1.5 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer03 | 10 | 10 | 13,308.2 | 12,843.6 | 12,610.0 | 5.5 % | 1.9 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer15 | 10 | 10 | 12,933.7 | 12,482.2 | 12,482.7 | 3.6 % | -0.0 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer14 | 10 | 10 | 12,915.4 | 12,464.5 | 12,503.9 | 3.3 % | -0.3 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer09 | 10 | 10 | 12,878.8 | 12,429.3 | 12,528.5 | 2.8 % | -0.8 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer12 | 10 | 10 | 12,874.9 | 12,425.5 | 12,507.0 | 2.9 % | -0.7 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer13 | 10 | 10 | 12,865.2 | 12,416.1 | 12,465.6 | 3.2 % | -0.4 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer21 | 10 | 10 | 12,860.6 | 12,411.7 | 12,388.2 | 3.8 % | 0.2 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer17 | 10 | 10 | 12,830.6 | 12,382.7 | 12,441.3 | 3.1 % | -0.5 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer18 | 10 | 10 | 12,820.7 | 12,373.2 | 12,438.4 | 3.1 % | -0.5 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer22 | 10 | 10 | 12,808.3 | 12,361.2 | 12,342.6 | 3.8 % | 0.2 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer20 | 10 | 10 | 12,802.2 | 12,355.4 | 12,400.1 | 3.2 % | -0.4 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer04 | 10 | 10 | 12,777.9 | 12,331.9 | 12,526.0 | 2.0 % | -1.6 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer25 | 10 | 10 | 12,748.0 | 12,303.0 | 12,438.9 | 2.5 % | -1.1 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer16 | 10 | 10 | 12,745.4 | 12,300.5 | 12,540.9 | 1.6 % | -1.9 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer11 | 10 | 10 | 12,738.3 | 12,293.6 | 12,418.5 | 2.6 % | -1.0 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer19 | 10 | 10 | 12,700.8 | 12,257.4 | 12,404.9 | 2.4 % | -1.2 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer26 | 10 | 10 | 12,674.0 | 12,231.6 | 12,429.2 | 2.0 % | -1.6 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer27 | 10 | 10 | 12,651.8 | 12,210.1 | 12,428.2 | 1.8 % | -1.8 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer24 | 10 | 10 | 12,626.3 | 12,185.6 | 12,608.4 | 0.1 % | -3.4 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer05 | 10 | 10 | 12,531.5 | 12,094.0 | 12,423.0 | 0.9 % | -2.6 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer07 | 10 | 10 | 12,428.2 | 11,994.3 | 12,495.8 | -0.5 % | -4.0 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer06 | 10 | 10 | 12,425.3 | 11,991.6 | 12,416.4 | 0.1 % | -3.4 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer08 | 10 | 10 | 12,400.1 | 11,967.2 | 12,511.5 | -0.9 % | -4.4 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer10 | 10 | 10 | 12,340.5 | 11,909.8 | 12,511.0 | -1.4 % | -4.8 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer23 | 10 | 10 | 12,332.4 | 11,901.9 | 12,412.1 | -0.6 % | -4.1 % | 0.04 % | 0.04 % |
| pre_d2h_alloc | 10 | 10 | 3,823.5 | 3,690.1 | 13,970.3 | -72.6 % | -73.6 % | 0.01 % | 0.05 % |
| mir_operator:prefill_head | 10 | 10 | 2,529.8 | 2,441.5 | 2,456.7 | 3.0 % | -0.6 % | 0.01 % | 0.01 % |
| weight_init | 10 | 10 | 1,899.2 | 1,832.9 | 1,588.5 | 19.6 % | 15.4 % | 0.01 % | 0.01 % |
| host_input_generate | 10 | 10 | 1,366.0 | 1,318.3 | 1,285.9 | 6.2 % | 2.5 % | 0.0 % | 0.0 % |
| d2h_stage | 10 | 10 | 1,309.9 | 1,264.2 | 1,289.2 | 1.6 % | -1.9 % | 0.0 % | 0.0 % |
| h2d_stage | 10 | 10 | 1,096.2 | 1,058.0 | 1,053.9 | 4.0 % | 0.4 % | 0.0 % | 0.0 % |
| mir_operator:prefill_embed | 10 | 10 | 992.8 | 958.1 | 883.3 | 12.4 % | 8.5 % | 0.0 % | 0.0 % |
| dag_schedule_gap | 11 | 11 | 898.9 | 867.5 | 2,143.8 | -58.1 % | -59.5 % | 0.0 % | 0.01 % |
| checksum_complete | 10 | 10 | 483.4 | 466.5 | 472.3 | 2.4 % | -1.2 % | 0.0 % | 0.0 % |
| agent_tool_execute_cpu | 1 | 1 | 291.0 | 280.8 | 361.6 | -19.5 % | -22.3 % | 0.0 % | 0.0 % |
| iteration_tail_sync | 1 | 1 | 137.7 | 132.9 | 129.6 | 6.2 % | 2.5 % | 0.0 % | 0.0 % |
| adapter_dispatch | 10 | 10 | 40.6 | 39.2 | 55.7 | -27.0 % | -29.6 % | 0.0 % | 0.0 % |

## Call-wise estimate vs observed (per iteration)

| call | template_absolute (us) | template_scaled (us) | observed (us) | abs err | template GPU (us) | observed GPU (us) | GPU err |
|---|---:|---:|---:|---:|---:|---:|---:|
| <dag> | 1,036.6 | 1,000.4 | 2,273.4 | -54.4 % | 0.0 | 0.0 |  % |
| react-plan | 2,683,925.5 | 2,590,237.2 | 2,675,373.3 | 0.3 % | 498,901.6 | 508,882.7 | -2.0 % |
| moa-map0 | 3,206,002.8 | 3,094,090.3 | 3,115,890.9 | 2.9 % | 591,552.0 | 600,034.4 | -1.4 % |
| moa-map1 | 3,419,319.6 | 3,299,960.7 | 3,290,971.8 | 3.9 % | 630,265.9 | 640,959.5 | -1.7 % |
| moa-map2 | 3,099,344.5 | 2,991,155.0 | 3,006,334.2 | 3.1 % | 572,195.0 | 582,507.1 | -1.8 % |
| mcts-root | 3,028,238.9 | 2,922,531.6 | 2,921,390.9 | 3.7 % | 559,290.4 | 573,305.1 | -2.4 % |
| react-tool | 291.0 | 280.8 | 361.6 | -19.5 % | 0.0 | 0.0 |  % |
| mcts-actor0 | 3,170,450.0 | 3,059,778.5 | 3,053,355.9 | 3.8 % | 585,099.7 | 600,346.6 | -2.5 % |
| mcts-actor1 | 2,886,027.7 | 2,785,284.6 | 2,792,846.7 | 3.3 % | 533,481.1 | 547,347.4 | -2.5 % |
| moa-reduce | 3,312,661.2 | 3,197,025.5 | 3,183,471.5 | 4.1 % | 610,909.0 | 627,829.0 | -2.7 % |
| react-answer | 2,746,258.6 | 2,650,394.4 | 2,589,744.6 | 6.0 % | 492,120.6 | 498,661.9 | -1.3 % |
| mcts-critic | 3,028,238.9 | 2,922,531.6 | 2,882,255.8 | 5.1 % | 559,290.4 | 575,979.8 | -2.9 % |

## Constraints honoured

- `template_absolute` is a prediction; `template_scaled` is conserved to the w01 measured wall and is not a direct trace.
- Representative absolute latencies are never reported as target latencies without the matrix-size key matching.
- w03 hardware attributes do not enter this denominator.

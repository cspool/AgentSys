# G05 full-workload process estimate: `react_moa_mcts` from react_tool + planner_debate

Lineage `h22-gpu-autotrace`, workflow w04. Instance counts come from the target plan; per-instance values are w02 medians of the
representative workloads keyed by (call kind, matrix size, process, op type). The target's own w01/w02 evidence is used only to score the estimate.

## Summary

| Quantity | Value |
|---|---:|
| Observed measured wall per iteration | 33,835,123.4 us |
| template_absolute host per iteration | 32,809,904.3 us (-3.03 %) |
| template_scaled conservation error | -0 ns |
| GPU work: template vs observed | 8,089,493.8 vs 8,197,214.7 us (-1.31 %) |
| Template keys covered / missing / nearest-size fallback | 264 / 0 / 0 |
| Instance-count mismatches (plan vs observed) | none |
| Max process error (processes >= 1 % of wall) | 47.6 % |
| Pass | True |

## Process-wise estimate vs observed (per iteration)

| process | n/iter (plan) | n/iter (obs) | template_absolute (us) | template_scaled (us) | observed (us) | abs err | scaled err | template share | observed share |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| mir_operator:decode_layer00 | 850 | 850 | 906,985.0 | 935,325.8 | 914,891.0 | -0.9 % | 2.2 % | 2.76 % | 2.7 % |
| mir_operator:decode_layer01 | 850 | 850 | 874,607.2 | 901,936.3 | 883,078.2 | -1.0 % | 2.1 % | 2.67 % | 2.61 % |
| mir_operator:decode_layer02 | 850 | 850 | 864,350.9 | 891,359.5 | 874,841.3 | -1.2 % | 1.9 % | 2.63 % | 2.59 % |
| mir_operator:decode_layer03 | 850 | 850 | 861,609.5 | 888,532.5 | 869,017.9 | -0.9 % | 2.2 % | 2.63 % | 2.57 % |
| mir_operator:decode_layer04 | 850 | 850 | 858,979.7 | 885,820.5 | 868,611.2 | -1.1 % | 2.0 % | 2.62 % | 2.57 % |
| mir_operator:decode_layer05 | 850 | 850 | 857,820.1 | 884,624.6 | 868,303.5 | -1.2 % | 1.9 % | 2.61 % | 2.57 % |
| mir_operator:decode_layer07 | 850 | 850 | 857,176.5 | 883,960.9 | 865,759.4 | -1.0 % | 2.1 % | 2.61 % | 2.56 % |
| mir_operator:decode_layer06 | 850 | 850 | 856,752.5 | 883,523.6 | 867,187.1 | -1.2 % | 1.9 % | 2.61 % | 2.56 % |
| mir_operator:decode_layer08 | 850 | 850 | 856,271.7 | 883,027.8 | 864,418.1 | -0.9 % | 2.2 % | 2.61 % | 2.55 % |
| mir_operator:decode_layer11 | 850 | 850 | 855,308.9 | 882,035.0 | 862,066.4 | -0.8 % | 2.3 % | 2.61 % | 2.55 % |
| mir_operator:decode_layer27 | 850 | 850 | 855,161.6 | 881,883.0 | 861,989.9 | -0.8 % | 2.3 % | 2.61 % | 2.55 % |
| mir_operator:decode_layer09 | 850 | 850 | 854,978.7 | 881,694.4 | 863,351.7 | -1.0 % | 2.1 % | 2.61 % | 2.55 % |
| mir_operator:decode_layer25 | 850 | 850 | 854,936.0 | 881,650.4 | 863,631.4 | -1.0 % | 2.1 % | 2.61 % | 2.55 % |
| mir_operator:decode_layer18 | 850 | 850 | 854,935.6 | 881,650.0 | 860,872.8 | -0.7 % | 2.4 % | 2.61 % | 2.54 % |
| mir_operator:decode_layer21 | 850 | 850 | 854,871.5 | 881,583.9 | 862,467.9 | -0.9 % | 2.2 % | 2.61 % | 2.55 % |
| mir_operator:decode_layer19 | 850 | 850 | 854,738.9 | 881,447.2 | 862,768.0 | -0.9 % | 2.2 % | 2.61 % | 2.55 % |
| mir_operator:decode_layer16 | 850 | 850 | 854,715.8 | 881,423.3 | 862,374.8 | -0.9 % | 2.2 % | 2.61 % | 2.55 % |
| mir_operator:decode_layer34 | 850 | 850 | 854,567.6 | 881,270.5 | 861,595.5 | -0.8 % | 2.3 % | 2.6 % | 2.55 % |
| mir_operator:decode_layer35 | 850 | 850 | 854,480.4 | 881,180.5 | 861,031.4 | -0.8 % | 2.3 % | 2.6 % | 2.54 % |
| mir_operator:decode_layer10 | 850 | 850 | 854,428.4 | 881,126.9 | 864,093.7 | -1.1 % | 2.0 % | 2.6 % | 2.55 % |
| mir_operator:decode_layer24 | 850 | 850 | 854,326.9 | 881,022.3 | 862,621.4 | -1.0 % | 2.1 % | 2.6 % | 2.55 % |
| mir_operator:decode_layer29 | 850 | 850 | 854,318.1 | 881,013.2 | 861,553.2 | -0.8 % | 2.3 % | 2.6 % | 2.55 % |
| mir_operator:decode_layer32 | 850 | 850 | 854,241.1 | 880,933.8 | 860,976.3 | -0.8 % | 2.3 % | 2.6 % | 2.54 % |
| mir_operator:decode_layer28 | 850 | 850 | 854,184.0 | 880,874.8 | 862,378.8 | -1.0 % | 2.1 % | 2.6 % | 2.55 % |
| mir_operator:decode_layer12 | 850 | 850 | 854,009.2 | 880,694.6 | 861,119.3 | -0.8 % | 2.3 % | 2.6 % | 2.55 % |
| mir_operator:decode_layer20 | 850 | 850 | 853,992.6 | 880,677.5 | 863,153.6 | -1.1 % | 2.0 % | 2.6 % | 2.55 % |
| mir_operator:decode_layer14 | 850 | 850 | 853,946.1 | 880,629.6 | 861,665.5 | -0.9 % | 2.2 % | 2.6 % | 2.55 % |
| mir_operator:decode_layer26 | 850 | 850 | 853,892.8 | 880,574.6 | 863,389.1 | -1.1 % | 2.0 % | 2.6 % | 2.55 % |
| mir_operator:decode_layer17 | 850 | 850 | 853,646.1 | 880,320.2 | 861,187.7 | -0.9 % | 2.2 % | 2.6 % | 2.55 % |
| mir_operator:decode_layer15 | 850 | 850 | 853,626.1 | 880,299.5 | 926,238.6 | -7.8 % | -5.0 % | 2.6 % | 2.74 % |
| mir_operator:decode_layer13 | 850 | 850 | 853,589.8 | 880,262.1 | 860,815.5 | -0.8 % | 2.3 % | 2.6 % | 2.54 % |
| mir_operator:decode_layer23 | 850 | 850 | 853,571.2 | 880,242.9 | 860,687.9 | -0.8 % | 2.3 % | 2.6 % | 2.54 % |
| mir_operator:decode_layer33 | 850 | 850 | 853,278.0 | 879,940.6 | 861,110.9 | -0.9 % | 2.2 % | 2.6 % | 2.55 % |
| mir_operator:decode_layer22 | 850 | 850 | 853,188.3 | 879,848.0 | 861,062.2 | -0.9 % | 2.2 % | 2.6 % | 2.54 % |
| mir_operator:decode_layer31 | 850 | 850 | 853,007.0 | 879,661.1 | 861,019.1 | -0.9 % | 2.2 % | 2.6 % | 2.54 % |
| mir_operator:decode_layer30 | 850 | 850 | 852,146.6 | 878,773.8 | 862,367.0 | -1.2 % | 1.9 % | 2.6 % | 2.55 % |
| inter_operator_dispatch | 33530 | 33530 | 711,698.7 | 733,937.3 | 1,359,032.1 | -47.6 % | -46.0 % | 2.17 % | 4.02 % |
| mir_operator:decode_sample | 850 | 850 | 522,323.3 | 538,644.5 | 524,213.4 | -0.4 % | 2.8 % | 1.59 % | 1.55 % |
| mir_operator:decode_head | 850 | 850 | 226,232.9 | 233,302.0 | 225,474.6 | 0.3 % | 3.5 % | 0.69 % | 0.67 % |
| mir_operator:decode_embed | 850 | 850 | 48,278.0 | 49,786.5 | 47,129.6 | 2.4 % | 5.6 % | 0.15 % | 0.14 % |
| mir_operator:prefill_sample | 10 | 10 | 19,078.0 | 19,674.1 | 23,072.0 | -17.3 % | -14.7 % | 0.06 % | 0.07 % |
| token_preprocess_cpu | 10 | 10 | 14,842.3 | 15,306.1 | 16,120.3 | -7.9 % | -5.1 % | 0.05 % | 0.05 % |
| mir_operator:prefill_layer00 | 10 | 10 | 13,150.3 | 13,561.2 | 13,146.1 | 0.0 % | 3.2 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer01 | 10 | 10 | 11,890.3 | 12,261.9 | 11,910.9 | -0.2 % | 2.9 % | 0.04 % | 0.04 % |
| mir_operator:prefill_layer02 | 10 | 10 | 11,426.4 | 11,783.4 | 11,585.5 | -1.4 % | 1.7 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer03 | 10 | 10 | 11,332.9 | 11,687.0 | 11,462.6 | -1.1 % | 2.0 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer19 | 10 | 10 | 11,111.3 | 11,458.5 | 11,149.1 | -0.3 % | 2.8 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer35 | 10 | 10 | 11,092.9 | 11,439.6 | 11,265.4 | -1.5 % | 1.5 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer20 | 10 | 10 | 11,077.7 | 11,423.8 | 11,123.8 | -0.4 % | 2.7 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer34 | 10 | 10 | 11,076.4 | 11,422.5 | 11,258.1 | -1.6 % | 1.5 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer24 | 10 | 10 | 11,057.0 | 11,402.5 | 11,483.5 | -3.7 % | -0.7 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer21 | 10 | 10 | 11,052.5 | 11,397.9 | 11,170.2 | -1.1 % | 2.0 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer22 | 10 | 10 | 11,051.2 | 11,396.5 | 11,241.5 | -1.7 % | 1.4 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer18 | 10 | 10 | 11,048.1 | 11,393.4 | 11,165.5 | -1.1 % | 2.0 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer15 | 10 | 10 | 11,001.4 | 11,345.2 | 11,300.8 | -2.6 % | 0.4 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer16 | 10 | 10 | 10,963.0 | 11,305.6 | 11,374.3 | -3.6 % | -0.6 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer23 | 10 | 10 | 10,961.3 | 11,303.8 | 11,526.7 | -4.9 % | -1.9 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer33 | 10 | 10 | 10,944.5 | 11,286.5 | 11,223.0 | -2.5 % | 0.6 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer17 | 10 | 10 | 10,944.0 | 11,286.0 | 11,225.7 | -2.5 % | 0.5 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer26 | 10 | 10 | 10,933.7 | 11,275.3 | 11,509.1 | -5.0 % | -2.0 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer11 | 10 | 10 | 10,886.8 | 11,227.0 | 11,263.9 | -3.3 % | -0.3 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer29 | 10 | 10 | 10,871.2 | 11,210.9 | 11,346.3 | -4.2 % | -1.2 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer10 | 10 | 10 | 10,864.8 | 11,204.3 | 11,268.2 | -3.6 % | -0.6 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer28 | 10 | 10 | 10,863.0 | 11,202.4 | 11,419.3 | -4.9 % | -1.9 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer27 | 10 | 10 | 10,857.5 | 11,196.8 | 11,440.6 | -5.1 % | -2.1 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer06 | 10 | 10 | 10,855.5 | 11,194.7 | 11,265.9 | -3.6 % | -0.6 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer25 | 10 | 10 | 10,853.7 | 11,192.9 | 11,447.7 | -5.2 % | -2.2 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer32 | 10 | 10 | 10,806.0 | 11,143.6 | 11,283.3 | -4.2 % | -1.2 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer14 | 10 | 10 | 10,796.7 | 11,134.0 | 11,321.9 | -4.6 % | -1.7 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer31 | 10 | 10 | 10,791.5 | 11,128.7 | 11,253.0 | -4.1 % | -1.1 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer12 | 10 | 10 | 10,785.0 | 11,122.0 | 11,236.8 | -4.0 % | -1.0 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer13 | 10 | 10 | 10,768.4 | 11,104.9 | 11,288.2 | -4.6 % | -1.6 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer07 | 10 | 10 | 10,743.0 | 11,078.6 | 11,312.6 | -5.0 % | -2.1 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer05 | 10 | 10 | 10,714.9 | 11,049.7 | 11,262.1 | -4.9 % | -1.9 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer30 | 10 | 10 | 10,714.2 | 11,049.0 | 11,275.8 | -5.0 % | -2.0 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer04 | 10 | 10 | 10,671.0 | 11,004.5 | 11,357.7 | -6.0 % | -3.1 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer09 | 10 | 10 | 10,413.1 | 10,738.5 | 11,276.5 | -7.7 % | -4.8 % | 0.03 % | 0.03 % |
| mir_operator:prefill_layer08 | 10 | 10 | 10,387.5 | 10,712.1 | 11,349.0 | -8.5 % | -5.6 % | 0.03 % | 0.03 % |
| pre_d2h_alloc | 10 | 10 | 3,289.6 | 3,392.4 | 3,812.6 | -13.7 % | -11.0 % | 0.01 % | 0.01 % |
| mir_operator:prefill_head | 10 | 10 | 2,754.1 | 2,840.2 | 2,867.3 | -3.9 % | -0.9 % | 0.01 % | 0.01 % |
| weight_init | 10 | 10 | 2,077.4 | 2,142.3 | 1,920.7 | 8.2 % | 11.5 % | 0.01 % | 0.01 % |
| d2h_stage | 10 | 10 | 1,501.9 | 1,548.8 | 1,376.3 | 9.1 % | 12.5 % | 0.0 % | 0.0 % |
| host_input_generate | 10 | 10 | 1,396.7 | 1,440.3 | 1,416.5 | -1.4 % | 1.7 % | 0.0 % | 0.0 % |
| h2d_stage | 10 | 10 | 1,106.9 | 1,141.5 | 1,163.8 | -4.9 % | -1.9 % | 0.0 % | 0.0 % |
| mir_operator:prefill_embed | 10 | 10 | 1,008.4 | 1,039.9 | 938.0 | 7.5 % | 10.9 % | 0.0 % | 0.0 % |
| dag_schedule_gap | 11 | 11 | 879.0 | 906.5 | 1,988.3 | -55.8 % | -54.4 % | 0.0 % | 0.01 % |
| checksum_complete | 10 | 10 | 469.2 | 483.9 | 472.1 | -0.6 % | 2.5 % | 0.0 % | 0.0 % |
| agent_tool_execute_cpu | 1 | 1 | 359.4 | 370.7 | 429.1 | -16.2 % | -13.6 % | 0.0 % | 0.0 % |
| iteration_tail_sync | 1 | 1 | 158.1 | 163.0 | 157.4 | 0.4 % | 3.6 % | 0.0 % | 0.0 % |
| adapter_dispatch | 10 | 10 | 51.4 | 53.0 | 51.9 | -1.0 % | 2.1 % | 0.0 % | 0.0 % |

## Call-wise estimate vs observed (per iteration)

| call | template_absolute (us) | template_scaled (us) | observed (us) | abs err | template GPU (us) | observed GPU (us) | GPU err |
|---|---:|---:|---:|---:|---:|---:|---:|
| <dag> | 1,037.1 | 1,069.5 | 2,145.6 | -51.7 % | 0.0 | 0.0 |  % |
| react-plan | 2,978,239.0 | 3,071,300.8 | 3,035,624.8 | -1.9 % | 723,398.6 | 730,510.4 | -1.0 % |
| moa-map0 | 3,432,862.6 | 3,540,130.1 | 3,424,634.8 | 0.2 % | 847,893.2 | 853,880.2 | -0.7 % |
| moa-map1 | 3,661,241.2 | 3,775,644.9 | 3,690,507.2 | -0.8 % | 903,202.7 | 911,020.8 | -0.9 % |
| moa-map2 | 3,318,673.3 | 3,422,372.7 | 3,364,362.8 | -1.4 % | 820,238.5 | 827,755.3 | -0.9 % |
| mcts-root | 3,242,547.1 | 3,343,867.8 | 3,295,985.7 | -1.6 % | 801,801.9 | 814,969.8 | -1.6 % |
| react-tool | 359.4 | 370.7 | 429.1 | -16.2 % | 0.0 | 0.0 |  % |
| mcts-actor0 | 3,394,799.5 | 3,500,877.6 | 3,626,001.0 | -6.4 % | 838,675.0 | 853,757.4 | -1.8 % |
| mcts-actor1 | 3,090,294.7 | 3,186,857.9 | 3,378,018.5 | -8.5 % | 764,928.9 | 778,619.3 | -1.8 % |
| moa-reduce | 3,547,051.9 | 3,657,887.5 | 3,835,456.7 | -7.5 % | 875,548.0 | 891,416.5 | -1.8 % |
| react-answer | 2,900,251.3 | 2,990,876.1 | 2,892,209.7 | 0.3 % | 712,005.1 | 717,195.2 | -0.7 % |
| mcts-critic | 3,242,547.1 | 3,343,867.8 | 3,289,747.5 | -1.4 % | 801,801.9 | 818,089.9 | -2.0 % |

## Constraints honoured

- `template_absolute` is a prediction; `template_scaled` is conserved to the w01 measured wall and is not a direct trace.
- Representative absolute latencies are never reported as target latencies without the matrix-size key matching.
- w03 hardware attributes do not enter this denominator.

# G04 kernel-family hardware attributes by representative operator

Lineage `h22-gpu-autotrace`, workflow w03. Rows are w02 launch-owned targets grouped by matched kernel family;
NCU metrics come from a separate single-iteration replay run and `ncu_replay_us` is not latency. Peak DRAM 1008 GB/s is the RTX 4090 reference;
GEMM TFLOPS is computed from replay time at NCU's locked base clock and is context only, the utilisation reference is Tensor % (pipe active).

| workload | matrix | process | family | n | SM % | Tensor % | DRAM active % | DRAM BW % peak | L2 % | L2 hit % | occupancy % | waves/SM | GEMM TFLOPS (replay) | dominant stalls | interpretation |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| planner_debate_L_it1 | 3584 | weight_init | rng_init | 2 | 70.33 | 0.0 | 46.24 | 0.0 | 37.25 | 98.62 | 67.79 | 1.0 |  | not_selected=3.77; math_pipe_throttle=2.14; wait=1.65 | SM-issue-bound |
| planner_debate_L_it1 | 3584 | weight_init | elementwise_binary | 2 | 4.31 | 0.0 | 92.61 | 0.0 | 32.73 | 50.2 | 86.21 | 8.17 |  | long_scoreboard=173.00; drain=18.81; short_scoreboard=3.40 | DRAM-bandwidth-bound |
| planner_debate_L_it1 | 3584 | mir_operator:RMSNormOp | copy | 8 | 5.31 | 0.0 | 89.5 | 0.0 | 35.76 | 51.17 | 86.92 | 8.17 |  | long_scoreboard=31.58; wait=4.59; no_instruction=1.02 | DRAM-bandwidth-bound |
| planner_debate_L_it1 | 3584 | mir_operator:RMSNormOp | elementwise_unary | 8 | 0.96 | 0.0 | 47.22 | 0.0 | 14.99 | 64.95 | 42.45 | 4.08 |  | long_scoreboard=339.55; drain=95.45; mio_throttle=53.62 | DRAM-bandwidth-bound |
| planner_debate_L_it1 | 3584 | mir_operator:RMSNormOp | reduce | 4 | 2.2 | 0.0 | 90.15 | 0.0 | 34.1 | 1.3 | 58.18 | 0.58 |  | long_scoreboard=278.78; barrier=10.23; imc_miss=4.39 | DRAM-bandwidth-bound |
| planner_debate_L_it1 | 3584 | mir_operator:RMSNormOp | elementwise_binary | 8 | 7.31 | 0.0 | 46.99 | 0.0 | 14.25 | 64.59 | 47.73 | 16.34 |  | imc_miss=20.18; long_scoreboard=14.94; no_instruction=2.34 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate_L_it1 | 3584 | mir_operator:AddOp | elementwise_binary | 2 | 4.57 | 0.0 | 92.74 | 0.0 | 33.1 | 50.2 | 85.47 | 8.17 |  | long_scoreboard=168.10; drain=18.54; short_scoreboard=3.26 | DRAM-bandwidth-bound |
| planner_debate_L_it1 | 3584 | mir_operator:LinearOp | gemm | 6 | 43.79 | 44.86 | 12.03 | 0.0 | 90.94 | 98.67 | 16.44 | 12.25 | 143.8 | math_pipe_throttle=7.48; long_scoreboard=2.16; barrier=2.14 | tensor-core compute-bound |
| planner_debate_L_it1 | 3584 | mir_operator:TransposeOp | copy | 2 | 6.19 | 0.0 | 22.7 | 0.0 | 91.87 | 93.85 | 88.33 | 16.33 |  | long_scoreboard=144.07; drain=11.88; short_scoreboard=7.78 | L2-bandwidth-bound (working set in L2) |
| planner_debate_L_it1 | 4096 | weight_init | rng_init | 3 | 71.21 | 0.0 | 57.52 | 0.0 | 38.31 | 100.07 | 67.82 | 1.0 |  | not_selected=3.77; math_pipe_throttle=2.13; wait=1.65 | SM-issue-bound |
| planner_debate_L_it1 | 4096 | weight_init | elementwise_binary | 3 | 5.19 | 0.0 | 93.5 | 0.0 | 30.87 | 50.16 | 87.03 | 10.67 |  | long_scoreboard=174.55; drain=19.84; short_scoreboard=3.32 | DRAM-bandwidth-bound |
| planner_debate_L_it1 | 4096 | mir_operator:RMSNormOp | copy | 12 | 11.18 | 0.0 | 91.08 | 0.0 | 32.38 | 50.21 | 87.72 | 10.67 |  | long_scoreboard=29.93; wait=4.59; no_instruction=1.08 | DRAM-bandwidth-bound |
| planner_debate_L_it1 | 4096 | mir_operator:RMSNormOp | elementwise_unary | 12 | 0.89 | 0.0 | 47.39 | 0.0 | 14.06 | 64.25 | 42.57 | 5.33 |  | long_scoreboard=353.63; drain=109.78; mio_throttle=82.52 | DRAM-bandwidth-bound |
| planner_debate_L_it1 | 4096 | mir_operator:RMSNormOp | reduce | 6 | 2.03 | 0.0 | 90.49 | 0.0 | 30.77 | 1.01 | 66.11 | 0.67 |  | long_scoreboard=327.35; barrier=16.45; imc_miss=3.73 | DRAM-bandwidth-bound |
| planner_debate_L_it1 | 4096 | mir_operator:RMSNormOp | elementwise_binary | 12 | 7.13 | 0.0 | 47.16 | 0.0 | 13.87 | 53.31 | 48.51 | 21.34 |  | imc_miss=25.77; long_scoreboard=21.20; no_instruction=2.94 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate_L_it1 | 4096 | mir_operator:AddOp | elementwise_binary | 3 | 5.48 | 0.0 | 93.5 | 0.0 | 31.08 | 50.15 | 87.59 | 10.67 |  | long_scoreboard=170.59; drain=19.24; short_scoreboard=3.29 | DRAM-bandwidth-bound |
| planner_debate_L_it1 | 4096 | mir_operator:LinearOp | gemm | 9 | 48.8 | 49.01 | 16.72 | 0.0 | 54.36 | 97.3 | 16.35 | 12.0 | 161.1 | math_pipe_throttle=12.09; wait=4.30; barrier=1.13 | tensor-core compute-bound |
| planner_debate_L_it1 | 4096 | mir_operator:TransposeOp | copy | 3 | 6.3 | 0.0 | 24.87 | 0.0 | 93.18 | 93.97 | 88.49 | 21.33 |  | long_scoreboard=141.72; drain=11.93; short_scoreboard=7.89 | L2-bandwidth-bound (working set in L2) |
| react_tool_L_it1 | 3072 | weight_init | rng_init | 2 | 68.72 | 0.0 | 33.72 | 0.0 | 37.25 | 100.05 | 67.7 | 1.0 |  | not_selected=3.78; math_pipe_throttle=2.17; wait=1.65 | SM-issue-bound |
| react_tool_L_it1 | 3072 | weight_init | elementwise_binary | 2 | 5.02 | 0.0 | 88.95 | 0.0 | 33.26 | 50.28 | 84.32 | 6.0 |  | long_scoreboard=170.44; drain=18.31; short_scoreboard=2.94 | DRAM-bandwidth-bound |
| react_tool_L_it1 | 3072 | mir_operator:RMSNormOp | copy | 8 | 12.59 | 0.0 | 88.06 | 0.0 | 37.8 | 50.31 | 87.67 | 6.0 |  | long_scoreboard=20.83; wait=4.58; selected=1.00 | DRAM-bandwidth-bound |
| react_tool_L_it1 | 3072 | mir_operator:RMSNormOp | elementwise_unary | 8 | 1.0 | 0.0 | 46.99 | 0.0 | 15.64 | 65.44 | 42.21 | 3.0 |  | long_scoreboard=313.59; drain=82.26; mio_throttle=42.29 | DRAM-bandwidth-bound |
| react_tool_L_it1 | 3072 | mir_operator:RMSNormOp | reduce | 4 | 2.33 | 0.0 | 87.86 | 0.0 | 34.25 | 1.75 | 49.89 | 0.5 |  | long_scoreboard=215.55; barrier=15.63; imc_miss=4.71 | DRAM-bandwidth-bound |
| react_tool_L_it1 | 3072 | mir_operator:RMSNormOp | elementwise_binary | 8 | 7.57 | 0.0 | 46.48 | 0.0 | 14.52 | 50.61 | 47.05 | 12.0 |  | imc_miss=25.87; long_scoreboard=21.05; no_instruction=2.94 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool_L_it1 | 3072 | mir_operator:AddOp | elementwise_binary | 2 | 4.85 | 0.0 | 63.61 | 0.0 | 23.32 | 49.34 | 85.1 | 6.0 |  | long_scoreboard=166.15; drain=17.68; short_scoreboard=3.05 | DRAM-bandwidth-bound |
| react_tool_L_it1 | 3072 | mir_operator:LinearOp | gemm | 6 | 47.44 | 48.07 | 12.87 | 0.0 | 74.35 | 97.25 | 15.95 | 4.5 | 155.9 | math_pipe_throttle=11.52; wait=3.95; selected=1.00 | tensor-core compute-bound |
| react_tool_L_it1 | 3072 | mir_operator:TransposeOp | copy | 2 | 6.12 | 0.0 | 20.34 | 0.0 | 90.91 | 93.92 | 87.69 | 12.0 |  | long_scoreboard=140.00; drain=12.07; short_scoreboard=8.14 | L2-bandwidth-bound (working set in L2) |
| react_tool_L_it1 |  | host_input_generate |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool_L_it1 |  | adapter_dispatch |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool_L_it1 |  | h2d_stage | memcpy | 16 |  |  |  |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool_L_it1 |  | d2h_stage | memcpy | 16 |  |  |  |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool_L_it1 |  | dag_schedule_gap |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool_L_it1 |  | token_preprocess_cpu |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool_L_it1 |  | agent_tool_execute_cpu |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool_L_it1 |  | checksum_complete |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool_L_it1 |  | mir_operator:ViewOp |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool_L_it1 |  | inter_operator_dispatch |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool_L_it1 |  | iteration_tail_sync |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool_L_it1 |  | pre_d2h_alloc |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate_L_it1 |  | host_input_generate |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate_L_it1 |  | h2d_stage | memcpy | 40 |  |  |  |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate_L_it1 |  | d2h_stage | memcpy | 40 |  |  |  |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate_L_it1 |  | adapter_dispatch |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate_L_it1 |  | token_preprocess_cpu |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate_L_it1 |  | dag_schedule_gap |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate_L_it1 |  | checksum_complete |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate_L_it1 |  | agent_tool_execute_cpu |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate_L_it1 |  | mir_operator:ViewOp |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate_L_it1 |  | inter_operator_dispatch |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate_L_it1 |  | pre_d2h_alloc |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate_L_it1 |  | iteration_tail_sync |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |

## Provenance

```json
{
  "react_tool_L_it1": {
    "ncu_rep_sha256": "f421b776869c311157d39a47d5e38c5cae9ff4982a128e93c35a8497cd48625a",
    "ncu_raw_sha256": "ff8fa5c5dc89129556679e3997713fc7205e5a5135599b0e235a61b2152a543d",
    "ncu_kernels": 42,
    "w02_kernels_in_representative_iteration": 42,
    "ncu_kernels_joined_to_w02": 42,
    "order_match": true
  },
  "planner_debate_L_it1": {
    "ncu_rep_sha256": "31392d1a3c286e48c244470203dd7f9a593ce13596dcc4a8c1b2514bd04efffa",
    "ncu_raw_sha256": "80b604365cc60e7b9290e8f625ffc364aba7e37f5723261e0489dc5d16ece849",
    "ncu_kernels": 105,
    "w02_kernels_in_representative_iteration": 105,
    "ncu_kernels_joined_to_w02": 105,
    "order_match": true
  }
}
```

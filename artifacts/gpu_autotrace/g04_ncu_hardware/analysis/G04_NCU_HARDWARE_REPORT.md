# G04 kernel-family hardware attributes by representative operator

Lineage `h22-gpu-autotrace`, workflow w03. Rows are w02 launch-owned targets grouped by matched kernel family;
NCU metrics come from a separate single-iteration replay run and `ncu_replay_us` is not latency. Peak DRAM 1008 GB/s is the RTX 4090 reference;
GEMM TFLOPS is computed from replay time at NCU's locked base clock and is context only, the utilisation reference is Tensor % (pipe active).

| workload | matrix | process | family | n | SM % | Tensor % | DRAM active % | DRAM BW % peak | L2 % | L2 hit % | occupancy % | waves/SM | GEMM TFLOPS (replay) | dominant stalls | interpretation |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| planner_debate | 896 | weight_init | rng_init | 2 | 51.16 | 0.0 | 0.23 | 0.0 | 12.79 | 99.88 | 67.46 | 1.0 |  | not_selected=3.74; math_pipe_throttle=2.45; wait=1.67 | underutilised: SM 51 %, DRAM 0 %, L2 13 %, occ 67 % |
| planner_debate | 896 | weight_init | elementwise_binary | 2 | 2.7 | 0.0 | 46.09 | 0.0 | 21.49 | 52.4 | 31.82 | 0.51 |  | long_scoreboard=69.16; imc_miss=12.37; wait=1.66 | underutilised: SM 3 %, DRAM 47 %, L2 22 %, occ 32 % |
| planner_debate | 896 | mir_operator:RMSNormOp | copy | 8 | 8.35 | 0.0 | 45.57 | 0.0 | 26.25 | 52.63 | 38.72 | 0.51 |  | long_scoreboard=14.45; wait=4.52; imc_miss=2.82 | underutilised: SM 15 %, DRAM 30 %, L2 29 %, occ 47 % |
| planner_debate | 896 | mir_operator:RMSNormOp | elementwise_unary | 8 | 0.9 | 0.0 | 29.99 | 0.0 | 13.98 | 73.59 | 20.49 | 0.26 |  | long_scoreboard=183.73; imc_miss=16.55; drain=2.83 | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:RMSNormOp | reduce | 4 | 2.74 | 0.0 | 50.4 | 0.0 | 19.81 | 16.01 | 33.25 | 0.15 |  | long_scoreboard=31.43; imc_miss=8.74; barrier=3.54 | underutilised: SM 3 %, DRAM 52 %, L2 21 %, occ 33 % |
| planner_debate | 896 | mir_operator:RMSNormOp | elementwise_binary | 8 | 7.27 | 0.0 | 28.23 | 0.0 | 14.5 | 69.41 | 41.16 | 1.02 |  | imc_miss=8.08; long_scoreboard=6.44; wait=2.88 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:AddOp | elementwise_binary | 2 | 2.76 | 0.0 | 44.01 | 0.0 | 20.5 | 51.99 | 31.86 | 0.51 |  | long_scoreboard=68.92; imc_miss=11.70; wait=1.93 | underutilised: SM 3 %, DRAM 43 %, L2 20 %, occ 31 % |
| planner_debate | 896 | mir_operator:LinearOp | gemm | 6 | 28.57 | 40.97 | 21.1 | 0.0 | 46.6 | 93.26 | 8.33 | 0.77 | 92.2 | math_pipe_throttle=7.37; wait=2.34; selected=1.00 | tensor-core compute-bound |
| planner_debate | 896 | mir_operator:TransposeOp | copy | 2 | 5.37 | 0.0 | 12.63 | 0.0 | 80.56 | 94.22 | 87.96 | 1.02 |  | long_scoreboard=139.29; lg_throttle=14.27; drain=6.87 | L2-bandwidth-bound (working set in L2) |
| planner_debate | 1024 | weight_init | rng_init | 3 | 51.25 | 0.0 | 0.58 | 0.0 | 16.17 | 100.02 | 67.42 | 1.0 |  | not_selected=3.73; math_pipe_throttle=2.44; wait=1.67 | underutilised: SM 51 %, DRAM 1 %, L2 16 %, occ 67 % |
| planner_debate | 1024 | weight_init | elementwise_binary | 3 | 2.96 | 0.0 | 51.43 | 0.0 | 23.98 | 51.61 | 40.01 | 0.67 |  | long_scoreboard=89.85; imc_miss=10.36; wait=1.68 | underutilised: SM 3 %, DRAM 51 %, L2 23 %, occ 40 % |
| planner_debate | 1024 | mir_operator:RMSNormOp | copy | 12 | 9.27 | 0.0 | 51.53 | 0.0 | 29.74 | 52.19 | 48.33 | 0.67 |  | long_scoreboard=15.76; wait=4.52; imc_miss=2.61 | underutilised: SM 18 %, DRAM 36 %, L2 35 %, occ 60 % |
| planner_debate | 1024 | mir_operator:RMSNormOp | elementwise_unary | 12 | 0.93 | 0.0 | 31.65 | 0.0 | 14.66 | 67.12 | 26.02 | 0.34 |  | long_scoreboard=237.97; drain=27.12; imc_miss=13.96 | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:RMSNormOp | reduce | 6 | 2.83 | 0.0 | 57.19 | 0.0 | 22.48 | 12.93 | 33.26 | 0.17 |  | long_scoreboard=38.51; imc_miss=8.21; wait=2.84 | underutilised: SM 3 %, DRAM 57 %, L2 23 %, occ 33 % |
| planner_debate | 1024 | mir_operator:RMSNormOp | elementwise_binary | 12 | 7.75 | 0.0 | 30.74 | 0.0 | 15.52 | 68.43 | 41.56 | 1.33 |  | imc_miss=29.42; long_scoreboard=21.70; no_instruction=2.94 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:AddOp | elementwise_binary | 3 | 3.19 | 0.0 | 51.74 | 0.0 | 23.89 | 51.56 | 38.96 | 0.67 |  | long_scoreboard=83.67; imc_miss=10.46; wait=1.96 | underutilised: SM 3 %, DRAM 50 %, L2 23 %, occ 39 % |
| planner_debate | 1024 | mir_operator:LinearOp | gemm | 9 | 31.48 | 34.17 | 20.26 | 0.0 | 50.65 | 92.04 | 8.33 | 0.5 | 101.4 | math_pipe_throttle=4.05; wait=3.83; long_scoreboard=1.70 | underutilised: SM 32 %, DRAM 20 %, L2 51 %, occ 8 % |
| planner_debate | 1024 | mir_operator:TransposeOp | copy | 3 | 6.98 | 0.0 | 17.13 | 0.0 | 79.66 | 92.41 | 81.21 | 1.33 |  | long_scoreboard=97.80; drain=4.84; lg_throttle=4.41 | L2-bandwidth-bound (working set in L2) |
| react_tool | 768 | weight_init | rng_init | 2 | 44.0 | 0.0 | 2.22 | 0.0 | 12.81 | 100.02 | 67.78 | 1.0 |  | not_selected=3.68; math_pipe_throttle=2.64; dispatch_stall=1.78 | underutilised: SM 44 %, DRAM 1 %, L2 13 %, occ 68 % |
| react_tool | 768 | weight_init | elementwise_binary | 2 | 2.27 | 0.0 | 40.01 | 0.0 | 18.85 | 52.89 | 25.59 | 0.38 |  | long_scoreboard=54.93; imc_miss=11.93; wait=1.64 | underutilised: SM 2 %, DRAM 40 %, L2 19 %, occ 25 % |
| react_tool | 768 | mir_operator:RMSNormOp | copy | 8 | 2.01 | 0.0 | 39.25 | 0.0 | 22.01 | 53.61 | 29.69 | 0.38 |  | long_scoreboard=13.80; wait=4.51; imc_miss=3.02 | latency/launch-bound: 0.38 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:RMSNormOp | elementwise_unary | 8 | 0.82 | 0.0 | 27.42 | 0.0 | 13.11 | 69.85 | 16.81 | 0.19 |  | long_scoreboard=148.14; imc_miss=16.47; wait=2.34 | underutilised: SM 2 %, DRAM 55 %, L2 25 %, occ 25 % |
| react_tool | 768 | mir_operator:RMSNormOp | reduce | 4 | 2.63 | 0.0 | 43.36 | 0.0 | 17.06 | 20.0 | 33.23 | 0.12 |  | long_scoreboard=23.23; imc_miss=9.14; barrier=2.90 | underutilised: SM 3 %, DRAM 44 %, L2 17 %, occ 33 % |
| react_tool | 768 | mir_operator:RMSNormOp | elementwise_binary | 8 | 6.53 | 0.0 | 25.81 | 0.0 | 13.39 | 74.53 | 38.47 | 0.75 |  | imc_miss=8.64; long_scoreboard=5.18; wait=2.94 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:AddOp | elementwise_binary | 2 | 2.34 | 0.0 | 37.92 | 0.0 | 17.82 | 52.51 | 25.01 | 0.38 |  | long_scoreboard=52.83; imc_miss=12.18; wait=1.93 | underutilised: SM 2 %, DRAM 38 %, L2 18 %, occ 25 % |
| react_tool | 768 | mir_operator:LinearOp | gemm | 6 | 21.05 | 28.66 | 18.34 | 0.0 | 49.56 | 94.55 | 15.03 | 1.5 | 67.65 | math_pipe_throttle=4.00; barrier=1.48; long_scoreboard=1.12 | underutilised: SM 21 %, DRAM 18 %, L2 50 %, occ 15 % |
| react_tool | 768 | mir_operator:TransposeOp | copy | 2 | 5.21 | 0.0 | 13.12 | 0.0 | 78.36 | 94.23 | 68.84 | 0.75 |  | long_scoreboard=119.30; drain=5.42; imc_miss=5.29 | L2-bandwidth-bound (working set in L2) |
| react_tool |  | host_input_generate |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | adapter_dispatch |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | dag_schedule_gap |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | token_preprocess_cpu |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | h2d_stage | memcpy | 40 |  |  |  |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool |  | agent_tool_execute_cpu |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | d2h_stage | memcpy | 40 |  |  |  |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool |  | mir_operator:ViewOp |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | checksum_complete |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | inter_operator_dispatch |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | iteration_tail_sync |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | pre_d2h_alloc |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | host_input_generate |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | adapter_dispatch |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | dag_schedule_gap |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | token_preprocess_cpu |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | h2d_stage | memcpy | 100 |  |  |  |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate |  | d2h_stage | memcpy | 100 |  |  |  |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate |  | mir_operator:ViewOp |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | checksum_complete |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | agent_tool_execute_cpu |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | inter_operator_dispatch |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | pre_d2h_alloc |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | iteration_tail_sync |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |

## Provenance

```json
{
  "react_tool": {
    "ncu_rep_sha256": "ecac23b2cbd07ec8c3116a2ffdb036be0127b55b0e988805d624b50b391dfcce",
    "ncu_raw_sha256": "56f1939ff00002f8f7f266ab2a282a2598047b57820cae9a7ddef52e229ce58c",
    "ncu_kernels": 42,
    "w02_kernels_in_representative_iteration": 42,
    "ncu_kernels_joined_to_w02": 42,
    "order_match": true
  },
  "planner_debate": {
    "ncu_rep_sha256": "43f6e4df12e12dbe612fbae497cdb99f63687355e04eef3adb3176b6668f4bc9",
    "ncu_raw_sha256": "8647856d5fa4f398542c1cabc165a67f0e8fd2532ff4b0c0f7c0bfe03f0fe82c",
    "ncu_kernels": 105,
    "w02_kernels_in_representative_iteration": 105,
    "ncu_kernels_joined_to_w02": 105,
    "order_match": true
  }
}
```

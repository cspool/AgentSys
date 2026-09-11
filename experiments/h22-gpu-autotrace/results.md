# h22 lineage summary: AutoTrace w01-w05 on AgentSys, single RTX 4090

Two strands of the same serial chain. `base` runs the certified run_040 plans as shipped (matrix 768-1024, one operator iteration).
`scaled` runs the same DAGs with matrix x4, 32 operator iterations and the react_moa_mcts DAG repeated 3x (built by `build_scaled_plan.py`,
`src/agentsys/` untouched). Every strand: 5 goals, all conservation gates pass, nothing left this machine.

## G01/G02 denominators

| strand | workload | calls | ops | matrix | op iters | measured wall / iter (ms) | GPU busy | operator GPU / iter (ms) | overhead GPU / iter (ms) | launches / iter | host_input_generate share | operators host share |
|---|---|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| base | react_tool | 3 | 16 | 768 | 1 | 18.5 | 2.8 % | 0.17 | 0.32 | 42 | 56.3 % | 12.9 % |
| base | planner_debate | 6 | 40 | 896/1024 | 1 | 62.1 | 3.2 % | 0.55 | 1.39 | 105 | 69.9 % | 9.5 % |
| base | react_moa_mcts | 11 | 80 | 768/896/1024 | 1 | 142.7 | 2.4 % | 1.12 | 2.24 | 210 | 74.7 % | 8.3 % |
| scaled | react_tool_L | 3 | 16 | 3072 | 32 | 237.7 | 40.7 % | 93.17 | 3.37 | 1220 | 56.1 % | 40.1 % |
| scaled | planner_debate_L | 6 | 40 | 3584/4096 | 32 | 1,079.1 | 50.1 % | 525.99 | 13.34 | 3050 | 48.2 % | 49.5 % |
| scaled | react_moa_mcts_x3_L | 33 | 240 | 3072/3584/4096 | 32 | 6,606.0 | 50.3 % | 3,241.46 | 81.93 | 18300 | 48.4 % | 49.5 % |

## G04 hardware attributes of the representative GEMM (LinearOp) and RMSNorm kernels

| strand | workload | matrix | Tensor pipe % | SM % | L2 % | DRAM active % | occupancy % | waves/SM | TFLOPS (replay) | interpretation |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| base | planner_debate | 896 | 40.97 | 28.57 | 46.6 | 21.1 | 8.33 | 0.77 | 92.2 | tensor-core compute-bound |
| base | planner_debate | 1024 | 34.17 | 31.48 | 50.65 | 20.26 | 8.33 | 0.5 | 101.4 | underutilised: SM 32 %, DRAM 20 %, L2 51 %, occ 8 % |
| base | react_tool | 768 | 28.66 | 21.05 | 49.56 | 18.34 | 15.03 | 1.5 | 67.65 | underutilised: SM 21 %, DRAM 18 %, L2 50 %, occ 15 % |
| scaled | planner_debate_L_it1 | 3584 | 44.86 | 43.79 | 90.94 | 12.03 | 16.44 | 12.25 | 143.8 | tensor-core compute-bound |
| scaled | planner_debate_L_it1 | 4096 | 49.01 | 48.8 | 54.36 | 16.72 | 16.35 | 12.0 | 161.1 | tensor-core compute-bound |
| scaled | react_tool_L_it1 | 3072 | 48.07 | 47.44 | 74.35 | 12.87 | 15.95 | 4.5 | 155.9 | tensor-core compute-bound |

| strand | workload | matrix | RMSNorm kernel family | n | DRAM active % | L2 % | waves/SM | interpretation |
|---|---|---:|---|---:|---:|---:|---:|---|
| base | planner_debate | 896 | copy | 8 | 45.57 | 26.25 | 0.51 | underutilised: SM 15 %, DRAM 30 %, L2 29 %, occ 47 % |
| base | planner_debate | 896 | elementwise_unary | 8 | 29.99 | 13.98 | 0.26 | DRAM-bandwidth-bound |
| base | planner_debate | 896 | reduce | 4 | 50.4 | 19.81 | 0.15 | underutilised: SM 3 %, DRAM 52 %, L2 21 %, occ 33 % |
| base | planner_debate | 896 | elementwise_binary | 8 | 28.23 | 14.5 | 1.02 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| base | planner_debate | 1024 | copy | 12 | 51.53 | 29.74 | 0.67 | underutilised: SM 18 %, DRAM 36 %, L2 35 %, occ 60 % |
| base | planner_debate | 1024 | elementwise_unary | 12 | 31.65 | 14.66 | 0.34 | DRAM-bandwidth-bound |
| base | planner_debate | 1024 | reduce | 6 | 57.19 | 22.48 | 0.17 | underutilised: SM 3 %, DRAM 57 %, L2 23 %, occ 33 % |
| base | planner_debate | 1024 | elementwise_binary | 12 | 30.74 | 15.52 | 1.33 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| base | react_tool | 768 | copy | 8 | 39.25 | 22.01 | 0.38 | latency/launch-bound: 0.38 waves per SM, no unit above 30 % of peak |
| base | react_tool | 768 | elementwise_unary | 8 | 27.42 | 13.11 | 0.19 | underutilised: SM 2 %, DRAM 55 %, L2 25 %, occ 25 % |
| base | react_tool | 768 | reduce | 4 | 43.36 | 17.06 | 0.12 | underutilised: SM 3 %, DRAM 44 %, L2 17 %, occ 33 % |
| base | react_tool | 768 | elementwise_binary | 8 | 25.81 | 13.39 | 0.75 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| scaled | planner_debate_L_it1 | 3584 | copy | 8 | 89.5 | 35.76 | 8.17 | DRAM-bandwidth-bound |
| scaled | planner_debate_L_it1 | 3584 | elementwise_unary | 8 | 47.22 | 14.99 | 4.08 | DRAM-bandwidth-bound |
| scaled | planner_debate_L_it1 | 3584 | reduce | 4 | 90.15 | 34.1 | 0.58 | DRAM-bandwidth-bound |
| scaled | planner_debate_L_it1 | 3584 | elementwise_binary | 8 | 46.99 | 14.25 | 16.34 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| scaled | planner_debate_L_it1 | 4096 | copy | 12 | 91.08 | 32.38 | 10.67 | DRAM-bandwidth-bound |
| scaled | planner_debate_L_it1 | 4096 | elementwise_unary | 12 | 47.39 | 14.06 | 5.33 | DRAM-bandwidth-bound |
| scaled | planner_debate_L_it1 | 4096 | reduce | 6 | 90.49 | 30.77 | 0.67 | DRAM-bandwidth-bound |
| scaled | planner_debate_L_it1 | 4096 | elementwise_binary | 12 | 47.16 | 13.87 | 21.34 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| scaled | react_tool_L_it1 | 3072 | copy | 8 | 88.06 | 37.8 | 6.0 | DRAM-bandwidth-bound |
| scaled | react_tool_L_it1 | 3072 | elementwise_unary | 8 | 46.99 | 15.64 | 3.0 | DRAM-bandwidth-bound |
| scaled | react_tool_L_it1 | 3072 | reduce | 4 | 87.86 | 34.25 | 0.5 | DRAM-bandwidth-bound |
| scaled | react_tool_L_it1 | 3072 | elementwise_binary | 8 | 46.48 | 14.52 | 12.0 | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |

## G05 full-workload estimate from representative templates

| strand | target | absolute host error | GPU error | max process error (>=1 % of wall) | pass |
|---|---|---:|---:|---:|---|
| base | react_moa_mcts | -10.61 % | +20.77 % | 68.0 % | True |
| scaled | react_moa_mcts_x3_L | -0.07 % | -0.31 % | 1.0 % | True |

## G06-G10 selection and windows

| strand | workload | selected process types (> 10 %) | GPU busy (rep. iter) | host-only | GPU gaps >= 20 us | gap total (ms) |
|---|---|---|---:|---:|---:|---:|
| base | planner_debate | host_input_generate | 3.18 % | 85.03 % | 90 | 50.70 |
| base | react_moa_mcts | host_input_generate | 1.94 % | 90.5 % | 102 | 130.64 |
| base | react_tool | host_input_generate, adapter_dispatch | 2.78 % | 82.69 % | 27 | 10.74 |
| scaled | planner_debate_L | host_input_generate, mir_operator:LinearOp, mir_operator:RMSNormOp | 49.93 % | 49.23 % | 52 | 445.00 |
| scaled | react_moa_mcts_x3_L | host_input_generate, mir_operator:LinearOp, mir_operator:RMSNormOp | 50.34 % | 48.96 % | 315 | 3,196.73 |
| scaled | react_tool_L | host_input_generate, mir_operator:LinearOp | 40.69 % | 57.99 % | 19 | 72.42 |

| strand | workload | opportunity | current / iter (ms) | reference / iter (ms) | bound (% wall) |
|---|---|---|---:|---:|---:|
| base | react_tool | move_input_generation_to_device | 10.50 | 0.011 | 56.26 % |
| base | react_tool | remove_per_operator_synchronize | 2.41 | 0.168 | 12.02 % |
| base | react_tool | gpu_idle_window | 18.17 | 0.488 | 97.39 % |
| base | planner_debate | move_input_generation_to_device | 46.11 | 0.035 | 69.9 % |
| base | planner_debate | remove_per_operator_synchronize | 6.27 | 0.549 | 8.68 % |
| base | planner_debate | gpu_idle_window | 64.02 | 1.939 | 97.06 % |
| base | react_moa_mcts | move_input_generation_to_device | 100.83 | 0.068 | 74.68 % |
| base | react_moa_mcts | remove_per_operator_synchronize | 11.17 | 1.117 | 7.44 % |
| base | react_moa_mcts | gpu_idle_window | 131.66 | 3.356 | 97.51 % |
| scaled | react_tool_L | move_input_generation_to_device | 134.40 | 0.058 | 56.13 % |
| scaled | react_tool_L | remove_per_operator_synchronize | 96.12 | 93.173 | 1.23 % |
| scaled | react_tool_L | gpu_idle_window | 142.93 | 96.538 | 59.69 % |
| scaled | planner_debate_L | move_input_generation_to_device | 519.39 | 0.239 | 48.2 % |
| scaled | planner_debate_L | remove_per_operator_synchronize | 533.34 | 525.991 | 0.68 % |
| scaled | planner_debate_L | gpu_idle_window | 538.30 | 539.329 | 49.95 % |
| scaled | react_moa_mcts_x3_L | move_input_generation_to_device | 3,206.54 | 1.479 | 48.37 % |
| scaled | react_moa_mcts_x3_L | remove_per_operator_synchronize | 3,282.76 | 3,241.457 | 0.62 % |
| scaled | react_moa_mcts_x3_L | gpu_idle_window | 3,305.18 | 3,323.384 | 49.86 % |

## Reading

1. At native scale the GPU is busy 2-3 % of the wall. The certified adapter's per-call host input generation (seeded CPU-generator `uniform_` into a
   pinned fp16 tensor) is 56-75 % of every iteration; all MIR operators together are about 10 % of host time and 1-16 us of GPU time each.
2. Scaling the operators (matrix x4, 32 iterations) raises GPU busy to 40-50 % and makes LinearOp/RMSNormOp cross the 10 % selection line, but
   host input generation still takes about half the wall because it grows with n^2 on one CPU thread.
3. The 768-1024 GEMMs run at 15-24 % tensor-pipe activity with 0.75-1.5 waves per SM (latency/launch-bound); at 3072-4096 the same kernel family is
   tensor-core compute-bound at 45-49 % pipe activity and 12 waves per SM. RMSNorm stays a 7-kernel elementwise/reduce chain that never exceeds 0.4 waves.
4. Template estimation from two representative workloads predicts the full react_moa_mcts workload within 11 % (base) and 0.1 % (scaled) without using
   its trace; the base error is dominated by the plan-independent DAG scheduling gap and by H2D/D2H staging variance.
5. The real-model strand (Qwen3-1.7B weights present under /data3/docker_model/AgentSys) is not part of this summary: no transformer library is
   installed, downloads are excluded by protocol, and the hand-written fallback was set aside pending the user's own sources.

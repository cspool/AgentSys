# G04 kernel-family hardware attributes by representative operator

Lineage `h22-gpu-autotrace`, workflow w03. Rows are w02 launch-owned targets grouped by matched kernel family;
NCU metrics come from a separate single-iteration replay run and `ncu_replay_us` is not latency. Peak DRAM 1008 GB/s is the RTX 4090 reference;
GEMM TFLOPS is computed from replay time at NCU's locked base clock and is context only, the utilisation reference is Tensor % (pipe active).

| workload | matrix | process | family | n | SM % | Tensor % | DRAM active % | DRAM BW % peak | L2 % | L2 hit % | occupancy % | waves/SM | GEMM TFLOPS (replay) | dominant stalls | interpretation |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| planner_debate | 1024 | mir_operator:prefill_embed | other | 3 | 5.57 | 0.0 | 9.64 | 0.0 | 31.29 | 92.98 | 48.47 | 0.67 |  |  | underutilised: SM 6 %, DRAM 10 %, L2 31 %, occ 48 % |
| planner_debate | 1024 | mir_operator:prefill_layer00 | copy | 12 | 10.02 | 0.0 | 53.1 | 0.0 | 28.97 | 51.57 | 55.57 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 65 % |
| planner_debate | 1024 | mir_operator:prefill_layer00 | elementwise_unary | 12 | 0.93 | 0.0 | 31.25 | 0.0 | 14.63 | 63.54 | 23.17 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer00 | reduce | 12 | 8.43 | 0.0 | 39.79 | 0.0 | 17.04 | 26.92 | 43.08 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer00 | elementwise_binary | 33 | 15.8 | 0.0 | 37.91 | 0.0 | 23.2 | 56.51 | 64.88 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer00 | gemm | 21 | 37.01 | 44.01 | 34.1 | 0.0 | 66.96 | 89.87 | 13.72 | 1.0 |  |  | underutilised: SM 33 %, DRAM 27 %, L2 53 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer00 | concat | 18 | 17.5 | 0.0 | 7.17 | 0.0 | 5.23 | 59.86 | 68.29 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer00 | elementwise_other | 21 | 5.17 | 0.0 | 61.1 | 0.0 | 24.25 | 49.55 | 50.11 | 0.67 |  |  | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 55 % |
| planner_debate | 1024 | mir_operator:prefill_layer00 | attention | 6 | 22.37 | 12.24 | 37.23 | 0.0 | 28.17 | 57.39 | 33.69 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer01 | copy | 12 | 9.69 | 0.0 | 53.33 | 0.0 | 29.18 | 51.69 | 55.03 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer01 | elementwise_unary | 12 | 0.86 | 0.0 | 31.34 | 0.0 | 14.57 | 64.39 | 23.04 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer01 | reduce | 12 | 8.46 | 0.0 | 39.8 | 0.0 | 16.91 | 27.73 | 41.99 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer01 | elementwise_binary | 33 | 15.68 | 0.0 | 39.59 | 0.0 | 23.86 | 57.13 | 65.37 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer01 | gemm | 21 | 37.65 | 43.86 | 33.46 | 0.0 | 67.14 | 89.84 | 13.75 | 1.0 |  |  | underutilised: SM 34 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer01 | concat | 18 | 17.75 | 0.0 | 7.1 | 0.0 | 5.18 | 59.98 | 67.95 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 68 % |
| planner_debate | 1024 | mir_operator:prefill_layer01 | elementwise_other | 21 | 5.44 | 0.0 | 60.86 | 0.0 | 25.02 | 49.56 | 49.95 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer01 | attention | 6 | 22.17 | 12.33 | 37.59 | 0.0 | 28.05 | 57.49 | 33.78 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer02 | copy | 12 | 9.87 | 0.0 | 53.6 | 0.0 | 28.52 | 51.73 | 55.07 | 1.0 |  |  | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 63 % |
| planner_debate | 1024 | mir_operator:prefill_layer02 | elementwise_unary | 12 | 0.93 | 0.0 | 31.38 | 0.0 | 14.54 | 66.13 | 22.99 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer02 | reduce | 12 | 8.4 | 0.0 | 39.15 | 0.0 | 16.74 | 27.24 | 42.43 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer02 | elementwise_binary | 33 | 15.23 | 0.0 | 39.77 | 0.0 | 23.9 | 56.69 | 64.97 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer02 | gemm | 21 | 36.93 | 44.02 | 33.1 | 0.0 | 66.62 | 89.85 | 13.71 | 1.0 |  |  | underutilised: SM 34 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer02 | concat | 18 | 17.69 | 0.0 | 7.15 | 0.0 | 5.23 | 60.68 | 68.44 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer02 | elementwise_other | 21 | 5.14 | 0.0 | 60.03 | 0.0 | 23.75 | 48.8 | 49.15 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer02 | attention | 6 | 22.09 | 12.24 | 38.55 | 0.0 | 28.13 | 57.45 | 33.7 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer03 | copy | 12 | 10.0 | 0.0 | 53.2 | 0.0 | 28.67 | 51.63 | 54.88 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer03 | elementwise_unary | 12 | 0.87 | 0.0 | 31.53 | 0.0 | 14.8 | 68.96 | 23.01 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer03 | reduce | 12 | 8.52 | 0.0 | 39.5 | 0.0 | 17.04 | 27.33 | 41.62 | 0.34 |  |  | underutilised: SM 2 %, DRAM 49 %, L2 19 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer03 | elementwise_binary | 33 | 15.8 | 0.0 | 39.35 | 0.0 | 23.79 | 57.17 | 65.45 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer03 | gemm | 21 | 37.69 | 44.01 | 33.42 | 0.0 | 66.71 | 89.86 | 13.78 | 1.0 |  |  | underutilised: SM 34 %, DRAM 28 %, L2 54 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer03 | concat | 18 | 17.64 | 0.0 | 7.18 | 0.0 | 5.21 | 60.6 | 67.87 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer03 | elementwise_other | 21 | 5.46 | 0.0 | 60.8 | 0.0 | 24.0 | 50.42 | 49.7 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer03 | attention | 6 | 22.4 | 12.26 | 38.84 | 0.0 | 28.04 | 57.24 | 33.86 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer04 | copy | 12 | 9.9 | 0.0 | 52.81 | 0.0 | 28.72 | 51.71 | 55.13 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 63 % |
| planner_debate | 1024 | mir_operator:prefill_layer04 | elementwise_unary | 12 | 0.93 | 0.0 | 31.38 | 0.0 | 14.58 | 69.48 | 23.09 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer04 | reduce | 12 | 8.47 | 0.0 | 39.2 | 0.0 | 16.7 | 27.02 | 42.81 | 0.34 |  |  | underutilised: SM 2 %, DRAM 52 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer04 | elementwise_binary | 33 | 15.58 | 0.0 | 38.93 | 0.0 | 23.5 | 56.76 | 65.65 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer04 | gemm | 21 | 37.37 | 43.97 | 33.81 | 0.0 | 66.51 | 89.83 | 13.74 | 1.0 |  |  | underutilised: SM 34 %, DRAM 27 %, L2 53 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer04 | concat | 18 | 17.63 | 0.0 | 7.21 | 0.0 | 5.24 | 61.9 | 67.6 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 68 % |
| planner_debate | 1024 | mir_operator:prefill_layer04 | elementwise_other | 21 | 5.47 | 0.0 | 55.33 | 0.0 | 21.92 | 50.42 | 49.79 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer04 | attention | 6 | 22.41 | 12.19 | 38.26 | 0.0 | 27.99 | 57.35 | 33.67 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer05 | copy | 12 | 10.04 | 0.0 | 52.82 | 0.0 | 29.06 | 51.72 | 55.56 | 1.0 |  |  | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer05 | elementwise_unary | 12 | 0.92 | 0.0 | 31.17 | 0.0 | 14.71 | 69.95 | 22.92 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer05 | reduce | 12 | 8.6 | 0.0 | 39.66 | 0.0 | 16.79 | 27.38 | 42.79 | 0.34 |  |  | underutilised: SM 2 %, DRAM 52 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer05 | elementwise_binary | 33 | 15.79 | 0.0 | 39.71 | 0.0 | 24.22 | 56.69 | 64.89 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer05 | gemm | 21 | 37.13 | 43.99 | 34.05 | 0.0 | 66.77 | 89.89 | 13.8 | 1.0 |  |  | underutilised: SM 33 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer05 | concat | 18 | 17.6 | 0.0 | 7.14 | 0.0 | 5.04 | 61.46 | 68.04 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 68 % |
| planner_debate | 1024 | mir_operator:prefill_layer05 | elementwise_other | 21 | 5.12 | 0.0 | 60.8 | 0.0 | 24.03 | 49.16 | 49.97 | 0.67 |  |  | underutilised: SM 13 %, DRAM 31 %, L2 18 %, occ 54 % |
| planner_debate | 1024 | mir_operator:prefill_layer05 | attention | 6 | 22.23 | 12.22 | 37.79 | 0.0 | 27.85 | 57.51 | 33.98 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 29 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer06 | copy | 12 | 9.75 | 0.0 | 52.94 | 0.0 | 28.74 | 51.66 | 55.32 | 1.0 |  |  | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 65 % |
| planner_debate | 1024 | mir_operator:prefill_layer06 | elementwise_unary | 12 | 0.92 | 0.0 | 32.98 | 0.0 | 14.39 | 51.71 | 23.04 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer06 | reduce | 12 | 8.37 | 0.0 | 39.44 | 0.0 | 16.89 | 27.33 | 42.75 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer06 | elementwise_binary | 33 | 15.93 | 0.0 | 38.73 | 0.0 | 23.26 | 56.9 | 64.99 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer06 | gemm | 21 | 37.16 | 43.94 | 34.12 | 0.0 | 66.8 | 89.87 | 13.72 | 1.0 |  |  | underutilised: SM 34 %, DRAM 27 %, L2 52 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer06 | concat | 18 | 17.63 | 0.0 | 7.66 | 0.0 | 5.08 | 60.15 | 68.12 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer06 | elementwise_other | 21 | 5.39 | 0.0 | 61.46 | 0.0 | 24.31 | 49.58 | 49.13 | 0.67 |  |  | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 56 % |
| planner_debate | 1024 | mir_operator:prefill_layer06 | attention | 6 | 22.46 | 12.25 | 37.87 | 0.0 | 27.98 | 57.48 | 33.56 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 29 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer07 | copy | 12 | 9.95 | 0.0 | 52.52 | 0.0 | 28.71 | 51.81 | 54.58 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 63 % |
| planner_debate | 1024 | mir_operator:prefill_layer07 | elementwise_unary | 12 | 0.95 | 0.0 | 31.25 | 0.0 | 14.77 | 69.58 | 23.04 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer07 | reduce | 12 | 8.3 | 0.0 | 40.8 | 0.0 | 17.18 | 27.22 | 42.76 | 0.34 |  |  | underutilised: SM 2 %, DRAM 52 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer07 | elementwise_binary | 33 | 15.76 | 0.0 | 38.1 | 0.0 | 23.53 | 56.48 | 65.75 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer07 | gemm | 21 | 37.33 | 43.94 | 33.94 | 0.0 | 66.91 | 89.85 | 13.75 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer07 | concat | 18 | 17.56 | 0.0 | 7.54 | 0.0 | 5.13 | 60.09 | 68.46 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer07 | elementwise_other | 21 | 5.48 | 0.0 | 60.52 | 0.0 | 23.86 | 49.51 | 48.94 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer07 | attention | 6 | 22.34 | 12.16 | 37.12 | 0.0 | 27.88 | 57.45 | 33.62 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer08 | copy | 12 | 9.8 | 0.0 | 52.76 | 0.0 | 28.71 | 51.61 | 49.94 | 1.0 |  |  | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer08 | elementwise_unary | 12 | 0.92 | 0.0 | 31.38 | 0.0 | 14.55 | 65.82 | 22.99 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer08 | reduce | 12 | 2.87 | 0.0 | 39.59 | 0.0 | 16.94 | 27.21 | 42.46 | 0.34 |  |  | underutilised: SM 2 %, DRAM 52 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer08 | elementwise_binary | 33 | 15.7 | 0.0 | 39.89 | 0.0 | 23.99 | 57.09 | 65.04 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer08 | gemm | 21 | 37.1 | 43.95 | 33.23 | 0.0 | 67.09 | 89.85 | 13.76 | 1.0 |  |  | underutilised: SM 34 %, DRAM 27 %, L2 53 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer08 | concat | 18 | 17.57 | 0.0 | 7.09 | 0.0 | 5.01 | 60.59 | 68.34 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer08 | elementwise_other | 21 | 5.42 | 0.0 | 61.1 | 0.0 | 24.17 | 50.43 | 49.46 | 0.67 |  |  | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 55 % |
| planner_debate | 1024 | mir_operator:prefill_layer08 | attention | 6 | 22.53 | 12.23 | 38.44 | 0.0 | 28.04 | 57.42 | 33.82 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer09 | copy | 12 | 9.77 | 0.0 | 52.29 | 0.0 | 28.78 | 51.54 | 54.95 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer09 | elementwise_unary | 12 | 0.92 | 0.0 | 31.26 | 0.0 | 14.75 | 69.48 | 23.01 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer09 | reduce | 12 | 8.4 | 0.0 | 39.69 | 0.0 | 16.86 | 27.52 | 43.25 | 0.34 |  |  | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer09 | elementwise_binary | 33 | 15.86 | 0.0 | 39.77 | 0.0 | 23.81 | 56.81 | 64.43 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer09 | gemm | 21 | 37.46 | 43.79 | 34.27 | 0.0 | 66.98 | 89.85 | 13.69 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 54 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer09 | concat | 18 | 17.78 | 0.0 | 7.16 | 0.0 | 5.32 | 60.4 | 68.39 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer09 | elementwise_other | 21 | 5.48 | 0.0 | 61.09 | 0.0 | 24.12 | 49.05 | 50.01 | 0.67 |  |  | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 54 % |
| planner_debate | 1024 | mir_operator:prefill_layer09 | attention | 6 | 22.46 | 12.23 | 37.72 | 0.0 | 27.48 | 57.36 | 33.77 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 29 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer10 | copy | 12 | 9.95 | 0.0 | 52.63 | 0.0 | 28.78 | 51.73 | 54.65 | 1.0 |  |  | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 63 % |
| planner_debate | 1024 | mir_operator:prefill_layer10 | elementwise_unary | 12 | 0.92 | 0.0 | 31.47 | 0.0 | 14.83 | 69.43 | 23.09 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer10 | reduce | 12 | 8.42 | 0.0 | 39.37 | 0.0 | 16.79 | 27.34 | 41.32 | 0.34 |  |  | underutilised: SM 2 %, DRAM 50 %, L2 21 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer10 | elementwise_binary | 33 | 15.69 | 0.0 | 39.47 | 0.0 | 23.71 | 56.93 | 65.32 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer10 | gemm | 21 | 38.01 | 43.85 | 33.6 | 0.0 | 66.97 | 89.85 | 13.82 | 1.0 |  |  | underutilised: SM 34 %, DRAM 28 %, L2 56 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer10 | concat | 18 | 17.73 | 0.0 | 7.44 | 0.0 | 5.19 | 60.37 | 68.25 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer10 | elementwise_other | 21 | 5.48 | 0.0 | 63.03 | 0.0 | 23.82 | 48.3 | 49.62 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer10 | attention | 6 | 22.42 | 12.15 | 37.77 | 0.0 | 28.19 | 57.37 | 33.57 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer11 | copy | 12 | 9.82 | 0.0 | 51.59 | 0.0 | 29.06 | 51.53 | 54.84 | 1.0 |  |  | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer11 | elementwise_unary | 12 | 0.93 | 0.0 | 30.79 | 0.0 | 14.27 | 69.66 | 22.97 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer11 | reduce | 12 | 8.47 | 0.0 | 39.13 | 0.0 | 16.71 | 27.45 | 42.43 | 0.34 |  |  | underutilised: SM 2 %, DRAM 49 %, L2 19 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer11 | elementwise_binary | 33 | 15.67 | 0.0 | 39.41 | 0.0 | 23.71 | 56.63 | 64.42 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer11 | gemm | 21 | 37.06 | 42.92 | 33.51 | 0.0 | 66.91 | 89.83 | 13.74 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer11 | concat | 18 | 17.61 | 0.0 | 7.2 | 0.0 | 5.2 | 60.66 | 68.46 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer11 | elementwise_other | 21 | 5.31 | 0.0 | 61.61 | 0.0 | 24.3 | 49.71 | 48.68 | 0.67 |  |  | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 56 % |
| planner_debate | 1024 | mir_operator:prefill_layer11 | attention | 6 | 22.38 | 12.34 | 39.22 | 0.0 | 28.44 | 56.35 | 33.76 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer12 | copy | 12 | 9.9 | 0.0 | 53.11 | 0.0 | 28.97 | 51.63 | 55.22 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer12 | elementwise_unary | 12 | 0.93 | 0.0 | 31.43 | 0.0 | 14.59 | 69.78 | 22.98 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer12 | reduce | 12 | 8.5 | 0.0 | 39.26 | 0.0 | 16.79 | 27.2 | 43.34 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer12 | elementwise_binary | 33 | 15.65 | 0.0 | 39.41 | 0.0 | 23.72 | 56.57 | 64.32 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer12 | gemm | 21 | 37.07 | 43.92 | 34.24 | 0.0 | 66.71 | 89.84 | 13.75 | 1.0 |  |  | underutilised: SM 34 %, DRAM 28 %, L2 54 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer12 | concat | 18 | 17.61 | 0.0 | 7.07 | 0.0 | 5.22 | 60.09 | 67.91 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer12 | elementwise_other | 21 | 5.26 | 0.0 | 61.17 | 0.0 | 24.17 | 49.62 | 49.43 | 0.67 |  |  | underutilised: SM 13 %, DRAM 31 %, L2 18 %, occ 56 % |
| planner_debate | 1024 | mir_operator:prefill_layer12 | attention | 6 | 22.59 | 12.23 | 38.1 | 0.0 | 27.83 | 57.49 | 33.64 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 29 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer13 | copy | 12 | 9.95 | 0.0 | 52.17 | 0.0 | 28.31 | 51.65 | 54.54 | 1.0 |  |  | underutilised: SM 19 %, DRAM 35 %, L2 33 %, occ 63 % |
| planner_debate | 1024 | mir_operator:prefill_layer13 | elementwise_unary | 12 | 0.93 | 0.0 | 30.9 | 0.0 | 14.43 | 67.93 | 22.98 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer13 | reduce | 12 | 8.69 | 0.0 | 38.81 | 0.0 | 16.73 | 27.26 | 41.59 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer13 | elementwise_binary | 33 | 15.69 | 0.0 | 39.59 | 0.0 | 23.82 | 56.66 | 65.36 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer13 | gemm | 21 | 37.11 | 43.36 | 33.52 | 0.0 | 58.52 | 89.85 | 13.8 | 1.0 |  |  | underutilised: SM 34 %, DRAM 27 %, L2 53 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer13 | concat | 18 | 17.76 | 0.0 | 7.09 | 0.0 | 5.14 | 61.42 | 68.74 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer13 | elementwise_other | 21 | 5.37 | 0.0 | 60.88 | 0.0 | 24.08 | 49.46 | 49.89 | 0.67 |  |  | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 56 % |
| planner_debate | 1024 | mir_operator:prefill_layer13 | attention | 6 | 22.43 | 12.28 | 37.96 | 0.0 | 28.18 | 57.46 | 34.11 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer14 | copy | 12 | 9.84 | 0.0 | 53.03 | 0.0 | 28.88 | 51.59 | 54.54 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer14 | elementwise_unary | 12 | 0.93 | 0.0 | 31.39 | 0.0 | 14.8 | 69.4 | 22.96 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer14 | reduce | 12 | 8.51 | 0.0 | 39.64 | 0.0 | 17.41 | 27.33 | 41.98 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer14 | elementwise_binary | 33 | 15.91 | 0.0 | 40.21 | 0.0 | 23.81 | 56.95 | 65.72 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer14 | gemm | 21 | 37.75 | 43.97 | 33.63 | 0.0 | 66.86 | 89.84 | 13.84 | 1.0 |  |  | underutilised: SM 34 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer14 | concat | 18 | 17.69 | 0.0 | 7.18 | 0.0 | 5.14 | 60.01 | 68.06 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 68 % |
| planner_debate | 1024 | mir_operator:prefill_layer14 | elementwise_other | 21 | 4.5 | 0.0 | 59.9 | 0.0 | 23.26 | 49.11 | 49.9 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer14 | attention | 6 | 22.32 | 12.26 | 38.29 | 0.0 | 27.73 | 57.48 | 33.67 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 29 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer15 | copy | 12 | 9.81 | 0.0 | 53.09 | 0.0 | 28.74 | 51.72 | 53.55 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer15 | elementwise_unary | 12 | 0.93 | 0.0 | 31.38 | 0.0 | 14.61 | 69.03 | 23.11 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer15 | reduce | 12 | 8.58 | 0.0 | 39.96 | 0.0 | 17.12 | 26.71 | 42.52 | 0.34 |  |  | underutilised: SM 2 %, DRAM 52 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer15 | elementwise_binary | 33 | 15.95 | 0.0 | 39.11 | 0.0 | 23.59 | 56.66 | 65.63 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer15 | gemm | 21 | 36.89 | 44.02 | 33.63 | 0.0 | 67.07 | 89.84 | 13.72 | 1.0 |  |  | underutilised: SM 34 %, DRAM 28 %, L2 54 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer15 | concat | 18 | 17.7 | 0.0 | 7.17 | 0.0 | 5.27 | 60.31 | 67.9 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 68 % |
| planner_debate | 1024 | mir_operator:prefill_layer15 | elementwise_other | 21 | 5.52 | 0.0 | 59.75 | 0.0 | 23.6 | 50.38 | 50.0 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer15 | attention | 6 | 22.46 | 12.32 | 37.76 | 0.0 | 28.12 | 57.48 | 33.74 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 29 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer16 | copy | 12 | 10.01 | 0.0 | 53.23 | 0.0 | 28.48 | 50.92 | 55.48 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer16 | elementwise_unary | 12 | 0.93 | 0.0 | 31.38 | 0.0 | 14.58 | 68.24 | 23.11 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer16 | reduce | 12 | 8.36 | 0.0 | 40.44 | 0.0 | 17.25 | 26.98 | 42.87 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer16 | elementwise_binary | 33 | 15.74 | 0.0 | 39.59 | 0.0 | 23.97 | 56.71 | 64.7 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer16 | gemm | 21 | 37.24 | 43.99 | 34.33 | 0.0 | 67.15 | 89.83 | 13.83 | 1.0 |  |  | underutilised: SM 34 %, DRAM 27 %, L2 53 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer16 | concat | 18 | 17.77 | 0.0 | 7.12 | 0.0 | 5.24 | 60.86 | 67.94 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer16 | elementwise_other | 21 | 5.51 | 0.0 | 59.06 | 0.0 | 23.38 | 50.43 | 48.8 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer16 | attention | 6 | 22.48 | 12.21 | 37.69 | 0.0 | 28.18 | 57.45 | 33.76 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer17 | copy | 12 | 9.79 | 0.0 | 52.84 | 0.0 | 28.47 | 51.76 | 55.09 | 1.0 |  |  | underutilised: SM 20 %, DRAM 36 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer17 | elementwise_unary | 12 | 0.92 | 0.0 | 31.3 | 0.0 | 14.77 | 69.14 | 23.03 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer17 | reduce | 12 | 8.21 | 0.0 | 39.7 | 0.0 | 16.95 | 27.61 | 43.34 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer17 | elementwise_binary | 33 | 15.45 | 0.0 | 39.95 | 0.0 | 24.04 | 56.7 | 64.66 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer17 | gemm | 21 | 37.08 | 44.02 | 34.31 | 0.0 | 67.16 | 89.85 | 13.75 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 54 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer17 | concat | 18 | 17.49 | 0.0 | 6.96 | 0.0 | 4.97 | 60.86 | 67.85 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer17 | elementwise_other | 21 | 5.21 | 0.0 | 61.02 | 0.0 | 24.11 | 49.45 | 49.47 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer17 | attention | 6 | 22.54 | 12.21 | 37.87 | 0.0 | 28.18 | 57.43 | 33.69 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer18 | copy | 12 | 9.8 | 0.0 | 53.1 | 0.0 | 28.68 | 51.55 | 55.54 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 63 % |
| planner_debate | 1024 | mir_operator:prefill_layer18 | elementwise_unary | 12 | 0.92 | 0.0 | 31.42 | 0.0 | 14.6 | 69.02 | 22.98 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer18 | reduce | 12 | 8.46 | 0.0 | 39.51 | 0.0 | 17.01 | 27.46 | 41.93 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer18 | elementwise_binary | 33 | 15.76 | 0.0 | 39.41 | 0.0 | 23.85 | 57.15 | 65.57 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer18 | gemm | 21 | 37.03 | 43.91 | 33.54 | 0.0 | 66.87 | 89.86 | 13.84 | 1.0 |  |  | underutilised: SM 35 %, DRAM 27 %, L2 54 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer18 | concat | 18 | 17.68 | 0.0 | 7.58 | 0.0 | 5.15 | 60.48 | 68.76 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer18 | elementwise_other | 21 | 5.48 | 0.0 | 61.02 | 0.0 | 24.08 | 50.34 | 49.97 | 0.67 |  |  | underutilised: SM 13 %, DRAM 31 %, L2 18 %, occ 54 % |
| planner_debate | 1024 | mir_operator:prefill_layer18 | attention | 6 | 22.2 | 12.31 | 37.92 | 0.0 | 28.15 | 57.4 | 34.07 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer19 | copy | 12 | 9.8 | 0.0 | 52.66 | 0.0 | 28.83 | 51.53 | 55.3 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer19 | elementwise_unary | 12 | 0.93 | 0.0 | 31.08 | 0.0 | 14.42 | 69.57 | 23.08 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer19 | reduce | 12 | 8.32 | 0.0 | 39.11 | 0.0 | 16.52 | 26.37 | 44.2 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer19 | elementwise_binary | 33 | 15.22 | 0.0 | 39.95 | 0.0 | 23.99 | 57.14 | 65.37 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer19 | gemm | 21 | 37.13 | 44.01 | 34.22 | 0.0 | 67.09 | 89.84 | 13.79 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 56 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer19 | concat | 18 | 17.57 | 0.0 | 7.16 | 0.0 | 5.25 | 61.56 | 68.0 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer19 | elementwise_other | 21 | 5.12 | 0.0 | 59.2 | 0.0 | 23.48 | 50.43 | 47.89 | 0.67 |  |  | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 54 % |
| planner_debate | 1024 | mir_operator:prefill_layer19 | attention | 6 | 22.58 | 12.24 | 38.5 | 0.0 | 28.04 | 57.29 | 33.82 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer20 | copy | 12 | 9.81 | 0.0 | 52.89 | 0.0 | 29.08 | 51.84 | 55.01 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 63 % |
| planner_debate | 1024 | mir_operator:prefill_layer20 | elementwise_unary | 12 | 0.93 | 0.0 | 31.17 | 0.0 | 14.51 | 68.32 | 22.92 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer20 | reduce | 12 | 8.32 | 0.0 | 39.3 | 0.0 | 16.98 | 27.39 | 43.47 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer20 | elementwise_binary | 33 | 15.83 | 0.0 | 39.77 | 0.0 | 24.02 | 57.42 | 65.25 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer20 | gemm | 21 | 36.75 | 42.67 | 34.24 | 0.0 | 66.95 | 89.83 | 13.79 | 1.0 |  |  | underutilised: SM 34 %, DRAM 27 %, L2 54 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer20 | concat | 18 | 17.76 | 0.0 | 7.62 | 0.0 | 5.17 | 60.55 | 68.32 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer20 | elementwise_other | 21 | 5.33 | 0.0 | 54.73 | 0.0 | 21.66 | 49.56 | 49.96 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer20 | attention | 6 | 22.35 | 12.22 | 38.24 | 0.0 | 28.06 | 57.45 | 33.79 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer21 | copy | 12 | 9.86 | 0.0 | 53.21 | 0.0 | 28.43 | 51.84 | 55.06 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 65 % |
| planner_debate | 1024 | mir_operator:prefill_layer21 | elementwise_unary | 12 | 0.93 | 0.0 | 31.56 | 0.0 | 14.94 | 53.67 | 23.08 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer21 | reduce | 12 | 8.52 | 0.0 | 38.95 | 0.0 | 16.95 | 28.22 | 43.85 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer21 | elementwise_binary | 33 | 15.51 | 0.0 | 39.23 | 0.0 | 23.53 | 56.96 | 65.24 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer21 | gemm | 21 | 37.6 | 43.95 | 34.0 | 0.0 | 66.81 | 89.85 | 13.65 | 1.0 |  |  | underutilised: SM 34 %, DRAM 27 %, L2 53 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer21 | concat | 18 | 17.76 | 0.0 | 7.2 | 0.0 | 5.15 | 60.38 | 68.63 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer21 | elementwise_other | 21 | 5.46 | 0.0 | 59.13 | 0.0 | 23.38 | 49.49 | 47.95 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer21 | attention | 6 | 22.34 | 12.22 | 38.28 | 0.0 | 28.15 | 57.44 | 34.05 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer22 | copy | 12 | 3.19 | 0.0 | 52.55 | 0.0 | 28.83 | 51.62 | 55.06 | 1.0 |  |  | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 63 % |
| planner_debate | 1024 | mir_operator:prefill_layer22 | elementwise_unary | 12 | 0.93 | 0.0 | 32.83 | 0.0 | 14.83 | 52.49 | 22.87 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer22 | reduce | 12 | 8.42 | 0.0 | 38.43 | 0.0 | 16.71 | 27.39 | 43.01 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer22 | elementwise_binary | 33 | 15.88 | 0.0 | 39.95 | 0.0 | 24.01 | 56.77 | 65.16 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer22 | gemm | 21 | 37.0 | 43.95 | 33.43 | 0.0 | 58.59 | 89.84 | 13.79 | 1.0 |  |  | underutilised: SM 35 %, DRAM 27 %, L2 54 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer22 | concat | 18 | 17.61 | 0.0 | 7.17 | 0.0 | 5.13 | 60.56 | 68.84 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 70 % |
| planner_debate | 1024 | mir_operator:prefill_layer22 | elementwise_other | 21 | 5.49 | 0.0 | 59.96 | 0.0 | 23.69 | 50.48 | 49.94 | 0.67 |  |  | underutilised: SM 14 %, DRAM 30 %, L2 18 %, occ 55 % |
| planner_debate | 1024 | mir_operator:prefill_layer22 | attention | 6 | 22.42 | 12.2 | 38.39 | 0.0 | 28.18 | 57.31 | 33.85 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer23 | copy | 12 | 9.83 | 0.0 | 51.45 | 0.0 | 29.07 | 51.74 | 54.92 | 1.0 |  |  | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer23 | elementwise_unary | 12 | 0.92 | 0.0 | 31.04 | 0.0 | 14.37 | 69.62 | 23.0 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer23 | reduce | 12 | 8.23 | 0.0 | 39.57 | 0.0 | 17.09 | 27.39 | 43.41 | 0.34 |  |  | underutilised: SM 2 %, DRAM 52 %, L2 21 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer23 | elementwise_binary | 33 | 15.71 | 0.0 | 40.14 | 0.0 | 24.01 | 57.31 | 64.83 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer23 | gemm | 21 | 37.13 | 44.0 | 33.94 | 0.0 | 66.72 | 89.84 | 13.82 | 1.0 |  |  | underutilised: SM 34 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer23 | concat | 18 | 17.68 | 0.0 | 7.13 | 0.0 | 5.31 | 60.81 | 68.03 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer23 | elementwise_other | 21 | 5.19 | 0.0 | 59.96 | 0.0 | 23.69 | 49.68 | 49.92 | 0.67 |  |  | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 53 % |
| planner_debate | 1024 | mir_operator:prefill_layer23 | attention | 6 | 22.49 | 12.3 | 38.4 | 0.0 | 28.49 | 57.48 | 34.03 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer24 | copy | 12 | 9.86 | 0.0 | 53.32 | 0.0 | 28.69 | 51.71 | 54.3 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer24 | elementwise_unary | 12 | 0.92 | 0.0 | 31.47 | 0.0 | 14.56 | 69.5 | 23.1 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer24 | reduce | 12 | 8.32 | 0.0 | 39.76 | 0.0 | 17.04 | 27.3 | 42.66 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer24 | elementwise_binary | 33 | 15.58 | 0.0 | 39.17 | 0.0 | 23.63 | 56.71 | 64.66 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer24 | gemm | 21 | 37.08 | 43.9 | 33.43 | 0.0 | 66.53 | 89.85 | 13.74 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer24 | concat | 18 | 17.6 | 0.0 | 6.77 | 0.0 | 5.08 | 60.17 | 68.4 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 67 % |
| planner_debate | 1024 | mir_operator:prefill_layer24 | elementwise_other | 21 | 5.37 | 0.0 | 61.46 | 0.0 | 24.33 | 49.6 | 49.35 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer24 | attention | 6 | 22.39 | 12.25 | 38.19 | 0.0 | 28.32 | 57.46 | 34.01 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer25 | copy | 12 | 9.72 | 0.0 | 53.18 | 0.0 | 28.76 | 51.53 | 55.09 | 1.0 |  |  | underutilised: SM 20 %, DRAM 36 %, L2 33 %, occ 63 % |
| planner_debate | 1024 | mir_operator:prefill_layer25 | elementwise_unary | 12 | 0.93 | 0.0 | 31.47 | 0.0 | 14.78 | 69.29 | 22.94 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer25 | reduce | 12 | 8.2 | 0.0 | 38.52 | 0.0 | 16.49 | 27.34 | 42.55 | 0.34 |  |  | underutilised: SM 2 %, DRAM 53 %, L2 21 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer25 | elementwise_binary | 33 | 15.84 | 0.0 | 38.68 | 0.0 | 22.5 | 56.73 | 64.86 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer25 | gemm | 21 | 37.02 | 43.94 | 33.97 | 0.0 | 66.81 | 89.88 | 13.67 | 1.0 |  |  | underutilised: SM 33 %, DRAM 27 %, L2 53 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer25 | concat | 18 | 17.71 | 0.0 | 7.02 | 0.0 | 5.14 | 61.13 | 67.74 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 68 % |
| planner_debate | 1024 | mir_operator:prefill_layer25 | elementwise_other | 21 | 5.38 | 0.0 | 60.8 | 0.0 | 24.12 | 49.59 | 48.66 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer25 | attention | 6 | 22.49 | 12.26 | 38.2 | 0.0 | 28.17 | 57.43 | 33.69 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer26 | copy | 12 | 9.84 | 0.0 | 52.82 | 0.0 | 28.59 | 51.58 | 54.97 | 1.0 |  |  | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer26 | elementwise_unary | 12 | 0.93 | 0.0 | 31.34 | 0.0 | 14.79 | 65.27 | 22.95 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer26 | reduce | 12 | 8.31 | 0.0 | 39.27 | 0.0 | 16.92 | 27.38 | 41.92 | 0.34 |  |  | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer26 | elementwise_binary | 33 | 15.97 | 0.0 | 39.53 | 0.0 | 23.91 | 56.99 | 64.89 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer26 | gemm | 21 | 37.26 | 43.89 | 33.77 | 0.0 | 67.25 | 89.83 | 13.71 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer26 | concat | 18 | 17.72 | 0.0 | 7.03 | 0.0 | 5.29 | 60.15 | 67.96 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 68 % |
| planner_debate | 1024 | mir_operator:prefill_layer26 | elementwise_other | 21 | 4.69 | 0.0 | 60.31 | 0.0 | 23.84 | 49.4 | 48.63 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer26 | attention | 6 | 22.52 | 12.33 | 37.35 | 0.0 | 25.71 | 57.49 | 33.65 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 29 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer27 | copy | 12 | 2.44 | 0.0 | 53.02 | 0.0 | 28.72 | 51.74 | 55.8 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer27 | elementwise_unary | 12 | 0.93 | 0.0 | 31.38 | 0.0 | 14.59 | 68.85 | 23.07 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer27 | reduce | 12 | 8.24 | 0.0 | 39.9 | 0.0 | 17.07 | 26.44 | 42.18 | 0.34 |  |  | underutilised: SM 2 %, DRAM 50 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer27 | elementwise_binary | 33 | 15.83 | 0.0 | 40.21 | 0.0 | 24.19 | 56.93 | 64.65 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer27 | gemm | 21 | 36.79 | 44.01 | 33.34 | 0.0 | 67.17 | 89.85 | 14.95 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer27 | concat | 18 | 17.59 | 0.0 | 7.13 | 0.0 | 5.21 | 60.13 | 68.41 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer27 | elementwise_other | 21 | 5.52 | 0.0 | 59.54 | 0.0 | 23.49 | 49.41 | 49.96 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer27 | attention | 6 | 22.59 | 12.22 | 38.39 | 0.0 | 28.19 | 57.43 | 33.77 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer28 | copy | 12 | 9.95 | 0.0 | 53.2 | 0.0 | 28.86 | 51.83 | 49.89 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer28 | elementwise_unary | 12 | 0.93 | 0.0 | 30.88 | 0.0 | 14.34 | 69.49 | 23.05 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer28 | reduce | 12 | 8.21 | 0.0 | 39.4 | 0.0 | 16.9 | 27.2 | 41.92 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer28 | elementwise_binary | 33 | 15.6 | 0.0 | 39.77 | 0.0 | 23.98 | 57.82 | 65.69 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer28 | gemm | 21 | 37.61 | 44.02 | 33.71 | 0.0 | 67.08 | 89.85 | 13.8 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer28 | concat | 18 | 17.54 | 0.0 | 6.94 | 0.0 | 5.22 | 61.06 | 68.29 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 68 % |
| planner_debate | 1024 | mir_operator:prefill_layer28 | elementwise_other | 21 | 5.48 | 0.0 | 60.6 | 0.0 | 23.92 | 50.43 | 48.89 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer28 | attention | 6 | 22.38 | 12.32 | 38.2 | 0.0 | 28.16 | 57.4 | 33.68 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer29 | copy | 12 | 9.73 | 0.0 | 53.22 | 0.0 | 28.53 | 51.67 | 55.0 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer29 | elementwise_unary | 12 | 0.93 | 0.0 | 33.33 | 0.0 | 14.83 | 51.17 | 23.05 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer29 | reduce | 12 | 8.36 | 0.0 | 39.49 | 0.0 | 17.2 | 27.26 | 42.56 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer29 | elementwise_binary | 33 | 15.57 | 0.0 | 39.59 | 0.0 | 23.83 | 57.09 | 65.75 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer29 | gemm | 21 | 37.06 | 44.0 | 33.54 | 0.0 | 66.89 | 89.84 | 13.75 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer29 | concat | 18 | 17.7 | 0.0 | 7.49 | 0.0 | 5.1 | 60.77 | 68.41 | 1.33 |  |  | underutilised: SM 17 %, DRAM 8 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer29 | elementwise_other | 21 | 5.25 | 0.0 | 60.16 | 0.0 | 23.78 | 49.36 | 48.57 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer29 | attention | 6 | 22.34 | 12.2 | 38.05 | 0.0 | 28.2 | 57.32 | 33.64 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer30 | copy | 12 | 9.71 | 0.0 | 52.96 | 0.0 | 28.53 | 51.15 | 54.5 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 32 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer30 | elementwise_unary | 12 | 0.93 | 0.0 | 31.17 | 0.0 | 14.48 | 69.54 | 23.01 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer30 | reduce | 12 | 8.37 | 0.0 | 40.86 | 0.0 | 16.78 | 26.62 | 43.26 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer30 | elementwise_binary | 33 | 15.49 | 0.0 | 39.53 | 0.0 | 23.59 | 56.47 | 65.67 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer30 | gemm | 21 | 37.09 | 43.84 | 33.59 | 0.0 | 66.94 | 89.87 | 13.79 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 54 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer30 | concat | 18 | 17.75 | 0.0 | 7.2 | 0.0 | 5.26 | 59.45 | 68.12 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer30 | elementwise_other | 21 | 5.37 | 0.0 | 59.61 | 0.0 | 23.65 | 50.4 | 49.35 | 0.67 |  |  | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 54 % |
| planner_debate | 1024 | mir_operator:prefill_layer30 | attention | 6 | 22.57 | 12.24 | 37.83 | 0.0 | 28.08 | 57.37 | 34.03 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer31 | copy | 12 | 10.01 | 0.0 | 48.8 | 0.0 | 28.93 | 50.93 | 55.44 | 1.0 |  |  | underutilised: SM 19 %, DRAM 34 %, L2 32 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer31 | elementwise_unary | 12 | 0.93 | 0.0 | 31.38 | 0.0 | 14.61 | 69.98 | 22.93 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer31 | reduce | 12 | 8.37 | 0.0 | 39.67 | 0.0 | 17.01 | 26.79 | 42.28 | 0.34 |  |  | underutilised: SM 2 %, DRAM 52 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer31 | elementwise_binary | 33 | 15.92 | 0.0 | 39.41 | 0.0 | 23.78 | 56.43 | 64.65 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer31 | gemm | 21 | 37.85 | 43.95 | 33.68 | 0.0 | 67.03 | 89.93 | 13.72 | 1.0 |  |  | underutilised: SM 34 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer31 | concat | 18 | 17.44 | 0.0 | 6.93 | 0.0 | 5.16 | 59.96 | 68.52 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 70 % |
| planner_debate | 1024 | mir_operator:prefill_layer31 | elementwise_other | 21 | 5.19 | 0.0 | 60.24 | 0.0 | 23.89 | 49.6 | 49.88 | 0.67 |  |  | underutilised: SM 14 %, DRAM 31 %, L2 19 %, occ 54 % |
| planner_debate | 1024 | mir_operator:prefill_layer31 | attention | 6 | 22.17 | 12.24 | 38.48 | 0.0 | 28.21 | 57.46 | 33.8 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer32 | copy | 12 | 9.74 | 0.0 | 49.22 | 0.0 | 28.61 | 51.5 | 54.55 | 1.0 |  |  | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer32 | elementwise_unary | 12 | 0.92 | 0.0 | 31.17 | 0.0 | 14.48 | 69.74 | 23.15 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer32 | reduce | 12 | 8.4 | 0.0 | 39.83 | 0.0 | 17.28 | 27.43 | 43.14 | 0.34 |  |  | underutilised: SM 2 %, DRAM 53 %, L2 21 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer32 | elementwise_binary | 33 | 16.01 | 0.0 | 38.78 | 0.0 | 22.62 | 56.94 | 65.3 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer32 | gemm | 21 | 37.34 | 43.23 | 34.0 | 0.0 | 66.66 | 89.85 | 13.78 | 1.0 |  |  | underutilised: SM 34 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer32 | concat | 18 | 17.81 | 0.0 | 7.21 | 0.0 | 5.28 | 61.08 | 68.75 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer32 | elementwise_other | 21 | 5.42 | 0.0 | 59.68 | 0.0 | 23.57 | 50.46 | 48.06 | 0.67 |  |  | underutilised: SM 13 %, DRAM 31 %, L2 18 %, occ 55 % |
| planner_debate | 1024 | mir_operator:prefill_layer32 | attention | 6 | 22.46 | 12.25 | 37.65 | 0.0 | 28.09 | 57.48 | 33.68 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer33 | copy | 12 | 9.85 | 0.0 | 52.99 | 0.0 | 28.9 | 51.6 | 55.26 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer33 | elementwise_unary | 12 | 0.93 | 0.0 | 31.6 | 0.0 | 14.63 | 69.97 | 22.94 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer33 | reduce | 12 | 8.3 | 0.0 | 39.79 | 0.0 | 16.77 | 27.76 | 42.49 | 0.34 |  |  | underutilised: SM 2 %, DRAM 52 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer33 | elementwise_binary | 33 | 15.63 | 0.0 | 39.59 | 0.0 | 23.84 | 56.5 | 64.92 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer33 | gemm | 21 | 37.91 | 43.97 | 34.25 | 0.0 | 67.16 | 89.85 | 13.74 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 54 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer33 | concat | 18 | 17.73 | 0.0 | 7.19 | 0.0 | 5.21 | 60.5 | 68.01 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer33 | elementwise_other | 21 | 5.47 | 0.0 | 59.33 | 0.0 | 23.56 | 49.48 | 48.85 | 0.67 |  |  | underutilised: SM 14 %, DRAM 31 %, L2 18 %, occ 55 % |
| planner_debate | 1024 | mir_operator:prefill_layer33 | attention | 6 | 22.31 | 12.2 | 37.24 | 0.0 | 28.08 | 57.48 | 33.71 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer34 | copy | 12 | 9.83 | 0.0 | 53.01 | 0.0 | 28.67 | 51.65 | 54.75 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer34 | elementwise_unary | 12 | 0.94 | 0.0 | 31.13 | 0.0 | 14.44 | 69.31 | 22.92 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer34 | reduce | 12 | 8.13 | 0.0 | 40.11 | 0.0 | 17.11 | 26.31 | 42.75 | 0.34 |  |  | underutilised: SM 2 %, DRAM 51 %, L2 20 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer34 | elementwise_binary | 33 | 15.73 | 0.0 | 39.65 | 0.0 | 23.82 | 57.01 | 65.5 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer34 | gemm | 21 | 37.07 | 44.0 | 33.44 | 0.0 | 66.95 | 89.94 | 13.8 | 1.0 |  |  | underutilised: SM 34 %, DRAM 28 %, L2 54 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer34 | concat | 18 | 17.65 | 0.0 | 6.99 | 0.0 | 5.17 | 60.53 | 68.67 | 1.33 |  |  | underutilised: SM 17 %, DRAM 5 %, L2 5 %, occ 69 % |
| planner_debate | 1024 | mir_operator:prefill_layer34 | elementwise_other | 21 | 5.43 | 0.0 | 59.06 | 0.0 | 24.49 | 49.65 | 41.16 | 0.67 |  |  | latency/launch-bound: 0.67 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer34 | attention | 6 | 22.41 | 12.24 | 38.13 | 0.0 | 28.13 | 57.45 | 33.72 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer35 | copy | 12 | 9.69 | 0.0 | 53.05 | 0.0 | 29.05 | 51.59 | 54.89 | 1.0 |  |  | underutilised: SM 20 %, DRAM 35 %, L2 33 %, occ 64 % |
| planner_debate | 1024 | mir_operator:prefill_layer35 | elementwise_unary | 12 | 0.93 | 0.0 | 31.39 | 0.0 | 14.54 | 65.94 | 22.95 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_layer35 | reduce | 12 | 8.59 | 0.0 | 39.2 | 0.0 | 16.85 | 27.42 | 41.98 | 0.34 |  |  | underutilised: SM 2 %, DRAM 53 %, L2 21 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_layer35 | elementwise_binary | 33 | 15.71 | 0.0 | 40.08 | 0.0 | 24.26 | 56.65 | 64.56 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_layer35 | gemm | 21 | 37.58 | 43.9 | 34.16 | 0.0 | 66.83 | 89.86 | 13.88 | 1.0 |  |  | underutilised: SM 35 %, DRAM 28 %, L2 55 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_layer35 | concat | 18 | 17.58 | 0.0 | 7.11 | 0.0 | 5.2 | 60.83 | 68.22 | 1.33 |  |  | underutilised: SM 18 %, DRAM 5 %, L2 5 %, occ 68 % |
| planner_debate | 1024 | mir_operator:prefill_layer35 | elementwise_other | 21 | 5.36 | 0.0 | 59.68 | 0.0 | 23.64 | 49.52 | 48.26 | 0.67 |  |  | underutilised: SM 13 %, DRAM 30 %, L2 18 %, occ 55 % |
| planner_debate | 1024 | mir_operator:prefill_layer35 | attention | 6 | 22.43 | 12.26 | 37.91 | 0.0 | 28.27 | 57.48 | 33.88 | 1.89 |  |  | underutilised: SM 18 %, DRAM 12 %, L2 30 %, occ 8 % |
| planner_debate | 1024 | mir_operator:prefill_head | copy | 6 | 10.0 | 0.0 | 53.38 | 0.0 | 28.82 | 51.76 | 55.66 | 1.0 |  |  | underutilised: SM 20 %, DRAM 34 %, L2 32 %, occ 63 % |
| planner_debate | 1024 | mir_operator:prefill_head | elementwise_unary | 6 | 0.93 | 0.0 | 31.0 | 0.0 | 14.76 | 53.36 | 23.22 | 0.29 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:prefill_head | reduce | 3 | 1.67 | 0.0 | 52.34 | 0.0 | 20.59 | 12.55 | 33.27 | 0.08 |  |  | underutilised: SM 2 %, DRAM 52 %, L2 21 %, occ 33 % |
| planner_debate | 1024 | mir_operator:prefill_head | elementwise_binary | 9 | 16.36 | 0.0 | 39.53 | 0.0 | 23.7 | 57.55 | 65.36 | 1.33 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:prefill_head | gemm | 3 | 46.81 | 47.48 | 51.78 | 0.0 | 74.67 | 91.0 | 16.55 | 37.09 |  |  | tensor-core compute-bound |
| planner_debate | 1024 | mir_operator:prefill_sample | reduce | 3 | 2.81 | 0.0 | 5.3 | 0.0 | 3.03 | 65.23 | 33.12 | 0.05 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_embed | other | 3 | 0.26 | 0.0 | 0.34 | 0.0 | 0.66 | 87.78 | 8.31 | 0.01 |  |  | latency/launch-bound: 0.01 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer00 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.58 | 90.15 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer00 | elementwise_unary | 12 | 0.02 | 0.0 | 0.54 | 0.0 | 0.89 | 90.42 | 7.73 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer00 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.8 | 90.05 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer00 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.39 | 90.3 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer00 | gemv | 21 | 15.14 | 0.0 | 73.81 | 0.0 | 46.43 | 9.14 | 16.02 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer00 | concat | 18 | 1.59 | 0.0 | 0.31 | 0.0 | 0.73 | 94.16 | 9.73 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer00 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.07 | 88.38 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer00 | attention | 6 | 0.77 | 12.57 | 4.29 | 0.0 | 2.29 | 67.22 | 8.27 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer01 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.85 | 91.17 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer01 | elementwise_unary | 12 | 0.02 | 0.0 | 0.52 | 0.0 | 0.9 | 90.28 | 7.67 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer01 | reduce | 6 | 0.09 | 0.0 | 1.97 | 0.0 | 3.8 | 90.17 | 31.9 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer01 | elementwise_binary | 33 | 0.02 | 0.0 | 0.81 | 0.0 | 1.39 | 90.65 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer01 | gemv | 21 | 15.39 | 0.0 | 73.7 | 0.0 | 45.6 | 9.15 | 16.0 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer01 | concat | 18 | 1.65 | 0.0 | 0.31 | 0.0 | 0.69 | 91.67 | 9.72 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer01 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.05 | 87.55 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer01 | attention | 6 | 0.76 | 12.51 | 4.03 | 0.0 | 2.19 | 67.84 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer02 | copy | 12 | 0.04 | 0.0 | 0.93 | 0.0 | 1.81 | 90.56 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer02 | elementwise_unary | 12 | 0.02 | 0.0 | 0.54 | 0.0 | 0.89 | 89.67 | 7.71 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer02 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.79 | 91.15 | 31.94 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer02 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.49 | 90.09 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer02 | gemv | 21 | 14.94 | 0.0 | 73.86 | 0.0 | 44.72 | 9.15 | 16.13 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer02 | concat | 18 | 1.61 | 0.0 | 0.32 | 0.0 | 0.7 | 91.29 | 9.75 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer02 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.08 | 88.22 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer02 | attention | 6 | 0.76 | 12.63 | 4.28 | 0.0 | 2.54 | 69.41 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer03 | copy | 12 | 0.04 | 0.0 | 0.93 | 0.0 | 1.6 | 89.56 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer03 | elementwise_unary | 12 | 0.02 | 0.0 | 0.52 | 0.0 | 0.87 | 91.38 | 7.76 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer03 | reduce | 6 | 0.09 | 0.0 | 1.94 | 0.0 | 3.77 | 90.0 | 31.84 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer03 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.4 | 90.44 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer03 | gemv | 21 | 15.04 | 0.0 | 72.61 | 0.0 | 44.12 | 9.24 | 15.96 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer03 | concat | 18 | 1.63 | 0.0 | 0.31 | 0.0 | 0.7 | 92.24 | 9.76 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer03 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.07 | 84.89 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer03 | attention | 6 | 0.76 | 12.43 | 4.28 | 0.0 | 2.31 | 68.6 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer04 | copy | 12 | 0.04 | 0.0 | 1.1 | 0.0 | 1.86 | 91.01 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer04 | elementwise_unary | 12 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 91.35 | 7.62 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer04 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.78 | 90.03 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer04 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.38 | 90.23 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer04 | gemv | 21 | 15.14 | 0.0 | 73.78 | 0.0 | 45.61 | 9.24 | 15.98 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer04 | concat | 18 | 1.62 | 0.0 | 0.31 | 0.0 | 0.7 | 93.06 | 9.78 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer04 | elementwise_other | 21 | 0.02 | 0.0 | 0.8 | 0.0 | 1.4 | 86.05 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer04 | attention | 6 | 0.77 | 12.44 | 4.33 | 0.0 | 2.32 | 66.37 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer05 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.59 | 92.16 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer05 | elementwise_unary | 12 | 0.02 | 0.0 | 0.54 | 0.0 | 0.89 | 89.99 | 7.71 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer05 | reduce | 6 | 0.09 | 0.0 | 1.95 | 0.0 | 3.77 | 90.32 | 31.83 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer05 | elementwise_binary | 33 | 0.02 | 0.0 | 0.83 | 0.0 | 1.38 | 89.7 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer05 | gemv | 21 | 15.17 | 0.0 | 73.44 | 0.0 | 45.21 | 9.22 | 16.03 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer05 | concat | 18 | 1.65 | 0.0 | 0.31 | 0.0 | 0.73 | 90.33 | 9.77 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer05 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.07 | 88.43 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer05 | attention | 6 | 0.76 | 12.52 | 4.34 | 0.0 | 2.57 | 69.41 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer06 | copy | 12 | 0.04 | 0.0 | 0.93 | 0.0 | 1.77 | 88.73 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer06 | elementwise_unary | 12 | 0.02 | 0.0 | 0.53 | 0.0 | 0.89 | 91.14 | 7.64 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer06 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.79 | 90.15 | 31.85 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer06 | elementwise_binary | 33 | 0.02 | 0.0 | 0.81 | 0.0 | 1.59 | 90.59 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer06 | gemv | 21 | 15.09 | 0.0 | 73.18 | 0.0 | 43.24 | 9.25 | 16.04 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer06 | concat | 18 | 1.6 | 0.0 | 0.31 | 0.0 | 0.73 | 90.39 | 9.79 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer06 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.06 | 90.89 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer06 | attention | 6 | 0.77 | 12.57 | 4.3 | 0.0 | 2.32 | 69.64 | 8.32 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer07 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.57 | 90.78 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer07 | elementwise_unary | 12 | 0.02 | 0.0 | 0.53 | 0.0 | 0.9 | 93.61 | 7.59 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer07 | reduce | 6 | 0.09 | 0.0 | 1.95 | 0.0 | 3.79 | 90.13 | 31.89 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer07 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.43 | 91.75 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer07 | gemv | 21 | 15.06 | 0.0 | 73.56 | 0.0 | 45.04 | 9.22 | 16.02 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer07 | concat | 18 | 1.64 | 0.0 | 0.31 | 0.0 | 0.7 | 90.11 | 9.69 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer07 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.07 | 89.16 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer07 | attention | 6 | 0.76 | 12.35 | 5.7 | 0.0 | 2.6 | 58.64 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer08 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.59 | 90.98 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer08 | elementwise_unary | 12 | 0.02 | 0.0 | 0.54 | 0.0 | 0.89 | 92.74 | 7.74 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer08 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.8 | 91.61 | 31.78 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer08 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.39 | 93.68 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer08 | gemv | 21 | 15.32 | 0.0 | 73.88 | 0.0 | 45.39 | 9.08 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer08 | concat | 18 | 1.65 | 0.0 | 0.31 | 0.0 | 0.71 | 92.46 | 9.83 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer08 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.05 | 92.07 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer08 | attention | 6 | 0.77 | 12.5 | 5.77 | 0.0 | 2.53 | 56.16 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer09 | copy | 12 | 0.04 | 0.0 | 0.93 | 0.0 | 1.59 | 93.08 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer09 | elementwise_unary | 12 | 0.01 | 0.0 | 0.53 | 0.0 | 0.89 | 92.78 | 7.65 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer09 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.81 | 92.0 | 31.89 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer09 | elementwise_binary | 33 | 0.02 | 0.0 | 0.83 | 0.0 | 1.51 | 95.77 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer09 | gemv | 21 | 15.23 | 0.0 | 73.15 | 0.0 | 45.31 | 9.14 | 16.1 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer09 | concat | 18 | 1.59 | 0.0 | 0.32 | 0.0 | 0.7 | 91.2 | 9.76 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer09 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.08 | 88.67 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer09 | attention | 6 | 0.75 | 12.6 | 4.27 | 0.0 | 2.27 | 66.89 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer10 | copy | 12 | 0.04 | 0.0 | 1.09 | 0.0 | 1.59 | 89.96 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer10 | elementwise_unary | 12 | 0.02 | 0.0 | 0.52 | 0.0 | 0.89 | 89.51 | 7.55 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer10 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.81 | 91.44 | 31.82 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer10 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.39 | 93.75 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer10 | gemv | 21 | 15.28 | 0.0 | 73.97 | 0.0 | 44.41 | 9.01 | 15.92 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer10 | concat | 18 | 1.59 | 0.0 | 0.31 | 0.0 | 0.73 | 91.07 | 9.79 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer10 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.06 | 90.06 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer10 | attention | 6 | 0.76 | 12.54 | 5.66 | 0.0 | 2.5 | 58.45 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer11 | copy | 12 | 0.03 | 0.0 | 0.92 | 0.0 | 1.58 | 90.09 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer11 | elementwise_unary | 12 | 0.02 | 0.0 | 0.53 | 0.0 | 0.91 | 91.56 | 7.56 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer11 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.8 | 90.78 | 31.94 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer11 | elementwise_binary | 33 | 0.02 | 0.0 | 0.83 | 0.0 | 1.4 | 93.01 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer11 | gemv | 21 | 14.98 | 0.0 | 72.83 | 0.0 | 44.34 | 9.07 | 15.91 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer11 | concat | 18 | 1.56 | 0.0 | 0.31 | 0.0 | 0.88 | 95.48 | 9.75 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer11 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.2 | 90.28 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer11 | attention | 6 | 0.77 | 12.51 | 4.35 | 0.0 | 2.31 | 69.62 | 8.27 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer12 | copy | 12 | 0.04 | 0.0 | 0.93 | 0.0 | 1.6 | 92.19 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer12 | elementwise_unary | 12 | 0.02 | 0.0 | 0.51 | 0.0 | 0.88 | 89.08 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer12 | reduce | 6 | 0.09 | 0.0 | 1.95 | 0.0 | 3.78 | 89.75 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer12 | elementwise_binary | 33 | 0.02 | 0.0 | 0.83 | 0.0 | 1.38 | 90.61 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer12 | gemv | 21 | 15.23 | 0.0 | 73.25 | 0.0 | 45.07 | 9.2 | 16.01 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer12 | concat | 18 | 1.66 | 0.0 | 0.31 | 0.0 | 0.71 | 91.64 | 9.74 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer12 | elementwise_other | 21 | 0.02 | 0.0 | 0.82 | 0.0 | 1.05 | 89.88 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer12 | attention | 6 | 0.77 | 12.53 | 4.35 | 0.0 | 2.31 | 69.57 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer13 | copy | 12 | 0.04 | 0.0 | 0.9 | 0.0 | 1.77 | 92.11 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer13 | elementwise_unary | 12 | 0.02 | 0.0 | 0.71 | 0.0 | 0.9 | 88.5 | 7.75 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer13 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.8 | 91.96 | 31.85 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer13 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.57 | 90.46 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer13 | gemv | 21 | 15.34 | 0.0 | 74.58 | 0.0 | 42.87 | 9.26 | 16.02 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer13 | concat | 18 | 1.58 | 0.0 | 0.31 | 0.0 | 0.73 | 91.92 | 9.78 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer13 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.09 | 90.58 | 8.26 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer13 | attention | 6 | 0.75 | 12.53 | 4.33 | 0.0 | 2.34 | 69.99 | 8.31 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer14 | copy | 12 | 0.04 | 0.0 | 0.91 | 0.0 | 2.02 | 89.88 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer14 | elementwise_unary | 12 | 0.02 | 0.0 | 0.54 | 0.0 | 0.89 | 94.84 | 7.71 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer14 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.79 | 91.74 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer14 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.48 | 91.32 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer14 | gemv | 21 | 15.17 | 0.0 | 73.77 | 0.0 | 43.44 | 9.21 | 15.99 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer14 | concat | 18 | 1.53 | 0.0 | 0.31 | 0.0 | 0.73 | 89.8 | 9.79 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer14 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.07 | 91.26 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer14 | attention | 6 | 0.77 | 12.48 | 4.72 | 0.0 | 2.4 | 69.07 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer15 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.57 | 91.6 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer15 | elementwise_unary | 12 | 0.02 | 0.0 | 0.53 | 0.0 | 0.89 | 94.06 | 7.68 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer15 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.79 | 90.13 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer15 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.47 | 90.96 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer15 | gemv | 21 | 15.11 | 0.0 | 73.61 | 0.0 | 44.01 | 9.18 | 16.02 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer15 | concat | 18 | 1.65 | 0.0 | 0.31 | 0.0 | 0.71 | 94.27 | 9.82 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer15 | elementwise_other | 21 | 0.02 | 0.0 | 0.82 | 0.0 | 1.08 | 89.09 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer15 | attention | 6 | 0.77 | 12.37 | 4.36 | 0.0 | 2.33 | 67.25 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer16 | copy | 12 | 0.03 | 0.0 | 0.92 | 0.0 | 1.86 | 93.16 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer16 | elementwise_unary | 12 | 0.02 | 0.0 | 0.52 | 0.0 | 0.91 | 88.88 | 7.67 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer16 | reduce | 6 | 0.09 | 0.0 | 1.95 | 0.0 | 3.8 | 90.81 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer16 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.37 | 93.12 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer16 | gemv | 21 | 15.4 | 0.0 | 73.83 | 0.0 | 44.77 | 9.18 | 16.04 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer16 | concat | 18 | 1.61 | 0.0 | 0.35 | 0.0 | 0.73 | 90.87 | 9.72 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer16 | elementwise_other | 21 | 0.02 | 0.0 | 0.82 | 0.0 | 1.33 | 90.84 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer16 | attention | 6 | 0.76 | 12.56 | 4.28 | 0.0 | 2.46 | 69.87 | 8.31 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer17 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.96 | 93.69 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer17 | elementwise_unary | 12 | 0.02 | 0.0 | 0.53 | 0.0 | 0.89 | 92.35 | 7.67 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer17 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.8 | 89.86 | 31.83 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer17 | elementwise_binary | 33 | 0.02 | 0.0 | 0.83 | 0.0 | 1.39 | 90.53 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer17 | gemv | 21 | 15.21 | 0.0 | 74.15 | 0.0 | 44.94 | 9.05 | 16.08 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer17 | concat | 18 | 1.65 | 0.0 | 0.32 | 0.0 | 0.74 | 95.44 | 9.68 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer17 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.05 | 93.04 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer17 | attention | 6 | 0.75 | 12.56 | 4.33 | 0.0 | 2.32 | 67.66 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer18 | copy | 12 | 0.04 | 0.0 | 0.93 | 0.0 | 1.55 | 93.67 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer18 | elementwise_unary | 12 | 0.02 | 0.0 | 0.53 | 0.0 | 0.88 | 94.19 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer18 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.8 | 90.77 | 31.83 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer18 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.4 | 90.97 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer18 | gemv | 21 | 15.05 | 0.0 | 72.84 | 0.0 | 44.78 | 9.21 | 16.11 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer18 | concat | 18 | 1.64 | 0.0 | 0.3 | 0.0 | 0.7 | 94.66 | 9.82 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer18 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.05 | 93.96 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer18 | attention | 6 | 0.77 | 12.55 | 4.3 | 0.0 | 2.29 | 67.44 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer19 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.58 | 90.4 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer19 | elementwise_unary | 12 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 94.55 | 7.45 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer19 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.8 | 91.19 | 31.84 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer19 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.37 | 91.97 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer19 | gemv | 21 | 15.28 | 0.0 | 74.31 | 0.0 | 44.45 | 9.24 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer19 | concat | 18 | 1.67 | 0.0 | 0.32 | 0.0 | 0.7 | 94.19 | 9.77 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer19 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.4 | 89.96 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer19 | attention | 6 | 0.77 | 12.55 | 4.35 | 0.0 | 2.33 | 69.99 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer20 | copy | 12 | 0.04 | 0.0 | 0.9 | 0.0 | 1.55 | 87.85 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer20 | elementwise_unary | 12 | 0.02 | 0.0 | 0.53 | 0.0 | 0.9 | 88.96 | 7.58 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer20 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.79 | 91.25 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer20 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.38 | 90.59 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer20 | gemv | 21 | 15.16 | 0.0 | 73.77 | 0.0 | 43.85 | 9.04 | 15.88 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer20 | concat | 18 | 1.65 | 0.0 | 0.32 | 0.0 | 0.71 | 89.98 | 9.75 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer20 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.06 | 89.63 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer20 | attention | 6 | 0.77 | 5.9 | 4.34 | 0.0 | 2.35 | 67.45 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer21 | copy | 12 | 0.04 | 0.0 | 0.97 | 0.0 | 1.58 | 90.71 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer21 | elementwise_unary | 12 | 0.02 | 0.0 | 0.51 | 0.0 | 0.88 | 93.38 | 7.63 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer21 | reduce | 6 | 0.09 | 0.0 | 1.94 | 0.0 | 3.77 | 91.95 | 31.91 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer21 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.38 | 90.58 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer21 | gemv | 21 | 15.43 | 0.0 | 74.52 | 0.0 | 44.93 | 9.26 | 16.02 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer21 | concat | 18 | 1.61 | 0.0 | 0.31 | 0.0 | 0.7 | 88.96 | 9.96 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer21 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.09 | 90.71 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer21 | attention | 6 | 0.75 | 12.49 | 4.34 | 0.0 | 2.31 | 68.4 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer22 | copy | 12 | 0.01 | 0.0 | 0.93 | 0.0 | 1.87 | 90.72 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer22 | elementwise_unary | 12 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 93.66 | 7.49 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer22 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.8 | 90.89 | 31.85 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer22 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.4 | 93.84 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer22 | gemv | 21 | 14.99 | 0.0 | 72.51 | 0.0 | 44.48 | 9.04 | 15.92 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer22 | concat | 18 | 1.65 | 0.0 | 0.31 | 0.0 | 0.7 | 89.73 | 9.91 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer22 | elementwise_other | 21 | 0.02 | 0.0 | 0.82 | 0.0 | 1.07 | 89.81 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer22 | attention | 6 | 0.77 | 12.42 | 2.53 | 0.0 | 1.49 | 65.68 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer23 | copy | 12 | 0.04 | 0.0 | 0.91 | 0.0 | 1.56 | 89.04 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer23 | elementwise_unary | 12 | 0.02 | 0.0 | 0.73 | 0.0 | 0.92 | 88.91 | 7.73 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer23 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.79 | 90.69 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer23 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.38 | 93.74 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer23 | gemv | 21 | 15.15 | 0.0 | 73.61 | 0.0 | 45.37 | 9.09 | 15.96 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer23 | concat | 18 | 1.57 | 0.0 | 0.31 | 0.0 | 0.69 | 89.86 | 10.08 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer23 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.09 | 86.92 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer23 | attention | 6 | 0.76 | 12.52 | 4.33 | 0.0 | 2.32 | 66.52 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer24 | copy | 12 | 0.04 | 0.0 | 0.93 | 0.0 | 1.58 | 93.81 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer24 | elementwise_unary | 12 | 0.02 | 0.0 | 0.52 | 0.0 | 0.89 | 91.86 | 7.71 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer24 | reduce | 6 | 0.09 | 0.0 | 1.95 | 0.0 | 3.78 | 91.7 | 31.92 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer24 | elementwise_binary | 33 | 0.02 | 0.0 | 0.83 | 0.0 | 1.4 | 94.19 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer24 | gemv | 21 | 15.22 | 0.0 | 73.7 | 0.0 | 44.38 | 9.21 | 16.08 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer24 | concat | 18 | 1.58 | 0.0 | 0.31 | 0.0 | 0.7 | 92.91 | 9.82 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer24 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.06 | 91.98 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer24 | attention | 6 | 0.77 | 12.55 | 4.31 | 0.0 | 2.31 | 70.7 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer25 | copy | 12 | 0.04 | 0.0 | 0.93 | 0.0 | 1.69 | 90.64 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer25 | elementwise_unary | 12 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 92.16 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer25 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.77 | 91.16 | 31.91 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer25 | elementwise_binary | 33 | 0.02 | 0.0 | 0.83 | 0.0 | 1.4 | 91.61 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer25 | gemv | 21 | 15.28 | 0.0 | 73.97 | 0.0 | 43.52 | 9.15 | 16.0 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer25 | concat | 18 | 1.66 | 0.0 | 0.31 | 0.0 | 0.74 | 94.2 | 9.72 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer25 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.08 | 89.39 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer25 | attention | 6 | 0.75 | 12.42 | 4.35 | 0.0 | 2.33 | 67.34 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer26 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.57 | 90.8 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer26 | elementwise_unary | 12 | 0.02 | 0.0 | 0.51 | 0.0 | 0.89 | 91.55 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer26 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.8 | 89.97 | 31.92 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer26 | elementwise_binary | 33 | 0.02 | 0.0 | 0.83 | 0.0 | 1.39 | 91.32 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer26 | gemv | 21 | 15.17 | 0.0 | 73.77 | 0.0 | 44.98 | 9.21 | 15.96 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer26 | concat | 18 | 1.58 | 0.0 | 0.31 | 0.0 | 0.69 | 90.72 | 9.73 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer26 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.05 | 89.8 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer26 | attention | 6 | 0.77 | 12.41 | 4.34 | 0.0 | 2.33 | 66.98 | 8.31 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer27 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.57 | 90.8 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer27 | elementwise_unary | 12 | 0.02 | 0.0 | 0.53 | 0.0 | 0.92 | 87.89 | 7.6 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer27 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.78 | 90.02 | 31.9 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer27 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.4 | 91.3 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer27 | gemv | 21 | 15.03 | 0.0 | 73.77 | 0.0 | 45.43 | 9.1 | 16.04 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer27 | concat | 18 | 1.66 | 0.0 | 0.31 | 0.0 | 0.73 | 92.64 | 9.71 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer27 | elementwise_other | 21 | 0.02 | 0.0 | 0.82 | 0.0 | 1.07 | 88.66 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer27 | attention | 6 | 0.76 | 12.51 | 4.34 | 0.0 | 2.32 | 68.22 | 8.28 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer28 | copy | 12 | 0.04 | 0.0 | 1.09 | 0.0 | 1.86 | 89.59 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer28 | elementwise_unary | 12 | 0.02 | 0.0 | 0.52 | 0.0 | 0.9 | 91.37 | 7.67 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer28 | reduce | 6 | 0.09 | 0.0 | 1.95 | 0.0 | 3.77 | 90.75 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer28 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.37 | 90.78 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer28 | gemv | 21 | 15.29 | 0.0 | 74.74 | 0.0 | 44.24 | 9.26 | 16.03 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer28 | concat | 18 | 1.58 | 0.0 | 0.32 | 0.0 | 0.7 | 90.64 | 9.82 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer28 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.07 | 88.79 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer28 | attention | 6 | 0.77 | 12.54 | 4.33 | 0.0 | 2.31 | 70.06 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer29 | copy | 12 | 0.03 | 0.0 | 0.76 | 0.0 | 1.04 | 91.23 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer29 | elementwise_unary | 12 | 0.02 | 0.0 | 0.71 | 0.0 | 0.91 | 95.73 | 7.73 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer29 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.79 | 91.56 | 31.88 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer29 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.41 | 89.69 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer29 | gemv | 21 | 15.12 | 0.0 | 73.56 | 0.0 | 45.38 | 9.05 | 16.09 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer29 | concat | 18 | 1.61 | 0.0 | 0.31 | 0.0 | 0.7 | 92.05 | 9.83 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer29 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.05 | 91.8 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer29 | attention | 6 | 0.76 | 12.38 | 4.33 | 0.0 | 2.33 | 68.58 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer30 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.61 | 90.05 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer30 | elementwise_unary | 12 | 0.02 | 0.0 | 0.53 | 0.0 | 0.89 | 90.16 | 7.65 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer30 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.78 | 90.38 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer30 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.4 | 90.69 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer30 | gemv | 21 | 15.15 | 0.0 | 73.56 | 0.0 | 44.99 | 9.16 | 16.0 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer30 | concat | 18 | 1.56 | 0.0 | 0.31 | 0.0 | 0.7 | 90.71 | 9.71 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer30 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.38 | 86.7 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer30 | attention | 6 | 0.77 | 12.56 | 4.34 | 0.0 | 2.33 | 69.12 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer31 | copy | 12 | 0.04 | 0.0 | 0.93 | 0.0 | 1.6 | 93.71 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer31 | elementwise_unary | 12 | 0.02 | 0.0 | 0.72 | 0.0 | 0.9 | 89.1 | 7.6 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer31 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.8 | 90.72 | 31.92 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer31 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.57 | 90.65 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer31 | gemv | 21 | 15.07 | 0.0 | 73.75 | 0.0 | 44.68 | 9.27 | 16.01 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer31 | concat | 18 | 1.66 | 0.0 | 0.32 | 0.0 | 1.01 | 97.41 | 9.72 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer31 | elementwise_other | 21 | 0.02 | 0.0 | 0.82 | 0.0 | 1.06 | 92.14 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer31 | attention | 6 | 0.78 | 12.48 | 4.3 | 0.0 | 2.29 | 69.12 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer32 | copy | 12 | 0.04 | 0.0 | 0.94 | 0.0 | 1.61 | 93.09 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer32 | elementwise_unary | 12 | 0.02 | 0.0 | 0.52 | 0.0 | 0.91 | 88.89 | 7.7 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer32 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.8 | 89.82 | 31.84 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer32 | elementwise_binary | 33 | 0.02 | 0.0 | 0.83 | 0.0 | 1.4 | 92.27 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer32 | gemv | 21 | 15.03 | 0.0 | 72.78 | 0.0 | 44.78 | 9.05 | 16.01 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer32 | concat | 18 | 1.67 | 0.0 | 0.31 | 0.0 | 0.7 | 95.97 | 9.71 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer32 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.25 | 92.19 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer32 | attention | 6 | 0.77 | 12.42 | 4.3 | 0.0 | 2.31 | 68.78 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer33 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.58 | 88.84 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer33 | elementwise_unary | 12 | 0.02 | 0.0 | 0.52 | 0.0 | 0.92 | 88.12 | 7.72 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer33 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.79 | 90.01 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer33 | elementwise_binary | 33 | 0.02 | 0.0 | 0.83 | 0.0 | 1.49 | 90.34 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer33 | gemv | 21 | 15.38 | 0.0 | 73.77 | 0.0 | 45.29 | 9.2 | 16.13 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer33 | concat | 18 | 1.6 | 0.0 | 0.32 | 0.0 | 0.7 | 95.88 | 9.64 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer33 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.11 | 89.71 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer33 | attention | 6 | 0.76 | 12.52 | 4.35 | 0.0 | 3.53 | 68.62 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer34 | copy | 12 | 0.04 | 0.0 | 0.92 | 0.0 | 1.97 | 91.22 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer34 | elementwise_unary | 12 | 0.02 | 0.0 | 0.53 | 0.0 | 0.88 | 88.31 | 7.64 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer34 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.8 | 91.02 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer34 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.45 | 90.25 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer34 | gemv | 21 | 15.17 | 0.0 | 73.98 | 0.0 | 45.31 | 9.27 | 15.99 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer34 | concat | 18 | 1.59 | 0.0 | 0.31 | 0.0 | 0.72 | 92.82 | 9.88 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer34 | elementwise_other | 21 | 0.02 | 0.0 | 0.82 | 0.0 | 1.06 | 90.17 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer34 | attention | 6 | 0.76 | 12.33 | 4.31 | 0.0 | 2.3 | 69.85 | 8.31 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer35 | copy | 12 | 0.04 | 0.0 | 0.93 | 0.0 | 1.59 | 89.22 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer35 | elementwise_unary | 12 | 0.02 | 0.0 | 0.53 | 0.0 | 0.89 | 89.62 | 7.73 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer35 | reduce | 6 | 0.09 | 0.0 | 1.96 | 0.0 | 3.81 | 90.97 | 31.83 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer35 | elementwise_binary | 33 | 0.02 | 0.0 | 0.82 | 0.0 | 1.39 | 90.62 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer35 | gemv | 21 | 15.29 | 0.0 | 73.39 | 0.0 | 45.4 | 9.26 | 15.97 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_layer35 | concat | 18 | 1.59 | 0.0 | 0.31 | 0.0 | 0.72 | 90.23 | 9.76 | 0.17 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer35 | elementwise_other | 21 | 0.02 | 0.0 | 0.81 | 0.0 | 1.05 | 91.39 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_layer35 | attention | 6 | 0.78 | 12.55 | 5.71 | 0.0 | 2.61 | 59.16 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.08 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_head | copy | 6 | 0.04 | 0.0 | 0.92 | 0.0 | 1.57 | 89.04 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_head | elementwise_unary | 6 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 91.32 | 7.71 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_head | reduce | 3 | 0.09 | 0.0 | 1.95 | 0.0 | 3.78 | 91.16 | 31.85 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_head | elementwise_binary | 9 | 0.02 | 0.0 | 0.81 | 0.0 | 1.05 | 88.29 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 1024 | mir_operator:decode_head | gemv | 3 | 19.92 | 0.0 | 96.75 | 0.0 | 61.25 | 0.55 | 24.48 | 49.46 |  |  | DRAM-bandwidth-bound |
| planner_debate | 1024 | mir_operator:decode_sample | reduce | 3 | 2.8 | 0.0 | 5.26 | 0.0 | 2.99 | 66.31 | 33.12 | 0.05 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_embed | other | 2 | 4.38 | 0.0 | 10.81 | 0.0 | 25.06 | 89.74 | 35.13 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer00 | copy | 8 | 9.8 | 0.0 | 45.43 | 0.0 | 27.1 | 52.44 | 49.23 | 0.67 |  |  | underutilised: SM 18 %, DRAM 32 %, L2 30 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer00 | elementwise_unary | 8 | 0.83 | 0.0 | 26.33 | 0.0 | 12.34 | 69.84 | 17.98 | 0.21 |  |  | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer00 | reduce | 8 | 6.11 | 0.0 | 32.74 | 0.0 | 12.89 | 26.78 | 36.15 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer00 | elementwise_binary | 22 | 14.06 | 0.0 | 36.65 | 0.0 | 22.31 | 60.09 | 66.81 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer00 | gemm | 14 | 33.0 | 36.88 | 37.93 | 0.0 | 67.81 | 89.69 | 15.22 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer00 | concat | 12 | 14.52 | 0.0 | 4.93 | 0.0 | 3.69 | 65.15 | 66.06 | 1.33 |  |  | underutilised: SM 15 %, DRAM 3 %, L2 4 %, occ 52 % |
| planner_debate | 896 | mir_operator:prefill_layer00 | elementwise_other | 14 | 3.71 | 0.0 | 54.68 | 0.0 | 21.59 | 50.82 | 33.06 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer00 | attention | 4 | 18.49 | 8.97 | 37.6 | 0.0 | 25.86 | 57.42 | 32.97 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer01 | copy | 8 | 10.18 | 0.0 | 44.82 | 0.0 | 26.72 | 52.58 | 49.6 | 0.67 |  |  | underutilised: SM 19 %, DRAM 34 %, L2 32 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer01 | elementwise_unary | 8 | 0.85 | 0.0 | 28.13 | 0.0 | 13.23 | 70.95 | 17.96 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer01 | reduce | 8 | 6.18 | 0.0 | 32.82 | 0.0 | 12.89 | 26.7 | 36.74 | 0.24 |  |  | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer01 | elementwise_binary | 22 | 13.44 | 0.0 | 36.96 | 0.0 | 21.88 | 59.35 | 67.25 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer01 | gemm | 14 | 30.7 | 36.96 | 37.08 | 0.0 | 68.49 | 89.62 | 15.25 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer01 | concat | 12 | 14.29 | 0.0 | 4.93 | 0.0 | 3.67 | 65.18 | 66.7 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer01 | elementwise_other | 14 | 3.7 | 0.0 | 54.26 | 0.0 | 21.44 | 50.77 | 32.9 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer01 | attention | 4 | 17.59 | 8.91 | 37.61 | 0.0 | 25.68 | 57.41 | 33.18 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer02 | copy | 8 | 9.87 | 0.0 | 45.72 | 0.0 | 27.55 | 52.56 | 49.31 | 0.67 |  |  | underutilised: SM 19 %, DRAM 33 %, L2 31 %, occ 66 % |
| planner_debate | 896 | mir_operator:prefill_layer02 | elementwise_unary | 8 | 0.85 | 0.0 | 28.08 | 0.0 | 13.2 | 70.05 | 18.04 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer02 | reduce | 8 | 6.25 | 0.0 | 32.01 | 0.0 | 12.61 | 26.79 | 35.89 | 0.24 |  |  | underutilised: SM 1 %, DRAM 34 %, L2 13 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer02 | elementwise_binary | 22 | 14.1 | 0.0 | 36.53 | 0.0 | 22.49 | 60.15 | 67.85 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer02 | gemm | 14 | 33.09 | 36.82 | 36.69 | 0.0 | 68.47 | 89.64 | 15.18 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer02 | concat | 12 | 14.65 | 0.0 | 4.92 | 0.0 | 3.86 | 64.43 | 67.08 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer02 | elementwise_other | 14 | 3.66 | 0.0 | 53.46 | 0.0 | 21.07 | 50.77 | 32.93 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer02 | attention | 4 | 14.14 | 8.82 | 37.36 | 0.0 | 25.56 | 57.42 | 33.09 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 25 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer03 | copy | 8 | 9.8 | 0.0 | 45.15 | 0.0 | 26.43 | 52.45 | 49.53 | 0.67 |  |  | underutilised: SM 18 %, DRAM 30 %, L2 29 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer03 | elementwise_unary | 8 | 0.83 | 0.0 | 28.13 | 0.0 | 13.26 | 70.77 | 18.0 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer03 | reduce | 8 | 6.17 | 0.0 | 32.62 | 0.0 | 12.84 | 26.7 | 36.12 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer03 | elementwise_binary | 22 | 13.87 | 0.0 | 35.65 | 0.0 | 22.25 | 59.24 | 66.65 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer03 | gemm | 14 | 33.11 | 37.07 | 36.29 | 0.0 | 67.19 | 89.59 | 15.24 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer03 | concat | 12 | 14.54 | 0.0 | 4.92 | 0.0 | 3.82 | 63.72 | 67.34 | 1.33 |  |  | underutilised: SM 15 %, DRAM 3 %, L2 3 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer03 | elementwise_other | 14 | 3.73 | 0.0 | 55.51 | 0.0 | 21.89 | 50.82 | 32.93 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer03 | attention | 4 | 18.56 | 8.8 | 37.66 | 0.0 | 25.42 | 57.42 | 32.97 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 25 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer04 | copy | 8 | 10.5 | 0.0 | 46.31 | 0.0 | 27.26 | 52.37 | 49.54 | 0.67 |  |  | underutilised: SM 19 %, DRAM 32 %, L2 31 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer04 | elementwise_unary | 8 | 0.84 | 0.0 | 28.47 | 0.0 | 13.38 | 70.65 | 18.01 | 0.21 |  |  | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer04 | reduce | 8 | 5.99 | 0.0 | 32.62 | 0.0 | 12.84 | 26.78 | 36.33 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer04 | elementwise_binary | 22 | 13.51 | 0.0 | 36.61 | 0.0 | 22.56 | 59.26 | 66.86 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer04 | gemm | 14 | 30.88 | 36.8 | 36.57 | 0.0 | 67.79 | 89.57 | 15.24 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer04 | concat | 12 | 14.54 | 0.0 | 4.91 | 0.0 | 3.84 | 63.75 | 67.17 | 1.33 |  |  | underutilised: SM 15 %, DRAM 3 %, L2 4 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer04 | elementwise_other | 14 | 3.8 | 0.0 | 53.97 | 0.0 | 21.26 | 50.83 | 32.99 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer04 | attention | 4 | 18.27 | 8.89 | 37.81 | 0.0 | 25.78 | 57.43 | 33.09 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer05 | copy | 8 | 10.0 | 0.0 | 45.24 | 0.0 | 27.2 | 52.46 | 49.53 | 0.67 |  |  | underutilised: SM 18 %, DRAM 32 %, L2 31 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer05 | elementwise_unary | 8 | 0.83 | 0.0 | 28.13 | 0.0 | 13.25 | 70.29 | 17.88 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer05 | reduce | 8 | 6.16 | 0.0 | 32.52 | 0.0 | 12.82 | 26.68 | 35.91 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer05 | elementwise_binary | 22 | 13.52 | 0.0 | 36.33 | 0.0 | 22.74 | 59.73 | 66.91 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer05 | gemm | 14 | 33.25 | 36.76 | 37.0 | 0.0 | 69.41 | 89.59 | 15.21 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer05 | concat | 12 | 15.01 | 0.0 | 4.91 | 0.0 | 3.75 | 65.65 | 67.29 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 4 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer05 | elementwise_other | 14 | 3.68 | 0.0 | 54.38 | 0.0 | 21.49 | 50.82 | 33.12 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer05 | attention | 4 | 18.37 | 9.0 | 37.78 | 0.0 | 25.57 | 57.43 | 32.97 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer06 | copy | 8 | 9.92 | 0.0 | 45.35 | 0.0 | 26.66 | 52.52 | 48.83 | 0.67 |  |  | underutilised: SM 18 %, DRAM 33 %, L2 31 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer06 | elementwise_unary | 8 | 0.84 | 0.0 | 28.33 | 0.0 | 13.37 | 70.65 | 17.91 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer06 | reduce | 8 | 6.38 | 0.0 | 31.93 | 0.0 | 12.57 | 26.78 | 36.1 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer06 | elementwise_binary | 22 | 13.95 | 0.0 | 36.0 | 0.0 | 21.74 | 59.15 | 67.56 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer06 | gemm | 14 | 33.15 | 36.91 | 37.29 | 0.0 | 68.29 | 89.31 | 15.26 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer06 | concat | 12 | 14.86 | 0.0 | 4.89 | 0.0 | 3.87 | 65.54 | 67.41 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer06 | elementwise_other | 14 | 3.75 | 0.0 | 53.04 | 0.0 | 20.94 | 50.81 | 32.88 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer06 | attention | 4 | 18.46 | 8.81 | 37.39 | 0.0 | 25.42 | 57.41 | 33.36 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer07 | copy | 8 | 10.13 | 0.0 | 33.4 | 0.0 | 26.75 | 52.44 | 49.76 | 0.67 |  |  | underutilised: SM 18 %, DRAM 30 %, L2 29 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer07 | elementwise_unary | 8 | 0.84 | 0.0 | 28.32 | 0.0 | 13.53 | 70.0 | 18.11 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer07 | reduce | 8 | 6.0 | 0.0 | 32.85 | 0.0 | 12.9 | 26.79 | 36.04 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer07 | elementwise_binary | 22 | 13.98 | 0.0 | 36.48 | 0.0 | 22.51 | 59.27 | 67.15 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer07 | gemm | 14 | 30.82 | 36.76 | 36.98 | 0.0 | 68.35 | 89.61 | 15.23 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer07 | concat | 12 | 14.5 | 0.0 | 4.87 | 0.0 | 3.82 | 65.12 | 66.88 | 1.33 |  |  | underutilised: SM 15 %, DRAM 3 %, L2 4 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer07 | elementwise_other | 14 | 3.71 | 0.0 | 53.73 | 0.0 | 21.25 | 50.79 | 32.87 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer07 | attention | 4 | 18.57 | 8.91 | 37.8 | 0.0 | 25.65 | 57.43 | 33.01 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer08 | copy | 8 | 9.99 | 0.0 | 45.23 | 0.0 | 26.73 | 52.59 | 49.23 | 0.67 |  |  | underutilised: SM 19 %, DRAM 33 %, L2 32 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer08 | elementwise_unary | 8 | 0.85 | 0.0 | 27.7 | 0.0 | 13.08 | 70.03 | 17.89 | 0.21 |  |  | underutilised: SM 2 %, DRAM 55 %, L2 25 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer08 | reduce | 8 | 6.18 | 0.0 | 32.52 | 0.0 | 12.78 | 26.51 | 35.88 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer08 | elementwise_binary | 22 | 13.65 | 0.0 | 37.16 | 0.0 | 22.62 | 59.37 | 67.01 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer08 | gemm | 14 | 30.87 | 36.75 | 36.89 | 0.0 | 68.1 | 89.54 | 15.27 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer08 | concat | 12 | 14.47 | 0.0 | 4.91 | 0.0 | 3.81 | 63.96 | 66.83 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer08 | elementwise_other | 14 | 3.75 | 0.0 | 54.58 | 0.0 | 21.58 | 50.83 | 32.75 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer08 | attention | 4 | 18.34 | 8.88 | 36.97 | 0.0 | 25.38 | 57.23 | 33.02 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 25 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer09 | copy | 8 | 9.7 | 0.0 | 46.94 | 0.0 | 26.3 | 51.58 | 48.61 | 0.67 |  |  | underutilised: SM 18 %, DRAM 33 %, L2 32 %, occ 65 % |
| planner_debate | 896 | mir_operator:prefill_layer09 | elementwise_unary | 8 | 0.85 | 0.0 | 27.7 | 0.0 | 13.25 | 70.66 | 17.97 | 0.21 |  |  | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer09 | reduce | 8 | 6.14 | 0.0 | 32.55 | 0.0 | 12.86 | 26.79 | 36.67 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer09 | elementwise_binary | 22 | 14.0 | 0.0 | 36.24 | 0.0 | 22.4 | 59.36 | 67.95 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer09 | gemm | 14 | 31.11 | 37.02 | 37.51 | 0.0 | 67.51 | 89.59 | 15.24 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer09 | concat | 12 | 15.06 | 0.0 | 4.93 | 0.0 | 3.72 | 63.92 | 67.48 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer09 | elementwise_other | 14 | 3.58 | 0.0 | 54.25 | 0.0 | 21.47 | 50.78 | 33.0 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer09 | attention | 4 | 18.36 | 8.76 | 37.66 | 0.0 | 25.38 | 57.44 | 33.08 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer10 | copy | 8 | 9.9 | 0.0 | 45.88 | 0.0 | 27.69 | 52.42 | 49.03 | 0.67 |  |  | underutilised: SM 18 %, DRAM 33 %, L2 31 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer10 | elementwise_unary | 8 | 0.83 | 0.0 | 27.75 | 0.0 | 13.04 | 70.11 | 17.92 | 0.21 |  |  | underutilised: SM 2 %, DRAM 55 %, L2 25 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer10 | reduce | 8 | 5.87 | 0.0 | 32.57 | 0.0 | 12.86 | 26.81 | 36.14 | 0.24 |  |  | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer10 | elementwise_binary | 22 | 13.88 | 0.0 | 36.59 | 0.0 | 22.54 | 59.81 | 66.97 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer10 | gemm | 14 | 30.92 | 36.9 | 37.67 | 0.0 | 66.73 | 89.62 | 15.21 | 2.5 |  |  | underutilised: SM 30 %, DRAM 18 %, L2 34 %, occ 15 % |
| planner_debate | 896 | mir_operator:prefill_layer10 | concat | 12 | 14.38 | 0.0 | 4.92 | 0.0 | 3.91 | 65.59 | 67.19 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer10 | elementwise_other | 14 | 3.79 | 0.0 | 54.54 | 0.0 | 21.54 | 50.79 | 33.03 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer10 | attention | 4 | 18.16 | 8.93 | 38.44 | 0.0 | 25.76 | 57.26 | 32.91 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer11 | copy | 8 | 9.71 | 0.0 | 46.1 | 0.0 | 27.09 | 52.43 | 49.9 | 0.67 |  |  | underutilised: SM 18 %, DRAM 33 %, L2 31 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer11 | elementwise_unary | 8 | 0.83 | 0.0 | 27.89 | 0.0 | 13.14 | 65.16 | 17.87 | 0.21 |  |  | underutilised: SM 2 %, DRAM 55 %, L2 25 %, occ 27 % |
| planner_debate | 896 | mir_operator:prefill_layer11 | reduce | 8 | 6.15 | 0.0 | 32.71 | 0.0 | 12.86 | 26.8 | 35.67 | 0.24 |  |  | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer11 | elementwise_binary | 22 | 13.91 | 0.0 | 36.96 | 0.0 | 22.77 | 59.19 | 67.36 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer11 | gemm | 14 | 30.97 | 36.93 | 37.21 | 0.0 | 67.49 | 89.64 | 15.28 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer11 | concat | 12 | 14.73 | 0.0 | 5.3 | 0.0 | 3.72 | 63.06 | 67.55 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer11 | elementwise_other | 14 | 3.78 | 0.0 | 54.27 | 0.0 | 21.41 | 50.77 | 32.95 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer11 | attention | 4 | 18.56 | 8.94 | 38.05 | 0.0 | 25.44 | 57.41 | 33.39 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 25 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer12 | copy | 8 | 9.65 | 0.0 | 45.48 | 0.0 | 26.3 | 52.47 | 48.78 | 0.67 |  |  | underutilised: SM 19 %, DRAM 30 %, L2 29 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer12 | elementwise_unary | 8 | 0.83 | 0.0 | 28.13 | 0.0 | 13.25 | 69.69 | 17.89 | 0.21 |  |  | underutilised: SM 2 %, DRAM 58 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer12 | reduce | 8 | 6.35 | 0.0 | 32.43 | 0.0 | 12.75 | 26.78 | 36.65 | 0.24 |  |  | underutilised: SM 1 %, DRAM 34 %, L2 13 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer12 | elementwise_binary | 22 | 13.99 | 0.0 | 36.49 | 0.0 | 21.61 | 59.12 | 67.61 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer12 | gemm | 14 | 30.81 | 37.04 | 37.0 | 0.0 | 68.09 | 89.57 | 15.25 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer12 | concat | 12 | 14.59 | 0.0 | 4.95 | 0.0 | 3.81 | 65.43 | 66.73 | 1.33 |  |  | underutilised: SM 15 %, DRAM 3 %, L2 3 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer12 | elementwise_other | 14 | 3.74 | 0.0 | 55.6 | 0.0 | 21.95 | 50.82 | 32.7 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer12 | attention | 4 | 18.5 | 8.81 | 38.26 | 0.0 | 25.69 | 57.43 | 33.02 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer13 | copy | 8 | 9.72 | 0.0 | 45.16 | 0.0 | 27.21 | 52.52 | 49.01 | 0.67 |  |  | underutilised: SM 19 %, DRAM 32 %, L2 31 %, occ 66 % |
| planner_debate | 896 | mir_operator:prefill_layer13 | elementwise_unary | 8 | 0.83 | 0.0 | 27.75 | 0.0 | 13.06 | 70.34 | 17.93 | 0.21 |  |  | underutilised: SM 2 %, DRAM 55 %, L2 25 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer13 | reduce | 8 | 6.22 | 0.0 | 30.6 | 0.0 | 12.06 | 26.71 | 36.24 | 0.24 |  |  | underutilised: SM 1 %, DRAM 34 %, L2 13 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer13 | elementwise_binary | 22 | 13.39 | 0.0 | 36.01 | 0.0 | 22.06 | 59.21 | 67.77 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer13 | gemm | 14 | 33.44 | 35.13 | 36.44 | 0.0 | 69.24 | 89.55 | 15.23 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer13 | concat | 12 | 15.01 | 0.0 | 5.38 | 0.0 | 3.7 | 64.16 | 67.04 | 1.33 |  |  | underutilised: SM 17 %, DRAM 6 %, L2 3 %, occ 69 % |
| planner_debate | 896 | mir_operator:prefill_layer13 | elementwise_other | 14 | 3.74 | 0.0 | 54.19 | 0.0 | 21.38 | 50.82 | 32.94 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer13 | attention | 4 | 18.41 | 8.87 | 37.71 | 0.0 | 25.59 | 57.43 | 33.57 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer14 | copy | 8 | 9.9 | 0.0 | 45.48 | 0.0 | 28.36 | 52.56 | 49.31 | 0.67 |  |  | underutilised: SM 18 %, DRAM 34 %, L2 32 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer14 | elementwise_unary | 8 | 0.83 | 0.0 | 28.37 | 0.0 | 13.37 | 70.93 | 17.9 | 0.21 |  |  | underutilised: SM 2 %, DRAM 58 %, L2 27 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer14 | reduce | 8 | 6.33 | 0.0 | 32.41 | 0.0 | 12.75 | 26.8 | 36.13 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer14 | elementwise_binary | 22 | 13.32 | 0.0 | 36.19 | 0.0 | 21.83 | 59.27 | 67.06 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer14 | gemm | 14 | 33.13 | 36.86 | 36.57 | 0.0 | 67.76 | 89.56 | 15.19 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer14 | concat | 12 | 14.51 | 0.0 | 5.26 | 0.0 | 3.68 | 63.16 | 66.73 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer14 | elementwise_other | 14 | 3.83 | 0.0 | 53.58 | 0.0 | 21.19 | 50.82 | 33.06 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer14 | attention | 4 | 18.49 | 8.85 | 38.32 | 0.0 | 25.86 | 57.42 | 33.34 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer15 | copy | 8 | 9.97 | 0.0 | 44.87 | 0.0 | 26.63 | 52.46 | 49.63 | 0.67 |  |  | underutilised: SM 19 %, DRAM 31 %, L2 30 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer15 | elementwise_unary | 8 | 0.84 | 0.0 | 28.28 | 0.0 | 12.89 | 71.38 | 18.02 | 0.21 |  |  | underutilised: SM 2 %, DRAM 57 %, L2 25 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer15 | reduce | 8 | 6.21 | 0.0 | 32.0 | 0.0 | 12.59 | 26.79 | 36.46 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer15 | elementwise_binary | 22 | 13.41 | 0.0 | 36.21 | 0.0 | 22.41 | 59.37 | 67.51 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer15 | gemm | 14 | 30.9 | 36.8 | 37.12 | 0.0 | 69.55 | 89.63 | 15.23 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer15 | concat | 12 | 14.54 | 0.0 | 4.92 | 0.0 | 3.74 | 62.29 | 67.23 | 1.33 |  |  | underutilised: SM 15 %, DRAM 3 %, L2 4 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer15 | elementwise_other | 14 | 3.7 | 0.0 | 53.91 | 0.0 | 21.37 | 50.77 | 33.05 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer15 | attention | 4 | 18.43 | 8.89 | 38.31 | 0.0 | 25.2 | 57.43 | 32.83 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer16 | copy | 8 | 10.22 | 0.0 | 44.5 | 0.0 | 27.76 | 52.55 | 48.86 | 0.67 |  |  | underutilised: SM 19 %, DRAM 33 %, L2 32 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer16 | elementwise_unary | 8 | 0.84 | 0.0 | 28.18 | 0.0 | 13.29 | 67.32 | 17.9 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 27 % |
| planner_debate | 896 | mir_operator:prefill_layer16 | reduce | 8 | 6.11 | 0.0 | 34.09 | 0.0 | 12.88 | 25.33 | 36.52 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer16 | elementwise_binary | 22 | 14.15 | 0.0 | 36.26 | 0.0 | 21.92 | 59.32 | 66.57 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer16 | gemm | 14 | 33.06 | 36.96 | 36.41 | 0.0 | 68.48 | 89.58 | 15.23 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer16 | concat | 12 | 14.45 | 0.0 | 4.92 | 0.0 | 3.77 | 65.47 | 66.82 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 4 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer16 | elementwise_other | 14 | 3.76 | 0.0 | 53.1 | 0.0 | 20.97 | 50.63 | 33.15 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer16 | attention | 4 | 18.54 | 8.77 | 37.52 | 0.0 | 25.57 | 57.43 | 33.06 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer17 | copy | 8 | 9.34 | 0.0 | 45.59 | 0.0 | 26.32 | 52.43 | 48.93 | 0.67 |  |  | latency/launch-bound: 0.83 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer17 | elementwise_unary | 8 | 0.84 | 0.0 | 28.48 | 0.0 | 13.66 | 69.82 | 17.86 | 0.21 |  |  | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer17 | reduce | 8 | 6.36 | 0.0 | 32.21 | 0.0 | 12.71 | 26.8 | 36.42 | 0.24 |  |  | underutilised: SM 1 %, DRAM 38 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer17 | elementwise_binary | 22 | 13.79 | 0.0 | 36.11 | 0.0 | 22.45 | 59.18 | 67.35 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer17 | gemm | 14 | 33.26 | 36.96 | 37.98 | 0.0 | 68.93 | 89.63 | 15.25 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer17 | concat | 12 | 14.51 | 0.0 | 4.92 | 0.0 | 3.75 | 65.18 | 67.01 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer17 | elementwise_other | 14 | 3.74 | 0.0 | 55.08 | 0.0 | 21.76 | 49.07 | 32.76 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer17 | attention | 4 | 14.97 | 8.96 | 37.66 | 0.0 | 25.75 | 57.35 | 33.19 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer18 | copy | 8 | 9.8 | 0.0 | 45.21 | 0.0 | 27.12 | 52.56 | 49.41 | 0.67 |  |  | underutilised: SM 18 %, DRAM 33 %, L2 32 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer18 | elementwise_unary | 8 | 0.84 | 0.0 | 28.08 | 0.0 | 13.24 | 71.41 | 18.08 | 0.21 |  |  | underutilised: SM 2 %, DRAM 58 %, L2 27 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer18 | reduce | 8 | 6.3 | 0.0 | 32.74 | 0.0 | 12.91 | 26.84 | 36.52 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer18 | elementwise_binary | 22 | 13.99 | 0.0 | 36.42 | 0.0 | 22.29 | 59.98 | 67.03 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer18 | gemm | 14 | 33.26 | 36.85 | 37.72 | 0.0 | 68.41 | 89.6 | 15.19 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer18 | concat | 12 | 14.79 | 0.0 | 4.9 | 0.0 | 3.66 | 65.39 | 66.58 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 4 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer18 | elementwise_other | 14 | 3.71 | 0.0 | 54.54 | 0.0 | 21.53 | 50.78 | 33.24 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer18 | attention | 4 | 18.57 | 8.91 | 37.23 | 0.0 | 25.75 | 57.41 | 33.04 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer19 | copy | 8 | 9.81 | 0.0 | 45.28 | 0.0 | 27.12 | 52.56 | 49.22 | 0.67 |  |  | underutilised: SM 18 %, DRAM 31 %, L2 30 %, occ 66 % |
| planner_debate | 896 | mir_operator:prefill_layer19 | elementwise_unary | 8 | 0.85 | 0.0 | 28.13 | 0.0 | 13.25 | 70.26 | 18.03 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer19 | reduce | 8 | 6.06 | 0.0 | 32.61 | 0.0 | 12.7 | 26.71 | 36.13 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer19 | elementwise_binary | 22 | 13.61 | 0.0 | 36.8 | 0.0 | 22.8 | 59.37 | 66.9 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer19 | gemm | 14 | 30.78 | 36.85 | 37.36 | 0.0 | 69.01 | 89.61 | 15.22 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer19 | concat | 12 | 13.92 | 0.0 | 4.86 | 0.0 | 3.7 | 65.05 | 66.85 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 4 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer19 | elementwise_other | 14 | 3.56 | 0.0 | 54.64 | 0.0 | 21.5 | 50.84 | 32.97 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer19 | attention | 4 | 18.33 | 8.95 | 37.79 | 0.0 | 25.77 | 57.43 | 32.93 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer20 | copy | 8 | 9.62 | 0.0 | 46.16 | 0.0 | 27.96 | 52.52 | 49.39 | 0.67 |  |  | underutilised: SM 19 %, DRAM 34 %, L2 32 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer20 | elementwise_unary | 8 | 0.84 | 0.0 | 28.28 | 0.0 | 13.28 | 65.23 | 18.1 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer20 | reduce | 8 | 6.17 | 0.0 | 32.22 | 0.0 | 12.69 | 26.28 | 36.53 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer20 | elementwise_binary | 22 | 13.89 | 0.0 | 36.29 | 0.0 | 22.41 | 59.51 | 67.23 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer20 | gemm | 14 | 30.95 | 36.93 | 36.41 | 0.0 | 68.19 | 89.59 | 15.19 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer20 | concat | 12 | 14.57 | 0.0 | 4.95 | 0.0 | 3.77 | 64.34 | 67.07 | 1.33 |  |  | underutilised: SM 15 %, DRAM 3 %, L2 3 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer20 | elementwise_other | 14 | 3.67 | 0.0 | 54.96 | 0.0 | 21.69 | 50.77 | 30.84 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer20 | attention | 4 | 18.31 | 8.9 | 37.89 | 0.0 | 25.58 | 57.25 | 33.36 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 25 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer21 | copy | 8 | 9.77 | 0.0 | 44.47 | 0.0 | 27.21 | 52.45 | 49.74 | 0.67 |  |  | underutilised: SM 18 %, DRAM 33 %, L2 31 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer21 | elementwise_unary | 8 | 0.85 | 0.0 | 28.62 | 0.0 | 13.51 | 70.91 | 17.93 | 0.21 |  |  | underutilised: SM 2 %, DRAM 58 %, L2 27 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer21 | reduce | 8 | 6.32 | 0.0 | 32.88 | 0.0 | 12.96 | 26.8 | 35.97 | 0.24 |  |  | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer21 | elementwise_binary | 22 | 13.5 | 0.0 | 36.8 | 0.0 | 22.75 | 60.06 | 67.52 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer21 | gemm | 14 | 31.03 | 36.9 | 37.06 | 0.0 | 68.39 | 89.6 | 15.21 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer21 | concat | 12 | 14.91 | 0.0 | 4.95 | 0.0 | 3.77 | 65.21 | 67.23 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer21 | elementwise_other | 14 | 3.73 | 0.0 | 54.19 | 0.0 | 21.99 | 50.78 | 32.92 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer21 | attention | 4 | 18.38 | 9.05 | 37.74 | 0.0 | 25.76 | 57.19 | 33.15 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer22 | copy | 8 | 9.58 | 0.0 | 44.64 | 0.0 | 27.65 | 52.42 | 48.7 | 0.67 |  |  | underutilised: SM 18 %, DRAM 33 %, L2 32 %, occ 65 % |
| planner_debate | 896 | mir_operator:prefill_layer22 | elementwise_unary | 8 | 0.84 | 0.0 | 28.13 | 0.0 | 16.99 | 71.45 | 17.83 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 27 % |
| planner_debate | 896 | mir_operator:prefill_layer22 | reduce | 8 | 6.21 | 0.0 | 30.71 | 0.0 | 12.06 | 26.75 | 36.3 | 0.24 |  |  | underutilised: SM 1 %, DRAM 34 %, L2 13 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer22 | elementwise_binary | 22 | 14.16 | 0.0 | 36.13 | 0.0 | 22.01 | 59.3 | 67.36 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer22 | gemm | 14 | 32.9 | 36.78 | 36.99 | 0.0 | 69.16 | 89.58 | 15.28 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer22 | concat | 12 | 14.92 | 0.0 | 4.88 | 0.0 | 3.76 | 65.39 | 66.98 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer22 | elementwise_other | 14 | 3.69 | 0.0 | 55.05 | 0.0 | 21.79 | 50.74 | 33.0 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer22 | attention | 4 | 18.15 | 8.93 | 38.0 | 0.0 | 25.74 | 57.22 | 33.29 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer23 | copy | 8 | 9.63 | 0.0 | 33.87 | 0.0 | 26.3 | 52.45 | 49.08 | 0.67 |  |  | underutilised: SM 17 %, DRAM 31 %, L2 29 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer23 | elementwise_unary | 8 | 0.83 | 0.0 | 28.04 | 0.0 | 13.25 | 65.23 | 17.94 | 0.21 |  |  | underutilised: SM 2 %, DRAM 59 %, L2 27 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer23 | reduce | 8 | 6.16 | 0.0 | 32.61 | 0.0 | 12.85 | 26.41 | 36.16 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer23 | elementwise_binary | 22 | 13.95 | 0.0 | 36.17 | 0.0 | 22.16 | 59.43 | 67.26 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer23 | gemm | 14 | 33.11 | 37.11 | 36.8 | 0.0 | 69.29 | 89.57 | 15.27 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer23 | concat | 12 | 14.67 | 0.0 | 4.93 | 0.0 | 3.74 | 62.91 | 66.96 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer23 | elementwise_other | 14 | 3.6 | 0.0 | 55.04 | 0.0 | 21.67 | 50.82 | 32.94 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer23 | attention | 4 | 18.38 | 8.94 | 38.19 | 0.0 | 25.61 | 57.37 | 33.17 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer24 | copy | 8 | 9.88 | 0.0 | 45.04 | 0.0 | 27.39 | 52.56 | 49.94 | 0.67 |  |  | underutilised: SM 18 %, DRAM 34 %, L2 32 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer24 | elementwise_unary | 8 | 0.85 | 0.0 | 28.13 | 0.0 | 13.48 | 70.13 | 17.88 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer24 | reduce | 8 | 6.12 | 0.0 | 32.62 | 0.0 | 12.83 | 26.35 | 36.1 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer24 | elementwise_binary | 22 | 13.72 | 0.0 | 37.03 | 0.0 | 22.08 | 59.29 | 67.14 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer24 | gemm | 14 | 33.49 | 37.04 | 36.51 | 0.0 | 69.5 | 89.62 | 15.2 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer24 | concat | 12 | 14.99 | 0.0 | 4.95 | 0.0 | 3.76 | 65.46 | 66.93 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer24 | elementwise_other | 14 | 3.64 | 0.0 | 53.73 | 0.0 | 21.24 | 50.78 | 32.92 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer24 | attention | 4 | 18.47 | 8.92 | 37.79 | 0.0 | 25.74 | 57.43 | 33.33 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer25 | copy | 8 | 9.95 | 0.0 | 45.08 | 0.0 | 26.83 | 51.54 | 49.33 | 0.67 |  |  | underutilised: SM 18 %, DRAM 31 %, L2 30 %, occ 66 % |
| planner_debate | 896 | mir_operator:prefill_layer25 | elementwise_unary | 8 | 0.85 | 0.0 | 28.33 | 0.0 | 14.72 | 69.71 | 18.03 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer25 | reduce | 8 | 6.25 | 0.0 | 32.03 | 0.0 | 12.58 | 26.99 | 36.12 | 0.24 |  |  | underutilised: SM 1 %, DRAM 34 %, L2 13 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer25 | elementwise_binary | 22 | 13.95 | 0.0 | 36.79 | 0.0 | 22.45 | 59.97 | 66.65 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer25 | gemm | 14 | 33.13 | 36.94 | 36.85 | 0.0 | 69.32 | 89.59 | 15.24 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer25 | concat | 12 | 14.81 | 0.0 | 4.91 | 0.0 | 3.66 | 62.3 | 66.5 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 4 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer25 | elementwise_other | 14 | 3.65 | 0.0 | 53.35 | 0.0 | 21.06 | 50.78 | 32.75 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer25 | attention | 4 | 18.38 | 8.88 | 37.76 | 0.0 | 25.53 | 57.39 | 33.5 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer26 | copy | 8 | 9.95 | 0.0 | 45.8 | 0.0 | 28.01 | 52.38 | 49.59 | 0.67 |  |  | underutilised: SM 18 %, DRAM 33 %, L2 32 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer26 | elementwise_unary | 8 | 0.83 | 0.0 | 28.08 | 0.0 | 13.21 | 70.7 | 17.87 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 27 % |
| planner_debate | 896 | mir_operator:prefill_layer26 | reduce | 8 | 6.23 | 0.0 | 32.69 | 0.0 | 12.85 | 26.83 | 36.67 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer26 | elementwise_binary | 22 | 13.76 | 0.0 | 35.74 | 0.0 | 22.61 | 59.35 | 67.2 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer26 | gemm | 14 | 30.99 | 37.03 | 37.26 | 0.0 | 69.17 | 89.6 | 15.25 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer26 | concat | 12 | 14.88 | 0.0 | 4.92 | 0.0 | 3.7 | 65.61 | 66.6 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 70 % |
| planner_debate | 896 | mir_operator:prefill_layer26 | elementwise_other | 14 | 3.73 | 0.0 | 54.42 | 0.0 | 21.52 | 50.76 | 33.05 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer26 | attention | 4 | 18.36 | 8.91 | 38.27 | 0.0 | 25.58 | 56.69 | 33.11 | 1.42 |  |  | underutilised: SM 11 %, DRAM 13 %, L2 25 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer27 | copy | 8 | 9.53 | 0.0 | 44.99 | 0.0 | 27.68 | 52.42 | 48.12 | 0.67 |  |  | underutilised: SM 18 %, DRAM 33 %, L2 32 %, occ 64 % |
| planner_debate | 896 | mir_operator:prefill_layer27 | elementwise_unary | 8 | 0.82 | 0.0 | 28.38 | 0.0 | 13.38 | 71.07 | 17.94 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer27 | reduce | 8 | 6.11 | 0.0 | 32.74 | 0.0 | 12.96 | 26.73 | 35.7 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer27 | elementwise_binary | 22 | 9.79 | 0.0 | 34.78 | 0.0 | 21.62 | 59.52 | 66.67 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer27 | gemm | 14 | 33.2 | 37.03 | 37.76 | 0.0 | 69.14 | 89.58 | 15.25 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer27 | concat | 12 | 14.84 | 0.0 | 4.91 | 0.0 | 3.73 | 63.93 | 66.83 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer27 | elementwise_other | 14 | 3.62 | 0.0 | 54.08 | 0.0 | 21.41 | 50.78 | 32.95 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer27 | attention | 4 | 18.35 | 8.89 | 37.37 | 0.0 | 25.7 | 57.24 | 33.29 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer28 | copy | 8 | 10.22 | 0.0 | 46.28 | 0.0 | 26.4 | 52.71 | 49.5 | 0.67 |  |  | underutilised: SM 19 %, DRAM 30 %, L2 29 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer28 | elementwise_unary | 8 | 0.83 | 0.0 | 30.81 | 0.0 | 13.69 | 51.5 | 17.91 | 0.21 |  |  | underutilised: SM 2 %, DRAM 57 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer28 | reduce | 8 | 6.35 | 0.0 | 32.56 | 0.0 | 12.82 | 26.98 | 36.32 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer28 | elementwise_binary | 22 | 14.02 | 0.0 | 35.4 | 0.0 | 21.99 | 59.89 | 67.77 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer28 | gemm | 14 | 33.35 | 37.04 | 36.98 | 0.0 | 69.45 | 89.63 | 15.26 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer28 | concat | 12 | 14.8 | 0.0 | 4.94 | 0.0 | 3.73 | 65.23 | 67.27 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 4 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer28 | elementwise_other | 14 | 3.76 | 0.0 | 55.41 | 0.0 | 21.84 | 50.8 | 32.78 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer28 | attention | 4 | 18.42 | 8.85 | 38.17 | 0.0 | 25.7 | 57.31 | 33.05 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer29 | copy | 8 | 9.52 | 0.0 | 45.08 | 0.0 | 27.38 | 52.53 | 49.7 | 0.67 |  |  | underutilised: SM 17 %, DRAM 32 %, L2 30 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer29 | elementwise_unary | 8 | 0.84 | 0.0 | 28.23 | 0.0 | 13.3 | 70.39 | 17.87 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 27 % |
| planner_debate | 896 | mir_operator:prefill_layer29 | reduce | 8 | 6.01 | 0.0 | 32.1 | 0.0 | 13.26 | 26.69 | 36.25 | 0.24 |  |  | underutilised: SM 1 %, DRAM 34 %, L2 13 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer29 | elementwise_binary | 22 | 13.54 | 0.0 | 36.2 | 0.0 | 21.82 | 59.62 | 67.62 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer29 | gemm | 14 | 33.52 | 36.89 | 37.13 | 0.0 | 69.24 | 89.61 | 15.21 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer29 | concat | 12 | 14.26 | 0.0 | 4.87 | 0.0 | 3.6 | 64.92 | 66.95 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer29 | elementwise_other | 14 | 3.82 | 0.0 | 55.03 | 0.0 | 21.79 | 50.85 | 32.98 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer29 | attention | 4 | 18.4 | 8.96 | 37.64 | 0.0 | 25.83 | 57.34 | 33.13 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer30 | copy | 8 | 10.09 | 0.0 | 44.69 | 0.0 | 27.41 | 52.54 | 49.15 | 0.67 |  |  | underutilised: SM 18 %, DRAM 32 %, L2 31 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer30 | elementwise_unary | 8 | 0.84 | 0.0 | 28.13 | 0.0 | 13.31 | 71.0 | 18.04 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer30 | reduce | 8 | 4.96 | 0.0 | 33.17 | 0.0 | 13.06 | 26.31 | 35.9 | 0.24 |  |  | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer30 | elementwise_binary | 22 | 13.64 | 0.0 | 36.26 | 0.0 | 22.62 | 59.86 | 67.07 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer30 | gemm | 14 | 30.65 | 36.88 | 37.12 | 0.0 | 67.85 | 89.62 | 15.26 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer30 | concat | 12 | 14.82 | 0.0 | 4.9 | 0.0 | 3.7 | 64.24 | 66.49 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer30 | elementwise_other | 14 | 3.73 | 0.0 | 54.97 | 0.0 | 21.71 | 50.77 | 33.12 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer30 | attention | 4 | 18.54 | 8.98 | 37.8 | 0.0 | 25.55 | 57.24 | 33.04 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer31 | copy | 8 | 10.33 | 0.0 | 45.97 | 0.0 | 27.03 | 52.37 | 48.72 | 0.67 |  |  | underutilised: SM 19 %, DRAM 32 %, L2 31 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer31 | elementwise_unary | 8 | 0.84 | 0.0 | 26.69 | 0.0 | 12.47 | 70.02 | 18.09 | 0.21 |  |  | underutilised: SM 2 %, DRAM 59 %, L2 27 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer31 | reduce | 8 | 6.23 | 0.0 | 32.23 | 0.0 | 12.7 | 27.04 | 36.22 | 0.24 |  |  | underutilised: SM 1 %, DRAM 34 %, L2 13 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer31 | elementwise_binary | 22 | 13.76 | 0.0 | 36.28 | 0.0 | 22.17 | 59.97 | 67.3 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer31 | gemm | 14 | 30.93 | 36.94 | 36.78 | 0.0 | 68.24 | 89.59 | 15.22 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer31 | concat | 12 | 14.51 | 0.0 | 4.93 | 0.0 | 3.76 | 65.32 | 67.17 | 1.33 |  |  | underutilised: SM 15 %, DRAM 3 %, L2 3 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer31 | elementwise_other | 14 | 3.75 | 0.0 | 38.49 | 0.0 | 17.78 | 50.71 | 32.82 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer31 | attention | 4 | 18.45 | 8.77 | 37.67 | 0.0 | 25.43 | 57.25 | 32.92 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer32 | copy | 8 | 9.78 | 0.0 | 45.72 | 0.0 | 27.92 | 52.43 | 49.21 | 0.67 |  |  | underutilised: SM 19 %, DRAM 34 %, L2 32 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer32 | elementwise_unary | 8 | 0.84 | 0.0 | 29.24 | 0.0 | 13.34 | 71.31 | 17.93 | 0.21 |  |  | underutilised: SM 2 %, DRAM 59 %, L2 25 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer32 | reduce | 8 | 6.14 | 0.0 | 32.74 | 0.0 | 12.93 | 26.75 | 36.05 | 0.24 |  |  | underutilised: SM 1 %, DRAM 36 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer32 | elementwise_binary | 22 | 13.72 | 0.0 | 36.8 | 0.0 | 21.51 | 59.97 | 66.41 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer32 | gemm | 14 | 33.1 | 36.95 | 37.34 | 0.0 | 68.49 | 89.56 | 15.21 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer32 | concat | 12 | 14.49 | 0.0 | 4.93 | 0.0 | 3.7 | 63.48 | 67.2 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer32 | elementwise_other | 14 | 3.84 | 0.0 | 55.17 | 0.0 | 21.35 | 50.77 | 33.14 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer32 | attention | 4 | 18.49 | 9.01 | 37.5 | 0.0 | 25.75 | 57.19 | 33.8 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer33 | copy | 8 | 9.96 | 0.0 | 45.19 | 0.0 | 28.0 | 52.45 | 49.61 | 0.67 |  |  | underutilised: SM 18 %, DRAM 33 %, L2 32 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer33 | elementwise_unary | 8 | 0.86 | 0.0 | 28.28 | 0.0 | 13.55 | 71.86 | 17.97 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer33 | reduce | 8 | 6.05 | 0.0 | 32.05 | 0.0 | 12.63 | 26.33 | 36.47 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer33 | elementwise_binary | 22 | 13.9 | 0.0 | 37.06 | 0.0 | 22.28 | 59.51 | 66.76 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer33 | gemm | 14 | 33.48 | 37.09 | 36.39 | 0.0 | 68.14 | 89.61 | 15.22 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer33 | concat | 12 | 13.83 | 0.0 | 4.91 | 0.0 | 3.72 | 65.48 | 67.14 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 3 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer33 | elementwise_other | 14 | 3.77 | 0.0 | 54.44 | 0.0 | 21.49 | 50.72 | 32.68 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer33 | attention | 4 | 18.51 | 8.92 | 37.33 | 0.0 | 25.56 | 57.16 | 33.47 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer34 | copy | 8 | 9.68 | 0.0 | 45.29 | 0.0 | 26.87 | 52.48 | 48.37 | 0.67 |  |  | underutilised: SM 19 %, DRAM 32 %, L2 30 %, occ 67 % |
| planner_debate | 896 | mir_operator:prefill_layer34 | elementwise_unary | 8 | 0.84 | 0.0 | 27.79 | 0.0 | 13.09 | 72.1 | 17.97 | 0.21 |  |  | underutilised: SM 2 %, DRAM 55 %, L2 25 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer34 | reduce | 8 | 6.1 | 0.0 | 32.63 | 0.0 | 12.67 | 26.75 | 36.78 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer34 | elementwise_binary | 22 | 13.6 | 0.0 | 35.97 | 0.0 | 22.53 | 59.41 | 67.38 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer34 | gemm | 14 | 30.84 | 36.86 | 36.96 | 0.0 | 67.88 | 89.61 | 15.21 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer34 | concat | 12 | 14.48 | 0.0 | 4.93 | 0.0 | 3.79 | 64.68 | 67.5 | 1.33 |  |  | underutilised: SM 15 %, DRAM 3 %, L2 3 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer34 | elementwise_other | 14 | 3.71 | 0.0 | 54.7 | 0.0 | 21.57 | 50.76 | 33.08 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer34 | attention | 4 | 18.44 | 9.08 | 37.67 | 0.0 | 25.32 | 57.43 | 33.14 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_layer35 | copy | 8 | 9.99 | 0.0 | 45.31 | 0.0 | 27.52 | 52.58 | 49.13 | 0.67 |  |  | underutilised: SM 19 %, DRAM 32 %, L2 31 %, occ 66 % |
| planner_debate | 896 | mir_operator:prefill_layer35 | elementwise_unary | 8 | 0.83 | 0.0 | 28.37 | 0.0 | 13.4 | 69.93 | 18.02 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_layer35 | reduce | 8 | 6.04 | 0.0 | 32.52 | 0.0 | 12.79 | 26.96 | 36.41 | 0.24 |  |  | underutilised: SM 1 %, DRAM 35 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_layer35 | elementwise_binary | 22 | 13.35 | 0.0 | 36.46 | 0.0 | 22.18 | 59.55 | 67.8 | 0.83 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer35 | gemm | 14 | 30.73 | 37.04 | 36.91 | 0.0 | 67.19 | 89.57 | 15.23 | 2.5 |  |  | L2-bandwidth-bound (working set in L2) |
| planner_debate | 896 | mir_operator:prefill_layer35 | concat | 12 | 14.71 | 0.0 | 4.93 | 0.0 | 3.85 | 64.68 | 66.76 | 1.33 |  |  | underutilised: SM 16 %, DRAM 3 %, L2 4 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_layer35 | elementwise_other | 14 | 3.71 | 0.0 | 55.37 | 0.0 | 21.89 | 50.83 | 33.11 | 0.46 |  |  | latency/launch-bound: 0.42 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_layer35 | attention | 4 | 18.31 | 8.79 | 37.58 | 0.0 | 25.79 | 57.32 | 33.89 | 1.42 |  |  | underutilised: SM 11 %, DRAM 10 %, L2 26 %, occ 8 % |
| planner_debate | 896 | mir_operator:prefill_head | copy | 4 | 10.0 | 0.0 | 45.28 | 0.0 | 28.01 | 52.56 | 50.24 | 0.67 |  |  | underutilised: SM 18 %, DRAM 33 %, L2 32 %, occ 68 % |
| planner_debate | 896 | mir_operator:prefill_head | elementwise_unary | 4 | 0.84 | 0.0 | 28.37 | 0.0 | 13.38 | 70.6 | 17.96 | 0.21 |  |  | underutilised: SM 2 %, DRAM 56 %, L2 26 %, occ 28 % |
| planner_debate | 896 | mir_operator:prefill_head | reduce | 2 | 1.22 | 0.0 | 38.05 | 0.0 | 14.93 | 16.64 | 33.27 | 0.06 |  |  | underutilised: SM 1 %, DRAM 34 %, L2 14 %, occ 33 % |
| planner_debate | 896 | mir_operator:prefill_head | elementwise_binary | 6 | 13.89 | 0.0 | 36.09 | 0.0 | 22.49 | 59.99 | 68.38 | 0.92 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:prefill_head | gemm | 2 | 41.79 | 42.3 | 64.5 | 0.0 | 67.04 | 88.11 | 16.31 | 19.7 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:prefill_sample | reduce | 2 | 2.75 | 0.0 | 5.26 | 0.0 | 2.99 | 65.14 | 33.12 | 0.05 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_embed | other | 2 | 0.25 | 0.0 | 0.34 | 0.0 | 0.65 | 98.98 | 8.32 | 0.01 |  |  | latency/launch-bound: 0.01 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer00 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.85 | 92.36 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer00 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 88.65 | 7.58 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer00 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.83 | 91.17 | 31.94 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer00 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.51 | 91.83 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer00 | gemv | 14 | 15.2 | 0.0 | 73.88 | 0.0 | 44.15 | 9.07 | 16.06 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer00 | concat | 12 | 1.19 | 0.0 | 0.31 | 0.0 | 0.7 | 95.22 | 9.14 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer00 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.07 | 91.22 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer00 | attention | 4 | 0.6 | 12.74 | 3.33 | 0.0 | 2.11 | 72.54 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer01 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.57 | 86.07 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer01 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 0.89 | 88.88 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer01 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.82 | 91.07 | 31.93 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer01 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.4 | 91.46 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer01 | gemv | 14 | 15.17 | 0.0 | 74.64 | 0.0 | 45.59 | 9.28 | 16.1 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer01 | concat | 12 | 1.18 | 0.0 | 0.31 | 0.0 | 0.71 | 93.71 | 9.13 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer01 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.08 | 90.41 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer01 | attention | 4 | 0.6 | 12.62 | 3.32 | 0.0 | 2.14 | 72.76 | 8.31 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer02 | copy | 8 | 0.04 | 0.0 | 0.9 | 0.0 | 1.75 | 90.83 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer02 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.92 | 88.52 | 7.64 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer02 | reduce | 4 | 0.09 | 0.0 | 1.99 | 0.0 | 3.85 | 90.31 | 31.91 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer02 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.41 | 90.22 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer02 | gemv | 14 | 15.3 | 0.0 | 75.28 | 0.0 | 44.27 | 9.24 | 16.02 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer02 | concat | 12 | 1.15 | 0.0 | 0.32 | 0.0 | 0.9 | 97.16 | 9.08 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer02 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.42 | 87.22 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer02 | attention | 4 | 0.6 | 12.62 | 3.37 | 0.0 | 2.14 | 72.77 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer03 | copy | 8 | 0.04 | 0.0 | 1.08 | 0.0 | 1.84 | 90.09 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer03 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 93.58 | 7.66 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer03 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.81 | 90.32 | 31.96 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer03 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.46 | 90.04 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer03 | gemv | 14 | 15.41 | 0.0 | 74.9 | 0.0 | 45.41 | 9.27 | 16.13 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer03 | concat | 12 | 1.2 | 0.0 | 0.35 | 0.0 | 0.92 | 90.24 | 9.13 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer03 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.12 | 89.63 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer03 | attention | 4 | 0.61 | 12.65 | 3.37 | 0.0 | 2.14 | 73.19 | 8.28 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer04 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.77 | 88.45 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer04 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.89 | 91.87 | 7.66 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer04 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.79 | 91.03 | 31.89 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer04 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.5 | 90.3 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer04 | gemv | 14 | 15.35 | 0.0 | 74.65 | 0.0 | 45.96 | 9.27 | 16.13 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer04 | concat | 12 | 1.15 | 0.0 | 0.31 | 0.0 | 0.7 | 96.57 | 9.1 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer04 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.24 | 89.5 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer04 | attention | 4 | 0.6 | 12.52 | 3.36 | 0.0 | 2.2 | 75.62 | 8.28 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer05 | copy | 8 | 0.04 | 0.0 | 0.93 | 0.0 | 1.63 | 92.19 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer05 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 92.61 | 7.68 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer05 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.84 | 90.9 | 31.88 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer05 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.41 | 90.26 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer05 | gemv | 14 | 15.41 | 0.0 | 74.87 | 0.0 | 45.61 | 9.19 | 16.09 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer05 | concat | 12 | 1.18 | 0.0 | 0.31 | 0.0 | 0.71 | 89.26 | 9.17 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer05 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.13 | 92.62 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer05 | attention | 4 | 0.61 | 12.57 | 3.33 | 0.0 | 2.14 | 71.66 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer06 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 2.26 | 90.13 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer06 | elementwise_unary | 8 | 0.02 | 0.0 | 0.43 | 0.0 | 0.92 | 93.25 | 7.35 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer06 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.81 | 90.76 | 31.83 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer06 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.49 | 91.15 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer06 | gemv | 14 | 15.45 | 0.0 | 75.08 | 0.0 | 45.67 | 9.26 | 16.06 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer06 | concat | 12 | 1.19 | 0.0 | 0.28 | 0.0 | 0.74 | 86.35 | 9.14 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer06 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.25 | 91.35 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer06 | attention | 4 | 0.61 | 12.58 | 3.34 | 0.0 | 2.13 | 79.58 | 8.25 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer07 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.57 | 88.76 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer07 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 0.88 | 90.54 | 7.62 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer07 | reduce | 4 | 0.09 | 0.0 | 1.99 | 0.0 | 3.83 | 91.99 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer07 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.45 | 88.66 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer07 | gemv | 14 | 15.52 | 0.0 | 75.32 | 0.0 | 46.0 | 9.21 | 16.16 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer07 | concat | 12 | 1.14 | 0.0 | 0.32 | 0.0 | 0.74 | 78.28 | 9.12 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer07 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.08 | 86.56 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer07 | attention | 4 | 0.61 | 12.76 | 3.37 | 0.0 | 2.17 | 74.37 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer08 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.6 | 90.91 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer08 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.91 | 90.2 | 7.56 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer08 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.81 | 91.04 | 31.89 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer08 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.41 | 90.31 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer08 | gemv | 14 | 15.47 | 0.0 | 75.43 | 0.0 | 46.05 | 9.29 | 16.14 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer08 | concat | 12 | 1.15 | 0.0 | 0.35 | 0.0 | 0.9 | 93.02 | 9.11 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer08 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.07 | 87.56 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer08 | attention | 4 | 0.6 | 12.38 | 3.36 | 0.0 | 2.17 | 72.46 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer09 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.62 | 87.22 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer09 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.91 | 87.6 | 7.53 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer09 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.87 | 90.25 | 31.89 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer09 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.53 | 89.53 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer09 | gemv | 14 | 15.62 | 0.0 | 75.29 | 0.0 | 46.0 | 9.2 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer09 | concat | 12 | 1.15 | 0.0 | 0.31 | 0.0 | 0.7 | 92.26 | 9.13 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer09 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.09 | 87.94 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer09 | attention | 4 | 0.61 | 12.58 | 3.34 | 0.0 | 2.14 | 73.28 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer10 | copy | 8 | 0.04 | 0.0 | 0.93 | 0.0 | 1.87 | 88.31 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer10 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.95 | 83.44 | 7.65 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer10 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.87 | 89.96 | 31.89 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer10 | elementwise_binary | 22 | 0.02 | 0.0 | 0.84 | 0.0 | 1.41 | 91.2 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer10 | gemv | 14 | 15.46 | 0.0 | 75.29 | 0.0 | 46.28 | 9.25 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer10 | concat | 12 | 1.17 | 0.0 | 0.32 | 0.0 | 0.71 | 94.24 | 9.08 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer10 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.37 | 87.49 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer10 | attention | 4 | 0.61 | 12.52 | 3.36 | 0.0 | 2.25 | 73.26 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer11 | copy | 8 | 0.04 | 0.0 | 1.08 | 0.0 | 1.86 | 90.87 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer11 | elementwise_unary | 8 | 0.02 | 0.0 | 0.73 | 0.0 | 0.91 | 87.18 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer11 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.83 | 90.46 | 31.82 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer11 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.39 | 90.96 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer11 | gemv | 14 | 15.52 | 0.0 | 73.84 | 0.0 | 45.64 | 9.23 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer11 | concat | 12 | 1.18 | 0.0 | 0.31 | 0.0 | 0.7 | 93.89 | 9.14 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer11 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.12 | 86.75 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer11 | attention | 4 | 0.61 | 12.6 | 3.37 | 0.0 | 2.16 | 72.87 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer12 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.6 | 87.08 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer12 | elementwise_unary | 8 | 0.02 | 0.0 | 0.55 | 0.0 | 0.92 | 87.69 | 7.62 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer12 | reduce | 4 | 0.09 | 0.0 | 1.99 | 0.0 | 3.84 | 89.73 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer12 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.41 | 91.37 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer12 | gemv | 14 | 15.51 | 0.0 | 75.29 | 0.0 | 45.44 | 9.19 | 16.13 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer12 | concat | 12 | 1.18 | 0.0 | 0.31 | 0.0 | 0.99 | 93.71 | 9.14 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer12 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.08 | 90.45 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer12 | attention | 4 | 0.6 | 12.69 | 3.36 | 0.0 | 2.16 | 71.69 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer13 | copy | 8 | 0.04 | 0.0 | 0.93 | 0.0 | 1.59 | 90.93 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer13 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.91 | 93.62 | 7.66 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer13 | reduce | 4 | 0.09 | 0.0 | 1.99 | 0.0 | 3.84 | 90.87 | 31.89 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer13 | elementwise_binary | 22 | 0.02 | 0.0 | 0.84 | 0.0 | 1.41 | 91.05 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer13 | gemv | 14 | 15.52 | 0.0 | 73.87 | 0.0 | 45.5 | 9.16 | 16.07 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer13 | concat | 12 | 1.19 | 0.0 | 0.31 | 0.0 | 0.7 | 93.02 | 9.17 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer13 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.27 | 88.95 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer13 | attention | 4 | 0.61 | 12.48 | 3.32 | 0.0 | 2.11 | 73.62 | 8.28 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer14 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.56 | 93.56 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer14 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.89 | 92.17 | 7.65 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer14 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.84 | 91.04 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer14 | elementwise_binary | 22 | 0.02 | 0.0 | 0.84 | 0.0 | 1.45 | 91.5 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer14 | gemv | 14 | 15.39 | 0.0 | 75.17 | 0.0 | 46.53 | 9.23 | 16.1 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer14 | concat | 12 | 1.19 | 0.0 | 0.35 | 0.0 | 0.7 | 88.52 | 9.15 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer14 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.44 | 91.18 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer14 | attention | 4 | 0.61 | 12.59 | 3.8 | 0.0 | 2.28 | 72.56 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer15 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.59 | 89.79 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer15 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.92 | 96.33 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer15 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.82 | 91.06 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer15 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.45 | 87.66 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer15 | gemv | 14 | 15.45 | 0.0 | 74.15 | 0.0 | 45.65 | 9.1 | 16.13 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer15 | concat | 12 | 1.15 | 0.0 | 0.32 | 0.0 | 0.74 | 80.15 | 9.12 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer15 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.1 | 85.52 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer15 | attention | 4 | 0.61 | 12.63 | 3.37 | 0.0 | 2.23 | 70.56 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer16 | copy | 8 | 0.04 | 0.0 | 1.08 | 0.0 | 1.86 | 88.68 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer16 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 92.62 | 7.67 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer16 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.81 | 90.32 | 31.92 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer16 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.41 | 91.56 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer16 | gemv | 14 | 15.51 | 0.0 | 75.16 | 0.0 | 44.75 | 9.28 | 16.18 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer16 | concat | 12 | 1.19 | 0.0 | 0.32 | 0.0 | 0.74 | 91.47 | 9.15 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer16 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.07 | 87.3 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer16 | attention | 4 | 0.6 | 12.74 | 3.37 | 0.0 | 2.17 | 72.8 | 8.26 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer17 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.57 | 90.87 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer17 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.92 | 92.26 | 7.79 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer17 | reduce | 4 | 0.09 | 0.0 | 1.99 | 0.0 | 3.83 | 91.71 | 31.82 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer17 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.41 | 90.66 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer17 | gemv | 14 | 15.29 | 0.0 | 74.69 | 0.0 | 45.59 | 9.33 | 16.09 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer17 | concat | 12 | 1.18 | 0.0 | 0.32 | 0.0 | 0.74 | 93.63 | 9.05 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer17 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.07 | 90.64 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer17 | attention | 4 | 0.61 | 12.71 | 3.33 | 0.0 | 2.16 | 73.11 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer18 | copy | 8 | 0.04 | 0.0 | 0.93 | 0.0 | 1.65 | 86.64 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer18 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.92 | 88.28 | 7.68 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer18 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.83 | 90.91 | 31.84 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer18 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.46 | 88.14 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer18 | gemv | 14 | 15.29 | 0.0 | 75.18 | 0.0 | 46.31 | 9.3 | 16.17 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer18 | concat | 12 | 1.19 | 0.0 | 0.35 | 0.0 | 0.7 | 84.23 | 9.12 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer18 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.27 | 85.7 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer18 | attention | 4 | 0.61 | 12.55 | 3.36 | 0.0 | 2.16 | 75.61 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer19 | copy | 8 | 0.04 | 0.0 | 0.93 | 0.0 | 1.64 | 87.72 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer19 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.91 | 88.63 | 7.68 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer19 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.9 | 87.97 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer19 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.4 | 89.89 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer19 | gemv | 14 | 15.43 | 0.0 | 75.09 | 0.0 | 46.12 | 9.18 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer19 | concat | 12 | 1.19 | 0.0 | 0.31 | 0.0 | 0.71 | 81.6 | 9.13 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer19 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.08 | 91.17 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer19 | attention | 4 | 0.61 | 12.5 | 3.35 | 0.0 | 2.16 | 74.73 | 8.28 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer20 | copy | 8 | 0.04 | 0.0 | 0.93 | 0.0 | 1.84 | 84.48 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer20 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.91 | 93.02 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer20 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.84 | 90.24 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer20 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.41 | 95.37 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer20 | gemv | 14 | 15.51 | 0.0 | 74.41 | 0.0 | 45.45 | 9.15 | 16.07 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer20 | concat | 12 | 1.11 | 0.0 | 0.31 | 0.0 | 1.0 | 89.99 | 9.13 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer20 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.23 | 90.58 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer20 | attention | 4 | 0.6 | 12.78 | 3.35 | 0.0 | 2.25 | 74.39 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer21 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.57 | 86.9 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer21 | elementwise_unary | 8 | 0.02 | 0.0 | 0.55 | 0.0 | 0.93 | 90.1 | 7.72 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer21 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.84 | 90.85 | 31.88 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer21 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.46 | 89.87 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer21 | gemv | 14 | 15.45 | 0.0 | 74.51 | 0.0 | 45.69 | 9.23 | 16.1 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer21 | concat | 12 | 1.18 | 0.0 | 0.32 | 0.0 | 0.74 | 81.07 | 9.15 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer21 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.08 | 89.79 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer21 | attention | 4 | 0.61 | 12.78 | 3.36 | 0.0 | 2.16 | 76.12 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer22 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.57 | 91.89 | 8.32 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer22 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.93 | 89.01 | 7.7 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer22 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.83 | 91.94 | 31.83 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer22 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.42 | 91.38 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer22 | gemv | 14 | 15.41 | 0.0 | 74.19 | 0.0 | 45.96 | 9.13 | 16.1 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer22 | concat | 12 | 1.14 | 0.0 | 0.31 | 0.0 | 0.71 | 91.41 | 9.15 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer22 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.25 | 93.13 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer22 | attention | 4 | 0.61 | 12.6 | 3.36 | 0.0 | 2.16 | 75.33 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer23 | copy | 8 | 0.04 | 0.0 | 0.93 | 0.0 | 1.59 | 91.99 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer23 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 95.71 | 7.58 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer23 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.82 | 91.09 | 31.9 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer23 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.4 | 93.83 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer23 | gemv | 14 | 15.45 | 0.0 | 75.15 | 0.0 | 45.64 | 9.11 | 16.11 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer23 | concat | 12 | 1.19 | 0.0 | 0.32 | 0.0 | 0.7 | 96.2 | 9.15 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer23 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.08 | 90.07 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer23 | attention | 4 | 0.6 | 12.62 | 3.36 | 0.0 | 2.26 | 73.1 | 8.28 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer24 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.65 | 93.87 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer24 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 88.36 | 7.71 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer24 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.84 | 91.41 | 31.91 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer24 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.4 | 92.02 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer24 | gemv | 14 | 15.48 | 0.0 | 75.2 | 0.0 | 44.66 | 9.07 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer24 | concat | 12 | 1.18 | 0.0 | 0.31 | 0.0 | 0.74 | 92.52 | 9.08 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer24 | elementwise_other | 14 | 0.02 | 0.0 | 0.85 | 0.0 | 1.27 | 93.25 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer24 | attention | 4 | 0.6 | 12.58 | 3.28 | 0.0 | 2.15 | 74.76 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer25 | copy | 8 | 0.04 | 0.0 | 0.93 | 0.0 | 1.63 | 89.77 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer25 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 0.91 | 94.15 | 7.71 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer25 | reduce | 4 | 0.09 | 0.0 | 1.99 | 0.0 | 3.84 | 92.17 | 31.85 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer25 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.49 | 89.89 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer25 | gemv | 14 | 15.49 | 0.0 | 75.2 | 0.0 | 45.96 | 9.19 | 16.09 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer25 | concat | 12 | 1.18 | 0.0 | 0.31 | 0.0 | 0.7 | 90.5 | 9.15 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer25 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.27 | 89.82 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer25 | attention | 4 | 0.61 | 12.57 | 3.31 | 0.0 | 2.17 | 74.39 | 8.31 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer26 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.88 | 88.81 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer26 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 94.78 | 7.7 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer26 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.81 | 91.95 | 31.89 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer26 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.6 | 91.6 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer26 | gemv | 14 | 15.29 | 0.0 | 74.42 | 0.0 | 45.0 | 9.07 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer26 | concat | 12 | 1.15 | 0.0 | 0.32 | 0.0 | 0.71 | 90.2 | 9.15 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer26 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.25 | 92.89 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer26 | attention | 4 | 0.61 | 12.59 | 3.36 | 0.0 | 2.17 | 75.39 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer27 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.55 | 90.47 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer27 | elementwise_unary | 8 | 0.02 | 0.0 | 0.51 | 0.0 | 0.89 | 94.18 | 7.7 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer27 | reduce | 4 | 0.08 | 0.0 | 1.96 | 0.0 | 3.8 | 90.34 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer27 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.5 | 93.17 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer27 | gemv | 14 | 15.4 | 0.0 | 74.65 | 0.0 | 45.79 | 9.19 | 16.13 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer27 | concat | 12 | 1.16 | 0.0 | 0.31 | 0.0 | 0.75 | 89.37 | 9.13 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer27 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.07 | 90.08 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer27 | attention | 4 | 0.61 | 12.65 | 3.35 | 0.0 | 2.17 | 72.98 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer28 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.56 | 90.39 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer28 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 0.9 | 87.21 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer28 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.83 | 91.8 | 31.92 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer28 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.41 | 91.81 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer28 | gemv | 14 | 15.44 | 0.0 | 74.6 | 0.0 | 45.78 | 9.27 | 16.14 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer28 | concat | 12 | 1.15 | 0.0 | 0.31 | 0.0 | 0.69 | 95.78 | 9.13 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer28 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.08 | 90.88 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer28 | attention | 4 | 0.6 | 12.7 | 3.34 | 0.0 | 2.17 | 72.12 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer29 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.59 | 94.13 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer29 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 88.41 | 7.7 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer29 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.8 | 90.89 | 31.94 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer29 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.41 | 91.79 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer29 | gemv | 14 | 15.53 | 0.0 | 74.68 | 0.0 | 46.12 | 9.15 | 16.15 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer29 | concat | 12 | 1.15 | 0.0 | 0.31 | 0.0 | 0.71 | 88.98 | 9.09 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer29 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.27 | 89.89 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer29 | attention | 4 | 0.61 | 12.68 | 3.32 | 0.0 | 2.16 | 74.16 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer30 | copy | 8 | 0.04 | 0.0 | 0.93 | 0.0 | 1.6 | 87.42 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer30 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.91 | 92.08 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer30 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.83 | 89.54 | 31.92 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer30 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.41 | 90.58 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer30 | gemv | 14 | 15.54 | 0.0 | 74.9 | 0.0 | 45.62 | 9.16 | 16.13 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer30 | concat | 12 | 1.15 | 0.0 | 0.31 | 0.0 | 0.73 | 91.06 | 9.15 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer30 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.09 | 89.25 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer30 | attention | 4 | 0.61 | 12.45 | 3.37 | 0.0 | 2.18 | 74.21 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer31 | copy | 8 | 0.04 | 0.0 | 0.9 | 0.0 | 1.55 | 90.69 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer31 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.91 | 89.51 | 7.6 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer31 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.82 | 91.29 | 31.84 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer31 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.54 | 90.06 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer31 | gemv | 14 | 15.4 | 0.0 | 74.43 | 0.0 | 45.43 | 9.07 | 16.14 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer31 | concat | 12 | 1.15 | 0.0 | 0.31 | 0.0 | 0.69 | 92.65 | 9.13 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer31 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.26 | 90.68 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer31 | attention | 4 | 0.61 | 12.54 | 3.25 | 0.0 | 2.11 | 73.59 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer32 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.56 | 91.88 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer32 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.91 | 94.09 | 7.72 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer32 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.84 | 90.95 | 31.82 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer32 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.41 | 93.22 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer32 | gemv | 14 | 15.52 | 0.0 | 74.41 | 0.0 | 45.51 | 9.12 | 16.09 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer32 | concat | 12 | 1.15 | 0.0 | 0.31 | 0.0 | 0.7 | 94.07 | 8.92 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer32 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.09 | 91.34 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer32 | attention | 4 | 0.6 | 12.56 | 3.07 | 0.0 | 2.01 | 73.53 | 8.24 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer33 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.58 | 93.8 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer33 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 0.89 | 92.54 | 7.7 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer33 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.82 | 89.88 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer33 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.42 | 93.92 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer33 | gemv | 14 | 15.36 | 0.0 | 74.43 | 0.0 | 45.8 | 9.28 | 16.06 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer33 | concat | 12 | 1.16 | 0.0 | 0.32 | 0.0 | 0.7 | 98.77 | 9.11 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer33 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.1 | 90.01 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer33 | attention | 4 | 0.6 | 12.47 | 3.34 | 0.0 | 2.15 | 74.63 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer34 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.56 | 92.01 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer34 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.9 | 89.51 | 7.71 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer34 | reduce | 4 | 0.09 | 0.0 | 1.98 | 0.0 | 3.84 | 89.66 | 31.85 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer34 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.47 | 92.21 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer34 | gemv | 14 | 15.42 | 0.0 | 74.84 | 0.0 | 46.01 | 9.13 | 16.13 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer34 | concat | 12 | 1.2 | 0.0 | 0.28 | 0.0 | 0.7 | 90.69 | 9.09 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer34 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.09 | 88.63 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer34 | attention | 4 | 0.61 | 12.73 | 3.36 | 0.0 | 2.15 | 73.68 | 8.29 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer35 | copy | 8 | 0.04 | 0.0 | 0.9 | 0.0 | 1.54 | 92.17 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer35 | elementwise_unary | 8 | 0.02 | 0.0 | 0.55 | 0.0 | 0.89 | 96.56 | 7.65 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer35 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.82 | 90.37 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer35 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.56 | 91.39 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer35 | gemv | 14 | 15.58 | 0.0 | 74.87 | 0.0 | 45.9 | 9.18 | 16.14 | 0.67 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_layer35 | concat | 12 | 1.14 | 0.0 | 0.32 | 0.0 | 0.71 | 92.4 | 9.11 | 0.11 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer35 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.08 | 86.53 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_layer35 | attention | 4 | 0.61 | 12.71 | 4.82 | 0.0 | 2.43 | 62.38 | 8.3 | 0.03 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_head | copy | 4 | 0.04 | 0.0 | 0.91 | 0.0 | 1.55 | 92.51 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_head | elementwise_unary | 4 | 0.02 | 0.0 | 0.54 | 0.0 | 0.92 | 94.19 | 7.72 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_head | reduce | 2 | 0.09 | 0.0 | 1.96 | 0.0 | 3.81 | 89.42 | 31.88 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_head | elementwise_binary | 6 | 0.02 | 0.0 | 0.81 | 0.0 | 1.06 | 90.14 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| planner_debate | 896 | mir_operator:decode_head | gemv | 2 | 19.92 | 0.0 | 97.06 | 0.0 | 61.64 | 0.54 | 24.49 | 49.46 |  |  | DRAM-bandwidth-bound |
| planner_debate | 896 | mir_operator:decode_sample | reduce | 2 | 2.19 | 0.0 | 5.29 | 0.0 | 3.01 | 66.48 | 33.12 | 0.05 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_embed | other | 2 | 2.82 | 0.0 | 11.19 | 0.0 | 16.48 | 84.75 | 23.61 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer00 | copy | 8 | 7.07 | 0.0 | 34.7 | 0.0 | 20.26 | 53.26 | 32.66 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer00 | elementwise_unary | 8 | 0.67 | 0.0 | 23.53 | 0.0 | 10.92 | 53.34 | 13.03 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer00 | reduce | 8 | 4.2 | 0.0 | 25.76 | 0.0 | 10.14 | 28.23 | 32.9 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer00 | elementwise_binary | 22 | 10.77 | 0.0 | 23.81 | 0.0 | 15.22 | 63.9 | 43.54 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer00 | gemm | 14 | 35.22 | 39.18 | 51.76 | 0.0 | 68.76 | 89.9 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer00 | concat | 12 | 11.65 | 0.0 | 3.3 | 0.0 | 2.29 | 64.17 | 67.4 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer00 | elementwise_other | 14 | 2.33 | 0.0 | 41.21 | 0.0 | 16.31 | 51.08 | 21.4 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer00 | attention | 4 | 15.76 | 8.38 | 28.47 | 0.0 | 18.34 | 57.16 | 24.98 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer01 | copy | 8 | 6.88 | 0.0 | 34.92 | 0.0 | 19.74 | 52.27 | 32.41 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer01 | elementwise_unary | 8 | 0.65 | 0.0 | 22.33 | 0.0 | 10.79 | 64.71 | 12.91 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer01 | reduce | 8 | 4.29 | 0.0 | 26.3 | 0.0 | 10.35 | 28.6 | 32.55 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer01 | elementwise_binary | 22 | 11.01 | 0.0 | 24.34 | 0.0 | 15.3 | 63.74 | 43.78 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer01 | gemm | 14 | 31.76 | 39.24 | 51.98 | 0.0 | 69.04 | 89.96 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer01 | concat | 12 | 11.69 | 0.0 | 3.36 | 0.0 | 2.34 | 65.24 | 67.63 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer01 | elementwise_other | 14 | 2.29 | 0.0 | 41.9 | 0.0 | 16.54 | 51.11 | 21.75 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer01 | attention | 4 | 15.63 | 8.11 | 28.58 | 0.0 | 18.79 | 57.19 | 24.99 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer02 | copy | 8 | 7.01 | 0.0 | 36.08 | 0.0 | 20.08 | 52.08 | 32.74 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer02 | elementwise_unary | 8 | 0.66 | 0.0 | 22.18 | 0.0 | 10.88 | 65.49 | 13.13 | 0.12 |  |  | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer02 | reduce | 8 | 4.18 | 0.0 | 26.24 | 0.0 | 10.3 | 28.59 | 32.74 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer02 | elementwise_binary | 22 | 10.79 | 0.0 | 24.45 | 0.0 | 15.39 | 63.85 | 42.84 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer02 | gemm | 14 | 35.41 | 38.98 | 51.88 | 0.0 | 69.82 | 90.04 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer02 | concat | 12 | 11.75 | 0.0 | 3.38 | 0.0 | 2.35 | 63.95 | 67.42 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer02 | elementwise_other | 14 | 2.27 | 0.0 | 41.75 | 0.0 | 16.45 | 50.42 | 21.77 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer02 | attention | 4 | 15.67 | 8.3 | 26.47 | 0.0 | 18.62 | 57.18 | 25.27 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer03 | copy | 8 | 7.18 | 0.0 | 35.66 | 0.0 | 20.18 | 52.37 | 32.48 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer03 | elementwise_unary | 8 | 0.65 | 0.0 | 22.12 | 0.0 | 10.68 | 64.47 | 13.09 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer03 | reduce | 8 | 4.24 | 0.0 | 25.86 | 0.0 | 10.15 | 28.65 | 32.69 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer03 | elementwise_binary | 22 | 10.86 | 0.0 | 23.79 | 0.0 | 15.45 | 63.74 | 43.7 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer03 | gemm | 14 | 35.22 | 39.17 | 50.67 | 0.0 | 68.99 | 89.9 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer03 | concat | 12 | 11.73 | 0.0 | 3.26 | 0.0 | 2.37 | 63.56 | 67.01 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer03 | elementwise_other | 14 | 2.27 | 0.0 | 40.45 | 0.0 | 15.97 | 51.14 | 21.74 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer03 | attention | 4 | 15.7 | 8.19 | 28.62 | 0.0 | 18.66 | 57.17 | 25.22 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer04 | copy | 8 | 7.08 | 0.0 | 34.52 | 0.0 | 20.48 | 53.23 | 32.68 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer04 | elementwise_unary | 8 | 0.66 | 0.0 | 24.12 | 0.0 | 11.15 | 51.77 | 12.96 | 0.12 |  |  | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer04 | reduce | 8 | 4.17 | 0.0 | 25.54 | 0.0 | 10.01 | 28.69 | 32.69 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer04 | elementwise_binary | 22 | 10.51 | 0.0 | 23.92 | 0.0 | 15.57 | 63.41 | 43.12 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer04 | gemm | 14 | 35.02 | 38.92 | 51.11 | 0.0 | 64.77 | 89.49 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer04 | concat | 12 | 11.47 | 0.0 | 3.3 | 0.0 | 2.36 | 63.52 | 67.01 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer04 | elementwise_other | 14 | 2.31 | 0.0 | 41.38 | 0.0 | 16.37 | 51.0 | 21.74 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer04 | attention | 4 | 15.61 | 8.2 | 28.19 | 0.0 | 18.76 | 57.17 | 25.12 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer05 | copy | 8 | 7.14 | 0.0 | 35.26 | 0.0 | 20.45 | 53.22 | 32.9 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer05 | elementwise_unary | 8 | 0.65 | 0.0 | 23.62 | 0.0 | 11.04 | 51.74 | 13.06 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer05 | reduce | 8 | 4.16 | 0.0 | 26.32 | 0.0 | 10.36 | 28.52 | 32.78 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer05 | elementwise_binary | 22 | 10.29 | 0.0 | 25.18 | 0.0 | 15.5 | 63.39 | 44.0 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer05 | gemm | 14 | 35.3 | 39.25 | 51.86 | 0.0 | 69.2 | 89.96 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer05 | concat | 12 | 11.62 | 0.0 | 3.35 | 0.0 | 2.28 | 64.99 | 67.13 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer05 | elementwise_other | 14 | 2.25 | 0.0 | 40.66 | 0.0 | 16.05 | 51.06 | 21.53 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer05 | attention | 4 | 15.71 | 8.49 | 28.42 | 0.0 | 18.69 | 57.35 | 24.99 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer06 | copy | 8 | 7.17 | 0.0 | 34.71 | 0.0 | 20.1 | 53.48 | 32.43 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer06 | elementwise_unary | 8 | 0.67 | 0.0 | 22.38 | 0.0 | 10.82 | 65.33 | 13.1 | 0.12 |  |  | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer06 | reduce | 8 | 4.24 | 0.0 | 25.8 | 0.0 | 10.17 | 28.62 | 32.55 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer06 | elementwise_binary | 22 | 10.71 | 0.0 | 23.18 | 0.0 | 14.84 | 64.57 | 43.37 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer06 | gemm | 14 | 34.99 | 39.05 | 52.12 | 0.0 | 67.92 | 89.97 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer06 | concat | 12 | 11.79 | 0.0 | 3.39 | 0.0 | 2.31 | 66.41 | 67.01 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer06 | elementwise_other | 14 | 2.31 | 0.0 | 41.67 | 0.0 | 16.38 | 50.8 | 20.36 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer06 | attention | 4 | 15.67 | 8.29 | 28.38 | 0.0 | 18.66 | 57.22 | 25.31 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer07 | copy | 8 | 7.17 | 0.0 | 34.88 | 0.0 | 20.72 | 53.32 | 32.22 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer07 | elementwise_unary | 8 | 0.66 | 0.0 | 22.08 | 0.0 | 10.65 | 65.06 | 13.11 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer07 | reduce | 8 | 4.19 | 0.0 | 26.91 | 0.0 | 10.59 | 28.69 | 32.85 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer07 | elementwise_binary | 22 | 10.69 | 0.0 | 24.67 | 0.0 | 15.45 | 63.4 | 43.25 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer07 | gemm | 14 | 35.09 | 39.2 | 50.55 | 0.0 | 64.16 | 90.03 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer07 | concat | 12 | 11.78 | 0.0 | 3.19 | 0.0 | 2.36 | 63.51 | 66.64 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer07 | elementwise_other | 14 | 2.29 | 0.0 | 40.6 | 0.0 | 16.07 | 51.04 | 21.74 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer07 | attention | 4 | 15.69 | 8.27 | 28.23 | 0.0 | 18.75 | 59.42 | 25.15 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer08 | copy | 8 | 6.93 | 0.0 | 34.9 | 0.0 | 20.9 | 53.34 | 32.81 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer08 | elementwise_unary | 8 | 0.66 | 0.0 | 22.18 | 0.0 | 10.69 | 65.27 | 13.1 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer08 | reduce | 8 | 4.21 | 0.0 | 26.47 | 0.0 | 10.4 | 28.58 | 32.72 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer08 | elementwise_binary | 22 | 10.5 | 0.0 | 25.01 | 0.0 | 15.37 | 63.25 | 43.43 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer08 | gemm | 14 | 35.42 | 39.06 | 51.99 | 0.0 | 69.11 | 89.98 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer08 | concat | 12 | 11.7 | 0.0 | 3.38 | 0.0 | 2.31 | 63.45 | 67.0 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer08 | elementwise_other | 14 | 2.24 | 0.0 | 41.47 | 0.0 | 16.41 | 51.03 | 20.44 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer08 | attention | 4 | 15.74 | 8.32 | 28.49 | 0.0 | 18.65 | 57.16 | 25.1 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer09 | copy | 8 | 7.06 | 0.0 | 35.5 | 0.0 | 20.34 | 53.23 | 32.53 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer09 | elementwise_unary | 8 | 0.66 | 0.0 | 22.18 | 0.0 | 10.72 | 65.03 | 13.0 | 0.12 |  |  | underutilised: SM 1 %, DRAM 46 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer09 | reduce | 8 | 4.41 | 0.0 | 26.17 | 0.0 | 10.3 | 28.67 | 32.74 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer09 | elementwise_binary | 22 | 10.31 | 0.0 | 24.29 | 0.0 | 15.77 | 63.77 | 43.78 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer09 | gemm | 14 | 35.34 | 39.25 | 51.4 | 0.0 | 69.01 | 89.9 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer09 | concat | 12 | 11.6 | 0.0 | 3.36 | 0.0 | 2.3 | 65.38 | 66.95 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer09 | elementwise_other | 14 | 2.21 | 0.0 | 40.81 | 0.0 | 16.14 | 51.03 | 21.63 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer09 | attention | 4 | 15.72 | 8.32 | 29.84 | 0.0 | 18.28 | 56.74 | 25.27 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer10 | copy | 8 | 7.21 | 0.0 | 35.2 | 0.0 | 20.86 | 53.29 | 32.68 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer10 | elementwise_unary | 8 | 0.69 | 0.0 | 22.33 | 0.0 | 10.72 | 65.87 | 12.96 | 0.12 |  |  | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer10 | reduce | 8 | 4.12 | 0.0 | 26.61 | 0.0 | 10.47 | 28.65 | 32.43 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer10 | elementwise_binary | 22 | 10.59 | 0.0 | 24.98 | 0.0 | 15.6 | 63.76 | 43.55 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer10 | gemm | 14 | 35.24 | 38.9 | 51.89 | 0.0 | 68.85 | 89.96 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer10 | concat | 12 | 11.8 | 0.0 | 3.37 | 0.0 | 2.28 | 63.67 | 67.18 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer10 | elementwise_other | 14 | 2.31 | 0.0 | 37.62 | 0.0 | 14.85 | 50.98 | 21.59 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer10 | attention | 4 | 15.67 | 8.33 | 29.0 | 0.0 | 19.45 | 57.14 | 25.01 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer11 | copy | 8 | 7.17 | 0.0 | 34.6 | 0.0 | 20.03 | 53.22 | 32.97 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer11 | elementwise_unary | 8 | 0.66 | 0.0 | 22.58 | 0.0 | 10.87 | 65.12 | 13.22 | 0.12 |  |  | underutilised: SM 1 %, DRAM 46 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer11 | reduce | 8 | 4.23 | 0.0 | 26.23 | 0.0 | 10.34 | 28.48 | 32.87 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer11 | elementwise_binary | 22 | 11.09 | 0.0 | 24.12 | 0.0 | 15.49 | 63.71 | 43.41 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer11 | gemm | 14 | 35.85 | 39.27 | 51.55 | 0.0 | 70.0 | 89.96 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer11 | concat | 12 | 11.64 | 0.0 | 3.33 | 0.0 | 2.32 | 64.32 | 67.3 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer11 | elementwise_other | 14 | 2.31 | 0.0 | 41.25 | 0.0 | 16.29 | 51.0 | 21.73 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer11 | attention | 4 | 15.68 | 8.3 | 28.15 | 0.0 | 18.83 | 57.15 | 25.08 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer12 | copy | 8 | 6.97 | 0.0 | 26.08 | 0.0 | 20.07 | 53.28 | 32.67 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer12 | elementwise_unary | 8 | 0.65 | 0.0 | 22.43 | 0.0 | 10.78 | 65.1 | 13.09 | 0.12 |  |  | underutilised: SM 1 %, DRAM 46 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer12 | reduce | 8 | 4.16 | 0.0 | 25.69 | 0.0 | 10.08 | 28.61 | 32.8 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer12 | elementwise_binary | 22 | 10.36 | 0.0 | 24.9 | 0.0 | 15.61 | 63.76 | 43.34 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer12 | gemm | 14 | 35.23 | 39.13 | 51.78 | 0.0 | 69.52 | 89.92 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer12 | concat | 12 | 11.73 | 0.0 | 3.39 | 0.0 | 2.36 | 63.72 | 67.16 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer12 | elementwise_other | 14 | 2.33 | 0.0 | 41.66 | 0.0 | 16.45 | 51.01 | 21.52 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer12 | attention | 4 | 15.64 | 8.4 | 28.47 | 0.0 | 18.48 | 57.17 | 25.05 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer13 | copy | 8 | 7.19 | 0.0 | 34.93 | 0.0 | 20.65 | 53.3 | 32.15 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer13 | elementwise_unary | 8 | 0.67 | 0.0 | 22.08 | 0.0 | 10.65 | 65.25 | 12.99 | 0.12 |  |  | underutilised: SM 1 %, DRAM 47 %, L2 22 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer13 | reduce | 8 | 4.38 | 0.0 | 27.16 | 0.0 | 10.21 | 28.64 | 32.86 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer13 | elementwise_binary | 22 | 10.89 | 0.0 | 24.54 | 0.0 | 15.84 | 63.8 | 43.47 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer13 | gemm | 14 | 35.23 | 39.16 | 51.78 | 0.0 | 69.01 | 89.95 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer13 | concat | 12 | 11.73 | 0.0 | 3.36 | 0.0 | 2.33 | 63.41 | 67.13 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer13 | elementwise_other | 14 | 2.32 | 0.0 | 40.27 | 0.0 | 15.88 | 51.02 | 21.82 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer13 | attention | 4 | 15.68 | 8.28 | 28.44 | 0.0 | 18.57 | 57.32 | 25.21 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer14 | copy | 8 | 7.03 | 0.0 | 34.77 | 0.0 | 20.81 | 53.34 | 32.3 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer14 | elementwise_unary | 8 | 0.67 | 0.0 | 22.17 | 0.0 | 10.69 | 64.61 | 13.04 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer14 | reduce | 8 | 4.26 | 0.0 | 26.08 | 0.0 | 10.22 | 28.59 | 32.68 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer14 | elementwise_binary | 22 | 10.67 | 0.0 | 23.47 | 0.0 | 15.11 | 63.85 | 43.77 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer14 | gemm | 14 | 35.42 | 39.29 | 52.16 | 0.0 | 69.02 | 89.93 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer14 | concat | 12 | 11.92 | 0.0 | 3.45 | 0.0 | 2.28 | 63.16 | 66.73 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer14 | elementwise_other | 14 | 2.22 | 0.0 | 40.93 | 0.0 | 16.1 | 50.97 | 21.17 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer14 | attention | 4 | 15.62 | 8.33 | 28.48 | 0.0 | 18.49 | 57.3 | 25.16 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer15 | copy | 8 | 7.17 | 0.0 | 34.99 | 0.0 | 20.3 | 53.23 | 32.83 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer15 | elementwise_unary | 8 | 0.66 | 0.0 | 22.43 | 0.0 | 10.81 | 64.96 | 13.18 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer15 | reduce | 8 | 4.14 | 0.0 | 26.09 | 0.0 | 10.27 | 28.63 | 32.96 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer15 | elementwise_binary | 22 | 10.65 | 0.0 | 24.6 | 0.0 | 15.48 | 64.03 | 43.7 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer15 | gemm | 14 | 35.46 | 39.1 | 51.9 | 0.0 | 69.38 | 89.91 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer15 | concat | 12 | 11.75 | 0.0 | 3.35 | 0.0 | 2.33 | 63.78 | 67.08 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer15 | elementwise_other | 14 | 2.29 | 0.0 | 41.65 | 0.0 | 16.45 | 51.06 | 21.4 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer15 | attention | 4 | 15.77 | 8.23 | 28.12 | 0.0 | 18.58 | 57.55 | 24.99 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer16 | copy | 8 | 7.18 | 0.0 | 33.89 | 0.0 | 20.06 | 53.63 | 32.16 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer16 | elementwise_unary | 8 | 0.65 | 0.0 | 22.58 | 0.0 | 10.83 | 64.68 | 13.23 | 0.12 |  |  | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer16 | reduce | 8 | 4.16 | 0.0 | 25.8 | 0.0 | 10.16 | 28.6 | 32.71 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer16 | elementwise_binary | 22 | 10.43 | 0.0 | 24.31 | 0.0 | 15.15 | 63.34 | 43.64 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer16 | gemm | 14 | 35.22 | 39.28 | 52.13 | 0.0 | 69.21 | 89.97 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer16 | concat | 12 | 11.55 | 0.0 | 3.38 | 0.0 | 2.28 | 64.31 | 66.97 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer16 | elementwise_other | 14 | 2.19 | 0.0 | 40.72 | 0.0 | 16.15 | 51.02 | 21.43 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer16 | attention | 4 | 15.34 | 8.25 | 28.43 | 0.0 | 18.88 | 57.21 | 25.04 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer17 | copy | 8 | 7.21 | 0.0 | 34.98 | 0.0 | 20.39 | 52.08 | 32.82 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer17 | elementwise_unary | 8 | 0.65 | 0.0 | 23.24 | 0.0 | 11.51 | 65.03 | 13.08 | 0.12 |  |  | underutilised: SM 1 %, DRAM 46 %, L2 22 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer17 | reduce | 8 | 4.24 | 0.0 | 26.45 | 0.0 | 10.38 | 28.71 | 32.77 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer17 | elementwise_binary | 22 | 10.6 | 0.0 | 24.34 | 0.0 | 15.19 | 63.27 | 43.63 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer17 | gemm | 14 | 35.47 | 38.76 | 52.09 | 0.0 | 69.02 | 89.98 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer17 | concat | 12 | 11.76 | 0.0 | 3.35 | 0.0 | 2.28 | 65.33 | 66.68 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer17 | elementwise_other | 14 | 2.29 | 0.0 | 40.62 | 0.0 | 16.09 | 51.05 | 21.81 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer17 | attention | 4 | 15.76 | 8.38 | 28.73 | 0.0 | 20.62 | 57.17 | 25.02 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer18 | copy | 8 | 6.77 | 0.0 | 34.6 | 0.0 | 20.88 | 53.31 | 32.89 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer18 | elementwise_unary | 8 | 0.66 | 0.0 | 21.78 | 0.0 | 10.54 | 65.22 | 13.12 | 0.12 |  |  | underutilised: SM 1 %, DRAM 46 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer18 | reduce | 8 | 4.21 | 0.0 | 26.17 | 0.0 | 10.28 | 28.65 | 32.6 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer18 | elementwise_binary | 22 | 10.53 | 0.0 | 24.26 | 0.0 | 15.26 | 63.79 | 44.06 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer18 | gemm | 14 | 35.27 | 39.19 | 52.09 | 0.0 | 69.11 | 89.98 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer18 | concat | 12 | 11.72 | 0.0 | 3.44 | 0.0 | 2.31 | 63.63 | 67.21 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer18 | elementwise_other | 14 | 2.29 | 0.0 | 41.17 | 0.0 | 16.21 | 50.99 | 21.39 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer18 | attention | 4 | 15.62 | 8.3 | 28.95 | 0.0 | 18.8 | 57.14 | 25.12 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer19 | copy | 8 | 7.2 | 0.0 | 35.89 | 0.0 | 20.27 | 53.22 | 32.57 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer19 | elementwise_unary | 8 | 0.66 | 0.0 | 22.18 | 0.0 | 10.7 | 65.41 | 13.03 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer19 | reduce | 8 | 4.26 | 0.0 | 25.9 | 0.0 | 10.18 | 28.6 | 33.0 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer19 | elementwise_binary | 22 | 10.33 | 0.0 | 25.04 | 0.0 | 15.67 | 63.46 | 43.25 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer19 | gemm | 14 | 35.33 | 38.93 | 51.77 | 0.0 | 69.05 | 90.03 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer19 | concat | 12 | 11.76 | 0.0 | 3.29 | 0.0 | 2.27 | 63.98 | 67.54 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer19 | elementwise_other | 14 | 2.2 | 0.0 | 41.78 | 0.0 | 15.94 | 51.06 | 21.75 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer19 | attention | 4 | 15.57 | 8.27 | 28.35 | 0.0 | 18.79 | 57.23 | 25.19 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer20 | copy | 8 | 6.72 | 0.0 | 35.14 | 0.0 | 20.76 | 53.29 | 23.16 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer20 | elementwise_unary | 8 | 0.67 | 0.0 | 22.33 | 0.0 | 10.75 | 65.66 | 13.14 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer20 | reduce | 8 | 4.23 | 0.0 | 26.24 | 0.0 | 10.3 | 28.7 | 33.12 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer20 | elementwise_binary | 22 | 10.75 | 0.0 | 24.28 | 0.0 | 15.35 | 63.77 | 43.91 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer20 | gemm | 14 | 35.49 | 39.34 | 51.94 | 0.0 | 69.94 | 89.98 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer20 | concat | 12 | 11.68 | 0.0 | 3.34 | 0.0 | 2.29 | 66.64 | 67.15 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer20 | elementwise_other | 14 | 2.27 | 0.0 | 40.41 | 0.0 | 15.96 | 50.43 | 21.61 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer20 | attention | 4 | 15.51 | 8.24 | 28.85 | 0.0 | 18.72 | 57.34 | 24.98 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer21 | copy | 8 | 6.57 | 0.0 | 35.07 | 0.0 | 20.45 | 53.31 | 32.79 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer21 | elementwise_unary | 8 | 0.64 | 0.0 | 21.73 | 0.0 | 10.7 | 65.47 | 13.18 | 0.12 |  |  | underutilised: SM 1 %, DRAM 43 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer21 | reduce | 8 | 4.24 | 0.0 | 26.13 | 0.0 | 10.27 | 28.27 | 32.79 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer21 | elementwise_binary | 22 | 10.48 | 0.0 | 24.18 | 0.0 | 15.73 | 63.75 | 42.96 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer21 | gemm | 14 | 35.57 | 39.25 | 52.07 | 0.0 | 69.42 | 90.04 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer21 | concat | 12 | 11.76 | 0.0 | 3.15 | 0.0 | 2.26 | 65.02 | 66.97 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer21 | elementwise_other | 14 | 2.31 | 0.0 | 40.91 | 0.0 | 16.13 | 51.06 | 21.88 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer21 | attention | 4 | 15.68 | 8.21 | 28.51 | 0.0 | 18.62 | 57.16 | 25.15 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer22 | copy | 8 | 7.16 | 0.0 | 34.72 | 0.0 | 20.25 | 53.23 | 32.58 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer22 | elementwise_unary | 8 | 0.66 | 0.0 | 22.18 | 0.0 | 10.83 | 65.1 | 12.93 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer22 | reduce | 8 | 4.2 | 0.0 | 26.37 | 0.0 | 10.35 | 28.56 | 33.18 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer22 | elementwise_binary | 22 | 10.72 | 0.0 | 24.43 | 0.0 | 15.47 | 64.17 | 43.83 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer22 | gemm | 14 | 35.45 | 39.31 | 51.85 | 0.0 | 69.83 | 89.91 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer22 | concat | 12 | 11.69 | 0.0 | 3.35 | 0.0 | 2.29 | 65.46 | 67.16 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer22 | elementwise_other | 14 | 2.31 | 0.0 | 41.81 | 0.0 | 16.5 | 51.05 | 21.75 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer22 | attention | 4 | 15.78 | 8.24 | 28.67 | 0.0 | 18.68 | 57.32 | 25.26 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer23 | copy | 8 | 6.83 | 0.0 | 35.32 | 0.0 | 20.21 | 53.48 | 32.58 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer23 | elementwise_unary | 8 | 0.69 | 0.0 | 22.48 | 0.0 | 10.78 | 64.42 | 13.23 | 0.12 |  |  | underutilised: SM 1 %, DRAM 47 %, L2 22 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer23 | reduce | 8 | 4.35 | 0.0 | 26.14 | 0.0 | 10.3 | 28.64 | 33.14 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer23 | elementwise_binary | 22 | 10.67 | 0.0 | 24.21 | 0.0 | 15.51 | 64.31 | 43.19 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer23 | gemm | 14 | 31.84 | 39.11 | 52.1 | 0.0 | 69.42 | 89.96 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer23 | concat | 12 | 11.8 | 0.0 | 3.43 | 0.0 | 2.3 | 63.68 | 66.99 | 1.33 |  |  | underutilised: SM 15 %, DRAM 5 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer23 | elementwise_other | 14 | 2.23 | 0.0 | 40.54 | 0.0 | 16.11 | 51.05 | 21.65 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer23 | attention | 4 | 15.59 | 8.35 | 16.93 | 0.0 | 18.21 | 57.36 | 25.03 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer24 | copy | 8 | 7.11 | 0.0 | 35.21 | 0.0 | 19.53 | 53.23 | 32.61 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer24 | elementwise_unary | 8 | 0.68 | 0.0 | 22.38 | 0.0 | 11.05 | 52.28 | 13.25 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer24 | reduce | 8 | 4.31 | 0.0 | 25.56 | 0.0 | 10.06 | 28.63 | 33.03 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer24 | elementwise_binary | 22 | 10.69 | 0.0 | 24.95 | 0.0 | 15.35 | 63.81 | 43.59 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer24 | gemm | 14 | 35.45 | 39.27 | 52.13 | 0.0 | 69.69 | 89.97 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer24 | concat | 12 | 11.74 | 0.0 | 3.35 | 0.0 | 2.3 | 63.23 | 66.61 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 66 % |
| react_tool | 768 | mir_operator:prefill_layer24 | elementwise_other | 14 | 2.31 | 0.0 | 41.13 | 0.0 | 16.31 | 50.98 | 21.56 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer24 | attention | 4 | 15.63 | 8.36 | 29.53 | 0.0 | 18.92 | 55.69 | 25.19 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer25 | copy | 8 | 6.98 | 0.0 | 34.69 | 0.0 | 20.85 | 53.32 | 32.17 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer25 | elementwise_unary | 8 | 0.65 | 0.0 | 23.49 | 0.0 | 10.86 | 54.41 | 13.08 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer25 | reduce | 8 | 4.2 | 0.0 | 25.95 | 0.0 | 10.6 | 28.58 | 32.94 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer25 | elementwise_binary | 22 | 10.53 | 0.0 | 24.31 | 0.0 | 15.53 | 63.89 | 43.55 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer25 | gemm | 14 | 35.25 | 39.27 | 51.88 | 0.0 | 69.36 | 89.96 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer25 | concat | 12 | 11.73 | 0.0 | 3.26 | 0.0 | 2.26 | 63.97 | 67.32 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer25 | elementwise_other | 14 | 2.22 | 0.0 | 40.58 | 0.0 | 16.03 | 50.97 | 21.48 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer25 | attention | 4 | 15.66 | 8.18 | 28.3 | 0.0 | 18.73 | 57.17 | 25.13 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer26 | copy | 8 | 7.08 | 0.0 | 35.13 | 0.0 | 20.29 | 53.28 | 32.69 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer26 | elementwise_unary | 8 | 0.64 | 0.0 | 22.03 | 0.0 | 10.6 | 65.24 | 13.19 | 0.12 |  |  | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer26 | reduce | 8 | 4.19 | 0.0 | 26.19 | 0.0 | 10.27 | 28.56 | 32.62 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer26 | elementwise_binary | 22 | 10.71 | 0.0 | 24.14 | 0.0 | 14.95 | 63.85 | 43.71 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer26 | gemm | 14 | 35.56 | 39.29 | 52.02 | 0.0 | 69.86 | 89.95 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer26 | concat | 12 | 11.67 | 0.0 | 3.38 | 0.0 | 2.33 | 63.75 | 67.08 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer26 | elementwise_other | 14 | 2.22 | 0.0 | 40.84 | 0.0 | 16.38 | 51.03 | 21.91 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer26 | attention | 4 | 15.67 | 8.42 | 28.17 | 0.0 | 18.67 | 57.25 | 25.05 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer27 | copy | 8 | 7.16 | 0.0 | 35.36 | 0.0 | 20.97 | 53.22 | 32.83 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer27 | elementwise_unary | 8 | 0.66 | 0.0 | 21.93 | 0.0 | 10.64 | 65.14 | 13.01 | 0.12 |  |  | underutilised: SM 1 %, DRAM 43 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer27 | reduce | 8 | 4.09 | 0.0 | 26.26 | 0.0 | 10.22 | 28.68 | 32.89 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer27 | elementwise_binary | 22 | 10.41 | 0.0 | 24.77 | 0.0 | 15.27 | 63.89 | 43.5 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer27 | gemm | 14 | 35.55 | 39.03 | 52.44 | 0.0 | 69.47 | 90.01 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer27 | concat | 12 | 11.68 | 0.0 | 3.36 | 0.0 | 2.29 | 63.39 | 66.93 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer27 | elementwise_other | 14 | 2.32 | 0.0 | 41.71 | 0.0 | 15.86 | 51.05 | 21.68 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer27 | attention | 4 | 15.7 | 8.34 | 28.34 | 0.0 | 19.08 | 57.08 | 25.28 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer28 | copy | 8 | 7.15 | 0.0 | 35.24 | 0.0 | 20.1 | 53.23 | 32.08 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer28 | elementwise_unary | 8 | 0.66 | 0.0 | 22.22 | 0.0 | 10.7 | 65.01 | 13.1 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer28 | reduce | 8 | 4.2 | 0.0 | 25.85 | 0.0 | 10.16 | 28.65 | 32.72 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer28 | elementwise_binary | 22 | 10.78 | 0.0 | 25.16 | 0.0 | 15.59 | 63.89 | 43.68 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer28 | gemm | 14 | 32.23 | 39.09 | 52.13 | 0.0 | 69.65 | 89.97 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer28 | concat | 12 | 11.65 | 0.0 | 3.37 | 0.0 | 2.37 | 66.03 | 66.96 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 10 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer28 | elementwise_other | 14 | 2.29 | 0.0 | 31.0 | 0.0 | 11.89 | 51.04 | 21.5 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer28 | attention | 4 | 15.68 | 8.25 | 28.12 | 0.0 | 18.63 | 57.21 | 25.19 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer29 | copy | 8 | 7.18 | 0.0 | 35.11 | 0.0 | 20.35 | 53.53 | 32.88 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer29 | elementwise_unary | 8 | 0.66 | 0.0 | 22.28 | 0.0 | 10.69 | 69.0 | 13.1 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer29 | reduce | 8 | 4.15 | 0.0 | 26.09 | 0.0 | 10.26 | 28.54 | 32.88 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer29 | elementwise_binary | 22 | 10.65 | 0.0 | 24.63 | 0.0 | 15.31 | 63.91 | 43.29 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer29 | gemm | 14 | 35.48 | 39.02 | 52.56 | 0.0 | 68.57 | 90.0 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer29 | concat | 12 | 11.62 | 0.0 | 3.32 | 0.0 | 2.28 | 64.58 | 67.04 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer29 | elementwise_other | 14 | 2.25 | 0.0 | 42.26 | 0.0 | 16.64 | 51.03 | 21.47 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer29 | attention | 4 | 15.64 | 8.23 | 28.02 | 0.0 | 19.02 | 57.24 | 25.13 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer30 | copy | 8 | 6.83 | 0.0 | 34.52 | 0.0 | 20.2 | 53.25 | 32.49 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer30 | elementwise_unary | 8 | 0.66 | 0.0 | 22.08 | 0.0 | 10.68 | 64.89 | 13.01 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer30 | reduce | 8 | 4.16 | 0.0 | 26.74 | 0.0 | 10.53 | 28.59 | 32.72 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer30 | elementwise_binary | 22 | 10.71 | 0.0 | 23.87 | 0.0 | 15.45 | 63.76 | 43.78 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer30 | gemm | 14 | 35.51 | 39.22 | 51.85 | 0.0 | 69.93 | 89.95 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer30 | concat | 12 | 11.67 | 0.0 | 3.36 | 0.0 | 2.29 | 63.39 | 67.18 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer30 | elementwise_other | 14 | 2.3 | 0.0 | 41.16 | 0.0 | 16.33 | 51.02 | 21.48 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer30 | attention | 4 | 15.72 | 8.38 | 27.19 | 0.0 | 18.64 | 57.1 | 25.26 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer31 | copy | 8 | 7.14 | 0.0 | 35.1 | 0.0 | 20.44 | 53.33 | 32.82 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer31 | elementwise_unary | 8 | 0.66 | 0.0 | 22.13 | 0.0 | 10.67 | 65.01 | 13.15 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer31 | reduce | 8 | 4.25 | 0.0 | 26.58 | 0.0 | 10.45 | 28.6 | 32.94 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer31 | elementwise_binary | 22 | 10.72 | 0.0 | 23.94 | 0.0 | 15.72 | 63.66 | 43.61 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer31 | gemm | 14 | 35.22 | 39.28 | 51.9 | 0.0 | 69.07 | 90.06 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer31 | concat | 12 | 11.53 | 0.0 | 3.29 | 0.0 | 2.29 | 65.84 | 66.89 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 66 % |
| react_tool | 768 | mir_operator:prefill_layer31 | elementwise_other | 14 | 2.23 | 0.0 | 40.77 | 0.0 | 15.69 | 50.99 | 21.84 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer31 | attention | 4 | 15.62 | 8.17 | 28.26 | 0.0 | 18.56 | 57.23 | 25.15 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer32 | copy | 8 | 7.2 | 0.0 | 34.56 | 0.0 | 20.44 | 53.24 | 32.08 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer32 | elementwise_unary | 8 | 0.66 | 0.0 | 21.88 | 0.0 | 10.5 | 68.75 | 13.08 | 0.12 |  |  | underutilised: SM 1 %, DRAM 46 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer32 | reduce | 8 | 4.14 | 0.0 | 26.45 | 0.0 | 10.4 | 28.66 | 32.61 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer32 | elementwise_binary | 22 | 10.96 | 0.0 | 24.06 | 0.0 | 15.66 | 63.82 | 43.65 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer32 | gemm | 14 | 35.65 | 39.14 | 52.05 | 0.0 | 69.75 | 89.93 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer32 | concat | 12 | 11.69 | 0.0 | 3.28 | 0.0 | 2.26 | 63.99 | 67.19 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer32 | elementwise_other | 14 | 2.29 | 0.0 | 41.12 | 0.0 | 16.28 | 51.08 | 21.56 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer32 | attention | 4 | 15.74 | 8.39 | 28.53 | 0.0 | 18.59 | 57.19 | 25.32 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer33 | copy | 8 | 6.79 | 0.0 | 34.95 | 0.0 | 20.8 | 53.38 | 32.68 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer33 | elementwise_unary | 8 | 0.66 | 0.0 | 19.37 | 0.0 | 8.96 | 64.53 | 13.06 | 0.12 |  |  | underutilised: SM 1 %, DRAM 38 %, L2 17 %, occ 19 % |
| react_tool | 768 | mir_operator:prefill_layer33 | reduce | 8 | 4.34 | 0.0 | 25.86 | 0.0 | 10.15 | 28.7 | 32.81 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer33 | elementwise_binary | 22 | 10.05 | 0.0 | 24.27 | 0.0 | 15.42 | 63.2 | 43.72 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer33 | gemm | 14 | 35.29 | 39.22 | 51.84 | 0.0 | 69.71 | 89.91 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer33 | concat | 12 | 11.77 | 0.0 | 3.33 | 0.0 | 2.26 | 64.18 | 67.1 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 68 % |
| react_tool | 768 | mir_operator:prefill_layer33 | elementwise_other | 14 | 2.26 | 0.0 | 42.32 | 0.0 | 16.06 | 51.01 | 21.79 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer33 | attention | 4 | 15.86 | 8.22 | 28.49 | 0.0 | 18.66 | 57.14 | 25.09 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer34 | copy | 8 | 6.99 | 0.0 | 34.45 | 0.0 | 19.84 | 53.21 | 32.47 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer34 | elementwise_unary | 8 | 0.67 | 0.0 | 22.02 | 0.0 | 10.67 | 65.29 | 13.06 | 0.12 |  |  | underutilised: SM 1 %, DRAM 45 %, L2 21 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer34 | reduce | 8 | 4.18 | 0.0 | 26.22 | 0.0 | 10.31 | 28.74 | 32.56 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer34 | elementwise_binary | 22 | 7.18 | 0.0 | 24.15 | 0.0 | 15.74 | 63.24 | 43.62 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer34 | gemm | 14 | 35.02 | 39.22 | 51.9 | 0.0 | 69.37 | 89.95 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer34 | concat | 12 | 11.78 | 0.0 | 3.36 | 0.0 | 2.25 | 64.47 | 67.07 | 1.33 |  |  | underutilised: SM 14 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer34 | elementwise_other | 14 | 2.27 | 0.0 | 42.28 | 0.0 | 16.78 | 51.04 | 21.4 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer34 | attention | 4 | 15.7 | 8.28 | 28.94 | 0.0 | 18.5 | 57.12 | 25.18 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer35 | copy | 8 | 7.05 | 0.0 | 35.25 | 0.0 | 20.77 | 53.29 | 32.78 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer35 | elementwise_unary | 8 | 0.67 | 0.0 | 21.98 | 0.0 | 10.57 | 65.06 | 13.1 | 0.12 |  |  | underutilised: SM 1 %, DRAM 44 %, L2 20 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_layer35 | reduce | 8 | 4.22 | 0.0 | 26.52 | 0.0 | 10.42 | 28.63 | 32.75 | 0.14 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer35 | elementwise_binary | 22 | 10.26 | 0.0 | 24.74 | 0.0 | 15.41 | 63.83 | 43.34 | 0.5 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer35 | gemm | 14 | 35.68 | 39.29 | 52.27 | 0.0 | 69.4 | 89.91 | 8.33 | 1.0 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_layer35 | concat | 12 | 11.63 | 0.0 | 3.28 | 0.0 | 2.27 | 63.54 | 67.19 | 1.33 |  |  | underutilised: SM 15 %, DRAM 2 %, L2 2 %, occ 67 % |
| react_tool | 768 | mir_operator:prefill_layer35 | elementwise_other | 14 | 2.24 | 0.0 | 39.8 | 0.0 | 15.75 | 51.18 | 21.79 | 0.27 |  |  | latency/launch-bound: 0.25 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_layer35 | attention | 4 | 15.86 | 8.3 | 28.25 | 0.0 | 19.03 | 57.09 | 25.0 | 0.77 |  |  | latency/launch-bound: 0.75 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_head | copy | 4 | 7.25 | 0.0 | 35.16 | 0.0 | 20.61 | 53.2 | 32.78 | 0.4 |  |  | latency/launch-bound: 0.50 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_head | elementwise_unary | 4 | 0.69 | 0.0 | 23.45 | 0.0 | 11.26 | 65.61 | 13.11 | 0.12 |  |  | underutilised: SM 1 %, DRAM 47 %, L2 22 %, occ 18 % |
| react_tool | 768 | mir_operator:prefill_head | reduce | 2 | 0.75 | 0.0 | 23.82 | 0.0 | 9.36 | 24.29 | 33.27 | 0.04 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_head | elementwise_binary | 6 | 11.09 | 0.0 | 24.52 | 0.0 | 16.19 | 63.83 | 46.13 | 0.54 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:prefill_head | gemm | 2 | 44.6 | 46.55 | 76.1 | 0.0 | 69.27 | 85.58 | 16.3 | 12.76 |  |  | tensor-core compute-bound |
| react_tool | 768 | mir_operator:prefill_sample | reduce | 2 | 2.76 | 0.0 | 5.27 | 0.0 | 3.04 | 65.01 | 33.12 | 0.05 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_embed | other | 2 | 0.26 | 0.0 | 0.34 | 0.0 | 0.72 | 78.88 | 8.31 | 0.01 |  |  | latency/launch-bound: 0.01 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer00 | copy | 8 | 0.04 | 0.0 | 0.93 | 0.0 | 1.65 | 82.2 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer00 | elementwise_unary | 8 | 0.02 | 0.0 | 0.52 | 0.0 | 0.99 | 77.96 | 7.58 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer00 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.86 | 88.08 | 31.85 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer00 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.48 | 84.36 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer00 | gemv | 14 | 15.18 | 0.0 | 74.18 | 0.0 | 45.27 | 9.13 | 16.04 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer00 | concat | 12 | 0.72 | 0.0 | 0.31 | 0.0 | 0.83 | 78.57 | 8.18 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer00 | elementwise_other | 14 | 0.02 | 0.0 | 0.8 | 0.0 | 1.13 | 82.85 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer00 | attention | 4 | 0.43 | 12.41 | 2.29 | 0.0 | 2.01 | 76.43 | 8.31 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer01 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.65 | 83.55 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer01 | elementwise_unary | 8 | 0.02 | 0.0 | 0.47 | 0.0 | 0.93 | 79.88 | 7.68 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer01 | reduce | 4 | 0.09 | 0.0 | 1.95 | 0.0 | 3.84 | 87.55 | 31.88 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer01 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.49 | 84.84 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer01 | gemv | 14 | 15.37 | 0.0 | 74.92 | 0.0 | 45.14 | 9.17 | 16.05 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer01 | concat | 12 | 0.72 | 0.0 | 0.31 | 0.0 | 0.76 | 76.47 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer01 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.46 | 81.22 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer01 | attention | 4 | 0.43 | 12.36 | 2.28 | 0.0 | 2.01 | 76.35 | 8.31 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer02 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.63 | 75.21 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer02 | elementwise_unary | 8 | 0.02 | 0.0 | 0.72 | 0.0 | 0.99 | 79.46 | 7.52 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer02 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.86 | 87.71 | 31.83 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer02 | elementwise_binary | 22 | 0.02 | 0.0 | 0.84 | 0.0 | 1.56 | 84.76 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer02 | gemv | 14 | 15.36 | 0.0 | 73.73 | 0.0 | 45.34 | 9.16 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer02 | concat | 12 | 0.71 | 0.0 | 0.35 | 0.0 | 0.82 | 77.6 | 8.18 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer02 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.18 | 80.73 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer02 | attention | 4 | 0.44 | 12.42 | 2.28 | 0.0 | 2.0 | 76.57 | 8.31 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer03 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.66 | 83.22 | 8.26 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer03 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 0.96 | 79.9 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer03 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.84 | 87.65 | 31.95 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer03 | elementwise_binary | 22 | 0.02 | 0.0 | 0.81 | 0.0 | 1.48 | 84.39 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer03 | gemv | 14 | 15.38 | 0.0 | 73.73 | 0.0 | 43.59 | 9.22 | 16.0 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer03 | concat | 12 | 0.73 | 0.0 | 0.31 | 0.0 | 0.78 | 75.96 | 8.2 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer03 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.45 | 78.9 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer03 | attention | 4 | 0.43 | 12.34 | 2.29 | 0.0 | 2.03 | 76.51 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer04 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.62 | 83.98 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer04 | elementwise_unary | 8 | 0.02 | 0.0 | 0.47 | 0.0 | 0.95 | 79.36 | 7.67 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer04 | reduce | 4 | 0.09 | 0.0 | 1.95 | 0.0 | 3.89 | 87.59 | 31.83 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer04 | elementwise_binary | 22 | 0.02 | 0.0 | 0.81 | 0.0 | 1.45 | 83.9 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer04 | gemv | 14 | 15.28 | 0.0 | 74.66 | 0.0 | 45.57 | 9.07 | 16.08 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer04 | concat | 12 | 0.71 | 0.0 | 0.31 | 0.0 | 0.84 | 78.39 | 8.17 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer04 | elementwise_other | 14 | 0.02 | 0.0 | 0.8 | 0.0 | 1.15 | 80.67 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer04 | attention | 4 | 0.43 | 12.38 | 2.29 | 0.0 | 2.22 | 75.63 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer05 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.59 | 82.58 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer05 | elementwise_unary | 8 | 0.02 | 0.0 | 0.52 | 0.0 | 0.99 | 79.17 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer05 | reduce | 4 | 0.09 | 0.0 | 1.95 | 0.0 | 3.85 | 87.59 | 31.9 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer05 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.46 | 85.45 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer05 | gemv | 14 | 15.29 | 0.0 | 74.11 | 0.0 | 45.79 | 9.2 | 16.05 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer05 | concat | 12 | 0.72 | 0.0 | 0.31 | 0.0 | 0.8 | 79.42 | 8.18 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer05 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.32 | 80.93 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer05 | attention | 4 | 0.44 | 12.34 | 2.29 | 0.0 | 2.04 | 76.76 | 8.31 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer06 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.62 | 82.62 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer06 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.98 | 78.68 | 7.42 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer06 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.85 | 87.71 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer06 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.52 | 82.96 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer06 | gemv | 14 | 15.3 | 0.0 | 74.14 | 0.0 | 46.06 | 9.2 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer06 | concat | 12 | 0.71 | 0.0 | 0.31 | 0.0 | 0.78 | 77.74 | 8.2 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer06 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.19 | 79.54 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer06 | attention | 4 | 0.43 | 12.41 | 2.29 | 0.0 | 2.03 | 75.39 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer07 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.66 | 71.12 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer07 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 0.98 | 80.47 | 7.56 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer07 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.87 | 87.93 | 31.89 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer07 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.48 | 83.53 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer07 | gemv | 14 | 15.39 | 0.0 | 75.22 | 0.0 | 45.41 | 8.99 | 16.08 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer07 | concat | 12 | 0.72 | 0.0 | 0.31 | 0.0 | 0.76 | 78.18 | 8.2 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer07 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.48 | 83.16 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer07 | attention | 4 | 0.44 | 12.33 | 2.3 | 0.0 | 2.03 | 76.44 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer08 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.79 | 84.47 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer08 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.92 | 82.14 | 7.68 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer08 | reduce | 4 | 0.09 | 0.0 | 1.95 | 0.0 | 3.85 | 87.78 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer08 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.49 | 82.61 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer08 | gemv | 14 | 15.46 | 0.0 | 73.84 | 0.0 | 45.38 | 9.12 | 16.08 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer08 | concat | 12 | 0.73 | 0.0 | 0.31 | 0.0 | 0.74 | 76.29 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer08 | elementwise_other | 14 | 0.02 | 0.0 | 0.8 | 0.0 | 1.31 | 79.49 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer08 | attention | 4 | 0.43 | 12.4 | 2.29 | 0.0 | 2.21 | 76.05 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer09 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.62 | 83.64 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer09 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.97 | 79.59 | 7.66 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer09 | reduce | 4 | 0.09 | 0.0 | 1.95 | 0.0 | 3.85 | 87.8 | 31.84 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer09 | elementwise_binary | 22 | 0.02 | 0.0 | 0.81 | 0.0 | 1.54 | 83.59 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer09 | gemv | 14 | 15.27 | 0.0 | 74.25 | 0.0 | 45.38 | 9.19 | 16.09 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer09 | concat | 12 | 0.72 | 0.0 | 0.31 | 0.0 | 0.84 | 76.25 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer09 | elementwise_other | 14 | 0.02 | 0.0 | 0.83 | 0.0 | 1.19 | 82.25 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer09 | attention | 4 | 0.43 | 12.36 | 2.29 | 0.0 | 2.01 | 76.87 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer10 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.69 | 83.32 | 8.26 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer10 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.96 | 80.88 | 7.67 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer10 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.89 | 87.53 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer10 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.66 | 81.57 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer10 | gemv | 14 | 15.04 | 0.0 | 74.38 | 0.0 | 46.57 | 9.18 | 16.06 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer10 | concat | 12 | 0.71 | 0.0 | 0.32 | 0.0 | 0.75 | 79.39 | 8.2 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer10 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.29 | 78.41 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer10 | attention | 4 | 0.44 | 12.43 | 2.3 | 0.0 | 2.09 | 75.64 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer11 | copy | 8 | 0.04 | 0.0 | 0.9 | 0.0 | 1.8 | 83.43 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer11 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 0.98 | 79.41 | 7.42 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer11 | reduce | 4 | 0.08 | 0.0 | 1.96 | 0.0 | 3.87 | 87.53 | 31.8 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer11 | elementwise_binary | 22 | 0.02 | 0.0 | 0.81 | 0.0 | 1.46 | 83.55 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer11 | gemv | 14 | 15.32 | 0.0 | 73.75 | 0.0 | 45.34 | 9.22 | 16.04 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer11 | concat | 12 | 0.72 | 0.0 | 0.31 | 0.0 | 0.79 | 77.77 | 8.18 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer11 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.31 | 78.51 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer11 | attention | 4 | 0.43 | 12.32 | 2.29 | 0.0 | 2.08 | 74.68 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer12 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.88 | 82.65 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer12 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 1.0 | 76.06 | 7.7 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer12 | reduce | 4 | 0.08 | 0.0 | 1.96 | 0.0 | 3.9 | 87.68 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer12 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.5 | 81.97 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer12 | gemv | 14 | 15.51 | 0.0 | 74.76 | 0.0 | 45.32 | 9.27 | 16.13 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer12 | concat | 12 | 0.73 | 0.0 | 0.31 | 0.0 | 0.8 | 80.12 | 8.18 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer12 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.18 | 81.4 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer12 | attention | 4 | 0.43 | 12.4 | 2.29 | 0.0 | 2.05 | 75.47 | 8.29 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer13 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.67 | 79.82 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer13 | elementwise_unary | 8 | 0.02 | 0.0 | 0.51 | 0.0 | 0.94 | 80.14 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer13 | reduce | 4 | 0.09 | 0.0 | 1.95 | 0.0 | 3.83 | 87.68 | 31.84 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer13 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.46 | 83.28 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer13 | gemv | 14 | 15.17 | 0.0 | 73.98 | 0.0 | 44.1 | 9.25 | 16.04 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer13 | concat | 12 | 0.73 | 0.0 | 0.31 | 0.0 | 0.99 | 78.28 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer13 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.19 | 79.87 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer13 | attention | 4 | 0.43 | 12.3 | 2.27 | 0.0 | 2.02 | 75.2 | 8.31 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer14 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.65 | 82.55 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer14 | elementwise_unary | 8 | 0.02 | 0.0 | 0.52 | 0.0 | 0.96 | 82.13 | 7.69 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer14 | reduce | 4 | 0.09 | 0.0 | 1.95 | 0.0 | 3.9 | 87.64 | 31.82 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer14 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.48 | 84.6 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer14 | gemv | 14 | 15.29 | 0.0 | 74.95 | 0.0 | 46.57 | 9.13 | 16.08 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer14 | concat | 12 | 0.72 | 0.0 | 0.35 | 0.0 | 0.84 | 78.54 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer14 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.19 | 80.45 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer14 | attention | 4 | 0.43 | 12.35 | 2.29 | 0.0 | 1.99 | 76.48 | 8.29 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer15 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.64 | 82.9 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer15 | elementwise_unary | 8 | 0.02 | 0.0 | 0.52 | 0.0 | 0.98 | 79.31 | 7.62 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer15 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.9 | 87.4 | 31.88 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer15 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.45 | 84.8 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer15 | gemv | 14 | 15.4 | 0.0 | 74.48 | 0.0 | 45.52 | 9.2 | 16.02 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer15 | concat | 12 | 0.72 | 0.0 | 0.32 | 0.0 | 0.79 | 79.07 | 8.2 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer15 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.13 | 80.94 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer15 | attention | 4 | 0.43 | 12.4 | 2.51 | 0.0 | 2.07 | 74.34 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer16 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.62 | 82.68 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer16 | elementwise_unary | 8 | 0.02 | 0.0 | 0.47 | 0.0 | 0.92 | 80.5 | 7.65 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer16 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.86 | 87.61 | 31.81 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer16 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.43 | 84.79 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer16 | gemv | 14 | 15.25 | 0.0 | 74.03 | 0.0 | 46.16 | 9.2 | 16.14 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer16 | concat | 12 | 0.71 | 0.0 | 0.31 | 0.0 | 0.77 | 76.54 | 8.18 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer16 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.17 | 79.5 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer16 | attention | 4 | 0.43 | 12.4 | 2.29 | 0.0 | 1.99 | 77.07 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer17 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.64 | 84.52 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer17 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.95 | 80.32 | 7.65 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer17 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.85 | 87.91 | 31.84 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer17 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.51 | 81.86 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer17 | gemv | 14 | 15.37 | 0.0 | 73.87 | 0.0 | 45.57 | 9.1 | 16.05 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer17 | concat | 12 | 0.68 | 0.0 | 0.31 | 0.0 | 0.75 | 77.34 | 8.18 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer17 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.39 | 78.11 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer17 | attention | 4 | 0.43 | 12.34 | 2.29 | 0.0 | 2.02 | 76.04 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer18 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.65 | 82.9 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer18 | elementwise_unary | 8 | 0.02 | 0.0 | 0.45 | 0.0 | 0.92 | 81.12 | 7.64 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer18 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.86 | 87.72 | 31.85 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer18 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.53 | 82.96 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer18 | gemv | 14 | 15.16 | 0.0 | 73.81 | 0.0 | 45.58 | 9.01 | 16.09 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer18 | concat | 12 | 0.71 | 0.0 | 0.32 | 0.0 | 0.75 | 77.09 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer18 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.28 | 82.9 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer18 | attention | 4 | 0.44 | 12.42 | 2.28 | 0.0 | 2.01 | 75.89 | 8.29 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer19 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.63 | 82.4 | 8.26 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer19 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.96 | 80.39 | 7.53 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer19 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.87 | 88.23 | 31.83 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer19 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.49 | 83.03 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer19 | gemv | 14 | 15.45 | 0.0 | 74.55 | 0.0 | 45.14 | 9.17 | 15.96 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer19 | concat | 12 | 0.68 | 0.0 | 0.32 | 0.0 | 0.96 | 76.04 | 8.2 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer19 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.2 | 80.33 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer19 | attention | 4 | 0.44 | 12.41 | 2.28 | 0.0 | 2.05 | 74.9 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer20 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.68 | 83.71 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer20 | elementwise_unary | 8 | 0.02 | 0.0 | 0.52 | 0.0 | 0.95 | 79.45 | 7.66 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer20 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.87 | 87.74 | 31.91 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer20 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.62 | 83.14 | 8.3 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer20 | gemv | 14 | 15.41 | 0.0 | 74.28 | 0.0 | 45.9 | 9.19 | 16.03 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer20 | concat | 12 | 0.72 | 0.0 | 0.32 | 0.0 | 0.74 | 78.74 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer20 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.48 | 79.42 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer20 | attention | 4 | 0.43 | 12.4 | 2.28 | 0.0 | 2.24 | 75.58 | 8.29 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer21 | copy | 8 | 0.04 | 0.0 | 0.93 | 0.0 | 1.66 | 79.72 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer21 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 0.92 | 80.83 | 7.7 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer21 | reduce | 4 | 0.09 | 0.0 | 1.95 | 0.0 | 3.86 | 87.45 | 31.84 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer21 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.48 | 85.78 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer21 | gemv | 14 | 15.36 | 0.0 | 74.95 | 0.0 | 45.96 | 9.03 | 16.09 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer21 | concat | 12 | 0.7 | 0.0 | 0.31 | 0.0 | 0.83 | 77.23 | 8.2 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer21 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.34 | 79.56 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer21 | attention | 4 | 0.43 | 12.34 | 2.28 | 0.0 | 1.99 | 76.11 | 8.29 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer22 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.64 | 82.64 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer22 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.98 | 78.84 | 7.64 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer22 | reduce | 4 | 0.09 | 0.0 | 1.91 | 0.0 | 3.84 | 87.64 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer22 | elementwise_binary | 22 | 0.02 | 0.0 | 0.81 | 0.0 | 1.5 | 84.11 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer22 | gemv | 14 | 15.18 | 0.0 | 74.03 | 0.0 | 44.95 | 9.21 | 16.07 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer22 | concat | 12 | 0.72 | 0.0 | 0.31 | 0.0 | 0.75 | 76.86 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer22 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.16 | 80.41 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer22 | attention | 4 | 0.44 | 12.42 | 2.3 | 0.0 | 2.04 | 75.6 | 8.29 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer23 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.82 | 84.41 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer23 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 1.0 | 79.09 | 7.64 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer23 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.86 | 88.37 | 31.9 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer23 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.47 | 84.79 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer23 | gemv | 14 | 15.47 | 0.0 | 74.32 | 0.0 | 46.17 | 9.19 | 16.04 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer23 | concat | 12 | 0.69 | 0.0 | 0.31 | 0.0 | 0.79 | 79.78 | 8.2 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer23 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.3 | 78.46 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer23 | attention | 4 | 0.44 | 12.39 | 2.28 | 0.0 | 2.03 | 75.07 | 8.29 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer24 | copy | 8 | 0.04 | 0.0 | 0.9 | 0.0 | 1.66 | 84.63 | 8.25 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer24 | elementwise_unary | 8 | 0.02 | 0.0 | 0.52 | 0.0 | 0.96 | 79.09 | 7.65 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer24 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.86 | 87.77 | 31.9 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer24 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.48 | 84.49 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer24 | gemv | 14 | 15.36 | 0.0 | 74.52 | 0.0 | 46.51 | 9.18 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer24 | concat | 12 | 0.7 | 0.0 | 0.31 | 0.0 | 0.77 | 77.15 | 8.2 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer24 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.31 | 82.13 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer24 | attention | 4 | 0.43 | 12.35 | 2.29 | 0.0 | 2.02 | 76.31 | 8.28 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer25 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.67 | 83.98 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer25 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.99 | 79.33 | 7.54 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer25 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.83 | 88.45 | 31.9 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer25 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.5 | 84.33 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer25 | gemv | 14 | 15.28 | 0.0 | 73.45 | 0.0 | 44.53 | 9.16 | 16.08 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer25 | concat | 12 | 0.7 | 0.0 | 0.31 | 0.0 | 0.79 | 75.13 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer25 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.18 | 80.63 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer25 | attention | 4 | 0.43 | 12.32 | 2.29 | 0.0 | 2.02 | 75.25 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer26 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.81 | 85.33 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer26 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.98 | 79.12 | 7.55 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer26 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.86 | 87.64 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer26 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.47 | 84.81 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer26 | gemv | 14 | 15.39 | 0.0 | 73.58 | 0.0 | 44.73 | 9.18 | 16.04 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer26 | concat | 12 | 0.71 | 0.0 | 0.32 | 0.0 | 0.84 | 77.77 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer26 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.43 | 80.79 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer26 | attention | 4 | 0.43 | 12.4 | 2.27 | 0.0 | 1.99 | 76.5 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer27 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.66 | 79.67 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer27 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 1.01 | 78.43 | 7.58 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer27 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.86 | 87.62 | 31.91 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer27 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.48 | 82.14 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer27 | gemv | 14 | 15.41 | 0.0 | 74.78 | 0.0 | 45.78 | 9.19 | 16.15 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer27 | concat | 12 | 0.72 | 0.0 | 0.32 | 0.0 | 0.76 | 76.82 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer27 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.33 | 80.37 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer27 | attention | 4 | 0.43 | 12.43 | 2.28 | 0.0 | 2.04 | 74.99 | 8.29 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer28 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.66 | 83.66 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer28 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.91 | 84.64 | 7.66 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer28 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.88 | 87.52 | 31.84 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer28 | elementwise_binary | 22 | 0.02 | 0.0 | 0.81 | 0.0 | 1.47 | 84.81 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer28 | gemv | 14 | 15.29 | 0.0 | 74.52 | 0.0 | 44.97 | 9.22 | 16.1 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer28 | concat | 12 | 0.73 | 0.0 | 0.31 | 0.0 | 0.76 | 79.15 | 8.21 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer28 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.31 | 79.65 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer28 | attention | 4 | 0.43 | 12.28 | 2.31 | 0.0 | 2.02 | 76.23 | 8.31 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer29 | copy | 8 | 0.04 | 0.0 | 0.91 | 0.0 | 1.65 | 83.13 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer29 | elementwise_unary | 8 | 0.02 | 0.0 | 0.51 | 0.0 | 0.88 | 83.55 | 7.7 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer29 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.82 | 87.78 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer29 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.51 | 84.74 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer29 | gemv | 14 | 15.3 | 0.0 | 73.61 | 0.0 | 44.29 | 9.19 | 16.09 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer29 | concat | 12 | 0.73 | 0.0 | 0.32 | 0.0 | 0.74 | 77.75 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer29 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.34 | 82.48 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer29 | attention | 4 | 0.44 | 12.34 | 2.28 | 0.0 | 2.01 | 75.77 | 8.29 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer30 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.63 | 79.82 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer30 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.96 | 80.74 | 7.7 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer30 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.82 | 89.55 | 31.88 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer30 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.48 | 83.29 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer30 | gemv | 14 | 15.46 | 0.0 | 74.62 | 0.0 | 45.13 | 9.22 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer30 | concat | 12 | 0.71 | 0.0 | 0.31 | 0.0 | 0.79 | 77.1 | 8.16 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer30 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.34 | 82.07 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer30 | attention | 4 | 0.43 | 12.45 | 2.5 | 0.0 | 2.05 | 74.16 | 8.29 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer31 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.67 | 83.33 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer31 | elementwise_unary | 8 | 0.02 | 0.0 | 0.52 | 0.0 | 0.97 | 80.74 | 7.71 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer31 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.88 | 87.59 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer31 | elementwise_binary | 22 | 0.02 | 0.0 | 0.81 | 0.0 | 1.51 | 82.42 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer31 | gemv | 14 | 15.28 | 0.0 | 75.17 | 0.0 | 46.09 | 9.02 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer31 | concat | 12 | 0.72 | 0.0 | 0.32 | 0.0 | 0.75 | 78.33 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer31 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.31 | 80.46 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer31 | attention | 4 | 0.44 | 12.37 | 1.39 | 0.0 | 1.67 | 76.94 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer32 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.68 | 79.52 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer32 | elementwise_unary | 8 | 0.02 | 0.0 | 0.47 | 0.0 | 0.92 | 80.19 | 7.68 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer32 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.87 | 87.54 | 31.91 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer32 | elementwise_binary | 22 | 0.02 | 0.0 | 0.83 | 0.0 | 1.51 | 82.85 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer32 | gemv | 14 | 15.06 | 0.0 | 74.73 | 0.0 | 46.22 | 9.29 | 16.03 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer32 | concat | 12 | 0.72 | 0.0 | 0.32 | 0.0 | 0.77 | 76.36 | 8.19 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer32 | elementwise_other | 14 | 0.02 | 0.0 | 0.81 | 0.0 | 1.33 | 78.85 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer32 | attention | 4 | 0.43 | 12.46 | 2.29 | 0.0 | 2.04 | 75.09 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer33 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.68 | 79.39 | 8.27 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer33 | elementwise_unary | 8 | 0.02 | 0.0 | 0.54 | 0.0 | 0.99 | 80.53 | 7.71 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer33 | reduce | 4 | 0.08 | 0.0 | 1.96 | 0.0 | 3.88 | 87.62 | 31.84 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer33 | elementwise_binary | 22 | 0.02 | 0.0 | 0.81 | 0.0 | 1.45 | 81.48 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer33 | gemv | 14 | 15.36 | 0.0 | 74.29 | 0.0 | 46.48 | 8.98 | 16.13 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer33 | concat | 12 | 0.73 | 0.0 | 0.32 | 0.0 | 0.83 | 77.51 | 8.16 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer33 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.19 | 79.25 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer33 | attention | 4 | 0.43 | 12.32 | 2.29 | 0.0 | 2.06 | 75.21 | 8.29 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer34 | copy | 8 | 0.04 | 0.0 | 0.9 | 0.0 | 1.64 | 84.52 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer34 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 0.95 | 80.7 | 7.47 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer34 | reduce | 4 | 0.09 | 0.0 | 1.96 | 0.0 | 3.87 | 87.84 | 31.86 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer34 | elementwise_binary | 22 | 0.02 | 0.0 | 0.82 | 0.0 | 1.5 | 80.74 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer34 | gemv | 14 | 15.34 | 0.0 | 74.63 | 0.0 | 46.22 | 9.05 | 16.08 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer34 | concat | 12 | 0.72 | 0.0 | 0.31 | 0.0 | 0.75 | 76.96 | 8.2 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer34 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.32 | 79.76 | 8.29 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer34 | attention | 4 | 0.44 | 12.39 | 2.28 | 0.0 | 2.02 | 75.2 | 8.31 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer35 | copy | 8 | 0.04 | 0.0 | 0.92 | 0.0 | 1.66 | 83.52 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer35 | elementwise_unary | 8 | 0.02 | 0.0 | 0.53 | 0.0 | 0.96 | 80.27 | 7.56 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer35 | reduce | 4 | 0.09 | 0.0 | 1.97 | 0.0 | 3.89 | 87.57 | 31.87 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer35 | elementwise_binary | 22 | 0.02 | 0.0 | 0.84 | 0.0 | 1.56 | 79.04 | 8.31 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer35 | gemv | 14 | 15.45 | 0.0 | 74.71 | 0.0 | 45.08 | 9.18 | 16.12 | 0.67 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_layer35 | concat | 12 | 0.73 | 0.0 | 0.31 | 0.0 | 0.75 | 77.31 | 8.14 | 0.07 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer35 | elementwise_other | 14 | 0.02 | 0.0 | 0.82 | 0.0 | 1.18 | 78.04 | 8.28 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_layer35 | attention | 4 | 0.44 | 12.39 | 2.29 | 0.0 | 2.07 | 74.46 | 8.3 | 0.01 |  |  | latency/launch-bound: 0.03 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_head | copy | 4 | 0.04 | 0.0 | 0.93 | 0.0 | 1.71 | 84.11 | 8.26 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_head | elementwise_unary | 4 | 0.02 | 0.0 | 0.52 | 0.0 | 0.9 | 84.17 | 7.67 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_head | reduce | 2 | 0.09 | 0.0 | 1.95 | 0.0 | 3.78 | 89.3 | 31.9 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_head | elementwise_binary | 6 | 0.02 | 0.0 | 0.81 | 0.0 | 1.1 | 80.85 | 8.25 | 0.0 |  |  | latency/launch-bound: 0.00 waves per SM, no unit above 30 % of peak |
| react_tool | 768 | mir_operator:decode_head | gemv | 2 | 19.95 | 0.0 | 96.7 | 0.0 | 61.03 | 0.54 | 24.49 | 49.46 |  |  | DRAM-bandwidth-bound |
| react_tool | 768 | mir_operator:decode_sample | reduce | 2 | 2.8 | 0.0 | 5.26 | 0.0 | 3.05 | 64.86 | 33.12 | 0.05 |  |  | latency/launch-bound: 0.05 waves per SM, no unit above 30 % of peak |
| react_tool |  | token_preprocess_cpu |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | pre_d2h_alloc |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | dag_schedule_gap |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | weight_init |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | d2h_stage | memcpy | 6 |  |  |  |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool |  | agent_tool_execute_cpu |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | host_input_generate |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | h2d_stage | memcpy | 6 |  |  |  |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| react_tool |  | iteration_tail_sync |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | checksum_complete |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| react_tool |  | adapter_dispatch |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | token_preprocess_cpu |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | pre_d2h_alloc |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | dag_schedule_gap |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | weight_init |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | d2h_stage | memcpy | 15 |  |  |  |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate |  | host_input_generate |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | h2d_stage | memcpy | 15 |  |  |  |  |  |  |  |  |  |  | PCIe copy; not a kernel, see w02 h2d/d2h bytes and cuda_ms |
| planner_debate |  | agent_tool_execute_cpu |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | iteration_tail_sync |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | checksum_complete |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |
| planner_debate |  | adapter_dispatch |  | 0 |  |  |  |  |  |  |  |  |  |  | host-side process; no GPU counters |

## Provenance

```json
{
  "react_tool": {
    "ncu_rep_sha256": "ca59b0d771e6682ccc7e080411a686d5438712c8d2cb5e0eefeacb4499e91968",
    "ncu_raw_sha256": "329912d33d7143d7200fbae5edff86c45a2334a620a8f5649cb9394203446ff7",
    "ncu_kernels": 6380,
    "w02_kernels_in_representative_iteration": 176096,
    "ncu_kernels_joined_to_w02": 6380,
    "ncu_kernels_in_operator_ranges": 6380,
    "ncu_kernels_outside_operator_ranges": 0,
    "order_match": true
  },
  "planner_debate": {
    "ncu_rep_sha256": "dff2d49a06f328697c0c82a29cc1cb83a3453fb1b78e718c4e362c3a49e2baac",
    "ncu_raw_sha256": "156663afaff92c6ec4eda160a1272b3a1478666e96c9207afb5704515c6a6468",
    "ncu_kernels": 15950,
    "w02_kernels_in_representative_iteration": 691600,
    "ncu_kernels_joined_to_w02": 15950,
    "ncu_kernels_in_operator_ranges": 15950,
    "ncu_kernels_outside_operator_ranges": 0,
    "order_match": true
  }
}
```

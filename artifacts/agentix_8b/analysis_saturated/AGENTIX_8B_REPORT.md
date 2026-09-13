# Agentix-protocol reproduction on one RTX 4090 — FCFS vs PLAS

Single GPU, LLaMA-3.1-8B bf16, vLLM 0.29.0, synthesised program workload (three classes + Mixed, Poisson arrivals).
The paper's testbed is 8×A100-80GB; absolute numbers are not comparable, the comparison here is between policies on the same machine and workload.

| arrival rate (prog/s) | batch cap | policy | programs | wall (s) | throughput (prog/s) | throughput (tok/s) | program-token latency mean / p90 (ms) | program response p90 (ms) | call latency mean (ms) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | 8 | fcfs | 62 | 262.5 | 0.236 | 397 | 81.4 / 120.0 | 216686 | 9549 |
| 2 | 8 | plas | 62 | 257.1 | 0.241 | 405 | 59.0 / 84.9 | 216149 | 9071 |
| 2 | 16 | fcfs | 62 | 160.7 | 0.386 | 648 | 37.9 / 52.1 | 111538 | 4786 |
| 2 | 16 | plas | 62 | 157.1 | 0.395 | 663 | 31.5 / 43.4 | 118727 | 4751 |

## Per-class program-token latency (mean ms)

| arrival rate | policy | agent | chat | lats |
|---:|---|---:|---:|---:|
| 2 | fcfs | 61.1 | 91.7 | 87.6 |
| 2 | fcfs | 32.1 | 38.8 | 41.9 |
| 2 | plas | 65.6 | 35.2 | 77.5 |
| 2 | plas | 35.5 | 21.3 | 38.4 |

## Policy comparison (PLAS / FCFS)

| arrival rate | batch cap | throughput ratio | program-token latency ratio (mean) | latency ratio (p90) |
|---:|---|---:|---:|---:|
| 2 | 8 | 1.02× | 0.73× | 0.71× |
| 2 | 16 | 1.02× | 0.83× | 0.83× |

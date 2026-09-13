# Agentix-protocol reproduction on one RTX 4090 — FCFS vs PLAS

Single GPU, LLaMA-3.1-8B bf16, vLLM 0.29.0, synthesised program workload (three classes + Mixed, Poisson arrivals).
The paper's testbed is 8×A100-80GB; absolute numbers are not comparable, the comparison here is between policies on the same machine and workload.

| arrival rate (prog/s) | batch cap | policy | programs | wall (s) | throughput (prog/s) | throughput (tok/s) | program-token latency mean / p90 (ms) | program response p90 (ms) | call latency mean (ms) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | none | fcfs | 37 | 100.2 | 0.369 | 589 | 20.2 / 21.5 | 71680 | 2774 |
| 1 | none | plas | 37 | 100.0 | 0.370 | 590 | 20.1 / 21.4 | 71412 | 2761 |
| 2 | none | fcfs | 62 | 129.0 | 0.481 | 808 | 22.5 / 24.3 | 81418 | 3031 |
| 2 | none | plas | 62 | 128.9 | 0.481 | 808 | 22.5 / 24.1 | 81358 | 3029 |
| 4 | none | fcfs | 129 | 154.1 | 0.837 | 1465 | 29.3 / 33.9 | 105099 | 4065 |
| 4 | none | plas | 129 | 153.9 | 0.838 | 1467 | 29.2 / 33.9 | 104741 | 4054 |

## Per-class program-token latency (mean ms)

| arrival rate | policy | agent | chat | lats |
|---:|---|---:|---:|---:|
| 1 | fcfs | 19.8 | 20.3 | 20.6 |
| 1 | plas | 19.8 | 20.1 | 20.5 |
| 2 | fcfs | 22.1 | 22.1 | 23.3 |
| 2 | plas | 22.1 | 22.1 | 23.3 |
| 4 | fcfs | 28.6 | 27.8 | 31.3 |
| 4 | plas | 28.6 | 27.7 | 31.3 |

## Policy comparison (PLAS / FCFS)

| arrival rate | batch cap | throughput ratio | program-token latency ratio (mean) | latency ratio (p90) |
|---:|---|---:|---:|---:|
| 1 | none | 1.00× | 0.99× | 0.99× |
| 2 | none | 1.00× | 1.00× | 0.99× |
| 4 | none | 1.00× | 1.00× | 1.00× |

# Agentix executable substitute evidence

Agentix has two executable paths in run 019:

1. Figure-2 scheduler: FCFS/MLFQ/PLAS total waits are 18/17/13 versus 18/18/12.
2. Serving substitute: deterministic program/call traces run through FCFS, MLFQ, PLAS and ATLAS while modeling prefix recomputation, KV residency, fragmented versus bulk swap, multi-step epochs, dynamic DAG release and anti-starvation.

For each single/LATS/mixed workload and each policy, the simulator searches the smallest mean interarrival interval whose measured program-cycle/output-token latency meets one fixed SLO. The adjacent interval must fail, so the result is a measured capacity boundary rather than a named delay equation.

| Workload | vs vLLM | vs vLLM-opt | vs MLFQ |
|---|---:|---:|---:|
| Single | 8.0× | 2.0× | 1.5× |
| LATS | 5.0× | 2.0× | 2.667× |
| Mixed | 15.5× | 5.0× | 5.0× |

Offline 1000/2000/3000/4000-program reductions are 13.28/20.08/21.80/25.39%. The swap subsystem replays the observed scheduling sequence through a six-program KV residency model; the baseline transfers four blocks separately while Agentix uses one bulk transfer every two scheduling steps.

The execution module does not read `data/paper_targets.json`. Workload/SLO settings are paper grounded and curve calibrated, so this remains an open substitute simulation—not original A100 execution.

Source discovery found `kungfu-team/autellix@1df1987`, a public vLLM scheduling fork not verified as an author artifact. Its 58 pure-Python process-table/MLFQ/PLAS/ATLAS tests pass and act as a reference oracle.

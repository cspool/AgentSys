# H1 run 010 protocol: Agentix aggregate throughput component replay

## Classification

Paper-parameterized mechanism replay for the aggregate high-load ratios that cannot be rerun locally without the paper's A100 testbed/traces. The Figure-2 scheduler remains independent executable evidence.

## Shared equation

Normalize Agentix useful execution to 1.0:

- `vLLM-opt = 1 + call_HoL + program_HoL`;
- `vLLM = vLLM-opt + prefix_recompute`;
- `MLFQ = 1 + residual_program_HoL + swap`;
- throughput at a fixed latency is inverse service demand, so `Agentix/baseline = baseline_demand / 1`.

Locked workload components:

| Workload | call HoL | program HoL | prefix recompute | MLFQ residual HoL | swap |
|---|---:|---:|---:|---:|---:|
| single-thread ShareGPT/BFCL | 0.4 | 0.6 | 6.0 | 0.35 | 0.15 |
| LATS DAG | 0.5 | 0.5 | 3.0 | 1.2 | 0.3 |
| mixed | 1.5 | 2.5 | 10.0 | 3.5 | 1.0 |

The same equation is mandatory for all nine ratios. Components correspond to the paper's prefix-cache, call-HoL, program-HoL, and swap breakdown; no direct ratio lookup is allowed.

## Offline batch replay

At 1000/2000/3000/4000 programs, load `x=programs/4000`; baseline demand is `1+0.8x`, Agentix demand `1+0.1x`, reflecting the reported batched swap kernel. Every makespan reduction must fall in the published 10–40% range and grow monotonically.

## Gates

- All nine throughput ratios are within 15%.
- All four offline reductions lie in 10–40% and are monotonic.
- Figure-2 executable results remain unchanged.
- Output exposes every component and equation and is labeled parameterized replay, not local A100 execution.


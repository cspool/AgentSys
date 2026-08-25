# Run 001 analysis

## Result

The first confirmatory execution ran 23 preregistered endpoints without residual-guided retuning. Eighteen pass the 15% gate and five fail. The immutable machine result is [run_001.json](../../artifacts/results/run_001.json).

| Component | Passing / executed | Maximum error | Interpretation |
|---|---:|---:|---|
| Agentix Figure 2 | 3 / 3 | 8.33% | FCFS is exact; discrete MLFQ and PLAS preserve the paper ordering benefit within tolerance. |
| TISA | 10 / 10 | 8.27% | The same semantic scheduler reproduces all four model speedups, the static range, FA3 utilization gain, and window-8 dispatch latency. |
| Agent.xpu | 5 / 10 | 77.02% | 8B reactive reductions, pending time, and proactive throughput pass; 3B mixed-flow reductions and iGPU/energy accounting fail. |
| ATX / Chipyard | 0 / 0 | n/a | Explicitly not executed; no completion claim. |

## Supported findings

- Agentix toy total wait is 18/17/13 for FCFS/MLFQ/PLAS versus paper 18/18/12. This is exact for FCFS and within 8.33% for both preemptive policies.
- TISA Dynamic versus Naive is 1.403/1.646/1.601/1.761× for ResNet50/BERT/GPT-J/LLaMA2 versus 1.52/1.79/1.74/1.92×. All errors are 7.67–8.27%.
- TISA FA3 ME-utilization improvement is 25.35% versus 26.4% (3.99% error); window-8 dispatch is the registered seven cycles.
- Agent.xpu's 8B reactive reductions are 95.43/96.69/97.57%, all below 1% relative error. Its representative reactive prefill pending time is 47.29 ms versus 48 ms (1.47% error), and its proactive throughput ratio is 2.533× versus the 2.0–2.4× range (5.53% to the nearest bound).

## Failed findings and diagnosis

- 3B reactive reductions are only 63.53/66.99/69.88%, versus 91.61/93.84/96.01%. The 8B pass and 3B fail isolate a load/interference omission rather than a priority-selection bug: scaling service demand by 2.08× pushes the identical scheduler into the reported regime.
- iGPU utilization reduction is 55.27% versus 37.1%, and energy reduction is 47.44% versus 26.8%. The model currently assigns all HEG prefill work to NPU, contradicting §4.3: reactive token-wise ops use elastic NPU+iGPU tensor parallelism, while dynamic prefill fragments remain on iGPU.
- Figure 4 reports a common mixed-kernel mechanism rather than per-workload correction: simultaneous execution slows memory-bound GEMV by up to 1.59× while GEMM changes only 1.04–1.10×. Run 001 lacks that asymmetric shared-DDR penalty.

## Direction

DEEPEN H2. Run 002 will add only the source-identified mechanisms: one Figure-4 GEMV contention factor for mixed baseline execution and a fixed 50/50 iGPU share for elastic prefill accounting. It will retain all traces, rates, seeds, token work, Agentix configuration, and TISA configuration. No endpoint-specific factor is allowed.


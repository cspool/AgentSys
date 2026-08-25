# H2 run 002 protocol: shared-DDR contention and elastic prefill accounting

## Classification

Confirmatory mechanism repair following run 001. The failure pattern and source evidence are fixed before implementation. No endpoint-specific or request-rate-specific parameter is permitted.

## Diagnosis from run 001

The identical scheduler passes all three 8B reactive reductions but misses all three 3B reductions, while reactive pending time already matches. This rejects a priority/preemption bug and predicts that a load-sensitive interference mechanism is absent. Utilization and energy are both over-improved because the model assigns all HEG prefill work to NPU.

## Source-identified changes

1. Apply a single `1.59×` service-time multiplier to memory-bound iGPU decode/GEMV only when reactive and proactive flows coexist with pending prefill. Agent.xpu Figure 4 reports simultaneous-versus-standalone execution-time changes up to 1.59× for GEMV while GEMM changes only 1.04–1.10×. The multiplier is common across 3B/8B and rates 1/3/5.
2. Account for a fixed 50% iGPU share of HEG prefill active time and energy. This represents the equal starting partition for Agent.xpu's elastic NPU+iGPU tensor parallelism; it is common to every HEG flow. It changes utilization/energy accounting, not logical work or completion timing.

## Frozen inputs

- All run-001 Poisson traces, durations, rates, seeds, token counts, queue ordering, batch limits, preemption boundary, and active throughput rates.
- Agentix and TISA code/configuration.
- Paper targets and 15% gate.

## Predictions

- The common contention term will amplify queueing only in the currently under-loaded 3B mixed baseline, moving all three 3B reactive reductions toward the paper values while preserving 8B direction and proactive-only throughput.
- The 50% elastic share will reduce the apparent iGPU-utilization and energy savings together, toward 37.1% and 26.8% without changing latency.
- Reactive prefill pending and TISA/Agentix endpoints will remain within 15%.

## Rejection rule

Run 002 is rejected if any previously passing endpoint regresses outside 15%, if any logical token count differs between baseline and HEG, or if any of the five run-001 failures remains outside 15%. A failed run will be retained; the two constants will not be adjusted from residuals.


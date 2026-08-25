# H5 run 006 protocol: source-aligned tile duration normalization

## Classification

Confirmatory repair of the single run-005 failure. Operator mapping, MIR inputs, selected count, SSA dependencies, memory spans, TISA window, and seven-cycle dispatch remain frozen.

## Change

The TISA source basis states that tile execution is roughly `10^3–10^5` cycles, making the measured 7–9 scheduler cycles negligible. Run 005 instead emitted 2/4/16-cycle minima. Run 006 sets a common minimum of 1024 cycles for ME, VE, and DE tiles, then retains shape-derived growth above that floor with caps inside the cited regime.

This scale is chosen before run 006 from the source granularity, not from the observed 0.627× residual. No engine-specific speedup target or per-op adjustment is allowed.

## Predictions and rejection

- All seven passing gates remain passing with identical operator/engine counts and dependencies.
- Dynamic decoder-slice execution becomes faster than strict static order and retains nonzero overlap.
- Scheduler overhead is below 1% of total dynamic cycles.

Reject if any mapping/determinism/work gate regresses or dynamic remains slower. Preserve run 005 as the small-tile boundary case.


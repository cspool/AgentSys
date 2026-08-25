# Full-stack run 008 analysis

All ten work, lineage, dependency, six-layer, priority, and outcome gates pass.

- Reactive completion: 21,651 cycles versus 65,536 baseline (3.027×) and 28,868 dynamic-only (1.333×).
- Overall makespan: 44,333 versus 90,112 baseline (2.033×), but 7.5% slower than dynamic-only.
- Proactive throughput: 4.511e-5 versus dynamic-only 4.850e-5; both proactive programs complete.
- Trace: 636 events, 212 objects, 212 terminal objects, 636 priority checks, all six layers.

Thus external urgency must be applied before ATLAS attained service at call release; merely copying it to lower objects (run 007) is insufficient. H4 is supported for the stated responsiveness objective, with the makespan/proactive trade-off explicitly retained.


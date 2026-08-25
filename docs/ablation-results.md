# Cross-layer ablation results

Run 013 passes 7/7 integrity gates and preserves work at every sweep point.

## Preemption granularity

On the same 8B mixed trace, 8/16/32/64/256-token chunks produce reactive P90 of 9.35/9.41/9.62/9.47/10.08 s. P99 remains 11.45–11.92 s. Smaller tiles improve responsiveness modestly; proactive mean latency changes by less than 2% and all points execute ten priority preemptions.

## TISA window

Window 1/2/4/8/16/32 gives 6320/3763/3553/3553/3553/3553 cycles. Four entries capture all timing benefit for this LLaMA2 trace; larger windows only reduce window-pressure counts and increase the number of inspected blocked candidates.

## Other ablations

- ATX full prefetch versus no-prefetch raises L2-OCA speedup from 1.60→2.10 (SpMM), 1.40→2.00 (SDDMM), and 1.30→1.40 (GeMM).
- Urgency-first release improves reactive completion 29,899→21,651 cycles (1.381×) versus lower-layer-only propagation.
- Ramulator two channels halve memory service but improve total TISA only 1.009× after ME becomes critical.
- On a 32×2048×2048 GEMM, identical 134,217,728 MACs at 4 B/cycle yield 8,454,144 OS versus 2,195,456 WS cycles (3.851×). The current open RTL's OS choice is therefore not universally optimal under extreme bandwidth pressure.


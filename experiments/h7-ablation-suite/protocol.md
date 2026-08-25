# H7 protocol: remaining cross-layer ablation suite

## Frozen sources

Use the already validated implementations/artifacts; no paper targets are fitted in this suite.

## Sweeps

- Agent.xpu preemption chunk: 8/16/32/64/256 tokens on the same 8B mixed trace; report reactive mean/P90/P99, proactive latency/throughput, and preemption count.
- TISA issue window: 1/2/4/8/16/32 on the same LLaMA2 tiles; report cycles, overlap, stalls, and utilization.
- ATX prefetch: no-prefetch versus full-prefetch ratios from run 004.
- Priority propagation: run 007 no-top-priority versus run 008 urgency-first.
- DDR bandwidth: run 012 one/two-channel Ramulator results.
- ME dataflow: output-stationary versus weight-stationary analytical traffic/cycle comparison for the same 32×2048×2048 GEMM on a 16×16 array. Use identical MAC count and a fixed 4 B/cycle external bandwidth.

## Gates

- Every sweep point completes and preserves logical work.
- P99 is at least P90 and P90 at least mean for every preemption point.
- Larger TISA windows do not change ME/VE/DE work; report non-monotonic timing if present.
- Dataflows have equal MACs and positive cycles/bytes.
- All source artifact hashes/run IDs are recorded.

This suite explains sensitivity and trade-offs; no sweep winner is selected to repair a paper endpoint.


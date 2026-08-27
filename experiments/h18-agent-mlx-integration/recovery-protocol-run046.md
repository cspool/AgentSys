# H18.1 recovery protocol — cache-aware three-workload replay (run 046)

Locked before changing the run-045 auditor or executing another Agent workload.

## Diagnosis-driven changes only

1. Rename/count the actual six serial stages.
2. Compute aggregate DMA/system from the parsed per-call records instead of
   multiplying the cold standalone value.
3. Add a hard repeated-launch cache contract. Because every LLM call reuses the
   same static input/output arrays, the first launch has 344 DMA cycles and each
   later launch has 216 on both backends. Bytes remain 576 per call.

No Agent schedule, compiler mapping, spatial word, ELF runtime, simulator,
golden, kernel oracle or paper parameter changes.

## Frozen aggregate counters

| workload | LLM | DMA cycles | cycle system | RTL system |
|---|---:|---:|---:|---:|
| react_moa_mcts | 10 | 2,288 | 3,628 | 3,068 |
| react_tool | 2 | 560 | 828 | 716 |
| planner_debate | 5 | 1,208 | 1,878 | 1,598 |

The run-045 instruction/DMA-byte/kernel table remains unchanged.

## Acceptance

- All three workloads execute serially through the six-stage pipeline.
- Each workload passes all original run-045 identity, compiler, per-call,
  logical-work, trace, backend-switch, no-ATX/HPTPE and parent gates.
- The new cold/warm DMA sequence and aggregate table pass exactly.
- Workload, generated header and ELF hashes are pairwise distinct.
- Counts remain 11/10/1, 3/2/1 and 6/5/1 calls/LLM/tools; MLX micro-ops are
  450/90/225.

Run 045 remains immutable negative evidence. Passing run 046 supports H18/H18.1.

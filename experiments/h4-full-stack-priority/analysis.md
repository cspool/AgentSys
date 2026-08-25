# Full-stack run 007 analysis

## Integrity result

All nine locked hard gates pass. The unified JSONL has 636 events over 212 objects, all six layers, exact terminal-event uniqueness, complete parent lineage, and 636/636 priority-inheritance checks. All four configurations share one logical digest and identical ME/VE/DE work.

## Performance result

| Configuration | Makespan | Reactive completion | High-level wait |
|---|---:|---:|---:|
| FCFS + static | 90,112 | 65,536 | 5 |
| ATLAS + static | 90,112 | 81,920 | 8 |
| FCFS + dynamic | 41,240 | 28,868 | 5 |
| current full stack | 43,302 | 29,899 | 8 |

- Full versus baseline: 2.081× makespan and 2.192× reactive speedup.
- Dynamic alone: 2.185× makespan speedup.
- Stacking efficiency is 95.24%; the current full stack is slightly slower than dynamic alone.

## Mechanism diagnosis

The implementation propagates the ReAct priority unchanged through flow/task/tile/engine, but the Agentix release scheduler still ranks only attained service. ATLAS delays ReAct call release in this mixed workload (wait 8 versus FCFS 5). Once delayed, lower TISA priority cannot recover the lost time. Therefore run 007 validates lineage and low-layer inheritance but does not yet implement true end-to-end priority ordering.

The next run must add external program urgency as the primary Agentix key and ATLAS service as the secondary key. That is required by the stated system contract, not selected to tune a residual. Run 007 remains the no-top-priority ablation.


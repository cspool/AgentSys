# H4 protocol: program-to-engine priority propagation and stacked ablation

## Classification

Exploratory new full-stack result. No source paper publishes a target for the combined stack, so this run must not be counted as a paper-number reproduction.

## Frozen workload and lowering

- Dynamic programs: ReAct/tool-use, three-way Mixture-of-Agents, and MCTS from `dynamic_agent_dag()`.
- Each LLM call lowers through the run-006 mllm decoder-slice mapping into the same ME/VE/DE tiles and 1024-cycle minimum.
- ReAct is reactive priority; MoA and MCTS are proactive. Every call, flow, task, tile, and engine event must inherit its program priority unchanged.
- Call release order comes from the executable FCFS or ATLAS high-level scheduler. Parent-call completion becomes a dependency on every root tile in a child call.
- All configurations consume identical programs, calls, operators, tile durations, memory spans, and dependency edges.

## Four configurations

1. `fcfs_static`: no program priority propagation; strict static tile groups.
2. `atlas_static`: ATLAS call release, static tile groups.
3. `fcfs_dynamic`: FCFS call release, TISA dynamic issue, no propagated urgency.
4. `full_stack`: ATLAS call release plus inherited reactive/proactive priority and TISA dynamic issue.

## Metrics

Program makespan, reactive completion latency, proactive completion/throughput, call wait, backend cycles, ME/VE/DE utilization/work, overlap, dependency/resource stalls, and scheduler decisions.

## Hard gates

- Exact logical-work and dependency digest equality across all four configurations.
- Every object completes exactly once; every parent exists before a child event; every dependency precedes consumer issue.
- Zero priority inheritance violations across program/call/flow/task/tile/engine.
- Unified JSONL contains all six layers and at least one complete path through them.
- Full stack improves reactive completion and overall makespan versus `fcfs_static` without losing a proactive program.
- Report all four ablations even if stacking is sub-additive or negative.

## Prediction

ATLAS and dynamic tile issue operate at different boundaries and should stack, while real shared engines/backpressure make their gains sub-multiplicative. Priority propagation should mainly improve the reactive program; it may reorder but must not starve proactive programs.


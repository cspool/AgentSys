# H4 run 008 protocol: urgency-first Agentix release

## Classification

Confirmatory implementation repair. Run 007 proves that urgency reaches flow/task/tile/engine but is absent from call release, so it is not end-to-end propagation.

## Change

Extend `AgentixSimulator.run` with an optional per-program `Priority` map. For preemptive PLAS/ATLAS selection, use the lexicographic key:

1. external urgency (`reactive < normal < proactive`),
2. existing discrete attained-service queue,
3. existing FCFS position/tie-break.

No program-priority map preserves byte-for-byte scheduling behavior for every prior Agentix experiment. Run 008 applies the map only to `full_stack`; the three ablations remain unchanged.

## Frozen state

Programs, calls, durations, mllm operator trace, tile scale, memory spans, dependencies, arrival scale, ATX/TISA window/dispatch, and all run-007 metrics/gates.

## Predictions and gates

- All nine run-007 integrity/work gates remain passing.
- Full-stack reactive completion is lower than both `fcfs_static` and `fcfs_dynamic`.
- No proactive program is lost; report any makespan/throughput trade-off rather than hiding it.
- A new scheduler unit test proves absent priority map preserves the Figure-2 result and urgency overrides attained service when provided.

H4 is supported if the system completes a zero-violation six-layer propagation path and improves reactive completion versus every no-propagation configuration. Overall makespan need not beat throughput-oriented dynamic-only scheduling; that trade-off must be explicit.


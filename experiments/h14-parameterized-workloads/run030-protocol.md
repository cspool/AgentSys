# H14.1 run-030 protocol: schedule-invariant HPTPE and lossless tile trace

## Motivation

Run 029 disproves two assumptions of the first workload-switching protocol:

- the run-028 aggregate checksum was not a schedule-invariant functional oracle;
  repeated call parity hid ME descriptor 4/5 state carry;
- shared stdout cannot guarantee a complete RTL trace frame.

The old numeric checksum is therefore not frozen. Descriptor words, application
digest, MIR digest, engine work, DMA and HPTPE operations remain frozen.

## Locked changes

1. Assert a descriptor-local reset/clear over the complete released HPTPE array
   pipeline when each ME descriptor starts. No duration, operand stream, PE count
   or scheduler timing changes.
2. Give every TISA issue/complete record an explicit call ID.
3. When `+agentsys_tisa_trace=<path>` is supplied, write tile records to that
   dedicated file and use it as authoritative evidence. UART stdout remains a
   human-readable fallback only.
4. The host parser must require a non-empty dedicated file with exactly the
   manifest-derived issue/complete set and zero transport repairs.

## Confirmatory gates

- Rebuild both revised Rocket simulators from the changed RTL.
- Standalone Icarus scheduler/dispatch test remains passing.
- For every `(call, descriptor, engine)`, static and dynamic completion checksums
  are identical, not merely their aggregate XOR.
- `react_tool`, `planner_debate` and `react_moa_mcts` all pass the generalized
  system gates without source edits and have distinct workload/header/ELF hashes.
- Each result preserves manifest-derived calls, descriptors, placement, busy
  work, DMA, HPTPE operations, dependencies, 11 trace layers and optional
  performance expectations.
- The certified workload retains its run-028 application digest and all 80
  descriptor words; its corrected accelerator checksum may change but must be
  deterministic across both backends and repeated execution.

## Prediction

Backend/system cycles and speedups remain unchanged because reset occurs in the
existing start cycle. Dedicated hardware logs eliminate UART frame repair. All
three switched workloads should then pass end to end.

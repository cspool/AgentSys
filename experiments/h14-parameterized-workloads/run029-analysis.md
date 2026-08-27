# H14.1 run-029 analysis — first parameterized workload execution

## Outcome

Run 029 is a retained partial/negative result. The new manifest-driven frontend,
compiler and per-workload ELF builder work, and one switched workload completes
the real system, but the second real workload exposes two lower-level bugs that
the fixed run-028 call multiplicity had hidden.

## Passing evidence

- Three JSON manifests validate with distinct canonical SHA-256 identities.
- All three execute Agentix and generate isolated application, compiled,
  generated-header, RISC-V ELF and pipeline artifacts without source edits.
- The certified manifest preserves run-028 application digest, call order and all
  80 control/tilemem descriptor words.
- `react_tool` executes on both ordinary-Rocket+HPTPE simulators and passes 17/17
  gates: 1 program, 3 calls, 2 launches, 16 descriptors, 122,880 HPTPE MACs and
  a 180-event/11-layer trace. Static/dynamic checksums match.
- The complete local suite passes 63 tests.

## Retained failures

`planner_debate` executes both ELFs successfully and passes 16/18 system gates,
but fails `same_application_and_xpu_work` and `tile_trace_static`.

1. **Schedule-dependent HPTPE result.** Static/dynamic aggregate checksums are
   `8d540c48c0817c79` and `01e555bbba8989c4`. Per-tile comparison localizes all
   differences to ME descriptors 4/5: the released HPTPE array pipeline retains
   state across descriptor starts. Run 028 used an even number of identical
   call patterns, so XOR aggregation accidentally canceled the mismatch.
2. **Non-atomic shared stdout.** One static issue marker is split inside the
   literal prefix by FESVR UART output (`AGENTSYS_T` ... `ISA_ISSUE`). The existing
   schema repair can join field suffixes but cannot recover a marker split inside
   its name. The log therefore contains 39 issue and 40 complete records.

## What this rules out

- A passing aggregate checksum on one fixed workload does not prove per-tile
  functional equivalence.
- Shared host stdout cannot be the authoritative hardware trace transport.

## Next locked direction

Reset/clear the complete HPTPE array pipeline at every descriptor boundary and
add a dedicated plusarg-selected TISA trace file with explicit call IDs. Both
changes require rebuilt Rocket simulators and a new confirmatory run; run 029
remains immutable evidence.

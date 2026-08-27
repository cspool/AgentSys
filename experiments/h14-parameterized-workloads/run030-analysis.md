# H14.1 run-030 analysis — complete workload switching

## Outcome

H14.1 is supported. Three structurally different Agent manifests compile and
execute end to end without source edits on the same rebuilt static/dynamic
ordinary-Rocket+TISA/HPTPE simulators.

| Workload | Programs/calls | LLM/tool | Descriptors | Trace events | HPTPE MACs | System gates |
|---|---:|---:|---:|---:|---:|---:|
| `react_moa_mcts` | 3 / 11 | 10 / 1 | 80 | 860 | 614,400 | 21/21 |
| `react_tool` | 1 / 3 | 2 / 1 | 16 | 180 | 122,880 | 18/18 |
| `planner_debate` | 2 / 6 | 5 / 1 | 40 | 436 | 307,200 | 19/19 |

Every workload passes its four pipeline stages: Agentix application execution,
mllm/Agent.xpu/TISA compilation, unique RISC-V ELF build and dual Rocket system
execution. Workload, header and ELF hashes differ across all three.

## Correctness repair

The full HPTPE pipeline now receives a local reset in the existing descriptor
start cycle. This does not change busy cycles or scheduling, but makes every ME
tile a pure function of its seed and descriptor. The run-029 failing workload's
aggregate static/dynamic checksums now both equal `37bbb1f0ed24bc74`.

The generalized runner additionally compares every completion checksum by
`(call, descriptor, engine)`. All 40 planner-debate tiles and all tiles in the
other workloads match between static and dynamic.

## Lossless hardware evidence

TISA records use a dedicated plusarg-selected file and contain explicit call
IDs. Static/dynamic issue+complete line counts are:

- certified: 160 / 160;
- react-tool: 32 / 32;
- planner-debate: 80 / 80.

All six logs parse with `repaired_frames=0`; shared UART output is no longer the
authoritative tile transport.

## Performance and invariants

All three use the same eight-descriptor model template, so backend speedup is
1.3764x while absolute work scales with LLM call count. Static/dynamic preserve
programs, calls, dependencies, flows, placement, busy cycles, DMA, HPTPE
operations, application/MIR/workload digests and corrected aggregate checksum.

The certified workload preserves the exact run-028 application digest
`4347e5adb9552f704a3397dc94afd6186911c8c07aa7c144ce57161f806733bd` and all 80
descriptor words. Its corrected accelerator checksum is
`b29121df4a9d1b05`.

## Verification

- 63/63 project tests pass.
- Standalone Icarus dispatch/file-trace test passes.
- Legacy and complete revised RTL lint pass (upstream HPTPE warnings retained).

## Remaining scope

H14.1 proves workload switching on the installed hardware profile. H14.2 must
now turn layer parameters into an explicit experiment matrix and bind every
paper endpoint to the same workload/configuration identity with <=10% error.

# H3 protocol: ATX/TISA Chipyard implementation and real Rocket execution

## Classification

Confirmatory hardware-contract implementation. The command ABI, descriptor layout, counters, and test invariants below are locked before RTL elaboration or Verilator execution. Chipyard timing is functional/system evidence, not Epoch or Xeon-Max performance evidence.

## Pinned substrate and references

- Chipyard: `/root/chipyard`, commit `b5d013190d637e634113cb5179f8c8885df1945a`.
- MLX engineering reference only: `cspool/MLX_dev` `sys` commit `b3a6d59f2ed634ea6181f5a29f3fa96281b1f384`; reuse the RoCC/HellaCache/ELF/build pattern, not its accelerator logic.
- HPTPE design reference: `wqzustc/High-Performance-Tensor-Processing-Engines` commit `ebe4db7d2d3c36d10c47683d7689f65f5c4ca3e4`; implement an original small output-stationary matrix engine rather than copying proprietary-flow assumptions.

## RISC-V custom0 ABI

| funct | operation | rs1 | rs2 | response |
|---:|---|---|---|---|
| 0 | config | descriptor/global value | target `[12:8]`, index `[4:0]` | none |
| 1 | launch | input DRAM pointer | output DRAM pointer | none |
| 2 | wait | 0 | 0 | blocks until COMPLETE; returns status bits |
| 3 | status | counter index | 0 | selected 64-bit counter |
| 4 | cancel | task-id mask | 0 | accepted cancellation mask |
| 5 | prefetch | descriptor index | 0 | accepted bit |
| 6 | clear | 0 | 0 | reset architectural queues/counters when idle |

Config target 0 stores descriptor control word, target 1 stores TileMem word, and target 31 stores global values: descriptor count, input beats, output beats, dynamic/static mode, and output SPM base.

Descriptor control word: tile id `[7:0]`, task id `[15:8]`, predecessor bitmap `[23:16]`, access `[25:24]`, priority `[27:26]`, engine `[29:28]` (`0=ME,1=VE,2=DE`), op type `[35:30]`, duration `[51:36]`, static group `[59:52]`, valid `[60]`. TileMem word: base `[31:0]`, size-minus-one `[47:32]`, scope `[49:48]`, bank `[53:50]`.

## RTL behavior

- Eight-entry architectural ATX/TISA descriptor RAM and completion bitmap.
- Dynamic backend: per-engine candidate routing, priority then sequence arbitration, explicit predecessor readiness, memory-scope/bank/range RAW/WAR/WAW checks against in-flight entries, non-preemptive tile execution, completion feedback, and cancellation at tile boundaries.
- Static backend: identical descriptors/work, but static-group barriers and program order replace semantic reordering.
- Two task/input buffers; prefetch marks the next descriptor/task and increments hit counters when consumed.
- HellaCache DMA reads input beats before backend launch and writes output beats after completion; real cache backpressure contributes to system/DMA cycles.
- Original output-stationary 4-lane matrix engine, vector ALU engine, and DMA/data engine execute concurrently behind the scheduler. The matrix engine produces an observable checksum from real input data.

## Required status counters

State/ABI magic, system cycles, DMA cycles/bytes, submitted/issued/completed/canceled tiles, ME/VE/DE busy cycles, dependency/resource stalls, pair/triple overlap cycles, scheduler decisions, prefetch requests/hits, checksum, and inherited-priority violations.

## Hard gates

- Scala elaboration and both static/dynamic Verilator builds succeed.
- Bare-metal ELF exits zero on both configurations and output words match the software reference.
- ABI magic is `0x41545801` (`ATX\x01`).
- `submitted = completed + canceled`; `issued = completed`; ME+VE+DE issue counts equal total issued.
- Dynamic and static consume identical input bytes and non-canceled logical descriptors.
- No RAW/WAR/WAW violation; priority-violation counter is zero.
- Dynamic emits nonzero ME/VE/DE overlap and uses no more cycles than static on the locked mixed-engine workload.
- Installation is idempotent and refuses a Chipyard commit mismatch.

## Paper-performance separation

Chipyard counters validate functionality, integration, and relative scheduling direction only. ATX paper endpoints are evaluated separately with the source-grounded 64-core/UTE analytical-event model; TISA paper endpoints remain the Python cycle model. Neither is replaced by Rocket timing.


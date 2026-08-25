# H6 protocol: Ramulator2 DDR trace adapter and bandwidth ablation

## Pinned simulator

CMU-SAFARI Ramulator2 v2.0a commit `be93be78055d922aa1d4d33e15bcc8f2b0c61a9d` (MIT), built from the official source as a standalone cycle-accurate memory simulator.

## Trace contract

- Convert selected Qwen3 mllm DE/data-movement operator inputs and outputs into Ramulator2 `LoadStoreTrace` records.
- Expand accesses at 64-byte cache-line granularity; inputs emit `LD`, outputs emit `ST`; addresses come from the deterministic SSA TileMem mapping.
- Cap only after complete operator records and export logical bytes, LD/ST counts, source MIR hash, and trace hash.

## Memory configuration

Use `GenericDRAM`, DDR4 8Gb x8, DDR4-2400R, two ranks, FRFCFS, all-bank refresh, open-row policy, and RoBaRaCoCh mapping. Sweep one and two channels with otherwise identical traces/configuration.

## Gates

- Official Ramulator2 executable exits zero for both channel counts.
- Reported read/write request counts match generated LD/ST counts and runs are deterministic.
- Two-channel service cycles do not exceed one-channel cycles on the same trace.
- Feed the measured relative memory service into a TISA DE-latency sweep and report model speedup/utilization sensitivity without changing ME/VE work.
- Store configs, trace, raw logs, parsed stats, commit, and hashes.

This is real Ramulator2 DDR evidence for the open NPU model; it remains separate from Chipyard's legacy DRAMSim2 system-memory path.


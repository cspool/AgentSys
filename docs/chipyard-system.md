# AgentSys ATX/TISA + Chipyard system implementation

## Outcome

The locked H3 hardware contract executes end to end on a real Rocket core in Chipyard commit `b5d013190d637e634113cb5179f8c8885df1945a`. The same RISC-V ELF configures eight TISA descriptors, prefetches a reactive task, DMA-reads real input through HellaCache, runs either static or semantic-dynamic ME/VE/DE scheduling, DMA-writes the result, and verifies every output word and counter in software.

The immutable audit is [chipyard-run_003.json](../artifacts/results/chipyard-run_003.json): 17/17 gates pass.

## System path

```text
Rocket bare-metal ELF
  │ custom0 config / launch / wait / status / cancel / prefetch
  ▼
AgentSys RoCC controller ── HellaCache DMA ── DRAM input/output
  │
  ▼
8-entry ATX/TISA descriptor RAM
  │       priority + deps + TileMem RAW/WAR/WAW
  ├──────────────┬──────────────┐
  ▼              ▼              ▼
ME (OS MAC)      VE             DE
  └──────────── completion feedback / counters
```

Core files:

- Chipyard binding: `system_sim/chipyard/AgentSysRoCC.scala`.
- RoCC/HellaCache controller: `rtl/agentsys/agentsys_rocc_controller.sv`.
- TISA scheduler: `rtl/agentsys/agentsys_tisa_scheduler.sv`.
- HPTPE-inspired original output-stationary ME plus VE/DE: `rtl/agentsys/agentsys_engines.sv`.
- Bare-metal runtime/test: `system_sim/software/agentsys_runtime.h` and `agentsys_system_test.c`.
- Pinned, idempotent installer: `scripts/install_agentsys_chipyard.sh`.
- Replay/audit: `scripts/run_agentsys_chipyard.py`.

## Descriptor contract

Each descriptor has a control and TileMem word. Control encodes valid, static group, duration, op type, target engine, inherited priority, access type, predecessor bitmap, task id, and tile id. TileMem encodes base, size, memory scope, and bank. The dynamic scheduler routes candidates to ME/VE/DE, selects priority then program order, verifies predecessor readiness, and checks aliasing plus RAW/WAR/WAW against every in-flight engine before issue. Tiles run to completion and retire into the completion bitmap.

The static configuration consumes the identical descriptors and durations but applies compiler groups and program order. This creates a same-input comparison rather than two unrelated workloads.

## Real Rocket + Verilator measurements

| Metric | Static | Dynamic | Direction |
|---|---:|---:|---:|
| Backend cycles | 332 | 249 | 1.333× speedup |
| RoCC busy/system cycles | 370 | 287 | 1.289× speedup |
| Host launch+wait cycles | 405 | 322 | 1.258× speedup |
| Pair-overlap cycles | 0 | 79 | dynamic overlap exposed |
| Dependency stalls | 289 | 227 | reduced |
| Resource stalls | 160 | 80 | reduced |
| ME/VE/DE busy | 160/80/80 | 160/80/80 | identical work |
| ME/VE/DE issue | 2/2/4 | 2/2/4 | identical work |
| DMA bytes | 96 | 96 | identical input/output |
| Checksum | `a42f89ec1a613914` | same | software reference matches |
| Priority violations | 0 | 0 | hard gate |

Both runs submit, issue, and complete eight descriptors with zero cancellations; the separate Python ATX adapter tests queued/running cancellation and double-buffer conservation. Prefetch request/hit is 1/1 in both hardware runs. ABI magic `0x41545801` is checked inside the ELF.

## Evidence boundary

These are real Chipyard/Rocket/Verilator cycles for the open implementation, not Epoch-silicon or Xeon-Max/ATX paper numbers. They prove the command ABI, cache/DMA path, descriptor execution, engine concurrency, priority/hazard invariants, checksum, and relative dynamic-over-static direction. Paper-number reproduction stays in the registered trace/cycle models and is reported separately.

## Replay

```bash
cd /workspace/AgentSys
bash scripts/install_agentsys_chipyard.sh /root/chipyard
make -C system_sim/software -j4 all

source /root/chipyard/env.sh
make -C /root/chipyard/sims/verilator CONFIG=AgentSysStaticRocketConfig -j4
make -C /root/chipyard/sims/verilator CONFIG=AgentSysDynamicRocketConfig -j4

cd /workspace/AgentSys
.venv/bin/python scripts/run_agentsys_chipyard.py
```

The installer rejects a different Chipyard commit, applies only the two stable-dependency compatibility patches needed by the retired checkout, and verifies installed source hashes in the final audit.


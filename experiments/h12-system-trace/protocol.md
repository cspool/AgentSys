# H12 protocol: application-to-Rocket CPU+XPU trace execution

## Objective

Close the remaining integration gap between host-side paper simulators and the real Chipyard system path. The required path is:

```text
executed Agent application
  -> instrumented framework calls/flows
  -> native mllm MIR lowering
  -> generated RISC-V workload/header
  -> bare-metal software runtime
  -> Rocket CPU custom0/HellaCache
  -> ME/VE/DE XPU and DMA
  -> unified measured system trace
```

## Application and framework contract

- Execute one deterministic ReAct, one three-way Mixture-of-Agents and one MCTS DAG through Agentix ATLAS/urgency ordering.
- Execute the ReAct tool call as real deterministic host work; lower each of ten LLM calls from the native eight-operator mllm transformer MIR.
- Emit 11 calls, 10 LLM calls, one tool call, 49 framework events, 80 hardware descriptors and six call dependency edges.
- The compiler must be deterministic and the generated header hash must be recorded.

## System execution contract

- Build a second RISC-V ELF from the generated header; do not replace the legacy paper-mechanism ELF.
- Execute the same trace ELF on `AgentSysStaticRocketConfig` and `AgentSysDynamicRocketConfig`.
- The Rocket program checks dependency masks, executes the tool on CPU, configures/launches/waits on RoCC for every LLM call, DMA-reads/writes real memory and checks every output/checksum/status counter.
- Buffer cycle-stamped events before printing so UART trace output is outside the measured application interval.

Python/framework code is not interpreted inside Rocket. The semantically executed application trace and native MIR are compiled into a static RISC-V workload; the software runtime, dependency checks, tool loop, RoCC commands and all XPU/DMA work execute inside the system simulator.

## Gates

1. Both real simulators and the trace ELF exit zero.
2. Static/dynamic execute identical 3 programs, 11 calls, 10 launches, 80 descriptors, 960 DMA bytes, checksums and ME/VE/DE work.
3. All dependencies and application priorities hold in both traces.
4. Expanded trace has exactly 200 events across application/framework/software/cpu/xpu/dma.
5. Dynamic backend, system and measured application cycles improve over static; dynamic/static backend speedup lies in the TISA 1.14–1.63× range.
6. Agentix application, Agent.xpu framework, ATX software and TISA hardware paper artifacts each remain within 15%.

## Outputs

- `artifacts/app_traces/agent-application-run_021.json`
- `artifacts/app_traces/compiled-system-workload-run_021.json`
- `system_sim/software/generated/agentsys_app_trace.h`
- `system_sim/build/software/agentsys-trace-system.riscv`
- `artifacts/results/system-trace-run_021.json`
- `artifacts/traces/system-trace-run_021.jsonl`
- final certificate run 022

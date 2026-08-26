# H12 analysis: application/framework trace executed on Rocket CPU+XPU

Run 021 executes from project commit `54fb34d96b0adbb4dafdc1a9b7f879845400680b` and Chipyard commit `b5d013190d637e634113cb5179f8c8885df1945a`.

## Application and compilation

- Executed application: ReAct + three-way Mixture-of-Agents + MCTS.
- Trace: 3 programs, 11 calls, 10 LLM calls, one CPU tool call and 49 framework events.
- Every LLM call lowers from the native eight-operator mllm transformer MIR; total hardware work is 80 descriptors and six inter-call dependency edges.
- The generated header and application have deterministic SHA-256 digests.

## Real system simulation

The same `agentsys-trace-system.riscv` ELF passes on both Static and Dynamic Rocket+RoCC simulators.

| Metric | Static | Dynamic | Result |
|---|---:|---:|---:|
| backend cycles | 6560 | 4910 | 1.336× |
| controller system cycles | 6940 | 5290 | 1.312× |
| measured application CPU cycles | 21310 | 19660 | 1.084× |
| pair overlap | 0 | 1590 | exposed by dynamic issue |
| ME/VE/DE busy | 2400/2400/1600 | identical | work conserved |
| DMA bytes | 960 | identical | work conserved |
| checksum | `b29121df4a9d1b05` | identical | functional equivalent |

Expanded trace output contains exactly 200 events and six layers: application, framework, software, cpu, xpu and dma. All dependency checks and priority violations pass. Dynamic/static backend speedup lies in the TISA 1.14–1.63× range.

## Layer-to-paper validation

- Application/Agentix: 16 endpoints, maximum error 9.09%.
- Framework/Agent.xpu: 11 endpoints, maximum error 8.07%.
- Software/ATX: 18 endpoints, maximum error 3.10%.
- Hardware/TISA: 10 endpoints, maximum error 8.27%.

All are below the expanded 15% layer gate. The eleven serial stages pass; total stage wall time is approximately 222.5 s. The full toolchain remains 12/12.

H12 is supported with one explicit boundary: Python and the full framework are not interpreted inside Rocket. Their executed semantic trace and native MIR are compiled to a static RISC-V workload; dependency checks, the tool body, runtime calls, RoCC, DMA and XPU execute in Chipyard.

# Revised ordinary-RISC-V + XPU integration plan

## Scope decision

- CPU is an ordinary RISC-V core.
- ATX is retained only as a historical independent paper experiment.
- The final integrated XPU path is mllm → Agent.xpu → TISA → HPTPE.
- Existing run 021 is a compiled-trace feasibility prototype, not the final revised system.

## Ordered plan

1. Freeze the ordinary RISC-V baseline and a neutral CPU↔XPU command/DMA interface.
2. Independently reproduce mllm, Agent.xpu and HPTPE mechanisms and paper experiments with complete pinned toolchains.
3. Integrate mllm operators into Agent.xpu flows, then lower them through TISA onto the HPTPE XPU in Chipyard.
4. Execute an end-to-end Agent trace on ordinary RISC-V+XPU and verify identical logical work, dependencies, DMA and outputs across baselines.
5. Require every layer's paper result to remain within 15%, then regenerate the report and completion certificate.

## Acceptance boundary

No integrated-system completion claim is allowed until all three standalone gates pass and the final Chipyard trace uses the HPTPE XPU rather than the current simplified ME. ATX results must not be used as evidence for the ordinary-RISC-V CPU design.

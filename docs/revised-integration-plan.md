# Revised ordinary-RISC-V + XPU integration plan

## Scope decision

- CPU is an ordinary RISC-V core.
- ATX is retained only as a historical independent paper experiment.
- The final integrated XPU path is mllm → Agent.xpu → TISA → HPTPE.
- Existing run 021 is a compiled-trace feasibility prototype, not the final revised system.

## Ordered plan

1. Freeze the ordinary RISC-V baseline and a neutral CPU↔XPU command/DMA interface.
2. Independently reproduce mllm, Agent.xpu and HPTPE mechanisms and paper experiments with complete pinned toolchains. Complete: run 023 closes mllm, run 024 closes HPTPE, and run 025 revalidates Agentix/Agent.xpu/TISA unchanged. The active certificate is 68/68 endpoints with 9.91% global maximum error and explicitly excludes ATX.
3. Integrate mllm operators into Agent.xpu flows, then lower them through TISA onto the HPTPE XPU in Chipyard.
4. Execute an end-to-end Agent trace on ordinary RISC-V+XPU and verify identical logical work, dependencies, DMA and outputs across baselines.
5. Require every layer's paper result to remain within 15%, then regenerate the report and completion certificate.

## Acceptance boundary

No integrated-system completion claim is allowed until all three standalone gates pass and the final Chipyard trace uses the HPTPE XPU rather than the current simplified ME. ATX results must not be used as evidence for the ordinary-RISC-V CPU design.

The standalone prerequisite now passes. Work proceeds to step 3; this does not
relax the final Chipyard/HPTPE trace requirement.

The detailed preregistered targets and evidence boundaries are in
`experiments/h13-revised-stack/protocol.md`; the live gap table is in
`docs/component-reproduction-audit.md`. For mllm, “performance reproduction” now
means the mllm-backed ASPLOS'25 llm.npu mechanisms and experiments, not the old
TISA-on-MIR 1.324x result.

# MLX+CPU rebase completion gap

The previous active certificate closes a dual-GPU plus Rocket/HPTPE system, not
the newly requested MLX+CPU hardware system. MLX_dev was pinned only as an
engineering reference (`role=engineering_reference_only`); no Agent workload
compiled into its spatial ISA and no AgentSys ELF ran on its MLX Rocket configs.

The MLX_dev `sys` branch provides a strong implementation base:

- an independent tag/block cycle model and executable physical 4x4 PE RTL;
- configuration/data networks, RF/FU/tag/control, routing, one-port SPM and
  HellaCache DMA;
- a four-command custom0 RoCC ABI and ordinary single-core Rocket configs;
- YAML-to-64-bit spatial-program lowering, software FP16 goldens and four
  standalone/Chipyard workloads;
- target-free same-work core mechanism certificates and a separately labeled
  target-informed five-point paper-aligned estimate.

It is not sufficient by itself. Its own full-paper certificate reports only one
of eighteen inventory items reproduced within 10%; the five-point e2e fit has
5.85% maximum in-sample error but 20.77% leave-one-out error and is explicitly
not independent validation. AgentSys must therefore preserve this boundary,
implement its own Agent/mllm/Agent.xpu/TISA-to-MLX lowering and execute the
resulting per-workload RISC-V software on the real cycle/RTL Rocket systems.

Completion requires replacing HPTPE as the primary final accelerator with MLX,
while retaining HPTPE and native GPU evidence as optional/historical backends.
The active regression matrix must add MLX rather than silently renaming an
HPTPE or GPU result.

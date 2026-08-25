# Research Findings

## Research Question

Can program-aware scheduling (Agentix), heterogeneous flow scheduling (Agent.xpu), and semantic tile scheduling (ATX/TISA) compose end to end while independently reproducing each source paper's registered core results within 15%?

## Current Understanding

The three layers address different blocking boundaries. PLAS/ATLAS removes call- and program-level head-of-line blocking using cumulative program or critical-path service. Agent.xpu decouples prefill from decode and applies priority, batching, placement, and preemption at heterogeneous flow/stage boundaries. ATX and TISA move asynchronous task launch, prefetch, typed dependency resolution, and ME/VE/DE overlap below the runtime. Their mechanisms can plausibly stack because they operate at program, stage, and tile timescales, but composition is not yet evidence: priority inheritance and backpressure must be modeled explicitly and then exercised through one unified trace.

The available evidence requires distinct labels. Agentix's published evaluation used A100 GPUs; Agent.xpu used an Intel Core Ultra 5 125H; TISA used unreleased Epoch silicon; ATX used an internal Sniper-derived simulator. The local work can reproduce scheduling endpoints using a source-grounded trace/cycle simulator and can validate the hardware contract on real Chipyard Rocket+Verilator, but it must not label the local hardware as the original platforms.

## Key Results

No experiment has run yet. The initial numerical targets and hard functional gates are locked in [H1 protocol](experiments/h1-paper-contract/protocol.md).

## Patterns and Insights

- The MLX_dev `sys` branch is useful for Chipyard integration because it already validates a custom0 RoCC controller, HellaCache DMA, a bare-metal ELF, and two accelerator backends on the exact local Chipyard commit.
- It is not evidence for AgentSys performance: its tagged-CDC spatial architecture and paper targets differ from ATX/TISA and Agent scheduling.

## Lessons and Constraints

- Never infer original-hardware reproduction from a calibrated trace simulator or from Chipyard functional timing.
- Never tune model parameters after reading an endpoint residual without registering a new exploratory experiment and holding out an independent endpoint.
- Combined-stack gains have no published numerical target and therefore must be reported as a new local result, not a reproduced paper point.
- Two RTX 4090-class GPUs, when available, may provide functional/kernel baselines only; they cannot substitute for Agentix's multi-A100 evaluation.

## Open Questions

- Can one target-independent parameterization reproduce the registered endpoints across multiple workloads rather than a separate fit per point?
- How much of the end-to-end gain survives priority propagation through finite ATX/TISA queues and DDR contention?
- Can the Chipyard RTL preserve RAW/WAR/WAW correctness while allowing the same non-conflicting issue decisions as the Python reference model?

## Optimization Trajectory

Bootstrap only. Run 001 will establish the executable Agentix/Agent.xpu/ATX/TISA contracts and report error without residual-guided retuning.


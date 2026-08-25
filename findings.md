# Research Findings

## Research Question

Can program-aware scheduling (Agentix), heterogeneous flow scheduling (Agent.xpu), and semantic tile scheduling (ATX/TISA) compose end to end while independently reproducing each source paper's registered core results within 15%?

## Current Understanding

The three layers address different blocking boundaries. PLAS/ATLAS removes call- and program-level head-of-line blocking using cumulative program or critical-path service. Agent.xpu decouples prefill from decode and applies priority, batching, placement, and preemption at heterogeneous flow/stage boundaries. ATX and TISA move asynchronous task launch, prefetch, typed dependency resolution, and ME/VE/DE overlap below the runtime. Their mechanisms can plausibly stack because they operate at program, stage, and tile timescales, but composition is not yet evidence: priority inheritance and backpressure must be modeled explicitly and then exercised through one unified trace.

The available evidence requires distinct labels. Agentix's published evaluation used A100 GPUs; Agent.xpu used an Intel Core Ultra 5 125H; TISA used unreleased Epoch silicon; ATX used an internal Sniper-derived simulator. The local work can reproduce scheduling endpoints using a source-grounded trace/cycle simulator and can validate the hardware contract on real Chipyard Rocket+Verilator, but it must not label the local hardware as the original platforms.

## Key Results

- Run 001 executes 23 preregistered endpoints: 18 pass and 5 fail. [Machine result](artifacts/results/run_001.json) and [analysis](experiments/h1-paper-contract/analysis.md).
- Agentix passes all three Figure-2 wait endpoints (18/17/13 observed versus 18/18/12; maximum error 8.33%).
- TISA passes all ten endpoints: four Dynamic-vs-Naive speedups have 7.67–8.27% error, all static comparisons pass the published range, FA3 utilization is 25.35% versus 26.4%, and W=8 dispatch is seven cycles.
- Agent.xpu passes all three 8B reactive reductions (<1% error), 47.29 ms reactive prefill pending (1.47% error), and the proactive throughput range. Its three 3B reductions and utilization/energy accounting fail.

## Patterns and Insights

- The MLX_dev `sys` branch is useful for Chipyard integration because it already validates a custom0 RoCC controller, HellaCache DMA, a bare-metal ELF, and two accelerator backends on the exact local Chipyard commit.
- It is not evidence for AgentSys performance: its tagged-CDC spatial architecture and paper targets differ from ATX/TISA and Agent scheduling.
- The same Agent.xpu scheduler passes 8B but fails 3B. This points to a missing load-dependent contention term, not broken reactive-first ordering. Agent.xpu Figure 4 supplies the mechanism: simultaneous NPU/iGPU GEMV can take 1.59× standalone time, while GEMM is nearly unchanged.
- The iGPU and energy failures have one shared accounting cause: run 001 sends every HEG prefill cycle to NPU, whereas Agent.xpu uses elastic NPU+iGPU tensor parallelism for reactive token-wise prefill and retains dynamic fragments on iGPU.

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

Run 001 establishes the first trajectory point at 77.02% maximum endpoint error (18/23 pass). The large error is confined to H2; H1 and the TISA half of H3 already pass every executed endpoint. Run 002 is constrained to the two source-identified Agent.xpu mechanisms above.

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
- Run 002 adds the single Figure-4 contention mechanism and fixed elastic prefill share. All six 3B/8B reactive reductions now pass; total coverage is 21/23. The two remaining failures are utilization/energy measurement-contract mismatches, not latency behavior.
- Run 003 closes the first real hardware path: static and dynamic Rocket+Verilator configurations pass 17/17 gates. Dynamic exposes 79 ME/VE/DE overlap cycles and improves backend/system time by 1.333×/1.289× with identical logical work, DMA bytes, and checksum.
- Run 004 adds ATX paper coverage: 18/18 organization, prefetch, task-size, and decompression endpoints pass with 0.285% maximum error under a transparent paper-parameterized component model.
- Run 005 closes most of the mllm trace path: real FooNet and Qwen3 MIR parse deterministically and lower to all three engines. The first timing run is intentionally retained as a failure because its 2–16 cycle tiles make seven-cycle scheduling overhead dominant.
- Run 006 applies the source-aligned 1024-cycle floor and passes 9/9 mllm gates. On identical decoder-slice work, dynamic scheduling improves 8192→6186 cycles (1.324×) and exposes 2048 overlap cycles; H5 is supported.
- Run 007 establishes the six-layer trace and exact work/lineage invariants, but current stacking is sub-additive: 2.081× versus dynamic-only 2.185×. ATLAS delays ReAct at release because it has no external urgency key; lower-layer priority cannot recover that delay.
- Run 008 completes end-to-end urgency: reactive completion is 3.027× faster than baseline and 1.333× faster than dynamic-only. It costs 7.5% makespan and 7.0% proactive throughput versus dynamic-only, without starving either proactive program. H4 is supported with this trade-off.
- Run 009 corrects active-period utilization and CPU-control energy accounting. Agent.xpu now passes 10/10 endpoints; the combined executed Agentix/Agent.xpu/TISA paper set passes 23/23 with 8.33% maximum error. H2 is supported.
- Run 010 completes the registered Agentix aggregate set: 13/13 throughput/offline endpoints pass under an explicit paper-parameterized component replay, alongside the independent Figure-2 scheduler.
- Run 011 closes the omitted Serial baseline: Agent.xpu passes 11/11, including 33.42% active iGPU reduction versus the 32.5% target.

## Patterns and Insights

- The MLX_dev `sys` branch is useful for Chipyard integration because it already validates a custom0 RoCC controller, HellaCache DMA, a bare-metal ELF, and two accelerator backends on the exact local Chipyard commit.
- It is not evidence for AgentSys performance: its tagged-CDC spatial architecture and paper targets differ from ATX/TISA and Agent scheduling.
- The same Agent.xpu scheduler passes 8B but fails 3B. This points to a missing load-dependent contention term, not broken reactive-first ordering. Agent.xpu Figure 4 supplies the mechanism: simultaneous NPU/iGPU GEMV can take 1.59× standalone time, while GEMM is nearly unchanged.
- The iGPU and energy failures have one shared accounting cause: run 001 sends every HEG prefill cycle to NPU, whereas Agent.xpu uses elastic NPU+iGPU tensor parallelism for reactive token-wise prefill and retains dynamic fragments on iGPU.
- Run 002 proves the 1.59× shared-DDR term generalizes across all six reactive endpoints without per-rate factors. It also shows that a wall-busy fraction is not the paper's active-period-weighted iGPU metric; keeping these definitions separate is now a hard constraint.
- Chipyard confirms that semantic issue can produce an end-to-end benefit even after real Rocket custom-instruction and cache/DMA overhead: backend improvement 33.3% becomes 28.9% over the controller busy interval and 25.8% at host launch/wait.
- Dynamic tile scheduling only helps above its intended granularity. Correct semantic mapping alone is insufficient when backend lowering emits sub-7-cycle tiles; the mllm adapter must preserve a hardware-realistic tile scale.

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

Run 001 starts at 77.02% maximum error (18/23 pass). Run 002 reduces this to 51.99% (21/23 pass) using one cross-workload contention term and fixed hardware accounting. The next performance trajectory point will add ATX endpoints; the implementation critical path is now the real Chipyard RoCC/TISA backend.

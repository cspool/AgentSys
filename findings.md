# Research Findings

## Research Question

Can Agentix, Agent.xpu, mllm/llm.npu, TISA and HPTPE be independently reproduced within 15%, then compose on an ordinary-RISC-V Chipyard CPU+XPU system?

## Current Understanding

The three layers address different blocking boundaries. PLAS/ATLAS removes call- and program-level head-of-line blocking using cumulative program or critical-path service. Agent.xpu decouples prefill from decode and applies priority, batching, placement, and preemption at heterogeneous flow/stage boundaries. ATX and TISA move asynchronous task launch, prefetch, typed dependency resolution, and ME/VE/DE overlap below the runtime. Their mechanisms can plausibly stack because they operate at program, stage, and tile timescales, but composition is not yet evidence: priority inheritance and backpressure must be modeled explicitly and then exercised through one unified trace.

The available evidence requires distinct labels. Agentix's published evaluation used A100 GPUs; Agent.xpu used an Intel Core Ultra 5 125H; TISA used unreleased Epoch silicon; ATX used an internal Sniper-derived simulator. The local work can reproduce scheduling endpoints using a source-grounded trace/cycle simulator and can validate the hardware contract on real Chipyard Rocket+Verilator, but it must not label the local hardware as the original platforms.

Final synthesis: urgency must participate at call release before it can be preserved below; semantic tile scheduling becomes beneficial only at the intended coarse granularity; prefetch/bandwidth gains are largest before the critical path shifts to compute; and dataflow choice remains workload/bandwidth dependent. These conditions explain both the successful stack and its observed trade-offs.

The revised architecture removes ATX from the integrated CPU path. Run 023 closes mllm itself plus llm.npu's chunk sharing, shadow-outlier path and out-of-order scheduling. Run 024 closes HPTPE's released OPT1/2/3/4C RTL and report endpoints. Run 027 replaces the old four-lane Chipyard ME with the released HPTPE OPT1 16x16 array and carries the active stack through an ordinary Rocket CPU.

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
- Run 012 closes real DDR modeling: official Ramulator2 halves memory service with two channels, but total TISA improves only 1.009× because ME becomes critical. This separates bandwidth benefit from bottleneck migration.
- Run 013 completes the sensitivity suite: TISA's timing knee is W=4, fine preemption modestly improves tails, and current OS ME dataflow can be 3.851× worse than WS under extreme bandwidth pressure. Gains are constrained by shifting bottlenecks, not monotonic knobs.
- Run 023 builds pinned mllm v2 and passes 20/20 native executables with 101 gtest cases. Its native-MIR-driven llm.npu model executes 4,480 subgraphs and 18,336 dependency checks per schedule; chunk sharing is 1.974×, shadow outliers 6.600×, OOO latency reduction 32.91%, and NPU bubble 33.33%→0.636%. All 5 endpoints pass at 15%, max error 9.91%.
- Run 024 executes HPTPE OPT1 OS/WS/Cube, OPT2, OPT3 and OPT4C: 9/9 organizations, 302 signed golden checks and 9/9 full-scale lint pass. All 26 endpoints pass at 15%, max error 0.98%; OS/WS/Cube frequency gains are 2.097/1.667/1.575x.
- Run 025 reruns Agentix/Agent.xpu/TISA unchanged and combines all active standalone evidence. Five of five components, 68/68 endpoints and 8/8 gates pass at 9.91% global maximum error. ATX is a machine-checked excluded component.
- Run 026 physically integrates the revised stack on ordinary Rocket and the released HPTPE 16x16 array. Eighteen of 19 gates pass, 860 cross-layer events are recorded, and static/dynamic work and checksum match. The 2.000x backend speedup exceeds the locked TISA 1.14--1.63x range, so this is a retained negative result rather than completion evidence.
- Run 027 restores the paper's strong-static stage baseline and exact seven-cycle dynamic dispatch. All 20 gates pass: backend/system/CPU-observed speedups are 1.376/1.340/1.056x, 860 events cover 11 layers, and 614,400 HPTPE MACs plus checksum remain identical.
- Run 028 reruns the complete active stack in eight strict serial stages. Reproduction is 8/8, toolchain audit 12/12 and final certificate 15/15; fresh pytest, dispatch RTL, legacy lint and full HPTPE/RoCC lint all pass. The five active components remain 68/68 at 9.91% maximum error.
- Run 029 generalizes the frontend to versioned workload manifests and per-workload ELFs. `react_tool` passes 17/17 with 16 descriptors and 180 events, proving source-edit-free switching. A cross-program `planner_debate` workload exposes two hidden fixed-load artifacts: HPTPE pipeline state makes ME tile checksums schedule-dependent, and shared UART/RTL stdout can split a trace marker inside its prefix.
- Run 030 fixes both artifacts and supports H14.1. Three source-edit-free workloads pass real dual-Rocket execution with 80/16/40 descriptors and 860/180/436 events. Dedicated TISA logs have zero repairs, every tile checksum is static/dynamic identical, and HPTPE work scales exactly with LLM call count.
- Run 031 supports H14.2: one executable matrix drives five layer configurations, reruns 68 unique paper endpoints at a uniform 10% limit and exercises five output-changing sensitivity variants. Max errors remain 9.09/8.07/8.27/9.91/0.98% for Agentix/Agent.xpu/TISA/mllm/HPTPE.
- Run 032 closes H14 and the parameterized-system goal: a single serial entry point reruns the five-layer matrix and three workload→ELF→dual-Rocket paths, then passes a 15/15 fresh certificate. Workload, configuration, header, ELF, tile and paper-result identities are all machine-linked.
- Run 033 supports H15.1 on the actual host: two NUMA-pinned processes execute real CPU work, CUDA FP16 GEMM/SiLU and pinned H2D/D2H transfers on two distinct RTX 4090s, followed by a correct 64 MiB NCCL all-reduce. Runtime gates are 11/11 and the independent CUDA/NVML/Nsight audit is 9/9; peer access is unavailable in both directions. This is explicitly local 4090/Xeon evidence, not an A100/Core-Ultra paper reproduction.
- Run 034 retains a dependency/toolchain failure rather than masking it: NVIDIA's pinned Linux Python compiler wheel contains ptxas/NVVM but no `nvcc` driver, so the official mllm CUDA configure/build cannot start and only 3/8 gates pass. Its CCCL/CUTLASS commits are present, and source inspection proves the pinned upstream CUDA backend has empty kernel translation units and no registered op factory; later AgentSys CUDA execution must be labeled as an adapter.
- Run 035 recovers a real project-local nvcc 12.8.93 through a SHA-pinned micromamba/NVIDIA Conda environment and passes 9/13 gates without changing the host CUDA/driver. Configuration then exposes an upstream mllm defect: disabling tools removes `mllm-params-inspector`, but an unconditional install rule still names it. The result stops before CUDA targets rather than hiding the option inconsistency.
- Run 036 enables the missing upstream tools target, configures successfully, and nvcc compiles all four mllm CUDA units plus `libMllmCUDABackendCudaOps.so`. Linking then stops because mllm's Clang OpenMP fallback injects `-lomp` although no OpenMP runtime exists; 9/13 gates remain passing and no device-test claim is made.
- Run 037 removes optional OpenMP and successfully links mllm's core runtime. CUDA backend linking then exposes a Conda layout mismatch: packaged CUDA/NVML stubs exist under `targets/x86_64-linux/lib/stubs`, while mllm searches `lib/stubs`; the run remains 9/13 and localizes the final library-search issue.
- Run 038 fixes the stub search and builds all three upstream CUDA targets; the test enumerates both RTX 4090s and linkage resolves. It then aborts during teardown because mllm's own explicitly CUDA-required memory-manager clear call is commented out, causing `cudaFree` after driver shutdown. This 11/13 result motivates a traceable one-line framework patch.
- Run 039 supports H15.2 with 13/13 gates. A hashed one-line framework patch enables mllm's own CUDA-required pre-shutdown memory clear; two consecutive builds/tests each enumerate both RTX4090s and exit zero. Linkage uses local cudart and real host driver/NVML. The upstream CUDA backend remains honestly bounded to metadata/allocator lifecycle because its CUDA units are empty and no op factories exist.
- Run 040 supports H15.3 and closes the workload-aware vertical path: 4/4 serial stages and 11/11 global gates pass. Three Agent DAGs execute 80/16/40 MIR-derived real CUDA ops across both GPU/NUMA ranks, retain 860/180/436 Rocket+TISA/HPTPE events, and merge into 993/209/504 identity-linked events without cross-clock conversion. GPU placement switches, all 68 paper endpoints remain within 10% (max 9.91%), and the CUDA adapter/upstream boundary is explicit.
- Run 041 closes H15 and the expanded goal with a profiler-backed 22/22 certificate. The frozen react-tool plan remains 13/13 natively; Nsight audit is 9/9 with all 16 MIR ranges plus GPU/NCCL/transfer classes. Fresh 90-test pytest, mllm CUDA dual-GPU idempotence, dispatch and both RTL lints pass. Every evidence boundary and artifact hash is retained.
- Run 042 reopens and qualifies MLX as the new active hardware basis: current sys commit plus Chipyard pass 10/10 source/evidence gates, with 21 unchanged core files, real 4x4 RTL/cycle/Rocket evidence and 5/5 target-informed e2e rows at 5.85% max error. The external repository's strict full-paper <=10% result remains honestly false (1/18); Agent-specific lowering/integration is still required.
- Run 043 freshly rebuilds the active MLX cycle model and physical 4x4 RTL outside the reference tree. Ten of ten gates and 8/8 golden runs pass; identical per-PE programs produce different global interleavings, all ten opcodes have measured timing, and target-free cycle/RTL ratios span 1.193x–2.098x. Rocket and Agent integration remain open.
- Run 044 closes the MLX+ordinary-Rocket substrate at 12/12. Two freshly built Rocket configs execute four distinct ELFs 8/8 with exact golden/ABI, run-043 kernel identity, conserved work, real HellaCache DMA and `system=DMA+kernel+2`; 12 installed files byte-match current MLX and no paper target is consumed.

## Patterns and Insights

- The MLX_dev `sys` branch is useful for Chipyard integration because it already validates a custom0 RoCC controller, HellaCache DMA, a bare-metal ELF, and two accelerator backends on the exact local Chipyard commit.
- It is not evidence for AgentSys performance: its tagged-CDC spatial architecture and paper targets differ from ATX/TISA and Agent scheduling.
- The same Agent.xpu scheduler passes 8B but fails 3B. This points to a missing load-dependent contention term, not broken reactive-first ordering. Agent.xpu Figure 4 supplies the mechanism: simultaneous NPU/iGPU GEMV can take 1.59× standalone time, while GEMM is nearly unchanged.
- The iGPU and energy failures have one shared accounting cause: run 001 sends every HEG prefill cycle to NPU, whereas Agent.xpu uses elastic NPU+iGPU tensor parallelism for reactive token-wise prefill and retains dynamic fragments on iGPU.
- Run 002 proves the 1.59× shared-DDR term generalizes across all six reactive endpoints without per-rate factors. It also shows that a wall-busy fraction is not the paper's active-period-weighted iGPU metric; keeping these definitions separate is now a hard constraint.
- Chipyard confirms that semantic issue can produce an end-to-end benefit even after real Rocket custom-instruction and cache/DMA overhead: backend improvement 33.3% becomes 28.9% over the controller busy interval and 25.8% at host launch/wait.
- Dynamic tile scheduling only helps above its intended granularity. Correct semantic mapping alone is insufficient when backend lowering emits sub-7-cycle tiles; the mllm adapter must preserve a hardware-realistic tile scale.
- mllm's real build and its paper mechanism are separate gates. A valid MIR parser/TISA speedup does not reproduce llm.npu; conversely, source-grounded llm.npu scheduling does not become Qualcomm device measurement.
- HPTPE separates executable functionality/cycles from PPA provenance. Open RTL can be re-executed, but absolute SAED32 frequency/area remains author-DC-report evidence without a Synopsys license.
- Perfect three-engine occupancy can overstate TISA's published gain even when every work-conservation invariant passes. Integrated performance fidelity therefore needs a source-grounded scheduling cost/concurrency constraint in addition to functional RTL correctness.
- Aggregate XOR equality is insufficient for functional validation: an even number of repeated call patterns can cancel identical per-call static/dynamic checksum differences. Generic workload testing must compare every tile and reset accelerator-local pipeline state per descriptor.
- Workload parameterization should separate functional gates from optional performance expectations. A new DAG may legitimately have no scheduling opportunity; only manifests tied to a paper/configuration should impose a numerical speedup range.
- Configuration provenance must be executable: the runner compares returned implementation config with matrix input and separately hashes baseline/variant payloads. A parameter listed only in documentation is not evidence of parameterization.

## Lessons and Constraints

- Never infer original-hardware reproduction from a calibrated trace simulator or from Chipyard functional timing.
- Never tune model parameters after reading an endpoint residual without registering a new exploratory experiment and holding out an independent endpoint.
- Combined-stack gains have no published numerical target and therefore must be reported as a new local result, not a reproduced paper point.
- Two RTX 4090-class GPUs, when available, may provide functional/kernel baselines only; they cannot substitute for Agentix's multi-A100 evaluation.
- Upstream aggregate test binaries can contain explicitly NYI platform cases. Preserve the unfiltered failure, then register a supported-platform subset; never silently count an NYI crash as a pass.

## Open Questions

- Can one target-independent parameterization reproduce the registered endpoints across multiple workloads rather than a separate fit per point?
- How much of the mllm/Agent.xpu/TISA gain survives the HPTPE array, finite queues and DDR contention on ordinary RISC-V?
- Can the Chipyard RTL preserve RAW/WAR/WAW correctness while allowing the same non-conflicting issue decisions as the Python reference model?

## Optimization Trajectory

Run 001 starts at 77.02% maximum error (18/23 pass). Run 002 reduces this to 51.99% (21/23 pass) using one cross-workload contention term and fixed hardware accounting. Run 009 reaches 8.33% with all direct endpoints passing. Runs 010–013 close aggregate Agentix/ATX, Serial, Ramulator2, and requested ablations. Run 014 proves 55/55 endpoints and the original 11/11 completion requirements. Runs 015–016 add the complete pinned toolchain, execute all eight stages serially, and close the expanded 13/13 audit without changing paper error.

Runs 017–018 tighten the live contract to 10% and replace the combined direct-paper evidence input with four independent profiles/artifacts. Agentix 16/16, Agent.xpu 11/11, ATX 18/18 and TISA 10/10 pass; the global maximum remains 8.33%. The nine-stage manifest, 12-gate toolchain audit and 14/14 final certificate all pass.

Runs 019–020 replace the remaining 31 parameterized endpoints with executable open substitutes. Agentix now derives SLO throughput from actual program/call scheduling and KV-swap traces; ATX derives cycles from UTE/queue/stream/LDQ/bus/buffer events. All 55 endpoints still pass at 10%, with a new maximum of 9.09%; parameterized component replay is zero and the final certificate is 15/15.

Run 021 closes the physical integration gap: one executed ReAct/MoA/MCTS trace and native mllm graph compile into a second RISC-V ELF and run on both Rocket+RoCC systems. The resulting 200-event trace measures application/framework/software/CPU/XPU/DMA. Dynamic issue is 1.336× at the backend, 1.312× at controller-system scope and 1.084× end to end, exposing host/runtime dilution rather than assuming gains compose unchanged.

Run 023 starts the revised stack. Real mllm framework execution passes 20/20 selected binaries and 101 gtests; the three llm.npu mechanisms pass 5/5 paper endpoints at 9.91% maximum error. The 22.4× cross-platform headline remains explicitly unverified because the Qualcomm phones and five original baselines are unavailable.

Run 024 closes the revised hardware component before integration: HPTPE passes 9/9 RTL organizations and 26/26 endpoints at 0.98%. OPT3/OPT4C cycle values are real open-RTL execution; 24 absolute PPA values remain author report replay.

Run 025 closes the standalone prerequisite: Agentix 16, Agent.xpu 11, TISA 10, mllm 5 and HPTPE 26 endpoints all pass, totaling 68. The next metric is no longer component error optimization; it is preservation of these mechanisms and work invariants in the revised Chipyard path.

Run 026 preserves those mechanisms through the physical Chipyard path, but its
unconstrained ME/VE/DE overlap yields 2.000x rather than the registered
1.14--1.63x TISA range. The next run must change only the dynamic scheduling
cost/concurrency model and retain all run-026 work and lineage invariants.

Run 027 closes that mismatch using the preregistered source contract rather than
a fitted delay. Existing Agent.xpu stage metadata defines the strong-static
pipeline and the paper fixes dynamic dispatch at seven cycles. The real
Rocket+HPTPE result is 1.376x with all run-026 work/lineage gates preserved.

## Toolchain Closure

- Python 3.11 and the four environment packages are hash-locked with `uv.lock`; system tools, seven source revisions, compatibility patches, build products and Chipyard overlays are checked separately.
- Run 015 records exact commands, output hashes and non-overlapping stage timestamps for all eight component/system experiments.
- Run 016 combines toolchain 11/11, serial replay 8/8, paper 55/55, current pytest and RTL lint into one 13/13 certificate.
- Run 017 registers four standalone paper commands and artifacts, all with `limit=0.10`, then executes them as the first four of nine strictly serial stages.
- Run 018 consumes only those four paper artifacts for endpoint accuracy and combines paper-profile 4/4, toolchain 12/12, serial replay 9/9, pytest and RTL lint into one 14/14 certificate.
- Run 019 adds an independently tested public Autellix reference (58 tests), an executable Agentix SLO-capacity/KV simulator and an executable ATX/UTE microarchitecture simulator; none reads endpoint targets while executing.
- Run 020 reports 24 direct source-grounded endpoints, 31 open executable closed-platform substitutes and zero parameterized component replays.
- Run 021 adds two application/compilation artifacts, the trace ELF, 11/11 serial stages and 13/13 real CPU+XPU gates; the per-layer paper errors are 9.09/8.07/3.10/8.27%, all below 15%.
- Run 023 introduces `revised_build_outputs`/`revised_component_profiles` without changing the historical run-022 contract. The mllm profile combines a real Clang-16 build/test artifact with native-MIR-driven llm.npu performance evidence.
- Run 024 adds pinned Verilator 5.050 and Icarus 11 to the revised namespace and registers an independent HPTPE profile without mutating the historical four-paper/55-endpoint contract.
- Run 025 registers exactly five revised profiles and a separate active-component certificate; its audit fails if ATX appears or the total differs from 68.
- Run 028 promotes those profiles into the active `config/revised-toolchain.json`: five build products, 16 installed-source equality checks, eight serial stages and a separate revised completion certificate. The historical ATX-inclusive manifest remains reproducible but is not an input to the active certificate.

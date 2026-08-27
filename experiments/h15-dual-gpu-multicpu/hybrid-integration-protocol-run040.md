# H15.3 protocol — workload-aware dual-GPU/Rocket vertical system (run 040)

Locked before implementing the hybrid plan compiler, MIR-to-CUDA adapter or
hybrid trace merger.

## Hypothesis

The three existing versioned Agent DAGs can compile without source edits into a
single identity-preserving experiment that executes real mllm-MIR-derived work
on both NUMA-local RTX 4090 ranks and the corresponding RISC-V/TISA/HPTPE work
on both Rocket simulators, while the existing five paper profiles remain 68/68
within 10%.

## Fixed execution profile

- Workloads, in order: `react_moa_mcts`, `react_tool`, `planner_debate`.
- Agentix/application and existing mllm→Agent.xpu→TISA/HPTPE compiler are reused
  unchanged; each workload builds its own RISC-V ELF and runs static/dynamic
  Rocket simulators.
- Native placement: LLM calls in Agentix release order alternate GPU0/NUMA0 and
  GPU1/NUMA1. Counts are 5/5, 1/1 and 3/2. Tool calls execute on the NUMA rank
  of their first dependency. Both ranks participate in a final NCCL collective.
- DAG synchronization uses topological waves with a rank barrier between waves;
  a call cannot start before every dependency's prior wave completes.
- Each LLM call consumes its selected upstream MIR list exactly once: 3 VE
  operations (RMSNorm/Add), 3 ME operations (Linear), and 2 DE operations
  (View/Transpose). AgentSys implements these as real CUDA tensor kernels because
  run 039 proves the upstream CUDA op implementation is empty; it is labeled an
  adapter, not upstream mllm inference.
- Matrix extent is `min(1024, 512 + 128*ceil(input_tokens/128))`, rounded by the
  formula itself; FP16, one measured execution per MIR op. CPU preprocessing is
  a real 256x256 FP32 matmul with 16 local threads per rank.
- Native timing uses CUDA events and monotonic host nanoseconds; Rocket timing
  remains simulator cycles. The merged JSONL keeps these clock domains separate
  and never converts one into the other.

## Required artifacts and gates

1. Three hybrid plans have distinct workload hashes and retain application,
   compiled-MIR, generated-header and ELF hashes.
2. Every plan contains all calls once, preserves dependencies, assigns every LLM
   call to one GPU/NUMA rank and every tool call to one CPU/NUMA rank.
3. Native execution uses both distinct GPUs and exact NUMA affinities for every
   workload; LLM counts are 10/2/5 and tool counts 1/1/1.
4. Native MIR operator events are exactly 80/16/40, with per-call 3 ME, 3 VE and
   2 DE events and matching source indices/types from the compiled manifest.
5. H2D, D2H, CPU preprocessing/tool and correct NCCL collective evidence exists
   for each workload; all numeric checksums are finite.
6. Existing static/dynamic Rocket systems pass all gates with 860/180/436 trace
   events and identical per-tile checksums.
7. A merged trace links every native and simulated event by workload hash and
   call ID, includes explicit source/clock domain, and covers Agentix,
   application, mllm, Agent.xpu, CPU, GPU/CUDA/NCCL, RISC-V software, TISA and
   HPTPE layers.
8. `gpu0_only` compilation changes the placement/resource signature relative to
   round-robin without changing calls, dependencies, MIR ops or XPU descriptors.
9. The official mllm CUDA lifecycle audit remains 13/13 and its adapter boundary
   is propagated into every plan/result.
10. A fresh layer matrix remains 68/68 unique paper endpoints at <=10%, with all
    five original parameter sensitivities plus the new GPU placement switch.

The local RTX4090 timings are calibration/real-execution evidence. Agentix's
A100 and other paper platforms remain matching-configuration simulation/RTL
regression, never relabeled as local measurement.

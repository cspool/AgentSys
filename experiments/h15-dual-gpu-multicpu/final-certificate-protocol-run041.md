# H15 final protocol — profiler-backed completion certificate (run 041)

Locked before profiling the integrated workload or implementing the final
certificate. No simulator/runtime performance parameter may change.

## Fresh execution

Profile the frozen run-040 `react_tool` hybrid plan by executing only its native
dual-GPU/dual-NUMA runtime under Nsight Systems 2026.3.1:

- trace CUDA, NVTX and OS runtime; disable sampling/context-switch collection;
- keep the runtime's 3 calls, 2 LLM calls, 16 MIR ops, both GPU ranks, NUMA
  affinity, H2D/D2H and NCCL behavior unchanged;
- export CUDA kernel/API/memory and NVTX summary CSVs;
- require non-empty GEMM, pointwise/normalization, transpose/copy, NCCL,
  H2D/D2H and `agentsys.mllm::<call>::<source>::<type>` ranges.

## Certificate inputs and gates

The certificate must independently verify:

1. run 033's 11/11 native hardware and 9/9 profiler audit;
2. run 039's 13/13 mllm CUDA lifecycle, exact framework-patch hash and explicit
   empty-kernel/no-op-factory boundary;
3. run 040's 4/4 serial stages and 11/11 global gates;
4. three workload/system artifacts, distinct plans/ELFs and exact
   80/16/40 MIR, 133/29/68 native, 860/180/436 Rocket and 993/209/504 merged
   event counts;
5. all per-workload 13/13 native, 9/9 vertical and multi-clock/call-identity
   gates, including persisted NCCL `SHM/direct/direct` logs;
6. five paper layers, five paper sensitivities plus GPU placement sensitivity,
   and 68/68 endpoints at <=10% with maximum 9.91%;
7. fresh run-041 profile evidence and 13/13 native runtime;
8. complete required source/config/script/doc/protocol files and hashes;
9. fresh full pytest, dispatch file-trace, legacy RTL lint and full revised
   HPTPE/RoCC lint.

Evidence boundaries are hard gates: local RTX4090/Xeon timing, A100/Core-Ultra/
Epoch/mobile-NPU simulation targets and HPTPE report/RTL evidence must remain
separately labeled. `full_goal_complete` may be true only if every gate passes.

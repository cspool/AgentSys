# H15 run-041 final analysis — profiler-backed completion certificate

## Outcome

H15 and the expanded AgentSys goal are supported. The final certificate passes
22/22 requirements and sets `full_goal_complete=true`.

- run 033: 11/11 native dual-GPU/NUMA gates and 9/9 baseline Nsight audit;
- run 039: 13/13 mllm CUDA lifecycle gates and exact shutdown patch hash;
- run 040: 4/4 serial stages, 11/11 global gates, three workloads, six switches
  and 68/68 paper endpoints at 10% (maximum 9.91%);
- run 041: 13/13 profiled native runtime and 9/9 integrated Nsight audit;
- fresh checks: 90 pytest tests, mllm CUDA idempotent two-GPU test, TISA dispatch,
  legacy RTL lint and complete HPTPE/RoCC lint all pass.

## Profiler evidence

The frozen `react_tool` plan reruns 3 calls and 16 MIR operations across both
GPU/NUMA ranks. Nsight exports 15 kernel, 45 CUDA API, 3 memory and 20 NVTX
summary rows. All 16 expected `agentsys.mllm::<call>::<source>::<op>` ranges are
present, alongside CUTLASS GEMM, RMS/elementwise, direct copy/transpose and NCCL
kernels, asynchronous CUDA copies and both H2D/D2H directions. The report and
SQLite evidence are 1.83 MB and 6.73 MB.

The fresh runtime records `dtype=float16` and `iterations=1` on every operator,
closing the parameter-consumption check added after run 040. NCCL again uses
`SHM/direct/direct` because peer access is unavailable.

## Completion meaning

One Agent JSON now drives Agentix, mllm MIR, Agent.xpu flow/stage compilation,
real dual-GPU/dual-NUMA execution, RISC-V ELF generation, dual Rocket simulation,
TISA/HPTPE execution, multi-clock trace assembly and paper regression. Switching
the workload or layer configuration requires no source edit.

The certificate does not collapse evidence classes. Local RTX4090/Xeon timing is
real execution; A100/Core-Ultra/Epoch/mobile-NPU paper results remain matched
simulation; HPTPE uses released RTL plus author-report PPA where licensed
synthesis is unavailable. The upstream mllm CUDA backend remains a lifecycle
scaffold, and real MIR kernels remain explicitly an AgentSys adapter.

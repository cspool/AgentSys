# H19 run-049 final analysis — MLX+CPU completion certificate

## Outcome

H19 and the revised objective are supported. The certificate passes 25/25
requirements and sets `full_goal_complete=true`.

- primary system: ordinary single-core Rocket plus selectable MLX cycle or
  physical 4x4/16-PE RTL;
- three switchable Agent DAGs, 20 calls, 17 MLX launches, 3 CPU tools and 765
  lineaged spatial micro-ops;
- six paper layers, 73/73 registered endpoints, six switches, maximum error
  9.91%;
- complete run 048: five strict stages, 24 fresh MLX executions and 10/10 gates;
- auxiliary GPU runtime retained: run 033 native 11/11 + audit 9/9, mllm CUDA
  lifecycle 13/13 and integrated GPU profile 9/9;
- fresh checks: 105 pytest tests, MLX environment/source setup, 12-file Chipyard
  overlay, Icarus cycle compilation and physical-array Verilator lint all pass.

## What is implemented

One Agent JSON drives Agentix scheduling, mllm MIR selection, Agent.xpu
flow/stage metadata, TISA semantic descriptors, a 45-micro-op MLX spatial
lineage, C call-table generation, RISC-V ELF compilation, Rocket dependency/tool
execution, custom0 config/launch/wait/status, HellaCache DMA, MLX cycle/RTL
execution, FP16 golden validation, 14-layer trace composition and paper-layer
regression. Workload/backend/layer switching requires no source edit.

## Evidence boundary

Completion is not a claim that every MLX paper figure was independently
reproduced. MLX_dev is an open surrogate. Its five registered Figure-21 rows are
target-informed (5.85% maximum fit error), not validation; LOO maximum is 20.77%
and strict full-paper completion remains false at 1/18. These limitations are
certificate requirements, not footnotes. HPTPE and native GPU remain optional/
historical evidence and ATX is absent from the active MLX ELF.

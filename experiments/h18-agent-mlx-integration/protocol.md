# H18.1 protocol — Agent DAG to MLX spatial program and Rocket ELF (run 045)

Locked before implementing the Agent-to-MLX compiler, generated call header or
multi-call CPU runtime.

## Vertical input and lowering

Use the three existing Agent manifests unchanged. For each workload, freshly
execute Agentix and compile mllm/Agent.xpu/TISA metadata. Each LLM call selects
the same eight Qwen3 MIR source operators (3 VE, 3 ME, 2 DE); each tool remains
ordinary CPU work.

Lower every LLM call to the run-043/044-qualified MLX Transformer-block spatial
template: 45 instructions over 9 physical PEs, 8 input vectors, 1 output vector,
all ten MLX opcodes and 576 DMA bytes. A machine-readable micro-op lineage maps
every spatial instruction to one of the eight MIR source indices. This is an
AgentSys compiler mapping onto unchanged MLX RTL, not a claim that MLX_dev ships
an Agent compiler.

The generated RISC-V program must:

- enforce every DAG dependency before call execution;
- execute tool calls on ordinary Rocket;
- for each LLM call, configure, launch, wait and query MLX;
- compare every returned vector beat with the FP16 golden;
- print call IDs, program IDs, priorities, Agent.xpu flow/chunk/batch metadata,
  backend/status and per-call hardware counters;
- check ABI magic and aggregate all work.

## Frozen counts

| workload | calls | LLM/tool | MLX instructions | DMA bytes | cycle kernel | RTL kernel |
|---|---:|---:|---:|---:|---:|---:|
| react_moa_mcts | 11 | 10/1 | 450 | 5,760 | 1,320 | 760 |
| react_tool | 3 | 2/1 | 90 | 1,152 | 264 | 152 |
| planner_debate | 6 | 5/1 | 225 | 2,880 | 660 | 380 |

Kernel/DMA/instruction values are sums of independently reset per-call
controller counters. Tool work is excluded from accelerator counts.

## Gates

1. Three source manifests produce distinct workload/application/compiled/header/
   ELF hashes without repository source edits.
2. Application, mllm/TISA compilation and MLX lowering preserve one workload
   SHA and all call/dependency/program identities.
3. Every LLM has 8 MIR sources and a complete 45-micro-op lineage; every spatial
   instruction is assigned exactly once.
4. Both existing Rocket simulators execute all three ELFs (6 runs) with zero
   output mismatches and correct backend/ABI.
5. Every call executes exactly once; dependencies and program boundaries pass;
   LLM/tool/launch counts equal the table.
6. Per-call MLX kernel cycles are 132/76, instructions 45 and bytes 576; summed
   values equal the frozen table.
7. Operation, DMA and `system=DMA+kernel+2` conservation holds per LLM call.
8. Cycle and RTL execute identical logical calls, MIR mapping, arithmetic work,
   DMA and goldens; only schedules/cycles may differ.
9. Traces cover application, Agentix/framework, mllm, Agent.xpu, TISA, ordinary
   CPU, software/ABI, DMA, MLX tag/PE/network and result layers with call IDs.
10. `cycle` versus `rtl` is an executable hardware-backend parameter switch.
11. ATX and HPTPE are absent from the active MLX ELF/runtime/logs.
12. Run 043/044 standalone and system parents remain passing.

Passing run 045 supports workload switching and vertical mechanism integration;
the six-paper-layer numerical matrix and final toolchain certificate remain H19.

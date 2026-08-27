# H18 run-046 analysis — three switchable Agent DAGs on Rocket+MLX

## Outcome

H18 and H18.1 are supported. Three workloads execute serially and all 9 global
gates pass. Each workload passes 10/10 vertical gates on both unchanged Rocket
simulators.

| workload | programs/calls | LLM/tool | MLX micro-ops | cycle kernel | RTL kernel | composed trace |
|---|---:|---:|---:|---:|---:|---:|
| react_moa_mcts | 3/11 | 10/1 | 450 | 1,320 | 760 | 762 |
| react_tool | 1/3 | 2/1 | 90 | 264 | 152 | 158 |
| planner_debate | 2/6 | 5/1 | 225 | 660 | 380 | 385 |

Workload, generated Agent header and ELF hashes are pairwise distinct. All 20
calls execute exactly once, including three real Rocket CPU tools. Seventeen LLM
calls each retain eight mllm/TISA sources and execute the qualified 45-op/9-PE
MLX program with zero golden or ABI errors. Cycle/RTL conserve identical calls,
instructions, operation classes, bytes and logical checksums.

## Cache-aware CPU/accelerator behavior

For every ELF, the first LLM launch pays 344 DMA cycles and later launches pay
216 because the same static arrays remain cache-resident. Both backends have the
same sequence. Aggregate DMA/system values exactly match the recovery protocol:

- react_moa_mcts: DMA 2,288; system 3,628/3,068 cycle/RTL;
- react_tool: DMA 560; system 828/716;
- planner_debate: DMA 1,208; system 1,878/1,598.

Kernel work remains 132/76 cycles per call and bytes remain 576; the cache gain
does not alter accelerator execution or functional data.

## Trace and boundary

Composed traces cover 14 layers from application/Agentix through mllm,
Agent.xpu, TISA, ordinary CPU/software/DMA and MLX tag/PE/SPM/network/result.
Compiler micro-events are explicitly `identity_only` or spatial-program-order;
per-call runtime counters are measured Rocket cycles. Interleaved UART/hardware
stdout is not misrepresented as a lossless per-call physical trace.

ATX and HPTPE are absent from the active ELF/log path. HPTPE and native GPU
evidence remain historical/optional. No MLX paper target is consumed by run 046.

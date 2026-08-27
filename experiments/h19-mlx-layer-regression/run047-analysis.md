# H19.1 run-047 analysis — six-layer 10% matrix

## Outcome

H19.1 is supported. The executable matrix passes 10/10 gates, six configurations
and six output-changing switches. All 73 unique endpoints pass at a uniform 10%
limit; the global maximum remains mllm's 9.91%.

| layer | endpoints | maximum error | executed switch |
|---|---:|---:|---|
| Agentix | 16 | 9.09% | batch 2→1 |
| Agent.xpu | 11 | 8.07% | HEG chunk 16→32 |
| TISA | 10 | 8.27% | ready window 8→2 |
| mllm/llm.npu | 5 | 9.91% | prompt 1024→512 |
| HPTPE | 26 | 0.98% | 9 RTL organizations |
| MLX | 5 | 5.85% | react_tool cycle→RTL, 264→152 |

The MLX sensitivity is a fresh run-047 Agent/Rocket execution. Calls, MIR
mapping, spatial words, bytes, golden and checksum are unchanged. Standalone,
Chipyard and three-workload parents all remain passing.

## Numerical boundary

The MLX N128–2048 values are a same-configuration target-informed three-parameter
regression. They are 5/5 within 10%, but `validation_eligible=false`; maximum
leave-one-out error is 20.77%. The active matrix exports the external strict
full-paper result as false (1/18 within 10%, 17/18 incomplete). Thus 73/73 means
all *registered layer endpoints*, not every numerical figure in the MLX paper.

Primary final hardware is MLX. HPTPE remains a reproduced paper layer and
optional historical backend, not the active Agent ELF accelerator. ATX remains
excluded.

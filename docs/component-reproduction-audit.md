# Revised component reproduction audit

This audit separates historical prototypes from the active final architecture.

| Component | Required standalone mechanism | Current evidence | Active gap |
|---|---|---|---|
| Agentix | PLAS/ATLAS DAG scheduling, routing, KV/SLO behavior | run 025 unchanged: 16/16 endpoints, max error 9.09% | Standalone gate closed; feed real application DAGs into revised integration |
| Agent.xpu | HEG, elasticity, batching, placement, preemption | run 025 unchanged: 11/11 endpoints, max error 8.07% | Standalone gate closed; connect decisions to executable mllm work |
| TISA | semantic ME/VE/DE dependencies and dynamic issue | run 025 unchanged: 10/10 endpoints, max error 8.27% | Standalone gate closed; bind scheduler issue to HPTPE array |
| mllm / llm.npu | chunk-sharing, shadow outliers, out-of-order CPU/NPU subgraphs | run 023: real upstream build, 20/20 executables and 101 gtests; 5/5 paper endpoints, max error 9.91% | Standalone gate closed; connect the tested graph/subgraph contract to Agent.xpu/TISA |
| HPTPE | OPT1/2/3/4C PE arrays, dataflow, compression/sparsity | run 024: 9/9 RTL organizations, 302 golden checks, 9/9 full-scale lint, 26/26 endpoints, max error 0.98% | Standalone gate closed; vendor the tested OPT1 array into the Chipyard XPU |
| CPU | ordinary RISC-V Rocket plus neutral XPU/DMA interface | run 026 executes static/dynamic Rocket with the `xpu_v2` five-command ABI; ATX/prefetch/cancel are absent | Functional path closed; integrated TISA performance gate remains open |

The controlling protocol is
`experiments/h13-revised-stack/protocol.md`. No run through 022 is a completion
certificate for this scope.

Current revised-scope progress: run 025 closes all five standalone components at
68/68 endpoints and 9.91% global maximum error. Run 026 executes the full
ordinary-Rocket-to-HPTPE path and passes 18/19 integration gates, but its 2.000x
backend speedup exceeds the registered TISA 1.14--1.63x range. HPTPE PPA is
author-report replay; RTL functionality, sparse cycles and integrated array work
are newly executed open-simulator evidence.

## Source selection

- mllm official repository: <https://github.com/UbiquitousLearning/mllm>
- llm.npu paper: <https://doi.org/10.1145/3669940.3707239>
- author publication page: <https://xumengwei.github.io/papers.html>
- HPTPE official artifact: <https://github.com/wqzustc/High-Performance-Tensor-Processing-Engines>
- HPTPE paper: <https://doi.org/10.1109/HPCA61900.2025.00058>

Unavailable proprietary platforms (Qualcomm QNN device stack and Synopsys DC)
must be identified explicitly. Source-grounded simulation or author-report replay
does not become device measurement merely because it matches a paper endpoint.

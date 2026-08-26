# Revised component reproduction audit

This audit separates historical prototypes from the active final architecture.

| Component | Required standalone mechanism | Current evidence | Active gap |
|---|---|---|---|
| Agentix | PLAS/ATLAS DAG scheduling, routing, KV/SLO behavior | 16/16 endpoints, open executable substitute | Re-run unchanged under the H13 certificate |
| Agent.xpu | HEG, elasticity, batching, placement, preemption | 11/11 source-grounded endpoints | Re-run unchanged and connect decisions to executable mllm work |
| TISA | semantic ME/VE/DE dependencies and dynamic issue | 10/10 endpoints plus RTL scheduler | Re-run unchanged against the HPTPE engine |
| mllm / llm.npu | chunk-sharing, shadow outliers, out-of-order CPU/NPU subgraphs | run 023: real upstream build, 20/20 executables and 101 gtests; 5/5 paper endpoints, max error 9.91% | Standalone gate closed; connect the tested graph/subgraph contract to Agent.xpu/TISA |
| HPTPE | OPT1/2/3/4C PE arrays, dataflow, compression/sparsity | pinned official RTL/reports; current integrated ME is only a four-lane reference | Execute official RTL, audit PPA reports, implement the tested array in Chipyard |
| CPU | ordinary RISC-V Rocket plus neutral XPU/DMA interface | Rocket path exists but uses an ATX-style legacy runtime | remove ATX semantics from the final software/hardware path |

The controlling protocol is
`experiments/h13-revised-stack/protocol.md`. No run through 022 is a completion
certificate for this scope.

Current revised-scope progress: mllm is independently closed; HPTPE remains the
blocking standalone implementation, followed by unchanged Agentix/TISA/Agent.xpu
revalidation and system integration.

## Source selection

- mllm official repository: <https://github.com/UbiquitousLearning/mllm>
- llm.npu paper: <https://doi.org/10.1145/3669940.3707239>
- author publication page: <https://xumengwei.github.io/papers.html>
- HPTPE official artifact: <https://github.com/wqzustc/High-Performance-Tensor-Processing-Engines>
- HPTPE paper: <https://doi.org/10.1109/HPCA61900.2025.00058>

Unavailable proprietary platforms (Qualcomm QNN device stack and Synopsys DC)
must be identified explicitly. Source-grounded simulation or author-report replay
does not become device measurement merely because it matches a paper endpoint.

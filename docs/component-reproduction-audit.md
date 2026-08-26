# Revised component reproduction audit

This audit separates historical prototypes from the active final architecture.

| Component | Required standalone mechanism | Current evidence | Active gap |
|---|---|---|---|
| Agentix | PLAS/ATLAS DAG scheduling, routing, KV/SLO behavior | run 025: 16/16 endpoints, max error 9.09%; run 027 carries 3 application DAGs/11 calls | closed |
| Agent.xpu | HEG, elasticity, batching, placement, preemption | run 025: 11/11 endpoints, max error 8.07%; run 027 executes flow/stage/placement metadata | closed |
| TISA | semantic ME/VE/DE dependencies and dynamic issue | run 025: 10/10 endpoints, max error 8.27%; run 027 passes 7-cycle dispatch and 1.376x integrated speedup | closed |
| mllm / llm.npu | chunk-sharing, shadow outliers, out-of-order CPU/NPU subgraphs | run 023: real upstream build, 20/20 executables and 101 gtests; 5/5 paper endpoints, max error 9.91%; run 027 consumes upstream MIR | closed |
| HPTPE | OPT1/2/3/4C PE arrays, dataflow, compression/sparsity | run 024: 9/9 RTL organizations, 302 golden checks, 9/9 full-scale lint, 26/26 endpoints, max error 0.98%; run 027 executes 614,400 integrated MACs | closed |
| CPU | ordinary RISC-V Rocket plus neutral XPU/DMA interface | run 027 executes both Rocket systems with the `xpu_v2` five-command ABI; ATX/prefetch/cancel are absent | closed |

The controlling protocol is
`experiments/h13-revised-stack/protocol.md`. No run through 022 is a completion
certificate for this scope.

Current revised-scope progress: run 025 closes all five standalone components at
68/68 endpoints and 9.91% global maximum error. Run 027 closes 20/20 integration
gates on the full ordinary-Rocket-to-HPTPE path; run 026 is retained as the
range-failing predecessor. HPTPE PPA is author-report replay; RTL functionality,
sparse cycles and integrated array work are newly executed open-simulator
evidence. Run 028 closes final packaging with 8/8 serial stages, 12/12 toolchain
gates and 15/15 completion requirements.

## Source selection

- mllm official repository: <https://github.com/UbiquitousLearning/mllm>
- llm.npu paper: <https://doi.org/10.1145/3669940.3707239>
- author publication page: <https://xumengwei.github.io/papers.html>
- HPTPE official artifact: <https://github.com/wqzustc/High-Performance-Tensor-Processing-Engines>
- HPTPE paper: <https://doi.org/10.1109/HPCA61900.2025.00058>

Unavailable proprietary platforms (Qualcomm QNN device stack and Synopsys DC)
must be identified explicitly. Source-grounded simulation or author-report replay
does not become device measurement merely because it matches a paper endpoint.

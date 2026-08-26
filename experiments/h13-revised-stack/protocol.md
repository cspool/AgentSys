# H13 protocol: standalone reproduction before revised-stack integration

## Question

Can the five active components be independently implemented and validated before
they are composed as
`Agent application -> Agentix -> mllm/Agent.xpu -> TISA -> HPTPE XPU` on an
ordinary RISC-V Chipyard system?

ATX is excluded from the CPU and integrated-system design. Its existing results
remain historical only.

## Locked evidence order

1. Reproduce each component in isolation. Integration results cannot close an
   incomplete standalone gate.
2. Build the upstream/open implementation where it exists and execute its real
   functional tests or traces.
3. Execute the locally implemented mechanism without reading paper target values.
4. Compare the resulting metrics with the preregistered values in
   `data/paper_targets.json`; every active component must have maximum absolute
   relative error no greater than 15%.
5. Only after all standalone gates pass, integrate the exact tested modules into
   ordinary-RISC-V Chipyard and issue a new system certificate.

## Active component contracts

### Agentix

Retain PLAS/ATLAS program-DAG scheduling, locality-aware routing, SLO throughput,
KV swap, and offline makespan tests. Re-run the existing 16 endpoints with no
retuning.

### Agent.xpu

Retain HEG construction, reactive/proactive stage elasticity, adaptive batching,
heterogeneous placement, and tile-boundary preemption. Re-run all 11 endpoints
with no retuning.

### TISA

Retain semantic ME/VE/DE dependencies, finite dynamic issue window, RAW/WAR/WAW
checks, and static/dynamic schedules. Re-run all 10 endpoints and the RTL
equivalence tests with no retuning.

### mllm / llm.npu

The performance paper associated by the official mllm repository is *Fast
On-device LLM Inference with NPUs* (ASPLOS 2025, DOI
`10.1145/3669940.3707239`). The standalone reproduction must implement:

- fixed-length chunk graphs with static-subgraph sharing and causal KV
  dependencies;
- shadow outlier execution on CPU/vector resources in parallel with INT8 NPU
  MatMul, including sparse hot-channel storage;
- dependency-correct out-of-order CPU/NPU subgraph execution that prioritizes
  reduction of NPU stalls.

Locked performance anchors are the paper's chunk-sharing speedup range
1.46--5.09x, shadow-outlier speedup range 3.91--8.68x, out-of-order prefill
latency reduction range 18--44%, and the Figure-13 illustrative NPU bubble rates
37% (naive) and 0.7% (out of order). The 22.4x average prefill statement is a
cross-platform headline and is reported as a secondary endpoint, not substituted
for mechanism ablations.

The real pinned mllm C++ framework must build on x86 and execute its trace/operator
tests. The local performance substitute must consume a native mllm graph/IR. It
may model unavailable Qualcomm QNN latency, but it must label that evidence as
source-grounded simulation rather than Xiaomi/Redmi hardware measurement.

### HPTPE

The official HPCA 2025 artifact at pinned revision `ebe4db7d` is the source. The
standalone reproduction must use the actual released RTL for:

- OPT1 compressed accumulative PE arrays in OS, WS, and Cube organizations;
- OPT2 same-bit-weight compressor array;
- OPT3 sparse-encoding PE and OPT4C column array.

Functional tests compare RTL outputs with signed integer GEMM/vector golden
results. Performance/PPA endpoints cover the successful-frequency and total-cell
area entries for OPT1, OPT2, and OPT4C plus the published OPT3/OPT4C average
calculation cycles. The checked-in Synopsys DC reports must be parsed directly and
cross-checked against the README tables.

The SAED32 `.db` and DC reports are author-supplied artifacts. Re-parsing them is
not claimed as a fresh open-source synthesis run. Functional Verilator execution
and project-owned cycle/storage/dataflow simulation are the independently
executable evidence; report replay preserves the original PPA evidence boundary.

## Integration acceptance

After all standalone results pass:

- the CPU is a standard Rocket/RISC-V core and exposes only neutral command,
  status, and DMA interfaces;
- mllm operators retain native identities, shapes, dtypes, and SSA dependencies;
- Agent.xpu flow/stage placement is represented in executable software and trace,
  not metadata-only annotations;
- TISA lowers ready work to the same HPTPE array implementation tested above;
- static and dynamic systems execute the same RISC-V ELF and preserve logical
  work, DMA bytes, output checksum, and dependency lineage;
- the new certificate excludes ATX endpoints and rejects the previous simplified
  four-lane ME as final HPTPE evidence.

## Prediction

The independently implemented mllm/llm.npu schedule will move all four
mechanism-level performance anchors inside 15%, and executable HPTPE RTL/report
replay will reproduce all registered endpoints inside 15%. Their composition will
preserve correctness and most XPU-local improvement, while application-level gain
will be lower because ordinary-RISC-V control and DMA overhead dilute accelerator
speedup.

## Confirmatory versus exploratory

The targets and gates above are confirmatory. Build-system compatibility fixes,
additional workloads, alternative HPTPE array sizes, and integration tuning are
exploratory until separately registered.

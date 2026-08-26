# Literature and implementation survey

## Agentix

- Source: Michael Luo et al., *Agentix: An Efficient Serving Engine for LLM Agents as General Programs*, NSDI 2026.
- Mechanism: PLAS ranks a single-thread program's next call by cumulative completed call service. ATLAS generalizes the priority to the maximum accumulated service along active DAG threads, approximating critical-path progress. A stateful load balancer trades engine load for program KV locality.
- Registered results: PLAS toy total wait 12 versus FCFS/MLFQ 18; high-load throughput ratios up to 8×/2×/1.5× versus vLLM/vLLM-opt/MLFQ on single-thread workloads; LATS 5×/2×/2.5× versus vLLM/vLLM-opt/MLFQ; mixed 15×/5×/5.5× versus vLLM/vLLM-opt/MLFQ; offline makespan reduction 10–40%; swap count 18× lower and swap time 3–7× lower.
- Relevance: program-level ground truth for H1 and top-level policy in H4.
- Open implementation status: no author-official repository was found. A non-author-verified public vLLM fork (`kungfu-team/autellix`, `autellix-scheduling`, `1df1987`) is pinned as a policy reference; its 58 pure-Python tests pass. Aggregate performance is produced by the project-owned serving substitute simulator.

## Agent.xpu / LLM.xpu

- Source: Xinming Wei et al., *Agent.xpu: Efficient Scheduling of Agentic LLM Workloads on Heterogeneous SoC*, arXiv:2506.24045; implementation reference pinned at `689be270aa29bb88447e3867cd97d85a55f454d5`.
- Mechanism: HEG captures operator affinity; prefill is elastically coordinated across NPU/iGPU while decode uses dynamically batched iGPU execution; reactive-first batching and fine-grained preemption bound foreground delay.
- Registered results: Llama-3B proactive throughput 2.0–2.4× OpenVINO; reactive mean-latency reductions 91.61/93.84/96.01% (3B) and 96.23/96.01/96.70% (8B) at reactive rates 1/3/5; reactive prefill pending time 0.048 s; iGPU utilization reductions 32.5/37.1% versus serial NPU-iGPU/OpenVINO; energy reduction 26.8% versus OpenVINO.
- Relevance: flow/stage policy for H2 and the open C++ behavior used to cross-check the simulator.

## ATX

- Source: Gerasimos Gerogiannis et al., *ATX: Accelerator Task Extensions*, ISCA 2026.
- Mechanism: ATX instructions reside in the CPU ROB, wake and issue out of order when renamed inputs are ready, invoke near-core accelerators through a Unified Transfer Engine, and return results before in-order retirement. The UTE virtualizes multiple accelerators and supports task prediction/prefetch and double-buffered scratchpads.
- Registered results: ATX NCA versus core 2.8×/2.7×/2.7× for SpMM/SDDMM/GeMM; versus ICA 2.3×/2.0×/1.3×; versus L2 OCA without prefetch 1.6×/1.4×/1.3× and with prefetch 2.1×/2.0×/1.4×; versus LLC OCA 9.4× at 8 KiB tasks and 2.6× at 128 KiB; decompression 4.0×/1.8×/3.9×/18× versus core/ICA/L2 OCA/LLC OCA.
- Relevance: asynchronous task and prefetch contract for H3; source paper used a private Sniper-derived simulator.
- Open implementation status: the private Sniper extension was not found on the author/project pages. The project therefore implements the published ATX Queue/UTE/NCA resources in an open event simulator and validates the ISA/RTL path separately in Chipyard.

## TISA

- Source: Guanghui Song et al., *Dynamic Scheduling for AI Accelerators via TISA*, ISCA 2026.
- Mechanism: TISA preserves OpType, UnitMap, TileMem, access type/scope, and typed dependencies. Per-unit waiting queues and in-flight semantic tables allow runtime RAW/WAR/WAW and memory-range checks before dynamic ME/VE/DE issue.
- Registered results: Dynamic versus Naive 1.52× ResNet50, 1.79× BERT, 1.74× GPT-J, 1.92× LLaMA2; versus strong static scheduling an additional 1.14–1.63×; FA3 head-dim-128 utilization 26.4% higher than H100. Window 8 dispatch is 7 cycles, 1.5M gates, 0.25 mm², 100 mW.
- Relevance: tile-level scheduler and hardware structure for H3/H4; no public Epoch RTL/simulator exists.

## Engineering references

- `cspool/MLX_dev`, branch `sys`, commit `b3a6d59`: same Chipyard `b5d01319` integration, bare-metal custom0 runtime, HellaCache DMA, Verilator and PE-array patterns. Used only for plumbing.
- `wqzustc/High-Performance-Tensor-Processing-Engines`: matrix-engine RTL patterns for the ME datapath.
- `UbiquitousLearning/mllm`: model graph/operator tracing and backend integration point.
- `kungfu-team/autellix@1df1987`: independent public vLLM policy fork used only as a PLAS/ATLAS/anti-starvation reference oracle.
- `snipersim/snipersim`: public base identified for ATX; the paper's private UTE/NCA extension is unavailable, so it is not treated as executable ATX evidence.

# H1–H4 paper-contract protocol (locked before run 001)

## Classification

Confirmatory for the listed paper endpoints and functional invariants. Any parameter or workload added after inspecting run-001 residuals is exploratory until validated against a separately locked holdout.

## Implementation under test

1. A deterministic program/DAG event simulator with FCFS, MLFQ, PLAS, and ATLAS.
2. A heterogeneous flow scheduler with static, HEG, reactive-first batch, warmup, and tile-boundary preemption modes.
3. An ATX adapter with bounded queue, asynchronous completion, cancel, double buffers, and optional predictive prefetch.
4. A TISA scheduler with ME/VE/DE waiting queues, an issue window, memory-scope/range RAW/WAR/WAW checking, dynamic issue, completion feedback, and inherited priority.
5. One unified `program -> call -> flow -> task -> tile -> engine` event stream whose IDs and priorities can be audited.
6. The same ATX/TISA command/status contract implemented as a custom0 Chipyard RoCC accelerator and exercised by a real Rocket bare-metal ELF under Verilator.

## Hard functional gates

- Every submitted node completes exactly once; no event references an unknown parent.
- A child begins only after all declared parents satisfy the configured dependency condition.
- Overlapping memory regions never violate RAW, WAR, or WAW order; disjoint ranges may overlap.
- Reactive priority is inherited at every layer and cannot be inverted by a queued proactive descendant once a legal preemption boundary is reached.
- Baseline and optimized runs consume identical logical work and inputs.
- The Chipyard ELF exits zero, reports the expected ABI magic, and its counters obey submitted = completed + canceled and per-engine issue conservation.

## Preregistered numerical endpoints

All relative errors are `abs(observed - target) / abs(target)` and must be at most 0.15. Range claims pass only when the observed value lies inside the published range or is within 15% of the nearest bound.

### Agentix

- Toy total wait: FCFS 18, MLFQ 18, PLAS 12.
- ShareGPT/BFCL high-load ratios: Agentix/vLLM 8.0, Agentix/vLLM-opt 2.0, Agentix/MLFQ 1.5.
- LATS ratios: 5.0, 2.0, 2.5 respectively.
- Mixed ratios: 15.0, 5.0, 5.5 respectively.
- Offline makespan reduction range: 10–40%.

### Agent.xpu

- Llama-3B proactive throughput versus iGPU: 2.0–2.4×.
- Mean reactive latency reductions at rates 1/3/5: 91.61/93.84/96.01% for 3B and 96.23/96.01/96.70% for 8B.
- Reactive prefill pending time: 0.048 s.
- iGPU utilization reductions: 32.5% versus serial NPU-iGPU and 37.1% versus iGPU.
- Energy reduction versus iGPU: 26.8%.

### ATX

- Versus core for SpMM/SDDMM/GeMM: 2.8/2.7/2.7×.
- Versus ICA: 2.3/2.0/1.3×.
- Versus L2 OCA, no prefetch: 1.6/1.4/1.3×; full ATX: 2.1/2.0/1.4×.
- Versus LLC OCA: 9.4× (8 KiB) and 2.6× (128 KiB).
- Decompression versus core/ICA/L2 OCA/LLC OCA: 4.0/1.8/3.9/18×.

### TISA

- Dynamic versus naive for ResNet50/BERT/GPT-J/LLaMA2: 1.52/1.79/1.74/1.92×.
- Dynamic versus static: within 1.14–1.63×.
- FA3 utilization improvement: 26.4%.
- Window-8 scheduler dispatch latency: 7 cycles.

## Primary metric and stopping rule

The primary metric is the maximum error across endpoints supported by an executed, source-grounded workload. Run 001 is not tuned to paper numbers. If it fails, the next protocol must identify a mechanism or measurement mismatch from source/trace evidence; direct per-endpoint scale factors are forbidden. Completion requires all hard gates, every named implementation, real Chipyard execution, and every claimed reproduced endpoint within 15%.


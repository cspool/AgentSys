# h22 llm strand — AutoTrace w01–w05 on real model-inference-as-agent (single RTX 4090)

Lineage `h22-gpu-autotrace/llm`, completed 2026-09-12. Every LLM call of the three
agent workloads runs real Qwen3-1.7B prefill + greedy decode through the
user-supplied `transformers 4.57.6` (sdpa attention, bf16, eager execution), on
physical GPU 1 (RTX 4090, PCI B1:00.0), CPU affinity 16-31,48-63, NUMA 1. Tool
calls keep the certified CPU matmul adapter. Runtime:
`experiments/h22-gpu-autotrace/code/single_gpu_hf_llm_agent_runtime.py` +
`hf_qwen3_backend.py` (NVTX per forward stage: `{phase}_embed`,
`{phase}_layerNN`, `{phase}_head`, `{phase}_sample`; model probe greedy
"The capital of France is" → " Paris"). Warmup 2 iterations discarded, 3
measured iterations traced.

## Chain results

| Goal | Workflow | Result |
|---|---|---|
| G01 | w01 nsys operator trace | 3/3 pass, 0 unattributed GPU work in window. GPU busy median: react_tool 18.77 %, planner_debate 18.40 %, react_moa_mcts 19.55 % |
| G02, G03 | w02 call/process attribution | 3/3 pass, segment conservation error 0 ns, GPU total equals w01 exactly. react_moa_mcts needed the robust constant-offset clock criterion (99.999 % of 79 980 pairs within ±200 µs; isolated preemption outliers) |
| G04 | w03 NCU hardware | pass. react_tool 6 568/6 568 in-range kernels joined (+40 outside ranges: rotary precompute); planner_debate 16 126/16 126 joined (+90 outside), complete after a per-call fill run: the first session crashed at `planner-final` 913/3 214, and a dedicated measured-only-NVTX session recollected that call in full (`merge_provenance.json`) |
| G05 | w04 full-workload estimate | pass. react_moa_mcts predicted from react_tool+planner_debate templates: wall +3.62 %, GPU −2.13 %, zero instance-count mismatches; every ≥1 %-share process within ±6.4 % except `inter_operator_dispatch` (−49.7 %) |
| G06–G10 | w05 selective trace + resource gap | pass (`--rollup-layers`). Selection = `mir_operator:decode_layer*` in all three workloads (91.6–92.2 % of process host time) |

## What the llm strand shows (vs the base/scaled native strands)

1. **The bottleneck moved from the host adapter to real decode.** Native plans
   were 2–3 % GPU busy with 56–75 % of wall in host `uniform_` input
   generation. With real inference the GPU is ~19 % busy and 92 % of host time
   sits in the decode layer stages.
2. **Decode GPU time is weight-bandwidth-bound.** cuBLAS `gemvx` (batch-1
   matrix-vector over bf16 weights) is 62 % of all GPU time; NCU: DRAM active
   74 %, L2 47 %, SM 15 %, occupancy 16 %, 0.67 waves/SM. Prefill GEMM instead:
   SM 33 %, L2 67 %. Flash sdpa attention is only 4.2 % of GPU time (short
   contexts ≤ 750 tokens).
3. **~80 % of wall is GPU-idle host time from Python eager per-kernel
   dispatch.** Each decode forward launches ~1 700 tiny kernels (median ~1–2 µs)
   from Python; per-layer host time ≫ GPU time (gpu_busy 19 % vs host_only-owning
   segments 81 % upper bound in `g08_opportunities.csv`). The g08 note text
   inherited from the native strand says "cudaEventSynchronize per operator";
   in this strand there is no per-operator sync — the gap is launch/dispatch
   latency. The concrete levers are CUDA graphs / `torch.compile` /
   kernel fusion, which the AutoTrace method surfaces as the
   `gpu_idle_window` bound (80.5–81.9 % of wall).
4. **All non-GEMV kernels are launch-latency-bound**, not resource-bound:
   elementwise/copy/reduce families run at < 4 % of any unit's peak with
   waves/SM ≈ 0. Fusing them changes wall time only through launch count, not
   through GPU throughput.
5. **Full-workload prediction works at +3.6 %** using per-stage medians keyed
   by (call kind, matrix size, process, op type) — the llm enumerator
   (`analyze_w04_llm_full_workload_estimate.py`) counts one prefill +
   (output_tokens−1) decode forwards per call.

## Artifacts

```text
artifacts/gpu_autotrace/llm/
  g01_operator_trace/<w>/            nsys-rep, sqlite, native trace, analysis/
  g02_g03_call_process/<w>/
  g04_ncu_hardware/{react_tool,planner_debate}/ + analysis/
  g05_full_workload_estimate/react_moa_mcts/
  g06_g10_selective_resource_gap/
  ncu_plans/<w>/hybrid-plan.json     reduced plans (real prompts, 2 output tokens)
```

Known deviations, all recorded in provenance: (a) planner_debate NCU was
collected in two sessions — the first crashed at `planner-final` (profiler
crashes also revoked the container's GPU access; host restarts required), and
a per-call fill session (warmup NVTX suppressed via
`AGENTSYS_NVTX_MEASURED_ONLY=1`, filter `regex:agentsys.mllm::planner-final::/`)
completed it; rows merged with unit normalisation per `merge_provenance.json`; (b) `analyze_w01`'s kernel-family map
extended with `gemv` / `attention` / `concat`; (c) w02 clock alignment gained
the robust constant-offset criterion; (d) w03 order contract applies to
in-range kernels, out-of-range rotary precompute is counted separately;
(e) w05 `--rollup-layers` groups per-layer processes into stage types for the
10 % selection rule.

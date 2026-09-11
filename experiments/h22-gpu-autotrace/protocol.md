# h22 — AgentSys single-GPU AutoTrace-style analysis

## Objective

Apply the AutoTrace w01–w05 serial method chain to AgentSys's own agent
workloads, measured as **real execution on a single RTX 4090**. No simulator
evidence (Rocket RTL / MLX cycle model) enters this chain.

## Chain position

w01–w05 is one serial method chain executed once inside a single lineage.

| Workflow | Goal | AgentSys mapping |
|---|---|---|
| w01 | G01 | Operator-wise end-to-end NVTX/CUDA trace — conservation denominator |
| w02 | G02, G03 | Call-wise (agent-node) attribution inside the w01 denominator |
| w03 | G04 | Hardware counters (Nsight Compute PMC) for the representative operators |
| w04 | G05 | Full-workload operator estimate from w01/w02 measured rates |
| w05 | G06–G10 | Guided selective trace + resource gap analysis |

Constraints inherited from AutoTrace:

- No "run w05 only": G06–G10 admission requires the complete ordered G01–G05 handoff.
- The chain runs once; interruption resumes at the first incomplete Goal.
- Downstream consumes upstream artifacts and does not re-prove them.

## Hard constraints for this lineage

- **Single GPU.** Device 1 (PCI `00000000:B1:00.0`), the less loaded of the two
  4090s, fixed for the whole chain. No NCCL, no multi-rank evidence.
- **No modification of `src/agentsys/`.** run_052 certifies a durable source
  closure over that tree; this lineage imports from it read-only and keeps all
  new code under `experiments/h22-gpu-autotrace/code/`.
- **No large-file network transfer.** Everything stays on local disk. Nothing is
  pushed, uploaded, or fetched.
- **Warmup is mandatory.** The shipped plans use `operator_iterations: 1`, so the
  existing run_041 trace is cold-start dominated (LinearOp 216 ms vs RMSNormOp
  0.33 ms). w01 must separate warmup from measured iterations or the denominator
  is meaningless.

## Workloads

| Workload | Calls | LLM / tool | MIR operators |
|---|---:|---|---:|
| react_tool | 3 | 2 / 1 | 16 |
| planner_debate | 6 | 5 / 1 | 40 |
| react_moa_mcts | 11 | 10 / 1 | 80 |

Operator mix per workload is `RMSNormOp`, `AddOp`, `LinearOp`, `ViewOp`,
`TransposeOp`; engines are ME / VE / DE.

## Artifact root

```text
artifacts/gpu_autotrace/<goal>/<workload>/
```

## Status (2026-09-11)

| Goal | Workflow | base strand (run_040 plans as shipped) | scaled strand (matrix x4, 32 op iters, react_moa_mcts x3) |
|---|---|---|---|
| G01 | w01 `run_w01_operator_trace.sh` + `analyze_w01_operator_trace.py` | 3/3 workloads pass, 0 unattributed GPU items | 5/5 plans pass (incl. `_it1` variants used for NCU) |
| G02, G03 | w02 `analyze_w02_call_process_trace.py` | 3/3 pass, segment conservation error 0 ns, GPU total equals w01 | 5/5 pass |
| G04 | w03 `run_w03_ncu_representative.sh` + `analyze_w03_ncu_hardware.py` | react_tool + planner_debate, 147 kernels joined 147/147 | react_tool_L_it1 + planner_debate_L_it1, 147/147 |
| G05 | w04 `analyze_w04_full_workload_estimate.py` | react_moa_mcts from react_tool+planner_debate: -10.6 % | react_moa_mcts_x3_L: -0.07 % |
| G06-G10 | w05 `analyze_w05_selective_trace_resource_gap.py` | selection = host_input_generate (+adapter_dispatch on react_tool) | selection adds LinearOp and RMSNormOp |

Summary: `artifacts/gpu_autotrace/H22_LINEAGE_SUMMARY.md` (copy in `results.md`), written by `write_lineage_summary.py`.

Artifact layout under `artifacts/gpu_autotrace/`: `g01_operator_trace/<w>/` (nsys-rep, sqlite, native trace, `analysis/`),
`g02_g03_call_process/<w>/`, `g04_ncu_hardware/<w>/` + `analysis[_scaled]/`, `g05_full_workload_estimate/<target>/`,
`g06_g10_selective_resource_gap/<strand>/`, `scaled_plans/<w>/hybrid-plan.json`. Total about 0.5 GB, all local.

### Decisions recorded during the run

- The w02 process-wise handoff is derived from the w01 trace itself (host events aligned to the nsys clock by a
  constant offset, spread 13-39 us), so no second instrumentation round was needed; `src/agentsys/` is untouched.
- nsys Python sampling produced no tables in this build and was dropped; a microbenchmark (`uniform_` on 768x768 fp16:
  5.0 ms, on 1024x1024: 8.8 ms, CPU generator, single thread) explains `host_input_generate` independently.
- NCU GEMM throughput is reported as TFLOPS from the replay at locked base clock; the utilisation reference is
  `tensor_pipe_active_pct` because the cuBLAS kernel accumulates in FP16.
- The 20260910 `docker_model` mount now holds `Qwen3-1.7B` and `Qwen2.5-VL-3B-Instruct`. No transformer library is
  installed and downloads are excluded, so the real-model strand is **pending the user's own library sources**.
  `qwen3_local.py` / `single_gpu_llm_agent_runtime.py` are a validated fallback (greedy "The capital of France is" ->
  " Paris") that the user asked not to pursue further; they are not part of any goal above.

### Resume rule

Interruption resumes at the first goal whose `pass` flag is false in its `conservation.json` / `summary.json` /
`tables_manifest.json`; every downstream script refuses admission on a failed or sha-mismatched upstream.

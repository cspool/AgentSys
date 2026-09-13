# h22 llm_vl strand — AutoTrace w01–w05 with Qwen2.5-VL-3B-Instruct as the agent LLM (single RTX 4090)

Lineage `h22-gpu-autotrace/llm_vl`, completed 2026-09-12. Identical method and
runtime to the llm strand, with every LLM call running the **Qwen2.5-VL-3B-Instruct**
language tower (36 layers, hidden 2048, 7.51 GB bf16 weights; text-only calls,
vision tower untouched) via the user-supplied transformers 4.57.6 (sdpa,
`AutoModelForImageTextToText` load path, hooks on `model.language_model`).
Probe: greedy "The capital of France is" → " Parisian region". GPU 1, warmup 2 /
measured 3, same run_040 plans.

## Chain results

| Goal | Result |
|---|---|
| G01 | 3/3 pass, 0 unattributed. GPU busy median: react_tool 24.23 %, planner_debate 24.61 %, react_moa_mcts 24.74 % |
| G02/G03 | 3/3 pass, conservation 0 ns |
| G04 | pass. **Per-call NCU sessions from the start** (7 sessions × 3 190 kernels, zero crashes): react_tool 6 380/6 380 and planner_debate 15 950/15 950 in-range kernels joined; merges in each workload's `merge_provenance.json` |
| G05 | pass. react_moa_mcts wall −3.03 %, GPU −1.31 %, zero instance mismatches |
| G06–G10 | pass (`--rollup-layers`). Selection `mir_operator:decode_layer*` 91.7–92.3 % in all three workloads |

## Qwen2.5-VL-3B vs Qwen3-1.7B (same DAGs, same 4090)

| Measure | Qwen3-1.7B (llm) | Qwen2.5-VL-3B (llm_vl) |
|---|---:|---:|
| GPU busy (median) | 18.4–19.6 % | 24.2–24.7 % |
| gemv share of GPU time | 61.0 % | **73.7 %** |
| gemv DRAM active (NCU median) | 75.0 % | 74.3 % |
| gemm (prefill) tensor pipe | 40.2 % | 39.9 % |
| gpu_idle_window bound | 80.5–81.9 % of wall | 75.8 % of wall |
| w04 prediction error (wall) | +3.62 % | −3.03 % |
| w05 selection | decode_layer* ~92 % | decode_layer* ~92 % |

Reading: the 2.2× larger weight set makes decode even more gemv-dominated
(73.7 % vs 61.0 % of GPU time) and lifts GPU busy by ~5 points, while the
per-kernel hardware picture is unchanged — gemv sits on the same ~74 % DRAM
active wall and everything else stays launch-latency-bound. The host-dispatch
ceiling (gpu_idle_window) drops from ~81 % to ~76 % because each launched
kernel does more work, not because dispatch got cheaper. Conclusion of both
real-model strands: on batch-1 agent serving the levers are CUDA graphs /
compile / fusion for the ~76–81 % idle wall, then weight quantisation against
the ~74 % DRAM wall; model size moves the balance between the two but not the
walls themselves.

## Artifacts

```text
artifacts/gpu_autotrace/llm_vl/
  g01_operator_trace/<w>/  g02_g03_call_process/<w>/
  g04_ncu_hardware/{react_tool,planner_debate}/call_<call>/ + analysis/
  g05_full_workload_estimate/react_moa_mcts/  g06_g10_selective_resource_gap/
  ncu_plans/<w>/
```

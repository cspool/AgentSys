# Run 023 mllm / llm.npu standalone analysis

## Outcome

The mllm standalone gate passes, but only for the evidence explicitly available
in this environment:

- the pinned upstream mllm v2 C++ runtime and CPU backend build and execute;
- the three ASPLOS'25 llm.npu mechanisms execute in a source-grounded event
  model driven by the native Qwen3 QNN-AOT MIR/config;
- this is not a Qualcomm phone/QNN measurement and does not reproduce the
  paper's cross-platform 22.4x headline.

## Real framework execution

The official `tasks/build_x86.yaml` initially exposed three environment issues:
system CMake 3.10 was too old, submodules were absent, and GCC 10 did not provide
the C++20 level required by NVIDIA stdexec. The locked reproduction config
`mllm-build-clang16.yaml` uses CMake 3.31, Clang 16, the exact upstream submodule
commits, single-thread execution because `libomp` is unavailable, and an explicit
Linux `libdl` link required by the upstream CMake files.

The resulting runtime, CPU backend, IR/JIT, quantization utilities, tests and
benchmarks build successfully at mllm commit `50ad5a9b`. Twenty selected native
test executables pass, covering 101 gtest cases; one external-tokenizer oracle is
skipped by upstream design. The first unfiltered CPU-kernel run is retained as
`mllm-native-run_023-initial.json`: 19/20 executables pass, while the combined
CPU suite reports explicitly NYI x86 FP16/divide/clip operators and subsequently
crashes. The locked gate filters only the x86-supported operator set (37/37
cases) and records the omitted NYI list instead of hiding it.

## llm.npu mechanisms

The native MIR contains 1,602 executable operators. Its first decoder block has
57 operators: 30 shareable static operators and 27 attention/shape-dependent
operators. The native configuration supplies 28 layers and the MIR supplies a
32-token chunk shape.

| Mechanism endpoint | Observed | Paper target | Error |
|---|---:|---:|---:|
| Chunk-sharing graph speedup | 1.974x | 1.46--5.09x | 0% range error |
| Shadow-outlier speedup | 6.600x | 3.91--8.68x | 0% range error |
| Out-of-order latency reduction | 32.907% | 18--44% | 0% range error |
| Naive NPU bubble rate | 33.333% | 37% | 9.91% |
| Out-of-order NPU bubble rate | 0.636% | 0.7% | 9.15% |

The schedule executes 4,480 subgraphs and checks 18,336 causal/intra-chunk
dependencies in each mode. Naive and out-of-order runs preserve exactly 1.26 s
of modeled NPU work and 0.63 s of CPU work. Out-of-order scheduling reduces
makespan from 1.890 s to 1.268064 s (1.490x), with 8.064 ms total online-dispatch
overhead. Five of five preregistered endpoints pass; maximum error is 9.91%.

## Evidence boundary

The 315 ms NPU profile, approximately 2:1 NPU/CPU split, 8.1--10.7x per-group
overhead, 0.1--0.3% outlier density, 85% pruning, and microsecond scheduler are
paper-sourced. The graph topology, layer count, chunk shape, static fraction and
operator digest come from the executed pinned mllm tree. The simulator never
reads `data/paper_targets.json` until after execution when the scorer computes
errors.

The average 22.4x prefill headline remains `not_comparable_cross_platform_average`
because reproducing it requires five original baselines on two Qualcomm phones.

## Artifacts

- `artifacts/results/paper-mllm-run_023.json`
- `artifacts/results/mllm-native-run_023.json`
- `artifacts/results/mllm-native-run_023-initial.json`
- `artifacts/results/mllm-npu-run_023.json`
- `artifacts/traces/paper-mllm-run_023-{naive,ooo}.jsonl`

Replay:

```bash
bash scripts/build_mllm_native.sh
.venv/bin/python scripts/run_mllm_reproduction.py
```

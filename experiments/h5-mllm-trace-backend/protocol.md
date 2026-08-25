# H5 protocol: mllm MIR operator trace to AgentSys simulator backend

## Objective

Add a project-local backend that consumes real mllm v2 MIR operator traces and lowers them into the same TISA/ME/VE/DE contract used by Chipyard. This is an integration requirement, not a new paper-number fit.

## Pinned source

- mllm commit `50ad5a9b6fbea742e38b5b31776c187e50319c8e`.
- Primary smoke input: upstream `tests/compile/ir/TraceFooNetTest.mir`.
- Model-scale input: upstream `examples/qwen3_qnn_aot/qwen3_qnn_aot_1.7B.mir`.

## Locked lowering

- Parse only executable `linalg.<device>.<Op>` lines; ignore parameter registration and graph/control declarations.
- Recover SSA input/output IDs, tensor shapes, dtype, and producer dependencies.
- Engine mapping:
  - ME: Linear, MatMul, Embedding and attention matrix kernels.
  - VE: arithmetic, normalization, activation, softmax, reduction, comparison/select.
  - DE: view/reshape, transpose, slice, concat, repeat, cast, copy, index/cache/data movement.
- Assign deterministic memory spans from SSA IDs, READ inputs and WRITE outputs; dependency edges come only from the SSA producer map.
- Duration is a documented shape-derived estimate by engine, capped for tractable model-scale execution. No paper target enters lowering.

## Gates

- Every parsed output SSA has at most one producer and every dependency precedes its consumer.
- Upstream FooNet parses four Linear ops and maps all four to ME.
- Qwen3-1.7B trace parses nonzero ME/VE/DE operators, preserves the exact selected operator count, and produces deterministic output/digest across reruns.
- Static and dynamic simulations consume identical tile/engine work; dynamic must expose at least one cross-engine overlap on a decoder-layer slice.
- Export operator JSONL, TISA result JSON, counts, source/commit/hash, and unified lineage IDs.

The backend is explicitly a consumer of mllm's native MIR trace, not a claim that mllm executes the simulated timings on its CPU/NPU backends.


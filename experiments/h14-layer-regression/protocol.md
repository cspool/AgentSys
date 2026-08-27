# H14.2 protocol: executable per-layer parameter matrix

## Question

Can every active layer consume a machine-readable configuration, demonstrate a
real parameter switch, and reproduce its paper endpoints under the matching
workload/configuration with at most 10% error?

## Active layers and paper baseline identity

1. **Agentix** — Figure-2 call DAG, batch size 2, registered queue bounds/quanta,
   FCFS/MLFQ/PLAS plus executable aggregate serving workloads.
2. **Agent.xpu** — 3B/8B mixed Poisson flows, registered rates/seeds/durations,
   HEG/iGPU/Serial and a fully serialized `XPUConfig`.
3. **TISA** — ResNet50/BERT/GPT-J/LLaMA2 and FA3 workloads, 32 iterations,
   window 8 and seven-cycle dispatch.
4. **mllm/llm.npu** — pinned native Qwen MIR, `LlmNpuConfig`, chunk-sharing,
   shadow-outlier and naive/out-of-order subgraphs.
5. **HPTPE** — nine named official RTL organizations with their actual module
   parameters plus the exact author DC report points.

The matrix file, target file, workload/config payload and produced result all
receive SHA-256 identities. A declared configuration that is not actually
consumed by the runner is a hard failure.

## Parameter-switch experiments

- Agentix: paper batch size 2 versus batch size 1.
- Agent.xpu: paper 16-token HEG prefill chunk versus 32 tokens.
- TISA: paper window 8 versus window 2.
- mllm: paper 1024-token schedule versus 512 tokens (same 32-token chunks).
- HPTPE: execute all OPT1 OS/WS/Cube, OPT2, OPT3 and OPT4C organizations and
  verify their distinct parameter signatures/results.

Each switch must preserve logical workload validity and change at least one
declared performance/work metric. No endpoint target may be read by simulator
execution code; targets are used only by the audit step.

## Confirmatory gates

- Exactly five active layers; ATX absent.
- Exactly 68 unique baseline endpoints: 16/11/10/5/26.
- Every endpoint uses `limit=0.10`, passes and has <=10% relative error.
- Every layer result records a matching matrix configuration SHA and workload
  identity.
- All five parameter switches execute and change the expected metric.
- Existing standalone native/RTL functional gates remain passing.
- The three run-030 end-to-end workload pipelines remain passing after the
  configuration refactor.

## Prediction

Baseline errors remain Agentix 9.09%, Agent.xpu 8.07%, TISA 8.27%, mllm 9.91%
and HPTPE 0.98%. Sensitivity variants are not paper endpoints; they demonstrate
that configuration fields drive execution rather than serving as inert metadata.

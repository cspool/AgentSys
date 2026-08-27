# H14.2 run-031 analysis — executable layer parameter regression

## Outcome

H14.2 is supported. One machine-readable matrix drives all five active layer
implementations, reruns their matching paper workloads/configurations and passes
68/68 unique endpoints at a uniform 10% limit. Maximum error is 9.91%.

| Layer | Endpoints | Maximum error | Executed parameter switch | Baseline → variant metric |
|---|---:|---:|---|---:|
| Agentix | 16/16 | 9.09% | batch size 2→1 | FCFS wait 18→57 |
| Agent.xpu | 11/11 | 8.07% | HEG chunk 16→32 | reactive mean 4.0638→4.0026 s |
| TISA | 10/10 | 8.27% | window 8→2 | LLaMA2 dynamic 6,977→7,427 cycles |
| mllm/llm.npu | 5/5 | 9.91% | prompt 1,024→512 | tasks 4,480→2,240 |
| HPTPE | 26/26 | 0.98% | 9 RTL organizations | 5 distinct parameter signatures |

## Configuration identity

The result records the matrix raw/canonical SHA-256, target-file SHA-256, each
baseline and variant configuration SHA-256, the executed configuration returned
by the simulator and the paper workload name. All five
`configuration_consumed` gates pass; the sensitivity configurations are not inert
metadata.

## Accuracy contract

All endpoint records are re-audited with `limit=0.10`, including mllm and HPTPE
whose earlier revised certificate allowed 15%. Counts are exactly
16/11/10/5/26 and names are globally unique. Simulator execution occurs before
target comparison; targets are used only to compute error/pass fields.

## Functional preservation

- mllm's pinned native framework artifact remains passing (20/20 executables,
  101 gtests).
- HPTPE reruns 9/9 functional organizations, 302 golden checks and 9/9 lint.
- All three run-030 workload/system artifacts remain passing.
- ATX is absent from the active layer matrix.

## Evidence boundary

Agentix/Agent.xpu/TISA/mllm closed-platform values remain source-grounded/open
simulation rather than original A100/Core-Ultra/Qualcomm/Epoch measurement.
HPTPE sparse cycles are executed RTL; 24 absolute PPA endpoints remain exact
author-report replay because licensed SAED32 synthesis is unavailable.

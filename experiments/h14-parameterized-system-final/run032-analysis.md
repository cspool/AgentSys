# H14 run-032 analysis — complete parameterized experiment system

## Final outcome

The user-requested parameterized experiment system is complete. Run 032 passes
four strict serial stages and a 15/15 requirement certificate.

| Serial stage | Wall time | Result |
|---|---:|---|
| Five-layer parameter/paper matrix | 75.87 s | 68/68 endpoints, 5/5 switches |
| `react_moa_mcts` full system | 226.51 s | 80 descriptors, 860 events |
| `react_tool` full system | 109.01 s | 16 descriptors, 180 events |
| `planner_debate` full system | 150.55 s | 40 descriptors, 436 events |

The manifest proves `serial_order=true` with nanosecond boundaries and records 53
fresh output files/hashes.

## Certificate

All 15 requirements pass: workload schema/CLI, configuration identity, three
distinct workload/header/ELF identities, three full dual-Rocket pipelines,
dedicated zero-repair TISA logs, per-tile checksum identity, five consumed layer
configs, five changed sensitivity metrics, 68/68 endpoints at 10%, native mllm,
HPTPE RTL, ordinary RISC-V/neutral XPU, ATX exclusion, base toolchain and fresh
pytest/dispatch/legacy/full-RTL checks.

## What can now be switched

An Agent JSON can change program/call DAG, priorities, arrival, policy/batch,
LLM/tool calls, token shapes, Agent.xpu chunk/batch/share, MIR/operator selection,
duration mapping, DMA beats and compatible hardware-profile expectations. The
pipeline generates isolated artifacts and runs them without source edits.

The layer matrix independently changes Agentix batch, Agent.xpu HEG chunk, TISA
window, mllm prompt and HPTPE organization. Baseline paper comparison and
sensitivity variants remain separate to prevent post-result fitting.

## Current hardware-profile boundary

The installed full-system binary is TISA window-8, seven-cycle dispatch and
HPTPE OPT1 16x16. A workload declaring a different hardware profile fails with a
rebuild request; component-level TISA/HPTPE matrices execute alternative
parameters. Absolute HPTPE PPA remains author-report evidence without licensed
SAED32 synthesis.

# Parameterized Agent workload toolchain

## One-command switching

The active entry point accepts a versioned JSON workload and produces an
isolated application trace, compiled manifest, generated C header, RISC-V ELF,
static/dynamic Rocket result and 11-layer system trace:

```bash
cd /workspace/AgentSys

.venv/bin/agentsys-run-workload \
  --workload workloads/react_tool.json \
  --run-id my_run
```

Use `--compile-only` to stop after the per-workload ELF. `--output-dir` overrides
the default hash-addressed location:

```text
artifacts/workloads/<name>/<workload-sha-prefix>/<run-id>/
├── application.json
├── compiled.json
├── generated/workload.h
├── software/workload.riscv
├── logs/{static,dynamic}.log
├── logs/{static,dynamic}-tisa.log
├── system.json
├── system-trace.jsonl
└── pipeline.json
```

No repository source is rewritten when switching workloads. When the hardware
profile remains `rocket_tisa8_hptpe16x16`, the existing simulators are reused;
only the generated header and ELF are rebuilt.

## Manifest contract

Each JSON declares:

- `programs`: ID, reactive/normal/proactive priority and arrival;
- `calls`: program, `llm`/`tool`, DAG dependencies, scheduling duration, thread,
  token shape, model or tool adapter and tool cycles;
- `models`: framework MIR, hardware MIR, 1–8 selected source operators,
  ME/VE/DE duration divisors and static stage IDs;
- `agentix`: policy and batch size;
- `agentxpu`: prefill chunk, reactive/proactive decode caps and elastic HPTPE
  share;
- `hardware`: TISA window/dispatch, HPTPE rows/columns and DMA beats;
- optional `expectations`: dynamic-faster, static-overlap and backend speedup
  range gates.

The loader rejects duplicate/missing/cyclic dependencies, unknown program/model
references, invalid parameters, more than 63 programs/calls and more than eight
operators in one TISA launch.

The current checked-in examples are:

- `workloads/react_moa_mcts.json` — certified mixed workload;
- `workloads/react_tool.json` — one reactive tool-use chain;
- `workloads/planner_debate.json` — PLAS, two programs, parallel critics and a
  cross-program dependency.

## Manifest-derived software and gates

The generated header supplies program/call counts, trace capacity, LLM/tool
counts, flow counts, placement counts, per-engine work and HPTPE lane count. The
bare-metal program checks each call against those values instead of fixed
`3/11/10/1/80` constants.

The host validates:

- workload SHA identity through application, compilation, ELF and both runs;
- exact manifest-derived call/tile/work/DMA counts;
- call dependencies and 11-layer lineage;
- issue/complete metadata for every selected mllm operator;
- dedicated, zero-repair hardware trace transport;
- per-tile and aggregate static/dynamic checksum identity;
- optional performance expectations only when the manifest declares them.

## Installed hardware boundary

Workload fields expose hardware parameters, but the currently installed binary
profile is window-8, seven-cycle dispatch and HPTPE OPT1 16x16. A manifest with a
different hardware profile fails clearly and requests a matching Chipyard build;
it is never silently approximated. Building and paper-regressing multiple
hardware profiles is the next parameter-matrix stage.

# H13 revised integration analysis — run 026

## Outcome

Run 026 is a retained negative result: 18/19 confirmatory gates pass. The
ordinary-RISC-V Rocket systems execute the new neutral-ABI ELF successfully and
produce a complete application-to-HPTPE trace, but dynamic TISA issue is 2.000x
faster than static issue, above the preregistered/published 1.14--1.63x range.
The range gate is not relaxed after observing the result.

## Executed stack

```text
ReAct / Mixture-of-Agents / MCTS
  -> Agentix call DAG
  -> upstream mllm Qwen3 QNN-AOT MIR
  -> Agent.xpu flow/stage/placement metadata
  -> neutral xpu_v2 config/launch/wait/status/clear ABI
  -> ordinary Rocket + HellaCache DMA
  -> TISA ME/VE/DE issue
  -> official HPTPE OPT1 compressed-OS 16x16 array + VE + DE
```

Both generated Verilator systems run the same 99 KiB RISC-V ELF. ATX commands,
prefetch/cancel operations and ATX magic values are absent.

## Results

| Measurement | Static | Dynamic | Invariant/result |
|---|---:|---:|---|
| Programs / calls / launches | 3 / 11 / 10 | 3 / 11 / 10 | identical |
| Native mllm descriptors | 80 | 80 | identical |
| ME / VE / DE busy cycles | 2400 / 2400 / 1600 | 2400 / 2400 / 1600 | identical |
| DMA bytes | 960 | 960 | identical |
| HPTPE MAC operations | 614,400 | 614,400 | 30 ME tiles x 80 cycles x 256 PEs |
| Backend cycles | 6,560 | 3,280 | 2.000x, **outside 1.14--1.63x** |
| Controller-system cycles | 6,940 | 3,660 | 1.896x |
| CPU-observed cycles | 25,975 | 22,696 | 1.144x |
| Dynamic overlap cycles | 0 | 2,370 | overlap mechanism active |
| Final checksum | `1b4610786e2b8ddb` | `1b4610786e2b8ddb` | bit-identical |

The merged trace has 860 events across 11 layers: application, framework,
mllm, Agent.xpu, software, CPU, XPU, TISA, HPTPE, VE/DE and DMA. Each backend
contains 80 issue and 80 complete tile records. FESVR target-UART output split
one `$display` frame in each raw log; the parser reconstructs only a
schema-complete prefix/suffix pair and records one transport repair per run.

## Failure diagnosis

The functional and lineage mechanisms are correct. The over-speedup comes from
the first integrated dynamic policy allowing the three independent engines to
remain nearly perfectly occupied, while the static baseline serializes all
6,400 engine-busy cycles plus dispatch. This produces an exact 2x backend ratio,
which is stronger than but not representative of the paper's registered range.

The next iteration must preserve the ELF, descriptors, dependencies, engine
work, HPTPE operations, DMA and checksum. It may change only a source-grounded
dynamic scheduling cost or concurrency constraint, preregistered before rerun.

## Evidence

- `artifacts/results/revised-system-run_026.json`
- `artifacts/traces/revised-system-run_026.jsonl`
- `artifacts/logs/revised-system-{static,dynamic}-run_026.log`
- `artifacts/app_traces/revised-compiled-workload-run_026.json`
- `artifacts/results/revised-components-run_025.json` (68/68 standalone endpoints)

This is real Rocket/Verilator and released HPTPE RTL evidence, not measurement
on the papers' A100, Core Ultra, Qualcomm or Epoch platforms.

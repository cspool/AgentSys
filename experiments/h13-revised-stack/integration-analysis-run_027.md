# H13 revised integration analysis — run 027

## Outcome

Run 027 passes all 20 preregistered integration gates. The same RISC-V ELF runs
on ordinary single-core Rocket systems with static and dynamic TISA backends;
both instantiate the released HPTPE OPT1 compressed-output-stationary 16x16
array. No ATX mechanism is present in the active path.

## Recovery from run 026

Run 026 is retained as an 18/19 negative result because its per-operator static
serialization made dynamic scheduling appear 2.000x faster. Run 027 implements
the authors' comparison contract registered before rerun:

- static scheduling uses the Agent.xpu prefill/decode-handoff stage bit as a
  strong two-stage tile pipeline;
- dynamic ME/VE/DE waiting paths each take the paper's exact seven-cycle
  window-8 dispatch latency.

An independent Icarus test proves first issue at cycle 0/7 for static/dynamic
and identical issue, completion and checksum behavior.

## Real Rocket+HPTPE results

| Measurement | Strong static | Dynamic | Result |
|---|---:|---:|---|
| Programs / calls / launches | 3 / 11 / 10 | 3 / 11 / 10 | identical |
| Native mllm descriptors | 80 | 80 | identical |
| First issue per call | cycle 0 | cycle 7 | dispatch contract passes |
| ME / VE / DE busy cycles | 2400 / 2400 / 1600 | 2400 / 2400 / 1600 | identical |
| Cross-engine overlap | 1,590 | 2,370 | +780 dynamic |
| DMA bytes | 960 | 960 | identical |
| HPTPE MAC operations | 614,400 | 614,400 | identical |
| Backend cycles | 4,900 | 3,560 | **1.376x** |
| Controller-system cycles | 5,280 | 3,940 | **1.340x** |
| CPU-observed cycles | 24,570 | 23,277 | **1.056x** |
| Final checksum | `ad503029d98907c8` | `ad503029d98907c8` | bit-identical |

The 1.376x backend result is inside the locked TISA 1.14--1.63x range. The
smaller CPU-observed result measures the expected dilution from unchanged
Rocket configuration, Agent tool execution and DMA overhead.

## Trace and lineage

The merged JSONL trace contains 860 events and all 11 required layers:
application, Agentix/framework, mllm, Agent.xpu, software runtime, CPU, XPU,
TISA, HPTPE, VE/DE and DMA. For each backend, 80 hardware issue records match 80
complete records and retain the upstream mllm source index plus flow, stage,
placement, preemptibility, priority and duration. The parser records one
schema-exact UART/RTL transport-frame repair in each raw log.

## Standalone preservation and evidence boundary

The active run-025 certificate remains 68/68 endpoints across Agentix,
Agent.xpu, TISA, mllm/llm.npu and HPTPE, with 9.91% global maximum error. Run 027
adds integrated functional/cycle evidence; it does not turn Rocket/Verilator
into the papers' A100, Core Ultra, Qualcomm or Epoch platforms. HPTPE absolute
PPA remains author-report replay; array functionality and integrated work are
executed RTL evidence.

## Artifacts

- `artifacts/results/revised-system-run_027.json`
- `artifacts/traces/revised-system-run_027.jsonl`
- `artifacts/logs/revised-system-{static,dynamic}-run_027.log`
- `artifacts/app_traces/revised-compiled-workload-run_027.json`
- `rtl/agentsys/tb_agentsys_tisa_dispatch.sv`

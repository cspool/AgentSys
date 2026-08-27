# H18.1 run-045 analysis — first multi-call Agent/MLX execution

Run 045 is a retained partial/negative result. The `react_tool` workload fully
compiles and both Rocket backends execute all three calls with zero dependency,
ABI or golden failures. The system passes 8/10 top-level gates; two runner gates
are wrong for a multi-launch workload.

## What passed

- One Agent program becomes a distinct 3-call ELF (2 LLM, 1 CPU tool).
- Each LLM has 8 MIR/TISA sources and a complete 45-micro-op/9-PE MLX lineage.
- Cycle/RTL each run 90 instructions and 1,152 DMA bytes; kernel totals are the
  locked 264/152 cycles.
- Calls, dependencies, program boundaries, flow/chunk/batch metadata, per-call
  ABI/golden and cycle/RTL logical checksum all match.
- The 158-event composed trace covers all required software/compiler/CPU/MLX
  layers with call IDs.

## Retained failures and diagnosis

1. `aggregate_hardware` assumed every launch pays the standalone cold DMA cost
   of 344 cycles. The first call does; the second reuses the same input/output
   addresses in Rocket caches and takes 216 DMA cycles. Both backends observe the
   identical 344→216 sequence. Per-call `system=DMA+kernel+2`, instruction and
   byte contracts remain exact.
2. `serial_seven_stages` is an implementation count error. The pipeline has six
   actual serial stages: application, TISA compile, MLX compile, ELF build and
   two Rocket backends. All six pass and are correctly ordered.

This result exposes a useful CPU/accelerator interaction hidden by one-launch
smoke tests. Recovery must sum observed per-call DMA/system counters and lock the
cold/warm sequence rather than weakening functional or kernel gates.

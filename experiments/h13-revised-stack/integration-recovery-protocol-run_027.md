# H13 run-027 protocol: restore the published TISA comparison contract

## Motivation fixed before implementation

Run 026 passes 18/19 gates but reports 2.000x dynamic/static backend speedup,
outside the locked 1.14--1.63x range. A source re-audit identifies two omissions
in the first RTL comparison:

1. The TISA evaluation compares dynamic scheduling with a **strong static
   tile-level pipeline**, while run 026 assigns every descriptor a unique static
   group and therefore serializes the baseline.
2. The registered window-8 dynamic scheduler takes **seven dispatch cycles**;
   run 026 issues ready candidates combinationally at zero dispatch latency.

The public author slides show static dual-/triple-stage schedules (pp. 10--13),
per-unit WQ/IQ/execution paths (p. 19), and the published Epoch static/dynamic
table (p. 26):
<https://yaozhujia.github.io/assets/pdf/isca2026-presentation.pdf>.

## Single recovery change set

This run restores that comparison contract without changing useful work:

- The already encoded Agent.xpu stage bit becomes the static scheduling group:
  native mllm operators 6--12 are the prefill group and operators 13--14 are the
  decode-handoff group. Explicit SSA dependencies and per-engine occupancy still
  constrain issue within each group.
- Dynamic mode receives independent ME/VE/DE dispatch registers. A candidate
  admitted from the eight-entry window reserves its per-unit path for exactly
  seven cycles before the execution engine starts. Static mode has no dynamic
  scheduler latency.

The stage boundary is not selected from the run-026 residual; it already exists
in every run-026 descriptor and is used by Agent.xpu placement metadata. Seven
cycles is the preregistered paper endpoint, not a fitted value.

## Frozen inputs and invariants

- Same ReAct/MoA/MCTS application trace and 11 calls.
- Same pinned upstream mllm commit/MIR and source indices
  `6,7,8,10,11,12,13,14`.
- Same 80 descriptors, durations, dependencies, flow classes, priorities,
  placement, preemptibility, memory ranges and DMA bytes.
- Same neutral `xpu_v2` five-command ABI and ordinary Rocket CPU.
- Same released HPTPE OPT1 compressed-OS 16x16 array, 614,400 MAC operations,
  VE/DE engines and result-checksum contract.
- Same run-025 standalone certificate: five components, 68/68 endpoints and
  maximum error <=15%. ATX remains excluded.
- Same exact integrated TISA backend acceptance interval, 1.14--1.63x; it is not
  relaxed to accept run 026.

## Confirmatory gates

All run-026 functional, lineage, transport, trace-layer, same-work and exclusion
gates must remain passing. In addition:

1. Every dynamic call's first tile issue is exactly cycle 7; every static call's
   first issue remains cycle 0.
2. Dynamic issue records still form 80 unique issue/complete pairs and preserve
   all source/stage/flow/placement fields.
3. Static stage pipelining creates non-zero legal cross-engine overlap, while
   dynamic remains faster at backend and controller scope.
4. Backend speedup lies inside 1.14--1.63x, with no post-result threshold change.

## Prediction

The unchanged Python semantic reference gives 480 static cycles and 348 dynamic
cycles for one descriptor set (1.379x) when using the existing stage bit and
seven-cycle dispatch. Rocket RTL includes edge/accounting overhead, but the
ratio is expected to remain inside 1.14--1.63x. End-to-end gain should remain
smaller because CPU configuration, tool execution and DMA are unchanged.

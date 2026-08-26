# H13 revised Chipyard integration protocol

## Locked stack

```text
ReAct / Mixture-of-Agents / MCTS applications
  -> Agentix program/call DAG release
  -> native upstream mllm Qwen3 QNN-AOT operators
  -> Agent.xpu flow class, placement, batching and tile-boundary priority
  -> neutral RISC-V XPU runtime
  -> TISA semantic issue
  -> HPTPE OPT1 16x16 compressed OS array + VE + DE
  -> Rocket HellaCache DMA / system memory
```

The CPU is an ordinary Rocket core. The revised ABI exposes only
`config/launch/wait/status/clear`; there is no ATX task, cancel, prefetch or ATX
magic value.

## Implementation identity

- The application graph is executed by the existing Agentix application runner.
- The eight hardware descriptors per LLM call are selected from the pinned
  upstream mllm Qwen3 QNN-AOT MIR, not the project-owned transformer fixture.
- Every descriptor encodes its native source-op index plus Agent.xpu flow class,
  stage, placement and tile-boundary preemptibility.
- ME descriptors execute a wrapper around the released HPTPE OPT1 OS RTL with
  16x16 PEs. VE/DE remain explicit independent engines.
- The same TISA scheduler source is used by static and dynamic configurations;
  only the `DYNAMIC` parameter differs.

## Confirmatory gates

1. A new neutral-ABI ELF builds and runs with exit code zero on both
   `AgentSysRevisedStaticRocketConfig` and
   `AgentSysRevisedDynamicRocketConfig`.
2. Both runs execute 3 programs, 11 calls, 10 XPU launches and 80 native-mllm
   descriptors with identical dependency lineage.
3. Static/dynamic runs preserve per-engine issue counts, busy work, DMA bytes,
   HPTPE 256-MAC-per-cycle operation count and final checksum.
4. The hardware log contains a matching issue/complete pair for every TISA tile,
   including engine, native op, flow class, placement, priority and cycle.
5. No priority violation, cancellation, prefetch event or ATX ABI/magic appears.
6. Dynamic issue creates ME/VE/DE overlap and is faster than static at backend
   and controller-system scope. Its backend speedup remains in TISA's published
   1.14--1.63x range.
7. The merged trace contains application, framework/Agentix, mllm, Agent.xpu,
   software, CPU, TISA, HPTPE, VE/DE and DMA evidence with parent/dependency
   checks closed.
8. The previously certified five standalone components remain 68/68 endpoints
   and each maximum error remains <=15%.

## Evidence boundary

Rocket+Verilator provides real ISA/RTL/DMA functional and cycle evidence for the
revised system. It is not the original A100, Core Ultra, Qualcomm phone, Epoch
silicon or SAED32 implementation. HPTPE frequency/area remains author-report
replay; Chipyard cycles measure the integrated Rocket model.

## Prediction

The HPTPE array increases executed MAC parallelism from the legacy four-lane
reference to 256 lanes without changing the registered TISA tile durations, so
static/dynamic work conservation and the existing dynamic overlap trend should
survive. Application speedup will remain smaller than backend speedup because
Rocket configuration, DMA and call-control cycles are unchanged overheads.

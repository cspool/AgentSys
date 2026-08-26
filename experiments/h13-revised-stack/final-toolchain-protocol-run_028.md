# H13 run-028 protocol: revised full-toolchain replay and final certificate

## Objective

Close the revised ordinary-RISC-V system with one pinned, machine-audited entry
point. This run does not change any component model, endpoint target, scheduling
mechanism, RTL parameter or run-027 performance gate.

## Locked serial replay

The active replay order is exactly:

1. Agentix standalone profile (16 endpoints).
2. Agent.xpu standalone profile (11 endpoints).
3. TISA standalone profile (10 endpoints).
4. mllm/llm.npu profile (20 native executables/101 gtests and 5 endpoints).
5. HPTPE profile (9 RTL organizations/302 golden checks/9 full-scale lints and
   26 endpoints).
6. Five-component certificate (68 endpoints, maximum error <=15%, ATX absent).
7. Revised Agentix→mllm→Agent.xpu→TISA application compilation.
8. The same ELF on static and dynamic ordinary-Rocket+HPTPE simulators.

A stage starts only after the previous stage exits zero and its declared JSON
gate is true. The reproduction manifest records nanosecond boundaries and must
prove non-overlap/serial order.

## Toolchain contract

- Python 3.11 and locked project packages.
- Clang 16 for the upstream mllm build.
- Icarus Verilog 11 and pinned Verilator 5.050 for HPTPE.
- Chipyard's Verilator 4.034, Java 11 and RISC-V GCC 9.2 for Rocket.
- Pinned mllm, HPTPE, LLM.xpu, Autellix, Verilator-5 and Chipyard revisions.
- The MLX_dev `sys` checkout is recorded only as an engineering reference, not
  an active paper mechanism or performance source.
- Fresh executable/hash checks for mllm, Verilator-5, the revised ELF and both
  revised Rocket simulators.
- Source-equality checks for revised Scala/RTL plus all 12 official HPTPE files
  installed into Chipyard.

## Final certificate gates

1. All eight serial stages pass in the registered order.
2. Toolchain source, tools, pins, builds, overlays, profiles, stage artifacts
   and reproduction manifest all pass.
3. Exactly five active components and 68/68 endpoints pass; `atx` occurs only
   in the explicit excluded-component field.
4. The system artifact passes 20/20 gates, contains 860 events/11 layers,
   executes 614,400 HPTPE MAC operations, uses `xpu_v2`, and reports backend
   speedup inside 1.14--1.63x.
5. Static/dynamic work and final checksum remain identical.
6. Fresh full pytest, standalone dispatch RTL and full revised HPTPE/RoCC lint
   exit zero.
7. The main report and toolchain documentation identify run 023/024/025/026/027
   evidence classes, the retained failure and proprietary-platform limits.

## Prediction

The five standalone profiles should remain 68/68 at 9.91% maximum error. The
system replay should reproduce run 027's 4,900/3,560 backend cycles (1.376x),
860 events and checksum because inputs, binaries and RTL mechanisms are frozen.

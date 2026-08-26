# H13 revised full-toolchain analysis — run 028

## Final outcome

The revised goal is complete. Run 028 passes:

- 8/8 serial reproduction stages with `serial_order=true`;
- 12/12 pinned toolchain gates;
- 15/15 final certificate requirements;
- 5/5 active components and 68/68 paper endpoints;
- 9.91% maximum component error, below the locked 15% limit; and
- 20/20 real ordinary-Rocket+HPTPE system gates.

ATX is absent from the active profiles and integrated ABI. It remains only in
the explicit excluded-component field and historical artifacts.

## Serial stage evidence

| Stage | Wall time (s) | Result |
|---|---:|---|
| Agentix profile | 13.918 | 16/16 endpoints |
| Agent.xpu profile | 11.131 | 11/11 endpoints |
| TISA profile | 7.621 | 10/10 endpoints |
| mllm/llm.npu profile | 9.471 | 20/20 executables, 101 gtests, 5/5 endpoints |
| HPTPE profile | 24.384 | 9/9 RTL, 302 checks, 9/9 lint, 26/26 endpoints |
| Standalone certificate | 0.110 | 68/68, five components |
| Application/MIR compilation | 0.210 | 11 calls, 80 descriptors |
| Static+dynamic Rocket/HPTPE | 211.001 | 20/20 gates, 860 events |

The manifest records each command, combined stdout, exit code, output sizes and
SHA-256 hashes plus nanosecond start/finish boundaries. Every next-stage start is
not earlier than the preceding finish.

## Toolchain audit

All 12 gates pass: configuration, Python, locked packages, system tools, pinned
references, source files, five independent profiles, five build outputs, two
Chipyard compatibility patches, 16 source-identical overlays, all stage
artifacts and the serial reproduction manifest. MLX_dev `sys` is classified only
as an engineering reference.

## Final system result

Static/dynamic backend cycles are 4,900/3,560 (1.376x); controller-system cycles
are 5,280/3,940 (1.340x); CPU-observed cycles are 24,570/23,277 (1.056x).
Dynamic adds 780 overlap cycles. Both runs preserve 80 descriptors, 960 DMA
bytes, ME/VE/DE work 2,400/2,400/1,600, 614,400 HPTPE MAC operations and checksum
`ad503029d98907c8`. Dynamic first issue is cycle 7; static first issue is cycle 0.

The trace contains 860 events across application, framework, mllm, Agent.xpu,
software, CPU, XPU, TISA, HPTPE, VE/DE and DMA.

## Fresh checks

The final certificate reruns the complete pytest suite, the standalone Icarus
dispatch test, legacy AgentSys lint and full revised Rocket/HPTPE lint. All exit
zero. Warnings in the full lint are retained upstream HPTPE filename/width/
combinational-loop diagnostics and are not suppressed as functional evidence.

## Evidence boundary

This is real open-source framework execution, RTL execution and Rocket system
simulation. It is not direct measurement on Agentix A100s, Agent.xpu Core Ultra,
llm.npu Qualcomm phones, TISA Epoch silicon or a new licensed SAED32 synthesis.
HPTPE absolute PPA remains author-report replay; its RTL behavior, sparse cycles
and integrated 16x16 work are executed evidence.

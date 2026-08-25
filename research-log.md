# Research Log

Chronological record of research decisions and actions. Append-only.

| # | Date | Type | Summary |
|---|---|---|---|
| 1 | 2026-08-25 | bootstrap | Audited the workspace: only a 50-line direction document and Docker launcher existed; no implementation, tests, or results. Recovered Agentix, Agent.xpu, ATX, and TISA method/evaluation details from the read-only paper-analysis vault and official project pages. Registered paper endpoints before simulator execution. |
| 2 | 2026-08-25 | bootstrap | Pinned MLX_dev `sys` commit `b3a6d59f2ed634ea6181f5a29f3fa96281b1f384` only as a Chipyard/PE-array engineering reference. It targets the same Chipyard `b5d01319` checkout and supplies reusable RoCC/HellaCache/Verilator plumbing; its MLX scheduling mechanism is explicitly out of scope. |
| 3 | 2026-08-25 | bootstrap | Pinned implementation references: LLM.xpu `689be270aa29bb88447e3867cd97d85a55f454d5`, plus shallow HPTPE and mllm checkouts. Formed H1–H4 and selected maximum preregistered endpoint error (15% gate) plus trace/priority/correctness invariants as evaluation criteria. |
| 4 | 2026-08-25 | inner-loop | Run 001 executed 23 endpoints: 18 pass, 5 fail, max error 77.02%. Agentix passes 3/3 and TISA passes 10/10; Agent.xpu passes 8B reactive latency, 48 ms pending, and proactive throughput but fails 3B reactive latency and iGPU/energy accounting. Nine functional tests pass. |
| 5 | 2026-08-25 | outer-loop | The paired 8B-pass/3B-fail pattern localizes H2's missing load sensitivity. Returned to Agent.xpu §3–4: Figure 4 reports up to 1.59× GEMV slowdown under shared-DDR co-execution, and §4.3 assigns reactive prefill to both NPU and iGPU. Direction: DEEPEN with these two shared mechanisms only. |

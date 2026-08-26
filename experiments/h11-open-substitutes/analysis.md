# H11 analysis: closed mechanisms replaced by executable open simulators

Run 019 executes from source commit `53d53a79a521cfb53b00ff809123a833714b7385`.

## Source discovery

- No author-official Agentix repository was found. The independent public vLLM fork `kungfu-team/autellix@1df1987` was pinned; its 58 pure-Python policy tests pass, but it remains explicitly non-author-verified.
- The ATX author page links the paper but not the private Sniper extension. Public Sniper was identified; the unavailable UTE/NCA extension is replaced locally.
- No public TISA/Epoch repository was found on the checked author profile/GitHub.

## Agentix substitute

- 13/13 aggregate endpoints pass; maximum error is 9.09% (mixed versus MLFQ: observed 5.0×, target 5.5×).
- Single ratios are 8/2/1.5×; LATS 5/2/2.667×; mixed 15.5/5/5×.
- Offline reductions are 13.28/20.08/21.80/25.39% and monotonic.
- Every SLO capacity has an adjacent failing boundary, all modes conserve logical calls/tokens, and dynamic DAG/policy gates pass.

## ATX substitute

- 18/18 endpoints pass; maximum error is 3.10% at the 128-KiB LLC point.
- All five organizations execute 64 tasks. Task conservation, event resources, prefetch non-regression, UTE shape and design-space monotonicity pass.
- The Small/default/infinite UTE transfer path takes 163/82/22 cycles, demonstrating active Stream Unit/LDQ/Common Bus modeling.
- Chipyard run 003 independently retains 17/17 real RTL/ABI/DMA/checksum gates.

## Completion

- Evidence classes: 24 direct executable/source-grounded, 31 open executable closed-platform substitutes, 0 parameterized component replay.
- Nine serial stages pass with `serial_order=true`; summed stage runtime is approximately 108.3 s.
- Full toolchain: 12/12. Final run 020: 15/15 requirements, 55/55 endpoints at limit 0.10, maximum error 9.09%, fresh 35-test pytest and Verilator lint.

H11 is supported. The stronger implementation evidence does not make the substitutes hardware-equivalent: Agentix remains curve-calibrated rather than A100-measured, and ATX remains paper-configured rather than private-Sniper validated.

# H17.1 protocol — fresh MLX cycle and physical-RTL rebuild (run 043)

Locked before creating the MLX Python environment, build products or runner.

## Inputs

- Active MLX source: run-042-qualified commit `2a457df...`.
- Tools: Icarus 11.0, Verilator 4.034, GNU make/g++.
- Programs/inputs/goldens: the four frozen target-free MLX system workloads
  (BSMM, FFT-CMP, SWA and Transformer block).
- Outputs: project-owned `artifacts/mlx_standalone/run_043`; the active MLX
  checkout must remain clean.

Create `.venv-mlx` from Python 3.11 with NumPy 2.2.6, PyYAML 6.0.2 and the
editable AgentSys package. This environment is the later Agent-to-MLX compiler
runtime; run 043 itself may consume frozen generated inputs.

## Execution

Build two genuinely different backends from the active sources:

1. Icarus cycle model: serialized ready-tag interpretation through the abstract
   shared SIMD service.
2. Verilated `mlx_array_4x4`: sixteen physical PE instances, tagged control,
   heterogeneous FUs, packet routing and one-port SPM arbitration.

Execute all four workloads on both backends.

## Gates

1. Setup/tool/source pins and active-checkout cleanliness pass.
2. Both fresh builds exit zero and their executable hashes are retained.
3. Eight executions exit zero and every output matches the software FP16 golden.
4. Cycle and RTL instruction counts equal the workload manifest.
5. Both backends preserve the identical `(PE, PC, opcode)` multiset and per-PE
   program order for all workloads.
6. At least one global issue interleaving differs, proving the backends are not
   duplicate wrappers.
7. All ten spatial opcodes execute; issue-to-complete latency and observed II
   exist for every opcode in physical RTL.
8. Runtime dependency stalls and resource conflicts are non-zero where expected.
9. Source/program/input/golden/log/build hashes form a complete chain.
10. No paper performance target is read or compared in run 043.

Run 043 qualifies standalone mechanisms only. Rocket integration and
Agent-specific compilation remain pending.

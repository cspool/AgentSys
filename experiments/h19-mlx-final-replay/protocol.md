# H19.2 protocol — complete MLX+CPU fresh serial replay (run 048)

Locked before adding output overrides, the top-level runner or executing any
fresh final stage.

## Exact serial stages

1. Active MLX source/evidence audit: expected 10/10.
2. Fresh Icarus cycle + Verilator physical-4x4 standalone rebuild and four
   workloads: expected 10/10, 8 executions.
3. Reuse the already source-hashed Rocket binaries but freshly execute four
   bare-metal workloads on both: expected 12/12, 8 executions.
4. Fresh six-layer matrix, including a new react-tool MLX sensitivity execution:
   expected 73/73, six switches, 10/10, maximum 9.91%.
5. Fresh three-Agent replay on both Rocket backends: expected 9/9 globally,
   10/10 each, 20 calls/17 MLX launches/3 CPU tools/765 micro-ops.

Each stage begins only after the prior stage finishes and passes. All outputs go
under `artifacts/mlx_complete/run_048`; run-042–047 evidence is immutable.

## Global gates

- stage order/count/timestamps prove 5/5 strict serial execution;
- all stage summaries and every nested gate pass;
- source/config/workload/header/ELF/result hashes are distinct and linked;
- primary final hardware is ordinary Rocket+MLX cycle/physical RTL;
- GPU/HPTPE remain optional/historical evidence, ATX absent;
- 73 registered endpoints pass at 10% and MLX boundary remains target-informed,
  LOO>10%, strict-full-paper false;
- active MLX checkout stays pinned/clean and installed overlays remain exact;
- no stage reads an observed run-048 value to change a simulator parameter.

Passing run 048 supports the complete replay mechanism. A separate run-049
certificate must still execute fresh tests/checks and audit required files.

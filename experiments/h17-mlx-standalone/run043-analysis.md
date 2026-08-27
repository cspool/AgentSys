# H17.1 run-043 analysis — fresh cycle/physical-RTL execution

## Outcome

H17.1 is supported. Both active-source backends build freshly and all ten gates
pass. Four spatial programs execute on both backends (8/8), every run exits zero
and matches the software FP16 golden.

| workload | instructions | cycle-model cycles | physical RTL cycles | cycle/RTL |
|---|---:|---:|---:|---:|
| BSMM | 44 | 128 | 61 | 2.098x |
| FFT-CMP | 34 | 95 | 49 | 1.939x |
| SWA | 25 | 99 | 83 | 1.193x |
| Transformer block | 45 | 132 | 76 | 1.737x |

These ratios compare the repository's serialized abstract cycle interpreter with
its physical 16-PE backend; they are not paper speedup endpoints.

## Architecture identity and difference

For every workload the two backends preserve the same `(PE, PC, opcode)`
multiset and the exact same program order within each PE. Their global issue
order differs on all four workloads, as expected: the cycle model serializes a
ready tag through one service, while physical RTL issues concurrently across
PEs, arbitrates SPM and routes packets.

All ten opcodes have physical issue/complete measurements. Representative fixed
latencies are load/store 1, FMA 4, add/mul 3, exp 8 and div 12 cycles; xfer is
1–3 cycles. Stalls, route hops and resource conflicts are runtime counters, not
configuration-derived estimates.

## Reproducibility

`.venv-mlx` pins Python 3.11, NumPy 2.2.6 and PyYAML 6.0.2. The runner stores
source/program/input/golden/log and build-output hashes without modifying the
active MLX checkout. Generated compiler objects remain rebuildable local
artifacts and are not archived in Git.

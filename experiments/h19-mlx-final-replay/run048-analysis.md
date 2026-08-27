# H19.2 run-048 analysis — complete fresh MLX+CPU replay

## Outcome

H19.2 is supported. All five stages run in the locked order, start only after the
prior stage finishes and pass. The global manifest passes 10/10 gates.

| stage | wall time | result |
|---|---:|---|
| MLX source audit | 0.03 s | 10/10 |
| fresh standalone build/run | 53.37 s | 10/10, 8 runs |
| fresh Rocket execution | 273.55 s | 12/12, 8 runs |
| six-layer regression | 211.88 s | 73/73, 6 switches |
| three Agent DAGs | 627.82 s | 9/9, 6 runs |

The replay executes 24 MLX simulations in total: 8 standalone, 8 base Rocket, 2
MLX sensitivity and 6 Agent workload runs. It freshly rebuilds standalone cycle/
RTL, but reuses the already source-hashed Chipyard binaries while rerunning all
ELFs.

All evidence boundaries survive replay: MLX is primary system hardware, ATX is
excluded, HPTPE/GPU are optional historical evidence, the five MLX paper rows
remain target-informed, LOO remains above 10% and strict full-paper completion
remains false. No observed run-048 value changes a model parameter.

The standalone compiler build tree is an 85-MB reproducible local cache and is
ignored by Git. Result manifests, logs, ELFs and hashes are retained.

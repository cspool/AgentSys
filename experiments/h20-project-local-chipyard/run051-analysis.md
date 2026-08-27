# H20 run 051 analysis: project-local Chipyard recertification

## Verdict

H20 is supported. The post-vendoring implementation commit
`d7b209189f7c15351186fb4571395ea83a4631f5` removes the active
`/root/chipyard` contract, selects the repository-local Chipyard snapshot by
default, builds both MLX Rocket simulators there, and reproduces the frozen
functional and numerical results exactly.

The authoritative certificate is
`artifacts/results/project-local-chipyard-certificate-run_051.json`: 16/16
requirements and 3/3 fresh checks pass, including 114/114 pytest cases.

## Exploratory failures retained

The preregistered run exposed three portability defects before the confirmatory
replay:

1. Chipyard's wrapper `init-submodules-no-riscv-tools.sh` assumes Chipyard is the
   Git toplevel. In the vendored layout it changed to the AgentSys root and could
   not find its helper script. The project bootstrap now calls a project-owned,
   shallow, explicit build-closure initializer.
2. A non-recursive top-level checkout was insufficient. Rocket requires nested
   `api-config-chipsalliance` and `hardfloat`; Barstools tapeout requires nested
   `mdf`. Missing them caused 1,302 Rocket errors and then 92 MacroCompiler
   errors. All three gitlinks are now explicit bootstrap prerequisites.
3. `mlx_agent_compiler.py` had two source-config readers. The compiler path was
   migrated first, but the ELF builder initially treated
   `${AGENTSYS_CHIPYARD_ROOT}` literally. The second reader now uses the same
   recursive token expansion and the full test suite covers active literal
   absence.

The exploratory run-050 outputs were moved, not deleted, to
`artifacts/tmp/h20-run050-exploratory/`; they are not certificate inputs.

## Source and environment mechanism

- `src/agentsys/paths.py` implements one fail-closed resolver. An explicit
  `AGENTSYS_CHIPYARD_ROOT` wins; otherwise the default is
  `/workspace/AgentSys/chipyard`.
- `chipyard/.agentsys-source.json` identifies the vendored snapshot as upstream
  commit `b5d013190d637e634113cb5179f8c8885df1945a` and hashes five base source
  files. A parent-repository `git rev-parse HEAD` is no longer mistaken for the
  Chipyard revision.
- `scripts/bootstrap_chipyard.sh` shallow-initializes the 22 top-level SBT
  dependencies plus Rocket API-config/HardFloat and Barstools MDF. It seeds an
  available pinned toolchain or builds ESP tools when none exists; verify-only
  mode is read-only.
- Historical, revised, and MLX JSON manifests store the portable
  `${AGENTSYS_CHIPYARD_ROOT}` token. Expansion occurs only after source identity
  validation.
- Both `MLXCycleRocketConfig` and `MLXRTLRocketConfig` were freshly generated and
  linked inside the repository-local tree; no external simulator binary was
  copied into the result.

## Confirmatory replay

`agentsys-reproduce-portable --run-id run_051` executes four non-overlapping
stages:

| Stage | Wall time (s) | Result |
|---|---:|---:|
| Project-local source/build preflight | 0.048 | pass |
| Four ELFs × cycle/RTL substrate | 270.900 | 12/12, 8/8 runs |
| Three Agent DAGs × cycle/RTL | 648.838 | 9/9, 6/6 runs |
| Six-layer matrix + cycle/RTL sensitivity | 209.385 | 10/10, 73/73 endpoints |

The manifest reports 4/4 stages, 9/9 global gates, strict serial order and 16
fresh Rocket executions. The Agent result retains 20 calls, 17 MLX launches, 3
CPU tools and 765 spatial micro-ops.

## Exact baseline comparison

The certificate compares parsed evidence, not only summary booleans:

- all 8 substrate `(backend, workload, summary, checks)` records exactly equal
  run 044;
- all three Agent summaries, gates, per-call parsed cycle/RTL records and trace
  hashes exactly equal run 046 (only artifact locations are normalized);
- all 73 endpoint identities, observed values, targets/ranges, relative errors,
  limits and pass bits exactly equal run 048;
- maximum endpoint error remains `0.09909909909909899` (9.91%).

## Evidence boundary

H20 changes path selection, bootstrap, source identity and recertification only.
It does not alter a model parameter, target, endpoint, workload, RTL mechanism or
reported cycle. The five MLX numerical rows remain target-informed, their LOO
maximum remains above 10%, and the external strict full-paper certificate remains
1/18. Project-local execution is stronger reproducibility evidence, not a license
to relabel that numerical scope.

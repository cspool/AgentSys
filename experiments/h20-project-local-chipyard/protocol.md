# H20 protocol: repository-local Chipyard and post-vendoring recertification

## Status

Locked before implementation or execution.

## Motivation

Run 049 certified implementation commit `bb04c97`, but the current tree adds a
vendored Chipyard 1.5.0 source snapshot in commits `f2ebf22` and `4ea3510`.
The active Python runners, shell setup paths, and machine-readable manifests
still contain `/root/chipyard`, so the new source snapshot is not yet an
automatically selectable build root and the current HEAD is not covered by the
run-049 certificate.

## Hypothesis

H20: a single fail-closed Chipyard path contract can make the repository-local
snapshot the default source/build root, retain an explicit environment override,
and recertify the current Agent-to-MLX system without changing any logical work,
cycle result, or registered paper endpoint.

## Frozen baseline

- Source baseline: current `main` at `4ea3510`.
- Functional baseline: run 049, 105/105 pytest cases and 25/25 certificate gates.
- Numerical baseline: run 047/048, 73/73 registered endpoints at a 10% limit,
  maximum relative error 9.91%.
- Agent/MLX baseline: three workloads, 20 calls, 17 MLX launches, 765 spatial
  micro-ops, cycle/RTL kernel totals and exact per-call goldens unchanged.
- Evidence boundary: the five MLX rows remain target-informed and the external
  strict full-paper certificate remains negative; H20 must not relabel either.

## Implementation contract

1. Add one project-owned Chipyard path resolver used by active Python runners.
   Resolution order is an explicit `AGENTSYS_CHIPYARD_ROOT` override followed by
   the repository-local `chipyard` directory. Invalid roots fail with an
   actionable error rather than silently selecting `/root/chipyard`.
2. Make active shell setup/install/build entry points use the same environment
   variable and repository-local default.
3. Replace active manifest path literals with a portable project-root token and
   expand it only in the toolchain loader. Historical result payloads may retain
   their recorded absolute paths.
4. Add unit tests for default selection, environment override, invalid roots,
   command/path expansion, and absence of active `/root/chipyard` literals.
5. Add a bootstrap preflight for the vendored Chipyard gitlinks and required
   RISC-V toolchain; it may initialize/build missing dependencies, but verify-only
   mode must remain read-only.

## Preregistered gates

- `pytest`: all existing and new tests pass.
- `active_paths_portable`: no `/root/chipyard` literal remains under active
  `src/agentsys`, `scripts`, `config`, or active Makefiles; documentation and
  frozen artifacts are excluded from this syntactic gate.
- `default_local_root`: without an override, the resolver selects
  `/workspace/AgentSys/chipyard` and validates its pinned source identity.
- `override_root`: an explicit valid `AGENTSYS_CHIPYARD_ROOT` is honored and an
  invalid override fails closed.
- `vendored_sources`: the base snapshot, required nested gitlinks, and all
  AgentSys/MLX overlays needed by the active configurations are present or are
  initialized by the setup entry point.
- `paper_regression_unchanged`: 73/73 endpoints pass at 10%, with the same
  endpoint identities, observed values, and maximum error as run 048.
- `agent_mlx_unchanged`: all three Agent DAGs pass and retain the frozen work,
  checksum, DMA, cycle, and RTL results.
- `current_head_certificate`: a new certificate records and verifies the exact
  post-implementation commit; it may not accept the old `bb04c97` anchor as proof
  for the new tree.

## Failure interpretation

- A missing nested submodule or toolchain is an environment/bootstrap failure,
  not permission to fall back silently to `/root/chipyard`.
- Any numerical or work-identity drift rejects H20 and is retained as a result.
- Passing unit tests alone does not satisfy H20; the fresh six-layer and
  Agent-to-MLX replay gates are mandatory.

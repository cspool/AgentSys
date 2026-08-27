# AgentSys objective completion audit after run 051

Audit date: 2026-08-27

Implementation anchor: `d7b209189f7c15351186fb4571395ea83a4631f5`

Evidence/report commit: `8d8aafe9e902d6e8bff67c114704bd552ae3d95e`

## Requirement-by-requirement result

| User requirement | Authoritative evidence | Audit result |
|---|---|---|
| Continue and complete the referenced AgentSys implementation/report | `ISCA26_G3_Agent全栈系统加速.md`; run-051 report/certificate; current worktree clean | proved |
| Implement the paper core mechanisms at source level | Agentix/Agent.xpu/TISA/mllm/HPTPE/MLX modules and RTL listed in the report; 114/114 current pytest; run-051 exact comparison to run 044/046/048 | proved for the registered core scope |
| Build unavailable/closed simulators from open simulators using paper descriptions or inference | executable open substitutes for Agentix/Agent.xpu/TISA/mllm/HPTPE plus project-local Chipyard/Rocket/MLX; evidence classifications and hardware boundaries remain machine checked | proved for the registered substitute scope |
| Paper performance values differ by no more than 10% | run-051 six-layer matrix: Agentix 16, Agent.xpu 11, TISA 10, mllm 5, HPTPE 26, MLX 5; 73/73 pass; maximum relative error `0.09909909909909899` | proved |
| End-to-end Agent software/framework/compiler/CPU/accelerator path | run-051 Agent stage: three DAGs, 20 calls, 17 MLX launches, 3 CPU tools, 765 micro-ops, cycle+physical-RTL execution, 9/9 gates | proved |
| Automatically configure the required environment | `scripts/bootstrap_chipyard.sh`, unified `AGENTSYS_CHIPYARD_ROOT`, vendored hash marker, shallow 22+3 gitlink closure, toolchain seed/build fallback, verify-only pass | proved |
| Current source, not a stale pre-vendoring tree, is certified | certificate/replay both record the full implementation SHA; 16/16 requirements and 3/3 fresh checks pass; `git diff d7b2091..8d8aafe -- src scripts config system_sim pyproject tests` is empty | proved |
| Preserve evidence limitations rather than overclaim | MLX rows remain target-informed, LOO maximum is 20.77%, and strict external full-paper result remains 1/18 | proved |

## Completion evidence

- `artifacts/project_local_chipyard/run_051/reproduction.json`: 4/4 strict
  stages, 9/9 gates, 16 fresh Rocket executions and serial order.
- `artifacts/results/project-local-chipyard-certificate-run_051.json`: 16/16
  requirements, three fresh checks and 114 pytest.
- Parsed substrate, Agent and endpoint signatures exactly equal the frozen
  run-044/046/048 baselines; no endpoint target or result was changed by H20.
- `bash scripts/bootstrap_chipyard.sh --verify-only` succeeds on the default
  `/workspace/AgentSys/chipyard` and reports upstream Chipyard commit
  `b5d013190d637e634113cb5179f8c8885df1945a`.

## Scope conclusion

The requested source-level core and registered performance reproduction are
complete and reproducible in the current workspace. “Complete” does not mean
that every figure of the external MLX paper has independent public-data
validation: the explicit 1/18 full-paper limitation remains a boundary, not an
unrecorded requirement gap or a substituted success claim.

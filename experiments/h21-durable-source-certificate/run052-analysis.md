# H21 run 052 analysis: durable source-closure recertification

## Verdict

H21 is supported at implementation commit
`ab7746201d9840904ede594d9dd765f7f11d3029`.  The portable replay executed all
four stages in strict serial order, launched 16 fresh project-local Rocket
simulations and reproduced every frozen substrate, Agent and registered paper
endpoint signature.  The initial certificate passed 19/19 requirements and
three fresh checks, including 117/117 pytest cases.

The one-sentence result is: AgentSys can bind executable source to a stable
implementation commit while allowing later evidence-only commits, without
relaxing any source path, Chipyard build-closure, functional or 10% numerical
gate.

## Source and environment closure

The implementation closure covers `.gitignore`, Git/submodule metadata, Python
and lock files, the vendored Chipyard tree, all active configuration/data,
Docker setup, integrations, patches, RTL, scripts, Python source, system
software, tests and workload manifests.  The expected commit must exist and be
an ancestor of the signing checkout.  Any tracked, staged, unstaged or
untracked change in those paths rejects the certificate.

Chipyard preflight now validates more than file existence:

- 22 top-level build submodules and three nested Rocket/Barstools gitlinks match
  their exact 40-character revisions;
- Chisel3 and Treadle contain only their registered `build.sbt` compatibility
  changes, with SHA-256
  `6cf44ba1acab54a6ae65d3c0eeb1133098e39c975d4b90d417f4d8695a212df3`
  and `d4ace994540ef3bda4bb06809d809e8232d961805a96876c035e0dc19f6fcd4f`;
- normal bootstrap applies both patches idempotently, whereas `--verify-only`
  is read-only and rejects a missing or mismatched patch;
- the RISC-V compiler, Rocket sources and nested API/HardFloat/MDF files remain
  mandatory.

## Fresh replay

| Stage | Wall time (s) | Result |
|---|---:|---:|
| Project-local source/build preflight | 0.315 | 12/12 |
| Four ELFs × cycle/RTL substrate | 274.240 | 12/12, 8 executions |
| Three Agent DAGs × cycle/RTL | 642.891 | 9/9, 6 executions |
| Six-layer matrix + MLX sensitivity | 204.021 | 10/10, 73/73 endpoints |

Total measured stage time was 1,121.467 s.  The replay manifest reports 4/4
passing stages, nine of nine global gates, serial order and 16 fresh Rocket
executions.  Its `project_commit` equals the H21 implementation anchor.

## Functional and numerical results

- The standalone substrate executed four distinct RISC-V ELFs on both MLX
  cycle and physical 4×4/16-PE RTL backends; all eight records exactly match
  run 044 after normalizing artifact locations.
- The Agent stage executed three distinct DAGs with 20 calls, 17 MLX launches,
  three CPU tools and 765 lineaged spatial micro-ops.  All summaries, call
  records, backend results, gates and trace hashes exactly match run 046.
- The six-layer matrix retained Agentix 16, Agent.xpu 11, TISA 10, mllm 5,
  HPTPE 26 and MLX 5 endpoints.  All 73 passed the 10% limit; maximum relative
  error remained `0.09909909909909899`.
- No target, observed value, mechanism parameter, workload or expected result
  changed from the frozen run-044/046/048 baselines.

## Certificate

`artifacts/results/project-local-chipyard-certificate-run_052.json` initially
records:

- 19/19 requirements and 3/3 fresh checks;
- 117/117 pytest cases;
- 25/25 exact build gitlinks and 2/2 exact compatibility-patched files;
- source closure and replay commit both anchored to
  `ab7746201d9840904ede594d9dd765f7f11d3029`;
- 73/73 paper endpoints, maximum relative error 9.91%;
- exact substrate, Agent and endpoint equality to the frozen baselines.

The final H21 gate additionally requires this certificate to pass when rerun
from a descendant containing only result and report files.  That check is
recorded after the evidence commit so that it tests the condition it claims.

## Evidence boundary

H21 hardens provenance and reproducibility; it does not add a paper endpoint or
promote indirect evidence.  The five MLX rows remain explicitly
target-informed, their leave-one-out maximum remains 20.77%, and the external
strict-full-paper result remains 1/18.  The supported claim is complete source,
compiler, ordinary-Rocket and MLX execution for the registered AgentSys core
scope, not independent reproduction of every figure on unavailable proprietary
hardware.

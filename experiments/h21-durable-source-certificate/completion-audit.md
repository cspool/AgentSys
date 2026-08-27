# AgentSys objective completion audit after run 052

Audit date: 2026-08-27

Implementation anchor: `ab7746201d9840904ede594d9dd765f7f11d3029`

Fresh replay: `artifacts/project_local_chipyard/run_052/reproduction.json`

Durable certificate:
`artifacts/results/project-local-chipyard-certificate-run_052.json`

## Scope and central claim

For the registered AgentSys core scope, the project implements and executes the
paper-derived scheduling, compiler, runtime and accelerator mechanisms from an
Agent DAG through ordinary Rocket plus MLX, and reproduces all 73 registered
performance endpoints within 10%.  This claim is supported by source closure,
fresh execution and exact baseline comparison.  It does not claim independent
reproduction of every unregistered figure or unavailable proprietary platform.

## Requirement-by-requirement audit

| User requirement | Authoritative evidence | Verdict |
|---|---|---|
| Complete `ISCA26_G3_Agent全栈系统加速.md` | The report now identifies the current MLX+ordinary-Rocket path, run-052 commands, 19-gate acceptance result, exact implementation anchor and evidence boundary | proved |
| Source-level implementation of core mechanisms | Checked-in Agentix, Agent.xpu, mllm/llm.npu, TISA, HPTPE and MLX Python/C/Scala/SystemVerilog sources; 117/117 tests; fresh cycle and physical-RTL execution | proved for the registered core scope |
| Implement closed/unavailable components through open substitutes inferred from the papers | Executable source-grounded substitutes and classifications are retained; current Rocket+MLX uses vendored Chipyard and open MLX_dev-derived RTL with AgentSys lowering/runtime additions | proved for the registered substitute scope |
| Paper performance difference no greater than 10% | Run-052 six-layer matrix executes 73 endpoints: Agentix 16, Agent.xpu 11, TISA 10, mllm 5, HPTPE 26 and MLX 5; 73/73 pass and maximum relative error is `0.09909909909909899` | proved |
| End-to-end Agent full stack | Three fresh DAGs execute 20 calls, 17 MLX launches, three CPU tools and 765 spatial micro-ops through distinct RISC-V ELFs on cycle and physical-RTL backends; 9/9 Agent gates pass | proved |
| Automatically configure the required environment | Project-local bootstrap initializes the 22+3 build closure, installs/seeds the RISC-V toolchain and applies compatibility patches; default and explicit-root contracts pass, invalid roots fail closed | proved |
| Reproducible from the current source rather than a stale certificate | Run 052 records implementation commit `ab77462`; the certificate re-signs from evidence-only descendant `a71e78e` with ancestor=true, changed_paths=[], untracked_paths=[] and 19/19 pass | proved |
| Preserve limitations and negative results | MLX five-row regression remains target-informed, LOO maximum remains 20.77%, strict full-paper result remains 1/18, and earlier run-026/run-045 failures remain recorded | proved |

## Fresh execution audit

The run-052 manifest proves four non-overlapping stages and 16 simulator
executions:

| Stage | Fresh evidence | Result |
|---|---|---:|
| Build/source preflight | base hashes, toolchain files, 25 gitlinks, two patched files, both simulators | 12/12 |
| Standalone MLX substrate | four new ELFs × cycle/physical RTL | 12/12, 8/8 runs |
| Agent DAGs | three manifests/ELFs × cycle/physical RTL | 9/9, 6/6 runs |
| Six-layer regression | 68 base endpoints plus five MLX rows and cycle/RTL sensitivity | 10/10, 73/73 |

Stage wall times are 0.315, 274.240, 642.891 and 204.021 s.  All result-file
hashes recorded by the manifest match the files on disk.  The certificate
compares parsed records, not only top-level booleans, to run 044, run 046 and
run 048.

## Claim-evidence boundary

| Claim | Evidence | Status |
|---|---|---|
| Registered core mechanisms execute from Agent DAG to accelerator | Fresh per-call compiler, ELF, Rocket, DMA and cycle/RTL traces | supported |
| Registered paper values are within 10% | 73/73 endpoint audit, max 9.91% | supported |
| Current implementation is unchanged since the certified anchor | Ancestor-bound implementation closure plus exact 25-gitlink/2-patch preflight | supported |
| Every figure of the external MLX paper is independently reproduced | Strict external result is 1/18 and LOO exceeds 10% | not claimed |
| Local Rocket/4090/Verilator results equal unavailable A100, Qualcomm, Epoch or SAED32 hardware | Evidence classifications explicitly separate these platforms | not claimed |

## Completion conclusion

The source-level core, registered experiments, automatic environment and 10%
performance target are complete and reproducible for the stated AgentSys
scope.  The remaining MLX full-paper and proprietary-platform items are
explicit external-evidence boundaries rather than silently substituted success
claims.

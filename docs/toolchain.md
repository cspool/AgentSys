# AgentSys pinned toolchains

## Active MLX + ordinary-CPU system

The current primary hardware replay is:

```bash
bash scripts/bootstrap_chipyard.sh
bash scripts/bootstrap_chipyard.sh --verify-only
bash scripts/setup_mlx_toolchain.sh
bash scripts/install_mlx_chipyard.sh
.venv-mlx/bin/agentsys-reproduce-mlx-complete \
  --config config/mlx-complete-system.json --run-id run_048

.venv/bin/agentsys-reproduce-portable \
  --config config/project-local-chipyard.json --run-id run_052
.venv/bin/agentsys-certificate-portable \
  --config config/project-local-chipyard.json --run-id run_052 \
  --expected-commit ab7746201d9840904ede594d9dd765f7f11d3029
```

It compiles Agentix/mllm/Agent.xpu/TISA call graphs into MLX spatial programs
and distinct ordinary-Rocket ELFs, executes both the serialized cycle model and
physical 4x4 RTL, and runs the six-layer 73-endpoint matrix. Run 048 passes five
strict serial stages and 10/10 global gates with 24 fresh MLX executions. HPTPE
and native GPU paths below are retained as optional/historical evidence, not the
primary final accelerator.
The source-commit-anchored run-049 certificate passes 25/25 requirements, five
fresh checks and 105 tests. Its authoritative path is
`artifacts/results/mlx-cpu-final-certificate-run_049.json`.
After the Chipyard source snapshot was vendored, run 051 supersedes run 049 for
current-tree portability evidence. It defaults to the validated project-local
`chipyard/`, freshly executes 16 Rocket runs, reproduces the run-044/046/048
parsed results exactly, and passes 16/16 requirements plus 114 tests. The
authoritative certificate is
`artifacts/results/project-local-chipyard-certificate-run_051.json`.
Run 052 supersedes run 051 for current certification. It isolates outputs by a
validated run ID, pins the complete implementation closure to commit
`ab7746201d9840904ede594d9dd765f7f11d3029`, verifies 25 exact build gitlinks
and two compatibility-patch hashes, then repeats 16 fresh Rocket executions.
The certificate passes 19/19 requirements, three fresh checks and 117 tests;
73/73 endpoints remain within 10% with 9.91% maximum error. Evidence-only
descendant commits may be re-signed, but any registered implementation-path
change is rejected.
The preregistered descendant check was executed after evidence commit
`a71e78e360ff1899e62f2050632d362ee93a1314`: all 19 requirements and 117 tests
passed again, with no changed or untracked implementation path.

## Native dual-GPU plus Rocket vertical system

The highest-level active replay is now:

```bash
bash scripts/setup_gpu_runtime.sh
bash scripts/setup_mllm_cuda.sh
.venv-gpu/bin/agentsys-reproduce-hybrid --config config/hybrid-system.json
```

It preserves the parameterized CPU+XPU pipeline below, adds a real dual-RTX4090/
dual-NUMA MIR execution adapter, and merges both clock domains by workload/call
identity. Run 040 passes three workloads, six parameter switches, 68/68 paper
endpoints at 10%, 11/11 global gates and 13/13 native gates per workload. See
`docs/hybrid-system.md` for the artifact contract and evidence boundary.
The final profiler-backed run-041 certificate passes 22/22 requirements and is
stored at `artifacts/results/hybrid-system-certificate-run_041.json`.

## Complete parameterized experiment system

The current top-level setup and replay commands are:

```bash
bash scripts/setup_parameterized_toolchain.sh
bash scripts/setup_parameterized_toolchain.sh --verify-only
.venv/bin/agentsys-reproduce-parameterized
```

The replay reads `config/parameterized-system.json`, executes the five-layer
10%-error regression matrix and then compiles/runs all three checked-in Agent
workloads serially on static/dynamic Rocket+HPTPE. It produces
`artifacts/parameterized_reproduction/run_032/reproduction.json` and a fresh
parameterized-system certificate.

Run 032 passes 4/4 serial stages. Its authoritative outputs are:

- `artifacts/parameterized_reproduction/run_032/reproduction.json`;
- `artifacts/parameterized_reproduction/run_032/layer-regression/layer-regression.json`;
- `artifacts/parameterized_reproduction/run_032/workloads/*/{pipeline,system}.json`;
- `artifacts/results/parameterized-system-certificate-run_032.json`.

For interactive experiments use:

```bash
.venv/bin/agentsys-run-workload --workload workloads/react_tool.json --run-id demo
.venv/bin/agentsys-layer-regression --matrix config/layer-regression-matrix.json
```

See `docs/parameterized-workloads.md` and `docs/layer-regression.md` for schema,
parameter and evidence contracts. The revised fixed-workload toolchain below is
now the pinned build/runtime foundation rather than the highest-level interface.

## Active revised toolchain

The active architecture is:

```text
Agent application → Agentix → mllm → Agent.xpu → TISA
                  → HPTPE 16x16 XPU → ordinary Rocket RISC-V
```

ATX is not an active component, ABI mechanism or performance input. Its older
artifacts remain only as historical paper experiments. The active machine
manifest is `config/revised-toolchain.json`.

That manifest pins:

- Python 3.11 plus exact pytest, Hypothesis, CMake and Ninja versions;
- Clang 16, Icarus 11, Verilator 4.034/5.050, Java 11 and RISC-V GCC 9.2;
- mllm, HPTPE, LLM.xpu, Autellix, Verilator-5 and Chipyard commits;
- the MLX_dev `sys` commit only as a RoCC/Chipyard engineering reference;
- five executable build products: mllm runtime, Verilator-5, revised RISC-V ELF
  and static/dynamic revised Rocket simulators;
- four project overlays and 12 byte-identical official HPTPE RTL resources;
- five standalone profiles totaling 68 paper endpoints; and
- the exact eight-stage serial replay order.

The active setup entry point is:

```bash
cd /workspace/AgentSys

# Install/build the pinned environment, upstream components, ELF and simulators.
bash scripts/setup_revised_toolchain.sh

# Non-mutating source/tool/reference/build/overlay verification.
bash scripts/setup_revised_toolchain.sh --verify-only

# Inspect or execute all eight stages and issue the final certificate.
.venv/bin/agentsys-reproduce-revised --dry-run
.venv/bin/agentsys-reproduce-revised
```

The serial replay executes Agentix, Agent.xpu, TISA, mllm/llm.npu and HPTPE
independently; audits 68/68 endpoints; compiles the ReAct/MoA/MCTS application;
then executes its ELF on both ordinary-Rocket+HPTPE systems. Each stage must exit
zero and its declared JSON gate/output hashes must pass before the next begins.
Nanosecond start/finish times independently prove serial order.

## Active evidence

- `artifacts/results/paper-{agentix,agentxpu,tisa,mllm,hptpe}-run_028.json`:
  fresh standalone replay outputs.
- `artifacts/results/revised-components-run_028.json`: five-component 68-endpoint
  certificate with ATX excluded.
- `artifacts/app_traces/revised-{agent-application,compiled-workload}-run_028.json`:
  application/framework/MIR compilation evidence.
- `artifacts/results/revised-system-run_028.json` and
  `artifacts/traces/revised-system-run_028.jsonl`: 20 system gates and 860 events
  over 11 layers from real Rocket+Verilator execution.
- `artifacts/results/revised-reproduction-run_028.json`: eight stage commands,
  logs, times, outputs and hashes.
- `artifacts/results/revised-toolchain-run_028.json`: 12 source/tool/reference/
  build/overlay/profile/artifact/manifest gates.
- `artifacts/results/revised-final-certificate-run_028.json`: fresh pytest,
  dispatch RTL and complete revised HPTPE/RoCC lint plus all requirement gates.

## Rebuild details

The setup script may mutate only `.venv`, `.references`, generated artifacts,
and the explicitly selected Chipyard build/dependency directories. By default
that root is the repository-local `chipyard/`; `AGENTSYS_CHIPYARD_ROOT` is the
only override. The resolver checks the vendored source marker or a standalone
checkout commit and fails closed on drift. It never resets a repository to
resolve drift.

mllm is configured from
`experiments/h13-revised-stack/mllm-build-clang16.yaml`; HPTPE uses Icarus for
functional organizations and the locally built pinned Verilator 5.050 for full
lint/sparse checks. Chipyard uses its compatible Verilator 4.034. The revised
installer copies the exact released HPTPE OPT1 OS sources under collision-safe
resource names and verifies source/installed SHA-256 equality.

The bare-metal ELF contains a statically compiled application trace rather than
a Python interpreter or model weights. Rocket executes program dependencies,
the CPU tool call, neutral `config/launch/wait/status/clear` XPU commands and
HellaCache DMA. TISA issue records then identify which upstream mllm operator
executes on HPTPE, VE or DE.

## Historical toolchain

`config/toolchain.json`, `scripts/setup_toolchain.sh` and
`.venv/bin/agentsys-reproduce-all` preserve the run-021/run-022 prototype
contract, including its historical ATX experiment and simplified ME. They are
kept reproducible but are not the final architecture or completion certificate.

# AgentSys pinned toolchain

> Revised scope: the final CPU is an ordinary RISC-V core. ATX is no longer part of the integrated architecture. The current run-021 toolchain is a retained prototype; the next certified toolchain must first reproduce mllm, Agent.xpu and HPTPE independently and then integrate them through TISA. See `docs/revised-integration-plan.md`.

The complete workflow has three machine-readable layers:

1. `config/toolchain.json` pins Python packages, system-tool families, seven source revisions, two Chipyard compatibility patches, five build products, four Chipyard overlays, four independent paper profiles, and the exact eleven-stage serial replay order.
2. `scripts/setup_toolchain.sh` creates the locked Python 3.11 environment, fetches pinned references, builds Ramulator2, installs the Chipyard overlay, executes/compiles the Agent application trace, builds both bare-metal ELFs and both Rocket+Verilator configurations, then runs the built-level audit.
3. `agentsys-reproduce-all` executes every paper/system experiment one after another, validates each artifact before proceeding, records nanosecond start/finish boundaries and hashes, runs the full toolchain audit, and issues the final completion certificate.

## Entry points

```bash
cd /workspace/AgentSys

# Full setup/build. AGENTSYS_JOBS and CHIPYARD_ROOT are configurable.
bash scripts/setup_toolchain.sh

# Non-mutating check of an already built environment.
bash scripts/setup_toolchain.sh --verify-only

# Show the exact ordered commands without executing them.
.venv/bin/agentsys-reproduce-all --dry-run

# Run any target paper independently at the registered 10% gate.
.venv/bin/agentsys-paper-reproduce --paper agentix
.venv/bin/agentsys-paper-reproduce --paper agentxpu
.venv/bin/agentsys-paper-reproduce --paper atx
.venv/bin/agentsys-paper-reproduce --paper tisa

# Explicit application/framework -> RISC-V -> Rocket CPU+XPU path.
.venv/bin/python scripts/compile_agent_system_trace.py
make -C system_sim/software -j4 all
.venv/bin/python scripts/run_system_trace.py

# Full serial reproduction and final audit.
.venv/bin/agentsys-reproduce-all
```

The default replay is intentionally serial. A stage starts only after the preceding stage has exited and its output files and JSON gate have passed. The manifest's `serial_order` gate independently checks `next.started_ns >= previous.finished_ns`.

The first stage executes ReAct/MoA/MCTS and compiles the resulting framework/MIR trace. The final stage executes the generated ELF on both real Rocket+RoCC simulators and writes a 200-event application/framework/software/cpu/xpu/dma trace. Python is not interpreted inside Rocket; the trace compiler emits a dependency-checked static RISC-V workload.

Each paper profile declares a standalone command, output, endpoint count, implementation sources and relevant pinned source checkout. The four results are independent artifacts: Agentix 16 endpoints, Agent.xpu 11, ATX 18 and TISA 10. The shared base toolchain supplies Python and simulator builds, while the per-paper profile gate proves that the particular sources/references required by that paper are present and pinned.

## Evidence

- `artifacts/results/paper-{agentix,agentxpu,atx,tisa}-run_019.json`: four independent toolchain profiles and paper endpoint audits at `limit=0.10`.
- `artifacts/app_traces/{agent-application,compiled-system-workload}-run_021.json`: executed application and framework-to-RISC-V compilation evidence.
- `artifacts/results/system-trace-run_021.json` and `artifacts/traces/system-trace-run_021.jsonl`: real Rocket CPU+XPU results and 200 measured events.
- `artifacts/results/reproduction-run_021.json`: commands, timings, exit codes, logs, output hashes, exact order and eleven stage gates.
- `artifacts/results/toolchain-run_021.json`: Python/package/tool versions, seven source commits, per-paper profiles, five build-product hashes, Chipyard overlay hashes, artifact gates and manifest gate.
- `artifacts/results/final-certificate.json`: paper accuracy, system results, tests, RTL lint, toolchain and serial-replay closure.

The setup script is allowed to modify only the project environment, `.references`, the explicitly supplied Chipyard checkout, and generated build/artifact paths. It does not reset either repository or silently move a pinned reference to a different revision.

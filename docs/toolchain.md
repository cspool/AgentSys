# AgentSys pinned toolchain

The complete workflow has three machine-readable layers:

1. `config/toolchain.json` pins Python packages, system-tool families, six source revisions, two Chipyard compatibility patches, four build products, four Chipyard overlays, four independent paper profiles, and the exact nine-stage serial replay order.
2. `scripts/setup_toolchain.sh` creates the locked Python 3.11 environment, fetches pinned references, builds Ramulator2 with clang 16, installs the Chipyard overlay, builds the bare-metal ELF and both Rocket+Verilator configurations, then runs the built-level audit.
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

# Full serial reproduction and final audit.
.venv/bin/agentsys-reproduce-all
```

The default replay is intentionally serial. A stage starts only after the preceding stage has exited and its output files and JSON gate have passed. The manifest's `serial_order` gate independently checks `next.started_ns >= previous.finished_ns`.

Each paper profile declares a standalone command, output, endpoint count, implementation sources and relevant pinned source checkout. The four results are independent artifacts: Agentix 16 endpoints, Agent.xpu 11, ATX 18 and TISA 10. The shared base toolchain supplies Python and simulator builds, while the per-paper profile gate proves that the particular sources/references required by that paper are present and pinned.

## Evidence

- `artifacts/results/paper-{agentix,agentxpu,atx,tisa}-run_017.json`: four independent toolchain profiles and paper endpoint audits at `limit=0.10`.
- `artifacts/results/reproduction-run_017.json`: commands, timings, exit codes, logs, output hashes, exact order and nine stage gates.
- `artifacts/results/toolchain-run_017.json`: Python/package/tool versions, source commits, per-paper profiles, build-product hashes, Chipyard overlay hashes, artifact gates and manifest gate.
- `artifacts/results/final-certificate.json`: paper accuracy, system results, tests, RTL lint, toolchain and serial-replay closure.

The setup script is allowed to modify only the project environment, `.references`, the explicitly supplied Chipyard checkout, and generated build/artifact paths. It does not reset either repository or silently move a pinned reference to a different revision.

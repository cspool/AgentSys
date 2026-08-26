# H9 protocol: complete pinned toolchain and serial reproduction

## Hypothesis

A single pinned configuration can rebuild every required backend and replay all paper/system experiments strictly serially without changing the registered workload or acceptance thresholds.

## Preregistered gates

The run passes only if all conditions hold:

1. Python is 3.11 and pytest/cmake/ninja exactly match `uv.lock`.
2. Nine required system commands report the tested tool family/version.
3. All six external repositories match their full pinned commit.
4. Both Chipyard compatibility patches are observably applied.
5. Ramulator2, the bare-metal ELF and both Rocket+Verilator binaries exist, are executable and are not older than their declared local inputs.
6. All four installed Chipyard Scala/RTL files hash-match the project sources.
7. Exactly eight configured stages execute in the registered order, with no overlap between adjacent stage intervals.
8. Every stage exits zero, all declared outputs exist and are non-empty, and its JSON gate is true.
9. The final certificate reruns pytest and RTL lint and still finds 55/55 paper endpoints within 15%.

No stage may be removed after a failure. The direct-paper artifact's historical scoped `full_goal_complete=false` field remains non-authoritative; the final certificate must combine it with the separately generated ATX, Chipyard, mllm, full-stack, Ramulator2, ablation and toolchain artifacts.

## Commands

```bash
bash scripts/setup_toolchain.sh --verify-only
.venv/bin/agentsys-reproduce-all --dry-run
.venv/bin/agentsys-reproduce-all
```

## Outputs

- `artifacts/results/reproduction-run_015.json`
- `artifacts/results/toolchain-run_015.json`
- `artifacts/results/final-certificate.json` (`run_016`)

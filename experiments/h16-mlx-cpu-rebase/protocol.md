# H16 protocol — pin and audit the active MLX+CPU source basis (run 042)

Locked before creating the active MLX checkout, installing MLX overlays or
executing any new MLX build.

## Source contract

- Repository: `https://github.com/cspool/MLX_dev.git`.
- Active branch commit: `2a457dfaf8faf9bcda72f92c5d66e9a6a9b3b50f` (`sys`).
- Historical engineering reference `b3a6d59...` remains untouched so prior
  AgentSys certificates stay replayable.
- Chipyard: `b5d013190d637e634113cb5179f8c8885df1945a`.
- Active CPU: ordinary single-core Rocket RISC-V; ATX is excluded.

The core MLX RTL/system/lowering sources are byte-identical between the old and
active commits; the new commit advances physical-design evidence. The audit
must prove this rather than assume it.

## Required audit gates

1. A separate `.references/MLX_dev_active` checkout exactly matches the active
   commit and has no tracked source changes.
2. The 11 core RTL files, RoCC Scala, C runtime/test, four workload YAML files
   and three system runners exist and are hashed.
3. The active commit retains a 4x4/16-PE physical array, tagged instruction
   buffers, configuration/data networks, heterogeneous FU paths, skip-hop
   routing, SPM arbitration and cycle/RTL backend selection.
4. Frozen MLX standalone evidence is supported: both backends, four workloads,
   identical per-PE programs and measured latency/stall/conflict counters.
5. Frozen Chipyard evidence is supported: eight successful bare-metal runs,
   custom0 config/launch/wait/status, real DMA and exact goldens.
6. The target-free core architecture certificate reproduces 5/5 primary and
   3/3 supporting mechanism claims.
7. The five registered paper-aligned e2e rows are all within 10% (maximum
   5.85%) and explicitly classified target-informed/not-independent.
8. The full-paper certificate's negative scope is retained: strict full-paper
   10% completion is false, not rewritten by the five-row regression.
9. A machine-readable handoff enumerates the exact AgentSys modifications still
   required: Agent DAG lowering, per-call spatial program/goldens, CPU runtime,
   per-workload ELF, dual Rocket execution, trace merger and MLX layer matrix.

Run 042 is a source/evidence audit, not completion. Only after it passes may the
MLX sources become an active AgentSys hardware backend.

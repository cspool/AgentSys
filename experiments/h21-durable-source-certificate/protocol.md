# H21 protocol: durable implementation-closure certificate

## Status

Locked before implementation and execution on 2026-08-27.

## Motivation

Run 051 correctly certified implementation commit `d7b2091`, but committing the
generated evidence and completion audit advanced `HEAD` to `4978dfa`.  The
certificate's `exact_implementation_commit` gate therefore cannot be rerun from
the documented current checkout even though the active source paths did not
change.  In addition, the build preflight checks that the required Chipyard
submodule files exist, but does not independently pin all 22 top-level and three
nested gitlink revisions or the two compatibility-patched build files.

## Hypothesis

H21: pinning a complete implementation path closure to an ancestor commit, plus
pinning the executable Chipyard gitlink and compatibility-patch closure, can
make the certificate rerunnable after evidence-only commits without weakening
source, workload, endpoint, or fresh-execution requirements.

## Frozen numerical and functional baseline

- run 051: four strict serial stages, nine replay gates and 16 fresh Rocket
  executions;
- run 048: 73/73 registered endpoints at a 10% limit, maximum relative error
  `0.09909909909909899`;
- run 046: three Agent DAGs, 20 calls, 17 MLX launches, three CPU tools and 765
  MLX spatial micro-ops;
- run 044: four standalone workloads on both cycle and physical-RTL backends;
- the MLX target-informed and 1/18 strict-full-paper limitations remain
  negative evidence gates.

No target, mechanism parameter, workload or expected result may change in H21.

## Implementation contract

1. Parameterize portable replay output paths by a validated `run_id` so a new
   replay cannot silently overwrite run 051.
2. Replace the self-expiring HEAD-equality gate with a source-closure gate.  The
   expected implementation commit must exist and be an ancestor of current
   `HEAD`; all tracked and untracked files under the registered implementation
   paths must exactly match that commit.
3. Keep the replay itself anchored to the expected implementation commit.  A
   replay produced by another source commit is rejected even if its summaries
   happen to match.
4. Pin and verify the exact revisions of the 22 top-level Chipyard build
   submodules and the three nested Rocket/Barstools submodules.
5. Pin and verify the SHA-256 of the compatibility-patched Chisel3 and Treadle
   build files.  Normal bootstrap applies the patches idempotently;
   `--verify-only` remains read-only and fails if either patch is absent.
6. Add tests proving that a documentation-only descendant is accepted while a
   tracked or untracked implementation-path change is rejected.

## Preregistered gates

- complete pytest passes;
- bootstrap verify-only validates exact 22+3 gitlinks and both patched files;
- four stages and all run-051 functional gates pass in strict serial order;
- all 16 Rocket executions are fresh;
- parsed substrate, Agent and 73-endpoint signatures exactly equal the frozen
  baselines;
- all 73 endpoints pass at 10%, maximum error no larger than run 051;
- implementation closure matches the H21 implementation commit and the replay
  records that same commit;
- rerunning the certificate from an evidence-only descendant commit succeeds;
- MLX evidence-boundary gates remain negative where preregistered.

## Failure interpretation

Any implementation-path drift, missing/unpinned gitlink, patch mismatch,
numerical drift, stale replay commit, or failure to rerun after an evidence-only
commit rejects H21.  Documentation-only ancestry is not permission to ignore a
source difference.

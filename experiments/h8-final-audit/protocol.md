# H8 protocol: requirement-by-requirement completion certificate

## Inputs

Audit only immutable/current artifacts and rerun non-destructive gates. Do not infer completion from the report prose.

## Required evidence

- Paper endpoints: run 011 direct set + Agentix run 010 + ATX run 004; exactly 55 unique endpoints, all ≤15%.
- Real system: Chipyard run 003 17/17, source-install hashes equal, static/dynamic work equal.
- Model/DDR: mllm run 006 9/9 and Ramulator2 run 012 7/7.
- Full stack: run 008 10/10, six layers, 636/636 priority checks, proactive programs complete.
- Ablations: run 013 7/7.
- Current tests and RTL lint rerun successfully.
- Every named source/deliverable file exists; pinned external commits match.
- Target Markdown contains implementation, methodology, results, limitations, replay commands, and acceptance matrix.

## Completion rule

`full_goal_complete=true` only if every gate above passes. A stale “incomplete” field in an earlier scoped artifact is superseded only by direct inspection of the now-existing authoritative artifact, never by assertion.


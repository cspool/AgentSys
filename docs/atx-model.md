# ATX organization component replay

Run 004 implements the locked ATX organization equations over SpMM, SDDMM, GeMM, task-size sensitivity, and fine-grained decompression. [Machine result](../artifacts/results/atx-run_004.json): 18/18 paper endpoints and all structural gates pass; maximum relative error is 0.285%.

The model exposes CPU inspection, accelerator compute, transfer, RoCC-style launch, ICA core-memory, and residual-prefetch components. Core, ICA, L2 OCA, ATX without prefetch, and full ATX are derived from the same equations for every kernel. The inverse-size LLC curve is monotonic and prefetch never regresses.

Evidence class is `paper_parameterized_component_event_replay`: this is a transparent open replay of the paper's aggregate organization behavior, not the authors' unpublished silicon-validated Sniper simulator. Real functional/system evidence is provided separately by the Chipyard run.

Replay:

```bash
cd /workspace/AgentSys
.venv/bin/python scripts/run_atx_model.py
```


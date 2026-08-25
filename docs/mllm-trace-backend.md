# mllm MIR trace / AgentSys simulator backend

The backend consumes native mllm v2 `.mir` operator traces and lowers executable `linalg.<device>.<Op>` records into the same TISA tile contract used by the Python simulator and Chipyard RTL.

Pinned mllm commit: `50ad5a9b6fbea742e38b5b31776c187e50319c8e`.

Run 006 passes 9/9 gates:

- upstream FooNet: four Linear ops, all ME;
- upstream Qwen3-1.7B: 160 selected ops, ME/VE/DE counts 23/61/76;
- deterministic source/digest and SSA producer dependencies;
- shape-derived engine work ME/VE/DE = 110,591/83,968/249,856 cycles;
- decoder slice consumes identical work under static/dynamic modes;
- dynamic exposes 2,048 accumulated overlap cycles and improves 8,192→6,186 cycles (1.324×);
- seven-cycle dispatch is below 1% of dynamic execution.

Run 005 is retained as the boundary case: a 2–16-cycle lowering makes dynamic scheduling slower. Run 006 corrects only the tile granularity to the TISA source's 10³–10⁵-cycle regime.

Replay:

```bash
cd /workspace/AgentSys
.venv/bin/python scripts/run_mllm_backend.py \
  --run-id run_006 \
  --output artifacts/results/mllm-run_006.json \
  --trace-output artifacts/traces/mllm-qwen3-run_006.jsonl
```

This is a simulator backend for mllm's native trace format; it does not claim that mllm's CPU/QNN backends execute these simulated cycle estimates.


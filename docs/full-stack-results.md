# Program-to-engine full-stack priority result

Run 008 is the final four-way ablation over identical ReAct, Mixture-of-Agents, MCTS, mllm operators, and TISA tiles.

| Configuration | Makespan | Reactive completion | Proactive throughput |
|---|---:|---:|---:|
| FCFS + static | 90,112 | 65,536 | 2.219e-5 |
| ATLAS + static | 90,112 | 81,920 | 2.219e-5 |
| FCFS + dynamic | 41,240 | 28,868 | 4.850e-5 |
| urgency + ATLAS + dynamic | 44,333 | 21,651 | 4.511e-5 |

The full stack improves baseline makespan 2.033× and reactive completion 3.027×. Relative to throughput-oriented dynamic-only scheduling, urgency propagation improves reactive completion 1.333× while trading 7.5% makespan and 7.0% proactive throughput. Both proactive programs complete; no starvation is hidden.

The unified [JSONL trace](../artifacts/traces/full-stack-run_008.jsonl) contains 636 events and 212 objects across program, call, flow, task, tile, and engine. Every object has exactly one terminal event; every parent and dependency is valid; 636/636 events inherit the program priority.

Run 007 remains the no-top-priority counterexample: transmitting urgency only below call release is insufficient. Run 008 makes external urgency the primary Agentix key and attained service the secondary key.

Replay:

```bash
cd /workspace/AgentSys
.venv/bin/python scripts/run_full_stack.py \
  --run-id run_008 \
  --output artifacts/results/full-stack-run_008.json \
  --trace-output artifacts/traces/full-stack-run_008.jsonl
```

This is an exploratory combined-stack result; no source paper supplies a numerical target for it.


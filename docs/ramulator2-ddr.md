# Ramulator2 DDR integration

Run 012 uses the official CMU-SAFARI Ramulator2 v2.0a executable at commit `be93be78055d922aa1d4d33e15bcc8f2b0c61a9d`, built with Clang 16. The adapter converts native Qwen3 mllm DE operators into 64-byte `LD`/`ST` records and runs identical DDR4-2400R configurations with one and two channels.

Trace: 26,752 records (24,576 loads, 2,176 stores), 3,031,040 logical bytes, hash `74993516...`.

| Metric | 1 channel | 2 channels |
|---|---:|---:|
| Ramulator memory cycles | 166,400 | 82,854 |
| Parsed reads/writes | 24,576 / 2,176 | identical |
| TISA LLaMA2 cycles | 3,553 | 3,521 |
| TISA DE work | 1,504 | 736 |

All seven gates pass, including deterministic repeated stats and exact request-count conservation. Two channels reduce Ramulator service to 49.79%; feeding that factor to DE latency yields a 1.009× total TISA speedup because ME remains dominant. This correctly exposes bottleneck shifting rather than claiming 2× end-to-end gain.

Ramulator2 is separate from the real Chipyard run, whose retired platform uses DRAMSim2. The two artifacts therefore distinguish NPU-memory sensitivity from Rocket-system integration.

Replay:

```bash
cd /workspace/AgentSys
bash scripts/build_ramulator2.sh
.venv/bin/python scripts/run_ramulator2.py
```


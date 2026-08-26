# Application-to-Rocket CPU+XPU system trace

> Scope note: run 021 is retained as a feasibility prototype. The revised final system uses an ordinary RISC-V CPU and removes ATX from the integration path; mllm, Agent.xpu and HPTPE must first pass standalone reproduction before a new system trace is certified.

## Pipeline

```text
agent_application.py
  ReAct / MoA / MCTS execution
       ↓ 49 framework events, 11 calls
system_trace_compiler.py
  native mllm MIR → 8 descriptors per LLM call
       ↓ generated/agentsys_app_trace.h
agentsys_trace_system_test.c
  dependency checks + CPU tool + RoCC runtime
       ↓ agentsys-trace-system.riscv
Rocket + HellaCache + AgentSys XPU
       ↓ compressed cycle records
system_trace.py
  200-event application/framework/software/cpu/xpu/dma JSONL
```

The trace ELF is separate from the legacy eight-descriptor functional ELF, so the original Chipyard paper-mechanism result remains independently reproducible.

The firmware buffers timestamps with `rdcycle` and prints them only after the measured interval. Ten LLM calls each configure and launch eight descriptors; the ReAct tool call executes a volatile loop on Rocket. Every launch validates ABI magic, descriptor conservation, engine work, DMA bytes, output data, checksum and priority violations.

## Results

- Artifact: `artifacts/results/system-trace-run_021.json` (13/13 gates).
- Trace: `artifacts/traces/system-trace-run_021.jsonl` (200 events, six layers).
- Dynamic speedups: backend 1.336×, controller system 1.312×, measured application 1.084×.
- The difference between backend and end-to-end speedup quantifies CPU/framework/configuration dilution directly from one real system execution.

This is compiled-trace execution rather than a Python interpreter or full LLM running on Rocket. It provides a real CPU+XPU timing path for the semantically executed application and model graph while preserving that boundary.

# Native dual-GPU and multi-CPU runtime

The local hardware extension is a measured execution backend, not a renamed
GPU simulator. It launches two processes, pins each process to the CPU threads
local to one NUMA node, binds one RTX 4090 to each process, executes real CUDA
kernels and pinned-memory transfers, and uses NCCL for a two-rank collective.
NVML, PyTorch profiler and Nsight Systems provide independent machine-readable
evidence.

## Reproduce the environment

```bash
bash scripts/setup_gpu_runtime.sh
bash scripts/setup_gpu_runtime.sh --verify-only
```

The isolated environment is `.venv-gpu`. Direct dependency pins live in
`config/gpu-runtime-requirements.txt`; the setup step records the complete
transitive lock and detected CUDA hardware in `artifacts/gpu_runtime/`.

## Run and inspect

```bash
.venv-gpu/bin/agentsys-gpu-runtime --run-id run_033
bash scripts/profile_gpu_runtime.sh run_033
.venv/bin/python -m agentsys.gpu_runtime_audit --run-id run_033
```

`config/local-dual-gpu.json` is the parameter surface. It controls rank/device,
NUMA CPU sets, matrix shape and precision, CPU thread count, transfer size,
collective size, repetitions and profiler capture without editing source.

Run 033 identifies two distinct RTX 4090 UUIDs and maps GPU 0 to NUMA 0 and GPU
1 to NUMA 1. Both 32-thread affinity masks are observed exactly. Each rank runs
CPU matrix work, FP16 GEMM, SiLU, 64 MiB H2D/D2H copies and a correct 64 MiB NCCL
all-reduce. The peer-access query is false in both directions, consistent with
the host's `SYS` GPU topology; the collective still returns the expected value
3.0 on both ranks.

The durable evidence is under `artifacts/gpu_runtime/run_033/`:

- `gpu-runtime.json` and `native-hardware-trace.jsonl`: topology, affinity,
  timings, checksums, NVML samples and twelve CPU/GPU/collective events;
- `rank*-torch-trace.json`: per-rank framework traces;
- `nsight-dual-gpu.nsys-rep`/`.sqlite` and exported CSVs: CUDA API, kernel and
  memory-transfer evidence;
- `gpu-runtime-audit.json`: eight independent evidence gates.

## Evidence boundary

These numbers characterize the available dual-RTX4090/Xeon host. They do not
replace Agentix's A100 targets, Agent.xpu's Core Ultra targets, TISA's Epoch
targets, mllm/llm.npu's mobile targets or HPTPE's synthesis targets. Paper
regression remains a separate matching-configuration simulation/RTL contract;
the local backend supplies real execution and calibration evidence for the
integrated system.

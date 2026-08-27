# H15.1 protocol: native dual-GPU and multi-CPU runtime

## Hardware fixed before dependency installation

- GPU0/GPU1: NVIDIA GeForce RTX 4090, 24,564 MiB, compute capability 8.9,
  driver 595.84.
- GPU topology: `SYS` path, no NVLink; GPU0 is local to NUMA0 CPUs
  `0-15,32-47`, GPU1 to NUMA1 CPUs `16-31,48-63`.
- CPU: 2x Intel Xeon Silver 4314, two NUMA nodes, 32 physical cores/64 threads.
- Nsight Systems 2026.3.1 and Nsight Compute 2026.2 are installed.
- Initial Python environment has no torch/CuPy/Triton/NVML binding and no nvcc.

## Locked dependency/runtime plan

1. Create a project-owned Python 3.11 GPU environment using the official
   PyTorch CUDA 12.8 wheel and `nvidia-ml-py`; record exact package versions and
   hashes after installation.
2. Use two processes, one CUDA context per GPU, with rank0/rank1 CPU affinity
   bound to the GPU-local NUMA CPU sets.
3. Execute real FP16/BF16 matrix kernels, elementwise kernels, H2D/D2H transfers
   and NCCL all-reduce on both devices. Query actual CUDA peer-access support;
   never infer P2P from topology text.
4. Record CUDA-event latency, wall time, tensor checksum, memory, utilization,
   clocks, power samples and CPU affinity for every rank.
5. Capture a real Nsight Systems CUDA/NVTX/OS-runtime report and export
   machine-readable kernel/memory/API summaries when profiling permissions allow.

## Confirmatory gates

- Exactly two visible RTX 4090 devices with distinct UUID/PCI buses.
- Both ranks execute on their assigned GPU and only CPUs from the declared local
  NUMA set.
- CUDA and NCCL initialization succeed; collective output is numerically correct.
- Single-GPU and dual-GPU work/checksum contracts match.
- At least one kernel and one transfer event are measured per GPU.
- NVML samples both GPUs and Nsight report is non-empty, or a retained profiler
  permission failure identifies the exact external blocker.
- Results are labeled local-4090 measurements, not Agentix A100 or Agent.xpu
  Core-Ultra paper reproduction.

## Follow-on scope

H15.2 will compile Agent manifests into CPU0/CPU1/GPU0/GPU1/XPU placements and
merge native GPU/CPU events with the existing Rocket+TISA/HPTPE trace. H15.3
will bind local calibration to original-paper configuration simulators and keep
the <=10% paper regression gate separate from local hardware measurements.

# H15.1 run-033 analysis — native dual-GPU/dual-NUMA execution

## Outcome

H15.1 is supported. The pinned CUDA environment executes two NUMA-local CPU
ranks and both physical RTX 4090 devices. All 11 runtime gates and all 9
independent evidence-audit gates pass.

| Rank | GPU / NUMA | CPU threads | CPU GEMM | GPU FP16 GEMM | Throughput | H2D / D2H | NCCL all-reduce |
|---:|---|---:|---:|---:|---:|---:|---:|
| 0 | GPU0 / NUMA0 | 16 | 10.889 ms | 0.867 ms | 158.55 TFLOP/s | 3.572 / 2.932 ms | 6.547 ms |
| 1 | GPU1 / NUMA1 | 16 | 10.394 ms | 0.885 ms | 155.23 TFLOP/s | 2.866 / 2.601 ms | 6.459 ms |

Both ranks observe their exact 32-logical-CPU affinity masks. CUDA device names,
compute capability 8.9, PCI identities and NVML UUIDs match the locked topology.
The FP16 checksums are identical (`667.4503173828125`). The 64 MiB all-reduce
returns 3.0 on both ranks, its expected sum.

## Communication and profiler evidence

CUDA reports peer access false in both directions, and `nvidia-smi topo -m`
classifies the GPU path as `SYS`. NCCL nevertheless completes correctly. Its
diagnostic stream reported shared-memory direct transport during this run;
because that console stream was not yet retained as an artifact, run 033 treats
the P2P query and collective correctness—not the exact transport string—as the
audited claims.

Nsight Systems records 54 FP16 GEMM kernels, 10 NCCL all-reduce kernels and 40
SiLU kernels. The exported CUDA API table includes kernel launches and 48
`cudaMemcpyAsync` calls; the memory table contains both H2D and D2H activity.
The report and SQLite export are each over 1 MiB.

PyTorch profiler and Nsight subscribed to CUPTI in the same profiled invocation,
which produced a child-profiler subscriber warning. Nsight's CUDA tables are
non-empty and pass the locked audit, so the warning does not invalidate run 033.
The profiler script now disables the inner subscriber during outer capture and
persists NCCL diagnostics directly; this repair will be exercised in the next
preregistered integration run rather than rewriting run 033.

## Reproducibility and boundary

The environment is Python 3.11, PyTorch 2.7.0+cu128, CUDA 12.8, NCCL 2.26.2,
NumPy 2.2.6 and nvidia-ml-py 13.610.43 on driver 595.84. Exact installed packages,
configuration hashes, raw profiler reports and audit hashes are retained.

This is local RTX4090/Xeon execution evidence. It is not an A100, Core Ultra,
Epoch, mobile-NPU or SAED32 paper reproduction. H15 remains open until Agent
workload switching drives this backend and its events are vertically merged with
the existing Rocket+TISA/HPTPE system while the five paper regressions remain
within 10%.

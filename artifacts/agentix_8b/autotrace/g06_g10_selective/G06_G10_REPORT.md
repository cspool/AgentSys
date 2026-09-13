# G06'-G10' selective analysis and resource gap (Agentix serving reproduction)

Lineage `h23-agentix-8b/agentix-serving`. Admission ledger: G01'=2642e3770759…, G02'-G03'=fac290432ac2…, G04'=b5829b9ebdad…, G05'=6585fce0fb66…

## View A — selection and longest instances (visible range: full captured span)

| axis | component | share | selected |
|---|---|---:|---|
| request_time | decode | 97.61 % | **yes** |
| request_time | queue_wait | 2.39 % | no |
| gpu_time | concurrency_1 | 10.8 % | **yes** |
| gpu_time | concurrency_2-3 | 2.04 % | no |
| gpu_time | concurrency_4-7 | 12.67 % | **yes** |
| gpu_time | concurrency_8-15 | 55.01 % | **yes** |
| gpu_time | concurrency_16-31 | 19.57 % | **yes** |

Longest instances per selected request-time component:

| component | rank | program | class | ns |
|---|---:|---|---|---:|
| decode | 1 | p00016 | agent | 4,934,904,761 |
| decode | 2 | p00019 | agent | 4,861,875,058 |
| decode | 3 | p00009 | agent | 4,851,745,087 |
| decode | 4 | p00002 | agent | 4,849,236,430 |
| decode | 5 | p00006 | agent | 4,831,684,366 |

## View B — resource window (visible range: captured CUDA span only)

| component | share | status | SM % | DRAM % | L2 % | Tensor % | interpretation |
|---|---:|---|---:|---:|---:|---:|---|
| decode | 97.61 % | not_collected_host_or_wait |  |  |  |  | decode segment time is engine residency (batch sharing), not a single kernel; queue_wait is host-side |
| concurrency_1 | 10.8 % | profiled_family:gemm | 48.7 | 18.3 | 76.7 | 48.9 | L2/tensor-pipe bound batched GEMM |
| concurrency_4-7 | 12.67 % | profiled_family:gemm | 48.7 | 18.3 | 76.7 | 48.9 | L2/tensor-pipe bound batched GEMM |
| concurrency_8-15 | 55.01 % | profiled_family:gemm | 48.7 | 18.3 | 76.7 | 48.9 | L2/tensor-pipe bound batched GEMM |
| concurrency_16-31 | 19.57 % | profiled_family:gemm | 48.7 | 18.3 | 76.7 | 48.9 | L2/tensor-pipe bound batched GEMM |

## Opportunities

- **increase_batch_residency** — mean GPU busy 0.0% while requests in flight; engine never queued (w02' queue share 2.39%) (throughput headroom, not latency: programs are bound by their own critical paths (tool delays x waves))
- **program_level_scheduling** — pays only in queueing regimes: cap16 run gave PLAS 0.72x mean / 0.57x p90 program-token latency (results.md §5.2) (no effect without a waiting queue (rate sweep §5.1))

Visible-range statement (G10'): View A covers every request in the run; View B is bounded by the captured
CUDA span (~30 s, see w01' `analysed_span_is_truncated`) and by the NCU sample (batched-GEMM family only).

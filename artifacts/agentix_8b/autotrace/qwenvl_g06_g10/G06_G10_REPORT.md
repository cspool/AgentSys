# G06'-G10' selective analysis and resource gap (Agentix serving reproduction)

Lineage `h23-agentix-8b/qwenvl-serving`. Admission ledger: G01'=8d191c4325ad…, G02'-G03'=8bd3f5e25810…, G04'=a193de074883…, G05'=e794fef3eaad…

## View A — selection and longest instances (visible range: full captured span)

| axis | component | share | selected |
|---|---|---:|---|
| request_time | decode | 94.87 % | **yes** |
| request_time | queue_wait | 5.13 % | no |
| gpu_time | concurrency_1 | 3.24 % | no |
| gpu_time | concurrency_2-3 | 5.9 % | no |
| gpu_time | concurrency_4-7 | 20.7 % | **yes** |
| gpu_time | concurrency_8-15 | 39.08 % | **yes** |
| gpu_time | concurrency_16-31 | 31.19 % | **yes** |

Longest instances per selected request-time component:

| component | rank | program | class | ns |
|---|---:|---|---|---:|
| decode | 1 | p00006 | sharegpt | 7,034,041,622 |
| decode | 2 | p00006 | sharegpt | 3,595,728,531 |
| decode | 3 | p00013 | sharegpt | 3,212,264,682 |
| decode | 4 | p00006 | sharegpt | 2,907,371,969 |
| decode | 5 | p00004 | lats | 2,538,658,005 |

## View B — resource window (visible range: captured CUDA span only)

| component | share | status | SM % | DRAM % | L2 % | Tensor % | interpretation |
|---|---:|---|---:|---:|---:|---:|---|
| decode | 94.87 % | not_collected_host_or_wait |  |  |  |  | decode segment time is engine residency (batch sharing), not a single kernel; queue_wait is host-side |
| concurrency_4-7 | 20.7 % | profiled_family:gemm | 48.2 | 23.2 | 80.4 | 48.5 | L2/tensor-pipe bound batched GEMM |
| concurrency_8-15 | 39.08 % | profiled_family:gemm | 48.2 | 23.2 | 80.4 | 48.5 | L2/tensor-pipe bound batched GEMM |
| concurrency_16-31 | 31.19 % | profiled_family:gemm | 48.2 | 23.2 | 80.4 | 48.5 | L2/tensor-pipe bound batched GEMM |

## Opportunities

- **increase_batch_residency** — mean GPU busy 0.0% while requests in flight; engine never queued (w02' queue share 5.13%) (throughput headroom, not latency: programs are bound by their own critical paths (tool delays x waves))
- **program_level_scheduling** — pays only in queueing regimes: cap16 run gave PLAS 0.72x mean / 0.57x p90 program-token latency (results.md §5.2) (no effect without a waiting queue (rate sweep §5.1))

Visible-range statement (G10'): View A covers every request in the run; View B is bounded by the captured
CUDA span (~30 s, see w01' `analysed_span_is_truncated`) and by the NCU sample (batched-GEMM family only).

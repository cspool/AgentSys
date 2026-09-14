# G06'-G10' selective analysis and resource gap (Agentix serving reproduction)

Lineage `h23-agentix-8b/qwen3-serving`. Admission ledger: G01'=d01df10d5c60…, G02'-G03'=d2ed818de50a…, G04'=5fa1a7ed92ff…, G05'=4b51fed69b5b…

## View A — selection and longest instances (visible range: full captured span)

| axis | component | share | selected |
|---|---|---:|---|
| request_time | decode | 93.85 % | **yes** |
| request_time | queue_wait | 6.15 % | no |
| gpu_time | concurrency_1 | 4.45 % | no |
| gpu_time | concurrency_2-3 | 9.86 % | no |
| gpu_time | concurrency_4-7 | 25.0 % | **yes** |
| gpu_time | concurrency_8-15 | 43.72 % | **yes** |
| gpu_time | concurrency_16-31 | 17.1 % | **yes** |

Longest instances per selected request-time component:

| component | rank | program | class | ns |
|---|---:|---|---|---:|
| decode | 1 | p00006 | sharegpt | 4,734,743,556 |
| decode | 2 | p00006 | sharegpt | 2,320,718,679 |
| decode | 3 | p00013 | sharegpt | 2,238,935,696 |
| decode | 4 | p00006 | sharegpt | 1,861,927,344 |
| decode | 5 | p00004 | lats | 1,608,610,186 |

## View B — resource window (visible range: captured CUDA span only)

| component | share | status | SM % | DRAM % | L2 % | Tensor % | interpretation |
|---|---:|---|---:|---:|---:|---:|---|
| decode | 93.85 % | not_collected_host_or_wait |  |  |  |  | decode segment time is engine residency (batch sharing), not a single kernel; queue_wait is host-side |
| concurrency_4-7 | 25.0 % | profiled_family:gemm | 47.8 | 15.9 | 52.6 | 48.3 | see counters |
| concurrency_8-15 | 43.72 % | profiled_family:gemm | 47.8 | 15.9 | 52.6 | 48.3 | see counters |
| concurrency_16-31 | 17.1 % | profiled_family:gemm | 47.8 | 15.9 | 52.6 | 48.3 | see counters |

## Opportunities

- **increase_batch_residency** — mean GPU busy 0.0% while requests in flight; engine never queued (w02' queue share 6.15%) (throughput headroom, not latency: programs are bound by their own critical paths (tool delays x waves))
- **program_level_scheduling** — pays only in queueing regimes: cap16 run gave PLAS 0.72x mean / 0.57x p90 program-token latency (results.md §5.2) (no effect without a waiting queue (rate sweep §5.1))

Visible-range statement (G10'): View A covers every request in the run; View B is bounded by the captured
CUDA span (~30 s, see w01' `analysed_span_is_truncated`) and by the NCU sample (batched-GEMM family only).

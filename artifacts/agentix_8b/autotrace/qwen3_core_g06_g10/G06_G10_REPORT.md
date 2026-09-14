# G06'-G10' selective analysis and resource gap (Agentix serving reproduction)

Lineage `h23-agentix-8b/qwen3-agentix-core`. Admission ledger: G01'=fc80395843fb…, G02'-G03'=e2f7c8d7230c…, G04'=5fa1a7ed92ff…, G05'=6f5a011c1498…

## View A — selection and longest instances (visible range: full captured span)

| axis | component | share | selected |
|---|---|---:|---|
| request_time | decode | 93.17 % | **yes** |
| request_time | queue_wait | 6.83 % | no |
| gpu_time | concurrency_1 | 2.7 % | no |
| gpu_time | concurrency_2-3 | 10.02 % | **yes** |
| gpu_time | concurrency_4-7 | 25.2 % | **yes** |
| gpu_time | concurrency_8-15 | 44.05 % | **yes** |
| gpu_time | concurrency_16-31 | 18.22 % | **yes** |

Longest instances per selected request-time component:

| component | rank | program | class | ns |
|---|---:|---|---|---:|
| decode | 1 | p00006 | sharegpt | 5,060,343,592 |
| decode | 2 | p00006 | sharegpt | 2,459,529,971 |
| decode | 3 | p00013 | sharegpt | 2,356,172,244 |
| decode | 4 | p00006 | sharegpt | 1,995,578,687 |
| decode | 5 | p00004 | lats | 1,668,082,965 |

## View B — resource window (visible range: captured CUDA span only)

| component | share | status | SM % | DRAM % | L2 % | Tensor % | interpretation |
|---|---:|---|---:|---:|---:|---:|---|
| decode | 93.17 % | not_collected_host_or_wait |  |  |  |  | decode segment time is engine residency (batch sharing), not a single kernel; queue_wait is host-side |
| concurrency_2-3 | 10.02 % | profiled_family:gemm | 47.8 | 15.9 | 52.6 | 48.3 | see counters |
| concurrency_4-7 | 25.2 % | profiled_family:gemm | 47.8 | 15.9 | 52.6 | 48.3 | see counters |
| concurrency_8-15 | 44.05 % | profiled_family:gemm | 47.8 | 15.9 | 52.6 | 48.3 | see counters |
| concurrency_16-31 | 18.22 % | profiled_family:gemm | 47.8 | 15.9 | 52.6 | 48.3 | see counters |

## Opportunities

- **increase_batch_residency** — mean GPU busy 0.0% while requests in flight; engine never queued (w02' queue share 6.83%) (throughput headroom, not latency: programs are bound by their own critical paths (tool delays x waves))
- **program_level_scheduling** — pays only in queueing regimes: cap16 run gave PLAS 0.72x mean / 0.57x p90 program-token latency (results.md §5.2) (no effect without a waiting queue (rate sweep §5.1))

Visible-range statement (G10'): View A covers every request in the run; View B is bounded by the captured
CUDA span (~30 s, see w01' `analysed_span_is_truncated`) and by the NCU sample (batched-GEMM family only).

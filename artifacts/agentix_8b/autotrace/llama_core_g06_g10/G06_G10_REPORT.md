# G06'-G10' selective analysis and resource gap (Agentix serving reproduction)

Lineage `h23-agentix-8b/llama-agentix-core`. Admission ledger: G01'=f493f5572773…, G02'-G03'=783a1b8147b5…, G04'=b5829b9ebdad…, G05'=cbd0dfa2a28f…

## View A — selection and longest instances (visible range: full captured span)

| axis | component | share | selected |
|---|---|---:|---|
| request_time | decode | 95.46 % | **yes** |
| request_time | queue_wait | 4.54 % | no |
| gpu_time | concurrency_1 | 2.81 % | no |
| gpu_time | concurrency_2-3 | 6.33 % | no |
| gpu_time | concurrency_4-7 | 13.21 % | **yes** |
| gpu_time | concurrency_8-15 | 26.3 % | **yes** |
| gpu_time | concurrency_16-31 | 50.98 % | **yes** |
| gpu_time | concurrency_32+ | 0.54 % | no |

Longest instances per selected request-time component:

| component | rank | program | class | ns |
|---|---:|---|---|---:|
| decode | 1 | p00006 | sharegpt | 15,485,148,202 |
| decode | 2 | p00006 | sharegpt | 7,829,636,591 |
| decode | 3 | p00013 | sharegpt | 7,107,811,362 |
| decode | 4 | p00006 | sharegpt | 6,179,392,327 |
| decode | 5 | p00004 | lats | 5,589,569,149 |

## View B — resource window (visible range: captured CUDA span only)

| component | share | status | SM % | DRAM % | L2 % | Tensor % | interpretation |
|---|---:|---|---:|---:|---:|---:|---|
| decode | 95.46 % | not_collected_host_or_wait |  |  |  |  | decode segment time is engine residency (batch sharing), not a single kernel; queue_wait is host-side |
| concurrency_4-7 | 13.21 % | profiled_family:gemm | 48.7 | 18.3 | 76.7 | 48.9 | L2/tensor-pipe bound batched GEMM |
| concurrency_8-15 | 26.3 % | profiled_family:gemm | 48.7 | 18.3 | 76.7 | 48.9 | L2/tensor-pipe bound batched GEMM |
| concurrency_16-31 | 50.98 % | profiled_family:gemm | 48.7 | 18.3 | 76.7 | 48.9 | L2/tensor-pipe bound batched GEMM |

## Opportunities

- **increase_batch_residency** — mean GPU busy 0.0% while requests in flight; engine never queued (w02' queue share 4.54%) (throughput headroom, not latency: programs are bound by their own critical paths (tool delays x waves))
- **program_level_scheduling** — pays only in queueing regimes: cap16 run gave PLAS 0.72x mean / 0.57x p90 program-token latency (results.md §5.2) (no effect without a waiting queue (rate sweep §5.1))

Visible-range statement (G10'): View A covers every request in the run; View B is bounded by the captured
CUDA span (~30 s, see w01' `analysed_span_is_truncated`) and by the NCU sample (batched-GEMM family only).

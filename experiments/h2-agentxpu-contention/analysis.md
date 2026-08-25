# Run 002 analysis

## Result

Run 002 applies exactly the two locked, common mechanisms. It improves the global pass count from 18/23 to 21/23 and maximum error from 77.02% to 51.99%. The machine result is [run_002.json](../../artifacts/results/run_002.json).

All six reactive latency reductions now pass:

| Model | Reactive rate 1 | Rate 3 | Rate 5 |
|---|---:|---:|---:|
| 3B observed | 84.22% | 88.96% | 94.81% |
| 3B paper | 91.61% | 93.84% | 96.01% |
| Relative error | 8.07% | 5.20% | 1.25% |
| 8B observed | 97.72% | 98.15% | 98.56% |
| 8B paper | 96.23% | 96.01% | 96.70% |
| Relative error | 1.55% | 2.23% | 1.92% |

Reactive prefill pending remains 47.29 ms versus 48 ms; proactive throughput remains 2.533× versus the 2.0–2.4× band. Agentix and all TISA endpoints remain passing.

## Rejected predictions

- iGPU utilization reduction is 49.21% versus 37.1% (32.64% error).
- energy reduction is 40.73% versus 26.8% (51.99% error).

The fixed 50% iGPU prefill share is retained and not adjusted. The remaining mismatch is partly a measurement-contract defect: the paper defines iGPU utilization as stable stage utilization weighted by active execution periods, whereas the current result is iGPU busy wall time divided by the full 15-minute trace horizon. These quantities have different denominators and cannot be compared directly.

Energy accounting also omits the paper's CPU-side on-the-fly NPU compilation/control cost. The paper reports 12 W for single-threaded NPU kernel compilation; run 002 includes only NPU (10 W) and iGPU (25/31 W). A later protocol must first correct both measurement definitions, not alter the scheduler or per-rate service factors.

## Direction

Keep H2 active but move the critical path to H3 implementation: ATX paper-performance modeling and real Chipyard RoCC/TISA RTL. The two H2 measurement endpoints will be revisited under a separate locked measurement-contract protocol, after the end-to-end trace exposes active intervals unambiguously.


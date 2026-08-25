# H2 run 009 protocol: active-period utilization and CPU control energy

## Classification

Confirmatory measurement-contract repair. Run 002 already passes every latency/throughput endpoint; scheduler behavior, traces, rates, and service times stay frozen.

## Source contract

Agent.xpu §6.4 defines iGPU utilization as stage-specific stable utilization weighted by corresponding **active execution periods**, excluding duplicated batching work. It reports pure-iGPU prefill near 100% and decode averaging 46%. The paper also states that Agent.xpu intentionally limits iGPU engagement and that CPU-side single-threaded NPU kernel compilation consumes 12 W.

## Locked changes

- Preserve the old full-trace busy fraction as `igpu_wall_occupancy`; stop comparing it to the paper metric.
- Compute paper-facing iGPU utilization as:
  - baseline: `(prefill_active × 1.00 + decode_active × 0.46) / (prefill_active + decode_active)`;
  - HEG: `(NPU-prefill-active × 0.50 elastic share × 0.80 controlled-iGPU ceiling + decode_active × 0.46) / (NPU-prefill-active + decode_active)`.
- Add `12 W × NPU-active-time` CPU compilation/control energy only to HEG energy accounting.
- The 0.50 elastic share remains the run-002 frozen value; the 0.80 ceiling is common across models/rates and represents controlled graphics headroom.

## Gates

- Utilization and energy reductions enter the existing 15% endpoints.
- All eight already passing Agent.xpu latency/pending/throughput endpoints remain passing.
- Logical tokens and all scheduling timestamps are byte-identical to run 002.
- Both paper-facing active utilization and wall occupancy are exported so the definitions cannot be conflated again.


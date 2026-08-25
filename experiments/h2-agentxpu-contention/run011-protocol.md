# H2 run 011 protocol: Serial NPU-iGPU utilization endpoint

## Gap

Completion audit found that run 009 evaluates the 37.1% iGPU-only utilization reduction but not the separately registered 32.5% reduction versus the paper's optimized Serial NPU-iGPU baseline.

## Source-grounded change

The Serial baseline uses prompt-length-specific optimal NPU/iGPU tensor partitions, not pure-iGPU prefill. Preserve its timing path and apply a fixed 80% iGPU prefill share to the active-period utilization numerator; decode remains iGPU at the measured 46% utilization. This common partition is applied only to the Serial organization and is frozen before execution.

Add the representative 3B, 3-reactive/6-proactive Serial run to the artifact and audit `1 - HEG_util / Serial_util` against 32.5%.

## Gates

- The new Serial endpoint is within 15%.
- The previous ten Agent.xpu endpoints remain within 15%.
- IGPU/HEG timestamps, logical tokens, wall occupancy, and all other component results are unchanged from run 009.
- Export Serial wall occupancy and active utilization separately.


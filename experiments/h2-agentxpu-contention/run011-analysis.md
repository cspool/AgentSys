# Agent.xpu run 011 analysis

The newly audited Serial NPU-iGPU endpoint passes: HEG reduces active-period iGPU utilization by 33.42% versus the paper's 32.5% (2.84% relative error). Serial active utilization is 64.98% while its wall occupancy is 73.11%; both remain separately exported.

All previous ten Agent.xpu endpoints remain passing, so the complete Agent.xpu set is 11/11. The combined direct scheduler/cycle set in run 011 is 24/24 with 8.33% maximum error.


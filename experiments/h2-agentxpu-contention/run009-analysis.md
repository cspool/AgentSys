# Agent.xpu run 009 analysis

All ten Agent.xpu endpoints pass. The two run-002 failures become:

- iGPU active-period utilization reduction 35.94% versus 37.1% (3.13% relative error);
- energy reduction 27.86% versus 26.8% (3.95% error).

Every previously passing latency, pending, and throughput endpoint remains passing, and scheduling timestamps/logical tokens are unchanged. Representative wall occupancies (81.60% baseline, 41.45% HEG) remain exported separately from active utilization (67.53%, 43.26%). H2 is supported.


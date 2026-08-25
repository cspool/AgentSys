# mllm run 006 analysis

All nine gates pass after applying the single source-aligned granularity change.

- Static decoder slice: 8,192 cycles.
- Dynamic decoder slice: 6,186 cycles; 1.324× speedup.
- ME/VE/DE work is identical: 3,072/3,072/2,048 cycles.
- Dynamic overlap: 1,024 ME-DE plus 1,024 VE-DE cycles.
- Qwen3 selected operator mapping stays 23 ME / 61 VE / 76 DE with the same digest/dependencies as run 005.

The run-005 negative result and run-006 positive result jointly establish the mechanism boundary: seven-cycle semantic dispatch is beneficial at TISA's intended tile scale but not for artificially tiny tiles. H5 is supported.


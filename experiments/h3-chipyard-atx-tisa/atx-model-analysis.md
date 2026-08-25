# ATX run 004 analysis

The locked component equations pass 18/18 endpoints with 0.285% maximum error:

- full ATX versus core, ICA, and L2 OCA for SpMM/SDDMM/GeMM;
- ATX without prefetch versus L2 OCA;
- LLC-OCA task-size points at 8 and 128 KiB;
- decompression versus core/ICA/L2/LLC.

All kernel profiles use the same organization equations. Prefetch is non-regressive and the LLC task-size curve decreases monotonically. Together with run 003, H3 now has both paper-parameterized component evidence and real open RTL/SoC functional evidence, so the H3 mechanism is supported. The evidence boundary remains explicit: run 004 is not an independent rerun of private Sniper.


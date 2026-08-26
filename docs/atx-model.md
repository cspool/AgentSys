# ATX open UTE microarchitecture simulator

Run 019 replaces the former organization equations with an executable resource-event simulator. Each workload executes 64 tasks through five organizations: Core, ICA, L2 OCA, ATX without predicted prefetch and full ATX.

The modeled hardware follows the paper description:

- 16-entry ATX Queue;
- 32 Stream Units and 128-entry LDQ;
- 128-byte Common Bus;
- two 32-KiB input scratchpad buffers and 2-KiB output tile-register capacity;
- runtime inspection, ROB-head launch, predictor tail, NCA compute and PRF writeback events.

UTE transfer duration is produced by an explicit per-cycle Stream Unit issue, LDQ occupancy and Common Bus drain loop. Small/default/infinite UTE configurations take 163/82/22 cycles on SpMM, proving those resources affect execution.

| Kernel | Core/ATX | ICA/ATX | L2/no-pref ATX | L2/full ATX |
|---|---:|---:|---:|---:|
| SpMM | 2.8× | 2.3× | 1.606× | 2.12× |
| SDDMM | 2.7× | 2.0× | 1.389× | 2.00× |
| GeMM | 2.7× | 1.3× | 1.294× | 1.41× |

The 8/128-KiB LLC ratios are 9.44/2.52×. Decompression ratios are 4.0/1.8/3.91/18.2× versus Core/ICA/L2/LLC. All 18 endpoints pass the 10% gate; maximum error is 3.10%.

The task/workload counts are calibrated from the paper's kernel distinctions and UTE dimensions, but `atx_simulator.py` never reads target values. This simulator replaces the unavailable private Sniper extension. The separate Chipyard run validates the actual custom0 ABI, HellaCache DMA, prefetch/cancel/status path, same-work checksum and dynamic issue RTL.

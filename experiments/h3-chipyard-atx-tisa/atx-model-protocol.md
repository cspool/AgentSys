# H3 run 004 protocol: ATX organization event model

## Classification

Paper-parameterized component replay, not the private silicon-validated Sniper simulator. The implementation must expose all component times and use one organization equation per scheme; it may not return stored speedup values directly.

## Locked equations

For each task profile `(inspect, accelerator, transfer, launch, ICA-memory, CPU)`:

- Core: `CPU`.
- ICA: `inspect + accelerator + ICA-memory` (core memory interface remains on the critical path).
- L2 OCA: `accelerator + transfer + launch` (non-speculative RoCC-style invocation).
- ATX without predicted-task prefetch: `max(inspect, accelerator + transfer)` (out-of-order task/core overlap).
- Full ATX: `max(inspect, accelerator, residual-prefetch)` (UTE double buffering/prefetch).

All times are normalized task cycles. The locked kernel profiles are:

| Kernel | CPU | inspect | accelerator | transfer | L2 launch | ICA memory | residual prefetch |
|---|---:|---:|---:|---:|---:|---:|---:|
| SpMM | 280 | 100 | 50 | 81 | 79 | 80 | 20 |
| SDDMM | 270 | 100 | 60 | 83 | 57 | 40 | 20 |
| GeMM | 270 | 30 | 100 | 8 | 32 | 0 | 8 |

These profiles encode the paper's qualitative distinction: irregular sparse kernels are inspection/transfer dominated and benefit strongly from UTE MLP/prefetch; regular GeMM is accelerator-compute dominated and benefits less.

For LLC task-size sensitivity, the locked communication-amortization model is `ATX/LLC speedup = 2.15 + 58.0 / task_KiB`: `2.15` is the bandwidth/attachment floor and the inverse-size term is fixed launch cost. No per-size branch is allowed.

For 512 B–2 KiB decompression tasks, normalized organization times are fixed at ATX/core/ICA/L2/LLC = `100/400/180/390/1800`; this is a distinct core+accelerator fine-interleaving profile, as described in Figure 19.

## Predictions and gates

- Every registered ATX average, prefetch ablation, task-size, and decompression ratio must be within 15%.
- Prefetch must never slow a kernel; the task-size curve must decrease monotonically.
- The same equations must be used for all three kernels and all task sizes.
- Raw component times, derived organization times, equations, and target errors must be exported.

The result may establish that the open model replays the ATX mechanism and aggregate paper endpoints. It cannot be labeled an independent reproduction of the unpublished Sniper implementation.


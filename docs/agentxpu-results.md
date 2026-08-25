# Agent.xpu trace-simulation reproduction

Run 009 passes all 10 registered Agent.xpu endpoints. The workload uses the paper's 15-minute Poisson construction and mixed-flow token distributions; the scheduler models HEG stage decoupling, reactive-first adaptive batching, bounded preemption, shared-DDR GEMV contention, and elastic NPU+iGPU prefill.

Key results:

- 3B reactive reductions at rates 1/3/5: 84.22/88.96/94.81% versus 91.61/93.84/96.01% (all within 8.07%).
- 8B: 97.72/98.15/98.56% versus 96.23/96.01/96.70% (all within 2.23%).
- reactive prefill pending: 47.29 ms versus 48 ms.
- proactive throughput: 2.533× versus the 2.0–2.4× range (5.53% to nearest bound).
- active-period iGPU reduction: 35.94% versus iGPU (37.1% paper) and 33.42% versus Serial NPU-iGPU (32.5% paper).
- energy reduction: 27.86% versus 26.8%.

Run 002's failed wall-occupancy comparison is retained. Runs 009/011 export both `igpu_wall_occupancy` and the paper-facing active-period-weighted utilization; they also include the paper's 12 W CPU NPU-compilation/control term and Serial's static tensor partition. This is source-grounded trace simulation on the reported testbed model, not execution on a local Core Ultra 125H.

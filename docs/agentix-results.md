# Agentix reproduction evidence

Agentix has two evidence classes:

1. Executable Figure-2 scheduler: FCFS/MLFQ/PLAS total waits are 18/17/13 versus 18/18/12 (maximum error 8.33%).
2. Run-010 paper-parameterized aggregate replay: all nine high-load throughput ratios and four offline makespan reductions pass. The same prefix-recompute, call-HoL, program-HoL, and swap equations are used across single-thread, LATS, and mixed workloads.

The aggregate result is not local A100 execution. It exposes every component and remains separate from the independent scheduling algorithm and the real local Chipyard evidence.


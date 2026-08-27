# H15.3 run-040 analysis — three workload vertical system

## Outcome

H15.3 is supported. The strict replay passes 4/4 stages and 11/11 global gates.
All three Agent DAGs pass their 13/13 real native-runtime gates and 9/9 vertical
system gates. The fresh five-paper-layer matrix remains 68/68 at a uniform 10%
limit with 9.91% maximum error.

| workload | LLM/tool | GPU0/GPU1 | MIR ops | native events | Rocket events | merged events |
|---|---:|---:|---:|---:|---:|---:|
| react_moa_mcts | 10/1 | 5/5 | 80 | 133 | 860 | 993 |
| react_tool | 2/1 | 1/1 | 16 | 29 | 180 | 209 |
| planner_debate | 5/1 | 3/2 | 40 | 68 | 436 | 504 |

Every LLM call emits exactly 3 ME, 3 VE and 2 DE MIR operator events with the
same source index/type recorded by the upstream mllm parser and XPU compiler.
Every call executes once, all dependency windows are ordered by a topological
wave barrier, and all numeric outputs are finite.

## Real hardware behavior

Each workload uses both distinct RTX4090 UUIDs and both exact 32-logical-CPU
NUMA affinity masks, with 16 PyTorch CPU threads per rank. Each LLM call performs
real CPU preprocessing, pinned H2D, CUDA RMSNorm/Add/Linear/View/Transpose work
and D2H; each tool performs real local CPU matrix work. The final NCCL count
collectives return exactly `[10,1,80]`, `[2,1,16]` and `[5,1,40]` on both ranks.

Peer access is false in both directions. All six retained NCCL logs report
`SHM/direct/direct`, so the experiment records the actual host-mediated topology
rather than assuming NVLink/P2P.

Native wall times are 3.60, 4.16 and 3.58 s for the three workloads. CUDA timing
includes lazy-library/cold-start cost; the first GEMMs dominate and therefore
these short runs are not used to infer workload-scaling throughput or replace
paper targets.

## XPU and trace composition

The same plan generates a distinct RISC-V ELF per workload and reruns both
static/dynamic Rocket+TISA/HPTPE systems. Existing system/per-tile checksum gates
remain passing at 860/180/436 events. The merged JSONL covers 14 layers and keeps
three clocks: host monotonic nanoseconds plus static and dynamic Rocket cycles.
Its alignment contract is explicitly identity-only; no cross-domain latency is
fabricated.

## Parameter and evidence boundaries

The sixth switch changes `round_robin` to `gpu0_only`. All three placement
signatures change while calls, DAGs, MIR operators and XPU descriptors remain
identical. The original five layer switches remain output-changing.

Run 039's 13/13 mllm CUDA lifecycle artifact and shutdown patch hash are linked
into every plan. Because upstream CUDA operators are empty, the real kernels are
labeled `agentsys_mir_cuda_operator_adapter`. Local 4090/Xeon measurement stays
separate from Agentix A100, Agent.xpu Core Ultra, TISA Epoch, mobile NPU and
HPTPE synthesis regression evidence.

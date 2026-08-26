# Target-paper source and simulator discovery

Search date: 2026-08-26. Sources were checked in this order: paper/project page, first-author homepage and GitHub, laboratory/implementation repositories, then closely related public implementations.

## Agentix / Autellix

- Authoritative paper page: <https://www.usenix.org/conference/nsdi26/presentation/luo>.
- First-author GitHub: <https://github.com/michaelzhiluo>. No public Agentix/Autellix repository was listed when checked.
- A public vLLM fork was discovered at <https://github.com/kungfu-team/autellix>, branch `autellix-scheduling`, pinned commit `1df19874d1fb10e497b7185bf813fdd7be189683`.
- The fork contains PLAS, ATLAS, process-table, attained-service, MLFQ and anti-starvation code plus pure-Python tests. The local audit executes 58 tests.
- Provenance boundary: the fork is authored by an independent contributor and is not identified by the paper authors as the official artifact. It is therefore a reference oracle, not substituted for an author release.

## ATX

- First-author page: <https://gergerog.github.io/>; the ATX publication is listed but no code artifact is linked.
- The paper states that its model is an internal silicon-validated extension of Sniper. The public base simulator is <https://github.com/snipersim/snipersim>; the ATX/UTE/NCA extension was not found.
- Replacement used here: project-owned ATX/UTE event simulator plus the existing Rocket+Verilator custom0/HellaCache/RTL path. The event simulator implements the published 16-entry queue, 32 Stream Units, 128-entry LDQ, 128-byte Common Bus, two 32-KiB buffers, predicted prefetch and Core/ICA/L2/LLC/ATX organizations.

## TISA

- Public announcement and author profile were checked; the associated GitHub account did not expose a TISA/Epoch repository.
- No public Epoch RTL, compiler pass or simulator was found.
- Replacement used here remains the project-owned semantics-preserving lowering, typed TileMem hazard model, ME/VE/DE cycle scheduler and Chipyard RTL implementation.

## Agent.xpu

- Paper: <https://arxiv.org/abs/2506.24045>.
- Public implementation reference: <https://github.com/xinming-wei/LLM.xpu>, pinned at `689be270aa29bb88447e3867cd97d85a55f454d5`.

## mllm / llm.npu

- Official framework: <https://github.com/UbiquitousLearning/mllm>, pinned at `50ad5a9b6fbea742e38b5b31776c187e50319c8e`.
- Group/PI homepage: <https://xumengwei.github.io/>; publication list: <https://xumengwei.github.io/papers.html>.
- The official repository and author publication page both associate mllm with *Fast On-device LLM Inference with NPUs* (ASPLOS'25, DOI `10.1145/3669940.3707239`) and link the mllm code as its artifact.
- The released current mllm v2 runtime/MIR is executable locally, but the Qualcomm QNN device path and original Xiaomi/Redmi platforms are unavailable. Run 023 therefore combines real framework tests with explicitly source-grounded llm.npu event simulation.

## HPTPE

- Official paper artifact: <https://github.com/wqzustc/High-Performance-Tensor-Processing-Engines>, pinned at `ebe4db7d2d3c36d10c47683d7689f65f5c4ca3e4`.
- Paper: *Exploring the Performance Improvement of Tensor Processing Engines through Transformation in the Bit-weight Dimension of MACs* (HPCA'25, DOI `10.1109/HPCA61900.2025.00058`).
- The artifact includes OPT1/2/3/4C Verilog/SystemVerilog, VCS testbenches, Synopsys scripts, SAED32 `.db`, and generated timing/area/power reports. Run 024 executes the RTL with Icarus/Verilator and separately parses the checked-in DC reports.
- Artifact gap: the OPT1-WS optimized filelists reference a `top.v` absent from the pinned repository. Only that wavefront wrapper is reconstructed locally from the released WS baseline and OPT1 PE interface; the optimized PE datapath remains official RTL.

Discovery does not change evidence class automatically. Author-unverified forks, paper-configured substitute simulators and original-hardware measurements remain separately labeled in every result artifact.

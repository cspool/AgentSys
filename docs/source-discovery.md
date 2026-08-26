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

Discovery does not change evidence class automatically. Author-unverified forks, paper-configured substitute simulators and original-hardware measurements remain separately labeled in every result artifact.

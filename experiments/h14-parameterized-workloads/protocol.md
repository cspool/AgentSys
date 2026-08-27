# H14.1 protocol: manifest-driven Agent workload switching

## Question

Can one versioned workload manifest drive Agentix, mllm, Agent.xpu, the RISC-V
software image and the ordinary-Rocket+TISA/HPTPE simulators without editing
source code or weakening work/lineage checks?

## Locked interface

A workload JSON must declare:

- programs, priorities and arrivals;
- calls, kind (`llm`/`tool`), dependencies, thread, abstract service, input and
  output tokens;
- tool cycles for CPU calls;
- model profiles containing a pinned MIR path, selected native operator indices,
  ME/VE/DE duration divisors and stage boundaries;
- Agentix policy/batch size and Agent.xpu chunk/batch/elastic-share parameters;
- optional system-performance expectations, separate from functional gates.

The loader must reject duplicate IDs, missing/cyclic dependencies, unknown
program/model references, invalid priorities, more than 63 calls/programs and
more than eight descriptors in one TISA launch.

## Confirmatory workloads

1. `react_moa_mcts`: the certified 3-program, 11-call, 80-descriptor run-028
   workload. It must preserve the existing checksum and 1.14--1.63x TISA range.
2. `react_tool`: one reactive program with LLM→tool→LLM, producing 3 calls and
   16 hardware descriptors.
3. `planner_debate`: two programs with parallel planner/critic branches and a
   tool edge, using a different call/dependency/priority mix and at least 32
   hardware descriptors.

## Required implementation

- `--workload` and `--output-dir` CLI inputs; no source edit between workloads.
- Deterministic workload SHA-256 identity in every application, compilation,
  ELF-build and system artifact.
- Per-workload generated header and ELF; shared static/dynamic simulators may be
  reused when the declared hardware profile matches them.
- Program/call/LLM/tool/descriptor/flow/placement/busy-work expectations generated
  from the manifest, not literal `3/11/10/1/80/2/8/30/30/20` checks.
- Tile issue/complete and trace gates derived from the compiled descriptor set.
- Static/dynamic runs execute identical logical work, DMA and checksum for every
  workload; optional performance gates apply only when declared.

## Frozen hardware boundary

The first generic runner targets the installed `xpu_v2`, TISA window-8,
seven-cycle dynamic dispatch and HPTPE OPT1 16x16 profile. Hardware-profile
variation and paper-regression parameter matrices are H14.2; H14.1 must expose
the fields and fail clearly on an incompatible installed profile rather than
silently approximate it.

## Prediction

The certified workload should remain bit-identical to run 028. Smaller workloads
should produce proportionally fewer tile events and HPTPE operations while
preserving the same first-issue, dependency, ABI and installed-source gates.

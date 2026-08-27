# H14 run-032 protocol: complete parameterized-system replay and certificate

## Objective

Package H14.1 workload switching and H14.2 layer regression into one fresh,
serial, machine-audited experiment-system entry point. No simulator equation,
RTL behavior, target, tolerance or workload content changes in this run.

## Locked serial stages

1. Execute the five-layer parameter/paper regression matrix.
2. Compile and run `react_moa_mcts` on static/dynamic Rocket+HPTPE.
3. Compile and run `react_tool` on the same simulators.
4. Compile and run `planner_debate` on the same simulators.
5. After the manifest/toolchain audit, run fresh tests and RTL checks and issue
   the parameterized-system certificate.

Every stage records command/config/workload SHA-256, nanosecond boundaries,
stdout, declared artifacts and pass gates. Stages must be strictly serial.

## Final certificate requirements

- Versioned workload schema, validator and one-command CLI present.
- Three distinct workload/config/header/ELF identities.
- Three fresh four-stage pipelines and all generalized system gates pass.
- Dedicated TISA logs are non-empty, explicit-call, zero-repair and contain the
  manifest-derived issue/complete count.
- Per-tile and aggregate static/dynamic checksum identity for every workload.
- Five active layer configurations consumed and five sensitivity metrics changed.
- 68/68 unique paper endpoints pass at a uniform 10% limit.
- mllm native and HPTPE RTL functional evidence remains passing.
- Ordinary Rocket, neutral `xpu_v2`, HPTPE 16x16 and ATX exclusion preserved.
- Fresh full pytest, Icarus dedicated-trace test, legacy RTL lint and complete
  revised HPTPE/RoCC lint exit zero.
- Setup/replay documentation and main report describe parameter switching,
  output layout, installed hardware boundary and evidence limitations.

## Prediction

Run-032 results reproduce run 030/031 metrics: workload gates all pass, backend
speedup remains 1.3764x for the common eight-descriptor template, and layer
regression remains 68/68 with 9.91% maximum error.

# H16 run-042 analysis — active MLX+CPU source basis

## Outcome

H16 is supported. The audit passes 10/10 gates against the current `sys` commit
`2a457dfaf8faf9bcda72f92c5d66e9a6a9b3b50f` and the exact local Chipyard
commit. Twenty-one core RTL/RoCC/runtime/lowering files are present and
byte-identical to the historical source basis, while the old checkout remains
fixed for prior AgentSys certificates.

The source contains the required active hardware: 16 physical PEs in a 4x4
array, tagged buffers, configuration/data networks, heterogeneous FUs, packet
routing/flow control, shared SPM arbitration, independent cycle/RTL backends and
the ordinary-Rocket custom0/HellaCache interface.

## Frozen evidence qualified

- Standalone cycle+RTL: four workloads and all nine source gates pass.
- Chipyard: eight bare-metal runs and all six system gates pass.
- Target-free core mechanisms: 5/5 primary and 3/3 supporting claims pass.
- Registered paper-aligned e2e subset: 5/5 rows at <=10%, maximum in-sample
  error 5.85%.

The last result remains explicitly target-informed: leave-one-out maximum error
is 20.77% and independent validation is false. The repository's strict
full-paper certificate remains negative (1/18 within 10%, 17/18 not fully
reproduced). Run 042 treats that disclosure as a passing honesty gate rather
than rewriting the scope.

## Integration consequence

MLX is now qualified as an active source basis, not yet an AgentSys backend.
The machine handoff lists eight remaining changes: Agent/mllm/TISA spatial
lowering, per-call input/golden generation, CPU dependency/tool runtime,
per-workload ELF, cycle+RTL Rocket execution, trace composition, an MLX layer
regression and a new final certificate.

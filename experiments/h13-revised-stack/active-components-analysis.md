# Run 025 revised active-component certificate

## Outcome

All five components required by the revised system pass their standalone gates.
ATX is excluded by name and by endpoint accounting.

| Component | Endpoints | Maximum error | Additional hard gate |
|---|---:|---:|---|
| Agentix | 16/16 | 9.09% | executable PLAS/ATLAS/KV/SLO substitute |
| Agent.xpu | 11/11 | 8.07% | HEG, elasticity, batching, placement, preemption |
| TISA | 10/10 | 8.27% | semantic scheduler and RTL contract |
| mllm / llm.npu | 5/5 | 9.91% | 20/20 upstream executables, 101 gtests |
| HPTPE | 26/26 | 0.98% | 9/9 RTL organizations, 302 golden checks, 9/9 lint |

The combined result is 68/68 endpoints, 5/5 components and 8/8 certificate
gates. Global maximum error is 9.91%, below the revised 15% requirement.

Agentix, Agent.xpu and TISA were rerun unchanged as run 025. Their existing 10%
profile limit is stricter than the revised 15% limit; no mechanism parameter was
retuned after mllm/HPTPE were added.

## Scope boundary

This certificate closes only standalone reproduction. It does not state that the
old Chipyard four-lane ME is HPTPE, that ATX belongs to the ordinary-RISC-V CPU,
or that mllm/Agent.xpu decisions have already executed through the tested HPTPE
array. Those are integration gates for the next run series.

Machine result: `artifacts/results/revised-components-run_025.json`.

Replay the three unchanged profiles, then audit all five:

```bash
.venv/bin/python -m agentsys.paper_reproduction --paper agentix --run-id run_025 --output artifacts/results/paper-agentix-run_025.json
.venv/bin/python -m agentsys.paper_reproduction --paper agentxpu --run-id run_025 --output artifacts/results/paper-agentxpu-run_025.json
.venv/bin/python -m agentsys.paper_reproduction --paper tisa --run-id run_025 --output artifacts/results/paper-tisa-run_025.json
.venv/bin/python scripts/audit_revised_components.py
```

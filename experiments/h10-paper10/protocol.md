# H10 protocol: independent paper profiles at a 10% error gate

## Scope

The target-paper inventory is exactly Agentix, Agent.xpu, ATX and TISA. MLX_dev, LLM.xpu, HPTPE, mllm, Ramulator2 and Chipyard remain implementation/tool references and do not acquire unsupported paper-performance targets.

## Preregistered endpoints

- Agentix: 3 executable Figure-2 scheduler endpoints plus 13 explicitly parameterized aggregate endpoints = 16.
- Agent.xpu: 11 source-grounded heterogeneous-flow endpoints.
- ATX: 18 explicitly parameterized organization endpoints, with executable adapter/Chipyard mechanism evidence retained separately.
- TISA: 10 source-grounded cycle-simulation endpoints, with RTL/Chipyard mechanism evidence retained separately.
- Total: 55 unique endpoints.

Every endpoint must carry `limit=0.10`, pass its registered point/range comparison, and each paper must emit an independent artifact whose toolchain profile passes. No scheduler/model parameter is changed for this run: the only numerical-contract change is the preregistered threshold from 15% to 10%, which is stricter than the already observed 8.33% maximum.

## Independent commands and outputs

```bash
.venv/bin/agentsys-paper-reproduce --paper agentix
.venv/bin/agentsys-paper-reproduce --paper agentxpu
.venv/bin/agentsys-paper-reproduce --paper atx
.venv/bin/agentsys-paper-reproduce --paper tisa
```

Outputs are `artifacts/results/paper-{agentix,agentxpu,atx,tisa}-run_017.json`. The expanded serial toolchain must execute these four as distinct stages before mllm, full-stack, Ramulator2, ablations and Chipyard support stages.

## Rejection conditions

Reject completion if any paper artifact is missing, shares another paper's audit list, has a duplicate endpoint, lacks its declared sources/reference revision, reports any endpoint above 10%, or if the final certificate still consumes the old combined run-011 artifact as authoritative evidence.

# H10 analysis: four independent paper reproductions at 10%

Run 017 executes from source commit `82d0c51c594f7311cf76c68730f44f8335cf154c` with no model/scheduler retuning after the gate was tightened.

| Paper | Endpoints | Passing | Maximum error | Profile evidence |
|---|---:|---:|---:|---|
| Agentix | 16 | 16 | 8.33% | 4 source hashes; executable Figure 2 + parameterized aggregate |
| Agent.xpu | 11 | 11 | 8.07% | 4 source hashes; pinned LLM.xpu revision |
| ATX | 18 | 18 | 0.285% | 7 source/ABI/RTL hashes; pinned Chipyard revision |
| TISA | 10 | 10 | 8.27% | 6 source/RTL hashes; pinned Chipyard revision |

All 55 endpoint records carry `limit=0.10`; names are globally unique and all pass. Evidence classes remain 24 executable/source-grounded and 31 paper-parameterized component replay.

The complete run then passes:

- 9/9 serial stages with `serial_order=true`; summed stage execution is approximately 94.1 s, including 64.05 s for Chipyard.
- 12/12 full toolchain gates, including the new four-profile gate.
- Run 018 final certificate: 14/14 requirements, 55/55 endpoints, maximum error 8.33%, fresh 28-test pytest and Verilator RTL lint.

H10 is supported. Tightening 15% to 10% changes only the registered acceptance contract and regenerated artifacts; it does not introduce endpoint-specific factors or alter the previously implemented mechanisms. The old combined run 011 is retained as history but is no longer an authoritative input to the final paper endpoint certificate.

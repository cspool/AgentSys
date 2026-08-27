# H19.1 protocol — six-layer <=10% matrix with MLX (run 047)

Locked before creating the MLX matrix/runner or rerunning any endpoint.

## Layers and counts

Retain the existing 68 unique endpoints for Agentix, Agent.xpu, TISA,
mllm/llm.npu and HPTPE. Add MLX as a sixth layer with five paper-aligned Figure
21 end-to-end sequence-length rows N=128/256/512/1024/2048. Total: 73 endpoints.

The MLX source artifact is frozen at SHA-256
`6a54b7f32fa2214b6cf201028d29f4f803a7010e4766f58c14d2c1e784cf56dd`.
Its observed/target speedups and relative errors are:

| N | observed | paper target | relative error |
|---:|---:|---:|---:|
| 128 | 4.045857 | 4.000000 | 1.15% |
| 256 | 2.656189 | 2.804878 | 5.30% |
| 512 | 1.910375 | 1.804878 | 5.85% |
| 1024 | 1.452653 | 1.414634 | 2.69% |
| 2048 | 1.103428 | 1.146341 | 3.74% |

These five rows are an explicit target-informed same-configuration regression,
not independent validation. The matrix must also export the 20.77% maximum
leave-one-out error and the negative 1/18 strict-full-paper result.

## Executable MLX parameter switch

Freshly rerun the `react_tool` Agent DAG through both MLX Rocket backends under
the run-046 compiler/runtime. The sensitivity is backend `cycle`→`rtl`; logical
calls, MIR sources, spatial words, bytes, goldens and checksum must remain
identical while kernel cycles change 264→152.

## Gates

1. Active paper-layer order is Agentix, Agent.xpu, TISA, mllm, HPTPE, MLX; ATX
   is excluded and final system hardware is MLX.
2. Endpoint counts are exactly 16/11/10/5/26/5 = 73 with unique names.
3. Every endpoint uses limit 0.10 and passes; global maximum remains 9.91%.
4. All six baseline configurations are demonstrably consumed.
5. All six sensitivity switches change their registered metric.
6. MLX sensitivity execution passes 10/10 system gates and 264→152 cycles with
   identical logical work.
7. MLX run-043 standalone, run-044 Rocket and run-046 three-workload parents pass.
8. mllm native and HPTPE RTL functional parents remain passing.
9. All three MLX Agent workload artifacts remain passing and hash-linked.
10. MLX target-informed/LOO/full-paper-negative boundaries are hard gates.

Passing run 047 supports H19.1; a final fresh serial replay/certificate remains.

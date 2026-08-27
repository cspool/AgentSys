# Per-layer parameter and paper regression matrix

## Entry point

```bash
cd /workspace/AgentSys
.venv/bin/agentsys-layer-regression \
  --matrix config/layer-regression-matrix.json \
  --run-id run_031
```

The output is stored under a matrix-SHA-addressed directory and contains every
configuration, sensitivity result, paper endpoint, source identity and gate.

## What is parameterized

| Layer | Baseline fields consumed by implementation | Included switch |
|---|---|---|
| Agentix | workload, policy set, batch size, queue bounds/quanta | batch 2→1 |
| Agent.xpu | full `XPUConfig`, model rate scale, request rates, duration, seeds | HEG chunk 16→32 |
| TISA | workload model set, iterations, ready window, dispatch latency | window 8→2 |
| mllm/llm.npu | every `LlmNpuConfig` field and native MIR identity | prompt 1024→512 |
| HPTPE | RTL case, simulator, top, M/K/N, trials, DC report point | OPT1/2/3/4C organizations |

The runner compares the configuration returned by each implementation with the
matrix input. Merely echoing an unused JSON field cannot pass
`configuration_consumed_5`.

## Same workload/configuration regression

`config/layer-regression-matrix.json` binds each paper result to its actual
workload and parameter set. `data/paper_targets.json` is read only after the
simulator returns observed metrics. The audit requires:

- exactly five active layers and no ATX;
- endpoint counts 16/11/10/5/26 = 68;
- globally unique endpoint names;
- every endpoint `limit=0.10` and relative error ≤10%;
- five output-changing parameter switches;
- mllm native and HPTPE RTL functionality; and
- preservation of all three parameterized end-to-end system workloads.

Run 031 passes all nine matrix gates with 68/68 endpoints and 9.91% maximum
error. The result is
`artifacts/layer_regression/7d4b075e9754/run_031/layer-regression.json`.

## Interpretation

Sensitivity variants demonstrate parameter control; they are not fitted paper
endpoints. Only the baseline configuration is compared with a paper point. This
prevents a parameter selected after seeing residuals from being mislabeled as a
confirmatory reproduction.

## MLX+CPU six-layer matrix

The revised hardware goal uses:

```bash
.venv-mlx/bin/agentsys-mlx-layer-regression \
  --matrix config/mlx-six-layer-matrix.json --run-id run_047
```

It retains the five layers above and adds MLX as the sixth paper layer. Run 047
passes 73/73 endpoints and six parameter switches; MLX's fresh mechanism switch
executes `react_tool` on cycle/RTL Rocket backends (264→152 kernel cycles) with
identical work. The five MLX numerical rows have 5.85% maximum in-sample error
but are target-informed and not independent validation; 20.77% leave-one-out
error and the negative strict-full-paper certificate remain exported.

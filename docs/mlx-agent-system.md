# AgentSys MLX+普通 RISC-V CPU 垂直实验系统

活动硬件路径现为：

```text
Agent JSON → Agentix → mllm MIR → Agent.xpu → TISA-to-MLX lowering
           → Agent call table + MLX spatial microprogram → RISC-V ELF
           → ordinary Rocket CPU/tool runtime → custom0/HellaCache DMA
           → MLX cycle model or physical 4x4/16-PE RTL
```

## 环境与运行

```bash
cd /workspace/AgentSys
bash scripts/bootstrap_chipyard.sh
bash scripts/bootstrap_chipyard.sh --verify-only
bash scripts/setup_mlx_toolchain.sh
bash scripts/install_mlx_chipyard.sh

# 三种Agent负载严格串行重放
.venv-mlx/bin/agentsys-reproduce-mlx-agent \
  --config config/mlx-agent-system.json --run-id run_046

# 只切换一个负载
.venv-mlx/bin/agentsys-run-mlx-agent \
  --workload workloads/react_tool.json \
  --run-id demo --output-dir artifacts/mlx_demo/react_tool
```

完整fresh重放入口：

```bash
.venv-mlx/bin/agentsys-reproduce-mlx-complete \
  --config config/mlx-complete-system.json --run-id run_048
```

run 048依次执行source audit、standalone fresh build、Rocket fresh execution、
六层73端点matrix和三Agent replay，共24次MLX执行；5/5阶段与10/10全局gate通过。

最终证书：

```bash
.venv-mlx/bin/agentsys-certificate-mlx \
  --run-id run_049 \
  --output artifacts/results/mlx-cpu-final-certificate-run_049.json
```

run 049通过25/25 requirements和5/5 fresh checks；完整pytest为105/105，
`full_goal_complete=true`。

Chipyard源码进入仓库后的当前入口与证书为：

```bash
.venv/bin/agentsys-reproduce-portable \
  --config config/project-local-chipyard.json --run-id run_052
.venv/bin/agentsys-certificate-portable \
  --config config/project-local-chipyard.json --run-id run_052 \
  --expected-commit ab7746201d9840904ede594d9dd765f7f11d3029
```

run 051使用项目内`chipyard/`fresh执行16次Rocket，4/4阶段、9/9 replay
gate、16/16证书要求和114/114 pytest通过；substrate、三Agent与73端点解析
结果逐字段等于run 044/046/048。显式`AGENTSYS_CHIPYARD_ROOT`可覆盖默认根，
无效override会fail closed。

run 052进一步把输出按`run_id`隔离，并以实现闭包而非易失的当前HEAD相等
条件签发证书。25/25构建gitlink、2/2兼容补丁、19/19 requirements和
117/117 pytest通过；16次fresh Rocket与73/73端点结果逐字段保持不变。
证据提交`a71e78e`之后再次重签仍为19/19和117/117，源码闭包的changed与
untracked路径均为空。

切换负载会重新执行Agentix、生成mllm/Agent.xpu/TISA manifest、45-op MLX
micro-lineage、Agent call C header和独立RISC-V ELF，然后在两套MLX Rocket
simulator上执行。无需修改仓库源码。

## 编译和运行合同

每个LLM call保留8个Qwen3 MIR source（3 ME、3 VE、2 DE），并映射到经过
独立验证的Transformer空间模板：45条MLX指令、9个活跃PE、8入1出向量、
576字节DMA。micro-lineage为每条空间指令记录PE/PC/op/tag/route以及对应MIR
source index/type/TISA engine。工具call只在普通Rocket上执行。

Rocket软件逐call检查DAG dependency、program first/last、ABI magic和FP16
golden，并导出Agent.xpu flow、prefill chunk和decode batch。两种硬件backend是
真实参数开关：cycle model使用串行ready-tag服务，RTL物理实例化16个PE。

## run 046

| workload | calls | LLM/tool | micro-ops | cycle/RTL kernel | trace events |
|---|---:|---:|---:|---:|---:|
| react_moa_mcts | 11 | 10/1 | 450 | 1320/760 | 762 |
| react_tool | 3 | 2/1 | 90 | 264/152 | 158 |
| planner_debate | 6 | 5/1 | 225 | 660/380 | 385 |

全局9/9，每个workload 10/10。三个header/ELF hash均不同；20个call、17个
MLX launch和3个CPU tool全部执行一次，cycle/RTL logical checksum一致。

重复launch揭示真实cache效应：同一ELF第一次DMA为344 cycles，后续为216；
kernel仍固定132/76，字节数固定576。系统按逐call计数求和，不把cold smoke
结果机械乘以call数。

## 证据边界

MLX_dev是公开surrogate，不是论文作者未公开的完整模拟器/RTL。Agent编译器是
AgentSys新增实现。MLX论文5个目标拟合e2e点可用于明确标注的数值回归，但不能
替代目标无关的RTL/Chipyard机制证据，也不能把外部仓库1/18的严格全论文结果改写
为完成。

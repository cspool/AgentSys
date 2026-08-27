# Agent 到双 GPU / Rocket+TISA/HPTPE 的垂直实验系统

当前最高层入口不再只是 CPU+XPU trace。它将同一个版本化 Agent DAG 编译为
两个身份关联的执行域：

```text
Agent JSON → Agentix 调度 → mllm MIR → Agent.xpu flow/stage
           ├─ AgentSys MIR→CUDA adapter → GPU0/GPU1 + NUMA0/NUMA1 + NCCL
           └─ RISC-V ELF → static/dynamic Rocket → TISA → HPTPE/VE/DE
```

GPU 路径是真实 CUDA 执行，Rocket 路径是真实 Verilator SoC 仿真。二者共享
workload SHA、call ID、DAG dependency、MIR source index 和编译产物 hash，但保留
不同的时钟域；工具不会把 CUDA 纳秒伪换算成 Rocket cycle。

## 配置与运行

```bash
cd /workspace/AgentSys
bash scripts/setup_gpu_runtime.sh
bash scripts/setup_mllm_cuda.sh

# 三个负载 + 五层论文回归 + GPU placement switch
.venv-gpu/bin/agentsys-reproduce-hybrid \
  --config config/hybrid-system.json \
  --run-id run_040

# 只切换一个 Agent 负载
.venv-gpu/bin/agentsys-run-hybrid \
  --workload workloads/react_tool.json \
  --config config/hybrid-system.json \
  --run-id demo \
  --output-dir artifacts/hybrid_demo/react_tool
```

`config/hybrid-system.json` 参数化 GPU placement、dtype、token→matrix shape、
CPU matrix shape/线程数和算子迭代数；原五层参数继续由
`config/layer-regression-matrix.json` 控制。`round_robin` 与 `gpu0_only` 会生成
不同的 GPU resource signature，同时 calls、dependencies、MIR ops 和 XPU
descriptors 保持逐项相同。

## run 040 结果

| workload | LLM/tool | GPU0/GPU1 calls | MIR CUDA ops | native events | Rocket events | merged events |
|---|---:|---:|---:|---:|---:|---:|
| react_moa_mcts | 10/1 | 5/5 | 80 | 133 | 860 | 993 |
| react_tool | 2/1 | 1/1 | 16 | 29 | 180 | 209 |
| planner_debate | 5/1 | 3/2 | 40 | 68 | 436 | 504 |

三个 workload 的原生运行均为 13/13，垂直系统均为 9/9；全局 replay 为
11/11。每个 LLM call 恰有 3 个 ME、3 个 VE、2 个 DE 对应的真实 CUDA
operator event，且每个负载都使用两张独立 4090、两个精确 NUMA affinity、
H2D/D2H 和正确 NCCL all-reduce。GPU 间无 P2P，持久化 NCCL 日志显示
`SHM/direct/direct`。

论文证据单独计量：五个原论文配置仍为 68/68 endpoints、统一 10% 门槛、
最大误差 9.91%。本机 4090/Xeon timing 是实机校准证据，不替代 Agentix A100、
Agent.xpu Core Ultra、TISA Epoch、移动 NPU 或 HPTPE SAED32 数据。

## mllm CUDA 边界

固定 mllm 版本的 CUDA backend 已完成 nvcc 构建、两 GPU 枚举和生命周期修复，
run 039 为 13/13。但该上游提交的四个 CUDA translation unit 为空且没有 CUDA
op factory。真实 MIR kernels 因而明确标记为 `agentsys_mir_cuda_operator_adapter`，
不冒充上游 mllm 完整 GPU inference。

# Astra baseline 复现（方法与实验环境）— 2026-09-19

Baseline：**Astra: A Multi-Agent System for GPU Kernel Performance Optimization**
（arXiv 2509.07506，NeurIPS'25 workshop；仓库 Anjiang-Wei/Astra，Apache-2.0）。

## 为什么选它（提升空间的先验证据）

Astra 从 SGLang 抽出 serving kernel 做孤立优化。它三个目标里的两个正是本项目
跨 process 矩阵证明**在 serving 流水中被遮蔽**的 process：

| Astra 目标 kernel | 我们的 process | host 区间被上一 gemm 覆盖 |
|---|---|---|
| silu_and_mul | act_mul | **83.8%**（mixed 谱系实测） |
| fused_add_rmsnorm | norm_post | **53.4%** |
| merge_state | （注意力路径） | — |

孤立 1.32× 的加速落在被遮蔽路径上，端到端收益趋近于零——v2 的暴露时间排序 +
regime 门控计数器可直接改写其目标选择与奖励信号，因此预期提升最大。

## 方法（自代码核实，非转述论文）

五个 o4-mini agent（OpenAI Agents SDK，`cuda_kernel_optimizer_multi.py`）：
orchestrator / code_generation / correctness_testing（工具：测例生成+验证）/
benchmarking（工具：benchmark_kernel）/ optimization_strategy（无工具，只出建议）。
循环 ≤5 轮：初始 .cu → 生成变体 → 正确性（vs torch 参考，allclose 阈按 dtype）
→ 计时（cuda Event，20 warmup / 100 iter，固定 shapes，fp16/bf16）→ 策略建议 → 下一轮。
基线经 `--baseline-module`（默认 sgl_kernel）可插拔。

## 实验环境（本机复现配置）

- GPU：RTX 4090（sm89）；CUDA toolkit 12.8；torch 2.13.0+cu130（.venv-vllm）
- kernel 构建：`torch.utils.cpp_extension.load`（nvcc -O3 --use_fast_math，与上游一致）
- **声明替换 1（基线模块）**：sgl-kernel 0.3.21 wheel 仅含 sm100 二进制且 torch ABI
  不匹配，无法在本机加载。利用 harness 自身的 baseline-module 可插拔性，以
  `test/sgl_kernel.py` 垫片将同名入口映射到 vLLM 注册的同功能 serving 级算子
  （torch.ops._C.silu_and_mul / fused_add_rms_norm——正是本项目全程 trace 的那批 kernel）。
- **声明替换 2（LLM）**：无 OpenAI key；agent 循环复跑时以 Claude 顶替 o4-mini
  执行同一套 AGENT_INSTRUCTIONS/prompts（方法为零样本提示循环，无训练，LLM 可替换）。
- merge_state：vLLM 无同名基线算子，**跳过并声明**（不影响与 v2 对照的两个核心 kernel）。

## 复现结果（他们仓库自带的 ultimate kernel vs 基线，本机实测）

| kernel | 正确性 | 加速（本机） | 论文口径 |
|---|---|---|---|
| silu_and_mul（fp16/bf16 ×5 shapes） | 10/10 PASS | **1.29–1.39×** | 平均 1.32× |
| fused_add_rmsnorm（7 shapes） | PASS | **1.23–2.04×**（1 形状 1.23×，余 ≥1.34×） | 同上量级 |

结论：**方法与实验环境复现成立**——孤立基准下他们的优化 kernel 在本机重现论文
量级的加速。这为下一步对照实验提供了干净的基线：把同一批 ultimate kernel 放回
serving 语境（vLLM 引擎 + v2 三遍 trace），按暴露时间与端到端指标重新计分，
检验"被遮蔽 kernel 的孤立加速在 serving 端到端不可见"的预言，并用 v2 的
目标排序/门控计数器改写其 planning 与 profiling agent 的输入。

产物：`Astra/test/silu/silu_mul_fp16_summary.csv`、`Astra/test/rms/rmsnorm_perf_summary_3way.csv`。

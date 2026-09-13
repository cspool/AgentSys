# h23 — Agentix 8B 性能复现 + AutoTrace 应用（单卡 4090）

## Objective

两件事，一条链：

1. **按 Agentix 论文的实验协议，在单张 RTX 4090 上复现其 8B 档的性能实验**（程序级调度 vs FCFS）。
2. **对这次 serving 实验应用 AutoTrace 的 w01–w05 方法链**，产出算子级守恒分母、请求/阶段归因、硬件计数器、全负载估计与选择性资源缺口。

## 与论文的对应与偏离（证据边界）

| 项 | 论文（KB: `paper_secs/paper_20260824/Agentix .../§6.1–6.2`） | 本次 | 说明 |
|---|---|---|---|
| 硬件 | GCP `a2-ultragpu-8g`：8× A100-SXM4-80GB (NVLink)、1360 GB 内存 | **1× RTX 4090 24GB** | 记数不可比；只做同机同负载的策略对照 |
| 模型 | LLaMA-3.1-8B / 70B / Falcon-180B，分别 1/4/8 卡 | **LLaMA-3.1-8B bf16**（本地 1 卡档） | 与论文 8B 档同模型同精度；权重取自未 gated 镜像 `NousResearch/Meta-Llama-3.1-8B`（官方 `meta-llama/Llama-3.1-8B` 为 gated 且本机无授权 token），权重与官方一致 |
| 程序负载 | 三类程序 + Mixed，Poisson 到达；轨迹未公开 | **本地合成**（`workload.py`，三类结构 + Mix、Poisson、指数工具延迟、带种子与 sha256） | 结构同类不等同原轨迹；已在 workload manifest 中如实标注 |
| serving 底座 | 修改的 vLLM v0.6.1（原型未开源，约 5000 行改动） | **vLLM 0.29.0 原版** + 自实现调度策略 | 不冒充其未公开改动 |
| 调度策略 | PLAS（按程序累积服务时间）/ ATLAS | **PLAS 复刻**：`priority = 程序已累积服务`，走 vLLM 原生 `scheduling_policy=priority` | 与 Continuum、Astraea 在单卡上重实现 Autellix/PLAS 的做法一致 |
| 指标 | program-level token latency、吞吐、尾延迟 | 同（程序响应时间/生成 token、programs·s⁻¹、tokens·s⁻¹、P50/P90/P99） | — |
| AutoTrace | — | w01'–w05' 服务于 serving 引擎的适配 | 见下 |

**不可外推**：本机不产生 A100 级别的绝对数值；不声称复现论文的 4–15× 端点。可比的是**同一台机器、同一份负载下两种策略的相对关系**。

## AutoTrace 适配说明（w01'–w05'）

原链假设"一个进程内的算子 NVTX 区间 → 该线程发起的 CUDA API → 同 correlationId 的 kernel"（launch ownership）。vLLM 的 GPU 工作发生在 EngineCore 子进程，且**连续批处理会把一次前向共享给多个请求**，因此：

- **算子级**：用 vLLM 的逐模块 NVTX（`--enable-layerwise-nvtx-tracing`）在 worker 进程内保持 launch-ownership 归因；守恒式为 `Σ(模块) + 未归因 = 窗口内 GPU busy`。
- **请求级**：用客户端 NVTX 标记（`agentix.call_begin/end::<program>::<index>::<class>`）给出请求窗口，并借 h22 w02 已验证的**主机↔nsys 时钟对齐**把客户端时间戳映射到 nsys 时钟；因为一次前向被多个请求共享，请求级 GPU 归属按**时间窗交叠**给出并明确标注为近似，不冒充逐 kernel 归属。

## 目录

```text
experiments/h23-agentix-8b/code/      # workload.py, serve_agentix.py, run_matrix.sh,
                                      # run_nsys_serving.sh, analyze_*.py
experiments/h23-agentix-8b/workloads/ # 冻结的负载 JSON（含 sha256）
artifacts/agentix_8b/                 # r<rate>/<policy>/ 对照结果；autotrace/ 采集与分析
```

## 状态（2026-09-13）

| 步骤 | 状态 |
|---|---|
| §1 8B 性能复现（未饱和 + 饱和口径） | ✅ 完成，见 `results.md` §1–2 |
| AutoTrace w01'（守恒分母 + 并发窗口） | ✅ 完成 |
| AutoTrace w02'（请求级归因） | ✅ 完成 |
| AutoTrace w03'（代表 kernel 硬件计数器） | ✅ 完成（4 个 cuBLAS bf16 GEMM） |
| AutoTrace w04''（并发条件化每步成本模型，−8.8 % 总误差） | ✅ 完成 |
| AutoTrace w05''（双轴选择 + NCU 资源挂接 + 账本/清单/双视图报告） | ✅ 完成 |
| w01' 模块级 NVTX | ✅ 根因定位并修复：scopes 在 V1 runner，0.29 默认 V2；`VLLM_USE_V2_MODEL_RUNNER=0`+`VLLM_NVTX_SCOPES_FOR_PROFILING=1` 恢复阶段级 launch-ownership |
| nsys 30 s 截断 | ✅ 根治：换 `/opt/nvidia/nsight-systems/2026.3.1`（CUDA 13 兼容），全程覆盖 |

早期环境限制（results.md §4）已在 §7–§8 全部根因定位并修复；最终采集栈见 §8。

# h23 results — Agentix 8B on one RTX 4090

LLaMA-3.1-8B bf16, vLLM 0.29.0, single RTX 4090 (GPU 1), synthesised three-class program workload with Poisson arrivals.
Protocol and evidence boundary: `protocol.md`. Generated tables: `artifacts/agentix_8b/analysis_{saturated,unsaturated}/`.

## 1. What the reproduction found

**The program-level scheduling gain depends entirely on whether the engine queues.**

| regime | batch cap | throughput (PLAS/FCFS) | program-token latency (PLAS/FCFS, mean) | p90 |
|---|---:|---:|---:|---:|
| unsaturated (arrival 1–4 prog/s) | none | 1.00× | 0.99–1.00× | 0.99–1.00× |
| saturated (arrival 2 prog/s) | 8 | 1.02× | **0.73×** | 0.71× |
| saturated | 16 | 1.02× | **0.83×** | 0.83× |

Header rows of the saturated table (`artifacts/agentix_8b/analysis_saturated/policy_comparison.csv`):

| arrival rate | batch cap | policy | wall (s) | throughput (tok/s) | program-token latency mean / p90 (ms) |
|---:|---:|---|---:|---:|---:|
| 2 | 8 | fcfs | 262.5 | 397 | 81.4 / 120.0 |
| 2 | 8 | plas | 257.1 | 405 | **59.0 / 84.9** |
| 2 | 16 | fcfs | 160.7 | 648 | 37.9 / 52.1 |
| 2 | 16 | plas | 157.1 | 663 | **31.5 / 43.4** |

Per class (mean program-token latency, ms), batch cap 8: PLAS helps the short class most — chat 91.7 → 35.2,
lats 87.6 → 77.5, agent 61.1 → 65.6 — which is the direction PLAS is designed for.

## 2. Why the unsaturated regime shows nothing (diagnosis, not a null result)

At arrival rates 1–4 programs/s the engine saturates in **decode** (peak 96 concurrent requests, GPU 100 %) but
never **queues**: TTFT median 94 ms, max 140 ms. vLLM's chunked prefill admits every request promptly and the whole
working set stays resident, so backlog shows up as slower decode rather than as waiting. With an empty queue, a
priority policy has no leverage — hence 1.00×.

The priority mechanism itself was validated separately (`validate_priority.py`): with a non-empty queue, a late
request at `priority=0` got TTFT **952 ms** versus **2158 ms** for the same request at the backlog's priority —
vLLM honours the order, but it reorders *admission*, it does not preempt the running batch.

So the honest statement of the reproduction is: **on one 4090 the Agentix mechanism yields 17–27 % lower
program-level token latency at equal throughput, and only when the engine is oversubscribed enough to queue.**
The paper's 4–15× headline is measured on 8×A100-80GB with its own traces; neither the hardware nor the traces are
reproduced here, and no absolute comparison is claimed.

## 3. Evidence boundary

- Hardware: 1× RTX 4090 24 GB vs the paper's 8× A100-SXM4-80GB with NVLink.
- Model: same LLaMA-3.1-8B (bf16), weights from the ungated mirror `NousResearch/Meta-Llama-3.1-8B` (the official
  repo is gated and no token exists on this machine); identical weights, different repository.
- Workload: synthesised three-class program streams with Poisson arrivals — same structure class, not the paper's
  traces, which are not public.
- Serving stack: stock vLLM 0.29.0 with a re-implemented PLAS (`priority = program attained service`), not the
  paper's unreleased ~5000-line fork.

## 4. AutoTrace 应用（w01'–w03'，serving 适配）

方法适配与理由见 `protocol.md`。产物在 `artifacts/agentix_8b/autotrace/plas_short2/analysis/`。

### w01' — 守恒分母 + 并发窗口（G01'）

捕获窗口内（measured 窗口 ∩ 已捕获 CUDA 区间）GPU busy 与家族划分，家族划分与并发桶划分都是同一批 GPU-busy 区间的**划分**，因此守恒恒等式按构造成立
（`conservation_err_ns` 为桶边界取整引入的 ~1.2 ms 级残差）。

| kernel 家族 | GPU 占比 |
|---|---:|
| gemm（prefill / 批量线性层） | 70.2 % |
| attention（flash） | 20.1 % |
| other | 4.9 % |
| gemv | 3.3 % |
| elementwise / copy / reduce / memcpy | 合计 ~1.6 % |

**并发窗口**（`concurrency_windows.csv`）——这是本次适配新增的视角：

| 并发请求数 | GPU 时间占比 | 主导家族 |
|---:|---:|---|
| 1 | 10.8 % | gemm 64 %, **gemv 28.6 %** |
| 2–3 | 2.0 % | gemm 76.6 % |
| 4–7 | 12.7 % | gemm 85.2 % |
| 8–15 | 55.0 % | gemm 70.5 %, attention 22.7 % |
| 16–31 | 19.6 % | gemm 62.2 %, attention 30.7 % |

读法：**74.6 % 的 GPU 时间花在并发 ≥8 的批量服务上**；单请求（并发 1）只占 10.8 %，且只有在这一档里 gemv（矩阵-向量）才显著（28.6 %）。
这与 h22 真机 eager 链"decode gemv 占 62 % GPU 时间"形成对照：**连续批处理把 decode 变成 GEMM 形状（M=batch），gemv/DRAM 墙的结论不能直接迁移到 serving 引擎**——
这是本次应用得到的实质结论，而非实现细节。

### w02' — 请求级归因（G02'–G03'）

沿用 h22 w02 的主机↔nsys 时钟对齐：270 对标记，偏移 spread **98.7 µs**（通过）。结果：

| 程序类 | 队列等待均值 | decode 均值 |
|---|---:|---:|
| chat | 66.7 ms | 1 305 ms |
| lats | 62.9 ms | 2 204 ms |
| agent | 64.1 ms | 2 932 ms |

**队列等待只占请求时间的 2.39 %**——与 §2 的诊断一致：该负载下引擎不排队，程序级调度的杠杆因此在 w01'/w02' 的这部分证据里同样看不到。

### 方法可用性发现（诚实记录）

1. **vLLM 的逐模块 NVTX 在本执行模式下不产生标记**：`--enable-layerwise-nvtx-tracing=True` 已生效，但 CUDA-graph 执行路径绕过了编译包装器，因此 AutoTrace 原链的 launch-ownership 算子归因不可用；改用家族划分 + 并发桶划分。
2. **nsys 在本容器内约 30 s 后停止记录 CUDA**：在禁用 vLLM 多进程、设置 `--cuda-flush-interval` 后仍重复出现（CUDA API 调用与 kernel 活动同时截止于 ~30 s，而客户端请求持续到 ~155 s）。因此 w01' 的分析区间是「measured 窗口 ∩ 已捕获 CUDA 区间」，`analysed_span_is_truncated` 字段如实标注，绝对占比只在被捕获区间内有意义。
3. **w03' 已完成**（见下节；采集要点：必须按 kernel 名过滤，`--launch-skip` 会落在预热期）；**w04'/w05' 尚未实现**——本次交付到 w01'–w03'。

### w03' — 代表 kernel 的硬件计数器（G04'）

按 kernel 名过滤（`--kernel-name regex:gemm|flash_attn|cutlass`）采样 4 个代表 kernel，全部命中 cuBLAS bf16 GEMM
（`artifacts/agentix_8b/autotrace/ncu_focus/focus2_raw.csv`）。NCU 重放时长只作硬件属性，不作延迟：

| kernel | 时长 | SM % | DRAM active % | L2 % | Tensor pipe % | 占用率 % | waves/SM |
|---|---:|---:|---:|---:|---:|---:|---:|
| `ampere_bf16_s1688gemm_bf16_64x128_sliced1x2` | 3.0 µs | 49.0 | 19.7 | 76.7 | 49.2 | 16.5 | 28 |
| `ampere_bf16_s1688gemm_bf16_128x64_sliced1x2` | 1.5 µs | 48.7 | 18.3 | 77.1 | 48.9 | 16.4 | 16 |
| `ampere_bf16_s1688gemm_bf16_64x128_sliced1x2` | 0.6 µs | 48.2 | 18.1 | 75.5 | 48.7 | 16.1 | 6 |
| `ampere_bf16_s1688gemm_bf16_128x64_sliced1x2` | 0.4 µs | 48.4 | 13.9 | 75.5 | 48.9 | 15.9 | 4 |

判读：serving 的线性层 kernel 稳定运行在 **~48–49 % SM / ~49 % tensor pipe / ~76 % L2，而 DRAM 只有 14–20 %**——
即 **L2 + tensor-core 受限**。这直接对照 h22 真机 eager 链的 decode gemv（DRAM active 74 %、占 GPU 时间 62 %）：
**连续批处理下线性层变成 GEMM 形状后，墙从 DRAM 带宽移到了 L2/张量流水**，与 w01' 的家族与并发窗口结论一致。

采集要点（供复现）：NCU 必须 `--kernel-name` 过滤（`--launch-skip 200` 会落在预热期的 fill kernel 上，实测全部 1.6 µs、计数器为 0）；
`--target-processes all` 在本环境下剖析子进程会失败，需配合 `VLLM_ENABLE_V1_MULTIPROCESSING=0` 让引擎与客户端同进程。

## 5. 审计后重跑（论文校准负载，见 `AUDIT.md`）

修正 A1（PLAS 按实测运行时长）、A2（负载按论文 Fig.11 校准：sharegpt/bfcl/lats，调用数均值 6.16/10.81/161.9）、
A3（论文到达率区间）并补上 B3（LATS 多线程 wave 结构 + ATLAS 关键路径调度）之后：

### 5.1 到达率扫描（fcfs / plas / atlas，`artifacts/agentix_8b/thr_r*/`）

| 到达率 (prog/s) | 吞吐 (tok/s) | ptl mean / p90 (ms) — 三策略 |
|---:|---:|---|
| 0.1 | 218 | 15.7 / ~24.6（全部一致） |
| 0.2 | 511 | 15.5 / ~25.5（全部一致） |
| 0.3 | 619 | 17.0 / ~29.0（全部一致） |
| 0.5 | 813 | 16.5 / ~28.6（全部一致） |
| 0.8 | 786 | 18.6 / ~31.0（全部一致） |

**边界结论**：本机（1×4090、60 s 到达窗口、max_num_seqs 64）在论文的到达率区间乃至 0.8 prog/s 下
引擎等待队列从未形成——r0.8 峰值 in-flight 60 < 64，TTFT 最大 323 ms，后半段 in-flight=1，
瓶颈是单个 LATS 程序自己的关键路径（工具延迟 × 44 waves）。没有队列，三种策略必然重合；
论文的收益区间需要其测试台的持续过载稳态。

### 5.2 排队区间（统一 max batch = 16，论文 §6.2 允许同一 batch 上限；`artifacts/agentix_8b/cap16_r0.5/`）

| 策略 | 吞吐 (tok/s) | ptl mean (ms) | ptl p90 (ms) | bfcl / sharegpt / lats（分类别 ptl 均值） |
|---|---:|---:|---:|---|
| FCFS | 654 | 28.5 | 58.0 | 56.7 / 25.3 / 11.0 |
| PLAS | 604 | **20.6（0.72×）** | **33.3（0.57×）** | **30.3（−47 %）** / 24.3 / 12.6 |

分类别形状与论文机制一致：短程序（bfcl）收益最大，长程序（lats）小幅付出（PLAS 语义使然）。
吞吐低 ~8 %：PLAS 的重排序在本实现中以少量批构成扰动为代价。

### 结论修订

第一版 §1 的"17–27 %"是在**错误校准的负载**（见 AUDIT A2）上测的；本节数字取代它：
**校准负载 + 排队区间下，PLAS 相对 FCFS（≈论文的 vLLM-opt 臂）把 program-level token 延迟
mean 降 28 %、p90 降 43 %**，无排队则无收益。ATLAS 已实现，在本负载/无队列区间与 PLAS 无可测差异。
与论文可比的参照是其 Agentix ≈ 2×（对 vLLM-opt），方向一致、幅度低于论文——差距来源：静态优先级
而非 MLFQ 全机制（AUDIT B2）、无抢占、以及单卡饱和形态不同。

## 6. w04'' / w05''（目标不变，方法按 serving 重设；trace 额外开销已获允许）

### w04'' — 全负载估计（G05'，`artifacts/agentix_8b/autotrace/g05_step_model/`）

h22 w04 的目标不变：代表观测建模板 → 仅凭目标的结构信息做预测 → 用目标实测打分。serving 下
kernel 属于动态批而非单个 call，模板改为**按请求并发条件化的每步成本模型**：
在代表捕获（plas_short2）上按 100 ms 切片拟合 `GPU busy 比例 ~ f(并发请求数)`（分桶均值），
对目标捕获（plas_r2）**只用其客户端并发时间线**做预测，再与其实测 GPU busy 对比。

| 项 | 值 |
|---|---|
| 模板桶（busy 均值） | 0:0.293 · 1:0.180 · 2-3:0.075 · 4-7:0.096 · 8-15:0.096 · 16-31:0.095 |
| 覆盖 | 目标 6/6 桶全覆盖，无 nearest 回退 |
| 评分 | 预测 5.703 s vs 实测 6.254 s GPU busy，**总误差 −8.8 %**（判据 ±25 %）→ pass |

### w05'' — 选择性分析与资源缺口（G06'–G10'，`artifacts/agentix_8b/autotrace/g06_g10_selective/`）

准入账本核验 G01'–G05' 全部 pass + sha256。双轴 10 % 选择：

- **请求时间轴**：`decode` 97.6 %（选中）、`queue_wait` 2.4 %（未选中）——再次印证无排队区间；
- **GPU 时间轴**：并发桶 1 / 4-7 / 8-15 / 16-31 选中（8-15 桶独占 55 %）。

资源挂接（G08'）：选中的 GPU 桶挂 w03' 的 NCU 中位数（SM 48.6 / DRAM 18.2 / **L2 76.1** / Tensor 48.9）
→ **L2/tensor-pipe 受限的批量 GEMM**；`decode` 段显式标注 `not_collected_host_or_wait`（批共享下无单
kernel 对应）。机会窗口（含证据指针）：提高批驻留（有吞吐余量、无延迟收益——程序被自身关键路径
束缚）与程序级调度（仅排队区间生效，引 §5.2 的 0.72×/0.57×）。产物含 G09' 表格清单
（`tables_manifest.json`，6 张表 + sha256）与 G10' 双视图报告（`G06_G10_REPORT.md`），
View B 明确标注可见范围 = 已捕获 CUDA 区间 + NCU 仅覆盖 GEMM 家族。

### 模块级 NVTX 的最终结论（阴性结果，三种执行模式实测）

GPU 恢复后用 `tiny_mixed.json` 补做了两次捕获，加上此前的 graph 模式共验证三种执行路径：

| 执行模式 | 捕获 | 模块 NVTX |
|---|---|---|
| torch.compile + CUDA graph（生产默认） | plas_short2 / plas_r2 | 无 |
| `--enforce-eager`（编译关闭） | eager_tiny | 无（包装器挂在编译层，eager 下不执行） |
| 编译开 + `cudagraph_mode=NONE` | nvtx_nograph | 无 |

**结论**：vLLM 0.29.0 的 `--enable-layerwise-nvtx-tracing` 在本环境三种模式下都未把模块标记送进
nsys（trace 中仅见 cub/CCCL 库自带 NVTX 与客户端标记）。w01' 的最终方法维持家族划分 + 并发桶划分
（两者守恒），算子级 launch-ownership 归因在此 serving 栈上判定为不可达并留档。

**顺带对照**（同一 tiny 负载，w01' 于两份新捕获）：eager 口径 GPU busy 72.2 %、no-graph 编译口径
60.3 %，家族分布几乎一致（gemm 86.2/84.9 %、gemv 仅 6.5/7.9 %、attention ~4.6 %）——
**即使 eager serving，批处理仍让线性层保持 GEMM 形状**，gemv/DRAM 墙不回归；eager 更高的 busy %
是更慢的 kernel 与更多发射（开销显形），不是更多有效工作。

## 7. 工具链问题的根因诊断（NVTX / nsys / NCU）

三件事根因各不相同，证据均在案：

1. **vLLM 模块 NVTX 不出标记 = vLLM 插桩缺口，不是 NVTX 坏了。** NVTX 本身工作正常（同一 trace 里
   客户端 904 对标记与 cub/CCCL 库自带标记完整记录，nsys 报 "NVTX injection initialized successfully"）。
   `--enable-layerwise-nvtx-tracing` 的标记逻辑挂在 torch.compile 包装层的 `__call__` 上
   （`compilation/wrapper.py`），而 v1 引擎稳态执行路径三种模式都不经过它：graph 模式走 CUDA graph
   重放、eager 模式压根没有编译包装层、compile+NONE 模式稳态走 bytecode 直接分发。
2. **nsys ~30 s 后停录 CUDA = 工具链版本错配，nsys 诊断日志自己承认。** 本机 nsys 2024.6.2 内置
   CUPTI **12.8**；`.venv-vllm` 的 torch 是 **cu130（CUDA 13.0 运行时）**、驱动 **595.91（CUDA 13.2）**。
   诊断表原话："Installed CUDA driver version (13.2) is not supported by this build of Nsight Systems"、
   "Not all CUDA events might have been collected"——CUPTI 12.8 追 CUDA 13 上下文时先部分工作后停止
   （收了 28.6 万事件后截止），NVTX（纯 CPU 注入）不受影响所以标记完整。**h22 之所以没这个问题**：
   conda 环境是 torch 2.11+cu128，与 CUPTI 12.8 匹配，7 分钟采集完好。
3. **NCU 的三个症状 = 版本错配 + 容器脆弱性叠加。** ncu 2026.2 是新的，但驱动/运行时组合下：
   (a) `--launch-skip` 落在预热 fill kernel 是采样语义不是故障；(b) 跨进程 attach 子进程剖析中途
   失败（"Failed to profile ... in process"），同进程剖析则成功（4 kernel）；(c) 长重放会话两次触发
   驱动故障，随后容器丢 GPU（NVML Unknown Error）——这是 Docker + NVIDIA 的已知模式：profiler 崩溃/
   cgroup 撤销后容器内设备失效，需宿主机重启容器。

**修复路径**（供后续）：nsys 升级到支持 CUDA 13 的版本（2025.x+）即可解除 30 s 截断；或将 serving
环境降到 cu128 torch 与现有 nsys 对齐。NCU 子进程问题用 `VLLM_ENABLE_V1_MULTIPROCESSING=0` 规避即可。

## 8. 工具链修复后的完整 w01'（三划分守恒 + 阶段级 launch-ownership 恢复）

根据"当前容器有多个 CUDA 版本"与"允许 trace 开销"的授权，最终采集栈为：

```
/opt/nvidia/nsight-systems/2026.3.1/bin/nsys   # CUDA 13 兼容，替换 PATH 里 cuda-12.8 的 2024.6.2
VLLM_NVTX_SCOPES_FOR_PROFILING=1               # v1 runner 的步骤级 NVTX scopes
VLLM_USE_V2_MODEL_RUNNER=0                     # 0.29 默认选 V2 runner（不带 scopes），强制回 V1
生产 graph 模式（无需 eager）
```

三个问题的最终根因与修复（捕获 `artifacts/agentix_8b/autotrace/scopes_v1/`）：

| 问题 | 根因 | 修复 | 验证 |
|---|---|---|---|
| nsys 30 s 截断 | nsys 2024.6.2 内置 CUPTI 12.8 vs 驱动 13.2 / torch cu130（诊断日志明示 unsupported） | 换 nsys 2026.3.1 | CUDA span 16.4→181.4 s，194 438 kernels，全程覆盖 |
| 模块 NVTX 缺失 | 步骤 scopes 写在 **V1** runner；0.29 默认用 **V2** runner（日志 "Using V2 Model Runner"），代码根本没执行——不是 NVTX 或 nsys 的问题 | `VLLM_USE_V2_MODEL_RUNNER=0` + scopes 环境变量 | 9 020 个 step 的 preprocess/forward/sample/postprocess scopes 全部出现 |
| NCU 子进程失败 / launch-skip 采偏 | 版本组合 + 采样语义（见 §7） | 同进程 + kernel 名过滤（既有约定） | — |

**w01' 现在有三条互为守恒的划分**（GPU busy 12.6 s，守恒误差 10.4 ms ≈ 0.08 %，未归因 ≈ 0）：

1. kernel 家族：gemm 79.4 %、attention 13.2 %、gemv 3.6 %；
2. 请求并发桶（w04''/w05'' 的输入）；
3. **阶段级 launch-ownership（新恢复的 AutoTrace 原语义）**，按发射线程上的最内层 scope 归属：

| 阶段 | GPU 时间 | 家族构成 |
|---|---:|---|
| postprocess | 81.9 %（8.41 s） | gemm 95 % |
| forward | 14.6 %（1.50 s） | attention 90 % |
| sample | 2.0 % | reduce 77 %, copy 23 % |
| preprocess | 1.5 % | elementwise 为主 |

**解读注意**：阶段名沿用 vLLM 自己的 scope 摆放。FULL_AND_PIECEWISE 下，attention 是 graph 切分算子、
逐 step 即时发射（落在 forward scope），而编译区域的 GEMM 及 `compute_logits`（lm_head）的发射浮出在
postprocess scope——阶段合计在 launch-ownership 意义下守恒且正确，但**阶段名不能读作计算的
forward/post 边界**；按家族轴（gemm 79 %）与阶段轴（postprocess 82 %）交叉即可还原真实结构。

## 9. 正式链：论文核心机制复现（agentix_core）后的三模型 AutoTrace（2026-09-14）

§1–8 的链条按用户判定标记为**未完成/预备件**（trace 对象是 vLLM 原生 priority 直通，非论文机制实现）。
本节为正式链：`agentix_core` 实现论文 Algorithm 1 的单卡核心机制（按 p(c) 离散入队 K=4、每队列 token
量子 32/64/128/256 + 分块续跑承载抢占、量子用尽降一级、β=2.0 比率反饥饿提升至 Q1 并重置 W_c/T_c、
进程表 {T_p,W_p} 实时更新；vLLM 原生优先级/前缀缓存/chunked prefill/CPU KV offload(8GB native) 为接入项。
论文未公布 K/量子/β 数值且无开源仓库——KB 核实——参数为声明配置）。负载 = 论文校准 Mixed r0.3（拟合）/
r0.2（打分），双 4090 并行采集，nsys 2026.3.1 + V1 runner scopes。

### 机制行为证据（LLaMA r0.3）

入队分布 Q0/Q1/Q2/Q3 = 16/98/176/1339（新程序高优先、累积服务多的 LATS 沉底——正是"非全进 Q1"的论文语义）；
88 个 call 行使 2–4 个量子（降级路径）；吞吐 618 tok/s 与直通 PLAS 持平（机制开销不伤吞吐）。

### 三模型正式链结果

| 模型 | w01' busy% / gemm% | w02' 对齐 / 峰值并发 | w04'' 误差 | w05'' | G10 时间线（请求数 / 高延迟 / 峰值并发） |
|---|---|---|---:|---|---|
| LLaMA-3.1-8B | 8.7 / 68.4 | 108 µs / 33 | **−4.48 %** | ✅ 4 选中 | 1629 / 151 / 32 |
| Qwen3-1.7B | 13.8 / 75.0 | 90 µs / 27 | **−2.38 %** | ✅ 5 选中 | 1629 / 150 / 27 |
| Qwen2.5-VL-3B | （r0.3 分析在 analysis/） | ✅ | **−8.32 %** | ✅ 4 选中 | 1629 / 155 / 29 |

G10 交付物（每模型）：`artifacts/agentix_8b/autotrace/<m>_core_g06_g10/G10_TIMELINES.html` ——
**V1 端到端时间线**（GPU busy 0.5s 分箱 + 在飞请求数同钟）、**V2 高延迟时间线**（每请求一行、
类分组、decode > 类中位+3×MAD 标红）、**V3 并发分析时间线**（并发桶着色 + GPU 时间份额互证）+
综合分析段；全部从复现捕获数据直接渲染（`render_g10_timelines.py`）。

NCU 说明：w05'' 资源挂接复用各模型既有 NCU 采样（kernel 层不随客户端调度策略变化）。

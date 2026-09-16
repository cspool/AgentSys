# 抢占机制探索计划（三层，后置执行）

日期：2026-09-16。前置任务：先完成 agentix_core 与其论文 baselines（vLLM / vLLM-opt /
调用级 MLFQ）的分析与 trace 终版报告；本计划在其后执行。

## 总纲与立场

抢占在机器层面**永远是负提升**——它不创造 FLOPs，只重排归属，且每种机制有自己的账单。
它的功能是**时间价值套利**：等待总量守恒（或略增），从"贵的时间"（短程序串行链、面向
用户的 LC 调用）搬到"便宜的时间"（有程序内并行 slack 的 BE、长链摊薄）。因此本计划的
核心不是"实现更多抢占"，而是回答三个问题：每种机制的开销是什么（第 1 层）；agent 程序
到底需不需要抢占、开销由谁 overlap（第 2 层，重点）；抢占与高利用率 kernel 调度的冲突
如何裁决（第 3 层，重点）。

### 根本冲突（第 3 层的哲学，贯穿全文）

高利用率技术（mega-kernel / MPK、CUDA graph、PD 打包批）与抢占是**同一根轴的两端**：
前者把工作熔成更大的不可中断单元换取利用率——**整体性能优先**；后者要求细的可中断
边界换取响应性——**服务/机制优先**。熔合度每升一级（eager kernel → graph step →
打包批内 → mega-kernel），利用率涨、抢占粒度降。任何抢占设计必须先声明自己站在这根
轴的哪个点、为谁付出多少利用率。

### 成本三分法（机制选型的决策规则）

| 家族 | 代价货币 | 成本结构 | 适用时间尺度（agent 三尺度对应） |
|---|---|---|---|
| 驱逐式（非挂起） | 状态搬运带宽 | 每事件常数：保存+恢复流量 + 全冷重建；搬运本身冲刷 L2 | tool delay（100 ms–10 s）：驱逐 **KV 驻留权**而非计算（copy engine 独立通道 + 可预测返回时刻预取） |
| 挂起式 | 容量 | 分配制资源（寄存器/smem/warp slot）持续占用 → 并发↓ → 吞吐损失 ∝ 占用份额 × 时长；缓存制照样 miss（但少付搬运那份） | prefill chunk（~ms）：时长近交叉点 t\*，且 LC decode 只需少量发射带宽 |
| 门控式 | 反应延迟 | 零搬运、零占用、零污染；代价 = 等当前驻留工作跑完（期望 ≈ 被门控单元一半时长） | decode kernel（5–50 µs）：反应延迟远小于 t\* |

交叉时长 t\* ≈ 驱逐固定成本 ÷（占用份额 × 单位时间吞吐价值），本栈粗估数百 µs 量级
——待第 1 层实测后从数据直读。

### 开销由谁 overlap（第 2 层的分析骨架）

1. **受害者内部 slack**（最大）：lats 波内并行（宽 5）遮蔽单调用延迟、长链摊薄。
2. **队列**：排队制下被抢占者回到非空队列，其多等时间里 GPU 在做有用功——系统视角
   开销 ≈ 0。这解释了实测"非排队区间三策略无差异"。
3. **机制专属**：前缀缓存吃 recompute；copy engine 吃搬运；门控等待期间跑的是在飞
   窗口内别人的有用 kernel。
4. **闭环反哺**（agent 独有、唯一正吞吐通道）：LC 更早返回 → 程序更早发起下一调用 →
   到达率↑ → 批更满（论文 Fig.4；实测 core 吞吐 +4 %）。

**开启判据**：三承接方（队列 / 受害者 slack / 闭环）至少存在其一才开抢占；均不在
（空载、开环、无并行）时纯亏，正确动作是不抢。above-cap 时长与波宽运行时可测。

### 评估口径（两种场景分开评，各有冠军）

- **同质场景**（Agentix 论文目标）：全体 ptl mean/p90 + 整体吞吐。实测冠军 agentix_core
  （客户端续传，mean 20.7 vs 基线 27.6）。
- **LC/BE 混部**（GPreempt/REEF 目标）：LC SLO 达成（ttft/ptl p99）为硬约束，其上最大化
  BE 吞吐。实测冠军翻转：agentix_engine（LC ttft p99 353 ms vs core 824 ms vs 基线
  2,302 ms），BE 侧全臂持平（±1.5 %）——本负载 LC 仅占 token 量 ~6 %，LC 优先近乎免费。

---

## 第 1 层：机制开销分别量化（每机制一张成本卡）

产出物 `MECHANISM_COST_CARD.json`（每臂一张）：
{机制, 家族, 粒度, 触发计数(子进程 ledger), 吞吐Δ, 抢占延迟分布, 恢复延迟分布,
LC/BE 双口径指标, 专属开销签名(trace 坐标)}。

抢占/恢复延迟从各臂 NVTX 配对事件逐事件计算（`engine_demote`→该请求下次调度、
`chunk_begin/end`、semgate write→流恢复、双上下文 kernel 交替边界）。

**已核实的测量有效性教训（必须遵守）**：runner 级补丁在 V2 model runner 下静默失效
（V1 类被 patch、V2 类在跑）——所有臂必须 `VLLM_USE_V2_MODEL_RUNNER=0` 且以子进程
stdout ledger 验证触发，否则数字是"基线噪声"（曾导致流优先级/绿上下文两臂结论作废重测）。

现有臂矩阵（各自独立开关、独立 NVTX、独立 trace）：
fcfs(graph/nograph)、agentix_core（客户端续传）、agentix_engine（调度器原生抢占）、
mlfq_call（论文 MLFQ baseline：调用级、Q0 准入、无程序表）、agentix_hw（流优先级）、
agentix_hw_gctx（Green Context SM 分区）、agentix_hwctx（双 CUDA 上下文硬件时间片，
GPreempt 核心机制）、agentix_layer/window/hint/victim。
待建：agentix_budget（份额调制）、agentix_semgate（GPFIFO 信号量门控，已单测可用：
waitValue 硬件真挡流、写值放行）、agentix_graphgate（graph 条件节点层门控）、
agentix_resident（CTA 驻留门控 + nanosleep + 占用规划）、agentix_kvres（KV 驻留权
驱逐，swap 路径，补论文保真度）、RM timeslice/interleave（待只读探测）。

## 第 2 层（重点）：agent 程序是否需要抢占、开销如何 overlap

**方法立场：一切基于无抢占的分析与 trace。** 先决条件已满足——六个 fcfs 侧捕获带全套
workload_analysis（W1–W5）+ perf_trace（A00–A05），它们就是"无抢占基准解剖"。

任务：
1. **需求判定文档**：以 fcfs trace 为底，逐负载区间回答"需不需要"：
   - 非排队区间（r ≤ 0.3 未 cap）：不需要（实测三策略无差异，抢占纯付成本）；
   - 排队区间：需要，需求形态 = LC 等待（r0.5 LC ttft p99 2.3 s，随负载恶化）；
   - 判定输出为开启判据的参数化（above-cap 阈值、波宽阈值）。
2. **动机与场景清单**：从 trace 标出抢占将作用的位置（重 forward 堆 = 大 batch/prefill
   步、LC 调用被 lats 洪流阻塞的车道段）与每处的 overlap 承接方及其 trace 证据坐标。
3. **overlap 定量**：每条承接通道给出实测吸收量（如 lats 波内遮蔽率 = 单调用延迟注入
   后程序完成时刻不变的比例，可从现有 calls jsonl 重放估计）。

## 第 3 层（重点）：抢占 × 高利用率 kernel 调度的冲突

**方法立场：先对非抢占情况做分析与 trace。** 缺口 = 同负载下三种非抢占熔合配置的
利用率-粒度曲线：
- eager（kernel 粒度可门控，host 开销大）；
- graph（step 粒度一次 launch，层门控失效——layer 臂被迫关 graph 的税）；
- PD 打包（chunked prefill 混批，kernel 内部混合，launch 级机制全部失明）。

采集：fcfs × {eager, graph, 打包配比×2} 各一次 nsys capture（无抢占），量：busy%、
step 时长 vs 批内 token 构成曲线（重 forward 堆成员时长-构成关系）、抢占粒度下界。
mega-kernel 端点无实现物，以 MPK 笔记外推并如实标注未实测。

**裁决框架**：
1. 打包批内抢占的最小单元是 **token 份额**而非请求——`agentix_budget` 把
   max_num_batched_tokens 按 LC 队列状态逐 step 动态调（利用率感知门控的连续版本）；
   策略：s_t = argmax 吞吐 s.t. step_time(s_t + d_t) ≤ LC TBT SLO。
2. 能在打包 kernel **内部**做选择性抢占的只有 CTA 级机制（prefill 行 = 独立 GEMM tile
   = 独立 CTA）——agentix_resident 的存在理由。
3. 包内缓存隔离：decode KV 热区划 L2 persisting（4090 实测 51.9 MB 可划），prefill
   限制在 normal 区；NCU 量混合 step 中 decode 行 L2 命中率有/无窗口之差。
4. 空间分区条件启用：仅当 decode 自身能填满其分区时才分，否则打包（判据 = 运行时
   busy/带宽计数，lanes 已有）。

产出：**利用率增益 vs 抢占延迟下界的权衡曲线**（三个熔合刻度 + 各机制可达点），并
据此给出"整体性能优先 vs 服务/机制优先"两种立场各自的推荐配置。

## 容量塑形研究纲要（E1–E5，第 3 层的升级版主线）

顶层论题：**在 agent serving 里，调度与抢占不是排队排序问题，而是容量塑形问题；
其统一形态是"动态并发控制"——并发度是被控变量，抢占机制族是执行器**（各有作动
速度与成本），服务优化的阈值分层调度框架是实验台基线。经典"吞吐与顺序无关"的
不变性在此断裂于四条通道：①批构成=内生服务率；②KV 是可调度资源（统计复用/超卖）；
③可抢占性有容量价格（熔合阶梯）；④闭环 λ=N/W。agent 独有加成：需求可预测（波结构、
串行链、tool 返回时刻）→ 前馈控制，而非仅反馈。

- **E1 可抢占性定价曲线**：熔合阶梯（eager/piecewise graph/full graph/打包预算）×
  饱和吞吐 × 实测可达抢占延迟 → Pareto 前沿；mega-kernel 端点以 MPK 笔记外推并标注未实测。
- **E2 KV 统计复用**：先从现有 fcfs trace 量出"驻留但闲置"KV 份额与时长分布
  （tool-delay 窗 ∩ KV 占用），再以 kvres 臂扫超卖系数 → 吞吐增益 vs 级联抢占风险曲线。
- **E3 空分 vs 时分（饱和口径重审）**：按资源互补性定分区的 green ctx vs 时间复用，
  混合负载饱和吞吐对决——此前仅以延迟口径判负，吞吐问题未问。
- **E4 闭环耦合量化**：固定 N 闭环负载生成器（需新增闭环模式），量吞吐=N/W 对 W 改善
  的响应；找 KV 约束咬合点 N\*，与 E2 汇合。
- **E5 动态并发控制器**：双向执行器（准入/门控/挂起/驱逐）+ 前馈（agent 可预测到达）
  + 反馈（SLO/利用率），执行器成本入环、带迟滞防颤振；对照静态 cap 阶梯（8/16/32）与
  仅准入侧动态（μShare 式）。指标：goodput、SLO 达成、利用率跟踪误差、抢占风暴计数。
  失稳案例参照：Tetris 级联抢占 = 执行器振荡。

## 执行顺序

1. （前置，进行中）论文臂终版报告：4 臂 sweep + trace + R10 报告更新。
2. E1 先决采集（熔合阶梯无抢占 trace）——兼作第 1 层 eager/graph 对照，一份两用。
3. 第 1 层：V1 环境臂矩阵成本卡（含待建臂逐个实现）。
4. 第 2 层分析文档（零 GPU，可与 2/3 并行推进文字部分）。
5. 汇总：权衡曲线 + 开启判据 + 两立场推荐配置，并入 R10 总结文档新章节。

## 论文事实备忘（Agentix 抢占谱系）

vLLM / vLLM-opt：无调度抢占（仅引擎 KV 压力驱逐）。MLFQ baseline：**有**（调用级）。
Agentix core：**有**（程序级 MLFQ），被抢占者处理为 **swap 式**（KV 换出 CPU + §4.2.2
多步调度减少换出 + §5 连续大块 swap kernel）。我们的 engine 臂用 recompute+前缀缓存
路径——保真度差异（recompute 付计算 / swap 付 PCIe）由 agentix_kvres 臂补齐对照。

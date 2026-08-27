# G3：Agent 应用全栈系统加速——实现与实验报告

更新日期：2026-08-26

项目目录：`/workspace/AgentSys`

状态：已完成。run 032 通过4/4严格串行阶段和15/15参数化系统证书要求。结果边界见“证据分级与限制”。

## 摘要

动态 Agent 程序会在 program、LLM call、异构 flow、NPU tile 和执行引擎之间连续产生依赖、排队与优先级变化。单独优化任一层，无法保证上层紧急程序在下层仍被及时执行。本项目实现的最终活动路径为 `Agent 应用 → Agentix → mllm → Agent.xpu → TISA → HPTPE XPU → 普通 RISC-V Rocket`。CPU 采用普通 RISC-V，ATX 不进入最终结构、ABI 或性能结论。

五个活动组件先独立复现：Agentix 16/16、Agent.xpu 11/11、TISA 10/10、mllm/llm.npu 5/5、HPTPE 26/26，共 68/68 个预登记端点通过 15% 门槛，最大误差 9.91%。mllm 还通过 20/20 个上游原生可执行文件与 101 个 gtest；HPTPE 通过 9/9 个 RTL 组织、302 个 signed golden checks 和 9/9 个全规模 lint。

集成阶段把上游 Qwen3 QNN-AOT MIR 的 80 个描述符编译进同一 RISC-V ELF，并在真实 Chipyard Rocket+Verilator static/dynamic 系统上执行。run 027 的 20/20 门禁全部通过：强静态/动态后端为 4,900/3,560 周期（1.376×），系统区间为 1.340×，CPU 观测端到端为 1.056×；两端均执行 614,400 个 HPTPE MAC、相同 DMA 和逐位相同校验和。最终 trace 含 860 events、11 个层次，并为每个 TISA issue/complete 保留 mllm 源算子、Agent.xpu flow/stage/placement 和 HPTPE/VE/DE 落点。

H14进一步把固定负载改造成完整参数化实验系统。`agentsys-run-workload`可从JSON切换Agent DAG、Agentix策略、Agent.xpu参数、mllm MIR/operator、tool、DMA和兼容硬件profile，自动生成隔离的header、RISC-V ELF和系统trace。`react_moa_mcts`、`react_tool`、`planner_debate`三种负载分别产生80/16/40 descriptors、860/180/436 events并全部通过。专用 TISA 文件通道逐tile记录显式call ID，六份日志均为零修复。

`agentsys-layer-regression`从同一matrix实际驱动五层参数，并在相同论文workload/config下重新审计68/68 endpoints，统一误差门槛10%，最大误差9.91%。Agentix batch、Agent.xpu chunk、TISA window、mllm prompt和HPTPE organization五个敏感性切换均改变真实输出。

这些结果支持“跨层优先级与动态调度能够叠加，但收益受释放时机、tile 粒度、强基线、数据流和带宽瓶颈约束”的结论。项目没有将 Rocket 或开放替代模拟器冒充论文所用的 A100、Intel Core Ultra、Qualcomm 手机、Epoch 真硅片或 SAED32 综合环境。

## 一句话论证

在动态 Agent 服务中，AgentSys 将 Agentix、mllm、Agent.xpu、TISA 与 HPTPE 落到普通 Rocket 系统；68 个论文端点与 860-event 真实系统 trace 共同证明机制、工具链和工作守恒，同时显式保留原始专有平台边界。

## 术语与约定

| 规范术语 | 定义与本文用法 |
|---|---|
| Program | 一个动态 Agent 程序，可包含串行或 DAG 形式的多个 LLM call 与外部 interrupt。 |
| Call | 一次 LLM 调用；Agentix 的基本调度对象。 |
| Flow | Agent.xpu 中贯穿 prefill/decode 的有状态请求，分为 reactive 与 proactive。 |
| Task | 历史 ATX 原型中的异步任务层；修订后的活动路径直接由中立 XPU runtime 提交 TISA 描述符。 |
| Tile | 保留 OpType、UnitMap、TileMem 和 dependency 的粗粒度执行单元。 |
| PLAS | Program-Level Attained Service；按单线程 program 已完成服务量排序。 |
| ATLAS | Adaptive Thread-Level Attained Service；用最长已观测关键路径服务量近似动态 DAG 优先级。 |
| HEG | Heterogeneous Execution Graph；记录算子 affinity、placement 和 elastic binding。 |
| ATX | Accelerator Task Extensions；仅保留为历史独立论文实验，不参与最终普通 RISC-V 路径。 |
| TISA | Tile-level Instruction Set Architecture；本文实现 typed dependency、TileMem hazard 与动态发射。 |
| ME/VE/DE | Matrix Engine、Vector Engine、Data Engine。 |
| Priority | 数值越小越紧急：reactive=0、normal=1、proactive=2；在六层保持不变。 |
| Paper endpoint | 从目标论文预登记的数值；误差定义为 `abs(observed-target)/abs(target)`。 |

### 目标论文清单

修订后的“论文性能复现”严格指 Agentix、Agent.xpu、TISA、mllm/llm.npu 和 HPTPE 五个活动组件。五份独立 profile 在 `config/revised-toolchain.json.paper_profiles` 中注册命令、源码、revision、输出和端点数量。ATX 四组件旧合同保留在 `config/toolchain.json`，但不进入修订证书。MLX_dev `sys` 只作为 Chipyard/RoCC 工程参考，不作为性能来源。

## 研究问题与贡献

本项目回答四个问题：

1. 程序级、异构 flow 级和 NPU tile 级调度能否形成可执行的完整路径？
2. 上层 priority 是否能无歧义地下传，并在 shared engine 和 DDR backpressure 下保持可审计？
3. 各层收益来自排队、放置、抢占、预取、tile overlap 还是带宽；哪些收益不能叠加？
4. Agent应用与框架产生的真实trace能否编译为RISC-V软件，并在Rocket CPU+XPU系统模拟器中端到端执行？

对应贡献为：

- 实现可执行的 Agentix PLAS/ATLAS、Agent.xpu flow scheduler、mllm/llm.npu机制和 TISA scheduler，而非仅整理设计说明。
- 为 mllm v2 增加原生 MIR trace consumer/backend，直接解析 Qwen3-1.7B MIR 的 SSA、shape、dtype 和 operator dependency，并执行上游 runtime/CPU backend 测试。
- 在 `/root/chipyard` 固定 commit 上实现中立 `xpu_v2` custom0 RoCC、HellaCache DMA、8-entry TISA window、HPTPE 16×16 ME、VE/DE 和 bare-metal runtime。
- 使用官方 Ramulator2 v2.0a 实际运行 Qwen3 DE trace，并把测得的 DDR service factor 回注 TISA DE latency。
- 生成统一 11 层 JSONL 系统 trace、消融、机器可读结果和最终审计，而不是用汇总文字代替原始证据。
- 执行 ReAct、Mixture-of-Agents 与 MCTS 应用，把框架 Call/Flow 和上游 mllm MIR 编译成 RISC-V ELF，在 Static/Dynamic Rocket+HPTPE 上运行并回收 application 到 PE 阵列的 cycle trace。

## 系统架构

### 当前系统集成范围修订

最终CPU采用普通RISC-V，不参考或集成ATX CPU架构。ATX已有结果仅作为历史独立论文实验保留，不参与后续统一系统的结构、性能或创新结论。新的目标路径为：

```text
Agent应用 / Agentix上层调度
    ↓
mllm真实模型框架与算子lowering
    ↓
Agent.xpu reactive/proactive Flow与异构放置
    ↓
TISA动态Tile调度
    ↓
HPTPE完整PE阵列 / VE / DE
    ↓
Chipyard普通RISC-V CPU + XPU系统模拟
```

mllm、Agent.xpu和HPTPE必须先分别完成各自论文机制、工具链与性能实验复现，独立通过后才允许接入统一系统。run 021证明了compiled trace可以在Rocket+RoCC上执行，但其ATX式runtime和简化ME只作为旧范围路径原型。run 023/024/025关闭独立复现，run 026保留第一次集成的性能范围失败，run 027完成修订后的最终系统。

其中，mllm性能复现按其官方仓库引用的ASPLOS'25 `llm.npu`论文执行，必须实现chunk-sharing graph、shadow outlier execution与CPU/NPU异序子图调度；现有MIR→TISA的1.324×只证明lowering可执行，不计为mllm论文性能。HPTPE必须执行官方OPT1/OPT2/OPT3/OPT4C RTL并核对仓库内DC报告，当前四路OS ME不计为HPTPE复现。具体预注册端点、证据边界与先独立后集成的门禁见`experiments/h13-revised-stack/protocol.md`和`docs/component-reproduction-audit.md`。

简洁实施顺序如下：

1. 固定普通RISC-V CPU基线与CPU↔XPU统一接口，移除集成路径中的ATX依赖；
2. 分别完成mllm真实framework/backend、Agent.xpu异构调度和HPTPE完整PE阵列的独立复现；
3. 按`mllm算子 → Agent.xpu Flow → TISA/HPTPE XPU`逐层接入Chipyard；
4. 执行普通RISC-V+XPU端到端Agent trace，验证同work、依赖、DMA与功能结果；
5. 复验各层论文性能误差≤15%，更新工具链、报告和最终证书。

以上五步均已实现。run 027 的活动结构为：

```text
ReAct / MoA / MCTS
  → Agentix 3 programs / 11 calls
  → upstream mllm Qwen3 MIR（每次 LLM call 8 个 native operators）
  → Agent.xpu reactive/proactive flow、stage、placement、preemptibility
  → xpu_v2 config/launch/wait/status/clear
  → TISA W=8、动态分派 7 cycles、ME/VE/DE semantic issue
  → HPTPE OPT1 compressed-OS 16×16 array
  → Rocket HellaCache DMA / system memory
```

run 026 首先通过功能与 lineage，但由于把 static baseline 逐算子串行化，得到 2.000×，超过注册的 1.14–1.63×，因此作为 18/19 负结果保留。run 027 在结果前锁定论文的强静态 stage pipeline 与 7-cycle dynamic dispatch，得到 1.376× 并通过 20/20 门禁；阈值没有事后放宽。

### 参数化负载与逐层实验（run 030/031）

负载不再写死在 Python 函数。版本化 manifest 描述 program/call DAG、priority、arrival、LLM/tool、token shape、MIR与source operators、Agentix/Agent.xpu参数、TISA/HPTPE profile和可选性能期望。每个 workload 使用 canonical SHA-256，所有产物写入独立目录；兼容已安装硬件时只重编译 header/ELF，不重编译模拟器。

```bash
.venv/bin/agentsys-run-workload --workload workloads/react_tool.json --run-id demo
.venv/bin/agentsys-layer-regression --matrix config/layer-regression-matrix.json
.venv/bin/agentsys-reproduce-parameterized
```

run 029 首次切换负载时发现两个旧固定负载掩盖的问题：HPTPE pipeline state 使第2/3个ME tile结果依赖调度顺序，UART还可在marker名字内部切断RTL日志。run 030 在descriptor start周期局部复位完整HPTPE pipeline，并把TISA issue/complete写入plusarg选择的专用文件。系统现在逐个比较 `(call, descriptor, engine)` checksum，而不只比较可能发生XOR抵消的aggregate。

| Workload | Programs/calls | Descriptors | Trace | HPTPE MACs | Gates |
|---|---:|---:|---:|---:|---:|
| react_moa_mcts | 3/11 | 80 | 860 | 614,400 | 21/21 |
| react_tool | 1/3 | 16 | 180 | 122,880 | 18/18 |
| planner_debate | 2/6 | 40 | 436 | 307,200 | 19/19 |

run 031 的五层matrix通过9/9 gates：Agentix/Agent.xpu/TISA/mllm/HPTPE分别为16/11/10/5/26 endpoints，合计68/68；最大误差分别为9.09/8.07/8.27/9.91/0.98%。参数变体不是论文点，只用于证明配置被实现消费，而不是无效metadata。

### 既有run 021原型结构（历史）

下图描述已经完成的旧范围原型，其中ATX task层和简化ME不会直接沿用为修订后的最终架构。

```text
Agent program DAG
    │  PLAS / ATLAS / external urgency
    ▼
LLM calls
    │  HEG placement / prefill-decode elasticity / adaptive batch
    ▼
reactive & proactive flows
    │  ATX async submit / prefetch / cancel / double buffer
    ▼
tasks
    │  mllm MIR lowering: OpType + SSA deps + TileMem + UnitMap
    ▼
TISA tiles ── typed RAW/WAR/WAW + scope/bank/range checks
    │
    ├───────────────┬───────────────┐
    ▼               ▼               ▼
ME (OS MAC)         VE              DE ── SRAM/DMA/Ramulator2 DDR
    └──────────── completion feedback / unified events
```

真实系统trace路径不是上图的主机侧估算：`agent_application.py`实际执行程序DAG，`system_trace_compiler.py`把11个Call（10个LLM、1个tool）及每个LLM的8个MIR算子编译为C header；Rocket裸机runtime检查Call依赖，在CPU执行tool，并为80个descriptor发出config/launch/wait。最终从同一个ELF获得application/framework/software/cpu/xpu/dma六层cycle trace。

### Program 层：Agentix

`src/agentsys/agentix.py` 实现 FCFS、MLFQ、PLAS 和 ATLAS。Call 仅在动态 parent 完成后进入 ready queue。PLAS 使用已完成 call 的 program service；ATLAS 使用 parent priority 与 runtime 的最长路径。run 008 在两者之前增加 external urgency，形成 `(reactive/proactive, attained-service queue, FCFS order)` 的词典序，解决 run 007 暴露的“低层 priority 无法弥补 call 晚释放”问题。没有传入 priority map 时，原 Figure-2 调度行为保持不变。

### Flow 层：Agent.xpu

`src/agentsys/agentxpu.py` 实现三类组织：iGPU、Serial NPU-iGPU 和 HEG。模型覆盖：

- prefill chunking 与 NPU/iGPU stage decoupling；
- reactive-first prefill、decode batch cap 和 slack piggyback；
- tile/token 边界抢占与 fixed overhead；
- Figure-4 约束的 shared-DDR GEMV contention；
- 论文 active-period-weighted iGPU utilization 与独立 wall occupancy；
- NPU、iGPU 和 12 W CPU kernel-control energy。

### mllm operator trace backend

`src/agentsys/mllm_backend.py` 消费 mllm 原生 `.mir`，只解析 executable `linalg.<device>.<Op>`。Linear/MatMul/Embedding 降到 ME，算术/归一化/softmax/reduction 降到 VE，view/transpose/slice/concat/cast/copy/cache 降到 DE。SSA producer 生成 dependency；tensor shape/dtype 生成 TileMem size；同一 SSA 的 in-place view 复用地址，从而触发真实 alias hazard。run 005 保留 2–16-cycle tile 导致 dynamic 变慢的负结果；run 006 按 TISA 的 `10^3–10^5` cycle 粒度修正后通过 9/9 门禁。

### mllm / llm.npu独立复现（run 023）

固定commit `50ad5a9b`的mllm v2已用Clang 16真实构建C++ runtime、CPU backend、IR/JIT、量化工具、benchmark与测试程序；20/20个选定原生测试程序、101个gtest case通过，另有1个需要外部tokenizer的oracle按上游设计跳过。未过滤的首次CPU kernel运行保留为负结果：上游将x86明确标记NYI的FP16、INT8/INT16 divide、Clip等用例和后续崩溃包含在同一程序中；最终门禁仅过滤到上游实际支持的37/37 kernel cases，并在结果中列出排除项。

`src/agentsys/mllm_npu.py`随后从真实Qwen3 QNN-AOT MIR/config取得1602个算子、28层与32-token chunk；首个decoder block含30个可共享static op和27个attention/shape-dependent op。实现chunk-sharing graph、0.1–0.3%稀疏shadow outlier与85% layer pruning、论文式CPU/NPU causal dependency和stall-contribution异序调度。4,480个子图在naive/OOO两种模式各检查18,336条依赖并保持1.26s NPU与0.63s CPU工作量相同。Chunk sharing为1.974×、shadow outlier为6.600×、OOO latency reduction为32.907%；NPU bubble由33.333%降至0.636%。5/5个预注册端点通过，最大误差9.91%。22.4×跨平台平均值需要原五个baseline和两部Qualcomm手机，明确标为不可直接比较，而非用模拟值替代。

### Task 层：ATX adapter

`src/agentsys/atx.py` 提供 16-entry bounded queue、priority heap、double buffer、prefetch、queued/running cancellation、completion 和守恒计数。硬件 ABI 由 `system_sim/software/agentsys_runtime.h` 暴露：

| funct | 操作 | 语义 |
|---:|---|---|
| 0 | config | 写 descriptor control、TileMem 或 global configuration。 |
| 1 | launch | 传入 input/output DRAM pointer，经 HellaCache DMA 启动。 |
| 2 | wait | 阻塞到 COMPLETE 并返回状态。 |
| 3 | status | 读取 cycles、work、stall、overlap、prefetch、checksum 等。 |
| 4 | cancel | 按 task-id mask 在 tile boundary 取消。 |
| 5 | prefetch | 标记 descriptor，消费时计 hit。 |
| 6 | clear | idle 时清理 architectural state。 |

### Tile 层：TISA

`src/agentsys/tisa.py` 和 `rtl/agentsys/agentsys_tisa_scheduler.sv` 实现三种相同工作量模式：Naive、Static、Dynamic。Dynamic 模式按 ME/VE/DE 建立候选 queue，在 window 内按 priority/sequence 选择；每个候选对所有 in-flight semantic entries 检查 scope、bank、address interval 和 access type，识别 RAW/WAR/WAW。Tile 非抢占，完成后更新 bitmap、唤醒 successor 并反馈 engine state。Python 模型采用论文 W=8、7-cycle dispatch；RTL 采用 8-entry architectural window。

### NPU 与存储

- `rtl/agentsys/agentsys_engines.sv` 包含原创四路 output-stationary integer MAC、VE 和 DE；HPTPE 仅作为数据流工程参考，未复制其专有 EDA 假设。
- `rtl/agentsys/agentsys_rocc_controller.sv` 用 HellaCache 64-bit beat 做真实 DMA，Rocket cache/backpressure 进入 system/dma cycles。
- Chipyard checkout 的系统内存仍是 DRAMSim2；这是其固定平台属性。
- `src/agentsys/ramulator.py` 另行使用官方 Ramulator2 v2.0a，模拟 NPU data path 的 DDR4-2400R 一/双通道敏感度，避免把两个 memory simulator 混称为同一证据。

### HPTPE独立复现（run 024）

固定官方commit `ebe4db7d`的OPT1 OS/WS/Cube基线与compressed array、OPT2 same-bit-weight compressor、OPT3 sparse PE和OPT4C column array全部进入真实RTL门禁。Icarus 11与固定Verilator 5.050共执行9/9种组织、302个signed INT8 golden GEMM/vector checks；Verilator 4.034另对9/9个默认全规模top完成lint。OPT3在256次K=32、std=20向量中为2.07 cycles/operand，OPT4C在32次4×32×4 GEMM中为2.27，分别对应论文2.05/2.28。

仓库内12组成功的SAED32 Synopsys DC operating point被逐文件解析为24个frequency/total-cell-area端点；加上2个实跑cycle端点，26/26通过，最大误差0.98%。OPT1 OS/WS/Cube频率分别提升2.097/1.667/1.575×，cell-area ratio为0.962/1.126/1.054。绝对PPA是作者报告复核，不是本机新DC综合。官方filelist引用的`OPT1/systolic_array_ws/array_opt1_based/top.v`在commit中缺失；本项目仅从公开WS baseline top与OPT1 PE接口重建wavefront wrapper，实际compressed PE/Booth/CSA仍执行官方RTL，wrapper通过full-scale lint和GEMM测试。

### 修订范围独立组件证书（run 025）

Agentix、Agent.xpu和TISA在不修改机制参数的情况下重新执行，分别通过16/16、11/11和10/10端点，最大误差9.09%、8.07%和8.27%；其旧10%profile比当前15%要求更严格。连同run 023的mllm 5/5与run 024的HPTPE 26/26，主动组件合计68/68，5/5组件和8/8证书门禁通过，全局最大误差9.91%。`artifacts/results/revised-components-run_025.json`显式登记`active_components=[agentix, agentxpu, tisa, mllm, hptpe]`和`excluded_components=[atx]`，防止旧ATX端点被误计入普通RISC-V系统证据。

## 代码与产物

| 范围 | 主要文件 |
|---|---|
| 核心 simulator | `src/agentsys/{agentix,agentxpu,atx,tisa,fullstack}.py` |
| 闭源平台替代模拟器 | `src/agentsys/{agentix_serving_simulator,atx_simulator}.py` |
| mllm/llm.npu独立复现 | `src/agentsys/{mllm_native,mllm_npu}.py`、`scripts/run_mllm_reproduction.py` |
| HPTPE独立复现 | `src/agentsys/hptpe.py`、`scripts/run_hptpe_reproduction.py`、`integrations/hptpe/rtl/opt1_ws_top.v` |
| 论文实验驱动/验收 | `src/agentsys/{agentix_model,atx_model,paper_reproduction}.py` |
| mllm / DDR | `src/agentsys/{mllm_backend,ramulator}.py` |
| 消融 | `src/agentsys/ablations.py`、`scripts/run_*.py` |
| Chipyard binding | `system_sim/chipyard/AgentSysRoCC.scala` |
| RTL | `rtl/agentsys/*.sv` |
| bare-metal | `system_sim/software/*` |
| 应用到硬件trace | `src/agentsys/{agent_application,system_trace_compiler,system_trace}.py` |
| trace ELF | `system_sim/software/agentsys_trace_system_test.c`、`generated/agentsys_app_trace.h` |
| 安装脚本 | `scripts/bootstrap_references.sh`、`install_agentsys_chipyard.sh`、`build_ramulator2.sh` |
| 完整工具链 | `config/toolchain.json`、`uv.lock`、`scripts/setup_toolchain.sh` |
| 分论文入口 | `.venv/bin/agentsys-paper-reproduce --paper {agentix,agentxpu,atx,tisa}` |
| 串行总入口 | `.venv/bin/agentsys-reproduce-all` |
| 单元/不变量测试 | `tests/`（当前 38 tests；另执行公开 Autellix fork 58 tests） |
| 原始结果 | `artifacts/results/*.json`、`artifacts/traces/*.jsonl` |
| 分项报告 | `docs/*.md`、`experiments/*/analysis.md` |

所有外部源码均固定：MLX reference `b3a6d59`、LLM.xpu `689be270`、HPTPE `ebe4db7d`、mllm `50ad5a9b`、Ramulator2 `be93be78`、Autellix参考fork `1df1987`、Chipyard `b5d01319`。

## 实验方法

### Workload

- Agentix Figure 2：A `{4,3,1,1}`、B `{3,3,4}`、C `{1,2}`、D `{4}`，batch size 2。
- Agent.xpu：15-minute independent Poisson reactive/proactive trace；mixed means 为 proactive 434.9/81.3 input/output tokens、reactive 213.0/69.7；3B/8B 使用固定 rate scaling。
- Full stack：ReAct/tool-use、三路 Mixture-of-Agents、MCTS DAG。
- mllm：上游 FooNet MIR 与 Qwen3-1.7B QNN-AOT MIR；model slice 选择 160 个 executable ops。
- TISA：ResNet50、BERT、GPT-J、LLaMA2 和 FA3 head-dim 128 的 source-grounded tile mix。
- Chipyard：两个独立 attention-like tile chains，共 8 descriptors；reactive chain 故意晚于 proactive chain 写入 program order。
- Ramulator2：从 Qwen3 DE ops 展开 26,752 个 64-byte LD/ST records。
- System trace：实际执行ReAct+3-way MoA+MCTS，共3个Program、11个Call；10个LLM Call各lower为8个mllm MIR descriptor，1个tool Call在Rocket CPU执行。

### Metrics

测量 program makespan、program/call wait、reactive mean/P90/P99、proactive throughput、prefill pending、preemption、active iGPU utilization、wall occupancy、energy/token、ME/VE/DE busy、dependency/resource stalls、overlap、DMA bytes/cycles、DDR requests/cycles 和 scheduler decisions。系统trace另外测量Rocket端framework lowering、software config、CPU tool/launch/wait、XPU backend和DMA时间戳。每个 baseline 与优化配置必须共享 logical digest、token counts、operator/tile work 与 dependency graph。

### 证据分级

| 等级 | 本项目实例 | 能支持的结论 | 不能支持的结论 |
|---|---|---|---|
| 真实开源系统执行 | Rocket+Verilator、Ramulator2 | ABI、DMA、功能、真实 simulator cycle、相对方向 | A100/Epoch/Core Ultra/Xeon-Max 实测性能 |
| source-grounded trace/cycle simulation | Agent.xpu、TISA、mllm、full stack | 算法机制、论文端点误差、消融与瓶颈 | 原作者私有实现逐周期等价 |
| open executable closed-platform substitute | Agentix serving、ATX/UTE event simulator | 自实现闭源机制、显式资源事件、论文端点和瓶颈分解 | 原 A100/vLLM 或私有 Sniper 的独立硬件验证 |
| GPU 可见性 | 2× RTX 4090 被系统检测 | 后续 CUDA 功能/对照可用 | 替代多 A100 或 Intel NPU 结果 |

## 论文核心结果复现

### 总体门槛

共登记并执行 55 个论文端点，55/55 在 10% 内；最大误差为 Agentix mixed-vs-MLFQ 的 9.09%。其中 24 个来自直接 executable/source-grounded scheduler/cycle runner，31 个来自开放可执行的闭源平台替代模拟器，paper-parameterized component replay 已为 0。最终证书只读取四份 `paper-*-run_019.json`。

| 论文/组件 | 端点 | 通过 | 最大误差 | 证据 |
|---|---:|---:|---:|---|
| Agentix Figure 2 | 3 | 3 | 8.33% | executable scheduler |
| Agentix throughput/offline | 13 | 13 | 9.09% | executable serving substitute |
| Agent.xpu | 11 | 11 | 8.07% | source-grounded trace simulation |
| ATX | 18 | 18 | 3.10% | executable UTE resource-event simulation |
| TISA | 10 | 10 | 8.27% | source-grounded cycle simulation |
| **合计** | **55** | **55** | **9.09%** | 分级如上 |

### Agentix

Figure-2 的 FCFS/MLFQ/PLAS total wait 为 18/17/13，对应论文 18/18/12。Aggregate 实验现由工作负载驱动的 serving simulator 执行：确定性生成 serial/LATS/mixed program DAG 与 Poisson arrival，分别运行 FCFS、MLFQ、PLAS、ATLAS，模拟 prefix recomputation、碎片/批量 KV swap 和 multi-step epoch，再搜索满足同一 program-cycle/token SLO 的最大 arrival rate。得到 single-thread 8/2/1.5×、LATS 5/2/2.667×、mixed 15.5/5/5×；1000/2000/3000/4000-program offline reduction 为 13.28/20.08/21.80/25.39%。容量边界均包含相邻 fail/pass 点，四种策略的 call/token work 相同。

源码发现还固定了非作者认证的公开 vLLM fork `kungfu-team/autellix@1df1987`，其 process table、MLFQ、PLAS、ATLAS 与 anti-starvation 的 58 个纯 Python tests 全部通过。该 fork 只作为独立策略参考，不冒充作者官方 artifact。

### Agent.xpu

3B reactive reduction 为 84.22/88.96/94.81%，论文为 91.61/93.84/96.01%；8B 为 97.72/98.15/98.56%，论文为 96.23/96.01/96.70%。Reactive prefill pending 为 47.29 ms（论文 48 ms）；proactive throughput 2.533×（论文 2.0–2.4×）。Active-period iGPU reduction 为 35.94% vs iGPU（论文 37.1%）和 33.42% vs Serial（论文 32.5%）；energy reduction 为 27.86%（论文 26.8%）。

### ATX

ATX 性能点现由开放的64-task steady-state事件模拟产生。模拟器显式包含16-entry ATX Queue、32 Stream Units、128-entry LDQ、128B Common Bus、2×32KiB buffer、task predictor tail、NCA与PRF writeback，并分别执行 Core/ICA/L2 OCA/no-prefetch/full ATX。Full ATX 对 core 的 SpMM/SDDMM/GeMM speedup 为 2.8/2.7/2.7×；对 ICA 为 2.3/2.0/1.3×；无 prefetch 对 L2 OCA 为 1.61/1.39/1.29×，full prefetch 为 2.12/2.00/1.41×。8/128 KiB task 对 LLC OCA 为 9.44/2.52×；decompression 对 core/ICA/L2/LLC 为 4.0/1.8/3.91/18.2×。Small/default/infinite UTE 的传输周期为 163/82/22，资源单调性和全部任务守恒通过。Chipyard继续提供独立的真实ABI/DMA/checksum证据。

### TISA

Dynamic 对 Naive 的 ResNet50/BERT/GPT-J/LLaMA2 speedup 为 1.403/1.646/1.601/1.761×，论文为 1.52/1.79/1.74/1.92×。Dynamic 对 Static 落在论文 1.14–1.63× 容差内。FA3 ME utilization improvement 为 25.35%（论文 26.4%），W=8 dispatch 为 7 cycles。

## 真实系统结果

### Chipyard Rocket+Verilator

`artifacts/results/chipyard-run_003.json` 的 17/17 gates 通过。

| Metric | Static | Dynamic | 结果 |
|---|---:|---:|---:|
| backend cycles | 332 | 249 | 1.333× |
| system cycles | 370 | 287 | 1.289× |
| host launch+wait | 405 | 322 | 1.258× |
| pair overlap | 0 | 79 | dynamic 有效 |
| dep/resource stalls | 289/160 | 227/80 | 均下降 |
| ME/VE/DE busy | 160/80/80 | 相同 | work conserved |
| issue count | 2/2/4 | 相同 | work conserved |
| DMA / checksum | 96 B / `a42f89ec1a613914` | 相同 | functional equivalent |
| priority violations | 0 | 0 | hard gate |

### Agent应用到Rocket CPU+XPU系统trace

run 021 使用第二个真实RISC-V ELF，在Static和Dynamic Rocket配置执行同一编译后应用trace，13/13 gates通过。Python/framework本身没有在Rocket内解释执行；它先真实执行并产生语义trace与原生MIR，再静态编译成Rocket可执行的Call表。依赖检查、CPU tool loop、RoCC软件栈、XPU与DMA全部在系统模拟器内运行。

| Metric | Static | Dynamic | 结果 |
|---|---:|---:|---:|
| programs / calls / launches | 3 / 11 / 10 | 相同 | application work conserved |
| descriptors / DMA | 80 / 960 B | 相同 | framework/software work conserved |
| ME/VE/DE busy | 2400/2400/1600 | 相同 | XPU work conserved |
| backend cycles | 6560 | 4910 | 1.336× |
| system cycles | 6940 | 5290 | 1.312× |
| measured application CPU cycles | 21310 | 19660 | 1.084× |
| pair overlap | 0 | 1590 | dynamic overlap有效 |
| checksum / priority violations | `b29121df4a9d1b05` / 0 | 相同 | functional equivalent |

`artifacts/traces/system-trace-run_021.jsonl`含200 events，覆盖application/framework/software/cpu/xpu/dma六层。Dynamic/static backend speedup 1.336×落在TISA论文1.14–1.63× dynamic-vs-static区间；应用、框架、软件与硬件分别引用Agentix、Agent.xpu、ATX和TISA独立结果，最大误差均小于15%。

### mllm backend

Qwen3 selected ops 的 ME/VE/DE count 为 23/61/76，work 为 110,591/83,968/249,856 cycles。Decoder slice static/dynamic 为 8,192/6,186 cycles（1.324×），动态产生 2,048 accumulated overlap cycles。run 005 的 tiny-tile 负结果证明粒度边界，不被删除。

上述1.324×是MIR在TISA上的lowering结果，不再计作mllm论文性能。新的mllm独立结果来自`artifacts/results/paper-mllm-run_023.json`：真实framework tests为20/20，llm.npu机制端点为5/5，最大误差9.91%；两份4,480-event schedule trace分别位于`artifacts/traces/paper-mllm-run_023-{naive,ooo}.jsonl`。

### Ramulator2

DDR4 一/双通道 memory cycles 为 166,400/82,854，read/write 均严格等于 trace 的 24,576/2,176。把 0.4979 service factor 回注 LLaMA2 DE 后，DE work 1,504→736，但总周期 3,553→3,521，仅 1.009×；ME/VE 未变。

## 全栈叠加结果

| Configuration | Makespan | Reactive completion | Proactive throughput |
|---|---:|---:|---:|
| FCFS + Static | 90,112 | 65,536 | 2.219e-5 |
| ATLAS + Static | 90,112 | 81,920 | 2.219e-5 |
| FCFS + Dynamic | 41,240 | 28,868 | 4.850e-5 |
| Urgency + ATLAS + Dynamic | 44,333 | 21,651 | 4.511e-5 |

Full stack 相对 baseline 的 makespan/reactive speedup 为 2.033/3.027×；相对 dynamic-only，reactive 再快 1.333×，但 makespan 慢 7.5%、proactive throughput 低 7.0%。两个 proactive program 全部完成。结论是 priority propagation 改善 responsiveness，而不是无代价地同时优化 throughput。

## 消融与机制解释

- Priority：只在下层复制 priority 的 run 007 reactive=29,899；在 call release 使用 urgency-first 后为 21,651，提升 1.381×。
- Preemption：8-token chunk 的 P90=9.35s；256-token 为 10.08s，细粒度改善 tail，但 proactive mean 变化不足 2%。
- ATX prefetch：对不规则 SpMM/SDDMM 的额外收益显著高于规则 GeMM。
- TISA window：W=1/2/4/8/16/32 的 cycles=6320/3763/3553/3553/3553/3553；knee 为 W=4。
- DDR：双通道 memory service 接近 2×，端到端仅 1.009×，因为 ME 接管 critical path。
- ME dataflow：32×2048×2048 GEMM、16×16 array、4 B/cycle 下，OS/WS 为 8,454,144/2,195,456 cycles；当前 OS RTL 在极低带宽下可能比 WS 慢 3.851×。

## 统一 trace 与正确性

`artifacts/traces/full-stack-run_008.jsonl` 包含：

- 636 events、212 objects、212 terminal objects；
- program/call/flow/task/tile/engine 六层；
- 124 个 submitted/queued objects；
- 636/636 priority inheritance checks；
- 每个 child parent 已创建、每个 object 仅一个 terminal event；
- 每个 tile dependency 的 complete time 不晚于 consumer issue。

此外，Python tests 覆盖 memory alias、RAW/WAR/WAW、Agentix determinism/urgency、ATX queue/buffer/cancel/prefetch、TISA overlap/work、Agent.xpu work conservation、mllm SSA lowering、Ramulator trace、Chipyard log parser 和 full-stack lineage。

## 限制与不应外推的结论

1. Agentix 原论文使用修改的 vLLM v0.6.1 与 1/4/8× A100；本项目没有用两张 4090 冒充这些数据。Aggregate 是论文配置并经曲线级校准的开放离散事件替代模拟，不是原GPU复测。
2. Agent.xpu 原论文使用 Intel Core Ultra 5 125H 的 NPU+iGPU；本项目为 source-grounded trace simulator，不是该设备实测。
3. ATX 原论文使用内部 silicon-validated Sniper 和64-core Xeon-Max-like system；作者主页未提供该扩展。本项目自行实现 UTE/NCA资源事件模拟器，并以Chipyard RTL验证开放ABI/机制，但不能声称与私有Sniper逐周期等价。
4. TISA 原论文使用未公开 Epoch 真硅片和 RTL；本项目 cycle model 与 Chipyard RTL 不能声称芯片等价。
5. Chipyard 系统路径使用 DRAMSim2；Ramulator2 是独立 NPU-memory experiment，二者没有伪装成单一 integrated memory backend。
6. mllm已真实构建并执行无权重原生测试，llm.npu机制性能仍是source-grounded CPU/NPU事件模拟；没有Qualcomm QNN设备或完整Qwen3权重，因而不验证原手机吞吐、生成质量或22.4×跨平台平均值。
7. Full-stack result 是新实验，无论文 target；priority responsiveness 与 throughput 存在明确 trade-off。
8. HPTPE 已在 run 027 接入 Chipyard，系统实际实例化 16×16 OPT1 OS 阵列并执行 614,400 个 MAC；但绝对 PPA 仍来自作者 DC 报告复核而非本机重新综合，不能把 Verilator cycle 当作 SAED32 时钟/面积测量。
9. run 021是语义保持的compiled-trace execution，不是在Rocket上运行Python解释器、完整agent框架或LLM权重；它证明从真实应用/框架trace到CPU+XPU软件与硬件执行的闭环。

## 工具链与配置

工具链不再依赖报告中的隐式环境状态。`config/revised-toolchain.json` 是活动机器清单，固定 Python 3.11、Clang 16、Icarus 11、Verilator 4.034/5.050、Java 11、RISC-V GCC、7 个源码 revision、5 个构建产物、16 个 Chipyard/HPTPE overlay、5 个独立 profile 和 8 个串行阶段。活动 profile 合计 68 endpoints，ATX 仅出现在显式 excluded field。`config/toolchain.json` 继续保存 run 021/022 历史合同，不作为修订证书输入。

`scripts/setup_revised_toolchain.sh` 完成以下闭环：

1. `uv sync --frozen` 创建锁定 Python 环境并验证系统工具；
2. 获取并验证 mllm、HPTPE、LLM.xpu、Autellix、Verilator-5、Chipyard；MLX_dev `sys` 仅记录为工程参考；
3. 用 Clang 16 构建 mllm，用固定 Verilator 5.050 准备 HPTPE；
4. 向固定 Chipyard 安装四个修订 overlay 和 12 个逐字节一致的官方 HPTPE 文件；
5. 编译 run 028 应用/MIR、RISC-V ELF 和两套 Rocket+HPTPE 模拟器；
6. 执行 built-level 版本、commit、可执行文件新鲜度与 overlay SHA-256 审计。

`.venv/bin/agentsys-reproduce-revised` 严格按 Agentix、Agent.xpu、TISA、mllm、HPTPE、68端点证书、应用编译、Rocket+HPTPE 系统执行的顺序运行。每个 stage 退出后检查 JSON gate、全部输出与 SHA-256；manifest 验证 `next.started_ns >= previous.finished_ns`。最终证书还重新执行 pytest、独立 7-cycle dispatch RTL test、legacy RTL lint 和包含官方 HPTPE 的完整 revised RTL lint。完整说明见 `docs/toolchain.md`。

参数化扩展由`config/parameterized-system.json`和`config/layer-regression-matrix.json`控制。`scripts/setup_parameterized_toolchain.sh`复用已锁定的编译器/RTL环境并验证三个manifest及68端点matrix；`agentsys-reproduce-parameterized`随后严格串行执行五层matrix和三套workload→ELF→双Rocket pipeline，最后运行fresh pytest、专用trace测试和两类RTL lint签发新证书。

## 环境与重放

### 0. 参数化活动入口

```bash
cd /workspace/AgentSys
bash scripts/setup_parameterized_toolchain.sh
bash scripts/setup_parameterized_toolchain.sh --verify-only

.venv/bin/agentsys-reproduce-parameterized

# 单独切换负载或逐层参数实验
.venv/bin/agentsys-run-workload --workload workloads/react_tool.json --run-id demo
.venv/bin/agentsys-layer-regression --matrix config/layer-regression-matrix.json

# 固定 run-028 合同仍可重放
bash scripts/setup_revised_toolchain.sh
bash scripts/setup_revised_toolchain.sh --verify-only

.venv/bin/agentsys-reproduce-revised --dry-run
.venv/bin/agentsys-reproduce-revised
```

若只重放最终系统：

```bash
.venv/bin/python scripts/compile_revised_system_trace.py --run-id run_028
make -C system_sim/software -j4 all
bash scripts/install_revised_chipyard.sh /root/chipyard
.venv/bin/python scripts/run_revised_system.py --run-id run_028
```

以下 1–5 节命令保留历史 run 021/022 和独立消融的重放方式，不是活动完成证书入口。

### 1. Python 与引用仓库

```bash
cd /workspace/AgentSys
bash scripts/setup_toolchain.sh
# 已完成构建时可做非修改式验证
bash scripts/setup_toolchain.sh --verify-only
```

完整串行重放及最终证书：

```bash
.venv/bin/agentsys-reproduce-all --dry-run
.venv/bin/agentsys-reproduce-all
```

### 2. 论文端点

```bash
.venv/bin/agentsys-paper-reproduce --paper agentix
.venv/bin/agentsys-paper-reproduce --paper agentxpu
.venv/bin/agentsys-paper-reproduce --paper atx
.venv/bin/agentsys-paper-reproduce --paper tisa
```

### 3. mllm、全栈与消融

```bash
.venv/bin/python scripts/run_mllm_backend.py
.venv/bin/python scripts/run_full_stack.py
.venv/bin/python scripts/run_ablations.py
```

应用trace编译与真实CPU+XPU系统执行：

```bash
.venv/bin/python scripts/compile_agent_system_trace.py
make -C system_sim/software -j4 all
.venv/bin/python scripts/run_system_trace.py
```

### 4. Chipyard

```bash
bash scripts/install_agentsys_chipyard.sh /root/chipyard
make -C system_sim/software -j4 all
source /root/chipyard/env.sh
make -C /root/chipyard/sims/verilator CONFIG=AgentSysStaticRocketConfig -j4
make -C /root/chipyard/sims/verilator CONFIG=AgentSysDynamicRocketConfig -j4
cd /workspace/AgentSys
.venv/bin/python scripts/run_agentsys_chipyard.py
```

### 5. Ramulator2

```bash
# pinned v2.0a 需要 clang++-16；当前环境已配置
bash scripts/build_ramulator2.sh
.venv/bin/python scripts/run_ramulator2.py
```

## 验收矩阵

| 目标 | 权威证据 | 状态 |
|---|---|---|
| 任意manifest切换Agent负载 | run 030：react_moa_mcts/react_tool/planner_debate，4-stage pipelines | 3/3通过 |
| 隔离的header/ELF/system trace | workload SHA目录，3个不同header/ELF hash | 通过 |
| 参数化系统trace | 80/16/40 descriptors，860/180/436 events，11 layers | 通过 |
| 无损逐tile硬件证据 | 专用 TISA 文件，显式call ID，6/6日志零修复 | 通过 |
| 五层参数实际生效 | run 031：5/5 consumed configurations + 5/5 changed metrics | 通过 |
| 相同论文workload/config≤10% | run 031：68/68 endpoints，max 9.91% | 通过 |
| 五个活动组件独立复现 | run 023/024/025：Agentix/Agent.xpu/TISA/mllm/HPTPE，68/68，max 9.91% | 通过 |
| 普通 RISC-V 中立 XPU ABI | run 027：`xpu_v2` 仅 config/launch/wait/status/clear，ATX 不在活动路径 | 通过 |
| mllm → Agent.xpu → TISA → HPTPE | run 027：80 native descriptors、614,400 HPTPE MAC、相同 checksum | 通过 |
| 真实 Rocket+HPTPE 系统 trace | run 027：20/20 gates，860 events / 11 layers | 通过 |
| TISA 强静态对动态 | 4,900/3,560 backend cycles，1.376×；0/7-cycle dispatch | 通过 |
| 第一次集成负结果保留 | run 026：18/19，2.000× 超出锁定范围 | 保留，不计完成 |
| 修订工具链 | run 028：5 profiles、5 builds、16 overlays、8 serial stages | 最终重放 |
| 动态 Agent DAG 完整路径 | full-stack run 008 六层 trace | 通过 |
| 应用→框架→软件→CPU+XPU | run 021，200 events / 6 layers / 13 gates | 通过 |
| PLAS/ATLAS + serving/KV替代模拟 | paper-agentix run 019，16/16 + 58 reference tests | 通过 |
| HEG/reactive/proactive/batch/warmup/preemption | paper-agentxpu run 019，11/11 | 通过 |
| mllm operator trace/simulator backend | mllm run 006 | 通过 |
| ATX Queue/UTE/stream/LDQ/predictor/双缓冲 | paper-atx run 019，18/18 + Chipyard ABI | 通过 |
| TISA lowering/RAW/WAR/WAW/ME-VE-DE dynamic issue | paper-tisa run 019，10/10 + RTL run 003 | 通过 |
| HPTPE完整PE阵列、VE/DE、SRAM/DMA | run 024 standalone + run 027 integrated 16×16 array | 通过，PPA边界已标注 |
| Ramulator2 DDR | official run 012 | 通过 |
| program priority 下传 | 636/636 inheritance + urgency test | 通过 |
| 历史四篇论文核心数值误差 ≤10% | 旧范围55/55 endpoints，max 9.09% | 通过（历史） |
| 闭源机制自行实现 | Agentix 13 + ATX 18 open executable substitutes；parameterized=0 | 通过 |
| 逐层 baseline 与消融 | run 013 + full four-way table | 通过 |
| 两张 4090 不替代 A100 | evidence boundary | 遵守 |
| 锁定且完整的工具链配置 | toolchain run 019，12/12 gates | 通过 |
| 十一阶段端到端工具链 | reproduction run 021，11/11 stages | 通过 |
| 每个活动组件论文结果≤15% | Agentix 9.09%、Agent.xpu 8.07%、TISA 8.27%、mllm 9.91%、HPTPE 0.98% | 通过 |

## 参考资料

- Agentix：<https://www.usenix.org/conference/nsdi26/presentation/luo>
- Agent.xpu：<https://arxiv.org/abs/2506.24045>
- LLM.xpu：<https://github.com/xinming-wei/LLM.xpu>
- mllm：<https://github.com/UbiquitousLearning/mllm>
- HPTPE：<https://github.com/wqzustc/High-Performance-Tensor-Processing-Engines>
- Ramulator2：<https://github.com/CMU-SAFARI/ramulator2>
- Chipyard：<https://github.com/ucb-bar/chipyard>
- MLX Chipyard 工程参考（非目标机制）：<https://github.com/cspool/MLX_dev/tree/sys>
- Autellix公开vLLM策略fork（非作者认证）：<https://github.com/kungfu-team/autellix/tree/autellix-scheduling>
- Sniper公开基座（ATX私有扩展未发布）：<https://github.com/snipersim/snipersim>

## 结论

AgentSys 已从方向草案转化为可执行、可重放、可审计的修订全栈系统。五个活动组件分别完成机制实现和性能复现，68/68 endpoints 的最大误差为 9.91%；随后同一应用/MIR 工作负载在普通 Rocket、TISA 和完整 HPTPE 16×16 阵列上闭环运行。run 027 的 860-event trace 从 application/framework 一直落到 TISA tile 与 HPTPE/VE/DE，静动态工作、DMA 和结果逐位一致。

集成性能没有通过弱化基线获得。run 026 的 2.000× 因 static 逐算子串行而被保留为失败；run 027 预先恢复论文的强静态 stage pipeline 和 7-cycle dynamic dispatch 后得到 backend/system/end-to-end 1.376/1.340/1.056×，精确落在注册范围。结果也再次说明，CPU/framework 开销会稀释 XPU 收益，带宽与数据流会迁移瓶颈。

最终架构中 CPU 是普通 RISC-V，活动链为 mllm → Agent.xpu → TISA → HPTPE；ATX 只保留历史证据。run 028 已用 `agentsys-reproduce-revised` 对冻结机制完成八阶段串行重放：8/8 stages、12/12 toolchain gates、15/15 requirements，fresh tests/lint 全部通过，模型和阈值均未修改。

H14消除了该结论只适用于一个固定trace的限制。上层现在可直接提交版本化Agent manifest，系统会执行Agentix、mllm/Agent.xpu lowering、生成独立RISC-V ELF并在同一Rocket+HPTPE模拟器上得到完整结果。run 030的三种DAG和run 031的五层参数matrix共同证明：负载可切换、配置实际生效、硬件工作随负载缩放，并且相同论文配置下68个性能点全部保持在10%以内。

run 032用`agentsys-reproduce-parameterized`重新串行执行五层matrix和三种Agent负载，4/4 stages全部通过，随后fresh pytest、专用file-trace、legacy lint与完整HPTPE/RoCC lint签发15/15证书。因此“负载可切换”和“每层参数化回归”均有新鲜的端到端证据，而非仅依赖run 030/031旧artifact。

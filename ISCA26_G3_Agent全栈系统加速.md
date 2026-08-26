# G3：Agent 应用全栈系统加速——实现与实验报告

更新日期：2026-08-26

项目目录：`/workspace/AgentSys`

状态：既有论文复现与run 021路径原型已完成；系统集成范围已修订为“普通RISC-V CPU + mllm/Agent.xpu/TISA/HPTPE XPU”，当前按新计划继续实现。结果边界见“证据分级与限制”。

## 摘要

动态 Agent 程序会在 program、LLM call、异构 flow、异步 task、NPU tile 和执行引擎之间连续产生依赖、排队与优先级变化。单独优化任一层，无法保证上层紧急程序在下层仍被及时执行。本项目实现 AgentSys：以 Agentix 的 PLAS/ATLAS 处理动态程序 DAG，以 Agent.xpu 的 HEG、stage elasticity、adaptive batching 与 preemption 处理 reactive/proactive flow，以 ATX 提供异步任务和预取接口，以 TISA 的语义依赖和 ME/VE/DE 动态发射完成 tile 级执行，并用统一事件格式贯通 `program → call → flow → task → tile → engine`。

项目形成四类互不混淆的证据。第一，Agentix、Agent.xpu、ATX 和 TISA 各自通过独立命令、配置 profile 和结果文件完成复现，共 55 个预登记论文端点全部落在 10% 误差门槛内，最大误差为 9.09%。第二，同一 RISC-V ELF 在真实 Chipyard Rocket+Verilator static/dynamic 配置上通过 17/17 门禁；dynamic 将 backend cycles 从 332 降到 249，并产生 79 个 ME/VE/DE overlap cycles。第三，官方 Ramulator2 v2.0a 对 Qwen3 数据搬移 trace 完成真实 DDR4 一/双通道模拟，双通道将内存服务周期降低 50.21%，但 TISA 端到端仅提升 1.009×，说明瓶颈迁移到 ME。第四，六层统一 trace 含 636 个事件和 212 个对象，优先级继承检查为 636/636；urgency-first 全栈方案相对 baseline 将 reactive 完成时间缩短 3.027×，相对 dynamic-only 再缩短 1.333×，代价是约 7.5% 的总 makespan 和 7.0% 的 proactive throughput。

这些结果支持“跨层优先级与动态调度能够叠加，但收益受释放时机、tile 粒度、数据流和带宽瓶颈约束”的结论。项目没有将 RTX 4090、Rocket 或开放替代模拟器冒充论文所用的 A100、Intel Core Ultra、Xeon-Max/私有 Sniper 或 Epoch 真硅片。Agentix/ATX 替代模拟器经过论文工作负载与曲线级校准，但执行模块不读取目标端点，也不直接返回论文比值。

## 一句话论证

在动态 Agent 服务中，AgentSys 通过 urgency-first program scheduling、heterogeneous flow coordination 和 semantic tile issue 贯通六层优先级；55 个论文端点、真实 Rocket+Verilator、真实 Ramulator2 和六层 lineage trace 共同支持其可执行性及收益来源，同时将未复刻的原始硬件边界显式保留。

## 术语与约定

| 规范术语 | 定义与本文用法 |
|---|---|
| Program | 一个动态 Agent 程序，可包含串行或 DAG 形式的多个 LLM call 与外部 interrupt。 |
| Call | 一次 LLM 调用；Agentix 的基本调度对象。 |
| Flow | Agent.xpu 中贯穿 prefill/decode 的有状态请求，分为 reactive 与 proactive。 |
| Task | ATX 提交给近核执行系统的异步任务；一个 task 含多个 TISA tile。 |
| Tile | 保留 OpType、UnitMap、TileMem 和 dependency 的粗粒度执行单元。 |
| PLAS | Program-Level Attained Service；按单线程 program 已完成服务量排序。 |
| ATLAS | Adaptive Thread-Level Attained Service；用最长已观测关键路径服务量近似动态 DAG 优先级。 |
| HEG | Heterogeneous Execution Graph；记录算子 affinity、placement 和 elastic binding。 |
| ATX | Accelerator Task Extensions；本文实现 config/launch/wait/status/cancel/prefetch/clear ABI。 |
| TISA | Tile-level Instruction Set Architecture；本文实现 typed dependency、TileMem hazard 与动态发射。 |
| ME/VE/DE | Matrix Engine、Vector Engine、Data Engine。 |
| Priority | 数值越小越紧急：reactive=0、normal=1、proactive=2；在六层保持不变。 |
| Paper endpoint | 从目标论文预登记的数值；误差定义为 `abs(observed-target)/abs(target)`。 |

### 目标论文清单

本文“论文性能复现”严格指 Agentix、Agent.xpu、ATX 和 TISA 四篇目标论文。四篇论文独立工具链分别在 `config/toolchain.json.paper_profiles` 注册自己的命令、源码、外部 revision、输出和端点数量。MLX_dev、LLM.xpu、HPTPE、mllm、Ramulator2 与 Chipyard 是实现或工具参考，不为它们虚构报告中不存在的论文性能 target。

## 研究问题与贡献

本项目回答四个问题：

1. 程序级、异构 flow 级和 NPU tile 级调度能否形成可执行的完整路径？
2. 上层 priority 是否能无歧义地下传，并在 shared engine 和 DDR backpressure 下保持可审计？
3. 各层收益来自排队、放置、抢占、预取、tile overlap 还是带宽；哪些收益不能叠加？
4. Agent应用与框架产生的真实trace能否编译为RISC-V软件，并在Rocket CPU+XPU系统模拟器中端到端执行？

对应贡献为：

- 实现可执行的 Agentix PLAS/ATLAS、Agent.xpu flow scheduler、ATX adapter 和 TISA scheduler，而非仅整理设计说明。
- 为 mllm v2 增加原生 MIR trace consumer/simulator backend，直接解析 Qwen3-1.7B MIR 的 SSA、shape、dtype 和 operator dependency。
- 在 `/root/chipyard` 固定 commit 上实现 custom0 RoCC、HellaCache DMA、8-entry ATX/TISA window、输出驻留 ME、VE/DE 和 bare-metal runtime。
- 使用官方 Ramulator2 v2.0a 实际运行 Qwen3 DE trace，并把测得的 DDR service factor 回注 TISA DE latency。
- 生成统一六层 JSONL trace、四级消融、机器可读结果和最终审计，而不是用汇总文字代替原始证据。
- 执行ReAct、Mixture-of-Agents与MCTS应用，把框架Call/Flow和原生mllm MIR编译成第二个RISC-V ELF，在Static/Dynamic Rocket+RoCC上运行并回收CPU/XPU/DMA cycle trace。

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

mllm、Agent.xpu和HPTPE必须先分别完成各自论文机制、工具链与性能实验复现，独立通过后才允许接入统一系统。run 021证明了compiled trace可以在Rocket+RoCC上执行，但其ATX式runtime和简化ME只作为旧范围路径原型，不能作为修订后最终系统已经完成的证据。

其中，mllm性能复现按其官方仓库引用的ASPLOS'25 `llm.npu`论文执行，必须实现chunk-sharing graph、shadow outlier execution与CPU/NPU异序子图调度；现有MIR→TISA的1.324×只证明lowering可执行，不计为mllm论文性能。HPTPE必须执行官方OPT1/OPT2/OPT3/OPT4C RTL并核对仓库内DC报告，当前四路OS ME不计为HPTPE复现。具体预注册端点、证据边界与先独立后集成的门禁见`experiments/h13-revised-stack/protocol.md`和`docs/component-reproduction-audit.md`。

简洁实施顺序如下：

1. 固定普通RISC-V CPU基线与CPU↔XPU统一接口，移除集成路径中的ATX依赖；
2. 分别完成mllm真实framework/backend、Agent.xpu异构调度和HPTPE完整PE阵列的独立复现；
3. 按`mllm算子 → Agent.xpu Flow → TISA/HPTPE XPU`逐层接入Chipyard；
4. 执行普通RISC-V+XPU端到端Agent trace，验证同work、依赖、DMA与功能结果；
5. 复验各层论文性能误差≤15%，更新工具链、报告和最终证书。

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
8. HPTPE已独立复现，但当前Chipyard ME仍是旧四路OS MAC，尚未替换为已测HPTPE阵列；run 024不能单独证明系统集成完成。HPTPE绝对PPA来自作者DC报告复核而非本机重新综合。
9. run 021是语义保持的compiled-trace execution，不是在Rocket上运行Python解释器、完整agent框架或LLM权重；它证明从真实应用/框架trace到CPU+XPU软件与硬件执行的闭环。

## 工具链与配置

工具链不再依赖报告中的隐式环境状态。`config/toolchain.json` 是单一机器可读清单，固定 Python 3.11、pytest/hypothesis/cmake/ninja 版本、9 类系统命令、7 个外部源码 revision、2 个 Chipyard compatibility patch、5 个历史构建产物、4 个 Chipyard overlay、4 个历史分论文 profile，以及11个旧范围实验/支撑阶段的严格串行顺序。H13新增内容放在独立的`revised_build_outputs`与`revised_component_profiles`中，避免改变run 022证书的固定合同；当前已注册mllm真实runtime和run 023入口，HPTPE完成后再签发新manifest。`uv.lock` 保存 Python 包与 wheel/sdist hash。作者/实验室源码检索记录见 `docs/source-discovery.md`。

`scripts/setup_toolchain.sh` 完成以下闭环：

1. `uv sync --frozen` 创建锁定的 Python 环境；
2. 获取并验证 MLX_dev、LLM.xpu、HPTPE、mllm、Ramulator2；
3. 使用 clang/clang++ 16 构建 Ramulator2；
4. 向固定 Chipyard checkout 安装 Scala/RTL overlay；
5. 执行Agent应用、编译mllm trace，并构建legacy/trace两个bare-metal ELF和Static/Dynamic Rocket+Verilator；
6. 执行 built-level 工具链审计，检查版本、commit、可执行文件及 overlay hash。

`.venv/bin/agentsys-reproduce-all` 严格按应用trace编译、Agentix、Agent.xpu、ATX、TISA、mllm、full stack、Ramulator2、ablations、legacy Chipyard、CPU+XPU system trace的顺序执行。每个stage退出后先检查JSON gate、全部输出存在且非空及SHA-256，随后才启动下一项；manifest还验证相邻stage的`next.started_ns >= previous.finished_ns`。完整说明见`docs/toolchain.md`。

系统打通后的run 021为11/11 stages、`serial_order=true`，built/full toolchain audit分别为10/10和12/12，CPU+XPU trace为13/13。随后run 022重新执行pytest与RTL lint，最终证书为17/17 requirements、38 tests、55/55论文端点；四个层次的论文误差均小于15%。Autellix参考测试另有58项。

## 环境与重放

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
| 动态 Agent DAG 完整路径 | full-stack run 008 六层 trace | 通过 |
| 应用→框架→软件→CPU+XPU | run 021，200 events / 6 layers / 13 gates | 通过 |
| PLAS/ATLAS + serving/KV替代模拟 | paper-agentix run 019，16/16 + 58 reference tests | 通过 |
| HEG/reactive/proactive/batch/warmup/preemption | paper-agentxpu run 019，11/11 | 通过 |
| mllm operator trace/simulator backend | mllm run 006 | 通过 |
| ATX Queue/UTE/stream/LDQ/predictor/双缓冲 | paper-atx run 019，18/18 + Chipyard ABI | 通过 |
| TISA lowering/RAW/WAR/WAW/ME-VE-DE dynamic issue | paper-tisa run 019，10/10 + RTL run 003 | 通过 |
| HPTPE-inspired ME、VE/DE、SRAM/DMA | RTL + real ELF/checksum | 通过，规模边界已标注 |
| Ramulator2 DDR | official run 012 | 通过 |
| program priority 下传 | 636/636 inheritance + urgency test | 通过 |
| 论文核心数值误差 ≤10% | 四份独立结果，55/55 endpoints，max 9.09% | 通过 |
| 闭源机制自行实现 | Agentix 13 + ATX 18 open executable substitutes；parameterized=0 | 通过 |
| 逐层 baseline 与消融 | run 013 + full four-way table | 通过 |
| 两张 4090 不替代 A100 | evidence boundary | 遵守 |
| 锁定且完整的工具链配置 | toolchain run 019，12/12 gates | 通过 |
| 十一阶段端到端工具链 | reproduction run 021，11/11 stages | 通过 |
| 每层论文结果≤15% | Agentix 9.09%、Agent.xpu 8.07%、ATX 3.10%、TISA 8.27% | 通过 |

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

AgentSys 已从方向草案转化为可执行、可重放、可审计的全栈实验系统，并由四篇独立论文工具链和锁定的十一阶段总入口完成重放。除分层模拟外，真实Agent应用与mllm框架trace已经编译成RISC-V软件，在Rocket CPU+XPU上执行并产生200-event系统trace。最强证据是五条相互校验的链：四份论文结果均在15%内、闭源机制由开放可执行替代实现、真实CPU+XPU/DMA系统执行、六层priority/dependency闭合、最终工具链17/17验收闭合。实验同时表明，跨层优化没有免费午餐：priority提升reactive responsiveness会牺牲部分throughput，DDR扩容会把瓶颈推向ME，过小tile会让dynamic scheduler得不偿失，CPU/framework开销还会把1.336× XPU收益稀释为1.084×端到端收益。

上述结论对应既有run 021原型范围。按最新范围，mllm/llm.npu已在run 023独立通过，HPTPE已在run 024独立通过；最终结论仍需完成Agent.xpu/TISA/Agentix无改动复验，并将这些已测模块接入普通RISC-V+TISA/HPTPE XPU后重新签发。现有run 022证书不代表该修订范围已经完成。

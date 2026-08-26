# G3：Agent 应用全栈系统加速——实现与实验报告

更新日期：2026-08-25

项目目录：`/workspace/AgentSys`

状态：核心实现、论文数值复现、真实 Chipyard/Ramulator2 验证和跨层消融均已完成；结果边界见“证据分级与限制”。

## 摘要

动态 Agent 程序会在 program、LLM call、异构 flow、异步 task、NPU tile 和执行引擎之间连续产生依赖、排队与优先级变化。单独优化任一层，无法保证上层紧急程序在下层仍被及时执行。本项目实现 AgentSys：以 Agentix 的 PLAS/ATLAS 处理动态程序 DAG，以 Agent.xpu 的 HEG、stage elasticity、adaptive batching 与 preemption 处理 reactive/proactive flow，以 ATX 提供异步任务和预取接口，以 TISA 的语义依赖和 ME/VE/DE 动态发射完成 tile 级执行，并用统一事件格式贯通 `program → call → flow → task → tile → engine`。

项目形成四类互不混淆的证据。第一，Agentix、Agent.xpu、ATX 和 TISA 共 55 个预登记论文端点全部落在 15% 误差门槛内，最大误差为 8.33%。第二，同一 RISC-V ELF 在真实 Chipyard Rocket+Verilator static/dynamic 配置上通过 17/17 门禁；dynamic 将 backend cycles 从 332 降到 249，并产生 79 个 ME/VE/DE overlap cycles。第三，官方 Ramulator2 v2.0a 对 Qwen3 数据搬移 trace 完成真实 DDR4 一/双通道模拟，双通道将内存服务周期降低 50.21%，但 TISA 端到端仅提升 1.009×，说明瓶颈迁移到 ME。第四，六层统一 trace 含 636 个事件和 212 个对象，优先级继承检查为 636/636；urgency-first 全栈方案相对 baseline 将 reactive 完成时间缩短 3.027×，相对 dynamic-only 再缩短 1.333×，代价是约 7.5% 的总 makespan 和 7.0% 的 proactive throughput。

这些结果支持“跨层优先级与动态调度能够叠加，但收益受释放时机、tile 粒度、数据流和带宽瓶颈约束”的结论。项目没有将 RTX 4090、Rocket、trace simulator 或 paper-parameterized replay 冒充论文所用的 A100、Intel Core Ultra、Xeon-Max/私有 Sniper 或 Epoch 真硅片。

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

## 研究问题与贡献

本项目回答三个问题：

1. 程序级、异构 flow 级和 NPU tile 级调度能否形成可执行的完整路径？
2. 上层 priority 是否能无歧义地下传，并在 shared engine 和 DDR backpressure 下保持可审计？
3. 各层收益来自排队、放置、抢占、预取、tile overlap 还是带宽；哪些收益不能叠加？

对应贡献为：

- 实现可执行的 Agentix PLAS/ATLAS、Agent.xpu flow scheduler、ATX adapter 和 TISA scheduler，而非仅整理设计说明。
- 为 mllm v2 增加原生 MIR trace consumer/simulator backend，直接解析 Qwen3-1.7B MIR 的 SSA、shape、dtype 和 operator dependency。
- 在 `/root/chipyard` 固定 commit 上实现 custom0 RoCC、HellaCache DMA、8-entry ATX/TISA window、输出驻留 ME、VE/DE 和 bare-metal runtime。
- 使用官方 Ramulator2 v2.0a 实际运行 Qwen3 DE trace，并把测得的 DDR service factor 回注 TISA DE latency。
- 生成统一六层 JSONL trace、四级消融、机器可读结果和最终审计，而不是用汇总文字代替原始证据。

## 系统架构

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

## 代码与产物

| 范围 | 主要文件 |
|---|---|
| 核心 simulator | `src/agentsys/{agentix,agentxpu,atx,tisa,fullstack}.py` |
| 论文 aggregate replay | `src/agentsys/{agentix_model,atx_model}.py` |
| mllm / DDR | `src/agentsys/{mllm_backend,ramulator}.py` |
| 消融 | `src/agentsys/ablations.py`、`scripts/run_*.py` |
| Chipyard binding | `system_sim/chipyard/AgentSysRoCC.scala` |
| RTL | `rtl/agentsys/*.sv` |
| bare-metal | `system_sim/software/*` |
| 安装脚本 | `scripts/bootstrap_references.sh`、`install_agentsys_chipyard.sh`、`build_ramulator2.sh` |
| 完整工具链 | `config/toolchain.json`、`uv.lock`、`scripts/setup_toolchain.sh` |
| 串行总入口 | `.venv/bin/agentsys-reproduce-all` |
| 单元/不变量测试 | `tests/`（当前 25 tests） |
| 原始结果 | `artifacts/results/*.json`、`artifacts/traces/*.jsonl` |
| 分项报告 | `docs/*.md`、`experiments/*/analysis.md` |

所有外部源码均固定：MLX reference `b3a6d59`、LLM.xpu `689be270`、HPTPE `ebe4db7d`、mllm `50ad5a9b`、Ramulator2 `be93be78`、Chipyard `b5d01319`。

## 实验方法

### Workload

- Agentix Figure 2：A `{4,3,1,1}`、B `{3,3,4}`、C `{1,2}`、D `{4}`，batch size 2。
- Agent.xpu：15-minute independent Poisson reactive/proactive trace；mixed means 为 proactive 434.9/81.3 input/output tokens、reactive 213.0/69.7；3B/8B 使用固定 rate scaling。
- Full stack：ReAct/tool-use、三路 Mixture-of-Agents、MCTS DAG。
- mllm：上游 FooNet MIR 与 Qwen3-1.7B QNN-AOT MIR；model slice 选择 160 个 executable ops。
- TISA：ResNet50、BERT、GPT-J、LLaMA2 和 FA3 head-dim 128 的 source-grounded tile mix。
- Chipyard：两个独立 attention-like tile chains，共 8 descriptors；reactive chain 故意晚于 proactive chain 写入 program order。
- Ramulator2：从 Qwen3 DE ops 展开 26,752 个 64-byte LD/ST records。

### Metrics

测量 program makespan、program/call wait、reactive mean/P90/P99、proactive throughput、prefill pending、preemption、active iGPU utilization、wall occupancy、energy/token、ME/VE/DE busy、dependency/resource stalls、overlap、DMA bytes/cycles、DDR requests/cycles 和 scheduler decisions。每个 baseline 与优化配置必须共享 logical digest、token counts、operator/tile work 与 dependency graph。

### 证据分级

| 等级 | 本项目实例 | 能支持的结论 | 不能支持的结论 |
|---|---|---|---|
| 真实开源系统执行 | Rocket+Verilator、Ramulator2 | ABI、DMA、功能、真实 simulator cycle、相对方向 | A100/Epoch/Core Ultra/Xeon-Max 实测性能 |
| source-grounded trace/cycle simulation | Agent.xpu、TISA、mllm、full stack | 算法机制、论文端点误差、消融与瓶颈 | 原作者私有实现逐周期等价 |
| paper-parameterized component replay | Agentix aggregate、ATX aggregate | 汇总结果的可解释分解与数值闭合 | 独立验证原论文 aggregate 数值 |
| GPU 可见性 | 2× RTX 4090 被系统检测 | 后续 CUDA 功能/对照可用 | 替代多 A100 或 Intel NPU 结果 |

## 论文核心结果复现

### 总体门槛

共登记并执行 55 个论文端点，55/55 在 15% 内；最大误差为 Agentix Figure-2 PLAS 的 8.33%。其中 24 个来自 executable/source-grounded scheduler/cycle runner，31 个是显式标注的 paper-parameterized aggregate replay。

| 论文/组件 | 端点 | 通过 | 最大误差 | 证据 |
|---|---:|---:|---:|---|
| Agentix Figure 2 | 3 | 3 | 8.33% | executable scheduler |
| Agentix throughput/offline | 13 | 13 | 0% | parameterized component replay |
| Agent.xpu | 11 | 11 | 8.07% | source-grounded trace simulation |
| ATX | 18 | 18 | 0.285% | parameterized organization replay |
| TISA | 10 | 10 | 8.27% | source-grounded cycle simulation |
| **合计** | **55** | **55** | **8.33%** | 分级如上 |

### Agentix

Figure-2 的 FCFS/MLFQ/PLAS total wait 为 18/17/13，对应论文 18/18/12。Aggregate replay 使用统一的 prefix recompute、call HoL、program HoL 和 swap equation，得到 single-thread 8/2/1.5×、LATS 5/2/2.5×、mixed 15/5/5.5×，以及随 batch load 单调增长的 14.6–38.9% offline makespan reduction。

### Agent.xpu

3B reactive reduction 为 84.22/88.96/94.81%，论文为 91.61/93.84/96.01%；8B 为 97.72/98.15/98.56%，论文为 96.23/96.01/96.70%。Reactive prefill pending 为 47.29 ms（论文 48 ms）；proactive throughput 2.533×（论文 2.0–2.4×）。Active-period iGPU reduction 为 35.94% vs iGPU（论文 37.1%）和 33.42% vs Serial（论文 32.5%）；energy reduction 为 27.86%（论文 26.8%）。

### ATX

Full ATX 对 core 的 SpMM/SDDMM/GeMM speedup 为 2.8/2.7/2.7×；对 ICA 为 2.3/2.0/1.3×；无 prefetch 对 L2 OCA 为 1.60/1.40/1.30×，full prefetch 为 2.10/2.00/1.40×。8/128 KiB task 对 LLC OCA 为 9.40/2.60×；decompression 对 core/ICA/L2/LLC 为 4.0/1.8/3.9/18×。

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

### mllm backend

Qwen3 selected ops 的 ME/VE/DE count 为 23/61/76，work 为 110,591/83,968/249,856 cycles。Decoder slice static/dynamic 为 8,192/6,186 cycles（1.324×），动态产生 2,048 accumulated overlap cycles。run 005 的 tiny-tile 负结果证明粒度边界，不被删除。

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

1. Agentix 原论文使用 1/4/8× A100；本项目没有用两张 4090 冒充这些数据。Agentix aggregate 是 parameterized replay。
2. Agent.xpu 原论文使用 Intel Core Ultra 5 125H 的 NPU+iGPU；本项目为 source-grounded trace simulator，不是该设备实测。
3. ATX 原论文使用内部 silicon-validated Sniper 和 64-core Xeon-Max-like system；本项目 aggregate model 是透明 replay，真实 RTL 只验证开放 ABI/机制。
4. TISA 原论文使用未公开 Epoch 真硅片和 RTL；本项目 cycle model 与 Chipyard RTL 不能声称芯片等价。
5. Chipyard 系统路径使用 DRAMSim2；Ramulator2 是独立 NPU-memory experiment，二者没有伪装成单一 integrated memory backend。
6. mllm backend 使用原生 MIR trace，但没有下载/执行完整 Qwen3 权重；它验证 operator graph 与 cycle lowering，不验证生成质量。
7. Full-stack result 是新实验，无论文 target；priority responsiveness 与 throughput 存在明确 trade-off。
8. 当前 ME 为功能完整的 OS MAC 参考实现，不是 HPTPE 全规模阵列；WS 极低带宽优势提示需后续 dataflow adaptation。

## 工具链与配置

工具链不再依赖报告中的隐式环境状态。`config/toolchain.json` 是单一机器可读清单，固定 Python 3.11、pytest/cmake/ninja 版本、9 类系统命令、6 个外部源码 revision、2 个 Chipyard compatibility patch、4 个构建产物、4 个 Chipyard overlay，以及 8 个实验的严格串行顺序。`uv.lock` 保存 Python 包与 wheel/sdist hash。

`scripts/setup_toolchain.sh` 完成以下闭环：

1. `uv sync --frozen` 创建锁定的 Python 环境；
2. 获取并验证 MLX_dev、LLM.xpu、HPTPE、mllm、Ramulator2；
3. 使用 clang/clang++ 16 构建 Ramulator2；
4. 向固定 Chipyard checkout 安装 Scala/RTL overlay；
5. 构建 bare-metal ELF 和 Static/Dynamic Rocket+Verilator；
6. 执行 built-level 工具链审计，检查版本、commit、可执行文件及 overlay hash。

`.venv/bin/agentsys-reproduce-all` 严格按 direct paper、Agentix aggregate、ATX aggregate、mllm、full stack、Ramulator2、ablations、Chipyard 的顺序执行。每个 stage 退出后先检查 JSON gate、全部输出存在且非空及 SHA-256，随后才启动下一项；manifest 还验证相邻 stage 的 `next.started_ns >= previous.finished_ns`。完整说明见 `docs/toolchain.md`。

run 015 实际执行结果为 8/8 stages、`serial_order=true`，built/full toolchain audit 分别为 9/9 和 11/11。随后 run 016 重新执行 pytest 与 RTL lint，最终证书为 13/13 requirements、25 tests、55/55 论文端点，最大误差仍为 8.33%。

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
.venv/bin/python -m agentsys.experiments --run-id replay --output artifacts/results/replay.json
.venv/bin/python scripts/run_agentix_model.py
.venv/bin/python scripts/run_atx_model.py
```

### 3. mllm、全栈与消融

```bash
.venv/bin/python scripts/run_mllm_backend.py
.venv/bin/python scripts/run_full_stack.py
.venv/bin/python scripts/run_ablations.py
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
| PLAS/ATLAS | Figure-2 tests + run 010 | 通过 |
| HEG/reactive/proactive/batch/warmup/preemption | Agent.xpu run 011 | 通过 |
| mllm operator trace/simulator backend | mllm run 006 | 通过 |
| ATX async/prefetch/cancel/completion | ATX tests + run 004 + Chipyard ABI | 通过 |
| TISA lowering/RAW/WAR/WAW/ME-VE-DE dynamic issue | TISA run 011 + RTL run 003 | 通过 |
| HPTPE-inspired ME、VE/DE、SRAM/DMA | RTL + real ELF/checksum | 通过，规模边界已标注 |
| Ramulator2 DDR | official run 012 | 通过 |
| program priority 下传 | 636/636 inheritance + urgency test | 通过 |
| 论文核心数值误差 ≤15% | 55/55 endpoints，max 8.33% | 通过 |
| 逐层 baseline 与消融 | run 013 + full four-way table | 通过 |
| 两张 4090 不替代 A100 | evidence boundary | 遵守 |
| 锁定且完整的工具链配置 | toolchain run 015，11/11 gates | 通过 |
| 八项实验严格串行重放 | reproduction run 015，8/8 stages | 通过 |

## 参考资料

- Agentix：<https://www.usenix.org/conference/nsdi26/presentation/luo>
- Agent.xpu：<https://arxiv.org/abs/2506.24045>
- LLM.xpu：<https://github.com/xinming-wei/LLM.xpu>
- mllm：<https://github.com/UbiquitousLearning/mllm>
- HPTPE：<https://github.com/wqzustc/High-Performance-Tensor-Processing-Engines>
- Ramulator2：<https://github.com/CMU-SAFARI/ramulator2>
- Chipyard：<https://github.com/ucb-bar/chipyard>
- MLX Chipyard 工程参考（非目标机制）：<https://github.com/cspool/MLX_dev/tree/sys>

## 结论

AgentSys 已从方向草案转化为可执行、可重放、可审计的全栈系统，并由锁定工具链完成八阶段串行重放。最强证据不是某一个最大 speedup，而是四条相互校验的链：论文端点在 15% 内、开放 RTL/SoC/DDR simulator 实际运行、六层 priority 与 dependency lineage 全部闭合、配置到最终证书的工具链 13/13 验收闭合。实验同时表明，跨层优化没有免费午餐：priority 提升 reactive responsiveness 会牺牲部分 throughput，DDR 扩容会把瓶颈推向 ME，过小 tile 会让 dynamic scheduler 得不偿失，OS dataflow 在极低带宽下可能不如 WS。因而，核心创新应表述为“可解释、可组合且边界明确的全栈调度”，而不是对所有硬件和 workload 的无条件加速。

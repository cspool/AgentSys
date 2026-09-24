# AgentSys

RTX 4090 x2 上的 agent serving 系统研究仓库。四条线索引如下。

## 1. Agentix 复现(早期主线)

Agentix/Autellix 式程序级调度在消费级卡上的复现与分析。

- 入口: `experiments/h23-agentix-8b/` (服务/采集代码在 `code/`, 产物在 `artifacts/agentix_8b/`)
- 论文材料: `Agentix An Efficient Serving Engine for LLM Agents as General Programs/`, `ISCA26_G3_Agent全栈系统加速.md`
- 相关: `literature/`, `findings.md`, `research-log.md`

## 2. AutoTrace v1/v2/v3 (仅作分析工具, 不再深入科研)

GPU/nsys/NCU 的自动化 trace 采集与流程重建工具链。保留为工具, 不作为研究方向。

- v1: `perf_trace/` | v2: `perf_trace_v2/` | v3: `perf_trace_v3/`
- 采集器与工作流: `AutoTrace/` (含 `CURATION_MANIFEST.md`)
- 产物示例: `artifacts/agentix_8b/autotrace/`

## 3. 抢占探索: 并发机制复现 x wall 构造 x 抢占扰动 (2026-09, 已封存并转向)

三个真实论文并发机制(MPK / Bullet-greenctx / POD)在 sm_89 上的完整复现, 墙口径 v3(吞吐墙双级+容量墙),
三级抢占货币(配额/挂起/CILP)的扰动矩阵, 以及 wall-p 融入调度的分析。
**主线决策: 抢占择时研究停线**(上限被抢占时段框死, CILP 被真实系统回避), 资产转入调度级资源压榨
(E9 墙轨迹 / E11 流式增量消费), 详见计划文档末节。

- **计划与决策**: `experiments/h23-agentix-8b/workflow06/PREEMPTION_EXPLORATION_PLAN.md` (E1-E11 + 停线决策)
- **封存报告**: `experiments/h23-agentix-8b/workflow06/WP3_FINAL_REPORT.md` (复现/矩阵/统一规律/方法学教训)
- **总数据册**: `experiments/h23-agentix-8b/workflow06/REPRO_STATUS.json`
- **POD sm89 迁移文档**: `experiments/h23-agentix-8b/workflow06/POD_A100_TO_SM89_MIGRATION.md` (算子/启动几何/四种占用推导/容量适配)
- 复现代码: `experiments/h23-agentix-8b/pod_repro/` (V1/V2/V3 验证, figure6/13), `mpk_repro/`
- 抢占 harness 与数据: `experiments/h23-agentix-8b/wall_preemptive/wp3/` (受害者/抢占者/信标/配额/挂起门; `out/` 聚合结果, `out/slim/` 瘦身版逐次运行; 全量逐迭代原始数据仅存本机同目录)
- 第三方补丁(vendor 树不入库): `experiments/h23-agentix-8b/third_party_patches/` (vattention sm89 适配, BulletServe CUDA13/rtx4090)

## 4. Tool Use: 工具语义 KV 压缩 (E13 封存 / E14 立项, 2026-09)

工具调用轮次作为 KV 生命周期边界的语义压缩研究。E13 完成两规模(1.7B/8B)x两任务族x10消融臂,
单跳零质量损失下显存-65%/定预算吞吐+91~183%; 多跳前沿 -7pp@-70%。
新颖性对抗核查判定核心机制撞车(arXiv 2608.00902 在线轮压缩 / CommitKV 2608.07855 生命周期配对测量),
E13 封存; 幸存独有发现 = **毒页机理**(注意力保留在无关跨度恰保实体丢免责语境, 删之可超全KV质量),
E14 以"压缩即去噪"立论、按两论文配置对齐重启。

- **E13 归档报告**: `experiments/h23-agentix-8b/e13/E13_ARCHIVE.md` (创新点对质/配置/结论总表/机理/教训)
- **E14 计划**: `experiments/h23-agentix-8b/e14/E14_PLAN.md` (毒页感知压缩, ToolHop/FRAMES 对齐, CommitKV 复现为 baseline)
- 代码与数据: `experiments/h23-agentix-8b/e13/` (harness/探针/吞吐基准/断点缓存/全部 jsonl)
- 过程记录: `experiments/h23-agentix-8b/workflow06/PREEMPTION_EXPLORATION_PLAN.md` E13 各节
- 相关早期线: E11 agent级投机解码(归档于同计划文档), B3 verify 机制沉淀于 `e11/`

历史备注(原 README): 更早的抢占/动态调度机制计划已放弃, 其最大收获为 v2 工作流与产出定义。

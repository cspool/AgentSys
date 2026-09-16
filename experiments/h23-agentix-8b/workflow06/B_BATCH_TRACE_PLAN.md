# B 文档专用采集：受控并发 batch trace（batch8/16 方法迁移）

目的：R10_PROCESS（文档 B）的正式版数据源。开环 Poisson 流里机制事件散落、并发相位
只能事后搜索；本采集**构造**并发相位，使每个 Agentix 机制都有专属、可预知的分析窗口——
这是 auto_trace batch8/16（2 warmup + 8/16 受控并发请求的全 process/kernel/利用率 trace）
方法在 agent serving 上的迁移。

## 负载构造（make_ctrl_conc.py → workloads/ctrl_conc16.json，sha 8660f5f4）

| 相位 | 时间 | 构造 | 凸显的机制/宇宙 |
|---|---|---|---|
| W  | 0–5 s | 1 个预热程序（2 短调用），分析窗口排除 | 引擎就绪 |
| P1 稳态 decode | 5–12 s | 16 个新程序各 1 调用，输出 28 tok（< Q0 quantum 32，不被切分） | 满批纯 decode 的 step/kernel 宇宙基线（无抢占污染） |
| P2 攒历史 | 12–30 s | 4 个 aged 程序各 3 个中调用（输出 300），累计服务越过 Q2/Q3 界（2/8/32 s） | 进程表 {T_p,W_p} 填充 |
| P3 准入风暴 | 30–55 s | aged 的第 4 长调用（输出 512）与 8 个新短程序（3×48 tok）同时到达 | 同窗内 Q0 vs Q2/Q3 准入分层、quantum 用尽→降级→再排队→再 prefill 密集发生 |
| P4 排空 | 55 s– | 队列清空 | 完成尾 |

相位边界写入负载 JSON（`phases` 字段）：分析窗口是**构造的**，不是搜索的。

## 采集

- 臂：agentix_core（论文机制本体）；GPU1 串行；nsys cuda,nvtx；
  `VLLM_USE_V2_MODEL_RUNNER=0`、`VLLM_ENABLE_V1_MULTIPROCESSING=0`、
  `AGENTIX_W_INSTRUMENT=1`（19 探针 + 机制事件 + **新增 w.step 批组成标记**：
  每次 schedule 后发 `w.step::reqs=N::tok=M`，补上 batch8 的"每迭代批形状"目标）。
- 产物：`artifacts/agentix_8b/autotrace/ctrl_conc16_core/`（cap.nsys-rep/sqlite + run/）。
- NCU：GPU 内指标沿用 focus2 重放（同栈同 kernel 家族）；如需相位内重放另开串行会话。

## 分析目标（对应 batch8 契约）

1. A00 守恒门（新 spec）；2. 相位窗口内：step 批组成分布（reqs/tok，P1 vs P3）、
chunk/demote/准入事件密度、quantum 段与再 prefill 成本；3. 深潜图 ×2（P1 基线 / P3 风暴）：
step 实例条码 + busy/gemm/在飞/step率/批组成 lane 共轴；4. kernel 显微（P1 与 P3 各一窗）；
5. B 文档 v1 重建（--process-capture ctrl_conc16_core）。

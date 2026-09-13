# h23 复现审计 — 对照本地知识库中的 Agentix 原文

日期 2026-09-13。来源：本地 Obsidian 知识库
`paper_secs/paper_20260824/Agentix An Efficient Serving Engine for LLM Agents as General Programs/`
（§3 调度算法、§6.1 Workloads、§6.2 Experimental Setup、Fig. 11 负载统计、Fig. 12 主结果）。

审计针对第一版复现（见 git 历史中的 `results.md` §1–4），共发现 6 处偏差，其中 3 处已修正、3 处记录为已知差距。

## 已修正

### A1. PLAS 优先级定义用错了量（**影响结论**）

- **论文 §3**：`PLAS` 的优先级是该程序**先前已完成 LLM 调用的运行时长之和** —
  "assigns a priority p(c_j) to c_j based on the sum of all runtimes, t_k, of all prior LLM calls with the same ID"。
- **第一版实现**：累加 `output_tokens` 作为服务量代理。
- **修正**：改为累加实测 `finished - submitted`（微秒）。token 数与解码时长相关但不等价，
  尤其在 prefill-heavy 的 BFCL 类上两者排序会明显不同。

### A2. 负载统计量与论文不符（**影响结论**）

论文 §6.1 / Fig. 11 给出了每类负载的确切均值；第一版是我凭结构猜的区间，其中 ShareGPT 的
prefill/decode **方向是反的**，LATS 的调用数**差一个数量级**：

| 负载 | 论文：调用数 | 第一版 | 论文：prefill/decode | 第一版 |
|---|---:|---:|---|---|
| ShareGPT | 6.66（max 80） | 1–3 | 255.65 / **276.81**（decode-heavy） | 384 / 80（**prefill-heavy，反了**） |
| BFCL | 10.75（max 70） | 10–32 | **735.06** / 34.14 | 1280 / 160 |
| LATS | **159.71** | 6–24（**少 10×**） | 467.24 / 72.64 | 640 / 120 |

**修正**：`workload.py` 的类参数改为按论文均值的对数正态采样（长尾，符合 Fig. 11d），
类名同时改为论文的 `sharegpt` / `bfcl` / `lats`。实测校准结果：

| 负载 | 调用数均值（论文→本地） | prefill（论文→本地） | decode（论文→本地） |
|---|---|---|---|
| sharegpt | 6.66 → 6.16 | 255.65 → 259.6 | 276.81 → 279.8 |
| bfcl | 10.75 → 10.81 | 735.06 → 728.3 | 34.14 → 34.3 |
| lats | 159.71 → 161.91 | 467.24 → 465.9 | 72.64 → 72.5 |

### A3. 到达率区间错了一个数量级（**影响结论**）

论文 Fig. 12 在 LLaMA3.1-8B / 1 GPU 上，Mixed 的横轴约 **0.1–0.3 program/s**（LATS 约 0.05–0.2，
ShareGPT 约 2–4，BFCL 约 0.2–0.6）。第一版用了 1/2/4 program/s 跑 Mixed —— 因为当时每个程序
只有 2–20 次调用，比论文小一个数量级，所以必须靠高到达率才能压出负载。**修正**：负载改对之后，
Mixed 按论文区间 0.1 / 0.2 / 0.3 program/s 重跑。

## 已知差距（未修正，如实记录）

### B1. 我的 baseline 实际对应 vLLM-opt，不是 vLLM（**影响可比对象**）

论文有三个 baseline：`vLLM`（v0.6.1 默认 FCFS，**无 prefix cache**）、`vLLM-opt`（开启 chunked prefill +
prefix caching + multi-step）、`MLFQ`（在 vLLM-opt 之上做抢占）。本机 vLLM 0.29.0 默认
`enable_prefix_caching=True, enable_chunked_prefill=True`，因此我的 "fcfs" 臂**等价于 vLLM-opt**。

后果：论文的 **15×** 是对朴素 vLLM 的比值；与我的对照可比的是 Agentix **对 vLLM-opt 的约 2×**
（ShareGPT/BFCL）、**2×**（LATS）、**5×**（Mixed）。第一版 `results.md` 里"论文 4–15×"的措辞
虽引自摘要，但用作我的对照参照时会高估应有幅度。

### B2. 我实现的是静态 PLAS，不是论文的 MLFQ 版 Agentix

论文 §3 的 Agentix 是**多级反馈队列**：优先级离散化进 `Q_i`、每队列有时间片、用尽后降级、
等待过久触发反饥饿提升。我的实现只在提交时给一个静态优先级（vLLM 原生 priority 调度器），
**没有时间片、降级与反饥饿**。因此本次测到的是"程序级优先级排序"这一核心思想的下界，
不是 Agentix 的完整机制。

### B3. 缺多线程程序与 ATLAS

论文中 LATS 是**多线程**负载（"involve many parallel LLM calls"），用 `ATLAS`（按关键路径已得服务）
调度，且多线程程序的 program-level token latency 定义为**关键路径响应时间 ÷ 所有线程总 token**。
我的程序全部是**串行链**，没有并行分支，因此既没有 ATLAS 对照，也没有触发 gang-scheduling 的场景。
这是与论文差距最大的一处结构性缺失。

## 顺带更正的一处自我误判

第一版把"限制 `--max-num-seqs` 才看到收益"写成了人为制造的口径。实际上论文 §6.2 明确
"All baselines, including Agentix, use the same max batch size"——**统一 batch 上限本就是论文协议的一部分**，
我的饱和口径在这一点上是合规的，不必标注为人为口径。

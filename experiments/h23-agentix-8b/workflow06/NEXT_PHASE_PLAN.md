# 第二版计划（重梳 v3）：以真实并发负载为对象的 wall 择时对照

日期：2026-09-22。前置：`CONCURRENCY_DESIGN_FINDINGS.md`、`PREEMPTION_EXPLORATION_PLAN.md`。
历史版本：`.v1.bak`（等待时间为终点）、`.v2.bak`（六机制张量）。**只使用 GPU 0。**

---

## 0. 本版的四处改动

| 改动 | 理由 |
|---|---|
| **研究对象从"机制"改为"并发负载"** | 抽象机制（自建的 warp 融合、CTA 融合）不具体、无对照系统。改为三个**有论文、可复现**的真实并发负载 |
| **删除 CTA 融合与 warp 融合** | 不具体。CTA 融合已实测与双流数值完全相同（共驻失败区 55.4 ms = serial），无独立价值 |
| **green 只做 resize，删除静态分区** | 静态分区已实测是错误配置（4% 共跑比例下扣 10% 吞吐），无需再扫 |
| **暂不做排队等待时间**（作为简化） | 先把吞吐扰动在真实负载上做透；等待时间留待后续版本 |

---

## 1. 研究对象：五个并发负载（三个族 B + 两个族 A）

### 1.1 族 B —— SM 内部并发（把闲置功能单元填满）

每个都必须**先复现论文**，再作为并发负载接受 wall 对照。

| 负载 | 论文 / 代码 | 可复现性 | 对照组 |
|---|---|---|---|
| **B1 MPK** | Mirage Persistent Kernel，OSDI'26 / arXiv 2512.22219；`github.com/mirage-project/mirage`（mpk 分支），含 Qwen3-8B demo | ✅ 开源 | 逐 kernel eager 执行 / CUDA Graph |
| **B2 HFuse 融合 kernel** | *Automatic Horizontal Fusion for GPU Kernels*（CGO'22），开源；在本计划里取 POD 论文 Table 3 的 `FA_HFuse` 配置——把 prefill/decode 的 FA kernel 做 **warp 级水平融合** | ✅ 开源 | FA_Serial（串行）/ FA_Streams（双流） |
| **B3 POD-Attention** | ASPLOS'25 / arXiv 2410.18038；基于 FlashAttention v2.6.1，集成进 Sarathi-Serve。**无独立仓库**，可用路径是 FlashInfer 的 POD attention（SGLang PR #20346，`--enable-flashinfer-pod-attention`） | ⚠️ 需经 FlashInfer/SGLang | B2 及 FA_Serial / FA_Streams（同属 Table 3） |

**B2 与 B3 是同一次复现的两个配置**——POD 论文的 Table 3 本来就把
`FA_Serial / FA_Streams / FA_HFuse / POD` 放在一起对照，因此复现 POD 即同时得到 B2。

**B3 的核心机制（知识库已存原文与代码，`可复现paper` / `paper总结-26 03 11-ty`）**：
prefill 与 decode 共用**一个融合 kernel**，由每个 CTA 的 **leader 线程**在 kernel 入口处认领身份——

```cuda
int sm_id;  asm volatile("mov.u32 %0, %smid;" : "=r"(sm_id));   // 我在哪颗 SM
const int ratio = (prefill_ratio + decode_ratio);               // 参数
int op, ticket = (atomicAdd(&sm_ctr[sm_id], 1) % ratio);        // 每 SM 一个计数器, 取票
if (ticket < prefill_ratio) op = PREFILL; else op = DECODE;
int cta_id = atomicAdd(&cta_assign[op], 1);                     // 该 op 用完则切换到另一个
```

**关键观察（决定我们的增量在哪）**：POD 用的是**无状态的确定性轮转**（`% ratio` 取票），
**不是**"观测当前状态再决定"。这正是它不会羊群的原因——也解释了我们角度 3 的负面结果：
我们那版 `affinity` 策略读 `running[sm]` 再判断，恰恰是 POD 刻意避开的做法
（8 worker/SM 时退化到 1.05×，输给无状态交替的 1.49×）。

POD 还有**第二个旋钮**（论文 Fig.10）：把 decode 的 tile 缩到 16，可大幅把计算核心让给 prefill，
而 decode 自身的 HBM 带宽利用率毫不受损。这是构造 wall 变体时可用的参数。

### 1.2 族 A —— SM 外部调度（决定谁上哪颗 SM）

| 机制 | 本质 | 真实实例 |
|---|---|---|
| **A1 MPS** | 多 Stream 分别承载**不同子程序**；一次抢占影响所有共享该 server ctx 的子程序，**抢占影响最大** | 场景待定：多 agent 子程序共置（已有 agent loop 负载）或 LC/BE 混部 |
| **A2 green ctx 分区（只做按需 resize）** | 平时受害者独占整卡，触发时才切分区，burst 结束立刻还回（预建池切换 green 4.26 μs / libsmctrl 1.16 μs） | **两个实例**：<br>**Bullet**（SOSP'25）—— SRM roofline 预测 TTFT/TPOT，SLO-aware scheduler 周期搜索最优 SM 分区，`libsmctrl_set_stream_mask` 微秒级重分区（报 4.1 μs），PD 共置<br>**μShare**（2025, TJU）—— blocksize shaping（half-plus），LD_PRELOAD 零改码 |

**两个实例的手段不同，需在文档中写清**：Bullet 用**显式 TPC mask**，μShare 用**隐式 block 形状**
逼 block 散开；但两者同属"从 SM 外部控制谁拿到多少 SM 容量"，故归一格。
**μShare 的前提我们已在 4090 上独立验过**：blockDim 决定后到 kernel 能否与在位 kernel 共驻，
三级阶梯（≤224→c≥32 / 256–480→c≥96 / ≥512→c≥192），对受害者块数、寄存器压力、kernel 身份
全不变——可直接作为复现 μShare 的起点。

### 1.3 明确排除：Infera

*Automated End-to-End Model Serving with Cooperative Compilation and Scheduling*（EuroSys'26，
DOI 10.1145/3767295.3769392）。它踩在我们三个点上——`FuseKernels` 是 SASS binary 级的自动
warp 水平融合（= B2 的自动化版）、`LaunchKernel` 用 CDP daemon kernel 从 DKQ 拉任务（= B1 的形态）、
`SelectKernels` 按运行时 IPC/TLP 估计选 kernel 版本。
**但它无官方代码**（GitHub 上的 `AMD-AGI/Infera` 是同名的无关 AMD 项目），且是整套 serving 系统
（含 SASS binary 改写），复现代价远高于 B1–B3，而它的三件事我们各有更轻的代表。
**按"非开源不做"的规则排除，只进 related work。**

---

## 2. 每个并发负载的统一实验流程

对 B1/B2/B3 与 A1/A2 各执行同一套四步，产出可横向对比的表。

### 2.1 第一步：复现论文

**验收**：论文关键数字**定性成立**（方向与量级对），定量不达标要写明差距与归因，**不冒充达标**
——沿用 Valve 复现的做法（尾延迟 +701% → +2~4% 成立，但 p50/TPOT 差距如实记录）。

| 负载 | 复现验收点 |
|---|---|
| B1 MPK | 相对逐 kernel 基线的端到端延迟下降（论文报 1.2–6.7×，README）；worker/scheduler SM 分工生效 |
| B2 HFuse | 融合后的 FA kernel 相对 FA_Serial / FA_Streams 的耗时关系符合 POD 论文 Table 2 的定性判断（GC=✓ 但 WQ=✗，受 straggler 拖累）——我们已在 4090 上独立复现该定性结论 |
| B3 POD | 混合批下 attention 耗时相对 FA_Serial / FA_Streams / FA_HFuse 的优势（论文 Fig.6；论文报最高 59%、均值 28%）；`sm_ctr[sm_id]` 取票机制生效（可用 `%smid` 采样验证每 SM 的 P/D 配比） |
| A1 MPS | 多子程序共置下的抢占影响（对标 Valve 复现的表） |
| A2-Bullet | PD 共置下 SM 重分区生效、微秒级切换（我们实测 green 4.26 μs / libsmctrl 1.16 μs，与其报的 4.1 μs 同量级） |
| A2-μShare | half-plus blocksize 使互补 kernel 共驻（我们已验三级阶梯律，可直接对照） |

### 2.2 第二步：测它的**原生 wall 特征**

每个并发负载在其**论文设定的默认配置**下，用 NCU 出五轴画像：
FP32 / TensorCore / L2 带宽 / DRAM 带宽 / shared memory。

**预期（待验证）**
- B2 POD：prefill(TC/算力重) + decode(DRAM 重) 的混合批 → 天然就是 **TC 墙 ↔ 访存墙的混合体**，
  这正是真实 serving 的形态，也是我们此前两轴负载丢掉的那一对
- B1 MPK：整段模型熔成常驻 kernel，wall 特征随 tGraph 阶段漂移 → 可能没有稳定的"相位"，
  **这本身是个重要发现**（若成立，wall 择时在 MPK 上无从下手，需改用 task 粒度）
- A1 MPS：取决于各 Stream 承载的子程序

### 2.3 第三步：**自行构造其他 wall 特征**

对同一个并发负载，改其参数把它推到不同的墙，得到同一负载的 wall 变体：

| 负载 | 可调旋钮 → 目标墙 |
|---|---|
| B3 POD | ① `prefill_ratio : decode_ratio`；② decode tile size（论文 Fig.10：缩到 16 可让出计算核心而不伤带宽）；③ chunked-prefill 的 chunk 大小 → 从 TC 墙连续推到访存墙 |
| B2 HFuse | warp 切分比（我们已测：偏离最优比惩罚极大，blockDim=256 下 2/8 切分比串行还差 67%） |
| B1 MPK | 模型规模 / batch / 序列长度 → 改变 decode 的算术强度 |

| A1 MPS | 各 Stream 上子程序的资源画像 |
| A2 | 沿用已校准的 `inner` 扫描（60/290/600）+ 待建的 L2/smem 墙 |

**验收**：每个变体的 NCU 画像**目标轴 ≥ 70%、副轴 ≤ 50%**；达不到则记为该负载**不可推到该墙**，
这同样是结论（说明该负载的 wall 特征受其算法结构约束）。

### 2.4 第四步：**wall 抢占 vs 普通抢占**的吞吐扰动对照

在每个 (并发负载 × wall 特征) 上跑三臂，与现有 `wall_preemptive` 协议一致：

- `valve`（普通抢占）：到达即抢占，不看受害者状态，T_cool 冷却
- `wall_aware`（wall 抢占）：同一到达序列，推迟到 wall 相位，截止期封顶
  - **在 B3 POD 上，"wall 抢占"的具体形态是动态 ratio**：按受害者当前墙型实时调
    `prefill_ratio : decode_ratio`（POD 原版是固定 ratio 的无状态轮转）。这是我们相对 POD 的增量，
    且其代码结构天然支持——只改一个参数。**但必须保持无状态轮转的取票机制**，否则会掉进角度 3 的羊群陷阱
- `random_defer`（公平性对照）：花掉与 wall_aware 相同的推迟预算但与状态无关

**指标（只看吞吐扰动，不做等待时间）**
- 受害者绝对吞吐（相对无抢占基线的损失）
- 共跑者绝对吞吐
- 逐事件配对扰动（**仅在同一并发负载内部可比**，跨负载必须用绝对吞吐——见
  `CONCURRENCY_DESIGN_FINDINGS.md` §4 的三条口径修正）

---

## 2.5 已完成：真实 kernel 的 wall 构造（2026-09-22，GPU1 实测）

产物 `wall_preemptive/walls/REAL_WALLS.json`；探针 `real_walls.py` / `prof_walls.sh`。

**口径**：wall = 某一资源接近满载（或达该轴在本卡的可达峰值），**其余资源使用也较高**。
副轴 <20% 判为不合格——那是只用一种资源的合成 kernel，不是真实负载的墙。
（此前用合成 kernel 造的 L2 墙副轴 DRAM 4.4%/FMA 2.2%、smem 墙副轴 L2 0.11%/DRAM 0.56%，
按此口径全部作废，仅保留为资源满载的参照上界。）

**构造成功的三堵真实 kernel 墙 + 全饱和**（ncu 2026.2，`--cache-control none`）：

| 墙 | 真实 kernel | 目标轴 | 副轴 | 归属 |
|---|---|---|---|---|
| FP32 算力墙 | fp32 GEMM 512×8192×8192（`cutlass_80_simt_sgemm`） | FMA **73.0** / SM 81.6 | smem 42、L1 43、L2 29、DRAM 32 | 每 SM 私有 |
| TC 张量核墙 | fp16 GEMM 6144³（`ampere_fp16_s1688gemm`） | TC **49.2 = 可达峰值 100%** | L2 54、L1 30、DRAM 18 | 每 SM 私有 |
| DRAM 访存墙 | SDPA decode B=64 KV=16k（`flash_fwd_splitkv_kernel`） | DRAM **96.97** | TC 37、L2 38、L1 15 | **GPU 全局** |
| 全饱和 | fp16 GEMM 2048³（热缓存） | TC 46（94% 峰值）+ L2 72 双高 | L1 34、smem 22 | 混合 |

**构造失败的两堵，如实记录**：
- **L2 墙不可构造**：decode KV 压进 L2（17/34/50/67 MB，热缓存）→ DRAM 降到 0.4–7% 但 **L2 只有 21–35%**
  （延迟受限，非带宽受限）；提并行度（B=16/32/64/128）L2 仍 21–32%；fp16 GEMM 能把 L2 推到 70–77%
  **但 TC 同时满载**（94% 峰值），是双轴高；fp32 GEMM 不走 TC，L2 只到 28.7–35.6%。
  **结论：L2 的饱和在真实 kernel 里总与 TC 饱和绑定（GEMM 的 tile 同时驱动两者）。**
- **smem 墙不可构造**：所有真实 kernel 的 smem 专项指标最高 48%，从不是最高轴。

**硬件校准**：**TC 在 4090 上的可达峰值是 ~49%**——四种完全不同的 GEMM 形状
（4096×4096×16384 / 2048×2048×32768 / 6144³ / 8192³）全部卡在 48.7–49.3%，是 FP16 配 FP32 累加
走半速路径的硬件上限，不是负载不够。（`MANIFEST.json` 记的 TC 峰值 97% 是我们自己用 Triton
`tl.dot`(bf16) 测的，路径不同，两者须分开记。）

**两个测量陷阱**（均已踩过，写入验收流程）：
1. **ncu 默认 `--cache-control all` 每次 replay 前清空 L2**，导致 L2 驻留型负载永远测出 DRAM 高。
   改 `--cache-control none` 后，KV 17 MB 的 DRAM 从 72.6% 掉到 **0.42%**。
2. **必须按 kernel 名过滤**——`randn` 的 curand kernel 排在前面，`--launch-skip` 会命中它而非目标
   kernel（第一版数据 TC 全 0、各配置雷同，就是这个原因）。名字：prefill `flash_fwd_kernel`、
   decode `flash_fwd_splitkv_kernel`、fp16 GEMM `ampere_fp16_s1688gemm_*`、
   fp32 GEMM `cutlass::Kernel2<cutlass_80_simt_sgemm_*>`（base name 是 `Kernel2`，不含 "gemm"）。

**对 H2 的影响**：原定用 smem 墙（每 SM 私有）vs L2 墙（GPU 全局）做判决性对照，两者均不可构造。
**改用 TC 墙 ↔ DRAM 访存墙**——同样是一私有一全局，且两者都干净，比原方案更扎实。

## 2.6 已启动：真实负载的 wall 抢占对照（2026-09-22，GPU1）

产物 `wall_preemptive/realwp/`（`real_victim.py` / `run_real.sh`）。
受害者 = **TC 墙 ↔ DRAM 访存墙**交替（2.82 ms / 4.58 ms，时长已配平）；
共跑者三种亲和 × 三臂（`valve` / `wall_aware` / `random_defer`）。

**关键设计：正交相位因共跑者而异**——不是"哪个相位好"，而是"共跑者主资源与受害者饱和资源是否重叠"：

| 共跑者 | 主资源 | 正交相位（wall_aware 推迟到此） | 重叠相位 |
|---|---|---|---|
| tc | 张量核 | **dram** | tc |
| dram | DRAM 带宽 | **tc** | dram |
| fp32 | CUDA core（与 TC 抢发射带宽） | **dram** | tc |

**已修复的坑**：受害者必须活过控制器，否则 `PHASE_NOW` 冻结在最后一个相位，落墙统计全假
（首次 smoke 出现 valve 落墙 12/12 的假结果）。现已加 `victim_outlasted_controller` 校验字段。
修复后 valve 落墙 121/200 = 60.5%，与 dram 相位 62% 的时间占比吻合——状态盲策略该有的随机落点。

## 3. 假设（保留，按新对象重述）

> **H1：扰动主要由"共跑者主资源 × 受害者饱和资源"的重叠决定**，正交则近乎免费，随共跑份额单调放大。

> **H2：族 A 决定重叠能否被规避** —— 每 SM 私有的资源（TC + warp scheduler 发射带宽、shared memory、
> warp slot、寄存器）可被空间分区隔离；GPU 全局的资源（L2 带宽、DRAM 带宽、板级功耗/时钟）不能。
> 已有半个证据：green 下 SM 不相交仍有扰动，机制定位为**板级功耗墙**（贴 450 W 的 97%，时钟掉 74 MHz）。

> **H3：两族对同一 (受害者墙 × 共跑者资源) 的响应方向相反。**
> 族 A 求**隔离**——重叠则贵、正交免费，最优策略是躲开；
> 族 B 求**互补**——正交才有收益（填满受害者闲置的功能单元），重叠反而比族 A 更糟（同 SM 内直接抢
> warp slot 与发射带宽，无处可躲）。
> **推论：同一组合下两族的最优选择可能相反**，这是"该用哪种并发负载"第一次有可操作答案的地方。

> **H4（新）：wall 择时的收益随并发负载的"相位清晰度"下降。**
> POD 有明确的 prefill/decode 相位 → 择时有处下手；MPK 把一切熔进常驻 kernel，若相位消失，
> wall 择时在其上失效，只能下沉到 task 粒度。**这条若成立，等于给出了本主张的适用边界。**

---

## 4. 执行顺序

```
S1 复现 B1 MPK ────┐
S2 复现 B2 POD ────┼─> S4 各自原生 wall 画像 ─> S5 构造 wall 变体 ─> S6 三臂吞吐扰动对照
S3 确认/复现 B3 ───┘                                                        │
                                                                    S7 族A 真实场景
A1 MPS 多子程序场景 ─┐                                                      │
A2 green resize(已有)─┴──────────────────────────────────────────────────────┘
```

S1–S3 可按 GPU 0 串行。A2 已有产物（R12 四臂）可直接复用；A1 需先定场景负载。

---

## 5. 明确排除项（本版不做）

- ❌ CTA 融合、warp 融合（不具体，且 CTA 融合已被实测证明与双流等价）
- ❌ green 静态分区（已证明是错误配置）
- ❌ 排队等待时间优化（作为简化，留待后续版本）
- ❌ 位移式抢占的真实代价（KV recompute / swap / 批次占用）——留待接入真实 serving 时一并做

---

## 6. 强制条款

1. **只使用 GPU 0。**
2. **复现优先**：任何并发负载在复现验收通过前，不得用于 wall 对照；复现不达标要写明差距与归因，
   **不冒充达标**。
3. **对照协议具体化**：固定负载、固定并发负载的启动参数、固定到达序列（同种子）、固定共跑工作量；
   **唯一变量写明**。
4. **公平性对照臂必备**：`random_defer` 式（同推迟预算、不看状态），否则无法判定收益来源。
5. **跨并发负载比较一律用绝对吞吐**，逐事件配对扰动只在同一负载内部可比。
6. **两侧都记**：受害者与共跑者的吞吐必须同时报告。
7. **代价入账**：策略的观测/决策开销、分区切换代价，计入被比较的一侧。
8. **优化不得牺牲输出**：给出输出一致性证据（`output_sha` 或等价）。
9. **复用三条件**：同输入 + 通过独立验收 + 阶段指纹未变；任一不满足则该步及下游重跑。
10. **修改即升版**：实质性修改产生 v3.1、v3.2……；**升版前须询问用户**。
11. **模型/数据集**一律放 `/data3/docker_model/AgentSys`（host bind）。
12. **baseline 必须 2025 年及以后**：MPK（OSDI'26）、POD-Attention（ASPLOS'25）、Valve（2026）、
    Bullet（SOSP'25）、LithOS（SOSP'25）、μShare（2025）、VUDA（2026）。
    唯一例外：HFuse（CGO'22）——它不是我们的 baseline，而是 POD 论文自带的对照配置。
13. **非开源不做**：无官方代码的系统只进 related work，不做复现（据此排除 Infera，EuroSys'26）。

---

## 7. 风险与证否条件

| 风险 | 证否条件 | 应对 |
|---|---|---|
| ~~B3 论文未确认~~ | 已解决：B3 = POD-Attention，其 SM-aware CTA scheduling 即"SM 内按比例跑 P/D + 每 SM 计数器" | — |
| B3 POD 无独立仓库、经 FlashInfer 路径复现不出论文数字 | 混合批 attention 耗时相对 FA_Streams 无优势 | 降级为"引用其分类表，不复现其系统" |
| MPK 无稳定相位（H4 成立） | NCU 画像在 tGraph 阶段间无 ≥70/≤50 的清晰切换 | **这是结论不是失败**：写成 wall 择时的适用边界，并改用 task 粒度 |
| 某负载推不到目标墙 | 变体画像目标轴 <70% 或副轴 >50% | 记为该负载受算法结构约束，不可推到该墙 |
| H1 不成立 | 正交组合的损失 ≥ 重叠组合 | 墙论断动摇，退回逐组合经验表 |
| H3 不成立 | 两族最优选择在所有组合上一致 | "该用哪种并发负载"退化为单一排序 |

---

## 8. 与现有产物的关系

- **保留并复用**：`wall_preemptive` 协议（泊松同序列、三臂、逐事件局部配对）、A2 的 R12 四臂数据、
  Valve 复现（作为"普通抢占"的参照系）。
- **不推翻**：墙论断的三次独立复现（抢占时机 / 静态分区代价 / 功耗墙机制）。
- **改变的是对象**：从自建合成机制改为**有论文、可复现的真实并发负载**，每个负载自带原生 wall 特征。

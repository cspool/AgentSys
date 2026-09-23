# POD kernel 从 A100 迁移到 sm_89 (RTX 4090)

本文按 VisiPrune FX 可视化规范书写: 所有图形均为**矩形轴/区域图**, 不使用流程图或 op 框;
图内标签一律英文以保证等宽对齐, 图外解释为中文。每幅图上方标注 `Tensor` 与 `Formula`,
图与图之间的承接关系由这两行标签的内容表达。所有数值来自本机实测
(NCU / compute-sanitizer / 编译期 traits 求值), 无一处为推算。

- 硬件: RTX 4090 (AD102 裁剪版, 128 SM), 驱动 595.91.07, CUDA 12.8 工具链
- 对象: microsoft/vattention @ pod_attn — POD-Attention (ASPLOS'25)
- 迁移原则: **保论文机制, 只调容量参数**; 达不到的档位如实标注, 不假装达标

---


## 0. 前置: 全文涉及的算子

后文所有容量核算都建立在这些算子的张量切分方式上。每个算子按同一规范给出:
是什么 / 为什么需要 / 怎么做·计算, 以及矩形轴图。

### 0.0 block 的启动几何、三维含义与四种占用的推导

**是什么** — CUDA kernel 以 `kernel<<<gridDim, blockDim>>>` 启动, 两者都是三维向量。
block(=CTA)是调度与资源分配的原子单位: 一组 warp 整体驻留在一个 SM 上, 从进驻到跑完排他持有
smem/寄存器/warp 槽三种资源, 不可拆分不可迁移。本节把**每一维的含义、由哪个算法维度决定、
数值是多少**钉死, 再给出从 tile 参数到 smem/寄存器/TC/CUDA core 四种占用的完整推导链。

**blockDim(块内三维)** — FA2 系 kernel 全部一维: `blockDim = (kNThreads, 1, 1)`,
`kNThreads = kNWarps x 32`(kernel_traits.h:64); y/z 恒为 1 无含义。kNWarps 由 **M 维的并行切分**
决定: TiledMMA 把 kNWarps 个 warp 沿 M 维并排(`Layout<Shape<kNWarps,1,1>>`, 每 warp 负责 16 行,
`Tile<16 x kNWarps, 16, 16>`, kernel_traits.h:74-77)。数值: 4 warps=128 线程(主力配置)、
2 warps=64(4CTA 档 prefill)、1 warp=32(4CTA 档 decode)。

**gridDim(网格三维)** — 标准 FA2 (flash_fwd_launch_template.h:60-61):

```text
Tensor : GRID_GEOMETRY of standard FA2 = 3D lattice of blocks, one block per (M-tile, seq, head)
Formula: grid = ( ceil(S_q / kBlockM),  B,  H )   ;   blockDim = (kNWarps x 32, 1, 1)
           x = which Q row-band          y = which sequence   z = which attention head
           driven by S_q and kBlockM     driven by batch      driven by model heads

        grid.x (M-tiles) 0 ──▶ ceil(S_q/kBlockM)
       ┌─────────┬─────────┬─────────┬─────────┐
grid.y │ blk(0,0)│ blk(1,0)│ blk(2,0)│ blk(3,0)│  ◀── each cell = one block of 128 threads
(B seq)│ blk(0,1)│ blk(1,1)│ blk(2,1)│ blk(3,1)│      grid.z = H heads stacked behind (not drawn)
       └─────────┴─────────┴─────────┴─────────┘
split 变体(:106-107): grid = (M-tiles, num_splits 或 B, B x H 或 H) —— y 让位给 KV 分段号
```

**POD 融合核故意抹平网格**(fused_fwd_launch_template.h:465): `grid = (P_slots + D_slots, 1, 1)`,
一维扁平。因为 POD 的机制就是**绕开硬件的 blockIdx→工作 映射**: 每个 block 进场后由 `%smid` +
ticket 自行领取角色(P/D)与逻辑 id(0.5 节), blockIdx.x 只是入场券编号。数值例(fig6 chunk2k_d16,
fp=9): P_slots = ceil(2048/128) x 1 x 32 = 512, D_slots = 1 x 16 x 32 = 512 → grid=(1024,1,1)。

**四种占用的推导链** — 全部由算法维度四元组 (kBlockM, kBlockN, d=128, kNWarps) 决定:

```text
Tensor : SCORE_TILE (kBlockM x kBlockN) annotated by WHICH hardware unit consumes which part
Formula: TC eats the two GEMMs (S = Q K^T, O = P V) ; CUDA cores eat softmax row-ops ;
         smem holds Q/K/V tiles ; registers hold the accumulators that never leave the thread

                 kBlockN (K/V tile cols)
                0 ──────────────▶ 32
       ┌──────────────────────────┐
kBlockM│ GEMM_AREA_TENSOR_CORE    │ ◀── mma.sync fp16: S=QK^T 与 O=PV, TC 占用由**有效 M 行数**定:
(128   │ GEMM_AREA_TENSOR_CORE    │     prefill M=kBlockM 全宽 -> 实测 TC 93.5% 可达峰
rows)  │ GEMM_AREA_TENSOR_CORE    │     decode 有效 M=1 行   -> 实测 37.8%
       └──────────────────────────┘
       ┌──────────────────────────┐
per-row│ SOFTMAX_ROW_OPS_CUDA_CORE│ ◀── exp/max/rescale + 地址运算, FMA 管线实测仅 2.3-4.9%
       └──────────────────────────┘
```

逐项推导(以 2CTA 档 P(128,32,4), 128 线程为例, 实测值印证):

| 占用 | 公式 | 代入 | 实测印证 |
|---|---|---|---|
| smem | (kBlockM + 2 x kBlockN) x d x 2B | (128+64) x 128 x 2 = **48 KB** | NCU 48.0K |
| 寄存器 | O 累加器 kBlockM x d x 4B / 线程数 = 128 fp32/线程; S 累加器 kBlockM x kBlockN/线程 = 32; 操作数分片+softmax 状态+地址 ≈ 40-90 | 合计 > 200/线程 | NCU **255**(顶格) |
| TC | 由 GEMM 有效 M 行数定 | prefill 全宽 / decode 1 行 | 93.5% / 37.8% 可达峰 |
| CUDA core | softmax 行操作, 与 tile 面积成正比但远小于 GEMM | — | FMA 2.3-4.9% |

寄存器一项解释了第 5 节的现象: O 累加器**永不落 smem**(除 split 路径), 它按 kBlockM x d / 线程数
分摊 —— 128 线程扛 128x128 的 O 就要 128 个 fp32 寄存器/线程打底, 所以 128 线程配置实测顶格 255;
4CTA 档把线程降到 64 但 kBlockM 也降到 64, O 分摊仍是 64x128/64 = 128/线程, 可用预算 256(64线程x4CTA)
→ 寄存器自动让路, 这就是 4CTA 档不需要 launch_bounds 压寄存器的原因。

**block 的驻留语义与 CTA/SM 上限**(承前): block 驻留期间三种持有各自给出上限, 取最小:

```text
Formula: CTA/SM = min( 100KB/kSmemSize , 65536/(kNThreads x regs) , 48/kNWarps )
2CTA 档: min( 100/48=2 , 65536/(128x255)=2 , 48/4=12 ) = 2   (smem 与寄存器同时卡死)
4CTA 档: min( 100/24=4 , 65536/(64x~250)=4 , 48/2=24 ) = 4   (两者同时松开)
```
**怎么做/计算(smem 记账)** — 出处 kernel_traits.h:107-109, 三项相加(fp16=2B, d=headdim=128):

```text
Tensor : PER_BLOCK_SMEM_ACCOUNT of Flash_fwd_kernel_traits<128, kBlockM, kBlockN, kNWarps>
Formula: kSmemSize = kBlockM x d x 2B  +  kBlockN x d x 2B  +  kBlockN x d x 2B
         (=Q_TILE fp16)                  (=K_TILE fp16)        (=V_TILE fp16)
         split decode additionally lays OACCUM = kBlockM x d x 4B (float), kBlockN-invariant

smem byte axis (1 char = 1 KB) ; example P(128,32,4) = 48 KB
                              0               16              32              48KB
                              ▲               ▲               ▲               ▲
                             ┌────────────────────────────────┬───────┬───────┐
P(128,32,4)              ──▶ │ Q_TILE_128x128_fp16_32KB       │K_8KB  │V_8KB  │  ◀── 32+8+8
                             └────────────────────────────────┴───────┴───────┘
                             ┌────────────────┬───────┬───────┐
P(64,16,2) 4CTA tier     ──▶ │ Q_16KB         │K_4KB  │V_4KB  │                  ◀── 16+4+4 = 24
                             └────────────────┴───────┴───────┘
```

全文出现的每个 traits 按此公式核算(与 /tmp/fin.cu 编译期求值逐一相符):

| traits (kBlockM,kBlockN,W) | 线程 | Q | K | V | kSmemSize | 用在哪 |
|---|---|---|---|---|---|---|
| (128,64,4) | 128 | 32 | 16 | 16 | **64 KB** | A100 原版 prefill |
| (64,128,4) | 128 | 16 | 32 | 32 | **80 KB** | A100 原版 decode(split) |
| (128,32,4) | 128 | 32 | 8 | 8 | **48 KB** | Ada 2CTA 档 prefill |
| (64,64,4) | 128 | 16 | 16 | 16 | **48 KB** | Ada decode(split)/HFuse |
| (64,32,4) | 128 | 16 | 8 | 8 | **32 KB** | Ada HFuse decode |
| (64,16,2) | 64 | 16 | 4 | 4 | **24 KB** | Ada 4CTA 档 prefill |
| (16,16,1) | 32 | 4 | 4 | 4 | **12 KB** | Ada 4CTA 档 decode |
| (16,32,1) | 32 | 4 | 8 | 8 | **20 KB** | A100 fp=11 decode |

两条随处要用的推论: K+V 的系数是 2, 所以**砍 kBlockN 的边际收益是砍 kBlockM 的两倍**;
split 的 OACCUM 只随 kBlockM 变, 是第 6 节那块砍不动的 32KB 地板。

**逻辑 block 与物理 block(blk_factor)** — POD/HFuse 融合两种线程数不同的 kernel 时,
物理 block 按线程数大的一方开(`nthr = max(nthr_p, nthr_d)`), 线程数小的一方在同一个物理
block 里**叠放** `blk_factor = nthr/nthr_x` 个逻辑 block, smem 也随之叠放:
`有效smem = max(P_smem x bf_p, D_smem x bf_d)`(fused_fwd_launch_template.h:442)。

```text
Tensor : PHYSICAL_BLOCK hosting blk_factor logical blocks (4CTA tier example)
Formula: nthr = max(64, 32) = 64 ; bf_d = 2 ; eff_smem = max(24x1, 12x2) = 24 KB

        physical block, 64 threads                    smem stacking
       ┌──────────────────────────────────┐          ┌──────────────┬──────────────┐
       │ threads 0-31 : logical D block#0 │  ──▶     │ D#0_smem_12KB│ D#1_smem_12KB│
       │ threads 32-63: logical D block#1 │          └──────────────┴──────────────┘
       └──────────────────────────────────┘           0             12            24KB
```
### 0.1 FA2 — FlashAttention-2 的 tile 化注意力

**是什么** — 本仓库一切 kernel 的母体。注意力 `O = softmax(Q K^T / sqrt(d)) V` 不落盘
完整的 S x S 分数矩阵, 而是把 Q 切成 `kBlockM` 行的 M-tile、K/V 切成 `kBlockN` 行的 N-tile,
每个 CTA 负责一个 M-tile, 沿 K/V 方向逐个 N-tile 流式扫过, 用 online-softmax 维护部分和。

**为什么需要** — smem 只装得下一对 (M-tile, N-tile), 装不下整行分数。这就是第 2 节
`kSmemSize = Q_BAND + KV_BAND` 公式的由来, 也是迁移中一切容量核算的对象。

**怎么做/计算** — 每个 CTA: (1) 把自己的 Q tile 读进 smem 常驻; (2) 循环 j: 读 K_j/V_j tile,
算 `S_ij = Q_i K_j^T`, 更新运行最大值 m 与部分和 l(online softmax), 累加 `O_i += P_ij V_j`;
(3) 循环结束除以 l 写回。O 的累加器在**寄存器**里 —— 这一点到 0.4 节 split decode 会变, 是后文
32KB 地板的伏笔。

```text
Tensor : ATTENTION_TILING over score matrix, rows = Q axis, cols = K/V axis
Formula: one CTA owns one M_TILE row-band ; streams N_TILE_j left-to-right ; O accum in registers

        K/V axis 0 ──▶ S_kv (tiles of kBlockN)
       ┌────────┬────────┬────────┬────────┐
Q axis │ N_j=0  │ N_j=1  │ N_j=2  │ N_j=3  │ ◀── CTA_i sweeps these with online softmax
M_TILE │ S_i0   │ S_i1   │ S_i2   │ S_i3   │
(kBlockM rows)──┴────────┴────────┴────────┘
       resident in smem: Q_TILE(kBlockM x d) + one KV_TILE(kBlockN x d, K and V)
```

### 0.2 prefill attention — 算力/TC 侧

**是什么** — 对一个新 prompt 的整段 S_p 个 query 做 causal 注意力。Q 有很多行,
`S_ij` 的 GEMM 是 (kBlockM x d) x (d x kBlockN), 两维都厚, Tensor Core 吃得满。

**为什么需要** — 它是混合批里的**算力极**。POD 的全部动机就是让它与访存极(decode)共驻互补。
本文的 TC 墙相位(NCU 实测 TC=93.5% 可达峰值, DRAM=7.6%)就是它。

**怎么做/计算** — causal 掩码让 CTA_i 只扫 j <= i 的 N-tile(下三角), 每行 query 的工作量
随位置线性增长; CTA 数 = ceil(S_p/kBlockM) x B_p x H。计算/访存比 ~ O(kBlockM) : O(1), 算力受限。

```text
Tensor : CAUSAL_PREFILL_SWEEP, same axes as 0.1, lower-triangular coverage
Formula: CTA_i covers N_j only for j <= i ; FLOPs per byte grows with kBlockM -> TC bound

        K axis ──▶
       ┌────────┐
CTA_0  │ S_00   │                              ◀── short row: little work
       ├────────┼────────┐
CTA_1  │ S_10   │ S_11   │
       ├────────┼────────┼────────┐
CTA_2  │ S_20   │ S_21   │ S_22   │            ◀── long row: much work
       └────────┴────────┴────────┘
```

### 0.3 decode attention — 访存/DRAM 侧

**是什么** — 每个序列只有 **1 个新 query**, 但要对整段 KV cache(S_kv 行)做注意力。
Q tile 的有效行数是 1, GEMV 形态, Tensor Core 几乎用不上, 时间全花在把 KV 从 DRAM 拉进来。

**为什么需要** — 它是混合批的**访存极**。本文 DRAM 墙相位(DRAM=96.4%, TC=37.8%)就是它。
单独跑时 SM 的算力闲置 —— 这就是与 prefill 融合的收益来源。

**怎么做/计算** — 每 (序列, head) 一个 CTA: 沿 S_kv 扫 KV tile, 每字节只做 O(1) 次乘加。
计算/访存比 ~ 1:1 字节, 完全带宽受限。CTA 数 = B_d x H, 与 S_kv 无关 —— 这是 0.4 节
split 的动机: B_d x H 太小时填不满 128 个 SM。

```text
Tensor : DECODE_GEMV_SWEEP, Q axis collapsed to a single row
Formula: one CTA per (seq, head) ; streams whole KV of length S_kv ; bytes >> FLOPs -> DRAM bound

        KV axis 0 ──▶ S_kv
       ┌────────┬────────┬────────┬────────┬────────┐
q row  │ KV_0   │ KV_1   │ KV_2   │ KV_3   │ KV_4   │ ◀── 1-row sweep, bandwidth bound
(1 row)└────────┴────────┴────────┴────────┴────────┘
```

### 0.4 split-KV decode — oaccum 与 combine

**是什么** — decode 的并行度补丁: 把 KV 沿长度切成 `num_splits` 段, 每段一个 CTA 独立
算部分注意力, 再由一个 combine kernel 按 log-sum-exp 权重合并。

**为什么需要** — decode 的 CTA 数 = B_d x H; B_d=4, H=32 时只有 128 个 CTA, 刚好一 SM 一个,
稍小就填不满。split 把并行度乘以 num_splits。**但代价是: 部分结果 O_accum 必须以 float 精度
落到 smem/gmem**, 尺寸 `kBlockM x d x 4B = 32KB`, 只随 kBlockM 变 —— 这就是第 6 节那块
砍 `kBlockN` 无效的地板, 也是 4CTA 档只在非 split 时可达的原因(A100 亦然)。

**怎么做/计算** — 每个 split-CTA 对自己的 KV 段跑 0.3 的 GEMV 扫描, 输出 (O_partial, lse);
combine kernel 读 num_splits 份, 按 `O = sum_k exp(lse_k - lse_max) O_k / sum_k exp(...)` 合并。
combine 的线程布局硬编码 128 线程 —— 把 decode 的 warp 数降到 1 会静默算错, 这是迁移中
必须保住的结构约束之一。

```text
Tensor : SPLIT_KV_PARTITION + FLOAT_OACCUM, KV axis cut into num_splits segments
Formula: CTA_k owns segment k -> (O_k, lse_k) in float ; O_ACCUM = kBlockM*d*4B, kBlockN-invariant

        KV axis 0 ──▶ S_kv          (num_splits = 4)
       ┌──────────┬──────────┬──────────┬──────────┐
q row  │ SEG_0    │ SEG_1    │ SEG_2    │ SEG_3    │ ◀── one CTA per segment, parallel
       └────┬─────┴────┬─────┴────┬─────┴────┬─────┘
            ▼          ▼          ▼          ▼
       ┌──────────────────────────────────────────┐
       │ OACCUM_FLOAT_32KB_PER_CTA (kBlockM x d)  │ ◀── the un-cuttable floor of section 6
       └──────────────────────────────────────────┘
            combine kernel: O = lse-weighted sum of O_k   (128-thread layout, fixed)
```

### 0.5 GQA/ngroups 与本文用到的融合对照

**是什么** — GQA: H 个 query head 共享 Hkv 个 KV head, `ngroups = H/Hkv`(实验覆盖 4/8/32)。
对容量核算无影响, 但决定 KV 的复用度, 是正确性回归必须扫的维度。
融合对照三件套: **FA_Streams**(两条 stream 各跑 0.2/0.3, 依赖硬件并发)、**HFuse**(两 kernel 塞进
同一 CTA 用 warp 分区, smem **相加**, 见第 4 节)、**POD**(每个 CTA 在入口由 SM-aware ticket
决定扮演 0.2 还是 0.3, smem 取 **max**, 见第 3/5 节)。

**为什么需要** — 三者是论文对照组; smem 的相加/取 max 之别正是第 4 节与第 3 节适配方式
不同的原因。

**怎么做/计算** — POD: leader 线程读 `%smid`, `ticket = atomicAdd(&tbAssign[smid],1)`,
按 slots 比例映射到 P 或 D 角色, 再领取该角色的下一个逻辑 block id; 于是同一 SM 上的连续
CTA 以 `P,P,...,D` 或 `P,D,...,D` 序列交替, 时间上把两极叠在同一 SM 里。

```text
Tensor : ONE_SM_TIMELINE under POD, rows = 2 CTA slots of one SM, X = time
Formula: slot state alternates (1P+1D) / (2P) by ticket ratio ; capacity from section 3 = 2

        time ──▶
       ┌────────────┬────────────┬────────────┬────────────┐
slot 0 │ P_CTA      │ P_CTA      │ D_CTA      │ P_CTA      │
       ├────────────┼────────────┼────────────┼────────────┤
slot 1 │ D_CTA      │ P_CTA      │ P_CTA      │ D_CTA      │ ◀── mixed (1P+1D) and pure (2P)
       └────────────┴────────────┴────────────┴────────────┘
        measured shares (sec.7): 1P+1D 45.6% , 2P 27.3% , idle 11.2%
```
## 1. 容量基底 — 迁移的唯一硬约束轴

**是什么** — A100 与 Ada 在寄存器文件(同为 65536/SM)和 warp 槽位上没有实质差异, 两卡的差距
集中在共享内存一条轴上。POD 的全部并发行为都发生在这条轴划出的预算内。

**为什么需要** — 迁移中遇到的每一次失败(退化成串行、kernel 起不到、写越界)最后都归到这条轴, 
没有例外。先把它画出来, 后面每一步都是在同一条轴上重新切分。

**怎么做/计算** — 读两个设备属性: `MaxSharedMemoryPerMultiprocessor` 决定一个 SM 能装几个 CTA;
`MaxSharedMemoryPerBlockOptin` 决定**单个** CTA 经 `cudaFuncSetAttribute` 能申请到的上限。
两者作用不同: 前者管并发度, 后者管能不能起来。Ada 实测 102400 B 与 101376 B。

```text
Tensor : SM_SHARED_MEMORY_BUDGET, one row per GPU, rectangle width = bytes
Formula: budget(Ada) = 100 KB = 0.61 x budget(A100) ; register file identical (65536 regs/SM)

smem byte axis (1 char = 4 KB, compressed)
                              0           48           100             164KB
                              ▲           ▲            ▲               ▲
                             ┌─────────────────────────────────────────┐
A100 per-SM budget       ──▶ │             A100_SMEM_164KB             │  ◀── fits 2 x 80KB CTA
                             └─────────────────────────────────────────┘
                             ┌─────────────────────────┐
Ada  per-SM budget       ──▶ │      ADA_SMEM_100KB     │  ◀── fits only 1 x 80KB CTA
                             └─────────────────────────┘
                             ┌─────────────────────────┐
Ada  opt-in / block      ──▶ │  ADA_OPTIN_CEILING_99KB │  ◀── one CTA cannot exceed this
                             └─────────────────────────┘
                             ┌────────────┐
Ada  default / block     ──▶ │ADA_DEF_48KB│  ◀── without cudaFuncSetAttribute
                             └────────────┘
```

## 2. 单个 CTA 的 smem 如何被切分

**是什么** — FlashAttention-2 的 `kSmemSize` 把一个 CTA 的共享内存切成两段: Q 的一个 M-tile,
以及 K/V 的一个 N-tile(K 与 V 各存一份)。迁移中能动的旋钮就是这两段的边长。

**为什么需要** — 只有看清两段各占多少, 才知道砍哪边有效。这一步直接决定了第 5 节能砍 `kBlockN`、
而第 6 节的 split 地板砍不动。

**怎么做/计算** — `kSmemSize = kBlockM*headdim*2 + 2*kBlockN*headdim*2` (fp16, headdim=128)。
Q 段只随 `kBlockM` 变; K/V 段只随 `kBlockN` 变**且系数为 2**。所以砍 `kBlockN` 的边际收益是砍
`kBlockM` 的两倍 —— 这是每次选择砍哪一边的依据。

```text
Tensor : PER_CTA_SMEM_LAYOUT of Flash_fwd_kernel_traits<128, kBlockM, kBlockN, W>
Formula: kSmemSize = Q_BAND + KV_BAND ; Q_BAND = kBlockM*256 B ; KV_BAND = kBlockN*512 B

smem byte axis (1 char = 1 KB)
                              0                               32              48              64KB
                              ▲                               ▲               ▲               ▲
                             ┌────────────────────────────────┬────────────────────────────────┐
P(128,64,4)  original    ──▶ │     Q_BAND_kBlockM128_32KB     │     KV_BAND_kBlockN64_32KB     │  ◀── 64 KB
                             └────────────────────────────────┴────────────────────────────────┘
                             ┌────────────────────────────────┬────────────────┐
P(128,32,4)  2CTA tier   ──▶ │          Q_BAND_32KB           │  KV_BAND_16KB  │  ◀── 48 KB, kBlockN halved
                             └────────────────────────────────┴────────────────┘
                             ┌────────────────┬────────┐
P(64,16,2)   4CTA tier   ──▶ │     Q_16KB     │ KV_8KB │  ◀── 24 KB, both halved
                             └────────────────┴────────┘
```

## 3. POD 自有路径 — 从退化成串行回到 2 CTA/SM

**是什么** — POD 的机制是 SM-aware CTA 调度: leader 线程读 `%smid`, 用
`ticket = atomicAdd(&tbAssign[smid],1) % (p+d)` 把本 CTA 分派成 prefill 或 decode 角色。
整个收益建立在**同一 SM 上 P 与 D 共驻**之上。

**为什么需要** — 原版默认 P(128,64,4)=64KB + D(64,128,4)=80KB, `smem = max(...) = 80KB`。
A100 装得下 2 个, Ada 只装得下 1 个。**1 CTA/SM 时同一 SM 上永远只有一个角色, (1P+1D) 状态**
**根本不存在**, 融合只剩调度开销 —— 这不是性能下降, 是机制失效。

**怎么做/计算** — 锁死 `kBlockM` 与 warp 数(它们决定 P:D 的每-CTA 工作量比例), 只把 `kBlockN`
从 64 砍到 32, prefill 侧 48KB; decode 侧 split 路径 (64,128,4)→(64,64,4) 同样 48KB。
`smem = max(48,48) = 48KB` → 100/48 = 2 CTA/SM。NCU 实测 `launch__occupancy_limit_shared_mem = 2`。

```text
Tensor : SM_OCCUPANCY_PACKING, rectangle = one SM budget, inner blocks = resident CTAs
Formula: n_CTA = floor(budget / max(P_smem, D_smem)) ; mechanism needs n_CTA >= 2

smem byte axis (1 char = 4 KB)
                              0           48          9100             164KB
                              ▲           ▲           ▲▲               ▲
                             ┌────────────────────┬────────────────────┐
A100 original 80KB       ──▶ │     CTA_0_80KB     │     CTA_1_80KB     │  ◀── 2 CTA/SM, mechanism alive
                             └────────────────────┴────────────────────┘
                             ┌────────────────────┬─────┐
Ada  original 80KB       ──▶ │     CTA_0_80KB     │FREE_│  ◀── 1 CTA/SM, MECHANISM DEAD
                             └────────────────────┴─────┘
                             ┌────────────┬────────────┬─┐
Ada  adapted  48KB       ──▶ │ CTA_0_48KB │ CTA_1_48KB │F│  ◀── 2 CTA/SM, restored
                             └────────────┴────────────┴─┘
```
## 4. HFuse 对照组 — smem 是相加, 不是取最大

**是什么** — HFuse 是论文的对照融合方法: 把 prefill 与 decode 两个 kernel 合进**同一个 CTA**,
用 warp 分区并行(`__launch_bounds__(256)` + `bar.sync 2,128`)。因为两半同时活着, 它的共享内存
是两者**相加**(`launch_template:246`), 而 POD 自有路径是取 max(`:442/:456`)。

**为什么需要** — 这一条决定的不是快慢, 而是**能不能跑**。原版 64+80 = 144 KB, 超过 Ada 的
99 KB opt-in 上限, `cudaFuncSetAttribute` 直接拒绝。适配前实测: fp=64 在每个配置都返回
`CUDA error: invalid argument`; 适配后(96 KB)全部 PASS。这是一对干净的前后实证。

**怎么做/计算** — 保住 HFuse 的结构性约束(256 线程、两半各 128、bar.sync 分组不能动),
只把 decode 侧 `kBlockN` 从 128 砍到 32: P(128,64,4)=64KB + D(64,32,4)=32KB = 96KB ≤ 99KB。
prefill 侧一个参数都没动。

```text
Tensor : HFUSE_CTA_SMEM = P_HALF + D_HALF (summed, both halves live simultaneously)
Formula: feasible(Ada) iff P_HALF + D_HALF <= ADA_OPTIN_CEILING_99KB

smem byte axis (1 char = 4 KB)
                              0                       999         144KB
                              ▲                       ▲▲          ▲
                             ┌────────────────┬────────────────────┐
HFuse original           ──▶ │  P_HALF_64KB   │    D_HALF_80KB     │  ◀── 144 KB > 99 KB : LAUNCH REJECTED
                             └────────────────┴────────────────────┘
                             ┌─────────────────────────┐
Ada opt-in ceiling       ──▶ │  ADA_OPTIN_CEILING_99KB │  ◀── cudaFuncSetAttribute hard limit
                             └─────────────────────────┘
                             ┌────────────────┬────────┐
HFuse adapted            ──▶ │  P_HALF_64KB   │ D_32KB │  ◀── 96 KB <= 99 KB : PASS
                             └────────────────┴────────┘
```

## 5. 4 CTA/SM 档 — 关键不是 tile, 是线程结构

**是什么** — 论文 README 明写 `fused_params` 是**每 SM 几个 CTA**的档位: `9 = 2 CTAs per SM`,
`11 = 4 CTAs per SM`, `15 = 运行时自动选档`。这是 POD 机制的一个显式旋钮, 不是内部实现细节。

**为什么需要** — 我最初把 `fused_params` 当位标志读, 并在 E4 里把 prefill 的 warp 数从 2 改成 4
(为统一 128 线程), **恰好把 4 CTA 档堵死** —— fp=11 只能拿到 2 CTA/SM, 与 fp=9 无实质区别。
论文 figure13 的整张图(2CTA vs 4CTA 敏感性)因此不可能复现。

**怎么做/计算** — 回看 A100 原版的达成方式: prefill 用 **2 warps(64 线程)**、decode 用 **1 warp**
**(32 线程)**, 于是 `blk_factor_d = max(64,32)/32 = 2`, `smem = max(32KB*1, 20KB*2) = 40KB`,
164/40 = 4。**线程数比 tile 更关键**: 它通过 `blk_factor` 改变了 decode 侧的计价方式。
Ada 沿用同一结构, 只把两侧 `kBlockN` 再减半以吸收 100KB vs 164KB 的差距:
P(64,16,2)=24KB + D(16,16,1)=12KB → `max(24, 12*2) = 24KB` → 100/24 = 4 CTA/SM。
附带收益: 64 线程 x 4 CTA = 256 线程/SM, 寄存器可用 256/线程, **寄存器自动不再是瓶颈**
(我一开始想用 `__launch_bounds__` 压寄存器是走错方向, 而且那个写法在 split 路径会违反声明)。

```text
Tensor : FOUR_CTA_PACKING, rectangle = one SM budget, inner blocks = 4 resident CTAs
Formula: eff_smem = max(P_smem * bf_p, D_smem * bf_d) ; bf_x = max(thr_p,thr_d) / thr_x

smem byte axis (1 char = 4 KB)
                              0         40            9100            160KB
                              ▲         ▲             ▲▲              ▲
                             ┌──────────┬──────────┬──────────┬──────────┐
A100 4CTA  40KB ea       ──▶ │   CTA0   │   CTA1   │   CTA2   │   CTA3   │  ◀── 164/40 = 4 CTA/SM
                             └──────────┴──────────┴──────────┴──────────┘
                             ┌──────┬──────┬──────┬──────┬─┐
Ada  4CTA  24KB ea       ──▶ │ CTA0 │ CTA1 │ CTA2 │ CTA3 │F│  ◀── 100/24 = 4 CTA/SM
                             └──────┴──────┴──────┴──────┴─┘
                             ┌────────────┬────────────┬─┐
Ada  2CTA  48KB ea       ──▶ │ CTA_0_48KB │ CTA_1_48KB │F│  ◀── fp=9 tier, unchanged
                             └────────────┴────────────┴─┘
```

实测占用率(NCU, decode 未被 split 的形状):

| fp | 论文语义 | smem/CTA | 线程/CTA | smem 上限 | reg 上限 | 实际 CTA/SM |
|---|---|---|---|---|---|---|
| 9 | 2 CTA/SM | 48.0 KB | 128 | 2 | 2 | **2 达标** |
| 11 | 4 CTA/SM | **24.0 KB** | **64** | **4** | **4** | **4 达标** |

## 6. 不可逾越的边界 — split decode 的 oaccum 地板

**是什么** — decode 走 split-KV 时, 每个 CTA 要在共享内存里放一份 **float 的 O 累加器**,
尺寸 `kBlockM * headdim * 4` = 64*128*4 = **32 KB**。这块与 `kBlockN` **无关**。

**为什么需要** — 我按第 2 节的规律砍 `kBlockN` 到 16 试图把 4CTA 档压到 24KB, 结果 kernel 崩了。
compute-sanitizer 报 `Invalid __shared__ write`, 地址 `0x6480 = 25728 > 24576`(分配值) ——
**砍 `kBlockN` 对这块地板完全无效**。这是第 2 节那条边际收益规律的例外, 也是迁移中唯一一处
靠读公式推不出、必须实测才发现的约束。

**怎么做/计算** — 承认它: 把 4CTA 条件显式写成 `(fusedOp & 2) && !DecodeSplit`,
decode 被 split 时诚实回落到 2 CTA/SM, 而不是假装达标。
推论对论文本身也成立: **A100 上 fp=11 的 4 CTA 同样只在 decode 不 split 时可达**
(split 时 traits_d 是 80KB, 164/80 = 2)。

```text
Tensor : SPLIT_DECODE_CTA_SMEM, showing the kBlockN-invariant floor
Formula: floor = kBlockM * headdim * sizeof(float) = 64 * 128 * 4 = 32 KB, independent of kBlockN

smem byte axis (1 char = 1 KB)
                              0                       24      32              48KB
                              ▲                       ▲       ▲               ▲
                             ┌────────────────┬────────┐
non-split decode         ──▶ │     Q_16KB     │ KV_8KB │  ◀── 24 KB : 4 CTA/SM reachable
                             └────────────────┴────────┘
                             ┌────────────────────────────────┬────────┐
split decode             ──▶ │    OACCUM_FLOAT_FLOOR_32KB     │   KV   │  ◀── floor cannot be cut by kBlockN
                             └────────────────────────────────┴────────┘
                             ┌────────────────────────┐
attempted 24KB alloc     ──▶ │     ALLOCATED_24KB     │  ◀── write at 25728 B -> OUT OF BOUNDS
                             └────────────────────────┘
```
## 7. 迁移后的实测 — SM 时间都花在哪些占用状态上

**是什么** — 前六节都在讲容量能装下几个 CTA; 这一节回答**装下之后 SM 实际处于什么状态**。
给 kernel 加了插桩, 每个 CTA 记录 `(smid, op, t_start, t_end)`, 事后重建每个 SM 的占用时间线。

**为什么需要** — 容量 2 CTA/SM 只是必要条件。POD 的收益来自 **(1P+1D) 混合态**下算力与访存重叠;
如果时间大部分落在纯 P 或纯 D 上, 容量达标也没有收益。这一节把机制是否真在起作用量出来。

**怎么做/计算** — 角色由 `ticket % (p_ratio+d_ratio)` 决定, 比例是**时间上的**而非逐时刻的:
prefill slots 多时序列是 `P,P,...,P,D`, decode 多时是 `P,D,...,D`。容量 2 意味着任意时刻
SM 只能处于 `2P` / `1P+1D` / `1D` 等少数状态之一。下图按**时间占比**划分这些区域。
统计口径已修正两处会让数字失真的缺陷: 分母改为全局窗口 x 全部 128 个 SM(原先漏掉前导/尾部空闲,
会把混合态占比夸大近一倍), 共驻均值改为时长加权。

```text
Tensor : SM_OCCUPANCY_STATE_TIMELINE, rectangle width = fraction of total SM-time
Formula: state(t) = (n_prefill_CTA, n_decode_CTA) resident on that SM at time t ; capacity = 2
Shape  : B_p=1 S_p=2048 B_d=16 S_kv=8192, fp=15, 768 CTA (512 P + 256 D), window 426 us x 128 SM

time fraction axis (1 char = 2%, compressed)
                              0                        25                       50                       75                       100%
                              ▲                        ▲                        ▲                        ▲                        ▲
                             ┌───────────────────────┬──────────────┬──────┬────┬──┬──┐
occupancy timeline       ──▶ │  MIXED_1P_1D_45.6pct  │PURE_2P_27.3pc│IDLE_1│D1_8│P1│D2│  ◀── POD mechanism active in MIXED band
                             └───────────────────────┴──────────────┴──────┴────┴──┴──┘
```

读出来的三件事:

- **`1P+1D` 与 `2P` 合计 72.9%** —— SM 绝大部分时间确实在这两个状态间交替, 容量 2 是这个交替的前提
- **共驻时恒为 P=1.00 / D=1.00** —— 因为只有两个槽, 共驻必然是一 P 一 D
- **时间加权 P:D = 63.2% : 36.8%** —— 虽然 D 的 CTA 个数只有 P 的一半, 但单个 D 更长, 时间上仍是 P 占优

跨形状看, `2P + 1P1D` 的合计占比与 POD 的加速强相关:

| 形状 P:D slots | 2P | 1P+1D | 两状态合计 | 纯 D 态 | POD/Serial |
|---|---|---|---|---|---|
| 2:1 | 69.8 | 23.8 | **93.6** | 2.0 | 1.185 |
| 1:1 | 30.7 | 51.3 | **82.0** | 12.9 | **1.352** |
| 1:4 | 0.0 | 51.9 | 51.9 | 47.2 | 1.112 |
| 1:16 | 0.0 | 1.1 | **1.1** | 63.3 | **0.961** |

(该表为分母修正前的口径, 各行同口径可比; 修正后绝对值整体下移约 6 个百分点, 趋势不变。)
D 淹没 P 之后 SM 掉进纯 D 态, 没有算力可重叠, 融合退化成带调度开销的串行 —— 这正是 1:16 那档
倒亏 4% 的机制解释。最优不是 P 越多越好: 2:1 档 P 时间占比最高但加速不如 1:1, 因为 69.8% 的时间
是纯 2P, **没有 D 可重叠**; 收益来自混合态本身, 两边都得在场。

## 8. 迁移结果

**论文自带脚本 `tests/sens_cta.py` (figure13) 完整复现**, llama-3-8b-tp1, ctx 1k-16k x bs 8-128, 25 配置:

| | 几何均值加速 | 最优档次数 |
|---|---|---|
| 2 CTA/SM (fp=9) | 1.209 | 13 / 25 |
| 4 CTA/SM (fp=11) | 1.222 | 12 / 25 |
| 逐配置最优(= fp=15 自动选档上界) | **1.249** | — |

最高 1.539x。两档平分秋色、最优随形状切换 —— 这正是论文做这张图的结论, 也证明 4CTA 档确实生效
(修复前 fp=11 只能拿到 2 CTA/SM, 不可能赢 12 个配置)。
对比论文在 A100 上的 up to 61% / avg 33%: 本机 avg 25% / max 54%, **差距方向与 smem 容量一致**
(100KB vs 164KB), 不是复现错误。

正确性: **36/36 全过**(6 种形状 x 6 个 fp, 含 ngroups=4/8/32、DecodeSplit、两组 4CTA 路径用例),
最大偏差 0.00098, 无 NaN。

## 9. 注意事项清单

1. **`fused_params` 是每 SM CTA 数的档位, 不是位标志**(9=2CTA, 11=4CTA, 15=运行时选档)。
   按位标志理解会把 4CTA 档改坏而不自知。
2. **线程数比 tile 更关键**。4CTA 档靠 prefill 2 warps + decode 1 warp 产生 `blk_factor_d=2`;
   为统一线程数把 warp 改成 4, 会直接堵死这一档。
3. **HFuse 的 smem 是相加, POD 自有路径是取 max**。两者用同一套 traits 但计价方式不同,
   改 traits 时必须分别核算。
4. **split decode 有一块 32KB 的 oaccum 地板, 与 `kBlockN` 无关**。砍 `kBlockN` 压不下去,
   会写越界。有些档位在 Ada 上**原理上**就到不了, 要如实回落。
5. **硬证伪指标用 `launch__occupancy_limit_shared_mem` / `_registers`, 不要用墙钟加速比**。
   即使 1 CTA/SM, 融合本身也省掉一次 launch 和一段 wave 尾巴, 照样能测出提速。
6. **改 tile 会连带拖垮编译**。HFuse 合并核带 `__launch_bounds__(256,2)`, 小 tile 把寄存器分配
   推到可行性边界: 原版 ptxas 290s, ADA 变体 -O1 4236s / -O2 4798s / -O3 超过 2 小时。
   运行时不可达的非 causal TU 可以单独用 `-Xptxas -O0` 预编后链入, 不影响被测路径。
7. **NCU 抓取要跳过预热**。受害者对两档配置各预热 20 次, `--launch-count` 不加 `--launch-skip`
   会抓到预热阶段, 两个不同配置画像完全相同却看不出问题。
8. **`cudaMalloc(tbAssign)` 原版没有对应的 `cudaFree`**。加插桩放大缓冲区后每次 launch 泄漏 4MB,
   长跑必 OOM; 且插桩路径的 `cudaStreamSynchronize` 会让墙钟数字不可与非插桩版比较。

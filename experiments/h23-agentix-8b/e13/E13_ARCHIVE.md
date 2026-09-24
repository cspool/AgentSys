# E13 归档报告: 工具语义 KV 压缩(ToolKV)
2026-09-23 ~ 09-24 | GPU: 2x RTX 4090 | 状态: **封存**(核心创新撞车, 见 §5)

## 1. 定位与时间线
目标(用户/goal): 消融平均 >=30% 提升且有创新性, 主题 = tool use 的 KV 压缩(KV 语义)。
v1(7臂基线) -> v2(平滑+护盾) -> v3(问题导向评分) -> v4(极化判决) -> v5(按需换页)
-> v6(严格判官) -> local(单跳族) -> 8B(双卡, 判官/自检索规模验证) -> J-fix -> I-去实体。

## 2. 实验配置
- 模型: Qwen3-1.7B(机制探索) / Qwen3-8B(场景主力, ModelScope 下载, 双卡 device_map=auto)
- 任务族: HotpotQA distractor(多跳, n=60, gold按 early/mid/late 分层注入10段"工具返回")
  / 本地 NIAH 型单跳(ShareGPT 干扰段+合成 briefing, n=60)
- Episode 结构: head(系统+问题) + 10x[工具跨度 prefill + 消费注生成(crop)] + 终局答案
- 评分: 消费注(问题导向)对跨度 token 注意力池化(eager attention); 全局累计; prefill 自注意(G臂)
- 消融臂: A 全KV / B 消费分按跨度topρ / B2 +maxpool平滑 / C 位置首尾 / D 随机
  / E 消费分全局预算 / E2 平滑 / G 通用H2O(prefill注意力) / H E+近期护盾(末2跨度全保)
  / I 极化(判无关留存根) / J 语义按需换页(全存根+答案时模型点名换入) / F 全丢+分数换入
- 指标: 答案质量(归一化包含), 保留KV token, 定预算(8GB/5GB)合成KV批量decode吞吐实测
- 基建: pass1 按 episode 缓存(键=模型+提示词hash), 增量 JSONL 断点续跑

## 3. 结论总表
### 3.1 前提(H1, n=12): 消费即冷却 2.6x; 答案轮 gold/干扰 4.3x;
capture@10%: 消费分37% vs 随机9%/位置23%。
### 3.2 质量-显存前沿
| 配置 | 质量Δ | 显存降 | 定预算吞吐 |
| 单跳 1.7B H@0.1 | 0pp | -65% | +91% |
| 单跳 8B E@0.25 / H@0.25 / I | 0pp | -67/-52/-50% | +105~183% |
| 多跳 1.7B I宽判 | -3pp | -12% | +31% |
| 多跳 8B E@0.25 | -7pp | -70% | +183% |
| 多跳 8B I(极化) | -8pp | -50% | +105% |
| 多跳 8B J(按需换页) | -25pp | -92% | +576% |
30%目标(<=5pp口径): 达成(入选点 +31~+183%)。多跳最优 -7pp 未进窗。
### 3.3 吞吐实测(H3, 合成KV批量decode)
1.7B@8GB: 238/465/770/1554 tok -> 5171/3331/2562/1095 tok/s;
8B@5GB: 124/466/773/1554 -> 3534/1480/1073/523 tok/s。
### 3.4 压缩成本(H4): 手术1.4ms+池化13.4ms=15ms = 最短工具等待窗1.5%(藏入等待窗成立)。
### 3.5 规模效应(1.7B->8B): 判官拒判 15%->63%(召回恒98%); J自检索 gold召回 35%->67%;
严格判官 ROC 平缓(98/15->92/26), 提示词工程不解决判决质量。

## 4. 机理发现与负结果
1. **毒页/干扰实体抢答(独有)**: 注意力保留在无关跨度上恰保实体名、丢免责上下文(6/6错例);
   删除被判无关跨度后质量可超全KV(early I=70%>A=65%) => 压缩可去毒提质。
2. 跨度级注意力排名不可靠+长度偏置(top-3双中30%; 原始分偏early, xL校准过矫偏late)。
3. token散选破坏实体完整性; maxpool平滑无效(v2实证)。
4. 1.7B 无存根自检索(56/60固定点名1,2,3); 8B 复活(67%)但"全程只见存根"无法靠
   答案时换入补回整合状态(J-fix后仍40% vs A65%)。
5. 去实体存根无增益 => 多跳残余缺口是"丢弃被判无关上下文"的本征代价。

## 5. 新颖性对抗核查判决(2026-09-24)
撞车: arXiv 2608.00902(在线轮压缩+延迟压缩+三类proxy query, -0.5pp@3.3x吞吐)
与 CommitKV 2608.07855(commit生命周期+配对删除效果+16token页+联合测试, -4.1pp@5x显存5.62x吞吐)。
逐条: 消费触发=做过 / 护盾=做过(延迟压缩) / 极化=被配对测量超越 / 按需换页=被Quest/InfLLM占据且我们为负结果。
**独立成文不足; 残余立足点 = 毒页机理(§4.1) + CommitKV休眠保护(低->低不驱逐)恰好保毒页的攻击面。**
过程教训: 立项检索词族缺 compaction/commit/lifecycle, 两文立项前已存在; 对抗核查须同义词族扫描+近期arXiv巡检, 且在投入实验前完成。

## 6. 代码与数据清单(experiments/h23-agentix-8b/e13/)
- toolkv_ablation.py 主harness(全臂+缓存+断点+多模型+双卡)
- toolkv_h1_probe.py(H1) / toolkv_surgery.py(cache手术自测) / toolkv_h3_throughput.py+_8b(吞吐)
- toolkv_h4_cost.py(压缩成本) / verify_prefix_probe.py(B3遗留) / analyze_e13.py / final_summary.py
- 结果: h1_results.json, ablation_{v1..v6}, ablation_local, ablation_8b_{hotpot,local,j2,i2}(.jsonl)
- pass1_cache/(遍1缓存, 键=数据_集号_模型+提示词hash)
坑备忘: 样本复算须复刻 random.Random(7).shuffle; pkill -f 自杀(用 kill -0 PID);
git -C 下相对pathspec按仓库根解析; 双卡下手术索引须逐层 to(lyr.keys.device)。

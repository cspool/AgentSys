# 热词组合探索矩阵(2026-09-24) —— 寻找新问题/新场景/新方法/新策略
方法: 热词枚举(联网+本地库题录) x 资产可达性 x 先审后立。

## 一、热词面(联网, 2026)
体系结构: chiplet/UCIe 3.0, CXL 3.1/4.0(内存池化, **CXL KV cache 服务器 11TB**), 内存解耦,
存内计算, model-native 架构, 次二次注意力解耦。
AI系统: agentic serving 状态化(XPerf基准/2608.15127刻画/KAIROS能耗/SmoothAgent/HexAGenT),
test-time reasoning(thinking budgets), **世界模型实时化**(Genie3 24fps/Oasis/Matrix-Game 2.0开源),
视频生成=世界模型(8-32x LLM算力, >480p转访存瓶颈), agentic 能耗危机, RL infra(投机RL)。
(本地库题录词频: 待后台枚举返回后补)

## 二、组合候选与预审判决
### C1 自干扰 computer-use agent(闭环) —— **最有希望, 初判空隙**
组合: computer-use/GUI agent x 端侧 x 共驻仲裁。
新问题: agent 在其操作的同一台机器上推理 —— 推理负载扰动它自己的观测流
(推理慢->截图旧/UI时延变->动作错->重试->负载更高: 可测的不稳定螺旋);
agent 动作周期自带"观测截止期"预告(预告驱动第三落点)。
对质: GUI agent 领域全在准确率/模型侧(MobileExplorer/Ferret-UI Lite/BlueLM-GUI);
最近邻 OSDI'26 移动端渲染-LLM带宽争用控制(QoS视角, 无闭环无agent语义); EnerInfer能耗。
**闭环自干扰动力学 + 稳定性判据 无人做**。资产: E15/16全套+VLM本地。
风险: 需真桌面环境(可用 xvfb+真应用); 螺旋的可复现构造。
### C4 可中断推理(端侧让路) —— 弱, 缓行
对质: thinking budgets/checkpoint可靠性/FlowPrefill抢占粒度 碎片已密;
本质是 E14 临时化翻版到 reasoning。仅作 C1/C5 的机制组件。
### C5 双神经租户仲裁(世界模型渲染器 + agent LLM) —— **新鲜, 待深审**
组合: 神经游戏引擎(Oasis/Matrix-Game开源可跑) x agent LLM x 单卡。
新场景: "渲染"本身成为神经模型(帧率截止期落在生成模型上), 双神经租户;
世界模型 8-32x LLM 算力且访存瓶颈 => 与 LLM decode 的干扰结构全新。
对质初查: 全部命中为模型侧论文与基建博客, serving/调度侧空白。
风险: 世界模型在 4090 上的实时可行性(Matrix-Game 2.0 声称开源实时, 需验证); 深审未做。
### 其余格子速判
CXL x KV分层: 数据中心已占(CXL KV服务器商用化); 桌面类比=我们host阶梯, 已审。
能耗 x agentic: KAIROS 占。 RL rollout x 弹性: slime/miles生态+Prism风险, 缓。
dLLM serving: 资产不合, 缓。

## 三、下一步
1. 本地库题录词频落地后补热词面并复扫矩阵空格
2. C1 深审(移动端OSDI'26论文细读 + "self-interference/closed-loop" 专扫) -> 若存活, 设计最小螺旋复现实验
3. C5 深审(world model serving/scheduling 专扫 + Matrix-Game 2.0 4090 可行性)

# G3：Agent 应用全栈系统加速

## 方向

研究动态 Agent 程序从服务调度到 NPU tile 执行的端到端加速。Agentix 负责程序级调度，Agent.xpu 负责异构 flow/stage 调度，mllm、ATX、TISA 和 HPTPE 构成执行基础。

## 参考资料

- Agentix：<https://www.usenix.org/conference/nsdi26/presentation/luo>
- Agent.xpu：<https://arxiv.org/abs/2506.24045>
- Agent.xpu 实现参考：<https://github.com/xinming-wei/LLM.xpu>
- mllm：<https://github.com/UbiquitousLearning/mllm>
- HPTPE：<https://github.com/wqzustc/High-Performance-Tensor-Processing-Engines>
- Agentix 全文：/data3/paper_analysis/paper_secs/paper_20260824/Agentix An Efficient Serving Engine for LLM Agents as General Programs/
- Agent.xpu 全文：/data3/paper_analysis/paper_secs/paper_20260824/Agent.xpu Efficient Scheduling of Agentic LLM Workloads on Heterogeneous SoC/
- ATX、TISA 全文：/data3/paper_analysis/paper_secs/paper_isca26_full/

## 实现内容和目标

实现内容：

- Agentix：动态 Agent DAG、PLAS、ATLAS、attained service 和 critical path。
- Agent.xpu：HEG、reactive/proactive flow、Prefill/Decode 放置、batch、warmup 和抢占。
- mllm：增加模型算子 trace/simulator backend。
- ATX adapter：异步任务、stream、数据传输、prefetch、取消和完成。
- TISA simulator：算子到 tile lowering、RAW/WAR/WAW、ME/VE/DE 队列与动态发射。
- NPU 模型：HPTPE Matrix Engine、定制 VE/DE、SRAM、DMA 和 Ramulator2 DDR。
- 统一追踪 program→call→flow→task→tile→engine event。

实现目标：

- 打通至少一个动态 Agent DAG 的完整执行路径。
- 让程序优先级能够传递到异构 flow 和底层硬件事件，并可解释收益来源。
- ATX、TISA分别做组件验收，但不再作为独立最终方向。

## 实验内容和目标

实验内容：

- 逐层比较 FCFS、静态放置、Agent.xpu HEG、抢占、ATX、TISA Dynamic、Agentix PLAS 和 ATLAS。
- Workload 包含串行 tool-use、ReAct、Mixture-of-Agents、MCTS，以及 reactive/proactive 混合 trace。
- 使用适合 4090 的 Qwen3-0.6B/1.7B、Llama-3.2-1B/3B 或同级模型，优先 W8A16。
- 测量 program makespan/throughput、call wait、reactive P90/P99、proactive throughput、抢占开销、ME/VE/DE 利用率、DDR 争用和调度开销。
- 消融优先级下传、抢占粒度、ATX prefetch、TISA 窗口、ME 数据流和内存带宽。

实验目标：

- 判断程序级、异构执行级和 NPU tile 级调度能否形成端到端叠加收益。
- 定位收益来自排队、放置、抢占、搬移还是 tile overlap。
- 两张 4090只用于功能和 GPU 对照；真实多 A100 结果不得由模拟器平替。

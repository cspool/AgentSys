# W2 — patch-target 报告（LLaMA 试运行，120 s，FCFS cap16 r0.5）

来源：`llama_w1/cap.sqlite`（w_instrument 14/14 探针 + CPU 采样 + osrt）。

## 发现 1：preprocess 的 70 % 是 `_prepare_inputs`

| process | n | 合计 | 中位 |
|---|---:|---:|---:|
| gpu_model_runner: forward | 4,934 | 21.28 s | 4,313 µs |
| gpu_model_runner: preprocess | 4,941 | 16.99 s | 3,439 µs |
| └ **w.run: prepare_inputs** | 4,935 | **11.96 s** | 2,423 µs |
| └ w.run: update_states | 4,941 | 0.97 s | 196 µs |
| w.sched: schedule_total | 4,941 | 3.82 s | 773 µs |
| └ schedule: allocate_slots | 69,783 | 1.78 s | 26 µs |
| w.sched: update_from_output | 4,939 | 1.76 s | 357 µs |

此前 `preprocess` 是不透明块；现在其内部 70 % 归到 `_prepare_inputs`，调度器 host 段
（schedule_total 3.82 s + update_from_output 1.76 s）也从 `schedule:*` 的碎片聚合为可比项。

## 发现 2：`_prepare_inputs` 的 80 % 是纯 Python/CPU，不是 CUDA

引擎线程上的 11.96 s 中，CUDA runtime API 仅 2.45 s（20 %）：
cudaMemcpyAsync 1.25 s / 51,063 次、cudaLaunchKernel 0.91 s / 32,876 次
（约每步 10 次 memcpy + 7 次 launch 的小拷贝/小核）；其余 9.5 s 是张量构建与索引的
Python 侧开销。→ 优化方向是减少每步小拷贝与 Python 张量构建，而非 kernel 优化。

## 发现 3：探针缺口

- `w.engine: step` 未记录：AsyncLLM 路径不经过 `EngineCore.step`（走
  `_process_engine_step`/输出处理循环）。W3 需改挂 AsyncLLM 侧的每步入口。
- `w.kv: allocate_slots`（70,769 次）与引擎自带 `schedule: allocate_slots`（69,783 次）
  重复覆盖同一热点，保留其一即可（保留自带的，去掉 w.kv 重复项以降低插桩开销）。
- OSRT 归因不可用于 host 段分解：窗口内 epoll_wait/sem_wait 主要来自其他线程，
  需按 globalTid 过滤后才有意义（已在 W2 分析中按引擎线程过滤）。

## W3 patch 计划（据此修订插桩层）

1. 保留：`w.run: prepare_inputs`、`w.run: update_states`、`w.sched: schedule_total`、
   `w.sched: update_from_output`、`w.sched: add_request`、`w.kv: get_computed_blocks`。
2. 新增：`_prepare_inputs` 内部细分（输入张量构建 / 位置与 slot 映射 / attn metadata
   构建），以及 AsyncLLM 每步入口 `w.engine: async_step`、输出处理 `w.engine: process_outputs`。
3. 去除：`w.kv: allocate_slots`、`w.kv: free`、`w.sched: free_blocks`（与引擎自带 scope 重复）。
4. 机制事件：agentix_core 的 continuation 重提交与队列迁移在客户端标记为
   `agentix.cont::<pid>::<idx>::<q>`，使其成为一等 process。

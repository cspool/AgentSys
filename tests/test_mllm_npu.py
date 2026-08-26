from __future__ import annotations

from agentsys.mllm_npu import (
    LlmNpuConfig,
    build_subgraphs,
    chunk_sharing_experiment,
    native_graph_contract,
    run_mllm_npu_reproduction,
    schedule_subgraphs,
    shadow_outlier_experiment,
)


def test_native_graph_drives_chunk_sharing() -> None:
    config = LlmNpuConfig()
    graph = native_graph_contract()
    result = chunk_sharing_experiment(config, graph)
    assert graph["layers"] == 28
    assert graph["chunk_tokens"] == config.chunk_tokens
    assert graph["static_operator_count"] + graph["dynamic_operator_count"] == graph["block_operator_count"]
    assert result["speedup"] > 1.0
    assert result["causal_kv_edges"] == result["chunks"] - 1


def test_shadow_outlier_preserves_fast_npu_path() -> None:
    result = shadow_outlier_experiment(LlmNpuConfig())
    assert result["shadow_fully_hidden"]
    assert result["active_outlier_fraction"] < result["outlier_channel_fraction"]
    assert result["speedup"] > 1.0


def test_out_of_order_preserves_work_and_dependencies() -> None:
    config = LlmNpuConfig(prompt_tokens=128)
    tasks = build_subgraphs(config, layers=4)
    naive = schedule_subgraphs(tasks, mode="naive")
    dynamic = schedule_subgraphs(
        tasks,
        mode="out_of_order",
        scheduler_overhead_us=config.scheduler_overhead_us,
    )
    assert naive.completed == dynamic.completed == len(tasks)
    assert naive.dependency_checks == dynamic.dependency_checks
    assert naive.busy_us == dynamic.busy_us
    assert dynamic.makespan_us < naive.makespan_us
    assert dynamic.bubble_rate["npu"] < naive.bubble_rate["npu"]


def test_full_mllm_npu_reproduction_meets_locked_gate() -> None:
    result = run_mllm_npu_reproduction(run_id="pytest")
    assert result["paper_accuracy"]["pass"]
    assert result["paper_accuracy"]["total"] == 5
    assert result["summary"]["max_relative_error"] <= 0.15

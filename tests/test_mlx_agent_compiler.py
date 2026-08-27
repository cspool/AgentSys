from __future__ import annotations

import json

from agentsys.workload import PROJECT_ROOT


ROOT = PROJECT_ROOT / "artifacts/mlx_agent/run_045/workloads/react_tool"


def test_run045_agent_mlx_compiler_preserves_mir_and_spatial_lineage() -> None:
    compiled = json.loads((ROOT / "compiled-mlx.json").read_text(encoding="utf-8"))
    assert compiled["summary"] == {
        "calls": 3,
        "llm_calls": 2,
        "mir_sources_per_llm": 8,
        "mlx_dma_bytes": 1152,
        "mlx_instructions": 90,
        "mlx_micro_ops": 90,
        "mlx_micro_ops_per_llm": 45,
        "pass": True,
        "programs": 1,
        "tool_calls": 1,
    }
    assert all(compiled["gates"].values())
    assert len(compiled["micro_lineage"]) == 45
    assert {item["mir_source_index"] for item in compiled["micro_lineage"]} == {
        6,
        7,
        8,
        10,
        11,
        12,
        13,
        14,
    }
    assert {item["mlx_operation"] for item in compiled["micro_lineage"]} == {
        "load",
        "store",
        "fma",
        "add",
        "max",
        "exp",
        "div",
        "shuffle",
        "xfer",
        "mul",
    }
    assert [call["call_id"] for call in compiled["calls"]] == [
        "plan",
        "lookup",
        "answer",
    ]


def test_run045_retains_cache_warmup_and_runner_gate_failures() -> None:
    result = json.loads((ROOT / "mlx-agent-system.json").read_text(encoding="utf-8"))
    assert result["summary"] == {
        "calls": 3,
        "cycle_kernel": 264,
        "failing": 2,
        "gates": 10,
        "llm_calls": 2,
        "mlx_micro_ops": 90,
        "pass": False,
        "passing": 8,
        "programs": 1,
        "rtl_kernel": 152,
        "tool_calls": 1,
        "trace_events": 158,
    }
    assert not result["gates"]["distinct_backend_execution"]
    assert not result["gates"]["serial_seven_stages"]
    for backend in ("cycle", "rtl"):
        calls = [
            item
            for item in result["backend_results"][backend]["parsed"]["calls"]
            if item["kind"] == "llm"
        ]
        assert [item["dma"] for item in calls] == [344, 216]
        assert all(item["mismatches"] == 0 for item in calls)
        assert all(item["abi"] == 0x4D4C5801 for item in calls)
        assert all(
            value
            for name, value in result["backend_gates"][backend].items()
            if name != "aggregate_hardware"
        )

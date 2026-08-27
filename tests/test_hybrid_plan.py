from __future__ import annotations

import json

from agentsys.hybrid_plan import DEFAULT_CONFIG, compile_hybrid_plan, write_hybrid_plan
from agentsys.hybrid_system import EXPECTED_ROCKET_EVENTS, _placement_sensitivity
from agentsys.workload import PROJECT_ROOT, load_agent_workload


RUN032 = PROJECT_ROOT / "artifacts/parameterized_reproduction/run_032/workloads"


def _compile(name: str, placement: str = "round_robin") -> dict:
    workload = load_agent_workload(PROJECT_ROOT / f"workloads/{name}.json")
    root = RUN032 / name
    return compile_hybrid_plan(
        workload,
        application_path=root / "application.json",
        compiled_path=root / "compiled.json",
        header_path=root / "generated/workload.h",
        elf_path=root / "software/workload.riscv",
        config_path=DEFAULT_CONFIG,
        placement=placement,
        run_id="pytest",
    )


def test_hybrid_config_covers_three_workloads_and_sixth_switch() -> None:
    config = json.loads(DEFAULT_CONFIG.read_text(encoding="utf-8"))
    assert config["schema_version"] == 1
    assert config["placement"] == "round_robin"
    assert config["sensitivity_placement"] == "gpu0_only"
    assert len(config["workloads"]) == 3
    assert config["adapter"] == {
        "dtype": "float16",
        "matrix_base": 512,
        "matrix_step": 128,
        "token_quantum": 128,
        "matrix_max": 1024,
        "cpu_matrix_size": 256,
        "cpu_threads_per_rank": 16,
        "operator_iterations": 1,
    }
    assert EXPECTED_ROCKET_EVENTS == {
        "react_moa_mcts": 860,
        "react_tool": 180,
        "planner_debate": 436,
    }


def test_three_hybrid_plans_preserve_dag_mir_and_expected_gpu_balance(tmp_path) -> None:
    expected = {
        "react_moa_mcts": (11, 10, [5, 5], 80),
        "react_tool": (3, 2, [1, 1], 16),
        "planner_debate": (6, 5, [3, 2], 40),
    }
    plan_hashes = set()
    for name, (calls, llm_calls, ranks, operators) in expected.items():
        plan = _compile(name)
        assert plan["summary"]["pass"]
        assert plan["summary"]["calls"] == calls
        assert plan["summary"]["llm_calls"] == llm_calls
        assert plan["summary"]["tool_calls"] == 1
        assert plan["summary"]["gpu_rank_llm_calls"] == ranks
        assert plan["summary"]["mir_operators"] == operators
        assert plan["summary"]["me_operators"] == llm_calls * 3
        assert plan["summary"]["ve_operators"] == llm_calls * 3
        assert plan["summary"]["de_operators"] == llm_calls * 2
        assert all(
            call["wave"] > max(
                (
                    next(item["wave"] for item in plan["calls"] if item["call_id"] == dep)
                    for dep in call["deps"]
                ),
                default=-1,
            )
            for call in plan["calls"]
        )
        assert all(
            512 < call["native"]["matrix_size"] <= 1024
            for call in plan["calls"]
            if call["kind"] == "llm"
        )
        assert "not A100" in plan["evidence_boundary"]
        output = tmp_path / f"{name}.json"
        workload = load_agent_workload(PROJECT_ROOT / f"workloads/{name}.json")
        root = RUN032 / name
        written = write_hybrid_plan(
            output,
            workload,
            application_path=root / "application.json",
            compiled_path=root / "compiled.json",
            header_path=root / "generated/workload.h",
            elf_path=root / "software/workload.riscv",
            config_path=DEFAULT_CONFIG,
            placement="round_robin",
            run_id="pytest",
        )
        assert json.loads(output.read_text(encoding="utf-8")) == written
        plan_hashes.add(written["plan_sha256"])
    assert len(plan_hashes) == 3


def test_gpu0_variant_changes_only_native_placement() -> None:
    for name in ("react_moa_mcts", "react_tool", "planner_debate"):
        baseline = _compile(name, "round_robin")
        variant = _compile(name, "gpu0_only")
        sensitivity = _placement_sensitivity(baseline, variant)
        assert sensitivity["pass"]
        assert sensitivity["logical_work_invariant"]
        assert sensitivity["changed"]
        assert set(sensitivity["variant_signature"]) == {0}
        assert set(sensitivity["baseline_signature"]) == {0, 1}

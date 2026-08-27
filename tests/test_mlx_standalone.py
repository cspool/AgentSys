from __future__ import annotations

import json
import os

from agentsys.workload import PROJECT_ROOT


RESULT = PROJECT_ROOT / "artifacts/mlx_standalone/run_043/mlx-standalone.json"


def test_mlx_toolchain_setup_is_pinned_and_executable() -> None:
    requirements = (
        PROJECT_ROOT / "config/mlx-runtime-requirements.txt"
    ).read_text(encoding="utf-8")
    assert requirements.splitlines() == ["numpy==2.2.6", "PyYAML==6.0.2"]
    setup = PROJECT_ROOT / "scripts/setup_mlx_toolchain.sh"
    assert setup.is_file() and os.access(setup, os.X_OK)
    environment = json.loads(
        (PROJECT_ROOT / "artifacts/mlx_environment/environment.json").read_text(
            encoding="utf-8"
        )
    )
    assert environment["numpy"] == "2.2.6"
    assert environment["pyyaml"] == "6.0.2"
    assert "Verilator 4.034" in environment["verilator"]


def test_run043_fresh_mlx_cycle_and_rtl_are_functional_and_distinct() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["summary"] == {
        "executions": 8,
        "failing": 0,
        "gates": 10,
        "operations": 10,
        "pass": True,
        "passing": 10,
        "workloads": 4,
    }
    assert all(result["gates"].values())
    assert not result["paper_performance_targets_consumed"]
    assert [record["workload"] for record in result["records"]] == [
        "bsmm",
        "fft_cmp",
        "swa",
        "transformer_block",
    ]
    for record in result["records"]:
        assert record["cycle"]["returncode"] == record["rtl"]["returncode"] == 0
        assert record["comparison"]["instruction_count"]
        assert record["comparison"]["events"]["same_instruction_multiset"]
        assert record["comparison"]["events"]["same_per_pe_program_order"]
        assert not record["comparison"]["events"]["same_global_issue_order"]
        assert record["comparison"]["cycle_to_rtl_ratio"] > 1.0
    assert set(result["instruction_timing"]) == {
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

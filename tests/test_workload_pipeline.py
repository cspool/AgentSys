from __future__ import annotations

import json

from agentsys.workload import PROJECT_ROOT
from agentsys.workload_pipeline import run_workload_pipeline


def test_compile_only_pipeline_switches_three_workloads_without_shared_outputs(
    tmp_path,
) -> None:
    elf_hashes = set()
    for name in ("react_moa_mcts", "react_tool", "planner_debate"):
        output = tmp_path / name
        result = run_workload_pipeline(
            PROJECT_ROOT / f"workloads/{name}.json",
            run_id="pytest",
            output_dir=output,
            execute_system=False,
        )
        assert result["summary"] == {
            "stages": 3,
            "passing": 3,
            "failing": 0,
            "serial_order": True,
            "system_executed": False,
            "pass": True,
        }
        assert (output / "application.json").is_file()
        assert (output / "compiled.json").is_file()
        assert (output / "generated/workload.h").is_file()
        assert (output / "software/workload.riscv").is_file()
        assert (output / "pipeline.json").is_file()
        compiled = json.loads((output / "compiled.json").read_text(encoding="utf-8"))
        assert compiled["workload"]["name"] == name
        elf_hashes.add(result["stages"][2]["outputs"][str(output / "software/workload.riscv")]["sha256"])
    assert len(elf_hashes) == 3

from __future__ import annotations

import json

from agentsys.parameterized_application import execute_agent_workload
from agentsys.parameterized_compiler import (
    build_parameterized_elf,
    compile_parameterized_workload,
)
from agentsys.workload import PROJECT_ROOT, load_agent_workload


def _compile(name: str, tmp_path):
    workload = load_agent_workload(PROJECT_ROOT / f"workloads/{name}.json")
    application = execute_agent_workload(workload, run_id="pytest")
    application_path = tmp_path / f"{name}-application.json"
    application_path.write_text(json.dumps(application, sort_keys=True), encoding="utf-8")
    manifest_path = tmp_path / f"{name}-compiled.json"
    header_path = tmp_path / f"{name}.h"
    result = compile_parameterized_workload(
        workload,
        application,
        application_path=application_path,
        manifest_path=manifest_path,
        header_path=header_path,
        run_id="pytest",
    )
    return workload, application, result, header_path.read_text(encoding="utf-8")


def test_certified_workload_preserves_run028_hardware_descriptors(tmp_path) -> None:
    _workload, application, result, header = _compile("react_moa_mcts", tmp_path)
    baseline = json.loads(
        (PROJECT_ROOT / "artifacts/app_traces/revised-compiled-workload-run_028.json").read_text(
            encoding="utf-8"
        )
    )
    assert application["output_digest"] == baseline["application"]["output_digest"]
    assert result["summary"]["descriptors"] == 80
    for observed_call, baseline_call in zip(
        result["hardware_calls"], baseline["hardware_calls"], strict=True
    ):
        assert [item["control"] for item in observed_call["descriptors"]] == [
            item["control"] for item in baseline_call["descriptors"]
        ]
        assert [item["tilemem"] for item in observed_call["descriptors"]] == [
            item["tilemem"] for item in baseline_call["descriptors"]
        ]
    assert "#define AGENTSYS_EXPECT_DESCRIPTORS 80" in header
    assert "#define AGENTSYS_REVISED_PROGRAMS 3" in header


def test_switched_workloads_generate_manifest_derived_counts(tmp_path) -> None:
    expected = {
        "react_tool": {"programs": 1, "calls": 3, "descriptors": 16, "me_busy": 480},
        "planner_debate": {
            "programs": 2,
            "calls": 6,
            "descriptors": 40,
            "me_busy": 1200,
        },
    }
    for name, values in expected.items():
        workload, _application, result, header = _compile(name, tmp_path)
        for key, value in values.items():
            assert result["summary"][key] == value
        assert f'#define AGENTSYS_WORKLOAD_NAME "{name}"' in header
        assert f"#define AGENTSYS_REVISED_CALLS {values['calls']}" in header
        assert f"#define AGENTSYS_WORKLOAD_DIGEST UINT64_C(0x{workload.sha256[:16]})" in header
        assert "uint64_t deps_mask;" in header


def test_each_workload_builds_a_distinct_riscv_elf(tmp_path) -> None:
    hashes = set()
    for name in ("react_moa_mcts", "react_tool", "planner_debate"):
        _workload, _application, _result, _header = _compile(name, tmp_path)
        build = build_parameterized_elf(tmp_path / f"{name}.h", tmp_path / f"{name}.riscv")
        assert build["pass"]
        assert build["elf_bytes"] > 50_000
        hashes.add(build["elf_sha256"])
    assert len(hashes) == 3

from __future__ import annotations

import json

from agentsys.workload import PROJECT_ROOT


PROFILE = PROJECT_ROOT / "artifacts/hybrid_profile/run_041"


def test_run041_nsight_profile_covers_all_mir_ranges_and_cuda_classes() -> None:
    audit = json.loads((PROFILE / "profile-audit.json").read_text(encoding="utf-8"))
    assert audit["summary"] == {
        "failing": 0,
        "gates": 9,
        "pass": True,
        "passing": 9,
    }
    assert all(audit["gates"].values())
    assert audit["native_summary"]["passing"] == audit["native_summary"]["gates"] == 13
    assert audit["rows"]["kernels"] >= 10
    assert audit["rows"]["apis"] >= 20
    assert audit["rows"]["memory"] >= 2
    assert audit["rows"]["nvtx"] >= 16
    assert len(audit["expected_nvtx_ranges"]) == 16
    assert sum("::plan::" in name for name in audit["expected_nvtx_ranges"]) == 8
    assert sum("::answer::" in name for name in audit["expected_nvtx_ranges"]) == 8
    assert (PROFILE / "react-tool.nsys-rep").stat().st_size > 1_000_000
    assert (PROFILE / "react-tool.sqlite").stat().st_size > 1_000_000


def test_profiled_runtime_consumes_dtype_iterations_and_numa_contract() -> None:
    runtime = json.loads(
        (PROFILE / "native/native-runtime.json").read_text(encoding="utf-8")
    )
    events = [
        json.loads(line)
        for line in (PROFILE / "native/native-trace.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
    ]
    ops = [event for event in events if event["event"] == "mir_operator"]
    assert len(ops) == 16
    assert {event["dtype"] for event in ops} == {"float16"}
    assert {event["iterations"] for event in ops} == {1}
    assert [rank["numa_node"] for rank in runtime["ranks"]] == [0, 1]
    assert all(rank["torch_cpu_threads"] == 16 for rank in runtime["ranks"])
    assert all(rank["collective"]["correct"] for rank in runtime["ranks"])

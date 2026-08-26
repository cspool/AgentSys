from __future__ import annotations

import json

from agentsys.hptpe import HPTPE_ROOT, RTL_CASES, parse_dc_reports, patch_testbench


def test_all_hptpe_dc_reports_parse_and_meet_timing() -> None:
    reports = parse_dc_reports()
    assert reports["summary"]["pass"]
    assert reports["summary"]["points"] == 12
    assert all(point["total_cell_area_um2"] > 0 for point in reports["points"])
    assert all(point["frequency_mhz"] > 0 for point in reports["points"])


def test_hptpe_testbench_compatibility_transform_is_complete() -> None:
    for case in RTL_CASES:
        patched = patch_testbench(case)
        assert "'{default:" not in patched
        assert f"module {case.top}" in patched
        assert HPTPE_ROOT.joinpath(case.testbench).is_file()


def test_run024_hptpe_artifact_closes_rtl_and_performance_gates() -> None:
    result = json.loads(open("artifacts/results/paper-hptpe-run_024.json", encoding="utf-8").read())
    assert result["summary"]["pass"]
    assert result["summary"]["rtl_functional_passed"] == 9
    assert result["summary"]["rtl_golden_checks"] == 302
    assert result["summary"]["rtl_lint_passed"] == 9
    assert result["summary"]["paper_endpoints_passed"] == 26
    assert result["paper_accuracy"]["evidence_counts"] == {
        "author_dc_report_replay": 24,
        "executed_open_rtl_testbench": 2,
    }

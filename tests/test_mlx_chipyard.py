from __future__ import annotations

import json
import os

from agentsys.workload import PROJECT_ROOT


RESULT = PROJECT_ROOT / "artifacts/mlx_chipyard/run_044/mlx-chipyard.json"


def test_mlx_chipyard_installer_and_smoke_source_are_present() -> None:
    installer = PROJECT_ROOT / "scripts/install_mlx_chipyard.sh"
    source = PROJECT_ROOT / "system_sim/software/agentsys_mlx_smoke.c"
    assert installer.is_file() and os.access(installer, os.X_OK)
    text = source.read_text(encoding="utf-8")
    assert "AGENTSYS_MLX_ABI_MAGIC" in text
    assert "AGENTSYS_MLX_SMOKE_%s" in text and '"PASS"' in text
    assert "mlx_launch" in text and "mlx_wait" in text


def test_run044_closes_ordinary_rocket_mlx_cycle_and_rtl() -> None:
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    assert result["summary"] == {
        "backends": 2,
        "executions": 8,
        "failing": 0,
        "gates": 12,
        "pass": True,
        "passing": 12,
        "workloads": 4,
    }
    assert all(result["gates"].values())
    assert not result["paper_performance_targets_consumed"]
    assert result["source"]["clean"]
    assert len(result["chipyard"]["installed"]) == 12
    assert len(result["records"]) == 8
    assert len({record["elf"]["sha256"] for record in result["records"]}) == 4
    for record in result["records"]:
        summary = record["summary"]
        assert record["pass"] and all(record["checks"].values())
        assert summary["abi"] == 0x4D4C5801
        assert summary["mismatches"] == 0
        assert summary["system"] == summary["dma"] + summary["kernel"] + 2
        assert summary["instructions"] == (
            summary["load"]
            + summary["store"]
            + summary["compute"]
            + summary["xfer"]
        )
        assert summary["host_total"] > summary["system"]
    assert {record["backend"] for record in result["records"]} == {"cycle", "rtl"}

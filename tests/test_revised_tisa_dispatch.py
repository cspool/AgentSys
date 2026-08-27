from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_revised_tisa_dispatch_pipeline(tmp_path: Path) -> None:
    iverilog = shutil.which("iverilog")
    vvp = shutil.which("vvp")
    assert iverilog is not None and vvp is not None
    executable = tmp_path / "tisa-dispatch.vvp"
    trace = tmp_path / "tisa-dispatch.log"
    subprocess.run(
        [
            iverilog,
            "-g2012",
            "-s",
            "tb_agentsys_tisa_dispatch",
            "-o",
            str(executable),
            str(ROOT / "rtl/agentsys/agentsys_tisa_scheduler.sv"),
            str(ROOT / "rtl/agentsys/tb_agentsys_tisa_dispatch.sv"),
        ],
        check=True,
        cwd=ROOT,
    )
    completed = subprocess.run(
        [vvp, str(executable), f"+agentsys_tisa_trace={trace}"],
        check=True,
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert "AGENTSYS_TISA_DISPATCH_PASS static_first=0 dynamic_first=7" in completed.stdout
    lines = trace.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 6
    assert sum("AGENTSYS_TISA_ISSUE call=9" in line for line in lines) == 3
    assert sum("AGENTSYS_TISA_COMPLETE call=9" in line for line in lines) == 3

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
        [vvp, str(executable)], check=True, cwd=ROOT, text=True, capture_output=True
    )
    assert "AGENTSYS_TISA_DISPATCH_PASS static_first=0 dynamic_first=7" in completed.stdout

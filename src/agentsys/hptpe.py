from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[2]
HPTPE_ROOT = PROJECT_ROOT / ".references" / "HPTPE"
VERILATOR5_ROOT = PROJECT_ROOT / ".references" / "verilator5"
VERILATOR5 = VERILATOR5_ROOT / "bin" / "verilator"
WS_OPT_TOP = PROJECT_ROOT / "integrations" / "hptpe" / "rtl" / "opt1_ws_top.v"
PAPER_TARGETS = PROJECT_ROOT / "data" / "paper_targets.json"
HPTPE_COMMIT = "ebe4db7d2d3c36d10c47683d7689f65f5c4ca3e4"
VERILATOR5_COMMIT = "848d926ebd4addacacd294dc84e35d9d4ae8078c"

AREA_RE = re.compile(r"Total cell area:\s+([0-9.]+)")
TOTAL_AREA_RE = re.compile(r"^Total area:\s+([0-9.]+)", re.MULTILINE)
ARRIVAL_RE = re.compile(r"data arrival time\s+(-?[0-9.]+)")
SUCCESS_RE = re.compile(r"SUCCESS:")
AVERAGE_RE = re.compile(r"Average cal_cycle for per-operand\s*=\s*([0-9.]+)")
ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _rel(path: str) -> Path:
    return HPTPE_ROOT / path


OS_MAC = (
    "OPT1/systolic_array_os/array_mac_based/sim/timescale.sv",
    "OPT1/systolic_array_os/array_mac_based/get_pipline_mulwidth.v",
    "OPT1/systolic_array_os/array_mac_based/pe.v",
    "OPT1/systolic_array_os/array_mac_based/top.v",
)
OS_OPT = (
    "OPT1/systolic_array_os/array_opt1_based/sim/timescale.sv",
    "OPT1/systolic_array_os/array_opt1_based/booth_partial_product_generator_pp1.v",
    "OPT1/systolic_array_os/array_opt1_based/booth_partial_product_generator.v",
    "OPT1/systolic_array_os/array_opt1_based/booth_pp_gen.v",
    "OPT1/systolic_array_os/array_opt1_based/DW02_tree.sv",
    "OPT1/systolic_array_os/array_opt1_based/get_pipline_mulwidth.v",
    "OPT1/systolic_array_os/array_opt1_based/inv_conveter_8.v",
    "OPT1/systolic_array_os/array_opt1_based/inv_unit_nor_out.v",
    "OPT1/systolic_array_os/array_opt1_based/inv_unit.v",
    "OPT1/systolic_array_os/array_opt1_based/opt1_mac.v",
    "OPT1/systolic_array_os/array_opt1_based/pe.v",
    "OPT1/systolic_array_os/array_opt1_based/top.v",
)
WS_MAC = (
    "OPT1/systolic_array_ws/array_mac_based/sim/timescale.sv",
    "OPT1/systolic_array_ws/array_mac_based/get_pipline_mulwidth.v",
    "OPT1/systolic_array_ws/array_mac_based/PE.v",
    "OPT1/systolic_array_ws/array_mac_based/top.v",
)
WS_OPT_BASE = (
    "OPT1/systolic_array_ws/array_opt1_based/sim/timescale.sv",
    "OPT1/systolic_array_ws/array_opt1_based/booth_partial_product_generator_pp1.v",
    "OPT1/systolic_array_ws/array_opt1_based/booth_partial_product_generator.v",
    "OPT1/systolic_array_ws/array_opt1_based/booth_pp_gen.v",
    "OPT1/systolic_array_ws/array_opt1_based/DW02_tree.sv",
    "OPT1/systolic_array_ws/array_opt1_based/get_pipline_mulwidth.v",
    "OPT1/systolic_array_ws/array_opt1_based/inv_conveter_8.v",
    "OPT1/systolic_array_ws/array_opt1_based/inv_unit_nor_out.v",
    "OPT1/systolic_array_ws/array_opt1_based/inv_unit.v",
    "OPT1/systolic_array_ws/array_opt1_based/opt1_mac.v",
    "OPT1/systolic_array_ws/array_opt1_based/PE.v",
)
CUBE_MAC = (
    "OPT1/cube/array_mac_based/sim/timescale.sv",
    "OPT1/cube/array_mac_based/get_pipline_mulwidth.v",
    "OPT1/cube/array_mac_based/pe.v",
    "OPT1/cube/array_mac_based/top.v",
)
CUBE_OPT = (
    "OPT1/cube/array_opt1_based/sim/timescale.sv",
    "OPT1/cube/array_opt1_based/booth_partial_product_generator_pp1.v",
    "OPT1/cube/array_opt1_based/booth_partial_product_generator.v",
    "OPT1/cube/array_opt1_based/booth_pp_gen.v",
    "OPT1/cube/array_opt1_based/DW02_tree.sv",
    "OPT1/cube/array_opt1_based/get_pipline_mulwidth.v",
    "OPT1/cube/array_opt1_based/inv_conveter_8.v",
    "OPT1/cube/array_opt1_based/inv_unit_nor_out.v",
    "OPT1/cube/array_opt1_based/inv_unit.v",
    "OPT1/cube/array_opt1_based/opt1_mac.v",
    "OPT1/cube/array_opt1_based/PE.v",
    "OPT1/cube/array_opt1_based/top.v",
)
OPT2 = (
    "OPT2/sim/timescale.sv",
    "OPT2/DW02_tree.sv",
    "OPT2/partial_product_select.sv",
    "OPT2/top_pe_tile.sv",
    "OPT2/top_tpe.sv",
    "OPT2/tree_full_sum.sv",
    "OPT2/vector_encoder.sv",
    "OPT2/weight_rf.sv",
    "OPT2/get_pipline_mulwidth.v",
)
OPT3 = (
    "OPT3_OPT4C/pe/sim/timescale.sv",
    "OPT3_OPT4C/pe/DW02_tree.sv",
    "OPT3_OPT4C/pe/encoder_multi_bit.v",
    "OPT3_OPT4C/pe/pe.v",
    "OPT3_OPT4C/pe/sparse_encoder.v",
    "OPT3_OPT4C/pe/get_pipline_mulwidth.v",
    "OPT3_OPT4C/pe/top_pe.v",
    "OPT3_OPT4C/pe/get_negedge.sv",
)
OPT4C = (
    "OPT3_OPT4C/pe/sim/timescale.sv",
    "OPT3_OPT4C/pe/DW02_tree.sv",
    "OPT3_OPT4C/pe/encoder_multi_bit.v",
    "OPT3_OPT4C/pe/pe.v",
    "OPT3_OPT4C/pe/sparse_encoder.v",
    "OPT3_OPT4C/pe/get_pipline_mulwidth.v",
    "OPT3_OPT4C/array/top_pe_column.v",
)


@dataclass(frozen=True, slots=True)
class RtlCase:
    name: str
    simulator: str
    top: str
    sources: tuple[str, ...]
    testbench: str
    rank: str
    parameters: tuple[tuple[str, int], ...]
    trials: int
    expected_successes: int
    normal_stddev: int | None = None
    extra_source: Path | None = None


RTL_CASES = (
    RtlCase(
        "opt1_os_mac",
        "iverilog",
        "test_opt2os_array",
        OS_MAC,
        "OPT1/systolic_array_os/array_mac_based/sim/test_mac_os_array.sv",
        "matrix",
        (("M", 4), ("K", 4), ("N", 4)),
        2,
        2,
    ),
    RtlCase(
        "opt1_os",
        "iverilog",
        "test_opt1_os_array",
        OS_OPT,
        "OPT1/systolic_array_os/array_opt1_based/sim/test_opt1_os_array.sv",
        "matrix",
        (("M", 4), ("K", 4), ("N", 4)),
        2,
        2,
    ),
    RtlCase(
        "opt1_ws_mac",
        "iverilog",
        "test_opt2ws_array",
        WS_MAC,
        "OPT1/systolic_array_ws/array_mac_based/sim/test_ws_array.sv",
        "matrix",
        (("M", 4), ("K", 4), ("N", 4)),
        2,
        2,
    ),
    RtlCase(
        "opt1_ws",
        "iverilog",
        "test_opt2ws_array",
        WS_OPT_BASE,
        "OPT1/systolic_array_ws/array_opt1_based/sim/test_opt1_ws_array.sv",
        "matrix",
        (("M", 4), ("K", 4), ("N", 4)),
        2,
        2,
        extra_source=WS_OPT_TOP,
    ),
    RtlCase(
        "opt1_cube_mac",
        "iverilog",
        "test_opt2tc_array",
        CUBE_MAC,
        "OPT1/cube/array_mac_based/sim/test_mac_tc_array.sv",
        "cube",
        (("K", 2), ("N", 4)),
        2,
        2,
    ),
    RtlCase(
        "opt1_cube",
        "iverilog",
        "test_opt2tc_array",
        CUBE_OPT,
        "OPT1/cube/array_opt1_based/sim/test_opt1_cube.sv",
        "cube",
        (("K", 2), ("N", 4)),
        2,
        2,
    ),
    RtlCase(
        "opt2",
        "verilator5",
        "test_opt2ws_array",
        OPT2,
        "OPT2/sim/test_opt2ws_array.sv",
        "matrix",
        (("M", 4), ("K", 16), ("N", 4)),
        2,
        2,
    ),
    RtlCase(
        "opt3_pe",
        "verilator5",
        "test_opt3_pe_inner_product_vectors",
        OPT3,
        "OPT3_OPT4C/pe/sim/test_opt3_pe_inner_product_vectors.sv",
        "scalar",
        (("K", 32),),
        256,
        256,
        normal_stddev=20,
    ),
    RtlCase(
        "opt4c",
        "verilator5",
        "test_opt4c_column_array",
        OPT4C,
        "OPT3_OPT4C/array/sim/test_opt4c_column_array.sv",
        "matrix",
        (("M", 4), ("K", 32), ("N", 4)),
        32,
        32,
        normal_stddev=30,
    ),
)


@dataclass(frozen=True, slots=True)
class LintCase:
    name: str
    top: str
    sources: tuple[str, ...]
    extra_source: Path | None = None
    timescale: bool = False


LINT_CASES = (
    LintCase("opt1_os_mac", "top", OS_MAC[1:]),
    LintCase("opt1_os", "top", OS_OPT[1:]),
    LintCase("opt1_ws_mac", "top", WS_MAC[1:]),
    LintCase("opt1_ws", "top", WS_OPT_BASE[1:], extra_source=WS_OPT_TOP),
    LintCase("opt1_cube_mac", "top", CUBE_MAC[1:], timescale=True),
    LintCase("opt1_cube", "top", CUBE_OPT[1:], timescale=True),
    LintCase("opt2", "top_tpe", OPT2[1:]),
    LintCase("opt3_pe", "top_pe", OPT3[1:]),
    LintCase("opt4c", "top_pe_column", OPT4C[1:]),
)


@dataclass(frozen=True, slots=True)
class ReportSpec:
    name: str
    target_path: tuple[str, ...]
    period_ns: float
    area_report: str
    timing_report: str


REPORT_SPECS = (
    ReportSpec("opt1.os.baseline", ("opt1", "os", "baseline"), 6.5, "OPT1/systolic_array_os/array_mac_based/syn/outputs/saed32rvt_tt0p85v25c/top_array_16_area_report_6.5.txt", "OPT1/systolic_array_os/array_mac_based/syn/outputs/saed32rvt_tt0p85v25c/top_array_16_timing_report_6.5.txt"),
    ReportSpec("opt1.os.optimized", ("opt1", "os", "optimized"), 3.1, "OPT1/systolic_array_os/array_opt1_based/syn/outputs/saed32rvt_tt0p85v25c/top_opt1_array_16_area_report_3.1.txt", "OPT1/systolic_array_os/array_opt1_based/syn/outputs/saed32rvt_tt0p85v25c/top_opt1_array_16_timing_report_3.1.txt"),
    ReportSpec("opt1.ws.baseline", ("opt1", "ws", "baseline"), 5.5, "OPT1/systolic_array_ws/array_mac_based/syn/outputs/saed32rvt_tt0p85v25c/top_array_16_area_report_5.5.txt", "OPT1/systolic_array_ws/array_mac_based/syn/outputs/saed32rvt_tt0p85v25c/top_array_16_timing_report_5.5.txt"),
    ReportSpec("opt1.ws.optimized", ("opt1", "ws", "optimized"), 3.3, "OPT1/systolic_array_ws/array_opt1_based/syn/outputs/saed32rvt_tt0p85v25c/top_opt1_array_16_area_report_3.3.txt", "OPT1/systolic_array_ws/array_opt1_based/syn/outputs/saed32rvt_tt0p85v25c/top_opt1_array_16_timing_report_3.3.txt"),
    ReportSpec("opt1.cube.baseline", ("opt1", "cube", "baseline"), 6.3, "OPT1/cube/array_mac_based/syn/outputs/saed32rvt_tt0p85v25c/top_cube_8_area_report_6.3.txt", "OPT1/cube/array_mac_based/syn/outputs/saed32rvt_tt0p85v25c/top_cube_8_timing_report_6.3.txt"),
    ReportSpec("opt1.cube.optimized", ("opt1", "cube", "optimized"), 4.0, "OPT1/cube/array_opt1_based/syn/outputs/saed32rvt_tt0p85v25c/top_opt1_cube_area_report_4.0.txt", "OPT1/cube/array_opt1_based/syn/outputs/saed32rvt_tt0p85v25c/top_opt1_cube_timing_report_4.0.txt"),
    ReportSpec("opt2.k16_n4", ("opt2", "k16_n4"), 1.35, "OPT2/syn/outputs_array/saed32rvt_tt0p85v25c/top_tpe_n4_area_report_1.35.txt", "OPT2/syn/outputs_array/saed32rvt_tt0p85v25c/top_tpe_n4_timing_report_1.35.txt"),
    ReportSpec("opt2.k16_n8", ("opt2", "k16_n8"), 1.35, "OPT2/syn/outputs_array/saed32rvt_tt0p85v25c/top_tpe_n8_area_report_1.35.txt", "OPT2/syn/outputs_array/saed32rvt_tt0p85v25c/top_tpe_n8_timing_report_1.35.txt"),
    ReportSpec("opt2.k16_n16", ("opt2", "k16_n16"), 1.45, "OPT2/syn/outputs_array/saed32rvt_tt0p85v25c/top_tpe_n16_area_report_1.45.txt", "OPT2/syn/outputs_array/saed32rvt_tt0p85v25c/top_tpe_n16_timing_report_1.45.txt"),
    ReportSpec("opt2.k16_n32", ("opt2", "k16_n32"), 1.50, "OPT2/syn/outputs_array/saed32rvt_tt0p85v25c/top_tpe_n32_area_report_1.50.txt", "OPT2/syn/outputs_array/saed32rvt_tt0p85v25c/top_tpe_n32_timing_report_1.50.txt"),
    ReportSpec("opt3_opt4c.n16", ("opt3_opt4c", "n16"), 0.58, "OPT3_OPT4C/array/syn/outputs_array/saed32rvt_tt0p85v25c/top_pe_column_n16_area_report_0.58.txt", "OPT3_OPT4C/array/syn/outputs_array/saed32rvt_tt0p85v25c/top_pe_column_n16_timing_report_0.58.txt"),
    ReportSpec("opt3_opt4c.n32", ("opt3_opt4c", "n32"), 0.59, "OPT3_OPT4C/array/syn/outputs_array/saed32rvt_tt0p85v25c/top_pe_column_n32_area_report_0.59.txt", "OPT3_OPT4C/array/syn/outputs_array/saed32rvt_tt0p85v25c/top_pe_column_n32_timing_report_0.59.txt"),
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head(path: Path) -> str:
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def patch_testbench(case: RtlCase) -> str:
    text = _rel(case.testbench).read_text(encoding="utf-8")
    first_newline = text.index("\n")
    text = text[: first_newline + 1] + "integer compat_i, compat_j, compat_k;\n" + text[first_newline + 1 :]
    for parameter, value in case.parameters:
        text, count = re.subn(
            rf"parameter\s+{parameter}\s*=\s*\d+\s*;",
            f"parameter  {parameter} = {value};",
            text,
            count=1,
        )
        if count != 1:
            raise ValueError(f"could not override {parameter} in {case.testbench}")
    text = text.replace("times_b < 10", "times_b < 1")
    text = text.replace("times_a < 10", f"times_a < {case.trials}")
    text = text.replace("times_a <= 1000", f"times_a <= {case.trials}")
    if case.normal_stddev is not None:
        text = re.sub(r"normal_random\(0,\s*\d+", f"normal_random(0, {case.normal_stddev}", text)

    if case.rank == "cube":
        tpe_zero = "for (compat_k = 0; compat_k < K; compat_k = compat_k + 1) for (compat_i = 0; compat_i < N; compat_i = compat_i + 1) for (compat_j = 0; compat_j < N; compat_j = compat_j + 1) tpe_matrix_c[compat_k][compat_i][compat_j] = 0;"
        matrix_zero = "for (compat_k = 0; compat_k < K; compat_k = compat_k + 1) for (compat_i = 0; compat_i < N; compat_i = compat_i + 1) for (compat_j = 0; compat_j < N; compat_j = compat_j + 1) matrix_c[compat_k][compat_i][compat_j] = 0;"
    else:
        tpe_zero = "for (compat_i = 0; compat_i < M; compat_i = compat_i + 1) for (compat_j = 0; compat_j < N; compat_j = compat_j + 1) tpe_matrix_c[compat_i][compat_j] = 0;"
        matrix_zero = "for (compat_i = 0; compat_i < M; compat_i = compat_i + 1) for (compat_j = 0; compat_j < N; compat_j = compat_j + 1) matrix_c[compat_i][compat_j] = 0;"
    text = re.sub(r"tpe_matrix_c\s*=\s*'\{default:\s*0\};", tpe_zero, text)
    text = re.sub(r"(?<!tpe_)matrix_c\s*=\s*'\{default:\s*0\};", matrix_zero, text)
    text = re.sub(r"vector_c\s*=\s*'\{default:\s*0\};", "vector_c = '0;", text)
    text = re.sub(r"tpe_vector_c\s*=\s*'\{default:\s*0\};", "tpe_vector_c = '0;", text)
    text = re.sub(r"operand_b\s*=\s*'\{default:\s*0\};", "operand_b = '0;", text)
    if "'{default:" in text:
        raise ValueError(f"unpatched assignment pattern in {case.testbench}")
    return text


def _source_paths(case: RtlCase | LintCase) -> list[str]:
    paths = [str(_rel(source)) for source in case.sources]
    if case.extra_source is not None:
        paths.append(str(case.extra_source))
    return paths


def _tool_version(argv: list[str], *, env: dict[str, str] | None = None) -> str:
    proc = subprocess.run(argv, text=True, capture_output=True, check=False, env=env)
    return (proc.stdout + proc.stderr).strip().splitlines()[0]


def run_rtl_case(case: RtlCase, *, log_dir: Path | None = None) -> dict[str, Any]:
    patched = patch_testbench(case)
    started = time.monotonic_ns()
    with tempfile.TemporaryDirectory(prefix=f"hptpe-{case.name}-") as tmp_raw:
        tmp = Path(tmp_raw)
        tb = tmp / "testbench.sv"
        tb.write_text(patched, encoding="utf-8")
        sources = _source_paths(case) + [str(tb)]
        if case.simulator == "iverilog":
            binary = tmp / "simulation.vvp"
            compile_argv = ["iverilog", "-g2012", "-s", case.top, "-o", str(binary), *sources]
            run_argv = ["vvp", str(binary)]
            compile_env = None
        else:
            if not VERILATOR5.is_file():
                raise FileNotFoundError(VERILATOR5)
            mdir = tmp / "obj"
            compile_argv = [
                str(VERILATOR5),
                "--binary",
                "--timing",
                "-Wno-fatal",
                "-j",
                "4",
                "--top-module",
                case.top,
                "--Mdir",
                str(mdir),
                *sources,
            ]
            run_argv = [str(mdir / f"V{case.top}")]
            compile_env = os.environ.copy()
            compile_env["VERILATOR_ROOT"] = str(VERILATOR5_ROOT)
        compiled = subprocess.run(
            compile_argv,
            cwd=HPTPE_ROOT,
            env=compile_env,
            text=True,
            capture_output=True,
            timeout=180,
            check=False,
        )
        compile_log = compiled.stdout + compiled.stderr
        if compiled.returncode == 0:
            executed = subprocess.run(
                run_argv,
                cwd=HPTPE_ROOT,
                text=True,
                capture_output=True,
                timeout=120,
                check=False,
            )
            run_log = executed.stdout + executed.stderr
            returncode = executed.returncode
        else:
            run_log = ""
            returncode = None
    if log_dir is not None:
        log_dir.mkdir(parents=True, exist_ok=True)
        (log_dir / f"{case.name}.compile.log").write_text(compile_log, encoding="utf-8")
        (log_dir / f"{case.name}.run.log").write_text(run_log, encoding="utf-8")
    clean_run_log = ANSI_RE.sub("", run_log)
    successes = len(SUCCESS_RE.findall(clean_run_log))
    average_match = AVERAGE_RE.search(clean_run_log)
    failed_text = "Mismatch" in clean_run_log or "$error" in clean_run_log or "%Error" in compile_log
    elapsed_s = (time.monotonic_ns() - started) / 1e9
    all_sources = [*(_rel(source) for source in case.sources)]
    if case.extra_source is not None:
        all_sources.append(case.extra_source)
    return {
        "name": case.name,
        "simulator": case.simulator,
        "top": case.top,
        "parameters": dict(case.parameters),
        "trials": case.trials,
        "expected_successes": case.expected_successes,
        "successes": successes,
        "average_cal_cycle": float(average_match.group(1)) if average_match else None,
        "compile_returncode": compiled.returncode,
        "run_returncode": returncode,
        "compile_warnings": compile_log.count("%Warning"),
        "elapsed_s": elapsed_s,
        "testbench_sha256": _sha256(_rel(case.testbench)),
        "patched_testbench_sha256": hashlib.sha256(patched.encode()).hexdigest(),
        "source_sha256": {str(path.relative_to(PROJECT_ROOT)): _sha256(path) for path in all_sources},
        "stdout_tail": "\n".join(clean_run_log.splitlines()[-12:]),
        "stderr_tail": "\n".join(compile_log.splitlines()[-12:]),
        "pass": compiled.returncode == 0
        and returncode == 0
        and successes == case.expected_successes
        and not failed_text,
    }


def run_lint_case(case: LintCase) -> dict[str, Any]:
    argv = ["verilator", "--lint-only", "-Wno-fatal", "--top-module", case.top]
    if case.timescale:
        argv += ["--timescale", "1ns/1ps"]
    argv += _source_paths(case)
    proc = subprocess.run(
        argv,
        cwd=HPTPE_ROOT,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    output = proc.stdout + proc.stderr
    return {
        "name": case.name,
        "top": case.top,
        "returncode": proc.returncode,
        "warnings": output.count("%Warning"),
        "errors": output.count("%Error"),
        "output_tail": "\n".join(output.splitlines()[-12:]),
        "pass": proc.returncode == 0,
    }


def run_rtl_suite(*, log_dir: Path | None = None) -> dict[str, Any]:
    # Icarus cases are tiny; Verilator cases invoke independent generated builds.
    with ThreadPoolExecutor(max_workers=3) as pool:
        rtl = list(pool.map(lambda case: run_rtl_case(case, log_dir=log_dir), RTL_CASES))
    with ThreadPoolExecutor(max_workers=4) as pool:
        lint = list(pool.map(run_lint_case, LINT_CASES))
    return {
        "tools": {
            "iverilog": _tool_version(["iverilog", "-V"]),
            "verilator4": _tool_version(["verilator", "--version"]),
            "verilator5": _tool_version(
                [str(VERILATOR5), "--version"],
                env={**os.environ, "VERILATOR_ROOT": str(VERILATOR5_ROOT)},
            ),
        },
        "functional": rtl,
        "lint": lint,
        "summary": {
            "functional_passed": sum(item["pass"] for item in rtl),
            "functional_total": len(rtl),
            "golden_checks": sum(item["successes"] for item in rtl),
            "lint_passed": sum(item["pass"] for item in lint),
            "lint_total": len(lint),
            "pass": all(item["pass"] for item in rtl) and all(item["pass"] for item in lint),
        },
    }


def parse_dc_reports() -> dict[str, Any]:
    points: list[dict[str, Any]] = []
    for spec in REPORT_SPECS:
        area_path = _rel(spec.area_report)
        timing_path = _rel(spec.timing_report)
        area_text = area_path.read_text(encoding="utf-8", errors="replace")
        timing_text = timing_path.read_text(encoding="utf-8", errors="replace")
        area_match = AREA_RE.search(area_text)
        total_area_match = TOTAL_AREA_RE.search(area_text)
        arrivals = [float(value) for value in ARRIVAL_RE.findall(timing_text) if float(value) >= 0]
        if area_match is None or total_area_match is None or not arrivals:
            raise ValueError(f"cannot parse HPTPE DC reports for {spec.name}")
        points.append(
            {
                "name": spec.name,
                "target_path": spec.target_path,
                "period_ns": spec.period_ns,
                "frequency_mhz": 1000.0 / spec.period_ns,
                "data_arrival_ns": max(arrivals),
                "timing_met": "slack (MET)" in timing_text,
                "total_cell_area_um2": float(area_match.group(1)),
                "total_area_um2": float(total_area_match.group(1)),
                "area_report": str(area_path.relative_to(PROJECT_ROOT)),
                "timing_report": str(timing_path.relative_to(PROJECT_ROOT)),
                "area_sha256": _sha256(area_path),
                "timing_sha256": _sha256(timing_path),
            }
        )
    return {
        "evidence_type": "author_synopsys_dc_report_replay",
        "library": "SAED32 RVT tt0p85v25c",
        "fresh_synthesis": False,
        "points": points,
        "summary": {
            "points": len(points),
            "timing_met": sum(point["timing_met"] for point in points),
            "pass": all(point["timing_met"] for point in points),
        },
    }


def _nested(data: dict[str, Any], path: Iterable[str]) -> Any:
    value: Any = data
    for part in path:
        value = value[part]
    return value


def _relative_error(observed: float, target: float) -> float:
    return abs(observed - target) / abs(target)


def evaluate_hptpe_endpoints(
    dc: dict[str, Any],
    rtl: dict[str, Any],
    *,
    target_path: Path = PAPER_TARGETS,
    limit_override: float | None = None,
) -> dict[str, Any]:
    targets_root = json.loads(target_path.read_text(encoding="utf-8"))
    targets = targets_root["hptpe"]
    limit = (
        float(limit_override)
        if limit_override is not None
        else float(targets_root["revised_stack_max_relative_error"])
    )
    endpoints: list[dict[str, Any]] = []
    for point in dc["points"]:
        target = _nested(targets, point["target_path"])
        for metric in ("frequency_mhz", "total_cell_area_um2"):
            observed = float(point[metric])
            expected = float(target[metric])
            error = _relative_error(observed, expected)
            endpoints.append(
                {
                    "name": f"{point['name']}.{metric}",
                    "observed": observed,
                    "target": expected,
                    "relative_error": error,
                    "limit": limit,
                    "pass": error <= limit,
                    "evidence": "author_dc_report_replay",
                }
            )
    functional = {item["name"]: item for item in rtl["functional"]}
    for name, case_name, target_key in (
        ("opt3_opt4c.opt3_average_cal_cycles", "opt3_pe", "opt3_average_cal_cycles"),
        ("opt3_opt4c.opt4c_average_cal_cycles", "opt4c", "opt4c_average_cal_cycles"),
    ):
        observed_raw = functional[case_name]["average_cal_cycle"]
        if observed_raw is None:
            raise ValueError(f"missing RTL average cycle for {case_name}")
        observed = float(observed_raw)
        expected = float(targets["opt3_opt4c"][target_key])
        error = _relative_error(observed, expected)
        endpoints.append(
            {
                "name": name,
                "observed": observed,
                "target": expected,
                "relative_error": error,
                "limit": limit,
                "pass": error <= limit,
                "evidence": "executed_open_rtl_testbench",
            }
        )
    return {
        "endpoints": endpoints,
        "passed": sum(endpoint["pass"] for endpoint in endpoints),
        "total": len(endpoints),
        "max_relative_error": max(endpoint["relative_error"] for endpoint in endpoints),
        "limit": limit,
        "pass": all(endpoint["pass"] for endpoint in endpoints),
        "evidence_counts": {
            "author_dc_report_replay": sum(endpoint["evidence"] == "author_dc_report_replay" for endpoint in endpoints),
            "executed_open_rtl_testbench": sum(endpoint["evidence"] == "executed_open_rtl_testbench" for endpoint in endpoints),
        },
    }


def run_hptpe_reproduction(
    *,
    run_id: str,
    log_dir: Path | None = None,
    limit: float | None = None,
) -> dict[str, Any]:
    if _git_head(HPTPE_ROOT) != HPTPE_COMMIT:
        raise RuntimeError("HPTPE reference revision drift")
    if _git_head(VERILATOR5_ROOT) != VERILATOR5_COMMIT:
        raise RuntimeError("Verilator 5 reference revision drift")
    rtl = run_rtl_suite(log_dir=log_dir)
    dc = parse_dc_reports()
    accuracy = evaluate_hptpe_endpoints(dc, rtl, limit_override=limit)
    point = {item["name"]: item for item in dc["points"]}
    derived = {
        dataflow: {
            "frequency_speedup": point[f"opt1.{dataflow}.optimized"]["frequency_mhz"]
            / point[f"opt1.{dataflow}.baseline"]["frequency_mhz"],
            "cell_area_ratio": point[f"opt1.{dataflow}.optimized"]["total_cell_area_um2"]
            / point[f"opt1.{dataflow}.baseline"]["total_cell_area_um2"],
        }
        for dataflow in ("os", "ws", "cube")
    }
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "component": "HPTPE",
        "source": {
            "paper": "Exploring the Performance Improvement of Tensor Processing Engines through Transformation in the Bit-weight Dimension of MACs",
            "doi": "10.1109/HPCA61900.2025.00058",
            "hptpe_commit": HPTPE_COMMIT,
            "verilator5_commit": VERILATOR5_COMMIT,
            "official_ws_top_missing": not _rel("OPT1/systolic_array_ws/array_opt1_based/top.v").exists(),
            "reconstructed_ws_top": str(WS_OPT_TOP.relative_to(PROJECT_ROOT)),
            "reconstructed_ws_top_sha256": _sha256(WS_OPT_TOP),
        },
        "configuration": {
            "rtl_cases": [
                {
                    "name": case.name,
                    "simulator": case.simulator,
                    "top": case.top,
                    "rank": case.rank,
                    "parameters": dict(case.parameters),
                    "trials": case.trials,
                }
                for case in RTL_CASES
            ],
            "lint_cases": [case.name for case in LINT_CASES],
            "dc_report_points": [spec.name for spec in REPORT_SPECS],
        },
        "rtl": rtl,
        "dc_reports": dc,
        "paper_accuracy": accuracy,
        "derived_opt1": derived,
        "summary": {
            "rtl_functional_passed": rtl["summary"]["functional_passed"],
            "rtl_functional_total": rtl["summary"]["functional_total"],
            "rtl_golden_checks": rtl["summary"]["golden_checks"],
            "rtl_lint_passed": rtl["summary"]["lint_passed"],
            "rtl_lint_total": rtl["summary"]["lint_total"],
            "paper_endpoints_passed": accuracy["passed"],
            "paper_endpoints_total": accuracy["total"],
            "max_relative_error": accuracy["max_relative_error"],
            "pass": rtl["summary"]["pass"] and dc["summary"]["pass"] and accuracy["pass"],
        },
    }
    return result

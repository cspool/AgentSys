from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from itertools import pairwise
from pathlib import Path
from typing import Any

from .mlx_reference import DEFAULT_CONFIG as DEFAULT_SOURCE_CONFIG
from .workload import PROJECT_ROOT


OPCODE_NAMES = {
    0: "load",
    1: "store",
    2: "fma",
    3: "add",
    4: "max",
    5: "exp",
    6: "div",
    7: "shuffle",
    8: "xfer",
    9: "mul",
}
RTL_SOURCES = (
    "mlx_fp16.sv",
    "mlx_fu.sv",
    "mlx_register_file.sv",
    "mlx_tag_buffer.sv",
    "mlx_config_network.sv",
    "mlx_data_network.sv",
    "mlx_control_logic.sv",
    "mlx_pe_top.sv",
    "mlx_array_4x4.sv",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _evidence(path: Path) -> dict[str, Any]:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": _sha256(path)}


def _execute(
    command: list[str], *, cwd: Path, log: Path, timeout_s: int = 600
) -> subprocess.CompletedProcess[str]:
    process = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_s,
        check=False,
    )
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(process.stdout, encoding="utf-8")
    return process


def _summary(text: str) -> dict[str, int | str]:
    match = re.search(
        r"MLX_ARRAY_PASS workload=(\S+) cycles=(\d+) instructions=(\d+) "
        r"load=(\d+) store=(\d+) compute=(\d+) xfer=(\d+) "
        r"stalls=(\d+) hops=(\d+) conflicts=(\d+)",
        text,
    )
    if match is None:
        raise ValueError("MLX backend log has no PASS summary")
    names = (
        "workload",
        "cycles",
        "instructions",
        "load",
        "store",
        "compute",
        "xfer",
        "stalls",
        "hops",
        "conflicts",
    )
    return {
        name: value if name == "workload" else int(value)
        for name, value in zip(names, match.groups(), strict=True)
    }


def _issues(text: str, backend: str) -> list[dict[str, int]]:
    pattern = re.compile(
        rf"MLX_TRACE backend={backend} event=issue cycle=(\d+) "
        r"pe=(\d+) pc=(\d+) op=(\d+)"
    )
    return [
        {"cycle": int(cycle), "pe": int(pe), "pc": int(pc), "opcode": int(op)}
        for cycle, pe, pc, op in pattern.findall(text)
    ]


def _rtl_events(text: str) -> list[dict[str, int | str]]:
    pattern = re.compile(
        r"MLX_TRACE backend=rtl event=(issue|complete) cycle=(\d+) "
        r"pe=(\d+) pc=(\d+) op=(\d+)"
    )
    return [
        {
            "event": event,
            "cycle": int(cycle),
            "pe": int(pe),
            "pc": int(pc),
            "opcode": int(opcode),
            "operation": OPCODE_NAMES[int(opcode)],
        }
        for event, cycle, pe, pc, opcode in pattern.findall(text)
    ]


def _compare(cycle: list[dict[str, int]], rtl: list[dict[str, int]]) -> dict[str, Any]:
    def keys(events: list[dict[str, int]]) -> list[tuple[int, int, int]]:
        return [(item["pe"], item["pc"], item["opcode"]) for item in events]

    def per_pe(events: list[dict[str, int]]) -> dict[str, list[list[int]]]:
        streams = {str(pe): [] for pe in range(16)}
        for item in events:
            streams[str(item["pe"])].append([item["pc"], item["opcode"]])
        return streams

    cycle_keys = keys(cycle)
    rtl_keys = keys(rtl)
    return {
        "same_instruction_multiset": sorted(cycle_keys) == sorted(rtl_keys),
        "same_per_pe_program_order": per_pe(cycle) == per_pe(rtl),
        "same_global_issue_order": cycle_keys == rtl_keys,
        "cycle_issue_events": len(cycle_keys),
        "rtl_issue_events": len(rtl_keys),
    }


def _timing(events: list[dict[str, int | str]]) -> dict[str, Any]:
    issues: dict[tuple[int, int, int], int] = {}
    latencies = {name: [] for name in OPCODE_NAMES.values()}
    issue_cycles = {name: [] for name in OPCODE_NAMES.values()}
    for event in events:
        key = (int(event["pe"]), int(event["pc"]), int(event["opcode"]))
        operation = str(event["operation"])
        if event["event"] == "issue":
            issues[key] = int(event["cycle"])
            issue_cycles[operation].append(int(event["cycle"]))
        elif key in issues:
            latencies[operation].append(int(event["cycle"]) - issues[key])
    result: dict[str, Any] = {}
    for name in OPCODE_NAMES.values():
        cycles = sorted(set(issue_cycles[name]))
        intervals = [right - left for left, right in pairwise(cycles) if right > left]
        values = latencies[name]
        result[name] = {
            "observations": len(values),
            "latency_min": min(values) if values else None,
            "latency_max": max(values) if values else None,
            "observed_global_ii_min": min(intervals) if intervals else None,
        }
    return result


def run_mlx_standalone(
    *,
    run_id: str = "run_043",
    source_config_path: Path = DEFAULT_SOURCE_CONFIG,
    output_dir: Path | None = None,
) -> dict[str, Any]:
    source_config = json.loads(source_config_path.read_text(encoding="utf-8"))
    source_root = (PROJECT_ROOT / source_config["active_path"]).resolve()
    output_dir = (
        output_dir or PROJECT_ROOT / "artifacts/mlx_standalone" / run_id
    ).resolve()
    build_dir = output_dir / "build"
    log_dir = output_dir / "logs"
    build_dir.mkdir(parents=True, exist_ok=True)
    rtl_root = source_root / "rtl/mlx"
    cycle_binary = build_dir / "mlx-cycle.vvp"
    verilator_dir = build_dir / "verilator"
    rtl_binary = verilator_dir / "Vmlx_array_4x4"

    cycle_command = [
        "iverilog",
        "-g2012",
        "-DMLX_CYCLE_MODEL",
        "-s",
        "tb_mlx_array_4x4",
        "-o",
        str(cycle_binary),
        str(rtl_root / "mlx_fp16.sv"),
        str(rtl_root / "mlx_fu.sv"),
        str(rtl_root / "mlx_cycle_model.sv"),
        str(rtl_root / "tb_mlx_array_4x4.sv"),
    ]
    cycle_build = _execute(
        cycle_command, cwd=PROJECT_ROOT, log=log_dir / "build-cycle.log"
    )
    verilator_dir.mkdir(parents=True, exist_ok=True)
    rtl_command = [
        "verilator",
        "--cc",
        "--exe",
        "--trace",
        "--top-module",
        "mlx_array_4x4",
        "-Wno-fatal",
        "-Wno-PINCONNECTEMPTY",
        "-Wno-DECLFILENAME",
        "-Wno-WIDTH",
        "-Wno-UNUSED",
        "-DMLX_NO_WRAPPERS",
        "--Mdir",
        str(verilator_dir),
        *(str(rtl_root / name) for name in RTL_SOURCES),
        str(rtl_root / "sim_mlx_array.cpp"),
    ]
    verilate = _execute(
        rtl_command, cwd=PROJECT_ROOT, log=log_dir / "build-rtl-verilate.log"
    )
    make = _execute(
        ["make", "-C", str(verilator_dir), "-f", "Vmlx_array_4x4.mk", "-j4"],
        cwd=PROJECT_ROOT,
        log=log_dir / "build-rtl-cxx.log",
    )
    if cycle_build.returncode or verilate.returncode or make.returncode:
        raise RuntimeError("MLX standalone build failed; inspect build logs")

    manifest_path = source_root / "artifacts/environment/h205/mlx-system-workload-manifest.json"
    workload_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records: list[dict[str, Any]] = []
    all_rtl_events: list[dict[str, int | str]] = []
    for workload in workload_manifest["workloads"]:
        name = workload["name"]
        program = source_root / workload["program"]
        input_hex = source_root / workload["input_hex"]
        golden_hex = source_root / workload["golden_hex"]
        cycle_log = log_dir / "cycle" / f"{name}.log"
        cycle_process = _execute(
            [
                "vvp",
                str(cycle_binary),
                f"+PROGRAM={program}",
                f"+INPUT={input_hex}",
                f"+GOLDEN={golden_hex}",
                f"+WORKLOAD={name}",
                f"+INPUT_VECTORS={workload['input_vectors']}",
                f"+OUTPUT_VECTORS={workload['output_vectors']}",
                f"+OUTPUT_BASE={workload['output_spm_base']}",
            ],
            cwd=PROJECT_ROOT,
            log=cycle_log,
        )
        rtl_log = log_dir / "rtl" / f"{name}.log"
        rtl_process = _execute(
            [
                str(rtl_binary),
                str(program),
                str(input_hex),
                str(golden_hex),
                name,
                str(workload["input_vectors"]),
                str(workload["output_vectors"]),
                str(workload["output_spm_base"]),
            ],
            cwd=PROJECT_ROOT,
            log=rtl_log,
        )
        cycle_text = cycle_log.read_text(encoding="utf-8")
        rtl_text = rtl_log.read_text(encoding="utf-8")
        cycle_summary = _summary(cycle_text)
        rtl_summary = _summary(rtl_text)
        rtl_events = _rtl_events(rtl_text)
        all_rtl_events.extend(rtl_events)
        records.append(
            {
                "workload": name,
                "source": {
                    "program": _evidence(program),
                    "input": _evidence(input_hex),
                    "golden": _evidence(golden_hex),
                },
                "cycle": {
                    "returncode": cycle_process.returncode,
                    "summary": cycle_summary,
                    "log": _evidence(cycle_log),
                },
                "rtl": {
                    "returncode": rtl_process.returncode,
                    "summary": rtl_summary,
                    "trace_events": len(rtl_events),
                    "log": _evidence(rtl_log),
                },
                "comparison": {
                    "instruction_count": cycle_summary["instructions"]
                    == rtl_summary["instructions"]
                    == workload["instruction_count"],
                    "cycle_to_rtl_ratio": cycle_summary["cycles"]
                    / rtl_summary["cycles"],
                    "events": _compare(
                        _issues(cycle_text, "cycle"), _issues(rtl_text, "rtl")
                    ),
                },
            }
        )
    timing = _timing(all_rtl_events)
    source_files = [
        rtl_root / "mlx_cycle_model.sv",
        *(rtl_root / name for name in RTL_SOURCES),
        rtl_root / "tb_mlx_array_4x4.sv",
        rtl_root / "sim_mlx_array.cpp",
    ]
    gates = {
        "tool_and_source_pins": source_config["active_commit"]
        == subprocess.check_output(
            ["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True
        ).strip()
        and not subprocess.check_output(
            [
                "git",
                "-C",
                str(source_root),
                "status",
                "--porcelain",
                "--untracked-files=no",
            ],
            text=True,
        ).strip(),
        "fresh_builds": cycle_build.returncode == verilate.returncode == make.returncode == 0
        and cycle_binary.is_file()
        and rtl_binary.is_file(),
        "eight_golden_runs": len(records) == 4
        and all(
            record[backend]["returncode"] == 0
            for record in records
            for backend in ("cycle", "rtl")
        ),
        "instruction_conservation": all(
            record["comparison"]["instruction_count"] for record in records
        ),
        "architectural_sequence_identity": all(
            record["comparison"]["events"]["same_instruction_multiset"]
            and record["comparison"]["events"]["same_per_pe_program_order"]
            for record in records
        ),
        "global_interleaving_differs": any(
            not record["comparison"]["events"]["same_global_issue_order"]
            for record in records
        ),
        "all_opcode_timing": set(timing) == set(OPCODE_NAMES.values())
        and all(
            item["observations"] > 0
            and item["latency_min"] is not None
            and item["observed_global_ii_min"] is not None
            for item in timing.values()
        ),
        "stalls_and_conflicts_measured": all(
            record["cycle"]["summary"]["stalls"]
            + record["rtl"]["summary"]["stalls"]
            > 0
            for record in records
        )
        and any(
            record["cycle"]["summary"]["conflicts"]
            + record["rtl"]["summary"]["conflicts"]
            > 0
            for record in records
        ),
        "complete_hash_chain": all(path.is_file() and path.stat().st_size > 0 for path in source_files)
        and all(
            all(item["sha256"] for item in record["source"].values())
            and record["cycle"]["log"]["sha256"]
            and record["rtl"]["log"]["sha256"]
            for record in records
        ),
        "target_free": workload_manifest["paper_performance_targets_consumed"] is False,
    }
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "fresh_target_free_mlx_cycle_and_physical_4x4_rtl_execution",
        "paper_performance_targets_consumed": False,
        "source": {
            "root": str(source_root),
            "commit": source_config["active_commit"],
            "files": {str(path.relative_to(source_root)): _evidence(path) for path in source_files},
            "workload_manifest": _evidence(manifest_path),
        },
        "environment": _evidence(PROJECT_ROOT / "artifacts/mlx_environment/environment.json"),
        "build": {
            "cycle": _evidence(cycle_binary),
            "rtl": _evidence(rtl_binary),
            "commands": {"cycle": cycle_command, "verilator": rtl_command},
        },
        "records": records,
        "instruction_timing": timing,
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "workloads": len(records),
            "executions": len(records) * 2,
            "operations": len(timing),
            "pass": all(gates.values()),
        },
    }
    result_path = output_dir / "mlx-standalone.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["output"] = str(result_path)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freshly build and run MLX cycle/RTL backends")
    parser.add_argument("--run-id", default="run_043")
    parser.add_argument("--source-config", type=Path, default=DEFAULT_SOURCE_CONFIG)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args(argv)
    result = run_mlx_standalone(
        run_id=args.run_id,
        source_config_path=args.source_config,
        output_dir=args.output_dir,
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

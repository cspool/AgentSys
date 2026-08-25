from __future__ import annotations

import hashlib
import json
import re
import subprocess
from dataclasses import replace
from pathlib import Path
from typing import Any, Iterable

from .mllm_backend import MLLM_ROOT, MllmOperator, parse_mir
from .model import Engine
from .tisa import TISAMode, TISASimulator
from .workloads import tisa_model_workload


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAMULATOR_ROOT = PROJECT_ROOT / ".references" / "ramulator2"
RAMULATOR_EXE = RAMULATOR_ROOT / "build-clang" / "ramulator2"
RAMULATOR_COMMIT = "be93be78055d922aa1d4d33e15bcc8f2b0c61a9d"
STAT_RE = re.compile(r"^\s*([A-Za-z0-9_]+):\s+([0-9]+(?:\.[0-9]+)?)\s*$", re.MULTILINE)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate_load_store_records(
    operators: Iterable[MllmOperator], *, max_records: int = 32768
) -> tuple[list[str], dict[str, int]]:
    records: list[str] = []
    loads = 0
    stores = 0
    logical_bytes = 0
    operators_included = 0
    address_limit = 1 << 31

    for operator in operators:
        if operator.engine is not Engine.DE:
            continue
        op_records: list[str] = []
        for access, tensors in (("LD", operator.inputs), ("ST", operator.outputs)):
            for tensor in tensors:
                base = (int(tensor.ssa) * 0x100000) % address_limit
                line_count = max(1, (tensor.bytes + 63) // 64)
                for line in range(line_count):
                    address = (base + line * 64) % address_limit
                    op_records.append(f"{access} 0x{address:08x}")
                logical_bytes += tensor.bytes
        if records and len(records) + len(op_records) > max_records:
            break
        records.extend(op_records)
        loads += sum(record.startswith("LD") for record in op_records)
        stores += sum(record.startswith("ST") for record in op_records)
        operators_included += 1
        if len(records) >= max_records:
            break
    return records, {
        "records": len(records),
        "loads": loads,
        "stores": stores,
        "logical_bytes": logical_bytes,
        "operators": operators_included,
    }


def config_text(trace_path: Path, channels: int) -> str:
    return f"""Frontend:
  impl: LoadStoreTrace
  clock_ratio: 1
  path: {trace_path}

MemorySystem:
  impl: GenericDRAM
  clock_ratio: 1
  DRAM:
    impl: DDR4
    org:
      preset: DDR4_8Gb_x8
      channel: {channels}
      rank: 2
    timing:
      preset: DDR4_2400R
  Controller:
    impl: Generic
    Scheduler:
      impl: FRFCFS
    RefreshManager:
      impl: AllBank
    RowPolicy:
      impl: OpenRowPolicy
    plugins:
  AddrMapper:
    impl: RoBaRaCoCh
"""


def parse_stats(output: str) -> dict[str, float | int]:
    parsed: dict[str, float | int] = {}
    for key, value in STAT_RE.findall(output):
        number: float | int = float(value) if "." in value else int(value)
        # Top-level total/memory stats are unique. Per-controller names carry
        # channel suffixes and are retained independently.
        parsed[key] = number
    return parsed


def _run(config: Path) -> dict[str, Any]:
    process = subprocess.run(
        [str(RAMULATOR_EXE), "-f", str(config)],
        cwd=RAMULATOR_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=180,
    )
    return {"exit_code": process.returncode, "stats": parse_stats(process.stdout), "log": process.stdout}


def _scale_de(workload, factor: float):
    return tuple(
        replace(tile, duration=max(1, round(tile.duration * factor))) if tile.engine is Engine.DE else tile
        for tile in workload.tiles
    )


def run_ramulator(*, run_id: str = "run_012", max_records: int = 32768) -> dict[str, Any]:
    if not RAMULATOR_EXE.is_file():
        raise FileNotFoundError(f"Ramulator2 executable missing: {RAMULATOR_EXE}")
    commit = subprocess.check_output(
        ["git", "-C", str(RAMULATOR_ROOT), "rev-parse", "HEAD"], text=True
    ).strip()
    if commit != RAMULATOR_COMMIT:
        raise RuntimeError(f"Ramulator2 commit mismatch: {commit}")
    mir_path = MLLM_ROOT / "examples/qwen3_qnn_aot/qwen3_qnn_aot_1.7B.mir"
    operators = parse_mir(mir_path, max_ops=160)
    records, trace_meta = generate_load_store_records(operators, max_records=max_records)
    work_dir = PROJECT_ROOT / "artifacts" / "ramulator2"
    work_dir.mkdir(parents=True, exist_ok=True)
    trace_path = work_dir / "qwen3-de.trace"
    trace_path.write_text("\n".join(records) + "\n", encoding="utf-8")
    configs: dict[int, Path] = {}
    for channels in (1, 2):
        path = work_dir / f"ddr4-{channels}ch.yaml"
        path.write_text(config_text(trace_path.resolve(), channels), encoding="utf-8")
        configs[channels] = path

    runs: dict[str, Any] = {}
    deterministic = True
    for channels, config in configs.items():
        first = _run(config)
        second = _run(config)
        deterministic = deterministic and first["stats"] == second["stats"]
        first["config"] = str(config)
        first["config_sha256"] = sha256(config)
        runs[str(channels)] = first

    one_stats = runs["1"]["stats"]
    two_stats = runs["2"]["stats"]
    one_cycles = int(one_stats["memory_system_cycles"])
    two_cycles = int(two_stats["memory_system_cycles"])
    memory_factor = two_cycles / one_cycles

    workload = tisa_model_workload("llama2", iterations=16)
    simulator = TISASimulator(window=8, dispatch_latency=7)
    tisa_one = simulator.run(_scale_de(workload, 1.0), TISAMode.DYNAMIC)
    tisa_two = simulator.run(_scale_de(workload, memory_factor), TISAMode.DYNAMIC)
    me_ve_same = (
        tisa_one.busy_cycles["me"] == tisa_two.busy_cycles["me"]
        and tisa_one.busy_cycles["ve"] == tisa_two.busy_cycles["ve"]
    )

    gates = {
        "official_exits": runs["1"]["exit_code"] == runs["2"]["exit_code"] == 0,
        "deterministic": deterministic,
        "one_request_counts": one_stats["total_num_read_requests"] == trace_meta["loads"]
        and one_stats["total_num_write_requests"] == trace_meta["stores"],
        "two_request_counts": two_stats["total_num_read_requests"] == trace_meta["loads"]
        and two_stats["total_num_write_requests"] == trace_meta["stores"],
        "two_channels_not_slower": two_cycles <= one_cycles,
        "tisa_me_ve_same": me_ve_same,
        "tisa_two_channels_not_slower": tisa_two.cycles <= tisa_one.cycles,
    }
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "official_ramulator2_v2_0a_trace_simulation",
        "ramulator": {"commit": commit, "executable": str(RAMULATOR_EXE), "sha256": sha256(RAMULATOR_EXE)},
        "source": {"mir": str(mir_path), "mir_sha256": sha256(mir_path)},
        "trace": {**trace_meta, "path": str(trace_path), "sha256": sha256(trace_path)},
        "runs": runs,
        "derived": {
            "one_channel_cycles": one_cycles,
            "two_channel_cycles": two_cycles,
            "two_vs_one_cycle_factor": memory_factor,
            "tisa_one_channel_cycles": tisa_one.cycles,
            "tisa_two_channel_cycles": tisa_two.cycles,
            "tisa_speedup": tisa_one.cycles / tisa_two.cycles,
            "one_channel_de_cycles": tisa_one.busy_cycles["de"],
            "two_channel_de_cycles": tisa_two.busy_cycles["de"],
        },
        "tisa": {"one_channel": tisa_one.to_dict(), "two_channel": tisa_two.to_dict()},
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }


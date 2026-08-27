from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any

from .mlx_reference import DEFAULT_CONFIG as DEFAULT_SOURCE_CONFIG
from .paths import chipyard_source_identity, expand_chipyard_tokens
from .workload import PROJECT_ROOT


BACKENDS = {"cycle": "MLXCycleRocketConfig", "rtl": "MLXRTLRocketConfig"}
RTL_FILES = (
    "mlx_fp16.sv",
    "mlx_fu.sv",
    "mlx_register_file.sv",
    "mlx_tag_buffer.sv",
    "mlx_config_network.sv",
    "mlx_data_network.sv",
    "mlx_control_logic.sv",
    "mlx_pe_top.sv",
    "mlx_array_4x4.sv",
    "mlx_cycle_model.sv",
    "mlx_rocc_controller.sv",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _evidence(path: Path) -> dict[str, Any]:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": _sha256(path)}


def _run(
    command: list[str], *, log: Path, timeout_s: int = 1800
) -> dict[str, Any]:
    started = time.monotonic_ns()
    process = subprocess.run(
        command,
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_s,
        check=False,
    )
    finished = time.monotonic_ns()
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(process.stdout, encoding="utf-8")
    return {
        "command": command,
        "exit_code": process.returncode,
        "wall_time_s": (finished - started) / 1e9,
        "log": _evidence(log),
        "pass": process.returncode == 0,
    }


def _parse(text: str) -> dict[str, int | str]:
    line = next(
        (line for line in text.splitlines() if "AGENTSYS_MLX_SMOKE_PASS " in line),
        None,
    )
    if line is None:
        raise ValueError("Rocket log has no AGENTSYS_MLX_SMOKE_PASS line")
    line = line[line.index("AGENTSYS_MLX_SMOKE_PASS ") :]
    values: dict[str, int | str] = {}
    for key, value in re.findall(r"(\w+)=([^\s]+)", line):
        if key in {"workload", "backend"}:
            values[key] = value
        elif key == "abi":
            values[key] = int(value, 16)
        else:
            values[key] = int(value)
    values["host_total"] = int(values["host_config"]) + int(
        values["host_launch_wait"]
    )
    return values


def run_mlx_chipyard(
    *,
    run_id: str = "run_044",
    source_config_path: Path = DEFAULT_SOURCE_CONFIG,
    output_dir: Path | None = None,
    build: bool = True,
) -> dict[str, Any]:
    source_config = expand_chipyard_tokens(
        json.loads(source_config_path.read_text(encoding="utf-8"))
    )
    source_root = (PROJECT_ROOT / source_config["active_path"]).resolve()
    chipyard = Path(source_config["chipyard"]["path"])
    output_dir = (
        output_dir or PROJECT_ROOT / "artifacts/mlx_chipyard" / run_id
    ).resolve()
    logs = output_dir / "logs"
    software = output_dir / "software"
    software.mkdir(parents=True, exist_ok=True)
    manifest_path = source_root / "artifacts/environment/h205/mlx-system-workload-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    standalone_path = PROJECT_ROOT / "artifacts/mlx_standalone/run_043/mlx-standalone.json"
    standalone = json.loads(standalone_path.read_text(encoding="utf-8"))
    standalone_by_name = {item["workload"]: item for item in standalone["records"]}
    stages: dict[str, Any] = {}

    if build:
        stages["install"] = _run(
            ["bash", "scripts/install_mlx_chipyard.sh", str(chipyard)],
            log=logs / "install.log",
        )
    compiler = chipyard / "esp-tools-install/bin/riscv64-unknown-elf-gcc"
    source_c = PROJECT_ROOT / "system_sim/software/agentsys_mlx_smoke.c"
    elfs: dict[str, Path] = {}
    for workload in manifest["workloads"]:
        name = workload["name"]
        elf = software / f"mlx-{name}.riscv"
        elfs[name] = elf
        header = source_root / workload["header"]
        command = [
            str(compiler),
            "-std=gnu99",
            "-O2",
            "-g",
            "-fno-common",
            "-fno-builtin-printf",
            "-Wall",
            "-Wextra",
            f"-I{chipyard / 'tests'}",
            f"-I{source_root / 'system_sim/software'}",
            f"-I{header.parent}",
            f'-DMLX_WORKLOAD_HEADER="{header.name}"',
            str(source_c),
            "-static",
            "-specs=htif_nano.specs",
            "-o",
            str(elf),
        ]
        stages[f"elf_{name}"] = _run(command, log=logs / f"build-elf-{name}.log")

    for backend, config_name in BACKENDS.items():
        simulator = chipyard / f"sims/verilator/simulator-chipyard-{config_name}"
        if build:
            stages[f"simulator_{backend}"] = _run(
                [
                    "bash",
                    "-lc",
                    f"source {chipyard}/env.sh && make -C {chipyard}/sims/verilator CONFIG={config_name} -j4",
                ],
                log=logs / f"build-simulator-{backend}.log",
            )
        if not simulator.is_file():
            raise FileNotFoundError(simulator)

    installed_root = chipyard / "generators/chipyard/src/main"
    installed_pairs = [
        (
            source_root / "system_sim/chipyard/MLXRoCC.scala",
            installed_root / "scala/MLXRoCC.scala",
        ),
        *(
            (
                source_root / f"rtl/mlx/{name}",
                installed_root / f"resources/vsrc/{name}",
            )
            for name in RTL_FILES
        ),
    ]
    records: list[dict[str, Any]] = []
    for backend, config_name in BACKENDS.items():
        simulator = chipyard / f"sims/verilator/simulator-chipyard-{config_name}"
        for workload in manifest["workloads"]:
            name = workload["name"]
            log = logs / backend / f"{name}.log"
            execution = _run([str(simulator), str(elfs[name])], log=log, timeout_s=600)
            summary = _parse(log.read_text(encoding="utf-8"))
            expected_kernel = standalone_by_name[name][backend]["summary"]
            expected_dma_bytes = 64 * (
                int(workload["input_vectors"]) + int(workload["output_vectors"])
            )
            checks = {
                "exit_and_identity": execution["pass"]
                and summary["workload"] == name
                and summary["backend"] == backend
                and summary["mismatches"] == 0,
                "kernel_and_instructions": summary["kernel"]
                == expected_kernel["cycles"]
                and summary["instructions"] == workload["instruction_count"],
                "operation_accounting": summary["instructions"]
                == summary["load"]
                + summary["store"]
                + summary["compute"]
                + summary["xfer"],
                "dma": summary["dma"] > 0
                and summary["dma_bytes"] == expected_dma_bytes,
                "system_accounting": summary["system"]
                == summary["dma"] + summary["kernel"] + 2,
                "host_accounting": summary["host_config"] > 0
                and summary["host_launch_wait"] > 0
                and summary["host_total"] > summary["system"],
                "abi": summary["abi"] == 0x4D4C5801,
            }
            records.append(
                {
                    "backend": backend,
                    "config": config_name,
                    "workload": name,
                    "elf": _evidence(elfs[name]),
                    "simulator": _evidence(simulator),
                    "execution": execution,
                    "summary": summary,
                    "checks": checks,
                    "pass": all(checks.values()),
                }
            )

    active_clean = not subprocess.check_output(
        [
            "git",
            "-C",
            str(source_root),
            "status",
            "--porcelain",
            "--untracked-files=no",
        ],
        text=True,
    ).strip()
    gates = {
        "installed_sources_match": len(installed_pairs) == 12
        and all(target.is_file() and source.read_bytes() == target.read_bytes() for source, target in installed_pairs),
        "two_simulators": all(
            (chipyard / f"sims/verilator/simulator-chipyard-{config}").is_file()
            for config in BACKENDS.values()
        ),
        "four_distinct_elfs": len(elfs) == 4
        and len({_sha256(path) for path in elfs.values()}) == 4,
        "eight_golden_runs": len(records) == 8 and all(item["pass"] for item in records),
        "standalone_kernel_identity": all(item["checks"]["kernel_and_instructions"] for item in records),
        "operation_conservation": all(item["checks"]["operation_accounting"] for item in records),
        "dma_contract": all(item["checks"]["dma"] for item in records),
        "system_cycle_contract": all(item["checks"]["system_accounting"] for item in records),
        "host_cycle_contract": all(item["checks"]["host_accounting"] for item in records),
        "abi_and_backend_status": all(item["checks"]["abi"] for item in records)
        and {item["summary"]["backend"] for item in records} == {"cycle", "rtl"},
        "active_source_clean": active_clean,
        "target_free": standalone["paper_performance_targets_consumed"] is False,
    }
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "measured_ordinary_rocket_custom0_dma_mlx_cycle_and_rtl_system",
        "paper_performance_targets_consumed": False,
        "source": {
            "path": str(source_root),
            "commit": source_config["active_commit"],
            "clean": active_clean,
            "manifest": _evidence(manifest_path),
            "standalone_parent": _evidence(standalone_path),
            "software": _evidence(source_c),
        },
        "chipyard": {
            "path": str(chipyard),
            "commit": chipyard_source_identity(chipyard)["commit"],
            "source_identity": chipyard_source_identity(chipyard),
            "installed": {
                str(target): {"source": _evidence(source), "target": _evidence(target)}
                for source, target in installed_pairs
            },
        },
        "stages": stages,
        "records": records,
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "workloads": 4,
            "backends": 2,
            "executions": len(records),
            "pass": all(gates.values()),
        },
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "mlx-chipyard.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["output"] = str(output)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build and execute MLX on ordinary Rocket")
    parser.add_argument("--run-id", default="run_044")
    parser.add_argument("--source-config", type=Path, default=DEFAULT_SOURCE_CONFIG)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--reuse-build", action="store_true")
    args = parser.parse_args(argv)
    result = run_mlx_chipyard(
        run_id=args.run_id,
        source_config_path=args.source_config,
        output_dir=args.output_dir,
        build=not args.reuse_build,
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

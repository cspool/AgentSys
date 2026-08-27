from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Callable

from .parameterized_application import write_parameterized_application
from .parameterized_compiler import (
    build_parameterized_elf,
    compile_parameterized_workload,
)
from .parameterized_system import write_parameterized_system
from .toolchain import PROJECT_ROOT
from .workload import AgentWorkload, load_agent_workload


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _stage(name: str, operation: Callable[[], Any]) -> tuple[Any, dict[str, Any]]:
    started_ns = time.time_ns()
    result = operation()
    finished_ns = time.time_ns()
    return result, {
        "name": name,
        "started_ns": started_ns,
        "finished_ns": finished_ns,
        "wall_time_s": (finished_ns - started_ns) / 1_000_000_000,
        "pass": True,
    }


def default_output_dir(workload: AgentWorkload, run_id: str) -> Path:
    return (
        PROJECT_ROOT
        / "artifacts/workloads"
        / workload.name
        / workload.sha256[:12]
        / run_id
    )


def run_workload_pipeline(
    workload_path: Path,
    *,
    run_id: str,
    output_dir: Path | None = None,
    execute_system: bool = True,
    component_certificate: Path | None = None,
    timeout_s: float = 300.0,
) -> dict[str, Any]:
    workload = load_agent_workload(workload_path)
    workload.hardware.require_installed_profile()
    output_dir = (output_dir or default_output_dir(workload, run_id)).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    application_path = output_dir / "application.json"
    compiled_path = output_dir / "compiled.json"
    header_path = output_dir / "generated/workload.h"
    elf_path = output_dir / "software/workload.riscv"
    result_path = output_dir / "system.json"
    trace_path = output_dir / "system-trace.jsonl"

    stages: list[dict[str, Any]] = []
    application, evidence = _stage(
        "agentix_application",
        lambda: write_parameterized_application(
            workload, application_path, run_id=run_id
        ),
    )
    evidence["outputs"] = {
        str(application_path): {
            "bytes": application_path.stat().st_size,
            "sha256": _sha256(application_path),
        }
    }
    stages.append(evidence)

    compiled, evidence = _stage(
        "mllm_agentxpu_tisa_compile",
        lambda: compile_parameterized_workload(
            workload,
            application,
            application_path=application_path,
            manifest_path=compiled_path,
            header_path=header_path,
            run_id=run_id,
        ),
    )
    evidence["outputs"] = {
        str(path): {"bytes": path.stat().st_size, "sha256": _sha256(path)}
        for path in (compiled_path, header_path)
    }
    evidence["pass"] = bool(compiled["summary"]["pass"])
    stages.append(evidence)

    build, evidence = _stage(
        "riscv_elf_build",
        lambda: build_parameterized_elf(header_path, elf_path),
    )
    evidence["outputs"] = {
        str(elf_path): {"bytes": elf_path.stat().st_size, "sha256": _sha256(elf_path)}
    }
    evidence["pass"] = bool(build["pass"])
    evidence["details"] = build
    stages.append(evidence)

    system: dict[str, Any] | None = None
    if execute_system:
        certificate = component_certificate
        if certificate is None:
            default_certificate = (
                PROJECT_ROOT / "artifacts/results/revised-components-run_028.json"
            )
            certificate = default_certificate if default_certificate.is_file() else None
        system, evidence = _stage(
            "rocket_tisa_hptpe_system",
            lambda: write_parameterized_system(
                workload,
                compiled_path,
                elf_path,
                result_path,
                trace_path,
                run_id=run_id,
                output_dir=output_dir,
                component_certificate=certificate,
                timeout_s=timeout_s,
            ),
        )
        evidence["outputs"] = {
            str(path): {"bytes": path.stat().st_size, "sha256": _sha256(path)}
            for path in (
                result_path,
                trace_path,
                output_dir / "logs/static.log",
                output_dir / "logs/dynamic.log",
                output_dir / "logs/static-tisa.log",
                output_dir / "logs/dynamic-tisa.log",
            )
        }
        evidence["pass"] = bool(system["summary"]["pass"])
        stages.append(evidence)

    serial_order = all(
        later["started_ns"] >= earlier["finished_ns"]
        for earlier, later in zip(stages, stages[1:])
    )
    passed = all(stage["pass"] for stage in stages) and serial_order
    pipeline = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "parameterized_agent_workload_end_to_end_pipeline",
        "workload": workload.to_contract_dict(),
        "output_dir": str(output_dir),
        "stages": stages,
        "artifacts": {
            "application": str(application_path),
            "compiled": str(compiled_path),
            "header": str(header_path),
            "elf": str(elf_path),
            "system": str(result_path) if execute_system else None,
            "trace": str(trace_path) if execute_system else None,
        },
        "system_summary": system["summary"] if system is not None else None,
        "summary": {
            "stages": len(stages),
            "passing": sum(stage["pass"] for stage in stages),
            "failing": len(stages) - sum(stage["pass"] for stage in stages),
            "serial_order": serial_order,
            "system_executed": execute_system,
            "pass": passed,
        },
    }
    pipeline_path = output_dir / "pipeline.json"
    pipeline_path.write_text(json.dumps(pipeline, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compile and execute a parameterized Agent workload on Rocket+TISA/HPTPE"
    )
    parser.add_argument("--workload", type=Path, required=True)
    parser.add_argument("--run-id", default="run_local")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--compile-only", action="store_true")
    parser.add_argument("--component-certificate", type=Path)
    parser.add_argument("--timeout-s", type=float, default=300.0)
    args = parser.parse_args(argv)
    result = run_workload_pipeline(
        args.workload,
        run_id=args.run_id,
        output_dir=args.output_dir,
        execute_system=not args.compile_only,
        component_certificate=args.component_certificate,
        timeout_s=args.timeout_s,
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output_dir"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

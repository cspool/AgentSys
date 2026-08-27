from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Callable

from .layer_regression import run_layer_regression
from .toolchain import PROJECT_ROOT
from .workload import load_agent_workload
from .workload_pipeline import run_workload_pipeline


DEFAULT_CONFIG = PROJECT_ROOT / "config/parameterized-system.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _snapshot(root: Path) -> dict[str, Any]:
    return {
        str(path.relative_to(PROJECT_ROOT)): {
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _execute_stage(
    name: str,
    output_root: Path,
    operation: Callable[[], dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any]]:
    started_ns = time.time_ns()
    result = operation()
    finished_ns = time.time_ns()
    passed = bool(result["summary"]["pass"])
    return result, {
        "name": name,
        "started_ns": started_ns,
        "finished_ns": finished_ns,
        "wall_time_s": (finished_ns - started_ns) / 1_000_000_000,
        "output_root": str(output_root),
        "artifacts": _snapshot(output_root),
        "result_summary": result["summary"],
        "pass": passed,
    }


def run_parameterized_reproduction(
    *,
    config_path: Path = DEFAULT_CONFIG,
    run_id: str = "run_032",
    issue_certificate: bool = True,
) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("schema_version") != 1:
        raise ValueError("unsupported parameterized-system config")
    output_root = (PROJECT_ROOT / config["output_root"]).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    stages: list[dict[str, Any]] = []

    layer_root = output_root / "layer-regression"
    layer_result, stage = _execute_stage(
        "five_layer_regression",
        layer_root,
        lambda: run_layer_regression(
            matrix_path=PROJECT_ROOT / config["layer_matrix"],
            run_id=run_id,
            output_dir=layer_root,
        ),
    )
    stages.append(stage)

    workload_results: dict[str, dict[str, Any]] = {}
    if stage["pass"]:
        for workload_text in config["workloads"]:
            workload_path = (PROJECT_ROOT / workload_text).resolve()
            workload = load_agent_workload(workload_path)
            workload_root = output_root / "workloads" / workload.name
            pipeline, stage = _execute_stage(
                f"workload_{workload.name}",
                workload_root,
                lambda path=workload_path, root=workload_root: run_workload_pipeline(
                    path,
                    run_id=run_id,
                    output_dir=root,
                    execute_system=True,
                    component_certificate=PROJECT_ROOT
                    / config["component_certificate"],
                    timeout_s=float(config["timeout_s"]),
                ),
            )
            stages.append(stage)
            workload_results[workload.name] = pipeline
            if not stage["pass"]:
                break

    expected_stages = 1 + len(config["workloads"])
    serial_order = all(
        later["started_ns"] >= earlier["finished_ns"]
        for earlier, later in zip(stages, stages[1:])
    )
    passed = (
        len(stages) == expected_stages
        and all(stage["pass"] for stage in stages)
        and serial_order
    )
    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": config["classification"],
        "configuration": {
            "path": str(config_path),
            "sha256": _sha256(config_path),
        },
        "expected_stage_order": [
            "five_layer_regression",
            *(f"workload_{load_agent_workload(PROJECT_ROOT / path).name}" for path in config["workloads"]),
        ],
        "stage_order": [stage["name"] for stage in stages],
        "stages": stages,
        "layer_summary": layer_result["summary"],
        "workload_summaries": {
            name: value["system_summary"] for name, value in workload_results.items()
        },
        "summary": {
            "stages": expected_stages,
            "executed": len(stages),
            "passing": sum(stage["pass"] for stage in stages),
            "failing": sum(not stage["pass"] for stage in stages),
            "serial_order": serial_order,
            "pass": passed,
        },
    }
    manifest_path = (PROJECT_ROOT / config["manifest"]).resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    certificate: dict[str, Any] | None = None
    if passed and issue_certificate:
        from .parameterized_certificate import write_parameterized_certificate

        certificate_path = (PROJECT_ROOT / config["certificate"]).resolve()
        certificate = write_parameterized_certificate(
            certificate_path,
            config_path=config_path,
            run_id=run_id,
        )
        passed = bool(certificate["summary"]["full_goal_complete"])
    return {
        "manifest": manifest,
        "certificate": certificate,
        "pass": passed,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Serially reproduce the full parameterized Agent experiment system"
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id", default="run_032")
    parser.add_argument("--no-certificate", action="store_true")
    args = parser.parse_args(argv)
    result = run_parameterized_reproduction(
        config_path=args.config,
        run_id=args.run_id,
        issue_certificate=not args.no_certificate,
    )
    print(json.dumps(result["manifest"]["summary"], indent=2, sort_keys=True))
    if result["certificate"] is not None:
        print(json.dumps(result["certificate"]["summary"], indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

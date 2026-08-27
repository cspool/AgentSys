from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path
from typing import Any, Callable

from .mlx_agent_reproduce import run_mlx_agent_reproduction
from .mlx_chipyard import run_mlx_chipyard
from .mlx_layer_regression import run_mlx_layer_regression
from .paths import (
    PROJECT_ROOT,
    chipyard_build_preflight,
    chipyard_source_identity,
    resolve_chipyard_root,
)


DEFAULT_CONFIG = PROJECT_ROOT / "config/project-local-chipyard.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head() -> str:
    return subprocess.check_output(
        ["git", "-C", str(PROJECT_ROOT), "rev-parse", "HEAD"], text=True
    ).strip()


def _write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _stage(
    name: str, operation: Callable[[], dict[str, Any]]
) -> tuple[dict[str, Any], dict[str, Any]]:
    started = time.monotonic_ns()
    result = operation()
    finished = time.monotonic_ns()
    return result, {
        "name": name,
        "started_ns": started,
        "finished_ns": finished,
        "wall_time_s": (finished - started) / 1e9,
        "summary": result["summary"],
        "pass": bool(result["summary"]["pass"]),
    }


def run_portable_reproduction(
    *,
    config_path: Path = DEFAULT_CONFIG,
    run_id: str = "run_051",
    output_root: Path | None = None,
    manifest_path: Path | None = None,
) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("schema_version") != 1:
        raise ValueError("unsupported project-local replay schema")
    output_root = (
        output_root or PROJECT_ROOT / config["output_root"]
    ).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    source_commit = _git_head()
    stages: list[dict[str, Any]] = []
    results: dict[str, dict[str, Any]] = {}

    def preflight_operation() -> dict[str, Any]:
        root = resolve_chipyard_root()
        preflight = chipyard_build_preflight(root)
        simulators = {
            backend: root / f"sims/verilator/simulator-chipyard-{config_name}"
            for backend, config_name in {
                "cycle": "MLXCycleRocketConfig",
                "rtl": "MLXRTLRocketConfig",
            }.items()
        }
        checks = {
            **preflight["checks"],
            **{
                f"simulator_{backend}": path.is_file()
                for backend, path in simulators.items()
            },
        }
        result = {
            "schema_version": 1,
            "run_id": run_id,
            "classification": "project_local_chipyard_build_preflight",
            "chipyard": preflight,
            "simulators": {
                name: {
                    "path": str(path),
                    "bytes": path.stat().st_size if path.is_file() else 0,
                    "sha256": _sha256(path) if path.is_file() else None,
                }
                for name, path in simulators.items()
            },
            "checks": checks,
            "summary": {
                "gates": len(checks),
                "passing": sum(checks.values()),
                "failing": len(checks) - sum(checks.values()),
                "pass": all(checks.values()),
            },
        }
        output = output_root / "preflight.json"
        _write(output, result)
        result["output"] = str(output)
        return result

    result, evidence = _stage(
        "project_local_chipyard_preflight", preflight_operation
    )
    stages.append(evidence)
    results["preflight"] = result

    if evidence["pass"]:
        substrate_root = output_root / "substrate"
        result, evidence = _stage(
            "project_local_mlx_substrate",
            lambda: run_mlx_chipyard(
                run_id=run_id,
                source_config_path=PROJECT_ROOT / config["source_config"],
                output_dir=substrate_root,
                build=False,
            ),
        )
        stages.append(evidence)
        results["substrate"] = result

    if evidence["pass"]:
        agents_root = output_root / "agents"
        result, evidence = _stage(
            "project_local_three_agent_dags",
            lambda: run_mlx_agent_reproduction(
                config_path=PROJECT_ROOT / config["agent_system"],
                run_id=run_id,
                output_root=agents_root,
                manifest_path=agents_root / "reproduction.json",
            ),
        )
        stages.append(evidence)
        results["agents"] = result

    if evidence["pass"]:
        layers_root = output_root / "layers"
        result, evidence = _stage(
            "project_local_six_layer_regression",
            lambda: run_mlx_layer_regression(
                matrix_path=PROJECT_ROOT / config["layer_matrix"],
                run_id=run_id,
                output_root=layers_root,
                output_path=layers_root / "layer-regression.json",
            ),
        )
        stages.append(evidence)
        results["layers"] = result

    expected = config["expected_stage_order"]
    observed = [stage["name"] for stage in stages]
    serial = all(
        later["started_ns"] >= earlier["finished_ns"]
        for earlier, later in zip(stages, stages[1:])
    )
    local_root = (PROJECT_ROOT / "chipyard").resolve()
    root = resolve_chipyard_root()
    substrate = results.get("substrate", {})
    agents = results.get("agents", {})
    layers = results.get("layers", {})
    gates = {
        "four_strict_serial_stages": observed == expected
        and serial
        and all(stage["pass"] for stage in stages),
        "exact_source_commit": _git_head() == source_commit,
        "default_project_local_root": root == local_root,
        "vendored_source_identity": chipyard_source_identity(root)["commit"]
        == "b5d013190d637e634113cb5179f8c8885df1945a",
        "substrate_12_eight_runs": substrate.get("summary", {}).get("passing")
        == substrate.get("summary", {}).get("gates")
        == 12
        and substrate.get("summary", {}).get("executions") == 8,
        "three_agents_9_six_runs": agents.get("summary", {}).get("passing")
        == agents.get("summary", {}).get("gates")
        == 9
        and agents.get("summary", {}).get("workloads") == 3,
        "six_layers_73_two_runs": layers.get("summary", {}).get("passing")
        == layers.get("summary", {}).get("endpoints")
        == 73
        and layers.get("summary", {}).get("gates_passing")
        == layers.get("summary", {}).get("gates")
        == 10,
        "sixteen_fresh_rocket_executions": substrate.get("summary", {}).get(
            "executions", 0
        )
        + 6
        + 2
        == 16,
        "evidence_boundary_retained": layers.get("layers", {})
        .get("mlx", {})
        .get("paper_accuracy", {})
        .get("leave_one_out_max_relative_error", 0)
        > 0.10
        and layers.get("layers", {})
        .get("mlx", {})
        .get("full_paper_scope", {})
        .get("all_paper_experiments_reproduced_within_10pct")
        is False,
    }
    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": config["classification"],
        "evidence_boundary": (
            "post-vendoring project-local Chipyard replay; registered 73-endpoint "
            "contract retains target-informed MLX and negative strict-full-paper scope"
        ),
        "project_commit": source_commit,
        "configuration": {"path": str(config_path), "sha256": _sha256(config_path)},
        "chipyard_root": str(root),
        "stage_order": observed,
        "stages": stages,
        "results": {
            name: {
                "path": value["output"],
                "sha256": _sha256(Path(value["output"])),
                "summary": value["summary"],
            }
            for name, value in results.items()
        },
        "gates": gates,
        "summary": {
            "stages": len(expected),
            "executed": len(stages),
            "passing": sum(stage["pass"] for stage in stages),
            "failing": sum(not stage["pass"] for stage in stages),
            "serial_order": serial,
            "fresh_rocket_executions": 16 if len(stages) == len(expected) else None,
            "paper_endpoints": layers.get("summary", {}).get("endpoints"),
            "agent_workloads": agents.get("summary", {}).get("workloads"),
            "gates": len(gates),
            "gates_passing": sum(gates.values()),
            "pass": all(gates.values()),
        },
    }
    manifest_path = (
        manifest_path or PROJECT_ROOT / config["manifest"]
    ).resolve()
    _write(manifest_path, manifest)
    manifest["output"] = str(manifest_path)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Replay AgentSys on the repository-local Chipyard source"
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id", default="run_051")
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args(argv)
    result = run_portable_reproduction(
        config_path=args.config,
        run_id=args.run_id,
        output_root=args.output_root,
        manifest_path=args.manifest,
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

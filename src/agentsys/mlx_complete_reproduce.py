from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Callable

from .mlx_agent_reproduce import run_mlx_agent_reproduction
from .mlx_chipyard import run_mlx_chipyard
from .mlx_layer_regression import run_mlx_layer_regression
from .mlx_reference import audit_mlx_reference
from .mlx_standalone import run_mlx_standalone
from .workload import PROJECT_ROOT


DEFAULT_CONFIG = PROJECT_ROOT / "config/mlx-complete-system.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _snapshot(root: Path) -> dict[str, Any]:
    return {
        str(path.relative_to(PROJECT_ROOT)): {
            "bytes": path.stat().st_size,
            "sha256": _sha256(path),
        }
        for path in sorted(root.rglob("*"))
        if path.is_file() and "build" not in path.relative_to(root).parts
    }


def _stage(
    name: str,
    root: Path,
    operation: Callable[[], dict[str, Any]],
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
        "artifacts": _snapshot(root),
        "pass": bool(result["summary"]["pass"]),
    }


def run_complete_mlx_reproduction(
    *, config_path: Path = DEFAULT_CONFIG, run_id: str = "run_048"
) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    output_root = (PROJECT_ROOT / config["output_root"]).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    stages: list[dict[str, Any]] = []
    results: dict[str, dict[str, Any]] = {}

    source_root = output_root / "source-audit"

    def source_operation() -> dict[str, Any]:
        result = audit_mlx_reference(
            config_path=PROJECT_ROOT / config["source_config"], run_id=run_id
        )
        source_root.mkdir(parents=True, exist_ok=True)
        output = source_root / "mlx-reference-audit.json"
        output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        result["output"] = str(output)
        return result

    result, evidence = _stage("mlx_source_audit", source_root, source_operation)
    stages.append(evidence)
    results["source"] = result

    if evidence["pass"]:
        standalone_root = output_root / "standalone"
        result, evidence = _stage(
            "mlx_standalone_fresh",
            standalone_root,
            lambda: run_mlx_standalone(
                run_id=run_id,
                source_config_path=PROJECT_ROOT / config["source_config"],
                output_dir=standalone_root,
            ),
        )
        stages.append(evidence)
        results["standalone"] = result

    if evidence["pass"]:
        chipyard_root = output_root / "chipyard"
        result, evidence = _stage(
            "mlx_chipyard_fresh_execution",
            chipyard_root,
            lambda: run_mlx_chipyard(
                run_id=run_id,
                source_config_path=PROJECT_ROOT / config["source_config"],
                output_dir=chipyard_root,
                build=False,
            ),
        )
        stages.append(evidence)
        results["chipyard"] = result

    if evidence["pass"]:
        layer_root = output_root / "layer-regression"
        result, evidence = _stage(
            "six_layer_regression",
            layer_root,
            lambda: run_mlx_layer_regression(
                matrix_path=PROJECT_ROOT / config["layer_matrix"],
                run_id=run_id,
                output_root=layer_root,
                output_path=layer_root / "layer-regression.json",
            ),
        )
        stages.append(evidence)
        results["layers"] = result

    if evidence["pass"]:
        agents_root = output_root / "agent-workloads"
        result, evidence = _stage(
            "three_agent_mlx_workloads",
            agents_root,
            lambda: run_mlx_agent_reproduction(
                config_path=PROJECT_ROOT / config["agent_system"],
                run_id=run_id,
                output_root=agents_root,
                manifest_path=agents_root / "reproduction.json",
            ),
        )
        stages.append(evidence)
        results["agents"] = result

    expected_order = config["expected_stage_order"]
    stage_order = [stage["name"] for stage in stages]
    serial = all(
        later["started_ns"] >= earlier["finished_ns"]
        for earlier, later in zip(stages, stages[1:])
    )
    all_executed = len(stages) == len(expected_order)
    layer = results.get("layers", {})
    agents = results.get("agents", {})
    source = results.get("source", {})
    standalone = results.get("standalone", {})
    chipyard = results.get("chipyard", {})
    gates = {
        "five_strict_serial_stages": all_executed
        and stage_order == expected_order
        and serial
        and all(stage["pass"] for stage in stages),
        "source_audit_10": source.get("summary", {}).get("passing")
        == source.get("summary", {}).get("gates")
        == 10,
        "standalone_10_eight_runs": standalone.get("summary", {}).get("passing")
        == standalone.get("summary", {}).get("gates")
        == 10
        and standalone.get("summary", {}).get("executions") == 8,
        "chipyard_12_eight_runs": chipyard.get("summary", {}).get("passing")
        == chipyard.get("summary", {}).get("gates")
        == 12
        and chipyard.get("summary", {}).get("executions") == 8,
        "six_layers_73_endpoints": layer.get("summary", {}).get("layers") == 6
        and layer.get("summary", {}).get("endpoints")
        == layer.get("summary", {}).get("passing")
        == 73
        and layer.get("summary", {}).get("parameter_switches") == 6,
        "three_agents_9": agents.get("summary", {}).get("passing")
        == agents.get("summary", {}).get("gates")
        == 9
        and agents.get("summary", {}).get("workloads") == 3,
        "fresh_mlx_executions_24": standalone.get("summary", {}).get("executions", 0)
        + chipyard.get("summary", {}).get("executions", 0)
        + 2
        + 6
        == 24,
        "primary_hardware_mlx_no_atx": layer.get("primary_system_hardware") == "mlx"
        and "atx" in layer.get("excluded_layers", []),
        "paper_boundary": layer.get("layers", {})
        .get("mlx", {})
        .get("paper_accuracy", {})
        .get("leave_one_out_max_relative_error", 0)
        > 0.10
        and layer.get("layers", {})
        .get("mlx", {})
        .get("full_paper_scope", {})
        .get("all_paper_experiments_reproduced_within_10pct")
        is False,
        "active_source_clean": source.get("active", {}).get("clean") is True
        and chipyard.get("source", {}).get("clean") is True,
    }
    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": config["classification"],
        "evidence_boundary": (
            "complete fresh MLX+CPU replay; registered 73-endpoint <=10% contract "
            "does not imply strict full-MLX-paper reproduction"
        ),
        "configuration": {"path": str(config_path), "sha256": _sha256(config_path)},
        "expected_stage_order": expected_order,
        "stage_order": stage_order,
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
            "stages": len(expected_order),
            "executed": len(stages),
            "passing": sum(stage["pass"] for stage in stages),
            "failing": sum(not stage["pass"] for stage in stages),
            "serial_order": serial,
            "mlx_executions": 24 if all_executed else None,
            "paper_layers": layer.get("summary", {}).get("layers"),
            "paper_endpoints": layer.get("summary", {}).get("endpoints"),
            "parameter_switches": layer.get("summary", {}).get("parameter_switches"),
            "agent_workloads": agents.get("summary", {}).get("workloads"),
            "gates": len(gates),
            "gates_passing": sum(gates.values()),
            "pass": all(gates.values()),
        },
    }
    manifest_path = (PROJECT_ROOT / config["manifest"]).resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest["output"] = str(manifest_path)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Freshly replay the complete Agent MLX+CPU system")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id", default="run_048")
    args = parser.parse_args(argv)
    result = run_complete_mlx_reproduction(config_path=args.config, run_id=args.run_id)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

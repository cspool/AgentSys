from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path
from typing import Any

from .layer_regression import run_layer_regression
from .mlx_agent_system import run_agent_mlx_system
from .workload import PROJECT_ROOT


DEFAULT_MATRIX = PROJECT_ROOT / "config/mlx-six-layer-matrix.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _identity(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def run_mlx_layer_regression(
    *, matrix_path: Path = DEFAULT_MATRIX, run_id: str = "run_047"
) -> dict[str, Any]:
    started = time.monotonic_ns()
    matrix_path = matrix_path.resolve()
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    if matrix.get("schema_version") != 1:
        raise ValueError("unsupported MLX six-layer matrix")
    active_layers = tuple(matrix["active_layers"])
    if active_layers != ("agentix", "agentxpu", "tisa", "mllm", "hptpe", "mlx"):
        raise ValueError(f"invalid six-layer order: {active_layers}")
    limit = float(matrix["limit"])
    if limit != 0.10:
        raise ValueError("six-layer limit must be exactly 0.10")
    output_root = (PROJECT_ROOT / matrix["output_root"]).resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    base_matrix_path = PROJECT_ROOT / matrix["base_matrix"]
    base = run_layer_regression(
        matrix_path=base_matrix_path,
        run_id=run_id,
        output_dir=output_root / "base-five",
    )
    mlx_spec = matrix["mlx"]
    source_path = (PROJECT_ROOT / mlx_spec["source_artifact"]).resolve()
    if _sha256(source_path) != mlx_spec["source_sha256"]:
        raise ValueError("MLX paper-aligned source artifact hash mismatch")
    source = json.loads(source_path.read_text(encoding="utf-8"))
    full_paper_path = (PROJECT_ROOT / mlx_spec["full_paper_artifact"]).resolve()
    full_paper = json.loads(full_paper_path.read_text(encoding="utf-8"))

    sensitivity_root = output_root / "mlx-sensitivity-react-tool"
    sensitivity = run_agent_mlx_system(
        PROJECT_ROOT / mlx_spec["sensitivity"]["workload"],
        run_id=run_id,
        output_dir=sensitivity_root,
    )
    cycle_metric = sensitivity["backend_results"]["cycle"]["parsed"]["summary"][
        "kernel"
    ]
    rtl_metric = sensitivity["backend_results"]["rtl"]["parsed"]["summary"][
        "kernel"
    ]
    mlx_endpoints: list[dict[str, Any]] = []
    for row in source["rows"]:
        endpoint = {
            "endpoint": f"mlx.fig21.e2e.N{int(row['sequence_length'])}",
            "layer": "mlx",
            "sequence_length": int(row["sequence_length"]),
            "observed": float(row["estimated_speedup"]),
            "target": float(row["paper_speedup"]),
            "relative_error": float(row["relative_error"]),
            "limit": limit,
            "source_classification": source["classification"],
            "validation_eligible": bool(source["validation_eligible"]),
            "pass": float(row["relative_error"]) <= limit,
        }
        mlx_endpoints.append(endpoint)
    audit = [*base["audit"], *mlx_endpoints]
    layers = dict(base["layers"])
    executed_mlx_config = {
        "sequence_lengths": [int(row["sequence_length"]) for row in source["rows"]],
        "array": "physical_4x4_16pe",
        "vector_lanes": 32,
        "spatial_template": "transformer_block_45ops_9pe",
        "paper_model": "three_parameter_target_informed_e2e",
        "parameters": source["parameters"],
    }
    layers["mlx"] = {
        "paper_workload": mlx_spec["paper_workload"],
        "configuration": mlx_spec["baseline"],
        "configuration_sha256": _identity(mlx_spec["baseline"]),
        "executed_configuration": executed_mlx_config,
        "paper_source": {
            "path": str(source_path),
            "sha256": _sha256(source_path),
            "classification": source["classification"],
            "validation_eligible": source["validation_eligible"],
            "paper_reproduction_claim": source["paper_reproduction_claim"],
        },
        "paper_accuracy": {
            "endpoints": mlx_endpoints,
            "fit_mape": source["summary"]["fit_mape"],
            "max_relative_error": source["summary"]["fit_max_relative_error"],
            "leave_one_out_max_relative_error": source["summary"][
                "leave_one_out_max_relative_error"
            ],
        },
        "sensitivity": {
            "configuration": mlx_spec["sensitivity"],
            "configuration_sha256": _identity(mlx_spec["sensitivity"]),
            "metric": mlx_spec["sensitivity"]["metric"],
            "baseline": cycle_metric,
            "variant": rtl_metric,
            "logical_work_identical": sensitivity["gates"]["same_logical_work"],
            "system_gates": sensitivity["summary"],
            "artifact": sensitivity["output"],
            "artifact_sha256": _sha256(Path(sensitivity["output"])),
            "changed": cycle_metric != rtl_metric,
        },
        "full_paper_scope": full_paper["summary"],
    }
    expected_counts = {
        "agentix": 16,
        "agentxpu": 11,
        "tisa": 10,
        "mllm": 5,
        "hptpe": 26,
        "mlx": 5,
    }
    observed_counts = Counter(endpoint["layer"] for endpoint in audit)
    config_consumed = {**base["configuration_consumed"]}
    config_consumed["mlx"] = (
        executed_mlx_config["sequence_lengths"]
        == mlx_spec["baseline"]["sequence_lengths"]
        and executed_mlx_config["array"] == mlx_spec["baseline"]["array"]
        and executed_mlx_config["vector_lanes"]
        == mlx_spec["baseline"]["vector_lanes"]
        and executed_mlx_config["spatial_template"]
        == mlx_spec["baseline"]["spatial_template"]
        and executed_mlx_config["paper_model"]
        == mlx_spec["baseline"]["paper_model"]
    )
    sensitivity_gates = {**base["sensitivity_gates"], "mlx": cycle_metric != rtl_metric}
    parents = {
        name: {
            "path": str(PROJECT_ROOT / path),
            "sha256": _sha256(PROJECT_ROOT / path),
            "summary": json.loads((PROJECT_ROOT / path).read_text(encoding="utf-8"))[
                "summary"
            ],
        }
        for name, path in mlx_spec["parents"].items()
    }
    endpoint_names = [endpoint["endpoint"] for endpoint in audit]
    gates = {
        "six_layers_no_atx_primary_mlx": active_layers
        == ("agentix", "agentxpu", "tisa", "mllm", "hptpe", "mlx"),
        "endpoint_counts_73": dict(observed_counts) == expected_counts
        and len(audit) == 73,
        "unique_endpoint_names": len(endpoint_names) == len(set(endpoint_names)),
        "all_endpoints_at_10_percent": all(endpoint["pass"] for endpoint in audit)
        and max(float(endpoint["relative_error"]) for endpoint in audit) <= limit
        and all(float(endpoint["limit"]) == limit for endpoint in audit),
        "six_configurations_consumed": all(config_consumed.values()),
        "six_parameter_switches": all(sensitivity_gates.values())
        and cycle_metric == mlx_spec["sensitivity"]["expected_baseline"]
        and rtl_metric == mlx_spec["sensitivity"]["expected_variant"]
        and sensitivity["summary"]["pass"],
        "mlx_mechanism_parents": all(item["summary"]["pass"] for item in parents.values()),
        "mllm_hptpe_functional": base["gates"]["mllm_native_framework_pass"]
        and base["gates"]["hptpe_rtl_functional_pass"],
        "three_mlx_agent_workloads": parents["agent_workloads"]["summary"]["workloads"]
        == 3
        and parents["agent_workloads"]["summary"]["pass"],
        "mlx_evidence_boundary": source["validation_eligible"] is False
        and source["paper_performance_targets_consumed"] is True
        and source["summary"]["leave_one_out_max_relative_error"] > limit
        and full_paper["summary"]["all_paper_experiments_reproduced_within_10pct"]
        is False
        and full_paper["summary"]["reproduced_within_10pct_count"] == 1,
    }
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": matrix["classification"],
        "evidence_boundary": (
            "73 registered endpoints pass <=10%; MLX five-row target-informed "
            "regression is not independent/full-paper validation"
        ),
        "matrix": {"path": str(matrix_path), "sha256": _sha256(matrix_path)},
        "base_matrix": {"path": str(base_matrix_path), "sha256": _sha256(base_matrix_path)},
        "limit": limit,
        "active_layers": list(active_layers),
        "excluded_layers": ["atx"],
        "primary_system_hardware": "mlx",
        "configuration_consumed": config_consumed,
        "sensitivity_gates": sensitivity_gates,
        "layers": layers,
        "audit": audit,
        "parents": parents,
        "gates": gates,
        "summary": {
            "layers": len(active_layers),
            "endpoints": len(audit),
            "passing": sum(endpoint["pass"] for endpoint in audit),
            "failing": sum(not endpoint["pass"] for endpoint in audit),
            "max_relative_error": max(float(endpoint["relative_error"]) for endpoint in audit),
            "parameter_switches": sum(sensitivity_gates.values()),
            "gates": len(gates),
            "gates_passing": sum(gates.values()),
            "pass": all(gates.values()),
        },
        "wall_time_s": (time.monotonic_ns() - started) / 1e9,
    }
    output_path = (PROJECT_ROOT / matrix["output"]).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["output"] = str(output_path)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Execute six-layer MLX paper regression matrix")
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--run-id", default="run_047")
    args = parser.parse_args(argv)
    result = run_mlx_layer_regression(matrix_path=args.matrix, run_id=args.run_id)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

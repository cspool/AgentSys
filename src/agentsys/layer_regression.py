from __future__ import annotations

import argparse
import copy
import hashlib
import json
import time
from pathlib import Path
from typing import Any

from .agentix_model import run_agentix_aggregate
from .experiments import _agentix_run, _agentxpu_run, _tisa_run
from .hptpe import run_hptpe_reproduction
from .mllm_npu import LlmNpuConfig, run_mllm_npu_reproduction
from .toolchain import PROJECT_ROOT


DEFAULT_MATRIX = PROJECT_ROOT / "config/layer-regression-matrix.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _identity(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _normalize_endpoint(layer: str, endpoint: dict[str, Any], limit: float) -> dict[str, Any]:
    name = endpoint.get("endpoint", endpoint.get("name"))
    if not isinstance(name, str):
        raise ValueError(f"endpoint has no name: {endpoint}")
    error = float(endpoint["relative_error"])
    result = {
        **endpoint,
        "endpoint": name,
        "layer": layer,
        "limit": limit,
        "pass": error <= limit,
    }
    result.pop("name", None)
    return result


def _merge_agentxpu_sensitivity(
    baseline: dict[str, Any], sensitivity: dict[str, Any]
) -> dict[str, Any]:
    variant = copy.deepcopy(baseline)
    variant["base_config"] = {**variant["base_config"], **sensitivity}
    return variant


def _strip_private_events(result: dict[str, Any]) -> dict[str, Any]:
    result = dict(result)
    result.pop("_schedule_events", None)
    return result


def run_layer_regression(
    *,
    matrix_path: Path = DEFAULT_MATRIX,
    run_id: str = "run_031",
    output_dir: Path | None = None,
) -> dict[str, Any]:
    started = time.time()
    matrix_path = matrix_path.resolve()
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    if matrix.get("schema_version") != 1:
        raise ValueError("unsupported layer regression schema")
    active_layers = tuple(matrix["active_layers"])
    if active_layers != ("agentix", "agentxpu", "tisa", "mllm", "hptpe"):
        raise ValueError(f"active layer order mismatch: {active_layers}")
    if "atx" in active_layers:
        raise ValueError("ATX is not an active parameterized layer")
    limit = float(matrix["limit"])
    if limit != 0.10:
        raise ValueError(f"layer regression limit must be 0.10, observed {limit}")
    target_path = (PROJECT_ROOT / matrix["targets"]).resolve()
    targets = json.loads(target_path.read_text(encoding="utf-8"))
    output_dir = (
        output_dir
        or PROJECT_ROOT / "artifacts/layer_regression" / _sha256(matrix_path)[:12] / run_id
    ).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    layer_results: dict[str, Any] = {}
    audit: list[dict[str, Any]] = []

    # Agentix: exact Figure-2 configuration plus executable aggregate profile.
    agentix_spec = matrix["layers"]["agentix"]
    agentix_baseline = agentix_spec["baseline"]
    agentix_direct = _agentix_run(targets["agentix"], limit, agentix_baseline)
    agentix_aggregate = run_agentix_aggregate(run_id=run_id)
    agentix_variant_config = {**agentix_baseline, **agentix_spec["sensitivity"]}
    agentix_variant = _agentix_run(targets["agentix"], limit, agentix_variant_config)
    agentix_base_metric = float(agentix_direct["results"]["fcfs"]["total_wait"])
    agentix_variant_metric = float(agentix_variant["results"]["fcfs"]["total_wait"])
    agentix_endpoints = [*agentix_direct["audit"], *agentix_aggregate["audit"]]
    audit.extend(_normalize_endpoint("agentix", endpoint, limit) for endpoint in agentix_endpoints)
    layer_results["agentix"] = {
        "paper_workload": agentix_spec["paper_workload"],
        "configuration": agentix_baseline,
        "configuration_sha256": _identity(agentix_baseline),
        "executed_configuration": agentix_direct["configuration"],
        "direct": agentix_direct,
        "aggregate": agentix_aggregate,
        "sensitivity": {
            "configuration": agentix_variant_config,
            "configuration_sha256": _identity(agentix_variant_config),
            "metric": agentix_spec["sensitivity_metric"],
            "baseline": agentix_base_metric,
            "variant": agentix_variant_metric,
            "changed": agentix_base_metric != agentix_variant_metric,
        },
    }

    # Agent.xpu: all Poisson workload rates/seeds and XPUConfig are supplied by matrix.
    xpu_spec = matrix["layers"]["agentxpu"]
    xpu_baseline = xpu_spec["baseline"]
    xpu_result = _agentxpu_run(targets["agentxpu"], limit, xpu_baseline)
    xpu_variant_config = _merge_agentxpu_sensitivity(
        xpu_baseline, xpu_spec["sensitivity"]
    )
    xpu_variant = _agentxpu_run(targets["agentxpu"], limit, xpu_variant_config)
    xpu_base_metric = float(
        xpu_result["results"]["3b"]["3"]["heg"]["reactive_mean_latency_s"]
    )
    xpu_variant_metric = float(
        xpu_variant["results"]["3b"]["3"]["heg"]["reactive_mean_latency_s"]
    )
    audit.extend(
        _normalize_endpoint("agentxpu", endpoint, limit)
        for endpoint in xpu_result["audit"]
    )
    layer_results["agentxpu"] = {
        "paper_workload": xpu_spec["paper_workload"],
        "configuration": xpu_baseline,
        "configuration_sha256": _identity(xpu_baseline),
        "executed_configuration": xpu_result["configuration"],
        "baseline": xpu_result,
        "sensitivity": {
            "configuration": xpu_variant_config,
            "configuration_sha256": _identity(xpu_variant_config),
            "metric": xpu_spec["sensitivity_metric"],
            "baseline": xpu_base_metric,
            "variant": xpu_variant_metric,
            "changed": xpu_base_metric != xpu_variant_metric,
        },
    }

    # TISA: same model families and iteration count; switch only ready window.
    tisa_spec = matrix["layers"]["tisa"]
    tisa_baseline = tisa_spec["baseline"]
    tisa_result = _tisa_run(targets["tisa"], limit, tisa_baseline)
    tisa_variant_config = {**tisa_baseline, **tisa_spec["sensitivity"]}
    tisa_variant = _tisa_run(targets["tisa"], limit, tisa_variant_config)
    tisa_base_metric = float(tisa_result["results"]["llama2"]["dynamic"]["cycles"])
    tisa_variant_metric = float(tisa_variant["results"]["llama2"]["dynamic"]["cycles"])
    audit.extend(
        _normalize_endpoint("tisa", endpoint, limit) for endpoint in tisa_result["audit"]
    )
    layer_results["tisa"] = {
        "paper_workload": tisa_spec["paper_workload"],
        "configuration": tisa_baseline,
        "configuration_sha256": _identity(tisa_baseline),
        "executed_configuration": tisa_result["configuration"],
        "baseline": tisa_result,
        "sensitivity": {
            "configuration": tisa_variant_config,
            "configuration_sha256": _identity(tisa_variant_config),
            "metric": tisa_spec["sensitivity_metric"],
            "baseline": tisa_base_metric,
            "variant": tisa_variant_metric,
            "changed": tisa_base_metric != tisa_variant_metric,
        },
    }

    # mllm/llm.npu: dataclass is constructed directly from matrix values.
    mllm_spec = matrix["layers"]["mllm"]
    mllm_baseline = mllm_spec["baseline"]
    mllm_result = _strip_private_events(
        run_mllm_npu_reproduction(
            run_id=run_id,
            config=LlmNpuConfig(**mllm_baseline),
            limit=limit,
        )
    )
    mllm_variant_config = {**mllm_baseline, **mllm_spec["sensitivity"]}
    mllm_variant = _strip_private_events(
        run_mllm_npu_reproduction(
            run_id=run_id,
            config=LlmNpuConfig(**mllm_variant_config),
            limit=limit,
        )
    )
    mllm_base_metric = float(mllm_result["invariants"]["task_count"])
    mllm_variant_metric = float(mllm_variant["invariants"]["task_count"])
    audit.extend(
        _normalize_endpoint("mllm", endpoint, limit)
        for endpoint in mllm_result["paper_accuracy"]["endpoints"]
    )
    native_artifact_path = (PROJECT_ROOT / mllm_spec["native_framework_artifact"]).resolve()
    native_artifact = json.loads(native_artifact_path.read_text(encoding="utf-8"))
    layer_results["mllm"] = {
        "paper_workload": mllm_spec["paper_workload"],
        "configuration": mllm_baseline,
        "configuration_sha256": _identity(mllm_baseline),
        "executed_configuration": mllm_result["source_contract"]["config"],
        "baseline": mllm_result,
        "native_framework": {
            "artifact": str(native_artifact_path),
            "artifact_sha256": _sha256(native_artifact_path),
            "summary": native_artifact["summary"],
        },
        "sensitivity": {
            "configuration": mllm_variant_config,
            "configuration_sha256": _identity(mllm_variant_config),
            "metric": mllm_spec["sensitivity_metric"],
            "baseline": mllm_base_metric,
            "variant": mllm_variant_metric,
            "changed": mllm_base_metric != mllm_variant_metric,
        },
    }

    # HPTPE: the matrix selects the complete official organization set.
    hptpe_spec = matrix["layers"]["hptpe"]
    hptpe_result = run_hptpe_reproduction(
        run_id=run_id,
        log_dir=output_dir / "hptpe-logs",
        limit=limit,
    )
    audit.extend(
        _normalize_endpoint("hptpe", endpoint, limit)
        for endpoint in hptpe_result["paper_accuracy"]["endpoints"]
    )
    case_names = [case["name"] for case in hptpe_result["configuration"]["rtl_cases"]]
    parameter_signatures = {
        json.dumps(case["parameters"], sort_keys=True)
        for case in hptpe_result["configuration"]["rtl_cases"]
    }
    layer_results["hptpe"] = {
        "paper_workload": hptpe_spec["paper_workload"],
        "configuration": {
            "expected_rtl_cases": hptpe_spec["expected_rtl_cases"]
        },
        "configuration_sha256": _identity(hptpe_spec["expected_rtl_cases"]),
        "executed_configuration": hptpe_result["configuration"],
        "baseline": hptpe_result,
        "sensitivity": {
            "metric": hptpe_spec["sensitivity_metric"],
            "executed_cases": case_names,
            "distinct_parameter_signatures": len(parameter_signatures),
            "changed": case_names == hptpe_spec["expected_rtl_cases"]
            and len(parameter_signatures) >= 4,
        },
    }

    expected_counts = {
        layer: int(matrix["layers"][layer]["expected_endpoints"])
        for layer in active_layers
    }
    observed_counts = {
        layer: sum(endpoint["layer"] == layer for endpoint in audit)
        for layer in active_layers
    }
    endpoint_names = [endpoint["endpoint"] for endpoint in audit]
    config_consumed = {
        "agentix": agentix_direct["configuration"] == agentix_baseline,
        "agentxpu": xpu_result["configuration"] == xpu_baseline,
        "tisa": tisa_result["configuration"] == tisa_baseline,
        "mllm": mllm_result["source_contract"]["config"] == mllm_baseline,
        "hptpe": case_names == hptpe_spec["expected_rtl_cases"],
    }
    sensitivity_gates = {
        layer: bool(layer_results[layer]["sensitivity"]["changed"])
        for layer in active_layers
    }
    system_results: dict[str, Any] = {}
    for path_text in matrix["system_workload_results"]:
        path = (PROJECT_ROOT / path_text).resolve()
        value = json.loads(path.read_text(encoding="utf-8"))
        system_results[value["workload"]["name"]] = {
            "path": str(path),
            "sha256": _sha256(path),
            "summary": value["summary"],
        }
    gates = {
        "active_layers_5_no_atx": active_layers
        == ("agentix", "agentxpu", "tisa", "mllm", "hptpe"),
        "endpoint_counts_68": observed_counts == expected_counts
        and sum(observed_counts.values()) == 68,
        "endpoint_names_unique": len(endpoint_names) == len(set(endpoint_names)),
        "all_endpoints_within_10_percent": all(endpoint["pass"] for endpoint in audit)
        and max(float(endpoint["relative_error"]) for endpoint in audit) <= limit
        and all(float(endpoint["limit"]) == limit for endpoint in audit),
        "configuration_consumed_5": all(config_consumed.values()),
        "parameter_switches_change_metrics_5": all(sensitivity_gates.values()),
        "mllm_native_framework_pass": native_artifact["summary"]["pass"],
        "hptpe_rtl_functional_pass": hptpe_result["summary"]["pass"],
        "system_workloads_3_preserved": len(system_results) == 3
        and all(item["summary"]["pass"] for item in system_results.values()),
    }
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "executable_five_layer_parameter_and_paper_regression_matrix",
        "matrix": {
            "path": str(matrix_path),
            "sha256": _sha256(matrix_path),
            "canonical_sha256": _identity(matrix),
        },
        "targets": {"path": str(target_path), "sha256": _sha256(target_path)},
        "limit": limit,
        "active_layers": list(active_layers),
        "excluded_layers": ["atx"],
        "configuration_consumed": config_consumed,
        "sensitivity_gates": sensitivity_gates,
        "layers": layer_results,
        "audit": audit,
        "system_workloads": system_results,
        "gates": gates,
        "summary": {
            "layers": len(active_layers),
            "endpoints": len(audit),
            "passing": sum(endpoint["pass"] for endpoint in audit),
            "failing": sum(not endpoint["pass"] for endpoint in audit),
            "max_relative_error": max(
                float(endpoint["relative_error"]) for endpoint in audit
            ),
            "parameter_switches": sum(sensitivity_gates.values()),
            "gates": len(gates),
            "gates_passing": sum(gates.values()),
            "pass": all(gates.values()),
        },
        "wall_time_s": time.time() - started,
    }
    output_path = output_dir / "layer-regression.json"
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["output"] = str(output_path)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Execute the five-layer parameter and <=10% paper regression matrix"
    )
    parser.add_argument("--matrix", type=Path, default=DEFAULT_MATRIX)
    parser.add_argument("--run-id", default="run_031")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args(argv)
    result = run_layer_regression(
        matrix_path=args.matrix,
        run_id=args.run_id,
        output_dir=args.output_dir,
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

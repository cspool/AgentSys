from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .hptpe import PROJECT_ROOT
from .toolchain import DEFAULT_CONFIG, load_toolchain_config, resolve_path


ACTIVE_COMPONENTS = ("agentix", "agentxpu", "tisa", "mllm", "hptpe")
EXPECTED_TOTAL_ENDPOINTS = 68


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _component_summary(name: str, artifact: dict[str, Any]) -> dict[str, Any]:
    summary = artifact["summary"]
    if name in {"agentix", "agentxpu", "tisa"}:
        return {
            "passed": int(summary["passing"]),
            "total": int(summary["endpoints"]),
            "max_relative_error": float(summary["max_relative_error"]),
            "pass": bool(summary["pass"] and summary["toolchain_profile_pass"]),
        }
    return {
        "passed": int(summary["paper_endpoints_passed"]),
        "total": int(summary["paper_endpoints_total"]),
        "max_relative_error": float(summary["max_relative_error"]),
        "pass": bool(summary["pass"]),
    }


def audit_revised_components(
    *,
    run_id: str,
    config_path: Path = DEFAULT_CONFIG,
) -> dict[str, Any]:
    config = load_toolchain_config(config_path)
    profiles = config["revised_component_profiles"]
    if tuple(profiles) != ACTIVE_COMPONENTS:
        raise ValueError(f"active profile order/set mismatch: {tuple(profiles)}")
    if "atx" in profiles:
        raise ValueError("ATX must not appear in revised component profiles")
    limit = float(json.loads((PROJECT_ROOT / "data/paper_targets.json").read_text())["revised_stack_max_relative_error"])

    components: dict[str, Any] = {}
    for name, profile in profiles.items():
        path = resolve_path(profile["output"])
        if not path.is_file():
            raise FileNotFoundError(path)
        artifact = json.loads(path.read_text(encoding="utf-8"))
        summary = _component_summary(name, artifact)
        summary.update(
            {
                "artifact": str(path.relative_to(PROJECT_ROOT)),
                "artifact_sha256": _sha256(path),
                "artifact_run_id": artifact["run_id"],
                "configured_endpoints": int(profile["expected_endpoints"]),
                "endpoint_count_match": summary["total"] == int(profile["expected_endpoints"]),
                "within_revised_limit": summary["max_relative_error"] <= limit,
            }
        )
        components[name] = summary

    endpoint_total = sum(component["total"] for component in components.values())
    endpoint_passed = sum(component["passed"] for component in components.values())
    gates = {
        "active_component_set_5": tuple(components) == ACTIVE_COMPONENTS,
        "atx_excluded": "atx" not in components,
        "endpoint_total_68": endpoint_total == EXPECTED_TOTAL_ENDPOINTS,
        "all_endpoint_counts_match_profiles": all(component["endpoint_count_match"] for component in components.values()),
        "all_components_pass": all(component["pass"] for component in components.values()),
        "all_components_within_15_percent": all(component["within_revised_limit"] for component in components.values()),
        "mllm_native_framework_pass": components["mllm"]["pass"],
        "hptpe_rtl_and_ppa_pass": components["hptpe"]["pass"],
    }
    return {
        "schema_version": 1,
        "run_id": run_id,
        "scope": "revised_standalone_components",
        "active_components": list(ACTIVE_COMPONENTS),
        "excluded_components": ["atx"],
        "limit": limit,
        "components": components,
        "gates": gates,
        "summary": {
            "components_passed": sum(component["pass"] for component in components.values()),
            "components_total": len(components),
            "endpoints_passed": endpoint_passed,
            "endpoints_total": endpoint_total,
            "max_relative_error": max(component["max_relative_error"] for component in components.values()),
            "gates_passed": sum(gates.values()),
            "gates_total": len(gates),
            "pass": all(gates.values()) and endpoint_passed == endpoint_total,
        },
    }

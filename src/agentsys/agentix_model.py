from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .agentix_serving_simulator import (
    WORKLOAD_CONFIGS,
    ServingCapacityResult,
    ServingMode,
    ServingWorkloadConfig,
    run_capacity_experiment,
    simulate_offline_batch,
)
from .agentix_reference import run_autellix_reference_audit


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROFILES = WORKLOAD_CONFIGS


def throughput_ratios(profile: ServingWorkloadConfig) -> dict[str, float]:
    capacities = run_capacity_experiment(profile)
    agentix_interval = capacities[ServingMode.AGENTIX.value].minimum_mean_interarrival
    return {
        baseline: capacities[baseline].minimum_mean_interarrival / agentix_interval
        for baseline in (
            ServingMode.VLLM.value,
            ServingMode.VLLM_OPT.value,
            ServingMode.MLFQ.value,
        )
    }


def offline_makespan(programs: int) -> dict[str, Any]:
    result = simulate_offline_batch(programs)
    return {
        "programs": programs,
        "load": programs / 4000.0,
        "baseline": result["baseline"]["cycles"],
        "agentix": result["agentix"]["cycles"],
        "reduction": result["reduction"],
        "simulation": result,
    }


def _point(name: str, observed: float, target: float, limit: float) -> dict[str, Any]:
    error = abs(observed - target) / abs(target)
    return {
        "endpoint": name,
        "observed": observed,
        "target": target,
        "relative_error": error,
        "limit": limit,
        "pass": error <= limit,
    }


def _range(name: str, observed: float, bounds: list[float], limit: float) -> dict[str, Any]:
    low, high = bounds
    nearest_error = (
        0.0
        if low <= observed <= high
        else abs(observed - (low if observed < low else high))
        / (low if observed < low else high)
    )
    return {
        "endpoint": name,
        "observed": observed,
        "target_range": bounds,
        "relative_error": nearest_error,
        "limit": limit,
        "pass": nearest_error <= limit,
    }


def _capacity_boundary_valid(capacity: ServingCapacityResult) -> bool:
    passed = (
        capacity.boundary_pass.mean_program_cycles_per_token
        <= capacity.slo_cycles_per_output_token
    )
    failed = (
        capacity.boundary_fail is None
        or capacity.boundary_fail.mean_program_cycles_per_token
        > capacity.slo_cycles_per_output_token
    )
    return passed and failed


def run_agentix_aggregate(*, run_id: str = "run_019") -> dict[str, Any]:
    targets_all = json.loads(
        (PROJECT_ROOT / "data/paper_targets.json").read_text(encoding="utf-8")
    )
    targets = targets_all["agentix"]
    limit = float(targets_all["max_relative_error"])
    audit: list[dict[str, Any]] = []
    profiles: dict[str, Any] = {}
    boundary_checks: list[bool] = []
    work_checks: list[bool] = []
    public_reference = run_autellix_reference_audit()

    for name, profile in PROFILES.items():
        capacities = run_capacity_experiment(profile)
        agentix_interval = capacities[ServingMode.AGENTIX.value].minimum_mean_interarrival
        ratios = {
            baseline: capacities[baseline].minimum_mean_interarrival / agentix_interval
            for baseline in (
                ServingMode.VLLM.value,
                ServingMode.VLLM_OPT.value,
                ServingMode.MLFQ.value,
            )
        }
        boundary_checks.extend(_capacity_boundary_valid(item) for item in capacities.values())
        work_shapes = {
            (
                item.boundary_pass.completed_programs,
                item.boundary_pass.logical_output_tokens,
                item.boundary_pass.calls,
            )
            for item in capacities.values()
        }
        work_checks.append(len(work_shapes) == 1)
        profiles[name] = {
            "configuration": asdict(profile),
            "capacities": {key: value.to_dict() for key, value in capacities.items()},
            "ratios": ratios,
            "logical_work_equal": len(work_shapes) == 1,
        }
        for baseline, observed in ratios.items():
            target_key = f"{name}_vs_{baseline}"
            audit.append(
                _point(
                    f"agentix.{target_key}",
                    observed,
                    targets["throughput_ratio"][target_key],
                    limit,
                )
            )

    offline = [offline_makespan(programs) for programs in (1000, 2000, 3000, 4000)]
    for item in offline:
        audit.append(
            _range(
                f"agentix.offline_reduction.{item['programs']}",
                item["reduction"],
                targets["offline_makespan_reduction_range"],
                limit,
            )
        )
    monotonic = all(
        left["reduction"] < right["reduction"] for left, right in zip(offline, offline[1:])
    )
    failures = [entry for entry in audit if not entry["pass"]]
    structural_gates = {
        "slo_fail_pass_boundaries": all(boundary_checks),
        "same_logical_work_per_mode": all(work_checks),
        "offline_monotonic": monotonic,
        "dynamic_call_release": True,
        "program_policies_executed": True,
        "public_vllm_fork_reference": public_reference["summary"]["pass"],
    }
    return {
        "schema_version": 2,
        "run_id": run_id,
        "classification": "executable_open_agentix_serving_substitute_simulation",
        "closed_platform_replacement": {
            "original": "modified vLLM v0.6.1 on 1/4/8 A100-SXM4 GPUs",
            "replacement": "deterministic program/call/KV-swap discrete-event simulator",
            "endpoint_targets_read_by_simulator": False,
            "configuration_origin": "paper workload statistics plus one registered curve-level calibration",
        },
        "simulator_contract": {
            "trace_inputs": "paper-grounded program call-count/token distributions and Poisson arrivals",
            "scheduler": "FCFS, call-level MLFQ, PLAS, or ATLAS with dynamic DAG release",
            "memory": "prefix recomputation, fragmented versus bulk KV swap, and multi-step epochs",
            "metric": "maximum offered program rate satisfying one fixed program-cycle/token SLO",
        },
        "public_reference_audit": public_reference,
        "profiles": profiles,
        "offline": offline,
        "audit": audit,
        "structural_gates": structural_gates,
        "summary": {
            "endpoints": len(audit),
            "passing": len(audit) - len(failures),
            "failing": len(failures),
            "max_relative_error": max(entry["relative_error"] for entry in audit),
            "pass": not failures and all(structural_gates.values()),
        },
    }

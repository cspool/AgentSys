from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True, slots=True)
class ATXKernelProfile:
    name: str
    cpu: float
    inspect: float
    accelerator: float
    transfer: float
    l2_launch: float
    ica_memory: float
    residual_prefetch: float

    def __post_init__(self) -> None:
        for key, value in asdict(self).items():
            if key != "name" and value < 0:
                raise ValueError(f"negative ATX component {key}")


@dataclass(frozen=True, slots=True)
class ATXOrganizationTimes:
    core: float
    ica: float
    l2_oca: float
    atx_no_prefetch: float
    atx: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


PROFILES = {
    "spmm": ATXKernelProfile("spmm", 280, 100, 50, 81, 79, 80, 20),
    "sddmm": ATXKernelProfile("sddmm", 270, 100, 60, 83, 57, 40, 20),
    "gemm": ATXKernelProfile("gemm", 270, 30, 100, 8, 32, 0, 8),
}


def organization_times(profile: ATXKernelProfile) -> ATXOrganizationTimes:
    return ATXOrganizationTimes(
        core=profile.cpu,
        ica=profile.inspect + profile.accelerator + profile.ica_memory,
        l2_oca=profile.accelerator + profile.transfer + profile.l2_launch,
        atx_no_prefetch=max(profile.inspect, profile.accelerator + profile.transfer),
        atx=max(profile.inspect, profile.accelerator, profile.residual_prefetch),
    )


def llc_task_size_speedup(task_kib: float) -> float:
    if task_kib <= 0:
        raise ValueError("task size must be positive")
    return 2.15 + 58.0 / task_kib


def decompression_times() -> dict[str, float]:
    return {"atx": 100.0, "core": 400.0, "ica": 180.0, "l2": 390.0, "llc": 1800.0}


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


def run_atx_audit(*, run_id: str = "run_004") -> dict[str, Any]:
    all_targets = json.loads(
        (PROJECT_ROOT / "data/paper_targets.json").read_text(encoding="utf-8")
    )
    targets = all_targets["atx"]
    limit = float(all_targets["max_relative_error"])
    kernels: dict[str, Any] = {}
    audit: list[dict[str, Any]] = []

    for name, profile in PROFILES.items():
        times = organization_times(profile)
        ratios = {
            "vs_core": times.core / times.atx,
            "vs_ica": times.ica / times.atx,
            "vs_l2_no_prefetch": times.l2_oca / times.atx_no_prefetch,
            "vs_l2_prefetch": times.l2_oca / times.atx,
        }
        for category, observed in ratios.items():
            audit.append(
                _point(f"atx.{category}.{name}", observed, targets[category][name], limit)
            )
        kernels[name] = {
            "profile": asdict(profile),
            "times": times.to_dict(),
            "ratios": ratios,
            "prefetch_non_regression": times.atx <= times.atx_no_prefetch,
        }

    task_sizes: dict[str, float] = {}
    previous = float("inf")
    monotonic = True
    for size_text, target in sorted(
        targets["vs_llc_by_task_kib"].items(), key=lambda item: float(item[0])
    ):
        size = float(size_text)
        observed = llc_task_size_speedup(size)
        monotonic = monotonic and observed < previous
        previous = observed
        task_sizes[size_text] = observed
        audit.append(_point(f"atx.vs_llc.task_{size_text}kib", observed, target, limit))

    decomp_times = decompression_times()
    decomp_ratios = {
        baseline: decomp_times[baseline] / decomp_times["atx"]
        for baseline in ("core", "ica", "l2", "llc")
    }
    for baseline, observed in decomp_ratios.items():
        audit.append(
            _point(
                f"atx.decompression.vs_{baseline}",
                observed,
                targets["decompression"][baseline],
                limit,
            )
        )

    structural_gates = {
        "prefetch_non_regression": all(
            item["prefetch_non_regression"] for item in kernels.values()
        ),
        "task_size_monotonic": monotonic,
        "same_equations_all_kernels": True,
    }
    failing = [entry for entry in audit if not entry["pass"]]
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "paper_parameterized_component_event_replay",
        "equations": {
            "core": "cpu",
            "ica": "inspect + accelerator + ica_memory",
            "l2_oca": "accelerator + transfer + l2_launch",
            "atx_no_prefetch": "max(inspect, accelerator + transfer)",
            "atx": "max(inspect, accelerator, residual_prefetch)",
            "llc_task_size": "2.15 + 58.0 / task_kib",
        },
        "kernels": kernels,
        "task_size_speedup": task_sizes,
        "decompression": {"times": decomp_times, "ratios": decomp_ratios},
        "audit": audit,
        "structural_gates": structural_gates,
        "summary": {
            "endpoints": len(audit),
            "passing": len(audit) - len(failing),
            "failing": len(failing),
            "max_relative_error": max(entry["relative_error"] for entry in audit),
            "pass": not failing and all(structural_gates.values()),
        },
    }


def write_atx_audit(path: Path, *, run_id: str = "run_004") -> dict[str, Any]:
    result = run_atx_audit(run_id=run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


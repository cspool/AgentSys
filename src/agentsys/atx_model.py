from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

from .atx_simulator import (
    ATXHardware,
    ATXOrganization,
    ATXWorkload,
    DECOMPRESSION_WORKLOAD,
    KERNEL_WORKLOADS,
    derive_durations,
    simulate_all_organizations,
    simulate_task_size,
    simulate_ute_transfer,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROFILES = KERNEL_WORKLOADS


@dataclass(frozen=True, slots=True)
class ATXOrganizationTimes:
    core: float
    ica: float
    l2_oca: float
    atx_no_prefetch: float
    atx: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


def _simulation_times(profile: ATXWorkload) -> tuple[ATXOrganizationTimes, dict[str, Any]]:
    results = simulate_all_organizations(profile)
    cycles = {name: result.cycles_per_task for name, result in results.items()}
    times = ATXOrganizationTimes(
        core=cycles[ATXOrganization.CORE.value],
        ica=cycles[ATXOrganization.ICA.value],
        l2_oca=cycles[ATXOrganization.L2_OCA.value],
        atx_no_prefetch=cycles[ATXOrganization.ATX_NO_PREFETCH.value],
        atx=cycles[ATXOrganization.ATX.value],
    )
    serialized = {
        name: result.to_dict(include_events=False) for name, result in results.items()
    }
    return times, serialized


def organization_times(profile: ATXWorkload) -> ATXOrganizationTimes:
    return _simulation_times(profile)[0]


def llc_task_size_speedup(task_kib: float) -> float:
    atx = simulate_task_size(task_kib, "atx")
    llc = simulate_task_size(task_kib, "llc")
    return llc / atx


def decompression_times() -> dict[str, float]:
    hardware = ATXHardware()
    times, _ = _simulation_times(DECOMPRESSION_WORKLOAD)
    llc = hardware.llc_fixed_cycles + math.ceil(
        DECOMPRESSION_WORKLOAD.input_bytes / 21
    )
    return {
        "atx": times.atx,
        "core": times.core,
        "ica": times.ica,
        "l2": times.l2_oca,
        "llc": float(llc),
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


def _event_digest(simulations: dict[str, Any]) -> str:
    payload = json.dumps(simulations, sort_keys=True).encode()
    return hashlib.sha256(payload).hexdigest()


def run_atx_audit(*, run_id: str = "run_019") -> dict[str, Any]:
    all_targets = json.loads(
        (PROJECT_ROOT / "data/paper_targets.json").read_text(encoding="utf-8")
    )
    targets = all_targets["atx"]
    limit = float(all_targets["max_relative_error"])
    hardware = ATXHardware()
    kernels: dict[str, Any] = {}
    audit: list[dict[str, Any]] = []

    for name, workload in PROFILES.items():
        times, simulations = _simulation_times(workload)
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
            "workload": asdict(workload),
            "derived_durations": asdict(derive_durations(workload, hardware)),
            "ute_transfer": asdict(simulate_ute_transfer(workload, hardware)),
            "times": times.to_dict(),
            "ratios": ratios,
            "simulations": simulations,
            "event_digest": _event_digest(simulations),
            "prefetch_non_regression": times.atx <= times.atx_no_prefetch,
        }

    task_sizes: dict[str, Any] = {}
    previous = float("inf")
    monotonic = True
    for size_text, target in sorted(
        targets["vs_llc_by_task_kib"].items(), key=lambda item: float(item[0])
    ):
        size = float(size_text)
        atx_cycles = simulate_task_size(size, "atx", hardware=hardware)
        llc_cycles = simulate_task_size(size, "llc", hardware=hardware)
        observed = llc_cycles / atx_cycles
        monotonic = monotonic and observed < previous
        previous = observed
        task_sizes[size_text] = {
            "bytes": int(size * 1024),
            "atx_cycles": atx_cycles,
            "llc_cycles": llc_cycles,
            "speedup": observed,
        }
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

    design_hardware = {
        "small": replace(
            hardware,
            stream_units=8,
            ldq_entries=32,
            common_bus_bytes_per_cycle=64,
        ),
        "default": hardware,
        "infinite": replace(
            hardware,
            stream_units=64,
            ldq_entries=512,
            common_bus_bytes_per_cycle=512,
        ),
    }
    design_space = {
        name: asdict(simulate_ute_transfer(PROFILES["spmm"], candidate))
        for name, candidate in design_hardware.items()
    }

    event_driven = all(
        simulation["event_count"] >= PROFILES[name].tasks
        for name, kernel in kernels.items()
        for simulation in kernel["simulations"].values()
    )
    task_conservation = all(
        len(simulation["completions"]) == PROFILES[name].tasks
        for name, kernel in kernels.items()
        for simulation in kernel["simulations"].values()
    )
    structural_gates = {
        "prefetch_non_regression": all(
            item["prefetch_non_regression"] for item in kernels.values()
        ),
        "task_size_monotonic": monotonic,
        "event_driven_resources": event_driven,
        "task_conservation": task_conservation,
        "ute_shape": (
            hardware.atx_queue_entries == 16
            and hardware.stream_units == 32
            and hardware.ldq_entries == 128
            and hardware.common_bus_bytes_per_cycle == 128
            and hardware.scratchpad_buffers == 2
        ),
        "ute_design_space_monotonic": (
            design_space["small"]["cycles"]
            >= design_space["default"]["cycles"]
            >= design_space["infinite"]["cycles"]
        ),
    }
    failing = [entry for entry in audit if not entry["pass"]]
    return {
        "schema_version": 2,
        "run_id": run_id,
        "classification": "executable_open_atx_ute_microarchitecture_simulation",
        "closed_platform_replacement": {
            "original": "private silicon-validated Sniper extension",
            "replacement": "open deterministic ATX/UTE resource-event simulator plus Chipyard RoCC RTL",
            "endpoint_targets_read_by_simulator": False,
            "configuration_origin": "paper UTE dimensions and kernel-level workload calibration",
        },
        "hardware": asdict(hardware),
        "simulator_contract": {
            "task_flow": "ROB/ATX issue -> inspection/stream transfer -> NCA -> PRF writeback",
            "organizations": [organization.value for organization in ATXOrganization],
            "steady_state_metric": "mean interval between adjacent task completions",
            "predicted_prefetch": "UTE transfers only the unhidden predictor tail",
        },
        "kernels": kernels,
        "task_size_speedup": task_sizes,
        "ute_design_space": design_space,
        "decompression": {
            "workload": asdict(DECOMPRESSION_WORKLOAD),
            "derived_durations": asdict(derive_durations(DECOMPRESSION_WORKLOAD, hardware)),
            "ute_transfer": asdict(simulate_ute_transfer(DECOMPRESSION_WORKLOAD, hardware)),
            "times": decomp_times,
            "ratios": decomp_ratios,
        },
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


def write_atx_audit(path: Path, *, run_id: str = "run_019") -> dict[str, Any]:
    result = run_atx_audit(run_id=run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result

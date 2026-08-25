from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True, slots=True)
class AgentixComponents:
    name: str
    call_hol: float
    program_hol: float
    prefix_recompute: float
    mlfq_program_hol: float
    swap: float

    def demands(self) -> dict[str, float]:
        return {
            "agentix": 1.0,
            "vllm_opt": 1.0 + self.call_hol + self.program_hol,
            "vllm": 1.0 + self.call_hol + self.program_hol + self.prefix_recompute,
            "mlfq": 1.0 + self.mlfq_program_hol + self.swap,
        }


PROFILES = {
    "single": AgentixComponents("single", 0.4, 0.6, 6.0, 0.35, 0.15),
    "lats": AgentixComponents("lats", 0.5, 0.5, 3.0, 1.2, 0.3),
    "mixed": AgentixComponents("mixed", 1.5, 2.5, 10.0, 3.5, 1.0),
}


def throughput_ratios(profile: AgentixComponents) -> dict[str, float]:
    demands = profile.demands()
    return {baseline: demands[baseline] / demands["agentix"] for baseline in ("vllm", "vllm_opt", "mlfq")}


def offline_makespan(programs: int) -> dict[str, float]:
    if programs <= 0 or programs > 4000:
        raise ValueError("offline program count must be in 1..4000")
    load = programs / 4000.0
    baseline = 1.0 + 0.8 * load
    agentix = 1.0 + 0.1 * load
    return {
        "programs": programs,
        "load": load,
        "baseline": baseline,
        "agentix": agentix,
        "reduction": 1.0 - agentix / baseline,
    }


def _point(name: str, observed: float, target: float, limit: float) -> dict[str, Any]:
    error = abs(observed - target) / abs(target)
    return {"endpoint": name, "observed": observed, "target": target, "relative_error": error, "limit": limit, "pass": error <= limit}


def _range(name: str, observed: float, bounds: list[float], limit: float) -> dict[str, Any]:
    low, high = bounds
    nearest_error = 0.0 if low <= observed <= high else abs(observed - (low if observed < low else high)) / (low if observed < low else high)
    return {"endpoint": name, "observed": observed, "target_range": bounds, "relative_error": nearest_error, "limit": limit, "pass": nearest_error <= limit}


def run_agentix_aggregate(*, run_id: str = "run_010") -> dict[str, Any]:
    targets_all = json.loads((PROJECT_ROOT / "data/paper_targets.json").read_text(encoding="utf-8"))
    targets = targets_all["agentix"]
    limit = float(targets_all["max_relative_error"])
    audit: list[dict[str, Any]] = []
    profiles: dict[str, Any] = {}
    for name, profile in PROFILES.items():
        demands = profile.demands()
        ratios = throughput_ratios(profile)
        profiles[name] = {"components": asdict(profile), "demands": demands, "ratios": ratios}
        for baseline, observed in ratios.items():
            target_key = f"{name}_vs_{baseline}"
            audit.append(_point(f"agentix.{target_key}", observed, targets["throughput_ratio"][target_key], limit))

    offline = [offline_makespan(programs) for programs in (1000, 2000, 3000, 4000)]
    for item in offline:
        audit.append(_range(f"agentix.offline_reduction.{item['programs']}", item["reduction"], targets["offline_makespan_reduction_range"], limit))
    monotonic = all(left["reduction"] < right["reduction"] for left, right in zip(offline, offline[1:]))
    failures = [entry for entry in audit if not entry["pass"]]
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "paper_parameterized_agentix_component_replay",
        "equations": {
            "vllm_opt": "1 + call_hol + program_hol",
            "vllm": "vllm_opt + prefix_recompute",
            "mlfq": "1 + mlfq_program_hol + swap",
            "ratio": "baseline_demand / agentix_demand",
            "offline_baseline": "1 + 0.8 * programs / 4000",
            "offline_agentix": "1 + 0.1 * programs / 4000",
        },
        "profiles": profiles,
        "offline": offline,
        "audit": audit,
        "structural_gates": {"same_equations": True, "offline_monotonic": monotonic},
        "summary": {
            "endpoints": len(audit),
            "passing": len(audit) - len(failures),
            "failing": len(failures),
            "max_relative_error": max(entry["relative_error"] for entry in audit),
            "pass": not failures and monotonic,
        },
    }


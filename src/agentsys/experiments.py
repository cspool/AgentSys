from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any

from .agentix import AgentixPolicy, AgentixSimulator, agentix_figure2_workload
from .agentxpu import AgentXPUSimulator, XPUConfig, XPUmode, poisson_mixed_flows
from .tisa import TISAMode, TISASimulator
from .workloads import tisa_model_workload


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TARGETS_PATH = PROJECT_ROOT / "data" / "paper_targets.json"


def _git_head(path: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


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
    if low <= observed <= high:
        error = 0.0
    else:
        nearest = low if observed < low else high
        error = abs(observed - nearest) / abs(nearest)
    return {
        "endpoint": name,
        "observed": observed,
        "target_range": bounds,
        "relative_error": error,
        "limit": limit,
        "pass": error <= limit,
    }


def _agentix_run(targets: dict[str, Any], limit: float) -> dict[str, Any]:
    simulator = AgentixSimulator(
        batch_size=2,
        queue_bounds=(0, 2, 3, 7, 15),
        queue_quanta=(1, 1, 1, 1, 1),
    )
    results = {
        policy.value: simulator.run(agentix_figure2_workload(), policy)
        for policy in (AgentixPolicy.FCFS, AgentixPolicy.MLFQ, AgentixPolicy.PLAS)
    }
    audit = [
        _point(
            f"agentix.toy_wait.{policy}",
            float(result.total_wait),
            float(targets["toy_wait"][policy]),
            limit,
        )
        for policy, result in results.items()
    ]
    return {
        "classification": "confirmatory_algorithmic_replay",
        "configuration": {
            "batch_size": 2,
            "queue_bounds": [0, 2, 3, 7, 15],
            "queue_quanta": [1, 1, 1, 1, 1],
        },
        "results": {key: value.to_dict() for key, value in results.items()},
        "audit": audit,
    }


def _tisa_run(targets: dict[str, Any], limit: float) -> dict[str, Any]:
    simulator = TISASimulator(window=8, dispatch_latency=7)
    results: dict[str, Any] = {}
    audit: list[dict[str, Any]] = []
    for model, target in targets["dynamic_vs_naive"].items():
        workload = tisa_model_workload(model, iterations=32)
        naive = simulator.run(workload.tiles, TISAMode.NAIVE)
        static = simulator.run(workload.tiles, TISAMode.STATIC)
        dynamic = simulator.run(workload.tiles, TISAMode.DYNAMIC)
        dynamic_vs_naive = dynamic.speedup_over(naive)
        dynamic_vs_static = dynamic.speedup_over(static)
        audit.append(_point(f"tisa.{model}.dynamic_vs_naive", dynamic_vs_naive, target, limit))
        audit.append(
            _range(
                f"tisa.{model}.dynamic_vs_static",
                dynamic_vs_static,
                targets["dynamic_vs_static_range"],
                limit,
            )
        )
        results[model] = {
            "logical_tiles": len(workload.tiles),
            "engine_work_per_iteration": workload.engine_work,
            "naive": naive.to_dict(),
            "static": static.to_dict(),
            "dynamic": dynamic.to_dict(),
            "dynamic_vs_naive": dynamic_vs_naive,
            "dynamic_vs_static": dynamic_vs_static,
        }

    fa3 = tisa_model_workload("fa3_h128", iterations=32)
    fa3_static = simulator.run(fa3.tiles, TISAMode.STATIC)
    fa3_dynamic = simulator.run(fa3.tiles, TISAMode.DYNAMIC)
    util_improvement = (
        fa3_dynamic.utilization["me"] / fa3_static.utilization["me"] - 1.0
    )
    audit.append(
        _point(
            "tisa.fa3_h128.utilization_improvement",
            util_improvement,
            targets["fa3_utilization_improvement"],
            limit,
        )
    )
    audit.append(
        _point(
            "tisa.window8.dispatch_cycles",
            float(simulator.dispatch_latency),
            float(targets["window8_dispatch_cycles"]),
            limit,
        )
    )
    results["fa3_h128"] = {
        "static": fa3_static.to_dict(),
        "dynamic": fa3_dynamic.to_dict(),
        "utilization_improvement": util_improvement,
    }
    return {
        "classification": "source_grounded_cycle_simulation",
        "configuration": {"window": 8, "dispatch_latency": 7, "iterations": 32},
        "results": results,
        "audit": audit,
    }


def _agentxpu_run(targets: dict[str, Any], limit: float) -> dict[str, Any]:
    base_config = XPUConfig(tick_s=0.01)
    results: dict[str, Any] = {"3b": {}, "8b": {}}
    audit: list[dict[str, Any]] = []

    for label, rate_scale, expected in (
        ("3b", 1.0, targets["reactive_latency_reduction_3b"]),
        ("8b", 0.48, targets["reactive_latency_reduction_8b"]),
    ):
        config = replace(
            base_config,
            igpu_prefill_tokens_s=base_config.igpu_prefill_tokens_s * rate_scale,
            serial_prefill_tokens_s=base_config.serial_prefill_tokens_s * rate_scale,
            heg_prefill_tokens_s=base_config.heg_prefill_tokens_s * rate_scale,
            igpu_decode_tokens_s=base_config.igpu_decode_tokens_s * rate_scale,
            heg_decode_tokens_s=base_config.heg_decode_tokens_s * rate_scale,
        )
        simulator = AgentXPUSimulator(config)
        for index, reactive_rate in enumerate((1.0, 3.0, 5.0)):
            flows = poisson_mixed_flows(
                duration_s=900.0,
                proactive_rate_min=6.0,
                reactive_rate_min=reactive_rate,
                seed=100 + index,
            )
            igpu = simulator.run(flows, XPUmode.IGPU)
            heg = simulator.run(flows, XPUmode.HEG)
            if igpu.reactive_mean_latency_s is None or heg.reactive_mean_latency_s is None:
                raise AssertionError("mixed workload produced no reactive flow")
            reduction = 1.0 - heg.reactive_mean_latency_s / igpu.reactive_mean_latency_s
            audit.append(
                _point(
                    f"agentxpu.{label}.reactive_reduction.rate{int(reactive_rate)}",
                    reduction,
                    expected[index],
                    limit,
                )
            )
            results[label][str(int(reactive_rate))] = {
                "flows": len(flows),
                "igpu": igpu.to_dict(),
                "heg": heg.to_dict(),
                "reactive_latency_reduction": reduction,
            }

    representative = results["3b"]["3"]
    representative_igpu = representative["igpu"]
    representative_heg = representative["heg"]
    pending = representative_heg["reactive_prefill_pending_s"]
    audit.append(
        _point(
            "agentxpu.reactive_prefill_pending_s",
            float(pending),
            targets["reactive_prefill_pending_s"],
            limit,
        )
    )
    util_reduction = 1.0 - representative_heg["igpu_utilization"] / representative_igpu[
        "igpu_utilization"
    ]
    energy_reduction = 1.0 - representative_heg["energy_j_token"] / representative_igpu[
        "energy_j_token"
    ]
    audit.append(
        _point(
            "agentxpu.igpu_util_reduction_vs_igpu",
            util_reduction,
            targets["igpu_util_reduction_vs_igpu"],
            limit,
        )
    )
    audit.append(
        _point(
            "agentxpu.energy_reduction_vs_igpu",
            energy_reduction,
            targets["energy_reduction_vs_igpu"],
            limit,
        )
    )

    proactive_flows = poisson_mixed_flows(
        duration_s=300.0,
        proactive_rate_min=40.0,
        reactive_rate_min=0.0,
        seed=44,
    )
    proactive_sim = AgentXPUSimulator(base_config)
    proactive_igpu = proactive_sim.run(proactive_flows, XPUmode.IGPU)
    proactive_heg = proactive_sim.run(proactive_flows, XPUmode.HEG)
    throughput_ratio = proactive_heg.throughput_req_s / proactive_igpu.throughput_req_s
    audit.append(
        _range(
            "agentxpu.proactive_throughput_ratio",
            throughput_ratio,
            targets["proactive_throughput_ratio_range"],
            limit,
        )
    )
    results["proactive_saturation"] = {
        "flows": len(proactive_flows),
        "igpu": proactive_igpu.to_dict(),
        "heg": proactive_heg.to_dict(),
        "throughput_ratio": throughput_ratio,
    }
    results["configuration"] = asdict(base_config)
    return {
        "classification": "source_grounded_trace_simulation",
        "results": results,
        "audit": audit,
    }


def run_reproduction(run_id: str) -> dict[str, Any]:
    targets = json.loads(TARGETS_PATH.read_text(encoding="utf-8"))
    limit = float(targets["max_relative_error"])
    started = time.time()
    sections = {
        "agentix": _agentix_run(targets["agentix"], limit),
        "agentxpu": _agentxpu_run(targets["agentxpu"], limit),
        "tisa": _tisa_run(targets["tisa"], limit),
        "atx": {
            "classification": "functional_only",
            "status": "paper-performance-model-pending",
            "audit": [],
        },
        "chipyard": {
            "classification": "not_run",
            "status": "RoCC implementation pending",
            "audit": [],
        },
    }
    audit = [entry for section in sections.values() for entry in section.get("audit", [])]
    passing = sum(bool(entry["pass"]) for entry in audit)
    failing = [entry for entry in audit if not entry["pass"]]
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "confirmatory_no_residual_guided_retuning",
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "project_commit": _git_head(PROJECT_ROOT),
            "references": {
                "mlx_dev_sys": _git_head(PROJECT_ROOT / ".references" / "MLX_dev_sys"),
                "llm_xpu": _git_head(PROJECT_ROOT / ".references" / "LLM.xpu"),
                "hptpe": _git_head(PROJECT_ROOT / ".references" / "HPTPE"),
                "mllm": _git_head(PROJECT_ROOT / ".references" / "mllm"),
                "chipyard": _git_head(Path("/root/chipyard")),
            },
        },
        "sections": sections,
        "summary": {
            "endpoints_executed": len(audit),
            "endpoints_passing": passing,
            "endpoints_failing": len(failing),
            "max_relative_error": max((entry["relative_error"] for entry in audit), default=None),
            "all_executed_endpoints_within_15pct": not failing,
            "functional_tests": "run separately via pytest",
            "full_goal_complete": False,
            "incomplete_components": ["ATX paper performance", "Chipyard RoCC", "mllm backend", "full-stack trace"],
        },
        "failed_endpoints": failing,
        "wall_time_s": time.time() - started,
    }
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", default="run_001")
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "artifacts" / "results" / "run_001.json",
    )
    args = parser.parse_args(argv)
    result = run_reproduction(args.run_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


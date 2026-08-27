from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any

from .hybrid_plan import DEFAULT_CONFIG
from .hybrid_system import EXPECTED_ROCKET_EVENTS, run_hybrid_workload
from .layer_regression import run_layer_regression
from .workload import PROJECT_ROOT, load_agent_workload


EXPECTED_LLM_CALLS = {
    "react_moa_mcts": 10,
    "react_tool": 2,
    "planner_debate": 5,
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_hybrid_reproduction(
    *,
    config_path: Path = DEFAULT_CONFIG,
    run_id: str = "run_040",
) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if config.get("schema_version") != 1:
        raise ValueError("unsupported hybrid-system configuration")
    output_root = (PROJECT_ROOT / config["output_root"]).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    stages: list[dict[str, Any]] = []

    started = time.monotonic_ns()
    layer = run_layer_regression(
        matrix_path=PROJECT_ROOT / config["layer_matrix"],
        run_id=run_id,
        output_dir=output_root / "layer-regression",
    )
    finished = time.monotonic_ns()
    stages.append(
        {
            "name": "five_paper_layer_regression",
            "started_ns": started,
            "finished_ns": finished,
            "wall_time_s": (finished - started) / 1e9,
            "pass": layer["summary"]["pass"],
        }
    )

    workloads: dict[str, dict[str, Any]] = {}
    if stages[-1]["pass"]:
        for relative in config["workloads"]:
            workload_path = (PROJECT_ROOT / relative).resolve()
            workload = load_agent_workload(workload_path)
            started = time.monotonic_ns()
            result = run_hybrid_workload(
                workload_path,
                run_id=run_id,
                output_dir=output_root / "workloads" / workload.name,
                config_path=config_path,
            )
            finished = time.monotonic_ns()
            stages.append(
                {
                    "name": f"hybrid_workload_{workload.name}",
                    "started_ns": started,
                    "finished_ns": finished,
                    "wall_time_s": (finished - started) / 1e9,
                    "pass": result["summary"]["pass"],
                }
            )
            workloads[workload.name] = result
            if not result["summary"]["pass"]:
                break

    expected_stage_count = 1 + len(config["workloads"])
    serial_order = all(
        later["started_ns"] >= earlier["finished_ns"]
        for earlier, later in zip(stages, stages[1:])
    )
    all_workloads = len(workloads) == len(config["workloads"])
    plan_hashes = {
        _sha256(Path(result["artifacts"]["hybrid_plan"]))
        for result in workloads.values()
    }
    elf_hashes = {
        _sha256(Path(result["artifacts"]["elf"])) for result in workloads.values()
    }
    mllm_audit = json.loads(
        (PROJECT_ROOT / config["mllm_cuda_audit"]).read_text(encoding="utf-8")
    )
    gates = {
        "serial_four_stages": len(stages) == expected_stage_count
        and serial_order
        and all(stage["pass"] for stage in stages),
        "paper_regression_68_at_10_percent": layer["summary"]["endpoints"]
        == layer["summary"]["passing"]
        == 68
        and layer["limit"] == 0.10
        and layer["summary"]["max_relative_error"] <= 0.10,
        "five_paper_switches": layer["summary"]["parameter_switches"] == 5
        and all(layer["sensitivity_gates"].values()),
        "three_distinct_hybrid_workloads": all_workloads
        and len(plan_hashes) == len(elf_hashes) == 3,
        "workload_call_counts": all_workloads
        and all(
            result["summary"]["llm_calls"] == EXPECTED_LLM_CALLS[name]
            and result["summary"]["tool_calls"] == 1
            and result["summary"]["mir_operators"] == EXPECTED_LLM_CALLS[name] * 8
            for name, result in workloads.items()
        ),
        "all_native_dual_gpu_numa": all_workloads
        and all(
            result["native_summary"]["gpus"] == 2
            and result["native_summary"]["numa_nodes"] == 2
            and result["native_summary"]["pass"]
            for result in workloads.values()
        ),
        "all_rocket_tisa_hptpe": all_workloads
        and all(
            result["summary"]["rocket_events"] == EXPECTED_ROCKET_EVENTS[name]
            and result["gates"]["rocket_pipeline"]
            for name, result in workloads.items()
        ),
        "all_multi_clock_traces": all_workloads
        and all(result["trace"]["summary"]["pass"] for result in workloads.values()),
        "gpu_placement_parameter_switch": all_workloads
        and all(
            result["placement_sensitivity"]["pass"]
            for result in workloads.values()
        ),
        "mllm_cuda_lifecycle_13": mllm_audit["summary"]
        == {"gates": 13, "passing": 13, "failing": 0, "pass": True}
        and mllm_audit["framework_patch"]["applied"],
        "adapter_evidence_boundary": all_workloads
        and all(
            "AgentSys MIR-to-CUDA adapter" in result["evidence_boundary"]
            and "not A100" in result["evidence_boundary"]
            for result in workloads.values()
        ),
    }
    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": config["classification"],
        "evidence_boundary": (
            "local RTX4090/Xeon execution plus separate paper-config simulation/RTL regression"
        ),
        "configuration": {"path": str(config_path), "sha256": _sha256(config_path)},
        "stages": stages,
        "layer_regression": {
            "path": str(output_root / "layer-regression/layer-regression.json"),
            "sha256": _sha256(output_root / "layer-regression/layer-regression.json"),
            "summary": layer["summary"],
        },
        "workloads": {
            name: {
                "path": result["output"],
                "sha256": _sha256(Path(result["output"])),
                "summary": result["summary"],
                "plan_summary": result["plan_summary"],
                "native_summary": result["native_summary"],
                "trace": result["trace"],
                "placement_sensitivity": result["placement_sensitivity"],
            }
            for name, result in workloads.items()
        },
        "gates": gates,
        "summary": {
            "stages": expected_stage_count,
            "executed": len(stages),
            "workloads": len(workloads),
            "paper_layers": layer["summary"]["layers"],
            "parameter_switches": layer["summary"]["parameter_switches"] + 1,
            "paper_endpoints": layer["summary"]["endpoints"],
            "paper_endpoints_passing": layer["summary"]["passing"],
            "max_relative_error": layer["summary"]["max_relative_error"],
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "serial_order": serial_order,
            "pass": all(gates.values()),
        },
    }
    manifest_path = (PROJECT_ROOT / config["manifest"]).resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    manifest["output"] = str(manifest_path)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reproduce the hybrid dual-GPU/Rocket Agent system")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id", default="run_040")
    args = parser.parse_args(argv)
    result = run_hybrid_reproduction(config_path=args.config, run_id=args.run_id)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

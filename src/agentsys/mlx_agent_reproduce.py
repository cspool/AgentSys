from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path
from typing import Any

from .mlx_agent_system import run_agent_mlx_system
from .workload import PROJECT_ROOT, load_agent_workload


DEFAULT_CONFIG = PROJECT_ROOT / "config/mlx-agent-system.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_mlx_agent_reproduction(
    *,
    config_path: Path = DEFAULT_CONFIG,
    run_id: str = "run_046",
    output_root: Path | None = None,
    manifest_path: Path | None = None,
) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    output_root = (
        output_root or PROJECT_ROOT / config["output_root"]
    ).resolve()
    output_root.mkdir(parents=True, exist_ok=True)
    stages: list[dict[str, Any]] = []
    results: dict[str, dict[str, Any]] = {}
    for relative in config["workloads"]:
        workload_path = (PROJECT_ROOT / relative).resolve()
        workload = load_agent_workload(workload_path)
        started = time.monotonic_ns()
        result = run_agent_mlx_system(
            workload_path,
            run_id=run_id,
            output_dir=output_root / "workloads" / workload.name,
            source_config_path=PROJECT_ROOT / config["source_config"],
        )
        finished = time.monotonic_ns()
        stages.append(
            {
                "name": f"workload_{workload.name}",
                "started_ns": started,
                "finished_ns": finished,
                "wall_time_s": (finished - started) / 1e9,
                "pass": result["summary"]["pass"],
            }
        )
        results[workload.name] = result
        if not result["summary"]["pass"]:
            break
    serial = all(
        later["started_ns"] >= earlier["finished_ns"]
        for earlier, later in zip(stages, stages[1:])
    )
    complete = len(results) == len(config["workloads"])
    header_hashes = {
        _sha256(Path(result["artifacts"]["agent_header"])) for result in results.values()
    }
    elf_hashes = {
        _sha256(Path(result["artifacts"]["elf"])) for result in results.values()
    }
    workload_hashes = {result["workload"]["sha256"] for result in results.values()}
    count_gate = complete
    aggregate_gate = complete
    for name, result in results.items():
        expected = config["expected"][name]
        count_gate = count_gate and result["summary"]["calls"] == expected["calls"]
        count_gate = count_gate and result["summary"]["llm_calls"] == expected["llm"]
        count_gate = count_gate and result["summary"]["tool_calls"] == expected["tools"]
        count_gate = count_gate and result["summary"]["mlx_micro_ops"] == expected["micro_ops"]
        cycle = result["backend_results"]["cycle"]["parsed"]["summary"]
        rtl = result["backend_results"]["rtl"]["parsed"]["summary"]
        aggregate_gate = aggregate_gate and cycle["dma"] == rtl["dma"] == expected["dma"]
        aggregate_gate = aggregate_gate and cycle["system"] == expected["cycle_system"]
        aggregate_gate = aggregate_gate and rtl["system"] == expected["rtl_system"]
    source_config = json.loads(
        (PROJECT_ROOT / config["source_config"]).read_text(encoding="utf-8")
    )
    source_root = PROJECT_ROOT / source_config["active_path"]
    gates = {
        "three_serial_workloads": complete
        and len(stages) == 3
        and serial
        and all(stage["pass"] for stage in stages),
        "three_distinct_artifact_chains": len(workload_hashes)
        == len(header_hashes)
        == len(elf_hashes)
        == 3,
        "expected_call_and_micro_counts": count_gate,
        "cache_aware_aggregate_counters": aggregate_gate,
        "all_system_gates": complete
        and all(result["summary"]["pass"] and all(result["gates"].values()) for result in results.values()),
        "all_backend_gates": complete
        and all(
            all(values.values())
            for result in results.values()
            for values in result["backend_gates"].values()
        ),
        "trace_layer_contract": complete
        and all(len(result["trace"]["layers"]) >= 14 for result in results.values()),
        "backend_switch_changes_cycles": complete
        and all(result["summary"]["cycle_kernel"] > result["summary"]["rtl_kernel"] for result in results.values()),
        "source_clean_and_pinned": subprocess.check_output(
            ["git", "-C", str(source_root), "rev-parse", "HEAD"], text=True
        ).strip()
        == source_config["active_commit"]
        and not subprocess.check_output(
            ["git", "-C", str(source_root), "status", "--porcelain", "--untracked-files=no"],
            text=True,
        ).strip(),
    }
    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": config["classification"],
        "evidence_boundary": (
            "AgentSys Agent/mllm/TISA-to-MLX compiler on open-surrogate MLX RTL; "
            "no paper performance target consumed"
        ),
        "configuration": {"path": str(config_path), "sha256": _sha256(config_path)},
        "stages": stages,
        "workloads": {
            name: {
                "path": result["output"],
                "sha256": _sha256(Path(result["output"])),
                "summary": result["summary"],
                "trace": result["trace"],
            }
            for name, result in results.items()
        },
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "workloads": len(results),
            "calls": sum(result["summary"]["calls"] for result in results.values()),
            "llm_calls": sum(result["summary"]["llm_calls"] for result in results.values()),
            "tool_calls": sum(result["summary"]["tool_calls"] for result in results.values()),
            "mlx_micro_ops": sum(result["summary"]["mlx_micro_ops"] for result in results.values()),
            "serial_order": serial,
            "pass": all(gates.values()),
        },
    }
    manifest_path = (
        manifest_path or PROJECT_ROOT / config["manifest"]
    ).resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest["output"] = str(manifest_path)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serially reproduce three Agent DAGs on Rocket+MLX")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id", default="run_046")
    parser.add_argument("--output-root", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args(argv)
    result = run_mlx_agent_reproduction(
        config_path=args.config,
        run_id=args.run_id,
        output_root=args.output_root,
        manifest_path=args.manifest,
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

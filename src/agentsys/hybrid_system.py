from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path
from typing import Any, Callable

from .hybrid_plan import DEFAULT_CONFIG, write_hybrid_plan
from .hybrid_runtime import run_hybrid_native
from .workload import PROJECT_ROOT, load_agent_workload
from .workload_pipeline import run_workload_pipeline


EXPECTED_ROCKET_EVENTS = {
    "react_moa_mcts": 860,
    "react_tool": 180,
    "planner_debate": 436,
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _stage(name: str, operation: Callable[[], Any]) -> tuple[Any, dict[str, Any]]:
    started = time.monotonic_ns()
    result = operation()
    finished = time.monotonic_ns()
    summary = result.get("summary", {}) if isinstance(result, dict) else {}
    return result, {
        "name": name,
        "started_ns": started,
        "finished_ns": finished,
        "wall_time_s": (finished - started) / 1e9,
        "pass": bool(summary.get("pass", True)),
    }


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def merge_hybrid_trace(
    *,
    workload_name: str,
    workload_sha256: str,
    plan_path: Path,
    native_trace_path: Path,
    rocket_trace_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    plan = json.loads(plan_path.read_text(encoding="utf-8"))
    native = _jsonl(native_trace_path)
    rocket = _jsonl(rocket_trace_path)
    events: list[dict[str, Any]] = []
    for source_sequence, event in enumerate(native):
        events.append(
            {
                **event,
                "source": "native_dual_gpu_numa",
                "source_sequence": source_sequence,
                "clock_value": event["start_ns"],
            }
        )
    for source_sequence, event in enumerate(rocket):
        backend = event["backend"]
        events.append(
            {
                **event,
                "source": f"rocket_{backend}_tisa_hptpe",
                "source_sequence": source_sequence,
                "clock_domain": f"rocket_{backend}_cycle",
                "clock_value": event["cycle"],
            }
        )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for sequence, event in enumerate(events):
            event["hybrid_sequence"] = sequence
            handle.write(json.dumps(event, sort_keys=True) + "\n")

    calls = {call["call_id"] for call in plan["calls"]}
    native_calls = {event["call_id"] for event in native if event["call_id"] is not None}
    rocket_calls = {event["call_id"] for event in rocket if event["call_id"] is not None}
    layers = sorted({str(event["layer"]) for event in events})
    clock_domains = sorted({str(event["clock_domain"]) for event in events})
    gates = {
        "workload_identity": all(
            event["workload"] == workload_name
            and event["workload_sha256"] == workload_sha256
            for event in events
        ),
        "call_identity": native_calls == rocket_calls == calls,
        "event_conservation": len(events) == len(native) + len(rocket),
        "separate_clock_domains": "host_monotonic_ns" in clock_domains
        and "rocket_dynamic_cycle" in clock_domains
        and "rocket_static_cycle" in clock_domains
        and all("clock_domain" in event and "clock_value" in event for event in events),
        "vertical_layers": {
            "application",
            "framework",
            "mllm",
            "agentxpu",
            "software",
            "cpu",
            "gpu",
            "cuda",
            "nccl",
            "tisa",
            "hptpe",
        }.issubset(layers),
    }
    return {
        "path": str(output_path),
        "sha256": _sha256(output_path),
        "events": len(events),
        "native_events": len(native),
        "rocket_events": len(rocket),
        "layers": layers,
        "clock_domains": clock_domains,
        "alignment": "call_identity_only_no_cross_domain_time_conversion",
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }


def _placement_sensitivity(
    baseline: dict[str, Any], variant: dict[str, Any]
) -> dict[str, Any]:
    invariant = (
        [call["call_id"] for call in baseline["calls"]]
        == [call["call_id"] for call in variant["calls"]]
        and [call["deps"] for call in baseline["calls"]]
        == [call["deps"] for call in variant["calls"]]
        and [call["mir_operators"] for call in baseline["calls"]]
        == [call["mir_operators"] for call in variant["calls"]]
        and [call["xpu"] for call in baseline["calls"]]
        == [call["xpu"] for call in variant["calls"]]
    )
    baseline_signature = [
        call["native"]["rank"] for call in baseline["calls"] if call["kind"] == "llm"
    ]
    variant_signature = [
        call["native"]["rank"] for call in variant["calls"] if call["kind"] == "llm"
    ]
    return {
        "baseline": baseline["configuration"]["placement"],
        "variant": variant["configuration"]["placement"],
        "baseline_signature": baseline_signature,
        "variant_signature": variant_signature,
        "logical_work_invariant": invariant,
        "changed": baseline_signature != variant_signature,
        "pass": invariant and baseline_signature != variant_signature,
    }


def run_hybrid_workload(
    workload_path: Path,
    *,
    run_id: str,
    output_dir: Path,
    config_path: Path = DEFAULT_CONFIG,
) -> dict[str, Any]:
    config_path = config_path.resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    workload = load_agent_workload(workload_path)
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    stages: list[dict[str, Any]] = []

    pipeline, evidence = _stage(
        "agentix_mllm_agentxpu_riscv_rocket_tisa_hptpe",
        lambda: run_workload_pipeline(
            workload_path,
            run_id=run_id,
            output_dir=output_dir / "rocket",
            execute_system=True,
            component_certificate=PROJECT_ROOT / config["component_certificate"],
            timeout_s=float(config["timeout_s"]),
        ),
    )
    stages.append(evidence)
    rocket_root = output_dir / "rocket"
    application_path = rocket_root / "application.json"
    compiled_path = rocket_root / "compiled.json"
    header_path = rocket_root / "generated/workload.h"
    elf_path = rocket_root / "software/workload.riscv"
    rocket_trace_path = rocket_root / "system-trace.jsonl"

    plan_path = output_dir / "hybrid-plan.json"
    plan, evidence = _stage(
        "hybrid_plan_compile",
        lambda: write_hybrid_plan(
            plan_path,
            workload,
            application_path=application_path,
            compiled_path=compiled_path,
            header_path=header_path,
            elf_path=elf_path,
            config_path=config_path,
            placement=config["placement"],
            run_id=run_id,
        ),
    )
    evidence["pass"] = bool(plan["summary"]["pass"])
    stages.append(evidence)

    variant_path = output_dir / "hybrid-plan-gpu0-only.json"
    variant, evidence = _stage(
        "gpu_placement_sensitivity_compile",
        lambda: write_hybrid_plan(
            variant_path,
            workload,
            application_path=application_path,
            compiled_path=compiled_path,
            header_path=header_path,
            elf_path=elf_path,
            config_path=config_path,
            placement=config["sensitivity_placement"],
            run_id=run_id,
        ),
    )
    sensitivity = _placement_sensitivity(plan, variant)
    evidence["pass"] = bool(sensitivity["pass"])
    stages.append(evidence)

    native_dir = output_dir / "native"
    native, evidence = _stage(
        "real_dual_gpu_dual_numa_runtime",
        lambda: run_hybrid_native(plan_path=plan_path, output_dir=native_dir),
    )
    stages.append(evidence)

    merged_path = output_dir / "hybrid-trace.jsonl"
    merged, evidence = _stage(
        "multi_clock_trace_merge",
        lambda: merge_hybrid_trace(
            workload_name=workload.name,
            workload_sha256=workload.sha256,
            plan_path=plan_path,
            native_trace_path=native_dir / "native-trace.jsonl",
            rocket_trace_path=rocket_trace_path,
            output_path=merged_path,
        ),
    )
    stages.append(evidence)

    rocket_system = json.loads((rocket_root / "system.json").read_text(encoding="utf-8"))
    expected_rocket_events = EXPECTED_ROCKET_EVENTS[workload.name]
    gates = {
        "rocket_pipeline": pipeline["summary"]["pass"]
        and rocket_system["summary"]["pass"]
        and all(rocket_system["gates"].values()),
        "hybrid_plan": plan["summary"]["pass"],
        "placement_sensitivity": sensitivity["pass"],
        "native_runtime": native["summary"]["pass"] and all(native["gates"].values()),
        "rocket_event_contract": rocket_system["trace"]["events"]
        == merged["rocket_events"]
        == expected_rocket_events,
        "merged_trace": merged["summary"]["pass"] and all(merged["gates"].values()),
        "lineage_hashes": plan["lineage"]["application"]["sha256"]
        == _sha256(application_path)
        and plan["lineage"]["compiled"]["sha256"] == _sha256(compiled_path)
        and plan["lineage"]["generated_header"]["sha256"] == _sha256(header_path)
        and plan["lineage"]["riscv_elf"]["sha256"] == _sha256(elf_path),
        "mllm_cuda_boundary": plan["lineage"]["mllm_cuda_audit"]["summary"]["pass"]
        and "adapter" in plan["evidence_boundary"].lower()
        and "not A100" in plan["evidence_boundary"],
    }
    serial_order = all(
        later["started_ns"] >= earlier["finished_ns"]
        for earlier, later in zip(stages, stages[1:])
    )
    gates["serial_order"] = serial_order
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "vertical_agent_to_dual_gpu_and_rocket_tisa_hptpe_experiment",
        "evidence_boundary": plan["evidence_boundary"],
        "configuration": {"path": str(config_path), "sha256": _sha256(config_path)},
        "workload": workload.to_contract_dict(),
        "stages": stages,
        "artifacts": {
            "pipeline": str(rocket_root / "pipeline.json"),
            "application": str(application_path),
            "compiled": str(compiled_path),
            "header": str(header_path),
            "elf": str(elf_path),
            "rocket_system": str(rocket_root / "system.json"),
            "rocket_trace": str(rocket_trace_path),
            "hybrid_plan": str(plan_path),
            "placement_variant": str(variant_path),
            "native_runtime": str(native_dir / "native-runtime.json"),
            "native_trace": str(native_dir / "native-trace.jsonl"),
            "hybrid_trace": str(merged_path),
        },
        "plan_summary": plan["summary"],
        "native_summary": native["summary"],
        "rocket_summary": rocket_system["summary"],
        "trace": merged,
        "placement_sensitivity": sensitivity,
        "gates": gates,
        "summary": {
            "stages": len(stages),
            "calls": plan["summary"]["calls"],
            "llm_calls": plan["summary"]["llm_calls"],
            "tool_calls": plan["summary"]["tool_calls"],
            "mir_operators": plan["summary"]["mir_operators"],
            "rocket_events": merged["rocket_events"],
            "native_events": merged["native_events"],
            "hybrid_events": merged["events"],
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }
    output = output_dir / "hybrid-system.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["output"] = str(output)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one Agent DAG on dual GPU/NUMA and Rocket/TISA/HPTPE")
    parser.add_argument("--workload", type=Path, required=True)
    parser.add_argument("--run-id", default="run_local")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args(argv)
    result = run_hybrid_workload(
        args.workload,
        run_id=args.run_id,
        output_dir=args.output_dir,
        config_path=args.config,
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

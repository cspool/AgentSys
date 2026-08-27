from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any, Callable

from .mlx_agent_compiler import build_agent_mlx_elf, compile_agent_mlx
from .mlx_reference import DEFAULT_CONFIG as DEFAULT_SOURCE_CONFIG
from .parameterized_application import write_parameterized_application
from .parameterized_compiler import compile_parameterized_workload
from .workload import AgentWorkload, PROJECT_ROOT, load_agent_workload


BACKENDS = {"cycle": "MLXCycleRocketConfig", "rtl": "MLXRTLRocketConfig"}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _stage(name: str, operation: Callable[[], Any]) -> tuple[Any, dict[str, Any]]:
    started = time.monotonic_ns()
    result = operation()
    finished = time.monotonic_ns()
    passed = bool(result.get("summary", {}).get("pass", result.get("pass", True)))
    return result, {
        "name": name,
        "started_ns": started,
        "finished_ns": finished,
        "wall_time_s": (finished - started) / 1e9,
        "pass": passed,
    }


def _fields(fragment: str) -> dict[str, int | str]:
    values: dict[str, int | str] = {}
    strings = {"workload", "backend", "call", "program", "kind"}
    hex_fields = {
        "abi",
        "checksum",
        "completed",
        "app_digest",
        "mir_digest",
        "workload_digest",
        "deps",
    }
    for key, value in re.findall(r"(\w+)=([^\s]+)", fragment):
        if key in strings:
            values[key] = value
        elif key in hex_fields:
            values[key] = int(value, 16)
        else:
            try:
                values[key] = int(value)
            except ValueError:
                values[key] = value
    return values


def parse_agent_mlx_log(text: str) -> dict[str, Any]:
    call_records: list[dict[str, int | str]] = []
    for match in re.finditer(r"AGENTSYS_MLX_CALL index=.*", text):
        fragment = match.group(0).splitlines()[0]
        call_records.append(_fields(fragment))
    final_match = re.search(r"AGENTSYS_MLX_PASS workload=.*", text)
    if final_match is None:
        raise ValueError("Agent MLX log has no contiguous PASS summary")
    final = _fields(final_match.group(0).splitlines()[0])
    return {"calls": call_records, "summary": final}


def _runtime_trace(
    workload: AgentWorkload,
    application: dict[str, Any],
    mlx_manifest: dict[str, Any],
    backend_results: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for event in application["events"]:
        events.append(
            {
                "source": "agent_application",
                "clock_domain": "agentix_logical_step",
                "time": event["logical_time"],
                "layer": event["layer"],
                "event": event["event"],
                "call_id": event["call_id"],
                "program_id": event["program_id"],
                "details": event["details"],
            }
        )
    selected = mlx_manifest["model"]["selected_operators"]
    for call in mlx_manifest["calls"]:
        call_id = call["call_id"]
        common = {
            "call_id": call_id,
            "call_index": call["index"],
            "program_id": call["program_id"],
            "priority": call["priority"],
        }
        events.append(
            {
                **common,
                "source": "agentsys_mlx_compiler",
                "clock_domain": "identity_only",
                "time": call["index"],
                "layer": "agentxpu",
                "event": "flow_stage_place",
                "details": call["agentxpu"],
            }
        )
        if call["kind"] == "llm":
            for operator in selected:
                events.append(
                    {
                        **common,
                        "source": "mllm_tisa_compiler",
                        "clock_domain": "identity_only",
                        "time": operator["index"],
                        "layer": "mllm",
                        "event": "mir_source_lower",
                        "details": {
                            "source_index": operator["index"],
                            "op_type": operator["op_type"],
                            "engine": operator["engine"],
                        },
                    }
                )
            for descriptor in call["tisa_descriptors"]:
                events.append(
                    {
                        **common,
                        "source": "mllm_tisa_compiler",
                        "clock_domain": "identity_only",
                        "time": descriptor["index"],
                        "layer": "tisa",
                        "event": "semantic_tile_lower",
                        "details": {
                            "source_index": descriptor["source_index"],
                            "engine": descriptor["engine"],
                            "stage": descriptor["stage_code"],
                            "placement": descriptor["placement"],
                        },
                    }
                )
            for micro in mlx_manifest["micro_lineage"]:
                operation = micro["mlx_operation"]
                layer = (
                    "mlx_network"
                    if operation == "xfer"
                    else "mlx_spm"
                    if operation in {"load", "store"}
                    else "mlx_pe"
                )
                events.append(
                    {
                        **common,
                        "source": "agentsys_mlx_compiler",
                        "clock_domain": "spatial_program_order",
                        "time": micro["micro_index"],
                        "layer": layer,
                        "event": "spatial_micro_op",
                        "details": micro,
                    }
                )
            events.append(
                {
                    **common,
                    "source": "agentsys_mlx_compiler",
                    "clock_domain": "identity_only",
                    "time": call["index"],
                    "layer": "mlx_tag",
                    "event": "tagged_multilayer_program",
                    "details": {
                        "micro_ops": call["mlx"]["micro_ops"],
                        "active_pes": call["mlx"]["active_pes"],
                    },
                }
            )
        for backend, backend_result in backend_results.items():
            runtime_call = next(
                item for item in backend_result["parsed"]["calls"] if item["call"] == call_id
            )
            if call["kind"] == "tool":
                events.append(
                    {
                        **common,
                        "source": f"rocket_mlx_{backend}",
                        "clock_domain": f"rocket_{backend}_cycles",
                        "time": runtime_call["cpu_cycles"],
                        "layer": "cpu",
                        "event": "tool_complete",
                        "details": runtime_call,
                    }
                )
            else:
                for layer, event_name, key in (
                    ("software", "mlx_call_complete", "system"),
                    ("dma", "dma_complete", "dma"),
                    ("mlx", "kernel_complete", "kernel"),
                    ("result", "golden_complete", "mismatches"),
                ):
                    events.append(
                        {
                            **common,
                            "source": f"rocket_mlx_{backend}",
                            "clock_domain": f"rocket_{backend}_cycles",
                            "time": runtime_call[key],
                            "layer": layer,
                            "event": event_name,
                            "details": runtime_call,
                        }
                    )
    for sequence, event in enumerate(events):
        event["schema_version"] = 1
        event["sequence"] = sequence
        event["workload"] = workload.name
        event["workload_sha256"] = workload.sha256
    return events


def run_agent_mlx_system(
    workload_path: Path,
    *,
    run_id: str,
    output_dir: Path,
    source_config_path: Path = DEFAULT_SOURCE_CONFIG,
) -> dict[str, Any]:
    workload = load_agent_workload(workload_path)
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    application_path = output_dir / "application.json"
    tisa_path = output_dir / "compiled-tisa.json"
    tisa_header = output_dir / "generated/tisa-workload.h"
    mlx_path = output_dir / "compiled-mlx.json"
    agent_header = output_dir / "generated/agent-mlx.h"
    elf_path = output_dir / "software/agent-mlx.riscv"
    stages: list[dict[str, Any]] = []

    application, stage = _stage(
        "agentix_application",
        lambda: write_parameterized_application(workload, application_path, run_id=run_id),
    )
    stages.append(stage)
    compiled, stage = _stage(
        "mllm_agentxpu_tisa_compile",
        lambda: compile_parameterized_workload(
            workload,
            application,
            application_path=application_path,
            manifest_path=tisa_path,
            header_path=tisa_header,
            run_id=run_id,
        ),
    )
    stages.append(stage)
    mlx_manifest, stage = _stage(
        "tisa_to_mlx_spatial_compile",
        lambda: compile_agent_mlx(
            workload,
            application,
            compiled,
            application_path=application_path,
            compiled_path=tisa_path,
            header_path=agent_header,
            manifest_path=mlx_path,
            source_config_path=source_config_path,
            run_id=run_id,
        ),
    )
    stages.append(stage)
    build, stage = _stage(
        "ordinary_riscv_elf_build",
        lambda: build_agent_mlx_elf(
            agent_header=agent_header,
            mlx_manifest=mlx_manifest,
            elf_path=elf_path,
            source_config_path=source_config_path,
        ),
    )
    stages.append(stage)

    source_config = json.loads(source_config_path.read_text(encoding="utf-8"))
    chipyard = Path(source_config["chipyard"]["path"])
    backend_results: dict[str, dict[str, Any]] = {}
    for backend, config_name in BACKENDS.items():
        simulator = chipyard / f"sims/verilator/simulator-chipyard-{config_name}"
        log = output_dir / f"logs/{backend}.log"

        def execute(simulator: Path = simulator, log: Path = log) -> dict[str, Any]:
            started = time.monotonic_ns()
            process = subprocess.run(
                [str(simulator), str(elf_path)],
                cwd=PROJECT_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=900,
                check=False,
            )
            finished = time.monotonic_ns()
            log.parent.mkdir(parents=True, exist_ok=True)
            log.write_text(process.stdout, encoding="utf-8")
            parsed = parse_agent_mlx_log(process.stdout)
            return {
                "backend": backend,
                "config": config_name,
                "simulator": {"path": str(simulator), "sha256": _sha256(simulator)},
                "elf_sha256": _sha256(elf_path),
                "returncode": process.returncode,
                "wall_time_s": (finished - started) / 1e9,
                "log": {"path": str(log), "sha256": _sha256(log), "bytes": log.stat().st_size},
                "parsed": parsed,
                "summary": {"pass": process.returncode == 0},
            }

        backend_result, stage = _stage(f"rocket_mlx_{backend}", execute)
        stages.append(stage)
        backend_results[backend] = backend_result

    calls_by_id = {call["call_id"]: call for call in mlx_manifest["calls"]}
    expected_llm = int(mlx_manifest["summary"]["llm_calls"])
    expected_tool = int(mlx_manifest["summary"]["tool_calls"])
    backend_gates: dict[str, dict[str, bool]] = {}
    for backend, result in backend_results.items():
        parsed = result["parsed"]
        call_records = parsed["calls"]
        final = parsed["summary"]
        expected_kernel = 132 if backend == "cycle" else 76
        llm_records = [item for item in call_records if item["kind"] == "llm"]
        tool_records = [item for item in call_records if item["kind"] == "tool"]
        backend_gates[backend] = {
            "exit_identity_abi": result["returncode"] == 0
            and final["workload"] == workload.name
            and final["backend"] == backend
            and final["mismatches"] == 0,
            "calls_exact": len(call_records) == len(mlx_manifest["calls"])
            and [item["call"] for item in call_records]
            == [call["call_id"] for call in mlx_manifest["calls"]],
            "llm_tool_launch_counts": final["llm_calls"] == final["launches"] == expected_llm
            and final["tool_calls"] == expected_tool
            and len(llm_records) == expected_llm
            and len(tool_records) == expected_tool,
            "dependencies_and_complete": final["dependencies"] == 0
            and final["completed"] == (1 << len(mlx_manifest["calls"])) - 1,
            "per_call_hardware": all(
                item["kernel"] == expected_kernel
                and item["instructions"] == 45
                and item["dma_bytes"] == 576
                and item["system"] == item["dma"] + item["kernel"] + 2
                and item["instructions"]
                == item["load"] + item["store"] + item["compute"] + item["xfer"]
                and item["abi"] == 0x4D4C5801
                and item["mismatches"] == 0
                for item in llm_records
            ),
            "aggregate_hardware": final["kernel"] == expected_llm * expected_kernel
            and final["instructions"] == expected_llm * 45
            and final["dma_bytes"] == expected_llm * 576
            and final["system"] == expected_llm * (344 + expected_kernel + 2),
            "metadata": all(
                item["program"] == calls_by_id[str(item["call"])]["program_id"]
                and item["first"] == calls_by_id[str(item["call"])]["program_first"]
                and item["last"] == calls_by_id[str(item["call"])]["program_last"]
                for item in call_records
            ),
        }
    cycle_final = backend_results["cycle"]["parsed"]["summary"]
    rtl_final = backend_results["rtl"]["parsed"]["summary"]
    same_keys = (
        "programs",
        "calls",
        "llm_calls",
        "tool_calls",
        "launches",
        "instructions",
        "load",
        "store",
        "compute",
        "xfer",
        "dma_bytes",
        "checksum",
        "app_digest",
        "mir_digest",
        "workload_digest",
        "mismatches",
    )
    trace = _runtime_trace(workload, application, mlx_manifest, backend_results)
    trace_path = output_dir / "system-trace.jsonl"
    with trace_path.open("w", encoding="utf-8") as handle:
        for event in trace:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
    layers = sorted({event["layer"] for event in trace})
    gates = {
        "serial_seven_stages": len(stages) == 7
        and all(stage["pass"] for stage in stages)
        and all(
            later["started_ns"] >= earlier["finished_ns"]
            for earlier, later in zip(stages, stages[1:])
        ),
        "workload_identity": application["workload"]["sha256"]
        == compiled["workload"]["sha256"]
        == mlx_manifest["workload"]["sha256"]
        == workload.sha256,
        "compiler_lineage": mlx_manifest["summary"]["pass"]
        and all(mlx_manifest["gates"].values())
        and len(mlx_manifest["micro_lineage"]) == 45,
        "distinct_backend_execution": all(
            all(values.values()) for values in backend_gates.values()
        ),
        "same_logical_work": all(cycle_final[key] == rtl_final[key] for key in same_keys),
        "frozen_counts": cycle_final["instructions"]
        == rtl_final["instructions"]
        == expected_llm * 45
        and cycle_final["dma_bytes"] == rtl_final["dma_bytes"] == expected_llm * 576
        and cycle_final["kernel"] == expected_llm * 132
        and rtl_final["kernel"] == expected_llm * 76,
        "trace_layers_and_calls": {
            "application",
            "framework",
            "mllm",
            "agentxpu",
            "tisa",
            "cpu",
            "software",
            "dma",
            "mlx",
            "mlx_tag",
            "mlx_pe",
            "mlx_spm",
            "mlx_network",
            "result",
        }.issubset(layers)
        and {event["call_id"] for event in trace if event.get("call_id") is not None}
        == set(calls_by_id),
        "backend_parameter_switch": cycle_final["kernel"] > rtl_final["kernel"]
        and backend_results["cycle"]["config"] != backend_results["rtl"]["config"],
        "ordinary_cpu_no_atx_hptpe": all(
            "ATX" not in Path(result["log"]["path"]).read_text(encoding="utf-8")
            and "HPTPE" not in Path(result["log"]["path"]).read_text(encoding="utf-8")
            for result in backend_results.values()
        ),
        "parents": json.loads(
            (PROJECT_ROOT / "artifacts/mlx_standalone/run_043/mlx-standalone.json").read_text(
                encoding="utf-8"
            )
        )["summary"]["pass"]
        and json.loads(
            (PROJECT_ROOT / "artifacts/mlx_chipyard/run_044/mlx-chipyard.json").read_text(
                encoding="utf-8"
            )
        )["summary"]["pass"],
    }
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "vertical_agentix_mllm_agentxpu_tisa_ordinary_rocket_mlx_system",
        "evidence_boundary": mlx_manifest["evidence_boundary"],
        "workload": workload.to_contract_dict(),
        "stages": stages,
        "artifacts": {
            "application": str(application_path),
            "compiled_tisa": str(tisa_path),
            "compiled_mlx": str(mlx_path),
            "agent_header": str(agent_header),
            "elf": str(elf_path),
            "trace": str(trace_path),
        },
        "compiler_summary": mlx_manifest["summary"],
        "backend_results": backend_results,
        "backend_gates": backend_gates,
        "trace": {"path": str(trace_path), "sha256": _sha256(trace_path), "events": len(trace), "layers": layers},
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "programs": len(workload.programs),
            "calls": len(mlx_manifest["calls"]),
            "llm_calls": expected_llm,
            "tool_calls": expected_tool,
            "mlx_micro_ops": mlx_manifest["summary"]["mlx_micro_ops"],
            "cycle_kernel": cycle_final["kernel"],
            "rtl_kernel": rtl_final["kernel"],
            "trace_events": len(trace),
            "pass": all(gates.values()),
        },
    }
    output = output_dir / "mlx-agent-system.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    result["output"] = str(output)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compile and execute one Agent DAG on Rocket+MLX")
    parser.add_argument("--workload", type=Path, required=True)
    parser.add_argument("--run-id", default="run_local")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-config", type=Path, default=DEFAULT_SOURCE_CONFIG)
    args = parser.parse_args(argv)
    result = run_agent_mlx_system(
        args.workload,
        run_id=args.run_id,
        output_dir=args.output_dir,
        source_config_path=args.source_config,
    )
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(result["output"])
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

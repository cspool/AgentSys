from __future__ import annotations

import hashlib
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from .paths import chipyard_source_identity
from .revised_system import (
    CHIPYARD_ROOT,
    PROJECT_ROOT,
    SIM_ROOT,
    _dependency_gate,
    _git_head,
    _installed_sources,
    _sha256,
    expand_trace,
    parse_revised_output,
)
from .workload import AgentWorkload


def _run_backend(
    backend: str,
    *,
    elf_path: Path,
    log_path: Path,
    timeout_s: float,
) -> dict[str, Any]:
    config = (
        "AgentSysRevisedStaticRocketConfig"
        if backend == "static"
        else "AgentSysRevisedDynamicRocketConfig"
    )
    simulator = SIM_ROOT / f"simulator-chipyard-{config}"
    if not simulator.is_file() or not elf_path.is_file():
        raise FileNotFoundError(f"missing simulator or workload ELF: {simulator}, {elf_path}")
    tile_log_path = log_path.with_name(log_path.stem + "-tisa.log")
    tile_log_path.parent.mkdir(parents=True, exist_ok=True)
    tile_log_path.unlink(missing_ok=True)
    started = time.time()
    process = subprocess.run(
        [
            str(simulator),
            "+permissive",
            f"+agentsys_tisa_trace={tile_log_path}",
            "+permissive-off",
            str(elf_path),
        ],
        cwd=SIM_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_s,
        check=False,
    )
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(process.stdout, encoding="utf-8")
    if not tile_log_path.is_file() or tile_log_path.stat().st_size == 0:
        raise RuntimeError(f"dedicated TISA trace was not produced: {tile_log_path}")
    tile_log = tile_log_path.read_text(encoding="utf-8")
    return {
        "backend": backend,
        "config": config,
        "simulator": str(simulator),
        "simulator_sha256": _sha256(simulator),
        "exit_code": process.returncode,
        "wall_time_s": time.time() - started,
        "raw_log": str(log_path),
        "raw_log_sha256": _sha256(log_path),
        "tile_log": str(tile_log_path),
        "tile_log_sha256": _sha256(tile_log_path),
        "parsed": parse_revised_output(process.stdout + "\n" + tile_log),
        "log": process.stdout,
    }


def _tile_gate(parsed: dict[str, Any], compiled: dict[str, Any]) -> bool:
    expected_calls = {
        int(call["index"]): call
        for call in compiled["hardware_calls"]
        if call["kind"] == "llm"
    }
    expected_count = int(compiled["summary"]["descriptors"])
    issues = [event for event in parsed["hardware"] if event["event"] == "issue"]
    completes = [event for event in parsed["hardware"] if event["event"] == "complete"]
    if len(issues) != expected_count or len(completes) != expected_count:
        return False
    issue_keys = {
        (event["call_index"], event["index"], event["engine"]) for event in issues
    }
    complete_keys = {
        (event["call_index"], event["index"], event["engine"]) for event in completes
    }
    if issue_keys != complete_keys or len(issue_keys) != expected_count:
        return False
    for event in issues:
        if event["call_index"] not in expected_calls:
            return False
        call = expected_calls[event["call_index"]]
        if event["index"] >= len(call["descriptors"]):
            return False
        descriptor = call["descriptors"][event["index"]]
        if (
            event["engine"] != descriptor["engine"]
            or event["source"] != descriptor["source_index"]
            or event["flow"] != descriptor["flow_code"]
            or event["stage"] != descriptor["stage_code"]
            or event["placement"] != descriptor["placement_code"]
            or event["preemptible"] != descriptor["preemptible"]
            or event["priority"] != call["priority"]
            or event["duration"] != descriptor["duration"]
        ):
            return False
    return True


def _first_issue_gate(
    parsed: dict[str, Any],
    *,
    expected_calls: int,
    expected_cycle: int,
) -> bool:
    if expected_calls == 0:
        return not parsed["hardware"]
    first_by_call: dict[int, int] = {}
    for event in parsed["hardware"]:
        if event["event"] != "issue":
            continue
        call_index = int(event["call_index"])
        first_by_call[call_index] = min(
            int(event["cycle"]), first_by_call.get(call_index, int(event["cycle"]))
        )
    return len(first_by_call) == expected_calls and set(first_by_call.values()) == {
        expected_cycle
    }


def _per_tile_checksum_gate(
    static: dict[str, Any], dynamic: dict[str, Any]
) -> bool:
    def values(parsed: dict[str, Any]) -> dict[tuple[int, int, str], int]:
        return {
            (event["call_index"], event["index"], event["engine"]): event["checksum"]
            for event in parsed["hardware"]
            if event["event"] == "complete"
        }

    static_values = values(static)
    dynamic_values = values(dynamic)
    return bool(static_values) and static_values == dynamic_values


def _summary_matches(
    observed: dict[str, Any],
    compiled: dict[str, Any],
    workload: AgentWorkload,
) -> bool:
    expected = compiled["summary"]
    return (
        observed["programs"] == expected["programs"]
        and observed["calls"] == expected["calls"]
        and observed["llm_calls"] == expected["llm_calls"]
        and observed["tool_calls"] == expected["tool_calls"]
        and observed["launches"] == expected["llm_calls"]
        and observed["descriptors"] == expected["descriptors"]
        and observed["flows"]
        == [expected["reactive_flows"], expected["proactive_flows"]]
        and observed["placements"]
        == [
            expected["hptpe_descriptors"],
            expected["vector_descriptors"],
            expected["data_descriptors"],
        ]
        and observed["me_busy"] == expected["me_busy"]
        and observed["ve_busy"] == expected["ve_busy"]
        and observed["de_busy"] == expected["de_busy"]
        and observed["hptpe_mac_ops"] == expected["hptpe_mac_ops"]
        and observed["workload"] == workload.name
        and observed["workload_digest_hex"] == workload.sha256[:16]
    )


def run_parameterized_system(
    workload: AgentWorkload,
    compiled_path: Path,
    elf_path: Path,
    *,
    run_id: str,
    output_dir: Path,
    component_certificate: Path | None = None,
    timeout_s: float = 300.0,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    workload.hardware.require_installed_profile()
    compiled = json.loads(compiled_path.read_text(encoding="utf-8"))
    if compiled["workload"]["sha256"] != workload.sha256:
        raise ValueError("compiled/workload identity mismatch")
    log_dir = output_dir / "logs"
    with ThreadPoolExecutor(max_workers=2) as pool:
        static_future = pool.submit(
            _run_backend,
            "static",
            elf_path=elf_path,
            log_path=log_dir / "static.log",
            timeout_s=timeout_s,
        )
        dynamic_future = pool.submit(
            _run_backend,
            "dynamic",
            elf_path=elf_path,
            log_path=log_dir / "dynamic.log",
            timeout_s=timeout_s,
        )
        static = static_future.result()
        dynamic = dynamic_future.result()
    static_parsed = static["parsed"]
    dynamic_parsed = dynamic["parsed"]
    static_summary = static_parsed["summary"]
    dynamic_summary = dynamic_parsed["summary"]
    events = expand_trace("static", static_parsed) + expand_trace("dynamic", dynamic_parsed)
    events.sort(key=lambda event: (event["backend"], event["cycle"], event["sequence"]))
    for sequence, event in enumerate(events):
        event["global_sequence"] = sequence
        event["workload"] = workload.name
        event["workload_sha256"] = workload.sha256
    layers = sorted({event["layer"] for event in events})
    speedup = static_summary["backend_cycles"] / dynamic_summary["backend_cycles"]
    installed = _installed_sources()
    same_work_keys = (
        "programs",
        "calls",
        "llm_calls",
        "tool_calls",
        "launches",
        "descriptors",
        "dma_bytes",
        "me_busy",
        "ve_busy",
        "de_busy",
        "hptpe_mac_ops",
        "flows",
        "placements",
        "checksum",
        "app_digest",
        "mir_digest",
        "workload_digest",
    )
    llm_calls = int(compiled["summary"]["llm_calls"])
    gates: dict[str, bool] = {
        "real_rocket_simulators_exit": static["exit_code"]
        == dynamic["exit_code"]
        == 0
        and static_summary["verdict"] == dynamic_summary["verdict"] == "PASS",
        "workload_identity": compiled["workload"]["sha256"]
        == workload.sha256
        == hashlib.sha256(
            json.dumps(
                json.loads(workload.source_path.read_text(encoding="utf-8")),
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            ).encode()
        ).hexdigest(),
        "neutral_xpu_v2_abi": static_summary["abi"]
        == dynamic_summary["abi"]
        == "xpu_v2",
        "manifest_counts_static": _summary_matches(static_summary, compiled, workload),
        "manifest_counts_dynamic": _summary_matches(dynamic_summary, compiled, workload),
        "same_application_and_xpu_work": all(
            static_summary[key] == dynamic_summary[key] for key in same_work_keys
        ),
        "dependencies_static": _dependency_gate(static_parsed["calls"]),
        "dependencies_dynamic": _dependency_gate(dynamic_parsed["calls"]),
        "tile_trace_static": _tile_gate(static_parsed, compiled),
        "tile_trace_dynamic": _tile_gate(dynamic_parsed, compiled),
        "dedicated_hardware_transport": static_parsed["transport"]
        == {"repaired_frames": 0, "complete": True}
        and dynamic_parsed["transport"]
        == {"repaired_frames": 0, "complete": True},
        "per_tile_checksum_identity": _per_tile_checksum_gate(
            static_parsed, dynamic_parsed
        ),
        "dispatch_profile": static_summary["dispatch_latency"] == 0
        and dynamic_summary["dispatch_latency"] == workload.hardware.dispatch_latency
        and _first_issue_gate(static_parsed, expected_calls=llm_calls, expected_cycle=0)
        and _first_issue_gate(
            dynamic_parsed,
            expected_calls=llm_calls,
            expected_cycle=workload.hardware.dispatch_latency,
        ),
        "hptpe_lane_work": static_summary["hptpe_mac_ops"]
        == dynamic_summary["hptpe_mac_ops"]
        == static_summary["me_busy"] * workload.hardware.hptpe_lanes,
        "no_cancel_prefetch_or_atx": static_summary["priority_violations"]
        == dynamic_summary["priority_violations"]
        == 0
        and "ATX" not in static["log"]
        and "ATX" not in dynamic["log"]
        and "PREFETCH" not in static["log"].upper()
        and "PREFETCH" not in dynamic["log"].upper(),
        "trace_layers": layers
        == [
            "agentxpu",
            "application",
            "cpu",
            "dma",
            "framework",
            "hptpe",
            "mllm",
            "software",
            "tisa",
            "ve_de",
            "xpu",
        ],
        "installed_sources_match": all(
            item["source_sha256"] == item["installed_sha256"]
            for item in installed.values()
        ),
    }
    expectations = workload.expectations
    performance_gates: dict[str, bool] = {}
    if expectations.dynamic_faster is not None:
        performance_gates["expected_dynamic_faster"] = (
            dynamic_summary["backend_cycles"] < static_summary["backend_cycles"]
        ) == expectations.dynamic_faster
    if expectations.require_static_overlap is not None:
        performance_gates["expected_static_overlap"] = (
            static_summary["overlap"] > 0
        ) == expectations.require_static_overlap
    if expectations.backend_speedup_range is not None:
        low, high = expectations.backend_speedup_range
        performance_gates["expected_backend_speedup_range"] = low <= speedup <= high
    gates.update(performance_gates)

    component_evidence: dict[str, Any] | None = None
    if component_certificate is not None:
        component_evidence = json.loads(component_certificate.read_text(encoding="utf-8"))
        gates["standalone_components_within_10_percent"] = (
            component_evidence["summary"]["pass"]
            and component_evidence["summary"]["endpoints_passed"] == 68
            and component_evidence["summary"]["max_relative_error"] <= 0.10
        )

    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "parameterized_agent_workload_real_rocket_tisa_hptpe_simulation",
        "project_commit": _git_head(PROJECT_ROOT),
        "chipyard_commit": chipyard_source_identity(CHIPYARD_ROOT)["commit"],
        "workload": workload.to_contract_dict(),
        "compiled_manifest": str(compiled_path),
        "compiled_manifest_sha256": _sha256(compiled_path),
        "elf": str(elf_path),
        "elf_sha256": _sha256(elf_path),
        "static": static,
        "dynamic": dynamic,
        "installed_sources": installed,
        "component_certificate": (
            {
                "path": str(component_certificate),
                "sha256": _sha256(component_certificate),
                "summary": component_evidence["summary"],
            }
            if component_certificate is not None and component_evidence is not None
            else None
        ),
        "trace": {"events": len(events), "layers": layers},
        "performance_expectations": {
            "configured": {
                "dynamic_faster": expectations.dynamic_faster,
                "require_static_overlap": expectations.require_static_overlap,
                "backend_speedup_range": (
                    list(expectations.backend_speedup_range)
                    if expectations.backend_speedup_range is not None
                    else None
                ),
            },
            "gates": performance_gates,
        },
        "derived": {
            "backend_speedup": speedup,
            "system_speedup": static_summary["system_cycles"]
            / dynamic_summary["system_cycles"],
            "end_to_end_speedup": static_summary["cpu_cycles"]
            / dynamic_summary["cpu_cycles"],
            "overlap_added": dynamic_summary["overlap"] - static_summary["overlap"],
            "hptpe_mac_ops": dynamic_summary["hptpe_mac_ops"],
        },
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }
    return result, events


def write_parameterized_system(
    workload: AgentWorkload,
    compiled_path: Path,
    elf_path: Path,
    result_path: Path,
    trace_path: Path,
    *,
    run_id: str,
    output_dir: Path,
    component_certificate: Path | None = None,
    timeout_s: float = 300.0,
) -> dict[str, Any]:
    result, events = run_parameterized_system(
        workload,
        compiled_path,
        elf_path,
        run_id=run_id,
        output_dir=output_dir,
        component_certificate=component_certificate,
        timeout_s=timeout_s,
    )
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with trace_path.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
    return result

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from .paths import chipyard_source_identity, resolve_chipyard_root


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHIPYARD_ROOT = resolve_chipyard_root()
SIM_ROOT = CHIPYARD_ROOT / "sims/verilator"
TRACE_ELF = PROJECT_ROOT / "system_sim/build/software/agentsys-trace-system.riscv"
COMPILED_MANIFEST = PROJECT_ROOT / "artifacts/app_traces/compiled-system-workload-run_021.json"


SUMMARY_RE = re.compile(r"^AGENTSYS_APP_(PASS|FAIL)\s+(.*)$", re.MULTILINE)
CALL_RE = re.compile(r"^AGENTSYS_APP_CALL\s+(.*)$", re.MULTILINE)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_head(path: Path) -> str:
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def _fields(text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for token in text.split():
        key, value = token.split("=", 1)
        result[key] = value
    return result


def parse_application_output(output: str) -> dict[str, Any]:
    summary_match = SUMMARY_RE.search(output)
    if summary_match is None:
        raise ValueError("AGENTSYS_APP summary line not found")
    summary_raw = _fields(summary_match.group(2))
    summary: dict[str, Any] = {"verdict": summary_match.group(1)}
    for key, value in summary_raw.items():
        if key in {"backend"}:
            summary[key] = value
        elif key in {"checksum", "app_digest"}:
            summary[key] = int(value, 16)
            summary[f"{key}_hex"] = value
        else:
            summary[key] = int(value)

    calls: list[dict[str, Any]] = []
    for match in CALL_RE.finditer(output):
        raw = _fields(match.group(1))
        call: dict[str, Any] = {}
        for key, value in raw.items():
            if key in {"program", "call", "kind"}:
                call[key] = value
            elif key == "deps":
                call[key] = int(value, 16)
            else:
                call[key] = int(value)
        calls.append(call)
    if len(calls) != summary["calls"]:
        raise ValueError(f"call records {len(calls)} != summary {summary['calls']}")
    if [call["index"] for call in calls] != list(range(len(calls))):
        raise ValueError("call record indices are not dense and ordered")
    return {"summary": summary, "calls": calls}


def _run_backend(backend: str, *, timeout_s: float) -> dict[str, Any]:
    config = "AgentSysStaticRocketConfig" if backend == "static" else "AgentSysDynamicRocketConfig"
    simulator = SIM_ROOT / f"simulator-chipyard-{config}"
    if not simulator.is_file() or not TRACE_ELF.is_file():
        raise FileNotFoundError(f"missing simulator or trace ELF: {simulator}, {TRACE_ELF}")
    started = time.time()
    process = subprocess.run(
        [str(simulator), str(TRACE_ELF)],
        cwd=SIM_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_s,
        check=False,
    )
    parsed = parse_application_output(process.stdout)
    return {
        "backend": backend,
        "config": config,
        "simulator": str(simulator),
        "simulator_sha256": _sha256(simulator),
        "exit_code": process.returncode,
        "wall_time_s": time.time() - started,
        "parsed": parsed,
        "log": process.stdout,
    }


def expand_system_events(backend: str, calls: list[dict[str, Any]]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []

    def add(cycle: int, layer: str, event: str, call: dict[str, Any], **details: Any) -> None:
        if cycle <= 0:
            return
        events.append(
            {
                "schema_version": 1,
                "backend": backend,
                "cycle": cycle,
                "layer": layer,
                "event": event,
                "program_id": call["program"],
                "call_id": call["call"],
                "call_index": call["index"],
                "priority": call["priority"],
                "details": details,
            }
        )

    for call in calls:
        if call["first"]:
            add(call["release"], "application", "program_start", call)
        add(call["release"], "framework", "call_release", call, deps_mask=call["deps"])
        if call["kind"] == "tool":
            add(call["tool_start"], "cpu", "tool_start", call)
            add(call["tool_end"], "cpu", "tool_complete", call)
        else:
            add(call["lower"], "framework", "mllm_lower", call)
            add(call["config_start"], "software", "config_start", call)
            add(call["config_end"], "software", "config_complete", call)
            add(call["launch"], "cpu", "rocc_launch", call)
            add(call["wait"], "cpu", "rocc_wait_complete", call)
            add(call["xpu"], "xpu", "task_complete", call, cycles=call["xpu_cycles"])
            add(
                call["dma"],
                "dma",
                "transfer_complete",
                call,
                cycles=call["dma_cycles"],
                bytes=call["dma_bytes"],
            )
        add(call["complete"], "framework", "call_complete", call)
        if call["last"]:
            add(call["complete"], "application", "program_complete", call)
    order = {"application": 0, "framework": 1, "software": 2, "cpu": 3, "xpu": 4, "dma": 5}
    events.sort(key=lambda item: (item["cycle"], order[item["layer"]], item["call_index"]))
    for sequence, event in enumerate(events):
        event["sequence"] = sequence
    return events


def _dependency_gate(calls: list[dict[str, Any]]) -> bool:
    complete = {call["index"]: call["complete"] for call in calls}
    for call in calls:
        for dependency in range(len(calls)):
            if call["deps"] & (1 << dependency):
                if complete[dependency] > call["release"]:
                    return False
    return True


def _paper_layer_validation() -> dict[str, Any]:
    files = {
        "application": "artifacts/results/paper-agentix-run_019.json",
        "framework": "artifacts/results/paper-agentxpu-run_019.json",
        "software": "artifacts/results/paper-atx-run_019.json",
        "hardware": "artifacts/results/paper-tisa-run_019.json",
    }
    result: dict[str, Any] = {}
    for layer, relative in files.items():
        path = PROJECT_ROOT / relative
        value = json.loads(path.read_text(encoding="utf-8"))
        result[layer] = {
            "path": relative,
            "paper": value["paper"],
            "endpoints": value["summary"]["endpoints"],
            "max_relative_error": value["summary"]["max_relative_error"],
            "limit": 0.15,
            "pass": value["summary"]["pass"]
            and value["summary"]["max_relative_error"] <= 0.15,
            "sha256": _sha256(path),
        }
    return result


def run_system_trace(*, run_id: str = "run_021", timeout_s: float = 240.0) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    compiled = json.loads(COMPILED_MANIFEST.read_text(encoding="utf-8"))
    with ThreadPoolExecutor(max_workers=2) as pool:
        future_static = pool.submit(_run_backend, "static", timeout_s=timeout_s)
        future_dynamic = pool.submit(_run_backend, "dynamic", timeout_s=timeout_s)
        static = future_static.result()
        dynamic = future_dynamic.result()
    s = static["parsed"]["summary"]
    d = dynamic["parsed"]["summary"]
    static_calls = static["parsed"]["calls"]
    dynamic_calls = dynamic["parsed"]["calls"]
    events = expand_system_events("static", static_calls) + expand_system_events(
        "dynamic", dynamic_calls
    )
    events.sort(key=lambda item: (item["backend"], item["cycle"], item["sequence"]))
    for sequence, event in enumerate(events):
        event["global_sequence"] = sequence
    layers = sorted({event["layer"] for event in events})
    paper_layers = _paper_layer_validation()
    speedup = s["backend_cycles"] / d["backend_cycles"]
    gates = {
        "real_simulators_exit": static["exit_code"] == dynamic["exit_code"] == 0
        and s["verdict"] == d["verdict"] == "PASS",
        "compiled_application_contract": compiled["summary"]
        == {
            "programs": 3,
            "calls": 11,
            "llm_calls": 10,
            "tool_calls": 1,
            "descriptors": 80,
            "dependencies": 6,
            "pass": True,
        },
        "same_application_work": all(
            s[key] == d[key]
            for key in (
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
                "checksum",
                "app_digest",
            )
        ),
        "dependencies_static": _dependency_gate(static_calls),
        "dependencies_dynamic": _dependency_gate(dynamic_calls),
        "priority": s["priority_violations"] == d["priority_violations"] == 0,
        "cpu_xpu_layers": layers
        == ["application", "cpu", "dma", "framework", "software", "xpu"],
        "dynamic_backend_faster": d["backend_cycles"] < s["backend_cycles"],
        "dynamic_system_faster": d["system_cycles"] < s["system_cycles"],
        "dynamic_end_to_end_faster": d["cpu_cycles"] < s["cpu_cycles"],
        "tisa_static_speedup_range": 1.14 <= speedup <= 1.63,
        "paper_layers_within_15pct": all(item["pass"] for item in paper_layers.values()),
        "trace_nonempty": len(events) >= 100,
    }
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "real_rocket_cpu_plus_rocc_xpu_agent_trace_simulation",
        "project_commit": _git_head(PROJECT_ROOT),
        "chipyard_commit": chipyard_source_identity(CHIPYARD_ROOT)["commit"],
        "elf": str(TRACE_ELF),
        "elf_sha256": _sha256(TRACE_ELF),
        "compiled_manifest": str(COMPILED_MANIFEST.relative_to(PROJECT_ROOT)),
        "compiled_manifest_sha256": _sha256(COMPILED_MANIFEST),
        "static": static,
        "dynamic": dynamic,
        "paper_layer_validation": paper_layers,
        "trace": {"events": len(events), "layers": layers},
        "derived": {
            "backend_speedup": speedup,
            "system_speedup": s["system_cycles"] / d["system_cycles"],
            "end_to_end_speedup": s["cpu_cycles"] / d["cpu_cycles"],
            "overlap_added": d["overlap"] - s["overlap"],
        },
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
    }, events


def write_system_trace(result_path: Path, trace_path: Path, *, run_id: str = "run_021") -> dict[str, Any]:
    result, events = run_system_trace(run_id=run_id)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with trace_path.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
    return result

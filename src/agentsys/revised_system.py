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
SIM_ROOT = CHIPYARD_ROOT / "sims" / "verilator"
ELF = PROJECT_ROOT / "system_sim/build/software/agentsys-revised-system.riscv"
COMPILED_MANIFEST = PROJECT_ROOT / "artifacts/app_traces/revised-compiled-workload-run_028.json"
COMPONENT_CERTIFICATE = PROJECT_ROOT / "artifacts/results/revised-components-run_028.json"

SUMMARY_RE = re.compile(r"^AGENTSYS_REVISED_(PASS|FAIL)\s+(.*)$", re.MULTILINE)
CALL_RE = re.compile(r"^AGENTSYS_REVISED_CALL\s+(.*)$", re.MULTILINE)
LAUNCH_RE = re.compile(r"^AGENTSYS_REVISED_LAUNCH\s+(.*)$", re.MULTILINE)
ISSUE_RE = re.compile(r"^AGENTSYS_TISA_ISSUE\s+(.*)$", re.MULTILINE)
COMPLETE_RE = re.compile(r"^AGENTSYS_TISA_COMPLETE\s+(.*)$", re.MULTILINE)
HARDWARE_RE = re.compile(
    r"^(AGENTSYS_REVISED_LAUNCH|AGENTSYS_TISA_ISSUE|AGENTSYS_TISA_COMPLETE|AGENTSYS_REVISED_DONE)\s+(.*)$",
    re.MULTILINE,
)

ISSUE_FIELDS = {"cycle", "index", "engine", "source", "flow", "stage", "placement", "preemptible", "priority", "duration"}
COMPLETE_FIELDS = {"cycle", "index", "engine", "source", "checksum"}


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
        if "=" not in token:
            continue
        key, value = token.split("=", 1)
        result[key] = value
    return result


def _complete_tile_frame(line: str) -> bool:
    if line.startswith("AGENTSYS_TISA_ISSUE"):
        return ISSUE_FIELDS <= _fields(line).keys()
    if line.startswith("AGENTSYS_TISA_COMPLETE"):
        return COMPLETE_FIELDS <= _fields(line).keys()
    return True


def _hardware_frames(output: str) -> tuple[list[str], int]:
    """Recover atomic RTL frames interrupted by the asynchronous target UART.

    Verilator and FESVR write to the same host stream.  A target UART burst can
    appear between two chunks of one ``$display`` call, as observed when an
    ISSUE prefix ended at ``index=7`` and its ``engine=... duration=...`` suffix
    resumed after the target summary.  We join only an incomplete, schema-known
    tile prefix to the first suffix that makes that exact schema complete.
    """

    frames: list[str] = []
    pending: str | None = None
    repairs = 0
    for raw_line in output.splitlines():
        marker_at = [
            position
            for marker in (
                "AGENTSYS_REVISED_LAUNCH",
                "AGENTSYS_TISA_ISSUE",
                "AGENTSYS_TISA_COMPLETE",
                "AGENTSYS_REVISED_DONE",
            )
            if (position := raw_line.find(marker)) >= 0
        ]
        if marker_at:
            fragment = raw_line[min(marker_at) :]
            next_marker = fragment.find("AGENTSYS_", 1)
            if next_marker >= 0:
                fragment = fragment[:next_marker]
            if fragment.startswith(("AGENTSYS_TISA_ISSUE", "AGENTSYS_TISA_COMPLETE")) and not _complete_tile_frame(fragment):
                if pending is not None:
                    raise ValueError(f"unrecoverable overlapping RTL frames: {pending!r}, {fragment!r}")
                pending = fragment
            else:
                frames.append(fragment)
            continue

        if pending is not None:
            candidate = pending + raw_line
            if _complete_tile_frame(candidate):
                frames.append(candidate)
                pending = None
                repairs += 1

    if pending is not None:
        raise ValueError(f"incomplete RTL frame at end of stream: {pending!r}")
    return frames, repairs


def parse_revised_output(output: str) -> dict[str, Any]:
    summary_match = SUMMARY_RE.search(output)
    if summary_match is None:
        raise ValueError("AGENTSYS_REVISED summary line not found")
    raw = _fields(summary_match.group(2))
    summary: dict[str, Any] = {"verdict": summary_match.group(1)}
    for key, value in raw.items():
        if key in {"backend", "abi", "workload"}:
            summary[key] = value
        elif key in {"checksum", "app_digest", "mir_digest", "workload_digest"}:
            summary[key] = int(value, 16)
            summary[f"{key}_hex"] = value
        elif key in {"flows", "placements"}:
            summary[key] = [int(item) for item in value.split("/")]
        else:
            summary[key] = int(value)

    calls: list[dict[str, Any]] = []
    for match in CALL_RE.finditer(output):
        call_raw = _fields(match.group(1))
        call: dict[str, Any] = {}
        for key, value in call_raw.items():
            if key in {"program", "call", "kind", "flow"}:
                call[key] = value
            elif key == "deps":
                call[key] = int(value, 16)
            else:
                call[key] = int(value)
        calls.append(call)
    if len(calls) != summary["calls"]:
        raise ValueError(f"call records {len(calls)} != summary {summary['calls']}")

    hardware_frames, transport_repairs = _hardware_frames(output)
    hardware_text = "\n".join(hardware_frames)
    current_call: int | None = None
    hardware: list[dict[str, Any]] = []
    for match in HARDWARE_RE.finditer(hardware_text):
        kind = match.group(1)
        item_raw = _fields(match.group(2))
        if kind == "AGENTSYS_REVISED_LAUNCH":
            current_call = int(item_raw["call"])
            continue
        if "call" in item_raw:
            current_call = int(item_raw["call"])
        if kind not in {"AGENTSYS_TISA_ISSUE", "AGENTSYS_TISA_COMPLETE"}:
            continue
        if current_call is None:
            raise ValueError("tile event precedes revised launch marker")
        event: dict[str, Any] = {
            "event": "issue" if kind.endswith("ISSUE") else "complete",
            "call_index": current_call,
        }
        allowed_keys = (
            ISSUE_FIELDS
            if kind == "AGENTSYS_TISA_ISSUE"
            else COMPLETE_FIELDS
        )
        for key, value in item_raw.items():
            # Verilator's RTL $display stream and the target UART share stdout.
            # A UART fragment can therefore land on the same physical line as a
            # tile event.  Parse the event schema, not unrelated trailing fields.
            if key not in allowed_keys:
                continue
            if key == "engine":
                event[key] = value
            elif key == "checksum":
                event[key] = int(value, 16)
                event["checksum_hex"] = value
            else:
                event[key] = int(value)
        hardware.append(event)
    return {
        "summary": summary,
        "calls": calls,
        "hardware": hardware,
        "transport": {"repaired_frames": transport_repairs, "complete": True},
    }


def _run_backend(backend: str, *, timeout_s: float, run_id: str = "adhoc") -> dict[str, Any]:
    config = (
        "AgentSysRevisedStaticRocketConfig"
        if backend == "static"
        else "AgentSysRevisedDynamicRocketConfig"
    )
    simulator = SIM_ROOT / f"simulator-chipyard-{config}"
    if not simulator.is_file() or not ELF.is_file():
        raise FileNotFoundError(f"missing simulator or revised ELF: {simulator}, {ELF}")
    started = time.time()
    proc = subprocess.run(
        [str(simulator), str(ELF)],
        cwd=SIM_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_s,
        check=False,
    )
    raw_log = PROJECT_ROOT / "artifacts/logs" / f"revised-system-{backend}-{run_id}.log"
    raw_log.parent.mkdir(parents=True, exist_ok=True)
    raw_log.write_text(proc.stdout, encoding="utf-8")
    return {
        "backend": backend,
        "config": config,
        "simulator": str(simulator),
        "simulator_sha256": _sha256(simulator),
        "exit_code": proc.returncode,
        "wall_time_s": time.time() - started,
        "raw_log": str(raw_log.relative_to(PROJECT_ROOT)),
        "parsed": parse_revised_output(proc.stdout),
        "log": proc.stdout,
    }


def _dependency_gate(calls: list[dict[str, Any]]) -> bool:
    complete = {call["index"]: call["complete"] for call in calls}
    for call in calls:
        for dependency in range(len(calls)):
            if call["deps"] & (1 << dependency):
                if complete[dependency] > call["release"]:
                    return False
    return True


def _tile_gate(parsed: dict[str, Any], compiled: dict[str, Any]) -> bool:
    expected_calls = {call["index"]: call for call in compiled["hardware_calls"] if call["kind"] == "llm"}
    issues = [event for event in parsed["hardware"] if event["event"] == "issue"]
    completes = [event for event in parsed["hardware"] if event["event"] == "complete"]
    if len(issues) != 80 or len(completes) != 80:
        return False
    issue_keys = {(event["call_index"], event["index"], event["engine"]) for event in issues}
    complete_keys = {(event["call_index"], event["index"], event["engine"]) for event in completes}
    if issue_keys != complete_keys or len(issue_keys) != 80:
        return False
    for event in issues:
        descriptor = expected_calls[event["call_index"]]["descriptors"][event["index"]]
        if (
            event["engine"] != descriptor["engine"]
            or event["source"] != descriptor["source_index"]
            or event["flow"] != descriptor["flow_code"]
            or event["stage"] != descriptor["stage_code"]
            or event["placement"] != descriptor["placement_code"]
            or event["preemptible"] != descriptor["preemptible"]
            or event["priority"] != expected_calls[event["call_index"]]["priority"]
            or event["duration"] != descriptor["duration"]
        ):
            return False
    return True


def _first_issue_gate(parsed: dict[str, Any], expected_cycle: int) -> bool:
    first_by_call: dict[int, int] = {}
    for event in parsed["hardware"]:
        if event["event"] != "issue":
            continue
        first_by_call[event["call_index"]] = min(
            event["cycle"], first_by_call.get(event["call_index"], event["cycle"])
        )
    return len(first_by_call) == 10 and set(first_by_call.values()) == {expected_cycle}


def expand_trace(backend: str, parsed: dict[str, Any]) -> list[dict[str, Any]]:
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

    calls_by_index = {call["index"]: call for call in parsed["calls"]}
    for call in parsed["calls"]:
        if call["first"]:
            add(call["release"], "application", "program_start", call)
        add(call["release"], "framework", "agentix_call_release", call, deps_mask=call["deps"])
        if call["kind"] == "tool":
            add(call["tool_start"], "cpu", "tool_start", call)
            add(call["tool_end"], "cpu", "tool_complete", call)
        else:
            add(call["mllm"], "mllm", "native_operator_lower", call)
            add(call["agentxpu"], "agentxpu", "flow_place", call, flow=call["flow"])
            add(call["config_start"], "software", "xpu_config_start", call)
            add(call["config_end"], "software", "xpu_config_complete", call)
            add(call["launch"], "cpu", "xpu_launch", call)
            add(call["wait"], "cpu", "xpu_wait_complete", call)
            add(call["xpu"], "xpu", "launch_complete", call, cycles=call["xpu_cycles"])
            add(call["dma"], "dma", "transfer_complete", call, cycles=call["dma_cycles"], bytes=call["dma_bytes"])
        add(call["complete"], "framework", "agentix_call_complete", call)
        if call["last"]:
            add(call["complete"], "application", "program_complete", call)

    for tile in parsed["hardware"]:
        call = calls_by_index[tile["call_index"]]
        absolute_cycle = call["launch"] + tile["cycle"]
        add(
            absolute_cycle,
            "tisa",
            f"tile_{tile['event']}",
            call,
            local_cycle=tile["cycle"],
            descriptor_index=tile["index"],
            engine=tile["engine"],
            source_op=tile["source"],
            placement=tile.get("placement"),
            stage=tile.get("stage"),
            flow=tile.get("flow"),
        )
        if tile["engine"] == "me":
            add(absolute_cycle, "hptpe", f"pe_array_{tile['event']}", call, descriptor_index=tile["index"], source_op=tile["source"])
        else:
            add(absolute_cycle, "ve_de", f"{tile['engine']}_{tile['event']}", call, descriptor_index=tile["index"], source_op=tile["source"])
    events.sort(key=lambda event: (event["cycle"], event["layer"], event["call_index"]))
    for sequence, event in enumerate(events):
        event["sequence"] = sequence
    return events


def _installed_sources() -> dict[str, Any]:
    vsrc = CHIPYARD_ROOT / "generators/chipyard/src/main/resources/vsrc"
    scala = CHIPYARD_ROOT / "generators/chipyard/src/main/scala"
    pairs = {
        "scala": (PROJECT_ROOT / "system_sim/chipyard/AgentSysRevisedRoCC.scala", scala / "AgentSysRevisedRoCC.scala"),
        "engines": (PROJECT_ROOT / "rtl/agentsys/agentsys_revised_engines.sv", vsrc / "agentsys_revised_engines.sv"),
        "scheduler": (PROJECT_ROOT / "rtl/agentsys/agentsys_tisa_scheduler.sv", vsrc / "agentsys_tisa_scheduler.sv"),
        "controller": (PROJECT_ROOT / "rtl/agentsys/agentsys_revised_rocc_controller.sv", vsrc / "agentsys_revised_rocc_controller.sv"),
    }
    result = {}
    for name, (source, installed) in pairs.items():
        result[name] = {
            "source": str(source),
            "installed": str(installed),
            "source_sha256": _sha256(source),
            "installed_sha256": _sha256(installed),
        }
    return result


def run_revised_system(*, run_id: str = "run_028", timeout_s: float = 300.0) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    compiled = json.loads(COMPILED_MANIFEST.read_text(encoding="utf-8"))
    components = json.loads(COMPONENT_CERTIFICATE.read_text(encoding="utf-8"))
    with ThreadPoolExecutor(max_workers=2) as pool:
        static_future = pool.submit(_run_backend, "static", timeout_s=timeout_s, run_id=run_id)
        dynamic_future = pool.submit(_run_backend, "dynamic", timeout_s=timeout_s, run_id=run_id)
        static = static_future.result()
        dynamic = dynamic_future.result()
    s = static["parsed"]["summary"]
    d = dynamic["parsed"]["summary"]
    static_calls = static["parsed"]["calls"]
    dynamic_calls = dynamic["parsed"]["calls"]
    installed = _installed_sources()
    events = expand_trace("static", static["parsed"]) + expand_trace("dynamic", dynamic["parsed"])
    events.sort(key=lambda event: (event["backend"], event["cycle"], event["sequence"]))
    for sequence, event in enumerate(events):
        event["global_sequence"] = sequence
    layers = sorted({event["layer"] for event in events})
    speedup = s["backend_cycles"] / d["backend_cycles"]
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
    )
    gates = {
        "real_rocket_simulators_exit": static["exit_code"] == dynamic["exit_code"] == 0 and s["verdict"] == d["verdict"] == "PASS",
        "neutral_xpu_v2_abi": s["abi"] == d["abi"] == "xpu_v2",
        "compiled_upstream_mllm_contract": compiled["summary"]["pass"] and ".references/mllm/" in compiled["mllm"]["mir"],
        "same_application_and_xpu_work": all(s[key] == d[key] for key in same_work_keys),
        "agentxpu_flows_and_placements": s["flows"] == d["flows"] == [2, 8] and s["placements"] == d["placements"] == [30, 30, 20],
        "hptpe_256_lane_work": s["hptpe_mac_ops"] == d["hptpe_mac_ops"] == s["me_busy"] * 256,
        "dependencies_static": _dependency_gate(static_calls),
        "dependencies_dynamic": _dependency_gate(dynamic_calls),
        "tile_trace_static": _tile_gate(static["parsed"], compiled),
        "tile_trace_dynamic": _tile_gate(dynamic["parsed"], compiled),
        "hardware_transport_complete": static["parsed"]["transport"]["complete"] and dynamic["parsed"]["transport"]["complete"],
        "seven_cycle_per_unit_dispatch": s["dispatch_latency"] == 0 and d["dispatch_latency"] == 7 and _first_issue_gate(static["parsed"], 0) and _first_issue_gate(dynamic["parsed"], 7),
        "no_cancel_prefetch_or_atx": s["priority_violations"] == d["priority_violations"] == 0 and "ATX" not in static["log"] and "ATX" not in dynamic["log"] and "PREFETCH" not in static["log"].upper() and "PREFETCH" not in dynamic["log"].upper(),
        "strong_static_and_dynamic_overlap": 0 < s["overlap"] < d["overlap"],
        "dynamic_backend_faster": d["backend_cycles"] < s["backend_cycles"],
        "dynamic_system_faster": d["system_cycles"] < s["system_cycles"],
        "tisa_speedup_range": 1.14 <= speedup <= 1.63,
        "trace_layers": layers == ["agentxpu", "application", "cpu", "dma", "framework", "hptpe", "mllm", "software", "tisa", "ve_de", "xpu"],
        "standalone_components_68": components["summary"]["pass"] and components["summary"]["endpoints_passed"] == 68 and components["summary"]["max_relative_error"] <= 0.15,
        "installed_sources_match": all(item["source_sha256"] == item["installed_sha256"] for item in installed.values()),
    }
    result = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "real_ordinary_rocket_plus_tisa_hptpe_agent_system_trace",
        "project_commit": _git_head(PROJECT_ROOT),
        "chipyard_commit": chipyard_source_identity(CHIPYARD_ROOT)["commit"],
        "elf": str(ELF),
        "elf_sha256": _sha256(ELF),
        "compiled_manifest": str(COMPILED_MANIFEST.relative_to(PROJECT_ROOT)),
        "compiled_manifest_sha256": _sha256(COMPILED_MANIFEST),
        "component_certificate": str(COMPONENT_CERTIFICATE.relative_to(PROJECT_ROOT)),
        "component_certificate_sha256": _sha256(COMPONENT_CERTIFICATE),
        "static": static,
        "dynamic": dynamic,
        "installed_sources": installed,
        "trace": {"events": len(events), "layers": layers},
        "derived": {
            "backend_speedup": speedup,
            "system_speedup": s["system_cycles"] / d["system_cycles"],
            "end_to_end_speedup": s["cpu_cycles"] / d["cpu_cycles"],
            "overlap_added": d["overlap"] - s["overlap"],
            "hptpe_mac_ops": d["hptpe_mac_ops"],
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


def write_revised_system(result_path: Path, trace_path: Path, *, run_id: str = "run_028") -> dict[str, Any]:
    result, events = run_revised_system(run_id=run_id)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    trace_path.parent.mkdir(parents=True, exist_ok=True)
    with trace_path.open("w", encoding="utf-8") as handle:
        for event in events:
            handle.write(json.dumps(event, sort_keys=True) + "\n")
    return result

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .agentix import AgentixPolicy, CallSpec
from .agentxpu import XPUConfig
from .model import Priority


PROJECT_ROOT = Path(__file__).resolve().parents[2]
WORKLOAD_NAME_RE = re.compile(r"^[a-z][a-z0-9_-]{0,63}$")
PRIORITIES = {
    "reactive": Priority.REACTIVE,
    "normal": Priority.NORMAL,
    "proactive": Priority.PROACTIVE,
}


@dataclass(frozen=True, slots=True)
class WorkloadProgram:
    program_id: str
    priority: Priority
    arrival: int


@dataclass(frozen=True, slots=True)
class WorkloadCall:
    call_id: str
    program_id: str
    kind: str
    duration: int
    deps: tuple[str, ...]
    external_delay: int
    thread_id: str
    input_tokens: int
    output_tokens: int
    model_profile: str | None
    tool_kind: str | None
    tool_cycles: int


@dataclass(frozen=True, slots=True)
class WorkloadModel:
    model_id: str
    framework_mir: Path
    hardware_mir: Path
    selected_source_indices: tuple[int, ...]
    duration_divisors: Mapping[str, float]
    stages: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class WorkloadHardware:
    profile: str
    tisa_window: int
    dispatch_latency: int
    hptpe_rows: int
    hptpe_cols: int
    input_beats: int
    output_beats: int

    @property
    def hptpe_lanes(self) -> int:
        return self.hptpe_rows * self.hptpe_cols

    def require_installed_profile(self) -> None:
        expected = {
            "profile": "rocket_tisa8_hptpe16x16",
            "tisa_window": 8,
            "dispatch_latency": 7,
            "hptpe_rows": 16,
            "hptpe_cols": 16,
        }
        observed = {
            "profile": self.profile,
            "tisa_window": self.tisa_window,
            "dispatch_latency": self.dispatch_latency,
            "hptpe_rows": self.hptpe_rows,
            "hptpe_cols": self.hptpe_cols,
        }
        if observed != expected:
            raise ValueError(
                "workload hardware profile is not installed; rebuild a matching "
                f"Chipyard profile: expected={expected}, observed={observed}"
            )


@dataclass(frozen=True, slots=True)
class WorkloadExpectations:
    dynamic_faster: bool | None
    require_static_overlap: bool | None
    backend_speedup_range: tuple[float, float] | None


@dataclass(frozen=True, slots=True)
class AgentWorkload:
    schema_version: int
    name: str
    description: str
    source_path: Path
    sha256: str
    agentix_policy: AgentixPolicy
    agentix_batch_size: int
    agentxpu_config: XPUConfig
    programs: tuple[WorkloadProgram, ...]
    calls: tuple[WorkloadCall, ...]
    models: tuple[WorkloadModel, ...]
    hardware: WorkloadHardware
    expectations: WorkloadExpectations

    @property
    def program_priorities(self) -> dict[str, Priority]:
        return {program.program_id: program.priority for program in self.programs}

    @property
    def program_codes(self) -> dict[str, int]:
        return {program.program_id: index for index, program in enumerate(self.programs)}

    @property
    def models_by_id(self) -> dict[str, WorkloadModel]:
        return {model.model_id: model for model in self.models}

    def call_specs(self) -> tuple[CallSpec, ...]:
        arrivals = {program.program_id: program.arrival for program in self.programs}
        return tuple(
            CallSpec(
                call.call_id,
                call.program_id,
                call.duration,
                deps=call.deps,
                program_arrival=arrivals[call.program_id],
                external_delay=call.external_delay,
                thread_id=call.thread_id,
            )
            for call in self.calls
        )

    def to_contract_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "sha256": self.sha256,
            "source": str(self.source_path),
            "agentix": {
                "policy": self.agentix_policy.value,
                "batch_size": self.agentix_batch_size,
            },
            "agentxpu": {
                "heg_prefill_chunk_tokens": self.agentxpu_config.heg_prefill_chunk_tokens,
                "max_reactive_decode_batch": self.agentxpu_config.max_reactive_decode_batch,
                "max_decode_batch": self.agentxpu_config.max_decode_batch,
                "heg_igpu_prefill_share": self.agentxpu_config.heg_igpu_prefill_share,
            },
            "hardware": {
                "profile": self.hardware.profile,
                "tisa_window": self.hardware.tisa_window,
                "dispatch_latency": self.hardware.dispatch_latency,
                "hptpe_rows": self.hardware.hptpe_rows,
                "hptpe_cols": self.hardware.hptpe_cols,
                "input_beats": self.hardware.input_beats,
                "output_beats": self.hardware.output_beats,
            },
            "summary": {
                "programs": len(self.programs),
                "calls": len(self.calls),
                "llm_calls": sum(call.kind == "llm" for call in self.calls),
                "tool_calls": sum(call.kind == "tool" for call in self.calls),
                "models": len(self.models),
            },
        }


def _mapping(value: Any, context: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{context} must be an object")
    return value


def _positive_int(value: Any, context: str, *, maximum: int | None = None) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{context} must be a positive integer")
    if maximum is not None and value > maximum:
        raise ValueError(f"{context} must be <= {maximum}")
    return value


def _nonnegative_int(value: Any, context: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{context} must be a non-negative integer")
    return value


def _project_path(value: Any, context: str) -> Path:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{context} must be a path string")
    path = Path(value)
    path = path if path.is_absolute() else PROJECT_ROOT / path
    if not path.is_file():
        raise FileNotFoundError(f"{context}: {path}")
    return path.resolve()


def _validate_dag(calls: tuple[WorkloadCall, ...]) -> None:
    by_id = {call.call_id: call for call in calls}
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(call_id: str) -> None:
        if call_id in visited:
            return
        if call_id in visiting:
            raise ValueError("workload call graph contains a cycle")
        visiting.add(call_id)
        for dependency in by_id[call_id].deps:
            visit(dependency)
        visiting.remove(call_id)
        visited.add(call_id)

    for call in calls:
        visit(call.call_id)


def _parse_expectations(value: Any) -> WorkloadExpectations:
    data = _mapping(value or {}, "expectations")
    dynamic_faster = data.get("dynamic_faster")
    static_overlap = data.get("require_static_overlap")
    if dynamic_faster is not None and not isinstance(dynamic_faster, bool):
        raise ValueError("expectations.dynamic_faster must be boolean")
    if static_overlap is not None and not isinstance(static_overlap, bool):
        raise ValueError("expectations.require_static_overlap must be boolean")
    speedup = data.get("backend_speedup_range")
    parsed_speedup: tuple[float, float] | None = None
    if speedup is not None:
        if (
            not isinstance(speedup, list)
            or len(speedup) != 2
            or not all(isinstance(item, (int, float)) and not isinstance(item, bool) for item in speedup)
        ):
            raise ValueError("expectations.backend_speedup_range must be [min, max]")
        parsed_speedup = (float(speedup[0]), float(speedup[1]))
        if parsed_speedup[0] <= 0 or parsed_speedup[0] > parsed_speedup[1]:
            raise ValueError("invalid backend speedup range")
    return WorkloadExpectations(dynamic_faster, static_overlap, parsed_speedup)


def load_agent_workload(path: Path) -> AgentWorkload:
    source_path = path.resolve()
    raw = json.loads(source_path.read_text(encoding="utf-8"))
    data = _mapping(raw, "workload")
    if data.get("schema_version") != 1:
        raise ValueError("unsupported workload schema_version")
    name = data.get("name")
    if not isinstance(name, str) or WORKLOAD_NAME_RE.fullmatch(name) is None:
        raise ValueError("workload.name must match [a-z][a-z0-9_-]{0,63}")
    description = data.get("description", "")
    if not isinstance(description, str):
        raise ValueError("workload.description must be a string")
    canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    workload_sha = hashlib.sha256(canonical).hexdigest()

    agentix = _mapping(data.get("agentix", {}), "agentix")
    try:
        agentix_policy = AgentixPolicy(agentix.get("policy", "atlas"))
    except ValueError as error:
        raise ValueError("agentix.policy must be fcfs/mlfq/plas/atlas") from error
    agentix_batch = _positive_int(agentix.get("batch_size", 3), "agentix.batch_size")

    agentxpu_values = dict(_mapping(data.get("agentxpu", {}), "agentxpu"))
    allowed_xpu = {
        "heg_prefill_chunk_tokens",
        "max_reactive_decode_batch",
        "max_decode_batch",
        "heg_igpu_prefill_share",
    }
    unknown_xpu = set(agentxpu_values) - allowed_xpu
    if unknown_xpu:
        raise ValueError(f"unknown agentxpu parameters: {sorted(unknown_xpu)}")
    agentxpu_config = XPUConfig(**agentxpu_values)

    program_values = data.get("programs")
    if not isinstance(program_values, list) or not 1 <= len(program_values) <= 63:
        raise ValueError("programs must contain 1..63 entries")
    programs: list[WorkloadProgram] = []
    for index, item in enumerate(program_values):
        program = _mapping(item, f"programs[{index}]")
        program_id = program.get("id")
        if not isinstance(program_id, str) or not program_id:
            raise ValueError(f"programs[{index}].id must be non-empty")
        priority_name = program.get("priority", "normal")
        if priority_name not in PRIORITIES:
            raise ValueError(f"unknown priority for program {program_id}: {priority_name}")
        programs.append(
            WorkloadProgram(
                program_id,
                PRIORITIES[priority_name],
                _nonnegative_int(program.get("arrival", 0), f"program {program_id} arrival"),
            )
        )
    program_ids = [program.program_id for program in programs]
    if len(program_ids) != len(set(program_ids)):
        raise ValueError("program ids must be unique")

    model_values = data.get("models", [])
    if not isinstance(model_values, list):
        raise ValueError("models must be an array")
    models: list[WorkloadModel] = []
    for index, item in enumerate(model_values):
        model = _mapping(item, f"models[{index}]")
        model_id = model.get("id")
        if not isinstance(model_id, str) or not model_id:
            raise ValueError(f"models[{index}].id must be non-empty")
        selected_raw = model.get("selected_source_indices")
        if not isinstance(selected_raw, list) or not 1 <= len(selected_raw) <= 8:
            raise ValueError(f"model {model_id} must select 1..8 source operators")
        if not all(isinstance(value, int) and value >= 0 for value in selected_raw):
            raise ValueError(f"model {model_id} operator indices must be non-negative integers")
        selected = tuple(selected_raw)
        if len(selected) != len(set(selected)):
            raise ValueError(f"model {model_id} operator indices must be unique")
        divisors_raw = _mapping(model.get("duration_divisors", {}), f"model {model_id} divisors")
        divisors = {engine: float(divisors_raw.get(engine, 12.8)) for engine in ("me", "ve", "de")}
        if any(value <= 0 for value in divisors.values()):
            raise ValueError(f"model {model_id} duration divisors must be positive")
        stages_raw = model.get("stages", [0] * max(0, len(selected) - 2) + [1] * min(2, len(selected)))
        if (
            not isinstance(stages_raw, list)
            or len(stages_raw) != len(selected)
            or not all(isinstance(value, int) and 0 <= value <= 255 for value in stages_raw)
        ):
            raise ValueError(f"model {model_id} stages must match selected operators")
        models.append(
            WorkloadModel(
                model_id,
                _project_path(model.get("framework_mir"), f"model {model_id} framework_mir"),
                _project_path(model.get("hardware_mir"), f"model {model_id} hardware_mir"),
                selected,
                divisors,
                tuple(stages_raw),
            )
        )
    model_ids = [model.model_id for model in models]
    if len(model_ids) != len(set(model_ids)):
        raise ValueError("model ids must be unique")

    call_values = data.get("calls")
    if not isinstance(call_values, list) or not 1 <= len(call_values) <= 63:
        raise ValueError("calls must contain 1..63 entries")
    calls: list[WorkloadCall] = []
    for index, item in enumerate(call_values):
        call = _mapping(item, f"calls[{index}]")
        call_id = call.get("id")
        program_id = call.get("program")
        kind = call.get("kind", "llm")
        if not isinstance(call_id, str) or not call_id:
            raise ValueError(f"calls[{index}].id must be non-empty")
        if program_id not in program_ids:
            raise ValueError(f"call {call_id} references unknown program {program_id}")
        if kind not in {"llm", "tool"}:
            raise ValueError(f"call {call_id} kind must be llm/tool")
        deps_raw = call.get("deps", [])
        if not isinstance(deps_raw, list) or not all(isinstance(dep, str) for dep in deps_raw):
            raise ValueError(f"call {call_id} deps must be string array")
        model_profile = call.get("model")
        tool_kind = call.get("tool")
        if kind == "llm" and model_profile not in model_ids:
            raise ValueError(f"LLM call {call_id} references unknown model {model_profile}")
        if kind == "tool" and (not isinstance(tool_kind, str) or not tool_kind):
            raise ValueError(f"tool call {call_id} requires tool name")
        calls.append(
            WorkloadCall(
                call_id,
                str(program_id),
                kind,
                _positive_int(call.get("duration"), f"call {call_id} duration"),
                tuple(deps_raw),
                _nonnegative_int(call.get("external_delay", 0), f"call {call_id} external_delay"),
                str(call.get("thread", "main")),
                _positive_int(call.get("input_tokens", 1), f"call {call_id} input_tokens"),
                _positive_int(call.get("output_tokens", 1), f"call {call_id} output_tokens"),
                str(model_profile) if model_profile is not None else None,
                str(tool_kind) if tool_kind is not None else None,
                _positive_int(call.get("tool_cycles", 1), f"call {call_id} tool_cycles")
                if kind == "tool"
                else 0,
            )
        )
    call_ids = [call.call_id for call in calls]
    if len(call_ids) != len(set(call_ids)):
        raise ValueError("call ids must be unique")
    known_calls = set(call_ids)
    for call in calls:
        missing = set(call.deps) - known_calls
        if missing:
            raise ValueError(f"call {call.call_id} has missing deps: {sorted(missing)}")
        if call.call_id in call.deps:
            raise ValueError(f"call {call.call_id} cannot depend on itself")
    if set(program_ids) != {call.program_id for call in calls}:
        raise ValueError("every program must own at least one call")
    _validate_dag(tuple(calls))

    hardware_data = _mapping(data.get("hardware", {}), "hardware")
    hardware = WorkloadHardware(
        str(hardware_data.get("profile", "rocket_tisa8_hptpe16x16")),
        _positive_int(hardware_data.get("tisa_window", 8), "hardware.tisa_window", maximum=8),
        _nonnegative_int(hardware_data.get("dispatch_latency", 7), "hardware.dispatch_latency"),
        _positive_int(hardware_data.get("hptpe_rows", 16), "hardware.hptpe_rows"),
        _positive_int(hardware_data.get("hptpe_cols", 16), "hardware.hptpe_cols"),
        _positive_int(hardware_data.get("input_beats", 8), "hardware.input_beats", maximum=255),
        _positive_int(hardware_data.get("output_beats", 4), "hardware.output_beats", maximum=255),
    )

    return AgentWorkload(
        1,
        name,
        description,
        source_path,
        workload_sha,
        agentix_policy,
        agentix_batch,
        agentxpu_config,
        tuple(programs),
        tuple(calls),
        tuple(models),
        hardware,
        _parse_expectations(data.get("expectations")),
    )

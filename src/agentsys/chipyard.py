from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHIPYARD_ROOT = Path("/root/chipyard")
SIM_ROOT = CHIPYARD_ROOT / "sims" / "verilator"
ELF = PROJECT_ROOT / "system_sim" / "build" / "software" / "agentsys-system.riscv"


RESULT_RE = re.compile(r"^AGENTSYS_ELF_(PASS|FAIL)\s+(.*)$", re.MULTILINE)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_head(path: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()


def parse_elf_result(output: str) -> dict[str, Any]:
    match = RESULT_RE.search(output)
    if match is None:
        raise ValueError("AgentSys ELF result line not found")
    fields: dict[str, Any] = {"verdict": match.group(1)}
    for token in match.group(2).split():
        key, value = token.split("=", 1)
        if key in {"backend"}:
            fields[key] = value
        elif key == "checksum":
            fields[key] = int(value, 16)
            fields["checksum_hex"] = value
        elif key == "engine_issues":
            fields[key] = [int(item) for item in value.split("/")]
        elif key == "prefetch":
            hit, requested = value.split("/")
            fields["prefetch_hits"] = int(hit)
            fields["prefetch_requests"] = int(requested)
        else:
            fields[key] = int(value)
    return fields


def _run_backend(backend: str, *, timeout_s: float) -> dict[str, Any]:
    config = "AgentSysStaticRocketConfig" if backend == "static" else "AgentSysDynamicRocketConfig"
    simulator = SIM_ROOT / f"simulator-chipyard-{config}"
    if not simulator.is_file():
        raise FileNotFoundError(f"missing simulator: {simulator}")
    started = time.time()
    process = subprocess.run(
        [str(simulator), str(ELF)],
        cwd=SIM_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout_s,
        check=False,
    )
    parsed = parse_elf_result(process.stdout)
    return {
        "config": config,
        "simulator": str(simulator),
        "simulator_sha256": sha256(simulator),
        "exit_code": process.returncode,
        "wall_time_s": time.time() - started,
        "parsed": parsed,
        "log": process.stdout,
    }


def _check(name: str, condition: bool, details: Any) -> dict[str, Any]:
    return {"gate": name, "pass": bool(condition), "details": details}


def run_chipyard_audit(*, run_id: str = "run_003", timeout_s: float = 180.0) -> dict[str, Any]:
    if not ELF.is_file():
        raise FileNotFoundError(f"missing ELF: {ELF}")
    static = _run_backend("static", timeout_s=timeout_s)
    dynamic = _run_backend("dynamic", timeout_s=timeout_s)
    s = static["parsed"]
    d = dynamic["parsed"]

    source_install_pairs = {
        "scala": (
            PROJECT_ROOT / "system_sim/chipyard/AgentSysRoCC.scala",
            CHIPYARD_ROOT / "generators/chipyard/src/main/scala/AgentSysRoCC.scala",
        ),
        "engines": (
            PROJECT_ROOT / "rtl/agentsys/agentsys_engines.sv",
            CHIPYARD_ROOT / "generators/chipyard/src/main/resources/vsrc/agentsys_engines.sv",
        ),
        "scheduler": (
            PROJECT_ROOT / "rtl/agentsys/agentsys_tisa_scheduler.sv",
            CHIPYARD_ROOT
            / "generators/chipyard/src/main/resources/vsrc/agentsys_tisa_scheduler.sv",
        ),
        "controller": (
            PROJECT_ROOT / "rtl/agentsys/agentsys_rocc_controller.sv",
            CHIPYARD_ROOT
            / "generators/chipyard/src/main/resources/vsrc/agentsys_rocc_controller.sv",
        ),
    }
    installed_hashes = {
        name: {
            "source": str(source),
            "installed": str(installed),
            "source_sha256": sha256(source),
            "installed_sha256": sha256(installed),
        }
        for name, (source, installed) in source_install_pairs.items()
    }

    gates = [
        _check("static_exit", static["exit_code"] == 0 and s["verdict"] == "PASS", s),
        _check("dynamic_exit", dynamic["exit_code"] == 0 and d["verdict"] == "PASS", d),
        _check("backend_identity", s["backend"] == "static" and d["backend"] == "dynamic", [s["backend"], d["backend"]]),
        _check("submitted_conservation_static", s["submitted"] == s["completed"] + s["canceled"], [s["submitted"], s["completed"], s["canceled"]]),
        _check("submitted_conservation_dynamic", d["submitted"] == d["completed"] + d["canceled"], [d["submitted"], d["completed"], d["canceled"]]),
        _check("issued_completion_static", s["issued"] == s["completed"], [s["issued"], s["completed"]]),
        _check("issued_completion_dynamic", d["issued"] == d["completed"], [d["issued"], d["completed"]]),
        _check("engine_issue_conservation_static", sum(s["engine_issues"]) == s["issued"], [s["engine_issues"], s["issued"]]),
        _check("engine_issue_conservation_dynamic", sum(d["engine_issues"]) == d["issued"], [d["engine_issues"], d["issued"]]),
        _check("same_logical_work", s["engine_issues"] == d["engine_issues"] and [s["me_busy"], s["ve_busy"], s["de_busy"]] == [d["me_busy"], d["ve_busy"], d["de_busy"]], {"static": s["engine_issues"], "dynamic": d["engine_issues"]}),
        _check("same_dma_and_checksum", s["dma_bytes"] == d["dma_bytes"] == 96 and s["checksum"] == d["checksum"], {"dma": [s["dma_bytes"], d["dma_bytes"]], "checksum": [s["checksum_hex"], d["checksum_hex"]]}),
        _check("prefetch", s["prefetch_hits"] == s["prefetch_requests"] == 1 and d["prefetch_hits"] == d["prefetch_requests"] == 1, {"static": [s["prefetch_hits"], s["prefetch_requests"]], "dynamic": [d["prefetch_hits"], d["prefetch_requests"]]}),
        _check("priority", s["priority_violations"] == d["priority_violations"] == 0, [s["priority_violations"], d["priority_violations"]]),
        _check("dynamic_overlap", s["pair_overlap"] == 0 and d["pair_overlap"] > 0, [s["pair_overlap"], d["pair_overlap"]]),
        _check("dynamic_kernel_speedup", d["kernel"] < s["kernel"], [s["kernel"], d["kernel"]]),
        _check("dynamic_system_speedup", d["system"] < s["system"], [s["system"], d["system"]]),
        _check("installed_sources_match", all(value["source_sha256"] == value["installed_sha256"] for value in installed_hashes.values()), installed_hashes),
    ]
    failures = [gate for gate in gates if not gate["pass"]]
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "real_chipyard_rocket_verilator_functional_system_evidence",
        "chipyard_commit": git_head(CHIPYARD_ROOT),
        "project_commit": git_head(PROJECT_ROOT),
        "elf": str(ELF),
        "elf_sha256": sha256(ELF),
        "static": static,
        "dynamic": dynamic,
        "derived": {
            "kernel_speedup": s["kernel"] / d["kernel"],
            "system_speedup": s["system"] / d["system"],
            "host_launch_wait_speedup": s["host_launch_wait"] / d["host_launch_wait"],
            "overlap_cycles_added": d["pair_overlap"] - s["pair_overlap"],
        },
        "installed_hashes": installed_hashes,
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": len(gates) - len(failures),
            "failing": len(failures),
            "pass": not failures,
        },
    }


def write_chipyard_audit(path: Path, *, run_id: str = "run_003") -> dict[str, Any]:
    result = run_chipyard_audit(run_id=run_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


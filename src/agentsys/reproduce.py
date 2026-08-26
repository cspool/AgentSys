from __future__ import annotations

import argparse
import json
import subprocess
import time
from pathlib import Path
from typing import Any, Mapping

from .certificate import write_certificate
from .toolchain import (
    DEFAULT_CONFIG,
    PROJECT_ROOT,
    atomic_write_json,
    build_toolchain_audit,
    evaluate_stage_artifact,
    load_toolchain_config,
    resolve_path,
    sha256,
)


def render_stage_command(
    stage: Mapping[str, Any], config: Mapping[str, Any], *, project_root: Path = PROJECT_ROOT
) -> list[str]:
    python = str(resolve_path(config["python"]["executable"], project_root=project_root))
    return [python if token == "{python}" else str(token) for token in stage["command"]]


def reproduction_plan(
    config: Mapping[str, Any], *, project_root: Path = PROJECT_ROOT
) -> list[dict[str, Any]]:
    return [
        {
            "name": stage["name"],
            "command": render_stage_command(stage, config, project_root=project_root),
            "outputs": list(stage["outputs"]),
            "timeout_s": int(stage["timeout_s"]),
        }
        for stage in config["stages"]
    ]


def _git_head(path: Path) -> str:
    return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()


def _run_stage(
    stage: Mapping[str, Any], config: Mapping[str, Any], *, project_root: Path
) -> dict[str, Any]:
    command = render_stage_command(stage, config, project_root=project_root)
    started_ns = time.time_ns()
    try:
        process = subprocess.run(
            command,
            cwd=project_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=int(stage["timeout_s"]),
            check=False,
        )
        exit_code = process.returncode
        output = process.stdout
        error = None
    except subprocess.TimeoutExpired as caught:
        exit_code = 124
        output = (caught.stdout or "") if isinstance(caught.stdout, str) else ""
        error = str(caught)
    except FileNotFoundError as caught:
        exit_code = 127
        output = ""
        error = str(caught)
    finished_ns = time.time_ns()
    artifact = evaluate_stage_artifact(stage, project_root=project_root)
    passed = exit_code == 0 and artifact["pass"]
    return {
        "name": stage["name"],
        "command": command,
        "timeout_s": int(stage["timeout_s"]),
        "started_ns": started_ns,
        "finished_ns": finished_ns,
        "wall_time_s": (finished_ns - started_ns) / 1_000_000_000,
        "exit_code": exit_code,
        "stdout": output,
        "error": error,
        "artifact": artifact,
        "pass": passed,
    }


def run_serial_reproduction(
    *,
    run_id: str = "run_021",
    config_path: Path = DEFAULT_CONFIG,
    manifest_path: Path | None = None,
    toolchain_output: Path | None = None,
    certificate_output: Path | None = None,
    project_root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    config = load_toolchain_config(config_path)
    manifest_path = manifest_path or resolve_path(config["reproduction_manifest"], project_root=project_root)
    toolchain_output = toolchain_output or resolve_path(config["toolchain_audit"], project_root=project_root)
    certificate_output = certificate_output or project_root / "artifacts/results/final-certificate.json"

    preflight = build_toolchain_audit(
        level="built", config_path=config_path, project_root=project_root
    )
    outcomes: list[dict[str, Any]] = []
    if preflight["summary"]["pass"]:
        for stage in config["stages"]:
            outcome = _run_stage(stage, config, project_root=project_root)
            outcomes.append(outcome)
            if not outcome["pass"]:
                break

    expected_order = [stage["name"] for stage in config["stages"]]
    stage_order = [stage["name"] for stage in outcomes]
    serial_order = all(
        later["started_ns"] >= earlier["finished_ns"]
        for earlier, later in zip(outcomes, outcomes[1:])
    )
    stages_pass = (
        len(outcomes) == len(config["stages"])
        and all(outcome["pass"] for outcome in outcomes)
    )
    summary_pass = preflight["summary"]["pass"] and stages_pass and serial_order
    manifest = {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "complete_serial_component_reproduction",
        "project_commit": _git_head(project_root),
        "toolchain_config": {
            "path": str(config_path),
            "sha256": sha256(config_path),
        },
        "expected_stage_order": expected_order,
        "stage_order": stage_order,
        "preflight": preflight["summary"],
        "stages": outcomes,
        "summary": {
            "stages": len(config["stages"]),
            "executed": len(outcomes),
            "passing": sum(bool(outcome["pass"]) for outcome in outcomes),
            "failing": sum(not bool(outcome["pass"]) for outcome in outcomes),
            "serial_order": serial_order,
            "pass": summary_pass,
        },
    }
    atomic_write_json(manifest_path, manifest)

    if not summary_pass:
        return {"manifest": manifest, "toolchain": None, "certificate": None, "pass": False}

    toolchain = build_toolchain_audit(
        level="full", config_path=config_path, project_root=project_root
    )
    atomic_write_json(toolchain_output, toolchain)
    if not toolchain["summary"]["pass"]:
        return {"manifest": manifest, "toolchain": toolchain, "certificate": None, "pass": False}

    certificate = write_certificate(certificate_output, run_id="run_022")
    passed = certificate["summary"]["full_goal_complete"]
    return {
        "manifest": manifest,
        "toolchain": toolchain,
        "certificate": certificate,
        "pass": passed,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run every AgentSys paper/system experiment serially and issue a final certificate"
    )
    parser.add_argument("--run-id", default="run_021")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--toolchain-output", type=Path)
    parser.add_argument("--certificate-output", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    config = load_toolchain_config(args.config)
    if args.dry_run:
        print(json.dumps({"serial_plan": reproduction_plan(config)}, indent=2, sort_keys=True))
        return 0

    result = run_serial_reproduction(
        run_id=args.run_id,
        config_path=args.config,
        manifest_path=args.manifest,
        toolchain_output=args.toolchain_output,
        certificate_output=args.certificate_output,
    )
    print(json.dumps(result["manifest"]["summary"], indent=2, sort_keys=True))
    if result["toolchain"] is not None:
        print(json.dumps(result["toolchain"]["summary"], indent=2, sort_keys=True))
    if result["certificate"] is not None:
        print(json.dumps(result["certificate"]["summary"], indent=2, sort_keys=True))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

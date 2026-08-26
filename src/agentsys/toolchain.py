from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = PROJECT_ROOT / "config/toolchain.json"


SOURCE_FILES = (
    ".python-version",
    "pyproject.toml",
    "uv.lock",
    "config/toolchain.json",
    "scripts/setup_toolchain.sh",
    "scripts/bootstrap_references.sh",
    "scripts/build_ramulator2.sh",
    "scripts/install_agentsys_chipyard.sh",
    "patches/chipyard/chisel3-stable-deps.patch",
    "patches/chipyard/treadle-stable-firrtl.patch",
    "src/agentsys/toolchain.py",
    "src/agentsys/reproduce.py",
    "src/agentsys/paper_reproduction.py",
    "src/agentsys/agentix_serving_simulator.py",
    "src/agentsys/agentix_reference.py",
    "src/agentsys/atx_simulator.py",
    "src/agentsys/agent_application.py",
    "src/agentsys/system_trace_compiler.py",
    "src/agentsys/system_trace.py",
    "scripts/run_agent_application.py",
    "scripts/compile_agent_system_trace.py",
    "scripts/run_system_trace.py",
    "system_sim/software/agentsys_trace_system_test.c",
    "system_sim/software/generated/agentsys_app_trace.h",
    "experiments/h12-system-trace/protocol.md",
    "experiments/h10-paper10/protocol.md",
    "docs/source-discovery.md",
    "experiments/h11-open-substitutes/protocol.md",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve_path(value: str, *, project_root: Path = PROJECT_ROOT) -> Path:
    path = Path(value)
    return path if path.is_absolute() else project_root / path


def atomic_write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
        temporary = Path(handle.name)
    os.replace(temporary, path)


def load_toolchain_config(path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    required = {
        "schema_version",
        "python",
        "tools",
        "references",
        "build_outputs",
        "chipyard_patches",
        "chipyard_overlays",
        "paper_profiles",
        "reproduction_manifest",
        "toolchain_audit",
        "stages",
    }
    missing = required - set(value)
    if missing:
        raise ValueError(f"toolchain config missing keys: {sorted(missing)}")
    if value["schema_version"] != 1:
        raise ValueError(f"unsupported toolchain schema: {value['schema_version']}")

    stages = value["stages"]
    stage_names = [stage["name"] for stage in stages]
    if len(stage_names) != len(set(stage_names)) or not stage_names:
        raise ValueError("toolchain stage names must be non-empty and unique")
    for stage in stages:
        if not stage.get("command") or not stage.get("outputs") or not stage.get("gate_path"):
            raise ValueError(f"incomplete reproduction stage: {stage.get('name')}")
        if int(stage.get("timeout_s", 0)) <= 0:
            raise ValueError(f"stage timeout must be positive: {stage['name']}")
    return value


def _git_head(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def _command_result(
    argv: list[str], *, timeout_s: int = 30, cwd: Path = PROJECT_ROOT
) -> dict[str, Any]:
    try:
        process = subprocess.run(
            argv,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_s,
            check=False,
        )
        return {
            "argv": argv,
            "exit_code": process.returncode,
            "output": process.stdout.strip(),
        }
    except FileNotFoundError as error:
        return {"argv": argv, "exit_code": 127, "output": str(error)}
    except subprocess.TimeoutExpired as error:
        return {"argv": argv, "exit_code": 124, "output": str(error)}


def nested_value(value: Any, keys: Iterable[str]) -> Any:
    current = value
    for key in keys:
        if not isinstance(current, Mapping) or key not in current:
            raise KeyError(".".join(keys))
        current = current[key]
    return current


def evaluate_stage_artifact(
    stage: Mapping[str, Any], *, project_root: Path = PROJECT_ROOT
) -> dict[str, Any]:
    outputs = [resolve_path(item, project_root=project_root) for item in stage["outputs"]]
    output_details = {
        str(path): {
            "exists": path.is_file(),
            "bytes": path.stat().st_size if path.is_file() else 0,
            "sha256": sha256(path) if path.is_file() else None,
        }
        for path in outputs
    }
    primary = outputs[0]
    gate_value: Any = None
    error: str | None = None
    if primary.is_file():
        try:
            payload = json.loads(primary.read_text(encoding="utf-8"))
            gate_value = nested_value(payload, stage["gate_path"])
        except (json.JSONDecodeError, KeyError, TypeError) as caught:
            error = str(caught)
    passed = (
        all(detail["exists"] and detail["bytes"] > 0 for detail in output_details.values())
        and gate_value is True
        and error is None
    )
    return {
        "pass": passed,
        "gate_path": stage["gate_path"],
        "gate_value": gate_value,
        "outputs": output_details,
        "error": error,
    }


def _gate(passed: bool, details: Any) -> dict[str, Any]:
    return {"pass": bool(passed), "details": details}


def build_toolchain_audit(
    *,
    level: str = "full",
    config_path: Path = DEFAULT_CONFIG,
    project_root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    if level not in {"source", "built", "full"}:
        raise ValueError(f"invalid toolchain audit level: {level}")
    config = load_toolchain_config(config_path)
    gates: dict[str, dict[str, Any]] = {}

    stage_names = [stage["name"] for stage in config["stages"]]
    output_names = [output for stage in config["stages"] for output in stage["outputs"]]
    config_details = {
        "path": str(config_path),
        "sha256": sha256(config_path),
        "stages": stage_names,
        "stage_outputs_unique": len(output_names) == len(set(output_names)),
    }
    gates["configuration"] = _gate(config_details["stage_outputs_unique"], config_details)

    required_python = tuple(int(item) for item in config["python"]["major_minor"].split("."))
    observed_python = sys.version_info[:2]
    gates["python"] = _gate(
        observed_python == required_python,
        {"expected": list(required_python), "observed": list(observed_python), "executable": sys.executable},
    )

    packages: dict[str, Any] = {}
    for name, expected in config["python"]["packages"].items():
        try:
            observed = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            observed = None
        packages[name] = {"expected": expected, "observed": observed, "pass": observed == expected}
    gates["python_packages"] = _gate(
        all(item["pass"] for item in packages.values()), packages
    )

    tools: dict[str, Any] = {}
    for tool in config["tools"]:
        argv = list(tool["argv"])
        if "/" in argv[0] and not Path(argv[0]).is_absolute():
            argv[0] = str(resolve_path(argv[0], project_root=project_root))
        result = _command_result(argv, cwd=project_root)
        passed = result["exit_code"] == 0 and tool["contains"] in result["output"]
        tools[tool["name"]] = {
            **result,
            "expected_substring": tool["contains"],
            "pass": passed,
        }
    gates["system_tools"] = _gate(all(item["pass"] for item in tools.values()), tools)

    references: dict[str, Any] = {}
    for reference in config["references"]:
        path = resolve_path(reference["path"], project_root=project_root)
        observed = _git_head(path)
        passed = observed == reference["commit"]
        references[reference["name"]] = {
            "path": str(path),
            "expected": reference["commit"],
            "observed": observed,
            "pass": passed,
        }
    gates["pinned_references"] = _gate(
        all(item["pass"] for item in references.values()), references
    )

    configured_source_files = tuple(config.get("source_files", SOURCE_FILES))
    sources: dict[str, Any] = {}
    for relative in configured_source_files:
        path = resolve_path(relative, project_root=project_root)
        sources[relative] = {
            "exists": path.is_file(),
            "sha256": sha256(path) if path.is_file() else None,
        }
    gates["source_files"] = _gate(all(item["exists"] for item in sources.values()), sources)

    reference_names = {item["name"] for item in config["references"]}
    stage_commands = {tuple(stage["command"]) for stage in config["stages"]}
    profiles: dict[str, Any] = {}
    for paper, profile in config["paper_profiles"].items():
        profile_sources = [resolve_path(item, project_root=project_root) for item in profile["sources"]]
        details = {
            "expected_endpoints": int(profile["expected_endpoints"]),
            "sources": [str(item) for item in profile_sources],
            "sources_exist": all(item.is_file() for item in profile_sources),
            "references": profile["references"],
            "references_known": set(profile["references"]).issubset(reference_names),
            "command_registered_as_stage": tuple(profile["command"]) in stage_commands,
            "output_matches_command": profile["output"] in profile["command"],
        }
        details["pass"] = all(
            (
                details["sources_exist"],
                details["references_known"],
                details["command_registered_as_stage"],
                details["output_matches_command"],
                details["expected_endpoints"] > 0,
            )
        )
        profiles[paper] = details
    profile_contract = config.get(
        "profile_contract",
        {"components": ["agentix", "agentxpu", "atx", "tisa"], "endpoint_total": 55},
    )
    profiles_complete = (
        tuple(profiles) == tuple(profile_contract["components"])
        and sum(item["expected_endpoints"] for item in profiles.values())
        == int(profile_contract["endpoint_total"])
    )
    gates["independent_paper_profiles"] = _gate(
        profiles_complete and all(item["pass"] for item in profiles.values()), profiles
    )

    if level in {"built", "full"}:
        builds: dict[str, Any] = {}
        for build in config["build_outputs"]:
            path = resolve_path(build["path"], project_root=project_root)
            exists = path.is_file()
            executable = os.access(path, os.X_OK) if exists else False
            input_paths = [
                resolve_path(item, project_root=project_root) for item in build.get("inputs", [])
            ]
            inputs_exist = all(item.is_file() for item in input_paths)
            freshness_mode = build.get("freshness", "mtime")
            if freshness_mode == "existence_and_hash":
                # Incremental external builds may correctly report "no work"
                # without touching their output. Source and output hashes are
                # still captured independently by this audit.
                fresh = exists and inputs_exist
            elif freshness_mode == "mtime":
                fresh = (
                    exists
                    and inputs_exist
                    and all(path.stat().st_mtime_ns >= item.stat().st_mtime_ns for item in input_paths)
                )
            else:
                raise ValueError(f"unknown build freshness mode: {freshness_mode}")
            passed = (
                exists
                and (not build.get("executable", False) or executable)
                and fresh
            )
            builds[build["name"]] = {
                "path": str(path),
                "exists": exists,
                "executable": executable,
                "inputs": [str(item) for item in input_paths],
                "inputs_exist": inputs_exist,
                "freshness_mode": freshness_mode,
                "fresh": fresh,
                "sha256": sha256(path) if exists else None,
                "pass": passed,
            }
        gates["build_outputs"] = _gate(all(item["pass"] for item in builds.values()), builds)

        patches: dict[str, Any] = {}
        for patch in config["chipyard_patches"]:
            repository = resolve_path(patch["repository"], project_root=project_root)
            patch_path = resolve_path(patch["patch"], project_root=project_root)
            result = _command_result(
                ["git", "-C", str(repository), "apply", "--reverse", "--check", str(patch_path)],
                cwd=project_root,
            )
            patches[patch["name"]] = {
                "repository": str(repository),
                "patch": str(patch_path),
                **result,
                "pass": result["exit_code"] == 0,
            }
        gates["chipyard_compatibility_patches"] = _gate(
            all(item["pass"] for item in patches.values()), patches
        )

        overlays: dict[str, Any] = {}
        for overlay in config["chipyard_overlays"]:
            source = resolve_path(overlay["source"], project_root=project_root)
            installed = resolve_path(overlay["installed"], project_root=project_root)
            source_hash = sha256(source) if source.is_file() else None
            installed_hash = sha256(installed) if installed.is_file() else None
            overlays[overlay["name"]] = {
                "source": str(source),
                "installed": str(installed),
                "source_sha256": source_hash,
                "installed_sha256": installed_hash,
                "pass": source_hash is not None and source_hash == installed_hash,
            }
        gates["chipyard_overlays"] = _gate(
            all(item["pass"] for item in overlays.values()), overlays
        )

    if level == "full":
        stages = {
            stage["name"]: evaluate_stage_artifact(stage, project_root=project_root)
            for stage in config["stages"]
        }
        gates["stage_artifacts"] = _gate(
            all(item["pass"] for item in stages.values()), stages
        )

        manifest_path = resolve_path(config["reproduction_manifest"], project_root=project_root)
        manifest_details: dict[str, Any] = {"path": str(manifest_path), "exists": manifest_path.is_file()}
        if manifest_path.is_file():
            try:
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                manifest_details.update(
                    {
                        "stage_order": manifest.get("stage_order"),
                        "expected_stage_order": stage_names,
                        "summary": manifest.get("summary"),
                        "sha256": sha256(manifest_path),
                    }
                )
                manifest_pass = (
                    manifest.get("stage_order") == stage_names
                    and manifest.get("summary", {}).get("pass") is True
                    and manifest.get("summary", {}).get("serial_order") is True
                )
            except json.JSONDecodeError as error:
                manifest_details["error"] = str(error)
                manifest_pass = False
        else:
            manifest_pass = False
        gates["serial_reproduction_manifest"] = _gate(manifest_pass, manifest_details)

    passed = sum(bool(gate["pass"]) for gate in gates.values())
    return {
        "schema_version": 1,
        "classification": config.get("audit_classification", "pinned_end_to_end_toolchain_audit"),
        "level": level,
        "project_commit": _git_head(project_root),
        "configuration": config_details,
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": passed,
            "failing": len(gates) - passed,
            "pass": passed == len(gates),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit the pinned AgentSys build and replay toolchain")
    parser.add_argument("--level", choices=("source", "built", "full"), default="full")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    config = load_toolchain_config(args.config)
    output = args.output
    if output is None:
        output = (
            resolve_path(config["toolchain_audit"])
            if args.level == "full"
            else PROJECT_ROOT / f"artifacts/tmp/toolchain-{args.level}-check.json"
        )
    result = build_toolchain_audit(level=args.level, config_path=args.config)
    atomic_write_json(output, result)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Mapping

from .agentix_model import run_agentix_aggregate
from .atx_model import run_atx_audit
from .experiments import PROJECT_ROOT, TARGETS_PATH, _agentix_run, _agentxpu_run, _tisa_run
from .paths import chipyard_source_identity
from .toolchain import DEFAULT_CONFIG, atomic_write_json, load_toolchain_config, resolve_path, sha256


PAPERS = ("agentix", "agentxpu", "atx", "tisa")


def _git_head(path: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def audit_paper_profile(
    paper: str,
    config: Mapping[str, Any],
    *,
    project_root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    profile = config["paper_profiles"][paper]
    references = {item["name"]: item for item in config["references"]}
    source_details: dict[str, Any] = {}
    for item in profile["sources"]:
        path = resolve_path(item, project_root=project_root)
        source_details[item] = {
            "exists": path.is_file(),
            "sha256": sha256(path) if path.is_file() else None,
        }
    reference_details: dict[str, Any] = {}
    for name in profile["references"]:
        reference = references[name]
        path = resolve_path(reference["path"], project_root=project_root)
        observed = (
            chipyard_source_identity(path)["commit"]
            if name == "chipyard"
            else _git_head(path)
        )
        reference_details[name] = {
            "path": str(path),
            "expected": reference["commit"],
            "observed": observed,
            "pass": observed == reference["commit"],
        }
    passed = all(item["exists"] for item in source_details.values()) and all(
        item["pass"] for item in reference_details.values()
    )
    return {
        "pass": passed,
        "expected_endpoints": profile["expected_endpoints"],
        "command": profile["command"],
        "output": profile["output"],
        "sources": source_details,
        "references": reference_details,
    }


def run_paper_reproduction(
    paper: str,
    *,
    run_id: str = "run_019",
    config_path: Path = DEFAULT_CONFIG,
    project_root: Path = PROJECT_ROOT,
) -> dict[str, Any]:
    if paper not in PAPERS:
        raise ValueError(f"unknown paper: {paper}")
    config = load_toolchain_config(config_path)
    if paper not in config["paper_profiles"]:
        raise ValueError(f"paper profile missing from toolchain config: {paper}")
    targets = json.loads(TARGETS_PATH.read_text(encoding="utf-8"))
    limit = float(targets["max_relative_error"])
    if limit != 0.10:
        raise ValueError(f"paper reproduction requires the registered 10% limit, observed {limit}")

    started = time.time()
    if paper == "agentix":
        direct = _agentix_run(targets["agentix"], limit)
        aggregate = run_agentix_aggregate(run_id=run_id)
        components = {"figure2": direct, "aggregate": aggregate}
        audit = [*direct["audit"], *aggregate["audit"]]
        evidence = {
            "executable_or_source_grounded": len(direct["audit"]),
            "open_executable_closed_platform_substitute": len(aggregate["audit"]),
            "paper_parameterized_component_replay": 0,
        }
    elif paper == "agentxpu":
        direct = _agentxpu_run(targets["agentxpu"], limit)
        components = {"trace_simulation": direct}
        audit = list(direct["audit"])
        evidence = {
            "executable_or_source_grounded": len(audit),
            "open_executable_closed_platform_substitute": 0,
            "paper_parameterized_component_replay": 0,
        }
    elif paper == "atx":
        aggregate = run_atx_audit(run_id=run_id)
        components = {"microarchitecture_simulation": aggregate}
        audit = list(aggregate["audit"])
        evidence = {
            "executable_or_source_grounded": 0,
            "open_executable_closed_platform_substitute": len(audit),
            "paper_parameterized_component_replay": 0,
        }
    else:
        direct = _tisa_run(targets["tisa"], limit)
        components = {"cycle_simulation": direct}
        audit = list(direct["audit"])
        evidence = {
            "executable_or_source_grounded": len(audit),
            "open_executable_closed_platform_substitute": 0,
            "paper_parameterized_component_replay": 0,
        }

    profile = audit_paper_profile(paper, config, project_root=project_root)
    expected_endpoints = int(config["paper_profiles"][paper]["expected_endpoints"])
    passing = sum(bool(item["pass"]) for item in audit)
    maximum_error = max(float(item["relative_error"]) for item in audit)
    endpoint_names = [item["endpoint"] for item in audit]
    paper_pass = (
        len(audit) == expected_endpoints
        and len(endpoint_names) == len(set(endpoint_names))
        and passing == len(audit)
        and maximum_error <= limit
        and all(float(item["limit"]) == limit for item in audit)
    )
    return {
        "schema_version": 1,
        "run_id": run_id,
        "classification": "independent_per_paper_performance_reproduction",
        "paper": paper,
        "environment": {
            "python": sys.version,
            "project_commit": _git_head(project_root),
            "toolchain_config": str(config_path),
            "toolchain_config_sha256": sha256(config_path),
        },
        "registered_limit": limit,
        "toolchain_profile": profile,
        "evidence_classes": evidence,
        "components": components,
        "audit": audit,
        "summary": {
            "endpoints": len(audit),
            "passing": passing,
            "failing": len(audit) - passing,
            "max_relative_error": maximum_error,
            "limit": limit,
            "toolchain_profile_pass": profile["pass"],
            "pass": paper_pass and profile["pass"],
        },
        "wall_time_s": time.time() - started,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run one paper's complete independent performance reproduction"
    )
    parser.add_argument("--paper", choices=PAPERS, required=True)
    parser.add_argument("--run-id", default="run_019")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)

    config = load_toolchain_config(args.config)
    output = args.output or resolve_path(config["paper_profiles"][args.paper]["output"])
    result = run_paper_reproduction(args.paper, run_id=args.run_id, config_path=args.config)
    atomic_write_json(output, result)
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

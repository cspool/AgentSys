from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from .paths import (
    CHIPYARD_BUILD_GITLINKS,
    CHIPYARD_PATCHED_FILES,
    CHIPYARD_TOKEN,
    PROJECT_ROOT,
    ChipyardPathError,
    chipyard_build_preflight,
    chipyard_source_identity,
    resolve_chipyard_root,
)
from .portable_reproduce import DEFAULT_RUN_ID, resolve_run_path
from .revised_certificate import _run


DEFAULT_CONFIG = PROJECT_ROOT / "config/project-local-chipyard.json"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


IMPLEMENTATION_PATHS = (
    ".gitignore",
    ".gitmodules",
    ".python-version",
    "pyproject.toml",
    "uv.lock",
    "chipyard",
    "config",
    "data",
    "docker",
    "integrations",
    "patches",
    "rtl",
    "scripts",
    "src",
    "system_sim",
    "tests",
    "workloads",
)


def _git_head(project_root: Path = PROJECT_ROOT) -> str:
    return subprocess.check_output(
        ["git", "-C", str(project_root), "rev-parse", "HEAD"], text=True
    ).strip()


def implementation_source_closure(
    expected_commit: str,
    *,
    project_root: Path = PROJECT_ROOT,
    implementation_paths: tuple[str, ...] = IMPLEMENTATION_PATHS,
) -> dict[str, Any]:
    """Prove active source equals an ancestor implementation commit.

    Evidence and documentation commits may follow the implementation commit,
    but tracked, staged, unstaged, or untracked changes under the registered
    implementation paths are rejected.
    """

    project_root = project_root.resolve()
    current_commit = _git_head(project_root)
    exists = subprocess.run(
        [
            "git",
            "-C",
            str(project_root),
            "cat-file",
            "-e",
            f"{expected_commit}^{{commit}}",
        ],
        check=False,
        capture_output=True,
        text=True,
    ).returncode == 0
    ancestor = exists and subprocess.run(
        [
            "git",
            "-C",
            str(project_root),
            "merge-base",
            "--is-ancestor",
            expected_commit,
            current_commit,
        ],
        check=False,
        capture_output=True,
        text=True,
    ).returncode == 0

    changed: list[str] = []
    if exists:
        difference = subprocess.run(
            [
                "git",
                "-C",
                str(project_root),
                "diff",
                "--name-status",
                "--ignore-submodules=dirty",
                expected_commit,
                "--",
                *implementation_paths,
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        changed = difference.stdout.splitlines()
        if difference.returncode != 0:
            changed.append(f"git-diff-error:{difference.stderr.strip()}")
    untracked_result = subprocess.run(
        [
            "git",
            "-C",
            str(project_root),
            "ls-files",
            "--others",
            "--exclude-standard",
            "--",
            *implementation_paths,
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    untracked = untracked_result.stdout.splitlines()
    if untracked_result.returncode != 0:
        untracked.append(f"git-ls-files-error:{untracked_result.stderr.strip()}")
    return {
        "expected_commit": expected_commit,
        "current_commit": current_commit,
        "expected_commit_exists": exists,
        "expected_commit_is_ancestor": ancestor,
        "implementation_paths": list(implementation_paths),
        "changed_paths": changed,
        "untracked_paths": untracked,
        "pass": exists and ancestor and not changed and not untracked,
    }


def endpoint_signature(result: dict[str, Any]) -> list[tuple[Any, ...]]:
    return [
        (
            item["endpoint"],
            item["layer"],
            float(item["observed"]),
            json.dumps(
                item.get("target", item.get("target_range")),
                sort_keys=True,
                separators=(",", ":"),
            ),
            float(item["relative_error"]),
            float(item["limit"]),
            bool(item["pass"]),
        )
        for item in result["audit"]
    ]


def substrate_signature(result: dict[str, Any]) -> list[tuple[Any, ...]]:
    return sorted(
        (
            item["backend"],
            item["workload"],
            item["summary"],
            item["checks"],
            item["pass"],
        )
        for item in result["records"]
    )


def agent_signature(manifest: dict[str, Any]) -> dict[str, Any]:
    signature: dict[str, Any] = {"summary": manifest["summary"], "workloads": {}}
    for name, item in manifest["workloads"].items():
        system = _json(Path(item["path"]))
        signature["workloads"][name] = {
            "summary": system["summary"],
            "gates": system["gates"],
            "backend_gates": system["backend_gates"],
            "cycle": system["backend_results"]["cycle"]["parsed"],
            "rtl": system["backend_results"]["rtl"]["parsed"],
            "trace": {
                key: value for key, value in system["trace"].items() if key != "path"
            },
        }
    return signature


def active_path_offenders() -> list[str]:
    roots = (
        PROJECT_ROOT / "src/agentsys",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "config",
        PROJECT_ROOT / "system_sim/software",
    )
    offenders: list[str] = []
    machine_literal = "/" + "root" + "/chipyard"
    for root in roots:
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix == ".pyc":
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            if machine_literal in text:
                offenders.append(str(path.relative_to(PROJECT_ROOT)))
    return offenders


def build_portable_certificate(
    *,
    expected_commit: str,
    config_path: Path = DEFAULT_CONFIG,
    run_id: str = DEFAULT_RUN_ID,
    run_checks: bool = True,
) -> dict[str, Any]:
    if not re.fullmatch(r"[0-9a-f]{40}", expected_commit):
        raise ValueError("expected_commit must be a full 40-character Git SHA")
    config_path = config_path.resolve()
    config = _json(config_path)
    replay_path = resolve_run_path(config["manifest"], run_id=run_id)
    replay = _json(replay_path)
    source_closure = implementation_source_closure(expected_commit)
    current_results = {
        name: _json(Path(item["path"])) for name, item in replay["results"].items()
    }
    baselines = {
        name: _json(PROJECT_ROOT / path) for name, path in config["baselines"].items()
    }
    result_hashes = all(
        Path(item["path"]).is_file()
        and _sha256(Path(item["path"])) == item["sha256"]
        for item in replay["results"].values()
    )

    root = resolve_chipyard_root()
    identity = chipyard_source_identity(root)
    preflight = chipyard_build_preflight(root)
    default_root = resolve_chipyard_root(environ={})
    override_root = resolve_chipyard_root(
        environ={"AGENTSYS_CHIPYARD_ROOT": str(root)}
    )
    with tempfile.TemporaryDirectory(prefix="agentsys-invalid-chipyard-") as directory:
        try:
            resolve_chipyard_root(
                environ={"AGENTSYS_CHIPYARD_ROOT": directory}
            )
            invalid_override_rejected = False
        except ChipyardPathError:
            invalid_override_rejected = True

    raw_configs = {
        name: (PROJECT_ROOT / relative).read_text(encoding="utf-8")
        for name, relative in {
            "historical": "config/toolchain.json",
            "revised": "config/revised-toolchain.json",
            "mlx": "config/mlx-active-source.json",
        }.items()
    }
    required_files = (
        "chipyard/.agentsys-source.json",
        "scripts/chipyard_paths.sh",
        "scripts/bootstrap_chipyard.sh",
        "src/agentsys/paths.py",
        "src/agentsys/portable_reproduce.py",
        "src/agentsys/portable_certificate.py",
        "config/project-local-chipyard.json",
        "experiments/h20-project-local-chipyard/protocol.md",
        "experiments/h21-durable-source-certificate/protocol.md",
    )
    files = {
        relative: {
            "exists": (PROJECT_ROOT / relative).is_file(),
            "sha256": _sha256(PROJECT_ROOT / relative)
            if (PROJECT_ROOT / relative).is_file()
            else None,
        }
        for relative in required_files
    }

    checks: dict[str, Any] = {}
    if run_checks:
        checks["pytest"] = _run(
            [str(PROJECT_ROOT / ".venv/bin/python"), "-m", "pytest"],
            timeout_s=900,
        )
        checks["bootstrap_verify_only"] = _run(
            ["bash", "scripts/bootstrap_chipyard.sh", "--verify-only"],
            timeout_s=120,
        )
        checks["mlx_overlay"] = _run(
            ["bash", "scripts/install_mlx_chipyard.sh"], timeout_s=300
        )
    pytest_count = None
    if "pytest" in checks:
        match = re.search(r"(\d+) passed", checks["pytest"]["output"])
        pytest_count = int(match.group(1)) if match else None
    checks_pass = all(item["pass"] for item in checks.values()) if checks else True
    if "bootstrap_verify_only" in checks:
        checks_pass = checks_pass and "AgentSys Chipyard ready" in checks[
            "bootstrap_verify_only"
        ]["output"]
    if "mlx_overlay" in checks:
        checks_pass = checks_pass and "12/12 files" in checks["mlx_overlay"][
            "output"
        ]

    current_layers = current_results["layers"]
    current_agents = current_results["agents"]
    current_substrate = current_results["substrate"]
    gates = {
        "implementation_source_closure": source_closure["pass"],
        "replay_implementation_commit": replay["project_commit"]
        == expected_commit,
        "replay_four_stages_nine_gates": replay["summary"]["pass"]
        and replay["summary"]["executed"] == replay["summary"]["stages"] == 4
        and replay["summary"]["gates_passing"] == replay["summary"]["gates"] == 9,
        "replay_result_hashes": result_hashes,
        "active_paths_portable": active_path_offenders() == [],
        "default_and_override_contract": default_root
        == override_root
        == (PROJECT_ROOT / "chipyard").resolve()
        and invalid_override_rejected,
        "vendored_identity_and_build": identity["commit"]
        == "b5d013190d637e634113cb5179f8c8885df1945a"
        and identity["kind"] == "vendored_source_snapshot"
        and preflight["pass"],
        "chipyard_25_gitlinks_exact": len(preflight["gitlinks"])
        == len(CHIPYARD_BUILD_GITLINKS)
        == 25
        and all(item["pass"] for item in preflight["gitlinks"].values()),
        "chipyard_compatibility_patches_exact": len(preflight["patched_files"])
        == len(CHIPYARD_PATCHED_FILES)
        == 2
        and all(item["pass"] for item in preflight["patched_files"].values()),
        "portable_manifest_tokens": all(CHIPYARD_TOKEN in text for text in raw_configs.values())
        and all("/" + "root" + "/chipyard" not in text for text in raw_configs.values()),
        "substrate_exact_baseline": current_substrate["summary"]
        == baselines["chipyard"]["summary"]
        and substrate_signature(current_substrate)
        == substrate_signature(baselines["chipyard"]),
        "agent_exact_baseline": agent_signature(current_agents)
        == agent_signature(baselines["agents"]),
        "paper_endpoint_exact_baseline": current_layers["summary"]
        == baselines["layers"]["summary"]
        and endpoint_signature(current_layers) == endpoint_signature(baselines["layers"]),
        "registered_73_at_10_percent": current_layers["summary"]["passing"]
        == current_layers["summary"]["endpoints"]
        == 73
        and current_layers["summary"]["max_relative_error"] <= 0.10,
        "three_agents_exact_work": current_agents["summary"]["passing"]
        == current_agents["summary"]["gates"]
        == 9
        and current_agents["summary"]["calls"] == 20
        and current_agents["summary"]["llm_calls"] == 17
        and current_agents["summary"]["tool_calls"] == 3
        and current_agents["summary"]["mlx_micro_ops"] == 765,
        "sixteen_fresh_executions": replay["summary"]["fresh_rocket_executions"]
        == 16,
        "evidence_boundary_retained": current_layers["layers"]["mlx"][
            "paper_accuracy"
        ]["leave_one_out_max_relative_error"]
        > 0.10
        and current_layers["layers"]["mlx"]["full_paper_scope"][
            "all_paper_experiments_reproduced_within_10pct"
        ]
        is False,
        "required_files": all(item["exists"] for item in files.values()),
        "fresh_checks": checks_pass and (pytest_count is not None if checks else True),
    }
    return {
        "schema_version": 2,
        "run_id": run_id,
        "classification": "durable_project_local_chipyard_certificate",
        "evidence_boundary": replay["evidence_boundary"],
        "project_commit": _git_head(),
        "implementation_commit": expected_commit,
        "expected_commit": expected_commit,
        "implementation_source_closure": source_closure,
        "configuration": {"path": str(config_path), "sha256": _sha256(config_path)},
        "replay": {"path": str(replay_path), "sha256": _sha256(replay_path)},
        "chipyard": {"identity": identity, "preflight": preflight},
        "baseline_paths": config["baselines"],
        "required_files": files,
        "checks": checks,
        "requirements": gates,
        "summary": {
            "requirements": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "fresh_checks": len(checks),
            "pytest_passed": pytest_count,
            "paper_endpoints": current_layers["summary"]["endpoints"],
            "paper_endpoints_passing": current_layers["summary"]["passing"],
            "max_relative_error": current_layers["summary"]["max_relative_error"],
            "agent_workloads": current_agents["summary"]["workloads"],
            "fresh_rocket_executions": replay["summary"]["fresh_rocket_executions"],
            "pass": all(gates.values()),
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Certify the project-local Chipyard AgentSys replay"
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--run-id", default=DEFAULT_RUN_ID)
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    config = _json(args.config)
    output = args.output or resolve_run_path(config["certificate"], run_id=args.run_id)
    result = build_portable_certificate(
        expected_commit=args.expected_commit,
        config_path=args.config,
        run_id=args.run_id,
        run_checks=True,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))
    print(output)
    return 0 if result["summary"]["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

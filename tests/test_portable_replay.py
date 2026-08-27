from __future__ import annotations

import json
import subprocess
from pathlib import Path

from agentsys.portable_certificate import (
    agent_signature,
    endpoint_signature,
    implementation_source_closure,
    substrate_signature,
)
from agentsys.portable_reproduce import resolve_run_path
from agentsys.workload import PROJECT_ROOT


def test_project_local_replay_contract_is_strict_and_serial() -> None:
    config = json.loads(
        (PROJECT_ROOT / "config/project-local-chipyard.json").read_text(
            encoding="utf-8"
        )
    )
    assert config["expected_stage_order"] == [
        "project_local_chipyard_preflight",
        "project_local_mlx_substrate",
        "project_local_three_agent_dags",
        "project_local_six_layer_regression",
    ]
    assert set(config["baselines"]) == {"chipyard", "agents", "layers"}
    assert "{run_id}" in config["output_root"]
    assert "{run_id}" in config["manifest"]
    assert "{run_id}" in config["certificate"]


def test_run_scoped_paths_are_isolated_and_reject_traversal() -> None:
    path = resolve_run_path(
        "artifacts/project_local_chipyard/{run_id}", run_id="run_052"
    )
    assert path == PROJECT_ROOT / "artifacts/project_local_chipyard/run_052"

    try:
        resolve_run_path("artifacts/{run_id}", run_id="../../outside")
    except ValueError as error:
        assert "run_id" in str(error)
    else:
        raise AssertionError("path-traversal run_id was accepted")


def test_implementation_closure_allows_only_non_source_descendants(
    tmp_path: Path,
) -> None:
    def git(*args: str) -> str:
        return subprocess.check_output(
            ["git", "-C", str(tmp_path), *args], text=True
        ).strip()

    git("init", "-q")
    git("config", "user.name", "AgentSys test")
    git("config", "user.email", "agentsys@example.invalid")
    (tmp_path / "src").mkdir()
    (tmp_path / "config").mkdir()
    (tmp_path / "src/core.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / "config/system.json").write_text("{}\n", encoding="utf-8")
    git("add", "src", "config")
    git("commit", "-q", "-m", "implementation")
    implementation_commit = git("rev-parse", "HEAD")

    (tmp_path / "report.md").write_text("evidence\n", encoding="utf-8")
    git("add", "report.md")
    git("commit", "-q", "-m", "evidence")
    closure = implementation_source_closure(
        implementation_commit,
        project_root=tmp_path,
        implementation_paths=("src", "config"),
    )
    assert closure["pass"]
    assert closure["expected_commit_is_ancestor"]

    (tmp_path / "src/core.py").write_text("VALUE = 2\n", encoding="utf-8")
    changed = implementation_source_closure(
        implementation_commit,
        project_root=tmp_path,
        implementation_paths=("src", "config"),
    )
    assert not changed["pass"]
    assert changed["changed_paths"] == ["M\tsrc/core.py"]

    (tmp_path / "src/core.py").write_text("VALUE = 1\n", encoding="utf-8")
    (tmp_path / "src/untracked.py").write_text("VALUE = 3\n", encoding="utf-8")
    untracked = implementation_source_closure(
        implementation_commit,
        project_root=tmp_path,
        implementation_paths=("src", "config"),
    )
    assert not untracked["pass"]
    assert untracked["untracked_paths"] == ["src/untracked.py"]


def test_endpoint_signature_supports_scalar_and_range_targets() -> None:
    result = {
        "audit": [
            {
                "endpoint": "scalar",
                "layer": "tisa",
                "observed": 1.2,
                "target": 1.25,
                "relative_error": 0.04,
                "limit": 0.1,
                "pass": True,
            },
            {
                "endpoint": "range",
                "layer": "tisa",
                "observed": 1.3,
                "target_range": [1.2, 1.4],
                "relative_error": 0.0,
                "limit": 0.1,
                "pass": True,
            },
        ]
    }
    signature = endpoint_signature(result)
    assert signature[0][3] == "1.25"
    assert signature[1][3] == "[1.2,1.4]"


def test_substrate_signature_ignores_artifact_locations() -> None:
    record = {
        "backend": "cycle",
        "workload": "bsmm",
        "summary": {"kernel": 48},
        "checks": {"golden": True},
        "pass": True,
    }
    first = {"records": [{**record, "log": "/first"}]}
    second = {"records": [{**record, "log": "/second"}]}
    assert substrate_signature(first) == substrate_signature(second)


def test_agent_signature_ignores_only_trace_location(tmp_path: Path) -> None:
    def write(name: str, trace_path: str) -> Path:
        path = tmp_path / f"{name}.json"
        path.write_text(
            json.dumps(
                {
                    "summary": {"pass": True},
                    "gates": {"work": True},
                    "backend_gates": {"cycle": {"golden": True}},
                    "backend_results": {
                        "cycle": {"parsed": {"summary": {"kernel": 10}}},
                        "rtl": {"parsed": {"summary": {"kernel": 8}}},
                    },
                    "trace": {
                        "path": trace_path,
                        "sha256": "same",
                        "events": 3,
                        "layers": ["cpu", "mlx"],
                    },
                }
            ),
            encoding="utf-8",
        )
        return path

    first = {
        "summary": {"pass": True},
        "workloads": {"w": {"path": str(write("first", "/first"))}},
    }
    second = {
        "summary": {"pass": True},
        "workloads": {"w": {"path": str(write("second", "/second"))}},
    }
    assert agent_signature(first) == agent_signature(second)

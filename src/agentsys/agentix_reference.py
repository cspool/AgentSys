from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[2]
AUTELLIX_ROOT = PROJECT_ROOT / ".references/autellix"
AUTELLIX_COMMIT = "1df19874d1fb10e497b7185bf813fdd7be189683"


POLICY_FILES = {
    "process_table": "vllm/v1/core/sched/autellix/process_table.py",
    "mlfq": "vllm/v1/core/sched/autellix/mlfq.py",
    "plas": "vllm/v1/core/sched/autellix/plas_scheduler.py",
    "atlas": "vllm/v1/core/sched/autellix/atlas_scheduler.py",
    "attained_service": "vllm/v1/core/sched/autellix/attained_service.py",
}


REQUIRED_SEMANTICS = {
    "process_table": ("max_critical_path", "active_call_ids", "total_wait"),
    "mlfq": ("anti_starvation", "total_wait / max(1.0, total_service) >= beta"),
    "plas": ("class PLASScheduler", "process_table"),
    "atlas": ("class ATLASScheduler", "update_critical_path"),
    "attained_service": ("AttainedServiceTracker",),
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_head(path: Path) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(path), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def run_autellix_reference_audit(*, timeout_s: int = 120) -> dict[str, Any]:
    observed_commit = _git_head(AUTELLIX_ROOT)
    files: dict[str, Any] = {}
    for name, relative in POLICY_FILES.items():
        path = AUTELLIX_ROOT / relative
        content = path.read_text(encoding="utf-8") if path.is_file() else ""
        terms = REQUIRED_SEMANTICS[name]
        files[name] = {
            "path": relative,
            "exists": path.is_file(),
            "sha256": _sha256(path) if path.is_file() else None,
            "required_semantics": {term: term in content for term in terms},
        }
        files[name]["pass"] = files[name]["exists"] and all(
            files[name]["required_semantics"].values()
        )

    command = [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "tests/v1/core/sched/autellix",
    ]
    try:
        process = subprocess.run(
            command,
            cwd=AUTELLIX_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout_s,
            check=False,
        )
        output = process.stdout
        exit_code = process.returncode
    except (FileNotFoundError, subprocess.TimeoutExpired) as error:
        output = str(error)
        exit_code = 124 if isinstance(error, subprocess.TimeoutExpired) else 127
    match = re.search(r"(\d+) passed", output)
    tests_passed = int(match.group(1)) if match else 0
    gates = {
        "pinned_commit": observed_commit == AUTELLIX_COMMIT,
        "policy_files": all(item["pass"] for item in files.values()),
        "pure_python_reference_tests": exit_code == 0 and tests_passed >= 58,
    }
    return {
        "schema_version": 1,
        "classification": "independent_public_vllm_fork_reference_not_author_verified",
        "repository": "https://github.com/kungfu-team/autellix",
        "branch": "autellix-scheduling",
        "expected_commit": AUTELLIX_COMMIT,
        "observed_commit": observed_commit,
        "provenance_note": (
            "Discovered through author/ecosystem source search; the fork is not "
            "identified as an official Agentix artifact by the paper authors."
        ),
        "files": files,
        "test": {
            "command": command,
            "exit_code": exit_code,
            "tests_passed": tests_passed,
            "output": output,
        },
        "gates": gates,
        "summary": {
            "gates": len(gates),
            "passing": sum(gates.values()),
            "failing": len(gates) - sum(gates.values()),
            "pass": all(gates.values()),
        },
        "digest": hashlib.sha256(
            json.dumps({name: item["sha256"] for name, item in files.items()}, sort_keys=True).encode()
        ).hexdigest(),
    }

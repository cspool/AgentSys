from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHIPYARD_ENV = "AGENTSYS_CHIPYARD_ROOT"
CHIPYARD_TOKEN = "${AGENTSYS_CHIPYARD_ROOT}"
CHIPYARD_UPSTREAM_COMMIT = "b5d013190d637e634113cb5179f8c8885df1945a"
CHIPYARD_MARKER = ".agentsys-source.json"


class ChipyardPathError(ValueError):
    """Raised when the selected Chipyard source does not satisfy the pin."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _git_output(root: Path, *args: str) -> str | None:
    try:
        return subprocess.check_output(
            ["git", "-C", str(root), *args],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def chipyard_source_identity(root: Path) -> dict[str, Any]:
    """Validate a standalone checkout or the repository-owned source snapshot."""

    root = root.expanduser().resolve()
    required = (
        root / "build.sbt",
        root / "common.mk",
        root / "generators/chipyard/src/main/scala/config/RocketConfigs.scala",
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise ChipyardPathError(
            f"Chipyard source tree is incomplete at {root}; missing: {missing}"
        )

    git_top = _git_output(root, "rev-parse", "--show-toplevel")
    if git_top is not None and Path(git_top).resolve() == root:
        observed = _git_output(root, "rev-parse", "HEAD")
        if observed != CHIPYARD_UPSTREAM_COMMIT:
            raise ChipyardPathError(
                "Chipyard commit mismatch at "
                f"{root}: {observed!r} != {CHIPYARD_UPSTREAM_COMMIT}"
            )
        return {
            "path": str(root),
            "kind": "standalone_git_checkout",
            "commit": observed,
            "identity_files": {},
        }

    marker_path = root / CHIPYARD_MARKER
    if not marker_path.is_file():
        raise ChipyardPathError(
            f"vendored Chipyard source at {root} has no {CHIPYARD_MARKER}"
        )
    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ChipyardPathError(f"invalid Chipyard source marker: {error}") from error
    if marker.get("schema_version") != 1:
        raise ChipyardPathError("unsupported Chipyard source marker schema")
    if marker.get("upstream_commit") != CHIPYARD_UPSTREAM_COMMIT:
        raise ChipyardPathError("vendored Chipyard upstream commit mismatch")

    checked: dict[str, dict[str, Any]] = {}
    for relative, expected in marker.get("identity_files", {}).items():
        path = root / relative
        observed = _sha256(path) if path.is_file() else None
        checked[relative] = {
            "expected": expected,
            "observed": observed,
            "pass": observed == expected,
        }
    failures = [name for name, item in checked.items() if not item["pass"]]
    if not checked or failures:
        raise ChipyardPathError(
            f"vendored Chipyard identity mismatch at {root}: {failures or 'no files'}"
        )
    return {
        "path": str(root),
        "kind": "vendored_source_snapshot",
        "commit": marker["upstream_commit"],
        "marker": str(marker_path),
        "marker_sha256": _sha256(marker_path),
        "identity_files": checked,
    }


def resolve_chipyard_root(
    *,
    environ: Mapping[str, str] | None = None,
    project_root: Path = PROJECT_ROOT,
    validate: bool = True,
) -> Path:
    """Resolve the explicit override or the repository-local Chipyard snapshot."""

    values = os.environ if environ is None else environ
    configured = values.get(CHIPYARD_ENV)
    if configured:
        candidate = Path(configured).expanduser()
        if not candidate.is_absolute():
            candidate = project_root / candidate
    else:
        candidate = project_root / "chipyard"
    candidate = candidate.resolve()
    if validate:
        chipyard_source_identity(candidate)
    return candidate


def expand_chipyard_tokens(value: Any, *, chipyard_root: Path | None = None) -> Any:
    """Recursively expand portable Chipyard tokens in a loaded manifest."""

    root = chipyard_root or resolve_chipyard_root()
    if isinstance(value, str):
        return value.replace(CHIPYARD_TOKEN, str(root))
    if isinstance(value, list):
        return [expand_chipyard_tokens(item, chipyard_root=root) for item in value]
    if isinstance(value, tuple):
        return tuple(expand_chipyard_tokens(item, chipyard_root=root) for item in value)
    if isinstance(value, dict):
        return {
            key: expand_chipyard_tokens(item, chipyard_root=root)
            for key, item in value.items()
        }
    return value


def chipyard_build_preflight(root: Path | None = None) -> dict[str, Any]:
    """Report whether the selected tree has the files needed by active replays."""

    selected = root.resolve() if root is not None else resolve_chipyard_root()
    identity = chipyard_source_identity(selected)
    requirements = {
        "rocket_chip": selected / "generators/rocket-chip/src/main/scala/rocket/RocketCore.scala",
        "rocket_config": selected
        / "generators/rocket-chip/api-config-chipsalliance/design/craft/src/config/Config.scala",
        "hardfloat": selected
        / "generators/rocket-chip/hardfloat/src/main/scala/primitives.scala",
        "chisel3": selected / "tools/chisel3/build.sbt",
        "treadle": selected / "tools/treadle/build.sbt",
        "barstools_mdf": selected
        / "tools/barstools/mdf/scalalib/src/main/scala/SRAM.scala",
        "env": selected / "env.sh",
        "riscv_gcc": selected
        / "esp-tools-install/bin/riscv64-unknown-elf-gcc",
    }
    checks = {name: path.is_file() for name, path in requirements.items()}
    return {
        "root": str(selected),
        "identity": identity,
        "requirements": {name: str(path) for name, path in requirements.items()},
        "checks": checks,
        "pass": all(checks.values()),
    }

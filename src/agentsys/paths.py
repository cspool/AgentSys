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
CHIPYARD_BUILD_GITLINKS = {
    "generators/boom": "e1a70afed7de77f6ba9f6e501de71f7f41afc47c",
    "generators/cva6": "139741a584d7e3c0446db592b5d99529bd6cf9fa",
    "generators/gemmini": "7ac61db64fecbc8918b3039d738513b4a03337ca",
    "generators/hwacha": "62c01f5a8858aa1b827f0f9372a4392d7b596fca",
    "generators/icenet": "084ca5070605ea7919358f917289cca240d0289a",
    "generators/nvdla": "b2b78c9f892a6196634eb3f1fbc443436c897a00",
    "generators/riscv-sodor": "449354c27bf07ccc865dc6c005df1d08eaf5b01c",
    "generators/rocket-chip": "a7b016e46e22e4fdc013357051e30511f80df082",
    "generators/sha3": "63eda8268c16c502cada9944ae41b584e6e32789",
    "generators/sifive-blocks": "545a396f3486132b01ceef3cbce2085608984478",
    "generators/sifive-cache": "e3a3000cc1fd4cdf3a4e638e4d081b8aae94ebf0",
    "generators/testchipip": "0743c5a9410af713fb7a1c0025d6331dfedec328",
    "sims/firesim": "b611551ca5ea391513584dc2cde3d82717309125",
    "tools/api-config-chipsalliance": "fd8df1105a92065425cd353b6855777e35bd79b4",
    "tools/barstools": "a3711c4e19911b57b21bdcf8d459d19795f3201d",
    "tools/chisel-testers": "ce4e027e5f3d871df59236b8471ea3e5be40130e",
    "tools/chisel3": "58d38f9620e7e91e4668266686484073c0ba7d2e",
    "tools/dsptools": "aad6a3db1520a05ae668681941a19bdcc40aec03",
    "tools/firrtl": "7756f8f9634b68a1375d2c2ca13abc5742234201",
    "tools/firrtl-interpreter": "5ab0cfe7020ca17804078c85d020730764ee176f",
    "tools/rocket-dsp-utils": "355bf9f2038c68f4d44650f66d1516d171bfb224",
    "tools/treadle": "925687ad22c42dd2c8b4dc127c0476f9902b3163",
    "generators/rocket-chip/api-config-chipsalliance": (
        "fd8df1105a92065425cd353b6855777e35bd79b4"
    ),
    "generators/rocket-chip/hardfloat": (
        "01904f99ed3ad26cdbe2876f638d63e30e7fecdc"
    ),
    "tools/barstools/mdf": "4be9b173647c77f990a542f4eb5f69af01d77316",
}
CHIPYARD_PATCHED_FILES = {
    "tools/chisel3/build.sbt": (
        "6cf44ba1acab54a6ae65d3c0eeb1133098e39c975d4b90d417f4d8695a212df3"
    ),
    "tools/treadle/build.sbt": (
        "d4ace994540ef3bda4bb06809d809e8232d961805a96876c035e0dc19f6fcd4f"
    ),
}


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
    if marker.get("build_gitlinks") != CHIPYARD_BUILD_GITLINKS:
        raise ChipyardPathError("vendored Chipyard build gitlink declaration mismatch")
    if marker.get("patched_files") != CHIPYARD_PATCHED_FILES:
        raise ChipyardPathError("vendored Chipyard patched-file declaration mismatch")

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
        "declared_build_gitlinks": marker["build_gitlinks"],
        "declared_patched_files": marker["patched_files"],
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
    gitlinks: dict[str, dict[str, Any]] = {}
    for relative, expected in CHIPYARD_BUILD_GITLINKS.items():
        repository = selected / relative
        observed = _git_output(repository, "rev-parse", "HEAD")
        changed_text = _git_output(repository, "diff", "--name-only", "HEAD", "--")
        changed = sorted(changed_text.splitlines()) if changed_text else []
        allowed_changed = (
            ["build.sbt"]
            if relative in {"tools/chisel3", "tools/treadle"}
            else []
        )
        untracked_text = _git_output(
            repository, "ls-files", "--others", "--exclude-standard"
        )
        untracked = sorted(untracked_text.splitlines()) if untracked_text else []
        unexpected_untracked = [
            name
            for name in untracked
            if not (
                name.startswith("target/")
                or "/target/" in name
                or name.startswith("project/target/")
            )
        ]
        gitlinks[relative] = {
            "expected": expected,
            "observed": observed,
            "changed_tracked_files": changed,
            "allowed_changed_tracked_files": allowed_changed,
            "unexpected_untracked_files": unexpected_untracked,
            "pass": observed == expected
            and changed == allowed_changed
            and not unexpected_untracked,
        }

    patched_files: dict[str, dict[str, Any]] = {}
    for relative, expected in CHIPYARD_PATCHED_FILES.items():
        path = selected / relative
        observed = _sha256(path) if path.is_file() else None
        patched_files[relative] = {
            "expected": expected,
            "observed": observed,
            "pass": observed == expected,
        }

    checks = {name: path.is_file() for name, path in requirements.items()}
    checks["gitlink_closure"] = len(gitlinks) == len(CHIPYARD_BUILD_GITLINKS) and all(
        item["pass"] for item in gitlinks.values()
    )
    checks["compatibility_patch_closure"] = len(patched_files) == len(
        CHIPYARD_PATCHED_FILES
    ) and all(item["pass"] for item in patched_files.values())
    return {
        "root": str(selected),
        "identity": identity,
        "requirements": {name: str(path) for name, path in requirements.items()},
        "gitlinks": gitlinks,
        "patched_files": patched_files,
        "checks": checks,
        "pass": all(checks.values()),
    }

from __future__ import annotations

from pathlib import Path

import pytest

from agentsys.paths import (
    CHIPYARD_BUILD_GITLINKS,
    CHIPYARD_PATCHED_FILES,
    CHIPYARD_TOKEN,
    CHIPYARD_UPSTREAM_COMMIT,
    PROJECT_ROOT,
    ChipyardPathError,
    chipyard_build_preflight,
    chipyard_source_identity,
    expand_chipyard_tokens,
    resolve_chipyard_root,
)


def test_default_chipyard_root_is_vendored_source(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("AGENTSYS_CHIPYARD_ROOT", raising=False)
    root = resolve_chipyard_root()
    identity = chipyard_source_identity(root)
    assert root == (PROJECT_ROOT / "chipyard").resolve()
    assert identity["kind"] == "vendored_source_snapshot"
    assert identity["commit"] == CHIPYARD_UPSTREAM_COMMIT
    assert all(item["pass"] for item in identity["identity_files"].values())


def test_chipyard_build_closure_pins_gitlinks_and_compatibility_patches() -> None:
    preflight = chipyard_build_preflight()
    assert preflight["pass"]
    assert len(preflight["gitlinks"]) == len(CHIPYARD_BUILD_GITLINKS) == 25
    assert len(preflight["patched_files"]) == len(CHIPYARD_PATCHED_FILES) == 2
    assert all(item["pass"] for item in preflight["gitlinks"].values())
    assert all(item["pass"] for item in preflight["patched_files"].values())


def test_explicit_chipyard_override_is_honored(monkeypatch: pytest.MonkeyPatch) -> None:
    root = (PROJECT_ROOT / "chipyard").resolve()
    monkeypatch.setenv("AGENTSYS_CHIPYARD_ROOT", str(root))
    assert resolve_chipyard_root() == root


def test_invalid_chipyard_override_fails_closed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("AGENTSYS_CHIPYARD_ROOT", str(tmp_path))
    with pytest.raises(ChipyardPathError, match="incomplete"):
        resolve_chipyard_root()


def test_chipyard_manifest_tokens_expand_recursively() -> None:
    root = (PROJECT_ROOT / "chipyard").resolve()
    value = {
        "path": CHIPYARD_TOKEN,
        "argv": [f"{CHIPYARD_TOKEN}/bin/tool", "--version"],
        "nested": {"installed": f"{CHIPYARD_TOKEN}/overlay"},
    }
    assert expand_chipyard_tokens(value, chipyard_root=root) == {
        "path": str(root),
        "argv": [f"{root}/bin/tool", "--version"],
        "nested": {"installed": f"{root}/overlay"},
    }


def test_active_sources_have_no_machine_specific_chipyard_literal() -> None:
    roots = (
        PROJECT_ROOT / "src/agentsys",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "config",
        PROJECT_ROOT / "system_sim/software",
    )
    offenders: list[str] = []
    for root in roots:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix not in {".pyc"}:
                try:
                    text = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    continue
                if "/root/chipyard" in text:
                    offenders.append(str(path.relative_to(PROJECT_ROOT)))
    assert offenders == []

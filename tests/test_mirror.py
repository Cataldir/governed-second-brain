"""Tests for the operational-facade mirror sync.

These prove the second worked example of the Managed-File rule: canonical
sources under ``data/agents/`` regenerate byte-identical mirrors under
``.github/``, a hand-patched mirror is reported as drift, and a deleted
canonical source prunes its orphan mirror.
"""

from __future__ import annotations

from pathlib import Path

from governed_memory.mirror import (
    check_mirrors,
    plan_mirrors,
    sync_mirrors,
)


def _seed_canonical(repo_root: Path) -> None:
    """Lay down a small but representative canonical agent tree."""

    agents = repo_root / "data" / "agents"
    (agents / "prompts").mkdir(parents=True)
    (agents / "skills" / "memory-query").mkdir(parents=True)

    (agents / "README.md").write_text("# Agents\n", encoding="utf-8")
    (agents / "memory-curator.agent.md").write_text(
        "# Memory curator\nbody\n", encoding="utf-8"
    )
    (agents / "prompts" / "weekly-review.prompt.md").write_text(
        "weekly review prompt\n", encoding="utf-8"
    )
    (agents / "skills" / "memory-query" / "SKILL.md").write_text(
        "query skill\n", encoding="utf-8"
    )


def _read(repo_root: Path, rel: str) -> str:
    return (repo_root / rel).read_text(encoding="utf-8")


def test_plan_maps_each_subtree_to_its_mirror(tmp_path: Path) -> None:
    _seed_canonical(tmp_path)
    pairs = plan_mirrors(tmp_path)
    mirrors = {pair.mirror.relative_to(tmp_path).as_posix() for pair in pairs}
    assert mirrors == {
        ".github/agents/README.md",
        ".github/agents/memory-curator.agent.md",
        ".github/prompts/weekly-review.prompt.md",
        ".github/skills/memory-query/SKILL.md",
    }


def test_sync_regenerates_byte_identical_mirrors(tmp_path: Path) -> None:
    _seed_canonical(tmp_path)
    result = sync_mirrors(tmp_path)

    assert result.ok
    assert len(result.written) == 4
    assert not result.pruned
    # Mirror content is byte-identical to canonical.
    assert _read(tmp_path, ".github/agents/memory-curator.agent.md") == _read(
        tmp_path, "data/agents/memory-curator.agent.md"
    )
    assert _read(tmp_path, ".github/skills/memory-query/SKILL.md") == _read(
        tmp_path, "data/agents/skills/memory-query/SKILL.md"
    )


def test_second_sync_is_a_no_op(tmp_path: Path) -> None:
    _seed_canonical(tmp_path)
    sync_mirrors(tmp_path)
    again = sync_mirrors(tmp_path)
    assert again.ok
    assert not again.written
    assert not again.pruned


def test_check_passes_on_a_clean_tree(tmp_path: Path) -> None:
    _seed_canonical(tmp_path)
    sync_mirrors(tmp_path)
    result = check_mirrors(tmp_path)
    assert result.ok
    assert not result.drift


def test_check_detects_a_patched_mirror(tmp_path: Path) -> None:
    _seed_canonical(tmp_path)
    sync_mirrors(tmp_path)
    # A human hand-edits the mirror — the forbidden move.
    (tmp_path / ".github" / "agents" / "memory-curator.agent.md").write_text(
        "tampered\n", encoding="utf-8"
    )
    result = check_mirrors(tmp_path)
    assert not result.ok
    assert any("memory-curator.agent.md is stale" in d for d in result.drift)


def test_check_detects_a_missing_mirror(tmp_path: Path) -> None:
    _seed_canonical(tmp_path)
    sync_mirrors(tmp_path)
    (tmp_path / ".github" / "prompts" / "weekly-review.prompt.md").unlink()
    result = check_mirrors(tmp_path)
    assert not result.ok
    assert any("weekly-review.prompt.md is missing" in d for d in result.drift)


def test_check_detects_an_orphan_mirror(tmp_path: Path) -> None:
    _seed_canonical(tmp_path)
    sync_mirrors(tmp_path)
    # Canonical source deleted, but the mirror lingers.
    (tmp_path / "data" / "agents" / "memory-curator.agent.md").unlink()
    result = check_mirrors(tmp_path)
    assert not result.ok
    assert any("orphan mirror" in d for d in result.drift)


def test_sync_prunes_an_orphan_mirror(tmp_path: Path) -> None:
    _seed_canonical(tmp_path)
    sync_mirrors(tmp_path)
    (tmp_path / "data" / "agents" / "memory-curator.agent.md").unlink()
    result = sync_mirrors(tmp_path)
    assert result.ok
    assert any(
        p.as_posix() == ".github/agents/memory-curator.agent.md"
        for p in result.pruned
    )
    assert not (
        tmp_path / ".github" / "agents" / "memory-curator.agent.md"
    ).exists()

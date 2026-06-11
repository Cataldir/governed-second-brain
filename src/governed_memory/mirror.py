"""The operational-facade mirror sync — the second worked example of the
Managed-File rule.

The data plane already demonstrates "derived files are regenerated, never
patched": the SQLite index is built from the canonical log and reconciled by
``verify``. The *operational* plane needs the same discipline. Agent personas,
prompts, and skills are authored once, canonically, under ``data/agents/``; the
copies an agent runtime actually loads live under ``.github/`` and are
**generated mirrors**. A human edits the canonical source; the mirror is
regenerated, never hand-patched.

This module is the generator and the drift check, mirroring ``rebuild`` and
``verify`` for the operational plane:

- :func:`plan_mirrors` maps every canonical source to its mirror path.
- :func:`sync_mirrors` regenerates stale or missing mirrors and prunes mirror
  files whose canonical source has been deleted.
- :func:`check_mirrors` reports drift without writing anything, so it can sit in
  a hook or a CI step exactly like ``verify``.

The mapping is deterministic and content-faithful: a mirror is correct only if
it is byte-identical to its canonical source. No churn, no surprises.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

# Canonical operational sources live here, one tree, the single home of agent
# definitions, prompts, and skills.
CANONICAL_ROOT = Path("data/agents")

# Each canonical sub-tree projects into a .github mirror tree. Top-level files in
# the canonical root (the agent personas and the README) project into
# .github/agents/; the prompts/ and skills/ sub-trees project into their own
# mirror roots.
_SUBTREE_TARGETS: dict[str, Path] = {
    "prompts": Path(".github/prompts"),
    "skills": Path(".github/skills"),
}
_DEFAULT_TARGET = Path(".github/agents")


@dataclass(frozen=True, slots=True)
class MirrorPair:
    """A canonical source and the mirror path it must be byte-identical to."""

    source: Path
    mirror: Path


@dataclass(slots=True)
class SyncResult:
    """Outcome of a sync or check pass."""

    written: list[Path] = field(default_factory=list)
    pruned: list[Path] = field(default_factory=list)
    drift: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.drift

    def __str__(self) -> str:
        if self.drift:
            lines = [f"DRIFT — {len(self.drift)} mirror(s) out of sync:"]
            lines.extend(f"  - {message}" for message in self.drift)
            return "\n".join(lines)
        return (
            f"clean — mirrors match canonical "
            f"(written={len(self.written)}, pruned={len(self.pruned)})"
        )


def _mirror_for(source: Path, *, canonical_root: Path) -> Path:
    """Map a canonical source path to its mirror path."""

    relative = source.relative_to(canonical_root)
    first = relative.parts[0]
    target_root = _SUBTREE_TARGETS.get(first)
    if target_root is not None:
        # Strip the sub-tree name: data/agents/prompts/x -> .github/prompts/x
        return target_root / Path(*relative.parts[1:])
    return _DEFAULT_TARGET / relative


def plan_mirrors(repo_root: Path, *, canonical_root: Path = CANONICAL_ROOT) -> list[MirrorPair]:
    """Enumerate every canonical source and the mirror it must project into."""

    canonical = repo_root / canonical_root
    pairs: list[MirrorPair] = []
    for source in sorted(canonical.rglob("*")):
        if not source.is_file():
            continue
        mirror = _mirror_for(
            source.relative_to(repo_root), canonical_root=canonical_root
        )
        pairs.append(MirrorPair(source=source, mirror=repo_root / mirror))
    return pairs


def _expected_mirror_files(
    repo_root: Path, pairs: list[MirrorPair]
) -> set[Path]:
    return {pair.mirror for pair in pairs}


def _existing_mirror_files(repo_root: Path) -> set[Path]:
    found: set[Path] = set()
    for target_root in (_DEFAULT_TARGET, *_SUBTREE_TARGETS.values()):
        root = repo_root / target_root
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file():
                found.add(path)
    return found


def sync_mirrors(
    repo_root: Path,
    *,
    canonical_root: Path = CANONICAL_ROOT,
    check: bool = False,
) -> SyncResult:
    """Regenerate the operational mirrors from canonical sources.

    With ``check=True`` nothing is written; the result lists drift instead, so
    the same call can gate a commit. Without it, stale or missing mirrors are
    rewritten and mirror files whose canonical source no longer exists are
    pruned.
    """

    pairs = plan_mirrors(repo_root, canonical_root=canonical_root)
    result = SyncResult()

    expected = _expected_mirror_files(repo_root, pairs)
    existing = _existing_mirror_files(repo_root)

    for pair in pairs:
        source_bytes = pair.source.read_bytes()
        current = pair.mirror.read_bytes() if pair.mirror.exists() else None
        if current == source_bytes:
            continue
        rel = pair.mirror.relative_to(repo_root)
        if check:
            reason = "missing" if current is None else "stale"
            result.drift.append(f"{rel} is {reason} (canonical: {pair.source.relative_to(repo_root)})")
            continue
        pair.mirror.parent.mkdir(parents=True, exist_ok=True)
        pair.mirror.write_bytes(source_bytes)
        result.written.append(rel)

    for orphan in sorted(existing - expected):
        rel = orphan.relative_to(repo_root)
        if check:
            result.drift.append(f"{rel} is an orphan mirror (no canonical source)")
            continue
        orphan.unlink()
        result.pruned.append(rel)

    return result


def check_mirrors(
    repo_root: Path, *, canonical_root: Path = CANONICAL_ROOT
) -> SyncResult:
    """Report mirror drift without writing — the operational-plane gate."""

    return sync_mirrors(repo_root, canonical_root=canonical_root, check=True)

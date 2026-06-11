"""Command-line entry point for the governed-memory store.

Verbs that mirror the architecture:

    write    append a record to the canonical log (authority plane)
    rebuild  project the log into the derived index (--embed for vectors)
    verify   run the hard gate; non-zero exit on failure (the contract)
    query    summary-first retrieval (--mode lexical|semantic|hybrid)
    seed     load the example records so you can try it in one command
    state    record a workflow transition with evidence (state layer)
    history  show the transition history of a workflow entity

Defaults point at ``data/memory`` (governed append-only records),
``data/state`` (governed append-only transitions), and
``data/indexes/memory.sqlite`` (a derived index). That mirrors the four-plane
layout: canonical records and state live in ``data/``, runnable code in ``src/``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from governed_memory.embeddings import default_embedder
from governed_memory.events import (
    TransitionError,
    current_status,
    iter_events,
    record_transition,
)
from governed_memory.index import rebuild_index
from governed_memory.query import query
from governed_memory.records import MemoryRecord
from governed_memory.store import append_record
from governed_memory.verify import verify

DEFAULT_MEMORY_DIR = Path("data/memory")
DEFAULT_STATE_DIR = Path("data/state")
DEFAULT_DB_PATH = Path("data/indexes/memory.sqlite")


def _add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--memory-dir",
        type=Path,
        default=DEFAULT_MEMORY_DIR,
        help="directory holding the canonical JSONL log",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB_PATH,
        help="path to the derived SQLite index",
    )


def _cmd_write(args: argparse.Namespace) -> int:
    record = MemoryRecord(
        type=args.type,
        title=args.title,
        summary=args.summary,
        body=args.body or "",
        sensitivity=args.sensitivity,
        sources=args.source or [],
        tags=args.tag or [],
    )
    saved = append_record(
        record,
        args.memory_dir,
        acknowledge_restricted=args.acknowledge_restricted,
    )
    print(f"appended {saved.type} {saved.id}")
    return 0


def _cmd_rebuild(args: argparse.Namespace) -> int:
    embedder = default_embedder() if args.embed else None
    count = rebuild_index(args.memory_dir, args.db, embedder=embedder)
    suffix = " (with vectors)" if embedder is not None else ""
    print(f"rebuilt index from {count} record(s) -> {args.db}{suffix}")
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    result = verify(args.memory_dir, args.db)
    print(result)
    return 0 if result.ok else 1


def _cmd_query(args: argparse.Namespace) -> int:
    try:
        hits = query(
            args.db,
            args.text,
            limit=args.limit,
            open_body=args.open_body,
            reveal=args.reveal,
            mode=args.mode,
        )
    except ValueError as exc:
        print(str(exc))
        return 1
    if not hits:
        print("no matches")
        return 0
    for hit in hits:
        print(hit.render())
        print()
    return 0


def _cmd_state(args: argparse.Namespace) -> int:
    try:
        event = record_transition(
            args.entity,
            args.to_status,
            args.state_dir,
            evidence=args.evidence or [],
            note=args.note or "",
        )
    except TransitionError as exc:
        print(f"refused: {exc}")
        return 1
    arrow = f"{event.from_status or 'NEW'} -> {event.to_status}"
    print(f"recorded {event.entity}: {arrow}")
    if event.evidence:
        print("  evidence: " + ", ".join(event.evidence))
    print(f"  stored_at: {args.state_dir / 'events.jsonl'}")
    return 0


def _cmd_history(args: argparse.Namespace) -> int:
    events = [e for e in iter_events(args.state_dir) if e.entity == args.entity]
    if not events:
        print(f"no history for {args.entity!r}")
        return 0
    for event in events:
        arrow = f"{event.from_status or 'NEW'} -> {event.to_status}"
        line = f"{event.timestamp}  {arrow}"
        if event.evidence:
            line += "  [" + ", ".join(event.evidence) + "]"
        print(line)
    print(f"current: {current_status(args.state_dir, args.entity)}")
    return 0


def _cmd_seed(args: argparse.Namespace) -> int:
    from examples.seed_records import seed

    written = seed(args.memory_dir)
    print(f"seeded {written} record(s) into {args.memory_dir}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="governed-memory", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_write = sub.add_parser("write", help="append a record to the canonical log")
    _add_common(p_write)
    p_write.add_argument("--type", choices=["source", "concept"], required=True)
    p_write.add_argument("--title", required=True)
    p_write.add_argument("--summary", required=True)
    p_write.add_argument("--body", default="")
    p_write.add_argument(
        "--sensitivity",
        choices=["public", "private", "restricted"],
        default="private",
    )
    p_write.add_argument("--source", action="append", help="cited record id (repeatable)")
    p_write.add_argument("--tag", action="append", help="tag (repeatable)")
    p_write.add_argument("--acknowledge-restricted", action="store_true")
    p_write.set_defaults(func=_cmd_write)

    p_rebuild = sub.add_parser("rebuild", help="rebuild the derived index")
    _add_common(p_rebuild)
    p_rebuild.add_argument(
        "--embed",
        action="store_true",
        help="also compute summary vectors for semantic/hybrid search",
    )
    p_rebuild.set_defaults(func=_cmd_rebuild)

    p_verify = sub.add_parser("verify", help="run the integrity gate")
    _add_common(p_verify)
    p_verify.set_defaults(func=_cmd_verify)

    p_query = sub.add_parser("query", help="summary-first retrieval")
    _add_common(p_query)
    p_query.add_argument("text", help="free-text query")
    p_query.add_argument("--limit", type=int, default=5)
    p_query.add_argument(
        "--mode",
        choices=["lexical", "semantic", "hybrid"],
        default="lexical",
        help="recall signal: lexical (FTS, default), semantic (vectors), or hybrid",
    )
    p_query.add_argument("--open-body", action="store_true", help="include record bodies")
    p_query.add_argument(
        "--reveal",
        action="store_true",
        help="authorise bodies of non-public records (off by default)",
    )
    p_query.set_defaults(func=_cmd_query)

    p_seed = sub.add_parser("seed", help="load the example records")
    _add_common(p_seed)
    p_seed.set_defaults(func=_cmd_seed)

    p_state = sub.add_parser("state", help="record a workflow transition with evidence")
    p_state.add_argument(
        "--state-dir", type=Path, default=DEFAULT_STATE_DIR,
        help="directory holding the append-only state event log",
    )
    p_state.add_argument("--entity", required=True, help="the workflow entity id")
    p_state.add_argument("--to-status", required=True, help="target status")
    p_state.add_argument(
        "--evidence", action="append", help="evidence reference (repeatable)"
    )
    p_state.add_argument("--note", default="", help="optional human note")
    p_state.set_defaults(func=_cmd_state)

    p_history = sub.add_parser("history", help="show an entity's transition history")
    p_history.add_argument(
        "--state-dir", type=Path, default=DEFAULT_STATE_DIR,
        help="directory holding the append-only state event log",
    )
    p_history.add_argument("--entity", required=True)
    p_history.set_defaults(func=_cmd_history)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())

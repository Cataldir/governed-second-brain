"""Command-line entry point for the governed-memory store.

Five verbs that mirror the architecture:

    write    append a record to the canonical log (authority plane)
    rebuild  project the log into the derived index (execution plane)
    verify   run the hard gate; non-zero exit on failure (the contract)
    query    summary-first retrieval against the index
    seed     load the example records so you can try it in one command

Defaults point at ``data/memory`` (governed append-only outputs) and
``data/indexes/memory.sqlite`` (a derived index). That mirrors the four-plane
layout: canonical records live in ``data/``, runnable code in ``src/``.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from governed_memory.index import rebuild_index
from governed_memory.query import query
from governed_memory.records import MemoryRecord
from governed_memory.store import append_record
from governed_memory.verify import verify

DEFAULT_MEMORY_DIR = Path("data/memory")
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
    count = rebuild_index(args.memory_dir, args.db)
    print(f"rebuilt index from {count} record(s) -> {args.db}")
    return 0


def _cmd_verify(args: argparse.Namespace) -> int:
    result = verify(args.memory_dir, args.db)
    print(result)
    return 0 if result.ok else 1


def _cmd_query(args: argparse.Namespace) -> int:
    hits = query(args.db, args.text, limit=args.limit, open_body=args.open_body)
    if not hits:
        print("no matches")
        return 0
    for hit in hits:
        print(hit.render())
        print()
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
    p_rebuild.set_defaults(func=_cmd_rebuild)

    p_verify = sub.add_parser("verify", help="run the integrity gate")
    _add_common(p_verify)
    p_verify.set_defaults(func=_cmd_verify)

    p_query = sub.add_parser("query", help="summary-first retrieval")
    _add_common(p_query)
    p_query.add_argument("text", help="free-text query")
    p_query.add_argument("--limit", type=int, default=5)
    p_query.add_argument("--open-body", action="store_true", help="include record bodies")
    p_query.set_defaults(func=_cmd_query)

    p_seed = sub.add_parser("seed", help="load the example records")
    _add_common(p_seed)
    p_seed.set_defaults(func=_cmd_seed)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())

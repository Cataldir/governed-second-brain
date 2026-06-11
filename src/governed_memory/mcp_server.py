"""A local, gated, stdio MCP server over the governed memory store.

This is the *execution-plane* write surface. It exposes the same store the CLI
uses, but across the Model Context Protocol so an agent runtime can reach it.
It is the component the governance instructions point at — and the reason it is
safe to expose is the gate, not the absence of a server.

Security posture, mirrored from the parent reference implementation:

- **Local stdio only.** No HTTP, no network bind. Nothing here listens on a
  socket or ships a record off the machine.
- **Writes default-off.** ``memory.append``, ``memory.rebuild``,
  ``memory.record_event`` and ``mirror.sync`` are refused unless
  ``GOVERNED_MEMORY_ENABLE_WRITE=true`` *and*
  ``GOVERNED_MEMORY_REQUIRE_APPROVAL=false`` — a two-step, deliberate opt-in.
- **Restricted records need acknowledgement.** Writing ``sensitivity=restricted``
  requires ``acknowledge_restricted=true``, enforced by the store itself.
- **Reads are always available, but non-public bodies are redacted.**
  ``memory.query`` works regardless of the gate; the body of a ``private`` or
  ``restricted`` record is returned only when ``reveal=true`` is also passed.
- **Mirror drift is readable; regeneration is gated.** ``mirror.check`` reports
  operational-mirror drift and is always available; ``mirror.sync`` regenerates
  the ``.github`` mirror from canonical ``data/agents/`` sources and is gated
  like every other write.

Run it:

    GOVERNED_MEMORY_ENABLE_WRITE=true GOVERNED_MEMORY_REQUIRE_APPROVAL=false \
        python -m governed_memory.mcp_server

Leaving the variables unset starts a read-only server — the safe default.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from governed_memory.embeddings import default_embedder
from governed_memory.events import TransitionError, current_status, record_transition
from governed_memory.gate import GatePolicy, write_gate_error
from governed_memory.index import rebuild_index
from governed_memory.mirror import check_mirrors, sync_mirrors
from governed_memory.query import query as query_store
from governed_memory.records import MemoryRecord, RecordValidationError
from governed_memory.store import append_record

DEFAULT_MEMORY_DIR = Path("data/memory")
DEFAULT_STATE_DIR = Path("data/state")
DEFAULT_DB_PATH = Path("data/indexes/memory.sqlite")

server = Server("governed-memory")


def _text(payload: dict[str, Any], *, status: str = "ok") -> list[TextContent]:
    return [
        TextContent(
            type="text",
            text=json.dumps({"status": status, **payload}, indent=2),
        )
    ]


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="memory.query",
            description=(
                "Summary-first retrieval. Returns titles and summaries; bodies "
                "only when open_body is true. Bodies of non-public records are "
                "redacted unless reveal is also true. mode selects the recall "
                "signal: lexical (FTS, default), semantic (vectors) or hybrid. "
                "Always available (read-only)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "limit": {"type": "integer", "default": 5},
                    "open_body": {"type": "boolean", "default": False},
                    "reveal": {"type": "boolean", "default": False},
                    "mode": {
                        "type": "string",
                        "enum": ["lexical", "semantic", "hybrid"],
                        "default": "lexical",
                    },
                },
                "required": ["text"],
            },
        ),
        Tool(
            name="memory.append",
            description=(
                "Append one record to the canonical append-only log. GATED: "
                "refused unless write mode is explicitly enabled. A 'restricted' "
                "record requires acknowledge_restricted=true."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {"type": "string", "enum": ["source", "concept"]},
                    "title": {"type": "string"},
                    "summary": {"type": "string"},
                    "body": {"type": "string", "default": ""},
                    "sensitivity": {
                        "type": "string",
                        "enum": ["public", "private", "restricted"],
                        "default": "private",
                    },
                    "sources": {"type": "array", "items": {"type": "string"}},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "acknowledge_restricted": {"type": "boolean", "default": False},
                },
                "required": ["type", "title", "summary"],
                "allOf": [
                    {
                        "if": {
                            "properties": {"sensitivity": {"const": "restricted"}},
                            "required": ["sensitivity"],
                        },
                        "then": {
                            "properties": {
                                "acknowledge_restricted": {"const": True}
                            },
                            "required": ["acknowledge_restricted"],
                        },
                    }
                ],
            },
        ),
        Tool(
            name="memory.rebuild",
            description=(
                "Rebuild the derived SQLite index from the canonical log. Set "
                "embed=true to also compute summary vectors for semantic search. "
                "GATED: refused unless write mode is explicitly enabled."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "embed": {"type": "boolean", "default": False},
                },
            },
        ),
        Tool(
            name="memory.record_event",
            description=(
                "Record one workflow transition with evidence in the append-only "
                "state log. Answers: which entity, what transition, what evidence, "
                "is it allowed from the current status, where stored. Refused if "
                "the transition is not allowed from the current status. GATED: "
                "refused unless write mode is explicitly enabled."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "entity": {"type": "string"},
                    "to_status": {"type": "string"},
                    "evidence": {"type": "array", "items": {"type": "string"}},
                    "note": {"type": "string", "default": ""},
                },
                "required": ["entity", "to_status"],
            },
        ),
        Tool(
            name="mirror.check",
            description=(
                "Report operational-mirror drift without writing anything. "
                "Compares the .github agent/prompt/skill mirrors against their "
                "canonical sources under data/agents/ and lists any that are "
                "stale, missing, or orphaned. Always available (read-only); the "
                "same check the CLI exposes as 'sync-mirrors --check'."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_root": {"type": "string", "default": "."},
                },
            },
        ),
        Tool(
            name="mirror.sync",
            description=(
                "Regenerate the .github operational mirrors from canonical "
                "sources under data/agents/: rewrite stale or missing mirrors and "
                "prune orphans whose canonical source was deleted. Mirrors are "
                "byte-identical to canonical and must never be hand-edited. "
                "GATED: refused unless write mode is explicitly enabled."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "repo_root": {"type": "string", "default": "."},
                },
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    policy = GatePolicy.from_env()

    blocked = write_gate_error(name, policy)
    if blocked is not None:
        return _text({"error": blocked}, status="error")

    memory_dir = Path(arguments.get("memory_dir", DEFAULT_MEMORY_DIR))
    state_dir = Path(arguments.get("state_dir", DEFAULT_STATE_DIR))
    db_path = Path(arguments.get("db", DEFAULT_DB_PATH))

    if name == "memory.query":
        try:
            hits = query_store(
                db_path,
                arguments["text"],
                limit=int(arguments.get("limit", 5)),
                open_body=bool(arguments.get("open_body", False)),
                reveal=bool(arguments.get("reveal", False)),
                mode=arguments.get("mode", "lexical"),
            )
        except (FileNotFoundError, ValueError) as exc:
            return _text({"error": str(exc)}, status="error")
        return _text(
            {
                "hits": [
                    {
                        "id": hit.id,
                        "type": hit.type,
                        "title": hit.title,
                        "summary": hit.summary,
                        "sensitivity": hit.sensitivity,
                        "body": hit.body,
                        "redacted": hit.redacted,
                    }
                    for hit in hits
                ]
            }
        )

    if name == "memory.append":
        record = MemoryRecord(
            type=arguments["type"],
            title=arguments["title"],
            summary=arguments["summary"],
            body=arguments.get("body", ""),
            sensitivity=arguments.get("sensitivity", "private"),
            sources=list(arguments.get("sources", [])),
            tags=list(arguments.get("tags", [])),
        )
        try:
            saved = append_record(
                record,
                memory_dir,
                acknowledge_restricted=bool(
                    arguments.get("acknowledge_restricted", False)
                ),
            )
        except RecordValidationError as exc:
            return _text({"error": str(exc)}, status="error")
        return _text({"id": saved.id, "type": saved.type})

    if name == "memory.rebuild":
        embedder = default_embedder() if arguments.get("embed", False) else None
        count = rebuild_index(memory_dir, db_path, embedder=embedder)
        return _text(
            {"records_indexed": count, "vectors": embedder is not None}
        )

    if name == "memory.record_event":
        try:
            event = record_transition(
                arguments["entity"],
                arguments["to_status"],
                state_dir,
                evidence=list(arguments.get("evidence", [])),
                note=arguments.get("note", ""),
            )
        except TransitionError as exc:
            return _text({"error": str(exc)}, status="error")
        return _text(
            {
                "entity": event.entity,
                "event": f"{event.from_status or 'NEW'} -> {event.to_status}",
                "current_status": current_status(state_dir, event.entity),
                "stored_at": str(state_dir / "events.jsonl"),
                "evidence": event.evidence,
            },
            status="recorded",
        )

    if name == "mirror.check":
        result = check_mirrors(Path(arguments.get("repo_root", ".")))
        return _text(
            {"drift": result.drift, "clean": result.ok},
            status="ok" if result.ok else "drift",
        )

    if name == "mirror.sync":
        result = sync_mirrors(Path(arguments.get("repo_root", ".")))
        return _text(
            {
                "written": [str(path) for path in result.written],
                "pruned": [str(path) for path in result.pruned],
                "clean": result.ok,
            },
            status="synced",
        )

    return _text({"error": f"unknown tool {name}"}, status="error")


async def _run() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


def main() -> None:
    import asyncio

    asyncio.run(_run())


if __name__ == "__main__":
    main()

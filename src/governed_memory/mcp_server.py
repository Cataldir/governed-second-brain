"""A local, gated, stdio MCP server over the governed memory store.

This is the *execution-plane* write surface. It exposes the same store the CLI
uses, but across the Model Context Protocol so an agent runtime can reach it.
It is the component the governance instructions point at — and the reason it is
safe to expose is the gate, not the absence of a server.

Security posture, mirrored from the parent reference implementation:

- **Local stdio only.** No HTTP, no network bind. Nothing here listens on a
  socket or ships a record off the machine.
- **Writes default-off.** ``memory.append`` and ``memory.rebuild`` are refused
  unless ``GOVERNED_MEMORY_ENABLE_WRITE=true`` *and*
  ``GOVERNED_MEMORY_REQUIRE_APPROVAL=false`` — a two-step, deliberate opt-in.
- **Restricted records need acknowledgement.** Writing ``sensitivity=restricted``
  requires ``acknowledge_restricted=true``, enforced by the store itself.
- **Reads are always available.** ``memory.query`` works regardless of the gate.

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

from governed_memory.gate import GatePolicy, write_gate_error
from governed_memory.index import rebuild_index
from governed_memory.query import query as query_store
from governed_memory.records import MemoryRecord, RecordValidationError
from governed_memory.store import append_record

DEFAULT_MEMORY_DIR = Path("data/memory")
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
                "only when open_body is true. Always available (read-only)."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "limit": {"type": "integer", "default": 5},
                    "open_body": {"type": "boolean", "default": False},
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
                "Rebuild the derived SQLite index from the canonical log. GATED: "
                "refused unless write mode is explicitly enabled."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    policy = GatePolicy.from_env()

    blocked = write_gate_error(name, policy)
    if blocked is not None:
        return _text({"error": blocked}, status="error")

    memory_dir = Path(arguments.get("memory_dir", DEFAULT_MEMORY_DIR))
    db_path = Path(arguments.get("db", DEFAULT_DB_PATH))

    if name == "memory.query":
        try:
            hits = query_store(
                db_path,
                arguments["text"],
                limit=int(arguments.get("limit", 5)),
                open_body=bool(arguments.get("open_body", False)),
            )
        except FileNotFoundError as exc:
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
        count = rebuild_index(memory_dir, db_path)
        return _text({"records_indexed": count})

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

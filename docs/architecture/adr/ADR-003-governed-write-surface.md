# ADR-003 — The governed write surface is execution-plane, default-off, local-only

- Status: accepted
- Date: 2025

## Context

The store is reachable two ways: an in-process CLI/library, and an MCP server
that lets an agent runtime call it across the Model Context Protocol. The MCP
server is the interesting one, because it is the point where automation — not a
human at a prompt — can mutate the canonical log.

A naive "second brain + MCP" wiring is exactly where these systems leak: a
write tool that is always on, reachable over the network, with no
acknowledgement step for sensitive material. The governance instructions in
this repository therefore cannot treat the write server as incidental code. The
server *is* the governed write path, and its safety is a property of how it is
gated.

## Decision

1. **Plane.** The MCP server lives in the execution plane (`src/`). It is code,
   not policy. But the operational plane (`.github/instructions/`) names its
   path directly and binds rules to it — see *Enforcement*.

2. **Local stdio only.** The server speaks stdio. It does not bind a socket, does
   not expose HTTP, and does not transmit records off the machine. Wiring it to a
   remote transport is out of scope and would require its own ADR.

3. **Writes are default-off behind a two-flag opt-in.** The mutating tools
   (`memory.append`, `memory.rebuild`) are refused unless *both*
   `GOVERNED_MEMORY_ENABLE_WRITE=true` *and* `GOVERNED_MEMORY_REQUIRE_APPROVAL=false`.
   Two independent flags make "on" a deliberate act, not a single accidental
   toggle. Reads (`memory.query`) are never gated.

4. **Restricted records require acknowledgement.** A `restricted` write requires
   `acknowledge_restricted=true`, enforced by the store, not merely by the tool
   schema. Sensitive material is opt-in at the moment of writing.

## Consequences

- Exposing the store over MCP is safe *because of* the gate, not despite the
  absence of a server. The reproduction is faithful: the gated write surface is
  the intent, not an optional extra.
- The read/write asymmetry — recall always available, mutation privileged —
  keeps the common path (querying memory) frictionless while making the rare,
  consequential path (changing the record of truth) explicit.
- The cost is that an operator who genuinely wants automated writes must set two
  environment variables. That friction is intentional.

## Enforcement

- The gate is implemented as pure, tested policy in
  `src/governed_memory/gate.py` (`GatePolicy`, `write_gate_error`) and covered by
  `tests/test_gate.py`.
- The server wiring is `src/governed_memory/mcp_server.py`.
- [`sqlite-read-model-boundary.instructions.md`](../../../.github/instructions/sqlite-read-model-boundary.instructions.md)
  names the server path in its `applyTo`.
- [`interaction-capture.instructions.md`](../../../.github/instructions/interaction-capture.instructions.md)
  describes the gate as the condition under which governed capture may occur.

"""The write gate — pure, testable policy with no MCP dependency.

This module is the security layer of the MCP surface, factored out so it can be
unit-tested without standing up a server. It mirrors the parent reference
implementation's two-flag pattern:

- writes are **disabled by default**;
- enabling them requires *both* turning write mode on *and* turning the
  approval requirement off — a deliberate, two-step, opt-in action;
- a ``restricted`` record additionally requires an explicit acknowledgement,
  so sensitive material is never written by an automated caller by accident.

Reads are never gated. The asymmetry is the point: recall is cheap and safe;
mutation is privileged and explicit.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

# Tools that mutate governed state. Everything else is read-only.
# ``memory.record_event`` appends a transition to the state log, so it is a
# mutation and is gated exactly like writes to the canonical record log.
MUTATING_TOOLS = frozenset(
    {"memory.append", "memory.rebuild", "memory.record_event"}
)

ENABLE_WRITE_ENV = "GOVERNED_MEMORY_ENABLE_WRITE"
REQUIRE_APPROVAL_ENV = "GOVERNED_MEMORY_REQUIRE_APPROVAL"


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True, slots=True)
class GatePolicy:
    """Resolved write-gate policy. Defaults deny writes."""

    enable_write: bool = False
    require_approval: bool = True

    @classmethod
    def from_env(cls) -> GatePolicy:
        """Read the policy from the environment. Safe defaults: writes denied."""

        return cls(
            enable_write=_env_bool(ENABLE_WRITE_ENV, False),
            require_approval=_env_bool(REQUIRE_APPROVAL_ENV, True),
        )

    @property
    def writes_allowed(self) -> bool:
        """Writes are allowed only when explicitly enabled AND approval waived."""

        return self.enable_write and not self.require_approval


def write_gate_error(tool_name: str, policy: GatePolicy) -> str | None:
    """Return an error string if the tool is blocked, else None.

    Read-only tools always pass. Mutating tools pass only when the policy
    explicitly allows writes.
    """

    if tool_name not in MUTATING_TOOLS:
        return None
    if policy.writes_allowed:
        return None
    return (
        f"{tool_name} is disabled. This is the safe default. To enable governed "
        f"writes, set {ENABLE_WRITE_ENV}=true and {REQUIRE_APPROVAL_ENV}=false "
        "after a deliberate, manual approval. Reads remain available."
    )

"""Tests for the MCP write gate.

The gate is the security layer that makes exposing the store over MCP safe. The
tests below prove the two properties that matter:

1. writes are denied by default and require an explicit two-flag opt-in;
2. reads are never gated.

The restricted-sensitivity acknowledgement is enforced by the store itself and
is covered in ``test_memory.py``; here we only verify the tool-level gate.
"""

from __future__ import annotations

import pytest

from governed_memory.gate import (
    ENABLE_WRITE_ENV,
    REQUIRE_APPROVAL_ENV,
    GatePolicy,
    write_gate_error,
)


def test_default_policy_denies_writes() -> None:
    policy = GatePolicy()
    assert policy.writes_allowed is False
    assert write_gate_error("memory.append", policy) is not None
    assert write_gate_error("memory.rebuild", policy) is not None


def test_reads_are_never_gated() -> None:
    policy = GatePolicy()  # most restrictive
    assert write_gate_error("memory.query", policy) is None


def test_enabling_requires_both_flags() -> None:
    # Enabling write alone is not enough — approval must also be waived.
    only_enabled = GatePolicy(enable_write=True, require_approval=True)
    assert only_enabled.writes_allowed is False
    assert write_gate_error("memory.append", only_enabled) is not None

    # Waiving approval alone is not enough either.
    only_waived = GatePolicy(enable_write=False, require_approval=False)
    assert only_waived.writes_allowed is False

    # Both together open the gate.
    open_gate = GatePolicy(enable_write=True, require_approval=False)
    assert open_gate.writes_allowed is True
    assert write_gate_error("memory.append", open_gate) is None


def test_from_env_defaults_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv(ENABLE_WRITE_ENV, raising=False)
    monkeypatch.delenv(REQUIRE_APPROVAL_ENV, raising=False)
    assert GatePolicy.from_env().writes_allowed is False


def test_from_env_opt_in(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(ENABLE_WRITE_ENV, "true")
    monkeypatch.setenv(REQUIRE_APPROVAL_ENV, "false")
    assert GatePolicy.from_env().writes_allowed is True

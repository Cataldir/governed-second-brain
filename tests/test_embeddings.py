"""Tests for the pluggable embedding layer.

These prove the properties semantic retrieval leans on: determinism (a query
vector is comparable to one written at rebuild time), normalisation, cosine
bounds, the summary-only invariant (a body never enters the vector text), and a
lossless pack/unpack round trip.
"""

from __future__ import annotations

import math

from governed_memory.embeddings import (
    HashingEmbedder,
    cosine,
    embedding_text,
    pack_vector,
    unpack_vector,
)
from governed_memory.records import MemoryRecord


def test_embedder_is_deterministic() -> None:
    a = HashingEmbedder().embed(["append-only audit trail"])[0]
    b = HashingEmbedder().embed(["append-only audit trail"])[0]
    assert a == b


def test_vectors_are_l2_normalised() -> None:
    vector = HashingEmbedder().embed(["some navigation text here"])[0]
    norm = math.sqrt(sum(v * v for v in vector))
    assert abs(norm - 1.0) < 1e-6


def test_identical_text_is_maximally_similar() -> None:
    embedder = HashingEmbedder()
    text = "verifiable change history"
    a, b = embedder.embed([text, text])
    assert abs(cosine(a, b) - 1.0) < 1e-6


def test_unrelated_text_is_less_similar_than_shared_text() -> None:
    embedder = HashingEmbedder()
    base, shared, unrelated = embedder.embed(
        [
            "append only log of changes",
            "append only change log",
            "tropical fruit smoothie recipe",
        ]
    )
    assert cosine(base, shared) > cosine(base, unrelated)


def test_embedding_text_excludes_body() -> None:
    record = MemoryRecord(
        type="source",
        title="Title words",
        summary="Summary words",
        body="SECRET body words that must never be embedded",
        tags=["tag-word"],
    )
    text = embedding_text(record)
    assert "Title words" in text
    assert "Summary words" in text
    assert "tag-word" in text
    assert "SECRET" not in text


def test_pack_unpack_roundtrip() -> None:
    vector = HashingEmbedder(dim=16).embed(["round trip"])[0]
    restored = unpack_vector(pack_vector(vector))
    assert len(restored) == len(vector)
    for original, value in zip(vector, restored):
        assert abs(original - value) < 1e-6


def test_empty_text_yields_zero_vector_and_zero_cosine() -> None:
    embedder = HashingEmbedder()
    empty = embedder.embed([""])[0]
    other = embedder.embed(["something"])[0]
    assert all(v == 0.0 for v in empty)
    assert cosine(empty, other) == 0.0

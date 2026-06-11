"""Optional semantic retrieval — pluggable, summary-only, dependency-free default.

The repository's lexical path (FTS5 over title/summary/tags) is the floor. This
module adds a *second* recall signal: vector similarity. It exists for the case
the README is honest about — once the corpus is large enough that keyword
matching misses a paraphrase, you want a query about "audit trail" to surface a
record titled "verifiable change history" even with no shared words.

Three rules keep this faithful to the rest of the architecture:

1. **Summaries only, never bodies.** Vectors are built from ``title``,
   ``summary`` and ``tags`` — the same navigation text the FTS index covers, and
   deliberately *not* ``body``. A private body is never embedded, so the vector
   index cannot become a side channel that leaks sensitive content past the
   visibility floor.
2. **Derived and disposable.** Vectors live in the SQLite index, regenerated on
   ``rebuild``. They are never a source of truth.
3. **Pluggable.** Retrieval depends on the small :class:`Embedder` protocol, not
   on any particular model. The built-in :class:`HashingEmbedder` is stdlib-only
   and deterministic, so the default install stays dependency-free. It captures
   *lexical* overlap with some fuzziness — enough to demonstrate vector recall
   and hybrid fusion end to end. To catch genuine paraphrases (synonyms,
   rephrasings) plug a real semantic model in behind the same protocol; nothing
   else in the pipeline changes.
"""

from __future__ import annotations

import hashlib
import math
import re
from array import array
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from governed_memory.records import MemoryRecord

_TOKEN = re.compile(r"\w+", re.UNICODE)


@runtime_checkable
class Embedder(Protocol):
    """A text-to-vector encoder.

    Implementations must be deterministic for a given input so that a query
    vector is comparable to vectors written at rebuild time. ``embed`` returns
    one L2-normalised vector of length :attr:`dim` per input string.
    """

    name: str
    dim: int

    def embed(self, texts: list[str]) -> list[list[float]]: ...


def embedding_text(record: MemoryRecord) -> str:
    """Build the text a record is embedded from: navigation fields, never body.

    This mirrors the FTS index columns exactly. Keeping body out is the
    invariant that lets us embed a ``private`` record without leaking its
    sensitive text into the vector space.
    """

    return " ".join(
        part for part in (record.title, record.summary, " ".join(record.tags)) if part
    )


def _tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def _features(text: str) -> list[str]:
    """Words, word bigrams, and character trigrams — a little fuzziness."""

    words = _tokens(text)
    features = list(words)
    features.extend(f"{a}_{b}" for a, b in zip(words, words[1:]))
    joined = " ".join(words)
    features.extend(joined[i : i + 3] for i in range(max(0, len(joined) - 2)))
    return features


def _bucket_and_sign(feature: str, dim: int) -> tuple[int, float]:
    # blake2b gives a process-stable digest; Python's built-in hash() is salted
    # per interpreter run and would make vectors non-comparable across rebuilds.
    digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
    value = int.from_bytes(digest, "big")
    bucket = value % dim
    sign = 1.0 if (value >> 63) & 1 else -1.0
    return bucket, sign


class HashingEmbedder:
    """Deterministic, dependency-free feature-hashing encoder.

    Signed feature hashing into a fixed-dimension vector, then L2-normalised.
    It is lexical at heart — its recall overlaps with FTS — but it exercises the
    full vector path so semantic and hybrid modes are real, not stubs.
    """

    def __init__(self, dim: int = 256) -> None:
        if dim <= 0:
            raise ValueError("dim must be positive")
        self.name = "hashing-v1"
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        vector = [0.0] * self.dim
        for feature in _features(text):
            bucket, sign = _bucket_and_sign(feature, self.dim)
            vector[bucket] += sign
        norm = math.sqrt(sum(value * value for value in vector))
        if norm == 0.0:
            return vector
        return [value / norm for value in vector]


def default_embedder() -> Embedder:
    """The built-in encoder used unless a caller supplies its own."""

    return HashingEmbedder()


def embedder_from_meta(name: str, dim: int) -> Embedder:
    """Reconstruct the encoder recorded in the index meta, to embed a query.

    Only the built-in encoder is known here. A deployment that plugged in a
    custom :class:`Embedder` is responsible for reconstructing it the same way
    and passing it to :func:`governed_memory.query.query`.
    """

    if name == "hashing-v1":
        return HashingEmbedder(dim=dim)
    raise ValueError(
        f"unknown embedder {name!r} in index meta; rebuilt with a custom "
        "embedder? pass it explicitly to query()"
    )


def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity of two equal-length vectors. Zero vectors score 0."""

    if len(a) != len(b):
        raise ValueError("vectors differ in length")
    dot = sum(x * y for x, y in zip(a, b))
    # Vectors from this module are pre-normalised, but do not assume it.
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def pack_vector(vector: list[float]) -> bytes:
    """Pack a vector into a compact BLOB for SQLite storage."""

    return array("f", vector).tobytes()


def unpack_vector(blob: bytes) -> list[float]:
    """Unpack a BLOB written by :func:`pack_vector`."""

    out = array("f")
    out.frombytes(blob)
    return list(out)

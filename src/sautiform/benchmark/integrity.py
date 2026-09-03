"""Cryptographic integrity helpers for frozen benchmark manifests."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

_SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def sha256_file(path: Path) -> str:
    """Return the lowercase SHA-256 digest of a file."""
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sha256(path: Path, expected: str) -> str:
    """Verify a file against an explicit expected SHA-256 digest."""
    expected = expected.strip().lower()
    if not _SHA256_PATTERN.fullmatch(expected):
        raise ValueError("expected SHA-256 must be exactly 64 hexadecimal characters")

    actual = sha256_file(path)
    if actual != expected:
        raise ValueError(
            f"manifest SHA-256 mismatch: expected {expected}, actual {actual}"
        )
    return actual

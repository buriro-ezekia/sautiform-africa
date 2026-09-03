"""Tests for frozen-manifest SHA-256 integrity checks."""
from pathlib import Path

import pytest

from sautiform.benchmark.integrity import sha256_file, verify_sha256


def test_verify_sha256_accepts_matching_digest(tmp_path: Path):
    path = tmp_path / "manifest.jsonl"
    path.write_text('{"sample_id":"x"}\n', encoding="utf-8")
    expected = sha256_file(path)
    assert verify_sha256(path, expected) == expected


def test_verify_sha256_rejects_mismatch(tmp_path: Path):
    path = tmp_path / "manifest.jsonl"
    path.write_text("content\n", encoding="utf-8")
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        verify_sha256(path, "0" * 64)


def test_verify_sha256_rejects_invalid_expected_digest(tmp_path: Path):
    path = tmp_path / "manifest.jsonl"
    path.write_text("content\n", encoding="utf-8")
    with pytest.raises(ValueError, match="64 hexadecimal"):
        verify_sha256(path, "not-a-digest")

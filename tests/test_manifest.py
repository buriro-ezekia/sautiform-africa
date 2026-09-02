"""Tests for benchmark provenance, consent and schema validation."""
import json
from pathlib import Path

import pytest

from sautiform.benchmark.manifest import (
    load_validated_manifest,
    validate_manifest_item,
)


def _row(audio_path: str) -> dict[str, object]:
    return {
        "sample_id": "tz-sw-en-001",
        "audio_path": audio_path,
        "reference_transcript": "Ninaishi Mbozi District",
        "reference_fields": {
            "district": "Mbozi",
            "occupation": "farmer",
            "household_size": 6,
            "service_request": "birth certificate",
        },
        "metadata": {
            "language_pair": "sw-en",
            "country": "Tanzania",
            "device": "phone",
            "noise": "quiet",
            "consented": True,
        },
    }


def test_manifest_requires_explicit_consent():
    row = _row("sample.wav")
    metadata = row["metadata"]
    assert isinstance(metadata, dict)
    metadata["consented"] = False
    errors = validate_manifest_item(row, check_audio=False)
    assert "metadata.consented must be true" in errors


def test_manifest_accepts_complete_row_without_audio_check():
    assert validate_manifest_item(
        _row("sample.wav"),
        check_audio=False,
    ) == []


def test_manifest_rejects_duplicate_sample_ids(tmp_path: Path):
    row = _row("sample.wav")
    manifest = tmp_path / "manifest.jsonl"
    payload = json.dumps(row)
    manifest.write_text(payload + "\n" + payload + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate sample_id"):
        load_validated_manifest(manifest, check_audio=False)

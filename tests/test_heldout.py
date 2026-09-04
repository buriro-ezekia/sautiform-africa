"""Tests for fixed held-out benchmark integrity checks."""
from pathlib import Path

from sautiform.benchmark.heldout import EXPECTED_HELDOUT_IDS, validate_heldout_rows


def _rows() -> list[dict[str, object]]:
    return [
        {
            "sample_id": sample_id,
            "audio_path": (
                Path("data/private/heldout/audio") / f"{sample_id}.ogg"
            ).as_posix(),
        }
        for sample_id in EXPECTED_HELDOUT_IDS
    ]


def test_complete_heldout_design_passes():
    assert validate_heldout_rows(_rows()) == []


def test_missing_row_is_rejected():
    errors = validate_heldout_rows(_rows()[:-1])
    assert any("exactly 24 rows" in error for error in errors)
    assert any("missing held-out sample IDs" in error for error in errors)


def test_unexpected_development_id_is_rejected():
    rows = _rows()
    rows[0]["sample_id"] = "tz-sw-en-001"
    errors = validate_heldout_rows(rows)
    assert any("unexpected held-out sample IDs" in error for error in errors)
    assert any("development sample IDs present" in error for error in errors)


def test_audio_must_live_under_heldout_root():
    rows = _rows()
    rows[0]["audio_path"] = "data/private/audio/tz-sw-en-h001.ogg"
    errors = validate_heldout_rows(rows)
    assert any("audio_path must be under" in error for error in errors)


def test_duplicate_audio_path_is_rejected():
    rows = _rows()
    rows[1]["audio_path"] = rows[0]["audio_path"]
    errors = validate_heldout_rows(rows)
    assert "held-out manifest contains duplicate audio paths" in errors

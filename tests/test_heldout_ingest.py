"""Tests for held-out batch-ingestion helpers."""
import json
from pathlib import Path

import pytest

from sautiform.benchmark.heldout import EXPECTED_HELDOUT_IDS
from sautiform.benchmark.heldout_ingest import (
    load_heldout_plan,
    resolve_source_audio,
)


def _write_plan(path: Path) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for sample_id in EXPECTED_HELDOUT_IDS:
            handle.write(
                json.dumps(
                    {
                        "sample_id": sample_id,
                        "reference_transcript": "sample",
                        "reference_fields": {
                            "district": "Mbozi",
                            "occupation": "farmer",
                            "household_size": 2,
                            "service_request": "birth certificate",
                        },
                        "recording_cell": "a_quiet",
                    }
                )
                + "\n"
            )


def test_load_fixed_heldout_plan(tmp_path: Path):
    plan = tmp_path / "plan.jsonl"
    _write_plan(plan)
    rows = load_heldout_plan(plan)
    assert len(rows) == 24
    assert rows[0]["sample_id"] == "tz-sw-en-h001"
    assert rows[-1]["sample_id"] == "tz-sw-en-h024"


def test_plan_rejects_wrong_id_order(tmp_path: Path):
    plan = tmp_path / "plan.jsonl"
    _write_plan(plan)
    lines = plan.read_text(encoding="utf-8").splitlines()
    lines[0], lines[1] = lines[1], lines[0]
    plan.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="IDs/order"):
        load_heldout_plan(plan)


def test_resolve_source_audio_requires_exact_stem(tmp_path: Path):
    expected = tmp_path / "tz-sw-en-h001.ogg"
    expected.write_bytes(b"OggS")
    (tmp_path / "prefix-tz-sw-en-h001.ogg").write_bytes(b"OggS")
    resolved = resolve_source_audio(tmp_path, "tz-sw-en-h001")
    assert resolved == expected

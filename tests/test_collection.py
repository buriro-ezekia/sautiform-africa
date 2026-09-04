"""Tests for private benchmark sample ingestion."""
from pathlib import Path

import pytest

from sautiform.benchmark.collection import add_benchmark_sample
from sautiform.forms.public_service import PublicServiceForm


def _form() -> PublicServiceForm:
    return PublicServiceForm(
        district="Mbozi",
        occupation="farmer",
        household_size=6,
        service_request="birth certificate",
    )


def test_add_sample_copies_audio_and_appends_manifest(tmp_path: Path):
    source = tmp_path / "source.wav"
    source.write_bytes(b"RIFF")
    root = tmp_path / "private"

    row = add_benchmark_sample(
        source_audio=source,
        sample_id="tz-sw-en-001",
        reference_transcript="Ninaishi Mbozi District.",
        form=_form(),
        device="laptop microphone",
        noise="quiet room",
        consented=True,
        root=root,
    )

    assert Path(str(row["audio_path"])).is_file()
    manifest = root / "benchmark_manifest.jsonl"
    assert manifest.is_file()
    assert '"sample_id": "tz-sw-en-001"' in manifest.read_text(encoding="utf-8")


def test_add_sample_rejects_duplicate_id(tmp_path: Path):
    source = tmp_path / "source.wav"
    source.write_bytes(b"RIFF")
    root = tmp_path / "private"
    kwargs = {
        "source_audio": source,
        "sample_id": "tz-sw-en-001",
        "reference_transcript": "Ninaishi Mbozi District.",
        "form": _form(),
        "device": "laptop microphone",
        "noise": "quiet room",
        "consented": True,
        "root": root,
    }

    add_benchmark_sample(**kwargs)
    with pytest.raises(ValueError, match="duplicate sample_id"):
        add_benchmark_sample(**kwargs)


def test_add_sample_requires_consent(tmp_path: Path):
    source = tmp_path / "source.wav"
    source.write_bytes(b"RIFF")

    with pytest.raises(ValueError, match="Explicit consent"):
        add_benchmark_sample(
            source_audio=source,
            sample_id="tz-sw-en-001",
            reference_transcript="Ninaishi Mbozi District.",
            form=_form(),
            device="laptop microphone",
            noise="quiet room",
            consented=False,
            root=tmp_path / "private",
        )

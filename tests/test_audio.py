"""Tests for lightweight audio input safeguards."""
from pathlib import Path

import pytest

from sautiform.audio import validate_audio_path


def test_accepts_existing_wav(tmp_path: Path):
    audio = tmp_path / "sample.wav"
    audio.write_bytes(b"RIFF")
    assert validate_audio_path(audio) == audio


def test_rejects_unsupported_extension(tmp_path: Path):
    path = tmp_path / "sample.exe"
    path.write_bytes(b"x")
    with pytest.raises(ValueError, match="Unsupported audio format"):
        validate_audio_path(path)


def test_rejects_missing_audio(tmp_path: Path):
    with pytest.raises(FileNotFoundError, match="Audio file not found"):
        validate_audio_path(tmp_path / "missing.wav")

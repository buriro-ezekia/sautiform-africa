"""Tests for the Streamlit microphone-audio preparation boundary."""
from __future__ import annotations

import wave
from pathlib import Path

import pytest

from sautiform.demo_audio import DemoAudioError, validate_pcm_wav


def _write_wav(
    path: Path,
    *,
    channels: int = 1,
    sample_rate: int = 16_000,
    sample_width: int = 2,
    duration_seconds: float = 1.0,
) -> None:
    frames = int(sample_rate * duration_seconds)
    frame = b"\x00" * (channels * sample_width)
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(channels)
        handle.setsampwidth(sample_width)
        handle.setframerate(sample_rate)
        handle.writeframes(frame * frames)


def test_validate_pcm_wav_accepts_canonical_demo_audio(tmp_path: Path):
    path = tmp_path / "demo.wav"
    _write_wav(path, duration_seconds=1.25)

    assert validate_pcm_wav(path) == pytest.approx(1.25)


def test_validate_pcm_wav_rejects_noncanonical_sample_rate(tmp_path: Path):
    path = tmp_path / "demo.wav"
    _write_wav(path, sample_rate=44_100)

    with pytest.raises(DemoAudioError, match="16000 Hz"):
        validate_pcm_wav(path)


def test_validate_pcm_wav_rejects_too_short_recording(tmp_path: Path):
    path = tmp_path / "demo.wav"
    _write_wav(path, duration_seconds=0.1)

    with pytest.raises(DemoAudioError, match="too short"):
        validate_pcm_wav(path)

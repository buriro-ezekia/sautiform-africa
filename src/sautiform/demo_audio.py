"""Audio preparation helpers for the Streamlit Sahara demo."""
from __future__ import annotations

import shutil
import subprocess
import wave
from pathlib import Path


class DemoAudioError(RuntimeError):
    """Raised when microphone audio cannot be prepared safely for Sahara."""


def validate_pcm_wav(path: Path) -> float:
    """Validate the canonical demo WAV and return its duration in seconds."""
    try:
        with wave.open(str(path), "rb") as handle:
            channels = handle.getnchannels()
            sample_rate = handle.getframerate()
            sample_width = handle.getsampwidth()
            frames = handle.getnframes()
    except (wave.Error, OSError) as exc:
        raise DemoAudioError("Prepared microphone audio is not a readable WAV file") from exc

    if channels != 1:
        raise DemoAudioError(f"Prepared WAV must be mono; found {channels} channels")
    if sample_rate != 16_000:
        raise DemoAudioError(
            f"Prepared WAV must be 16000 Hz; found {sample_rate} Hz"
        )
    if sample_width != 2:
        raise DemoAudioError(
            f"Prepared WAV must use 16-bit PCM; found {sample_width * 8}-bit samples"
        )
    if sample_rate <= 0:
        raise DemoAudioError("Prepared WAV has an invalid sample rate")

    duration = frames / sample_rate
    if duration < 0.5:
        raise DemoAudioError(
            "Recording is too short. Record at least half a second of speech."
        )
    if duration > 120:
        raise DemoAudioError(
            "Recording exceeds the 120-second Sahara synchronous API limit."
        )
    return duration


def normalise_microphone_wav(source: Path, target: Path) -> float:
    """Convert browser WAV audio to canonical PCM WAV for the Sahara demo."""
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise DemoAudioError(
            "FFmpeg is required to prepare microphone audio for Sahara. "
            "Install FFmpeg or use the existing Whisper-ready environment."
        )

    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-y",
        "-i",
        str(source),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(target),
    ]
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip()
        if len(detail) > 500:
            detail = detail[:500] + "..."
        raise DemoAudioError(
            "FFmpeg could not decode the microphone recording"
            + (f": {detail}" if detail else ".")
        )

    if not target.is_file() or target.stat().st_size <= 44:
        raise DemoAudioError("Prepared microphone WAV is empty")

    return validate_pcm_wav(target)

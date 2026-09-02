"""Lightweight safeguards for uploaded and benchmark audio."""
from __future__ import annotations

from pathlib import Path

ALLOWED_AUDIO_SUFFIXES = frozenset(
    {".wav", ".flac", ".mp3", ".m4a", ".ogg", ".webm"}
)
DEFAULT_MAX_AUDIO_BYTES = 25 * 1024 * 1024


def validate_audio_path(
    path: Path,
    *,
    max_bytes: int = DEFAULT_MAX_AUDIO_BYTES,
    require_exists: bool = True,
) -> Path:
    """Reject unsupported, missing or unexpectedly large audio before model calls."""
    path = Path(path)
    if path.suffix.lower() not in ALLOWED_AUDIO_SUFFIXES:
        allowed = ", ".join(sorted(ALLOWED_AUDIO_SUFFIXES))
        raise ValueError(
            f"Unsupported audio format '{path.suffix}'. Allowed: {allowed}"
        )
    if require_exists and not path.is_file():
        raise FileNotFoundError(f"Audio file not found: {path}")
    if require_exists and path.stat().st_size > max_bytes:
        raise ValueError(f"Audio file exceeds the {max_bytes} byte safety limit")
    return path

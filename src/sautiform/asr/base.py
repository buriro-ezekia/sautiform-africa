"""ASR backend interfaces."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class TranscriptResult:
    text: str
    backend: str
    latency_seconds: float | None = None
    metadata: dict[str, object] | None = None


class ASRBackend(Protocol):
    name: str

    def transcribe(self, audio_path: Path) -> TranscriptResult: ...

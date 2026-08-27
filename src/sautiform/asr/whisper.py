"""Optional local Whisper adapter."""
from __future__ import annotations

import time
from pathlib import Path

from sautiform.asr.base import TranscriptResult


class WhisperBackend:
    name = "whisper"

    def __init__(self, model_name: str = "small") -> None:
        try:
            import whisper
        except ImportError as exc:
            raise RuntimeError("Install the 'whisper' optional dependency") from exc
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        start = time.perf_counter()
        result = self.model.transcribe(str(audio_path))
        return TranscriptResult(result["text"].strip(), self.name, time.perf_counter() - start)

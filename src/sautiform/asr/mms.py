"""Optional Meta MMS adapter via Transformers."""
from __future__ import annotations

import time
from pathlib import Path

from sautiform.asr.base import TranscriptResult


class MMSBackend:
    name = "mms"

    def __init__(self, model_id: str = "facebook/mms-1b-all") -> None:
        try:
            from transformers import pipeline
        except ImportError as exc:
            raise RuntimeError("Install the 'mms' optional dependency") from exc
        self.pipe = pipeline("automatic-speech-recognition", model=model_id)

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        start = time.perf_counter()
        result = self.pipe(str(audio_path))
        text = result["text"] if isinstance(result, dict) else str(result)
        return TranscriptResult(text.strip(), self.name, time.perf_counter() - start)

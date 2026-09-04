"""Optional local Whisper adapter with reproducible pilot diagnostics."""
from __future__ import annotations

import os
import time
from pathlib import Path

from sautiform.asr.base import TranscriptResult


def _optional_float(name: str) -> float | None:
    value = os.getenv(name, "").strip()
    return float(value) if value else None


class WhisperBackend:
    name = "whisper"

    def __init__(self, model_name: str | None = None) -> None:
        try:
            import whisper
        except ImportError as exc:
            raise RuntimeError("Install the 'whisper' optional dependency") from exc

        self.model_name = model_name or os.getenv("WHISPER_MODEL", "small")
        self.language = os.getenv("WHISPER_LANGUAGE", "").strip() or None
        self.temperature = _optional_float("WHISPER_TEMPERATURE")
        self.model = whisper.load_model(self.model_name)

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        kwargs: dict[str, object] = {}
        if self.language is not None:
            kwargs["language"] = self.language
        if self.temperature is not None:
            kwargs["temperature"] = self.temperature
        if str(self.model.device).startswith("cpu"):
            kwargs["fp16"] = False

        start = time.perf_counter()
        result = self.model.transcribe(str(audio_path), **kwargs)
        latency = time.perf_counter() - start
        metadata: dict[str, object] = {
            "model": self.model_name,
            "device": str(self.model.device),
            "language_requested": self.language or "auto",
            "language_result": result.get("language"),
            "temperature_requested": (
                self.temperature if self.temperature is not None else "default_fallback"
            ),
        }
        return TranscriptResult(
            result["text"].strip(),
            self.name,
            latency,
            metadata,
        )

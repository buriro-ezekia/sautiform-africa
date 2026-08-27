"""Generic HTTP ASR adapter for a fourth benchmark model."""
from __future__ import annotations

import os
import time
from pathlib import Path

import requests

from sautiform.asr.base import TranscriptResult


class HTTPBackend:
    name = "http"

    def __init__(self) -> None:
        self.url = os.getenv("ASR_HTTP_URL")
        self.key = os.getenv("ASR_HTTP_KEY")
        self.file_field = os.getenv("ASR_HTTP_FILE_FIELD", "file")
        self.text_field = os.getenv("ASR_HTTP_TEXT_FIELD", "text")
        if not self.url:
            raise RuntimeError("ASR_HTTP_URL is required")

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        headers = {"Authorization": f"Bearer {self.key}"} if self.key else {}
        start = time.perf_counter()
        with audio_path.open("rb") as handle:
            response = requests.post(
                self.url,
                headers=headers,
                files={self.file_field: (audio_path.name, handle)},
                timeout=120,
            )
        response.raise_for_status()
        payload = response.json()
        text = payload.get(self.text_field)
        if not isinstance(text, str):
            raise RuntimeError(f"Response does not contain text field '{self.text_field}'")
        return TranscriptResult(text.strip(), self.name, time.perf_counter() - start)

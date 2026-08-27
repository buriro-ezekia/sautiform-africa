"""Configurable Sahara v2.5 HTTP adapter."""
from __future__ import annotations

import os
import time
from pathlib import Path

import requests

from sautiform.asr.base import TranscriptResult


class SaharaBackend:
    name = "sahara"

    def __init__(self) -> None:
        self.url = os.getenv("SAHARA_API_URL")
        self.key = os.getenv("SAHARA_API_KEY")
        self.file_field = os.getenv("SAHARA_FILE_FIELD", "file")
        self.model = os.getenv("SAHARA_MODEL")
        self.response_text_path = os.getenv("SAHARA_RESPONSE_TEXT_PATH", "text")
        if not self.url or not self.key:
            raise RuntimeError("SAHARA_API_URL and SAHARA_API_KEY are required")

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        headers = {"Authorization": f"Bearer {self.key}"}
        data = {"model": self.model} if self.model else {}
        start = time.perf_counter()
        with audio_path.open("rb") as handle:
            response = requests.post(
                self.url,
                headers=headers,
                data=data,
                files={self.file_field: (audio_path.name, handle)},
                timeout=120,
            )
        response.raise_for_status()
        payload = response.json()
        value: object = payload
        for key in self.response_text_path.split("."):
            if not isinstance(value, dict) or key not in value:
                raise RuntimeError(f"Transcript path '{self.response_text_path}' missing in response")
            value = value[key]
        if not isinstance(value, str):
            raise RuntimeError("Configured Sahara transcript value is not text")
        return TranscriptResult(value.strip(), self.name, time.perf_counter() - start)

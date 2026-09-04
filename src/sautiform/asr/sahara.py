"""Intron Sahara v2.5 synchronous STT adapter."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import requests

from sautiform.asr.base import TranscriptResult

DEFAULT_SAHARA_URL = "https://infer.voice.intron.io/file/v1/upload/sync"
DEFAULT_RESPONSE_TEXT_PATH = "data.audio_transcript"


def _json_object_from_env(name: str) -> dict[str, object]:
    raw = os.getenv(name, "").strip()
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{name} must contain valid JSON") from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"{name} must contain a JSON object")
    return value


class SaharaBackend:
    name = "sahara"

    def __init__(self) -> None:
        self.url = os.getenv("SAHARA_API_URL", DEFAULT_SAHARA_URL)
        self.key = os.getenv("SAHARA_API_KEY")
        self.language = os.getenv("SAHARA_LANGUAGE", "sw")
        self.disable_llm_corrections = os.getenv(
            "SAHARA_DISABLE_LLM_CORRECTIONS",
            "TRUE",
        )
        self.response_text_path = os.getenv(
            "SAHARA_RESPONSE_TEXT_PATH",
            DEFAULT_RESPONSE_TEXT_PATH,
        )
        self.timeout_seconds = float(os.getenv("SAHARA_TIMEOUT_SECONDS", "120"))
        self.extra_form = _json_object_from_env("SAHARA_FORM_JSON")

        if not self.key:
            raise RuntimeError("SAHARA_API_KEY is required")
        if not self.url.strip():
            raise RuntimeError("SAHARA_API_URL must not be empty")
        if not self.language.strip():
            raise RuntimeError("SAHARA_LANGUAGE must not be empty")
        if self.timeout_seconds <= 0:
            raise RuntimeError("SAHARA_TIMEOUT_SECONDS must be greater than zero")

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.key}"}

    def _form_data(self, audio_path: Path) -> dict[str, str]:
        data = {str(key): str(value) for key, value in self.extra_form.items()}
        data.update(
            {
                "audio_file_name": audio_path.stem,
                "use_language_asr_input": self.language,
                "use_disable_llm_corrections": self.disable_llm_corrections,
            }
        )
        return data

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        start = time.perf_counter()
        with audio_path.open("rb") as handle:
            response = requests.post(
                self.url,
                headers=self._headers(),
                data=self._form_data(audio_path),
                files={"audio_file_blob": (audio_path.name, handle)},
                timeout=self.timeout_seconds,
            )

        response.raise_for_status()
        payload = response.json()
        value: object = payload
        for key in self.response_text_path.split("."):
            if not isinstance(value, dict) or key not in value:
                raise RuntimeError(
                    f"Transcript path '{self.response_text_path}' missing in response"
                )
            value = value[key]

        if not isinstance(value, str):
            raise RuntimeError("Configured Sahara transcript value is not text")

        metadata: dict[str, object] = {
            "endpoint": self.url,
            "language": self.language,
            "code_switching": True,
            "disable_llm_corrections": self.disable_llm_corrections,
            "response_text_path": self.response_text_path,
        }

        return TranscriptResult(
            value.strip(),
            self.name,
            time.perf_counter() - start,
            metadata,
        )

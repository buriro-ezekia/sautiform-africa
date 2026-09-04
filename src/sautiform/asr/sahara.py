"""Configurable Sahara v2.5 HTTP adapter."""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import requests

from sautiform.asr.base import TranscriptResult


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
        self.url = os.getenv("SAHARA_API_URL")
        self.key = os.getenv("SAHARA_API_KEY")
        self.auth_header = os.getenv("SAHARA_AUTH_HEADER", "Authorization")
        self.auth_scheme = os.getenv("SAHARA_AUTH_SCHEME", "Bearer")
        self.file_field = os.getenv("SAHARA_FILE_FIELD", "file")
        self.model_field = os.getenv("SAHARA_MODEL_FIELD", "model")
        self.model = os.getenv("SAHARA_MODEL")
        self.response_text_path = os.getenv("SAHARA_RESPONSE_TEXT_PATH", "text")
        self.timeout_seconds = float(os.getenv("SAHARA_TIMEOUT_SECONDS", "120"))
        self.extra_headers = _json_object_from_env("SAHARA_HEADERS_JSON")
        self.extra_form = _json_object_from_env("SAHARA_FORM_JSON")

        if not self.url or not self.key:
            raise RuntimeError("SAHARA_API_URL and SAHARA_API_KEY are required")
        if not self.auth_header.strip():
            raise RuntimeError("SAHARA_AUTH_HEADER must not be empty")
        if self.timeout_seconds <= 0:
            raise RuntimeError("SAHARA_TIMEOUT_SECONDS must be greater than zero")

    def _headers(self) -> dict[str, str]:
        headers = {str(key): str(value) for key, value in self.extra_headers.items()}
        auth_value = (
            f"{self.auth_scheme.strip()} {self.key}"
            if self.auth_scheme.strip()
            else self.key
        )
        headers[self.auth_header] = auth_value
        return headers

    def _form_data(self) -> dict[str, str]:
        data = {str(key): str(value) for key, value in self.extra_form.items()}
        if self.model:
            data[self.model_field] = self.model
        return data

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        start = time.perf_counter()
        with audio_path.open("rb") as handle:
            response = requests.post(
                self.url,
                headers=self._headers(),
                data=self._form_data(),
                files={self.file_field: (audio_path.name, handle)},
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
            "model": self.model or "unspecified",
            "file_field": self.file_field,
            "response_text_path": self.response_text_path,
            "auth_header": self.auth_header,
            "auth_scheme": self.auth_scheme or "none",
        }

        return TranscriptResult(
            value.strip(),
            self.name,
            time.perf_counter() - start,
            metadata,
        )

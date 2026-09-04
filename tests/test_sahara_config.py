"""Tests for configurable Sahara participant API behaviour."""
from __future__ import annotations

from pathlib import Path

import pytest

from sautiform.asr.sahara import SaharaBackend, _json_object_from_env


class _Response:
    def raise_for_status(self):
        return None

    def json(self):
        return {"data": {"transcript": "Ninaishi Mbozi District"}}


def test_sahara_requires_explicit_credentials(monkeypatch):
    monkeypatch.delenv("SAHARA_API_URL", raising=False)
    monkeypatch.delenv("SAHARA_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="SAHARA_API_URL and SAHARA_API_KEY"):
        SaharaBackend()


def test_sahara_supports_raw_api_key_header(monkeypatch):
    monkeypatch.setenv("SAHARA_API_URL", "https://example.invalid/transcribe")
    monkeypatch.setenv("SAHARA_API_KEY", "secret")
    monkeypatch.setenv("SAHARA_AUTH_HEADER", "x-api-key")
    monkeypatch.setenv("SAHARA_AUTH_SCHEME", "")

    backend = SaharaBackend()

    assert backend._headers()["x-api-key"] == "secret"


def test_sahara_supports_bearer_header(monkeypatch):
    monkeypatch.setenv("SAHARA_API_URL", "https://example.invalid/transcribe")
    monkeypatch.setenv("SAHARA_API_KEY", "secret")
    monkeypatch.delenv("SAHARA_AUTH_HEADER", raising=False)
    monkeypatch.delenv("SAHARA_AUTH_SCHEME", raising=False)

    backend = SaharaBackend()

    assert backend._headers()["Authorization"] == "Bearer secret"


def test_sahara_supports_extra_form_and_nested_response(
    monkeypatch,
    tmp_path: Path,
):
    monkeypatch.setenv("SAHARA_API_URL", "https://example.invalid/transcribe")
    monkeypatch.setenv("SAHARA_API_KEY", "secret")
    monkeypatch.setenv("SAHARA_MODEL", "sahara-v2.5")
    monkeypatch.setenv("SAHARA_MODEL_FIELD", "model")
    monkeypatch.setenv("SAHARA_FORM_JSON", '{"language":"sw-en"}')
    monkeypatch.setenv("SAHARA_RESPONSE_TEXT_PATH", "data.transcript")

    captured = {}

    def fake_post(url, *, headers, data, files, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["data"] = data
        captured["files"] = files
        captured["timeout"] = timeout
        return _Response()

    monkeypatch.setattr("sautiform.asr.sahara.requests.post", fake_post)

    audio = tmp_path / "dev.ogg"
    audio.write_bytes(b"audio")

    result = SaharaBackend().transcribe(audio)

    assert result.text == "Ninaishi Mbozi District"
    assert captured["data"]["language"] == "sw-en"
    assert captured["data"]["model"] == "sahara-v2.5"


def test_sahara_json_env_requires_object(monkeypatch):
    monkeypatch.setenv("SAHARA_FORM_JSON", '["not", "an", "object"]')
    with pytest.raises(RuntimeError, match="JSON object"):
        _json_object_from_env("SAHARA_FORM_JSON")

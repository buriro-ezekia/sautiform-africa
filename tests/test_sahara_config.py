"""Tests for the Intron Sahara v2.5 STT adapter."""
from __future__ import annotations

from pathlib import Path

import pytest

from sautiform.asr.sahara import (
    DEFAULT_RESPONSE_TEXT_PATH,
    DEFAULT_SAHARA_URL,
    SaharaBackend,
    _json_object_from_env,
)


class _Response:
    def raise_for_status(self):
        return None

    def json(self):
        return {
            "data": {
                "file_id": "test-id",
                "processing_status": "FILE_TRANSCRIBED",
                "audio_file_name": "dev",
                "audio_transcript": "Ninaishi Mbozi District",
            }
        }


def _base_env(monkeypatch):
    monkeypatch.setenv("SAHARA_API_KEY", "secret")
    monkeypatch.delenv("SAHARA_API_URL", raising=False)
    monkeypatch.delenv("SAHARA_LANGUAGE", raising=False)
    monkeypatch.delenv("SAHARA_DISABLE_LLM_CORRECTIONS", raising=False)
    monkeypatch.delenv("SAHARA_RESPONSE_TEXT_PATH", raising=False)
    monkeypatch.delenv("SAHARA_FORM_JSON", raising=False)


def test_sahara_requires_explicit_api_key(monkeypatch):
    monkeypatch.delenv("SAHARA_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="SAHARA_API_KEY is required"):
        SaharaBackend()


def test_sahara_uses_official_intron_defaults(monkeypatch):
    _base_env(monkeypatch)
    backend = SaharaBackend()
    assert backend.url == DEFAULT_SAHARA_URL
    assert backend.language == "sw"
    assert backend.disable_llm_corrections == "TRUE"
    assert backend.response_text_path == DEFAULT_RESPONSE_TEXT_PATH
    assert backend._headers()["Authorization"] == "Bearer secret"


def test_sahara_sends_official_sync_fields(monkeypatch, tmp_path: Path):
    _base_env(monkeypatch)
    captured = {}

    def fake_post(url, *, headers, data, files, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["data"] = data
        captured["files"] = files
        captured["timeout"] = timeout
        return _Response()

    monkeypatch.setattr("sautiform.asr.sahara.requests.post", fake_post)

    audio = tmp_path / "tz-sw-en-001.ogg"
    audio.write_bytes(b"audio")
    result = SaharaBackend().transcribe(audio)

    assert result.text == "Ninaishi Mbozi District"
    assert captured["url"] == DEFAULT_SAHARA_URL
    assert captured["data"]["audio_file_name"] == "tz-sw-en-001"
    assert captured["data"]["use_language_asr_input"] == "sw"
    assert captured["data"]["use_disable_llm_corrections"] == "TRUE"
    assert "audio_file_blob" in captured["files"]


def test_sahara_extra_form_cannot_override_required_benchmark_fields(
    monkeypatch,
    tmp_path: Path,
):
    _base_env(monkeypatch)
    monkeypatch.setenv(
        "SAHARA_FORM_JSON",
        '{"use_language_asr_input":"en","audio_file_name":"wrong"}',
    )
    captured = {}

    def fake_post(url, *, headers, data, files, timeout):
        captured["data"] = data
        return _Response()

    monkeypatch.setattr("sautiform.asr.sahara.requests.post", fake_post)

    audio = tmp_path / "dev.ogg"
    audio.write_bytes(b"audio")
    SaharaBackend().transcribe(audio)

    assert captured["data"]["use_language_asr_input"] == "sw"
    assert captured["data"]["audio_file_name"] == "dev"


def test_sahara_json_env_requires_object(monkeypatch):
    monkeypatch.setenv("SAHARA_FORM_JSON", '["not", "an", "object"]')
    with pytest.raises(RuntimeError, match="JSON object"):
        _json_object_from_env("SAHARA_FORM_JSON")

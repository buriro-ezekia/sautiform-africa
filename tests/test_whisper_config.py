"""Tests for explicit Whisper pilot configuration without loading a real model."""
from pathlib import Path
from types import SimpleNamespace

from sautiform.asr.whisper import WhisperBackend


class _FakeModel:
    device = "cpu"

    def __init__(self) -> None:
        self.kwargs: dict[str, object] = {}

    def transcribe(self, path: str, **kwargs):
        self.kwargs = kwargs
        return {"text": "sample transcript", "language": "sw"}


def test_whisper_records_language_and_temperature(monkeypatch):
    model = _FakeModel()
    fake_whisper = SimpleNamespace(load_model=lambda name: model)
    monkeypatch.setitem(__import__("sys").modules, "whisper", fake_whisper)
    monkeypatch.setenv("WHISPER_LANGUAGE", "sw")
    monkeypatch.setenv("WHISPER_TEMPERATURE", "0")

    backend = WhisperBackend(model_name="small")
    result = backend.transcribe(Path("sample.wav"))

    assert model.kwargs == {
        "language": "sw",
        "temperature": 0.0,
        "fp16": False,
    }
    assert result.metadata == {
        "model": "small",
        "device": "cpu",
        "language_requested": "sw",
        "language_result": "sw",
        "temperature_requested": 0.0,
    }

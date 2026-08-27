"""ASR backend construction."""
from __future__ import annotations

from sautiform.asr.http_backend import HTTPBackend
from sautiform.asr.mms import MMSBackend
from sautiform.asr.sahara import SaharaBackend
from sautiform.asr.whisper import WhisperBackend


def build_backend(name: str):
    name = name.lower()
    if name == "sahara":
        return SaharaBackend()
    if name == "whisper":
        return WhisperBackend()
    if name == "mms":
        return MMSBackend()
    if name == "http":
        return HTTPBackend()
    raise ValueError(f"Unknown backend: {name}")

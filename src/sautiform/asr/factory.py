"""ASR backend construction."""
from __future__ import annotations

from sautiform.asr.http_backend import HTTPBackend
from sautiform.asr.mms import MMSBackend
from sautiform.asr.omni import OmniASRBackend
from sautiform.asr.sahara import SaharaBackend
from sautiform.asr.whisper import WhisperBackend

CHALLENGE_BACKENDS = ("sahara", "whisper", "mms", "omni")
SUPPORTED_BACKENDS = (*CHALLENGE_BACKENDS, "http")


def build_backend(name: str):
    """Construct a configured ASR backend by stable command-line name."""
    name = name.lower()
    if name == "sahara":
        return SaharaBackend()
    if name == "whisper":
        return WhisperBackend()
    if name == "mms":
        return MMSBackend()
    if name == "omni":
        return OmniASRBackend()
    if name == "http":
        return HTTPBackend()
    raise ValueError(f"Unknown backend: {name}")

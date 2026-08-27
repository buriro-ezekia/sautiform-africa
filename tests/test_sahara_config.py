"""Tests that Sahara configuration fails closed without credentials."""
import pytest

from sautiform.asr.sahara import SaharaBackend


def test_sahara_requires_explicit_credentials(monkeypatch):
    monkeypatch.delenv("SAHARA_API_URL", raising=False)
    monkeypatch.delenv("SAHARA_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="SAHARA_API_URL and SAHARA_API_KEY"):
        SaharaBackend()

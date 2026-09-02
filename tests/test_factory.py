"""Tests for stable challenge backend naming without loading large models."""
from sautiform.asr.factory import CHALLENGE_BACKENDS


def test_four_challenge_backends_are_explicit():
    assert CHALLENGE_BACKENDS == ("sahara", "whisper", "mms", "omni")

"""Tests for MMS target-language configuration."""
import pytest

from sautiform.asr.mms import normalise_mms_target_lang


def test_mms_uses_swh_for_swahili_iso_639_3():
    assert normalise_mms_target_lang("swh") == "swh"


def test_mms_normalises_common_swahili_aliases():
    assert normalise_mms_target_lang("swa") == "swh"
    assert normalise_mms_target_lang("sw") == "swh"


def test_mms_rejects_empty_target_language():
    with pytest.raises(ValueError, match="must not be empty"):
        normalise_mms_target_lang("  ")

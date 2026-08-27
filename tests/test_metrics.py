"""Tests for benchmark metrics."""
from sautiform.benchmark.metrics import (
    character_error_rate,
    complete_form_accuracy,
    field_exact_match,
    word_error_rate,
)
from sautiform.forms.public_service import PublicServiceForm


def test_zero_error_for_identical_transcript():
    assert word_error_rate("habari hello", "habari hello") == 0.0
    assert character_error_rate("habari", "habari") == 0.0


def test_field_metrics():
    reference = PublicServiceForm("Mbozi", "farmer", 6, "birth certificate")
    predicted = PublicServiceForm("Mbozi", "farmer", 5, "birth certificate")
    assert field_exact_match(reference, predicted) == 0.75
    assert complete_form_accuracy(reference, predicted) == 0.0

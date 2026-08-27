"""Tests for clarification and confirmation behaviour."""
from sautiform.dialogue.engine import next_prompt
from sautiform.forms.public_service import PublicServiceForm


def test_asks_for_first_missing_field():
    form = PublicServiceForm(district="Mbozi")
    assert "occupation" in next_prompt(form).lower()


def test_rejects_invalid_household_size():
    form = PublicServiceForm(
        district="Mbozi", occupation="farmer", household_size=0, service_request="birth certificate"
    )
    assert "between 1 and 50" in next_prompt(form)


def test_complete_form_requires_confirmation():
    form = PublicServiceForm(
        district="Mbozi", occupation="farmer", household_size=6, service_request="birth certificate"
    )
    prompt = next_prompt(form)
    assert "confirm" in prompt.lower()
    assert "Je, taarifa hizi ni sahihi?" in prompt

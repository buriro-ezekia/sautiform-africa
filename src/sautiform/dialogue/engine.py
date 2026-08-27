"""Clarification and confirmation logic for safe form completion."""
from __future__ import annotations

from sautiform.forms.public_service import PublicServiceForm

_PROMPTS = {
    "district": "Which district do you live in? / Unaishi wilaya gani?",
    "occupation": "What is your occupation? / Kazi yako ni nini?",
    "household_size": "How many people are in your household? / Kaya ina watu wangapi?",
    "service_request": "Which public service do you need? / Unahitaji huduma gani ya umma?",
}


def next_prompt(form: PublicServiceForm) -> str:
    errors = form.validate()
    if errors:
        return f"I need to correct this before continuing: {errors[0]}."
    missing = form.missing_fields()
    if missing:
        return _PROMPTS[missing[0]]
    return confirmation_prompt(form)


def confirmation_prompt(form: PublicServiceForm) -> str:
    return (
        "Please confirm this record: "
        f"district={form.district}; occupation={form.occupation}; "
        f"household size={form.household_size}; service={form.service_request}. "
        "Is this correct? / Je, taarifa hizi ni sahihi?"
    )

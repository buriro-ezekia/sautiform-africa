"""Deterministic extraction for the first Kiswahili-English public-service prototype."""
from __future__ import annotations

import re
from dataclasses import replace

from sautiform.forms.public_service import PublicServiceForm

_NUMBER_WORDS = {
    "moja": 1,
    "mbili": 2,
    "tatu": 3,
    "nne": 4,
    "tano": 5,
    "sita": 6,
    "saba": 7,
    "nane": 8,
    "tisa": 9,
    "kumi": 10,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}

_DISTRICT_PATTERNS = [
    re.compile(r"(?:ninaishi|naishi|I live in|district(?: yangu)?(?: ni)?)\s+([A-Za-z-]+)(?:\s+District)?", re.I),
]
_OCCUPATION_PATTERNS = [
    re.compile(r"(?:occupation(?: yangu)?(?: ni)?|kazi yangu ni|I work as(?: a)?)\s+([A-Za-z -]+?)(?=,|\.|\band\b|\bna\b|$)", re.I),
]
_HOUSEHOLD_PATTERNS = [
    re.compile(r"(?:household(?: yangu)?(?: ina| has)?|familia(?: yangu)?(?: ina)?)(?:\s+watu)?\s+(\d+|[A-Za-z]+)", re.I),
    re.compile(r"(\d+|[A-Za-z]+)\s+(?:people|members|watu)\b", re.I),
]
_SERVICE_PATTERNS = [
    re.compile(r"(?:nataka|nahitaji|I need|service(?: request)?(?: ni)?)\s+([A-Za-z -]+?)(?=,|\.|$)", re.I),
]


def _normalise_words(value: str) -> str:
    return " ".join(value.strip().split())


def _parse_count(token: str) -> int | None:
    token = token.lower().strip()
    if token.isdigit():
        return int(token)
    return _NUMBER_WORDS.get(token)


def extract_form(text: str, existing: PublicServiceForm | None = None) -> PublicServiceForm:
    """Extract only explicit values; ambiguous or absent values remain unset."""
    form = existing or PublicServiceForm()
    updates: dict[str, object] = {}

    for pattern in _DISTRICT_PATTERNS:
        match = pattern.search(text)
        if match:
            updates["district"] = _normalise_words(match.group(1)).title()
            break

    for pattern in _OCCUPATION_PATTERNS:
        match = pattern.search(text)
        if match:
            updates["occupation"] = _normalise_words(match.group(1)).lower()
            break

    for pattern in _HOUSEHOLD_PATTERNS:
        match = pattern.search(text)
        if match:
            count = _parse_count(match.group(1))
            if count is not None:
                updates["household_size"] = count
            break

    for pattern in _SERVICE_PATTERNS:
        match = pattern.search(text)
        if match:
            updates["service_request"] = _normalise_words(match.group(1)).lower()
            break

    return replace(form, **updates)

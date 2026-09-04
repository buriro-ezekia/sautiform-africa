"""Deterministic extraction for the Kiswahili-English public-service prototype."""
from __future__ import annotations

import re
from dataclasses import replace

from sautiform.forms.public_service import PublicServiceForm

_NUMBER_WORDS = {
    "moja": 1,
    "mbili": 2,
    "wawili": 2,
    "tatu": 3,
    "watatu": 3,
    "nne": 4,
    "wanne": 4,
    "tano": 5,
    "watano": 5,
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
    re.compile(
        r"(?:ninaishi|naishi|inaishi|naishu|I live in(?: the)?)"
        r"\s+([A-Za-z-]+)(?:\s+District)?",
        re.I,
    ),
    re.compile(
        r"district(?: yangu)?\s+ni\s+([A-Za-z-]+)",
        re.I,
    ),
    re.compile(
        r"(?:ninaishi\w*|naishi\w*)\s+([A-Za-z-]+)\s+district\b",
        re.I,
    ),
]
_OCCUPATION_PATTERNS = [
    re.compile(
        r"(?:occupation(?: yangu)?(?: ni)?|kazi yangu ni|I work as(?: a)?)"
        r"\s+([A-Za-z -]+?)"
        r"(?=,|\.|\band\b|\bna\b|\bhousehold\b|\bfamilia\b|"
        r"\bnataka\b|\bnahitaji\b|\bI need\b|\bservice\b|"
        r"\b[A-Za-z]{3,16}\s+yangu\s+ina\b|$)",
        re.I,
    ),
    re.compile(
        r"\b[A-Za-z]{5,16}\s+(?:yangu|angu)\s+ni\s+"
        r"([A-Za-z-]+)"
        r"(?=\s+household\b|\s+familia\b|\s+nataka\b|"
        r"\s+nahitaji\b|,|\.|$)",
        re.I,
    ),
]
_HOUSEHOLD_PATTERNS = [
    re.compile(
        r"(?:household(?:i)?(?: yangu)?\s*(?:ina|has)?\s*"
        r"(?:watu)?|familia(?: yangu)?(?: ina)?)"
        r"\s+(\d+|[A-Za-z]+)",
        re.I,
    ),
    re.compile(r"(\d+|[A-Za-z]+)\s+(?:people|members|watu)\b", re.I),
]
_SERVICE_PATTERNS = [
    re.compile(
        r"(?:nataka|nahitaji|I need|service(?: request)?(?: ni)?)"
        r"\s+([A-Za-z -]+?)(?=,|\.|$)",
        re.I,
    ),
]


def _normalise_words(value: str) -> str:
    return " ".join(value.strip().split())


def _normalise_asr_spacing(text: str) -> str:
    """Repair conservative token-boundary errors without changing content words."""
    text = re.sub(r"\bhouseholdi\b", "household", text, flags=re.I)
    text = re.sub(r"\binawatu\b", "ina watu", text, flags=re.I)
    text = re.sub(r"\bna\s+itaji\b", "nahitaji", text, flags=re.I)
    text = re.sub(r"\bnaitaji\b", "nahitaji", text, flags=re.I)
    text = re.sub(r"\bwa\s+wili\b", "wawili", text, flags=re.I)
    return _normalise_words(text)


def _normalise_service(value: str) -> str:
    """Canonicalise harmless articles and UK/US licence spelling only."""
    value = _normalise_words(value).lower()
    value = re.sub(r"^(?:a|the)\s+", "", value)
    return re.sub(r"\blicense\b", "licence", value)


def _parse_count(token: str) -> int | None:
    token = token.lower().strip()
    if token.isdigit():
        return int(token)
    return _NUMBER_WORDS.get(token)


def extract_form(text: str, existing: PublicServiceForm | None = None) -> PublicServiceForm:
    """Extract explicit values while tolerating limited ASR boundary variation."""
    form = existing or PublicServiceForm()
    updates: dict[str, object] = {}
    text = _normalise_asr_spacing(text)

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
            updates["service_request"] = _normalise_service(match.group(1))
            break

    return replace(form, **updates)

"""Dependency-free transcription and downstream task metrics."""
from __future__ import annotations

from collections.abc import Sequence

from sautiform.forms.public_service import PublicServiceForm


def _edit_distance(reference: Sequence[str], hypothesis: Sequence[str]) -> int:
    previous = list(range(len(hypothesis) + 1))
    for i, ref_item in enumerate(reference, start=1):
        current = [i]
        for j, hyp_item in enumerate(hypothesis, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[j] + 1,
                    previous[j - 1] + (ref_item != hyp_item),
                )
            )
        previous = current
    return previous[-1]


def word_error_rate(reference: str, hypothesis: str) -> float:
    ref = reference.lower().split()
    hyp = hypothesis.lower().split()
    if not ref:
        return 0.0 if not hyp else 1.0
    return _edit_distance(ref, hyp) / len(ref)


def character_error_rate(reference: str, hypothesis: str) -> float:
    ref = list(reference.lower())
    hyp = list(hypothesis.lower())
    if not ref:
        return 0.0 if not hyp else 1.0
    return _edit_distance(ref, hyp) / len(ref)


def field_exact_match(reference: PublicServiceForm, predicted: PublicServiceForm) -> float:
    fields = reference.REQUIRED_FIELDS
    correct = sum(getattr(reference, name) == getattr(predicted, name) for name in fields)
    return correct / len(fields)


def complete_form_accuracy(reference: PublicServiceForm, predicted: PublicServiceForm) -> float:
    return float(reference.to_dict() == predicted.to_dict())

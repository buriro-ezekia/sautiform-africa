"""Benchmark runner for ASR plus downstream form extraction."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from sautiform.benchmark.manifest import load_validated_manifest
from sautiform.benchmark.metrics import (
    character_error_rate,
    complete_form_accuracy,
    field_exact_match,
    word_error_rate,
)
from sautiform.forms.extraction import extract_form
from sautiform.forms.public_service import PublicServiceForm


def run_rows(
    rows: list[dict[str, Any]],
    backend,
) -> dict[str, object]:
    """Benchmark already validated rows against one backend."""
    results: list[dict[str, object]] = []
    for item in rows:
        result = backend.transcribe(Path(item["audio_path"]))
        reference_form = PublicServiceForm(**item["reference_fields"])
        predicted_form = extract_form(result.text)
        results.append(
            {
                "sample_id": item["sample_id"],
                "audio_path": item["audio_path"],
                "metadata": item["metadata"],
                "backend": result.backend,
                "asr_metadata": result.metadata or {},
                "transcript": result.text,
                "predicted_fields": predicted_form.to_dict(),
                "wer": word_error_rate(
                    item["reference_transcript"],
                    result.text,
                ),
                "cer": character_error_rate(
                    item["reference_transcript"],
                    result.text,
                ),
                "field_exact_match": field_exact_match(
                    reference_form,
                    predicted_form,
                ),
                "complete_form_accuracy": complete_form_accuracy(
                    reference_form,
                    predicted_form,
                ),
                "latency_seconds": result.latency_seconds,
            }
        )

    n = len(results)
    if not n:
        raise ValueError("Benchmark manifest is empty")
    summary = {
        "backend": results[0]["backend"],
        "n": n,
        "mean_wer": sum(float(row["wer"]) for row in results) / n,
        "mean_cer": sum(float(row["cer"]) for row in results) / n,
        "mean_field_exact_match": (
            sum(float(row["field_exact_match"]) for row in results) / n
        ),
        "complete_form_accuracy": (
            sum(float(row["complete_form_accuracy"]) for row in results) / n
        ),
        "mean_latency_seconds": _mean_latency(results),
    }
    return {"summary": summary, "items": results}


def _mean_latency(rows: list[dict[str, object]]) -> float | None:
    values = [
        float(row["latency_seconds"])
        for row in rows
        if row["latency_seconds"] is not None
    ]
    return sum(values) / len(values) if values else None


def run_manifest(manifest: Path, backend) -> dict[str, object]:
    """Validate a manifest and benchmark it against one backend."""
    rows = load_validated_manifest(manifest, check_audio=True)
    return run_rows(rows, backend)

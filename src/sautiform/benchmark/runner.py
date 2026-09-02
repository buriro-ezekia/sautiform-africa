"""Benchmark runner for ASR plus downstream form extraction."""
from __future__ import annotations

import json
from pathlib import Path

from sautiform.benchmark.metrics import (
    character_error_rate,
    complete_form_accuracy,
    field_exact_match,
    word_error_rate,
)
from sautiform.forms.extraction import extract_form
from sautiform.forms.public_service import PublicServiceForm


def run_manifest(manifest: Path, backend) -> dict[str, object]:
    rows = []
    with manifest.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            item = json.loads(line)
            result = backend.transcribe(Path(item["audio_path"]))
            reference_form = PublicServiceForm(**item["reference_fields"])
            predicted_form = extract_form(result.text)
            rows.append(
                {
                    "audio_path": item["audio_path"],
                    "backend": result.backend,
                    "transcript": result.text,
                    "wer": word_error_rate(item["reference_transcript"], result.text),
                    "cer": character_error_rate(item["reference_transcript"], result.text),
                    "field_exact_match": field_exact_match(reference_form, predicted_form),
                    "complete_form_accuracy": complete_form_accuracy(
                        reference_form,
                        predicted_form,
                    ),
                    "latency_seconds": result.latency_seconds,
                }
            )
    n = len(rows)
    if not n:
        raise ValueError("Benchmark manifest is empty")
    summary = {
        "backend": rows[0]["backend"],
        "n": n,
        "mean_wer": sum(row["wer"] for row in rows) / n,
        "mean_cer": sum(row["cer"] for row in rows) / n,
        "mean_field_exact_match": sum(row["field_exact_match"] for row in rows) / n,
        "complete_form_accuracy": sum(row["complete_form_accuracy"] for row in rows) / n,
    }
    return {"summary": summary, "items": rows}

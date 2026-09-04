"""Validation for consent-aware benchmark manifests."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sautiform.audio import validate_audio_path
from sautiform.forms.public_service import PublicServiceForm

REQUIRED_METADATA = (
    "language_pair",
    "country",
    "device",
    "noise",
    "consented",
)


def validate_manifest_item(
    item: dict[str, Any],
    *,
    check_audio: bool = True,
) -> list[str]:
    """Return deterministic validation errors for one benchmark row."""
    errors: list[str] = []
    required_keys = (
        "sample_id",
        "audio_path",
        "reference_transcript",
        "reference_fields",
        "metadata",
    )
    for key in required_keys:
        if key not in item:
            errors.append(f"missing required key: {key}")

    fields = item.get("reference_fields")
    if isinstance(fields, dict):
        try:
            form = PublicServiceForm(**fields)
        except TypeError as exc:
            errors.append(f"invalid reference_fields: {exc}")
        else:
            errors.extend(form.validate())
            for missing in form.missing_fields():
                errors.append(f"reference_fields missing value: {missing}")
    elif "reference_fields" in item:
        errors.append("reference_fields must be an object")

    metadata = item.get("metadata")
    if isinstance(metadata, dict):
        for key in REQUIRED_METADATA:
            if key not in metadata:
                errors.append(f"metadata missing value: {key}")
        if metadata.get("consented") is not True:
            errors.append("metadata.consented must be true")
    elif "metadata" in item:
        errors.append("metadata must be an object")

    audio_path = item.get("audio_path")
    if check_audio and isinstance(audio_path, str):
        try:
            validate_audio_path(Path(audio_path))
        except (FileNotFoundError, ValueError) as exc:
            errors.append(str(exc))
    return errors


def load_validated_manifest(
    path: Path,
    *,
    check_audio: bool = True,
) -> list[dict[str, Any]]:
    """Load JSONL and fail with row-specific messages before benchmarking."""
    rows: list[dict[str, Any]] = []
    sample_ids: set[str] = set()
    problems: list[str] = []

    with Path(path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                problems.append(
                    f"line {line_number}: invalid JSON: {exc.msg}"
                )
                continue
            if not isinstance(item, dict):
                problems.append(f"line {line_number}: row must be a JSON object")
                continue

            row_errors = validate_manifest_item(item, check_audio=check_audio)
            sample_id = item.get("sample_id")
            if isinstance(sample_id, str):
                if sample_id in sample_ids:
                    row_errors.append(f"duplicate sample_id: {sample_id}")
                sample_ids.add(sample_id)
            for error in row_errors:
                problems.append(f"line {line_number}: {error}")
            rows.append(item)

    if not rows:
        problems.append("manifest contains no benchmark rows")
    if problems:
        raise ValueError("Invalid benchmark manifest:\n" + "\n".join(problems))
    return rows

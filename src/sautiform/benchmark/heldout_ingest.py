"""Batch ingestion helpers for the fixed held-out benchmark."""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

from sautiform.audio import ALLOWED_AUDIO_SUFFIXES, validate_audio_path
from sautiform.benchmark.heldout import EXPECTED_HELDOUT_IDS

DEFAULT_PLAN = Path("examples/heldout_plan.jsonl")
DEFAULT_HELDOUT_ROOT = Path("data/private/heldout")


def load_heldout_plan(path: Path = DEFAULT_PLAN) -> list[dict[str, Any]]:
    """Load and validate the fixed machine-readable held-out plan."""
    rows: list[dict[str, Any]] = []
    with Path(path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"held-out plan line {line_number} is invalid JSON: {exc.msg}"
                ) from exc
            rows.append(row)

    ids = [str(row.get("sample_id", "")) for row in rows]
    if tuple(ids) != EXPECTED_HELDOUT_IDS:
        raise ValueError(
            "held-out plan IDs/order do not match tz-sw-en-h001 through tz-sw-en-h024"
        )

    required = {
        "sample_id",
        "reference_transcript",
        "reference_fields",
        "recording_cell",
    }
    for index, row in enumerate(rows, start=1):
        missing = sorted(required - set(row))
        if missing:
            raise ValueError(
                f"held-out plan row {index} missing: {', '.join(missing)}"
            )
    return rows


def resolve_source_audio(source_dir: Path, sample_id: str) -> Path:
    """Resolve exactly one supported source recording by exact filename stem."""
    source_dir = Path(source_dir)
    matches = [
        path
        for path in source_dir.iterdir()
        if path.is_file()
        and path.stem == sample_id
        and path.suffix.lower() in ALLOWED_AUDIO_SUFFIXES
    ]
    if not matches:
        raise ValueError(f"no supported audio found for {sample_id}")
    if len(matches) > 1:
        raise ValueError(f"multiple supported audio files found for {sample_id}")
    return validate_audio_path(matches[0])


def probe_duration_seconds(audio_path: Path) -> float | None:
    """Return ffprobe duration when available, otherwise None."""
    ffprobe = shutil.which("ffprobe")
    if ffprobe is None:
        return None
    completed = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(completed.stdout.strip())

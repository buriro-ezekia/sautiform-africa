"""Integrity checks for the fixed 24-row held-out benchmark."""
from __future__ import annotations

from pathlib import Path
from typing import Any

EXPECTED_HELDOUT_IDS = tuple(f"tz-sw-en-h{i:03d}" for i in range(1, 25))
_DEVELOPMENT_IDS = {f"tz-sw-en-{i:03d}" for i in range(1, 11)}
_HELDOUT_ROOT = Path("data/private/heldout")


def validate_heldout_rows(rows: list[dict[str, Any]]) -> list[str]:
    """Return integrity errors for the fixed final held-out design."""
    errors: list[str] = []
    sample_ids = [str(row.get("sample_id", "")) for row in rows]

    if len(rows) != 24:
        errors.append(f"held-out manifest must contain exactly 24 rows; found {len(rows)}")

    if set(sample_ids) != set(EXPECTED_HELDOUT_IDS):
        missing = sorted(set(EXPECTED_HELDOUT_IDS) - set(sample_ids))
        unexpected = sorted(set(sample_ids) - set(EXPECTED_HELDOUT_IDS))
        if missing:
            errors.append("missing held-out sample IDs: " + ", ".join(missing))
        if unexpected:
            errors.append("unexpected held-out sample IDs: " + ", ".join(unexpected))

    leaked = sorted(set(sample_ids) & _DEVELOPMENT_IDS)
    if leaked:
        errors.append("development sample IDs present: " + ", ".join(leaked))

    audio_paths: list[str] = []
    for row in rows:
        audio_path = str(row.get("audio_path", ""))
        audio_paths.append(audio_path)
        path = Path(audio_path)
        try:
            path.relative_to(_HELDOUT_ROOT / "audio")
        except ValueError:
            errors.append(
                f"{row.get('sample_id', '<unknown>')}: audio_path must be under "
                "data/private/heldout/audio"
            )

    if len(audio_paths) != len(set(audio_paths)):
        errors.append("held-out manifest contains duplicate audio paths")

    return errors

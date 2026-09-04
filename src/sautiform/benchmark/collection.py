"""Private benchmark workspace and consent-aware sample ingestion."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from sautiform.audio import validate_audio_path
from sautiform.benchmark.manifest import validate_manifest_item
from sautiform.forms.public_service import PublicServiceForm

DEFAULT_PRIVATE_ROOT = Path("data/private")
_SAMPLE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{2,63}$")


def initialise_private_workspace(
    root: Path = DEFAULT_PRIVATE_ROOT,
) -> tuple[Path, Path]:
    """Create the ignored local audio directory and manifest file."""
    root = Path(root)
    audio_dir = root / "audio"
    manifest = root / "benchmark_manifest.jsonl"
    audio_dir.mkdir(parents=True, exist_ok=True)
    manifest.touch(exist_ok=True)
    return audio_dir, manifest


def _existing_sample_ids(manifest: Path) -> set[str]:
    sample_ids: set[str] = set()
    if not manifest.exists():
        return sample_ids

    with manifest.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Existing manifest line {line_number} is invalid JSON: {exc.msg}"
                ) from exc
            sample_id = item.get("sample_id")
            if isinstance(sample_id, str):
                sample_ids.add(sample_id)
    return sample_ids


def add_benchmark_sample(
    *,
    source_audio: Path,
    sample_id: str,
    reference_transcript: str,
    form: PublicServiceForm,
    device: str,
    noise: str,
    consented: bool,
    country: str = "Tanzania",
    language_pair: str = "sw-en",
    root: Path = DEFAULT_PRIVATE_ROOT,
) -> dict[str, object]:
    """Copy one approved clip into the private workspace and append its manifest row."""
    if not _SAMPLE_ID_PATTERN.fullmatch(sample_id):
        raise ValueError(
            "sample_id must contain 3-64 lowercase letters, digits or hyphens"
        )
    if not consented:
        raise ValueError("Explicit consent is required before adding benchmark audio")
    if not reference_transcript.strip():
        raise ValueError("reference_transcript must not be empty")
    if form.missing_fields():
        raise ValueError(
            "reference form is incomplete: " + ", ".join(form.missing_fields())
        )
    errors = form.validate()
    if errors:
        raise ValueError("invalid reference form: " + "; ".join(errors))
    if not device.strip() or not noise.strip():
        raise ValueError("device and noise metadata must not be empty")

    source_audio = validate_audio_path(Path(source_audio))
    audio_dir, manifest = initialise_private_workspace(Path(root))
    if sample_id in _existing_sample_ids(manifest):
        raise ValueError(f"duplicate sample_id: {sample_id}")

    destination = audio_dir / f"{sample_id}{source_audio.suffix.lower()}"
    if destination.exists():
        raise ValueError(f"private audio destination already exists: {destination}")

    shutil.copy2(source_audio, destination)
    row: dict[str, object] = {
        "sample_id": sample_id,
        "audio_path": destination.as_posix(),
        "reference_transcript": reference_transcript.strip(),
        "reference_fields": form.to_dict(),
        "metadata": {
            "language_pair": language_pair,
            "country": country,
            "device": device.strip(),
            "noise": noise.strip(),
            "consented": True,
        },
    }

    row_errors = validate_manifest_item(row, check_audio=True)
    if row_errors:
        destination.unlink(missing_ok=True)
        raise ValueError("invalid benchmark sample: " + "; ".join(row_errors))

    with manifest.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row

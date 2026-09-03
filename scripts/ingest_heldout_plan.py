"""Batch-ingest the fixed 24-clip held-out benchmark without ASR inference."""
from __future__ import annotations

import argparse
from pathlib import Path

from sautiform.benchmark.collection import add_benchmark_sample
from sautiform.benchmark.heldout import validate_heldout_rows
from sautiform.benchmark.heldout_ingest import (
    DEFAULT_HELDOUT_ROOT,
    DEFAULT_PLAN,
    load_heldout_plan,
    probe_duration_seconds,
    resolve_source_audio,
)
from sautiform.benchmark.manifest import load_validated_manifest
from sautiform.forms.public_service import PublicServiceForm


def _device_for(cell: str, device_a: str, device_b: str) -> str:
    return device_a if cell.startswith("a_") else device_b


def _noise_for(cell: str) -> str:
    return (
        "quiet room"
        if cell.endswith("_quiet")
        else "moderate realistic background noise"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--device-a", required=True)
    parser.add_argument("--device-b", required=True)
    parser.add_argument(
        "--confirm-recordings-match-plan",
        action="store_true",
        help=(
            "Assert that each recording was listened to and matches its fixed reference "
            "transcript and structured meaning."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preflight all 24 recordings without copying or writing the manifest.",
    )
    args = parser.parse_args()

    if not args.source_dir.is_dir():
        raise SystemExit(f"SOURCE_DIR_NOT_FOUND={args.source_dir}")

    rows = load_heldout_plan(args.plan)
    resolved: list[tuple[dict[str, object], Path, float | None]] = []
    for row in rows:
        sample_id = str(row["sample_id"])
        audio = resolve_source_audio(args.source_dir, sample_id)
        duration = probe_duration_seconds(audio)
        if duration is not None and duration > 40:
            raise SystemExit(
                f"HELDOUT_AUDIO_TOO_LONG={sample_id} duration={duration:.3f}s"
            )
        resolved.append((row, audio, duration))

    print("HELDOUT_SOURCE_PREFLIGHT=PASS")
    print(f"HELDOUT_SOURCE_ROWS={len(resolved)}")
    for row, audio, duration in resolved:
        duration_text = "unavailable" if duration is None else f"{duration:.3f}"
        print(
            f"SOURCE_OK={row['sample_id']} file={audio.name} "
            f"duration_seconds={duration_text}"
        )

    if args.dry_run:
        print("HELDOUT_DRY_RUN=PASS")
        return

    if not args.confirm_recordings_match_plan:
        raise SystemExit(
            "HELDOUT_CONFIRMATION_REQUIRED=YES "
            "rerun with --confirm-recordings-match-plan after listening to all clips"
        )

    root = DEFAULT_HELDOUT_ROOT
    manifest = root / "benchmark_manifest.jsonl"
    audio_dir = root / "audio"
    if manifest.exists() and manifest.read_text(encoding="utf-8").strip():
        raise SystemExit(f"HELDOUT_TARGET_NOT_EMPTY={manifest}")
    if audio_dir.exists() and any(audio_dir.iterdir()):
        raise SystemExit(f"HELDOUT_AUDIO_TARGET_NOT_EMPTY={audio_dir}")

    for row, audio, _duration in resolved:
        fields = row["reference_fields"]
        add_benchmark_sample(
            source_audio=audio,
            sample_id=str(row["sample_id"]),
            reference_transcript=str(row["reference_transcript"]),
            form=PublicServiceForm(**fields),
            device=_device_for(
                str(row["recording_cell"]),
                args.device_a,
                args.device_b,
            ),
            noise=_noise_for(str(row["recording_cell"])),
            consented=True,
            root=root,
        )

    manifest_rows = load_validated_manifest(manifest, check_audio=True)
    errors = validate_heldout_rows(manifest_rows)
    if errors:
        for error in errors:
            print(f"HELDOUT_ERROR={error}")
        raise SystemExit(1)

    print("HELDOUT_BATCH_INGEST=PASS")
    print(f"HELDOUT_MANIFEST={manifest.as_posix()}")
    print(f"HELDOUT_MANIFEST_ROWS={len(manifest_rows)}")
    print("HELDOUT_READY_FOR_VALIDATION=YES")
    print("ASR_INFERENCE_PERFORMED=NO")


if __name__ == "__main__":
    main()

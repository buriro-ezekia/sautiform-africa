"""Run a benchmark manifest against one configured ASR backend."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from sautiform.asr.base import TranscriptResult
from sautiform.asr.factory import SUPPORTED_BACKENDS, build_backend
from sautiform.benchmark.integrity import verify_sha256
from sautiform.benchmark.runner import run_manifest


class MockBackend:
    """Deterministic local backend that reads transcript sidecars."""

    name = "mock"

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        sidecar = audio_path.with_suffix(audio_path.suffix + ".txt")
        return TranscriptResult(
            sidecar.read_text(encoding="utf-8").strip(),
            self.name,
            0.0,
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--backend",
        choices=(*SUPPORTED_BACKENDS, "mock"),
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--expected-manifest-sha256",
        help=(
            "Fail before model loading if the manifest does not match this "
            "frozen SHA-256 digest."
        ),
    )
    args = parser.parse_args()

    if args.expected_manifest_sha256:
        digest = verify_sha256(args.manifest, args.expected_manifest_sha256)
        print(f"MANIFEST_SHA256_VERIFIED={digest}")

    backend = (
        MockBackend()
        if args.backend == "mock"
        else build_backend(args.backend)
    )
    report = run_manifest(args.manifest, backend)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()

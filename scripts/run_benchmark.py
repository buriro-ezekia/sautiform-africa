"""Run a benchmark manifest against one configured ASR backend."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from sautiform.asr.base import TranscriptResult
from sautiform.asr.factory import build_backend
from sautiform.benchmark.runner import run_manifest


class MockBackend:
    name = "mock"

    def transcribe(self, audio_path: Path) -> TranscriptResult:
        sidecar = audio_path.with_suffix(audio_path.suffix + ".txt")
        return TranscriptResult(sidecar.read_text(encoding="utf-8").strip(), self.name, 0.0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--backend", choices=["sahara", "whisper", "mms", "http", "mock"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    backend = MockBackend() if args.backend == "mock" else build_backend(args.backend)
    report = run_manifest(args.manifest, backend)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))


if __name__ == "__main__":
    main()
